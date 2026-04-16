---
source: MySQL 8.4 Reference
title: 00_Overview
---

If you flush the error log using a FLUSH ERROR LOGS or FLUSH LOGS statement, or a mysqladmin flush-logs command, the server closes and reopens any error log file to which it is writing. To rename an error log file, do so manually before flushing. Flushing the logs then opens a new file with the original file name. For example, assuming a log file name of host\_name.err, use the following commands to rename the file and create a new one:

```
mv host_name.err host_name.err-old
mysqladmin flush-logs error
mv host_name.err-old backup-directory
```

On Windows, use rename rather than mv.

If the location of the error log file is not writable by the server, the log-flushing operation fails to create a new log file. For example, on Linux, the server might write the error log to the /var/log/mysqld.log file, where the /var/log directory is owned by root and is not writable by mysqld. For information about handling this case, see [Section 7.4.6, "Server Log Maintenance".](#page-56-0)

If the server is not writing to a named error log file, no error log file renaming occurs when the error log is flushed.

# <span id="page-35-0"></span>**7.4.3 The General Query Log**

The general query log is a general record of what mysqld is doing. The server writes information to this log when clients connect or disconnect, and it logs each SQL statement received from clients. The general query log can be very useful when you suspect an error in a client and want to know exactly what the client sent to mysqld.

Each line that shows when a client connects also includes using connection\_type to indicate the protocol used to establish the connection. connection\_type is one of TCP/IP (TCP/IP connection established without SSL), SSL/TLS (TCP/IP connection established with SSL), Socket (Unix socket file connection), Named Pipe (Windows named pipe connection), or Shared Memory (Windows shared memory connection).

mysqld writes statements to the query log in the order that it receives them, which might differ from the order in which they are executed. This logging order is in contrast with that of the binary log, for which statements are written after they are executed but before any locks are released. In addition, the query log may contain statements that only select data while such statements are never written to the binary log.

When using statement-based binary logging on a replication source server, statements received by its replicas are written to the query log of each replica. Statements are written to the query log of the source if a client reads events with the mysqlbinlog utility and passes them to the server.

However, when using row-based binary logging, updates are sent as row changes rather than SQL statements, and thus these statements are never written to the query log when binlog\_format is ROW. A given update also might not be written to the query log when this variable is set to MIXED, depending on the statement used. See Section 19.2.1.1, "Advantages and Disadvantages of Statement-Based and Row-Based Replication", for more information.

By default, the general query log is disabled. To specify the initial general query log state explicitly, use --general\_log[={0|1}]. With no argument or an argument of 1, --general\_log enables the log. With an argument of 0, this option disables the log. To specify a log file name, use - general\_log\_file=file\_name. To specify the log destination, use the log\_output system variable (as described in [Section 7.4.1, "Selecting General Query Log and Slow Query Log Output](#page-12-0) [Destinations"](#page-12-0)).

![](_page_36_Picture_3.jpeg)

#### **Note**

If you specify the TABLE log destination, see [Log Tables and "Too many open](#page-13-1) [files" Errors](#page-13-1).

If you specify no name for the general query log file, the default name is host\_name.log. The server creates the file in the data directory unless an absolute path name is given to specify a different directory.

To disable or enable the general query log or change the log file name at runtime, use the global general\_log and general\_log\_file system variables. Set general\_log to 0 (or OFF) to disable the log or to 1 (or ON) to enable it. Set general\_log\_file to specify the name of the log file. If a log file already is open, it is closed and the new file is opened.

When the general query log is enabled, the server writes output to any destinations specified by the log\_output system variable. If you enable the log, the server opens the log file and writes startup messages to it. However, further logging of queries to the file does not occur unless the FILE log destination is selected. If the destination is NONE, the server writes no queries even if the general log is enabled. Setting the log file name has no effect on logging if the log destination value does not contain FILE.

Server restarts and log flushing do not cause a new general query log file to be generated (although flushing closes and reopens it). To rename the file and create a new one, use the following commands:

```
$> mv host_name.log host_name-old.log
$> mysqladmin flush-logs general
$> mv host_name-old.log backup-directory
```

On Windows, use rename rather than mv.

You can also rename the general query log file at runtime by disabling the log:

```
SET GLOBAL general_log = 'OFF';
```

With the log disabled, rename the log file externally (for example, from the command line). Then enable the log again:

```
SET GLOBAL general_log = 'ON';
```

This method works on any platform and does not require a server restart.

To disable or enable general query logging for the current session, set the session sql\_log\_off variable to ON or OFF. (This assumes that the general query log itself is enabled.)

Passwords in statements written to the general query log are rewritten by the server not to occur literally in plain text. Password rewriting can be suppressed for the general query log by starting the server with the --log-raw option. This option may be useful for diagnostic purposes, to see the exact text of statements as received by the server, but for security reasons is not recommended for production use. See also [Section 8.1.2.3, "Passwords and Logging"](#page-159-0).

An implication of password rewriting is that statements that cannot be parsed (due, for example, to syntax errors) are not written to the general query log because they cannot be known to be password free. Use cases that require logging of all statements including those with errors should use the - log-raw option, bearing in mind that this also bypasses password rewriting.

Password rewriting occurs only when plain text passwords are expected. For statements with syntax that expect a password hash value, no rewriting occurs. If a plain text password is supplied erroneously for such syntax, the password is logged as given, without rewriting.

The log\_timestamps system variable controls the time zone of timestamps in messages written to the general query log file (as well as to the slow query log file and the error log). It does not affect the time zone of general query log and slow query log messages written to log tables, but rows retrieved from those tables can be converted from the local system time zone to any desired time zone with CONVERT\_TZ() or by setting the session time\_zone system variable.

# <span id="page-37-0"></span>**7.4.4 The Binary Log**

The binary log contains "events" that describe database changes such as table creation operations or changes to table data. It also contains events for statements that potentially could have made changes (for example, a DELETE which matched no rows), unless row-based logging is used. The binary log also contains information about how long each statement took that updated data. The binary log has two important purposes:

- For replication, the binary log on a replication source server provides a record of the data changes to be sent to replicas. The source sends the information contained in its binary log to its replicas, which reproduce those transactions to make the same data changes that were made on the source. See Section 19.2, "Replication Implementation".
- Certain data recovery operations require use of the binary log. After a backup has been restored, the events in the binary log that were recorded after the backup was made are re-executed. These events bring databases up to date from the point of the backup. See Section 9.5, "Point-in-Time (Incremental) Recovery".

The binary log is not used for statements such as SELECT or SHOW that do not modify data. To log all statements (for example, to identify a problem query), use the general query log. See [Section 7.4.3,](#page-35-0) ["The General Query Log".](#page-35-0)

Running a server with binary logging enabled makes performance slightly slower. However, the benefits of the binary log in enabling you to set up replication and for restore operations generally outweigh this minor performance decrement.

The binary log is resilient to unexpected halts. Only complete events or transactions are logged or read back.

Passwords in statements written to the binary log are rewritten by the server not to occur literally in plain text. See also [Section 8.1.2.3, "Passwords and Logging".](#page-159-0)

MySQL binary log files and relay log files can be encrypted, helping to protect these files and the potentially sensitive data contained in them from being misused by outside attackers, and also from unauthorized viewing by users of the operating system where they are stored. You enable encryption on a MySQL server by setting the binlog\_encryption system variable to ON. For more information, see Section 19.3.2, "Encrypting Binary Log Files and Relay Log Files".

The following discussion describes some of the server options and variables that affect the operation of binary logging. For a complete list, see Section 19.1.6.4, "Binary Logging Options and Variables".

Binary logging is enabled by default (the log\_bin system variable is set to ON). The exception is if you use mysqld to initialize the data directory manually by invoking it with the --initialize or - initialize-insecure option, when binary logging is disabled by default, but can be enabled by specifying the --log-bin option.

To disable binary logging, you can specify the --skip-log-bin or --disable-log-bin option at startup. If either of these options is specified and --log-bin is also specified, the option specified later takes precedence.

The --log-replica-updates and --replica-preserve-commit-order options require binary logging. If you disable binary logging, either omit these options, or specify --log-replicaupdates=OFF and --skip-replica-preserve-commit-order. MySQL disables these options by default when --skip-log-bin or --disable-log-bin is specified. If you specify --logreplica-updates or --replica-preserve-commit-order together with --skip-log-bin or --disable-log-bin, a warning or error message is issued.

The --log-bin[=base\_name] option is used to specify the base name for binary log files. If you do not supply the --log-bin option, MySQL uses binlog as the default base name for the binary log files. For compatibility with earlier releases, if you supply the --log-bin option with no string or with an empty string, the base name defaults to host\_name-bin, using the name of the host machine. It is recommended that you specify a base name, so that if the host name changes, you can easily continue to use the same binary log file names (see Section B.3.7, "Known Issues in MySQL"). If you supply an extension in the log name (for example, --log-bin=base\_name.extension), the extension is silently removed and ignored.

mysqld appends a numeric extension to the binary log base name to generate binary log file names. The number increases each time the server creates a new log file, thus creating an ordered series of files. The server creates a new file in the series each time any of the following events occurs:

- The server is started or restarted
- The server flushes the logs.
- The size of the current log file reaches max\_binlog\_size.

A binary log file may become larger than max\_binlog\_size if you are using large transactions because a transaction is written to the file in one piece, never split between files.

To keep track of which binary log files have been used, mysqld also creates a binary log index file that contains the names of the binary log files. By default, this has the same base name as the binary log file, with the extension '.index'. You can change the name of the binary log index file with the --log-bin-index[=file\_name] option. You should not manually edit this file while mysqld is running; doing so would confuse mysqld.

The term "binary log file" generally denotes an individual numbered file containing database events. The term "binary log" collectively denotes the set of numbered binary log files plus the index file.

The default location for binary log files and the binary log index file is the data directory. You can use the --log-bin option to specify an alternative location, by adding a leading absolute path name to the base name to specify a different directory. When the server reads an entry from the binary log index file, which tracks the binary log files that have been used, it checks whether the entry contains a relative path. If it does, the relative part of the path is replaced with the absolute path set using the - log-bin option. An absolute path recorded in the binary log index file remains unchanged; in such a case, the index file must be edited manually to enable a new path or paths to be used. The binary log file base name and any specified path are available as the log\_bin\_basename system variable.

The server can be started with the default server ID when binary logging is enabled, but an informational message is issued if you do not specify a server ID explicitly using the server\_id system variable. For servers that are used in a replication topology, you must specify a unique nonzero server ID for each server.

A client that has privileges sufficient to set restricted session system variables (see Section 7.1.9.1, "System Variable Privileges") can disable binary logging of its own statements by using a SET sql\_log\_bin=OFF statement.

By default, the server logs the length of the event as well as the event itself and uses this to verify that the event was written correctly. You can also cause the server to write checksums for the events by setting the binlog\_checksum system variable. When reading back from the binary log, the source uses the event length by default, but can be made to use checksums if available by enabling source\_verify\_checksum. The replication I/O (receiver) thread on the replica also verifies events received from the source. You can cause the replication SQL (applier) thread to use checksums if available when reading from the relay log by enabling replica\_sql\_verify\_checksum.

The format of the events recorded in the binary log is dependent on the binary logging format. Three format types are supported: row-based logging, statement-based logging and mixed-base logging. The binary logging format used depends on the MySQL version. For descriptions of the logging formats, see [Section 7.4.4.1, "Binary Logging Formats".](#page-41-0)

The server evaluates the --binlog-do-db and --binlog-ignore-db options in the same way as it does the --replicate-do-db and --replicate-ignore-db options. For information about how this is done, see Section 19.2.5.1, "Evaluation of Database-Level Replication and Binary Logging Options".

A replica is started with log\_replica\_updates enabled by default, meaning that the replica writes to its own binary log any data modifications that are received from the source. The binary log must be enabled for this setting to work (see Section 19.1.6.3, "Replica Server Options and Variables"). This setting enables the replica to act as a source to other replicas.

You can delete all binary log files with the RESET BINARY LOGS AND GTIDS statement, or a subset of them with PURGE BINARY LOGS. See Section 15.7.8.6, "RESET Statement", and Section 15.4.1.1, "PURGE BINARY LOGS Statement".

If you are using MySQL Replication, you should not delete old binary log files on the source until you are sure that no replica still needs to use them. For example, if your replicas never run more than three days behind, once a day you can execute mysqladmin flush-logs binary on the source and then remove any logs that are more than three days old. You can remove the files manually, but it is preferable to use PURGE BINARY LOGS, which also safely updates the binary log index file for you (and which can take a date argument). See Section 15.4.1.1, "PURGE BINARY LOGS Statement".

You can display the contents of binary log files with the mysqlbinlog utility. This can be useful when you want to reprocess statements in the log for a recovery operation. For example, you can update a MySQL server from the binary log as follows:

```
$> mysqlbinlog log_file | mysql -h server_name
```

mysqlbinlog also can be used to display the contents of the relay log file on a replica, because they are written using the same format as binary log files. For more information on the mysqlbinlog utility and how to use it, see Section 6.6.9, "mysqlbinlog — Utility for Processing Binary Log Files". For more information about the binary log and recovery operations, see Section 9.5, "Point-in-Time (Incremental) Recovery".

Binary logging is done immediately after a statement or transaction completes but before any locks are released or any commit is done. This ensures that the log is logged in commit order.

Updates to nontransactional tables are stored in the binary log immediately after execution.

Within an uncommitted transaction, all updates (UPDATE, DELETE, or INSERT) that change transactional tables such as InnoDB tables are cached until a COMMIT statement is received by the server. At that point, mysqld writes the entire transaction to the binary log before the COMMIT is executed.

Modifications to nontransactional tables cannot be rolled back. If a transaction that is rolled back includes modifications to nontransactional tables, the entire transaction is logged with a ROLLBACK statement at the end to ensure that the modifications to those tables are replicated.

When a thread that handles the transaction starts, it allocates a buffer of binlog\_cache\_size to buffer statements. If a statement is bigger than this, the thread opens a temporary file to store the

transaction. The temporary file is deleted when the thread ends. If binary log encryption is active on the server, the temporary file is encrypted.

The Binlog\_cache\_use status variable shows the number of transactions that used this buffer (and possibly a temporary file) for storing statements. The Binlog\_cache\_disk\_use status variable shows how many of those transactions actually had to use a temporary file. These two variables can be used for tuning binlog\_cache\_size to a large enough value that avoids the use of temporary files.

The max\_binlog\_cache\_size system variable (default 4GB, which is also the maximum) can be used to restrict the total size used to cache a multiple-statement transaction. If a transaction is larger than this many bytes, it fails and rolls back. The minimum value is 4096.

If you are using the binary log and row based logging, concurrent inserts are converted to normal inserts for CREATE ... SELECT or INSERT ... SELECT statements. This is done to ensure that you can re-create an exact copy of your tables by applying the log during a backup operation. If you are using statement-based logging, the original statement is written to the log.

The binary log format has some known limitations that can affect recovery from backups. See Section 19.5.1, "Replication Features and Issues".

Binary logging for stored programs is done as described in Section 27.7, "Stored Program Binary Logging".

Note that the binary log format differs in MySQL 8.4 from previous versions of MySQL, due to enhancements in replication. See Section 19.5.2, "Replication Compatibility Between MySQL Versions".

If the server is unable to write to the binary log, flush binary log files, or synchronize the binary log to disk, the binary log on the replication source server can become inconsistent and replicas can lose synchronization with the source. The binlog\_error\_action system variable controls the action taken if an error of this type is encountered with the binary log.

- The default setting, ABORT\_SERVER, makes the server halt binary logging and shut down. At this point, you can identify and correct the cause of the error. On restart, recovery proceeds as in the case of an unexpected server halt (see Section 19.4.2, "Handling an Unexpected Halt of a Replica").
- The setting IGNORE\_ERROR provides backward compatibility with older versions of MySQL. With this setting, the server continues the ongoing transaction and logs the error, then halts binary logging, but continues to perform updates. At this point, you can identify and correct the cause of the error. To resume binary logging, log\_bin must be enabled again, which requires a server restart. Only use this option if you require backward compatibility, and the binary log is non-essential on this MySQL server instance. For example, you might use the binary log only for intermittent auditing or debugging of the server, and not use it for replication from the server or rely on it for point-in-time restore operations.

By default, the binary log is synchronized to disk at each write (sync\_binlog=1). If sync\_binlog was not enabled, and the operating system or machine (not only the MySQL server) crashed, there is a chance that the last statements of the binary log could be lost. To prevent this, enable the sync\_binlog system variable to synchronize the binary log to disk after every N commit groups. See Section 7.1.8, "Server System Variables". The safest value for sync\_binlog is 1 (the default), but this is also the slowest.

In earlier MySQL releases, there was a chance of inconsistency between the table content and binary log content if a crash occurred, even with sync\_binlog set to 1. For example, if you are using InnoDB tables and the MySQL server processes a COMMIT statement, it writes many prepared transactions to the binary log in sequence, synchronizes the binary log, and then commits the transaction into InnoDB. If the server unexpectedly exited between those two operations, the transaction would be rolled back by InnoDB at restart but still exist in the binary log. Such an issue was resolved in previous releases by enabling InnoDB support for two-phase commit in XA transactions. In MySQL 8.4, InnoDB support for two-phase commit in XA transactions is always enabled.

InnoDB support for two-phase commit in XA transactions ensures that the binary log and InnoDB data files are synchronized. However, the MySQL server should also be configured to synchronize the binary log and the InnoDB logs to disk before committing the transaction. The InnoDB logs are synchronized by default, and sync\_binlog=1 ensures the binary log is synchronized. The effect of implicit InnoDB support for two-phase commit in XA transactions and sync\_binlog=1 is that at restart after a crash, after doing a rollback of transactions, the MySQL server scans the latest binary log file to collect transaction xid values and calculate the last valid position in the binary log file. The MySQL server then tells InnoDB to complete any prepared transactions that were successfully written to the to the binary log, and truncates the binary log to the last valid position. This ensures that the binary log reflects the exact data of InnoDB tables, and therefore the replica remains in synchrony with the source because it does not receive a statement which has been rolled back.

If the MySQL server discovers at crash recovery that the binary log is shorter than it should have been, it lacks at least one successfully committed InnoDB transaction. This should not happen if sync\_binlog=1 and the disk/file system do an actual sync when they are requested to (some do not), so the server prints an error message The binary log file\_name is shorter than its expected size. In this case, this binary log is not correct and replication should be restarted from a fresh snapshot of the source's data.

The session values of the following system variables are written to the binary log and honored by the replica when parsing the binary log:

- sql\_mode (except that the NO\_DIR\_IN\_CREATE mode is not replicated; see Section 19.5.1.39, "Replication and Variables")
- foreign\_key\_checks
- unique\_checks
- character\_set\_client
- collation\_connection
- collation\_database
- collation\_server
- sql\_auto\_is\_null

## <span id="page-41-0"></span>**7.4.4.1 Binary Logging Formats**

The server uses several logging formats to record information in the binary log:

- Replication capabilities in MySQL originally were based on propagation of SQL statements from source to replica. This is called statement-based logging. You can cause this format to be used by starting the server with --binlog-format=STATEMENT.
- In row-based logging (the default), the source writes events to the binary log that indicate how individual table rows are affected. You can cause the server to use row-based logging by starting it with --binlog-format=ROW.
- A third option is also available: mixed logging. With mixed logging, statement-based logging is used by default, but the logging mode switches automatically to row-based in certain cases as described below. You can cause MySQL to use mixed logging explicitly by starting mysqld with the option - binlog-format=MIXED.

The logging format can also be set or limited by the storage engine being used. This helps to eliminate issues when replicating certain statements between a source and replica which are using different storage engines.

With statement-based replication, there may be issues with replicating nondeterministic statements. In deciding whether or not a given statement is safe for statement-based replication, MySQL determines

whether it can guarantee that the statement can be replicated using statement-based logging. If MySQL cannot make this guarantee, it marks the statement as potentially unreliable and issues the warning, Statement may not be safe to log in statement format.

You can avoid these issues by using MySQL's row-based replication instead.