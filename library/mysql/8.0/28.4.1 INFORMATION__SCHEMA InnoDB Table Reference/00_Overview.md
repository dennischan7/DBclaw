---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following table summarizes INFORMATION\_SCHEMA InnoDB tables. For greater detail, see the individual table descriptions.

**Table 28.3 INFORMATION\_SCHEMA InnoDB Tables**

| Table Name                      | Description                                                                                    |
|---------------------------------|------------------------------------------------------------------------------------------------|
| INNODB_BUFFER_PAGE              | Pages in InnoDB buffer pool                                                                    |
| INNODB_BUFFER_PAGE_LRU          | LRU ordering of pages in InnoDB buffer pool                                                    |
| INNODB_BUFFER_POOL_STATS        | InnoDB buffer pool statistics                                                                  |
| INNODB_CACHED_INDEXES           | Number of index pages cached per index in<br>InnoDB buffer pool                                |
| INNODB_CMP                      | Status for operations related to compressed<br>InnoDB tables                                   |
| INNODB_CMP_PER_INDEX            | Status for operations related to compressed<br>InnoDB tables and indexes                       |
| INNODB_CMP_PER_INDEX_RESET      | Status for operations related to compressed<br>InnoDB tables and indexes                       |
| INNODB_CMP_RESET                | Status for operations related to compressed<br>InnoDB tables                                   |
| INNODB_CMPMEM                   | Status for compressed pages within InnoDB buffer<br>pool                                       |
| INNODB_CMPMEM_RESET             | Status for compressed pages within InnoDB buffer<br>pool                                       |
| INNODB_COLUMNS                  | Columns in each InnoDB table                                                                   |
| INNODB_DATAFILES                | Data file path information for InnoDB file-per-table<br>and general tablespaces                |
| INNODB_FIELDS                   | Key columns of InnoDB indexes                                                                  |
| INNODB_FOREIGN                  | InnoDB foreign-key metadata                                                                    |
| INNODB_FOREIGN_COLS             | InnoDB foreign-key column status information                                                   |
| INNODB_FT_BEING_DELETED         | Snapshot of INNODB_FT_DELETED table                                                            |
| INNODB_FT_CONFIG                | Metadata for InnoDB table FULLTEXT index and<br>associated processing                          |
| INNODB_FT_DEFAULT_STOPWORD      | Default list of stopwords for InnoDB FULLTEXT<br>indexes                                       |
| INNODB_FT_DELETED               | Rows deleted from InnoDB table FULLTEXT index                                                  |
| INNODB_FT_INDEX_CACHE           | Token information for newly inserted rows in<br>InnoDB FULLTEXT index                          |
| INNODB_FT_INDEX_TABLE           | Inverted index information for processing text<br>searches against InnoDB table FULLTEXT index |
| INNODB_INDEXES                  | InnoDB index metadata                                                                          |
| INNODB_METRICS                  | InnoDB performance information                                                                 |
| INNODB_SESSION_TEMP_TABLESPACES | Session temporary-tablespace metadata                                                          |
| INNODB_TABLES                   | InnoDB table metadata                                                                          |
| INNODB_TABLESPACES              | InnoDB file-per-table, general, and undo<br>tablespace metadata                                |
| INNODB_TABLESPACES_BRIEF        | Brief file-per-table, general, undo, and system<br>tablespace metadata                         |

| Table Name             | Description                                                      |
|------------------------|------------------------------------------------------------------|
| INNODB_TABLESTATS      | InnoDB table low-level status information                        |
| INNODB_TEMP_TABLE_INFO | Information about active user-created InnoDB<br>temporary tables |
| INNODB_TRX             | Active InnoDB transaction information                            |
| INNODB_VIRTUAL         | InnoDB virtual generated column metadata                         |

## <span id="page-61-0"></span>**28.4.2 The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE Table**

The [INNODB\\_BUFFER\\_PAGE](#page-61-0) table provides information about each page in the InnoDB buffer pool.

For related usage information and examples, see Section 17.15.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

![](_page_61_Picture_5.jpeg)

#### **Warning**

Querying the [INNODB\\_BUFFER\\_PAGE](#page-61-0) table can affect performance. Do not query this table on a production system unless you are aware of the performance impact and have determined it to be acceptable. To avoid impacting performance on a production system, reproduce the issue you want to investigate and query buffer pool statistics on a test instance.

The [INNODB\\_BUFFER\\_PAGE](#page-61-0) table has these columns:

• POOL\_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• BLOCK\_ID

The buffer pool block ID.

• SPACE

The tablespace ID; the same value as INNODB\_TABLES.SPACE.

• PAGE\_NUMBER

The page number.

• PAGE\_TYPE

The page type. The following table shows the permitted values.

**Table 28.4 INNODB\_BUFFER\_PAGE.PAGE\_TYPE Values**

| Page Type            | Description                |
|----------------------|----------------------------|
| ALLOCATED            | Freshly allocated page     |
| BLOB                 | Uncompressed BLOB page     |
| COMPRESSED_BLOB2     | Subsequent comp BLOB page  |
| COMPRESSED_BLOB      | First compressed BLOB page |
| ENCRYPTED_RTREE      | Encrypted R-tree           |
| EXTENT_DESCRIPTOR    | Extent descriptor page     |
| FILE_SPACE_HEADER    | File space header          |
| FIL_PAGE_TYPE_UNUSED | Unused                     |
| IBUF_BITMAP          | Insert buffer bitmap       |

| Page Type                    | Description                    |
|------------------------------|--------------------------------|
| IBUF_FREE_LIST               | Insert buffer free list        |
| IBUF_INDEX                   | Insert buffer index            |
| INDEX                        | B-tree node                    |
| INODE                        | Index node                     |
| LOB_DATA                     | Uncompressed LOB data          |
| LOB_FIRST                    | First page of uncompressed LOB |
| LOB_INDEX                    | Uncompressed LOB index         |
| PAGE_IO_COMPRESSED           | Compressed page                |
| PAGE_IO_COMPRESSED_ENCRYPTED | Compressed and encrypted page  |
| PAGE_IO_ENCRYPTED            | Encrypted page                 |
| RSEG_ARRAY                   | Rollback segment array         |
| RTREE_INDEX                  | R-tree index                   |
| SDI_BLOB                     | Uncompressed SDI BLOB          |
| SDI_COMPRESSED_BLOB          | Compressed SDI BLOB            |
| SDI_INDEX                    | SDI index                      |
| SYSTEM                       | System page                    |
| TRX_SYSTEM                   | Transaction system data        |
| UNDO_LOG                     | Undo log page                  |
| UNKNOWN                      | Unknown                        |
| ZLOB_DATA                    | Compressed LOB data            |
| ZLOB_FIRST                   | First page of compressed LOB   |
| ZLOB_FRAG                    | Compressed LOB fragment        |
| ZLOB_FRAG_ENTRY              | Compressed LOB fragment index  |
| ZLOB_INDEX                   | Compressed LOB index           |

• FLUSH\_TYPE

The flush type.

• FIX\_COUNT

The number of threads using this block within the buffer pool. When zero, the block is eligible to be evicted.

• IS\_HASHED

Whether a hash index has been built on this page.

• NEWEST\_MODIFICATION

The Log Sequence Number of the youngest modification.

• OLDEST\_MODIFICATION

The Log Sequence Number of the oldest modification.

• ACCESS\_TIME

An abstract number used to judge the first access time of the page.

• TABLE\_NAME

The name of the table the page belongs to. This column is applicable only to pages with a PAGE\_TYPE value of INDEX. The column is NULL if the server has not yet accessed the table.

• INDEX\_NAME

The name of the index the page belongs to. This can be the name of a clustered index or a secondary index. This column is applicable only to pages with a PAGE\_TYPE value of INDEX.

• NUMBER\_RECORDS

The number of records within the page.

• DATA\_SIZE

The sum of the sizes of the records. This column is applicable only to pages with a PAGE\_TYPE value of INDEX.

• COMPRESSED\_SIZE

The compressed page size. NULL for pages that are not compressed.

• PAGE\_STATE

The page state. The following table shows the permitted values.

#### **Table 28.5 INNODB\_BUFFER\_PAGE.PAGE\_STATE Values**

| Page State    | Description                                                                                                 |
|---------------|-------------------------------------------------------------------------------------------------------------|
| FILE_PAGE     | A buffered file page                                                                                        |
| MEMORY        | Contains a main memory object                                                                               |
| NOT_USED      | In the free list                                                                                            |
| NULL          | Clean compressed pages, compressed pages<br>in the flush list, pages used as buffer pool watch<br>sentinels |
| READY_FOR_USE | A free page                                                                                                 |
| REMOVE_HASH   | Hash index should be removed before placing in<br>the free list                                             |

• IO\_FIX

Whether any I/O is pending for this page: IO\_NONE = no pending I/O, IO\_READ = read pending, IO\_WRITE = write pending, IO\_PIN = relocation and removal from the flush not permitted.

• IS\_OLD

Whether the block is in the sublist of old blocks in the LRU list.

• FREE\_PAGE\_CLOCK

The value of the freed\_page\_clock counter when the block was the last placed at the head of the LRU list. The freed\_page\_clock counter tracks the number of blocks removed from the end of the LRU list.

• IS\_STALE

Whether the page is stale. Added in MySQL 8.0.24.

### **Example**

mysql> **SELECT \* FROM INFORMATION\_SCHEMA.INNODB\_BUFFER\_PAGE LIMIT 1\G**

```
*************************** 1. row ***************************
 POOL_ID: 0
 BLOCK_ID: 0
 SPACE: 97
 PAGE_NUMBER: 2473
 PAGE_TYPE: INDEX
 FLUSH_TYPE: 1
 FIX_COUNT: 0
 IS_HASHED: YES
NEWEST_MODIFICATION: 733855581
OLDEST_MODIFICATION: 0
 ACCESS_TIME: 3378385672
 TABLE_NAME: `employees`.`salaries`
 INDEX_NAME: PRIMARY
 NUMBER_RECORDS: 468
 DATA_SIZE: 14976
 COMPRESSED_SIZE: 0
 PAGE_STATE: FILE_PAGE
 IO_FIX: IO_NONE
 IS_OLD: YES
 FREE_PAGE_CLOCK: 66
 IS_STALE: NO
```

## **Notes**

- This table is useful primarily for expert-level performance monitoring, or when developing performance-related extensions for MySQL.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- When tables, table rows, partitions, or indexes are deleted, associated pages remain in the buffer pool until space is required for other data. The [INNODB\\_BUFFER\\_PAGE](#page-61-0) table reports information about these pages until they are evicted from the buffer pool. For more information about how the InnoDB manages buffer pool data, see Section 17.5.1, "Buffer Pool".

# <span id="page-64-0"></span>**28.4.3 The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE\_LRU Table**

The [INNODB\\_BUFFER\\_PAGE\\_LRU](#page-64-0) table provides information about the pages in the InnoDB buffer pool; in particular, how they are ordered in the LRU list that determines which pages to evict from the buffer pool when it becomes full.

The [INNODB\\_BUFFER\\_PAGE\\_LRU](#page-64-0) table has the same columns as the [INNODB\\_BUFFER\\_PAGE](#page-61-0) table with a few exceptions. It has LRU\_POSITION and COMPRESSED columns instead of BLOCK\_ID and PAGE\_STATE columns, and it does not include and IS\_STALE column.

For related usage information and examples, see Section 17.15.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

![](_page_64_Picture_11.jpeg)

### **Warning**

Querying the [INNODB\\_BUFFER\\_PAGE\\_LRU](#page-64-0) table can affect performance. Do not query this table on a production system unless you are aware of the performance impact and have determined it to be acceptable. To avoid impacting performance on a production system, reproduce the issue you want to investigate and query buffer pool statistics on a test instance.

The [INNODB\\_BUFFER\\_PAGE\\_LRU](#page-64-0) table has these columns:

• POOL\_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• LRU\_POSITION

The position of the page in the LRU list.

• SPACE

The tablespace ID; the same value as INNODB\_TABLES.SPACE.

• PAGE\_NUMBER

The page number.

• PAGE\_TYPE

The page type. The following table shows the permitted values.

### **Table 28.6 INNODB\_BUFFER\_PAGE\_LRU.PAGE\_TYPE Values**

| Page Type                    | Description                    |
|------------------------------|--------------------------------|
| ALLOCATED                    | Freshly allocated page         |
| BLOB                         | Uncompressed BLOB page         |
| COMPRESSED_BLOB2             | Subsequent comp BLOB page      |
| COMPRESSED_BLOB              | First compressed BLOB page     |
| ENCRYPTED_RTREE              | Encrypted R-tree               |
| EXTENT_DESCRIPTOR            | Extent descriptor page         |
| FILE_SPACE_HEADER            | File space header              |
| FIL_PAGE_TYPE_UNUSED         | Unused                         |
| IBUF_BITMAP                  | Insert buffer bitmap           |
| IBUF_FREE_LIST               | Insert buffer free list        |
| IBUF_INDEX                   | Insert buffer index            |
| INDEX                        | B-tree node                    |
| INODE                        | Index node                     |
| LOB_DATA                     | Uncompressed LOB data          |
| LOB_FIRST                    | First page of uncompressed LOB |
| LOB_INDEX                    | Uncompressed LOB index         |
| PAGE_IO_COMPRESSED           | Compressed page                |
| PAGE_IO_COMPRESSED_ENCRYPTED | Compressed and encrypted page  |
| PAGE_IO_ENCRYPTED            | Encrypted page                 |
| RSEG_ARRAY                   | Rollback segment array         |
| RTREE_INDEX                  | R-tree index                   |
| SDI_BLOB                     | Uncompressed SDI BLOB          |
| SDI_COMPRESSED_BLOB          | Compressed SDI BLOB            |
| SDI_INDEX                    | SDI index                      |
| SYSTEM                       | System page                    |
| TRX_SYSTEM                   | Transaction system data        |
| UNDO_LOG                     | Undo log page                  |
| UNKNOWN                      | Unknown                        |
| ZLOB_DATA                    | Compressed LOB data            |
| ZLOB_FIRST                   | First page of compressed LOB   |

| Page Type       | Description                   |
|-----------------|-------------------------------|
| ZLOB_FRAG       | Compressed LOB fragment       |
| ZLOB_FRAG_ENTRY | Compressed LOB fragment index |
| ZLOB_INDEX      | Compressed LOB index          |

• FLUSH\_TYPE

The flush type.

• FIX\_COUNT

The number of threads using this block within the buffer pool. When zero, the block is eligible to be evicted.

• IS\_HASHED

Whether a hash index has been built on this page.

• NEWEST\_MODIFICATION

The Log Sequence Number of the youngest modification.

• OLDEST\_MODIFICATION

The Log Sequence Number of the oldest modification.

• ACCESS\_TIME

An abstract number used to judge the first access time of the page.

• TABLE\_NAME

The name of the table the page belongs to. This column is applicable only to pages with a PAGE\_TYPE value of INDEX. The column is NULL if the server has not yet accessed the table.

• INDEX\_NAME

The name of the index the page belongs to. This can be the name of a clustered index or a secondary index. This column is applicable only to pages with a PAGE\_TYPE value of INDEX.

• NUMBER\_RECORDS

The number of records within the page.

• DATA\_SIZE

The sum of the sizes of the records. This column is applicable only to pages with a PAGE\_TYPE value of INDEX.

• COMPRESSED\_SIZE

The compressed page size. NULL for pages that are not compressed.

• COMPRESSED

Whether the page is compressed.

• IO\_FIX

Whether any I/O is pending for this page: IO\_NONE = no pending I/O, IO\_READ = read pending, IO\_WRITE = write pending.

• IS\_OLD

Whether the block is in the sublist of old blocks in the LRU list.

• FREE\_PAGE\_CLOCK

The value of the freed\_page\_clock counter when the block was the last placed at the head of the LRU list. The freed\_page\_clock counter tracks the number of blocks removed from the end of the LRU list.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU LIMIT 1\G
*************************** 1. row ***************************
 POOL_ID: 0
 LRU_POSITION: 0
 SPACE: 97
 PAGE_NUMBER: 1984
 PAGE_TYPE: INDEX
 FLUSH_TYPE: 1
 FIX_COUNT: 0
 IS_HASHED: YES
NEWEST_MODIFICATION: 719490396
OLDEST_MODIFICATION: 0
 ACCESS_TIME: 3378383796
 TABLE_NAME: `employees`.`salaries`
 INDEX_NAME: PRIMARY
 NUMBER_RECORDS: 468
 DATA_SIZE: 14976
 COMPRESSED_SIZE: 0
 COMPRESSED: NO
 IO_FIX: IO_NONE
 IS_OLD: YES
 FREE_PAGE_CLOCK: 0
```

### **Notes**

- This table is useful primarily for expert-level performance monitoring, or when developing performance-related extensions for MySQL.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- Querying this table can require MySQL to allocate a large block of contiguous memory, more than 64 bytes times the number of active pages in the buffer pool. This allocation could potentially cause an out-of-memory error, especially for systems with multi-gigabyte buffer pools.
- Querying this table requires MySQL to lock the data structure representing the buffer pool while traversing the LRU list, which can reduce concurrency, especially for systems with multi-gigabyte buffer pools.
- When tables, table rows, partitions, or indexes are deleted, associated pages remain in the buffer pool until space is required for other data. The [INNODB\\_BUFFER\\_PAGE\\_LRU](#page-64-0) table reports information about these pages until they are evicted from the buffer pool. For more information about how the InnoDB manages buffer pool data, see Section 17.5.1, "Buffer Pool".

# <span id="page-67-0"></span>**28.4.4 The INFORMATION\_SCHEMA INNODB\_BUFFER\_POOL\_STATS Table**

The [INNODB\\_BUFFER\\_POOL\\_STATS](#page-67-0) table provides much of the same buffer pool information provided in SHOW ENGINE INNODB STATUS output. Much of the same information may also be obtained using InnoDB buffer pool server status variables.

The idea of making pages in the buffer pool "young" or "not young" refers to transferring them between the sublists at the head and tail of the buffer pool data structure. Pages made "young" take longer

to age out of the buffer pool, while pages made "not young" are moved much closer to the point of eviction.

For related usage information and examples, see Section 17.15.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

The [INNODB\\_BUFFER\\_POOL\\_STATS](#page-67-0) table has these columns:

• POOL\_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• POOL\_SIZE

The InnoDB buffer pool size in pages.

• FREE\_BUFFERS

The number of free pages in the InnoDB buffer pool.

• DATABASE\_PAGES

The number of pages in the InnoDB buffer pool containing data. This number includes both dirty and clean pages.

• OLD\_DATABASE\_PAGES

The number of pages in the old buffer pool sublist.

• MODIFIED\_DATABASE\_PAGES

The number of modified (dirty) database pages.

• PENDING\_DECOMPRESS

The number of pages pending decompression.

• PENDING\_READS

The number of pending reads.

• PENDING\_FLUSH\_LRU

The number of pages pending flush in the LRU.

• PENDING\_FLUSH\_LIST

The number of pages pending flush in the flush list.

• PAGES\_MADE\_YOUNG

The number of pages made young.

• PAGES\_NOT\_MADE\_YOUNG

The number of pages not made young.

• PAGES\_MADE\_YOUNG\_RATE

The number of pages made young per second (pages made young since the last printout / time elapsed).

• PAGES\_MADE\_NOT\_YOUNG\_RATE

The number of pages not made per second (pages not made young since the last printout / time elapsed).

• NUMBER\_PAGES\_READ

The number of pages read.

• NUMBER\_PAGES\_CREATED

The number of pages created.

• NUMBER\_PAGES\_WRITTEN

The number of pages written.

• PAGES\_READ\_RATE

The number of pages read per second (pages read since the last printout / time elapsed).

• PAGES\_CREATE\_RATE

The number of pages created per second (pages created since the last printout / time elapsed).

• PAGES\_WRITTEN\_RATE

The number of pages written per second (pages written since the last printout / time elapsed).

• NUMBER\_PAGES\_GET

The number of logical read requests.

• HIT\_RATE

The buffer pool hit rate.

• YOUNG\_MAKE\_PER\_THOUSAND\_GETS

The number of pages made young per thousand gets.

• NOT\_YOUNG\_MAKE\_PER\_THOUSAND\_GETS

The number of pages not made young per thousand gets.

• NUMBER\_PAGES\_READ\_AHEAD

The number of pages read ahead.

• NUMBER\_READ\_AHEAD\_EVICTED

The number of pages read into the InnoDB buffer pool by the read-ahead background thread that were subsequently evicted without having been accessed by queries.

• READ\_AHEAD\_RATE

The read-ahead rate per second (pages read ahead since the last printout / time elapsed).

• READ\_AHEAD\_EVICTED\_RATE

The number of read-ahead pages evicted without access per second (read-ahead pages not accessed since the last printout / time elapsed).

• LRU\_IO\_TOTAL

Total LRU I/O.

• LRU\_IO\_CURRENT

LRU I/O for the current interval.

• UNCOMPRESS\_TOTAL

The total number of pages decompressed.

• UNCOMPRESS\_CURRENT

The number of pages decompressed in the current interval.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_POOL_STATS\G
*************************** 1. row ***************************
 POOL_ID: 0
 POOL_SIZE: 8192
 FREE_BUFFERS: 1
 DATABASE_PAGES: 8085
 OLD_DATABASE_PAGES: 2964
 MODIFIED_DATABASE_PAGES: 0
 PENDING_DECOMPRESS: 0
 PENDING_READS: 0
 PENDING_FLUSH_LRU: 0
 PENDING_FLUSH_LIST: 0
 PAGES_MADE_YOUNG: 22821
 PAGES_NOT_MADE_YOUNG: 3544303
 PAGES_MADE_YOUNG_RATE: 357.62602199870594
 PAGES_MADE_NOT_YOUNG_RATE: 0
 NUMBER_PAGES_READ: 2389
 NUMBER_PAGES_CREATED: 12385
 NUMBER_PAGES_WRITTEN: 13111
 PAGES_READ_RATE: 0
 PAGES_CREATE_RATE: 0
 PAGES_WRITTEN_RATE: 0
 NUMBER_PAGES_GET: 33322210
 HIT_RATE: 1000
 YOUNG_MAKE_PER_THOUSAND_GETS: 18
NOT_YOUNG_MAKE_PER_THOUSAND_GETS: 0
 NUMBER_PAGES_READ_AHEAD: 2024
 NUMBER_READ_AHEAD_EVICTED: 0
 READ_AHEAD_RATE: 0
 READ_AHEAD_EVICTED_RATE: 0
 LRU_IO_TOTAL: 0
 LRU_IO_CURRENT: 0
 UNCOMPRESS_TOTAL: 0
 UNCOMPRESS_CURRENT: 0
```

### **Notes**

- This table is useful primarily for expert-level performance monitoring, or when developing performance-related extensions for MySQL.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-70-0"></span>**28.4.5 The INFORMATION\_SCHEMA INNODB\_CACHED\_INDEXES Table**

The [INNODB\\_CACHED\\_INDEXES](#page-70-0) table reports the number of index pages cached in the InnoDB buffer pool for each index.

For related usage information and examples, see Section 17.15.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

The [INNODB\\_CACHED\\_INDEXES](#page-70-0) table has these columns:

• SPACE\_ID

The tablespace ID.

• INDEX\_ID

An identifier for the index. Index identifiers are unique across all the databases in an instance.

• N\_CACHED\_PAGES

The total number of index pages cached in the InnoDB buffer pool for a specific index since MySQL Server last started.

## **Examples**

This query returns the number of index pages cached in the InnoDB buffer pool for a specific index:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_CACHED_INDEXES WHERE INDEX_ID=65\G
*************************** 1. row ***************************
 SPACE_ID: 4294967294
 INDEX_ID: 65
N_CACHED_PAGES: 45
```

This query returns the number of index pages cached in the InnoDB buffer pool for each index, using the [INNODB\\_INDEXES](#page-86-0) and [INNODB\\_TABLES](#page-90-0) tables to resolve the table name and index name for each INDEX\_ID value.

```
SELECT
 tables.NAME AS table_name,
 indexes.NAME AS index_name,
 cached.N_CACHED_PAGES AS n_cached_pages
FROM
 INFORMATION_SCHEMA.INNODB_CACHED_INDEXES AS cached,
 INFORMATION_SCHEMA.INNODB_INDEXES AS indexes,
 INFORMATION_SCHEMA.INNODB_TABLES AS tables
WHERE
 cached.INDEX_ID = indexes.INDEX_ID
 AND indexes.TABLE_ID = tables.TABLE_ID;
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-71-0"></span>**28.4.6 The INFORMATION\_SCHEMA INNODB\_CMP and INNODB\_CMP\_RESET Tables**

The [INNODB\\_CMP](#page-71-0) and [INNODB\\_CMP\\_RESET](#page-71-0) tables provide status information on operations related to compressed InnoDB tables.

The [INNODB\\_CMP](#page-71-0) and [INNODB\\_CMP\\_RESET](#page-71-0) tables have these columns:

• PAGE\_SIZE

The compressed page size in bytes.

• COMPRESS\_OPS

The number of times a B-tree page of size PAGE\_SIZE has been compressed. Pages are compressed whenever an empty page is created or the space for the uncompressed modification log runs out.

• COMPRESS\_OPS\_OK

The number of times a B-tree page of size PAGE\_SIZE has been successfully compressed. This count should never exceed COMPRESS OPS.

• COMPRESS TIME

The total time in seconds used for attempts to compress B-tree pages of size PAGE SIZE.

• UNCOMPRESS OPS

The number of times a B-tree page of size PAGE\_SIZE has been uncompressed. B-tree pages are uncompressed whenever compression fails or at first access when the uncompressed page does not exist in the buffer pool.

• UNCOMPRESS TIME

The total time in seconds used for uncompressing B-tree pages of the size PAGE SIZE.

### **Example**

```
mysql> SELECT * FROM INFORMATION SCHEMA.INNODB CMP\G
            ************ 1. row ********
    page size: 1024
  compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress ops: 0
uncompress time: 0
          .
*********** 2. row *****************
    page size: 2048
 compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress ops: 0
uncompress time: 0
          ************* 3. row ****************
    page size: 4096
 compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress ops: 0
uncompress time: 0
                 ****** 4. row **************
    page_size: 8192
 compress ops: 86955
compress_ops_ok: 81182
 compress time: 27
uncompress ops: 26828
uncompress time: 5
*******
                 ****** 5. row ***************
    page_size: 16384
 compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress ops: 0
uncompress time: 0
```

### **Notes**

- Use these tables to measure the effectiveness of InnoDB table compression in your database.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For usage information, see Section 17.9.1.4, "Monitoring InnoDB Table Compression at Runtime" and Section 17.15.1.3, "Using the Compression Information Schema Tables". For general

information about InnoDB table compression, see Section 17.9, "InnoDB Table and Page Compression".

## <span id="page-73-0"></span>**28.4.7 The INFORMATION\_SCHEMA INNODB\_CMPMEM and INNODB\_CMPMEM\_RESET Tables**

The [INNODB\\_CMPMEM](#page-73-0) and [INNODB\\_CMPMEM\\_RESET](#page-73-0) tables provide status information on compressed pages within the InnoDB buffer pool.

The [INNODB\\_CMPMEM](#page-73-0) and [INNODB\\_CMPMEM\\_RESET](#page-73-0) tables have these columns:

• PAGE\_SIZE

The block size in bytes. Each record of this table describes blocks of this size.

• BUFFER\_POOL\_INSTANCE

A unique identifier for the buffer pool instance.

• PAGES\_USED

The number of blocks of size PAGE\_SIZE that are currently in use.

• PAGES\_FREE

The number of blocks of size PAGE\_SIZE that are currently available for allocation. This column shows the external fragmentation in the memory pool. Ideally, these numbers should be at most 1.

• RELOCATION\_OPS

The number of times a block of size PAGE\_SIZE has been relocated. The buddy system can relocate the allocated "buddy neighbor" of a freed block when it tries to form a bigger freed block. Reading from the [INNODB\\_CMPMEM\\_RESET](#page-73-0) table resets this count.

• RELOCATION\_TIME

The total time in microseconds used for relocating blocks of size PAGE\_SIZE. Reading from the table INNODB\_CMPMEM\_RESET resets this count.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_CMPMEM\G
*************************** 1. row ***************************
 page_size: 1024
buffer_pool_instance: 0
 pages_used: 0
 pages_free: 0
 relocation_ops: 0
 relocation_time: 0
*************************** 2. row ***************************
 page_size: 2048
buffer_pool_instance: 0
 pages_used: 0
 pages_free: 0
 relocation_ops: 0
 relocation_time: 0
*************************** 3. row ***************************
 page_size: 4096
buffer_pool_instance: 0
 pages_used: 0
 pages_free: 0
 relocation_ops: 0
 relocation_time: 0
*************************** 4. row ***************************
 page_size: 8192
```

```
buffer_pool_instance: 0
 pages_used: 7673
 pages_free: 15
 relocation_ops: 4638
 relocation_time: 0
*************************** 5. row ***************************
 page_size: 16384
buffer_pool_instance: 0
 pages_used: 0
 pages_free: 0
 relocation_ops: 0
 relocation_time: 0
```

## **Notes**

- Use these tables to measure the effectiveness of InnoDB table compression in your database.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For usage information, see Section 17.9.1.4, "Monitoring InnoDB Table Compression at Runtime" and Section 17.15.1.3, "Using the Compression Information Schema Tables". For general information about InnoDB table compression, see Section 17.9, "InnoDB Table and Page Compression".

# <span id="page-74-0"></span>**28.4.8 The INFORMATION\_SCHEMA INNODB\_CMP\_PER\_INDEX and INNODB\_CMP\_PER\_INDEX\_RESET Tables**

The [INNODB\\_CMP\\_PER\\_INDEX](#page-74-0) and [INNODB\\_CMP\\_PER\\_INDEX\\_RESET](#page-74-0) tables provide status information on operations related to compressed InnoDB tables and indexes, with separate statistics for each combination of database, table, and index, to help you evaluate the performance and usefulness of compression for specific tables.

For a compressed InnoDB table, both the table data and all the secondary indexes are compressed. In this context, the table data is treated as just another index, one that happens to contain all the columns: the clustered index.

The [INNODB\\_CMP\\_PER\\_INDEX](#page-74-0) and [INNODB\\_CMP\\_PER\\_INDEX\\_RESET](#page-74-0) tables have these columns:

• DATABASE\_NAME

The schema (database) containing the applicable table.

• TABLE\_NAME

The table to monitor for compression statistics.

• INDEX\_NAME

The index to monitor for compression statistics.

• COMPRESS\_OPS

The number of compression operations attempted. Pages are compressed whenever an empty page is created or the space for the uncompressed modification log runs out.

• COMPRESS\_OPS\_OK

The number of successful compression operations. Subtract from the COMPRESS\_OPS value to get the number of compression failures. Divide by the COMPRESS\_OPS value to get the percentage of compression failures.

• COMPRESS TIME

The total time in seconds used for compressing data in this index.

• UNCOMPRESS OPS

The number of uncompression operations performed. Compressed InnoDB pages are uncompressed whenever compression fails, or the first time a compressed page is accessed in the buffer pool and the uncompressed page does not exist.

• UNCOMPRESS TIME

The total time in seconds used for uncompressing data in this index.

### **Example**

```
mysql> SELECT * FROM INFORMATION SCHEMA.INNODB CMP PER INDEX\G
                ****** 1. row **
 database name: employees
    table_name: salaries
    index name: PRIMARY
  compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress_ops: 23451
uncompress time: 4
                   ***** 2. row ***************
 database name: employees
    table name: salaries
    index name: emp no
  compress ops: 0
compress ops ok: 0
 compress time: 0
uncompress ops: 1597
uncompress time: 0
```

#### **Notes**

- Use these tables to measure the effectiveness of Innobe table compression for specific tables, indexes, or both.
- You must have the PROCESS privilege to query these tables.
- Use the INFORMATION\_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional information about the columns of these tables, including data types and default values.
- Because collecting separate measurements for every index imposes substantial performance overhead, INNODB\_CMP\_PER\_INDEX and INNODB\_CMP\_PER\_INDEX\_RESET statistics are not gathered by default. You must enable the innodb\_cmp\_per\_index\_enabled system variable before performing the operations on compressed tables that you want to monitor.
- For usage information, see Section 17.9.1.4, "Monitoring InnoDB Table Compression at Runtime" and Section 17.15.1.3, "Using the Compression Information Schema Tables". For general information about InnoDB table compression, see Section 17.9, "InnoDB Table and Page Compression".

# <span id="page-75-0"></span>28.4.9 The INFORMATION\_SCHEMA INNODB\_COLUMNS Table

The INNODE COLUMNS table provides metadata about InnoDE table columns.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The INNODB COLUMNS table has these columns:

### • TABLE\_ID

An identifier representing the table associated with the column; the same value as INNODB\_TABLES.TABLE\_ID.

### • NAME

The name of the column. These names can be uppercase or lowercase depending on the lower\_case\_table\_names setting. There are no special system-reserved names for columns.

### • POS

The ordinal position of the column within the table, starting from 0 and incrementing sequentially. When a column is dropped, the remaining columns are reordered so that the sequence has no gaps. The POS value for a virtual generated column encodes the column sequence number and ordinal position of the column. For more information, see the POS column description in [Section 28.4.29,](#page-100-0) ["The INFORMATION\\_SCHEMA INNODB\\_VIRTUAL Table"](#page-100-0).

### • MTYPE

Stands for "main type". A numeric identifier for the column type. 1 = VARCHAR, 2 = CHAR, 3 = FIXBINARY, 4 = BINARY, 5 = BLOB, 6 = INT, 7 = SYS\_CHILD, 8 = SYS, 9 = FLOAT, 10 = DOUBLE, 11 = DECIMAL, 12 = VARMYSQL, 13 = MYSQL, 14 = GEOMETRY.

### • PRTYPE

The InnoDB "precise type", a binary value with bits representing MySQL data type, character set code, and nullability.

### • LEN

The column length, for example 4 for INT and 8 for BIGINT. For character columns in multibyte character sets, this length value is the maximum length in bytes needed to represent a definition such as VARCHAR(N); that is, it might be 2\*N, 3\*N, and so on depending on the character encoding.

### • HAS\_DEFAULT

A boolean value indicating whether a column that was added instantly using ALTER TABLE ... ADD COLUMN with ALGORITHM=INSTANT has a default value. All columns added instantly have a default value, which makes this column an indicator of whether the column was added instantly.

## • DEFAULT\_VALUE

The initial default value of a column that was added instantly using ALTER TABLE ... ADD COLUMN with ALGORITHM=INSTANT. If the default value is NULL or was not specified, this column reports NULL. An explicitly specified non-NULL default value is shown in an internal binary format. Subsequent modifications of the column default value do not change the value reported by this column.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_COLUMNS where TABLE_ID = 71\G
*************************** 1. row ***************************
 TABLE_ID: 71
 NAME: col1
 POS: 0
 MTYPE: 6
 PRTYPE: 1027
 LEN: 4
 HAS_DEFAULT: 0
DEFAULT_VALUE: NULL
*************************** 2. row ***************************
 TABLE_ID: 71
 NAME: col2
```

```
 POS: 1
 MTYPE: 2
 PRTYPE: 524542
 LEN: 10
 HAS_DEFAULT: 0
DEFAULT_VALUE: NULL
*************************** 3. row ***************************
 TABLE_ID: 71
 NAME: col3
 POS: 2
 MTYPE: 1
 PRTYPE: 524303
 LEN: 10
 HAS_DEFAULT: 0
DEFAULT_VALUE: NULL
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-77-0"></span>**28.4.10 The INFORMATION\_SCHEMA INNODB\_DATAFILES Table**

The [INNODB\\_DATAFILES](#page-77-0) table provides data file path information for InnoDB file-per-table and general tablespaces.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

![](_page_77_Picture_8.jpeg)

### **Note**

The INFORMATION\_SCHEMA [FILES](#page-14-0) table reports metadata for InnoDB tablespace types including file-per-table tablespaces, general tablespaces, the system tablespace, the global temporary tablespace, and undo tablespaces.

The [INNODB\\_DATAFILES](#page-77-0) table has these columns:

• SPACE

The tablespace ID.

• PATH

The tablespace data file path. If a file-per-table tablespace is created in a location outside the MySQL data directory, the path value is a fully qualified directory path. Otherwise, the path is relative to the data directory.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_DATAFILES WHERE SPACE = 57\G
*************************** 1. row ***************************
SPACE: 57
 PATH: ./test/t1.ibd
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-77-1"></span>**28.4.11 The INFORMATION\_SCHEMA INNODB\_FIELDS Table**

The [INNODB\\_FIELDS](#page-77-1) table provides metadata about the key columns (fields) of InnoDB indexes.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_FIELDS](#page-77-1) table has these columns:

• INDEX\_ID

An identifier for the index associated with this key field; the same value as INNODB\_INDEXES.INDEX\_ID.

• NAME

The name of the original column from the table; the same value as INNODB\_COLUMNS.NAME.

• POS

The ordinal position of the key field within the index, starting from 0 and incrementing sequentially. When a column is dropped, the remaining columns are reordered so that the sequence has no gaps.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FIELDS WHERE INDEX_ID = 117\G
*************************** 1. row ***************************
INDEX_ID: 117
 NAME: col1
 POS: 0
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-78-0"></span>**28.4.12 The INFORMATION\_SCHEMA INNODB\_FOREIGN Table**

The [INNODB\\_FOREIGN](#page-78-0) table provides metadata about InnoDB foreign keys.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_FOREIGN](#page-78-0) table has these columns:

• ID

The name (not a numeric value) of the foreign key index, preceded by the schema (database) name (for example, test/products\_fk).

• FOR\_NAME

The name of the child table in this foreign key relationship.

• REF\_NAME

The name of the parent table in this foreign key relationship.

• N\_COLS

The number of columns in the foreign key index.

• TYPE

A collection of bit flags with information about the foreign key column, ORed together. 0 = ON DELETE/UPDATE RESTRICT, 1 = ON DELETE CASCADE, 2 = ON DELETE SET NULL, 4 = ON UPDATE CASCADE, 8 = ON UPDATE SET NULL, 16 = ON DELETE NO ACTION, 32 = ON UPDATE NO ACTION.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FOREIGN\G
*************************** 1. row ***************************
 ID: test/fk1
FOR_NAME: test/child
REF_NAME: test/parent
 N_COLS: 1
 TYPE: 1
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-79-0"></span>**28.4.13 The INFORMATION\_SCHEMA INNODB\_FOREIGN\_COLS Table**

The [INNODB\\_FOREIGN\\_COLS](#page-79-0) table provides status information about InnoDB foreign key columns.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_FOREIGN\\_COLS](#page-79-0) table has these columns:

• ID

The foreign key index associated with this index key field; the same value as INNODB\_FOREIGN.ID.

• FOR\_COL\_NAME

The name of the associated column in the child table.

• REF\_COL\_NAME

The name of the associated column in the parent table.

• POS

The ordinal position of this key field within the foreign key index, starting from 0.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FOREIGN_COLS WHERE ID = 'test/fk1'\G
*************************** 1. row ***************************
 ID: test/fk1
FOR_COL_NAME: parent_id
REF_COL_NAME: id
 POS: 0
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-79-1"></span>**28.4.14 The INFORMATION\_SCHEMA INNODB\_FT\_BEING\_DELETED Table**

The [INNODB\\_FT\\_BEING\\_DELETED](#page-79-1) table provides a snapshot of the [INNODB\\_FT\\_DELETED](#page-82-0) table; it is used only during an OPTIMIZE TABLE maintenance operation. When OPTIMIZE TABLE is run, the [INNODB\\_FT\\_BEING\\_DELETED](#page-79-1) table is emptied, and DOC\_ID values are removed from the [INNODB\\_FT\\_DELETED](#page-82-0) table. Because the contents of [INNODB\\_FT\\_BEING\\_DELETED](#page-79-1) typically have a short lifetime, this table has limited utility for monitoring or debugging. For information about running OPTIMIZE TABLE on tables with FULLTEXT indexes, see Section 14.9.6, "Fine-Tuning MySQL Full-Text Search".

This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles). The output appears similar to the example provided for the [INNODB\\_FT\\_DELETED](#page-82-0) table.

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_BEING\\_DELETED](#page-79-1) table has these columns:

• DOC\_ID

The document ID of the row that is in the process of being deleted. This value might reflect the value of an ID column that you defined for the underlying table, or it can be a sequence value generated by InnoDB when the table contains no suitable column. This value is used when you perform text searches, to skip rows in the [INNODB\\_FT\\_INDEX\\_TABLE](#page-84-0) table before data for deleted rows is physically removed from the FULLTEXT index by an OPTIMIZE TABLE statement. For more information, see Optimizing InnoDB Full-Text Indexes.

## **Notes**

- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- You must have the PROCESS privilege to query this table.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

# <span id="page-80-0"></span>**28.4.15 The INFORMATION\_SCHEMA INNODB\_FT\_CONFIG Table**

The [INNODB\\_FT\\_CONFIG](#page-80-0) table provides metadata about the FULLTEXT index and associated processing for an InnoDB table.

This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles).

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_CONFIG](#page-80-0) table has these columns:

• KEY

The name designating an item of metadata for an InnoDB table containing a FULLTEXT index.

The values for this column might change, depending on the needs for performance tuning and debugging for InnoDB full-text processing. The key names and their meanings include:

- optimize\_checkpoint\_limit: The number of seconds after which an OPTIMIZE TABLE run stops.
- synced\_doc\_id: The next DOC\_ID to be issued.

- stopword\_table\_name: The database/table name for a user-defined stopword table. The VALUE column is empty if there is no user-defined stopword table.
- use\_stopword: Indicates whether a stopword table is used, which is defined when the FULLTEXT index is created.
- VALUE

The value associated with the corresponding KEY column, reflecting some limit or current value for an aspect of a FULLTEXT index for an InnoDB table.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_CONFIG;
+---------------------------+-------------------+
| KEY | VALUE |
+---------------------------+-------------------+
| optimize_checkpoint_limit | 180 |
| synced_doc_id | 0 |
| stopword_table_name | test/my_stopwords |
| use_stopword | 1 |
+---------------------------+-------------------+
```

## **Notes**

- This table is intended only for internal configuration. It is not intended for statistical information purposes.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

# <span id="page-81-0"></span>**28.4.16 The INFORMATION\_SCHEMA INNODB\_FT\_DEFAULT\_STOPWORD Table**

The [INNODB\\_FT\\_DEFAULT\\_STOPWORD](#page-81-0) table holds a list of stopwords that are used by default when creating a FULLTEXT index on InnoDB tables. For information about the default InnoDB stopword list and how to define your own stopword lists, see Section 14.9.4, "Full-Text Stopwords".

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_DEFAULT\\_STOPWORD](#page-81-0) table has these columns:

• value

A word that is used by default as a stopword for FULLTEXT indexes on InnoDB tables. This is not used if you override the default stopword processing with either the innodb\_ft\_server\_stopword\_table or the innodb\_ft\_user\_stopword\_table system variable.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_DEFAULT_STOPWORD;
+-------+
| value |
+-------+
| a |
```

```
| about |
| an |
| are |
| as |
| at |
| be |
| by |
| com |
| de |
| en |
| for |
| from |
| how |
| i |
| in |
| is |
| it |
| la |
| of |
| on |
| or |
| that |
| the |
| this |
| to |
| was |
| what |
| when |
| where |
| who |
| will |
| with |
| und |
| the |
| www |
+-------+
36 rows in set (0.00 sec)
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

# <span id="page-82-0"></span>**28.4.17 The INFORMATION\_SCHEMA INNODB\_FT\_DELETED Table**

The [INNODB\\_FT\\_DELETED](#page-82-0) table stores rows that are deleted from the FULLTEXT index for an InnoDB table. To avoid expensive index reorganization during DML operations for an InnoDB FULLTEXT index, the information about newly deleted words is stored separately, filtered out of search results when you do a text search, and removed from the main search index only when you issue an OPTIMIZE TABLE statement for the InnoDB table. For more information, see Optimizing InnoDB Full-Text Indexes.

This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles).

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_DELETED](#page-82-0) table has these columns:

• DOC\_ID

The document ID of the newly deleted row. This value might reflect the value of an ID column that you defined for the underlying table, or it can be a sequence value generated by InnoDB when the table contains no suitable column. This value is used when you perform text searches, to skip rows in the [INNODB\\_FT\\_INDEX\\_TABLE](#page-84-0) table before data for deleted rows is physically removed from the FULLTEXT index by an OPTIMIZE TABLE statement. For more information, see Optimizing InnoDB Full-Text Indexes.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_DELETED;
+--------+
| DOC_ID |
+--------+
| 6 |
| 7 |
| 8 |
+--------+
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

## <span id="page-83-0"></span>**28.4.18 The INFORMATION\_SCHEMA INNODB\_FT\_INDEX\_CACHE Table**

The [INNODB\\_FT\\_INDEX\\_CACHE](#page-83-0) table provides token information about newly inserted rows in a FULLTEXT index. To avoid expensive index reorganization during DML operations, the information about newly indexed words is stored separately, and combined with the main search index only when OPTIMIZE TABLE is run, when the server is shut down, or when the cache size exceeds a limit defined by the innodb\_ft\_cache\_size or innodb\_ft\_total\_cache\_size system variable.

This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles).

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_INDEX\\_CACHE](#page-83-0) table has these columns:

• WORD

A word extracted from the text of a newly inserted row.

• FIRST\_DOC\_ID

The first document ID in which this word appears in the FULLTEXT index.

• LAST\_DOC\_ID

The last document ID in which this word appears in the FULLTEXT index.

• DOC\_COUNT

The number of rows in which this word appears in the FULLTEXT index. The same word can occur several times within the cache table, once for each combination of DOC\_ID and POSITION values.

• DOC\_ID

The document ID of the newly inserted row. This value might reflect the value of an ID column that you defined for the underlying table, or it can be a sequence value generated by InnoDB when the table contains no suitable column.

• POSITION

The position of this particular instance of the word within the relevant document identified by the DOC\_ID value. The value does not represent an absolute position; it is an offset added to the POSITION of the previous instance of that word.

## **Notes**

• This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example test/articles). The following example demonstrates how to use the innodb\_ft\_aux\_table system variable to show information about a FULLTEXT index for a specified table.

```
mysql> USE test;
mysql> CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT,
 FULLTEXT (title,body)
 ) ENGINE=InnoDB;
mysql> INSERT INTO articles (title,body) VALUES
 ('MySQL Tutorial','DBMS stands for DataBase ...'),
 ('How To Use MySQL Well','After you went through a ...'),
 ('Optimizing MySQL','In this tutorial we show ...'),
 ('1001 MySQL Tricks','1. Never run mysqld as root. 2. ...'),
 ('MySQL vs. YourSQL','In the following database comparison ...'),
 ('MySQL Security','When configured properly, MySQL ...');
mysql> SET GLOBAL innodb_ft_aux_table = 'test/articles';
mysql> SELECT WORD, DOC_COUNT, DOC_ID, POSITION
 FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_CACHE LIMIT 5;
+------------+-----------+--------+----------+
| WORD | DOC_COUNT | DOC_ID | POSITION |
+------------+-----------+--------+----------+
| 1001 | 1 | 4 | 0 |
| after | 1 | 2 | 22 |
| comparison | 1 | 5 | 44 |
| configured | 1 | 6 | 20 |
| database | 2 | 1 | 31 |
+------------+-----------+--------+----------+
```

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

# <span id="page-84-0"></span>**28.4.19 The INFORMATION\_SCHEMA INNODB\_FT\_INDEX\_TABLE Table**

The [INNODB\\_FT\\_INDEX\\_TABLE](#page-84-0) table provides information about the inverted index used to process text searches against the FULLTEXT index of an InnoDB table.

This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles).

For related usage information and examples, see Section 17.15.4, "InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables".

The [INNODB\\_FT\\_INDEX\\_TABLE](#page-84-0) table has these columns:

• WORD

A word extracted from the text of the columns that are part of a FULLTEXT.

• FIRST\_DOC\_ID

The first document ID in which this word appears in the FULLTEXT index.

• LAST\_DOC\_ID

The last document ID in which this word appears in the FULLTEXT index.

• DOC\_COUNT

The number of rows in which this word appears in the FULLTEXT index. The same word can occur several times within the cache table, once for each combination of DOC\_ID and POSITION values.

• DOC\_ID

The document ID of the row containing the word. This value might reflect the value of an ID column that you defined for the underlying table, or it can be a sequence value generated by InnoDB when the table contains no suitable column.

• POSITION

The position of this particular instance of the word within the relevant document identified by the DOC\_ID value.

### **Notes**

• This table is empty initially. Before querying it, set the value of the innodb\_ft\_aux\_table system variable to the name (including the database name) of the table that contains the FULLTEXT index (for example, test/articles). The following example demonstrates how to use the innodb\_ft\_aux\_table system variable to show information about a FULLTEXT index for a specified table. Before information for newly inserted rows appears in INNODB\_FT\_INDEX\_TABLE, the FULLTEXT index cache must be flushed to disk. This is accomplished by running an OPTIMIZE TABLE operation on the indexed table with the innodb\_optimize\_fulltext\_only system variable enabled. (The example disables that variable again at the end because it is intended to be enabled only temporarily.)

```
mysql> USE test;
mysql> CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT,
 FULLTEXT (title,body)
 ) ENGINE=InnoDB;
mysql> INSERT INTO articles (title,body) VALUES
 ('MySQL Tutorial','DBMS stands for DataBase ...'),
 ('How To Use MySQL Well','After you went through a ...'),
 ('Optimizing MySQL','In this tutorial we show ...'),
 ('1001 MySQL Tricks','1. Never run mysqld as root. 2. ...'),
 ('MySQL vs. YourSQL','In the following database comparison ...'),
 ('MySQL Security','When configured properly, MySQL ...');
mysql> SET GLOBAL innodb_optimize_fulltext_only=ON;
mysql> OPTIMIZE TABLE articles;
```

```
+---------------+----------+----------+----------+
| Table | Op | Msg_type | Msg_text |
+---------------+----------+----------+----------+
| test.articles | optimize | status | OK |
+---------------+----------+----------+----------+
mysql> SET GLOBAL innodb_ft_aux_table = 'test/articles';
mysql> SELECT WORD, DOC_COUNT, DOC_ID, POSITION
 FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_TABLE LIMIT 5;
+------------+-----------+--------+----------+
| WORD | DOC_COUNT | DOC_ID | POSITION |
+------------+-----------+--------+----------+
| 1001 | 1 | 4 | 0 |
| after | 1 | 2 | 22 |
| comparison | 1 | 5 | 44 |
| configured | 1 | 6 | 20 |
| database | 2 | 1 | 31 |
+------------+-----------+--------+----------+
mysql> SET GLOBAL innodb_optimize_fulltext_only=OFF;
```

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- For more information about InnoDB FULLTEXT search, see Section 17.6.2.4, "InnoDB Full-Text Indexes", and Section 14.9, "Full-Text Search Functions".

## <span id="page-86-0"></span>**28.4.20 The INFORMATION\_SCHEMA INNODB\_INDEXES Table**

The [INNODB\\_INDEXES](#page-86-0) table provides metadata about InnoDB indexes.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_INDEXES](#page-86-0) table has these columns:

• INDEX\_ID

An identifier for the index. Index identifiers are unique across all the databases in an instance.

• NAME

The name of the index. Most indexes created implicitly by InnoDB have consistent names but the index names are not necessarily unique. Examples: PRIMARY for a primary key index, GEN\_CLUST\_INDEX for the index representing a primary key when one is not specified, and ID\_IND, FOR\_IND, and REF\_IND for foreign key constraints.

• TABLE\_ID

An identifier representing the table associated with the index; the same value as INNODB\_TABLES.TABLE\_ID.

• TYPE

A numeric value derived from bit-level information that identifies the index type. 0 = nonunique secondary index; 1 = automatically generated clustered index (GEN\_CLUST\_INDEX); 2 = unique nonclustered index; 3 = clustered index; 32 = full-text index; 64 = spatial index; 128 = secondary index on a virtual generated column.

• N\_FIELDS

The number of columns in the index key. For GEN\_CLUST\_INDEX indexes, this value is 0 because the index is created using an artificial value rather than a real table column.

#### • PAGE NO

The root page number of the index B-tree. For full-text indexes, the PAGE\_NO column is unused and set to -1 (FIL NULL) because the full-text index is laid out in several B-trees (auxiliary tables).

#### • SPACE

An identifier for the tablespace where the index resides. 0 means the InnoDB system tablespace. Any other number represents a table created with a separate .ibd file in file-per-table mode. This identifier stays the same after a TRUNCATE TABLE statement. Because all indexes for a table reside in the same tablespace as the table, this value is not necessarily unique.

• MERGE THRESHOLD

The merge threshold value for index pages. If the amount of data in an index page falls below the MERGE\_THRESHOLD value when a row is deleted or when a row is shortened by an update operation, InnoDB attempts to merge the index page with the neighboring index page. The default threshold value is 50%. For more information, see Section 17.8.11, "Configuring the Merge Threshold for Index Pages".

### **Example**

```
mysql> SELECT * FROM INFORMATION SCHEMA.INNODB INDEXES WHERE TABLE ID = 34\G
                   ****** 1. row ***
      INDEX ID: 39
         NAME: GEN CLUST INDEX
      TABLE ID: 34
         TYPE: 1
      N FIELDS: 0
       PAGE NO: 3
        SPACE: 23
MERGE THRESHOLD: 50
                    ***** 2. row ***************
     INDEX ID: 40
         NAME: i1
      TABLE ID: 34
         TYPE. O
      N FIELDS: 1
       PAGE NO: 4
         SPACE: 23
MERGE THRESHOLD: 50
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-87-0"></span>28.4.21 The INFORMATION\_SCHEMA INNODB\_METRICS Table

The INNODB\_METRICS table provides a wide variety of InnoDB performance information, complementing the specific focus areas of the Performance Schema tables for InnoDB. With simple queries, you can check the overall health of the system. With more detailed queries, you can diagnose issues such as performance bottlenecks, resource shortages, and application issues.

Each monitor represents a point within the InnoDB source code that is instrumented to gather counter information. Each counter can be started, stopped, and reset. You can also perform these actions for a group of counters using their common module name.

By default, relatively little data is collected. To start, stop, and reset counters, set one of the system variables <code>innodb\_monitor\_enable</code>, <code>innodb\_monitor\_disable</code>, <code>innodb\_monitor\_reset</code>, or <code>innodb\_monitor\_reset\_all</code>, using the name of the counter, the name of the module, a wildcard match for such a name using the "%" character, or the special keyword <code>all</code>.

For usage information, see Section 17.15.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

The [INNODB\\_METRICS](#page-87-0) table has these columns:

• NAME

A unique name for the counter.

• SUBSYSTEM

The aspect of InnoDB that the metric applies to.

• COUNT

The value since the counter was enabled.

• MAX\_COUNT

The maximum value since the counter was enabled.

• MIN\_COUNT

The minimum value since the counter was enabled.

• AVG\_COUNT

The average value since the counter was enabled.

• COUNT\_RESET

The counter value since it was last reset. (The \_RESET columns act like the lap counter on a stopwatch: you can measure the activity during some time interval, while the cumulative figures are still available in COUNT, MAX\_COUNT, and so on.)

• MAX\_COUNT\_RESET

The maximum counter value since it was last reset.

• MIN\_COUNT\_RESET

The minimum counter value since it was last reset.

• AVG\_COUNT\_RESET

The average counter value since it was last reset.

• TIME\_ENABLED

The timestamp of the last start.

• TIME\_DISABLED

The timestamp of the last stop.

• TIME\_ELAPSED

The elapsed time in seconds since the counter started.

• TIME\_RESET

The timestamp of the last reset.

• STATUS

Whether the counter is still running (enabled) or stopped (disabled).

• TYPE

Whether the item is a cumulative counter, or measures the current value of some resource.

• COMMENT

The counter description.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME='dml_inserts'\G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 3
 MAX_COUNT: 3
 MIN_COUNT: NULL
 AVG_COUNT: 0.046153846153846156
 COUNT_RESET: 3
MAX_COUNT_RESET: 3
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
 TIME_ENABLED: 2014-12-04 14:18:28
 TIME_DISABLED: NULL
 TIME_ELAPSED: 65
 TIME_RESET: NULL
 STATUS: enabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.
- Transaction counter COUNT values may differ from the number of transaction events reported in Performance Schema EVENTS\_TRANSACTIONS\_SUMMARY tables. InnoDB counts only those transactions that it executes, whereas Performance Schema collects events for all non-aborted transactions initiated by the server, including empty transactions.

# <span id="page-89-0"></span>**28.4.22 The INFORMATION\_SCHEMA INNODB\_SESSION\_TEMP\_TABLESPACES Table**

The [INNODB\\_SESSION\\_TEMP\\_TABLESPACES](#page-89-0) table provides metadata about session temporary tablespaces used for internal and user-created temporary tables. This table was added in MySQL 8.0.13.

The [INNODB\\_SESSION\\_TEMP\\_TABLESPACES](#page-89-0) table has these columns:

• ID

The process or session ID.

• SPACE

The tablespace ID. A range of 400 thousand space IDs is reserved for session temporary tablespaces. Session temporary tablespaces are recreated each time the server is started. Space IDs are not persisted when the server is shut down and may be reused.

• PATH

The tablespace data file path. A session temporary tablespace has an ibt file extension.

• SIZE

The size of the tablespace, in bytes.

• STATE

The state of the tablespace. ACTIVE indicates that the tablespace is currently used by a session. INACTIVE indicates that the tablespace is in the pool of available session temporary tablespaces.

• PURPOSE

The purpose of the tablespace. INTRINSIC indicates that the tablespace is used for optimized internal temporary tables use by the optimizer. SLAVE indicates that the tablespace is allocated for storing user-created temporary tables on a replication slave. USER indicates that the tablespace is used for user-created temporary tables. NONE indicates that the tablespace is not in use.

### **Example**

| +++++++<br>  ID   SPACE<br>  PATH<br>  SIZE   STATE<br>  PURPOSE<br> <br>+++++++<br>  8   4294566162   ./#innodb_temp/temp_10.ibt   81920   ACTIVE<br>  INTRINSIC  <br>  8   4294566161   ./#innodb_temp/temp_9.ibt   98304   ACTIVE<br>  USER<br> <br>  0   4294566153   ./#innodb_temp/temp_1.ibt   81920   INACTIVE   NONE<br> <br>  0   4294566154   ./#innodb_temp/temp_2.ibt   81920   INACTIVE   NONE<br> <br>  0   4294566155   ./#innodb_temp/temp_3.ibt   81920   INACTIVE   NONE<br>  0   4294566156   ./#innodb_temp/temp_4.ibt   81920   INACTIVE   NONE<br>  0   4294566157   ./#innodb_temp/temp_5.ibt   81920   INACTIVE   NONE<br>  0   4294566158   ./#innodb_temp/temp_6.ibt   81920   INACTIVE   NONE<br>  0   4294566159   ./#innodb_temp/temp_7.ibt   81920   INACTIVE   NONE<br>  0   4294566160   ./#innodb_temp/temp_8.ibt   81920   INACTIVE   NONE | mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SESSION_TEMP_TABLESPACES; |  |  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|--|--|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |
| <br> <br> <br> <br> <br> <br>+++++++                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                          |  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                          |  |  |

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

# <span id="page-90-0"></span>**28.4.23 The INFORMATION\_SCHEMA INNODB\_TABLES Table**

The [INNODB\\_TABLES](#page-90-0) table provides metadata about InnoDB tables.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_TABLES](#page-90-0) table has these columns:

• TABLE\_ID

An identifier for the InnoDB table. This value is unique across all databases in the instance.

• NAME

The name of the table, preceded by the schema (database) name where appropriate (for example, test/t1). Names of databases and user tables are in the same case as they were originally defined, possibly influenced by the lower\_case\_table\_names setting.

• FLAG

A numeric value that represents bit-level information about table format and storage characteristics.

• N\_COLS

The number of columns in the table. The number reported includes three hidden columns that are created by InnoDB (DB\_ROW\_ID, DB\_TRX\_ID, and DB\_ROLL\_PTR). The number reported also includes virtual generated columns, if present.

• SPACE

An identifier for the tablespace where the table resides. 0 means the InnoDB system tablespace. Any other number represents either a file-per-table tablespace or a general tablespace. This identifier stays the same after a TRUNCATE TABLE statement. For file-per-table tablespaces, this identifier is unique for tables across all databases in the instance.

• ROW\_FORMAT

The table's row format (Compact, Redundant, Dynamic, or Compressed).

• ZIP\_PAGE\_SIZE

The zip page size. Applies only to tables with a row format of Compressed.

• SPACE\_TYPE

The type of tablespace to which the table belongs. Possible values include System for the system tablespace, General for general tablespaces, and Single for file-per-table tablespaces. Tables assigned to the system tablespace using CREATE TABLE or ALTER TABLE TABLESPACE=innodb\_system have a SPACE\_TYPE of General. For more information, see CREATE TABLESPACE.

• INSTANT\_COLS

The number of columns that existed before the first instant column was added using ALTER TABLE ... ADD COLUMN with ALGORITHM=INSTANT. This column is no longer used as of MySQL 8.0.29 but continues to show information for tables with columns that were added instantly prior to MySQL 8.0.29.

• TOTAL\_ROW\_VERSIONS

The number of row versions for the table. The initial value is 0. The value is incremented by ALTER TABLE ... ALGORITHM=INSTANT operations that add or remove columns. When a table with instantly added or dropped columns is rebuilt due to a table-rebuilding ALTER TABLE or OPTIMIZE TABLE operation, the value is reset to 0. For more information, see Column Operations.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TABLES WHERE TABLE_ID = 214\G
*************************** 1. row ***************************
 TABLE_ID: 1064
 NAME: test/t1
 FLAG: 33
 N_COLS: 6
 SPACE: 3
 ROW_FORMAT: Dynamic
 ZIP_PAGE_SIZE: 0
 SPACE_TYPE: Single
 INSTANT_COLS: 0
TOTAL_ROW_VERSIONS: 3
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-92-0"></span>**28.4.24 The INFORMATION\_SCHEMA INNODB\_TABLESPACES Table**

The [INNODB\\_TABLESPACES](#page-92-0) table provides metadata about InnoDB file-per-table, general, and undo tablespaces.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

![](_page_92_Picture_4.jpeg)

#### **Note**

The INFORMATION\_SCHEMA [FILES](#page-14-0) table reports metadata for InnoDB tablespace types including file-per-table tablespaces, general tablespaces, the system tablespace, the global temporary tablespace, and undo tablespaces.

The [INNODB\\_TABLESPACES](#page-92-0) table has these columns:

• SPACE

The tablespace ID.

• NAME

The schema (database) and table name.

• FLAG

A numeric value that represents bit-level information about tablespace format and storage characteristics.

• ROW\_FORMAT

The tablespace row format (Compact or Redundant, Dynamic or Compressed, or Undo). The data in this column is interpreted from the tablespace flag information that resides in the data file.

There is no way to determine from this flag information if the tablespace row format is Redundant or Compact, which is why one of the possible ROW\_FORMAT values is Compact or Redundant.

• PAGE\_SIZE

The tablespace page size. The data in this column is interpreted from the tablespace flags information that resides in the .ibd file.

• ZIP\_PAGE\_SIZE

The tablespace zip page size. The data in this column is interpreted from the tablespace flags information that resides in the .ibd file.

• SPACE\_TYPE

The type of tablespace. Possible values include General for general tablespaces, Single for fileper-table tablespaces, System for the system tablespace, and Undo for undo tablespaces.

• FS\_BLOCK\_SIZE

The file system block size, which is the unit size used for hole punching. This column pertains to the InnoDB transparent page compression feature.

• FILE\_SIZE

The apparent size of the file, which represents the maximum size of the file, uncompressed. This column pertains to the InnoDB transparent page compression feature.

• ALLOCATED\_SIZE

The actual size of the file, which is the amount of space allocated on disk. This column pertains to the InnoDB transparent page compression feature.

• AUTOEXTEND\_SIZE

The auto-extend size of the tablespace. This column was added in MySQL 8.0.23.

• SERVER\_VERSION

The MySQL version that created the tablespace, or the MySQL version into which the tablespace was imported, or the version of the last major MySQL version upgrade. The value is unchanged by a release series upgrade, such as an upgrade from MySQL 8.0.x to 8.0.y. The value can be considered a "creation" marker or "certified" marker for the tablespace.

• SPACE\_VERSION

The tablespace version, used to track changes to the tablespace format.

• ENCRYPTION

Whether the tablespace is encrypted. This column was added in MySQL 8.0.13.

• STATE

The tablespace state. This column was added in MySQL 8.0.14.

For file-per-table and general tablespaces, states include:

- normal: The tablespace is normal and active.
- discarded: The tablespace was discarded by an ALTER TABLE ... DISCARD TABLESPACE statement.
- corrupted: The tablespace is identified by InnoDB as corrupted.

For undo tablespaces, states include:

- active: Rollback segments in the undo tablespace can be allocated to new transactions.
- inactive: Rollback segments in the undo tablespace are no longer used by new transactions. The truncate process is in progress. The undo tablespace was either selected by the purge thread implicitly or was made inactive by an ALTER UNDO TABLESPACE ... SET INACTIVE statement.
- empty: The undo tablespace was truncated and is no longer active. It is ready to be dropped or made active again by an ALTER UNDO TABLESPACE ... SET INACTIVE statement.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE SPACE = 26\G
*************************** 1. row ***************************
 SPACE: 26
 NAME: test/t1
 FLAG: 0
 ROW_FORMAT: Compact or Redundant
 PAGE_SIZE: 16384
 ZIP_PAGE_SIZE: 0
 SPACE_TYPE: Single
 FS_BLOCK_SIZE: 4096
 FILE_SIZE: 98304
ALLOCATED_SIZE: 65536
AUTOEXTEND_SIZE: 0
SERVER_VERSION: 8.0.23
 SPACE_VERSION: 1
```

```
 ENCRYPTION: N
 STATE: normal
```

### **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-94-0"></span>**28.4.25 The INFORMATION\_SCHEMA INNODB\_TABLESPACES\_BRIEF Table**

The [INNODB\\_TABLESPACES\\_BRIEF](#page-94-0) table provides space ID, name, path, flag, and space type metadata for file-per-table, general, undo, and system tablespaces.

[INNODB\\_TABLESPACES](#page-92-0) provides the same metadata but loads more slowly because other metadata provided by the table, such as FS\_BLOCK\_SIZE, FILE\_SIZE, and ALLOCATED\_SIZE, must be loaded dynamically.

Space and path metadata is also provided by the [INNODB\\_DATAFILES](#page-77-0) table.

The [INNODB\\_TABLESPACES\\_BRIEF](#page-94-0) table has these columns:

• SPACE

The tablespace ID.

• NAME

The tablespace name. For file-per-table tablespaces, the name is in the form of schema/ table\_name.

• PATH

The tablespace data file path. If a file-per-table tablespace is created in a location outside the MySQL data directory, the path value is a fully qualified directory path. Otherwise, the path is relative to the data directory.

• FLAG

A numeric value that represents bit-level information about tablespace format and storage characteristics.

• SPACE\_TYPE

The type of tablespace. Possible values include General for InnoDB general tablespaces, Single for InnoDB file-per-table tablespaces, and System for the InnoDB system tablespace.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TABLESPACES_BRIEF WHERE SPACE = 7;
+-------+---------+---------------+-------+------------+
| SPACE | NAME | PATH | FLAG | SPACE_TYPE |
+-------+---------+---------------+-------+------------+
| 7 | test/t1 | ./test/t1.ibd | 16417 | Single |
+-------+---------+---------------+-------+------------+
```

## **Notes**

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-95-0"></span>**28.4.26 The INFORMATION\_SCHEMA INNODB\_TABLESTATS View**

The [INNODB\\_TABLESTATS](#page-95-0) table provides a view of low-level status information about InnoDB tables. This data is used by the MySQL optimizer to calculate which index to use when querying an InnoDB table. This information is derived from in-memory data structures rather than data stored on disk. There is no corresponding internal InnoDB system table.

InnoDB tables are represented in this view if they have been opened since the last server restart and have not aged out of the table cache. Tables for which persistent stats are available are always represented in this view.

Table statistics are updated only for DELETE or UPDATE operations that modify indexed columns. Statistics are not updated by operations that modify only nonindexed columns.

ANALYZE TABLE clears table statistics and sets the STATS\_INITIALIZED column to Uninitialized. Statistics are collected again the next time the table is accessed.

For related usage information and examples, see Section 17.15.3, "InnoDB INFORMATION\_SCHEMA Schema Object Tables".

The [INNODB\\_TABLESTATS](#page-95-0) table has these columns:

• TABLE\_ID

An identifier representing the table for which statistics are available; the same value as INNODB\_TABLES.TABLE\_ID.

• NAME

The name of the table; the same value as INNODB\_TABLES.NAME.

• STATS\_INITIALIZED

The value is Initialized if the statistics are already collected, Uninitialized if not.

• NUM\_ROWS

The current estimated number of rows in the table. Updated after each DML operation. The value could be imprecise if uncommitted transactions are inserting into or deleting from the table.

• CLUST\_INDEX\_SIZE

The number of pages on disk that store the clustered index, which holds the InnoDB table data in primary key order. This value might be null if no statistics are collected yet for the table.

• OTHER\_INDEX\_SIZE

The number of pages on disk that store all secondary indexes for the table. This value might be null if no statistics are collected yet for the table.

• MODIFIED\_COUNTER

The number of rows modified by DML operations, such as INSERT, UPDATE, DELETE, and also cascade operations from foreign keys. This column is reset each time table statistics are recalculated

• AUTOINC

The next number to be issued for any auto-increment-based operation. The rate at which the AUTOINC value changes depends on how many times auto-increment numbers have been requested and how many numbers are granted per request.

• REF\_COUNT

When this counter reaches zero, the table metadata can be evicted from the table cache.

## **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TABLESTATS where TABLE_ID = 71\G
*************************** 1. row ***************************
 TABLE_ID: 71
 NAME: test/t1
STATS_INITIALIZED: Initialized
 NUM_ROWS: 1
 CLUST_INDEX_SIZE: 1
 OTHER_INDEX_SIZE: 0
 MODIFIED_COUNTER: 1
 AUTOINC: 0
 REF_COUNT: 1
```

## **Notes**

- This table is useful primarily for expert-level performance monitoring, or when developing performance-related extensions for MySQL.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-96-0"></span>**28.4.27 The INFORMATION\_SCHEMA INNODB\_TEMP\_TABLE\_INFO Table**

The [INNODB\\_TEMP\\_TABLE\\_INFO](#page-96-0) table provides information about user-created InnoDB temporary tables that are active in an InnoDB instance. It does not provide information about internal InnoDB temporary tables used by the optimizer. The [INNODB\\_TEMP\\_TABLE\\_INFO](#page-96-0) table is created when first queried, exists only in memory, and is not persisted to disk.

For usage information and examples, see Section 17.15.7, "InnoDB INFORMATION\_SCHEMA Temporary Table Info Table".

The [INNODB\\_TEMP\\_TABLE\\_INFO](#page-96-0) table has these columns:

• TABLE\_ID

The table ID of the temporary table.

• NAME

The name of the temporary table.

• N\_COLS

The number of columns in the temporary table. The number includes three hidden columns created by InnoDB (DB\_ROW\_ID, DB\_TRX\_ID, and DB\_ROLL\_PTR).

• SPACE

The ID of the temporary tablespace where the temporary table resides.

### **Example**

```
mysql> CREATE TEMPORARY TABLE t1 (c1 INT PRIMARY KEY) ENGINE=INNODB;
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TEMP_TABLE_INFO\G
*************************** 1. row ***************************
TABLE_ID: 97
 NAME: #sql8c88_43_0
 N_COLS: 4
 SPACE: 76
```

### **Notes**

- This table is useful primarily for expert-level monitoring.
- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-97-0"></span>**28.4.28 The INFORMATION\_SCHEMA INNODB\_TRX Table**

The [INNODB\\_TRX](#page-97-0) table provides information about every transaction currently executing inside InnoDB, including whether the transaction is waiting for a lock, when the transaction started, and the SQL statement the transaction is executing, if any.

For usage information, see Section 17.15.2.1, "Using InnoDB Transaction and Locking Information".

The [INNODB\\_TRX](#page-97-0) table has these columns:

• TRX\_ID

A unique transaction ID number, internal to InnoDB. These IDs are not created for transactions that are read only and nonlocking. For details, see Section 10.5.3, "Optimizing InnoDB Read-Only Transactions".

• TRX\_WEIGHT

The weight of a transaction, reflecting (but not necessarily the exact count of) the number of rows altered and the number of rows locked by the transaction. To resolve a deadlock, InnoDB selects the transaction with the smallest weight as the "victim" to roll back. Transactions that have changed nontransactional tables are considered heavier than others, regardless of the number of altered and locked rows.

• TRX\_STATE

The transaction execution state. Permitted values are RUNNING, LOCK WAIT, ROLLING BACK, and COMMITTING.

• TRX\_STARTED

The transaction start time.

• TRX\_REQUESTED\_LOCK\_ID

The ID of the lock the transaction is currently waiting for, if TRX\_STATE is LOCK WAIT; otherwise NULL. To obtain details about the lock, join this column with the ENGINE\_LOCK\_ID column of the Performance Schema data\_locks table.

• TRX\_WAIT\_STARTED

The time when the transaction started waiting on the lock, if TRX\_STATE is LOCK WAIT; otherwise NULL.

• TRX\_MYSQL\_THREAD\_ID

The MySQL thread ID. To obtain details about the thread, join this column with the ID column of the INFORMATION\_SCHEMA [PROCESSLIST](#page-31-0) table, but see Section 17.15.2.3, "Persistence and Consistency of InnoDB Transaction and Locking Information".

• TRX\_QUERY

The SQL statement that is being executed by the transaction.

• TRX\_OPERATION\_STATE

The transaction's current operation, if any; otherwise NULL.

• TRX\_TABLES\_IN\_USE

The number of InnoDB tables used while processing the current SQL statement of this transaction.

• TRX\_TABLES\_LOCKED

The number of InnoDB tables that the current SQL statement has row locks on. (Because these are row locks, not table locks, the tables can usually still be read from and written to by multiple transactions, despite some rows being locked.)

• TRX\_LOCK\_STRUCTS

The number of locks reserved by the transaction.

• TRX\_LOCK\_MEMORY\_BYTES

The total size taken up by the lock structures of this transaction in memory.

• TRX\_ROWS\_LOCKED

The approximate number or rows locked by this transaction. The value might include delete-marked rows that are physically present but not visible to the transaction.

• TRX\_ROWS\_MODIFIED

The number of modified and inserted rows in this transaction.

• TRX\_CONCURRENCY\_TICKETS

A value indicating how much work the current transaction can do before being swapped out, as specified by the innodb\_concurrency\_tickets system variable.

• TRX\_ISOLATION\_LEVEL

The isolation level of the current transaction.

• TRX\_UNIQUE\_CHECKS

Whether unique checks are turned on or off for the current transaction. For example, they might be turned off during a bulk data load.

• TRX\_FOREIGN\_KEY\_CHECKS

Whether foreign key checks are turned on or off for the current transaction. For example, they might be turned off during a bulk data load.

• TRX\_LAST\_FOREIGN\_KEY\_ERROR

The detailed error message for the last foreign key error, if any; otherwise NULL.

• TRX\_ADAPTIVE\_HASH\_LATCHED

Whether the adaptive hash index is locked by the current transaction. When the adaptive hash index search system is partitioned, a single transaction does not lock the entire adaptive hash index. Adaptive hash index partitioning is controlled by innodb\_adaptive\_hash\_index\_parts, which is set to 8 by default.

• TRX\_ADAPTIVE\_HASH\_TIMEOUT

Deprecated in MySQL 5.7.8. Always returns 0.

Whether to relinquish the search latch immediately for the adaptive hash index, or reserve it across calls from MySQL. When there is no adaptive hash index contention, this value remains zero and statements reserve the latch until they finish. During times of contention, it counts down to zero, and statements release the latch immediately after each row lookup. When the adaptive hash index search system is partitioned (controlled by innodb\_adaptive\_hash\_index\_parts), the value remains 0.

• TRX\_IS\_READ\_ONLY

A value of 1 indicates the transaction is read only.

• TRX\_AUTOCOMMIT\_NON\_LOCKING

A value of 1 indicates the transaction is a SELECT statement that does not use the FOR UPDATE or LOCK IN SHARED MODE clauses, and is executing with autocommit enabled so that the transaction contains only this one statement. When this column and TRX\_IS\_READ\_ONLY are both 1, InnoDB optimizes the transaction to reduce the overhead associated with transactions that change table data.

• TRX\_SCHEDULE\_WEIGHT

The transaction schedule weight assigned by the Contention-Aware Transaction Scheduling (CATS) algorithm to transactions waiting for a lock. The value is relative to the values of other transactions. A higher value has a greater weight. A value is computed only for transactions in a LOCK WAIT state, as reported by the TRX\_STATE column. A NULL value is reported for transactions that are not waiting for a lock. The TRX\_SCHEDULE\_WEIGHT value is different from the TRX\_WEIGHT value, which is computed by a different algorithm for a different purpose.

### **Example**

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX\G
*************************** 1. row ***************************
 trx_id: 1510
 trx_state: RUNNING
 trx_started: 2014-11-19 13:24:40
 trx_requested_lock_id: NULL
 trx_wait_started: NULL
 trx_weight: 586739
 trx_mysql_thread_id: 2
 trx_query: DELETE FROM employees.salaries WHERE salary > 65000
 trx_operation_state: updating or deleting
 trx_tables_in_use: 1
 trx_tables_locked: 1
 trx_lock_structs: 3003
 trx_lock_memory_bytes: 450768
 trx_rows_locked: 1407513
 trx_rows_modified: 583736
 trx_concurrency_tickets: 0
 trx_isolation_level: REPEATABLE READ
 trx_unique_checks: 1
 trx_foreign_key_checks: 1
trx_last_foreign_key_error: NULL
 trx_adaptive_hash_latched: 0
 trx_adaptive_hash_timeout: 10000
 trx_is_read_only: 0
trx_autocommit_non_locking: 0
 trx_schedule_weight: NULL
```

## **Notes**

- Use this table to help diagnose performance problems that occur during times of heavy concurrent load. Its contents are updated as described in Section 17.15.2.3, "Persistence and Consistency of InnoDB Transaction and Locking Information".
- You must have the PROCESS privilege to query this table.

• Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.

## <span id="page-100-0"></span>**28.4.29 The INFORMATION\_SCHEMA INNODB\_VIRTUAL Table**

The [INNODB\\_VIRTUAL](#page-100-0) table provides metadata about InnoDB virtual generated columns and columns upon which virtual generated columns are based.

A row appears in the [INNODB\\_VIRTUAL](#page-100-0) table for each column upon which a virtual generated column is based.

The [INNODB\\_VIRTUAL](#page-100-0) table has these columns:

• TABLE\_ID

An identifier representing the table associated with the virtual column; the same value as INNODB\_TABLES.TABLE\_ID.

• POS

The position value of the virtual generated column. The value is large because it encodes the column sequence number and ordinal position. The formula used to calculate the value uses a bitwise operation:

```
((nth virtual generated column for the InnoDB instance + 1) << 16)
+ the ordinal position of the virtual generated column
```

For example, if the first virtual generated column in the InnoDB instance is the third column of the table, the formula is (0 + 1) << 16) + 2. The first virtual generated column in the InnoDB instance is always number 0. As the third column in the table, the ordinal position of the virtual generated column is 2. Ordinal positions are counted from 0.

• BASE\_POS

The ordinal position of the columns upon which a virtual generated column is based.

### **Example**

```
mysql> CREATE TABLE `t1` (
 `a` int(11) DEFAULT NULL,
 `b` int(11) DEFAULT NULL,
 `c` int(11) GENERATED ALWAYS AS (a+b) VIRTUAL,
 `h` varchar(10) DEFAULT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_VIRTUAL
 WHERE TABLE_ID IN
 (SELECT TABLE_ID FROM INFORMATION_SCHEMA.INNODB_TABLES
 WHERE NAME LIKE "test/t1");
+----------+-------+----------+
| TABLE_ID | POS | BASE_POS |
+----------+-------+----------+
| 98 | 65538 | 0 |
| 98 | 65538 | 1 |
+----------+-------+----------+
```

## **Notes**

• If a constant value is assigned to a virtual generated column, as in the following table, an entry for the column does not appear in the INNODB\_VIRTUAL table. For an entry to appear, a virtual generated column must have a base column.

```
CREATE TABLE `t1` (
 `a` int(11) DEFAULT NULL,
 `b` int(11) DEFAULT NULL,
```

```
 `c` int(11) GENERATED ALWAYS AS (5) VIRTUAL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

However, metadata for such a column does appear in the [INNODB\\_COLUMNS](#page-75-0) table.

- You must have the PROCESS privilege to query this table.
- Use the INFORMATION\_SCHEMA [COLUMNS](#page-5-1) table or the SHOW COLUMNS statement to view additional information about the columns of this table, including data types and default values.