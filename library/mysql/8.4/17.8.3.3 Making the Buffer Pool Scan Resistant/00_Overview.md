---
source: MySQL 8.4 Reference
title: 00_Overview
---

Rather than using a strict LRU algorithm, InnoDB uses a technique to minimize the amount of data that is brought into the buffer pool and never accessed again. The goal is to make sure that frequently accessed ("hot") pages remain in the buffer pool, even as read-ahead and full table scans bring in new blocks that might or might not be accessed afterward.

Newly read blocks are inserted into the middle of the LRU list. All newly read pages are inserted at a location that by default is 3/8 from the tail of the LRU list. The pages are moved to the front of the list (the most-recently used end) when they are accessed in the buffer pool for the first time. Thus, pages that are never accessed never make it to the front portion of the LRU list, and "age out" sooner than with a strict LRU approach. This arrangement divides the LRU list into two segments, where the pages downstream of the insertion point are considered "old" and are desirable victims for LRU eviction.

For an explanation of the inner workings of the InnoDB buffer pool and specifics about the LRU algorithm, see Section 17.5.1, "Buffer Pool".

You can control the insertion point in the LRU list and choose whether InnoDB applies the same optimization to blocks brought into the buffer pool by table or index scans. The configuration parameter innodb\_old\_blocks\_pct controls the percentage of "old" blocks in the LRU list. The default value of innodb\_old\_blocks\_pct is 37, corresponding to the original fixed ratio of 3/8. The value range is 5 (new pages in the buffer pool age out very quickly) to 95 (only 5% of the buffer pool is reserved for hot pages, making the algorithm close to the familiar LRU strategy).

The optimization that keeps the buffer pool from being churned by read-ahead can avoid similar problems due to table or index scans. In these scans, a data page is typically accessed a few times in quick succession and is never touched again. The configuration parameter innodb\_old\_blocks\_time specifies the time window (in milliseconds) after the first access to a page during which it can be accessed without being moved to the front (most-recently used end) of the LRU list. The default value of innodb\_old\_blocks\_time is 1000. Increasing this value makes more and more blocks likely to age out faster from the buffer pool.

Both innodb\_old\_blocks\_pct and innodb\_old\_blocks\_time can be specified in the MySQL option file (my.cnf or my.ini) or changed at runtime with the SET GLOBAL statement. Changing

the value at runtime requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

To help you gauge the effect of setting these parameters, the SHOW ENGINE INNODB STATUS statement reports buffer pool statistics. For details, see Monitoring the Buffer Pool Using the InnoDB Standard Monitor.

Because the effects of these parameters can vary widely based on your hardware configuration, your data, and the details of your workload, always benchmark to verify the effectiveness before changing these settings in any performance-critical or production environment.

In mixed workloads where most of the activity is OLTP type with periodic batch reporting queries which result in large scans, setting the value of innodb\_old\_blocks\_time during the batch runs can help keep the working set of the normal workload in the buffer pool.

When scanning large tables that cannot fit entirely in the buffer pool, setting innodb\_old\_blocks\_pct to a small value keeps the data that is only read once from consuming a significant portion of the buffer pool. For example, setting innodb\_old\_blocks\_pct=5 restricts this data that is only read once to 5% of the buffer pool.

When scanning small tables that do fit into memory, there is less overhead for moving pages around within the buffer pool, so you can leave innodb\_old\_blocks\_pct at its default value, or even higher, such as innodb\_old\_blocks\_pct=50.

The effect of the innodb\_old\_blocks\_time parameter is harder to predict than the innodb\_old\_blocks\_pct parameter, is relatively small, and varies more with the workload. To arrive at an optimal value, conduct your own benchmarks if the performance improvement from adjusting innodb\_old\_blocks\_pct is not sufficient.

# <span id="page-96-0"></span>**17.8.3.4 Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)**

A read-ahead request is an I/O request to prefetch multiple pages in the buffer pool asynchronously, in anticipation of impending need for these pages. The requests bring in all the pages in one extent. InnoDB uses two read-ahead algorithms to improve I/O performance:

**Linear** read-ahead is a technique that predicts what pages might be needed soon based on pages in the buffer pool being accessed sequentially. You control when InnoDB performs a read-ahead operation by adjusting the number of sequential page accesses required to trigger an asynchronous read request, using the configuration parameter innodb\_read\_ahead\_threshold. Before this parameter was added, InnoDB would only calculate whether to issue an asynchronous prefetch request for the entire next extent when it read the last page of the current extent.

The configuration parameter innodb\_read\_ahead\_threshold controls how sensitive InnoDB is in detecting patterns of sequential page access. If the number of pages read sequentially from an extent is greater than or equal to innodb\_read\_ahead\_threshold, InnoDB initiates an asynchronous read-ahead operation of the entire following extent. innodb\_read\_ahead\_threshold can be set to any value from 0-64. The default value is 56. The higher the value, the more strict the access pattern check. For example, if you set the value to 48, InnoDB triggers a linear read-ahead request only when 48 pages in the current extent have been accessed sequentially. If the value is 8, InnoDB triggers an asynchronous read-ahead even if as few as 8 pages in the extent are accessed sequentially. You can set the value of this parameter in the MySQL configuration file, or change it dynamically with the SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

**Random** read-ahead is a technique that predicts when pages might be needed soon based on pages already in the buffer pool, regardless of the order in which those pages were read. If 13 consecutive pages from the same extent are found in the buffer pool, InnoDB asynchronously issues a request to prefetch the remaining pages of the extent. To enable this feature, set the configuration variable innodb\_random\_read\_ahead to ON.

The SHOW ENGINE INNODB STATUS statement displays statistics to help you evaluate the effectiveness of the read-ahead algorithm. Statistics include counter information for the following global status variables:

- Innodb\_buffer\_pool\_read\_ahead
- Innodb\_buffer\_pool\_read\_ahead\_evicted
- Innodb\_buffer\_pool\_read\_ahead\_rnd

This information can be useful when fine-tuning the innodb\_random\_read\_ahead setting.

For more information about I/O performance, see Section 10.5.8, "Optimizing InnoDB Disk I/O" and Section 10.12.1, "Optimizing Disk I/O".

# <span id="page-97-0"></span>**17.8.3.5 Configuring Buffer Pool Flushing**

InnoDB performs certain tasks in the background, including flushing of dirty pages from the buffer pool. Dirty pages are those that have been modified but are not yet written to the data files on disk.

Buffer pool flushing is performed by page cleaner threads. The number of page cleaner threads is controlled by the innodb\_page\_cleaners variable, which has a default value set to the same value as [innodb\\_buffer\\_pool\\_instances](#page-196-0).

Buffer pool flushing is initiated when the percentage of dirty pages reaches the low water mark value defined by the innodb\_max\_dirty\_pages\_pct\_lwm variable. The default low water mark is 10% of buffer pool pages. A innodb\_max\_dirty\_pages\_pct\_lwm value of 0 disables this early flushing behaviour.

The purpose of the innodb\_max\_dirty\_pages\_pct\_lwm threshold is to control the percentage dirty pages in the buffer pool and to prevent the amount of dirty pages from reaching the threshold defined by the innodb\_max\_dirty\_pages\_pct variable, which has a default value of 90. InnoDB aggressively flushes buffer pool pages if the percentage of dirty pages in the buffer pool reaches the innodb\_max\_dirty\_pages\_pct threshold.

When configuring innodb\_max\_dirty\_pages\_pct\_lwm, the value should always be lower than the innodb\_max\_dirty\_pages\_pct value.

Additional variables permit fine-tuning of buffer pool flushing behavior:

- The innodb\_flush\_neighbors variable defines whether flushing a page from the buffer pool also flushes other dirty pages in the same extent.
  - The default setting of 0 disables innodb\_flush\_neighbors. Dirty pages in the same extent are not flushed. This setting is recommended for non-rotational storage (SSD) devices where seek time is not a significant factor.
  - A setting of 1 flushes contiguous dirty pages in the same extent.
  - A setting of 2 flushes dirty pages in the same extent.

When table data is stored on a traditional HDD storage device, flushing neighbor pages in one operation reduces I/O overhead (primarily for disk seek operations) compared to flushing individual pages at different times. For table data stored on SSD, seek time is not a significant factor and you can disable this setting to spread out write operations.

• The innodb\_lru\_scan\_depth variable specifies, per buffer pool instance, how far down the buffer pool LRU list the page cleaner thread scans looking for dirty pages to flush. This is a background operation performed by a page cleaner thread once per second.

A setting smaller than the default is generally suitable for most workloads. A value that is significantly higher than necessary may impact performance. Only consider increasing the value if you have

spare I/O capacity under a typical workload. Conversely, if a write-intensive workload saturates your I/O capacity, decrease the value, especially in the case of a large buffer pool.

When tuning innodb\_lru\_scan\_depth, start with a low value and configure the setting upward with the goal of rarely seeing zero free pages. Also, consider adjusting innodb\_lru\_scan\_depth when changing the number of buffer pool instances, since innodb\_lru\_scan\_depth \* [innodb\\_buffer\\_pool\\_instances](#page-196-0) defines the amount of work performed by the page cleaner thread each second.

The innodb\_flush\_neighbors and innodb\_lru\_scan\_depth variables are primarily intended for write-intensive workloads. With heavy DML activity, flushing can fall behind if it is not aggressive enough, or disk writes can saturate I/O capacity if flushing is too aggressive. The ideal settings depend on your workload, data access patterns, and storage configuration (for example, whether data is stored on HDD or SSD devices).

### **Adaptive Flushing**

InnoDB uses an adaptive flushing algorithm to dynamically adjust the rate of flushing based on the speed of redo log generation and the current rate of flushing. The intent is to smooth overall performance by ensuring that flushing activity keeps pace with the current workload. Automatically adjusting the flushing rate helps avoid sudden dips in throughput that can occur when bursts of I/O activity due to buffer pool flushing affects the I/O capacity available for ordinary read and write activity.

Sharp checkpoints, which are typically associated with write-intensive workloads that generate a lot of redo entries, can cause a sudden change in throughput, for example. A sharp checkpoint occurs when InnoDB wants to reuse a portion of a log file. Before doing so, all dirty pages with redo entries in that portion of the log file must be flushed. If log files become full, a sharp checkpoint occurs, causing a temporary reduction in throughput. This scenario can occur even if innodb\_max\_dirty\_pages\_pct threshold is not reached.

The adaptive flushing algorithm helps avoid such scenarios by tracking the number of dirty pages in the buffer pool and the rate at which redo log records are being generated. Based on this information, it decides how many dirty pages to flush from the buffer pool each second, which permits it to manage sudden changes in workload.

The [innodb\\_adaptive\\_flushing\\_lwm](#page-189-0) variable defines a low water mark for redo log capacity. When that threshold is crossed, adaptive flushing is enabled, even if the [innodb\\_adaptive\\_flushing](#page-189-1) variable is disabled.

Internal benchmarking has shown that the algorithm not only maintains throughput over time, but can also improve overall throughput significantly. However, adaptive flushing can affect the I/O pattern of a workload significantly and may not be appropriate in all cases. It gives the most benefit when the redo log is in danger of filling up. If adaptive flushing is not appropriate to the characteristics of your workload, you can disable it. Adaptive flushing controlled by the [innodb\\_adaptive\\_flushing](#page-189-1) variable, which is enabled by default.

innodb\_flushing\_avg\_loops defines the number of iterations that InnoDB keeps the previously calculated snapshot of the flushing state, controlling how quickly adaptive flushing responds to foreground workload changes. A high innodb\_flushing\_avg\_loops value means that InnoDB keeps the previously calculated snapshot longer, so adaptive flushing responds more slowly. When setting a high value it is important to ensure that redo log utilization does not reach 75% (the hardcoded limit at which asynchronous flushing starts), and that the innodb\_max\_dirty\_pages\_pct threshold keeps the number of dirty pages to a level that is appropriate for the workload.

Systems with consistent workloads, a large log file size (innodb\_log\_file\_size), and small spikes that do not reach 75% log space utilization should use a high innodb\_flushing\_avg\_loops value to keep flushing as smooth as possible. For systems with extreme load spikes or log files that do not provide a lot of space, a smaller value allows flushing to closely track workload changes, and helps to avoid reaching 75% log space utilization.

Be aware that if flushing falls behind, the rate of buffer pool flushing can exceed the I/O capacity available to InnoDB, as defined by innodb\_io\_capacity setting. The innodb\_io\_capacity\_max value defines an upper limit on I/O capacity in such situations, so that a spike in I/O activity does not consume the entire I/O capacity of the server.

The innodb\_io\_capacity setting is applicable to all buffer pool instances. When dirty pages are flushed, I/O capacity is divided equally among buffer pool instances.

### **Limiting Buffer Flushing During Idle Periods**

The innodb\_idle\_flush\_pct variable limits the rate of buffer pool flushing during idle periods, which are periods of time that database pages are not modified. Its value is interpreted as a percentage of innodb\_io\_capacity (which defines the number of I/O operations per second available to InnoDB). The default value is 100, or 100 percent of the value of innodb\_io\_capacity. To limit flushing during idle periods, set innodb\_idle\_flush\_pct to less than 100.

Limiting page flushing during idle periods can help extend the life of solid state storage devices. Side effects of limiting page flushing during idle periods may include a longer shutdown time following a lengthy idle period, and a longer recovery period should a server failure occur.

## <span id="page-99-0"></span>**17.8.3.6 Saving and Restoring the Buffer Pool State**

To reduce the warmup period after restarting the server, InnoDB saves a percentage of the most recently used pages for each buffer pool at server shutdown and restores these pages at server startup. The percentage of recently used pages that is stored is defined by the [innodb\\_buffer\\_pool\\_dump\\_pct](#page-194-0) configuration option.

After restarting a busy server, there is typically a warmup period with steadily increasing throughput, as disk pages that were in the buffer pool are brought back into memory (as the same data is queried, updated, and so on). The ability to restore the buffer pool at startup shortens the warmup period by reloading disk pages that were in the buffer pool before the restart rather than waiting for DML operations to access corresponding rows. Also, I/O requests can be performed in large batches, making the overall I/O faster. Page loading happens in the background, and does not delay database startup.

In addition to saving the buffer pool state at shutdown and restoring it at startup, you can save and restore the buffer pool state at any time, while the server is running. For example, you can save the state of the buffer pool after reaching a stable throughput under a steady workload. You could also restore the previous buffer pool state after running reports or maintenance jobs that bring data pages into the buffer pool that are only requited for those operations, or after running some other non-typical workload.

Even though a buffer pool can be many gigabytes in size, the buffer pool data that InnoDB saves to disk is tiny by comparison. Only tablespace IDs and page IDs necessary to locate the appropriate pages are saved to disk. This information is derived from the INNODB\_BUFFER\_PAGE\_LRU INFORMATION\_SCHEMA table. By default, tablespace ID and page ID data is saved in a file named ib\_buffer\_pool, which is saved to the InnoDB data directory. The file name and location can be modified using the [innodb\\_buffer\\_pool\\_filename](#page-195-0) configuration parameter.

Because data is cached in and aged out of the buffer pool as it is with regular database operations, there is no problem if the disk pages are recently updated, or if a DML operation involves data that has not yet been loaded. The loading mechanism skips requested pages that no longer exist.

The underlying mechanism involves a background thread that is dispatched to perform the dump and load operations.

Disk pages from compressed tables are loaded into the buffer pool in their compressed form. Pages are uncompressed as usual when page contents are accessed during DML operations. Because uncompressing pages is a CPU-intensive process, it is more efficient for concurrency to perform the

operation in a connection thread rather than in the single thread that performs the buffer pool restore operation.

Operations related to saving and restoring the buffer pool state are described in the following topics:

- [Configuring the Dump Percentage for Buffer Pool Pages](#page-100-0)
- [Saving the Buffer Pool State at Shutdown and Restoring it at Startup](#page-100-1)
- [Saving and Restoring the Buffer Pool State Online](#page-100-2)
- [Displaying Buffer Pool Dump Progress](#page-100-3)
- [Displaying Buffer Pool Load Progress](#page-101-0)
- [Aborting a Buffer Pool Load Operation](#page-101-1)
- [Monitoring Buffer Pool Load Progress Using Performance Schema](#page-101-2)

### <span id="page-100-0"></span>**Configuring the Dump Percentage for Buffer Pool Pages**

Before dumping pages from the buffer pool, you can configure the percentage of most-recentlyused buffer pool pages that you want to dump by setting the [innodb\\_buffer\\_pool\\_dump\\_pct](#page-194-0) option. If you plan to dump buffer pool pages while the server is running, you can configure the option dynamically:

```
SET GLOBAL innodb_buffer_pool_dump_pct=40;
```

If you plan to dump buffer pool pages at server shutdown, set [innodb\\_buffer\\_pool\\_dump\\_pct](#page-194-0) in your configuration file.

```
[mysqld]
innodb_buffer_pool_dump_pct=40
```

The [innodb\\_buffer\\_pool\\_dump\\_pct](#page-194-0) default value is 25 (dump 25% of most-recently-used pages).

### <span id="page-100-1"></span>**Saving the Buffer Pool State at Shutdown and Restoring it at Startup**

To save the state of the buffer pool at server shutdown, issue the following statement prior to shutting down the server:

```
SET GLOBAL innodb_buffer_pool_dump_at_shutdown=ON;
innodb_buffer_pool_dump_at_shutdown is enabled by default.
```

To restore the buffer pool state at server startup, specify the --innodb-buffer-pool-load-atstartup option when starting the server:

```
mysqld --innodb-buffer-pool-load-at-startup=ON;
```

[innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-197-1) is enabled by default.

### <span id="page-100-2"></span>**Saving and Restoring the Buffer Pool State Online**

To save the state of the buffer pool while MySQL server is running, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_dump_now=ON;
```

To restore the buffer pool state while MySQL is running, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_load_now=ON;
```

### <span id="page-100-3"></span>**Displaying Buffer Pool Dump Progress**

To display progress when saving the buffer pool state to disk, issue the following statement:

```
SHOW STATUS LIKE 'Innodb_buffer_pool_dump_status';
```

If the operation has not yet started, "not started" is returned. If the operation is complete, the completion time is printed (e.g. Finished at 110505 12:18:02). If the operation is in progress, status information is provided (e.g. Dumping buffer pool 5/7, page 237/2873).

### <span id="page-101-0"></span>**Displaying Buffer Pool Load Progress**

To display progress when loading the buffer pool, issue the following statement:

```
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```

If the operation has not yet started, "not started" is returned. If the operation is complete, the completion time is printed (e.g. Finished at 110505 12:23:24). If the operation is in progress, status information is provided (e.g. Loaded 123/22301 pages).

### <span id="page-101-1"></span>**Aborting a Buffer Pool Load Operation**

To abort a buffer pool load operation, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_load_abort=ON;
```

### <span id="page-101-2"></span>**Monitoring Buffer Pool Load Progress Using Performance Schema**

You can monitor buffer pool load progress using Performance Schema.

The following example demonstrates how to enable the stage/innodb/buffer pool load stage event instrument and related consumer tables to monitor buffer pool load progress.

For information about buffer pool dump and load procedures used in this example, see [Section 17.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-99-0). For information about Performance Schema stage event instruments and related consumers, see Section 29.12.5, "Performance Schema Stage Event Tables".

1. Enable the stage/innodb/buffer pool load instrument:

```
mysql> UPDATE performance_schema.setup_instruments SET ENABLED = 'YES' 
 WHERE NAME LIKE 'stage/innodb/buffer%';
```

2. Enable the stage event consumer tables, which include events\_stages\_current, events\_stages\_history, and events\_stages\_history\_long.

```
mysql> UPDATE performance_schema.setup_consumers SET ENABLED = 'YES' 
 WHERE NAME LIKE '%stages%';
```

3. Dump the current buffer pool state by enabling [innodb\\_buffer\\_pool\\_dump\\_now](#page-194-1).

```
mysql> SET GLOBAL innodb_buffer_pool_dump_now=ON;
```

4. Check the buffer pool dump status to ensure that the operation has completed.

```
mysql> SHOW STATUS LIKE 'Innodb_buffer_pool_dump_status'\G
*************************** 1. row ***************************
Variable_name: Innodb_buffer_pool_dump_status
 Value: Buffer pool(s) dump completed at 150202 16:38:58
```

5. Load the buffer pool by enabling [innodb\\_buffer\\_pool\\_load\\_now](#page-197-2):

```
mysql> SET GLOBAL innodb_buffer_pool_load_now=ON;
```

6. Check the current status of the buffer pool load operation by querying the Performance Schema events\_stages\_current table. The WORK\_COMPLETED column shows the number of buffer pool pages loaded. The WORK\_ESTIMATED column provides an estimate of the remaining work, in pages.

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED
```

| ++++<br>  EVENT_NAME<br>  WORK_COMPLETED   WORK_ESTIMATED  <br>++++<br>  stage/innodb/buffer pool load  <br>5353  <br>7167  <br>++++ | FROM performance_schema.events_stages_current; |  |  |
|--------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|--|--|
|                                                                                                                                      |                                                |  |  |
|                                                                                                                                      |                                                |  |  |

The events\_stages\_current table returns an empty set if the buffer pool load operation has completed. In this case, you can check the events\_stages\_history table to view data for the completed event. For example:

| mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED<br>FROM performance_schema.events_stages_history;<br>++++ |      |                                 |
|--------------------------------------------------------------------------------------------------------------------|------|---------------------------------|
| EVENT_NAME                                                                                                         |      | WORK_COMPLETED   WORK_ESTIMATED |
| ++++<br>  stage/innodb/buffer pool load                                                                            | 7167 | 7167                            |
| ++++                                                                                                               |      |                                 |

![](_page_102_Picture_4.jpeg)

#### **Note**

You can also monitor buffer pool load progress using Performance Schema when loading the buffer pool at startup using [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-197-1). In this case, the stage/ innodb/buffer pool load instrument and related consumers must be enabled at startup. For more information, see Section 29.3, "Performance Schema Startup Configuration".

# <span id="page-102-0"></span>**17.8.3.7 Excluding or Including Buffer Pool Pages from Core Files**

A core file records the status and memory image of a running process. Because the buffer pool resides in main memory, and the memory image of a running process is dumped to the core file, systems with large buffer pools can produce large core files when the mysqld process dies.

Large core files can be problematic for a number of reasons including the time it takes to write them, the amount of disk space they consume, and the challenges associated with transferring large files.

Excluding buffer pool pages may also be desirable from a security perspective if you have concerns about dumping database pages to core files that may be shared inside or outside of your organization for debugging purposes.

![](_page_102_Picture_11.jpeg)

# **Note**

Access to the data present in buffer pool pages at the time the mysqld process died may be beneficial in some debugging scenarios. If in doubt whether to include or exclude buffer pool pages, consult MySQL Support.

The [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) option is only relevant if the core\_file variable is enabled and the operating system supports the MADV\_DONTDUMP non-POSIX extension to the [madvise\(\)](http://man7.org/linux/man-pages/man2/madvise.2.md) system call, which is supported in Linux 3.4 and later. The MADV\_DONTDUMP extension causes pages in a specified range to be excluded from core dumps. The [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) option is disabled by default on systems that support MADV\_DONTDUMP, otherwise it defaults to ON.

![](_page_102_Picture_15.jpeg)

### **Note**

Before MySQL 8.4, [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) was enabled by default instead of disabled.

To generate core files with buffer pool pages, start the server with the --core-file and [--innodb](#page-195-1)[buffer-pool-in-core-file=ON](#page-195-1) options.

\$> mysqld --core-file --innodb-buffer-pool-in-core-file=ON

The core\_file variable is read-only and disabled by default. It is enabled by specifying the --corefile option at startup. The [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) variable is dynamic. It can be specified at startup or configured at runtime using a SET statement.

```
mysql> SET GLOBAL innodb_buffer_pool_in_core_file=OFF;
```

If the [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) variable is disabled but MADV\_DONTDUMP is not supported by the operating system, or an madvise() failure occurs, a warning is written to the MySQL server error log and the core\_file variable is disabled to prevent writing core files that unintentionally include buffer pool pages. If the read-only core\_file variable becomes disabled, the server must be restarted to enable it again.

The following table shows configuration and MADV\_DONTDUMP support scenarios that determine whether core files are generated and whether they include buffer pool pages.

**Table 17.4 Core File Configuration Scenarios**

| core_file variable | innodb_buffer_pool_in_core_file<br>variable                    | madvise()<br>MADV_DONTDUMP<br>Support | Outcome                                                                                                         |  |
|--------------------|----------------------------------------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------|--|
| OFF (default)      | Not relevant to outcome                                        | Not relevant to outcome               | Core file is not<br>generated                                                                                   |  |
| ON                 | ON (default on<br>systems without<br>MADV_DONTDUMP<br>support) | Not relevant to outcome               | Core file is generated<br>with buffer pool pages                                                                |  |
| ON                 | OFF (default on systems<br>with MADV_DONTDUMP<br>support)      | Yes                                   | Core file is generated<br>without buffer pool<br>pages                                                          |  |
| ON                 | OFF                                                            | No                                    | Core file is not<br>generated, core_file<br>is disabled, and a<br>warning is written to the<br>server error log |  |

The reduction in core file size achieved by disabling the [innodb\\_buffer\\_pool\\_in\\_core\\_file](#page-195-1) variable depends on the size of the buffer pool, but it is also affected by the InnoDB page size. A smaller page size means more pages are required for the same amount of data, and more pages means more page metadata. The following table provides size reduction examples that you might see for a 1GB buffer pool with different pages sizes.

**Table 17.5 Core File Size with Buffer Pool Pages Included and Excluded**

| innodb_page_size Setting | Buffer Pool Pages Included<br>(innodb_buffer_pool_in_core_file=ON) | Buffer Pool Pages Excluded<br>(innodb_buffer_pool_in_core_file=OFF) |  |
|--------------------------|--------------------------------------------------------------------|---------------------------------------------------------------------|--|
| 4KB                      | 2.1GB                                                              | 0.9GB                                                               |  |
| 64KB                     | 1.7GB                                                              | 0.7GB                                                               |  |

# <span id="page-103-0"></span>**17.8.4 Configuring Thread Concurrency for InnoDB**

InnoDB uses operating system threads to process requests from user transactions. (Transactions may issue many requests to InnoDB before they commit or roll back.) On modern operating systems and servers with multi-core processors, where context switching is efficient, most workloads run well without any limit on the number of concurrent threads.

In situations where it is helpful to minimize context switching between threads, InnoDB can use a number of techniques to limit the number of concurrently executing operating system threads (and thus the number of requests that are processed at any one time). When InnoDB receives a new request

from a user session, if the number of threads concurrently executing is at a pre-defined limit, the new request sleeps for a short time before it tries again. Threads waiting for locks are not counted in the number of concurrently executing threads.

You can limit the number of concurrent threads by setting the configuration parameter innodb\_thread\_concurrency. Once the number of executing threads reaches this limit, additional threads sleep for a number of microseconds, set by the configuration parameter innodb\_thread\_sleep\_delay, before being placed into the queue.

You can set the configuration option [innodb\\_adaptive\\_max\\_sleep\\_delay](#page-190-0) to the highest value you would allow for innodb\_thread\_sleep\_delay, and InnoDB automatically adjusts innodb\_thread\_sleep\_delay up or down depending on the current thread-scheduling activity. This dynamic adjustment helps the thread scheduling mechanism to work smoothly during times when the system is lightly loaded and when it is operating near full capacity.

The default value for innodb\_thread\_concurrency and the implied default limit on the number of concurrent threads has been changed in various releases of MySQL and InnoDB. The default value of innodb\_thread\_concurrency is 0, so that by default there is no limit on the number of concurrently executing threads.

InnoDB causes threads to sleep only when the number of concurrent threads is limited. When there is no limit on the number of threads, all contend equally to be scheduled. That is, if innodb\_thread\_concurrency is 0, the value of innodb\_thread\_sleep\_delay is ignored.

When there is a limit on the number of threads (when innodb\_thread\_concurrency is > 0), InnoDB reduces context switching overhead by permitting multiple requests made during the execution of a single SQL statement to enter InnoDB without observing the limit set by innodb\_thread\_concurrency. Since an SQL statement (such as a join) may comprise multiple row operations within InnoDB, InnoDB assigns a specified number of "tickets" that allow a thread to be scheduled repeatedly with minimal overhead.

When a new SQL statement starts, a thread has no tickets, and it must observe innodb\_thread\_concurrency. Once the thread is entitled to enter InnoDB, it is assigned a number of tickets that it can use for subsequently entering InnoDB to perform row operations. If the tickets run out, the thread is evicted, and innodb\_thread\_concurrency is observed again which may place the thread back into the first-in/first-out queue of waiting threads. When the thread is once again entitled to enter InnoDB, tickets are assigned again. The number of tickets assigned is specified by the global option innodb\_concurrency\_tickets, which is 5000 by default. A thread that is waiting for a lock is given one ticket once the lock becomes available.

The correct values of these variables depend on your environment and workload. Try a range of different values to determine what value works for your applications. Before limiting the number of concurrently executing threads, review configuration options that may improve the performance of InnoDB on multi-core and multi-processor computers, such as [innodb\\_adaptive\\_hash\\_index](#page-190-1).

For general performance information about MySQL thread handling, see Section 7.1.12.1, "Connection Interfaces".

# <span id="page-104-0"></span>**17.8.5 Configuring the Number of Background InnoDB I/O Threads**

InnoDB uses background threads to service various types of I/O requests. You can configure the number of background threads that service read and write I/O on data pages using the innodb\_read\_io\_threads and innodb\_write\_io\_threads configuration parameters. These parameters signify the number of background threads used for read and write requests, respectively. They are effective on all supported platforms. You can set values for these parameters in the MySQL option file (my.cnf or my.ini); you cannot change values dynamically. The default value for innodb\_read\_io\_threads is the number of available logical processors on the system divided by 2, with a minimum default value of 4. The default value for innodb\_write\_io\_threads is 4. The permissible values range from 1-64 for both options.

The purpose of these configuration options to make InnoDB more scalable on high end systems. Each background thread can handle up to 256 pending I/O requests. A major source of background I/O is read-ahead requests. InnoDB tries to balance the load of incoming requests in such way that most background threads share work equally. InnoDB also attempts to allocate read requests from the same extent to the same thread, to increase the chances of coalescing the requests. If you have a high end I/O subsystem and you see more than 64 × innodb\_read\_io\_threads pending read requests in SHOW ENGINE INNODB STATUS output, you might improve performance by increasing the value of innodb\_read\_io\_threads.

On Linux systems, InnoDB uses the asynchronous I/O subsystem by default to perform read-ahead and write requests for data file pages, which changes the way that InnoDB background threads service these types of I/O requests. For more information, see [Section 17.8.6, "Using Asynchronous I/O on](#page-105-0) [Linux"](#page-105-0).

For more information about InnoDB I/O performance, see Section 10.5.8, "Optimizing InnoDB Disk I/ O".

# <span id="page-105-0"></span>**17.8.6 Using Asynchronous I/O on Linux**

InnoDB uses the asynchronous I/O subsystem (native AIO) on Linux to perform read-ahead and write requests for data file pages. This behavior is controlled by the innodb\_use\_native\_aio configuration option, which applies to Linux systems only and is enabled by default. On other Unixlike systems, InnoDB uses synchronous I/O only. Historically, InnoDB only used asynchronous I/O on Windows systems. Using the asynchronous I/O subsystem on Linux requires the libaio library.

With synchronous I/O, query threads queue I/O requests, and InnoDB background threads retrieve the queued requests one at a time, issuing a synchronous I/O call for each. When an I/O request is completed and the I/O call returns, the InnoDB background thread that is handling the request calls an I/O completion routine and returns to process the next request. The number of requests that can be processed in parallel is n, where n is the number of InnoDB background threads. The number of InnoDB background threads is controlled by innodb\_read\_io\_threads and innodb\_write\_io\_threads. See [Section 17.8.5, "Configuring the Number of Background InnoDB I/](#page-104-0) [O Threads".](#page-104-0)

With native AIO, query threads dispatch I/O requests directly to the operating system, thereby removing the limit imposed by the number of background threads. InnoDB background threads wait for I/O events to signal completed requests. When a request is completed, a background thread calls an I/ O completion routine and resumes waiting for I/O events.

The advantage of native AIO is scalability for heavily I/O-bound systems that typically show many pending reads and writes in SHOW ENGINE INNODB STATUS output. The increase in parallel processing when using native AIO means that the type of I/O scheduler or properties of the disk array controller have a greater influence on I/O performance.

A potential disadvantage of native AIO for heavily I/O-bound systems is lack of control over the number of I/O write requests dispatched to the operating system at once. Too many I/O write requests dispatched to the operating system for parallel processing could, in some cases, result in I/O read starvation, depending on the amount of I/O activity and system capabilities.

If a problem with the asynchronous I/O subsystem in the OS prevents InnoDB from starting, you can start the server with innodb\_use\_native\_aio=0. This option may also be disabled automatically during startup if InnoDB detects a potential problem such as a combination of tmpdir location, tmpfs file system, and Linux kernel that does not support asynchronous I/O on tmpfs.