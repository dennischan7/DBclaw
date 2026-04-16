---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes issues that you may encounter when using the InnoDB memcached plugin.

• If you encounter the following error in the MySQL error log, the server might fail to start:

```
failed to set rlimit for open files. Try running as root or requesting
smaller maxconns value.
```

The error message is from the memcached daemon. One solution is to raise the OS limit for the number of open files. The commands for checking and increasing the open file limit varies by operating system. This example shows commands for Linux and macOS:

```
# Linux
$> ulimit -n
1024
$> ulimit -n 4096
$> ulimit -n
4096
# macOS
$> ulimit -n
256
$> ulimit -n 4096
$> ulimit -n
4096
```

The other solution is to reduce the number of concurrent connections permitted for the memcached daemon. To do so, encode the -c memcached option in the daemon\_memcached\_option configuration parameter in the MySQL configuration file. The -c option has a default value of 1024.

```
[mysqld]
...
loose-daemon_memcached_option='-c 64'
```

• To troubleshoot problems where the memcached daemon is unable to store or retrieve InnoDB table data, encode the -vvv memcached option in the daemon\_memcached\_option configuration parameter in the MySQL configuration file. Examine the MySQL error log for debug output related to memcached operations.

```
[mysqld]
...
loose-daemon_memcached_option='-vvv'
```

- If columns specified to hold memcached values are the wrong data type, such as a numeric type instead of a string type, attempts to store key-value pairs fail with no specific error code or message.
- If the daemon\_memcached plugin causes MySQL server startup issues, you can temporarily disable the daemon\_memcached plugin while troubleshooting by adding this line under the [mysqld] group in the MySQL configuration file:

```
daemon_memcached=OFF
```

For example, if you run the INSTALL PLUGIN statement before running the innodb\_memcached\_config.sql configuration script to set up the necessary database and tables, the server might unexpectedly exit and fail to start. The server could also fail to start if you incorrectly configure an entry in the innodb\_memcache.containers table.

To uninstall the memcached plugin for a MySQL instance, issue the following statement:

```
mysql> UNINSTALL PLUGIN daemon_memcached;
```

- If you run more than one instance of MySQL on the same machine with the daemon\_memcached plugin enabled in each instance, use the daemon\_memcached\_option configuration parameter to specify a unique memcached port for each daemon\_memcached plugin.
- If an SQL statement cannot find the InnoDB table or finds no data in the table, but memcached API calls retrieve the expected data, you may be missing an entry for the InnoDB table in the innodb\_memcache.containers table, or you may have not switched to the correct InnoDB table by issuing a get or set request using @@table\_id notation. This problem could also occur if you change an existing entry in the innodb\_memcache.containers table without restarting the MySQL server afterward. The free-form storage mechanism is flexible enough that your requests to store or retrieve a multi-column value such as col1|col2|col3 may still work, even if the daemon is using the test.demo\_test table which stores values in a single column.
- When defining your own InnoDB table for use with the daemon\_memcached plugin, and columns in the table are defined as NOT NULL, ensure that values are supplied for the NOT NULL columns when inserting a record for the table into the innodb\_memcache.containers table. If the INSERT statement for the innodb\_memcache.containers record contains fewer delimited values than there are mapped columns, unfilled columns are set to NULL. Attempting to insert a NULL value into a NOT NULL column causes the INSERT to fail, which may only become evident after you reinitialize the daemon\_memcached plugin to apply changes to the innodb\_memcache.containers table.
- If cas\_column and expire\_time\_column fields of the innodb\_memcached.containers table are set to NULL, the following error is returned when attempting to load the memcached plugin:

```
InnoDB_Memcached: column 6 in the entry for config table 'containers' in
database 'innodb_memcache' has an invalid NULL value.
```

The memcached plugin rejects usage of NULL in the cas\_column and expire\_time\_column columns. Set the value of these columns to 0 when the columns are unused.

• As the length of the memcached key and values increase, you might encounter size and length limits.

- When the key exceeds 250 bytes, memcached operations return an error. This is currently a fixed limit within memcached.
- InnoDB table limits may be encountered if values exceed 768 bytes in size, 3072 bytes in size, or half of the [innodb\\_page\\_size](#page-52-0) value. These limits primarily apply if you intend to create an index on a value column to run report-generating queries on that column using SQL. See [Section 17.22,](#page-166-1) ["InnoDB Limits"](#page-166-1) for details.
- The maximum size for the key-value combination is 1 MB.
- If you share configuration files across MySQL servers of different versions, using the latest configuration options for the daemon\_memcached plugin could cause startup errors on older MySQL versions. To avoid compatibility problems, use the loose prefix with option names. For example, use loose-daemon\_memcached\_option='-c 64' instead of daemon\_memcached\_option=' c 64'.
- There is no restriction or check in place to validate character set settings. memcached stores and retrieves keys and values in bytes and is therefore not character set sensitive. However, you must ensure that the memcached client and the MySQL table use the same character set.
- memcached connections are blocked from accessing tables that contain an indexed virtual column. Accessing an indexed virtual column requires a callback to the server, but a memcached connection does not have access to the server code.

# <span id="page-162-0"></span>**17.21 InnoDB Troubleshooting**

The following general guidelines apply to troubleshooting InnoDB problems:

- When an operation fails or you suspect a bug, look at the MySQL server error log (see Section 7.4.2, "The Error Log"). [Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md) provides troubleshooting information for some of the common InnoDB-specific errors that you may encounter.
- If the failure is related to a deadlock, run with the [innodb\\_print\\_all\\_deadlocks](#page-54-0) option enabled so that details about each deadlock are printed to the MySQL server error log. For information about deadlocks, see Section 17.7.5, "Deadlocks in InnoDB".
- If the issue is related to the InnoDB data dictionary, see [Section 17.21.4, "Troubleshooting InnoDB](#page-165-0) [Data Dictionary Operations"](#page-165-0).
- When troubleshooting, it is usually best to run the MySQL server from the command prompt, rather than through mysqld\_safe or as a Windows service. You can then see what mysqld prints to the console, and so have a better grasp of what is going on. On Windows, start mysqld with the - console option to direct the output to the console window.
- Enable the InnoDB Monitors to obtain information about a problem (see [Section 17.17, "InnoDB](#page-116-0) [Monitors"\)](#page-116-0). If the problem is performance-related, or your server appears to be hung, you should enable the standard Monitor to print information about the internal state of InnoDB. If the problem is with locks, enable the Lock Monitor. If the problem is with table creation, tablespaces, or data dictionary operations, refer to the [InnoDB Information Schema system tables](#page-86-0) to examine contents of the InnoDB internal data dictionary.

InnoDB temporarily enables standard InnoDB Monitor output under the following conditions:

- A long semaphore wait
- InnoDB cannot find free blocks in the buffer pool
- Over 67% of the buffer pool is occupied by lock heaps or the adaptive hash index
- If you suspect that a table is corrupt, run CHECK TABLE on that table.