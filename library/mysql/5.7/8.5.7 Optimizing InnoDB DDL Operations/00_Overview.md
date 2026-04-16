---
source: MySQL 5.7 Reference
title: 00_Overview
---

- Many DDL operations on tables and indexes (CREATE, ALTER, and DROP statements) can be performed online. See Section 14.13, "InnoDB and Online DDL" for details.
- Online DDL support for adding secondary indexes means that you can generally speed up the process of creating and loading a table and associated indexes by creating the table without secondary indexes, then adding secondary indexes after the data is loaded.
- Use TRUNCATE TABLE to empty a table, not DELETE FROM tbl\_name. Foreign key constraints can make a TRUNCATE statement work like a regular DELETE statement, in which case a sequence of commands like DROP TABLE and CREATE TABLE might be fastest.
- Because the primary key is integral to the storage layout of each InnoDB table, and changing the definition of the primary key involves reorganizing the whole table, always set up the primary key as part of the CREATE TABLE statement, and plan ahead so that you do not need to ALTER or DROP the primary key afterward.

# <span id="page-59-0"></span>**8.5.8 Optimizing InnoDB Disk I/O**

If you follow best practices for database design and tuning techniques for SQL operations, but your database is still slow due to heavy disk I/O activity, consider these disk I/O optimizations. If the Unix top tool or the Windows Task Manager shows that the CPU usage percentage with your workload is less than 70%, your workload is probably disk-bound.

• Increase buffer pool size

When table data is cached in the InnoDB buffer pool, it can be accessed repeatedly by queries without requiring any disk I/O. Specify the size of the buffer pool with the innodb\_buffer\_pool\_size option. This memory area is important enough that it is typically recommended that innodb\_buffer\_pool\_size is configured to 50 to 75 percent of system memory. For more information see, [Section 8.12.4.1, "How MySQL Uses Memory".](#page-128-0)

• Adjust the flush method

In some versions of GNU/Linux and Unix, flushing files to disk with the Unix fsync() call (which InnoDB uses by default) and similar methods is surprisingly slow. If database write performance is an issue, conduct benchmarks with the innodb\_flush\_method parameter set to O\_DSYNC.

• Use a noop or deadline I/O scheduler with native AIO on Linux

InnoDB uses the asynchronous I/O subsystem (native AIO) on Linux to perform read-ahead and write requests for data file pages. This behavior is controlled by the innodb\_use\_native\_aio configuration option, which is enabled by default. With native AIO, the type of I/O scheduler

has greater influence on I/O performance. Generally, noop and deadline I/O schedulers are recommended. Conduct benchmarks to determine which I/O scheduler provides the best results for your workload and environment. For more information, see Section 14.8.7, "Using Asynchronous I/O on Linux".

• Use direct I/O on Solaris 10 for x86\_64 architecture

When using the InnoDB storage engine on Solaris 10 for x86\_64 architecture (AMD Opteron), use direct I/O for InnoDB-related files to avoid degradation of InnoDB performance. To use direct I/O for an entire UFS file system used for storing InnoDB-related files, mount it with the forcedirectio option; see mount\_ufs(1M). (The default on Solaris 10/x86\_64 is not to use this option.) To apply direct I/O only to InnoDB file operations rather than the whole file system, set innodb\_flush\_method = O\_DIRECT. With this setting, InnoDB calls directio() instead of fcntl() for I/O to data files (not for I/O to log files).

• Use raw storage for data and log files with Solaris 2.6 or later

When using the InnoDB storage engine with a large innodb\_buffer\_pool\_size value on any release of Solaris 2.6 and up and any platform (sparc/x86/x64/amd64), conduct benchmarks with InnoDB data files and log files on raw devices or on a separate direct I/O UFS file system, using the forcedirectio mount option as described previously. (It is necessary to use the mount option rather than setting innodb\_flush\_method if you want direct I/O for the log files.) Users of the Veritas file system VxFS should use the convosync=direct mount option.

Do not place other MySQL data files, such as those for MyISAM tables, on a direct I/O file system. Executables or libraries must not be placed on a direct I/O file system.

• Use additional storage devices

Additional storage devices could be used to set up a RAID configuration. For related information, see [Section 8.12.2, "Optimizing Disk I/O".](#page-124-0)

Alternatively, InnoDB tablespace data files and log files can be placed on different physical disks. For more information, refer to the following sections:

- Section 14.8.1, "InnoDB Startup Configuration"
- Section 14.6.1.2, "Creating Tables Externally"
- Creating a General Tablespace
- Section 14.6.1.4, "Moving or Copying InnoDB Tables"
- Consider non-rotational storage

Non-rotational storage generally provides better performance for random I/O operations; and rotational storage for sequential I/O operations. When distributing data and log files across rotational and non-rotational storage devices, consider the type of I/O operations that are predominantly performed on each file.

Random I/O-oriented files typically include file-per-table and general tablespace data files, undo tablespace files, and temporary tablespace files. Sequential I/O-oriented files include InnoDB

system tablespace files (due to doublewrite buffering and change buffering) and log files such as binary log files and redo log files.

Review settings for the following configuration options when using non-rotational storage:

• innodb\_checksum\_algorithm

The crc32 option uses a faster checksum algorithm and is recommended for fast storage systems.

• innodb\_flush\_neighbors

Optimizes I/O for rotational storage devices. Disable it for non-rotational storage or a mix of rotational and non-rotational storage.

• innodb\_io\_capacity

The default setting of 200 is generally sufficient for a lower-end non-rotational storage device. For higher-end, bus-attached devices, consider a higher setting such as 1000.

• innodb\_io\_capacity\_max

The default value of 2000 is intended for workloads that use non-rotational storage. For a highend, bus-attached non-rotational storage device, consider a higher setting such as 2500.

• innodb\_log\_compressed\_pages

If redo logs are on non-rotational storage, consider disabling this option to reduce logging. See [Disable logging of compressed pages.](#page-62-0)

• innodb\_log\_file\_size

If redo logs are on non-rotational storage, configure this option to maximize caching and write combining.

• innodb\_page\_size

Consider using a page size that matches the internal sector size of the disk. Early-generation SSD devices often have a 4KB sector size. Some newer devices have a 16KB sector size. The default InnoDB page size is 16KB. Keeping the page size close to the storage device block size minimizes the amount of unchanged data that is rewritten to disk.

• binlog\_row\_image

If binary logs are on non-rotational storage and all tables have primary keys, consider setting this option to minimal to reduce logging.

Ensure that TRIM support is enabled for your operating system. It is typically enabled by default.

• Increase I/O capacity to avoid backlogs

If throughput drops periodically because of InnoDB checkpoint operations, consider increasing the value of the innodb\_io\_capacity configuration option. Higher values cause more frequent flushing, avoiding the backlog of work that can cause dips in throughput.

• Lower I/O capacity if flushing does not fall behind

If the system is not falling behind with InnoDB flushing operations, consider lowering the value of the innodb\_io\_capacity configuration option. Typically, you keep this option value as low as practical, but not so low that it causes periodic drops in throughput as mentioned in the preceding bullet. In a typical scenario where you could lower the option value, you might see a combination like this in the output from SHOW ENGINE INNODB STATUS:

- History list length low, below a few thousand.
- Insert buffer merges close to rows inserted.
- Modified pages in buffer pool consistently well below innodb\_max\_dirty\_pages\_pct of the buffer pool. (Measure at a time when the server is not doing bulk inserts; it is normal during bulk inserts for the modified pages percentage to rise significantly.)
- Log sequence number Last checkpoint is at less than 7/8 or ideally less than 6/8 of the total size of the InnoDB log files.
- Store system tablespace files on Fusion-io devices

You can take advantage of a doublewrite buffer-related I/O optimization by storing system tablespace files ("ibdata files") on Fusion-io devices that support atomic writes. In this case, doublewrite buffering (innodb\_doublewrite) is automatically disabled and Fusion-io atomic writes are used for all data files. This feature is only supported on Fusion-io hardware and is only enabled for Fusion-io NVMFS on Linux. To take full advantage of this feature, an innodb\_flush\_method setting of O\_DIRECT is recommended.

![](_page_62_Picture_7.jpeg)

#### **Note**

Because the doublewrite buffer setting is global, doublewrite buffering is also disabled for data files residing on non-Fusion-io hardware.

<span id="page-62-0"></span>• Disable logging of compressed pages

When using the InnoDB table compression feature, images of re-compressed pages are written to the redo log when changes are made to compressed data. This behavior is controlled by innodb\_log\_compressed\_pages, which is enabled by default to prevent corruption that can occur if a different version of the zlib compression algorithm is used during recovery. If you are certain that the zlib version is not subject to change, disable innodb\_log\_compressed\_pages to reduce redo log generation for workloads that modify compressed data.