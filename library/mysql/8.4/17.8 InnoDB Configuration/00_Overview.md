---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section provides configuration information and procedures for InnoDB initialization, startup, and various components and features of the InnoDB storage engine. For information about optimizing database operations for InnoDB tables, see Section 10.5, "Optimizing for InnoDB Tables".

# <span id="page-81-0"></span>**17.8.1 InnoDB Startup Configuration**

The first decisions to make about InnoDB configuration involve the configuration of data files, log files, page size, and memory buffers, which should be configured before initializing InnoDB. Modifying the configuration after InnoDB is initialized may involve non-trivial procedures.

This section provides information about specifying InnoDB settings in a configuration file, viewing InnoDB initialization information, and important storage considerations.

- [Specifying Options in a MySQL Option File](#page-82-0)
- [Viewing InnoDB Initialization Information](#page-82-1)
- [Important Storage Considerations](#page-82-2)
- [System Tablespace Data File Configuration](#page-83-0)
- [InnoDB Doublewrite Buffer File Configuration](#page-84-0)

- [Redo Log Configuration](#page-85-0)
- [Undo Tablespace Configuration](#page-85-1)
- [Global Temporary Tablespace Configuration](#page-86-0)
- [Session Temporary Tablespace Configuration](#page-86-1)
- [Page Size Configuration](#page-86-2)
- [Memory Configuration](#page-86-3)

# <span id="page-82-0"></span>**Specifying Options in a MySQL Option File**

Because MySQL uses data file, log file, and page size settings to initialize InnoDB, it is recommended that you define these settings in an option file that MySQL reads at startup, prior to initializing InnoDB. Normally, InnoDB is initialized when the MySQL server is started for the first time.

You can place InnoDB options in the [mysqld] group of any option file that your server reads when it starts. The locations of MySQL option files are described in Section 6.2.2.2, "Using Option Files".

To make sure that mysqld reads options only from a specific file (and mysqld-auto.cnf), use the --defaults-file option as the first option on the command line when starting the server:

mysqld --defaults-file=path\_to\_option\_file

# <span id="page-82-1"></span>**Viewing InnoDB Initialization Information**

To view InnoDB initialization information during startup, start mysqld from a command prompt, which prints initialization information to the console.

For example, on Windows, if mysqld is located in C:\Program Files\MySQL\MySQL Server 8.4\bin, start the MySQL server like this:

C:\> **"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld" --console**

On Unix-like systems, mysqld is located in the bin directory of your MySQL installation:

```
$> bin/mysqld --user=mysql &
```

If you do not send server output to the console, check the error log after startup to see the initialization information InnoDB printed during the startup process.

For information about starting MySQL using other methods, see Section 2.9.5, "Starting and Stopping MySQL Automatically".

![](_page_82_Picture_20.jpeg)

### **Note**

InnoDB does not open all user tables and associated data files at startup. However, InnoDB does check for the existence of tablespace files referenced in the data dictionary. If a tablespace file is not found, InnoDB logs an error and continues the startup sequence. Tablespace files referenced in the redo log may be opened during crash recovery for redo application.

## <span id="page-82-2"></span>**Important Storage Considerations**

Review the following storage-related considerations before proceeding with your startup configuration.

- In some cases, you can improve database performance by placing data and log files on separate physical disks. You can also use raw disk partitions (raw devices) for InnoDB data files, which may speed up I/O. See [Using Raw Disk Partitions for the System Tablespace](#page-29-0).
- InnoDB is a transaction-safe (ACID compliant) storage engine with commit, rollback, and crashrecovery capabilities to protect user data. **However, it cannot do so** if the underlying operating

system or hardware does not work as advertised. Many operating systems or disk subsystems may delay or reorder write operations to improve performance. On some operating systems, the very fsync() system call that should wait until all unwritten data for a file has been flushed might actually return before the data has been flushed to stable storage. Because of this, an operating system crash or a power outage may destroy recently committed data, or in the worst case, even corrupt the database because write operations have been reordered. If data integrity is important to you, perform "pull-the-plug" tests before using anything in production. On macOS, InnoDB uses a special fcntl() file flush method. Under Linux, it is advisable to **disable the write-back cache**.

On ATA/SATA disk drives, a command such hdparm -W0 /dev/hda may work to disable the write-back cache. **Beware that some drives or disk controllers may be unable to disable the write-back cache.**

- With regard to InnoDB recovery capabilities that protect user data, InnoDB uses a file flush technique involving a structure called the doublewrite buffer, which is enabled by default (innodb\_doublewrite=ON). The doublewrite buffer adds safety to recovery following an unexpected exit or power outage, and improves performance on most varieties of Unix by reducing the need for fsync() operations. It is recommended that the innodb\_doublewrite option remains enabled if you are concerned with data integrity or possible failures. For information about the doublewrite buffer, see [Section 17.11.1, "InnoDB Disk I/O"](#page-148-1).
- Before using NFS with InnoDB, review potential issues outlined in Using NFS with MySQL.

# <span id="page-83-0"></span>**System Tablespace Data File Configuration**

The innodb\_data\_file\_path option defines the name, size, and attributes of InnoDB system tablespace data files. If you do not configure this option prior to initializing the MySQL server, the default behavior is to create a single auto-extending data file, slightly larger than 12MB, named ibdata1:

```
mysql> SHOW VARIABLES LIKE 'innodb_data_file_path';
+-----------------------+------------------------+
| Variable_name | Value |
+-----------------------+------------------------+
| innodb_data_file_path | ibdata1:12M:autoextend |
+-----------------------+------------------------+
```

The full data file specification syntax includes the file name, file size, autoextend attribute, and max attribute:

```
file_name:file_size[:autoextend[:max:max_file_size]]
```

File sizes are specified in kilobytes, megabytes, or gigabytes by appending K, M or G to the size value. If specifying the data file size in kilobytes, do so in multiples of 1024. Otherwise, kilobyte values are rounded to nearest megabyte (MB) boundary. The sum of file sizes must be, at a minimum, slightly larger than 12MB.

You can specify more than one data file using a semicolon-separated list. For example:

```
[mysqld]
innodb_data_file_path=ibdata1:50M;ibdata2:50M:autoextend
```

The autoextend and max attributes can be used only for the data file that is specified last.

When the autoextend attribute is specified, the data file automatically increases in size by 64MB increments as space is required. The [innodb\\_autoextend\\_increment](#page-191-1) variable controls the increment size.

To specify a maximum size for an auto-extending data file, use the max attribute following the autoextend attribute. Use the max attribute only in cases where constraining disk usage is of critical importance. The following configuration permits ibdata1 to grow to a limit of 500MB:

```
[mysqld]
innodb_data_file_path=ibdata1:12M:autoextend:max:500M
```

A minimum file size is enforced for the first system tablespace data file to ensure that there is enough space for doublewrite buffer pages. The following table shows minimum file sizes for each InnoDB page size. The default InnoDB page size is 16384 (16KB).

| Page Size (innodb_page_size) | Minimum File Size |
|------------------------------|-------------------|
| 16384 (16KB) or less         | 5MB               |
| 32768 (32KB)                 | 6MB               |
| 65536 (64KB)                 | 12MB              |

If your disk becomes full, you can add a data file on another disk. For instructions, see [Resizing the](#page-28-0) [System Tablespace.](#page-28-0)

The size limit for individual files is determined by your operating system. You can set the file size to more than 4GB on operating systems that support large files. You can also use raw disk partitions as data files. See [Using Raw Disk Partitions for the System Tablespace.](#page-29-0)

InnoDB is not aware of the file system maximum file size, so be cautious on file systems where the maximum file size is a small value such as 2GB.

System tablespace files are created in the data directory by default (datadir). To specify an alternate location, use the innodb\_data\_home\_dir option. For example, to create a system tablespace data file in a directory named myibdata, use this configuration:

```
[mysqld]
innodb_data_home_dir = /myibdata/
innodb_data_file_path=ibdata1:50M:autoextend
```

A trailing slash is required when specifying a value for innodb\_data\_home\_dir. InnoDB does not create directories, so ensure that the specified directory exists before you start the server. Also, ensure sure that the MySQL server has the proper access rights to create files in the directory.

InnoDB forms the directory path for each data file by textually concatenating the value of innodb\_data\_home\_dir to the data file name. If innodb\_data\_home\_dir is not defined, the default value is "./", which is the data directory. (The MySQL server changes its current working directory to the data directory when it begins executing.)

Alternatively, you can specify an absolute path for system tablespace data files. The following configuration is equivalent to the preceding one:

```
[mysqld]
innodb_data_file_path=/myibdata/ibdata1:50M:autoextend
```

When you specify an absolute path for innodb\_data\_file\_path, the setting is not concatenated with the innodb\_data\_home\_dir setting. System tablespace files are created in the specified absolute path. The specified directory must exist before you start the server.

## <span id="page-84-0"></span>**InnoDB Doublewrite Buffer File Configuration**

The InnoDB doublewrite buffer storage area resides in doublewrite files, which provides flexibility with respect to the storage location of doublewrite pages. In previous releases, the doublewrite buffer storage area resided in the system tablespace. The innodb\_doublewrite\_dir variable defines the directory where InnoDB creates doublewrite files at startup. If no directory is specified, doublewrite files are created in the innodb\_data\_home\_dir directory, which defaults to the data directory if unspecified.

To have doublewrite files created in a location other than the innodb\_data\_home\_dir directory, configure innodb\_doublewrite\_dir variable. For example:

```
innodb_doublewrite_dir=/path/to/doublewrite_directory
```

Other doublewrite buffer variables permit defining the number of doublewrite files, the number of pages per thread, and the doublewrite batch size. For more information about doublewrite buffer configuration, see [Section 17.6.4, "Doublewrite Buffer"](#page-48-0).

# <span id="page-85-0"></span>**Redo Log Configuration**

The amount of disk space occupied by redo log files is controlled by the innodb\_redo\_log\_capacity variable, which can be set at startup or runtime; for example, to set the variable to 8GiB in an option file, add the following entry:

```
[mysqld]
innodb_redo_log_capacity = 8589934592
```

For information about configuring redo log capacity at runtime, see [Configuring Redo Log Capacity.](#page-50-0)

The innodb\_redo\_log\_capacity variable supersedes the innodb\_log\_file\_size and innodb\_log\_files\_in\_group variables, which are deprecated. When the innodb\_redo\_log\_capacity setting is defined, the innodb\_log\_file\_size and innodb\_log\_files\_in\_group settings are ignored; otherwise, if one or both of these deprecated settings are defined then they are used to compute Innodb\_redo\_log\_capacity\_resized as (innodb\_log\_files\_in\_group \* innodb\_log\_file\_size). If none of those variables are set, then the default innodb\_redo\_log\_capacity value is used.

InnoDB attempts to maintain 32 redo log files, with each file equal to 1/32 \* innodb\_redo\_log\_capacity. The redo log files reside in the #innodb\_redo directory in the data directory unless a different directory was specified by the innodb\_log\_group\_home\_dir variable. If innodb\_log\_group\_home\_dir was defined, the redo log files reside in the #innodb\_redo directory in that directory. For more information, see [Section 17.6.5, "Redo Log".](#page-50-1)

You can define a different number of redo log files and different redo log file size when initializing the MySQL Server instance by configuring the innodb\_log\_files\_in\_group and innodb\_log\_file\_size variables.

innodb\_log\_files\_in\_group defines the number of log files in the log group. The default and recommended value is 2.

innodb\_log\_file\_size defines the size in bytes of each log file in the log group. The combined log file size (innodb\_log\_file\_size \* innodb\_log\_files\_in\_group) cannot exceed the maximum value, which is slightly less than 512GB. A pair of 255 GB log files, for example, approaches the limit but does not exceed it. The default log file size is 48MB. Generally, the combined size of the log files should be large enough that the server can smooth out peaks and troughs in workload activity, which often means that there is enough redo log space to handle more than an hour of write activity. A larger log file size means less checkpoint flush activity in the buffer pool, which reduces disk I/O. For additional information, see Section 10.5.4, "Optimizing InnoDB Redo Logging".

The innodb\_log\_group\_home\_dir defines the directory path to the InnoDB log files. You might use this option to place InnoDB redo log files in a different physical storage location than InnoDB data files to avoid potential I/O resource conflicts; for example:

```
[mysqld]
innodb_log_group_home_dir = /dr3/iblogs
```

![](_page_85_Picture_12.jpeg)

#### **Note**

InnoDB does not create directories, so make sure that the log directory exists before you start the server. Use the Unix or DOS mkdir command to create any necessary directories.

Make sure that the MySQL server has the proper access rights to create files in the log directory. More generally, the server must have access rights in any directory where it needs to create files.

## <span id="page-85-1"></span>**Undo Tablespace Configuration**

Undo logs, by default, reside in two undo tablespaces created when the MySQL instance is initialized.

The innodb\_undo\_directory variable defines the path where InnoDB creates default undo tablespaces. If that variable is undefined, default undo tablespaces are created in the data directory. The innodb\_undo\_directory variable is not dynamic. Configuring it requires restarting the server.

The I/O patterns for undo logs make undo tablespaces good candidates for SSD storage.

For information about configuring additional undo tablespaces, see [Section 17.6.3.4, "Undo](#page-37-1) [Tablespaces"](#page-37-1).

# <span id="page-86-0"></span>**Global Temporary Tablespace Configuration**

The global temporary tablespace stores rollback segments for changes made to user-created temporary tables.

A single auto-extending global temporary tablespace data file named ibtmp1 in the innodb\_data\_home\_dir directory by default. The initial file size is slightly larger than 12MB.

The innodb\_temp\_data\_file\_path option specifies the path, file name, and file size for global temporary tablespace data files. File size is specified in KB, MB, or GB by appending K, M, or G to the size value. The file size or combined file size must be slightly larger than 12MB.

To specify an alternate location for global temporary tablespace data files, configure the innodb\_temp\_data\_file\_path option at startup.

## <span id="page-86-1"></span>**Session Temporary Tablespace Configuration**

In MySQL 8.4, InnoDB is always used as the on-disk storage engine for internal temporary tables.

The innodb\_temp\_tablespaces\_dir variable defines the location where InnoDB creates session temporary tablespaces. The default location is the #innodb\_temp directory in the data directory.

To specify an alternate location for session temporary tablespaces, configure the innodb\_temp\_tablespaces\_dir variable at startup. A fully qualified path or path relative to the data directory is permitted.

# <span id="page-86-2"></span>**Page Size Configuration**

The innodb\_page\_size option specifies the page size for all InnoDB tablespaces in a MySQL instance. This value is set when the instance is created and remains constant afterward. Valid values are 64KB, 32KB, 16KB (the default), 8KB, and 4KB. Alternatively, you can specify page size in bytes (65536, 32768, 16384, 8192, 4096).

The default 16KB page size is appropriate for a wide range of workloads, particularly for queries involving table scans and DML operations involving bulk updates. Smaller page sizes might be more efficient for OLTP workloads involving many small writes, where contention can be an issue when a single page contains many rows. Smaller pages can also be more efficient for SSD storage devices, which typically use small block sizes. Keeping the InnoDB page size close to the storage device block size minimizes the amount of unchanged data that is rewritten to disk.

![](_page_86_Picture_16.jpeg)

#### **Important**

innodb\_page\_size can be set only when initializing the data directory. See the description of this variable for more information.

## <span id="page-86-3"></span>**Memory Configuration**

MySQL allocates memory to various caches and buffers to improve performance of database operations. When allocating memory for InnoDB, always consider memory required by the operating system, memory allocated to other applications, and memory allocated for other MySQL buffers and caches. For example, if you use MyISAM tables, consider the amount of memory allocated for the key buffer (key\_buffer\_size). For an overview of MySQL buffers and caches, see Section 10.12.3.1, "How MySQL Uses Memory".

Buffers specific to InnoDB are configured using the following parameters:

• [innodb\\_buffer\\_pool\\_size](#page-197-0) defines size of the buffer pool, which is the memory area that holds cached data for InnoDB tables, indexes, and other auxiliary buffers. The size of the buffer pool is important for system performance, and it is typically recommended that [innodb\\_buffer\\_pool\\_size](#page-197-0) is configured to 50 to 75 percent of system memory. The default buffer pool size is 128MB. For additional guidance, see Section 10.12.3.1, "How MySQL Uses Memory". For information about how to configure InnoDB buffer pool size, see [Section 17.8.3.1,](#page-89-0) ["Configuring InnoDB Buffer Pool Size"](#page-89-0). Buffer pool size can be configured at startup or dynamically.

On systems with a large amount of memory, you can improve concurrency by dividing the buffer pool into multiple buffer pool instances. The number of buffer pool instances is controlled by the by [innodb\\_buffer\\_pool\\_instances](#page-196-0) option. By default, InnoDB creates one buffer pool instance. The number of buffer pool instances can be configured at startup. For more information, see [Section 17.8.3.2, "Configuring Multiple Buffer Pool Instances".](#page-95-0)

• innodb\_log\_buffer\_size defines the size of the buffer that InnoDB uses to write to the log files on disk. The default size is 64MB. A large log buffer enables large transactions to run without writing the log to disk before the transactions commit. If you have transactions that update, insert, or delete many rows, you might consider increasing the size of the log buffer to save disk I/O. innodb\_log\_buffer\_size can be configured at startup. For related information, see Section 10.5.4, "Optimizing InnoDB Redo Logging".

![](_page_87_Picture_5.jpeg)

#### **Warning**

On 32-bit GNU/Linux x86, if memory usage is set too high, glibc may permit the process heap to grow over the thread stacks, causing a server failure. It is a risk if the memory allocated to the mysqld process for global and per-thread buffers and caches is close to or exceeds 2GB.

A formula similar to the following that calculates global and per-thread memory allocation for MySQL can be used to estimate MySQL memory usage. You may need to modify the formula to account for buffers and caches in your MySQL version and configuration. For an overview of MySQL buffers and caches, see Section 10.12.3.1, "How MySQL Uses Memory".

```
innodb_buffer_pool_size
+ key_buffer_size
+ max_connections*(sort_buffer_size+read_buffer_size+binlog_cache_size)
+ max_connections*2MB
```

Each thread uses a stack (often 2MB, but only 256KB in MySQL binaries provided by Oracle Corporation.) and in the worst case also uses sort\_buffer\_size + read\_buffer\_size additional memory.

On Linux, if the kernel is enabled for large page support, InnoDB can use large pages to allocate memory for its buffer pool. See Section 10.12.3.3, "Enabling Large Page Support".