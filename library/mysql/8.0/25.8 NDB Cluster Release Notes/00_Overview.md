---
source: MySQL 8.0 Reference
title: 00_Overview
---

Changes in NDB Cluster releases are documented separately from this reference manual; you can find release notes for the changes in each NDB Cluster 8.0 release at [NDB 8.0 Release Notes](https://dev.mysql.com/doc/relnotes/mysql-cluster/8.0/en/).

You can obtain release notes for older versions of NDB Cluster from [NDB Cluster Release Notes.](https://dev.mysql.com/doc/index-cluster.md#cluster-relnotes)

# Chapter 26 Partitioning

# **Table of Contents**

| 26.1 Overview of Partitioning in MySQL 4858                      |      |
|------------------------------------------------------------------|------|
| 26.2 Partitioning Types 4860                                     |      |
| 26.2.1 RANGE Partitioning 4862                                   |      |
| 26.2.2 LIST Partitioning 4866                                    |      |
| 26.2.3 COLUMNS Partitioning                                      | 4869 |
| 26.2.4 HASH Partitioning 4876                                    |      |
| 26.2.5 KEY Partitioning 4879                                     |      |
| 26.2.6 Subpartitioning 4880                                      |      |
| 26.2.7 How MySQL Partitioning Handles NULL 4882                  |      |
| 26.3 Partition Management 4886                                   |      |
| 26.3.1 Management of RANGE and LIST Partitions 4887              |      |
| 26.3.2 Management of HASH and KEY Partitions 4893                |      |
| 26.3.3 Exchanging Partitions and Subpartitions with Tables       | 4894 |
| 26.3.4 Maintenance of Partitions 4901                            |      |
| 26.3.5 Obtaining Information About Partitions 4902               |      |
| 26.4 Partition Pruning 4904                                      |      |
| 26.5 Partition Selection 4907                                    |      |
| 26.6 Restrictions and Limitations on Partitioning 4913           |      |
| 26.6.1 Partitioning Keys, Primary Keys, and Unique Keys 4919     |      |
| 26.6.2 Partitioning Limitations Relating to Storage Engines 4922 |      |
| 26.6.3 Partitioning Limitations Relating to Functions 4923       |      |
|                                                                  |      |

This chapter discusses user-defined partitioning.

![](_page_86_Picture_4.jpeg)

#### **Note**

Table partitioning differs from partitioning as used by window functions. For information about window functions, see Section 14.20, "Window Functions".

In MySQL 8.0, partitioning support is provided by the InnoDB and NDB storage engines.

MySQL 8.0 does not currently support partitioning of tables using any storage engine other than InnoDB or NDB, such as MyISAM. An attempt to create a partitioned tables using a storage engine that does not supply native partitioning support fails with [ER\\_CHECK\\_NOT\\_IMPLEMENTED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_check_not_implemented).

If you are compiling MySQL 8.0 from source, configuring the build with InnoDB support is sufficient to produce binaries with partition support for InnoDB tables. For more information, see Section 2.8, "Installing MySQL from Source".

Nothing further needs to be done to enable partitioning support by InnoDB (for example, no special entries are required in the my.cnf file).

It is not possible to disable partitioning support by the InnoDB storage engine.

See [Section 26.1, "Overview of Partitioning in MySQL",](#page-87-0) for an introduction to partitioning and partitioning concepts.

Several types of partitioning are supported, as well as subpartitioning; see [Section 26.2, "Partitioning](#page-89-0) [Types",](#page-89-0) and [Section 26.2.6, "Subpartitioning"](#page-109-0).

[Section 26.3, "Partition Management",](#page-115-0) covers methods of adding, removing, and altering partitions in existing partitioned tables.

[Section 26.3.4, "Maintenance of Partitions",](#page-130-0) discusses table maintenance commands for use with partitioned tables.

The PARTITIONS table in the INFORMATION\_SCHEMA database provides information about partitions and partitioned tables. See Section 28.3.21, "The INFORMATION\_SCHEMA PARTITIONS Table", for more information; for some examples of queries against this table, see [Section 26.2.7, "How MySQL](#page-111-0) [Partitioning Handles NULL"](#page-111-0).

For known issues with partitioning in MySQL 8.0, see [Section 26.6, "Restrictions and Limitations on](#page-142-0) [Partitioning"](#page-142-0).

You may also find the following resources to be useful when working with partitioned tables.

**Additional Resources.** Other sources of information about user-defined partitioning in MySQL include the following:

#### • [MySQL Partitioning Forum](https://forums.mysql.com/list.php?106)

This is the official discussion forum for those interested in or experimenting with MySQL Partitioning technology. It features announcements and updates from MySQL developers and others. It is monitored by members of the Partitioning Development and Documentation Teams.

#### • [PlanetMySQL](http://www.planetmysql.org/)

A MySQL news site featuring MySQL-related blogs, which should be of interest to anyone using my MySQL. We encourage you to check here for links to blogs kept by those working with MySQL Partitioning, or to have your own blog added to those covered.

# <span id="page-87-0"></span>**26.1 Overview of Partitioning in MySQL**

This section provides a conceptual overview of partitioning in MySQL 8.0.

For information on partitioning restrictions and feature limitations, see [Section 26.6, "Restrictions and](#page-142-0) [Limitations on Partitioning".](#page-142-0)

The SQL standard does not provide much in the way of guidance regarding the physical aspects of data storage. The SQL language itself is intended to work independently of any data structures or media underlying the schemas, tables, rows, or columns with which it works. Nonetheless, most advanced database management systems have evolved some means of determining the physical location to be used for storing specific pieces of data in terms of the file system, hardware or even both. In MySQL, the InnoDB storage engine has long supported the notion of a tablespace (see Section 17.6.3, "Tablespaces"), and the MySQL Server, even prior to the introduction of partitioning, could be configured to employ different physical directories for storing different databases (see Section 10.12.2, "Using Symbolic Links", for an explanation of how this is done).

Partitioning takes this notion a step further, by enabling you to distribute portions of individual tables across a file system according to rules which you can set largely as needed. In effect, different portions of a table are stored as separate tables in different locations. The user-selected rule by which the division of data is accomplished is known as a partitioning function, which in MySQL can be the modulus, simple matching against a set of ranges or value lists, an internal hashing function, or a linear hashing function. The function is selected according to the partitioning type specified by the user, and takes as its parameter the value of a user-supplied expression. This expression can be a column value, a function acting on one or more column values, or a set of one or more column values, depending on the type of partitioning that is used.

In the case of RANGE, LIST, and [LINEAR] HASH partitioning, the value of the partitioning column is passed to the partitioning function, which returns an integer value representing the number of the partition in which that particular record should be stored. This function must be nonconstant and nonrandom. It may not contain any queries, but may use an SQL expression that is valid in MySQL, as long as that expression returns either NULL or an integer intval such that

```
-MAXVALUE <= intval <= MAXVALUE
```

(MAXVALUE is used to represent the least upper bound for the type of integer in question. -MAXVALUE represents the greatest lower bound.)

For [LINEAR] KEY, RANGE COLUMNS, and LIST COLUMNS partitioning, the partitioning expression consists of a list of one or more columns.

For [LINEAR] KEY partitioning, the partitioning function is supplied by MySQL.

For more information about permitted partitioning column types and partitioning functions, see [Section 26.2, "Partitioning Types",](#page-89-0) as well as Section 15.1.20, "CREATE TABLE Statement", which provides partitioning syntax descriptions and additional examples. For information about restrictions on partitioning functions, see [Section 26.6.3, "Partitioning Limitations Relating to Functions".](#page-152-0)

This is known as horizontal partitioning—that is, different rows of a table may be assigned to different physical partitions. MySQL 8.0 does not support vertical partitioning, in which different columns of a table are assigned to different physical partitions. There are no plans at this time to introduce vertical partitioning into MySQL.

For creating partitioned tables, you must use a storage engine that supports them. In MySQL 8.0, all partitions of the same partitioned table must use the same storage engine. However, there is nothing preventing you from using different storage engines for different partitioned tables on the same MySQL server or even in the same database.

In MySQL 8.0, the only storage engines that support partitioning are InnoDB and NDB. Partitioning cannot be used with storage engines that do not support it; these include the MyISAM, MERGE, CSV, and FEDERATED storage engines.

Partitioning by KEY or LINEAR KEY is possible with NDB, but other types of user-defined partitioning are not supported for tables using this storage engine. In addition, an NDB table that employs userdefined partitioning must have an explicit primary key, and any columns referenced in the table's partitioning expression must be part of the primary key. However, if no columns are listed in the PARTITION BY KEY or PARTITION BY LINEAR KEY clause of the CREATE TABLE or ALTER TABLE statement used to create or modify a user-partitioned NDB table, then the table is not required to have an explicit primary key. For more information, see Section 25.2.7.1, "Noncompliance with SQL Syntax in NDB Cluster".

When creating a partitioned table, the default storage engine is used just as when creating any other table; to override this behavior, it is necessary only to use the [STORAGE] ENGINE option just as you would for a table that is not partitioned. The target storage engine must provide native partitioning support, or the statement fails. You should keep in mind that [STORAGE] ENGINE (and other table options) need to be listed before any partitioning options are used in a CREATE TABLE statement. This example shows how to create a table that is partitioned by hash into 6 partitions and which uses the InnoDB storage engine (regardless of the value of default\_storage\_engine):

```
CREATE TABLE ti (id INT, amount DECIMAL(7,2), tr_date DATE)
 ENGINE=INNODB
 PARTITION BY HASH( MONTH(tr_date) )
 PARTITIONS 6;
```

Each PARTITION clause can include a [STORAGE] ENGINE option, but in MySQL 8.0 this has no effect.

Unless otherwise specified, the remaining examples in this discussion assume that default\_storage\_engine is InnoDB.

![](_page_88_Picture_14.jpeg)

#### **Important**

Partitioning applies to all data and indexes of a table; you cannot partition only the data and not the indexes, or vice versa, nor can you partition only a portion of the table.

Data and indexes for each partition can be assigned to a specific directory using the DATA DIRECTORY and INDEX DIRECTORY options for the PARTITION clause of the CREATE TABLE statement used to create the partitioned table.

Only the DATA DIRECTORY option is supported for individual partitions and subpartitions of InnoDB tables. As of MySQL 8.0.21, the directory specified in a DATA DIRECTORY clause must be known to InnoDB. For more information, see Using the DATA DIRECTORY Clause.

All columns used in the table's partitioning expression must be part of every unique key that the table may have, including any primary key. This means that a table such as this one, created by the following SQL statement, cannot be partitioned:

```
CREATE TABLE tnp (
 id INT NOT NULL AUTO_INCREMENT,
 ref BIGINT NOT NULL,
 name VARCHAR(255),
 PRIMARY KEY pk (id),
 UNIQUE KEY uk (name)
);
```

Because the keys pk and uk have no columns in common, there are no columns available for use in a partitioning expression. Possible workarounds in this situation include adding the name column to the table's primary key, adding the id column to uk, or simply removing the unique key altogether. See [Section 26.6.1, "Partitioning Keys, Primary Keys, and Unique Keys",](#page-148-0) for more information.

In addition, MAX\_ROWS and MIN\_ROWS can be used to determine the maximum and minimum numbers of rows, respectively, that can be stored in each partition. See [Section 26.3, "Partition Management"](#page-115-0), for more information on these options.

The MAX\_ROWS option can also be useful for creating NDB Cluster tables with extra partitions, thus allowing for greater storage of hash indexes. See the documentation for the DataMemory data node configuration parameter, as well as Section 25.2.2, "NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions", for more information.

Some advantages of partitioning are listed here:

- Partitioning makes it possible to store more data in one table than can be held on a single disk or file system partition.
- Data that loses its usefulness can often be easily removed from a partitioned table by dropping the partition (or partitions) containing only that data. Conversely, the process of adding new data can in some cases be greatly facilitated by adding one or more new partitions for storing specifically that data.
- Some queries can be greatly optimized in virtue of the fact that data satisfying a given WHERE clause can be stored only on one or more partitions, which automatically excludes any remaining partitions from the search. Because partitions can be altered after a partitioned table has been created, you can reorganize your data to enhance frequent queries that may not have been often used when the partitioning scheme was first set up. This ability to exclude non-matching partitions (and thus any rows they contain) is often referred to as partition pruning. For more information, see [Section 26.4,](#page-133-0) ["Partition Pruning".](#page-133-0)

In addition, MySQL supports explicit partition selection for queries. For example, SELECT \* FROM t PARTITION (p0,p1) WHERE c < 5 selects only those rows in partitions p0 and p1 that match the WHERE condition. In this case, MySQL does not check any other partitions of table t; this can greatly speed up queries when you already know which partition or partitions you wish to examine. Partition selection is also supported for the data modification statements DELETE, INSERT, REPLACE, UPDATE, and LOAD DATA, LOAD XML. See the descriptions of these statements for more information and examples.

# <span id="page-89-0"></span>**26.2 Partitioning Types**

This section discusses the types of partitioning which are available in MySQL 8.0. These include the types listed here:

- **RANGE partitioning.** This type of partitioning assigns rows to partitions based on column values falling within a given range. See [Section 26.2.1, "RANGE Partitioning"](#page-91-0). For information about an extension to this type, RANGE COLUMNS, see [Section 26.2.3.1, "RANGE COLUMNS partitioning"](#page-98-1).
- **LIST partitioning.** Similar to partitioning by RANGE, except that the partition is selected based on columns matching one of a set of discrete values. See [Section 26.2.2, "LIST Partitioning"](#page-95-0). For information about an extension to this type, LIST COLUMNS, see [Section 26.2.3.2, "LIST COLUMNS](#page-103-0) [partitioning"](#page-103-0).
- **HASH partitioning.** With this type of partitioning, a partition is selected based on the value returned by a user-defined expression that operates on column values in rows to be inserted into the table. The function may consist of any expression valid in MySQL that yields an integer value. See [Section 26.2.4, "HASH Partitioning".](#page-105-0)

An extension to this type, LINEAR HASH, is also available, see [Section 26.2.4.1, "LINEAR HASH](#page-107-0) [Partitioning"](#page-107-0).

• **KEY partitioning.** This type of partitioning is similar to partitioning by HASH, except that only one or more columns to be evaluated are supplied, and the MySQL server provides its own hashing function. These columns can contain other than integer values, since the hashing function supplied by MySQL guarantees an integer result regardless of the column data type. An extension to this type, LINEAR KEY, is also available. See [Section 26.2.5, "KEY Partitioning".](#page-108-0)

A very common use of database partitioning is to segregate data by date. Some database systems support explicit date partitioning, which MySQL does not implement in 8.0. However, it is not difficult in MySQL to create partitioning schemes based on DATE, TIME, or DATETIME columns, or based on expressions making use of such columns.

When partitioning by KEY or LINEAR KEY, you can use a DATE, TIME, or DATETIME column as the partitioning column without performing any modification of the column value. For example, this table creation statement is perfectly valid in MySQL:

```
CREATE TABLE members (
 firstname VARCHAR(25) NOT NULL,
 lastname VARCHAR(25) NOT NULL,
 username VARCHAR(16) NOT NULL,
 email VARCHAR(35),
 joined DATE NOT NULL
)
PARTITION BY KEY(joined)
PARTITIONS 6;
```

In MySQL 8.0, it is also possible to use a DATE or DATETIME column as the partitioning column using RANGE COLUMNS and LIST COLUMNS partitioning.

Other partitioning types require a partitioning expression that yields an integer value or NULL. If you wish to use date-based partitioning by RANGE, LIST, HASH, or LINEAR HASH, you can simply employ a function that operates on a DATE, TIME, or DATETIME column and returns such a value, as shown here:

```
CREATE TABLE members (
 firstname VARCHAR(25) NOT NULL,
 lastname VARCHAR(25) NOT NULL,
 username VARCHAR(16) NOT NULL,
 email VARCHAR(35),
 joined DATE NOT NULL
)
PARTITION BY RANGE( YEAR(joined) ) (
 PARTITION p0 VALUES LESS THAN (1960),
 PARTITION p1 VALUES LESS THAN (1970),
```

```
 PARTITION p2 VALUES LESS THAN (1980),
 PARTITION p3 VALUES LESS THAN (1990),
 PARTITION p4 VALUES LESS THAN MAXVALUE
);
```

Additional examples of partitioning using dates may be found in the following sections of this chapter:

- [Section 26.2.1, "RANGE Partitioning"](#page-91-0)
- [Section 26.2.4, "HASH Partitioning"](#page-105-0)
- [Section 26.2.4.1, "LINEAR HASH Partitioning"](#page-107-0)

For more complex examples of date-based partitioning, see the following sections:

- [Section 26.4, "Partition Pruning"](#page-133-0)
- [Section 26.2.6, "Subpartitioning"](#page-109-0)

MySQL partitioning is optimized for use with the TO\_DAYS(), YEAR(), and TO\_SECONDS() functions. However, you can use other date and time functions that return an integer or NULL, such as WEEKDAY(), DAYOFYEAR(), or MONTH(). See Section 14.7, "Date and Time Functions", for more information about such functions.

It is important to remember—regardless of the type of partitioning that you use—that partitions are always numbered automatically and in sequence when created, starting with 0. When a new row is inserted into a partitioned table, it is these partition numbers that are used in identifying the correct partition. For example, if your table uses 4 partitions, these partitions are numbered 0, 1, 2, and 3. For the RANGE and LIST partitioning types, it is necessary to ensure that there is a partition defined for each partition number. For HASH partitioning, the user-supplied expression must evaluate to an integer value. For KEY partitioning, this issue is taken care of automatically by the hashing function which the MySQL server employs internally.

Names of partitions generally follow the rules governing other MySQL identifiers, such as those for tables and databases. However, you should note that partition names are not case-sensitive. For example, the following CREATE TABLE statement fails as shown:

```
mysql> CREATE TABLE t2 (val INT)
 -> PARTITION BY LIST(val)(
 -> PARTITION mypart VALUES IN (1,3,5),
 -> PARTITION MyPart VALUES IN (2,4,6)
 -> );
ERROR 1488 (HY000): Duplicate partition name mypart
```

Failure occurs because MySQL sees no difference between the partition names mypart and MyPart.

When you specify the number of partitions for the table, this must be expressed as a positive, nonzero integer literal with no leading zeros, and may not be an expression such as 0.8E+01 or 6-2, even if it evaluates to an integer value. Decimal fractions are not permitted.

In the sections that follow, we do not necessarily provide all possible forms for the syntax that can be used for creating each partition type; for this information, see Section 15.1.20, "CREATE TABLE Statement".

# <span id="page-91-0"></span>**26.2.1 RANGE Partitioning**

A table that is partitioned by range is partitioned in such a way that each partition contains rows for which the partitioning expression value lies within a given range. Ranges should be contiguous but not overlapping, and are defined using the VALUES LESS THAN operator. For the next few examples, suppose that you are creating a table such as the following to hold personnel records for a chain of 20 video stores, numbered 1 through 20:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
);
```

![](_page_92_Picture_2.jpeg)

#### **Note**

The employees table used here has no primary or unique keys. While the examples work as shown for purposes of the present discussion, you should keep in mind that tables are extremely likely in practice to have primary keys, unique keys, or both, and that allowable choices for partitioning columns depend on the columns used for these keys, if any are present. For a discussion of these issues, see [Section 26.6.1, "Partitioning Keys, Primary Keys, and](#page-148-0) [Unique Keys"](#page-148-0).

This table can be partitioned by range in a number of ways, depending on your needs. One way would be to use the store\_id column. For instance, you might decide to partition the table 4 ways by adding a PARTITION BY RANGE clause as shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
)
PARTITION BY RANGE (store_id) (
 PARTITION p0 VALUES LESS THAN (6),
 PARTITION p1 VALUES LESS THAN (11),
 PARTITION p2 VALUES LESS THAN (16),
 PARTITION p3 VALUES LESS THAN (21)
);
```

In this partitioning scheme, all rows corresponding to employees working at stores 1 through 5 are stored in partition p0, to those employed at stores 6 through 10 are stored in partition p1, and so on. Each partition is defined in order, from lowest to highest. This is a requirement of the PARTITION BY RANGE syntax; you can think of it as being analogous to a series of if ... elseif ... statements in C or Java in this regard.

It is easy to determine that a new row containing the data (72, 'Mitchell', 'Wilson', '1998-06-25', DEFAULT, 7, 13) is inserted into partition p2, but what happens when your chain adds a 21st store? Under this scheme, there is no rule that covers a row whose store\_id is greater than 20, so an error results because the server does not know where to place it. You can keep this from occurring by using a "catchall" VALUES LESS THAN clause in the CREATE TABLE statement that provides for all values greater than the highest value explicitly named:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
)
PARTITION BY RANGE (store_id) (
 PARTITION p0 VALUES LESS THAN (6),
 PARTITION p1 VALUES LESS THAN (11),
 PARTITION p2 VALUES LESS THAN (16),
 PARTITION p3 VALUES LESS THAN MAXVALUE
```

);

(As with the other examples in this chapter, we assume that the default storage engine is InnoDB.)

Another way to avoid an error when no matching value is found is to use the IGNORE keyword as part of the INSERT statement. For an example, see [Section 26.2.2, "LIST Partitioning"](#page-95-0).

MAXVALUE represents an integer value that is always greater than the largest possible integer value (in mathematical language, it serves as a least upper bound). Now, any rows whose store\_id column value is greater than or equal to 16 (the highest value defined) are stored in partition p3. At some point in the future—when the number of stores has increased to 25, 30, or more—you can use an ALTER TABLE statement to add new partitions for stores 21-25, 26-30, and so on (see [Section 26.3, "Partition](#page-115-0) [Management",](#page-115-0) for details of how to do this).

In much the same fashion, you could partition the table based on employee job codes—that is, based on ranges of job\_code column values. For example—assuming that two-digit job codes are used for regular (in-store) workers, three-digit codes are used for office and support personnel, and four-digit codes are used for management positions—you could create the partitioned table using the following statement:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
)
PARTITION BY RANGE (job_code) (
 PARTITION p0 VALUES LESS THAN (100),
 PARTITION p1 VALUES LESS THAN (1000),
 PARTITION p2 VALUES LESS THAN (10000)
);
```

In this instance, all rows relating to in-store workers would be stored in partition p0, those relating to office and support staff in p1, and those relating to managers in partition p2.

It is also possible to use an expression in VALUES LESS THAN clauses. However, MySQL must be able to evaluate the expression's return value as part of a LESS THAN (<) comparison.

Rather than splitting up the table data according to store number, you can use an expression based on one of the two DATE columns instead. For example, let us suppose that you wish to partition based on the year that each employee left the company; that is, the value of YEAR(separated). An example of a CREATE TABLE statement that implements such a partitioning scheme is shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
)
PARTITION BY RANGE ( YEAR(separated) ) (
 PARTITION p0 VALUES LESS THAN (1991),
 PARTITION p1 VALUES LESS THAN (1996),
 PARTITION p2 VALUES LESS THAN (2001),
 PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

In this scheme, for all employees who left before 1991, the rows are stored in partition p0; for those who left in the years 1991 through 1995, in p1; for those who left in the years 1996 through 2000, in p2; and for any workers who left after the year 2000, in p3.

It is also possible to partition a table by RANGE, based on the value of a TIMESTAMP column, using the UNIX\_TIMESTAMP() function, as shown in this example:

```
CREATE TABLE quarterly_report_status (
 report_id INT NOT NULL,
 report_status VARCHAR(20) NOT NULL,
 report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
 PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
 PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
 PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
 PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
 PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
 PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
 PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
 PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
 PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
 PARTITION p9 VALUES LESS THAN (MAXVALUE)
);
```

Any other expressions involving TIMESTAMP values are not permitted. (See Bug #42849.)

Range partitioning is particularly useful when one or more of the following conditions is true:

- You want or need to delete "old" data. If you are using the partitioning scheme shown previously for the employees table, you can simply use ALTER TABLE employees DROP PARTITION p0; to delete all rows relating to employees who stopped working for the firm prior to 1991. (See Section 15.1.9, "ALTER TABLE Statement", and [Section 26.3, "Partition Management",](#page-115-0) for more information.) For a table with a great many rows, this can be much more efficient than running a DELETE query such as DELETE FROM employees WHERE YEAR(separated) <= 1990;.
- You want to use a column containing date or time values, or containing values arising from some other series.
- You frequently run queries that depend directly on the column used for partitioning the table. For example, when executing a query such as EXPLAIN SELECT COUNT(\*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store\_id;, MySQL can quickly determine that only partition p2 needs to be scanned because the remaining partitions cannot contain any records satisfying the WHERE clause. See [Section 26.4, "Partition](#page-133-0) [Pruning",](#page-133-0) for more information about how this is accomplished.

A variant on this type of partitioning is RANGE COLUMNS partitioning. Partitioning by RANGE COLUMNS makes it possible to employ multiple columns for defining partitioning ranges that apply both to placement of rows in partitions and for determining the inclusion or exclusion of specific partitions when performing partition pruning. See [Section 26.2.3.1, "RANGE COLUMNS partitioning",](#page-98-1) for more information.

**Partitioning schemes based on time intervals.** If you wish to implement a partitioning scheme based on ranges or intervals of time in MySQL 8.0, you have two options:

1. Partition the table by RANGE, and for the partitioning expression, employ a function operating on a DATE, TIME, or DATETIME column and returning an integer value, as shown here:

```
CREATE TABLE members (
 firstname VARCHAR(25) NOT NULL,
 lastname VARCHAR(25) NOT NULL,
 username VARCHAR(16) NOT NULL,
 email VARCHAR(35),
 joined DATE NOT NULL
)
PARTITION BY RANGE( YEAR(joined) ) (
 PARTITION p0 VALUES LESS THAN (1960),
 PARTITION p1 VALUES LESS THAN (1970),
 PARTITION p2 VALUES LESS THAN (1980),
```

```
 PARTITION p3 VALUES LESS THAN (1990),
 PARTITION p4 VALUES LESS THAN MAXVALUE
);
```

In MySQL 8.0, it is also possible to partition a table by RANGE based on the value of a TIMESTAMP column, using the UNIX\_TIMESTAMP() function, as shown in this example:

```
CREATE TABLE quarterly_report_status (
 report_id INT NOT NULL,
 report_status VARCHAR(20) NOT NULL,
 report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
 PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
 PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
 PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
 PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
 PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
 PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
 PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
 PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
 PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
 PARTITION p9 VALUES LESS THAN (MAXVALUE)
);
```

In MySQL 8.0, any other expressions involving TIMESTAMP values are not permitted. (See Bug #42849.)

![](_page_95_Picture_5.jpeg)

#### **Note**

It is also possible in MySQL 8.0 to use UNIX\_TIMESTAMP(timestamp\_column) as a partitioning expression for tables that are partitioned by LIST. However, it is usually not practical to do so.

2. Partition the table by RANGE COLUMNS, using a DATE or DATETIME column as the partitioning column. For example, the members table could be defined using the joined column directly, as shown here:

```
CREATE TABLE members (
 firstname VARCHAR(25) NOT NULL,
 lastname VARCHAR(25) NOT NULL,
 username VARCHAR(16) NOT NULL,
 email VARCHAR(35),
 joined DATE NOT NULL
)
PARTITION BY RANGE COLUMNS(joined) (
 PARTITION p0 VALUES LESS THAN ('1960-01-01'),
 PARTITION p1 VALUES LESS THAN ('1970-01-01'),
 PARTITION p2 VALUES LESS THAN ('1980-01-01'),
 PARTITION p3 VALUES LESS THAN ('1990-01-01'),
 PARTITION p4 VALUES LESS THAN MAXVALUE
);
```

![](_page_95_Picture_10.jpeg)

### **Note**

The use of partitioning columns employing date or time types other than DATE or DATETIME is not supported with RANGE COLUMNS.

# <span id="page-95-0"></span>**26.2.2 LIST Partitioning**

List partitioning in MySQL is similar to range partitioning in many ways. As in partitioning by RANGE, each partition must be explicitly defined. The chief difference between the two types of partitioning is that, in list partitioning, each partition is defined and selected based on the membership of a column value in one of a set of value lists, rather than in one of a set of contiguous ranges of values. This is done by using PARTITION BY LIST(expr) where expr is a column value or an expression based on a column value and returning an integer value, and then defining each partition by means of a VALUES IN (value\_list), where value\_list is a comma-separated list of integers.

![](_page_96_Picture_2.jpeg)

#### **Note**

In MySQL 8.0, it is possible to match against only a list of integers (and possibly NULL—see [Section 26.2.7, "How MySQL Partitioning Handles NULL"\)](#page-111-0) when partitioning by LIST.

However, other column types may be used in value lists when employing LIST COLUMN partitioning, which is described later in this section.

Unlike the case with partitions defined by range, list partitions do not need to be declared in any particular order. For more detailed syntactical information, see Section 15.1.20, "CREATE TABLE Statement".

For the examples that follow, we assume that the basic definition of the table to be partitioned is provided by the CREATE TABLE statement shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
);
```

(This is the same table used as a basis for the examples in [Section 26.2.1, "RANGE Partitioning"](#page-91-0). As with the other partitioning examples, we assume that the default\_storage\_engine is InnoDB.)

Suppose that there are 20 video stores distributed among 4 franchises as shown in the following table.

| Region  | Store ID Numbers     |
|---------|----------------------|
| North   | 3, 5, 6, 9, 17       |
| East    | 1, 2, 10, 11, 19, 20 |
| West    | 4, 12, 13, 14, 18    |
| Central | 7, 8, 15, 16         |

To partition this table in such a way that rows for stores belonging to the same region are stored in the same partition, you could use the CREATE TABLE statement shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
)
PARTITION BY LIST(store_id) (
 PARTITION pNorth VALUES IN (3,5,6,9,17),
 PARTITION pEast VALUES IN (1,2,10,11,19,20),
 PARTITION pWest VALUES IN (4,12,13,14,18),
 PARTITION pCentral VALUES IN (7,8,15,16)
);
```

This makes it easy to add or drop employee records relating to specific regions to or from the table. For instance, suppose that all stores in the West region are sold to another company. In MySQL 8.0, all rows relating to employees working at stores in that region can be deleted with the query ALTER TABLE employees TRUNCATE PARTITION pWest, which can be executed much more efficiently than the equivalent DELETE statement DELETE FROM employees WHERE store\_id IN (4,12,13,14,18);. (Using ALTER TABLE employees DROP PARTITION pWest would also delete all of these rows, but would also remove the partition pWest from the definition of the table; you would need to use an ALTER TABLE ... ADD PARTITION statement to restore the table's original partitioning scheme.)

As with RANGE partitioning, it is possible to combine LIST partitioning with partitioning by hash or key to produce a composite partitioning (subpartitioning). See [Section 26.2.6, "Subpartitioning"](#page-109-0).

Unlike the case with RANGE partitioning, there is no "catch-all" such as MAXVALUE; all expected values for the partitioning expression should be covered in PARTITION ... VALUES IN (...) clauses. An INSERT statement containing an unmatched partitioning column value fails with an error, as shown in this example:

```
mysql> CREATE TABLE h2 (
 -> c1 INT,
 -> c2 INT
 -> )
 -> PARTITION BY LIST(c1) (
 -> PARTITION p0 VALUES IN (1, 4, 7),
 -> PARTITION p1 VALUES IN (2, 5, 8)
 -> );
Query OK, 0 rows affected (0.11 sec)
mysql> INSERT INTO h2 VALUES (3, 5);
ERROR 1525 (HY000): Table has no partition for value 3
```

When inserting multiple rows using a single INSERT statement into a single InnoDB table, InnoDB considers the statement a single transaction, so that the presence of any unmatched values causes the statement to fail completely, and so no rows are inserted.

You can cause this type of error to be ignored by using the IGNORE keyword, although a warning is issued for each row containing unmatched partitioning column values, as shown here.

```
mysql> TRUNCATE h2;
Query OK, 1 row affected (0.00 sec)
mysql> TABLE h2;
Empty set (0.00 sec)
mysql> INSERT IGNORE INTO h2 VALUES (2, 5), (6, 10), (7, 5), (3, 1), (1, 9);
Query OK, 3 rows affected, 2 warnings (0.01 sec)
Records: 5 Duplicates: 2 Warnings: 2
mysql> SHOW WARNINGS;
+---------+------+------------------------------------+
| Level | Code | Message |
+---------+------+------------------------------------+
| Warning | 1526 | Table has no partition for value 6 |
| Warning | 1526 | Table has no partition for value 3 |
+---------+------+------------------------------------+
2 rows in set (0.00 sec)
```

You can see in the output of the following TABLE statement that rows containing unmatched partitioning column values were silently rejected, while rows containing no unmatched values were inserted into the table:

```
mysql> TABLE h2;
+------+------+
| c1 | c2 |
+------+------+
| 7 | 5 |
| 1 | 9 |
| 2 | 5 |
+------+------+
3 rows in set (0.00 sec)
```

MySQL also provides support for LIST COLUMNS partitioning, a variant of LIST partitioning that enables you to use columns of types other than integer for partitioning columns, and to use multiple columns as partitioning keys. For more information, see [Section 26.2.3.2, "LIST COLUMNS](#page-103-0) [partitioning"](#page-103-0).

# <span id="page-98-0"></span>**26.2.3 COLUMNS Partitioning**

The next two sections discuss COLUMNS partitioning, which are variants on RANGE and LIST partitioning. COLUMNS partitioning enables the use of multiple columns in partitioning keys. All of these columns are taken into account both for the purpose of placing rows in partitions and for the determination of which partitions are to be checked for matching rows in partition pruning.

In addition, both RANGE COLUMNS partitioning and LIST COLUMNS partitioning support the use of noninteger columns for defining value ranges or list members. The permitted data types are shown in the following list:

• All integer types: TINYINT, SMALLINT, MEDIUMINT, INT (INTEGER), and BIGINT. (This is the same as with partitioning by RANGE and LIST.)

Other numeric data types (such as DECIMAL or FLOAT) are not supported as partitioning columns.

• DATE and DATETIME.

Columns using other data types relating to dates or times are not supported as partitioning columns.

• The following string types: CHAR, VARCHAR, BINARY, and VARBINARY.

TEXT and BLOB columns are not supported as partitioning columns.

The discussions of RANGE COLUMNS and LIST COLUMNS partitioning in the next two sections assume that you are already familiar with partitioning based on ranges and lists as supported in MySQL 5.1 and later; for more information about these, see [Section 26.2.1, "RANGE Partitioning"](#page-91-0), and [Section 26.2.2,](#page-95-0) ["LIST Partitioning",](#page-95-0) respectively.

## <span id="page-98-1"></span>**26.2.3.1 RANGE COLUMNS partitioning**

Range columns partitioning is similar to range partitioning, but enables you to define partitions using ranges based on multiple column values. In addition, you can define the ranges using columns of types other than integer types.

RANGE COLUMNS partitioning differs significantly from RANGE partitioning in the following ways:

- RANGE COLUMNS does not accept expressions, only names of columns.
- RANGE COLUMNS accepts a list of one or more columns.

RANGE COLUMNS partitions are based on comparisons between tuples (lists of column values) rather than comparisons between scalar values. Placement of rows in RANGE COLUMNS partitions is also based on comparisons between tuples; this is discussed further later in this section.

• RANGE COLUMNS partitioning columns are not restricted to integer columns; string, DATE and DATETIME columns can also be used as partitioning columns. (See [Section 26.2.3, "COLUMNS](#page-98-0) [Partitioning"](#page-98-0), for details.)

The basic syntax for creating a table partitioned by RANGE COLUMNS is shown here:

```
CREATE TABLE table_name
PARTITION BY RANGE COLUMNS(column_list) (
 PARTITION partition_name VALUES LESS THAN (value_list)[,
 PARTITION partition_name VALUES LESS THAN (value_list)][,
 ...]
)
column_list:
 column_name[, column_name][, ...]
```

```
value_list:
 value[, value][, ...]
```

![](_page_99_Picture_2.jpeg)

#### **Note**

Not all CREATE TABLE options that can be used when creating partitioned tables are shown here. For complete information, see Section 15.1.20, "CREATE TABLE Statement".

In the syntax just shown, column\_list is a list of one or more columns (sometimes called a partitioning column list), and value\_list is a list of values (that is, it is a partition definition value list). A value\_list must be supplied for each partition definition, and each value\_list must have the same number of values as the column\_list has columns. Generally speaking, if you use N columns in the COLUMNS clause, then each VALUES LESS THAN clause must also be supplied with a list of N values.

The elements in the partitioning column list and in the value list defining each partition must occur in the same order. In addition, each element in the value list must be of the same data type as the corresponding element in the column list. However, the order of the column names in the partitioning column list and the value lists does not have to be the same as the order of the table column definitions in the main part of the CREATE TABLE statement. As with table partitioned by RANGE, you can use MAXVALUE to represent a value such that any legal value inserted into a given column is always less than this value. Here is an example of a CREATE TABLE statement that helps to illustrate all of these points:

```
mysql> CREATE TABLE rcx (
 -> a INT,
 -> b INT,
 -> c CHAR(3),
 -> d INT
 -> )
 -> PARTITION BY RANGE COLUMNS(a,d,c) (
 -> PARTITION p0 VALUES LESS THAN (5,10,'ggg'),
 -> PARTITION p1 VALUES LESS THAN (10,20,'mmm'),
 -> PARTITION p2 VALUES LESS THAN (15,30,'sss'),
 -> PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
 -> );
Query OK, 0 rows affected (0.15 sec)
```

Table rcx contains the columns a, b, c, d. The partitioning column list supplied to the COLUMNS clause uses 3 of these columns, in the order a, d, c. Each value list used to define a partition contains 3 values in the same order; that is, each value list tuple has the form (INT, INT, CHAR(3)), which corresponds to the data types used by columns a, d, and c (in that order).

Placement of rows into partitions is determined by comparing the tuple from a row to be inserted that matches the column list in the COLUMNS clause with the tuples used in the VALUES LESS THAN clauses to define partitions of the table. Because we are comparing tuples (that is, lists or sets of values) rather than scalar values, the semantics of VALUES LESS THAN as used with RANGE COLUMNS partitions differs somewhat from the case with simple RANGE partitions. In RANGE partitioning, a row generating an expression value that is equal to a limiting value in a VALUES LESS THAN is never placed in the corresponding partition; however, when using RANGE COLUMNS partitioning, it is sometimes possible for a row whose partitioning column list's first element is equal in value to the that of the first element in a VALUES LESS THAN value list to be placed in the corresponding partition.

Consider the RANGE partitioned table created by this statement:

```
CREATE TABLE r1 (
 a INT,
 b INT
)
PARTITION BY RANGE (a) (
 PARTITION p0 VALUES LESS THAN (5),
 PARTITION p1 VALUES LESS THAN (MAXVALUE)
);
```

If we insert 3 rows into this table such that the column value for a is 5 for each row, all 3 rows are stored in partition p1 because the a column value is in each case not less than 5, as we can see by executing the proper query against the Information Schema PARTITIONS table:

```
mysql> INSERT INTO r1 VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 -> FROM INFORMATION_SCHEMA.PARTITIONS
 -> WHERE TABLE_NAME = 'r1';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 0 |
| p1 | 3 |
+----------------+------------+
2 rows in set (0.00 sec)
```

Now consider a similar table rc1 that uses RANGE COLUMNS partitioning with both columns a and b referenced in the COLUMNS clause, created as shown here:

```
CREATE TABLE rc1 (
 a INT,
 b INT
)
PARTITION BY RANGE COLUMNS(a, b) (
 PARTITION p0 VALUES LESS THAN (5, 12),
 PARTITION p3 VALUES LESS THAN (MAXVALUE, MAXVALUE)
);
```

If we insert exactly the same rows into rc1 as we just inserted into r1, the distribution of the rows is quite different:

```
mysql> INSERT INTO rc1 VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 -> FROM INFORMATION_SCHEMA.PARTITIONS
 -> WHERE TABLE_NAME = 'rc1';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 2 |
| p3 | 1 |
+----------------+------------+
2 rows in set (0.00 sec)
```

This is because we are comparing rows rather than scalar values. We can compare the row values inserted with the limiting row value from the VALUES THAN LESS THAN clause used to define partition p0 in table rc1, like this:

```
mysql> SELECT (5,10) < (5,12), (5,11) < (5,12), (5,12) < (5,12);
+-----------------+-----------------+-----------------+
| (5,10) < (5,12) | (5,11) < (5,12) | (5,12) < (5,12) |
+-----------------+-----------------+-----------------+
| 1 | 1 | 0 |
+-----------------+-----------------+-----------------+
1 row in set (0.00 sec)
```

The 2 tuples (5,10) and (5,11) evaluate as less than (5,12), so they are stored in partition p0. Since 5 is not less than 5 and 12 is not less than 12, (5,12) is considered not less than (5,12), and is stored in partition p1.

The SELECT statement in the preceding example could also have been written using explicit row constructors, like this:

```
SELECT ROW(5,10) < ROW(5,12), ROW(5,11) < ROW(5,12), ROW(5,12) < ROW(5,12);
```

For more information about the use of row constructors in MySQL, see Section 15.2.15.5, "Row Subqueries".

For a table partitioned by RANGE COLUMNS using only a single partitioning column, the storing of rows in partitions is the same as that of an equivalent table that is partitioned by RANGE. The following CREATE TABLE statement creates a table partitioned by RANGE COLUMNS using 1 partitioning column:

```
CREATE TABLE rx (
 a INT,
 b INT
)
PARTITION BY RANGE COLUMNS (a) (
 PARTITION p0 VALUES LESS THAN (5),
 PARTITION p1 VALUES LESS THAN (MAXVALUE)
);
```

If we insert the rows (5,10), (5,11), and (5,12) into this table, we can see that their placement is the same as it is for the table r we created and populated earlier:

```
mysql> INSERT INTO rx VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT PARTITION_NAME,TABLE_ROWS
 -> FROM INFORMATION_SCHEMA.PARTITIONS
 -> WHERE TABLE_NAME = 'rx';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 0 |
| p1 | 3 |
+----------------+------------+
2 rows in set (0.00 sec)
```

It is also possible to create tables partitioned by RANGE COLUMNS where limiting values for one or more columns are repeated in successive partition definitions. You can do this as long as the tuples of column values used to define the partitions are strictly increasing. For example, each of the following CREATE TABLE statements is valid:

```
CREATE TABLE rc2 (
 a INT,
 b INT
)
PARTITION BY RANGE COLUMNS(a,b) (
 PARTITION p0 VALUES LESS THAN (0,10),
 PARTITION p1 VALUES LESS THAN (10,20),
 PARTITION p2 VALUES LESS THAN (10,30),
 PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE)
 );
CREATE TABLE rc3 (
 a INT,
 b INT
)
PARTITION BY RANGE COLUMNS(a,b) (
 PARTITION p0 VALUES LESS THAN (0,10),
 PARTITION p1 VALUES LESS THAN (10,20),
 PARTITION p2 VALUES LESS THAN (10,30),
 PARTITION p3 VALUES LESS THAN (10,35),
 PARTITION p4 VALUES LESS THAN (20,40),
 PARTITION p5 VALUES LESS THAN (MAXVALUE,MAXVALUE)
 );
```

The following statement also succeeds, even though it might appear at first glance that it would not, since the limiting value of column b is 25 for partition p0 and 20 for partition p1, and the limiting value of column c is 100 for partition p1 and 50 for partition p2:

```
CREATE TABLE rc4 (
 a INT,
```

```
 b INT,
 c INT
)
PARTITION BY RANGE COLUMNS(a,b,c) (
 PARTITION p0 VALUES LESS THAN (0,25,50),
 PARTITION p1 VALUES LESS THAN (10,20,100),
 PARTITION p2 VALUES LESS THAN (10,30,50),
 PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
 );
```

When designing tables partitioned by RANGE COLUMNS, you can always test successive partition definitions by comparing the desired tuples using the mysql client, like this:

```
mysql> SELECT (0,25,50) < (10,20,100), (10,20,100) < (10,30,50);
+-------------------------+--------------------------+
| (0,25,50) < (10,20,100) | (10,20,100) < (10,30,50) |
+-------------------------+--------------------------+
| 1 | 1 |
+-------------------------+--------------------------+
1 row in set (0.00 sec)
```

If a CREATE TABLE statement contains partition definitions that are not in strictly increasing order, it fails with an error, as shown in this example:

```
mysql> CREATE TABLE rcf (
 -> a INT,
 -> b INT,
 -> c INT
 -> )
 -> PARTITION BY RANGE COLUMNS(a,b,c) (
 -> PARTITION p0 VALUES LESS THAN (0,25,50),
 -> PARTITION p1 VALUES LESS THAN (20,20,100),
 -> PARTITION p2 VALUES LESS THAN (10,30,50),
 -> PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
 -> );
ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition
```

When you get such an error, you can deduce which partition definitions are invalid by making "less than" comparisons between their column lists. In this case, the problem is with the definition of partition p2 because the tuple used to define it is not less than the tuple used to define partition p3, as shown here:

```
mysql> SELECT (0,25,50) < (20,20,100), (20,20,100) < (10,30,50);
+-------------------------+--------------------------+
| (0,25,50) < (20,20,100) | (20,20,100) < (10,30,50) |
+-------------------------+--------------------------+
| 1 | 0 |
+-------------------------+--------------------------+
1 row in set (0.00 sec)
```

It is also possible for MAXVALUE to appear for the same column in more than one VALUES LESS THAN clause when using RANGE COLUMNS. However, the limiting values for individual columns in successive partition definitions should otherwise be increasing, there should be no more than one partition defined where MAXVALUE is used as the upper limit for all column values, and this partition definition should appear last in the list of PARTITION ... VALUES LESS THAN clauses. In addition, you cannot use MAXVALUE as the limiting value for the first column in more than one partition definition.

As stated previously, it is also possible with RANGE COLUMNS partitioning to use non-integer columns as partitioning columns. (See [Section 26.2.3, "COLUMNS Partitioning",](#page-98-0) for a complete listing of these.) Consider a table named employees (which is not partitioned), created using the following statement:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
```

);

Using RANGE COLUMNS partitioning, you can create a version of this table that stores each row in one of four partitions based on the employee's last name, like this:

```
CREATE TABLE employees_by_lname (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT NOT NULL,
 store_id INT NOT NULL
)
PARTITION BY RANGE COLUMNS (lname) (
 PARTITION p0 VALUES LESS THAN ('g'),
 PARTITION p1 VALUES LESS THAN ('m'),
 PARTITION p2 VALUES LESS THAN ('t'),
 PARTITION p3 VALUES LESS THAN (MAXVALUE)
);
```

Alternatively, you could cause the employees table as created previously to be partitioned using this scheme by executing the following ALTER TABLE statement:

```
ALTER TABLE employees PARTITION BY RANGE COLUMNS (lname) (
 PARTITION p0 VALUES LESS THAN ('g'),
 PARTITION p1 VALUES LESS THAN ('m'),
 PARTITION p2 VALUES LESS THAN ('t'),
 PARTITION p3 VALUES LESS THAN (MAXVALUE)
);
```

![](_page_103_Picture_6.jpeg)

#### **Note**

Because different character sets and collations have different sort orders, the character sets and collations in use may effect which partition of a table partitioned by RANGE COLUMNS a given row is stored in when using string columns as partitioning columns. In addition, changing the character set or collation for a given database, table, or column after such a table is created may cause changes in how rows are distributed. For example, when using a casesensitive collation, 'and' sorts before 'Andersen', but when using a collation that is case-insensitive, the reverse is true.

For information about how MySQL handles character sets and collations, see Chapter 12, Character Sets, Collations, Unicode.

Similarly, you can cause the employees table to be partitioned in such a way that each row is stored in one of several partitions based on the decade in which the corresponding employee was hired using the ALTER TABLE statement shown here:

```
ALTER TABLE employees PARTITION BY RANGE COLUMNS (hired) (
 PARTITION p0 VALUES LESS THAN ('1970-01-01'),
 PARTITION p1 VALUES LESS THAN ('1980-01-01'),
 PARTITION p2 VALUES LESS THAN ('1990-01-01'),
 PARTITION p3 VALUES LESS THAN ('2000-01-01'),
 PARTITION p4 VALUES LESS THAN ('2010-01-01'),
 PARTITION p5 VALUES LESS THAN (MAXVALUE)
);
```

See Section 15.1.20, "CREATE TABLE Statement", for additional information about PARTITION BY RANGE COLUMNS syntax.

## <span id="page-103-0"></span>**26.2.3.2 LIST COLUMNS partitioning**

MySQL 8.0 provides support for LIST COLUMNS partitioning. This is a variant of LIST partitioning that enables the use of multiple columns as partition keys, and for columns of data types other than integer types to be used as partitioning columns; you can use string types, DATE, and DATETIME

columns. (For more information about permitted data types for COLUMNS partitioning columns, see [Section 26.2.3, "COLUMNS Partitioning".](#page-98-0))

Suppose that you have a business that has customers in 12 cities which, for sales and marketing purposes, you organize into 4 regions of 3 cities each as shown in the following table:

| Region | Cities                         |
|--------|--------------------------------|
| 1      | Oskarshamn, Högsby, Mönsterås  |
| 2      | Vimmerby, Hultsfred, Västervik |
| 3      | Nässjö, Eksjö, Vetlanda        |
| 4      | Uppvidinge, Alvesta, Växjo     |

With LIST COLUMNS partitioning, you can create a table for customer data that assigns a row to any of 4 partitions corresponding to these regions based on the name of the city where a customer resides, as shown here:

```
CREATE TABLE customers_1 (
 first_name VARCHAR(25),
 last_name VARCHAR(25),
 street_1 VARCHAR(30),
 street_2 VARCHAR(30),
 city VARCHAR(15),
 renewal DATE
)
PARTITION BY LIST COLUMNS(city) (
 PARTITION pRegion_1 VALUES IN('Oskarshamn', 'Högsby', 'Mönsterås'),
 PARTITION pRegion_2 VALUES IN('Vimmerby', 'Hultsfred', 'Västervik'),
 PARTITION pRegion_3 VALUES IN('Nässjö', 'Eksjö', 'Vetlanda'),
 PARTITION pRegion_4 VALUES IN('Uppvidinge', 'Alvesta', 'Växjo')
);
```

As with partitioning by RANGE COLUMNS, you do not need to use expressions in the COLUMNS() clause to convert column values into integers. (In fact, the use of expressions other than column names is not permitted with COLUMNS().)

It is also possible to use DATE and DATETIME columns, as shown in the following example that uses the same name and columns as the customers\_1 table shown previously, but employs LIST COLUMNS partitioning based on the renewal column to store rows in one of 4 partitions depending on the week in February 2010 the customer's account is scheduled to renew:

```
CREATE TABLE customers_2 (
 first_name VARCHAR(25),
 last_name VARCHAR(25),
 street_1 VARCHAR(30),
 street_2 VARCHAR(30),
 city VARCHAR(15),
 renewal DATE
)
PARTITION BY LIST COLUMNS(renewal) (
 PARTITION pWeek_1 VALUES IN('2010-02-01', '2010-02-02', '2010-02-03',
 '2010-02-04', '2010-02-05', '2010-02-06', '2010-02-07'),
 PARTITION pWeek_2 VALUES IN('2010-02-08', '2010-02-09', '2010-02-10',
 '2010-02-11', '2010-02-12', '2010-02-13', '2010-02-14'),
 PARTITION pWeek_3 VALUES IN('2010-02-15', '2010-02-16', '2010-02-17',
 '2010-02-18', '2010-02-19', '2010-02-20', '2010-02-21'),
 PARTITION pWeek_4 VALUES IN('2010-02-22', '2010-02-23', '2010-02-24',
 '2010-02-25', '2010-02-26', '2010-02-27', '2010-02-28')
);
```

This works, but becomes cumbersome to define and maintain if the number of dates involved grows very large; in such cases, it is usually more practical to employ RANGE or RANGE COLUMNS partitioning instead. In this case, since the column we wish to use as the partitioning key is a DATE column, we use RANGE COLUMNS partitioning, as shown here:

```
CREATE TABLE customers_3 (
```

```
 first_name VARCHAR(25),
 last_name VARCHAR(25),
 street_1 VARCHAR(30),
 street_2 VARCHAR(30),
 city VARCHAR(15),
 renewal DATE
)
PARTITION BY RANGE COLUMNS(renewal) (
 PARTITION pWeek_1 VALUES LESS THAN('2010-02-09'),
 PARTITION pWeek_2 VALUES LESS THAN('2010-02-15'),
 PARTITION pWeek_3 VALUES LESS THAN('2010-02-22'),
 PARTITION pWeek_4 VALUES LESS THAN('2010-03-01')
);
```

See [Section 26.2.3.1, "RANGE COLUMNS partitioning"](#page-98-1), for more information.

In addition (as with RANGE COLUMNS partitioning), you can use multiple columns in the COLUMNS() clause.

See Section 15.1.20, "CREATE TABLE Statement", for additional information about PARTITION BY LIST COLUMNS() syntax.

## <span id="page-105-0"></span>**26.2.4 HASH Partitioning**

Partitioning by HASH is used primarily to ensure an even distribution of data among a predetermined number of partitions. With range or list partitioning, you must specify explicitly which partition a given column value or set of column values should be stored in; with hash partitioning, this decision is taken care of for you, and you need only specify a column value or expression based on a column value to be hashed and the number of partitions into which the partitioned table is to be divided.

To partition a table using HASH partitioning, it is necessary to append to the CREATE TABLE statement a PARTITION BY HASH (expr) clause, where expr is an expression that returns an integer. This can simply be the name of a column whose type is one of MySQL's integer types. In addition, you most likely want to follow this with PARTITIONS num, where num is a positive integer representing the number of partitions into which the table is to be divided.

![](_page_105_Picture_8.jpeg)

### **Note**

For simplicity, the tables in the examples that follow do not use any keys. You should be aware that, if a table has any unique keys, every column used in the partitioning expression for this table must be part of every unique key, including the primary key. See [Section 26.6.1, "Partitioning Keys, Primary Keys, and](#page-148-0) [Unique Keys"](#page-148-0), for more information.

The following statement creates a table that uses hashing on the store\_id column and is divided into 4 partitions:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
)
PARTITION BY HASH(store_id)
PARTITIONS 4;
```

If you do not include a PARTITIONS clause, the number of partitions defaults to 1; using the PARTITIONS keyword without a number following it results in a syntax error.

You can also use an SQL expression that returns an integer for expr. For instance, you might want to partition based on the year in which an employee was hired. This can be done as shown here:

```
CREATE TABLE employees (
```

```
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
)
PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

expr must return a nonconstant, nonrandom integer value (in other words, it should be varying but deterministic), and must not contain any prohibited constructs as described in [Section 26.6,](#page-142-0) ["Restrictions and Limitations on Partitioning".](#page-142-0) You should also keep in mind that this expression is evaluated each time a row is inserted or updated (or possibly deleted); this means that very complex expressions may give rise to performance issues, particularly when performing operations (such as batch inserts) that affect a great many rows at one time.

The most efficient hashing function is one which operates upon a single table column and whose value increases or decreases consistently with the column value, as this allows for "pruning" on ranges of partitions. That is, the more closely that the expression varies with the value of the column on which it is based, the more efficiently MySQL can use the expression for hash partitioning.

For example, where date\_col is a column of type DATE, then the expression TO\_DAYS(date\_col) is said to vary directly with the value of date\_col, because for every change in the value of date\_col, the value of the expression changes in a consistent manner. The variance of the expression YEAR(date\_col) with respect to date\_col is not quite as direct as that of TO\_DAYS(date\_col), because not every possible change in date\_col produces an equivalent change in YEAR(date\_col). Even so, YEAR(date\_col) is a good candidate for a hashing function, because it varies directly with a portion of date\_col and there is no possible change in date\_col that produces a disproportionate change in YEAR(date\_col).

By way of contrast, suppose that you have a column named int\_col whose type is INT. Now consider the expression POW(5-int\_col,3) + 6. This would be a poor choice for a hashing function because a change in the value of int\_col is not guaranteed to produce a proportional change in the value of the expression. Changing the value of int\_col by a given amount can produce widely differing changes in the value of the expression. For example, changing int\_col from 5 to 6 produces a change of -1 in the value of the expression, but changing the value of int\_col from 6 to 7 produces a change of -7 in the expression value.

In other words, the more closely the graph of the column value versus the value of the expression follows a straight line as traced by the equation y=cx where c is some nonzero constant, the better the expression is suited to hashing. This has to do with the fact that the more nonlinear an expression is, the more uneven the distribution of data among the partitions it tends to produce.

In theory, pruning is also possible for expressions involving more than one column value, but determining which of such expressions are suitable can be quite difficult and time-consuming. For this reason, the use of hashing expressions involving multiple columns is not particularly recommended.

When PARTITION BY HASH is used, the storage engine determines which partition of num partitions to use based on the modulus of the result of the expression. In other words, for a given expression expr, the partition in which the record is stored is partition number N, where N = MOD(expr, num). Suppose that table t1 is defined as follows, so that it has 4 partitions:

```
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
 PARTITION BY HASH( YEAR(col3) )
 PARTITIONS 4;
```

If you insert a record into t1 whose col3 value is '2005-09-15', then the partition in which it is stored is determined as follows:

```
MOD(YEAR('2005-09-01'),4)
= MOD(2005,4)
```

= 1

MySQL 8.0 also supports a variant of HASH partitioning known as linear hashing which employs a more complex algorithm for determining the placement of new rows inserted into the partitioned table. See [Section 26.2.4.1, "LINEAR HASH Partitioning",](#page-107-0) for a description of this algorithm.

The user-supplied expression is evaluated each time a record is inserted or updated. It may also depending on the circumstances—be evaluated when records are deleted.

### <span id="page-107-0"></span>**26.2.4.1 LINEAR HASH Partitioning**

MySQL also supports linear hashing, which differs from regular hashing in that linear hashing utilizes a linear powers-of-two algorithm whereas regular hashing employs the modulus of the hashing function's value.

Syntactically, the only difference between linear-hash partitioning and regular hashing is the addition of the LINEAR keyword in the PARTITION BY clause, as shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30),
 hired DATE NOT NULL DEFAULT '1970-01-01',
 separated DATE NOT NULL DEFAULT '9999-12-31',
 job_code INT,
 store_id INT
)
PARTITION BY LINEAR HASH( YEAR(hired) )
PARTITIONS 4;
```

Given an expression expr, the partition in which the record is stored when linear hashing is used is partition number N from among num partitions, where N is derived according to the following algorithm:

1. Find the next power of 2 greater than num. We call this value V; it can be calculated as:

```
V = POWER(2, CEILING(LOG(2, num)))
(Suppose that num is 13. Then LOG(2,13) is 3.7004397181411. CEILING(3.7004397181411)
is 4, and V = POWER(2,4), which is 16.)
```

- 2. Set N = F(column\_list) & (V 1).
- 3. While N >= num:
  - Set V = V / 2
  - Set N = N & (V 1)

Suppose that the table t1, using linear hash partitioning and having 6 partitions, is created using this statement:

```
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
 PARTITION BY LINEAR HASH( YEAR(col3) )
 PARTITIONS 6;
```

Now assume that you want to insert two records into t1 having the col3 column values '2003-04-14' and '1998-10-19'. The partition number for the first of these is determined as follows:

```
V = POWER(2, CEILING( LOG(2,6) )) = 8
N = YEAR('2003-04-14') & (8 - 1)
 = 2003 & 7
 = 3
(3 >= 6 is FALSE: record stored in partition #3)
```

The number of the partition where the second record is stored is calculated as shown here:

```
V = 8
N = YEAR('1998-10-19') & (8 - 1)
 = 1998 & 7
 = 6
(6 >= 6 is TRUE: additional step required)
N = 6 & ((8 / 2) - 1)
 = 6 & 3
 = 2
(2 >= 6 is FALSE: record stored in partition #2)
```

The advantage in partitioning by linear hash is that the adding, dropping, merging, and splitting of partitions is made much faster, which can be beneficial when dealing with tables containing extremely large amounts (terabytes) of data. The disadvantage is that data is less likely to be evenly distributed between partitions as compared with the distribution obtained using regular hash partitioning.

# <span id="page-108-0"></span>**26.2.5 KEY Partitioning**

Partitioning by key is similar to partitioning by hash, except that where hash partitioning employs a user-defined expression, the hashing function for key partitioning is supplied by the MySQL server. NDB Cluster uses MD5() for this purpose; for tables using other storage engines, the server employs its own internal hashing function.

The syntax rules for CREATE TABLE ... PARTITION BY KEY are similar to those for creating a table that is partitioned by hash. The major differences are listed here:

- KEY is used rather than HASH.
- KEY takes only a list of zero or more column names. Any columns used as the partitioning key must comprise part or all of the table's primary key, if the table has one. Where no column name is specified as the partitioning key, the table's primary key is used, if there is one. For example, the following CREATE TABLE statement is valid in MySQL 8.0:

```
CREATE TABLE k1 (
 id INT NOT NULL PRIMARY KEY,
 name VARCHAR(20)
)
PARTITION BY KEY()
PARTITIONS 2;
```

If there is no primary key but there is a unique key, then the unique key is used for the partitioning key:

```
CREATE TABLE k1 (
 id INT NOT NULL,
 name VARCHAR(20),
 UNIQUE KEY (id)
)
PARTITION BY KEY()
PARTITIONS 2;
```

However, if the unique key column were not defined as NOT NULL, then the previous statement would fail.

In both of these cases, the partitioning key is the id column, even though it is not shown in the output of SHOW CREATE TABLE or in the PARTITION\_EXPRESSION column of the Information Schema PARTITIONS table.

Unlike the case with other partitioning types, columns used for partitioning by KEY are not restricted to integer or NULL values. For example, the following CREATE TABLE statement is valid:

```
CREATE TABLE tm1 (
 s1 CHAR(32) PRIMARY KEY
)
```

```
PARTITION BY KEY(s1)
PARTITIONS 10;
```

The preceding statement would not be valid, were a different partitioning type to be specified. (In this case, simply using PARTITION BY KEY() would also be valid and have the same effect as PARTITION BY KEY(s1), since s1 is the table's primary key.)

For additional information about this issue, see [Section 26.6, "Restrictions and Limitations on](#page-142-0) [Partitioning"](#page-142-0).

Columns with index prefixes are not supported in partitioning keys. This means that CHAR, VARCHAR, BINARY, and VARBINARY columns can be used in a partitioning key, as long as they do not employ prefixes; because a prefix must be specified for BLOB and TEXT columns in index definitions, it is not possible to use columns of these two types in partitioning keys. Prior to MySQL 8.0.21, columns using prefixes were permitted when creating, altering, or upgrading a partitioned table, even though they were not included in the table's partitioning key; in MySQL 8.0.21 and later, this permissive behavior is deprecated, and the server displays appropriate warnings or errors when one or more such columns are used. See [Column index prefixes not supported for key partitioning](#page-145-0), for more information and examples.

![](_page_109_Picture_5.jpeg)

#### **Note**

Tables using the NDB storage engine are implicitly partitioned by KEY, using the table's primary key as the partitioning key (as with other MySQL storage engines). In the event that the NDB Cluster table has no explicit primary key, the "hidden" primary key generated by the NDB storage engine for each NDB Cluster table is used as the partitioning key.

If you define an explicit partitioning scheme for an NDB table, the table must have an explicit primary key, and any columns used in the partitioning expression must be part of this key. However, if the table uses an "empty" partitioning expression—that is, PARTITION BY KEY() with no column references—then no explicit primary key is required.

You can observe this partitioning using the ndb\_desc utility (with the -p option).

![](_page_109_Picture_10.jpeg)

### **Important**

For a key-partitioned table, you cannot execute an ALTER TABLE DROP PRIMARY KEY, as doing so generates the error ERROR 1466 (HY000): Field in list of fields for partition function not found in table. This is not an issue for NDB Cluster tables which are partitioned by KEY; in such cases, the table is reorganized using the "hidden" primary key as the table's new partitioning key. See Chapter 25, MySQL NDB Cluster 8.0.

It is also possible to partition a table by linear key. Here is a simple example:

```
CREATE TABLE tk (
 col1 INT NOT NULL,
 col2 CHAR(5),
 col3 DATE
)
PARTITION BY LINEAR KEY (col1)
PARTITIONS 3;
```

The LINEAR keyword has the same effect on KEY partitioning as it does on HASH partitioning, with the partition number being derived using a powers-of-two algorithm rather than modulo arithmetic. See [Section 26.2.4.1, "LINEAR HASH Partitioning",](#page-107-0) for a description of this algorithm and its implications.

# <span id="page-109-0"></span>**26.2.6 Subpartitioning**

Subpartitioning—also known as composite partitioning—is the further division of each partition in a partitioned table. Consider the following CREATE TABLE statement:

```
CREATE TABLE ts (id INT, purchased DATE)
 PARTITION BY RANGE( YEAR(purchased) )
 SUBPARTITION BY HASH( TO_DAYS(purchased) )
 SUBPARTITIONS 2 (
 PARTITION p0 VALUES LESS THAN (1990),
 PARTITION p1 VALUES LESS THAN (2000),
 PARTITION p2 VALUES LESS THAN MAXVALUE
 );
```

Table ts has 3 RANGE partitions. Each of these partitions—p0, p1, and p2—is further divided into 2 subpartitions. In effect, the entire table is divided into 3 \* 2 = 6 partitions. However, due to the action of the PARTITION BY RANGE clause, the first 2 of these store only those records with a value less than 1990 in the purchased column.

It is possible to subpartition tables that are partitioned by RANGE or LIST. Subpartitions may use either HASH or KEY partitioning. This is also known as composite partitioning.

![](_page_110_Picture_5.jpeg)

#### **Note**

SUBPARTITION BY HASH and SUBPARTITION BY KEY generally follow the same syntax rules as PARTITION BY HASH and PARTITION BY KEY, respectively. An exception to this is that SUBPARTITION BY KEY (unlike PARTITION BY KEY) does not currently support a default column, so the column used for this purpose must be specified, even if the table has an explicit primary key. This is a known issue which we are working to address; see [Issues](#page-146-0) [with subpartitions](#page-146-0), for more information and an example.

It is also possible to define subpartitions explicitly using SUBPARTITION clauses to specify options for individual subpartitions. For example, a more verbose fashion of creating the same table ts as shown in the previous example would be:

```
CREATE TABLE ts (id INT, purchased DATE)
 PARTITION BY RANGE( YEAR(purchased) )
 SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
 PARTITION p0 VALUES LESS THAN (1990) (
 SUBPARTITION s0,
 SUBPARTITION s1
 ),
 PARTITION p1 VALUES LESS THAN (2000) (
 SUBPARTITION s2,
 SUBPARTITION s3
 ),
 PARTITION p2 VALUES LESS THAN MAXVALUE (
 SUBPARTITION s4,
 SUBPARTITION s5
 )
 );
```

Some syntactical items of note are listed here:

- Each partition must have the same number of subpartitions.
- If you explicitly define any subpartitions using SUBPARTITION on any partition of a partitioned table, you must define them all. In other words, the following statement fails:

```
CREATE TABLE ts (id INT, purchased DATE)
 PARTITION BY RANGE( YEAR(purchased) )
 SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
 PARTITION p0 VALUES LESS THAN (1990) (
 SUBPARTITION s0,
 SUBPARTITION s1
 ),
 PARTITION p1 VALUES LESS THAN (2000),
 PARTITION p2 VALUES LESS THAN MAXVALUE (
```

```
 SUBPARTITION s2,
 SUBPARTITION s3
 )
 );
```

This statement would still fail even if it used SUBPARTITIONS 2.

- Each SUBPARTITION clause must include (at a minimum) a name for the subpartition. Otherwise, you may set any desired option for the subpartition or allow it to assume its default setting for that option.
- Subpartition names must be unique across the entire table. For example, the following CREATE TABLE statement is valid:

```
CREATE TABLE ts (id INT, purchased DATE)
 PARTITION BY RANGE( YEAR(purchased) )
 SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
 PARTITION p0 VALUES LESS THAN (1990) (
 SUBPARTITION s0,
 SUBPARTITION s1
 ),
 PARTITION p1 VALUES LESS THAN (2000) (
 SUBPARTITION s2,
 SUBPARTITION s3
 ),
 PARTITION p2 VALUES LESS THAN MAXVALUE (
 SUBPARTITION s4,
 SUBPARTITION s5
 )
 );
```

## <span id="page-111-0"></span>**26.2.7 How MySQL Partitioning Handles NULL**

Partitioning in MySQL does nothing to disallow NULL as the value of a partitioning expression, whether it is a column value or the value of a user-supplied expression. Even though it is permitted to use NULL as the value of an expression that must otherwise yield an integer, it is important to keep in mind that NULL is not a number. MySQL's partitioning implementation treats NULL as being less than any non-NULL value, just as ORDER BY does.

This means that treatment of NULL varies between partitioning of different types, and may produce behavior which you do not expect if you are not prepared for it. This being the case, we discuss in this section how each MySQL partitioning type handles NULL values when determining the partition in which a row should be stored, and provide examples for each.

**Handling of NULL with RANGE partitioning.** If you insert a row into a table partitioned by RANGE such that the column value used to determine the partition is NULL, the row is inserted into the lowest partition. Consider these two tables in a database named p, created as follows:

```
mysql> CREATE TABLE t1 (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY RANGE(c1) (
 -> PARTITION p0 VALUES LESS THAN (0),
 -> PARTITION p1 VALUES LESS THAN (10),
 -> PARTITION p2 VALUES LESS THAN MAXVALUE
 -> );
Query OK, 0 rows affected (0.09 sec)
mysql> CREATE TABLE t2 (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY RANGE(c1) (
 -> PARTITION p0 VALUES LESS THAN (-5),
 -> PARTITION p1 VALUES LESS THAN (0),
 -> PARTITION p2 VALUES LESS THAN (10),
 -> PARTITION p3 VALUES LESS THAN MAXVALUE
```

```
 -> );
Query OK, 0 rows affected (0.09 sec)
```

You can see the partitions created by these two CREATE TABLE statements using the following query against the PARTITIONS table in the INFORMATION\_SCHEMA database:

```
mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
 > FROM INFORMATION_SCHEMA.PARTITIONS
 > WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 't_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| t1 | p0 | 0 | 0 | 0 |
| t1 | p1 | 0 | 0 | 0 |
| t1 | p2 | 0 | 0 | 0 |
| t2 | p0 | 0 | 0 | 0 |
| t2 | p1 | 0 | 0 | 0 |
| t2 | p2 | 0 | 0 | 0 |
| t2 | p3 | 0 | 0 | 0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.00 sec)
```

(For more information about this table, see Section 28.3.21, "The INFORMATION\_SCHEMA PARTITIONS Table".) Now let us populate each of these tables with a single row containing a NULL in the column used as the partitioning key, and verify that the rows were inserted using a pair of SELECT statements:

```
mysql> INSERT INTO t1 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)
mysql> INSERT INTO t2 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)
mysql> SELECT * FROM t1;
+------+--------+
| id | name |
+------+--------+
| NULL | mothra |
+------+--------+
1 row in set (0.00 sec)
mysql> SELECT * FROM t2;
+------+--------+
| id | name |
+------+--------+
| NULL | mothra |
+------+--------+
1 row in set (0.00 sec)
```

You can see which partitions are used to store the inserted rows by rerunning the previous query against INFORMATION\_SCHEMA.PARTITIONS and inspecting the output:

```
mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
 > FROM INFORMATION_SCHEMA.PARTITIONS
 > WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 't_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| t1 | p0 | 1 | 20 | 20 |
| t1 | p1 | 0 | 0 | 0 |
| t1 | p2 | 0 | 0 | 0 |
| t2 | p0 | 1 | 20 | 20 |
| t2 | p1 | 0 | 0 | 0 |
| t2 | p2 | 0 | 0 | 0 |
| t2 | p3 | 0 | 0 | 0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.01 sec)
```

You can also demonstrate that these rows were stored in the lowest-numbered partition of each table by dropping these partitions, and then re-running the SELECT statements:

```
mysql> ALTER TABLE t1 DROP PARTITION p0;
Query OK, 0 rows affected (0.16 sec)
mysql> ALTER TABLE t2 DROP PARTITION p0;
Query OK, 0 rows affected (0.16 sec)
mysql> SELECT * FROM t1;
Empty set (0.00 sec)
mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

(For more information on ALTER TABLE ... DROP PARTITION, see Section 15.1.9, "ALTER TABLE Statement".)

NULL is also treated in this way for partitioning expressions that use SQL functions. Suppose that we define a table using a CREATE TABLE statement such as this one:

```
CREATE TABLE tndate (
 id INT,
 dt DATE
)
PARTITION BY RANGE( YEAR(dt) ) (
 PARTITION p0 VALUES LESS THAN (1990),
 PARTITION p1 VALUES LESS THAN (2000),
 PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

As with other MySQL functions, YEAR(NULL) returns NULL. A row with a dt column value of NULL is treated as though the partitioning expression evaluated to a value less than any other value, and so is inserted into partition p0.

**Handling of NULL with LIST partitioning.** A table that is partitioned by LIST admits NULL values if and only if one of its partitions is defined using that value-list that contains NULL. The converse of this is that a table partitioned by LIST which does not explicitly use NULL in a value list rejects rows resulting in a NULL value for the partitioning expression, as shown in this example:

```
mysql> CREATE TABLE ts1 (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY LIST(c1) (
 -> PARTITION p0 VALUES IN (0, 3, 6),
 -> PARTITION p1 VALUES IN (1, 4, 7),
 -> PARTITION p2 VALUES IN (2, 5, 8)
 -> );
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO ts1 VALUES (9, 'mothra');
ERROR 1504 (HY000): Table has no partition for value 9
mysql> INSERT INTO ts1 VALUES (NULL, 'mothra');
ERROR 1504 (HY000): Table has no partition for value NULL
```

Only rows having a c1 value between 0 and 8 inclusive can be inserted into ts1. NULL falls outside this range, just like the number 9. We can create tables ts2 and ts3 having value lists containing NULL, as shown here:

```
mysql> CREATE TABLE ts2 (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY LIST(c1) (
 -> PARTITION p0 VALUES IN (0, 3, 6),
 -> PARTITION p1 VALUES IN (1, 4, 7),
 -> PARTITION p2 VALUES IN (2, 5, 8),
 -> PARTITION p3 VALUES IN (NULL)
 -> );
Query OK, 0 rows affected (0.01 sec)
```

```
mysql> CREATE TABLE ts3 (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY LIST(c1) (
 -> PARTITION p0 VALUES IN (0, 3, 6),
 -> PARTITION p1 VALUES IN (1, 4, 7, NULL),
 -> PARTITION p2 VALUES IN (2, 5, 8)
 -> );
Query OK, 0 rows affected (0.01 sec)
```

When defining value lists for partitioning, you can (and should) treat NULL just as you would any other value. For example, both VALUES IN (NULL) and VALUES IN (1, 4, 7, NULL) are valid, as are VALUES IN (1, NULL, 4, 7), VALUES IN (NULL, 1, 4, 7), and so on. You can insert a row having NULL for column c1 into each of the tables ts2 and ts3:

```
mysql> INSERT INTO ts2 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)
mysql> INSERT INTO ts3 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)
```

By issuing the appropriate query against INFORMATION\_SCHEMA.PARTITIONS, you can determine which partitions were used to store the rows just inserted (we assume, as in the previous examples, that the partitioned tables were created in the p database):

```
mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
 > FROM INFORMATION_SCHEMA.PARTITIONS
 > WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 'ts_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| ts2 | p0 | 0 | 0 | 0 |
| ts2 | p1 | 0 | 0 | 0 |
| ts2 | p2 | 0 | 0 | 0 |
| ts2 | p3 | 1 | 20 | 20 |
| ts3 | p0 | 0 | 0 | 0 |
| ts3 | p1 | 1 | 20 | 20 |
| ts3 | p2 | 0 | 0 | 0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.01 sec)
```

As shown earlier in this section, you can also verify which partitions were used for storing the rows by deleting these partitions and then performing a SELECT.

**Handling of NULL with HASH and KEY partitioning.** NULL is handled somewhat differently for tables partitioned by HASH or KEY. In these cases, any partition expression that yields a NULL value is treated as though its return value were zero. We can verify this behavior by examining the effects on the file system of creating a table partitioned by HASH and populating it with a record containing appropriate values. Suppose that you have a table th (also in the p database) created using the following statement:

```
mysql> CREATE TABLE th (
 -> c1 INT,
 -> c2 VARCHAR(20)
 -> )
 -> PARTITION BY HASH(c1)
 -> PARTITIONS 2;
Query OK, 0 rows affected (0.00 sec)
```

The partitions belonging to this table can be viewed using the query shown here:

```
mysql> SELECT TABLE_NAME,PARTITION_NAME,TABLE_ROWS,AVG_ROW_LENGTH,DATA_LENGTH
 > FROM INFORMATION_SCHEMA.PARTITIONS
 > WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME ='th';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
```

```
| th | p0 | 0 | 0 | 0 |
| th | p1 | 0 | 0 | 0 |
+------------+----------------+------------+----------------+-------------+
2 rows in set (0.00 sec)
```

TABLE\_ROWS for each partition is 0. Now insert two rows into th whose c1 column values are NULL and 0, and verify that these rows were inserted, as shown here:

```
mysql> INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
Query OK, 1 row affected (0.00 sec)
mysql> SELECT * FROM th;
+------+---------+
| c1 | c2 |
+------+---------+
| NULL | mothra |
+------+---------+
| 0 | gigan |
+------+---------+
2 rows in set (0.01 sec)
```

Recall that for any integer N, the value of NULL MOD N is always NULL. For tables that are partitioned by HASH or KEY, this result is treated for determining the correct partition as 0. Checking the Information Schema PARTITIONS table once again, we can see that both rows were inserted into partition p0:

```
mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
 > FROM INFORMATION_SCHEMA.PARTITIONS
 > WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME ='th';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| th | p0 | 2 | 20 | 20 |
| th | p1 | 0 | 0 | 0 |
+------------+----------------+------------+----------------+-------------+
2 rows in set (0.00 sec)
```

By repeating the last example using PARTITION BY KEY in place of PARTITION BY HASH in the definition of the table, you can verify that NULL is also treated like 0 for this type of partitioning.

# <span id="page-115-0"></span>**26.3 Partition Management**

There are a number of ways using SQL statements to modify partitioned tables; it is possible to add, drop, redefine, merge, or split existing partitions using the partitioning extensions to the ALTER TABLE statement. There are also ways to obtain information about partitioned tables and partitions. We discuss these topics in the sections that follow.

- For information about partition management in tables partitioned by RANGE or LIST, see [Section 26.3.1, "Management of RANGE and LIST Partitions".](#page-116-0)
- For a discussion of managing HASH and KEY partitions, see [Section 26.3.2, "Management of HASH](#page-122-0) [and KEY Partitions"](#page-122-0).
- See [Section 26.3.5, "Obtaining Information About Partitions",](#page-131-0) for a discussion of mechanisms provided in MySQL 8.0 for obtaining information about partitioned tables and partitions.
- For a discussion of performing maintenance operations on partitions, see [Section 26.3.4,](#page-130-0) ["Maintenance of Partitions"](#page-130-0).

![](_page_115_Picture_13.jpeg)

### **Note**

All partitions of a partitioned table must have the same number of subpartitions; it is not possible to change the subpartitioning once the table has been created.

To change a table's partitioning scheme, it is necessary only to use the ALTER TABLE statement with a partition\_options option, which has the same syntax as that as used with CREATE TABLE

for creating a partitioned table; this option (also) always begins with the keywords PARTITION BY. Suppose that the following CREATE TABLE statement was used to create a table that is partitioned by range:

```
CREATE TABLE trb3 (id INT, name VARCHAR(50), purchased DATE)
 PARTITION BY RANGE( YEAR(purchased) ) (
 PARTITION p0 VALUES LESS THAN (1990),
 PARTITION p1 VALUES LESS THAN (1995),
 PARTITION p2 VALUES LESS THAN (2000),
 PARTITION p3 VALUES LESS THAN (2005)
 );
```

To repartition this table so that it is partitioned by key into two partitions using the id column value as the basis for the key, you can use this statement:

```
ALTER TABLE trb3 PARTITION BY KEY(id) PARTITIONS 2;
```

This has the same effect on the structure of the table as dropping the table and re-creating it using CREATE TABLE trb3 PARTITION BY KEY(id) PARTITIONS 2;.

ALTER TABLE ... ENGINE = ... changes only the storage engine used by the table, and leaves the table's partitioning scheme intact. The statement succeeds only if the target storage engine provides partitioning support. You can use ALTER TABLE ... REMOVE PARTITIONING to remove a table's partitioning; see Section 15.1.9, "ALTER TABLE Statement".

![](_page_116_Picture_7.jpeg)

#### **Important**

Only a single PARTITION BY, ADD PARTITION, DROP PARTITION, REORGANIZE PARTITION, or COALESCE PARTITION clause can be used in a given ALTER TABLE statement. If you (for example) wish to drop a partition and reorganize a table's remaining partitions, you must do so in two separate ALTER TABLE statements (one using DROP PARTITION and then a second one using REORGANIZE PARTITION).

You can delete all rows from one or more selected partitions using ALTER TABLE ... TRUNCATE PARTITION.

# <span id="page-116-0"></span>**26.3.1 Management of RANGE and LIST Partitions**

Adding and dropping of range and list partitions are handled in a similar fashion, so we discuss the management of both sorts of partitioning in this section. For information about working with tables that are partitioned by hash or key, see [Section 26.3.2, "Management of HASH and KEY Partitions"](#page-122-0).

Dropping a partition from a table that is partitioned by either RANGE or by LIST can be accomplished using the ALTER TABLE statement with the DROP PARTITION option. Suppose that you have created a table that is partitioned by range and then populated with 10 records using the following CREATE TABLE and INSERT statements:

```
mysql> CREATE TABLE tr (id INT, name VARCHAR(50), purchased DATE)
 -> PARTITION BY RANGE( YEAR(purchased) ) (
 -> PARTITION p0 VALUES LESS THAN (1990),
 -> PARTITION p1 VALUES LESS THAN (1995),
 -> PARTITION p2 VALUES LESS THAN (2000),
 -> PARTITION p3 VALUES LESS THAN (2005),
 -> PARTITION p4 VALUES LESS THAN (2010),
 -> PARTITION p5 VALUES LESS THAN (2015)
 -> );
Query OK, 0 rows affected (0.28 sec)
mysql> INSERT INTO tr VALUES
 -> (1, 'desk organiser', '2003-10-15'),
 -> (2, 'alarm clock', '1997-11-05'),
 -> (3, 'chair', '2009-03-10'),
 -> (4, 'bookcase', '1989-01-10'),
 -> (5, 'exercise bike', '2014-05-09'),
 -> (6, 'sofa', '1987-06-05'),
```

```
 -> (7, 'espresso maker', '2011-11-22'),
 -> (8, 'aquarium', '1992-08-04'),
 -> (9, 'study desk', '2006-09-16'),
 -> (10, 'lava lamp', '1998-12-25');
Query OK, 10 rows affected (0.05 sec)
Records: 10 Duplicates: 0 Warnings: 0
```

You can see which items should have been inserted into partition p2 as shown here:

```
mysql> SELECT * FROM tr
 -> WHERE purchased BETWEEN '1995-01-01' AND '1999-12-31';
+------+-------------+------------+
| id | name | purchased |
+------+-------------+------------+
| 2 | alarm clock | 1997-11-05 |
| 10 | lava lamp | 1998-12-25 |
+------+-------------+------------+
2 rows in set (0.00 sec)
```

You can also get this information using partition selection, as shown here:

```
mysql> SELECT * FROM tr PARTITION (p2);
+------+-------------+------------+
| id | name | purchased |
+------+-------------+------------+
| 2 | alarm clock | 1997-11-05 |
| 10 | lava lamp | 1998-12-25 |
+------+-------------+------------+
2 rows in set (0.00 sec)
```

See [Section 26.5, "Partition Selection",](#page-136-0) for more information.

To drop the partition named p2, execute the following command:

```
mysql> ALTER TABLE tr DROP PARTITION p2;
Query OK, 0 rows affected (0.03 sec)
```

![](_page_117_Picture_9.jpeg)

#### **Note**

The NDBCLUSTER storage engine does not support ALTER TABLE ... DROP PARTITION. It does, however, support the other partitioning-related extensions to ALTER TABLE that are described in this chapter.

It is very important to remember that, when you drop a partition, you also delete all the data that was stored in that partition. You can see that this is the case by re-running the previous SELECT query:

```
mysql> SELECT * FROM tr WHERE purchased
 -> BETWEEN '1995-01-01' AND '1999-12-31';
Empty set (0.00 sec)
```

![](_page_117_Picture_14.jpeg)

#### **Note**

DROP PARTITION is supported by native partitioning in-place APIs and may be used with ALGORITHM={COPY|INPLACE}. DROP PARTITION with ALGORITHM=INPLACE deletes data stored in the partition and drops the partition. However, DROP PARTITION with ALGORITHM=COPY or old\_alter\_table=ON rebuilds the partitioned table and attempts to move data from the dropped partition to another partition with a compatible PARTITION ... VALUES definition. Data that cannot be moved to another partition is deleted.

Because of this, you must have the DROP privilege for a table before you can execute ALTER TABLE ... DROP PARTITION on that table.

If you wish to drop all data from all partitions while preserving the table definition and its partitioning scheme, use the TRUNCATE TABLE statement. (See Section 15.1.37, "TRUNCATE TABLE Statement".)

If you intend to change the partitioning of a table without losing data, use ALTER TABLE ... REORGANIZE PARTITION instead. See below or in Section 15.1.9, "ALTER TABLE Statement", for information about REORGANIZE PARTITION.

If you now execute a SHOW CREATE TABLE statement, you can see how the partitioning makeup of the table has been changed:

```
mysql> SHOW CREATE TABLE tr\G
*************************** 1. row ***************************
 Table: tr
Create Table: CREATE TABLE `tr` (
 `id` int(11) DEFAULT NULL,
 `name` varchar(50) DEFAULT NULL,
 `purchased` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(purchased))
(PARTITION p0 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1995) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2005) ENGINE = InnoDB,
 PARTITION p4 VALUES LESS THAN (2010) ENGINE = InnoDB,
 PARTITION p5 VALUES LESS THAN (2015) ENGINE = InnoDB) */
1 row in set (0.00 sec)
```

When you insert new rows into the changed table with purchased column values between '1995-01-01' and '2004-12-31' inclusive, those rows are stored in partition p3. You can verify this as follows:

```
mysql> INSERT INTO tr VALUES (11, 'pencil holder', '1995-07-12');
Query OK, 1 row affected (0.00 sec)
mysql> SELECT * FROM tr WHERE purchased
 -> BETWEEN '1995-01-01' AND '2004-12-31';
+------+----------------+------------+
| id | name | purchased |
+------+----------------+------------+
| 1 | desk organiser | 2003-10-15 |
| 11 | pencil holder | 1995-07-12 |
+------+----------------+------------+
2 rows in set (0.00 sec)
mysql> ALTER TABLE tr DROP PARTITION p3;
Query OK, 0 rows affected (0.03 sec)
mysql> SELECT * FROM tr WHERE purchased
 -> BETWEEN '1995-01-01' AND '2004-12-31';
Empty set (0.00 sec)
```

The number of rows dropped from the table as a result of ALTER TABLE ... DROP PARTITION is not reported by the server as it would be by the equivalent DELETE query.

Dropping LIST partitions uses exactly the same ALTER TABLE ... DROP PARTITION syntax as used for dropping RANGE partitions. However, there is one important difference in the effect this has on your use of the table afterward: You can no longer insert into the table any rows having any of the values that were included in the value list defining the deleted partition. (See [Section 26.2.2, "LIST](#page-95-0) [Partitioning"](#page-95-0), for an example.)

To add a new range or list partition to a previously partitioned table, use the ALTER TABLE ... ADD PARTITION statement. For tables which are partitioned by RANGE, this can be used to add a new range to the end of the list of existing partitions. Suppose that you have a partitioned table containing membership data for your organization, which is defined as follows:

```
CREATE TABLE members (
 id INT,
 fname VARCHAR(25),
 lname VARCHAR(25),
 dob DATE
)
```

```
PARTITION BY RANGE( YEAR(dob) ) (
 PARTITION p0 VALUES LESS THAN (1980),
 PARTITION p1 VALUES LESS THAN (1990),
 PARTITION p2 VALUES LESS THAN (2000)
);
```

Suppose further that the minimum age for members is 16. As the calendar approaches the end of 2015, you realize that you must soon be prepared to admit members who were born in 2000 (and later). You can modify the members table to accommodate new members born in the years 2000 to 2010 as shown here:

```
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

With tables that are partitioned by range, you can use ADD PARTITION to add new partitions to the high end of the partitions list only. Trying to add a new partition in this manner between or before existing partitions results in an error as shown here:

```
mysql> ALTER TABLE members
 > ADD PARTITION (
 > PARTITION n VALUES LESS THAN (1970));
ERROR 1463 (HY000): VALUES LESS THAN value must be strictly »
 increasing for each partition
```

You can work around this problem by reorganizing the first partition into two new ones that split the range between them, like this:

```
ALTER TABLE members
 REORGANIZE PARTITION p0 INTO (
 PARTITION n0 VALUES LESS THAN (1970),
 PARTITION n1 VALUES LESS THAN (1980)
);
```

Using SHOW CREATE TABLE you can see that the ALTER TABLE statement has had the desired effect:

```
mysql> SHOW CREATE TABLE members\G
*************************** 1. row ***************************
 Table: members
Create Table: CREATE TABLE `members` (
 `id` int(11) DEFAULT NULL,
 `fname` varchar(25) DEFAULT NULL,
 `lname` varchar(25) DEFAULT NULL,
 `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(dob))
(PARTITION n0 VALUES LESS THAN (1970) ENGINE = InnoDB,
 PARTITION n1 VALUES LESS THAN (1980) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2010) ENGINE = InnoDB) */
1 row in set (0.00 sec)
```

See also Section 15.1.9.1, "ALTER TABLE Partition Operations".

You can also use ALTER TABLE ... ADD PARTITION to add new partitions to a table that is partitioned by LIST. Suppose a table tt is defined using the following CREATE TABLE statement:

```
CREATE TABLE tt (
 id INT,
 data INT
)
PARTITION BY LIST(data) (
 PARTITION p0 VALUES IN (5, 10, 15),
 PARTITION p1 VALUES IN (6, 12, 18)
);
```

You can add a new partition in which to store rows having the data column values 7, 14, and 21 as shown:

```
ALTER TABLE tt ADD PARTITION (PARTITION p2 VALUES IN (7, 14, 21));
```

Keep in mind that you cannot add a new LIST partition encompassing any values that are already included in the value list of an existing partition. If you attempt to do so, an error results:

```
mysql> ALTER TABLE tt ADD PARTITION 
 > (PARTITION np VALUES IN (4, 8, 12));
ERROR 1465 (HY000): Multiple definition of same constant »
 in list partitioning
```

Because any rows with the data column value 12 have already been assigned to partition p1, you cannot create a new partition on table tt that includes 12 in its value list. To accomplish this, you could drop p1, and add np and then a new p1 with a modified definition. However, as discussed earlier, this would result in the loss of all data stored in p1—and it is often the case that this is not what you really want to do. Another solution might appear to be to make a copy of the table with the new partitioning and to copy the data into it using CREATE TABLE ... SELECT ..., then drop the old table and rename the new one, but this could be very time-consuming when dealing with a large amounts of data. This also might not be feasible in situations where high availability is a requirement.

You can add multiple partitions in a single ALTER TABLE ... ADD PARTITION statement as shown here:

```
CREATE TABLE employees (
 id INT NOT NULL,
 fname VARCHAR(50) NOT NULL,
 lname VARCHAR(50) NOT NULL,
 hired DATE NOT NULL
)
PARTITION BY RANGE( YEAR(hired) ) (
 PARTITION p1 VALUES LESS THAN (1991),
 PARTITION p2 VALUES LESS THAN (1996),
 PARTITION p3 VALUES LESS THAN (2001),
 PARTITION p4 VALUES LESS THAN (2005)
);
ALTER TABLE employees ADD PARTITION (
 PARTITION p5 VALUES LESS THAN (2010),
 PARTITION p6 VALUES LESS THAN MAXVALUE
);
```

Fortunately, MySQL's partitioning implementation provides ways to redefine partitions without losing data. Let us look first at a couple of simple examples involving RANGE partitioning. Recall the members table which is now defined as shown here:

```
mysql> SHOW CREATE TABLE members\G
*************************** 1. row ***************************
 Table: members
Create Table: CREATE TABLE `members` (
 `id` int(11) DEFAULT NULL,
 `fname` varchar(25) DEFAULT NULL,
 `lname` varchar(25) DEFAULT NULL,
 `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(dob))
(PARTITION n0 VALUES LESS THAN (1970) ENGINE = InnoDB,
 PARTITION n1 VALUES LESS THAN (1980) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2010) ENGINE = InnoDB) */
1 row in set (0.00 sec)
```

Suppose that you would like to move all rows representing members born before 1960 into a separate partition. As we have already seen, this cannot be done using ALTER TABLE ... ADD PARTITION. However, you can use another partition-related extension to ALTER TABLE to accomplish this:

```
ALTER TABLE members REORGANIZE PARTITION n0 INTO (
 PARTITION s0 VALUES LESS THAN (1960),
 PARTITION s1 VALUES LESS THAN (1970)
```

);

In effect, this command splits partition n0 into two new partitions s0 and s1. It also moves the data that was stored in n0 into the new partitions according to the rules embodied in the two PARTITION ... VALUES ... clauses, so that s0 contains only those records for which YEAR(dob) is less than 1960 and s1 contains those rows in which YEAR(dob) is greater than or equal to 1960 but less than 1970.

A REORGANIZE PARTITION clause may also be used for merging adjacent partitions. You can reverse the effect of the previous statement on the members table as shown here:

```
ALTER TABLE members REORGANIZE PARTITION s0,s1 INTO (
 PARTITION p0 VALUES LESS THAN (1970)
);
```

No data is lost in splitting or merging partitions using REORGANIZE PARTITION. In executing the above statement, MySQL moves all of the records that were stored in partitions s0 and s1 into partition p0.

The general syntax for REORGANIZE PARTITION is shown here:

```
ALTER TABLE tbl_name
 REORGANIZE PARTITION partition_list
 INTO (partition_definitions);
```

Here, tbl\_name is the name of the partitioned table, and partition\_list is a comma-separated list of names of one or more existing partitions to be changed. partition\_definitions is a comma-separated list of new partition definitions, which follow the same rules as for the partition\_definitions list used in CREATE TABLE. You are not limited to merging several partitions into one, or to splitting one partition into many, when using REORGANIZE PARTITION. For example, you can reorganize all four partitions of the members table into two, like this:

```
ALTER TABLE members REORGANIZE PARTITION p0,p1,p2,p3 INTO (
 PARTITION m0 VALUES LESS THAN (1980),
 PARTITION m1 VALUES LESS THAN (2000)
);
```

You can also use REORGANIZE PARTITION with tables that are partitioned by LIST. Let us return to the problem of adding a new partition to the list-partitioned tt table and failing because the new partition had a value that was already present in the value-list of one of the existing partitions. We can handle this by adding a partition that contains only nonconflicting values, and then reorganizing the new partition and the existing one so that the value which was stored in the existing one is now moved to the new one:

```
ALTER TABLE tt ADD PARTITION (PARTITION np VALUES IN (4, 8));
ALTER TABLE tt REORGANIZE PARTITION p1,np INTO (
 PARTITION p1 VALUES IN (6, 18),
 PARTITION np VALUES in (4, 8, 12)
);
```

Here are some key points to keep in mind when using ALTER TABLE ... REORGANIZE PARTITION to repartition tables that are partitioned by RANGE or LIST:

• The PARTITION options used to determine the new partitioning scheme are subject to the same rules as those used with a CREATE TABLE statement.

A new RANGE partitioning scheme cannot have any overlapping ranges; a new LIST partitioning scheme cannot have any overlapping sets of values.

• The combination of partitions in the partition\_definitions list should account for the same range or set of values overall as the combined partitions named in the partition\_list.

For example, partitions p1 and p2 together cover the years 1980 through 1999 in the members table used as an example in this section. Any reorganization of these two partitions should cover the same range of years overall.

• For tables partitioned by RANGE, you can reorganize only adjacent partitions; you cannot skip range partitions.

For instance, you could not reorganize the example members table using a statement beginning with ALTER TABLE members REORGANIZE PARTITION p0,p2 INTO ... because p0 covers the years prior to 1970 and p2 the years from 1990 through 1999 inclusive, so these are not adjacent partitions. (You cannot skip partition p1 in this case.)

• You cannot use REORGANIZE PARTITION to change the type of partitioning used by the table (for example, you cannot change RANGE partitions to HASH partitions or the reverse). You also cannot use this statement to change the partitioning expression or column. To accomplish either of these tasks without dropping and re-creating the table, you can use ALTER TABLE ... PARTITION BY ..., as shown here:

```
ALTER TABLE members
 PARTITION BY HASH( YEAR(dob) )
 PARTITIONS 8;
```

# <span id="page-122-0"></span>**26.3.2 Management of HASH and KEY Partitions**

Tables which are partitioned by hash or by key are very similar to one another with regard to making changes in a partitioning setup, and both differ in a number of ways from tables which have been partitioned by range or list. For that reason, this section addresses the modification of tables partitioned by hash or by key only. For a discussion of adding and dropping of partitions of tables that are partitioned by range or list, see [Section 26.3.1, "Management of RANGE and LIST Partitions"](#page-116-0).

You cannot drop partitions from tables that are partitioned by HASH or KEY in the same way that you can from tables that are partitioned by RANGE or LIST. However, you can merge HASH or KEY partitions using ALTER TABLE ... COALESCE PARTITION. Suppose that a clients table containing data about clients is divided into 12 partitions, created as shown here:

```
CREATE TABLE clients (
 id INT,
 fname VARCHAR(30),
 lname VARCHAR(30),
 signed DATE
)
PARTITION BY HASH( MONTH(signed) )
PARTITIONS 12;
```

To reduce the number of partitions from 12 to 8, execute the following ALTER TABLE statement:

```
mysql> ALTER TABLE clients COALESCE PARTITION 4;
Query OK, 0 rows affected (0.02 sec)
```

COALESCE works equally well with tables that are partitioned by HASH, KEY, LINEAR HASH, or LINEAR KEY. Here is an example similar to the previous one, differing only in that the table is partitioned by LINEAR KEY:

```
mysql> CREATE TABLE clients_lk (
 -> id INT,
 -> fname VARCHAR(30),
 -> lname VARCHAR(30),
 -> signed DATE
 -> )
 -> PARTITION BY LINEAR KEY(signed)
 -> PARTITIONS 12;
Query OK, 0 rows affected (0.03 sec)
mysql> ALTER TABLE clients_lk COALESCE PARTITION 4;
Query OK, 0 rows affected (0.06 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

The number following COALESCE PARTITION is the number of partitions to merge into the remainder —in other words, it is the number of partitions to remove from the table.

Attempting to remove more partitions than are in the table results in an error like this one:

```
mysql> ALTER TABLE clients COALESCE PARTITION 18;
ERROR 1478 (HY000): Cannot remove all partitions, use DROP TABLE instead
```

To increase the number of partitions for the clients table from 12 to 18, use ALTER TABLE ... ADD PARTITION as shown here:

ALTER TABLE clients ADD PARTITION PARTITIONS 6;

## <span id="page-123-0"></span>**26.3.3 Exchanging Partitions and Subpartitions with Tables**

In MySQL 8.0, it is possible to exchange a table partition or subpartition with a table using ALTER TABLE pt EXCHANGE PARTITION p WITH TABLE nt, where pt is the partitioned table and p is the partition or subpartition of pt to be exchanged with unpartitioned table nt, provided that the following statements are true:

- 1. Table nt is not itself partitioned.
- 2. Table nt is not a temporary table.
- 3. The structures of tables pt and nt are otherwise identical.
- 4. Table nt contains no foreign key references, and no other table has any foreign keys that refer to nt.
- 5. There are no rows in nt that lie outside the boundaries of the partition definition for p. This condition does not apply if WITHOUT VALIDATION is used.
- 6. Both tables must use the same character set and collation.
- 7. For InnoDB tables, both tables must use the same row format. To determine the row format of an InnoDB table, query INFORMATION\_SCHEMA.INNODB\_TABLES.
- 8. Any partition-level MAX\_ROWS setting for p must be the same as the table-level MAX\_ROWS value set for nt. The setting for any partition-level MIN\_ROWS setting for p must also be the same any tablelevel MIN\_ROWS value set for nt.

This is true in either case whether not pt has an explicit table-level MAX\_ROWS or MIN\_ROWS option in effect.

- 9. The AVG\_ROW\_LENGTH cannot differ between the two tables pt and nt.
- 10. pt does not have any partitions that use the DATA DIRECTORY option. This restriction is lifted for InnoDB tables in MySQL 8.0.14 and later.
- 11. INDEX DIRECTORY cannot differ between the table and the partition to be exchanged with it.
- 12. No table or partition TABLESPACE options can be used in either of the tables.

In addition to the ALTER, INSERT, and CREATE privileges usually required for ALTER TABLE statements, you must have the DROP privilege to perform ALTER TABLE ... EXCHANGE PARTITION.

You should also be aware of the following effects of ALTER TABLE ... EXCHANGE PARTITION:

- Executing ALTER TABLE ... EXCHANGE PARTITION does not invoke any triggers on either the partitioned table or the table to be exchanged.
- Any AUTO\_INCREMENT columns in the exchanged table are reset.
- The IGNORE keyword has no effect when used with ALTER TABLE ... EXCHANGE PARTITION.

The syntax for ALTER TABLE ... EXCHANGE PARTITION is shown here, where pt is the partitioned table, p is the partition (or subpartition) to be exchanged, and nt is the nonpartitioned table to be exchanged with p:

```
ALTER TABLE pt
 EXCHANGE PARTITION p
 WITH TABLE nt;
```

Optionally, you can append WITH VALIDATION or WITHOUT VALIDATION. When WITHOUT VALIDATION is specified, the ALTER TABLE ... EXCHANGE PARTITION operation does not perform any row-by-row validation when exchanging a partition a nonpartitioned table, allowing database administrators to assume responsibility for ensuring that rows are within the boundaries of the partition definition. WITH VALIDATION is the default.

One and only one partition or subpartition may be exchanged with one and only one nonpartitioned table in a single ALTER TABLE EXCHANGE PARTITION statement. To exchange multiple partitions or subpartitions, use multiple ALTER TABLE EXCHANGE PARTITION statements. EXCHANGE PARTITION may not be combined with other ALTER TABLE options. The partitioning and (if applicable) subpartitioning used by the partitioned table may be of any type or types supported in MySQL 8.0.

## **Exchanging a Partition with a Nonpartitioned Table**

Suppose that a partitioned table e has been created and populated using the following SQL statements:

```
CREATE TABLE e (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30)
)
 PARTITION BY RANGE (id) (
 PARTITION p0 VALUES LESS THAN (50),
 PARTITION p1 VALUES LESS THAN (100),
 PARTITION p2 VALUES LESS THAN (150),
 PARTITION p3 VALUES LESS THAN (MAXVALUE)
);
INSERT INTO e VALUES
 (1669, "Jim", "Smith"),
 (337, "Mary", "Jones"),
 (16, "Frank", "White"),
 (2005, "Linda", "Black");
```

Now we create a nonpartitioned copy of e named e2. This can be done using the mysql client as shown here:

```
mysql> CREATE TABLE e2 LIKE e;
Query OK, 0 rows affected (0.04 sec)
mysql> ALTER TABLE e2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.07 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

You can see which partitions in table e contain rows by querying the Information Schema PARTITIONS table, like this:

```
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 FROM INFORMATION_SCHEMA.PARTITIONS
 WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 1 |
| p1 | 0 |
| p2 | 0 |
| p3 | 3 |
```

+----------------+------------+ 2 rows in set (0.00 sec)

![](_page_125_Picture_2.jpeg)

#### **Note**

For partitioned InnoDB tables, the row count given in the TABLE\_ROWS column of the Information Schema PARTITIONS table is only an estimated value used in SQL optimization, and is not always exact.

To exchange partition p0 in table e with table e2, you can use ALTER TABLE, as shown here:

```
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
Query OK, 0 rows affected (0.04 sec)
```

More precisely, the statement just issued causes any rows found in the partition to be swapped with those found in the table. You can observe how this has happened by querying the Information Schema PARTITIONS table, as before. The table row that was previously found in partition p0 is no longer present:

```
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 FROM INFORMATION_SCHEMA.PARTITIONS
 WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 0 |
| p1 | 0 |
| p2 | 0 |
| p3 | 3 |
+----------------+------------+
4 rows in set (0.00 sec)
```

If you query table e2, you can see that the "missing" row can now be found there:

```
mysql> SELECT * FROM e2;
+----+-------+-------+
| id | fname | lname |
+----+-------+-------+
| 16 | Frank | White |
+----+-------+-------+
1 row in set (0.00 sec)
```

The table to be exchanged with the partition does not necessarily have to be empty. To demonstrate this, we first insert a new row into table e, making sure that this row is stored in partition p0 by choosing an id column value that is less than 50, and verifying this afterward by querying the PARTITIONS table:

```
mysql> INSERT INTO e VALUES (41, "Michael", "Green");
Query OK, 1 row affected (0.05 sec)
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 FROM INFORMATION_SCHEMA.PARTITIONS
 WHERE TABLE_NAME = 'e'; 
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 1 |
| p1 | 0 |
| p2 | 0 |
| p3 | 3 |
+----------------+------------+
4 rows in set (0.00 sec)
```

Now we once again exchange partition p0 with table e2 using the same ALTER TABLE statement as previously:

```
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
Query OK, 0 rows affected (0.28 sec)
```

The output of the following queries shows that the table row that was stored in partition p0 and the table row that was stored in table e2, prior to issuing the ALTER TABLE statement, have now switched places:

```
mysql> SELECT * FROM e;
+------+-------+-------+
| id | fname | lname |
+------+-------+-------+
| 16 | Frank | White |
| 1669 | Jim | Smith |
| 337 | Mary | Jones |
| 2005 | Linda | Black |
+------+-------+-------+
4 rows in set (0.00 sec)
mysql> SELECT PARTITION_NAME, TABLE_ROWS
 FROM INFORMATION_SCHEMA.PARTITIONS
 WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 1 |
| p1 | 0 |
| p2 | 0 |
| p3 | 3 |
+----------------+------------+
4 rows in set (0.00 sec)
mysql> SELECT * FROM e2;
+----+---------+-------+
| id | fname | lname |
+----+---------+-------+
| 41 | Michael | Green |
+----+---------+-------+
1 row in set (0.00 sec)
```

## **Nonmatching Rows**

You should keep in mind that any rows found in the nonpartitioned table prior to issuing the ALTER TABLE ... EXCHANGE PARTITION statement must meet the conditions required for them to be stored in the target partition; otherwise, the statement fails. To see how this occurs, first insert a row into e2 that is outside the boundaries of the partition definition for partition p0 of table e. For example, insert a row with an id column value that is too large; then, try to exchange the table with the partition again:

```
mysql> INSERT INTO e2 VALUES (51, "Ellen", "McDonald");
Query OK, 1 row affected (0.08 sec)
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
ERROR 1707 (HY000): Found row that does not match the partition
```

Only the WITHOUT VALIDATION option would permit this operation to succeed:

```
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2 WITHOUT VALIDATION;
Query OK, 0 rows affected (0.02 sec)
```

When a partition is exchanged with a table that contains rows that do not match the partition definition, it is the responsibility of the database administrator to fix the non-matching rows, which can be performed using REPAIR TABLE or ALTER TABLE ... REPAIR PARTITION.

### **Exchanging Partitions Without Row-By-Row Validation**

To avoid time consuming validation when exchanging a partition with a table that has many rows, it is possible to skip the row-by-row validation step by appending WITHOUT VALIDATION to the ALTER TABLE ... EXCHANGE PARTITION statement.

The following example compares the difference between execution times when exchanging a partition with a nonpartitioned table, with and without validation. The partitioned table (table e) contains two

partitions of 1 million rows each. The rows in p0 of table e are removed and p0 is exchanged with a nonpartitioned table of 1 million rows. The WITH VALIDATION operation takes 0.74 seconds. By comparison, the WITHOUT VALIDATION operation takes 0.01 seconds.

```
# Create a partitioned table with 1 million rows in each partition
CREATE TABLE e (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30)
)
 PARTITION BY RANGE (id) (
 PARTITION p0 VALUES LESS THAN (1000001),
 PARTITION p1 VALUES LESS THAN (2000001),
);
mysql> SELECT COUNT(*) FROM e;
| COUNT(*) |
+----------+
| 2000000 |
+----------+
1 row in set (0.27 sec)
# View the rows in each partition
SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+-------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+-------------+
| p0 | 1000000 |
| p1 | 1000000 |
+----------------+-------------+
2 rows in set (0.00 sec)
# Create a nonpartitioned table of the same structure and populate it with 1 million rows
CREATE TABLE e2 (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30)
);
mysql> SELECT COUNT(*) FROM e2;
+----------+
| COUNT(*) |
+----------+
| 1000000 |
+----------+
1 row in set (0.24 sec)
# Create another nonpartitioned table of the same structure and populate it with 1 million rows
CREATE TABLE e3 (
 id INT NOT NULL,
 fname VARCHAR(30),
 lname VARCHAR(30)
);
mysql> SELECT COUNT(*) FROM e3;
+----------+
| COUNT(*) |
+----------+
| 1000000 |
+----------+
1 row in set (0.25 sec)
# Drop the rows from p0 of table e
mysql> DELETE FROM e WHERE id < 1000001;
Query OK, 1000000 rows affected (5.55 sec)
# Confirm that there are no rows in partition p0
```

```
mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 0 |
| p1 | 1000000 |
+----------------+------------+
2 rows in set (0.00 sec)
# Exchange partition p0 of table e with the table e2 'WITH VALIDATION'
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2 WITH VALIDATION;
Query OK, 0 rows affected (0.74 sec)
# Confirm that the partition was exchanged with table e2
mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 1000000 |
| p1 | 1000000 |
+----------------+------------+
2 rows in set (0.00 sec)
# Once again, drop the rows from p0 of table e
mysql> DELETE FROM e WHERE id < 1000001;
Query OK, 1000000 rows affected (5.55 sec)
# Confirm that there are no rows in partition p0
mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 0 |
| p1 | 1000000 |
+----------------+------------+
2 rows in set (0.00 sec)
# Exchange partition p0 of table e with the table e3 'WITHOUT VALIDATION'
mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e3 WITHOUT VALIDATION;
Query OK, 0 rows affected (0.01 sec)
# Confirm that the partition was exchanged with table e3
mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0 | 1000000 |
| p1 | 1000000 |
+----------------+------------+
2 rows in set (0.00 sec)
```

If a partition is exchanged with a table that contains rows that do not match the partition definition, it is the responsibility of the database administrator to fix the non-matching rows, which can be performed using REPAIR TABLE or ALTER TABLE ... REPAIR PARTITION.

### **Exchanging a Subpartition with a Nonpartitioned Table**

You can also exchange a subpartition of a subpartitioned table (see [Section 26.2.6, "Subpartitioning"](#page-109-0)) with a nonpartitioned table using an ALTER TABLE ... EXCHANGE PARTITION statement. In the following example, we first create a table es that is partitioned by RANGE and subpartitioned by KEY, populate this table as we did table e, and then create an empty, nonpartitioned copy es2 of the table, as shown here:

```
mysql> CREATE TABLE es (
 -> id INT NOT NULL,
 -> fname VARCHAR(30),
 -> lname VARCHAR(30)
 -> )
 -> PARTITION BY RANGE (id)
 -> SUBPARTITION BY KEY (lname)
 -> SUBPARTITIONS 2 (
 -> PARTITION p0 VALUES LESS THAN (50),
 -> PARTITION p1 VALUES LESS THAN (100),
 -> PARTITION p2 VALUES LESS THAN (150),
 -> PARTITION p3 VALUES LESS THAN (MAXVALUE)
 -> );
Query OK, 0 rows affected (2.76 sec)
mysql> INSERT INTO es VALUES
 -> (1669, "Jim", "Smith"),
 -> (337, "Mary", "Jones"),
 -> (16, "Frank", "White"),
 -> (2005, "Linda", "Black");
Query OK, 4 rows affected (0.04 sec)
Records: 4 Duplicates: 0 Warnings: 0
mysql> CREATE TABLE es2 LIKE es;
Query OK, 0 rows affected (1.27 sec)
mysql> ALTER TABLE es2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.70 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

Although we did not explicitly name any of the subpartitions when creating table es, we can obtain generated names for these by including the SUBPARTITION\_NAME column of the PARTITIONS table from INFORMATION\_SCHEMA when selecting from that table, as shown here:

```
mysql> SELECT PARTITION_NAME, SUBPARTITION_NAME, TABLE_ROWS
 -> FROM INFORMATION_SCHEMA.PARTITIONS
 -> WHERE TABLE_NAME = 'es';
+----------------+-------------------+------------+
| PARTITION_NAME | SUBPARTITION_NAME | TABLE_ROWS |
+----------------+-------------------+------------+
| p0 | p0sp0 | 1 |
| p0 | p0sp1 | 0 |
| p1 | p1sp0 | 0 |
| p1 | p1sp1 | 0 |
| p2 | p2sp0 | 0 |
| p2 | p2sp1 | 0 |
| p3 | p3sp0 | 3 |
| p3 | p3sp1 | 0 |
+----------------+-------------------+------------+
8 rows in set (0.00 sec)
```

The following ALTER TABLE statement exchanges subpartition p3sp0 in table es with the nonpartitioned table es2:

```
mysql> ALTER TABLE es EXCHANGE PARTITION p3sp0 WITH TABLE es2;
Query OK, 0 rows affected (0.29 sec)
```

You can verify that the rows were exchanged by issuing the following queries:

```
mysql> SELECT PARTITION_NAME, SUBPARTITION_NAME, TABLE_ROWS
 -> FROM INFORMATION_SCHEMA.PARTITIONS
 -> WHERE TABLE_NAME = 'es';
+----------------+-------------------+------------+
| PARTITION_NAME | SUBPARTITION_NAME | TABLE_ROWS |
+----------------+-------------------+------------+
| p0 | p0sp0 | 1 |
| p0 | p0sp1 | 0 |
| p1 | p1sp0 | 0 |
| p1 | p1sp1 | 0 |
| p2 | p2sp0 | 0 |
| p2 | p2sp1 | 0 |
```

```
| p3 | p3sp0 | 0 |
| p3 | p3sp1 | 0 |
+----------------+-------------------+------------+
8 rows in set (0.00 sec)
mysql> SELECT * FROM es2;
+------+-------+-------+
| id | fname | lname |
+------+-------+-------+
| 1669 | Jim | Smith |
| 337 | Mary | Jones |
| 2005 | Linda | Black |
+------+-------+-------+
3 rows in set (0.00 sec)
```

If a table is subpartitioned, you can exchange only a subpartition of the table—not an entire partition with an unpartitioned table, as shown here:

```
mysql> ALTER TABLE es EXCHANGE PARTITION p3 WITH TABLE es2;
ERROR 1704 (HY000): Subpartitioned table, use subpartition instead of partition
```

Table structures are compared in a strict fashion; the number, order, names, and types of columns and indexes of the partitioned table and the nonpartitioned table must match exactly. In addition, both tables must use the same storage engine:

```
mysql> CREATE TABLE es3 LIKE e;
Query OK, 0 rows affected (1.31 sec)
mysql> ALTER TABLE es3 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.53 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW CREATE TABLE es3\G
*************************** 1. row ***************************
 Table: es3
Create Table: CREATE TABLE `es3` (
 `id` int(11) NOT NULL,
 `fname` varchar(30) DEFAULT NULL,
 `lname` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> ALTER TABLE es3 ENGINE = MyISAM;
Query OK, 0 rows affected (0.15 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> ALTER TABLE es EXCHANGE PARTITION p3sp0 WITH TABLE es3;
ERROR 1497 (HY000): The mix of handlers in the partitions is not allowed in this version of MySQL
```

## <span id="page-130-0"></span>**26.3.4 Maintenance of Partitions**

A number of table and partition maintenance tasks can be carried out on partitioned tables using SQL statements intended for such purposes.

Table maintenance of partitioned tables can be accomplished using the statements CHECK TABLE, OPTIMIZE TABLE, ANALYZE TABLE, and REPAIR TABLE, which are supported for partitioned tables.

You can use a number of extensions to ALTER TABLE for performing operations of this type on one or more partitions directly, as described in the following list:

• **Rebuilding partitions.** Rebuilds the partition; this has the same effect as dropping all records stored in the partition, then reinserting them. This can be useful for purposes of defragmentation.

Example:

```
ALTER TABLE t1 REBUILD PARTITION p0, p1;
```

• **Optimizing partitions.** If you have deleted a large number of rows from a partition or if you have made many changes to a partitioned table with variable-length rows (that is, having VARCHAR, BLOB, or TEXT columns), you can use ALTER TABLE ... OPTIMIZE PARTITION to reclaim any unused space and to defragment the partition data file.

#### Example:

ALTER TABLE t1 OPTIMIZE PARTITION p0, p1;

Using OPTIMIZE PARTITION on a given partition is equivalent to running CHECK PARTITION, ANALYZE PARTITION, and REPAIR PARTITION on that partition.

Some MySQL storage engines, including InnoDB, do not support per-partition optimization; in these cases, ALTER TABLE ... OPTIMIZE PARTITION analyzes and rebuilds the entire table, and causes an appropriate warning to be issued. (Bug #11751825, Bug #42822) Use ALTER TABLE ... REBUILD PARTITION and ALTER TABLE ... ANALYZE PARTITION instead, to avoid this issue.

• **Analyzing partitions.** This reads and stores the key distributions for partitions.

#### Example:

ALTER TABLE t1 ANALYZE PARTITION p3;

• **Repairing partitions.** This repairs corrupted partitions.

#### Example:

ALTER TABLE t1 REPAIR PARTITION p0,p1;

Normally, REPAIR PARTITION fails when the partition contains duplicate key errors. You can use ALTER IGNORE TABLE with this option, in which case all rows that cannot be moved due to the presence of duplicate keys are removed from the partition (Bug #16900947).

• **Checking partitions.** You can check partitions for errors in much the same way that you can use CHECK TABLE with nonpartitioned tables.

#### Example:

```
ALTER TABLE trb3 CHECK PARTITION p1;
```

This statement tells you whether the data or indexes in partition p1 of table t1 are corrupted. If this is the case, use ALTER TABLE ... REPAIR PARTITION to repair the partition.

Normally, CHECK PARTITION fails when the partition contains duplicate key errors. You can use ALTER IGNORE TABLE with this option, in which case the statement returns the contents of each row in the partition where a duplicate key violation is found. Only the values for the columns in the partitioning expression for the table are reported. (Bug #16900947)

Each of the statements in the list just shown also supports the keyword ALL in place of the list of partition names. Using ALL causes the statement to act on all partitions in the table.

You can also truncate partitions using ALTER TABLE ... TRUNCATE PARTITION. This statement can be used to delete all rows from one or more partitions in much the same way that TRUNCATE TABLE deletes all rows from a table.

ALTER TABLE ... TRUNCATE PARTITION ALL truncates all partitions in the table.

# <span id="page-131-0"></span>**26.3.5 Obtaining Information About Partitions**

This section discusses obtaining information about existing partitions, which can be done in a number of ways. Methods of obtaining such information include the following:

• Using the SHOW CREATE TABLE statement to view the partitioning clauses used in creating a partitioned table.

- Using the SHOW TABLE STATUS statement to determine whether a table is partitioned.
- Querying the Information Schema PARTITIONS table.
- Using the statement EXPLAIN SELECT to see which partitions are used by a given SELECT.

From MySQL 8.0.16, when insertions, deletions, or updates are made to partitioned tables, the binary log records information about the partition and (if any) the subpartition in which the row event took place. A new row event is created for a modification that takes place in a different partition or subpartition, even if the table involved is the same. So if a transaction involves three partitions or subpartitions, three row events are generated. For an update event, the partition information is recorded for both the "before" image and the "after" image. The partition information is displayed if you specify the -v or --verbose option when viewing the binary log using mysqlbinlog. Partition information is only recorded when row-based logging is in use (binlog\_format=ROW).

As discussed elsewhere in this chapter, SHOW CREATE TABLE includes in its output the PARTITION BY clause used to create a partitioned table. For example:

```
mysql> SHOW CREATE TABLE trb3\G
*************************** 1. row ***************************
 Table: trb3
Create Table: CREATE TABLE `trb3` (
 `id` int(11) DEFAULT NULL,
 `name` varchar(50) DEFAULT NULL,
 `purchased` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
/*!50100 PARTITION BY RANGE (YEAR(purchased))
(PARTITION p0 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1995) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2005) ENGINE = InnoDB) */
0 row in set (0.00 sec)
```

The output from SHOW TABLE STATUS for partitioned tables is the same as that for nonpartitioned tables, except that the Create\_options column contains the string partitioned. The Engine column contains the name of the storage engine used by all partitions of the table. (See Section 15.7.7.38, "SHOW TABLE STATUS Statement", for more information about this statement.)

You can also obtain information about partitions from INFORMATION\_SCHEMA, which contains a PARTITIONS table. See Section 28.3.21, "The INFORMATION\_SCHEMA PARTITIONS Table".

It is possible to determine which partitions of a partitioned table are involved in a given SELECT query using EXPLAIN. The partitions column in the EXPLAIN output lists the partitions from which records would be matched by the query.

Suppose that a table trb1 is created and populated as follows:

```
CREATE TABLE trb1 (id INT, name VARCHAR(50), purchased DATE)
 PARTITION BY RANGE(id)
 (
 PARTITION p0 VALUES LESS THAN (3),
 PARTITION p1 VALUES LESS THAN (7),
 PARTITION p2 VALUES LESS THAN (9),
 PARTITION p3 VALUES LESS THAN (11)
 );
INSERT INTO trb1 VALUES
 (1, 'desk organiser', '2003-10-15'),
 (2, 'CD player', '1993-11-05'),
 (3, 'TV set', '1996-03-10'),
 (4, 'bookcase', '1982-01-10'),
 (5, 'exercise bike', '2004-05-09'),
 (6, 'sofa', '1987-06-05'),
 (7, 'popcorn maker', '2001-11-22'),
 (8, 'aquarium', '1992-08-04'),
 (9, 'study desk', '1984-09-16'),
```

```
(10, 'lava lamp', '1998-12-25');
```

You can see which partitions are used in a query such as SELECT \* FROM trb1;, as shown here:

```
mysql> EXPLAIN SELECT * FROM trb1\G

***********************************
```

In this case, all four partitions are searched. However, when a limiting condition making use of the partitioning key is added to the query, you can see that only those partitions containing matching values are scanned, as shown here:

```
mysql> EXPLAIN SELECT * FROM trb1 WHERE id < 5\G
***************************
        id: 1
select_type: SIMPLE
        table: trb1
partitions: p0,p1
        type: ALL
possible_keys: NULL
        key: NULL
        key: NULL
        ref: NULL
        rows: 10
        Extra: Using where</pre>
```

EXPLAIN also provides information about keys used and possible keys:

```
mysql> ALTER TABLE trb1 ADD PRIMARY KEY (id);
Query OK, 10 rows affected (0.03 sec)
Records: 10 Duplicates: 0 Warnings: 0
mysql> EXPLAIN SELECT * FROM trb1 WHERE id < 5\G
****** 1. row ******
         id: 1
 select type: SIMPLE
       table: trb1
  partitions: p0,p1
       type: range
possible_keys: PRIMARY
         kev: PRIMARY
     key len: 4
        ref: NULL
        rows: 7
      Extra: Using where
```

If EXPLAIN is used to examine a query against a nonpartitioned table, no error is produced, but the value of the partitions column is always NULL.

The  ${\tt rows}$  column of  ${\tt EXPLAIN}$  output displays the total number of rows in the table.

See also Section 15.8.2, "EXPLAIN Statement".

# <span id="page-133-0"></span>26.4 Partition Pruning

The optimization known as *partition pruning* is based on a relatively simple concept which can be described as "Do not scan partitions where there can be no matching values". Suppose a partitioned table t1 is created by this statement:

```
CREATE TABLE t1 (
 fname VARCHAR(50) NOT NULL,
 lname VARCHAR(50) NOT NULL,
 region_code TINYINT UNSIGNED NOT NULL,
 dob DATE NOT NULL
)
PARTITION BY RANGE( region_code ) (
 PARTITION p0 VALUES LESS THAN (64),
 PARTITION p1 VALUES LESS THAN (128),
 PARTITION p2 VALUES LESS THAN (192),
 PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

Suppose that you wish to obtain results from a SELECT statement such as this one:

```
SELECT fname, lname, region_code, dob
 FROM t1
 WHERE region_code > 125 AND region_code < 130;
```

It is easy to see that none of the rows which ought to be returned are in either of the partitions p0 or p3; that is, we need search only in partitions p1 and p2 to find matching rows. By limiting the search, it is possible to expend much less time and effort in finding matching rows than by scanning all partitions in the table. This "cutting away" of unneeded partitions is known as pruning. When the optimizer can make use of partition pruning in performing this query, execution of the query can be an order of magnitude faster than the same query against a nonpartitioned table containing the same column definitions and data.

The optimizer can perform pruning whenever a WHERE condition can be reduced to either one of the following two cases:

- partition\_column = constant
- partition\_column IN (constant1, constant2, ..., constantN)

In the first case, the optimizer simply evaluates the partitioning expression for the value given, determines which partition contains that value, and scans only this partition. In many cases, the equal sign can be replaced with another arithmetic comparison, including <, >, <=, >=, and <>. Some queries using BETWEEN in the WHERE clause can also take advantage of partition pruning. See the examples later in this section.

In the second case, the optimizer evaluates the partitioning expression for each value in the list, creates a list of matching partitions, and then scans only the partitions in this partition list.

SELECT, DELETE, and UPDATE statements support partition pruning. An INSERT statement also accesses only one partition per inserted row; this is true even for a table that is partitioned by HASH or KEY although this is not currently shown in the output of EXPLAIN.

Pruning can also be applied to short ranges, which the optimizer can convert into equivalent lists of values. For instance, in the previous example, the WHERE clause can be converted to WHERE region\_code IN (126, 127, 128, 129). Then the optimizer can determine that the first two values in the list are found in partition p1, the remaining two values in partition p2, and that the other partitions contain no relevant values and so do not need to be searched for matching rows.

The optimizer can also perform pruning for WHERE conditions that involve comparisons of the preceding types on multiple columns for tables that use RANGE COLUMNS or LIST COLUMNS partitioning.

This type of optimization can be applied whenever the partitioning expression consists of an equality or a range which can be reduced to a set of equalities, or when the partitioning expression represents an increasing or decreasing relationship. Pruning can also be applied for tables partitioned on a DATE or DATETIME column when the partitioning expression uses the YEAR() or TO\_DAYS() function. Pruning can also be applied for such tables when the partitioning expression uses the TO\_SECONDS() function.

Suppose that table t2, partitioned on a DATE column, is created using the statement shown here:

```
CREATE TABLE t2 (
 fname VARCHAR(50) NOT NULL,
 lname VARCHAR(50) NOT NULL,
 region_code TINYINT UNSIGNED NOT NULL,
 dob DATE NOT NULL
)
PARTITION BY RANGE( YEAR(dob) ) (
 PARTITION d0 VALUES LESS THAN (1970),
 PARTITION d1 VALUES LESS THAN (1975),
 PARTITION d2 VALUES LESS THAN (1980),
 PARTITION d3 VALUES LESS THAN (1985),
 PARTITION d4 VALUES LESS THAN (1990),
 PARTITION d5 VALUES LESS THAN (2000),
 PARTITION d6 VALUES LESS THAN (2005),
 PARTITION d7 VALUES LESS THAN MAXVALUE
);
```

The following statements using t2 can make of use partition pruning:

```
SELECT * FROM t2 WHERE dob = '1982-06-23';
UPDATE t2 SET region_code = 8 WHERE dob BETWEEN '1991-02-15' AND '1997-04-25';
DELETE FROM t2 WHERE dob >= '1984-06-21' AND dob <= '1999-06-21'
```

In the case of the last statement, the optimizer can also act as follows:

1. Find the partition containing the low end of the range.

```
YEAR('1984-06-21') yields the value 1984, which is found in partition d3.
```

2. Find the partition containing the high end of the range.

```
YEAR('1999-06-21') evaluates to 1999, which is found in partition d5.
```

3. Scan only these two partitions and any partitions that may lie between them.

In this case, this means that only partitions d3, d4, and d5 are scanned. The remaining partitions may be safely ignored (and are ignored).

![](_page_135_Picture_11.jpeg)

#### **Important**

Invalid DATE and DATETIME values referenced in the WHERE condition of a statement against a partitioned table are treated as NULL. This means that a query such as SELECT \* FROM partitioned\_table WHERE date\_column < '2008-12-00' does not return any values (see Bug #40972).

So far, we have looked only at examples using RANGE partitioning, but pruning can be applied with other partitioning types as well.

Consider a table that is partitioned by LIST, where the partitioning expression is increasing or decreasing, such as the table t3 shown here. (In this example, we assume for the sake of brevity that the region\_code column is limited to values between 1 and 10 inclusive.)

```
CREATE TABLE t3 (
 fname VARCHAR(50) NOT NULL,
 lname VARCHAR(50) NOT NULL,
 region_code TINYINT UNSIGNED NOT NULL,
 dob DATE NOT NULL
)
PARTITION BY LIST(region_code) (
 PARTITION r0 VALUES IN (1, 3),
 PARTITION r1 VALUES IN (2, 5, 8),
 PARTITION r2 VALUES IN (4, 9),
 PARTITION r3 VALUES IN (6, 7, 10)
);
```

For a statement such as SELECT \* FROM t3 WHERE region\_code BETWEEN 1 AND 3, the optimizer determines in which partitions the values 1, 2, and 3 are found (r0 and r1) and skips the remaining ones (r2 and r3).

For tables that are partitioned by HASH or [LINEAR] KEY, partition pruning is also possible in cases in which the WHERE clause uses a simple = relation against a column used in the partitioning expression. Consider a table created like this:

```
CREATE TABLE t4 (
 fname VARCHAR(50) NOT NULL,
 lname VARCHAR(50) NOT NULL,
 region_code TINYINT UNSIGNED NOT NULL,
 dob DATE NOT NULL
)
PARTITION BY KEY(region_code)
PARTITIONS 8;
```

A statement that compares a column value with a constant can be pruned:

```
UPDATE t4 WHERE region_code = 7;
```

Pruning can also be employed for short ranges, because the optimizer can turn such conditions into IN relations. For example, using the same table t4 as defined previously, queries such as these can be pruned:

```
SELECT * FROM t4 WHERE region_code > 2 AND region_code < 6;
SELECT * FROM t4 WHERE region_code BETWEEN 3 AND 5;
```

In both these cases, the WHERE clause is transformed by the optimizer into WHERE region\_code IN (3, 4, 5).

![](_page_136_Picture_9.jpeg)

#### **Important**

This optimization is used only if the range size is smaller than the number of partitions. Consider this statement:

```
DELETE FROM t4 WHERE region_code BETWEEN 4 AND 12;
```

The range in the WHERE clause covers 9 values (4, 5, 6, 7, 8, 9, 10, 11, 12), but t4 has only 8 partitions. This means that the DELETE cannot be pruned.

When a table is partitioned by HASH or [LINEAR] KEY, pruning can be used only on integer columns. For example, this statement cannot use pruning because dob is a DATE column:

```
SELECT * FROM t4 WHERE dob >= '2001-04-14' AND dob <= '2005-10-15';
```

However, if the table stores year values in an INT column, then a query having WHERE year\_col >= 2001 AND year\_col <= 2005 can be pruned.

Tables using a storage engine that provides automatic partitioning, such as the NDB storage engine used by MySQL Cluster can be pruned if they are explicitly partitioned.

# <span id="page-136-0"></span>**26.5 Partition Selection**

Explicit selection of partitions and subpartitions for rows matching a given WHERE condition is supported. Partition selection is similar to partition pruning, in that only specific partitions are checked for matches, but differs in two key respects:

- 1. The partitions to be checked are specified by the issuer of the statement, unlike partition pruning, which is automatic.
- 2. Whereas partition pruning applies only to queries, explicit selection of partitions is supported for both queries and a number of DML statements.

SQL statements supporting explicit partition selection are listed here:

- SELECT
- DELETE
- INSERT
- REPLACE
- UPDATE
- LOAD DATA.
- LOAD XML.

The remainder of this section discusses explicit partition selection as it applies generally to the statements just listed, and provides some examples.

Explicit partition selection is implemented using a PARTITION option. For all supported statements, this option uses the syntax shown here:

```
 PARTITION (partition_names)
 partition_names:
 partition_name, ...
```

This option always follows the name of the table to which the partition or partitions belong. partition\_names is a comma-separated list of partitions or subpartitions to be used. Each name in this list must be the name of an existing partition or subpartition of the specified table; if any of the partitions or subpartitions are not found, the statement fails with an error (partition 'partition\_name' doesn't exist). Partitions and subpartitions named in partition\_names may be listed in any order, and may overlap.

When the PARTITION option is used, only the partitions and subpartitions listed are checked for matching rows. This option can be used in a SELECT statement to determine which rows belong to a given partition. Consider a partitioned table named employees, created and populated using the statements shown here:

```
SET @@SQL_MODE = '';
CREATE TABLE employees (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 fname VARCHAR(25) NOT NULL,
 lname VARCHAR(25) NOT NULL,
 store_id INT NOT NULL,
 department_id INT NOT NULL
)
 PARTITION BY RANGE(id) (
 PARTITION p0 VALUES LESS THAN (5),
 PARTITION p1 VALUES LESS THAN (10),
 PARTITION p2 VALUES LESS THAN (15),
 PARTITION p3 VALUES LESS THAN MAXVALUE
);
INSERT INTO employees VALUES
 ('', 'Bob', 'Taylor', 3, 2), ('', 'Frank', 'Williams', 1, 2),
 ('', 'Ellen', 'Johnson', 3, 4), ('', 'Jim', 'Smith', 2, 4),
 ('', 'Mary', 'Jones', 1, 1), ('', 'Linda', 'Black', 2, 3),
 ('', 'Ed', 'Jones', 2, 1), ('', 'June', 'Wilson', 3, 1),
 ('', 'Andy', 'Smith', 1, 3), ('', 'Lou', 'Waters', 2, 4),
 ('', 'Jill', 'Stone', 1, 4), ('', 'Roger', 'White', 3, 2),
 ('', 'Howard', 'Andrews', 1, 2), ('', 'Fred', 'Goldberg', 3, 3),
 ('', 'Barbara', 'Brown', 2, 3), ('', 'Alice', 'Rogers', 2, 2),
 ('', 'Mark', 'Morgan', 3, 3), ('', 'Karen', 'Cole', 3, 2);
```

You can see which rows are stored in partition p1 like this:

```
mysql> SELECT * FROM employees PARTITION (p1);
+----+-------+--------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+--------+----------+---------------+
| 5 | Mary | Jones | 1 | 1 |
| 6 | Linda | Black | 2 | 3 |
| 7 | Ed | Jones | 2 | 1 |
| 8 | June | Wilson | 3 | 1 |
| 9 | Andy | Smith | 1 | 3 |
+----+-------+--------+----------+---------------+
5 rows in set (0.00 sec)
```

The result is the same as obtained by the query SELECT \* FROM employees WHERE id BETWEEN 5 AND 9.

To obtain rows from multiple partitions, supply their names as a comma-delimited list. For example, SELECT \* FROM employees PARTITION (p1, p2) returns all rows from partitions p1 and p2 while excluding rows from the remaining partitions.

Any valid query against a partitioned table can be rewritten with a PARTITION option to restrict the result to one or more desired partitions. You can use WHERE conditions, ORDER BY and LIMIT options, and so on. You can also use aggregate functions with HAVING and GROUP BY options. Each of the following queries produces a valid result when run on the employees table as previously defined:

```
mysql> SELECT * FROM employees PARTITION (p0, p2)
 -> WHERE lname LIKE 'S%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 4 | Jim | Smith | 2 | 4 |
| 11 | Jill | Stone | 1 | 4 |
+----+-------+-------+----------+---------------+
2 rows in set (0.00 sec)
mysql> SELECT id, CONCAT(fname, ' ', lname) AS name
 -> FROM employees PARTITION (p0) ORDER BY lname;
+----+----------------+
| id | name |
+----+----------------+
| 3 | Ellen Johnson |
| 4 | Jim Smith |
| 1 | Bob Taylor |
| 2 | Frank Williams |
+----+----------------+
4 rows in set (0.06 sec)
mysql> SELECT store_id, COUNT(department_id) AS c
 -> FROM employees PARTITION (p1,p2,p3)
 -> GROUP BY store_id HAVING c > 4;
+---+----------+
| c | store_id |
+---+----------+
| 5 | 2 |
| 5 | 3 |
+---+----------+
2 rows in set (0.00 sec)
```

Statements using partition selection can be employed with tables using any of the supported partitioning types. When a table is created using [LINEAR] HASH or [LINEAR] KEY partitioning and the names of the partitions are not specified, MySQL automatically names the partitions p0, p1, p2, ..., pN-1, where N is the number of partitions. For subpartitions not explicitly named, MySQL assigns automatically to the subpartitions in each partition pX the names pXsp0, pXsp1, pXsp2, ..., pXspM-1, where M is the number of subpartitions. When executing against this table a SELECT (or other SQL statement for which explicit partition selection is allowed), you can use these generated names in a PARTITION option, as shown here:

```
mysql> CREATE TABLE employees_sub (
 -> id INT NOT NULL AUTO_INCREMENT,
```

```
 -> fname VARCHAR(25) NOT NULL,
 -> lname VARCHAR(25) NOT NULL,
 -> store_id INT NOT NULL,
 -> department_id INT NOT NULL,
 -> PRIMARY KEY pk (id, lname)
 -> )
 -> PARTITION BY RANGE(id)
 -> SUBPARTITION BY KEY (lname)
 -> SUBPARTITIONS 2 (
 -> PARTITION p0 VALUES LESS THAN (5),
 -> PARTITION p1 VALUES LESS THAN (10),
 -> PARTITION p2 VALUES LESS THAN (15),
 -> PARTITION p3 VALUES LESS THAN MAXVALUE
 -> );
Query OK, 0 rows affected (1.14 sec)
mysql> INSERT INTO employees_sub # reuse data in employees table
 -> SELECT * FROM employees;
Query OK, 18 rows affected (0.09 sec)
Records: 18 Duplicates: 0 Warnings: 0
mysql> SELECT id, CONCAT(fname, ' ', lname) AS name
 -> FROM employees_sub PARTITION (p2sp1);
+----+---------------+
| id | name |
+----+---------------+
| 10 | Lou Waters |
| 14 | Fred Goldberg |
+----+---------------+
2 rows in set (0.00 sec)
```

You may also use a PARTITION option in the SELECT portion of an INSERT ... SELECT statement, as shown here:

```
mysql> CREATE TABLE employees_copy LIKE employees;
Query OK, 0 rows affected (0.28 sec)
mysql> INSERT INTO employees_copy
 -> SELECT * FROM employees PARTITION (p2);
Query OK, 5 rows affected (0.04 sec)
Records: 5 Duplicates: 0 Warnings: 0
mysql> SELECT * FROM employees_copy;
+----+--------+----------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+--------+----------+----------+---------------+
| 10 | Lou | Waters | 2 | 4 |
| 11 | Jill | Stone | 1 | 4 |
| 12 | Roger | White | 3 | 2 |
| 13 | Howard | Andrews | 1 | 2 |
| 14 | Fred | Goldberg | 3 | 3 |
+----+--------+----------+----------+---------------+
5 rows in set (0.00 sec)
```

Partition selection can also be used with joins. Suppose we create and populate two tables using the statements shown here:

```
CREATE TABLE stores (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 city VARCHAR(30) NOT NULL
)
 PARTITION BY HASH(id)
 PARTITIONS 2;
INSERT INTO stores VALUES
 ('', 'Nambucca'), ('', 'Uranga'),
 ('', 'Bellingen'), ('', 'Grafton');
CREATE TABLE departments (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(30) NOT NULL
)
```

```
 PARTITION BY KEY(id)
 PARTITIONS 2;
INSERT INTO departments VALUES
 ('', 'Sales'), ('', 'Customer Service'),
 ('', 'Delivery'), ('', 'Accounting');
```

You can explicitly select partitions (or subpartitions, or both) from any or all of the tables in a join. (The PARTITION option used to select partitions from a given table immediately follows the name of the table, before all other options, including any table alias.) For example, the following query gets the name, employee ID, department, and city of all employees who work in the Sales or Delivery department (partition p1 of the departments table) at the stores in either of the cities of Nambucca and Bellingen (partition p0 of the stores table):

```
mysql> SELECT
 -> e.id AS 'Employee ID', CONCAT(e.fname, ' ', e.lname) AS Name,
 -> s.city AS City, d.name AS department
 -> FROM employees AS e
 -> JOIN stores PARTITION (p1) AS s ON e.store_id=s.id
 -> JOIN departments PARTITION (p0) AS d ON e.department_id=d.id
 -> ORDER BY e.lname;
+-------------+---------------+-----------+------------+
| Employee ID | Name | City | department |
+-------------+---------------+-----------+------------+
| 14 | Fred Goldberg | Bellingen | Delivery |
| 5 | Mary Jones | Nambucca | Sales |
| 17 | Mark Morgan | Bellingen | Delivery |
| 9 | Andy Smith | Nambucca | Delivery |
| 8 | June Wilson | Bellingen | Sales |
+-------------+---------------+-----------+------------+
5 rows in set (0.00 sec)
```

For general information about joins in MySQL, see Section 15.2.13.2, "JOIN Clause".

When the PARTITION option is used with DELETE statements, only those partitions (and subpartitions, if any) listed with the option are checked for rows to be deleted. Any other partitions are ignored, as shown here:

```
mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+--------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+--------+----------+---------------+
| 4 | Jim | Smith | 2 | 4 |
| 8 | June | Wilson | 3 | 1 |
| 11 | Jill | Stone | 1 | 4 |
+----+-------+--------+----------+---------------+
3 rows in set (0.00 sec)
mysql> DELETE FROM employees PARTITION (p0, p1)
 -> WHERE fname LIKE 'j%';
Query OK, 2 rows affected (0.09 sec)
mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill | Stone | 1 | 4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)
```

Only the two rows in partitions p0 and p1 matching the WHERE condition were deleted. As you can see from the result when the SELECT is run a second time, there remains a row in the table matching the WHERE condition, but residing in a different partition (p2).

UPDATE statements using explicit partition selection behave in the same way; only rows in the partitions referenced by the PARTITION option are considered when determining the rows to be updated, as can be seen by executing the following statements:

```
mysql> UPDATE employees PARTITION (p0)
```

```
 -> SET store_id = 2 WHERE fname = 'Jill';
Query OK, 0 rows affected (0.00 sec)
Rows matched: 0 Changed: 0 Warnings: 0
mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill | Stone | 1 | 4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)
mysql> UPDATE employees PARTITION (p2)
 -> SET store_id = 2 WHERE fname = 'Jill';
Query OK, 1 row affected (0.09 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill | Stone | 2 | 4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)
```

In the same way, when PARTITION is used with DELETE, only rows in the partition or partitions named in the partition list are checked for deletion.

For statements that insert rows, the behavior differs in that failure to find a suitable partition causes the statement to fail. This is true for both INSERT and REPLACE statements, as shown here:

```
mysql> INSERT INTO employees PARTITION (p2) VALUES (20, 'Jan', 'Jones', 1, 3);
ERROR 1729 (HY000): Found a row not matching the given partition set
mysql> INSERT INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 1, 3);
Query OK, 1 row affected (0.07 sec)
mysql> REPLACE INTO employees PARTITION (p0) VALUES (20, 'Jan', 'Jones', 3, 2);
ERROR 1729 (HY000): Found a row not matching the given partition set
mysql> REPLACE INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 3, 2);
Query OK, 2 rows affected (0.09 sec)
```

For statements that write multiple rows to a partitioned table that using the InnoDB storage engine: If any row in the list following VALUES cannot be written to one of the partitions specified in the partition\_names list, the entire statement fails and no rows are written. This is shown for INSERT statements in the following example, reusing the employees table created previously:

```
mysql> ALTER TABLE employees
 -> REORGANIZE PARTITION p3 INTO (
 -> PARTITION p3 VALUES LESS THAN (20),
 -> PARTITION p4 VALUES LESS THAN (25),
 -> PARTITION p5 VALUES LESS THAN MAXVALUE
 -> );
Query OK, 6 rows affected (2.09 sec)
Records: 6 Duplicates: 0 Warnings: 0
mysql> SHOW CREATE TABLE employees\G
*************************** 1. row ***************************
 Table: employees
Create Table: CREATE TABLE `employees` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `fname` varchar(25) NOT NULL,
 `lname` varchar(25) NOT NULL,
 `store_id` int(11) NOT NULL,
 `department_id` int(11) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4
/*!50100 PARTITION BY RANGE (id)
(PARTITION p0 VALUES LESS THAN (5) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (10) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (15) ENGINE = InnoDB,
```

```
 PARTITION p3 VALUES LESS THAN (20) ENGINE = InnoDB,
 PARTITION p4 VALUES LESS THAN (25) ENGINE = InnoDB,
 PARTITION p5 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */
1 row in set (0.00 sec)
mysql> INSERT INTO employees PARTITION (p3, p4) VALUES
 -> (24, 'Tim', 'Greene', 3, 1), (26, 'Linda', 'Mills', 2, 1);
ERROR 1729 (HY000): Found a row not matching the given partition set
mysql> INSERT INTO employees PARTITION (p3, p4, p5) VALUES
 -> (24, 'Tim', 'Greene', 3, 1), (26, 'Linda', 'Mills', 2, 1);
Query OK, 2 rows affected (0.06 sec)
Records: 2 Duplicates: 0 Warnings: 0
```

The preceding is true for both INSERT statements and REPLACE statements that write multiple rows.

Partition selection is disabled for tables employing a storage engine that supplies automatic partitioning, such as NDB.

# <span id="page-142-0"></span>**26.6 Restrictions and Limitations on Partitioning**

This section discusses current restrictions and limitations on MySQL partitioning support.

**Prohibited constructs.** The following constructs are not permitted in partitioning expressions:

- Stored procedures, stored functions, loadable functions, or plugins.
- Declared variables or user variables.

For a list of SQL functions which are permitted in partitioning expressions, see [Section 26.6.3,](#page-152-0) ["Partitioning Limitations Relating to Functions".](#page-152-0)

**Arithmetic and logical operators.** Use of the arithmetic operators +, -, and \* is permitted in partitioning expressions. However, the result must be an integer value or NULL (except in the case of [LINEAR] KEY partitioning, as discussed elsewhere in this chapter; see [Section 26.2, "Partitioning](#page-89-0) [Types",](#page-89-0) for more information).

The DIV operator is also supported; the / operator is not permitted.

The bit operators |, &, ^, <<, >>, and ~ are not permitted in partitioning expressions.

**Server SQL mode.** Tables employing user-defined partitioning do not preserve the SQL mode in effect at the time that they were created. As discussed elsewhere in this Manual (see Section 7.1.11, "Server SQL Modes"), the results of many MySQL functions and operators may change according to the server SQL mode. Therefore, a change in the SQL mode at any time after the creation of partitioned tables may lead to major changes in the behavior of such tables, and could easily lead to corruption or loss of data. For these reasons, it is strongly recommended that you never change the server SQL mode after creating partitioned tables.

For one such change in the server SQL mode making a partitioned tables unusable, consider the following CREATE TABLE statement, which can be executed successfully only if the NO\_UNSIGNED\_SUBTRACTION mode is in effect:

```
mysql> SELECT @@sql_mode;
+------------+
| @@sql_mode |
+------------+
| |
+------------+
1 row in set (0.00 sec)
mysql> CREATE TABLE tu (c1 BIGINT UNSIGNED)
 -> PARTITION BY RANGE(c1 - 10) (
 -> PARTITION p0 VALUES LESS THAN (-5),
 -> PARTITION p1 VALUES LESS THAN (0),
 -> PARTITION p2 VALUES LESS THAN (5),
```

```
 -> PARTITION p3 VALUES LESS THAN (10),
 -> PARTITION p4 VALUES LESS THAN (MAXVALUE)
 -> );
ERROR 1563 (HY000): Partition constant is out of partition function domain
mysql> SET sql_mode='NO_UNSIGNED_SUBTRACTION';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@sql_mode;
+-------------------------+
| @@sql_mode |
+-------------------------+
| NO_UNSIGNED_SUBTRACTION |
+-------------------------+
1 row in set (0.00 sec)
mysql> CREATE TABLE tu (c1 BIGINT UNSIGNED)
 -> PARTITION BY RANGE(c1 - 10) (
 -> PARTITION p0 VALUES LESS THAN (-5),
 -> PARTITION p1 VALUES LESS THAN (0),
 -> PARTITION p2 VALUES LESS THAN (5),
 -> PARTITION p3 VALUES LESS THAN (10),
 -> PARTITION p4 VALUES LESS THAN (MAXVALUE)
 -> );
Query OK, 0 rows affected (0.05 sec)
```

If you remove the NO\_UNSIGNED\_SUBTRACTION server SQL mode after creating tu, you may no longer be able to access this table:

```
mysql> SET sql_mode='';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM tu;
ERROR 1563 (HY000): Partition constant is out of partition function domain
mysql> INSERT INTO tu VALUES (20);
ERROR 1563 (HY000): Partition constant is out of partition function domain
```

See also Section 7.1.11, "Server SQL Modes".

Server SQL modes also impact replication of partitioned tables. Disparate SQL modes on source and replica can lead to partitioning expressions being evaluated differently; this can cause the distribution of data among partitions to be different in the source's and replica's copies of a given table, and may even cause inserts into partitioned tables that succeed on the source to fail on the replica. For best results, you should always use the same server SQL mode on the source and on the replica.

**Performance considerations.** Some effects of partitioning operations on performance are given in the following list:

<span id="page-143-0"></span>• **File system operations.** Partitioning and repartitioning operations (such as ALTER TABLE with PARTITION BY ..., REORGANIZE PARTITION, or REMOVE PARTITIONING) depend on file system operations for their implementation. This means that the speed of these operations is affected by such factors as file system type and characteristics, disk speed, swap space, file handling efficiency of the operating system, and MySQL server options and variables that relate to file handling. In particular, you should make sure that large\_files\_support is enabled and that open\_files\_limit is set properly. Partitioning and repartitioning operations involving InnoDB tables may be made more efficient by enabling innodb\_file\_per\_table.

See also [Maximum number of partitions](#page-144-0).

- **Table locks.** Generally, the process executing a partitioning operation on a table takes a write lock on the table. Reads from such tables are relatively unaffected; pending INSERT and UPDATE operations are performed as soon as the partitioning operation has completed. For InnoDB-specific exceptions to this limitation, see Partitioning Operations.
- **Indexes; partition pruning.** As with nonpartitioned tables, proper use of indexes can speed up queries on partitioned tables significantly. In addition, designing partitioned tables and queries

on these tables to take advantage of partition pruning can improve performance dramatically. See [Section 26.4, "Partition Pruning",](#page-133-0) for more information.

Index condition pushdown is supported for partitioned tables. See Section 10.2.1.6, "Index Condition Pushdown Optimization".

• **Performance with LOAD DATA.** In MySQL 8.0, LOAD DATA uses buffering to improve performance. You should be aware that the buffer uses 130 KB memory per partition to achieve this.

#### <span id="page-144-0"></span>**Maximum number of partitions.**

The maximum possible number of partitions for a given table not using the NDB storage engine is 8192. This number includes subpartitions.

The maximum possible number of user-defined partitions for a table using the NDB storage engine is determined according to the version of the NDB Cluster software being used, the number of data nodes, and other factors. See NDB and user-defined partitioning, for more information.

If, when creating tables with a large number of partitions (but less than the maximum), you encounter an error message such as Got error ... from storage engine: Out of resources when opening file, you may be able to address the issue by increasing the value of the open\_files\_limit system variable. However, this is dependent on the operating system, and may not be possible or advisable on all platforms; see Section B.3.2.16, "File Not Found and Similar Errors", for more information. In some cases, using large numbers (hundreds) of partitions may also not be advisable due to other concerns, so using more partitions does not automatically lead to better results.

See also [File system operations.](#page-143-0)

#### **Foreign keys not supported for partitioned InnoDB tables.**

Partitioned tables using the InnoDB storage engine do not support foreign keys. More specifically, this means that the following two statements are true:

- 1. No definition of an InnoDB table employing user-defined partitioning may contain foreign key references; no InnoDB table whose definition contains foreign key references may be partitioned.
- 2. No InnoDB table definition may contain a foreign key reference to a user-partitioned table; no InnoDB table with user-defined partitioning may contain columns referenced by foreign keys.

The scope of the restrictions just listed includes all tables that use the InnoDB storage engine. CREATE TABLE and ALTER TABLE statements that would result in tables violating these restrictions are not allowed.

**ALTER TABLE ... ORDER BY.** An ALTER TABLE ... ORDER BY column statement run against a partitioned table causes ordering of rows only within each partition.

**ADD COLUMN ... ALGORITHM=INSTANT.** Once you perform ALTER TABLE ... ADD COLUMN ... ALGORITHM=INSTANT on a partitioned table, it is no longer possible to exchange partitions with this table.

**Effects on REPLACE statements by modification of primary keys.** It can be desirable in some cases (see [Section 26.6.1, "Partitioning Keys, Primary Keys, and Unique Keys"](#page-148-0)) to modify a table's primary key. Be aware that, if your application uses REPLACE statements and you do this, the results of these statements can be drastically altered. See Section 15.2.12, "REPLACE Statement", for more information and an example.

### **FULLTEXT indexes.**

Partitioned tables do not support FULLTEXT indexes or searches.

**Spatial columns.** Columns with spatial data types such as POINT or GEOMETRY cannot be used in partitioned tables.

**Temporary tables.** 

Temporary tables cannot be partitioned.

**Log tables.** It is not possible to partition the log tables; an ALTER TABLE ... PARTITION BY ... statement on such a table fails with an error.

#### **Data type of partitioning key.**

A partitioning key must be either an integer column or an expression that resolves to an integer. Expressions employing ENUM columns cannot be used. The column or expression value may also be NULL; see [Section 26.2.7, "How MySQL Partitioning Handles NULL"](#page-111-0).

There are two exceptions to this restriction:

1. When partitioning by [LINEAR] KEY, it is possible to use columns of any valid MySQL data type other than TEXT or BLOB as partitioning keys, because the internal key-hashing functions produce the correct data type from these types. For example, the following two CREATE TABLE statements are valid:

```
CREATE TABLE tkc (c1 CHAR)
PARTITION BY KEY(c1)
PARTITIONS 4;
CREATE TABLE tke
 ( c1 ENUM('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet') )
PARTITION BY LINEAR KEY(c1)
PARTITIONS 6;
```

2. When partitioning by RANGE COLUMNS or LIST COLUMNS, it is possible to use string, DATE, and DATETIME columns. For example, each of the following CREATE TABLE statements is valid:

```
CREATE TABLE rc (c1 INT, c2 DATE)
PARTITION BY RANGE COLUMNS(c2) (
 PARTITION p0 VALUES LESS THAN('1990-01-01'),
 PARTITION p1 VALUES LESS THAN('1995-01-01'),
 PARTITION p2 VALUES LESS THAN('2000-01-01'),
 PARTITION p3 VALUES LESS THAN('2005-01-01'),
 PARTITION p4 VALUES LESS THAN(MAXVALUE)
);
CREATE TABLE lc (c1 INT, c2 CHAR(1))
PARTITION BY LIST COLUMNS(c2) (
 PARTITION p0 VALUES IN('a', 'd', 'g', 'j', 'm', 'p', 's', 'v', 'y'),
 PARTITION p1 VALUES IN('b', 'e', 'h', 'k', 'n', 'q', 't', 'w', 'z'),
 PARTITION p2 VALUES IN('c', 'f', 'i', 'l', 'o', 'r', 'u', 'x', NULL)
);
```

Neither of the preceding exceptions applies to BLOB or TEXT column types.

#### **Subqueries.**

A partitioning key may not be a subquery, even if that subquery resolves to an integer value or NULL.

<span id="page-145-0"></span>**Column index prefixes not supported for key partitioning.** When creating a table that is partitioned by key, any columns in the partitioning key which use column prefixes are not used in the table's partitioning function. Consider the following CREATE TABLE statement, which has three VARCHAR columns, and whose primary key uses all three columns and specifies prefixes for two of them:

```
CREATE TABLE t1 (
 a VARCHAR(10000),
 b VARCHAR(25),
 c VARCHAR(10),
 PRIMARY KEY (a(10), b, c(2))
) PARTITION BY KEY() PARTITIONS 2;
```

This statement is accepted, but the resulting table is actually created as if you had issued the following statement, using only the primary key column which does not include a prefix (column b) for the partitioning key:

```
CREATE TABLE t1 (
 a VARCHAR(10000),
 b VARCHAR(25),
 c VARCHAR(10),
 PRIMARY KEY (a(10), b, c(2))
) PARTITION BY KEY(b) PARTITIONS 2;
```

Prior to MySQL 8.0.21, no warning was issued or any other indication provided that this occurred, except in the event that all columns specified for the partitioning key used prefixes, in which case the statement failed, but with a misleading error message, as shown here:

```
mysql> CREATE TABLE t2 (
 -> a VARCHAR(10000),
 -> b VARCHAR(25),
 -> c VARCHAR(10),
 -> PRIMARY KEY (a(10), b(5), c(2))
 -> ) PARTITION BY KEY() PARTITIONS 2;
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the
table's partitioning function
```

This also occurred when performing ALTER TABLE or when upgrading such tables.

This permissive behavior is deprecated as of MySQL 8.0.21 (and is subject to removal in a future version of MySQL). Beginning with MySQL 8.0.21, using one or more columns having a prefix in the partitioning key results in a warning for each such column, as shown here:

```
mysql> CREATE TABLE t1 (
 -> a VARCHAR(10000),
 -> b VARCHAR(25),
 -> c VARCHAR(10),
 -> PRIMARY KEY (a(10), b, c(2))
 -> ) PARTITION BY KEY() PARTITIONS 2;
Query OK, 0 rows affected, 2 warnings (1.25 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1681
Message: Column 'test.t1.a' having prefix key part 'a(10)' is ignored by the
partitioning function. Use of prefixed columns in the PARTITION BY KEY() clause
is deprecated and will be removed in a future release.
*************************** 2. row ***************************
 Level: Warning
 Code: 1681
Message: Column 'test.t1.c' having prefix key part 'c(2)' is ignored by the
partitioning function. Use of prefixed columns in the PARTITION BY KEY() clause
is deprecated and will be removed in a future release.
2 rows in set (0.00 sec)
```

This includes cases in which the columns used in the partitioning function are defined implicitly as those in the table's primary key by employing an empty PARTITION BY KEY() clause.

In MySQL 8.0.21 and later, if all columns specified for the partitioning key employ prefixes, the CREATE TABLE statement used fails with an error message that identifies the issue correctly:

```
mysql> CREATE TABLE t1 (
 -> a VARCHAR(10000),
 -> b VARCHAR(25),
 -> c VARCHAR(10),
 -> PRIMARY KEY (a(10), b(5), c(2))
 -> ) PARTITION BY KEY() PARTITIONS 2;
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the table's
partitioning function (prefixed columns are not considered).
```

For general information about partitioning tables by key, see [Section 26.2.5, "KEY Partitioning"](#page-108-0).

#### <span id="page-146-0"></span>**Issues with subpartitions.**

Subpartitions must use HASH or KEY partitioning. Only RANGE and LIST partitions may be subpartitioned; HASH and KEY partitions cannot be subpartitioned.

SUBPARTITION BY KEY requires that the subpartitioning column or columns be specified explicitly, unlike the case with PARTITION BY KEY, where it can be omitted (in which case the table's primary key column is used by default). Consider the table created by this statement:

```
CREATE TABLE ts (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(30)
);
```

You can create a table having the same columns, partitioned by KEY, using a statement such as this one:

```
CREATE TABLE ts (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(30)
)
PARTITION BY KEY()
PARTITIONS 4;
```

The previous statement is treated as though it had been written like this, with the table's primary key column used as the partitioning column:

```
CREATE TABLE ts (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(30)
)
PARTITION BY KEY(id)
PARTITIONS 4;
```

However, the following statement that attempts to create a subpartitioned table using the default column as the subpartitioning column fails, and the column must be specified for the statement to succeed, as shown here:

```
mysql> CREATE TABLE ts (
 -> id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> name VARCHAR(30)
 -> )
 -> PARTITION BY RANGE(id)
 -> SUBPARTITION BY KEY()
 -> SUBPARTITIONS 4
 -> (
 -> PARTITION p0 VALUES LESS THAN (100),
 -> PARTITION p1 VALUES LESS THAN (MAXVALUE)
 -> );
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near ')
mysql> CREATE TABLE ts (
 -> id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> name VARCHAR(30)
 -> )
 -> PARTITION BY RANGE(id)
 -> SUBPARTITION BY KEY(id)
 -> SUBPARTITIONS 4
 -> (
 -> PARTITION p0 VALUES LESS THAN (100),
 -> PARTITION p1 VALUES LESS THAN (MAXVALUE)
 -> );
Query OK, 0 rows affected (0.07 sec)
```

This is a known issue (see Bug #51470).

**DATA DIRECTORY and INDEX DIRECTORY options.** Table-level DATA DIRECTORY and INDEX DIRECTORY options are ignored (see Bug #32091). You can employ these options for individual partitions or subpartitions of InnoDB tables. As of MySQL 8.0.21, the directory specified in a DATA DIRECTORY clause must be known to InnoDB. For more information, see Using the DATA DIRECTORY Clause.

**Repairing and rebuilding partitioned tables.** The statements CHECK TABLE, OPTIMIZE TABLE, ANALYZE TABLE, and REPAIR TABLE are supported for partitioned tables.

In addition, you can use ALTER TABLE ... REBUILD PARTITION to rebuild one or more partitions of a partitioned table; ALTER TABLE ... REORGANIZE PARTITION also causes partitions to be rebuilt. See Section 15.1.9, "ALTER TABLE Statement", for more information about these two statements.

ANALYZE, CHECK, OPTIMIZE, REPAIR, and TRUNCATE operations are supported with subpartitions. See Section 15.1.9.1, "ALTER TABLE Partition Operations".

**File name delimiters for partitions and subpartitions.** Table partition and subpartition file names include generated delimiters such as #P# and #SP#. The lettercase of such delimiters can vary and should not be depended upon.

## <span id="page-148-0"></span>**26.6.1 Partitioning Keys, Primary Keys, and Unique Keys**

This section discusses the relationship of partitioning keys with primary keys and unique keys. The rule governing this relationship can be expressed as follows: All columns used in the partitioning expression for a partitioned table must be part of every unique key that the table may have.

In other words, every unique key on the table must use every column in the table's partitioning expression. (This also includes the table's primary key, since it is by definition a unique key. This particular case is discussed later in this section.) For example, each of the following table creation statements is invalid:

```
CREATE TABLE t1 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 UNIQUE KEY (col1, col2)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t2 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 UNIQUE KEY (col1),
 UNIQUE KEY (col3)
)
PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

In each case, the proposed table would have at least one unique key that does not include all columns used in the partitioning expression.

Each of the following statements is valid, and represents one way in which the corresponding invalid table creation statement could be made to work:

```
CREATE TABLE t1 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 UNIQUE KEY (col1, col2, col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t2 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
```

```
 col4 INT NOT NULL,
 UNIQUE KEY (col1, col3)
)
PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

This example shows the error produced in such cases:

```
mysql> CREATE TABLE t3 (
 -> col1 INT NOT NULL,
 -> col2 DATE NOT NULL,
 -> col3 INT NOT NULL,
 -> col4 INT NOT NULL,
 -> UNIQUE KEY (col1, col2),
 -> UNIQUE KEY (col3)
 -> )
 -> PARTITION BY HASH(col1 + col3)
 -> PARTITIONS 4;
ERROR 1491 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function
```

The CREATE TABLE statement fails because both col1 and col3 are included in the proposed partitioning key, but neither of these columns is part of both of unique keys on the table. This shows one possible fix for the invalid table definition:

```
mysql> CREATE TABLE t3 (
 -> col1 INT NOT NULL,
 -> col2 DATE NOT NULL,
 -> col3 INT NOT NULL,
 -> col4 INT NOT NULL,
 -> UNIQUE KEY (col1, col2, col3),
 -> UNIQUE KEY (col3)
 -> )
 -> PARTITION BY HASH(col3)
 -> PARTITIONS 4;
Query OK, 0 rows affected (0.05 sec)
```

In this case, the proposed partitioning key col3 is part of both unique keys, and the table creation statement succeeds.

The following table cannot be partitioned at all, because there is no way to include in a partitioning key any columns that belong to both unique keys:

```
CREATE TABLE t4 (
 col1 INT NOT NULL,
 col2 INT NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 UNIQUE KEY (col1, col3),
 UNIQUE KEY (col2, col4)
);
```

Since every primary key is by definition a unique key, this restriction also includes the table's primary key, if it has one. For example, the next two statements are invalid:

```
CREATE TABLE t5 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 PRIMARY KEY(col1, col2)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t6 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 PRIMARY KEY(col1, col3),
```

```
 UNIQUE KEY(col2)
)
PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

In both cases, the primary key does not include all columns referenced in the partitioning expression. However, both of the next two statements are valid:

```
CREATE TABLE t7 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 PRIMARY KEY(col1, col2)
)
PARTITION BY HASH(col1 + YEAR(col2))
PARTITIONS 4;
CREATE TABLE t8 (
 col1 INT NOT NULL,
 col2 DATE NOT NULL,
 col3 INT NOT NULL,
 col4 INT NOT NULL,
 PRIMARY KEY(col1, col2, col4),
 UNIQUE KEY(col2, col1)
)
PARTITION BY HASH(col1 + YEAR(col2))
PARTITIONS 4;
```

If a table has no unique keys—this includes having no primary key—then this restriction does not apply, and you may use any column or columns in the partitioning expression as long as the column type is compatible with the partitioning type.

For the same reason, you cannot later add a unique key to a partitioned table unless the key includes all columns used by the table's partitioning expression. Consider the partitioned table created as shown here:

```
mysql> CREATE TABLE t_no_pk (c1 INT, c2 INT)
 -> PARTITION BY RANGE(c1) (
 -> PARTITION p0 VALUES LESS THAN (10),
 -> PARTITION p1 VALUES LESS THAN (20),
 -> PARTITION p2 VALUES LESS THAN (30),
 -> PARTITION p3 VALUES LESS THAN (40)
 -> );
Query OK, 0 rows affected (0.12 sec)
```

It is possible to add a primary key to t\_no\_pk using either of these ALTER TABLE statements:

```
# possible PK
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c1);
Query OK, 0 rows affected (0.13 sec)
Records: 0 Duplicates: 0 Warnings: 0
# drop this PK
mysql> ALTER TABLE t_no_pk DROP PRIMARY KEY;
Query OK, 0 rows affected (0.10 sec)
Records: 0 Duplicates: 0 Warnings: 0
# use another possible PK
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c1, c2);
Query OK, 0 rows affected (0.12 sec)
Records: 0 Duplicates: 0 Warnings: 0
# drop this PK
mysql> ALTER TABLE t_no_pk DROP PRIMARY KEY;
Query OK, 0 rows affected (0.09 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

However, the next statement fails, because c1 is part of the partitioning key, but is not part of the proposed primary key:

```
# fails with error 1503
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c2);
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function
```

Since t\_no\_pk has only c1 in its partitioning expression, attempting to adding a unique key on c2 alone fails. However, you can add a unique key that uses both c1 and c2.

These rules also apply to existing nonpartitioned tables that you wish to partition using ALTER TABLE ... PARTITION BY. Consider a table np\_pk created as shown here:

```
mysql> CREATE TABLE np_pk (
 -> id INT NOT NULL AUTO_INCREMENT,
 -> name VARCHAR(50),
 -> added DATE,
 -> PRIMARY KEY (id)
 -> );
Query OK, 0 rows affected (0.08 sec)
```

The following ALTER TABLE statement fails with an error, because the added column is not part of any unique key in the table:

```
mysql> ALTER TABLE np_pk
 -> PARTITION BY HASH( TO_DAYS(added) )
 -> PARTITIONS 4;
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function
```

However, this statement using the id column for the partitioning column is valid, as shown here:

```
mysql> ALTER TABLE np_pk
 -> PARTITION BY HASH(id)
 -> PARTITIONS 4;
Query OK, 0 rows affected (0.11 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

In the case of np\_pk, the only column that may be used as part of a partitioning expression is id; if you wish to partition this table using any other column or columns in the partitioning expression, you must first modify the table, either by adding the desired column or columns to the primary key, or by dropping the primary key altogether.

# <span id="page-151-0"></span>**26.6.2 Partitioning Limitations Relating to Storage Engines**

In MySQL 8.0, partitioning support is not actually provided by the MySQL Server, but rather by a table storage engine's own or native partitioning handler. In MySQL 8.0, only the InnoDB and NDB storage engines provide native partitioning handlers. This means that partitioned tables cannot be created using any other storage engine than these. (You must be using MySQL NDB Cluster with the NDB storage engine to create NDB tables.)

**InnoDB storage engine.** InnoDB foreign keys and MySQL partitioning are not compatible. Partitioned InnoDB tables cannot have foreign key references, nor can they have columns referenced by foreign keys. InnoDB tables which have or which are referenced by foreign keys cannot be partitioned.

ALTER TABLE ... OPTIMIZE PARTITION does not work correctly with partitioned tables that use InnoDB. Use ALTER TABLE ... REBUILD PARTITION and ALTER TABLE ... ANALYZE PARTITION, instead, for such tables. For more information, see Section 15.1.9.1, "ALTER TABLE Partition Operations".

**User-defined partitioning and the NDB storage engine (NDB Cluster).** Partitioning by KEY (including LINEAR KEY) is the only type of partitioning supported for the NDB storage engine. It is not possible under normal circumstances in NDB Cluster to create an NDB Cluster table using any partitioning type other than [LINEAR] KEY, and attempting to do so fails with an error.

Exception (not for production): It is possible to override this restriction by setting the new system variable on NDB Cluster SQL nodes to ON. If you choose to do this, you should be aware that tables using partitioning types other than [LINEAR] KEY are not supported in production. In such cases, you can create and use tables with partitioning types other than KEY or LINEAR KEY, but you do this entirely at your own risk. You should also be aware that this functionality is now deprecated and subject to removal without further notice in a future release of NDB Cluster.

The maximum number of partitions that can be defined for an NDB table depends on the number of data nodes and node groups in the cluster, the version of the NDB Cluster software in use, and other factors. See NDB and user-defined partitioning, for more information.

The maximum amount of fixed-size data that can be stored per partition in an NDB table is 128 TB. Previously, this was 16 GB.

CREATE TABLE and ALTER TABLE statements that would cause a user-partitioned NDB table not to meet either or both of the following two requirements are not permitted, and fail with an error:

- 1. The table must have an explicit primary key.
- 2. All columns listed in the table's partitioning expression must be part of the primary key.

**Exception.** If a user-partitioned NDB table is created using an empty column-list (that is, using PARTITION BY KEY() or PARTITION BY LINEAR KEY()), then no explicit primary key is required.

**Partition selection.** Partition selection is not supported for NDB tables. See [Section 26.5, "Partition](#page-136-0) [Selection"](#page-136-0), for more information.

**Upgrading partitioned tables.** When performing an upgrade, tables which are partitioned by KEY must be dumped and reloaded. Partitioned tables using storage engines other than InnoDB cannot be upgraded from MySQL 5.7 or earlier to MySQL 8.0 or later; you must either drop the partitioning from such tables with ALTER TABLE ... REMOVE PARTITIONING or convert them to InnoDB using ALTER TABLE ... ENGINE=INNODB prior to the upgrade.

For information about converting MyISAM tables to InnoDB, see Section 17.6.1.5, "Converting Tables from MyISAM to InnoDB".

# <span id="page-152-0"></span>**26.6.3 Partitioning Limitations Relating to Functions**

This section discusses limitations in MySQL Partitioning relating specifically to functions used in partitioning expressions.

Only the MySQL functions shown in the following list are allowed in partitioning expressions:

- ABS()
- CEILING() (see [CEILING\(\) and FLOOR\(\)](#page-153-0))
- DATEDIFF()
- DAY()
- DAYOFMONTH()
- DAYOFWEEK()
- DAYOFYEAR()
- EXTRACT() (see [EXTRACT\(\) function with WEEK specifier\)](#page-153-1)
- FLOOR() (see [CEILING\(\) and FLOOR\(\)](#page-153-0))
- HOUR()
- MICROSECOND()

```
• MINUTE()
```

- MOD()
- MONTH()
- QUARTER()
- SECOND()
- TIME\_TO\_SEC()
- TO\_DAYS()
- TO\_SECONDS()
- UNIX\_TIMESTAMP() (with TIMESTAMP columns)
- WEEKDAY()
- YEAR()
- YEARWEEK()

In MySQL 8.0, partition pruning is supported for the TO\_DAYS(), TO\_SECONDS(), YEAR(), and UNIX\_TIMESTAMP() functions. See [Section 26.4, "Partition Pruning",](#page-133-0) for more information.

<span id="page-153-0"></span>**CEILING() and FLOOR().** Each of these functions returns an integer only if it is passed an argument of an exact numeric type, such as one of the INT types or DECIMAL. This means, for example, that the following CREATE TABLE statement fails with an error, as shown here:

```
mysql> CREATE TABLE t (c FLOAT) PARTITION BY LIST( FLOOR(c) )(
 -> PARTITION p0 VALUES IN (1,3,5),
 -> PARTITION p1 VALUES IN (2,4,6)
 -> );
ERROR 1490 (HY000): The PARTITION function returns the wrong type
```

<span id="page-153-1"></span>**EXTRACT() function with WEEK specifier.** The value returned by the EXTRACT() function, when used as EXTRACT(WEEK FROM col), depends on the value of the default\_week\_format system variable. For this reason, EXTRACT() is not permitted as a partitioning function when it specifies the unit as WEEK. (Bug #54483)

See Section 14.6.2, "Mathematical Functions", for more information about the return types of these functions, as well as Section 13.1, "Numeric Data Types".

# <span id="page-154-0"></span>Chapter 27 Stored Objects

# **Table of Contents**

| 27.1 Defining Stored Programs 4926                                  |      |
|---------------------------------------------------------------------|------|
| 27.2 Using Stored Routines 4927                                     |      |
| 27.2.1 Stored Routine Syntax 4928                                   |      |
| 27.2.2 Stored Routines and MySQL Privileges 4928                    |      |
| 27.2.3 Stored Routine Metadata 4929                                 |      |
| 27.2.4 Stored Procedures, Functions, Triggers, and LAST_INSERT_ID() | 4929 |
| 27.3 Using Triggers 4929                                            |      |
| 27.3.1 Trigger Syntax and Examples 4930                             |      |
| 27.3.2 Trigger Metadata 4934                                        |      |
| 27.4 Using the Event Scheduler 4934                                 |      |
| 27.4.1 Event Scheduler Overview 4935                                |      |
| 27.4.2 Event Scheduler Configuration 4935                           |      |
| 27.4.3 Event Syntax 4938                                            |      |
| 27.4.4 Event Metadata 4938                                          |      |
| 27.4.5 Event Scheduler Status 4939                                  |      |
| 27.4.6 The Event Scheduler and MySQL Privileges 4939                |      |
| 27.5 Using Views 4942                                               |      |
| 27.5.1 View Syntax 4942                                             |      |
| 27.5.2 View Processing Algorithms 4942                              |      |
| 27.5.3 Updatable and Insertable Views 4943                          |      |
| 27.5.4 The View WITH CHECK OPTION Clause 4946                       |      |
| 27.5.5 View Metadata 4947                                           |      |
| 27.6 Stored Object Access Control 4947                              |      |
| 27.7 Stored Program Binary Logging 4951                             |      |
| 27.8 Restrictions on Stored Programs 4957                           |      |
| 27.9 Restrictions on Views 4960                                     |      |

This chapter discusses stored database objects that are defined in terms of SQL code that is stored on the server for later execution.

Stored objects include these object types:

- Stored procedure: An object created with CREATE PROCEDURE and invoked using the CALL statement. A procedure does not have a return value but can modify its parameters for later inspection by the caller. It can also generate result sets to be returned to the client program.
- Stored function: An object created with CREATE FUNCTION and used much like a built-in function. You invoke it in an expression and it returns a value during expression evaluation.
- Trigger: An object created with CREATE TRIGGER that is associated with a table. A trigger is activated when a particular event occurs for the table, such as an insert or update.
- Event: An object created with CREATE EVENT and invoked by the server according to schedule.
- View: An object created with CREATE VIEW that when referenced produces a result set. A view acts as a virtual table.

Terminology used in this document reflects the stored object hierarchy:

- Stored routines include stored procedures and functions.
- Stored programs include stored routines, triggers, and events.
- Stored objects include stored programs and views.

This chapter describes how to use stored objects. The following sections provide additional information about SQL syntax for statements related to these objects, and about object processing:

- For each object type, there are CREATE, ALTER, and DROP statements that control which objects exist and how they are defined. See Section 15.1, "Data Definition Statements".
- The CALL statement is used to invoke stored procedures. See Section 15.2.1, "CALL Statement".
- Stored program definitions include a body that may use compound statements, loops, conditionals, and declared variables. See Section 15.6, "Compound Statement Syntax".
- Metadata changes to objects referred to by stored programs are detected and cause automatic reparsing of the affected statements when the program is next executed. For more information, see Section 10.10.3, "Caching of Prepared Statements and Stored Programs".

# <span id="page-155-0"></span>**27.1 Defining Stored Programs**

Each stored program contains a body that consists of an SQL statement. This statement may be a compound statement made up of several statements separated by semicolon (;) characters. For example, the following stored procedure has a body made up of a BEGIN ... END block that contains a SET statement and a REPEAT loop that itself contains another SET statement:

```
CREATE PROCEDURE dorepeat(p1 INT)
BEGIN
 SET @x = 0;
 REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;
END;
```

If you use the mysql client program to define a stored program containing semicolon characters, a problem arises. By default, mysql itself recognizes the semicolon as a statement delimiter, so you must redefine the delimiter temporarily to cause mysql to pass the entire stored program definition to the server.

To redefine the mysql delimiter, use the delimiter command. The following example shows how to do this for the dorepeat() procedure just shown. The delimiter is changed to // to enable the entire definition to be passed to the server as a single statement, and then restored to ; before invoking the procedure. This enables the ; delimiter used in the procedure body to be passed through to the server rather than being interpreted by mysql itself.

```
mysql> delimiter //
mysql> CREATE PROCEDURE dorepeat(p1 INT)
 -> BEGIN
 -> SET @x = 0;
 -> REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;
 -> END
 -> //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> CALL dorepeat(1000);
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @x;
+------+
| @x |
+------+
| 1001 |
+------+
1 row in set (0.00 sec)
```

You can redefine the delimiter to a string other than //, and the delimiter can consist of a single character or multiple characters. You should avoid the use of the backslash (\) character because that is the escape character for MySQL.

The following is an example of a function that takes a parameter, performs an operation using an SQL function, and returns the result. In this case, it is unnecessary to use delimiter because the function definition contains no internal ; statement delimiters:

```
mysql> CREATE FUNCTION hello (s CHAR(20))
mysql> RETURNS CHAR(50) DETERMINISTIC
 -> RETURN CONCAT('Hello, ',s,'!');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT hello('world');
+----------------+
| hello('world') |
+----------------+
| Hello, world! |
+----------------+
1 row in set (0.00 sec)
```

# <span id="page-156-0"></span>**27.2 Using Stored Routines**

MySQL supports stored routines (procedures and functions). A stored routine is a set of SQL statements that can be stored in the server. Once this has been done, clients don't need to keep reissuing the individual statements but can refer to the stored routine instead.

Stored routines can be particularly useful in certain situations:

- When multiple client applications are written in different languages or work on different platforms, but need to perform the same database operations.
- When security is paramount. Banks, for example, use stored procedures and functions for all common operations. This provides a consistent and secure environment, and routines can ensure that each operation is properly logged. In such a setup, applications and users would have no access to the database tables directly, but can only execute specific stored routines.

Stored routines can provide improved performance because less information needs to be sent between the server and the client. The tradeoff is that this does increase the load on the database server because more of the work is done on the server side and less is done on the client (application) side. Consider this if many client machines (such as Web servers) are serviced by only one or a few database servers.

Stored routines also enable you to have libraries of functions in the database server. This is a feature shared by modern application languages that enable such design internally (for example, by using classes). Using these client application language features is beneficial for the programmer even outside the scope of database use.

MySQL follows the SQL:2003 syntax for stored routines, which is also used by IBM's DB2. All syntax described here is supported and any limitations and extensions are documented where appropriate.

## **Additional Resources**

- You may find the [Stored Procedures User Forum](https://forums.mysql.com/list.php?98) of use when working with stored procedures and functions.
- For answers to some commonly asked questions regarding stored routines in MySQL, see Section A.4, "MySQL 8.0 FAQ: Stored Procedures and Functions".
- There are some restrictions on the use of stored routines. See [Section 27.8, "Restrictions on Stored](#page-186-0) [Programs".](#page-186-0)
- Binary logging for stored routines takes place as described in [Section 27.7, "Stored Program Binary](#page-180-0) [Logging".](#page-180-0)

## <span id="page-157-0"></span>**27.2.1 Stored Routine Syntax**

A stored routine is either a procedure or a function. Stored routines are created with the CREATE PROCEDURE and CREATE FUNCTION statements (see Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements"). A procedure is invoked using a CALL statement (see Section 15.2.1, "CALL Statement"), and can only pass back values using output variables. A function can be called from inside a statement just like any other function (that is, by invoking the function's name), and can return a scalar value. The body of a stored routine can use compound statements (see Section 15.6, "Compound Statement Syntax").

Stored routines can be dropped with the DROP PROCEDURE and DROP FUNCTION statements (see Section 15.1.29, "DROP PROCEDURE and DROP FUNCTION Statements"), and altered with the ALTER PROCEDURE and ALTER FUNCTION statements (see Section 15.1.7, "ALTER PROCEDURE Statement").

A stored procedure or function is associated with a particular database. This has several implications:

- When the routine is invoked, an implicit USE db\_name is performed (and undone when the routine terminates). USE statements within stored routines are not permitted.
- You can qualify routine names with the database name. This can be used to refer to a routine that is not in the current database. For example, to invoke a stored procedure p or function f that is associated with the test database, you can say CALL test.p() or test.f().
- When a database is dropped, all stored routines associated with it are dropped as well.

Stored functions cannot be recursive.

Recursion in stored procedures is permitted but disabled by default. To enable recursion, set the max\_sp\_recursion\_depth server system variable to a value greater than zero. Stored procedure recursion increases the demand on thread stack space. If you increase the value of max\_sp\_recursion\_depth, it may be necessary to increase thread stack size by increasing the value of thread\_stack at server startup. See Section 7.1.8, "Server System Variables", for more information.

MySQL supports a very useful extension that enables the use of regular SELECT statements (that is, without using cursors or local variables) inside a stored procedure. The result set of such a query is simply sent directly to the client. Multiple SELECT statements generate multiple result sets, so the client must use a MySQL client library that supports multiple result sets. This means the client must use a client library from a version of MySQL at least as recent as 4.1. The client should also specify the CLIENT\_MULTI\_RESULTS option when it connects. For C programs, this can be done with the [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md) C API function. See [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md), and [Multiple Statement](https://dev.mysql.com/doc/c-api/8.0/en/c-api-multiple-queries.md) [Execution Support.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-multiple-queries.md)

In MySQL 8.0.22 and later, a user variable referenced by a statement in a stored procedure has its type determined the first time the procedure is invoked, and retains this type each time the procedure is invoked thereafter.

# <span id="page-157-1"></span>**27.2.2 Stored Routines and MySQL Privileges**

The MySQL grant system takes stored routines into account as follows:

- The CREATE ROUTINE privilege is needed to create stored routines.
- The ALTER ROUTINE privilege is needed to alter or drop stored routines. This privilege is granted automatically to the creator of a routine if necessary, and dropped from the creator when the routine is dropped.
- The EXECUTE privilege is required to execute stored routines. However, this privilege is granted automatically to the creator of a routine if necessary (and dropped from the creator when the routine is dropped). Also, the default SQL SECURITY characteristic for a routine is DEFINER, which enables users who have access to the database with which the routine is associated to execute the routine.

- If the automatic\_sp\_privileges system variable is 0, the EXECUTE and ALTER ROUTINE privileges are not automatically granted to and dropped from the routine creator.
- The creator of a routine is the account used to execute the CREATE statement for it. This might not be the same as the account named as the DEFINER in the routine definition.
- The account named as a routine DEFINER can see all routine properties, including its definition. The account thus has full access to the routine output as produced by:
  - The contents of the Information Schema ROUTINES table.
  - The SHOW CREATE FUNCTION and SHOW CREATE PROCEDURE statements.
  - The SHOW FUNCTION CODE and SHOW PROCEDURE CODE statements.
  - The SHOW FUNCTION STATUS and SHOW PROCEDURE STATUS statements.
- For an account other than the account named as the routine DEFINER, access to routine properties depends on the privileges granted to the account:
  - With the SHOW\_ROUTINE privilege or the global SELECT privilege, the account can see all routine properties, including its definition.
  - With the CREATE ROUTINE, ALTER ROUTINE or EXECUTE privilege granted at a scope that includes the routine, the account can see all routine properties except its definition.

## <span id="page-158-0"></span>**27.2.3 Stored Routine Metadata**

To obtain metadata about stored routines:

- Query the ROUTINES table of the INFORMATION\_SCHEMA database. See Section 28.3.30, "The INFORMATION\_SCHEMA ROUTINES Table".
- Use the SHOW CREATE PROCEDURE and SHOW CREATE FUNCTION statements to see routine definitions. See Section 15.7.7.9, "SHOW CREATE PROCEDURE Statement".
- Use the SHOW PROCEDURE STATUS and SHOW FUNCTION STATUS statements to see routine characteristics. See Section 15.7.7.28, "SHOW PROCEDURE STATUS Statement".
- Use the SHOW PROCEDURE CODE and SHOW FUNCTION CODE statements to see a representation of the internal implementation of the routine. See Section 15.7.7.27, "SHOW PROCEDURE CODE Statement".

# <span id="page-158-1"></span>**27.2.4 Stored Procedures, Functions, Triggers, and LAST\_INSERT\_ID()**

Within the body of a stored routine (procedure or function) or a trigger, the value of LAST\_INSERT\_ID() changes the same way as for statements executed outside the body of these kinds of objects (see Section 14.15, "Information Functions"). The effect of a stored routine or trigger upon the value of LAST\_INSERT\_ID() that is seen by following statements depends on the kind of routine:

- If a stored procedure executes statements that change the value of LAST\_INSERT\_ID(), the changed value is seen by statements that follow the procedure call.
- For stored functions and triggers that change the value, the value is restored when the function or trigger ends, so following statements do not see a changed value.

# <span id="page-158-2"></span>**27.3 Using Triggers**

A trigger is a named database object that is associated with a table, and that activates when a particular event occurs for the table. Some uses for triggers are to perform checks of values to be inserted into a table or to perform calculations on values involved in an update.

A trigger is defined to activate when a statement inserts, updates, or deletes rows in the associated table. These row operations are trigger events. For example, rows can be inserted by INSERT or LOAD DATA statements, and an insert trigger activates for each inserted row. A trigger can be set to activate either before or after the trigger event. For example, you can have a trigger activate before each row that is inserted into a table or after each row that is updated.

![](_page_159_Picture_2.jpeg)

### **Important**

MySQL triggers activate only for changes made to tables by SQL statements. This includes changes to base tables that underlie updatable views. Triggers do not activate for changes to tables made by APIs that do not transmit SQL statements to the MySQL Server. This means that triggers are not activated by updates made using the NDB API.

Triggers are not activated by changes in INFORMATION\_SCHEMA or performance\_schema tables. Those tables are actually views and triggers are not permitted on views.

The following sections describe the syntax for creating and dropping triggers, show some examples of how to use them, and indicate how to obtain trigger metadata.

## **Additional Resources**

- You may find the [MySQL User Forums](https://forums.mysql.com/list.php?20) helpful when working with triggers.
- For answers to commonly asked questions regarding triggers in MySQL, see Section A.5, "MySQL 8.0 FAQ: Triggers".
- There are some restrictions on the use of triggers; see [Section 27.8, "Restrictions on Stored](#page-186-0) [Programs".](#page-186-0)
- Binary logging for triggers takes place as described in [Section 27.7, "Stored Program Binary](#page-180-0) [Logging".](#page-180-0)

# <span id="page-159-0"></span>**27.3.1 Trigger Syntax and Examples**

To create a trigger or drop a trigger, use the CREATE TRIGGER or DROP TRIGGER statement, described in Section 15.1.22, "CREATE TRIGGER Statement", and Section 15.1.34, "DROP TRIGGER Statement".

Here is a simple example that associates a trigger with a table, to activate for INSERT operations. The trigger acts as an accumulator, summing the values inserted into one of the columns of the table.

```
mysql> CREATE TABLE account (acct_num INT, amount DECIMAL(10,2));
Query OK, 0 rows affected (0.03 sec)
mysql> CREATE TRIGGER ins_sum BEFORE INSERT ON account
 FOR EACH ROW SET @sum = @sum + NEW.amount;
Query OK, 0 rows affected (0.01 sec)
```

The CREATE TRIGGER statement creates a trigger named ins\_sum that is associated with the account table. It also includes clauses that specify the trigger action time, the triggering event, and what to do when the trigger activates:

- The keyword BEFORE indicates the trigger action time. In this case, the trigger activates before each row inserted into the table. The other permitted keyword here is AFTER.
- The keyword INSERT indicates the trigger event; that is, the type of operation that activates the trigger. In the example, INSERT operations cause trigger activation. You can also create triggers for DELETE and UPDATE operations.
- The statement following FOR EACH ROW defines the trigger body; that is, the statement to execute each time the trigger activates, which occurs once for each row affected by the triggering event.

In the example, the trigger body is a simple SET that accumulates into a user variable the values inserted into the amount column. The statement refers to the column as NEW.amount which means "the value of the amount column to be inserted into the new row."

To use the trigger, set the accumulator variable to zero, execute an INSERT statement, and then see what value the variable has afterward:

```
mysql> SET @sum = 0;
mysql> INSERT INTO account VALUES(137,14.98),(141,1937.50),(97,-100.00);
mysql> SELECT @sum AS 'Total amount inserted';
+-----------------------+
| Total amount inserted |
+-----------------------+
| 1852.48 |
+-----------------------+
```

In this case, the value of @sum after the INSERT statement has executed is 14.98 + 1937.50 - 100, or 1852.48.

To destroy the trigger, use a DROP TRIGGER statement. You must specify the schema name if the trigger is not in the default schema:

```
mysql> DROP TRIGGER test.ins_sum;
```

If you drop a table, any triggers for the table are also dropped.

Trigger names exist in the schema namespace, meaning that all triggers must have unique names within a schema. Triggers in different schemas can have the same name.

It is possible to define multiple triggers for a given table that have the same trigger event and action time. For example, you can have two BEFORE UPDATE triggers for a table. By default, triggers that have the same trigger event and action time activate in the order they were created. To affect trigger order, specify a clause after FOR EACH ROW that indicates FOLLOWS or PRECEDES and the name of an existing trigger that also has the same trigger event and action time. With FOLLOWS, the new trigger activates after the existing trigger. With PRECEDES, the new trigger activates before the existing trigger.

For example, the following trigger definition defines another BEFORE INSERT trigger for the account table:

```
mysql> CREATE TRIGGER ins_transaction BEFORE INSERT ON account
 FOR EACH ROW PRECEDES ins_sum
 SET
 @deposits = @deposits + IF(NEW.amount>0,NEW.amount,0),
 @withdrawals = @withdrawals + IF(NEW.amount<0,-NEW.amount,0);
Query OK, 0 rows affected (0.01 sec)
```

This trigger, ins\_transaction, is similar to ins\_sum but accumulates deposits and withdrawals separately. It has a PRECEDES clause that causes it to activate before ins\_sum; without that clause, it would activate after ins\_sum because it is created after ins\_sum.

Within the trigger body, the OLD and NEW keywords enable you to access columns in the rows affected by a trigger. OLD and NEW are MySQL extensions to triggers; they are not case-sensitive.

In an INSERT trigger, only NEW.col\_name can be used; there is no old row. In a DELETE trigger, only OLD.col\_name can be used; there is no new row. In an UPDATE trigger, you can use OLD.col\_name to refer to the columns of a row before it is updated and NEW.col\_name to refer to the columns of the row after it is updated.

A column named with OLD is read only. You can refer to it (if you have the SELECT privilege), but not modify it. You can refer to a column named with NEW if you have the SELECT privilege for it. In a BEFORE trigger, you can also change its value with SET NEW.col\_name = value if you have the UPDATE privilege for it. This means you can use a trigger to modify the values to be inserted into a new row or used to update a row. (Such a SET statement has no effect in an AFTER trigger because the row change has already occurred.)

In a BEFORE trigger, the NEW value for an AUTO\_INCREMENT column is 0, not the sequence number that is generated automatically when the new row actually is inserted.

By using the BEGIN ... END construct, you can define a trigger that executes multiple statements. Within the BEGIN block, you also can use other syntax that is permitted within stored routines such as conditionals and loops. However, just as for stored routines, if you use the mysql program to define a trigger that executes multiple statements, it is necessary to redefine the mysql statement delimiter so that you can use the ; statement delimiter within the trigger definition. The following example illustrates these points. It defines an UPDATE trigger that checks the new value to be used for updating each row, and modifies the value to be within the range from 0 to 100. This must be a BEFORE trigger because the value must be checked before it is used to update the row:

```
mysql> delimiter //
mysql> CREATE TRIGGER upd_check BEFORE UPDATE ON account
 FOR EACH ROW
 BEGIN
 IF NEW.amount < 0 THEN
 SET NEW.amount = 0;
 ELSEIF NEW.amount > 100 THEN
 SET NEW.amount = 100;
 END IF;
 END;//
mysql> delimiter ;
```

It can be easier to define a stored procedure separately and then invoke it from the trigger using a simple CALL statement. This is also advantageous if you want to execute the same code from within several triggers.

There are limitations on what can appear in statements that a trigger executes when activated:

- The trigger cannot use the CALL statement to invoke stored procedures that return data to the client or that use dynamic SQL. (Stored procedures are permitted to return data to the trigger through OUT or INOUT parameters.)
- The trigger cannot use statements that explicitly or implicitly begin or end a transaction, such as START TRANSACTION, COMMIT, or ROLLBACK. (ROLLBACK to SAVEPOINT is permitted because it does not end a transaction.).

See also [Section 27.8, "Restrictions on Stored Programs".](#page-186-0)

MySQL handles errors during trigger execution as follows:

- If a BEFORE trigger fails, the operation on the corresponding row is not performed.
- A BEFORE trigger is activated by the attempt to insert or modify the row, regardless of whether the attempt subsequently succeeds.
- An AFTER trigger is executed only if any BEFORE triggers and the row operation execute successfully.
- An error during either a BEFORE or AFTER trigger results in failure of the entire statement that caused trigger invocation.
- For transactional tables, failure of a statement should cause rollback of all changes performed by the statement. Failure of a trigger causes the statement to fail, so trigger failure also causes rollback. For nontransactional tables, such rollback cannot be done, so although the statement fails, any changes performed prior to the point of the error remain in effect.

Triggers can contain direct references to tables by name, such as the trigger named testref shown in this example:

```
CREATE TABLE test1(a1 INT);
CREATE TABLE test2(a2 INT);
CREATE TABLE test3(a3 INT NOT NULL AUTO_INCREMENT PRIMARY KEY);
```

```
CREATE TABLE test4(
 a4 INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 b4 INT DEFAULT 0
);
delimiter |
CREATE TRIGGER testref BEFORE INSERT ON test1
 FOR EACH ROW
 BEGIN
 INSERT INTO test2 SET a2 = NEW.a1;
 DELETE FROM test3 WHERE a3 = NEW.a1;
 UPDATE test4 SET b4 = b4 + 1 WHERE a4 = NEW.a1;
 END;
|
delimiter ;
INSERT INTO test3 (a3) VALUES
 (NULL), (NULL), (NULL), (NULL), (NULL),
 (NULL), (NULL), (NULL), (NULL), (NULL);
INSERT INTO test4 (a4) VALUES
 (0), (0), (0), (0), (0), (0), (0), (0), (0), (0);
```

Suppose that you insert the following values into table test1 as shown here:

```
mysql> INSERT INTO test1 VALUES 
 (1), (3), (1), (7), (1), (8), (4), (4);
Query OK, 8 rows affected (0.01 sec)
Records: 8 Duplicates: 0 Warnings: 0
```

As a result, the four tables contain the following data:

```
mysql> SELECT * FROM test1;
+------+
| a1 |
+------+
| 1 |
| 3 |
| 1 |
| 7 |
| 1 |
| 8 |
| 4 |
| 4 |
+------+
8 rows in set (0.00 sec)
mysql> SELECT * FROM test2;
+------+
| a2 |
+------+
| 1 |
| 3 |
| 1 |
| 7 |
| 1 |
| 8 |
| 4 |
| 4 |
+------+
8 rows in set (0.00 sec)
mysql> SELECT * FROM test3;
+----+
| a3 |
+----+
| 2 |
| 5 |
| 6 |
| 9 |
```

```
| 10 |
+----+
5 rows in set (0.00 sec)
mysql> SELECT * FROM test4;
+----+------+
| a4 | b4 |
+----+------+
| 1 | 3 |
| 2 | 0 |
| 3 | 1 |
| 4 | 2 |
| 5 | 0 |
| 6 | 0 |
| 7 | 1 |
| 8 | 1 |
| 9 | 0 |
| 10 | 0 |
+----+------+
10 rows in set (0.00 sec)
```

# <span id="page-163-1"></span>**27.3.2 Trigger Metadata**

To obtain metadata about triggers:

- Query the TRIGGERS table of the INFORMATION\_SCHEMA database. See Section 28.3.45, "The INFORMATION\_SCHEMA TRIGGERS Table".
- Use the SHOW CREATE TRIGGER statement. See Section 15.7.7.11, "SHOW CREATE TRIGGER Statement".
- Use the SHOW TRIGGERS statement. See Section 15.7.7.40, "SHOW TRIGGERS Statement".

# <span id="page-163-0"></span>**27.4 Using the Event Scheduler**

The MySQL Event Scheduler manages the scheduling and execution of events, that is, tasks that run according to a schedule. The following discussion covers the Event Scheduler and is divided into the following sections:

- [Section 27.4.1, "Event Scheduler Overview",](#page-164-0) provides an introduction to and conceptual overview of MySQL Events.
- [Section 27.4.3, "Event Syntax"](#page-167-0), discusses the SQL statements for creating, altering, and dropping MySQL Events.
- [Section 27.4.4, "Event Metadata"](#page-167-1), shows how to obtain information about events and how this information is stored by the MySQL Server.
- [Section 27.4.6, "The Event Scheduler and MySQL Privileges"](#page-168-1), discusses the privileges required to work with events and the ramifications that events have with regard to privileges when executing.

Stored routines require the events data dictionary table in the mysql system database. This table is created during the MySQL 8.0 installation procedure. If you are upgrading to MySQL 8.0 from an earlier version, be sure to perform the upgrade procedure to make sure that your system database is up to date. See Chapter 3, Upgrading MySQL.

# **Additional Resources**

- There are some restrictions on the use of events; see [Section 27.8, "Restrictions on Stored](#page-186-0) [Programs".](#page-186-0)
- Binary logging for events takes place as described in [Section 27.7, "Stored Program Binary Logging"](#page-180-0).
- You may also find the [MySQL User Forums](https://forums.mysql.com/list.php?20) to be helpful.

## <span id="page-164-0"></span>**27.4.1 Event Scheduler Overview**

MySQL Events are tasks that run according to a schedule. Therefore, we sometimes refer to them as scheduled events. When you create an event, you are creating a named database object containing one or more SQL statements to be executed at one or more regular intervals, beginning and ending at a specific date and time. Conceptually, this is similar to the idea of the Unix crontab (also known as a "cron job") or the Windows Task Scheduler.

Scheduled tasks of this type are also sometimes known as "temporal triggers", implying that these are objects that are triggered by the passage of time. While this is essentially correct, we prefer to use the term events to avoid confusion with triggers of the type discussed in [Section 27.3, "Using Triggers"](#page-158-2). Events should more specifically not be confused with "temporary triggers". Whereas a trigger is a database object whose statements are executed in response to a specific type of event that occurs on a given table, a (scheduled) event is an object whose statements are executed in response to the passage of a specified time interval.

While there is no provision in the SQL Standard for event scheduling, there are precedents in other database systems, and you may notice some similarities between these implementations and that found in the MySQL Server.

MySQL Events have the following major features and properties:

- In MySQL, an event is uniquely identified by its name and the schema to which it is assigned.
- An event performs a specific action according to a schedule. This action consists of an SQL statement, which can be a compound statement in a BEGIN ... END block if desired (see Section 15.6, "Compound Statement Syntax"). An event's timing can be either one-time or recurrent. A one-time event executes one time only. A recurrent event repeats its action at a regular interval, and the schedule for a recurring event can be assigned a specific start day and time, end day and time, both, or neither. (By default, a recurring event's schedule begins as soon as it is created, and continues indefinitely, until it is disabled or dropped.)

If a repeating event does not terminate within its scheduling interval, the result may be multiple instances of the event executing simultaneously. If this is undesirable, you should institute a mechanism to prevent simultaneous instances. For example, you could use the GET\_LOCK() function, or row or table locking.

- Users can create, modify, and drop scheduled events using SQL statements intended for these purposes. Syntactically invalid event creation and modification statements fail with an appropriate error message. A user may include statements in an event's action which require privileges that the user does not actually have. The event creation or modification statement succeeds but the event's action fails. See [Section 27.4.6, "The Event Scheduler and MySQL Privileges"](#page-168-1) for details.
- Many of the properties of an event can be set or modified using SQL statements. These properties include the event's name, timing, persistence (that is, whether it is preserved following the expiration of its schedule), status (enabled or disabled), action to be performed, and the schema to which it is assigned. See Section 15.1.3, "ALTER EVENT Statement".

The default definer of an event is the user who created the event, unless the event has been altered, in which case the definer is the user who issued the last ALTER EVENT statement affecting that event. An event can be modified by any user having the EVENT privilege on the database for which the event is defined. See [Section 27.4.6, "The Event Scheduler and MySQL Privileges"](#page-168-1).

• An event's action statement may include most SQL statements permitted within stored routines. For restrictions, see [Section 27.8, "Restrictions on Stored Programs"](#page-186-0).

# <span id="page-164-1"></span>**27.4.2 Event Scheduler Configuration**

Events are executed by a special event scheduler thread; when we refer to the Event Scheduler, we actually refer to this thread. When running, the event scheduler thread and its current state can be

seen by users having the PROCESS privilege in the output of SHOW PROCESSLIST, as shown in the discussion that follows.

The global event\_scheduler system variable determines whether the Event Scheduler is enabled and running on the server. It has one of the following values, which affect event scheduling as described:

• ON: The Event Scheduler is started; the event scheduler thread runs and executes all scheduled events. ON is the default event\_scheduler value.

When the Event Scheduler is ON, the event scheduler thread is listed in the output of SHOW PROCESSLIST as a daemon process, and its state is represented as shown here:

```
mysql> SHOW PROCESSLIST\G
*************************** 1. row ***************************
 Id: 1
 User: root
 Host: localhost
 db: NULL
Command: Query
 Time: 0
 State: NULL
 Info: show processlist
*************************** 2. row ***************************
 Id: 2
 User: event_scheduler
 Host: localhost
 db: NULL
Command: Daemon
 Time: 3
 State: Waiting for next activation
 Info: NULL
2 rows in set (0.00 sec)
```

Event scheduling can be stopped by setting the value of event\_scheduler to OFF.

• OFF: The Event Scheduler is stopped. The event scheduler thread does not run, is not shown in the output of SHOW PROCESSLIST, and no scheduled events execute.

When the Event Scheduler is stopped (event\_scheduler is OFF), it can be started by setting the value of event\_scheduler to ON. (See next item.)

• DISABLED: This value renders the Event Scheduler nonoperational. When the Event Scheduler is DISABLED, the event scheduler thread does not run (and so does not appear in the output of SHOW PROCESSLIST). In addition, the Event Scheduler state cannot be changed at runtime.

If the Event Scheduler status has not been set to DISABLED, event\_scheduler can be toggled between ON and OFF (using SET). It is also possible to use 0 for OFF, and 1 for ON when setting this variable. Thus, any of the following 4 statements can be used in the mysql client to turn on the Event Scheduler:

```
SET GLOBAL event_scheduler = ON;
SET @@GLOBAL.event_scheduler = ON;
SET GLOBAL event_scheduler = 1;
SET @@GLOBAL.event_scheduler = 1;
```

Similarly, any of these 4 statements can be used to turn off the Event Scheduler:

```
SET GLOBAL event_scheduler = OFF;
SET @@GLOBAL.event_scheduler = OFF;
SET GLOBAL event_scheduler = 0;
SET @@GLOBAL.event_scheduler = 0;
```

![](_page_165_Picture_14.jpeg)

#### **Note**

If the Event Scheduler is enabled, enabling the super\_read\_only system variable prevents it from updating event "last executed" timestamps in the

events data dictionary table. This causes the Event Scheduler to stop the next time it tries to execute a scheduled event, after writing a message to the server error log. (In this situation the event\_scheduler system variable does not change from ON to OFF. An implication is that this variable rejects the DBA intent that the Event Scheduler be enabled or disabled, where its actual status of started or stopped may be distinct.). If super\_read\_only is subsequently disabled after being enabled, the server automatically restarts the Event Scheduler as needed, as of MySQL 8.0.26. Prior to MySQL 8.0.26, it is necessary to manually restart the Event Scheduler by enabling it again.

Although ON and OFF have numeric equivalents, the value displayed for event\_scheduler by SELECT or SHOW VARIABLES is always one of OFF, ON, or DISABLED. DISABLED has no numeric equivalent. For this reason, ON and OFF are usually preferred over 1 and 0 when setting this variable.

Note that attempting to set event\_scheduler without specifying it as a global variable causes an error:

```
mysql< SET @@event_scheduler = OFF;
ERROR 1229 (HY000): Variable 'event_scheduler' is a GLOBAL
variable and should be set with SET GLOBAL
```

![](_page_166_Picture_5.jpeg)

#### **Important**

It is possible to set the Event Scheduler to DISABLED only at server startup. If event\_scheduler is ON or OFF, you cannot set it to DISABLED at runtime. Also, if the Event Scheduler is set to DISABLED at startup, you cannot change the value of event\_scheduler at runtime.

To disable the event scheduler, use one of the following two methods:

• As a command-line option when starting the server:

```
--event-scheduler=DISABLED
```

• In the server configuration file (my.cnf, or my.ini on Windows systems), include the line where it can be read by the server (for example, in a [mysqld] section):

```
event_scheduler=DISABLED
```

To enable the Event Scheduler, restart the server without the --event-scheduler=DISABLED command-line option, or after removing or commenting out the line containing eventscheduler=DISABLED in the server configuration file, as appropriate. Alternatively, you can use ON (or 1) or OFF (or 0) in place of the DISABLED value when starting the server.

![](_page_166_Picture_14.jpeg)

### **Note**

You can issue event-manipulation statements when event\_scheduler is set to DISABLED. No warnings or errors are generated in such cases (provided that the statements are themselves valid). However, scheduled events cannot execute until this variable is set to ON (or 1). Once this has been done, the event scheduler thread executes all events whose scheduling conditions are satisfied.

Starting the MySQL server with the --skip-grant-tables option causes event\_scheduler to be set to DISABLED, overriding any other value set either on the command line or in the my.cnf or my.ini file (Bug #26807).

For SQL statements used to create, alter, and drop events, see [Section 27.4.3, "Event Syntax"](#page-167-0).

MySQL provides an EVENTS table in the INFORMATION\_SCHEMA database. This table can be queried to obtain information about scheduled events which have been defined on the server. See [Section 27.4.4, "Event Metadata"](#page-167-1), and Section 28.3.14, "The INFORMATION\_SCHEMA EVENTS Table", for more information.

For information regarding event scheduling and the MySQL privilege system, see [Section 27.4.6, "The](#page-168-1) [Event Scheduler and MySQL Privileges"](#page-168-1).

# <span id="page-167-0"></span>**27.4.3 Event Syntax**

MySQL provides several SQL statements for working with scheduled events:

- New events are defined using the CREATE EVENT statement. See Section 15.1.13, "CREATE EVENT Statement".
- The definition of an existing event can be changed by means of the ALTER EVENT statement. See Section 15.1.3, "ALTER EVENT Statement".
- When a scheduled event is no longer wanted or needed, it can be deleted from the server by its definer using the DROP EVENT statement. See Section 15.1.25, "DROP EVENT Statement". Whether an event persists past the end of its schedule also depends on its ON COMPLETION clause, if it has one. See Section 15.1.13, "CREATE EVENT Statement".

An event can be dropped by any user having the EVENT privilege for the database on which the event is defined. See [Section 27.4.6, "The Event Scheduler and MySQL Privileges"](#page-168-1).

## <span id="page-167-1"></span>**27.4.4 Event Metadata**

To obtain metadata about events:

- Query the EVENTS table of the INFORMATION\_SCHEMA database. See Section 28.3.14, "The INFORMATION\_SCHEMA EVENTS Table".
- Use the SHOW CREATE EVENT statement. See Section 15.7.7.7, "SHOW CREATE EVENT Statement".
- Use the SHOW EVENTS statement. See Section 15.7.7.18, "SHOW EVENTS Statement".

#### **Event Scheduler Time Representation**

Each session in MySQL has a session time zone (STZ). This is the session time\_zone value that is initialized from the server's global time\_zone value when the session begins but may be changed during the session.

The session time zone that is current when a CREATE EVENT or ALTER EVENT statement executes is used to interpret times specified in the event definition. This becomes the event time zone (ETZ); that is, the time zone that is used for event scheduling and is in effect within the event as it executes.

For representation of event information in the data dictionary, the execute\_at, starts, and ends times are converted to UTC and stored along with the event time zone. This enables event execution to proceed as defined regardless of any subsequent changes to the server time zone or daylight saving time effects. The last\_executed time is also stored in UTC.

Event times can be obtained by selecting from the Information Schema EVENTS table or from SHOW EVENTS, but they are reported as ETZ or STZ values. The following table summarizes representation of event times.

| Value         | EVENTS Table | SHOW EVENTS |
|---------------|--------------|-------------|
| Execute at    | ETZ          | ETZ         |
| Starts        | ETZ          | ETZ         |
| Ends          | ETZ          | ETZ         |
| Last executed | ETZ          | n/a         |
| Created       | STZ          | n/a         |
| Last altered  | STZ          | n/a         |

## <span id="page-168-0"></span>**27.4.5 Event Scheduler Status**

The Event Scheduler writes information about event execution that terminates with an error or warning to the MySQL Server's error log. See [Section 27.4.6, "The Event Scheduler and MySQL Privileges"](#page-168-1) for an example.

To obtain information about the state of the Event Scheduler for debugging and troubleshooting purposes, run mysqladmin debug (see Section 6.5.2, "mysqladmin — A MySQL Server Administration Program"); after running this command, the server's error log contains output relating to the Event Scheduler, similar to what is shown here:

```
Events status:
LLA = Last Locked At LUA = Last Unlocked At
WOC = Waiting On Condition DL = Data Locked
Event scheduler status:
State : INITIALIZED
Thread id : 0
LLA : n/a:0
LUA : n/a:0
WOC : NO
Workers : 0
Executed : 0
Data locked: NO
Event queue status:
Element count : 0
Data locked : NO
Attempting lock : NO
LLA : init_queue:95
LUA : init_queue:103
WOC : NO
Next activation : never
```

In statements that occur as part of events executed by the Event Scheduler, diagnostics messages (not only errors, but also warnings) are written to the error log, and, on Windows, to the application event log. For frequently executed events, it is possible for this to result in many logged messages. For example, for SELECT ... INTO var\_list statements, if the query returns no rows, a warning with error code 1329 occurs (No data), and the variable values remain unchanged. If the query returns multiple rows, error 1172 occurs (Result consisted of more than one row). For either condition, you can avoid having the warnings be logged by declaring a condition handler; see Section 15.6.7.2, "DECLARE ... HANDLER Statement". For statements that may retrieve multiple rows, another strategy is to use LIMIT 1 to limit the result set to a single row.

# <span id="page-168-1"></span>**27.4.6 The Event Scheduler and MySQL Privileges**

To enable or disable the execution of scheduled events, it is necessary to set the value of the global event\_scheduler system variable. This requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

The EVENT privilege governs the creation, modification, and deletion of events. This privilege can be bestowed using GRANT. For example, this GRANT statement confers the EVENT privilege for the schema named myschema on the user jon@ghidora:

```
GRANT EVENT ON myschema.* TO jon@ghidora;
```

(We assume that this user account already exists, and that we wish for it to remain unchanged otherwise.)

To grant this same user the EVENT privilege on all schemas, use the following statement:

```
GRANT EVENT ON *.* TO jon@ghidora;
```

The EVENT privilege has global or schema-level scope. Therefore, trying to grant it on a single table results in an error as shown:

```
mysql> GRANT EVENT ON myschema.mytable TO jon@ghidora;
ERROR 1144 (42000): Illegal GRANT/REVOKE command; please
consult the manual to see which privileges can be used
```

It is important to understand that an event is executed with the privileges of its definer, and that it cannot perform any actions for which its definer does not have the requisite privileges. For example, suppose that jon@ghidora has the EVENT privilege for myschema. Suppose also that this user has the SELECT privilege for myschema, but no other privileges for this schema. It is possible for jon@ghidora to create a new event such as this one:

```
CREATE EVENT e_store_ts
 ON SCHEDULE
 EVERY 10 SECOND
 DO
 INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP());
```

The user waits for a minute or so, and then performs a SELECT \* FROM mytable; query, expecting to see several new rows in the table. Instead, the table is empty. Since the user does not have the INSERT privilege for the table in question, the event has no effect.

If you inspect the MySQL error log (hostname.err), you can see that the event is executing, but the action it is attempting to perform fails:

```
2013-09-24T12:41:31.261992Z 25 [ERROR] Event Scheduler:
[jon@ghidora][cookbook.e_store_ts] INSERT command denied to user
'jon'@'ghidora' for table 'mytable'
2013-09-24T12:41:31.262022Z 25 [Note] Event Scheduler:
[jon@ghidora].[myschema.e_store_ts] event execution failed.
2013-09-24T12:41:41.271796Z 26 [ERROR] Event Scheduler:
[jon@ghidora][cookbook.e_store_ts] INSERT command denied to user
'jon'@'ghidora' for table 'mytable'
2013-09-24T12:41:41.272761Z 26 [Note] Event Scheduler:
[jon@ghidora].[myschema.e_store_ts] event execution failed.
```

Since this user very likely does not have access to the error log, it is possible to verify whether the event's action statement is valid by executing it directly:

```
mysql> INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP());
ERROR 1142 (42000): INSERT command denied to user
'jon'@'ghidora' for table 'mytable'
```

Inspection of the Information Schema EVENTS table shows that e\_store\_ts exists and is enabled, but its LAST\_EXECUTED column is NULL:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.EVENTS
 > WHERE EVENT_NAME='e_store_ts'
 > AND EVENT_SCHEMA='myschema'\G
*************************** 1. row ***************************
 EVENT_CATALOG: NULL
 EVENT_SCHEMA: myschema
 EVENT_NAME: e_store_ts
 DEFINER: jon@ghidora
 EVENT_BODY: SQL
EVENT_DEFINITION: INSERT INTO myschema.mytable VALUES (UNIX_TIMESTAMP())
 EVENT_TYPE: RECURRING
 EXECUTE_AT: NULL
 INTERVAL_VALUE: 5
 INTERVAL_FIELD: SECOND
 SQL_MODE: NULL
 STARTS: 0000-00-00 00:00:00
 ENDS: 0000-00-00 00:00:00
 STATUS: ENABLED
 ON_COMPLETION: NOT PRESERVE
 CREATED: 2006-02-09 22:36:06
 LAST_ALTERED: 2006-02-09 22:36:06
 LAST_EXECUTED: NULL
 EVENT_COMMENT:
1 row in set (0.00 sec)
```

To rescind the EVENT privilege, use the REVOKE statement. In this example, the EVENT privilege on the schema myschema is removed from the jon@ghidora user account:

REVOKE EVENT ON myschema.\* FROM jon@ghidora;

![](_page_170_Picture_3.jpeg)

#### **Important**

Revoking the EVENT privilege from a user does not delete or disable any events that may have been created by that user.

An event is not migrated or dropped as a result of renaming or dropping the user who created it.

Suppose that the user jon@ghidora has been granted the EVENT and INSERT privileges on the myschema schema. This user then creates the following event:

```
CREATE EVENT e_insert
 ON SCHEDULE
 EVERY 7 SECOND
 DO
 INSERT INTO myschema.mytable;
```

After this event has been created, root revokes the EVENT privilege for jon@ghidora. However, e\_insert continues to execute, inserting a new row into mytable each seven seconds. The same would be true if root had issued either of these statements:

- DROP USER jon@ghidora;
- RENAME USER jon@ghidora TO someotherguy@ghidora;

You can verify that this is true by examining the Information Schema EVENTS table before and after issuing a DROP USER or RENAME USER statement.

Event definitions are stored in the data dictionary. To drop an event created by another user account, you must be the MySQL root user or another user with the necessary privileges.

Users' EVENT privileges are stored in the Event\_priv columns of the mysql.user and mysql.db tables. In both cases, this column holds one of the values 'Y' or 'N'. 'N' is the default. mysql.user.Event\_priv is set to 'Y' for a given user only if that user has the global EVENT privilege (that is, if the privilege was bestowed using GRANT EVENT ON \*.\*). For a schema-level EVENT privilege, GRANT creates a row in mysql.db and sets that row's Db column to the name of the schema, the User column to the name of the user, and the Event\_priv column to 'Y'. There should never be any need to manipulate these tables directly, since the GRANT EVENT and REVOKE EVENT statements perform the required operations on them.

Five status variables provide counts of event-related operations (but not of statements executed by events; see [Section 27.8, "Restrictions on Stored Programs"](#page-186-0)). These are:

- Com\_create\_event: The number of CREATE EVENT statements executed since the last server restart.
- Com\_alter\_event: The number of ALTER EVENT statements executed since the last server restart.
- Com\_drop\_event: The number of DROP EVENT statements executed since the last server restart.
- Com\_show\_create\_event: The number of SHOW CREATE EVENT statements executed since the last server restart.
- Com\_show\_events: The number of SHOW EVENTS statements executed since the last server restart.

You can view current values for all of these at one time by running the statement SHOW STATUS LIKE '%event%';.

# <span id="page-171-0"></span>**27.5 Using Views**

MySQL supports views, including updatable views. Views are stored queries that when invoked produce a result set. A view acts as a virtual table.

The following discussion describes the syntax for creating and dropping views, and shows some examples of how to use them.

## **Additional Resources**

- You may find the [MySQL User Forums](https://forums.mysql.com/list.php?20) helpful when working with views.
- For answers to some commonly asked questions regarding views in MySQL, see Section A.6, "MySQL 8.0 FAQ: Views".
- There are some restrictions on the use of views; see [Section 27.9, "Restrictions on Views".](#page-189-0)

## <span id="page-171-1"></span>**27.5.1 View Syntax**

The CREATE VIEW statement creates a new view (see Section 15.1.23, "CREATE VIEW Statement"). To alter the definition of a view or drop a view, use ALTER VIEW (see Section 15.1.11, "ALTER VIEW Statement"), or DROP VIEW (see Section 15.1.35, "DROP VIEW Statement").

A view can be created from many kinds of SELECT statements. It can refer to base tables or other views. It can use joins, UNION, and subqueries. The SELECT need not even refer to any tables. The following example defines a view that selects two columns from another table, as well as an expression calculated from those columns:

```
mysql> CREATE TABLE t (qty INT, price INT);
mysql> INSERT INTO t VALUES(3, 50), (5, 60);
mysql> CREATE VIEW v AS SELECT qty, price, qty*price AS value FROM t;
mysql> SELECT * FROM v;
+------+-------+-------+
| qty | price | value |
+------+-------+-------+
| 3 | 50 | 150 |
| 5 | 60 | 300 |
+------+-------+-------+
mysql> SELECT * FROM v WHERE qty = 5;
+------+-------+-------+
| qty | price | value |
+------+-------+-------+
| 5 | 60 | 300 |
+------+-------+-------+
```

# <span id="page-171-2"></span>**27.5.2 View Processing Algorithms**

The optional ALGORITHM clause for CREATE VIEW or ALTER VIEW is a MySQL extension to standard SQL. It affects how MySQL processes the view. ALGORITHM takes three values: MERGE, TEMPTABLE, or UNDEFINED.

- For MERGE, the text of a statement that refers to the view and the view definition are merged such that parts of the view definition replace corresponding parts of the statement.
- For TEMPTABLE, the results from the view are retrieved into a temporary table, which then is used to execute the statement.
- For UNDEFINED, MySQL chooses which algorithm to use. It prefers MERGE over TEMPTABLE if possible, because MERGE is usually more efficient and because a view cannot be updated if a temporary table is used.
- If no ALGORITHM clause is present, the default algorithm is determined by the value of the derived\_merge flag of the optimizer\_switch system variable. For additional discussion, see

Section 10.2.2.4, "Optimizing Derived Tables, View References, and Common Table Expressions with Merging or Materialization".

A reason to specify TEMPTABLE explicitly is that locks can be released on underlying tables after the temporary table has been created and before it is used to finish processing the statement. This might result in quicker lock release than the MERGE algorithm so that other clients that use the view are not blocked as long.

A view algorithm can be UNDEFINED for three reasons:

- No ALGORITHM clause is present in the CREATE VIEW statement.
- The CREATE VIEW statement has an explicit ALGORITHM = UNDEFINED clause.
- ALGORITHM = MERGE is specified for a view that can be processed only with a temporary table. In this case, MySQL generates a warning and sets the algorithm to UNDEFINED.

As mentioned earlier, MERGE is handled by merging corresponding parts of a view definition into the statement that refers to the view. The following examples briefly illustrate how the MERGE algorithm works. The examples assume that there is a view v\_merge that has this definition:

```
CREATE ALGORITHM = MERGE VIEW v_merge (vc1, vc2) AS
SELECT c1, c2 FROM t WHERE c3 > 100;
```

Example 1: Suppose that we issue this statement:

```
SELECT * FROM v_merge;
```

MySQL handles the statement as follows:

- v\_merge becomes t
- \* becomes vc1, vc2, which corresponds to c1, c2
- The view WHERE clause is added

The resulting statement to be executed becomes:

```
SELECT c1, c2 FROM t WHERE c3 > 100;
```

Example 2: Suppose that we issue this statement:

```
SELECT * FROM v_merge WHERE vc1 < 100;
```

This statement is handled similarly to the previous one, except that vc1 < 100 becomes c1 < 100 and the view WHERE clause is added to the statement WHERE clause using an AND connective (and parentheses are added to make sure the parts of the clause are executed with correct precedence). The resulting statement to be executed becomes:

```
SELECT c1, c2 FROM t WHERE (c3 > 100) AND (c1 < 100);
```

Effectively, the statement to be executed has a WHERE clause of this form:

```
WHERE (select WHERE) AND (view WHERE)
```

If the MERGE algorithm cannot be used, a temporary table must be used instead. Constructs that prevent merging are the same as those that prevent merging in derived tables and common table expressions. Examples are SELECT DISTINCT or LIMIT in the subquery. For details, see Section 10.2.2.4, "Optimizing Derived Tables, View References, and Common Table Expressions with Merging or Materialization".

# <span id="page-172-0"></span>**27.5.3 Updatable and Insertable Views**

Some views are updatable and references to them can be used to specify tables to be updated in data change statements. That is, you can use them in statements such as UPDATE, DELETE, or INSERT to update the contents of the underlying table. Derived tables and common table expressions can also be specified in multiple-table UPDATE and DELETE statements, but can only be used for reading data to specify rows to be updated or deleted. Generally, the view references must be updatable, meaning that they may be merged and not materialized. Composite views have more complex rules.

For a view to be updatable, there must be a one-to-one relationship between the rows in the view and the rows in the underlying table. There are also certain other constructs that make a view nonupdatable. To be more specific, a view is not updatable if it contains any of the following:

- Aggregate functions or window functions (SUM(), MIN(), MAX(), COUNT(), and so forth)
- DISTINCT
- GROUP BY
- HAVING
- UNION or UNION ALL
- Subquery in the select list

Nondependent subqueries in the select list fail for INSERT, but are okay for UPDATE, DELETE. For dependent subqueries in the select list, no data change statements are permitted.

- Certain joins (see additional join discussion later in this section)
- Reference to nonupdatable view in the FROM clause
- Subquery in the WHERE clause that refers to a table in the FROM clause
- Refers only to literal values (in this case, there is no underlying table to update)
- ALGORITHM = TEMPTABLE (use of a temporary table always makes a view nonupdatable)
- Multiple references to any column of a base table (fails for INSERT, okay for UPDATE, DELETE)

A generated column in a view is considered updatable because it is possible to assign to it. However, if such a column is updated explicitly, the only permitted value is DEFAULT. For information about generated columns, see Section 15.1.20.8, "CREATE TABLE and Generated Columns".

It is sometimes possible for a multiple-table view to be updatable, assuming that it can be processed with the MERGE algorithm. For this to work, the view must use an inner join (not an outer join or a UNION). Also, only a single table in the view definition can be updated, so the SET clause must name only columns from one of the tables in the view. Views that use UNION ALL are not permitted even though they might be theoretically updatable.

With respect to insertability (being updatable with INSERT statements), an updatable view is insertable if it also satisfies these additional requirements for the view columns:

- There must be no duplicate view column names.
- The view must contain all columns in the base table that do not have a default value.
- The view columns must be simple column references. They must not be expressions, such as these:

```
3.14159
col1 + 3
UPPER(col2)
col3 / col4
(subquery)
```

MySQL sets a flag, called the view updatability flag, at CREATE VIEW time. The flag is set to YES (true) if UPDATE and DELETE (and similar operations) are legal for the view. Otherwise, the flag is set to NO (false). The IS\_UPDATABLE column in the Information Schema VIEWS table displays the status of this flag. It means that the server always knows whether a view is updatable.

If a view is not updatable, statements such UPDATE, DELETE, and INSERT are illegal and are rejected. (Even if a view is updatable, it might not be possible to insert into it, as described elsewhere in this section.)

The updatability of views may be affected by the value of the updatable\_views\_with\_limit system variable. See Section 7.1.8, "Server System Variables".

For the following discussion, suppose that these tables and views exist:

```
CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (c INTEGER);
CREATE VIEW vmat AS SELECT SUM(x) AS s FROM t1;
CREATE VIEW vup AS SELECT * FROM t2;
CREATE VIEW vjoin AS SELECT * FROM vmat JOIN vup ON vmat.s=vup.c;
```

INSERT, UPDATE, and DELETE statements are permitted as follows:

• INSERT: The insert table of an INSERT statement may be a view reference that is merged. If the view is a join view, all components of the view must be updatable (not materialized). For a multipletable updatable view, INSERT can work if it inserts into a single table.

This statement is invalid because one component of the join view is nonupdatable:

```
INSERT INTO vjoin (c) VALUES (1);
```

This statement is valid; the view contains no materialized components:

```
INSERT INTO vup (c) VALUES (1);
```

• UPDATE: The table or tables to be updated in an UPDATE statement may be view references that are merged. If a view is a join view, at least one component of the view must be updatable (this differs from INSERT).

In a multiple-table UPDATE statement, the updated table references of the statement must be base tables or updatable view references. Nonupdated table references may be materialized views or derived tables.

This statement is valid; column c is from the updatable part of the join view:

```
UPDATE vjoin SET c=c+1;
```

This statement is invalid; column x is from the nonupdatable part:

```
UPDATE vjoin SET x=x+1;
```

This statement is valid; the updated table reference of the multiple-table UPDATE is an updatable view (vup):

```
UPDATE vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...
SET c=c+1;
```

This statement is invalid; it tries to update a materialized derived table:

```
UPDATE vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...
SET s=s+1;
```

• DELETE: The table or tables to be deleted from in a DELETE statement must be merged views. Join views are not allowed (this differs from INSERT and UPDATE).

This statement is invalid because the view is a join view:

```
DELETE vjoin WHERE ...;
```

This statement is valid because the view is a merged (updatable) view:

```
DELETE vup WHERE ...;
```

This statement is valid because it deletes from a merged (updatable) view:

```
DELETE vup FROM vup JOIN (SELECT SUM(x) AS s FROM t1) AS dt ON ...;
```

Additional discussion and examples follow.

Earlier discussion in this section pointed out that a view is not insertable if not all columns are simple column references (for example, if it contains columns that are expressions or composite expressions). Although such a view is not insertable, it can be updatable if you update only columns that are not expressions. Consider this view:

```
CREATE VIEW v AS SELECT col1, 1 AS col2 FROM t;
```

This view is not insertable because col2 is an expression. But it is updatable if the update does not try to update col2. This update is permissible:

```
UPDATE v SET col1 = 0;
```

This update is not permissible because it attempts to update an expression column:

```
UPDATE v SET col2 = 0;
```

If a table contains an AUTO\_INCREMENT column, inserting into an insertable view on the table that does not include the AUTO\_INCREMENT column does not change the value of LAST\_INSERT\_ID(), because the side effects of inserting default values into columns not part of the view should not be visible.

## <span id="page-175-0"></span>**27.5.4 The View WITH CHECK OPTION Clause**

The WITH CHECK OPTION clause can be given for an updatable view to prevent inserts to rows for which the WHERE clause in the select\_statement is not true. It also prevents updates to rows for which the WHERE clause is true but the update would cause it to be not true (in other words, it prevents visible rows from being updated to nonvisible rows).

In a WITH CHECK OPTION clause for an updatable view, the LOCAL and CASCADED keywords determine the scope of check testing when the view is defined in terms of another view. When neither keyword is given, the default is CASCADED.

WITH CHECK OPTION testing is standard-compliant:

- With LOCAL, the view WHERE clause is checked, then checking recurses to underlying views and applies the same rules.
- With CASCADED, the view WHERE clause is checked, then checking recurses to underlying views, adds WITH CASCADED CHECK OPTION to them (for purposes of the check; their definitions remain unchanged), and applies the same rules.
- With no check option, the view WHERE clause is not checked, then checking recurses to underlying views, and applies the same rules.

Consider the definitions for the following table and set of views:

```
CREATE TABLE t1 (a INT);
CREATE VIEW v1 AS SELECT * FROM t1 WHERE a < 2
WITH CHECK OPTION;
CREATE VIEW v2 AS SELECT * FROM v1 WHERE a > 0
WITH LOCAL CHECK OPTION;
CREATE VIEW v3 AS SELECT * FROM v1 WHERE a > 0
WITH CASCADED CHECK OPTION;
```

Here the v2 and v3 views are defined in terms of another view, v1.

Inserts for v2 are checked against its LOCAL check option, then the check recurses to v1 and the rules are applied again. The rules for v1 cause a check failure. The check for v3 also fails:

```
mysql> INSERT INTO v2 VALUES (2);
ERROR 1369 (HY000): CHECK OPTION failed 'test.v2'
mysql> INSERT INTO v3 VALUES (2);
ERROR 1369 (HY000): CHECK OPTION failed 'test.v3'
```

## <span id="page-176-0"></span>**27.5.5 View Metadata**

To obtain metadata about views:

- Query the VIEWS table of the INFORMATION\_SCHEMA database. See Section 28.3.48, "The INFORMATION\_SCHEMA VIEWS Table".
- Use the SHOW CREATE VIEW statement. See Section 15.7.7.13, "SHOW CREATE VIEW Statement".

# <span id="page-176-1"></span>**27.6 Stored Object Access Control**

Stored programs (procedures, functions, triggers, and events) and views are defined prior to use and, when referenced, execute within a security context that determines their privileges. The privileges applicable to execution of a stored object are controlled by its DEFINER attribute and SQL SECURITY characteristic.

- [The DEFINER Attribute](#page-176-2)
- [The SQL SECURITY Characteristic](#page-176-3)
- [Examples](#page-177-0)
- [Orphan Stored Objects](#page-177-1)
- [Risk-Minimization Guidelines](#page-179-0)

## <span id="page-176-2"></span>**The DEFINER Attribute**

A stored object definition can include a DEFINER attribute that names a MySQL account. If a definition omits the DEFINER attribute, the default object definer is the user who creates it.

The following rules determine which accounts you can specify as the DEFINER attribute for a stored object:

- If you have the SET\_USER\_ID privilege (or the deprecated SUPER privilege), you can specify any account as the DEFINER attribute. If the account does not exist, a warning is generated. Additionally, to set a stored object DEFINER attribute to an account that has the SYSTEM\_USER privilege, you must have the SYSTEM\_USER privilege.
- Otherwise, the only permitted account is your own, specified either literally or as CURRENT\_USER or CURRENT\_USER(). You cannot set the definer to any other account.

Creating a stored object with a nonexistent DEFINER account creates an orphan object, which may have negative consequences; see [Orphan Stored Objects](#page-177-1).

## <span id="page-176-3"></span>**The SQL SECURITY Characteristic**

For stored routines (procedures and functions) and views, the object definition can include an SQL SECURITY characteristic with a value of DEFINER or INVOKER to specify whether the object executes in definer or invoker context. If the definition omits the SQL SECURITY characteristic, the default is definer context.

Triggers and events have no SQL SECURITY characteristic and always execute in definer context. The server invokes these objects automatically as necessary, so there is no invoking user.

Definer and invoker security contexts differ as follows:

- A stored object that executes in definer security context executes with the privileges of the account named by its DEFINER attribute. These privileges may be entirely different from those of the invoking user. The invoker must have appropriate privileges to reference the object (for example, EXECUTE to call a stored procedure or SELECT to select from a view), but during object execution, the invoker's privileges are ignored and only the DEFINER account privileges matter. If the DEFINER account has few privileges, the object is correspondingly limited in the operations it can perform. If the DEFINER account is highly privileged (such as an administrative account), the object can perform powerful operations no matter who invokes it.
- A stored routine or view that executes in invoker security context can perform only operations for which the invoker has privileges. The DEFINER attribute has no effect on object execution.

## <span id="page-177-0"></span>**Examples**

Consider the following stored procedure, which is declared with SQL SECURITY DEFINER to execute in definer security context:

```
CREATE DEFINER = 'admin'@'localhost' PROCEDURE p1()
SQL SECURITY DEFINER
BEGIN
 UPDATE t1 SET counter = counter + 1;
END;
```

Any user who has the EXECUTE privilege for p1 can invoke it with a CALL statement. However, when p1 executes, it does so in definer security context and thus executes with the privileges of 'admin'@'localhost', the account named as its DEFINER attribute. This account must have the EXECUTE privilege for p1 as well as the UPDATE privilege for the table t1 referenced within the object body. Otherwise, the procedure fails.

Now consider this stored procedure, which is identical to p1 except that its SQL SECURITY characteristic is INVOKER:

```
CREATE DEFINER = 'admin'@'localhost' PROCEDURE p2()
SQL SECURITY INVOKER
BEGIN
 UPDATE t1 SET counter = counter + 1;
END;
```

Unlike p1, p2 executes in invoker security context and thus with the privileges of the invoking user regardless of the DEFINER attribute value. p2 fails if the invoker lacks the EXECUTE privilege for p2 or the UPDATE privilege for the table t1.

# <span id="page-177-1"></span>**Orphan Stored Objects**

An orphan stored object is one for which its DEFINER attribute names a nonexistent account:

- An orphan stored object can be created by specifying a nonexistent DEFINER account at objectcreation time.
- An existing stored object can become orphaned through execution of a DROP USER statement that drops the object DEFINER account, or a RENAME USER statement that renames the object DEFINER account.

An orphan stored object may be problematic in these ways:

- Because the DEFINER account does not exist, the object may not work as expected if it executes in definer security context:
  - For a stored routine, an error occurs at routine execution time if the SQL SECURITY value is DEFINER but the definer account does not exist.
  - For a trigger, it is not a good idea for trigger activation to occur until the account actually does exist. Otherwise, the behavior with respect to privilege checking is undefined.

- For an event, an error occurs at event execution time if the account does not exist.
- For a view, an error occurs when the view is referenced if the SQL SECURITY value is DEFINER but the definer account does not exist.
- The object may present a security risk if the nonexistent DEFINER account is subsequently recreated for a purpose unrelated to the object. In this case, the account "adopts" the object and, with the appropriate privileges, is able to execute it even if that is not intended.

As of MySQL 8.0.22, the server imposes additional account-management security checks designed to prevent operations that (perhaps inadvertently) cause stored objects to become orphaned or that cause adoption of stored objects that are currently orphaned:

- DROP USER fails with an error if any account to be dropped is named as the DEFINER attribute for any stored object. (That is, the statement fails if dropping an account would cause a stored object to become orphaned.)
- RENAME USER fails with an error if any account to be renamed is named as the DEFINER attribute for any stored object. (That is, the statement fails if renaming an account would cause a stored object to become orphaned.)
- CREATE USER fails with an error if any account to be created is named as the DEFINER attribute for any stored object. (That is, the statement fails if creating an account would cause the account to adopt a currently orphaned stored object.)

In certain situations, it may be necessary to deliberately execute those account-management statements even when they would otherwise fail. To make this possible, if a user has the SET\_USER\_ID privilege, that privilege overrides the orphan object security checks and the statements succeed with a warning rather than failing with an error.

To obtain information about the accounts used as stored object definers in a MySQL installation, query the INFORMATION\_SCHEMA.

This query identifies which INFORMATION\_SCHEMA tables describe objects that have a DEFINER attribute:

```
mysql> SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS
 WHERE COLUMN_NAME = 'DEFINER';
+--------------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------------+------------+
| information_schema | EVENTS |
| information_schema | ROUTINES |
| information_schema | TRIGGERS |
| information_schema | VIEWS |
+--------------------+------------+
```

The result tells you which tables to query to discover which stored object DEFINER values exist and which objects have a particular DEFINER value:

• To identify which DEFINER values exist in each table, use these queries:

```
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.EVENTS;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.ROUTINES;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.TRIGGERS;
SELECT DISTINCT DEFINER FROM INFORMATION_SCHEMA.VIEWS;
```

The query results are significant for any account displayed as follows:

• If the account exists, dropping or renaming it causes stored objects to become orphaned. If you plan to drop or rename the account, consider first dropping its associated stored objects or redefining them to have a different definer.

• If the account does not exist, creating it causes it to adopt currently orphaned stored objects. If you plan to create the account, consider whether the orphaned objects should be associated with it. If not, redefine them to have a different definer.

To redefine an object with a different definer, you can use ALTER EVENT or ALTER VIEW to directly modify the DEFINER account of events and views. For stored procedures and functions and for triggers, you must drop the object and re-create it to assign a different DEFINER account

• To identify which objects have a given DEFINER account, use these queries, substituting the account of interest for user\_name@host\_name:

```
SELECT EVENT_SCHEMA, EVENT_NAME FROM INFORMATION_SCHEMA.EVENTS
WHERE DEFINER = 'user_name@host_name';
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, ROUTINE_TYPE
FROM INFORMATION_SCHEMA.ROUTINES
WHERE DEFINER = 'user_name@host_name';
SELECT TRIGGER_SCHEMA, TRIGGER_NAME FROM INFORMATION_SCHEMA.TRIGGERS
WHERE DEFINER = 'user_name@host_name';
SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS
WHERE DEFINER = 'user_name@host_name';
```

For the ROUTINES table, the query includes the ROUTINE\_TYPE column so that output rows distinguish whether the DEFINER is for a stored procedure or stored function.

If the account you are searching for does not exist, any objects displayed by those queries are orphan objects.

## <span id="page-179-0"></span>**Risk-Minimization Guidelines**

To minimize the risk potential for stored object creation and use, follow these guidelines:

- Do not create orphan stored objects; that is, objects for which the DEFINER attribute names a nonexistent account. Do not cause stored objects to become orphaned by dropping or renaming an account named by the DEFINER attribute of any existing object.
- For a stored routine or view, use SQL SECURITY INVOKER in the object definition when possible so that it can be used only by users with permissions appropriate for the operations performed by the object.
- If you create definer-context stored objects while using an account that has the SET\_USER\_ID privilege (or the deprecated SUPER privilege), specify an explicit DEFINER attribute that names an account possessing only the privileges required for the operations performed by the object. Specify a highly privileged DEFINER account only when absolutely necessary.
- Administrators can prevent users from creating stored objects that specify highly privileged DEFINER accounts by not granting them the SET\_USER\_ID privilege (or the deprecated SUPER privilege).
- Definer-context objects should be written keeping in mind that they may be able to access data for which the invoking user has no privileges. In some cases, you can prevent references to these objects by not granting unauthorized users particular privileges:
  - A stored routine cannot be referenced by a user who does not have the EXECUTE privilege for it.
  - A view cannot be referenced by a user who does not have the appropriate privilege for it (SELECT to select from it, INSERT to insert into it, and so forth).

However, no such control exists for triggers and events because they always execute in definer context. The server invokes these objects automatically as necessary, and users do not reference them directly:

• A trigger is activated by access to the table with which it is associated, even ordinary table accesses by users with no special privileges.

• An event is executed by the server on a scheduled basis.

In both cases, if the DEFINER account is highly privileged, the object may be able to perform sensitive or dangerous operations. This remains true if the privileges needed to create the object are revoked from the account of the user who created it. Administrators should be especially careful about granting users object-creation privileges.

• By default, when a routine with the SQL SECURITY DEFINER characteristic is executed, MySQL Server does not set any active roles for the MySQL account named in the DEFINER clause, only the default roles. The exception is if the activate\_all\_roles\_on\_login system variable is enabled, in which case MySQL Server sets all roles granted to the DEFINER user, including mandatory roles. Any privileges granted through roles are therefore not checked by default when the CREATE PROCEDURE or CREATE FUNCTION statement is issued. For stored programs, if execution should occur with roles different from the default, the program body can execute SET ROLE to activate the required roles. This must be done with caution since the privileges assigned to roles can be changed.

# <span id="page-180-0"></span>**27.7 Stored Program Binary Logging**

The binary log contains information about SQL statements that modify database contents. This information is stored in the form of "events" that describe the modifications. (Binary log events differ from scheduled event stored objects.) The binary log has two important purposes:

- For replication, the binary log is used on source replication servers as a record of the statements to be sent to replica servers. The source sends the events contained in its binary log to its replicas, which execute those events to make the same data changes that were made on the source. See Section 19.2, "Replication Implementation".
- Certain data recovery operations require use of the binary log. After a backup file has been restored, the events in the binary log that were recorded after the backup was made are re-executed. These events bring databases up to date from the point of the backup. See Section 9.3.2, "Using Backups for Recovery".

However, if logging occurs at the statement level, there are certain binary logging issues with respect to stored programs (stored procedures and functions, triggers, and events):

- In some cases, a statement might affect different sets of rows on source and replica.
- Replicated statements executed on a replica are processed by the replica's applier thread. Unless you implement replication privilege checks, which are available from MySQL 8.0.18 (see Section 19.3.3, "Replication Privilege Checks"), the applier thread has full privileges. In this situation, it is possible for a procedure to follow different execution paths on source and replica servers, so a user could write a routine containing a dangerous statement that executes only on the replica.
- If a stored program that modifies data is nondeterministic, it is not repeatable. This can result in different data on source and replica, or cause restored data to differ from the original data.

This section describes how MySQL handles binary logging for stored programs. It states the current conditions that the implementation places on the use of stored programs, and what you can do to avoid logging problems. It also provides additional information about the reasons for these conditions.

Unless noted otherwise, the remarks here assume that binary logging is enabled on the server (see Section 7.4.4, "The Binary Log".) If the binary log is not enabled, replication is not possible, nor is the binary log available for data recovery. From MySQL 8.0, binary logging is enabled by default, and is only disabled if you specify the --skip-log-bin or --disable-log-bin option at startup.

In general, the issues described here result when binary logging occurs at the SQL statement level (statement-based binary logging). If you use row-based binary logging, the log contains changes made to individual rows as a result of executing SQL statements. When routines or triggers execute, row changes are logged, not the statements that make the changes. For stored procedures, this means

that the CALL statement is not logged. For stored functions, row changes made within the function are logged, not the function invocation. For triggers, row changes made by the trigger are logged. On the replica side, only the row changes are seen, not the stored program invocation.

Mixed format binary logging (binlog\_format=MIXED) uses statement-based binary logging, except for cases where only row-based binary logging is guaranteed to lead to proper results. With mixed format, when a stored function, stored procedure, trigger, event, or prepared statement contains anything that is not safe for statement-based binary logging, the entire statement is marked as unsafe and logged in row format. The statements used to create and drop procedures, functions, triggers, and events are always safe, and are logged in statement format. For more information about rowbased, mixed, and statement-based logging, and how safe and unsafe statements are determined, see Section 19.2.1, "Replication Formats".

The conditions on the use of stored functions in MySQL can be summarized as follows. These conditions do not apply to stored procedures or Event Scheduler events and they do not apply unless binary logging is enabled.

- To create or alter a stored function, you must have the SET\_USER\_ID privilege (or the deprecated SUPER privilege), in addition to the CREATE ROUTINE or ALTER ROUTINE privilege that is normally required. (Depending on the DEFINER value in the function definition, SET\_USER\_ID or SUPER might be required regardless of whether binary logging is enabled. See Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements".)
- When you create a stored function, you must declare either that it is deterministic or that it does not modify data. Otherwise, it may be unsafe for data recovery or replication.

By default, for a CREATE FUNCTION statement to be accepted, at least one of DETERMINISTIC, NO SQL, or READS SQL DATA must be specified explicitly. Otherwise an error occurs:

```
ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL,
or READS SQL DATA in its declaration and binary logging is enabled
(you *might* want to use the less safe log_bin_trust_function_creators
variable)
```

This function is deterministic (and does not modify data), so it is safe:

```
CREATE FUNCTION f1(i INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
 RETURN i;
END;
```

This function uses UUID(), which is not deterministic, so the function also is not deterministic and is not safe:

```
CREATE FUNCTION f2()
RETURNS CHAR(36) CHARACTER SET utf8mb4
BEGIN
 RETURN UUID();
END;
```

This function modifies data, so it may not be safe:

```
CREATE FUNCTION f3(p_id INT)
RETURNS INT
BEGIN
 UPDATE t SET modtime = NOW() WHERE id = p_id;
 RETURN ROW_COUNT();
END;
```

Assessment of the nature of a function is based on the "honesty" of the creator. MySQL does not check that a function declared DETERMINISTIC is free of statements that produce nondeterministic results.

- When you attempt to execute a stored function, if binlog\_format=STATEMENT is set, the DETERMINISTIC keyword must be specified in the function definition. If this is not the case, an error is generated and the function does not run, unless log\_bin\_trust\_function\_creators=1 is specified to override this check (see below). For recursive function calls, the DETERMINISTIC keyword is required on the outermost call only. If row-based or mixed binary logging is in use, the statement is accepted and replicated even if the function was defined without the DETERMINISTIC keyword.
- Because MySQL does not check if a function really is deterministic at creation time, the invocation of a stored function with the DETERMINISTIC keyword might carry out an action that is unsafe for statement-based logging, or invoke a function or procedure containing unsafe statements. If this occurs when binlog\_format=STATEMENT is set, a warning message is issued. If row-based or mixed binary logging is in use, no warning is issued, and the statement is replicated in row-based format.
- To relax the preceding conditions on function creation (that you must have the SUPER privilege and that a function must be declared deterministic or to not modify data), set the global log\_bin\_trust\_function\_creators system variable to 1. By default, this variable has a value of 0, but you can change it like this:

```
mysql> SET GLOBAL log_bin_trust_function_creators = 1;
```

You can also set this variable at server startup.

If binary logging is not enabled, log\_bin\_trust\_function\_creators does not apply. SUPER is not required for function creation unless, as described previously, the DEFINER value in the function definition requires it.

• For information about built-in functions that may be unsafe for replication (and thus cause stored functions that use them to be unsafe as well), see Section 19.5.1, "Replication Features and Issues".

Triggers are similar to stored functions, so the preceding remarks regarding functions also apply to triggers with the following exception: CREATE TRIGGER does not have an optional DETERMINISTIC characteristic, so triggers are assumed to be always deterministic. However, this assumption might be invalid in some cases. For example, the UUID() function is nondeterministic (and does not replicate). Be careful about using such functions in triggers.

Triggers can update tables, so error messages similar to those for stored functions occur with CREATE TRIGGER if you do not have the required privileges. On the replica side, the replica uses the trigger DEFINER attribute to determine which user is considered to be the creator of the trigger.

The rest of this section provides additional detail about the logging implementation and its implications. You need not read it unless you are interested in the background on the rationale for the current logging-related conditions on stored routine use. This discussion applies only for statement-based logging, and not for row-based logging, with the exception of the first item: CREATE and DROP statements are logged as statements regardless of the logging mode.

- The server writes CREATE EVENT, CREATE PROCEDURE, CREATE FUNCTION, ALTER EVENT, ALTER PROCEDURE, ALTER FUNCTION, DROP EVENT, DROP PROCEDURE, and DROP FUNCTION statements to the binary log.
- A stored function invocation is logged as a SELECT statement if the function changes data and occurs within a statement that would not otherwise be logged. This prevents nonreplication of data changes that result from use of stored functions in nonlogged statements. For example, SELECT statements are not written to the binary log, but a SELECT might invoke a stored function that makes changes. To handle this, a SELECT func\_name() statement is written to the binary log when the given function makes a change. Suppose that the following statements are executed on the source server:

```
CREATE FUNCTION f1(a INT) RETURNS INT
BEGIN
```

```
 IF (a < 3) THEN
 INSERT INTO t2 VALUES (a);
 END IF;
 RETURN 0;
END;
CREATE TABLE t1 (a INT);
INSERT INTO t1 VALUES (1),(2),(3);
SELECT f1(a) FROM t1;
```

When the SELECT statement executes, the function f1() is invoked three times. Two of those invocations insert a row, and MySQL logs a SELECT statement for each of them. That is, MySQL writes the following statements to the binary log:

```
SELECT f1(1);
SELECT f1(2);
```

The server also logs a SELECT statement for a stored function invocation when the function invokes a stored procedure that causes an error. In this case, the server writes the SELECT statement to the log along with the expected error code. On the replica, if the same error occurs, that is the expected result and replication continues. Otherwise, replication stops.

- Logging stored function invocations rather than the statements executed by a function has a security implication for replication, which arises from two factors:
  - It is possible for a function to follow different execution paths on source and replica servers.
  - Statements executed on a replica are processed by the replica's applier thread. Unless you implement replication privilege checks, which are available from MySQL 8.0.18 (see Section 19.3.3, "Replication Privilege Checks"), the applier thread has full privileges.

The implication is that although a user must have the CREATE ROUTINE privilege to create a function, the user can write a function containing a dangerous statement that executes only on the replica where it is processed by a thread that has full privileges. For example, if the source and replica servers have server ID values of 1 and 2, respectively, a user on the source server could create and invoke an unsafe function unsafe\_func() as follows:

```
mysql> delimiter //
mysql> CREATE FUNCTION unsafe_func () RETURNS INT
 -> BEGIN
 -> IF @@server_id=2 THEN dangerous_statement; END IF;
 -> RETURN 1;
 -> END;
 -> //
mysql> delimiter ;
mysql> INSERT INTO t VALUES(unsafe_func());
```

The CREATE FUNCTION and INSERT statements are written to the binary log, so the replica executes them. Because the replica's applier thread has full privileges, it executes the dangerous statement. Thus, the function invocation has different effects on the source and replica and is not replication-safe.

To guard against this danger for servers that have binary logging enabled, stored function creators must have the SUPER privilege, in addition to the usual CREATE ROUTINE privilege that is required. Similarly, to use ALTER FUNCTION, you must have the SUPER privilege in addition to the ALTER ROUTINE privilege. Without the SUPER privilege, an error occurs:

```
ERROR 1419 (HY000): You do not have the SUPER privilege and
binary logging is enabled (you *might* want to use the less safe
log_bin_trust_function_creators variable)
```

If you do not want to require function creators to have the SUPER privilege (for example, if all users with the CREATE ROUTINE privilege on your system are experienced application developers), set the global log\_bin\_trust\_function\_creators system variable to 1. You can also set this

variable at server startup. If binary logging is not enabled, log\_bin\_trust\_function\_creators does not apply. SUPER is not required for function creation unless, as described previously, the DEFINER value in the function definition requires it.

- The use of replication privilege checks where available (from MySQL 8.0.18) is recommended whatever choice you make about privileges for function creators. Replication privilege checks can be set up to ensure that only expected and relevant operations are authorized for the replication channel. For instructions to do this, see Section 19.3.3, "Replication Privilege Checks".
- If a function that performs updates is nondeterministic, it is not repeatable. This can have two undesirable effects:
  - It causes a replica to differ from the source.
  - Restored data does not match the original data.

To deal with these problems, MySQL enforces the following requirement: On a source server, creation and alteration of a function is refused unless you declare the function to be deterministic or to not modify data. Two sets of function characteristics apply here:

- The DETERMINISTIC and NOT DETERMINISTIC characteristics indicate whether a function always produces the same result for given inputs. The default is NOT DETERMINISTIC if neither characteristic is given. To declare that a function is deterministic, you must specify DETERMINISTIC explicitly.
- The CONTAINS SQL, NO SQL, READS SQL DATA, and MODIFIES SQL DATA characteristics provide information about whether the function reads or writes data. Either NO SQL or READS SQL DATA indicates that a function does not change data, but you must specify one of these explicitly because the default is CONTAINS SQL if no characteristic is given.

By default, for a CREATE FUNCTION statement to be accepted, at least one of DETERMINISTIC, NO SQL, or READS SQL DATA must be specified explicitly. Otherwise an error occurs:

```
ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL,
or READS SQL DATA in its declaration and binary logging is enabled
(you *might* want to use the less safe log_bin_trust_function_creators
variable)
```

If you set log\_bin\_trust\_function\_creators to 1, the requirement that functions be deterministic or not modify data is dropped.

• Stored procedure calls are logged at the statement level rather than at the CALL level. That is, the server does not log the CALL statement, it logs those statements within the procedure that actually execute. As a result, the same changes that occur on the source server also occur on replicas. This prevents problems that could result from a procedure having different execution paths on different machines.

In general, statements executed within a stored procedure are written to the binary log using the same rules that would apply were the statements to be executed in standalone fashion. Some special care is taken when logging procedure statements because statement execution within procedures is not quite the same as in nonprocedure context:

• A statement to be logged might contain references to local procedure variables. These variables do not exist outside of stored procedure context, so a statement that refers to such a variable cannot be logged literally. Instead, each reference to a local variable is replaced by this construct for logging purposes:

```
NAME_CONST(var_name, var_value)
```

var\_name is the local variable name, and var\_value is a constant indicating the value that the variable has at the time the statement is logged. NAME\_CONST() has a value of var\_value, and a "name" of var\_name. Thus, if you invoke this function directly, you get a result like this:

```
mysql> SELECT NAME_CONST('myname', 14);
+--------+
| myname |
+--------+
| 14 |
+--------+
```

NAME\_CONST() enables a logged standalone statement to be executed on a replica with the same effect as the original statement that was executed on the source within a stored procedure.

The use of NAME\_CONST() can result in a problem for CREATE TABLE ... SELECT statements when the source column expressions refer to local variables. Converting these references to NAME\_CONST() expressions can result in column names that are different on the source and replica servers, or names that are too long to be legal column identifiers. A workaround is to supply aliases for columns that refer to local variables. Consider this statement when myvar has a value of 1:

```
CREATE TABLE t1 SELECT myvar;
```

This is rewritten as follows:

```
CREATE TABLE t1 SELECT NAME_CONST(myvar, 1);
```

To ensure that the source and replica tables have the same column names, write the statement like this:

```
CREATE TABLE t1 SELECT myvar AS myvar;
```

The rewritten statement becomes:

```
CREATE TABLE t1 SELECT NAME_CONST(myvar, 1) AS myvar;
```

• A statement to be logged might contain references to user-defined variables. To handle this, MySQL writes a SET statement to the binary log to make sure that the variable exists on the replica with the same value as on the source. For example, if a statement refers to a variable @my\_var, that statement is preceded in the binary log by the following statement, where value is the value of @my\_var on the source:

```
SET @my_var = value;
```

- Procedure calls can occur within a committed or rolled-back transaction. Transactional context is accounted for so that the transactional aspects of procedure execution are replicated correctly. That is, the server logs those statements within the procedure that actually execute and modify data, and also logs BEGIN, COMMIT, and ROLLBACK statements as necessary. For example, if a procedure updates only transactional tables and is executed within a transaction that is rolled back, those updates are not logged. If the procedure occurs within a committed transaction, BEGIN and COMMIT statements are logged with the updates. For a procedure that executes within a rolled-back transaction, its statements are logged using the same rules that would apply if the statements were executed in standalone fashion:
  - Updates to transactional tables are not logged.
  - Updates to nontransactional tables are logged because rollback does not cancel them.
  - Updates to a mix of transactional and nontransactional tables are logged surrounded by BEGIN and ROLLBACK so that replicas make the same changes and rollbacks as on the source.
- A stored procedure call is not written to the binary log at the statement level if the procedure is invoked from within a stored function. In that case, the only thing logged is the statement that invokes the function (if it occurs within a statement that is logged) or a DO statement (if it occurs within a statement that is not logged). For this reason, care should be exercised in the use of stored functions that invoke a procedure, even if the procedure is otherwise safe in itself.

# <span id="page-186-0"></span>**27.8 Restrictions on Stored Programs**

- [SQL Statements Not Permitted in Stored Routines](#page-186-1)
- [Restrictions for Stored Functions](#page-187-0)
- [Restrictions for Triggers](#page-187-1)
- [Name Conflicts within Stored Routines](#page-187-2)
- [Replication Considerations](#page-188-0)
- [Debugging Considerations](#page-188-1)
- [Unsupported Syntax from the SQL:2003 Standard](#page-188-2)
- [Stored Routine Concurrency Considerations](#page-188-3)
- [Event Scheduler Restrictions](#page-188-4)
- [Stored routines and triggers in NDB Cluster](#page-189-1)

These restrictions apply to the features described in Chapter 27, [Stored Objects](#page-154-0).

Some of the restrictions noted here apply to all stored routines; that is, both to stored procedures and stored functions. There are also some [restrictions specific to stored functions](#page-187-0) but not to stored procedures.

The restrictions for stored functions also apply to triggers. There are also some [restrictions specific to](#page-187-1) [triggers](#page-187-1).

The restrictions for stored procedures also apply to the DO clause of Event Scheduler event definitions. There are also some [restrictions specific to events](#page-188-4).

## <span id="page-186-1"></span>**SQL Statements Not Permitted in Stored Routines**

Stored routines cannot contain arbitrary SQL statements. The following statements are not permitted:

- The locking statements LOCK TABLES and UNLOCK TABLES.
- ALTER VIEW.
- LOAD DATA and LOAD XML.
- SQL prepared statements (PREPARE, EXECUTE, DEALLOCATE PREPARE) can be used in stored procedures, but not in stored functions or triggers. Thus, stored functions and triggers cannot use dynamic SQL (where you construct statements as strings and then execute them).
- Generally, statements not permitted in SQL prepared statements are also not permitted in stored programs. For a list of statements supported as prepared statements, see Section 15.5, "Prepared Statements". Exceptions are SIGNAL, RESIGNAL, and GET DIAGNOSTICS, which are not permissible as prepared statements but are permitted in stored programs.
- Because local variables are in scope only during stored program execution, references to them are not permitted in prepared statements created within a stored program. Prepared statement scope is the current session, not the stored program, so the statement could be executed after the program ends, at which point the variables would no longer be in scope. For example, SELECT ... INTO local\_var cannot be used as a prepared statement. This restriction also applies to stored procedure and function parameters. See Section 15.5.1, "PREPARE Statement".
- Within all stored programs (stored procedures and functions, triggers, and events), the parser treats BEGIN [WORK] as the beginning of a BEGIN ... END block.

To begin a transaction within a stored procedure or event, use START TRANSACTION instead.

START TRANSACTION cannot be used within a stored function or trigger.

# <span id="page-187-0"></span>**Restrictions for Stored Functions**

The following additional statements or operations are not permitted within stored functions. They are permitted within stored procedures, except stored procedures that are invoked from within a stored function or trigger. For example, if you use FLUSH in a stored procedure, that stored procedure cannot be called from a stored function or trigger.

- Statements that perform explicit or implicit commit or rollback. Support for these statements is not required by the SQL standard, which states that each DBMS vendor may decide whether to permit them.
- Statements that return a result set. This includes SELECT statements that do not have an INTO var\_list clause and other statements such as SHOW, EXPLAIN, and CHECK TABLE. A function can process a result set either with SELECT ... INTO var\_list or by using a cursor and FETCH statements. See Section 15.2.13.1, "SELECT ... INTO Statement", and Section 15.6.6, "Cursors".
- FLUSH statements.
- Stored functions cannot be used recursively.
- A stored function or trigger cannot modify a table that is already being used (for reading or writing) by the statement that invoked the function or trigger.
- If you refer to a temporary table multiple times in a stored function under different aliases, a Can't reopen table: 'tbl\_name' error occurs, even if the references occur in different statements within the function.
- HANDLER ... READ statements that invoke stored functions can cause replication errors and are disallowed.

# <span id="page-187-1"></span>**Restrictions for Triggers**

For triggers, the following additional restrictions apply:

- Triggers are not activated by foreign key actions.
- When using row-based replication, triggers on the replica are not activated by statements originating on the source. The triggers on the replica are activated when using statement-based replication. For more information, see Section 19.5.1.36, "Replication and Triggers".
- The RETURN statement is not permitted in triggers, which cannot return a value. To exit a trigger immediately, use the LEAVE statement.
- Triggers are not permitted on tables in the mysql database. Nor are they permitted on INFORMATION\_SCHEMA or performance\_schema tables. Those tables are actually views and triggers are not permitted on views.
- The trigger cache does not detect when metadata of the underlying objects has changed. If a trigger uses a table and the table has changed since the trigger was loaded into the cache, the trigger operates using the outdated metadata.

## <span id="page-187-2"></span>**Name Conflicts within Stored Routines**

The same identifier might be used for a routine parameter, a local variable, and a table column. Also, the same local variable name can be used in nested blocks. For example:

```
CREATE PROCEDURE p (i INT)
BEGIN
 DECLARE i INT DEFAULT 0;
 SELECT i FROM t;
```

```
 BEGIN
 DECLARE i INT DEFAULT 1;
 SELECT i FROM t;
 END;
END;
```

In such cases, the identifier is ambiguous and the following precedence rules apply:

- A local variable takes precedence over a routine parameter or table column.
- A routine parameter takes precedence over a table column.
- A local variable in an inner block takes precedence over a local variable in an outer block.

The behavior that variables take precedence over table columns is nonstandard.

## <span id="page-188-0"></span>**Replication Considerations**

Use of stored routines can cause replication problems. This issue is discussed further in [Section 27.7,](#page-180-0) ["Stored Program Binary Logging".](#page-180-0)

The --replicate-wild-do-table=db\_name.tbl\_name option applies to tables, views, and triggers. It does not apply to stored procedures and functions, or events. To filter statements operating on the latter objects, use one or more of the --replicate-\*-db options.

## <span id="page-188-1"></span>**Debugging Considerations**

There are no stored routine debugging facilities.

# <span id="page-188-2"></span>**Unsupported Syntax from the SQL:2003 Standard**

The MySQL stored routine syntax is based on the SQL:2003 standard. The following items from that standard are not currently supported:

- UNDO handlers
- FOR loops

# <span id="page-188-3"></span>**Stored Routine Concurrency Considerations**

To prevent problems of interaction between sessions, when a client issues a statement, the server uses a snapshot of routines and triggers available for execution of the statement. That is, the server calculates a list of procedures, functions, and triggers that may be used during execution of the statement, loads them, and then proceeds to execute the statement. While the statement executes, it does not see changes to routines performed by other sessions.

For maximum concurrency, stored functions should minimize their side-effects; in particular, updating a table within a stored function can reduce concurrent operations on that table. A stored function acquires table locks before executing, to avoid inconsistency in the binary log due to mismatch of the order in which statements execute and when they appear in the log. When statement-based binary logging is used, statements that invoke a function are recorded rather than the statements executed within the function. Consequently, stored functions that update the same underlying tables do not execute in parallel. In contrast, stored procedures do not acquire table-level locks. All statements executed within stored procedures are written to the binary log, even for statement-based binary logging. See [Section 27.7, "Stored Program Binary Logging"](#page-180-0).

## <span id="page-188-4"></span>**Event Scheduler Restrictions**

The following limitations are specific to the Event Scheduler:

• Event names are handled in case-insensitive fashion. For example, you cannot have two events in the same database with the names anEvent and AnEvent.

- An event may not be created from within a stored program. An event may not be altered, or dropped from within a stored program, if the event name is specified by means of a variable. An event also may not create, alter, or drop stored routines or triggers.
- DDL statements on events are prohibited while a LOCK TABLES statement is in effect.
- Event timings using the intervals YEAR, QUARTER, MONTH, and YEAR\_MONTH are resolved in months; those using any other interval are resolved in seconds. There is no way to cause events scheduled to occur at the same second to execute in a given order. In addition—due to rounding, the nature of threaded applications, and the fact that a nonzero length of time is required to create events and to signal their execution—events may be delayed by as much as 1 or 2 seconds. However, the time shown in the Information Schema EVENTS table's LAST\_EXECUTED column is always accurate to within one second of the actual event execution time. (See also Bug #16522.)
- Each execution of the statements contained in the body of an event takes place in a new connection; thus, these statements have no effect in a given user session on the server's statement counts such as Com\_select and Com\_insert that are displayed by SHOW STATUS. However, such counts are updated in the global scope. (Bug #16422)
- Events do not support times later than the end of the Unix Epoch; this is approximately the beginning of the year 2038. Such dates are specifically not permitted by the Event Scheduler. (Bug #16396)
- References to stored functions, loadable functions, and tables in the ON SCHEDULE clauses of CREATE EVENT and ALTER EVENT statements are not supported. These sorts of references are not permitted. (See Bug #22830 for more information.)

## <span id="page-189-1"></span>**Stored routines and triggers in NDB Cluster**

While stored procedures, stored functions, triggers, and scheduled events are all supported by tables using the NDB storage engine, you must keep in mind that these do not propagate automatically between MySQL Servers acting as Cluster SQL nodes. This is because stored routine and trigger definitions are stored in tables in the mysql system database using InnoDB tables, which are not copied between Cluster nodes.

Any stored routine or trigger that interacts with MySQL Cluster tables must be re-created by running the appropriate CREATE PROCEDURE, CREATE FUNCTION, or CREATE TRIGGER statements on each MySQL Server that participates in the cluster where you wish to use the stored routine or trigger. Similarly, any changes to existing stored routines or triggers must be carried out explicitly on all Cluster SQL nodes, using the appropriate ALTER or DROP statements on each MySQL Server accessing the cluster.

![](_page_189_Picture_10.jpeg)

### **Warning**

Do not attempt to work around the issue just described by converting any mysql database tables to use the NDB storage engine. Altering the system tables in the mysql database is not supported and is very likely to produce undesirable results.

# <span id="page-189-0"></span>**27.9 Restrictions on Views**

The maximum number of tables that can be referenced in the definition of a view is 61.

View processing is not optimized:

- It is not possible to create an index on a view.
- Indexes can be used for views processed using the merge algorithm. However, a view that is processed with the temptable algorithm is unable to take advantage of indexes on its underlying tables (although indexes can be used during generation of the temporary tables).

There is a general principle that you cannot modify a table and select from the same table in a subquery. See Section 15.2.15.12, "Restrictions on Subqueries".

The same principle also applies if you select from a view that selects from the table, if the view selects from the table in a subquery and the view is evaluated using the merge algorithm. Example:

```
CREATE VIEW v1 AS
SELECT * FROM t2 WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t2.a);
UPDATE t1, v2 SET t1.a = 1 WHERE t1.b = v2.b;
```

If the view is evaluated using a temporary table, you can select from the table in the view subquery and still modify that table in the outer query. In this case, the view is stored in a temporary table and thus you are not really selecting from the table in a subquery and modifying it at the same time. (This is another reason you might wish to force MySQL to use the temptable algorithm by specifying ALGORITHM = TEMPTABLE in the view definition.)

You can use DROP TABLE or ALTER TABLE to drop or alter a table that is used in a view definition. No warning results from the DROP or ALTER operation, even though this invalidates the view. Instead, an error occurs later, when the view is used. CHECK TABLE can be used to check for views that have been invalidated by DROP or ALTER operations.

With regard to view updatability, the overall goal for views is that if any view is theoretically updatable, it should be updatable in practice. Many theoretically updatable views can be updated now, but limitations still exist. For details, see [Section 27.5.3, "Updatable and Insertable Views"](#page-172-0).

There exists a shortcoming with the current implementation of views. If a user is granted the basic privileges necessary to create a view (the CREATE VIEW and SELECT privileges), that user cannot call SHOW CREATE VIEW on that object unless the user is also granted the SHOW VIEW privilege.

That shortcoming can lead to problems backing up a database with mysqldump, which may fail due to insufficient privileges. This problem is described in Bug #22062.

The workaround to the problem is for the administrator to manually grant the SHOW VIEW privilege to users who are granted CREATE VIEW, since MySQL doesn't grant it implicitly when views are created.

Views do not have indexes, so index hints do not apply. Use of index hints when selecting from a view is not permitted.

SHOW CREATE VIEW displays view definitions using an AS alias\_name clause for each column. If a column is created from an expression, the default alias is the expression text, which can be quite long. Aliases for column names in CREATE VIEW statements are checked against the maximum column length of 64 characters (not the maximum alias length of 256 characters). As a result, views created from the output of SHOW CREATE VIEW fail if any column alias exceeds 64 characters. This can cause problems in the following circumstances for views with too-long aliases:

- View definitions fail to replicate to newer replicas that enforce the column-length restriction.
- Dump files created with mysqldump cannot be loaded into servers that enforce the column-length restriction.

A workaround for either problem is to modify each problematic view definition to use aliases that provide shorter column names. Then the view replicates properly, and can be dumped and reloaded without causing an error. To modify the definition, drop and create the view again with DROP VIEW and CREATE VIEW, or replace the definition with CREATE OR REPLACE VIEW.

For problems that occur when reloading view definitions in dump files, another workaround is to edit the dump file to modify its CREATE VIEW statements. However, this does not change the original view definitions, which may cause problems for subsequent dump operations.

# <span id="page-192-0"></span>Chapter 28 INFORMATION\_SCHEMA Tables

# **Table of Contents**

| 28.1 Introduction 4964                                                     |      |
|----------------------------------------------------------------------------|------|
| 28.2 INFORMATION_SCHEMA Table Reference 4967                               |      |
| 28.3 INFORMATION_SCHEMA General Tables 4971                                |      |
| 28.3.1 INFORMATION_SCHEMA General Table Reference 4971                     |      |
| 28.3.2 The INFORMATION_SCHEMA ADMINISTRABLE_ROLE_AUTHORIZATIONS Table 4973 |      |
| 28.3.3 The INFORMATION_SCHEMA APPLICABLE_ROLES Table 4973                  |      |
| 28.3.4 The INFORMATION_SCHEMA CHARACTER_SETS Table 4974                    |      |
| 28.3.5 The INFORMATION_SCHEMA CHECK_CONSTRAINTS Table 4975                 |      |
| 28.3.6 The INFORMATION_SCHEMA COLLATIONS Table 4975                        |      |
| 28.3.7 The INFORMATION_SCHEMA COLLATION_CHARACTER_SET_APPLICABILITY        |      |
| Table 4976                                                                 |      |
| 28.3.8 The INFORMATION_SCHEMA COLUMNS Table 4976                           |      |
| 28.3.9 The INFORMATION_SCHEMA COLUMNS_EXTENSIONS Table 4979                |      |
|                                                                            |      |
| 28.3.10 The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table 4979                |      |
| 28.3.11 The INFORMATION_SCHEMA COLUMN_STATISTICS Table 4980                |      |
| 28.3.12 The INFORMATION_SCHEMA ENABLED_ROLES Table 4980                    |      |
| 28.3.13 The INFORMATION_SCHEMA ENGINES Table                               | 4981 |
| 28.3.14 The INFORMATION_SCHEMA EVENTS Table 4982                           |      |
| 28.3.15 The INFORMATION_SCHEMA FILES Table 4985                            |      |
| 28.3.16 The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table 4993                 |      |
| 28.3.17 The INFORMATION_SCHEMA KEYWORDS Table 4994                         |      |
| 28.3.18 The INFORMATION_SCHEMA ndb_transid_mysql_connection_map Table 4994 |      |
| 28.3.19 The INFORMATION_SCHEMA OPTIMIZER_TRACE Table 4996                  |      |
| 28.3.20 The INFORMATION_SCHEMA PARAMETERS Table 4996                       |      |
| 28.3.21 The INFORMATION_SCHEMA PARTITIONS Table 4997                       |      |
| 28.3.22 The INFORMATION_SCHEMA PLUGINS Table 5001                          |      |
| 28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table 5002                      |      |
| 28.3.24 The INFORMATION_SCHEMA PROFILING Table 5003                        |      |
| 28.3.25 The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table 5004          |      |
| 28.3.26 The INFORMATION_SCHEMA RESOURCE_GROUPS Table 5005                  |      |
| 28.3.27 The INFORMATION_SCHEMA ROLE_COLUMN_GRANTS Table 5006               |      |
| 28.3.28 The INFORMATION_SCHEMA ROLE_ROUTINE_GRANTS Table 5006              |      |
| 28.3.29 The INFORMATION_SCHEMA ROLE_TABLE_GRANTS Table 5007                |      |
| 28.3.30 The INFORMATION_SCHEMA ROUTINES Table 5008                         |      |
| 28.3.31 The INFORMATION_SCHEMA SCHEMATA Table 5011                         |      |
| 28.3.32 The INFORMATION_SCHEMA SCHEMATA_EXTENSIONS Table 5011              |      |
| 28.3.33 The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table 5012                |      |
| 28.3.34 The INFORMATION_SCHEMA STATISTICS Table 5013                       |      |
| 28.3.35 The INFORMATION_SCHEMA ST_GEOMETRY_COLUMNS Table 5015              |      |
| 28.3.36 The INFORMATION_SCHEMA ST_SPATIAL_REFERENCE_SYSTEMS Table 5016     |      |
| 28.3.37 The INFORMATION_SCHEMA ST_UNITS_OF_MEASURE Table 5017              |      |
| 28.3.38 The INFORMATION_SCHEMA TABLES Table 5018                           |      |
| 28.3.39 The INFORMATION_SCHEMA TABLES_EXTENSIONS Table 5021                |      |
| 28.3.40 The INFORMATION_SCHEMA TABLESPACES Table 5022                      |      |
| 28.3.41 The INFORMATION_SCHEMA TABLESPACES_EXTENSIONS Table                | 5022 |
| 28.3.42 The INFORMATION_SCHEMA TABLE_CONSTRAINTS Table                     | 5022 |
| 28.3.43 The INFORMATION_SCHEMA TABLE_CONSTRAINTS_EXTENSIONS Table          | 5023 |
| 28.3.44 The INFORMATION_SCHEMA TABLE_PRIVILEGES Table                      | 5024 |
|                                                                            |      |
| 28.3.45 The INFORMATION_SCHEMA TRIGGERS Table 5024                         |      |
| 28.3.46 The INFORMATION_SCHEMA USER_ATTRIBUTES Table 5026                  |      |
| 28.3.47 The INFORMATION_SCHEMA USER_PRIVILEGES Table 5027                  |      |
| 28.3.48 The INFORMATION_SCHEMA VIEWS Table 5028                            |      |

| 28.3.49 The INFORMATION_SCHEMA VIEW_ROUTINE_USAGE Table 5029              |      |
|---------------------------------------------------------------------------|------|
| 28.3.50 The INFORMATION_SCHEMA VIEW_TABLE_USAGE Table 5030                |      |
| 28.4 INFORMATION_SCHEMA InnoDB Tables 5030                                |      |
| 28.4.1 INFORMATION_SCHEMA InnoDB Table Reference 5030                     |      |
| 28.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table 5032               |      |
| 28.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table 5035           |      |
|                                                                           |      |
| 28.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table 5038         |      |
| 28.4.5 The INFORMATION_SCHEMA INNODB_CACHED_INDEXES Table 5041            |      |
| 28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables 5042 |      |
| 28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and                           |      |
| INNODB_CMPMEM_RESET Tables 5044                                           |      |
| 28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and                    |      |
| INNODB_CMP_PER_INDEX_RESET Tables                                         | 5045 |
| 28.4.9 The INFORMATION_SCHEMA INNODB_COLUMNS Table 5046                   |      |
| 28.4.10 The INFORMATION_SCHEMA INNODB_DATAFILES Table 5048                |      |
| 28.4.11 The INFORMATION_SCHEMA INNODB_FIELDS Table 5048                   |      |
| 28.4.12 The INFORMATION_SCHEMA INNODB_FOREIGN Table 5049                  |      |
| 28.4.13 The INFORMATION_SCHEMA INNODB_FOREIGN_COLS Table 5050             |      |
| 28.4.14 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table 5050         |      |
| 28.4.15 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table 5051                |      |
| 28.4.16 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table 5052      |      |
| 28.4.17 The INFORMATION_SCHEMA INNODB_FT_DELETED Table 5053               |      |
| 28.4.18 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table                | 5054 |
| 28.4.19 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table 5055           |      |
| 28.4.20 The INFORMATION_SCHEMA INNODB_INDEXES Table 5057                  |      |
| 28.4.21 The INFORMATION_SCHEMA INNODB_METRICS Table 5058                  |      |
| 28.4.22 The INFORMATION_SCHEMA INNODB_SESSION_TEMP_TABLESPACES Table 5060 |      |
| 28.4.23 The INFORMATION_SCHEMA INNODB_TABLES Table 5061                   |      |
| 28.4.24 The INFORMATION_SCHEMA INNODB_TABLESPACES Table 5063              |      |
| 28.4.25 The INFORMATION_SCHEMA INNODB_TABLESPACES_BRIEF Table 5065        |      |
| 28.4.26 The INFORMATION_SCHEMA INNODB_TABLESTATS View 5066                |      |
|                                                                           |      |
| 28.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table 5067          |      |
| 28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table 5068                      |      |
| 28.4.29 The INFORMATION_SCHEMA INNODB_VIRTUAL Table 5071                  |      |
| 28.5 INFORMATION_SCHEMA Thread Pool Tables 5072                           |      |
| 28.5.1 INFORMATION_SCHEMA Thread Pool Table Reference 5072                |      |
| 28.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table 5073            |      |
| 28.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table 5073            |      |
| 28.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table 5073                  |      |
| 28.6 INFORMATION_SCHEMA Connection Control Tables 5074                    |      |
| 28.6.1 INFORMATION_SCHEMA Connection Control Table Reference 5074         |      |
| 28.6.2 The INFORMATION_SCHEMA                                             |      |
| CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table 5074                       |      |
| 28.7 INFORMATION_SCHEMA MySQL Enterprise Firewall Tables                  | 5075 |
| 28.7.1 INFORMATION_SCHEMA Firewall Table Reference 5075                   |      |
| 28.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table 5075             |      |
| 28.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table 5075         |      |
| 28.8 Extensions to SHOW Statements 5076                                   |      |
|                                                                           |      |

INFORMATION\_SCHEMA provides access to database metadata, information about the MySQL server such as the name of a database or table, the data type of a column, or access privileges. Other terms that are sometimes used for this information are data dictionary and system catalog.

# <span id="page-193-0"></span>**28.1 Introduction**

INFORMATION\_SCHEMA provides access to database metadata, information about the MySQL server such as the name of a database or table, the data type of a column, or access privileges. Other terms that are sometimes used for this information are data dictionary and system catalog.

- [INFORMATION\\_SCHEMA Usage Notes](#page-194-0)
- [Character Set Considerations](#page-195-0)
- [INFORMATION\\_SCHEMA as Alternative to SHOW Statements](#page-195-1)
- [INFORMATION\\_SCHEMA and Privileges](#page-195-2)
- [Performance Considerations](#page-195-3)
- [Standards Considerations](#page-195-4)
- [Conventions in the INFORMATION\\_SCHEMA Reference Sections](#page-196-1)
- [Related Information](#page-196-2)

# <span id="page-194-0"></span>**INFORMATION\_SCHEMA Usage Notes**

INFORMATION\_SCHEMA is a database within each MySQL instance, the place that stores information about all the other databases that the MySQL server maintains. The INFORMATION\_SCHEMA database contains several read-only tables. They are actually views, not base tables, so there are no files associated with them, and you cannot set triggers on them. Also, there is no database directory with that name.

Although you can select INFORMATION\_SCHEMA as the default database with a USE statement, you can only read the contents of tables, not perform INSERT, UPDATE, or DELETE operations on them.

Here is an example of a statement that retrieves information from INFORMATION\_SCHEMA:

```
mysql> SELECT table_name, table_type, engine
 FROM information_schema.tables
 WHERE table_schema = 'db5'
 ORDER BY table_name;
+------------+------------+--------+
| table_name | table_type | engine |
+------------+------------+--------+
| fk | BASE TABLE | InnoDB |
| fk2 | BASE TABLE | InnoDB |
| goto | BASE TABLE | MyISAM |
| into | BASE TABLE | MyISAM |
| k | BASE TABLE | MyISAM |
| kurs | BASE TABLE | MyISAM |
| loop | BASE TABLE | MyISAM |
| pk | BASE TABLE | InnoDB |
| t | BASE TABLE | MyISAM |
| t2 | BASE TABLE | MyISAM |
| t3 | BASE TABLE | MyISAM |
| t7 | BASE TABLE | MyISAM |
| tables | BASE TABLE | MyISAM |
| v | VIEW | NULL |
| v2 | VIEW | NULL |
| v3 | VIEW | NULL |
| v56 | VIEW | NULL |
+------------+------------+--------+
17 rows in set (0.01 sec)
```

Explanation: The statement requests a list of all the tables in database db5, showing just three pieces of information: the name of the table, its type, and its storage engine.

Beginning with MySQL 8.0.30, information about generated invisible primary keys is visible by default in all INFORMATION\_SCHEMA tables describing table columns, keys, or both, such as the COLUMNS and STATISTICS tables. If you wish to make such information hidden from queries that select from these tables, you can do so by setting the value of the show\_gipk\_in\_create\_table\_and\_information\_schema server system variable to OFF. For more information, see Section 15.1.20.11, "Generated Invisible Primary Keys".

## <span id="page-195-0"></span>**Character Set Considerations**

The definition for character columns (for example, TABLES.TABLE\_NAME) is generally VARCHAR(N) CHARACTER SET utf8mb3 where N is at least 64. MySQL uses the default collation for this character set (utf8mb3\_general\_ci) for all searches, sorts, comparisons, and other string operations on such columns.

Because some MySQL objects are represented as files, searches in INFORMATION\_SCHEMA string columns can be affected by file system case sensitivity. For more information, see Section 12.8.7, "Using Collation in INFORMATION\_SCHEMA Searches".

## <span id="page-195-1"></span>**INFORMATION\_SCHEMA as Alternative to SHOW Statements**

The SELECT ... FROM INFORMATION\_SCHEMA statement is intended as a more consistent way to provide access to the information provided by the various SHOW statements that MySQL supports (SHOW DATABASES, SHOW TABLES, and so forth). Using SELECT has these advantages, compared to SHOW:

- It conforms to Codd's rules, because all access is done on tables.
- You can use the familiar syntax of the SELECT statement, and only need to learn some table and column names.
- The implementor need not worry about adding keywords.
- You can filter, sort, concatenate, and transform the results from INFORMATION\_SCHEMA queries into whatever format your application needs, such as a data structure or a text representation to parse.
- This technique is more interoperable with other database systems. For example, Oracle Database users are familiar with querying tables in the Oracle data dictionary.

Because SHOW is familiar and widely used, the SHOW statements remain as an alternative. In fact, along with the implementation of INFORMATION\_SCHEMA, there are enhancements to SHOW as described in Section 28.8, "Extensions to SHOW Statements".

# <span id="page-195-2"></span>**INFORMATION\_SCHEMA and Privileges**

For most INFORMATION\_SCHEMA tables, each MySQL user has the right to access them, but can see only the rows in the tables that correspond to objects for which the user has the proper access privileges. In some cases (for example, the ROUTINE\_DEFINITION column in the INFORMATION\_SCHEMA ROUTINES table), users who have insufficient privileges see NULL. Some tables have different privilege requirements; for these, the requirements are mentioned in the applicable table descriptions. For example, InnoDB tables (tables with names that begin with INNODB\_) require the PROCESS privilege.

The same privileges apply to selecting information from INFORMATION\_SCHEMA and viewing the same information through SHOW statements. In either case, you must have some privilege on an object to see information about it.

## <span id="page-195-3"></span>**Performance Considerations**

INFORMATION\_SCHEMA queries that search for information from more than one database might take a long time and impact performance. To check the efficiency of a query, you can use EXPLAIN. For information about using EXPLAIN output to tune INFORMATION\_SCHEMA queries, see Section 10.2.3, "Optimizing INFORMATION\_SCHEMA Queries".

## <span id="page-195-4"></span>**Standards Considerations**

The implementation for the INFORMATION\_SCHEMA table structures in MySQL follows the ANSI/ISO SQL:2003 standard Part 11 Schemata. Our intent is approximate compliance with SQL:2003 core feature F021 Basic information schema.

Users of SQL Server 2000 (which also follows the standard) may notice a strong similarity. However, MySQL has omitted many columns that are not relevant for our implementation, and added columns that are MySQL-specific. One such added column is the ENGINE column in the INFORMATION\_SCHEMA TABLES table.

Although other DBMSs use a variety of names, like syscat or system, the standard name is INFORMATION\_SCHEMA.

To avoid using any name that is reserved in the standard or in DB2, SQL Server, or Oracle, we changed the names of some columns marked "MySQL extension". (For example, we changed COLLATION to TABLE\_COLLATION in the TABLES table.) See the list of reserved words near the end of this article: [https://web.archive.org/web/20070428032454/http://www.dbazine.com/db2/db2](https://web.archive.org/web/20070428032454/http://www.dbazine.com/db2/db2-disarticles/gulutzan5) [disarticles/gulutzan5.](https://web.archive.org/web/20070428032454/http://www.dbazine.com/db2/db2-disarticles/gulutzan5)

# <span id="page-196-1"></span>**Conventions in the INFORMATION\_SCHEMA Reference Sections**

The following sections describe each of the tables and columns in INFORMATION\_SCHEMA. For each column, there are three pieces of information:

- "INFORMATION\_SCHEMA Name" indicates the name for the column in the INFORMATION\_SCHEMA table. This corresponds to the standard SQL name unless the "Remarks" field says "MySQL extension."
- "SHOW Name" indicates the equivalent field name in the closest SHOW statement, if there is one.
- "Remarks" provides additional information where applicable. If this field is NULL, it means that the value of the column is always NULL. If this field says "MySQL extension," the column is a MySQL extension to standard SQL.

Many sections indicate what SHOW statement is equivalent to a SELECT that retrieves information from INFORMATION\_SCHEMA. For SHOW statements that display information for the default database if you omit a FROM db\_name clause, you can often select information for the default database by adding an AND TABLE\_SCHEMA = SCHEMA() condition to the WHERE clause of a query that retrieves information from an INFORMATION\_SCHEMA table.

## <span id="page-196-2"></span>**Related Information**

These sections discuss additional INFORMATION\_SCHEMA-related topics:

- information about INFORMATION\_SCHEMA tables specific to the InnoDB storage engine: Section 28.4, "INFORMATION\_SCHEMA InnoDB Tables"
- information about INFORMATION\_SCHEMA tables specific to the thread pool plugin: Section 28.5, "INFORMATION\_SCHEMA Thread Pool Tables"
- information about INFORMATION\_SCHEMA tables specific to the CONNECTION\_CONTROL plugin: Section 28.6, "INFORMATION\_SCHEMA Connection Control Tables"
- Answers to questions that are often asked concerning the INFORMATION\_SCHEMA database: Section A.7, "MySQL 8.0 FAQ: INFORMATION\_SCHEMA"
- INFORMATION\_SCHEMA queries and the optimizer: Section 10.2.3, "Optimizing INFORMATION\_SCHEMA Queries"
- The effect of collation on INFORMATION\_SCHEMA comparisons: Section 12.8.7, "Using Collation in INFORMATION\_SCHEMA Searches"

# <span id="page-196-0"></span>**28.2 INFORMATION\_SCHEMA Table Reference**

The following table summarizes all available INFORMATION\_SCHEMA tables. For greater detail, see the individual table descriptions.

**Table 28.1 INFORMATION\_SCHEMA Tables**

| Table Name                                                 | Description                                                                 | Deprecated |
|------------------------------------------------------------|-----------------------------------------------------------------------------|------------|
| ADMINISTRABLE_ROLE_AUTHORIZATIONS                          | Grantable users or roles for<br>current user or role                        |            |
| APPLICABLE_ROLES                                           | Applicable roles for current user                                           |            |
| CHARACTER_SETS                                             | Available character sets                                                    |            |
| CHECK_CONSTRAINTS                                          | Table and column CHECK<br>constraints                                       |            |
| COLLATION_CHARACTER_SET_APPLICABILITY                      | Character set applicable to each<br>collation                               |            |
| COLLATIONS                                                 | Collations for each character set                                           |            |
| COLUMN_PRIVILEGES                                          | Privileges defined on columns                                               |            |
| COLUMN_STATISTICS                                          | Histogram statistics for column<br>values                                   |            |
| COLUMNS                                                    | Columns in each table                                                       |            |
| COLUMNS_EXTENSIONS                                         | Column attributes for primary<br>and secondary storage engines              |            |
| CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS                   | Current number of consecutive<br>failed connection attempts per<br>account  |            |
| ENABLED_ROLES                                              | Roles enabled within current<br>session                                     |            |
| ENGINES                                                    | Storage engine properties                                                   |            |
| EVENTS                                                     | Event Manager events                                                        |            |
| FILES                                                      | Files that store tablespace data                                            |            |
| INNODB_BUFFER_PAGE                                         | Pages in InnoDB buffer pool                                                 |            |
| INNODB_BUFFER_PAGE_LRU                                     | LRU ordering of pages in InnoDB<br>buffer pool                              |            |
| INNODB_BUFFER_POOL_STATS                                   | InnoDB buffer pool statistics                                               |            |
| INNODB_CACHED_INDEXES                                      | Number of index pages cached<br>per index in InnoDB buffer pool             |            |
| INNODB_CMP                                                 | Status for operations related to<br>compressed InnoDB tables                |            |
| INNODB_CMP_PER_INDEX                                       | Status for operations related to<br>compressed InnoDB tables and<br>indexes |            |
| INNODB_CMP_PER_INDEX_RESETStatus for operations related to | compressed InnoDB tables and<br>indexes                                     |            |
| INNODB_CMP_RESET                                           | Status for operations related to<br>compressed InnoDB tables                |            |
| INNODB_CMPMEM                                              | Status for compressed pages<br>within InnoDB buffer pool                    |            |
| INNODB_CMPMEM_RESET                                        | Status for compressed pages<br>within InnoDB buffer pool                    |            |
| INNODB_COLUMNS                                             | Columns in each InnoDB table                                                |            |

| Table Name                                                   | Description                                                                                       | Deprecated |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------|------------|
| INNODB_DATAFILES                                             | Data file path information for<br>InnoDB file-per-table and general<br>tablespaces                |            |
| INNODB_FIELDS                                                | Key columns of InnoDB indexes                                                                     |            |
| INNODB_FOREIGN                                               | InnoDB foreign-key metadata                                                                       |            |
| INNODB_FOREIGN_COLS                                          | InnoDB foreign-key column<br>status information                                                   |            |
| INNODB_FT_BEING_DELETED                                      | Snapshot of<br>INNODB_FT_DELETED table                                                            |            |
| INNODB_FT_CONFIG                                             | Metadata for InnoDB table<br>FULLTEXT index and associated<br>processing                          |            |
| INNODB_FT_DEFAULT_STOPWORDDefault list of stopwords for      | InnoDB FULLTEXT indexes                                                                           |            |
| INNODB_FT_DELETED                                            | Rows deleted from InnoDB table<br>FULLTEXT index                                                  |            |
| INNODB_FT_INDEX_CACHE                                        | Token information for newly<br>inserted rows in InnoDB<br>FULLTEXT index                          |            |
| INNODB_FT_INDEX_TABLE                                        | Inverted index information for<br>processing text searches against<br>InnoDB table FULLTEXT index |            |
| INNODB_INDEXES                                               | InnoDB index metadata                                                                             |            |
| INNODB_METRICS                                               | InnoDB performance information                                                                    |            |
| INNODB_SESSION_TEMP_TABLESPACES Session temporary-tablespace | metadata                                                                                          |            |
| INNODB_TABLES                                                | InnoDB table metadata                                                                             |            |
| INNODB_TABLESPACES                                           | InnoDB file-per-table, general,<br>and undo tablespace metadata                                   |            |
| INNODB_TABLESPACES_BRIEF                                     | Brief file-per-table, general,<br>undo, and system tablespace<br>metadata                         |            |
| INNODB_TABLESTATS                                            | InnoDB table low-level status<br>information                                                      |            |
| INNODB_TEMP_TABLE_INFO                                       | Information about active user<br>created InnoDB temporary tables                                  |            |
| INNODB_TRX                                                   | Active InnoDB transaction<br>information                                                          |            |
| INNODB_VIRTUAL                                               | InnoDB virtual generated column<br>metadata                                                       |            |
| KEY_COLUMN_USAGE                                             | Which key columns have<br>constraints                                                             |            |
| KEYWORDS                                                     | MySQL keywords                                                                                    |            |
| MYSQL_FIREWALL_USERS                                         | Firewall in-memory data for<br>account profiles                                                   | Yes        |
| MYSQL_FIREWALL_WHITELIST                                     | Firewall in-memory data for<br>account profile allowlists                                         | Yes        |

| Table Name                                                   | Description                                                                           | Deprecated |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------|------------|
| ndb_transid_mysql_connection_map NDB transaction information |                                                                                       |            |
| OPTIMIZER_TRACE                                              | Information produced by<br>optimizer trace activity                                   |            |
| PARAMETERS                                                   | Stored routine parameters and<br>stored function return values                        |            |
| PARTITIONS                                                   | Table partition information                                                           |            |
| PLUGINS                                                      | Plugin information                                                                    |            |
| PROCESSLIST                                                  | Information about currently<br>executing threads                                      |            |
| PROFILING                                                    | Statement profiling information                                                       |            |
| REFERENTIAL_CONSTRAINTS                                      | Foreign key information                                                               |            |
| RESOURCE_GROUPS                                              | Resource group information                                                            |            |
| ROLE_COLUMN_GRANTS                                           | Column privileges for roles<br>available to or granted by<br>currently enabled roles  |            |
| ROLE_ROUTINE_GRANTS                                          | Routine privileges for roles<br>available to or granted by<br>currently enabled roles |            |
| ROLE_TABLE_GRANTS                                            | Table privileges for roles<br>available to or granted by<br>currently enabled roles   |            |
| ROUTINES                                                     | Stored routine information                                                            |            |
| SCHEMA_PRIVILEGES                                            | Privileges defined on schemas                                                         |            |
| SCHEMATA                                                     | Schema information                                                                    |            |
| SCHEMATA_EXTENSIONS                                          | Schema options                                                                        |            |
| ST_GEOMETRY_COLUMNS                                          | Columns in each table that store<br>spatial data                                      |            |
| ST_SPATIAL_REFERENCE_SYSTEMS Available spatial reference     | systems                                                                               |            |
| ST_UNITS_OF_MEASURE                                          | Acceptable units for<br>ST_Distance()                                                 |            |
| STATISTICS                                                   | Table index statistics                                                                |            |
| TABLE_CONSTRAINTS                                            | Which tables have constraints                                                         |            |
| TABLE_CONSTRAINTS_EXTENSIONS Table constraint attributes for | primary and secondary storage<br>engines                                              |            |
| TABLE_PRIVILEGES                                             | Privileges defined on tables                                                          |            |
| TABLES                                                       | Table information                                                                     |            |
| TABLES_EXTENSIONS                                            | Table attributes for primary and<br>secondary storage engines                         |            |
| TABLESPACES                                                  | Tablespace information                                                                | Yes        |
| TABLESPACES_EXTENSIONS                                       | Tablespace attributes for primary<br>storage engines                                  |            |
| TP_THREAD_GROUP_STATE                                        | Thread pool thread group states                                                       |            |

| Table Name            | Description                             | Deprecated |
|-----------------------|-----------------------------------------|------------|
| TP_THREAD_GROUP_STATS | Thread pool thread group<br>statistics  |            |
| TP_THREAD_STATE       | Thread pool thread information          |            |
| TRIGGERS              | Trigger information                     |            |
| USER_ATTRIBUTES       | User comments and attributes            |            |
| USER_PRIVILEGES       | Privileges defined globally per<br>user |            |
| VIEW_ROUTINE_USAGE    | Stored functions used in views          |            |
| VIEW_TABLE_USAGE      | Tables and views used in views          |            |
| VIEWS                 | View information                        |            |