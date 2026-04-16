---
source: MySQL 5.7 Reference
title: 00_Overview
---

Full-text indexes are created on text-based columns (CHAR, VARCHAR, or TEXT columns) to speed up queries and DML operations on data contained within those columns.

A full-text index is defined as part of a CREATE TABLE statement or added to an existing table using ALTER TABLE or CREATE INDEX.

Full-text search is performed using MATCH() ... AGAINST syntax. For usage information, see Section 12.9, "Full-Text Search Functions".

InnoDB full-text indexes are described under the following topics in this section:

- [InnoDB Full-Text Index Design](#page-44-0)
- [InnoDB Full-Text Index Tables](#page-44-1)
- [InnoDB Full-Text Index Cache](#page-45-0)
- [InnoDB Full-Text Index DOC\\_ID and FTS\\_DOC\\_ID Column](#page-46-0)
- [InnoDB Full-Text Index Deletion Handling](#page-47-0)
- [InnoDB Full-Text Index Transaction Handling](#page-47-1)
- [Monitoring InnoDB Full-Text Indexes](#page-48-1)

### <span id="page-44-0"></span>**InnoDB Full-Text Index Design**

InnoDB full-text indexes have an inverted index design. Inverted indexes store a list of words, and for each word, a list of documents that the word appears in. To support proximity search, position information for each word is also stored, as a byte offset.

### <span id="page-44-1"></span>**InnoDB Full-Text Index Tables**

When an InnoDB full-text index is created, a set of index tables is created, as shown in the following example:

```
mysql> CREATE TABLE opening_lines (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 opening_line TEXT(500),
 author VARCHAR(200),
 title VARCHAR(200),
 FULLTEXT idx (opening_line)
 ) ENGINE=InnoDB;
mysql> SELECT table_id, name, space from INFORMATION_SCHEMA.INNODB_SYS_TABLES
 WHERE name LIKE 'test/%';
+----------+----------------------------------------------------+-------+
| table_id | name | space |
+----------+----------------------------------------------------+-------+
| 333 | test/FTS_0000000000000147_00000000000001c9_INDEX_1 | 289 |
| 334 | test/FTS_0000000000000147_00000000000001c9_INDEX_2 | 290 |
| 335 | test/FTS_0000000000000147_00000000000001c9_INDEX_3 | 291 |
| 336 | test/FTS_0000000000000147_00000000000001c9_INDEX_4 | 292 |
| 337 | test/FTS_0000000000000147_00000000000001c9_INDEX_5 | 293 |
| 338 | test/FTS_0000000000000147_00000000000001c9_INDEX_6 | 294 |
| 330 | test/FTS_0000000000000147_BEING_DELETED | 286 |
| 331 | test/FTS_0000000000000147_BEING_DELETED_CACHE | 287 |
| 332 | test/FTS_0000000000000147_CONFIG | 288 |
| 328 | test/FTS_0000000000000147_DELETED | 284 |
| 329 | test/FTS_0000000000000147_DELETED_CACHE | 285 |
| 327 | test/opening_lines | 283 |
+----------+----------------------------------------------------+-------+
```

The first six index tables comprise the inverted index and are referred to as auxiliary index tables. When incoming documents are tokenized, the individual words (also referred to as "tokens") are inserted into the index tables along with position information and an associated DOC\_ID. The words are fully sorted and partitioned among the six index tables based on the character set sort weight of the word's first character.

The inverted index is partitioned into six auxiliary index tables to support parallel index creation. By default, two threads tokenize, sort, and insert words and associated data into the index tables. The number of threads that perform this work is configurable using the innodb\_ft\_sort\_pll\_degree variable. Consider increasing the number of threads when creating full-text indexes on large tables.

Auxiliary index table names are prefixed with fts\_ and postfixed with index\_#. Each auxiliary index table is associated with the indexed table by a hex value in the auxiliary index table name that matches the table\_id of the indexed table. For example, the table\_id of the test/opening\_lines table is 327, for which the hex value is 0x147. As shown in the preceding example, the "147" hex value

appears in the names of auxiliary index tables that are associated with the test/opening\_lines table.

A hex value representing the index\_id of the full-text index also appears in auxiliary index table names. For example, in the auxiliary table name test/ FTS\_0000000000000147\_00000000000001c9\_INDEX\_1, the hex value 1c9 has a decimal value of 457. The index defined on the opening\_lines table (idx) can be identified by querying the Information Schema INNODB\_SYS\_INDEXES table for this value (457).

```
mysql> SELECT index_id, name, table_id, space from INFORMATION_SCHEMA.INNODB_SYS_INDEXES
 WHERE index_id=457;
+----------+------+----------+-------+
| index_id | name | table_id | space |
+----------+------+----------+-------+
| 457 | idx | 327 | 283 |
+----------+------+----------+-------+
```

Index tables are stored in their own tablespace if the primary table is created in a file-per-table tablespace. Otherwise, index tables are stored in the tablespace where the indexed table resides.

The other index tables shown in the preceding example are referred to as common index tables and are used for deletion handling and storing the internal state of full-text indexes. Unlike the inverted index tables, which are created for each full-text index, this set of tables is common to all full-text indexes created on a particular table.

Common index tables are retained even if full-text indexes are dropped. When a full-text index is dropped, the FTS\_DOC\_ID column that was created for the index is retained, as removing the FTS\_DOC\_ID column would require rebuilding the previously indexed table. Common index tables are required to manage the FTS\_DOC\_ID column.

• FTS\_\*\_DELETED and FTS\_\*\_DELETED\_CACHE

Contain the document IDs (DOC\_ID) for documents that are deleted but whose data is not yet removed from the full-text index. The FTS\_\*\_DELETED\_CACHE is the in-memory version of the FTS\_\*\_DELETED table.

• FTS\_\*\_BEING\_DELETED and FTS\_\*\_BEING\_DELETED\_CACHE

Contain the document IDs (DOC\_ID) for documents that are deleted and whose data is currently in the process of being removed from the full-text index. The FTS\_\*\_BEING\_DELETED\_CACHE table is the in-memory version of the FTS\_\*\_BEING\_DELETED table.

• FTS\_\*\_CONFIG

Stores information about the internal state of the full-text index. Most importantly, it stores the FTS\_SYNCED\_DOC\_ID, which identifies documents that have been parsed and flushed to disk. In case of crash recovery, FTS\_SYNCED\_DOC\_ID values are used to identify documents that have not been flushed to disk so that the documents can be re-parsed and added back to the full-text index cache. To view the data in this table, query the Information Schema INNODB\_FT\_CONFIG table.

#### <span id="page-45-0"></span>**InnoDB Full-Text Index Cache**

When a document is inserted, it is tokenized, and the individual words and associated data are inserted into the full-text index. This process, even for small documents, can result in numerous small insertions into the auxiliary index tables, making concurrent access to these tables a point of contention. To avoid this problem, InnoDB uses a full-text index cache to temporarily cache index table insertions for recently inserted rows. This in-memory cache structure holds insertions until the cache is full and then batch flushes them to disk (to the auxiliary index tables). You can query the Information Schema INNODB\_FT\_INDEX\_CACHE table to view tokenized data for recently inserted rows.

The caching and batch flushing behavior avoids frequent updates to auxiliary index tables, which could result in concurrent access issues during busy insert and update times. The batching technique also avoids multiple insertions for the same word, and minimizes duplicate entries. Instead of flushing each word individually, insertions for the same word are merged and flushed to disk as a single entry, improving insertion efficiency while keeping auxiliary index tables as small as possible.

The innodb\_ft\_cache\_size variable is used to configure the full-text index cache size (on a per-table basis), which affects how often the full-text index cache is flushed. You can also define a global full-text index cache size limit for all tables in a given instance using the innodb\_ft\_total\_cache\_size variable.

The full-text index cache stores the same information as auxiliary index tables. However, the full-text index cache only caches tokenized data for recently inserted rows. The data that is already flushed to disk (to the auxiliary index tables) is not brought back into the full-text index cache when queried. The data in auxiliary index tables is queried directly, and results from the auxiliary index tables are merged with results from the full-text index cache before being returned.

### <span id="page-46-0"></span>**InnoDB Full-Text Index DOC\_ID and FTS\_DOC\_ID Column**

InnoDB uses a unique document identifier referred to as the DOC\_ID to map words in the full-text index to document records where the word appears. The mapping requires an FTS\_DOC\_ID column on the indexed table. If an FTS\_DOC\_ID column is not defined, InnoDB automatically adds a hidden FTS\_DOC\_ID column when the full-text index is created. The following example demonstrates this behavior.

The following table definition does not include an FTS\_DOC\_ID column:

```
mysql> CREATE TABLE opening_lines (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 opening_line TEXT(500),
 author VARCHAR(200),
 title VARCHAR(200)
 ) ENGINE=InnoDB;
```

When you create a full-text index on the table using CREATE FULLTEXT INDEX syntax, a warning is returned which reports that InnoDB is rebuilding the table to add the FTS\_DOC\_ID column.

```
mysql> CREATE FULLTEXT INDEX idx ON opening_lines(opening_line);
Query OK, 0 rows affected, 1 warning (0.19 sec)
Records: 0 Duplicates: 0 Warnings: 1
mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------+
| Level | Code | Message |
+---------+------+--------------------------------------------------+
| Warning | 124 | InnoDB rebuilding table to add column FTS_DOC_ID |
+---------+------+--------------------------------------------------+
```

The same warning is returned when using ALTER TABLE to add a full-text index to a table that does not have an FTS\_DOC\_ID column. If you create a full-text index at CREATE TABLE time and do not specify an FTS\_DOC\_ID column, InnoDB adds a hidden FTS\_DOC\_ID column, without warning.

Defining an FTS\_DOC\_ID column at CREATE TABLE time is less expensive than creating a full-text index on a table that is already loaded with data. If an FTS\_DOC\_ID column is defined on a table prior to loading data, the table and its indexes do not have to be rebuilt to add the new column. If you are not concerned with CREATE FULLTEXT INDEX performance, leave out the FTS\_DOC\_ID column to have InnoDB create it for you. InnoDB creates a hidden FTS\_DOC\_ID column along with a unique index (FTS\_DOC\_ID\_INDEX) on the FTS\_DOC\_ID column. If you want to create your own FTS\_DOC\_ID column, the column must be defined as BIGINT UNSIGNED NOT NULL and named FTS\_DOC\_ID (all uppercase), as in the following example:

![](_page_46_Picture_12.jpeg)

# **Note**

The FTS\_DOC\_ID column does not need to be defined as an AUTO\_INCREMENT column, but doing so could make loading data easier.

```
mysql> CREATE TABLE opening_lines (
 FTS_DOC_ID BIGINT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 opening_line TEXT(500),
 author VARCHAR(200),
 title VARCHAR(200)
 ) ENGINE=InnoDB;
```

If you choose to define the FTS\_DOC\_ID column yourself, you are responsible for managing the column to avoid empty or duplicate values. FTS\_DOC\_ID values cannot be reused, which means FTS\_DOC\_ID values must be ever increasing.

Optionally, you can create the required unique FTS\_DOC\_ID\_INDEX (all uppercase) on the FTS\_DOC\_ID column.

```
mysql> CREATE UNIQUE INDEX FTS_DOC_ID_INDEX on opening_lines(FTS_DOC_ID);
```

If you do not create the FTS\_DOC\_ID\_INDEX, InnoDB creates it automatically.

Before MySQL 5.7.13, the permitted gap between the largest used FTS\_DOC\_ID value and new FTS\_DOC\_ID value is 10000. In MySQL 5.7.13 and later, the permitted gap is 65535.

To avoid rebuilding the table, the FTS\_DOC\_ID column is retained when dropping a full-text index.

#### <span id="page-47-0"></span>**InnoDB Full-Text Index Deletion Handling**

Deleting a record that has a full-text index column could result in numerous small deletions in the auxiliary index tables, making concurrent access to these tables a point of contention. To avoid this problem, the DOC\_ID of a deleted document is logged in a special FTS\_\*\_DELETED table whenever a record is deleted from an indexed table, and the indexed record remains in the full-text index. Before returning query results, information in the FTS\_\*\_DELETED table is used to filter out deleted DOC\_IDs. The benefit of this design is that deletions are fast and inexpensive. The drawback is that the size of the index is not immediately reduced after deleting records. To remove full-text index entries for deleted records, run OPTIMIZE TABLE on the indexed table with innodb\_optimize\_fulltext\_only=ON to rebuild the full-text index. For more information, see Optimizing InnoDB Full-Text Indexes.

#### <span id="page-47-1"></span>**InnoDB Full-Text Index Transaction Handling**

InnoDB full-text indexes have special transaction handling characteristics due its caching and batch processing behavior. Specifically, updates and insertions on a full-text index are processed at transaction commit time, which means that a full-text search can only see committed data. The following example demonstrates this behavior. The full-text search only returns a result after the inserted lines are committed.

```
mysql> CREATE TABLE opening_lines (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 opening_line TEXT(500),
 author VARCHAR(200),
 title VARCHAR(200),
 FULLTEXT idx (opening_line)
 ) ENGINE=InnoDB;
mysql> BEGIN;
mysql> INSERT INTO opening_lines(opening_line,author,title) VALUES
 ('Call me Ishmael.','Herman Melville','Moby-Dick'),
 ('A screaming comes across the sky.','Thomas Pynchon','Gravity\'s Rainbow'),
 ('I am an invisible man.','Ralph Ellison','Invisible Man'),
 ('Where now? Who now? When now?','Samuel Beckett','The Unnamable'),
 ('It was love at first sight.','Joseph Heller','Catch-22'),
 ('All this happened, more or less.','Kurt Vonnegut','Slaughterhouse-Five'),
 ('Mrs. Dalloway said she would buy the flowers herself.','Virginia Woolf','Mrs. Dalloway'),
 ('It was a pleasure to burn.','Ray Bradbury','Fahrenheit 451');
mysql> SELECT COUNT(*) FROM opening_lines WHERE MATCH(opening_line) AGAINST('Ishmael');
+----------+
```

```
| COUNT(*) |
+----------+
| 0 |
+----------+
mysql> COMMIT;
mysql> SELECT COUNT(*) FROM opening_lines WHERE MATCH(opening_line) AGAINST('Ishmael');
+----------+
| COUNT(*) |
+----------+
| 1 |
+----------+
```

#### <span id="page-48-1"></span>**Monitoring InnoDB Full-Text Indexes**

You can monitor and examine the special text-processing aspects of InnoDB full-text indexes by querying the following INFORMATION\_SCHEMA tables:

```
• INNODB_FT_CONFIG
```

- INNODB\_FT\_INDEX\_TABLE
- INNODB\_FT\_INDEX\_CACHE
- INNODB\_FT\_DEFAULT\_STOPWORD
- INNODB\_FT\_DELETED
- INNODB\_FT\_BEING\_DELETED

You can also view basic information for full-text indexes and tables by querying INNODB\_SYS\_INDEXES and INNODB\_SYS\_TABLES.

For more information, see Section 14.16.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

# <span id="page-48-0"></span>**14.6.3 Tablespaces**

This section covers topics related to InnoDB tablespaces.