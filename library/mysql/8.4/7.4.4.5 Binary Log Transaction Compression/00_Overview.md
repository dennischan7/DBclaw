---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports binary log transaction compression; when this is enabled, transaction payloads are compressed using the zstd algorithm, and then written to the server's binary log file as a single event (a Transaction\_payload\_event).

Compressed transaction payloads remain in a compressed state while they are sent in the replication stream to replicas, other Group Replication group members, or clients such as mysqlbinlog. They are not decompressed by receiver threads, and are written to the relay log still in their compressed state. Binary log transaction compression therefore saves storage space both on the originator of the transaction and on the recipient (and for their backups), and saves network bandwidth when the transactions are sent between server instances.

Compressed transaction payloads are decompressed when the individual events contained in them need to be inspected. For example, the Transaction\_payload\_event is decompressed by an applier thread in order to apply the events it contains on the recipient. Decompression is also carried out during recovery, by mysqlbinlog when replaying transactions, and by the SHOW BINLOG EVENTS and SHOW RELAYLOG EVENTS statements.

You can enable binary log transaction compression on a MySQL server instance using the binlog\_transaction\_compression system variable, which defaults to OFF. You can also use the binlog\_transaction\_compression\_level\_zstd system variable to set the level for the zstd algorithm that is used for compression. This value determines the compression effort, from 1 (the lowest effort) to 22 (the highest effort). As the compression level increases, the compression ratio increases, which reduces the storage space and network bandwidth required for the transaction payload. However, the effort required for data compression also increases, taking time and CPU and memory resources on the originating server. Increases in the compression effort do not have a linear relationship to increases in the compression ratio.

Setting binlog\_transaction\_compression or binlog\_transaction\_compression\_level\_zstd (or both) has no immediate effect but rather applies to all subsequent START REPLICA statements.

![](_page_50_Picture_7.jpeg)

### **Note**

You can enable binary logging of compressed transactions for tables using the NDB storage engine at run time using the ndb\_log\_transaction\_compression system variable, and control the level of compression using ndb\_log\_transaction\_compression\_level\_zstd. Starting mysqld with --binlog-transactioncompression on the command line or in a my.cnf file causes ndb\_log\_transaction\_compression to be enabled automatically and any setting for the --ndb-log-transaction-compression option to be ignored; to disable binary log transaction compression for the NDB storage engine only, set ndb\_log\_transaction\_compression=OFF in a client session after starting mysqld.

The following types of event are excluded from binary log transaction compression, so are always written uncompressed to the binary log:

- Events relating to the GTID for the transaction (including anonymous GTID events).
- Other types of control event, such as view change events and heartbeat events.
- Incident events and the whole of any transactions that contain them.
- Non-transactional events and the whole of any transactions that contain them. A transaction involving a mix of non-transactional and transactional storage engines does not have its payload compressed.
- Events that are logged using statement-based binary logging. Binary log transaction compression is only applied for the row-based binary logging format.

Binary log encryption can be used on binary log files that contain compressed transactions.

# **Behaviors When Binary Log Transaction Compression is Enabled**

Transactions with payloads that are compressed can be rolled back like any other transaction, and they can also be filtered out on a replica by the usual filtering options. Binary log transaction compression can be applied to XA transactions.

When binary log transaction compression is enabled, the max\_allowed\_packet and replica\_max\_allowed\_packet limits for the server still apply, and are measured on the compressed size of the Transaction\_payload\_event, plus the bytes used for the event header.

![](_page_51_Picture_5.jpeg)

## **Important**

Compressed transaction payloads are sent as a single packet, rather than each event of the transaction being sent in an individual packet, as is the case when binary log transaction compression is not in use. In case the compressed transaction packet exceeds the maximum packet size used in replication, which is 1 GiB, the source server writes the transaction uncompressed, so that it can be sent in smaller pieces.

For multithreaded workers, each transaction (including its GTID event and Transaction\_payload\_event) is assigned to a worker thread. The worker thread decompresses the transaction payload and applies the individual events in it one by one. If an error is found applying any event within the Transaction\_payload\_event, the complete transaction is reported to the co-ordinator as having failed. When replica\_parallel\_type or replica\_parallel\_type is set to DATABASE, all the databases affected by the transaction are mapped before the transaction is scheduled. The use of binary log transaction compression with the DATABASE policy can reduce parallelism compared to uncompressed transactions, which are mapped and scheduled for each event.

For semisynchronous replication (see Section 19.4.10, "Semisynchronous Replication"), the replica acknowledges the transaction when the complete Transaction\_payload\_event has been received.

When binary log checksums are enabled (which is the default), the replication source server does not write checksums for individual events in a compressed transaction payload. Instead, a checksum is written for the complete Transaction\_payload\_event, and individual checksums are written for any events that were not compressed, such as events relating to GTIDs.

For the SHOW BINLOG EVENTS and SHOW RELAYLOG EVENTS statements, the Transaction\_payload\_event is first printed as a single unit, then it is unpacked and each event inside it is printed.

For operations that reference the end position of an event, such as START REPLICA with the UNTIL clause, SOURCE\_POS\_WAIT(), and sql\_replica\_skip\_counter, you must specify the end position of the compressed transaction payload (the Transaction\_payload\_event). When skipping events using sql\_replica\_skip\_counter, a compressed transaction payload is counted as a single counter value, so all the events inside it are skipped as a unit.

#### **Combining Compressed and Uncompressed Transaction Payloads**

MySQL Server releases that support binary log transaction compression can handle a mix of compressed and uncompressed transaction payloads.

- The system variables relating to binary log transaction compression do not need to be set the same on all Group Replication group members, and are not replicated from sources to replicas in a replication topology. You can decide whether or not binary log transaction compression is appropriate for each MySQL Server instance that has a binary log.
- If transaction compression is enabled then disabled on a server, compression is not applied to future transactions originated on that server, but transaction payloads that have been compressed can still be handled and displayed.

• If transaction compression is specified for individual sessions by setting the session value of binlog\_transaction\_compression, the binary log can contain a mix of compressed and uncompressed transaction payloads.

When a source in a replication topology and its replica both have binary log transaction compression enabled, the replica receives compressed transaction payloads and writes them compressed to its relay log. It decompresses the transaction payloads to apply the transactions, and then compresses them again after applying for writing to its binary log. Any downstream replicas receive the compressed transaction payloads.

When a source in a replication topology has binary log transaction compression enabled but its replica does not, the replica receives compressed transaction payloads and writes them compressed to its relay log. It decompresses the transaction payloads to apply the transactions, and then writes them uncompressed to its own binary log, if it has one. Any downstream replicas receive the uncompressed transaction payloads.

When a source in a replication topology does not have binary log transaction compression enabled but its replica does, if the replica has a binary log, it compresses the transaction payloads after applying them, and writes the compressed transaction payloads to its binary log. Any downstream replicas receive the compressed transaction payloads.

When a MySQL server instance has no binary log, it can receive, handle, and display compressed transaction payloads regardless of its value for binlog\_transaction\_compression. Compressed transaction payloads received by such server instances are written in their compressed state to the relay log, so they benefit indirectly from compression that was carried out by other servers in the replication topology.

### **Monitoring Binary Log Transaction Compression**

You can monitor the effects of binary log transaction compression using the Performance Schema table binary\_log\_transaction\_compression\_stats. The statistics include the data compression ratio for the monitored period, and you can also view the effect of compression on the last transaction on the server. You can reset the statistics by truncating the table. Statistics for binary logs and relay logs are split out so you can see the impact of compression for each log type. The MySQL server instance must have a binary log to produce these statistics.

The Performance Schema table events\_stages\_current shows when a transaction is in the stage of decompression or compression for its transaction payload, and displays its progress for this stage. Compression is carried out by the worker thread handling the transaction, just before the transaction is committed, provided that there are no events in the finalized capture cache that exclude the transaction from binary log transaction compression (for example, incident events). When decompression is required, it is carried out for one event from the payload at a time.

mysqlbinlog with the --verbose option includes comments stating the compressed size and the uncompressed size for compressed transaction payloads, and the compression algorithm that was used.

You can enable connection compression at the protocol level for replication connections, using the SOURCE\_COMPRESSION\_ALGORITHMS and SOURCE\_ZSTD\_COMPRESSION\_LEVEL options of the CHANGE REPLICATION SOURCE TO statement, or the replica\_compressed\_protocol system variable. If you enable binary log transaction compression in a system where connection compression is also enabled, the impact of connection compression is reduced, as there might be little opportunity to further compress the compressed transaction payloads. However, connection compression can still operate on uncompressed events and on message headers. Binary log transaction compression can be enabled in combination with connection compression if you need to save storage space as well as network bandwidth. For more information on connection compression for replication connections, see Section 6.2.8, "Connection Compression Control".

For Group Replication, compression is enabled by default for messages that exceed the threshold set by the group\_replication\_compression\_threshold system variable. You can also

configure compression for messages sent for distributed recovery by the method of state transfer from a donor's binary log, using the group\_replication\_recovery\_compression\_algorithms and group\_replication\_recovery\_zstd\_compression\_level system variables. If you enable binary log transaction compression in a system where these are configured, Group Replication's message compression can still operate on uncompressed events and on message headers, but its impact is reduced. For more information on message compression for Group Replication, see Section 20.7.4, "Message Compression".

# <span id="page-53-0"></span>**7.4.5 The Slow Query Log**

The slow query log consists of SQL statements that take more than long\_query\_time seconds to execute and require at least min\_examined\_row\_limit rows to be examined. The slow query log can be used to find queries that take a long time to execute and are therefore candidates for optimization. However, examining a long slow query log can be a time-consuming task. To make this easier, you can use the mysqldumpslow command to process a slow query log file and summarize its contents. See Section 6.6.10, "mysqldumpslow — Summarize Slow Query Log Files".

The time to acquire the initial locks is not counted as execution time. mysqld writes a statement to the slow query log after it has been executed and after all locks have been released, so log order might differ from execution order.

- [Slow Query Log Parameters](#page-53-1)
- [Slow Query Log Contents](#page-54-0)

# <span id="page-53-1"></span>**Slow Query Log Parameters**

The minimum and default values of long\_query\_time are 0 and 10, respectively. The value can be specified to a resolution of microseconds.

By default, administrative statements are not logged, nor are queries that do not use indexes for lookups. This behavior can be changed using log\_slow\_admin\_statements and log\_queries\_not\_using\_indexes, as described later.

By default, the slow query log is disabled. To specify the initial slow query log state explicitly, use --slow\_query\_log[={0|1}]. With no argument or an argument of 1, --slow\_query\_log enables the log. With an argument of 0, this option disables the log. To specify a log file name, use - slow\_query\_log\_file=file\_name. To specify the log destination, use the log\_output system variable (as described in [Section 7.4.1, "Selecting General Query Log and Slow Query Log Output](#page-12-0) [Destinations"](#page-12-0)).

![](_page_53_Picture_11.jpeg)

#### **Note**

If you specify the TABLE log destination, see [Log Tables and "Too many open](#page-13-1) [files" Errors](#page-13-1).

If you specify no name for the slow query log file, the default name is host\_name-slow.log. The server creates the file in the data directory unless an absolute path name is given to specify a different directory.

To disable or enable the slow query log or change the log file name at runtime, use the global slow\_query\_log and slow\_query\_log\_file system variables. Set slow\_query\_log to 0 to disable the log or to 1 to enable it. Set slow\_query\_log\_file to specify the name of the log file. If a log file already is open, it is closed and the new file is opened.

The server writes less information to the slow query log if you use the --log-short-format option.

To include slow administrative statements in the slow query log, enable the log\_slow\_admin\_statements system variable. Administrative statements include ALTER TABLE, ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX, OPTIMIZE TABLE, and REPAIR TABLE.

To include queries that do not use indexes for row lookups in the statements written to the slow query log, enable the log\_queries\_not\_using\_indexes system variable. (Even with that variable enabled, the server does not log queries that would not benefit from the presence of an index due to the table having fewer than two rows.)

When queries that do not use an index are logged, the slow query log may grow quickly. It is possible to put a rate limit on these queries by setting the log\_throttle\_queries\_not\_using\_indexes system variable. By default, this variable is 0, which means there is no limit. Positive values impose a per-minute limit on logging of queries that do not use indexes. The first such query opens a 60-second window within which the server logs queries up to the given limit, then suppresses additional queries. If there are suppressed queries when the window ends, the server logs a summary that indicates how many there were and the aggregate time spent in them. The next 60-second window begins when the server logs the next query that does not use indexes.

The server uses the controlling parameters in the following order to determine whether to write a query to the slow query log:

- 1. The query must either not be an administrative statement, or log\_slow\_admin\_statements must be enabled.
- 2. The query must have taken at least long\_query\_time seconds, or log\_queries\_not\_using\_indexes must be enabled and the query used no indexes for row lookups.
- 3. The query must have examined at least min\_examined\_row\_limit rows.
- 4. The query must not be suppressed according to the log\_throttle\_queries\_not\_using\_indexes setting.

The log\_timestamps system variable controls the time zone of timestamps in messages written to the slow query log file (as well as to the general query log file and the error log). It does not affect the time zone of general query log and slow query log messages written to log tables, but rows retrieved from those tables can be converted from the local system time zone to any desired time zone with CONVERT\_TZ() or by setting the session time\_zone system variable.

By default, a replica does not write replicated queries to the slow query log. To change this, enable the log\_slow\_replica\_statements system variable. Note that if row-based replication is in use (binlog\_format=ROW), these system variables have no effect. Queries are only added to the replica's slow query log when they are logged in statement format in the binary log, that is, when binlog\_format=STATEMENT is set, or when binlog\_format=MIXED is set and the statement is logged in statement format. Slow queries that are logged in row format when binlog\_format=MIXED is set, or that are logged when binlog\_format=ROW is set, are not added to the replica's slow query log, even if log\_slow\_replica\_statements is enabled.

## <span id="page-54-0"></span>**Slow Query Log Contents**

When the slow query log is enabled, the server writes output to any destinations specified by the log\_output system variable. If you enable the log, the server opens the log file and writes startup messages to it. However, further logging of queries to the file does not occur unless the FILE log destination is selected. If the destination is NONE, the server writes no queries even if the slow query log is enabled. Setting the log file name has no effect on logging if FILE is not selected as an output destination.

If the slow query log is enabled and FILE is selected as an output destination, each statement written to the log is preceded by a line that begins with a # character and has these fields (with all fields on a single line):

• Query\_time: duration

The statement execution time in seconds.

• Lock\_time: duration

The time to acquire locks in seconds.

• Rows\_sent: N

The number of rows sent to the client.

• Rows\_examined:

The number of rows examined by the server layer (not counting any processing internal to storage engines).

Enabling the log\_slow\_extra system variable causes the server to write the following extra fields to FILE output in addition to those just listed (TABLE output is unaffected). Some field descriptions refer to status variable names. Consult the status variable descriptions for more information. However, in the slow query log, the counters are per-statement values, not cumulative per-session values.

• Thread\_id: ID

The statement thread identifier.

• Errno: error\_number

The statement error number, or 0 if no error occurred.

• Killed: N

If the statement was terminated, the error number indicating why, or 0 if the statement terminated normally.

• Bytes\_received: N

The Bytes\_received value for the statement.

• Bytes\_sent: N

The Bytes\_sent value for the statement.

• Read\_first: N

The Handler\_read\_first value for the statement.

• Read\_last: N

The Handler\_read\_last value for the statement.

• Read\_key: N

The Handler\_read\_key value for the statement.

• Read\_next: N

The Handler\_read\_next value for the statement.

• Read\_prev: N

The Handler\_read\_prev value for the statement.

• Read\_rnd: N

The Handler\_read\_rnd value for the statement.

• Read\_rnd\_next: N

The Handler\_read\_rnd\_next value for the statement.

• Sort\_merge\_passes: N

The Sort\_merge\_passes value for the statement.

• Sort\_range\_count: N

The Sort\_range value for the statement.

• Sort\_rows: N

The Sort\_rows value for the statement.

• Sort\_scan\_count: N

The Sort\_scan value for the statement.

• Created\_tmp\_disk\_tables: N

The Created\_tmp\_disk\_tables value for the statement.

• Created\_tmp\_tables: N

The Created\_tmp\_tables value for the statement.

• Start: timestamp

The statement execution start time.

• End: timestamp

The statement execution end time.

A given slow query log file may contain a mix of lines with and without the extra fields added by enabling log\_slow\_extra. Log file analyzers can determine whether a line contains the additional fields by the field count.

Each statement written to the slow query log file is preceded by a SET statement that includes a timestamp, which indicates when the slow statement began executing.

Passwords in statements written to the slow query log are rewritten by the server not to occur literally in plain text. See [Section 8.1.2.3, "Passwords and Logging".](#page-159-0)

Statements that cannot be parsed (due, for example, to syntax errors) are not written to the slow query log.

# <span id="page-56-0"></span>**7.4.6 Server Log Maintenance**

As described in [Section 7.4, "MySQL Server Logs"](#page-11-0), MySQL Server can create several different log files to help you see what activity is taking place. However, you must clean up these files regularly to ensure that the logs do not take up too much disk space.

When using MySQL with logging enabled, you may want to back up and remove old log files from time to time and tell MySQL to start logging to new files. See Section 9.2, "Database Backup Methods".

On a Linux (Red Hat) installation, you can use the mysql-log-rotate script for log maintenance. If you installed MySQL from an RPM distribution, this script should have been installed automatically. Be careful with this script if you are using the binary log for replication. You should not remove binary logs until you are certain that their contents have been processed by all replicas.

On other systems, you must install a short script yourself that you start from cron (or its equivalent) for handling log files.

Binary log files are automatically removed after the server's binary log expiration period. Removal of the files can take place at startup and when the binary log is flushed. The default binary log expiration period is 30 days. To specify an alternative expiration period, use the binlog\_expire\_logs\_seconds system variable. If you are using replication, you should specify an expiration period that is no lower than the maximum amount of time your replicas might lag behind the source. To remove binary logs on demand, use the PURGE BINARY LOGS statement (see Section 15.4.1.1, "PURGE BINARY LOGS Statement").

To force MySQL to start using new log files, flush the logs. Log flushing occurs when you execute a FLUSH LOGS statement or a mysqladmin flush-logs, mysqladmin refresh, mysqldump - flush-logs, or mysqldump --source-data command. See Section 15.7.8.3, "FLUSH Statement", Section 6.5.2, "mysqladmin — A MySQL Server Administration Program", and Section 6.5.4, "mysqldump — A Database Backup Program". In addition, the server flushes the binary log automatically when current binary log file size reaches the value of the max\_binlog\_size system variable.

FLUSH LOGS supports optional modifiers to enable selective flushing of individual logs (for example, FLUSH BINARY LOGS). See Section 15.7.8.3, "FLUSH Statement".

A log-flushing operation has the following effects:

- If binary logging is enabled, the server closes the current binary log file and opens a new log file with the next sequence number.
- If general query logging or slow query logging to a log file is enabled, the server closes and reopens the log file.
- If the server was started with the --log-error option to cause the error log to be written to a file, the server closes and reopens the log file.

Execution of log-flushing statements or commands requires connecting to the server using an account that has the [RELOAD](#page-176-0) privilege. On Unix and Unix-like systems, another way to flush the logs is to send a signal to the server, which can be done by root or the account that owns the server process. (See Section 6.10, "Unix Signal Handling in MySQL".) Signals enable log flushing to be performed without having to connect to the server:

- A SIGHUP signal flushes all the logs. However, SIGHUP has additional effects other than log flushing that might be undesirable.
- SIGUSR1 causes the server to flush the error log, general query log, and slow query log. If you are interested in flushing only those logs, SIGUSR1 can be used as a more "lightweight" signal that does not have the SIGHUP effects that are unrelated to logs.

As mentioned previously, flushing the binary log creates a new binary log file, whereas flushing the general query log, slow query log, or error log just closes and reopens the log file. For the latter logs, to cause a new log file to be created on Unix, rename the current log file first before flushing it. At flush time, the server opens the new log file with the original name. For example, if the general query log, slow query log, and error log files are named mysql.log, mysql-slow.log, and err.log, you can use a series of commands like this from the command line:

```
cd mysql-data-directory
mv mysql.log mysql.log.old
mv mysql-slow.log mysql-slow.log.old
mv err.log err.log.old
mysqladmin flush-logs
```

On Windows, use rename rather than mv.

At this point, you can make a backup of mysql.log.old, mysql-slow.log.old, and err.log.old, then remove them from disk.

To rename the general query log or slow query log at runtime, first connect to the server and disable the log:

```
SET GLOBAL general_log = 'OFF';
```

```
SET GLOBAL slow_query_log = 'OFF';
```

With the logs disabled, rename the log files externally (for example, from the command line). Then enable the logs again:

```
SET GLOBAL general_log = 'ON';
SET GLOBAL slow_query_log = 'ON';
```

This method works on any platform and does not require a server restart.

![](_page_58_Picture_5.jpeg)

#### **Note**

For the server to recreate a given log file after you have renamed the file externally, the file location must be writable by the server. This may not always be the case. For example, on Linux, the server might write the error log as / var/log/mysqld.log, where /var/log is owned by root and not writable by mysqld. In this case, log-flushing operations fail to create a new log file.

To handle this situation, you must manually create the new log file with the proper ownership after renaming the original log file. For example, execute these commands as root:

```
mv /var/log/mysqld.log /var/log/mysqld.log.old
install -omysql -gmysql -m0644 /dev/null /var/log/mysqld.log
```

# <span id="page-58-1"></span>**7.5 MySQL Components**

MySQL Server includes a component-based infrastructure for extending server capabilities. A component provides services that are available to the server and other components. (With respect to service use, the server is a component, equal to other components.) Components interact with each other only through the services they provide.

MySQL distributions include several components that implement server extensions:

- Components for configuring error logging. See [Section 7.4.2, "The Error Log"](#page-14-1), and [Section 7.5.3,](#page-59-0) ["Error Log Components".](#page-59-0)
- A component for checking passwords. See Section 8.4.3, "The Password Validation Component".
- Keyring components provide secure storage for sensitive information. See Section 8.4.4, "The MySQL Keyring".
- A component that enables applications to add their own message events to the audit log. See Section 8.4.6, "The Audit Message Component".
- A component that implements a loadable function for accessing query attributes. See Section 11.6, "Query Attributes".
- A component for scheduling actively executing tasks. See [Section 7.5.5, "Scheduler Component".](#page-62-0)

System and status variables implemented by a component are exposed when the component is installed and have names that begin with a component-specific prefix. For example, the log\_filter\_dragnet error log filter component implements a system variable named log\_error\_filter\_rules, the full name of which is dragnet.log\_error\_filter\_rules. To refer to this variable, use the full name.

The following sections describe how to install and uninstall components, and how to determine at runtime which components are installed and obtain information about them.

For information about the internal implementation of components, see the MySQL Server Doxygen documentation, available at [https://dev.mysql.com/doc/index-other.html.](https://dev.mysql.com/doc/index-other.md) For example, if you intend to write your own components, this information is important for understanding how components work.

# <span id="page-58-0"></span>**7.5.1 Installing and Uninstalling Components**

Components must be loaded into the server before they can be used. MySQL supports manual component loading at runtime and automatic loading during server startup.

While a component is loaded, information about it is available as described in [Section 7.5.2, "Obtaining](#page-59-1) [Component Information".](#page-59-1)

The INSTALL COMPONENT and UNINSTALL COMPONENT SQL statements enable component loading and unloading. For example:

```
INSTALL COMPONENT 'file://component_validate_password';
UNINSTALL COMPONENT 'file://component_validate_password';
```

A loader service handles component loading and unloading, and also registers loaded components in the mysql.component system table.

Components are loaded in the server locally (not replicated).

The SQL statements for component manipulation affect server operation and the mysql.component system table as follows:

- INSTALL COMPONENT loads components into the server. The components become active immediately. The loader service also registers loaded components in the mysql.component system table. For subsequent server restarts, the loader service loads any components listed in mysql.component during the startup sequence. This occurs even if the server is started with the --skip-grant-tables option. The optional SET clause permits setting component systemvariable values when you install components.
- UNINSTALL COMPONENT deactivates components and unloads them from the server. The loader service also unregisters the components from the mysql.component system table so that the server no longer loads them during its startup sequence for subsequent restarts.

Compared to the corresponding INSTALL PLUGIN statement for server plugins, the INSTALL COMPONENT statement for components offers the significant advantage that it is not necessary to know any platform-specific file name suffix for naming the component. This means that a given INSTALL COMPONENT statement can be executed uniformly across platforms.

A component when installed may also automatically install related loadable functions. If so, the component when uninstalled also automatically uninstalls those functions.

# <span id="page-59-1"></span>**7.5.2 Obtaining Component Information**

The mysql.component system table contains information about currently loaded components and shows which components have been registered using INSTALL COMPONENT. Selecting from the table shows which components are installed. For example:

```
mysql> SELECT * FROM mysql.component;
+--------------+--------------------+------------------------------------+
| component_id | component_group_id | component_urn |
+--------------+--------------------+------------------------------------+
| 1 | 1 | file://component_validate_password |
| 2 | 2 | file://component_log_sink_json |
+--------------+--------------------+------------------------------------+
```

The component\_id and component\_group\_id values are for internal use. The component\_urn is the URN used in INSTALL COMPONENT and UNINSTALL COMPONENT statements to load and unload the component.

# <span id="page-59-0"></span>**7.5.3 Error Log Components**

This section describes the characteristics of individual error log components. For general information about configuring error logging, see [Section 7.4.2, "The Error Log"](#page-14-1).

A log component can be a filter or a sink:

- A filter processes log events, to add, remove, or modify event fields, or to delete events entirely. The resulting events pass to the next log component in the list of enabled components.
- A sink is a destination (writer) for log events. Typically, a sink processes log events into log messages that have a particular format and writes these messages to its associated output, such as a file or the system log. A sink may also write to the Performance Schema error\_log table; see Section 29.12.22.2, "The error\_log Table". Events pass unmodified to the next log component in the list of enabled components (that is, although a sink formats events to produce output messages, it does not modify events as they pass internally to the next component).

The log\_error\_services system variable lists the enabled log components. Components not named in the list are disabled. log\_error\_services also implicitly loads error log components if they are not already loaded. For more information, see [Section 7.4.2.1, "Error Log Configuration".](#page-14-0)

The following sections describe individual log components, grouped by component type:

- [Filter Error Log Components](#page-60-0)
- [Sink Error Log Components](#page-61-0)

Component descriptions include these types of information:

- The component name and intended purpose.
- Whether the component is built in or must be loaded. For a loadable component, the description specifies the URN to use if explicitly loading or unloading the component with the INSTALL COMPONENT and UNINSTALL COMPONENT statements. Implicitly loading error log components requires only the component name. For more information, see [Section 7.4.2.1, "Error Log](#page-14-0) [Configuration".](#page-14-0)
- Whether the component can be listed multiple times in the log\_error\_services value.
- For a sink component, the destination to which the component writes output.
- For a sink component, whether it supports an interface to the Performance Schema error\_log table.

## <span id="page-60-0"></span>**Filter Error Log Components**

Error log filter components implement filtering of error log events. If no filter component is enabled, no filtering occurs.

Any enabled filter component affects log events only for components listed later in the log\_error\_services value. In particular, for any log sink component listed in log\_error\_services earlier than any filter component, no log event filtering occurs.

#### **The log\_filter\_internal Component**

- Purpose: Implements filtering based on log event priority and error code, in combination with the log\_error\_verbosity and log\_error\_suppression\_list system variables. See [Section 7.4.2.5, "Priority-Based Error Log Filtering \(log\\_filter\\_internal\)"](#page-24-1).
- URN: This component is built in and need not be loaded.
- Multiple uses permitted: No.

If log\_filter\_internal is disabled, log\_error\_verbosity and log\_error\_suppression\_list have no effect.

### **The log\_filter\_dragnet Component**

• Purpose: Implements filtering based on the rules defined by the dragnet.log\_error\_filter\_rules system variable setting. See [Section 7.4.2.6, "Rule-Based](#page-26-0) [Error Log Filtering \(log\\_filter\\_dragnet\)"](#page-26-0).

- URN: file://component\_log\_filter\_dragnet
- Multiple uses permitted: No.

## <span id="page-61-0"></span>**Sink Error Log Components**

Error log sink components are writers that implement error log output. If no sink component is enabled, no log output occurs.

Some sink component descriptions refer to the default error log destination. This is the console or a file and is indicated by the value of the log\_error system variable, determined as described in [Section 7.4.2.2, "Default Error Log Destination Configuration"](#page-20-1).

#### **The log\_sink\_internal Component**

- Purpose: Implements traditional error log message output format.
- URN: This component is built in and need not be loaded.
- Multiple uses permitted: No.
- Output destination: Writes to the default error log destination.
- Performance Schema support: Writes to the error\_log table. Provides a parser for reading error log files created by previous server instances.

### **The log\_sink\_json Component**

- Purpose: Implements JSON-format error logging. See [Section 7.4.2.7, "Error Logging in JSON](#page-31-0) [Format"](#page-31-0).
- URN: file://component\_log\_sink\_json
- Multiple uses permitted: Yes.
- Output destination: This sink determines its output destination based on the default error log destination, which is given by the log\_error system variable:
  - If log\_error names a file, the sink bases output file naming on that file name, plus a numbered .NN.json suffix, with NN starting at 00. For example, if log\_error is file\_name, successive instances of log\_sink\_json named in the log\_error\_services value write to file\_name.00.json, file\_name.01.json, and so forth.
  - If log\_error is stderr, the sink writes to the console. If log\_sink\_json is named multiple times in the log\_error\_services value, they all write to the console, which is likely not useful.
- Performance Schema support: Writes to the error\_log table. Provides a parser for reading error log files created by previous server instances.

## **The log\_sink\_syseventlog Component**

- Purpose: Implements error logging to the system log. This is the Event Log on Windows, and syslog on Unix and Unix-like systems. See [Section 7.4.2.8, "Error Logging to the System Log".](#page-32-0)
- URN: file://component\_log\_sink\_syseventlog
- Multiple uses permitted: No.
- Output destination: Writes to the system log. Does not use the default error log destination.
- Performance Schema support: Does not write to the error\_log table. Does not provide a parser for reading error log files created by previous server instances.

#### **The log\_sink\_test Component**

- Purpose: Intended for internal use in writing test cases, not for production use.
- URN: file://component\_log\_sink\_test

Sink properties such as whether multiple uses are permitted and the output destination are not specified for log\_sink\_test because, as mentioned, it is for internal use. As such, its behavior is subject to change at any time.