---
source: MySQL 8.0 Reference
title: 00_Overview
---

To reclaim operating system disk space when truncating an InnoDB table, the table must be stored in its own .ibd file. For a table to be stored in its own .ibd file, innodb\_file\_per\_table must enabled when the table is created. Additionally, there cannot be a foreign key constraint between the table being truncated and other tables, otherwise the TRUNCATE TABLE operation fails. A foreign key constraint between two columns in the same table, however, is permitted.

When a table is truncated, it is dropped and re-created in a new .ibd file, and the freed space is returned to the operating system. This is in contrast to truncating InnoDB tables that are stored within the InnoDB system tablespace (tables created when innodb\_file\_per\_table=OFF) and tables stored in shared general tablespaces, where only InnoDB can use the freed space after the table is truncated.

The ability to truncate tables and return disk space to the operating system also means that physical backups can be smaller. Truncating tables that are stored in the system tablespace (tables created when innodb\_file\_per\_table=OFF) or in a general tablespace leaves blocks of unused space in the tablespace.

# <span id="page-155-0"></span>**17.12 InnoDB and Online DDL**

The online DDL feature provides support for instant and in-place table alterations and concurrent DML. Benefits of this feature include:

- Improved responsiveness and availability in busy production environments, where making a table unavailable for minutes or hours is not practical.
- For in-place operations, the ability to adjust the balance between performance and concurrency during DDL operations using the LOCK clause. See [The LOCK clause.](#page-172-0)
- Less disk space usage and I/O overhead than the table-copy method.

![](_page_155_Picture_16.jpeg)

#### **Note**

ALGORITHM=INSTANT support is available for ADD COLUMN and other operations in MySQL 8.0.12.

Typically, you do not need to do anything special to enable online DDL. By default, MySQL performs the operation instantly or in place, as permitted, with as little locking as possible.

You can control aspects of a DDL operation using the ALGORITHM and LOCK clauses of the ALTER TABLE statement. These clauses are placed at the end of the statement, separated from the table and column specifications by commas. For example:

ALTER TABLE tbl\_name ADD PRIMARY KEY (column), ALGORITHM=INPLACE;

The LOCK clause may be used for operations that are performed in place and is useful for fine-tuning the degree of concurrent access to the table during operations. Only LOCK=DEFAULT is supported for operations that are performed instantly. The ALGORITHM clause is primarily intended for performance comparisons and as a fallback to the older table-copying behavior in case you encounter any issues. For example:

- To avoid accidentally making the table unavailable for reads, writes, or both, during an in-place ALTER TABLE operation, specify a clause on the ALTER TABLE statement such as LOCK=NONE (permit reads and writes) or LOCK=SHARED (permit reads). The operation halts immediately if the requested level of concurrency is not available.
- To compare performance between algorithms, run a statement with ALGORITHM=INSTANT, ALGORITHM=INPLACE and ALGORITHM=COPY. You can also run a statement with the old\_alter\_table configuration option enabled to force the use of ALGORITHM=COPY.
- To avoid tying up the server with an ALTER TABLE operation that copies the table, include ALGORITHM=INSTANT or ALGORITHM=INPLACE. The statement halts immediately if it cannot use the specified algorithm.

# <span id="page-156-0"></span>**17.12.1 Online DDL Operations**

Online support details, syntax examples, and usage notes for DDL operations are provided under the following topics in this section.

- [Index Operations](#page-156-1)
- [Primary Key Operations](#page-158-0)
- [Column Operations](#page-159-0)
- [Generated Column Operations](#page-164-0)
- [Foreign Key Operations](#page-166-0)
- [Table Operations](#page-167-0)
- [Tablespace Operations](#page-168-0)
- [Partitioning Operations](#page-169-0)

# <span id="page-156-1"></span>**Index Operations**

The following table provides an overview of online DDL support for index operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-157-0) [Notes](#page-157-0).

**Table 17.16 Online DDL Support for Index Operations**

| Operation                                     | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-----------------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Creating or<br>adding a<br>secondary<br>index | No      | Yes      | No                     | Yes               | No                        |
| Dropping an<br>index                          | No      | Yes      | No                     | Yes               | Yes                       |

| Operation                     | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Renaming an<br>index          | No      | Yes      | No                     | Yes               | Yes                       |
| Adding a<br>FULLTEXT<br>index | No      | Yes*     | No*                    | No                | No                        |
| Adding a<br>SPATIAL index     | No      | Yes      | No                     | No                | No                        |
| Changing the<br>index type    | Yes     | Yes      | No                     | Yes               | Yes                       |

### <span id="page-157-0"></span>**Syntax and Usage Notes**

• Creating or adding a secondary index

```
CREATE INDEX name ON table (col_list);
ALTER TABLE tbl_name ADD INDEX name (col_list);
```

The table remains available for read and write operations while the index is being created. The CREATE INDEX statement only finishes after all transactions that are accessing the table are completed, so that the initial state of the index reflects the most recent contents of the table.

Online DDL support for adding secondary indexes means that you can generally speed the overall process of creating and loading a table and associated indexes by creating the table without secondary indexes, then adding secondary indexes after the data is loaded.

A newly created secondary index contains only the committed data in the table at the time the CREATE INDEX or ALTER TABLE statement finishes executing. It does not contain any uncommitted values, old versions of values, or values marked for deletion but not yet removed from the old index.

Some factors affect the performance, space usage, and semantics of this operation. For details, see [Section 17.12.8, "Online DDL Limitations".](#page-178-1)

• Dropping an index

```
DROP INDEX name ON table;
ALTER TABLE tbl_name DROP INDEX name;
```

The table remains available for read and write operations while the index is being dropped. The DROP INDEX statement only finishes after all transactions that are accessing the table are completed, so that the initial state of the index reflects the most recent contents of the table.

• Renaming an index

```
ALTER TABLE tbl_name RENAME INDEX old_index_name TO new_index_name, ALGORITHM=INPLACE, LOCK=NONE;
```

• Adding a FULLTEXT index

```
CREATE FULLTEXT INDEX name ON table(column);
```

Adding the first FULLTEXT index rebuilds the table if there is no user-defined FTS\_DOC\_ID column. Additional FULLTEXT indexes may be added without rebuilding the table.

• Adding a SPATIAL index

```
CREATE TABLE geom (g GEOMETRY NOT NULL);
```

ALTER TABLE geom ADD SPATIAL INDEX(g), ALGORITHM=INPLACE, LOCK=SHARED;

• Changing the index type (USING {BTREE | HASH})

ALTER TABLE tbl\_name DROP INDEX i1, ADD INDEX i1(key\_part,...) USING BTREE, ALGORITHM=INSTANT;

# <span id="page-158-0"></span>**Primary Key Operations**

The following table provides an overview of online DDL support for primary key operations. An asterisk indicates additional information, an exception, or a dependency. See [Syntax and Usage Notes](#page-158-1).

**Table 17.17 Online DDL Support for Primary Key Operations**

| Operation                                       | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-------------------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Adding a<br>primary key                         | No      | Yes*     | Yes*                   | Yes               | No                        |
| Dropping a<br>primary key                       | No      | No       | Yes                    | No                | No                        |
| Dropping a<br>primary key and<br>adding another | No      | Yes      | Yes                    | Yes               | No                        |

### <span id="page-158-1"></span>**Syntax and Usage Notes**

• Adding a primary key

ALTER TABLE tbl\_name ADD PRIMARY KEY (column), ALGORITHM=INPLACE, LOCK=NONE;

Rebuilds the table in place. Data is reorganized substantially, making it an expensive operation. ALGORITHM=INPLACE is not permitted under certain conditions if columns have to be converted to NOT NULL.

Restructuring the clustered index always requires copying of table data. Thus, it is best to define the primary key when you create a table, rather than issuing ALTER TABLE ... ADD PRIMARY KEY later.

When you create a UNIQUE or PRIMARY KEY index, MySQL must do some extra work. For UNIQUE indexes, MySQL checks that the table contains no duplicate values for the key. For a PRIMARY KEY index, MySQL also checks that none of the PRIMARY KEY columns contains a NULL.

When you add a primary key using the ALGORITHM=COPY clause, MySQL converts NULL values in the associated columns to default values: 0 for numbers, an empty string for character-based columns and BLOBs, and 0000-00-00 00:00:00 for DATETIME. This is a non-standard behavior that Oracle recommends you not rely on. Adding a primary key using ALGORITHM=INPLACE is only permitted when the SQL\_MODE setting includes the strict\_trans\_tables or strict\_all\_tables flags; when the SQL\_MODE setting is strict, ALGORITHM=INPLACE is permitted, but the statement can still fail if the requested primary key columns contain NULL values. The ALGORITHM=INPLACE behavior is more standard-compliant.

If you create a table without a primary key, InnoDB chooses one for you, which can be the first UNIQUE key defined on NOT NULL columns, or a system-generated key. To avoid uncertainty and the potential space requirement for an extra hidden column, specify the PRIMARY KEY clause as part of the CREATE TABLE statement.

MySQL creates a new clustered index by copying the existing data from the original table to a temporary table that has the desired index structure. Once the data is completely copied to the temporary table, the original table is renamed with a different temporary table name. The temporary table comprising the new clustered index is renamed with the name of the original table, and the original table is dropped from the database.

The online performance enhancements that apply to operations on secondary indexes do not apply to the primary key index. The rows of an InnoDB table are stored in a clustered index organized based on the primary key, forming what some database systems call an "index-organized table". Because the table structure is closely tied to the primary key, redefining the primary key still requires copying the data.

When an operation on the primary key uses ALGORITHM=INPLACE, even though the data is still copied, it is more efficient than using ALGORITHM=COPY because:

- No undo logging or associated redo logging is required for ALGORITHM=INPLACE. These operations add overhead to DDL statements that use ALGORITHM=COPY.
- The secondary index entries are pre-sorted, and so can be loaded in order.
- The change buffer is not used, because there are no random-access inserts into the secondary indexes.
- Dropping a primary key

```
ALTER TABLE tbl_name DROP PRIMARY KEY, ALGORITHM=COPY;
```

Only ALGORITHM=COPY supports dropping a primary key without adding a new one in the same ALTER TABLE statement.

• Dropping a primary key and adding another

```
ALTER TABLE tbl_name DROP PRIMARY KEY, ADD PRIMARY KEY (column), ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

# <span id="page-159-0"></span>**Column Operations**

The following table provides an overview of online DDL support for column operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-160-0) [Notes](#page-160-0).

**Table 17.18 Online DDL Support for Column Operations**

| Operation                            | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|--------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Adding a<br>column                   | Yes*    | Yes      | No*                    | Yes*              | Yes                       |
| Dropping a<br>column                 | Yes*    | Yes      | Yes                    | Yes               | Yes                       |
| Renaming a<br>column                 | Yes*    | Yes      | No                     | Yes*              | Yes                       |
| Reordering<br>columns                | No      | Yes      | Yes                    | Yes               | No                        |
| Setting a<br>column default<br>value | Yes     | Yes      | No                     | Yes               | Yes                       |
| Changing the<br>column data<br>type  | No      | No       | Yes                    | No                | No                        |
| Extending<br>VARCHAR<br>column size  | No      | Yes      | No                     | Yes               | Yes                       |

| Operation                                                  | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|------------------------------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Dropping the<br>column default<br>value                    | Yes     | Yes      | No                     | Yes               | Yes                       |
| Changing the<br>auto-increment<br>value                    | No      | Yes      | No                     | Yes               | No*                       |
| Making a<br>column NULL                                    | No      | Yes      | Yes*                   | Yes               | No                        |
| Making a<br>column NOT<br>NULL                             | No      | Yes*     | Yes*                   | Yes               | No                        |
| Modifying the<br>definition of an<br>ENUM or SET<br>column | Yes     | Yes      | No                     | Yes               | Yes                       |

### <span id="page-160-0"></span>**Syntax and Usage Notes**

• Adding a column

```
ALTER TABLE tbl_name ADD COLUMN column_name column_definition, ALGORITHM=INSTANT;
```

INSTANT is the default algorithm as of MySQL 8.0.12, and INPLACE before that.

The following limitations apply when the INSTANT algorithm adds a column:

- A statement cannot combine the addition of a column with other ALTER TABLE actions that do not support the INSTANT algorithm.
- The INSTANT algorithm can add a column at any position in the table. Before MySQL 8.0.29, the INSTANT algorithm could only add a column as the last column of the table.
- Columns cannot be added to tables that use ROW\_FORMAT=COMPRESSED, tables with a FULLTEXT index, tables that reside in the data dictionary tablespace, or temporary tables. Temporary tables only support ALGORITHM=COPY.
- MySQL checks the row size when the INSTANT algorithm adds a column, and throws the following error if the addition exceeds the limit.

```
ERROR 4092 (HY000): Column can't be added with ALGORITHM=INSTANT as
after this max possible row size crosses max permissible row size. Try
ALGORITHM=INPLACE/COPY.
```

Before MySQL 8.0.29, MySQL does not check the row size when the INSTANT algorithm adds a column. However, MySQL does check the row size during DML operations that insert and update rows in the table.

• The maximum number of columns in the internal representation of the table cannot exceed 1022 after column addition with the INSTANT algorithm. The error message is:

```
ERROR 4158 (HY000): Column can't be added to tbl_name with
ALGORITHM=INSTANT anymore. Please try ALGORITHM=INPLACE/COPY
```

• The INSTANT algorithm can not add or drop columns to system schema tables, such as the internal mysql table. This limitation was added in MySQL 8.0.29.

• A column with a functional index cannot be dropped using the INSTANT algorithm.

Multiple columns may be added in the same ALTER TABLE statement. For example:

```
ALTER TABLE t1 ADD COLUMN c2 INT, ADD COLUMN c3 INT, ALGORITHM=INSTANT;
```

A new row version is created after each ALTER TABLE ... ALGORITHM=INSTANT operation that adds one or more columns, drops one or more columns, or adds and drops one or more columns in the same operation. The INFORMATION\_SCHEMA.INNODB\_TABLES.TOTAL\_ROW\_VERSIONS column tracks the number of row versions for a table. The value is incremented each time a column is instantly added or dropped. The initial value is 0.

```
mysql> SELECT NAME, TOTAL_ROW_VERSIONS FROM INFORMATION_SCHEMA.INNODB_TABLES 
 WHERE NAME LIKE 'test/t1';
+---------+--------------------+
| NAME | TOTAL_ROW_VERSIONS |
+---------+--------------------+
| test/t1 | 0 |
+---------+--------------------+
```

When a table with instantly added or dropped columns is rebuilt by table-rebuilding ALTER TABLE or OPTIMIZE TABLE operation, the TOTAL\_ROW\_VERSIONS value is reset to 0. The maximum number of row versions permitted is 64, as each row version requires additional space for table metadata. When the row version limit is reached, ADD COLUMN and DROP COLUMN operations using ALGORITHM=INSTANT are rejected with an error message that recommends rebuilding the table using the COPY or INPLACE algorithm.

ERROR 4092 (HY000): Maximum row versions reached for table test/t1. No more columns can be added or dropped instantly. Please use COPY/INPLACE.

The following INFORMATION\_SCHEMA columns provide additional metadata for instantly added columns. Refer to the descriptions of those columns for more information. See Section 28.4.9, "The INFORMATION\_SCHEMA INNODB\_COLUMNS Table", and Section 28.4.23, "The INFORMATION\_SCHEMA INNODB\_TABLES Table".

- INNODB\_COLUMNS.DEFAULT\_VALUE
- INNODB\_COLUMNS.HAS\_DEFAULT
- INNODB\_TABLES.INSTANT\_COLS

Concurrent DML is not permitted when adding an auto-increment column. Data is reorganized substantially, making it an expensive operation. At a minimum, ALGORITHM=INPLACE, LOCK=SHARED is required.

The table is rebuilt if ALGORITHM=INPLACE is used to add a column.

• Dropping a column

```
ALTER TABLE tbl_name DROP COLUMN column_name, ALGORITHM=INSTANT;
```

INSTANT is the default algorithm as of MySQL 8.0.29, and INPLACE before that.

The following limitations apply when the INSTANT algorithm is used to drop a column:

- Dropping a column cannot be combined in the same statement with other ALTER TABLE actions that do not support ALGORITHM=INSTANT.
- Columns cannot be dropped from tables that use ROW\_FORMAT=COMPRESSED, tables with a FULLTEXT index, tables that reside in the data dictionary tablespace, or temporary tables. Temporary tables only support ALGORITHM=COPY.

Multiple columns may be dropped in the same ALTER TABLE statement; for example:

```
ALTER TABLE t1 DROP COLUMN c4, DROP COLUMN c5, ALGORITHM=INSTANT;
```

Each time a column is added or dropped using ALGORITHM=INSTANT, a new row version is created. The INFORMATION\_SCHEMA.INNODB\_TABLES.TOTAL\_ROW\_VERSIONS column tracks the number of row versions for a table. The value is incremented each time a column is instantly added or dropped. The initial value is 0.

```
mysql> SELECT NAME, TOTAL_ROW_VERSIONS FROM INFORMATION_SCHEMA.INNODB_TABLES 
 WHERE NAME LIKE 'test/t1';
+---------+--------------------+
| NAME | TOTAL_ROW_VERSIONS |
+---------+--------------------+
| test/t1 | 0 |
+---------+--------------------+
```

When a table with instantly added or dropped columns is rebuilt by table-rebuilding ALTER TABLE or OPTIMIZE TABLE operation, the TOTAL\_ROW\_VERSIONS value is reset to 0. The maximum number of row versions permitted is 64, as each row version requires additional space for table metadata. When the row version limit is reached, ADD COLUMN and DROP COLUMN operations using ALGORITHM=INSTANT are rejected with an error message that recommends rebuilding the table using the COPY or INPLACE algorithm.

```
ERROR 4092 (HY000): Maximum row versions reached for table test/t1. No
more columns can be added or dropped instantly. Please use COPY/INPLACE.
```

If an algorithm other than ALGORITHM=INSTANT is used, data is reorganized substantially, making it an expensive operation.

#### • Renaming a column

```
ALTER TABLE tbl CHANGE old_col_name new_col_name data_type, ALGORITHM=INSTANT;
```

ALGORITHM=INSTANT support for renaming a column was added in MySQL 8.0.28. Earlier MySQL Server releases support only ALGORITHM=INPLACE and ALGORITHM=COPY when renaming a column.

To permit concurrent DML, keep the same data type and only change the column name.

When you keep the same data type and [NOT] NULL attribute, only changing the column name, the operation can always be performed online.

Renaming a column referenced from another table is only permitted with ALGORITHM=INPLACE. If you use ALGORITHM=INSTANT, ALGORITHM=COPY, or some other condition that causes the operation to use those algorithms, the ALTER TABLE statement fails.

ALGORITHM=INSTANT supports renaming a virtual column; ALGORITHM=INPLACE does not.

ALGORITHM=INSTANT and ALGORITHM=INPLACE do not support renaming a column when adding or dropping a virtual column in the same statement. In this case, only ALGORITHM=COPY is supported.

• Reordering columns

To reorder columns, use FIRST or AFTER in CHANGE or MODIFY operations.

```
ALTER TABLE tbl_name MODIFY COLUMN col_name column_definition FIRST, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

• Changing the column data type

```
ALTER TABLE tbl_name CHANGE c1 c1 BIGINT, ALGORITHM=COPY;
```

Changing the column data type is only supported with ALGORITHM=COPY.

• Extending VARCHAR column size

```
ALTER TABLE tbl_name CHANGE COLUMN c1 c1 VARCHAR(255), ALGORITHM=INPLACE, LOCK=NONE;
```

The number of length bytes required by a VARCHAR column must remain the same. For VARCHAR columns of 0 to 255 bytes in size, one length byte is required to encode the value. For VARCHAR columns of 256 bytes in size or more, two length bytes are required. As a result, in-place ALTER TABLE only supports increasing VARCHAR column size from 0 to 255 bytes, or from 256 bytes to a greater size. In-place ALTER TABLE does not support increasing the size of a VARCHAR column from less than 256 bytes to a size equal to or greater than 256 bytes. In this case, the number of required length bytes changes from 1 to 2, which is only supported by a table copy (ALGORITHM=COPY). For example, attempting to change VARCHAR column size for a single byte character set from VARCHAR(255) to VARCHAR(256) using in-place ALTER TABLE returns this error:

```
ALTER TABLE tbl_name ALGORITHM=INPLACE, CHANGE COLUMN c1 c1 VARCHAR(256);
ERROR 0A000: ALGORITHM=INPLACE is not supported. Reason: Cannot change
column type INPLACE. Try ALGORITHM=COPY.
```

![](_page_163_Picture_20.jpeg)

#### **Note**

The byte length of a VARCHAR column is dependant on the byte length of the character set.

Decreasing VARCHAR size using in-place ALTER TABLE is not supported. Decreasing VARCHAR size requires a table copy (ALGORITHM=COPY).

• Setting a column default value

```
ALTER TABLE tbl_name ALTER COLUMN col SET DEFAULT literal, ALGORITHM=INSTANT;
```

Only modifies table metadata. Default column values are stored in the data dictionary.

• Dropping a column default value

```
ALTER TABLE tbl ALTER COLUMN col DROP DEFAULT, ALGORITHM=INSTANT;
```

• Changing the auto-increment value

```
ALTER TABLE table AUTO_INCREMENT=next_value, ALGORITHM=INPLACE, LOCK=NONE;
```

Modifies a value stored in memory, not the data file.

In a distributed system using replication or sharding, you sometimes reset the auto-increment counter for a table to a specific value. The next row inserted into the table uses the specified value for its auto-increment column. You might also use this technique in a data warehousing environment where you periodically empty all the tables and reload them, and restart the autoincrement sequence from 1.

• Making a column NULL

```
ALTER TABLE tbl_name MODIFY COLUMN column_name data_type NULL, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place. Data is reorganized substantially, making it an expensive operation.

• Making a column NOT NULL

```
ALTER TABLE tbl_name MODIFY COLUMN column_name data_type NOT NULL, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place. STRICT\_ALL\_TABLES or STRICT\_TRANS\_TABLES SQL\_MODE is required for the operation to succeed. The operation fails if the column contains NULL values. The server prohibits changes to foreign key columns that have the potential to cause loss of referential integrity. See Section 15.1.9, "ALTER TABLE Statement". Data is reorganized substantially, making it an expensive operation.

• Modifying the definition of an ENUM or SET column

```
CREATE TABLE t1 (c1 ENUM('a', 'b', 'c'));
ALTER TABLE t1 MODIFY COLUMN c1 ENUM('a', 'b', 'c', 'd'), ALGORITHM=INSTANT;
```

Modifying the definition of an ENUM or SET column by adding new enumeration or set members to the end of the list of valid member values may be performed instantly or in place, as long as the storage size of the data type does not change. For example, adding a member to a SET column that has 8 members changes the required storage per value from 1 byte to 2 bytes; this requires a table copy. Adding members in the middle of the list causes renumbering of existing members, which requires a table copy.

# <span id="page-164-0"></span>**Generated Column Operations**

The following table provides an overview of online DDL support for generated column operations. For details, see [Syntax and Usage Notes.](#page-165-0)

**Table 17.19 Online DDL Support for Generated Column Operations**

| Operation                 | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|---------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Adding a<br>STORED column | No      | No       | Yes                    | No                | No                        |

| Operation                            | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|--------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Modifying<br>STORED column<br>order  | No      | No       | Yes                    | No                | No                        |
| Dropping a<br>STORED column          | No      | Yes      | Yes                    | Yes               | No                        |
| Adding a<br>VIRTUAL<br>column        | Yes     | Yes      | No                     | Yes               | Yes                       |
| Modifying<br>VIRTUAL<br>column order | No      | No       | Yes                    | No                | No                        |
| Dropping a<br>VIRTUAL<br>column      | Yes     | Yes      | No                     | Yes               | Yes                       |

#### <span id="page-165-0"></span>**Syntax and Usage Notes**

• Adding a STORED column

```
ALTER TABLE t1 ADD COLUMN (c2 INT GENERATED ALWAYS AS (c1 + 1) STORED), ALGORITHM=COPY;
```

ADD COLUMN is not an in-place operation for stored columns (done without using a temporary table) because the expression must be evaluated by the server.

• Modifying STORED column order

```
ALTER TABLE t1 MODIFY COLUMN c2 INT GENERATED ALWAYS AS (c1 + 1) STORED FIRST, ALGORITHM=COPY;
```

Rebuilds the table in place.

• Dropping a STORED column

```
ALTER TABLE t1 DROP COLUMN c2, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place.

• Adding a VIRTUAL column

```
ALTER TABLE t1 ADD COLUMN (c2 INT GENERATED ALWAYS AS (c1 + 1) VIRTUAL), ALGORITHM=INSTANT;
```

Adding a virtual column can be performed instantly or in place for non-partitioned tables.

Adding a VIRTUAL is not an in-place operation for partitioned tables.

• Modifying VIRTUAL column order

```
ALTER TABLE t1 MODIFY COLUMN c2 INT GENERATED ALWAYS AS (c1 + 1) VIRTUAL FIRST, ALGORITHM=COPY;
```

• Dropping a VIRTUAL column

```
ALTER TABLE t1 DROP COLUMN c2, ALGORITHM=INSTANT;
```

Dropping a VIRTUAL column can be performed instantly or in place for non-partitioned tables.

# <span id="page-166-0"></span>**Foreign Key Operations**

The following table provides an overview of online DDL support for foreign key operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-166-1) [Notes](#page-166-1).

**Table 17.20 Online DDL Support for Foreign Key Operations**

| Operation                               | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-----------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Adding a<br>foreign key<br>constraint   | No      | Yes*     | No                     | Yes               | Yes                       |
| Dropping a<br>foreign key<br>constraint | No      | Yes      | No                     | Yes               | Yes                       |

#### <span id="page-166-1"></span>**Syntax and Usage Notes**

• Adding a foreign key constraint

The INPLACE algorithm is supported when foreign\_key\_checks is disabled. Otherwise, only the COPY algorithm is supported.

```
ALTER TABLE tbl1 ADD CONSTRAINT fk_name FOREIGN KEY index (col1)
 REFERENCES tbl2(col2) referential_actions;
```

• Dropping a foreign key constraint

```
ALTER TABLE tbl DROP FOREIGN KEY fk_name;
```

Dropping a foreign key can be performed online with the foreign\_key\_checks option enabled or disabled.

If you do not know the names of the foreign key constraints on a particular table, issue the following statement and find the constraint name in the CONSTRAINT clause for each foreign key:

```
SHOW CREATE TABLE table\G
```

Or, query the Information Schema TABLE\_CONSTRAINTS table and use the CONSTRAINT\_NAME and CONSTRAINT\_TYPE columns to identify the foreign key names.

You can also drop a foreign key and its associated index in a single statement:

ALTER TABLE table DROP FOREIGN KEY constraint, DROP INDEX index;

![](_page_166_Picture_17.jpeg)

#### **Note**

If foreign keys are already present in the table being altered (that is, it is a child table containing a FOREIGN KEY ... REFERENCE clause), additional restrictions apply to online DDL operations, even those not directly involving the foreign key columns:

- An ALTER TABLE on the child table could wait for another transaction to commit, if a change to the parent table causes associated changes in the child table through an ON UPDATE or ON DELETE clause using the CASCADE or SET NULL parameters.
- In the same way, if a table is the parent table in a foreign key relationship, even though it does not contain any FOREIGN KEY clauses, it could wait for

the ALTER TABLE to complete if an INSERT, UPDATE, or DELETE statement causes an ON UPDATE or ON DELETE action in the child table.

# <span id="page-167-0"></span>**Table Operations**

The following table provides an overview of online DDL support for table operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-167-1) [Notes](#page-167-1).

**Table 17.21 Online DDL Support for Table Operations**

| Operation                                 | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-------------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Changing the<br>ROW_FORMAT                | No      | Yes      | Yes                    | Yes               | No                        |
| Changing the<br>KEY_BLOCK_SIZE            | No      | Yes      | Yes                    | Yes               | No                        |
| Setting<br>persistent table<br>statistics | No      | Yes      | No                     | Yes               | Yes                       |
| Specifying a<br>character set             | No      | Yes      | Yes*                   | Yes               | No                        |
| Converting a<br>character set             | No      | Yes      | Yes*                   | No                | No                        |
| Optimizing a<br>table                     | No      | Yes*     | Yes                    | Yes               | No                        |
| Rebuilding<br>with the FORCE<br>option    | No      | Yes*     | Yes                    | Yes               | No                        |
| Performing a<br>null rebuild              | No      | Yes*     | Yes                    | Yes               | No                        |
| Renaming a<br>table                       | Yes     | Yes      | No                     | Yes               | Yes                       |

#### <span id="page-167-1"></span>**Syntax and Usage Notes**

• Changing the ROW\_FORMAT

```
ALTER TABLE tbl_name ROW_FORMAT = row_format, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

For additional information about the ROW\_FORMAT option, see Table Options.

• Changing the KEY\_BLOCK\_SIZE

```
ALTER TABLE tbl_name KEY_BLOCK_SIZE = value, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

For additional information about the KEY\_BLOCK\_SIZE option, see Table Options.

• Setting persistent table statistics options

```
ALTER TABLE tbl_name STATS_PERSISTENT=0, STATS_SAMPLE_PAGES=20, STATS_AUTO_RECALC=1, ALGORITHM=INPLACE, LOCK=NONE;
```

Only modifies table metadata.

Persistent statistics include STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES. For more information, see [Section 17.8.10.1, "Configuring Persistent](#page-113-0) [Optimizer Statistics Parameters"](#page-113-0).

• Specifying a character set

```
ALTER TABLE tbl_name CHARACTER SET = charset_name, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table if the new character encoding is different.

• Converting a character set

```
ALTER TABLE tbl_name CONVERT TO CHARACTER SET charset_name, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table if the new character encoding is different.

• Optimizing a table

```
OPTIMIZE TABLE tbl_name;
```

In-place operation is not supported for tables with FULLTEXT indexes. The operation uses the INPLACE algorithm, but ALGORITHM and LOCK syntax is not permitted.

• Rebuilding a table with the FORCE option

```
ALTER TABLE tbl_name FORCE, ALGORITHM=INPLACE, LOCK=NONE;
```

Uses ALGORITHM=INPLACE as of MySQL 5.6.17. ALGORITHM=INPLACE is not supported for tables with FULLTEXT indexes.

• Performing a "null" rebuild

```
ALTER TABLE tbl_name ENGINE=InnoDB, ALGORITHM=INPLACE, LOCK=NONE;
```

Uses ALGORITHM=INPLACE as of MySQL 5.6.17. ALGORITHM=INPLACE is not supported for tables with FULLTEXT indexes.

• Renaming a table

```
ALTER TABLE old_tbl_name RENAME TO new_tbl_name, ALGORITHM=INSTANT;
```

Renaming a table can be performed instantly or in place. MySQL renames files that correspond to the table tbl\_name without making a copy. (You can also use the RENAME TABLE statement to rename tables. See Section 15.1.36, "RENAME TABLE Statement".) Privileges granted specifically for the renamed table are not migrated to the new name. They must be changed manually.

# <span id="page-168-0"></span>**Tablespace Operations**

The following table provides an overview of online DDL support for tablespace operations. For details, see [Syntax and Usage Notes.](#page-169-1)

**Table 17.22 Online DDL Support for Tablespace Operations**

| Operation                           | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|-------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| Renaming<br>a general<br>tablespace | No      | Yes      | No                     | Yes               | Yes                       |
| Enabling or<br>disabling<br>general | No      | Yes      | No                     | Yes               | No                        |

| Operation                                                              | Instant | In Place | Rebuilds Table Permits | Concurrent<br>DML | Only Modifies<br>Metadata |
|------------------------------------------------------------------------|---------|----------|------------------------|-------------------|---------------------------|
| tablespace<br>encryption                                               |         |          |                        |                   |                           |
| Enabling or<br>disabling file<br>per-table<br>tablespace<br>encryption | No      | No       | Yes                    | No                | No                        |

#### <span id="page-169-1"></span>**Syntax and Usage Notes**

• Renaming a general tablespace

ALTER TABLESPACE tablespace\_name RENAME TO new\_tablespace\_name;

ALTER TABLESPACE ... RENAME TO uses the INPLACE algorithm but does not support the ALGORITHM clause.

• Enabling or disabling general tablespace encryption

ALTER TABLESPACE tablespace\_name ENCRYPTION='Y';

ALTER TABLESPACE ... ENCRYPTION uses the INPLACE algorithm but does not support the ALGORITHM clause.

For related information, see [Section 17.13, "InnoDB Data-at-Rest Encryption"](#page-178-0).

• Enabling or disabling file-per-table tablespace encryption

ALTER TABLE tbl\_name ENCRYPTION='Y', ALGORITHM=COPY;

For related information, see [Section 17.13, "InnoDB Data-at-Rest Encryption"](#page-178-0).

# <span id="page-169-0"></span>**Partitioning Operations**

With the exception of some ALTER TABLE partitioning clauses, online DDL operations for partitioned InnoDB tables follow the same rules that apply to regular InnoDB tables.

Some ALTER TABLE partitioning clauses do not go through the same internal online DDL API as regular non-partitioned InnoDB tables. As a result, online support for ALTER TABLE partitioning clauses varies.

The following table shows the online status for each ALTER TABLE partitioning statement. Regardless of the online DDL API that is used, MySQL attempts to minimize data copying and locking where possible.

ALTER TABLE partitioning options that use ALGORITHM=COPY or that only permit "ALGORITHM=DEFAULT, LOCK=DEFAULT", repartition the table using the COPY algorithm. In other words, a new partitioned table is created with the new partitioning scheme. The newly created table includes any changes applied by the ALTER TABLE statement, and table data is copied into the new table structure.

**Table 17.23 Online DDL Support for Partitioning Operations**

| Partitioning<br>Clause | Instant | In Place | Permits DML | Notes           |
|------------------------|---------|----------|-------------|-----------------|
| PARTITION BY           | No      | No       | No          | Permits         |
|                        |         |          |             | ALGORITHM=COPY, |
|                        |         |          |             | LOCK={DEFAULT   |

| Partitioning<br>Clause | Instant | In Place | Permits DML | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|------------------------|---------|----------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                        |         |          |             | SHARED <br>EXCLUSIVE}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ADD PARTITION          | No      | Yes*     | Yes*        | ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>NONE SHARED <br>EXCLUSISVE}<br>is supported<br>for RANGE and<br>LIST partitions,<br>ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>SHARED <br>EXCLUSISVE}<br>for HASH and KEY<br>partitions, and<br>ALGORITHM=COPY,<br>LOCK={SHARED <br>EXCLUSIVE} for<br>all partition types.<br>Does not copy<br>existing data for<br>tables partitioned<br>by RANGE or LIST.<br>Concurrent queries<br>are permitted with<br>ALGORITHM=COPY<br>for tables<br>partitioned by<br>HASH or LIST, as<br>MySQL copies the<br>data while holding<br>a shared lock. |
| DROP PARTITION         | No      | Yes*     | Yes*        | ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>NONE SHARED <br>EXCLUSIVE} is<br>supported. Does<br>not copy data for<br>tables partitioned<br>by RANGE or LIST.<br>DROP<br>PARTITION with<br>ALGORITHM=INPLACE<br>deletes data stored<br>in the partition and<br>drops the partition.<br>However, DROP<br>PARTITION with<br>ALGORITHM=COPY<br>or<br>old_alter_table=ON<br>rebuilds the<br>partitioned table<br>and attempts to                                                                                                                                                        |

| Partitioning<br>Clause  | Instant | In Place | Permits DML | Notes                                                                                                                                                                                          |
|-------------------------|---------|----------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                         |         |          |             | move data from the<br>dropped partition<br>to another partition<br>with a compatible<br>PARTITION<br>VALUES definition.<br>Data that cannot<br>be moved to<br>another partition is<br>deleted. |
| DISCARD<br>PARTITION    | No      | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT                                                                                                                                             |
| IMPORT<br>PARTITION     | No      | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT                                                                                                                                             |
| TRUNCATE<br>PARTITION   | No      | Yes      | Yes         | Does not copy<br>existing data. It<br>merely deletes<br>rows; it does not<br>alter the definition<br>of the table itself,<br>or of any of its<br>partitions.                                   |
| COALESCE<br>PARTITION   | No      | Yes*     | No          | ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>SHARED <br>EXCLUSIVE} is<br>supported.                                                                                                                 |
| REORGANIZE<br>PARTITION | No      | Yes*     | No          | ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>SHARED <br>EXCLUSIVE} is<br>supported.                                                                                                                 |
| EXCHANGE<br>PARTITION   | No      | Yes      | Yes         |                                                                                                                                                                                                |
| ANALYZE<br>PARTITION    | No      | Yes      | Yes         |                                                                                                                                                                                                |
| CHECK<br>PARTITION      | No      | Yes      | Yes         |                                                                                                                                                                                                |
| OPTIMIZE<br>PARTITION   | No      | No       | No          | ALGORITHM and<br>LOCK clauses<br>are ignored.<br>Rebuilds the<br>entire table. See<br>Section 26.3.4,<br>"Maintenance of<br>Partitions".                                                       |
| REBUILD<br>PARTITION    | No      | Yes*     | No          | ALGORITHM=INPLACE,<br>LOCK={DEFAULT <br>SHARED                                                                                                                                                 |

| Partitioning<br>Clause | Instant | In Place | Permits DML | Notes                                                                 |
|------------------------|---------|----------|-------------|-----------------------------------------------------------------------|
|                        |         |          |             | EXCLUSIVE} is<br>supported.                                           |
| REPAIR<br>PARTITION    | No      | Yes      | Yes         |                                                                       |
| REMOVE<br>PARTITIONING | No      | No       | No          | Permits<br>ALGORITHM=COPY,<br>LOCK={DEFAULT <br>SHARED <br>EXCLUSIVE} |

Non-partitioning online ALTER TABLE operations on partitioned tables follow the same rules that apply to regular tables. However, ALTER TABLE performs online operations on each table partition, which causes increased demand on system resources due to operations being performed on multiple partitions.

For additional information about ALTER TABLE partitioning clauses, see Partitioning Options, and Section 15.1.9.1, "ALTER TABLE Partition Operations". For information about partitioning in general, see Chapter 26, Partitioning.

# <span id="page-172-1"></span>**17.12.2 Online DDL Performance and Concurrency**

Online DDL improves several aspects of MySQL operation:

- Applications that access the table are more responsive because queries and DML operations on the table can proceed while the DDL operation is in progress. Reduced locking and waiting for MySQL server resources leads to greater scalability, even for operations that are not involved in the DDL operation.
- Instant operations only modify metadata in the data dictionary. An exclusive metadata lock on the table may be taken briefly during the execution phase of the operation. Table data is unaffected, making operations instantaneous. Concurrent DML is permitted.
- Online operations avoid the disk I/O and CPU cycles associated with the table-copy method, which minimizes overall load on the database. Minimizing load helps maintain good performance and high throughput during the DDL operation.
- Online operations read less data into the buffer pool than table-copy operations, which reduces purging of frequently accessed data from memory. Purging of frequently accessed data can cause a temporary performance dip after a DDL operation.

# <span id="page-172-0"></span>**The LOCK clause**

By default, MySQL uses as little locking as possible during a DDL operation. The LOCK clause can be specified for in-place operations and some copy operations to enforce more restrictive locking, if required. If the LOCK clause specifies a less restrictive level of locking than is permitted for a particular DDL operation, the statement fails with an error. LOCK clauses are described below, in order of least to most restrictive:

#### • LOCK=NONE:

Permits concurrent queries and DML.

For example, use this clause for tables involving customer signups or purchases, to avoid making the tables unavailable during lengthy DDL operations.

#### • LOCK=SHARED:

Permits concurrent queries but blocks DML.

For example, use this clause on data warehouse tables, where you can delay data load operations until the DDL operation is finished, but queries cannot be delayed for long periods.

#### • LOCK=DEFAULT:

Permits as much concurrency as possible (concurrent queries, DML, or both). Omitting the LOCK clause is the same as specifying LOCK=DEFAULT.

Use this clause when you do not expect the default locking level of the DDL statement to cause any availability problems for the table.

#### • LOCK=EXCLUSIVE:

Blocks concurrent queries and DML.

Use this clause if the primary concern is finishing the DDL operation in the shortest amount of time possible, and concurrent query and DML access is not necessary. You might also use this clause if the server is supposed to be idle, to avoid unexpected table accesses.

# **Online DDL and Metadata Locks**

Online DDL operations can be viewed as having three phases:

#### • Phase 1: Initialization

In the initialization phase, the server determines how much concurrency is permitted during the operation, taking into account storage engine capabilities, operations specified in the statement, and user-specified ALGORITHM and LOCK options. During this phase, a shared upgradeable metadata lock is taken to protect the current table definition.

#### • Phase 2: Execution

In this phase, the statement is prepared and executed. Whether the metadata lock is upgraded to exclusive depends on the factors assessed in the initialization phase. If an exclusive metadata lock is required, it is only taken briefly during statement preparation.

# • Phase 3: Commit Table Definition

In the commit table definition phase, the metadata lock is upgraded to exclusive to evict the old table definition and commit the new one. Once granted, the duration of the exclusive metadata lock is brief.

Due to the exclusive metadata lock requirements outlined above, an online DDL operation may have to wait for concurrent transactions that hold metadata locks on the table to commit or rollback. Transactions started before or during the DDL operation can hold metadata locks on the table being altered. In the case of a long running or inactive transaction, an online DDL operation can time out waiting for an exclusive metadata lock. Additionally, a pending exclusive metadata lock requested by an online DDL operation blocks subsequent transactions on the table.

The following example demonstrates an online DDL operation waiting for an exclusive metadata lock, and how a pending metadata lock blocks subsequent transactions on the table.

#### Session 1:

```
mysql> CREATE TABLE t1 (c1 INT) ENGINE=InnoDB;
mysql> START TRANSACTION;
mysql> SELECT * FROM t1;
```

The session 1 SELECT statement takes a shared metadata lock on table t1.

#### Session 2:

```
mysql> ALTER TABLE t1 ADD COLUMN x INT, ALGORITHM=INPLACE, LOCK=NONE;
```

The online DDL operation in session 2, which requires an exclusive metadata lock on table t1 to commit table definition changes, must wait for the session 1 transaction to commit or roll back.

#### Session 3:

```
mysql> SELECT * FROM t1;
```

The SELECT statement issued in session 3 is blocked waiting for the exclusive metadata lock requested by the ALTER TABLE operation in session 2 to be granted.

You can use SHOW FULL PROCESSLIST to determine if transactions are waiting for a metadata lock.

```
mysql> SHOW FULL PROCESSLIST\G
...
*************************** 2. row ***************************
 Id: 5
 User: root
 Host: localhost
 db: test
Command: Query
 Time: 44
 State: Waiting for table metadata lock
 Info: ALTER TABLE t1 ADD COLUMN x INT, ALGORITHM=INPLACE, LOCK=NONE
...
*************************** 4. row ***************************
 Id: 7
 User: root
 Host: localhost
 db: test
Command: Query
 Time: 5
 State: Waiting for table metadata lock
 Info: SELECT * FROM t1
4 rows in set (0.00 sec)
```

Metadata lock information is also exposed through the Performance Schema metadata\_locks table, which provides information about metadata lock dependencies between sessions, the metadata lock a session is waiting for, and the session that currently holds the metadata lock. For more information, see Section 29.12.13.3, "The metadata\_locks Table".

# **Online DDL Performance**

The performance of a DDL operation is largely determined by whether the operation is performed instantly, in place, and whether it rebuilds the table.

To assess the relative performance of a DDL operation, you can compare results using ALGORITHM=INSTANT, ALGORITHM=INPLACE, and ALGORITHM=COPY. A statement can also be run with old\_alter\_table enabled to force the use of ALGORITHM=COPY.

For DDL operations that modify table data, you can determine whether a DDL operation performs changes in place or performs a table copy by looking at the "rows affected" value displayed after the command finishes. For example:

• Changing the default value of a column (fast, does not affect the table data):

```
Query OK, 0 rows affected (0.07 sec)
```

• Adding an index (takes time, but 0 rows affected shows that the table is not copied):

```
Query OK, 0 rows affected (21.42 sec)
```

• Changing the data type of a column (takes substantial time and requires rebuilding all the rows of the table):

```
Query OK, 1671168 rows affected (1 min 35.54 sec)
```

Before running a DDL operation on a large table, check whether the operation is fast or slow as follows:

- 1. Clone the table structure.
- 2. Populate the cloned table with a small amount of data.
- 3. Run the DDL operation on the cloned table.
- 4. Check whether the "rows affected" value is zero or not. A nonzero value means the operation copies table data, which might require special planning. For example, you might do the DDL operation during a period of scheduled downtime, or on each replica server one at a time.

![](_page_175_Picture_6.jpeg)

#### **Note**

For a greater understanding of the MySQL processing associated with a DDL operation, examine Performance Schema and INFORMATION\_SCHEMA tables related to InnoDB before and after DDL operations to see the number of physical reads, writes, memory allocations, and so on.

Performance Schema stage events can be used to monitor ALTER TABLE progress. See Section 17.16.1, "Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema".

Because there is some processing work involved with recording the changes made by concurrent DML operations, then applying those changes at the end, an online DDL operation could take longer overall than the table-copy mechanism that blocks table access from other sessions. The reduction in raw performance is balanced against better responsiveness for applications that use the table. When evaluating the techniques for changing table structure, consider end-user perception of performance, based on factors such as load times for web pages.

# <span id="page-175-0"></span>**17.12.3 Online DDL Space Requirements**

Disk space requirements for online DDL operations are outlined below. The requirements do not apply to operations that are performed instantly.

• Temporary log files:

A temporary log file records concurrent DML when an online DDL operation creates an index or alters a table. The temporary log file is extended as required by the value of innodb\_sort\_buffer\_size up to a maximum specified by innodb\_online\_alter\_log\_max\_size. If the operation takes a long time and concurrent DML modifies the table so much that the size of the temporary log file exceeds the value of innodb\_online\_alter\_log\_max\_size, the online DDL operation fails with a DB\_ONLINE\_LOG\_TOO\_BIG error, and uncommitted concurrent DML operations are rolled back. A large innodb\_online\_alter\_log\_max\_size setting permits more DML during an online DDL operation, but it also extends the period of time at the end of the DDL operation when the table is locked to apply logged DML.

The innodb\_sort\_buffer\_size variable also defines the size of the temporary log file read buffer and write buffer.

• Temporary sort files:

Online DDL operations that rebuild the table write temporary sort files to the MySQL temporary directory (\$TMPDIR on Unix, %TEMP% on Windows, or the directory specified by --tmpdir) during index creation. Temporary sort files are not created in the directory that contains the original table. Each temporary sort file is large enough to hold one column of data, and each sort file is removed when its data is merged into the final table or index. Operations involving temporary sort files may require temporary space equal to the amount of data in the table plus indexes. An error is reported if online DDL operation uses all of the available disk space on the file system where the data directory resides.

If the MySQL temporary directory is not large enough to hold the sort files, set tmpdir to a different directory. Alternatively, define a separate temporary directory for online DDL operations using innodb\_tmpdir. This option was introduced to help avoid temporary directory overflows that could occur as a result of large temporary sort files.

• Intermediate table files:

Some online DDL operations that rebuild the table create a temporary intermediate table file in the same directory as the original table. An intermediate table file may require space equal to the size of the original table. Intermediate table file names begin with #sql-ib prefix and only appear briefly during the online DDL operation.

The innodb\_tmpdir option is not applicable to intermediate table files.