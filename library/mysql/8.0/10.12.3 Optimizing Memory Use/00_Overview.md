---
source: MySQL 8.0 Reference
title: 00_Overview
---

### **10.12.3.1 How MySQL Uses Memory**

MySQL allocates buffers and caches to improve performance of database operations. The default configuration is designed to permit a MySQL server to start on a virtual machine that has approximately 512MB of RAM. You can improve MySQL performance by increasing the values of certain cache and buffer-related system variables. You can also modify the default configuration to run MySQL on systems with limited memory.

The following list describes some of the ways that MySQL uses memory. Where applicable, relevant system variables are referenced. Some items are storage engine or feature specific.

• The InnoDB buffer pool is a memory area that holds cached InnoDB data for tables, indexes, and other auxiliary buffers. For efficiency of high-volume read operations, the buffer pool is divided into pages that can potentially hold multiple rows. For efficiency of cache management, the buffer pool is implemented as a linked list of pages; data that is rarely used is aged out of the cache, using a variation of the LRU algorithm. For more information, see Section 17.5.1, "Buffer Pool".

The size of the buffer pool is important for system performance:

- InnoDB allocates memory for the entire buffer pool at server startup, using malloc() operations. The innodb\_buffer\_pool\_size system variable defines the buffer pool size. Typically, a recommended innodb\_buffer\_pool\_size value is 50 to 75 percent of system memory. innodb\_buffer\_pool\_size can be configured dynamically, while the server is running. For more information, see Section 17.8.3.1, "Configuring InnoDB Buffer Pool Size".
- On systems with a large amount of memory, you can improve concurrency by dividing the buffer pool into multiple buffer pool instances. The innodb\_buffer\_pool\_instances system variable defines the number of buffer pool instances.
- A buffer pool that is too small may cause excessive churning as pages are flushed from the buffer pool only to be required again a short time later.
- A buffer pool that is too large may cause swapping due to competition for memory.
- The storage engine interface enables the optimizer to provide information about the size of the record buffer to be used for scans that the optimizer estimates are likely to read multiple rows. The buffer size can vary based on the size of the estimate. InnoDB uses this variable-size buffering capability to take advantage of row prefetching, and to reduce the overhead of latching and B-tree navigation.
- All threads share the MyISAM key buffer. The key\_buffer\_size system variable determines its size.

For each MyISAM table the server opens, the index file is opened once; the data file is opened once for each concurrently running thread that accesses the table. For each concurrent thread, a table structure, column structures for each column, and a buffer of size 3 \* N are allocated (where N is the maximum row length, not counting BLOB columns). A BLOB column requires five to eight bytes plus the length of the BLOB data. The MyISAM storage engine maintains one extra row buffer for internal use.

- The myisam\_use\_mmap system variable can be set to 1 to enable memory-mapping for all MyISAM tables.
- If an internal in-memory temporary table becomes too large (as determined using the tmp\_table\_size and max\_heap\_table\_size system variables), MySQL automatically converts the table from in-memory to on-disk format. As of MySQL 8.0.16, on-disk temporary tables always use the InnoDB storage engine. (Previously, the storage engine employed for this purpose was determined by the internal\_tmp\_disk\_storage\_engine system variable, which is no longer supported.) You can increase the permissible temporary table size as described in Section 10.4.4, "Internal Temporary Table Use in MySQL".

For MEMORY tables explicitly created with CREATE TABLE, only the max\_heap\_table\_size system variable determines how large a table can grow, and there is no conversion to on-disk format.

- The MySQL Performance Schema is a feature for monitoring MySQL server execution at a low level. The Performance Schema dynamically allocates memory incrementally, scaling its memory use to actual server load, instead of allocating required memory during server startup. Once memory is allocated, it is not freed until the server is restarted. For more information, see Section 29.17, "The Performance Schema Memory-Allocation Model".
- Each thread that the server uses to manage client connections requires some thread-specific space. The following list indicates these and which system variables control their size:

- A stack (thread\_stack)
- A connection buffer (net\_buffer\_length)
- A result buffer (net\_buffer\_length)

The connection buffer and result buffer each begin with a size equal to net\_buffer\_length bytes, but are dynamically enlarged up to max\_allowed\_packet bytes as needed. The result buffer shrinks to net\_buffer\_length bytes after each SQL statement. While a statement is running, a copy of the current statement string is also allocated.

Each connection thread uses memory for computing statement digests. The server allocates max\_digest\_length bytes per session. See Section 29.10, "Performance Schema Statement Digests and Sampling".

- All threads share the same base memory.
- When a thread is no longer needed, the memory allocated to it is released and returned to the system unless the thread goes back into the thread cache. In that case, the memory remains allocated.
- Each request that performs a sequential scan of a table allocates a read buffer. The read\_buffer\_size system variable determines the buffer size.
- When reading rows in an arbitrary sequence (for example, following a sort), a random-read buffer may be allocated to avoid disk seeks. The read\_rnd\_buffer\_size system variable determines the buffer size.
- All joins are executed in a single pass, and most joins can be done without even using a temporary table. Most temporary tables are memory-based hash tables. Temporary tables with a large row length (calculated as the sum of all column lengths) or that contain BLOB columns are stored on disk.
- Most requests that perform a sort allocate a sort buffer and zero to two temporary files depending on the result set size. See Section B.3.3.5, "Where MySQL Stores Temporary Files".
- Almost all parsing and calculating is done in thread-local and reusable memory pools. No memory overhead is needed for small items, thus avoiding the normal slow memory allocation and freeing. Memory is allocated only for unexpectedly large strings.
- For each table having BLOB columns, a buffer is enlarged dynamically to read in larger BLOB values. If you scan a table, the buffer grows as large as the largest BLOB value.
- MySQL requires memory and descriptors for the table cache. Handler structures for all in-use tables are saved in the table cache and managed as "First In, First Out" (FIFO). The table\_open\_cache system variable defines the initial table cache size; see Section 10.4.3.1, "How MySQL Opens and Closes Tables".

MySQL also requires memory for the table definition cache. The table\_definition\_cache system variable defines the number of table definitions that can be stored in the table definition cache. If you use a large number of tables, you can create a large table definition cache to speed up the opening of tables. The table definition cache takes less space and does not use file descriptors, unlike the table cache.

- A FLUSH TABLES statement or mysqladmin flush-tables command closes all tables that are not in use at once and marks all in-use tables to be closed when the currently executing thread finishes. This effectively frees most in-use memory. FLUSH TABLES does not return until all tables have been closed.
- The server caches information in memory as a result of GRANT, CREATE USER, CREATE SERVER, and INSTALL PLUGIN statements. This memory is not released by the corresponding REVOKE,

DROP USER, DROP SERVER, and UNINSTALL PLUGIN statements, so for a server that executes many instances of the statements that cause caching, there is an increase in cached memory use unless it is freed with FLUSH PRIVILEGES.

- In a replication topology, the following settings affect memory usage, and can be adjusted as required:
  - The max\_allowed\_packet system variable on a replication source limits the maximum message size that the source sends to its replicas for processing. This setting defaults to 64M.
  - The system variable replica\_pending\_jobs\_size\_max (from MySQL 8.0.26) or slave\_pending\_jobs\_size\_max (before MySQL 8.0.26) on a multithreaded replica sets the maximum amount of memory that is made available for holding messages awaiting processing. This setting defaults to 128M. The memory is only allocated when needed, but it might be used if your replication topology handles large transactions sometimes. It is a soft limit, and larger transactions can be processed.
  - The rpl\_read\_size system variable on a replication source or replica controls the minimum amount of data in bytes that is read from the binary log files and relay log files. The default is 8192 bytes. A buffer the size of this value is allocated for each thread that reads from the binary log and relay log files, including dump threads on sources and coordinator threads on replicas.
  - The binlog\_transaction\_dependency\_history\_size system variable limits the number of row hashes held as an in-memory history.
  - The max\_binlog\_cache\_size system variable specifies the upper limit of memory usage by an individual transaction.
  - The max\_binlog\_stmt\_cache\_size system variable specifies the upper limit of memory usage by the statement cache.

ps and other system status programs may report that mysqld uses a lot of memory. This may be caused by thread stacks on different memory addresses. For example, the Solaris version of ps counts the unused memory between stacks as used memory. To verify this, check available swap with swap -s. We test mysqld with several memory-leakage detectors (both commercial and Open Source), so there should be no memory leaks.

### **10.12.3.2 Monitoring MySQL Memory Usage**

The following example demonstrates how to use Performance Schema and sys schema to monitor MySQL memory usage.

Most Performance Schema memory instrumentation is disabled by default. Instruments can be enabled by updating the ENABLED column of the Performance Schema setup\_instruments table. Memory instruments have names in the form of memory/code\_area/instrument\_name, where code\_area is a value such as sql or innodb, and instrument\_name is the instrument detail.

1. To view available MySQL memory instruments, query the Performance Schema setup\_instruments table. The following query returns hundreds of memory instruments for all code areas.

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%memory%';
```

You can narrow results by specifying a code area. For example, you can limit results to InnoDB memory instruments by specifying innodb as the code area.

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%memory/innodb%';
+-------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------+---------+-------+
```

```
| memory/innodb/adaptive hash index | NO | NO |
| memory/innodb/buf_buf_pool | NO | NO |
| memory/innodb/dict_stats_bg_recalc_pool_t | NO | NO |
| memory/innodb/dict_stats_index_map_t | NO | NO |
| memory/innodb/dict_stats_n_diff_on_level | NO | NO |
| memory/innodb/other | NO | NO |
| memory/innodb/row_log_buf | NO | NO |
| memory/innodb/row_merge_sort | NO | NO |
| memory/innodb/std | NO | NO |
| memory/innodb/trx_sys_t::rw_trx_ids | NO | NO |
...
```

Depending on your MySQL installation, code areas may include performance\_schema, sql, client, innodb, myisam, csv, memory, blackhole, archive, partition, and others.

2. To enable memory instruments, add a performance-schema-instrument rule to your MySQL configuration file. For example, to enable all memory instruments, add this rule to your configuration file and restart the server:

performance-schema-instrument='memory/%=COUNTED'

![](_page_15_Picture_5.jpeg)

#### **Note**

Enabling memory instruments at startup ensures that memory allocations that occur at startup are counted.

After restarting the server, the ENABLED column of the Performance Schema setup\_instruments table should report YES for memory instruments that you enabled. The TIMED column in the setup\_instruments table is ignored for memory instruments because memory operations are not timed.

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%memory/innodb%';
+-------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------+---------+-------+
| memory/innodb/adaptive hash index | NO | NO |
| memory/innodb/buf_buf_pool | NO | NO |
| memory/innodb/dict_stats_bg_recalc_pool_t | NO | NO |
| memory/innodb/dict_stats_index_map_t | NO | NO |
| memory/innodb/dict_stats_n_diff_on_level | NO | NO |
| memory/innodb/other | NO | NO |
| memory/innodb/row_log_buf | NO | NO |
| memory/innodb/row_merge_sort | NO | NO |
| memory/innodb/std | NO | NO |
| memory/innodb/trx_sys_t::rw_trx_ids | NO | NO |
...
```

3. Query memory instrument data. In this example, memory instrument data is queried in the Performance Schema memory\_summary\_global\_by\_event\_name table, which summarizes data by EVENT\_NAME. The EVENT\_NAME is the name of the instrument.

The following query returns memory data for the InnoDB buffer pool. For column descriptions, see Section 29.12.20.10, "Memory Summary Tables".

```
mysql> SELECT * FROM performance_schema.memory_summary_global_by_event_name
 WHERE EVENT_NAME LIKE 'memory/innodb/buf_buf_pool'\G
 EVENT_NAME: memory/innodb/buf_buf_pool
 COUNT_ALLOC: 1
 COUNT_FREE: 0
 SUM_NUMBER_OF_BYTES_ALLOC: 137428992
 SUM_NUMBER_OF_BYTES_FREE: 0
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 1
 HIGH_COUNT_USED: 1
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 137428992
 HIGH_NUMBER_OF_BYTES_USED: 137428992
```

The same underlying data can be queried using the sys schema memory\_global\_by\_current\_bytes table, which shows current memory usage within the server globally, broken down by allocation type.

```
mysql> SELECT * FROM sys.memory_global_by_current_bytes
 WHERE event_name LIKE 'memory/innodb/buf_buf_pool'\G
*************************** 1. row ***************************
 event_name: memory/innodb/buf_buf_pool
 current_count: 1
 current_alloc: 131.06 MiB
current_avg_alloc: 131.06 MiB
 high_count: 1
 high_alloc: 131.06 MiB
 high_avg_alloc: 131.06 MiB
```

This sys schema query aggregates currently allocated memory (current\_alloc) by code area:

```
mysql> SELECT SUBSTRING_INDEX(event_name,'/',2) AS
 code_area, FORMAT_BYTES(SUM(current_alloc))
 AS current_alloc
 FROM sys.x$memory_global_by_current_bytes
 GROUP BY SUBSTRING_INDEX(event_name,'/',2)
 ORDER BY SUM(current_alloc) DESC;
+---------------------------+---------------+
| code_area | current_alloc |
+---------------------------+---------------+
| memory/innodb | 843.24 MiB |
| memory/performance_schema | 81.29 MiB |
| memory/mysys | 8.20 MiB |
| memory/sql | 2.47 MiB |
| memory/memory | 174.01 KiB |
| memory/myisam | 46.53 KiB |
| memory/blackhole | 512 bytes |
| memory/federated | 512 bytes |
| memory/csv | 512 bytes |
| memory/vio | 496 bytes |
+---------------------------+---------------+
```

![](_page_16_Picture_5.jpeg)

#### **Note**

Prior to MySQL 8.0.16, sys.format\_bytes() was used for FORMAT\_BYTES().

For more information about sys schema, see Chapter 30, MySQL sys Schema.

### **10.12.3.3 Enabling Large Page Support**

Some hardware and operating system architectures support memory pages greater than the default (usually 4KB). The actual implementation of this support depends on the underlying hardware and operating system. Applications that perform a lot of memory accesses may obtain performance improvements by using large pages due to reduced Translation Lookaside Buffer (TLB) misses.

In MySQL, large pages can be used by InnoDB, to allocate memory for its buffer pool and additional memory pool.

Standard use of large pages in MySQL attempts to use the largest size supported, up to 4MB. Under Solaris, a "super large pages" feature enables uses of pages up to 256MB. This feature is available for recent SPARC platforms. It can be enabled or disabled by using the --super-large-pages or - skip-super-large-pages option.

MySQL also supports the Linux implementation of large page support (which is called HugeTLB in Linux).

Before large pages can be used on Linux, the kernel must be enabled to support them and it is necessary to configure the HugeTLB memory pool. For reference, the HugeTBL API is documented in the Documentation/vm/hugetlbpage.txt file of your Linux sources.

The kernels for some recent systems such as Red Hat Enterprise Linux may have the large pages feature enabled by default. To check whether this is true for your kernel, use the following command and look for output lines containing "huge":

```
$> grep -i huge /proc/meminfo
AnonHugePages: 2658304 kB
ShmemHugePages: 0 kB
HugePages_Total: 0
HugePages_Free: 0
HugePages_Rsvd: 0
HugePages_Surp: 0
Hugepagesize: 2048 kB
Hugetlb: 0 kB
```

The nonempty command output indicates that large page support is present, but the zero values indicate that no pages are configured for use.

If your kernel needs to be reconfigured to support large pages, consult the hugetlbpage.txt file for instructions.

Assuming that your Linux kernel has large page support enabled, configure it for use by MySQL using the following steps:

- 1. Determine the number of large pages needed. This is the size of the InnoDB buffer pool divided by the large page size, which we can calculate as innodb\_buffer\_pool\_size / Hugepagesize. Assuming the default value for the innodb\_buffer\_pool\_size (128MB) and using the Hugepagesize value obtained from /proc/meminfo (2MB), this is 128MB / 2MB, or 64 Huge Pages. We call this value P.
- 2. As system root, open the file /etc/sysctl.conf in a text editor, and add the line shown here, where P is the number of large pages obtained in the previous step:

```
vm.nr_hugepages=P
```

Using the actual value obtained previously, the additional line should look like this:

```
vm.nr_hugepages=66
```

Save the updated file.

3. As system root, run the following command:

```
$> sudo sysctl -p
```

![](_page_17_Picture_14.jpeg)

### **Note**

On some systems the large pages file may be named slightly differently; for example, some distributions call it nr\_hugepages. In the event sysctl returns an error relating to the file name, check the name of the corresponding file in /proc/sys/vm and use that instead.

To verify the large page configuration, check /proc/meminfo again as described previously. Now you should see some additional nonzero values in the output, similar to this:

```
$> grep -i huge /proc/meminfo
AnonHugePages: 2686976 kB
ShmemHugePages: 0 kB
HugePages_Total: 233
HugePages_Free: 233
HugePages_Rsvd: 0
HugePages_Surp: 0
Hugepagesize: 2048 kB
Hugetlb: 477184 kB
```

4. Optionally, you may wish to compact the Linux VM. You can do this using a sequence of commands, possibly in a script file, similar to what is shown here:

```
sync
sync
sync
echo 3 > /proc/sys/vm/drop_caches
echo 1 > /proc/sys/vm/compact_memory
```

See your operating platform documentation for more information about how to do this.

- 5. Check any configuration files such as my.cnf used by the server, and make sure that innodb\_buffer\_pool\_chunk\_size is set larger than the huge page size. The default for this variable is 128M.
- 6. Large page support in the MySQL server is disabled by default. To enable it, start the server with --large-pages. You can also do so by adding the following line to the [mysqld] section of the server my.cnf file:

```
large-pages=ON
```

With this option enabled, InnoDB uses large pages automatically for its buffer pool and additional memory pool. If InnoDB cannot do this, it falls back to use of traditional memory and writes a warning to the error log: Warning: Using conventional memory pool.

You can verify that MySQL is now using large pages by checking /proc/meminfo again after restarting mysqld, like this:

```
$> grep -i huge /proc/meminfo
AnonHugePages: 2516992 kB
ShmemHugePages: 0 kB
HugePages_Total: 233
HugePages_Free: 222
HugePages_Rsvd: 55
HugePages_Surp: 0
Hugepagesize: 2048 kB
Hugetlb: 477184 kB
```