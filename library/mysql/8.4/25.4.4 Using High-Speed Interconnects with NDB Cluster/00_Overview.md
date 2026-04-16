---
source: MySQL 8.4 Reference
title: 00_Overview
---

Even before design of NDBCLUSTER began in 1996, it was evident that one of the major problems to be encountered in building parallel databases would be communication between the nodes in the network. For this reason, NDBCLUSTER was designed from the very beginning to permit the use of a number of different data transport mechanisms, or transporters.

NDB Cluster supports three of these (see Section 25.2.1, "NDB Cluster Core Concepts"). A fourth transporter, Scalable Coherent Interface (SCI), was also supported in very old versions of NDB. This required specialized hardware, software, and MySQL binaries that are no longer available.

# <span id="page-134-1"></span>**25.5 NDB Cluster Programs**

Using and managing an NDB Cluster requires several specialized programs, which we describe in this chapter. We discuss the purposes of these programs in an NDB Cluster, how to use the programs, and what startup options are available for each of them.

These programs include the NDB Cluster data, management, and SQL node processes ([ndbd](#page-134-0), [ndbmtd](#page-148-0), [ndb\\_mgmd](#page-149-0), and mysqld) and the management client ([ndb\\_mgm](#page-159-0)).

For information about using mysqld as an NDB Cluster process, see Section 25.6.10, "MySQL Server Usage for NDB Cluster".

Other NDB utility, diagnostic, and example programs are included with the NDB Cluster distribution. These include ndb\_restore, ndb\_show\_tables, and [ndb\\_config](#page-169-0). These programs are also covered in this section.

## <span id="page-134-0"></span>**25.5.1 ndbd — The NDB Cluster Data Node Daemon**

The [ndbd](#page-134-0) binary provides the single-threaded version of the process that is used to handle all the data in tables employing the NDBCLUSTER storage engine. This data node process enables a data node to accomplish distributed transaction handling, node recovery, checkpointing to disk, online backup, and related tasks. In NDB 8.4.1 and later, when started, [ndbd](#page-134-0) logs a warning similar to that shown here:

```
2024-05-28 13:32:16 [ndbd] WARNING -- Running ndbd with a single thread of
signal execution. For multi-threaded signal execution run the ndbmtd binary.
```

[ndbmtd](#page-148-0) is the multi-threaded version of this binary.

In an NDB Cluster, a set of [ndbd](#page-134-0) processes cooperate in handling data. These processes can execute on the same computer (host) or on different computers. The correspondences between data nodes and Cluster hosts is completely configurable.

Options that can be used with [ndbd](#page-134-0) are shown in the following table. Additional descriptions follow the table.

![](_page_134_Picture_13.jpeg)

## **Note**

All of these options also apply to the multithreaded version of this program ([ndbmtd](#page-148-0)) and you may substitute "[ndbmtd](#page-148-0)" for "[ndbd](#page-134-0)" wherever the latter occurs in this section.

#### <span id="page-134-2"></span>• [--bind-address](#page-134-2)

| Command-Line Format | bind-address=name |
|---------------------|-------------------|
| Type                | String            |
| Default Value       |                   |

Causes [ndbd](#page-134-0) to bind to a specific network interface (host name or IP address). This option has no default value.

<span id="page-134-3"></span>• [--character-sets-dir](#page-134-3)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|

Directory containing character sets.

#### <span id="page-135-0"></span>• [--connect-delay=](#page-135-0)#

| Command-Line Format | connect-delay=# |
|---------------------|-----------------|
| Deprecated          | Yes             |
| Type                | Numeric         |
| Default Value       | 5               |
| Minimum Value       | 0               |
| Maximum Value       | 3600            |

Determines the time to wait between attempts to contact a management server when starting (the number of attempts is controlled by the [--connect-retries](#page-135-1) option). The default is 5 seconds.

This option is deprecated, and is subject to removal in a future release of NDB Cluster. Use [-](#page-135-2) [connect-retry-delay](#page-135-2) instead.

#### <span id="page-135-1"></span>• [--connect-retries=](#page-135-1)#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 12                |
| Minimum Value       | -1                |
| Maximum Value       | 65535             |

Set the number of times to retry a connection before giving up; 0 means 1 attempt only (and no retries). The default is 12 attempts. The time to wait between attempts is controlled by the [-](#page-135-2) [connect-retry-delay](#page-135-2) option.

It is also possible to set this option to -1, in which case, the data node process continues indefinitely to try to connect.

#### <span id="page-135-2"></span>• [--connect-retry-delay=](#page-135-2)#

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Numeric               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 4294967295            |

Determines the time to wait between attempts to contact a management server when starting (the time between attempts is controlled by the [--connect-retries](#page-135-1) option). The default is 5 seconds.

This option takes the place of the [--connect-delay](#page-135-0) option, which is now deprecated and subject to removal in a future release of NDB Cluster.

The short form -r for this option is also deprecated, and thus subject to removal. Use the long form instead.

#### <span id="page-135-3"></span>• [--connect-string](#page-135-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-139-0).

#### <span id="page-136-0"></span>• [--core-file](#page-136-0)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-136-1"></span>• [--daemon](#page-136-1), -d

| Command-Line Format | daemon |
|---------------------|--------|
|---------------------|--------|

Instructs [ndbd](#page-134-0) or [ndbmtd](#page-148-0) to execute as a daemon process. This is the default behavior. [-](#page-141-0) [nodaemon](#page-141-0) can be used to prevent the process from running as a daemon.

This option has no effect when running [ndbd](#page-134-0) or [ndbmtd](#page-148-0) on Windows platforms.

<span id="page-136-2"></span>• [--defaults-extra-file](#page-136-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-136-3"></span>• [--defaults-file](#page-136-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-136-4"></span>• [--defaults-group-suffix](#page-136-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-136-5"></span>• [--filesystem-password](#page-136-5)

| Command-Line Format | filesystem-password=password |
|---------------------|------------------------------|

Pass the filesystem encryption and decryption password to the data node process using stdin, tty, or the my.cnf file.

Requires EncryptedFileSystem = 1.

For more information, see Section 25.6.19.4, "File System Encryption for NDB Cluster".

<span id="page-137-1"></span>• [--filesystem-password-from-stdin](#page-137-1)

| Command-Line Format | filesystem-password-from |
|---------------------|--------------------------|
|                     | stdin={TRUE FALSE}       |

Pass the filesystem encryption and decryption password to the data node process from stdin (only).

Requires EncryptedFileSystem = 1.

For more information, see Section 25.6.19.4, "File System Encryption for NDB Cluster".

<span id="page-137-2"></span>• [--foreground](#page-137-2)

| Command-Line Format | foreground |
|---------------------|------------|
|                     |            |

Causes [ndbd](#page-134-0) or [ndbmtd](#page-148-0) to execute as a foreground process, primarily for debugging purposes. This option implies the [--nodaemon](#page-141-0) option.

This option has no effect when running [ndbd](#page-134-0) or [ndbmtd](#page-148-0) on Windows platforms.

<span id="page-137-3"></span>• [--help](#page-137-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-137-0"></span>• [--initial](#page-137-0)

| Command-Line Format | initial |
|---------------------|---------|
|---------------------|---------|

Instructs [ndbd](#page-134-0) to perform an initial start. An initial start erases any files created for recovery purposes by earlier instances of [ndbd](#page-134-0). It also re-creates recovery log files. On some operating systems, this process can take a substantial amount of time.

The option also causes the removal of all data files associated with Disk Data tablespaces and undo log files associated with log file groups that existed previously on this data node (see Section 25.6.11, "NDB Cluster Disk Data Tables").

An [--initial](#page-137-0) start is to be used only when starting the [ndbd](#page-134-0) process under very special circumstances; this is because this option causes all files to be removed from the NDB Cluster file system and all redo log files to be re-created. These circumstances are listed here:

- When performing a software upgrade which has changed the contents of any files.
- When restarting the node with a new version of [ndbd](#page-134-0).
- As a measure of last resort when for some reason the node restart or system restart repeatedly fails. In this case, be aware that this node can no longer be used to restore data due to the destruction of the data files.

![](_page_137_Picture_21.jpeg)

#### **Warning**

To avoid the possibility of eventual data loss, it is recommended that you not use the --initial option together with StopOnError = 0. Instead, set StopOnError to 0 in config.ini only after the cluster has been started, then restart the data nodes normally—that is, without the --initial option. See the description of the StopOnError parameter for a detailed explanation of this issue. (Bug #24945638)

Use of this option prevents the StartPartialTimeout and StartPartitionedTimeout configuration parameters from having any effect.

![](_page_138_Picture_3.jpeg)

#### **Important**

This option does not affect backup files that have already been created by the affected node.

This option also has no effect on recovery of data by a data node that is just starting (or restarting) from data nodes that are already running (unless they also were started with --initial, as part of an initial restart). This recovery of data occurs automatically, and requires no user intervention in an NDB Cluster that is running normally.

It is permissible to use this option when starting the cluster for the very first time (that is, before any data node files have been created); however, it is not necessary to do so.

<span id="page-138-0"></span>• [--initial-start](#page-138-0)

| Command-Line Format | initial-start |
|---------------------|---------------|

This option is used when performing a partial initial start of the cluster. Each node should be started with this option, as well as [--nowait-nodes](#page-141-1).

Suppose that you have a 4-node cluster whose data nodes have the IDs 2, 3, 4, and 5, and you wish to perform a partial initial start using only nodes 2, 4, and 5—that is, omitting node 3:

```
$> ndbd --ndb-nodeid=2 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=4 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=5 --nowait-nodes=3 --initial-start
```

When using this option, you must also specify the node ID for the data node being started with the [--ndb-nodeid](#page-140-0) option.

![](_page_138_Picture_14.jpeg)

#### **Important**

Do not confuse this option with the [--nowait-nodes](#page-155-0) option for [ndb\\_mgmd](#page-149-0), which can be used to enable a cluster configured with multiple management servers to be started without all management servers being online.

<span id="page-138-1"></span>• [--install\[=](#page-138-1)name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndbd           |

Causes [ndbd](#page-134-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndbd. Although it is preferable to specify other [ndbd](#page-134-0) program options in a my.ini or my.cnf configuration file, it is possible to use together with - install. However, in such cases, the --install option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-137-0) option, since this causes the data node file system to be wiped and rebuilt every time the service is stopped and started. Extreme care should also be taken if you intend to use any of the other [ndbd](#page-134-0) options that affect the starting of data nodes—including [--initial-start](#page-138-0), [--nostart](#page-141-2), and [--nowait-nodes](#page-141-1)— together with [--install](#page-138-1), and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-138-1) option has no effect on non-Windows platforms.

<span id="page-139-1"></span>• [--logbuffer-size=](#page-139-1)#

| Command-Line Format | logbuffer-size=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 32768            |
| Minimum Value       | 2048             |
| Maximum Value       | 4294967295       |

Sets the size of the data node log buffer. When debugging with high amounts of extra logging, it is possible for the log buffer to run out of space if there are too many log messages, in which case some log messages can be lost. This should not occur during normal operations.

<span id="page-139-2"></span>• [--login-path](#page-139-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-139-3"></span>• [--no-login-paths](#page-139-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-139-0"></span>• [--ndb-connectstring](#page-139-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-139-4"></span>• [--ndb-log-timestamps](#page-139-4)

| Command-Line Format | ndb-log-timestamps |
|---------------------|--------------------|
| Type                | Enumeration        |
| Default Value       | LEGACY             |
| Valid Values        | LEGACY             |
|                     | UTC                |
|                     | SYSTEM             |

Sets the format used for timestamps in node logs. This is one of the following values: 4110

• LEGACY: The system timezone, with resolution in seconds.

- UTC: [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) format, with microsecond resolution.
- SYSTEM: RFC 3339 format.

LEGACY is the default in MySQL 8.4, for backwards compatibility with previous versions.

<span id="page-140-1"></span>• [--ndb-mgmd-host](#page-140-1)

| Command-Line Format | ndb-mgmd-host=connection_string |  |  |
|---------------------|---------------------------------|--|--|
| Type                | String                          |  |  |
| Default Value       | [none]                          |  |  |

Same as [--ndb-connectstring](#page-139-0).

<span id="page-140-2"></span>• [--ndb-mgm-tls](#page-140-2)

| Command-Line Format | ndb-mgm-tls=level |  |  |
|---------------------|-------------------|--|--|
| Type                | Enumeration       |  |  |
| Default Value       | relaxed           |  |  |
| Valid Values        | relaxed           |  |  |
|                     | strict            |  |  |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-140-0"></span>• [--ndb-nodeid](#page-140-0)

| Command-Line Format | ndb-nodeid=# |  |  |
|---------------------|--------------|--|--|
| Type                | Integer      |  |  |
| Default Value       | [none]       |  |  |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-140-3"></span>• [--ndb-optimized-node-selection](#page-140-3)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-140-4"></span>• [--ndb-tls-search-path](#page-140-4)

| Command-Line Format     | ndb-tls-search-path=list |  |  |
|-------------------------|--------------------------|--|--|
| Type                    | Path name                |  |  |
| Default Value (Unix)    | \$HOME/ndb-tls           |  |  |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |  |  |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-141-0"></span>• [--nodaemon](#page-141-0)

| Command-Line Format | nodaemon |
|---------------------|----------|
|---------------------|----------|

Prevents [ndbd](#page-134-0) or [ndbmtd](#page-148-0) from executing as a daemon process. This option overrides the [-](#page-136-1) [daemon](#page-136-1) option. This is useful for redirecting output to the screen when debugging the binary.

The default behavior for [ndbd](#page-134-0) and [ndbmtd](#page-148-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms, where it has no effect.

<span id="page-141-3"></span>• [--no-defaults](#page-141-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-141-2"></span>• [--nostart](#page-141-2), -n

| Command-Line Format | nostart |
|---------------------|---------|
|---------------------|---------|

Instructs [ndbd](#page-134-0) not to start automatically. When this option is used, [ndbd](#page-134-0) connects to the management server, obtains configuration data from it, and initializes communication objects. However, it does not actually start the execution engine until specifically requested to do so by the management server. This can be accomplished by issuing the proper START command in the management client (see Section 25.6.1, "Commands in the NDB Cluster Management Client").

<span id="page-141-1"></span>• [--nowait-nodes=](#page-141-1)node\_id\_1[, node\_id\_2[, ...]]

| Command-Line Format | nowait-nodes=list |  |  |
|---------------------|-------------------|--|--|
| Type                | String            |  |  |
| Default Value       |                   |  |  |

This option takes a list of data nodes for which the cluster does not wait, prior to starting.

This can be used to start the cluster in a partitioned state. For example, to start the cluster with only half of the data nodes (nodes 2, 3, 4, and 5) running in a 4-node cluster, you can start each [ndbd](#page-134-0) process with --nowait-nodes=3,5. In this case, the cluster starts as soon as nodes 2 and 4 connect, and does not wait StartPartitionedTimeout milliseconds for nodes 3 and 5 to connect as it would otherwise.

If you wanted to start up the same cluster as in the previous example without one [ndbd](#page-134-0) (say, for example, that the host machine for node 3 has suffered a hardware failure) then start nodes 2, 4, and 5 with --nowait-nodes=3. Then the cluster starts as soon as nodes 2, 4, and 5 connect, and does not wait for node 3 to start.

<span id="page-142-0"></span>• [--print-defaults](#page-142-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-142-1"></span>• [--remove\[=](#page-142-1)name]

| Command-Line Format | remove[=name] |  |  |
|---------------------|---------------|--|--|
| Platform Specific   | Windows       |  |  |
| Type                | String        |  |  |
| Default Value       | ndbd          |  |  |

Causes an [ndbd](#page-134-0) process that was previously installed as a Windows service to be removed. Optionally, you can specify a name for the service to be uninstalled; if not set, the service name defaults to ndbd.

The [--remove](#page-142-1) option has no effect on non-Windows platforms.

<span id="page-142-2"></span>• [--usage](#page-142-2)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-142-3"></span>• [--verbose](#page-142-3), -v

Causes extra debug output to be written to the node log.

You can also use NODELOG DEBUG ON and NODELOG DEBUG OFF to enable and disable this extra logging while the data node is running.

<span id="page-142-4"></span>• [--version](#page-142-4)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

[ndbd](#page-134-0) generates a set of log files which are placed in the directory specified by DataDir in the config.ini configuration file.

These log files are listed below. node\_id is and represents the node's unique identifier. For example, ndb\_2\_error.log is the error log generated by the data node whose node ID is 2.

• ndb\_node\_id\_error.log is a file containing records of all crashes which the referenced [ndbd](#page-134-0) process has encountered. Each record in this file contains a brief error string and a reference to a trace file for this crash. A typical entry in this file might appear as shown here:

```
Date/Time: Saturday 30 July 2004 - 00:20:01
Type of error: error
Message: Internal program error (failed ndbrequire)
Fault ID: 2341
Problem data: DbtupFixAlloc.cpp
Object of reference: DBTUP (Line: 173)
ProgramName: NDB Kernel
ProcessID: 14909
TraceFile: ndb_2_trace.log.2
***EOM***
```

Listings of possible [ndbd](#page-134-0) exit codes and messages generated when a data node process shuts down prematurely can be found in [Data Node Error Messages.](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md)

![](_page_143_Picture_1.jpeg)

#### **Important**

The last entry in the error log file is not necessarily the newest one (nor is it likely to be). Entries in the error log are not listed in chronological order; rather, they correspond to the order of the trace files as determined in the ndb\_node\_id\_trace.log.next file (see below). Error log entries are thus overwritten in a cyclical and not sequential fashion.

• ndb\_node\_id\_trace.log.trace\_id is a trace file describing exactly what happened just before the error occurred. This information is useful for analysis by the NDB Cluster development team.

It is possible to configure the number of these trace files that are created before old files are overwritten. trace\_id is a number which is incremented for each successive trace file.

- ndb\_node\_id\_trace.log.next is the file that keeps track of the next trace file number to be assigned.
- ndb\_node\_id\_out.log is a file containing any data output by the [ndbd](#page-134-0) process. This file is created only if [ndbd](#page-134-0) is started as a daemon, which is the default behavior.
- ndb\_node\_id.pid is a file containing the process ID of the [ndbd](#page-134-0) process when started as a daemon. It also functions as a lock file to avoid the starting of nodes with the same identifier.
- ndb\_node\_id\_signal.log is a file used only in debug versions of [ndbd](#page-134-0), where it is possible to trace all incoming, outgoing, and internal messages with their data in the [ndbd](#page-134-0) process.

It is recommended not to use a directory mounted through NFS because in some environments this can cause problems whereby the lock on the .pid file remains in effect even after the process has terminated.

To start [ndbd](#page-134-0), it may also be necessary to specify the host name of the management server and the port on which it is listening. Optionally, one may also specify the node ID that the process is to use.

```
$> ndbd --connect-string="nodeid=2;host=ndb_mgmd.mysql.com:1186"
```

See Section 25.4.3.3, "NDB Cluster Connection Strings", for additional information about this issue. For more information about data node configuration parameters, see Section 25.4.3.6, "Defining NDB Cluster Data Nodes".

When [ndbd](#page-134-0) starts, it actually initiates two processes. The first of these is called the "angel process"; its only job is to discover when the execution process has been completed, and then to restart the [ndbd](#page-134-0) process if it is configured to do so. Thus, if you attempt to kill [ndbd](#page-134-0) using the Unix kill command, it is necessary to kill both processes, beginning with the angel process. The preferred method of terminating an [ndbd](#page-134-0) process is to use the management client and stop the process from there.

The execution process uses one thread for reading, writing, and scanning data, as well as all other activities. This thread is implemented asynchronously so that it can easily handle thousands of concurrent actions. In addition, a watch-dog thread supervises the execution thread to make sure that it does not hang in an endless loop. A pool of threads handles file I/O, with each thread able to handle one open file. Threads can also be used for transporter connections by the transporters in the [ndbd](#page-134-0) process. In a multi-processor system performing a large number of operations (including updates), the [ndbd](#page-134-0) process can consume up to 2 CPUs if permitted to do so.

For a machine with many CPUs it is possible to use several [ndbd](#page-134-0) processes which belong to different node groups; however, such a configuration is still considered experimental and is not supported for MySQL 8.4 in a production setting. See Section 25.2.7, "Known Limitations of NDB Cluster".

# <span id="page-143-0"></span>**25.5.2 ndbinfo\_select\_all — Select From ndbinfo Tables**

[ndbinfo\\_select\\_all](#page-143-0) is a client program that selects all rows and columns from one or more tables in the ndbinfo database

Not all ndbinfo tables available in the mysql client can be read by this program (see later in this section). In addition, [ndbinfo\\_select\\_all](#page-143-0) can show information about some tables internal to ndbinfo which cannot be accessed using SQL, including the tables and columns metadata tables.

To select from one or more ndbinfo tables using [ndbinfo\\_select\\_all](#page-143-0), it is necessary to supply the names of the tables when invoking the program as shown here:

```
$> ndbinfo_select_all table_name1 [table_name2] [...]
```

#### For example:

|     |                  |   |   | \$> ndbinfo_select_all logbuffers logspaces |          |      |      |
|-----|------------------|---|---|---------------------------------------------|----------|------|------|
|     | == logbuffers == |   |   |                                             |          |      |      |
|     | node_id log_type |   |   | log_id log_part                             | total    | used | high |
| 5   | 0                | 0 | 0 | 33554432                                    | 262144 0 |      |      |
| 6   | 0                | 0 | 0 | 33554432                                    | 262144 0 |      |      |
| 7   | 0                | 0 | 0 | 33554432                                    | 262144 0 |      |      |
| 8   | 0                | 0 | 0 | 33554432                                    | 262144 0 |      |      |
|     | == logspaces ==  |   |   |                                             |          |      |      |
|     | node_id log_type |   |   | log_id log_part                             | total    | used | high |
| 5   | 0                | 0 | 0 | 268435456                                   | 0        | 0    |      |
| 5   | 0                | 0 | 1 | 268435456                                   | 0        | 0    |      |
| 5   | 0                | 0 | 2 | 268435456                                   | 0        | 0    |      |
| 5   | 0                | 0 | 3 | 268435456                                   | 0        | 0    |      |
| 6   | 0                | 0 | 0 | 268435456                                   | 0        | 0    |      |
| 6   | 0                | 0 | 1 | 268435456                                   | 0        | 0    |      |
| 6   | 0                | 0 | 2 | 268435456                                   | 0        | 0    |      |
| 6   | 0                | 0 | 3 | 268435456                                   | 0        | 0    |      |
| 7   | 0                | 0 | 0 | 268435456                                   | 0        | 0    |      |
| 7   | 0                | 0 | 1 | 268435456                                   | 0        | 0    |      |
| 7   | 0                | 0 | 2 | 268435456                                   | 0        | 0    |      |
| 7   | 0                | 0 | 3 | 268435456                                   | 0        | 0    |      |
| 8   | 0                | 0 | 0 | 268435456                                   | 0        | 0    |      |
| 8   | 0                | 0 | 1 | 268435456                                   | 0        | 0    |      |
| 8   | 0                | 0 | 2 | 268435456                                   | 0        | 0    |      |
| 8   | 0                | 0 | 3 | 268435456                                   | 0        | 0    |      |
| \$> |                  |   |   |                                             |          |      |      |

Options that can be used with [ndbinfo\\_select\\_all](#page-143-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-144-0"></span>• [--character-sets-dir](#page-144-0)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-144-1"></span>• [--core-file](#page-144-1)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-144-2"></span>• [--connect-retries](#page-144-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |

| Maximum Value | 12 |
|---------------|----|
|---------------|----|

Number of times to retry connection before giving up.

<span id="page-145-0"></span>• [--connect-retry-delay](#page-145-0)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-145-1"></span>• [--connect-string](#page-145-1)

| Command-Line Format | connect-string=connection-string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-146-0).

<span id="page-145-2"></span>• [--defaults-extra-file](#page-145-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-145-3"></span>• [--defaults-file](#page-145-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-145-4"></span>• [--defaults-group-suffix](#page-145-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-145-5"></span>• [--delay=seconds](#page-145-5)

| Command-Line Format | delay=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 5       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of seconds to wait between executing loops. Has no effect if [--loops](#page-146-1) is set to 0 or 1.

#### <span id="page-146-2"></span>• [--help](#page-146-2)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

#### <span id="page-146-3"></span>• [--login-path](#page-146-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

#### <span id="page-146-4"></span>• [--no-login-paths](#page-146-4)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

#### <span id="page-146-1"></span>• [--loops=number](#page-146-1), -l number

| Command-Line Format | loops=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 1       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of times to execute the select. Use [--delay](#page-145-5) to set the time between loops.

#### <span id="page-146-0"></span>• [--ndb-connectstring](#page-146-0)

| Command-Line Format | ndb-connectstring=connection<br>string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

### <span id="page-146-5"></span>• [--ndb-mgmd-host](#page-146-5)

| Command-Line Format | ndb-mgmd-host=connection-string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-146-0).

#### <span id="page-146-6"></span>• [--ndb-nodeid](#page-146-6)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|

| Type          | Integer |
|---------------|---------|
| Default Value | [none]  |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-147-0"></span>• [--ndb-optimized-node-selection](#page-147-0)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-147-1"></span>• [--no-defaults](#page-147-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-147-2"></span>• [--print-defaults](#page-147-2)

| Command-Line Format<br>print-defaults |
|---------------------------------------|
|---------------------------------------|

Print program argument list and exit.

<span id="page-147-3"></span>• [--usage](#page-147-3)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-147-4"></span>• [--version](#page-147-4)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

[ndbinfo\\_select\\_all](#page-143-0) is unable to read the following tables:

- arbitrator\_validity\_detail
- arbitrator\_validity\_summary
- cluster\_locks
- cluster\_operations
- cluster\_transactions
- disk\_write\_speed\_aggregate\_node
- locks\_per\_fragment
- memory\_per\_fragment
- memoryusage
- operations\_per\_fragment
- server\_locks
- server\_operations

- server\_transactions
- table\_info

## <span id="page-148-0"></span>**25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)**

[ndbmtd](#page-148-0) is a multithreaded version of [ndbd](#page-134-0), the process that is used to handle all the data in tables using the NDBCLUSTER storage engine. [ndbmtd](#page-148-0) is intended for use on host computers having multiple CPU cores. Except where otherwise noted, [ndbmtd](#page-148-0) functions in the same way as [ndbd](#page-134-0); therefore, in this section, we concentrate on the ways in which [ndbmtd](#page-148-0) differs from [ndbd](#page-134-0), and you should consult [Section 25.5.1, "ndbd — The NDB Cluster Data Node Daemon",](#page-134-0) for additional information about running NDB Cluster data nodes that apply to both the single-threaded and multithreaded versions of the data node process.

Command-line options and configuration parameters used with [ndbd](#page-134-0) also apply to [ndbmtd](#page-148-0). For more information about these options and parameters, see [Section 25.5.1, "ndbd — The NDB Cluster Data](#page-134-0) [Node Daemon",](#page-134-0) and Section 25.4.3.6, "Defining NDB Cluster Data Nodes", respectively.

[ndbmtd](#page-148-0) is also file system-compatible with [ndbd](#page-134-0). In other words, a data node running [ndbd](#page-134-0) can be stopped, the binary replaced with [ndbmtd](#page-148-0), and then restarted without any loss of data. (However, when doing this, you must make sure that [MaxNoOfExecutionThreads](#page-22-0) is set to an appropriate value before restarting the node if you wish for [ndbmtd](#page-148-0) to run in multithreaded fashion.) Similarly, an [ndbmtd](#page-148-0) binary can be replaced with [ndbd](#page-134-0) simply by stopping the node and then starting [ndbd](#page-134-0) in place of the multithreaded binary. It is not necessary when switching between the two to start the data node binary using [--initial](#page-137-0).

Using [ndbmtd](#page-148-0) differs from using [ndbd](#page-134-0) in two key respects:

- 1. Because [ndbmtd](#page-148-0) runs by default in single-threaded mode (that is, it behaves like [ndbd](#page-134-0)), you must configure it to use multiple threads. This can be done by setting an appropriate value in the config.ini file for the [MaxNoOfExecutionThreads](#page-22-0) configuration parameter or the [ThreadConfig](#page-27-0) configuration parameter. Using MaxNoOfExecutionThreads is simpler, but ThreadConfig offers more flexibility. For more information about these configuration parameters and their use, see [Multi-Threading Configuration Parameters \(ndbmtd\)](#page-21-2).
- 2. Trace files are generated by critical errors in [ndbmtd](#page-148-0) processes in a somewhat different fashion from how these are generated by [ndbd](#page-134-0) failures. These differences are discussed in more detail in the next few paragraphs.

Like [ndbd](#page-134-0), [ndbmtd](#page-148-0) generates a set of log files which are placed in the directory specified by DataDir in the config.ini configuration file. Except for trace files, these are generated in the same way and have the same names as those generated by [ndbd](#page-134-0).

In the event of a critical error, [ndbmtd](#page-148-0) generates trace files describing what happened just prior to the error' occurrence. These files, which can be found in the data node's DataDir, are useful for analysis of problems by the NDB Cluster Development and Support teams. One trace file is generated for each [ndbmtd](#page-148-0) thread. The names of these files have the following pattern:

```
ndb_node_id_trace.log.trace_id_tthread_id,
```

In this pattern, node\_id stands for the data node's unique node ID in the cluster, trace\_id is a trace sequence number, and thread\_id is the thread ID. For example, in the event of the failure of an [ndbmtd](#page-148-0) process running as an NDB Cluster data node having the node ID 3 and with [MaxNoOfExecutionThreads](#page-22-0) equal to 4, four trace files are generated in the data node's data directory. If the is the first time this node has failed, then these files are named ndb\_3\_trace.log.1\_t1, ndb\_3\_trace.log.1\_t2, ndb\_3\_trace.log.1\_t3, and ndb\_3\_trace.log.1\_t4. Internally, these trace files follow the same format as [ndbd](#page-134-0) trace files.

The [ndbd](#page-134-0) exit codes and messages that are generated when a data node process shuts down prematurely are also used by [ndbmtd](#page-148-0). See [Data Node Error Messages](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md), for a listing of these.

![](_page_149_Picture_1.jpeg)

#### **Note**

It is possible to use [ndbd](#page-134-0) and [ndbmtd](#page-148-0) concurrently on different data nodes in the same NDB Cluster. However, such configurations have not been tested extensively; thus, we cannot recommend doing so in a production setting at this time.

# <span id="page-149-0"></span>**25.5.4 ndb\_mgmd — The NDB Cluster Management Server Daemon**

The management server is the process that reads the cluster configuration file and distributes this information to all nodes in the cluster that request it. It also maintains a log of cluster activities. Management clients can connect to the management server and check the cluster's status.

All options that can be used with [ndb\\_mgmd](#page-149-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-149-1"></span>• [--bind-address=](#page-149-1)host

| Command-Line Format | bind-address=host |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | [none]            |

Causes the management server to bind to a specific network interface (host name or IP address). This option has no default value.

<span id="page-149-2"></span>• [--character-sets-dir](#page-149-2)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-149-3"></span>• [cluster-config-suffix](#page-149-3)

| Command-Line Format | cluster-config-suffix=name |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | [none]                     |

Override defaults group suffix when reading cluster configuration sections in my.cnf; used in testing.

<span id="page-149-4"></span>• [--config-cache](#page-149-4)

| Command-Line Format | config-cache[=TRUE FALSE] |
|---------------------|---------------------------|
| Type                | Boolean                   |
| Default Value       | TRUE                      |

This option, whose default value is 1 (or TRUE, or ON), can be used to disable the management server's configuration cache, so that it reads its configuration from config.ini every time it starts (see Section 25.4.3, "NDB Cluster Configuration Files"). You can do this by starting the [ndb\\_mgmd](#page-149-0) process with any one of the following options:

- --config-cache=0
- --config-cache=FALSE
- --config-cache=OFF

#### <span id="page-150-0"></span>• [--skip-config-cache](#page-150-0)

Using one of the options just listed is effective only if the management server has no stored configuration at the time it is started. If the management server finds any configuration cache files, then the --config-cache option or the --skip-config-cache option is ignored. Therefore, to disable configuration caching, the option should be used the first time that the management server is started. Otherwise—that is, if you wish to disable configuration caching for a management server that has already created a configuration cache—you must stop the management server, delete any existing configuration cache files manually, then restart the management server with --skipconfig-cache (or with --config-cache set equal to 0, OFF, or FALSE).

Configuration cache files are normally created in a directory named mysql-cluster under the installation directory (unless this location has been overridden using the [--configdir](#page-150-1) option). Each time the management server updates its configuration data, it writes a new cache file. The files are named sequentially in order of creation using the following format:

```
ndb_node-id_config.bin.seq-number
```

node-id is the management server's node ID; seq-number is a sequence number, beginning with 1. For example, if the management server's node ID is 5, then the first three configuration cache files would, when they are created, be named ndb\_5\_config.bin.1, ndb\_5\_config.bin.2, and ndb\_5\_config.bin.3.

If your intent is to purge or reload the configuration cache without actually disabling caching, you should start [ndb\\_mgmd](#page-149-0) with one of the options [--reload](#page-157-0) or [--initial](#page-152-0) instead of --skipconfig-cache.

To re-enable the configuration cache, simply restart the management server, but without the --config-cache or --skip-config-cache option that was used previously to disable the configuration cache.

[ndb\\_mgmd](#page-149-0) does not check for the configuration directory ([--configdir](#page-150-1)) or attempts to create one when --skip-config-cache is used. (Bug #13428853)

<span id="page-150-2"></span>• [--config-file=](#page-150-2)filename, -f filename

| Command-Line Format | config-file=file |
|---------------------|------------------|
| Disabled by         | skip-config-file |
| Type                | File name        |
| Default Value       |                  |

Instructs the management server as to which file it should use for its configuration file. By default, the management server looks for a file named config.ini in the same directory as the [ndb\\_mgmd](#page-149-0) executable; otherwise the file name and location must be specified explicitly.

This option has no default value, and is ignored unless the management server is forced to read the configuration file, either because [ndb\\_mgmd](#page-149-0) was started with the [--reload](#page-157-0) or [--initial](#page-152-0) option, or because the management server could not find any configuration cache. If [--config-file](#page-150-2) is specified without either of [--initial](#page-152-0) or [--reload](#page-157-0), [ndb\\_mgmd](#page-149-0) refuses to start.

The [--config-file](#page-150-2) option is also read if [ndb\\_mgmd](#page-149-0) was started with [--config-cache=OFF](#page-149-4). See Section 25.4.3, "NDB Cluster Configuration Files", for more information.

<span id="page-150-1"></span>• [--configdir=](#page-150-1)dir\_name

| Command-Line Format | configdir=directory  |
|---------------------|----------------------|
|                     | config-dir=directory |

| Type          | File name                  |
|---------------|----------------------------|
| Default Value | \$INSTALLDIR/mysql-cluster |

Specifies the cluster management server's configuration cache directory. This must be an absolute path. Otherwise, the management server refuses to start.

--config-dir is an alias for this option.

<span id="page-151-0"></span>• [--connect-retries](#page-151-0)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-151-1"></span>• [--connect-retry-delay](#page-151-1)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-151-2"></span>• [--connect-string](#page-151-2)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as --ndb-connectstring.

<span id="page-151-3"></span>• [--core-file](#page-151-3)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-151-4"></span>• [--daemon](#page-151-4), -d

| Command-Line Format | daemon |
|---------------------|--------|
|---------------------|--------|

Instructs [ndb\\_mgmd](#page-149-0) to start as a daemon process. This is the default behavior.

This option has no effect when running [ndb\\_mgmd](#page-149-0) on Windows platforms.

• [--defaults-extra-file](#page-151-5)

<span id="page-151-5"></span>

|  | 4122 |
|--|------|
|--|------|

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read given file after global files are read.

<span id="page-152-1"></span>• [--defaults-file](#page-152-1)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-152-2"></span>• [--defaults-group-suffix](#page-152-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-152-3"></span>• [--help](#page-152-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-152-0"></span>• [--initial](#page-152-0)

Configuration data is cached internally, rather than being read from the cluster global configuration file each time the management server is started (see Section 25.4.3, "NDB Cluster Configuration Files"). Using the --initial option overrides this behavior, by forcing the management server to delete any existing cache files, and then to re-read the configuration data from the cluster configuration file and to build a new cache.

This differs in two ways from the [--reload](#page-157-0) option. First, --reload forces the server to check the configuration file against the cache and reload its data only if the contents of the file are different from the cache. Second, --reload does not delete any existing cache files.

If [ndb\\_mgmd](#page-149-0) is invoked with --initial but cannot find a global configuration file, the management server cannot start.

When a management server starts, it checks for another management server in the same NDB Cluster and tries to use the other management server's configuration data. This behavior has implications when performing a rolling restart of an NDB Cluster with multiple management nodes. See Section 25.6.5, "Performing a Rolling Restart of an NDB Cluster", for more information.

When used together with the [--config-file](#page-150-2) option, the cache is cleared only if the configuration file is actually found.

<span id="page-152-4"></span>• [--install\[=](#page-152-4)name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndb_mgmd       |

Causes [ndb\\_mgmd](#page-149-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndb\_mgmd. Although it is preferable to specify other [ndb\\_mgmd](#page-149-0) program options in a my.ini or my.cnf configuration file, it is possible to use them together with [--install](#page-152-4). However, in such cases, the [--install](#page-152-4) option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-137-0) option, since this causes the configuration cache to be wiped and rebuilt every time the service is stopped and started. Care should also be taken if you intend to use any other [ndb\\_mgmd](#page-149-0) options that affect the starting of the management server, and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-152-4) option has no effect on non-Windows platforms.

<span id="page-153-0"></span>• [--interactive](#page-153-0)

| Command-Line Format | interactive |
|---------------------|-------------|
|---------------------|-------------|

Starts [ndb\\_mgmd](#page-149-0) in interactive mode; that is, an [ndb\\_mgm](#page-159-0) client session is started as soon as the management server is running. This option does not start any other NDB Cluster nodes.

<span id="page-153-1"></span>• [--log-name=](#page-153-1)name

| Command-Line Format | log-name=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | MgmtSrvr      |

Provides a name to be used for this node in the cluster log.

<span id="page-153-2"></span>• [--login-path](#page-153-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-153-3"></span>• [--no-login-paths](#page-153-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-153-4"></span>• [--mycnf](#page-153-4)

| Command-Line Format | mycnf |
|---------------------|-------|

Read configuration data from the my.cnf file.

• [--ndb-connectstring](#page-153-5)

<span id="page-153-5"></span>

|      | Command-Line Format | ndb<br>connectstring=connection_string |
|------|---------------------|----------------------------------------|
| 4124 | Type                | String                                 |

| Default Value | [none] |  |
|---------------|--------|--|
|---------------|--------|--|

Set connection string. Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf. Ignored if [--config-file](#page-150-2) is specified; a warning is issued if both options are used concurrently.

• [--ndb-log-timestamps](#page-139-4)

| Command-Line Format | ndb-log-timestamps |
|---------------------|--------------------|
| Type                | Enumeration        |
| Default Value       | LEGACY             |
| Valid Values        | LEGACY             |
|                     | UTC                |
|                     | SYSTEM             |

Sets the format used for timestamps in node logs. This is one of the following values:

- LEGACY: The system timezone, with resolution in seconds.
- UTC: [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) format, with microsecond resolution.
- SYSTEM: RFC 3339 format.

LEGACY is the default in MySQL 8.4, for backwards compatibility with previous versions.

<span id="page-154-0"></span>• [--ndb-mgm-tls](#page-154-0)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-154-1"></span>• [--ndb-mgmd-host](#page-154-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as --ndb-connectstring.

<span id="page-154-2"></span>• [--ndb-nodeid](#page-154-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

<span id="page-155-1"></span>• [--ndb-optimized-node-selection](#page-155-1)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-155-2"></span>• [--ndb-tls-search-path](#page-155-2)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-155-3"></span>• [--no-nodeid-checks](#page-155-3)

| Command-Line Format | no-nodeid-checks |
|---------------------|------------------|
|---------------------|------------------|

Do not perform any checks of node IDs.

<span id="page-155-4"></span>• [--nodaemon](#page-155-4)

| Command-Line Format | nodaemon |
|---------------------|----------|
|---------------------|----------|

Instructs [ndb\\_mgmd](#page-149-0) not to start as a daemon process.

The default behavior for [ndb\\_mgmd](#page-149-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms.

<span id="page-155-5"></span>• [--no-defaults](#page-155-5)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-155-0"></span>• [--nowait-nodes](#page-155-0)

| Command-Line Format | nowait-nodes=list |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | [none]            |
| Minimum Value       | 1                 |

| Maximum Value | 255 |
|---------------|-----|
|---------------|-----|

When starting an NDB Cluster is configured with two management nodes, each management server normally checks to see whether the other [ndb\\_mgmd](#page-149-0) is also operational and whether the other management server's configuration is identical to its own. However, it is sometimes desirable to start the cluster with only one management node (and perhaps to allow the other [ndb\\_mgmd](#page-149-0) to be started later). This option causes the management node to bypass any checks for any other management nodes whose node IDs are passed to this option, permitting the cluster to start as though configured to use only the management node that was started.

For purposes of illustration, consider the following portion of a config.ini file (where we have omitted most of the configuration parameters that are not relevant to this example):

```
[ndbd]
NodeId = 1
HostName = 198.51.100.101
[ndbd]
NodeId = 2
HostName = 198.51.100.102
[ndbd]
NodeId = 3
HostName = 198.51.100.103
[ndbd]
NodeId = 4
HostName = 198.51.100.104
[ndb_mgmd]
NodeId = 10
HostName = 198.51.100.150
[ndb_mgmd]
NodeId = 11
HostName = 198.51.100.151
[api]
NodeId = 20
HostName = 198.51.100.200
[api]
NodeId = 21
HostName = 198.51.100.201
```

Assume that you wish to start this cluster using only the management server having node ID 10 and running on the host having the IP address 198.51.100.150. (Suppose, for example, that the host computer on which you intend to the other management server is temporarily unavailable due to a hardware failure, and you are waiting for it to be repaired.) To start the cluster in this way, use a command line on the machine at 198.51.100.150 to enter the following command:

```
$> ndb_mgmd --ndb-nodeid=10 --nowait-nodes=11
```

As shown in the preceding example, when using [--nowait-nodes](#page-155-0), you must also use the [--ndb](#page-154-2)[nodeid](#page-154-2) option to specify the node ID of this [ndb\\_mgmd](#page-149-0) process.

You can then start each of the cluster's data nodes in the usual way. If you wish to start and use the second management server in addition to the first management server at a later time without restarting the data nodes, you must start each data node with a connection string that references both management servers, like this:

```
$> ndbd -c 198.51.100.150,198.51.100.151
```

The same is true with regard to the connection string used with any mysqld processes that you wish to start as NDB Cluster SQL nodes connected to this cluster. See Section 25.4.3.3, "NDB Cluster Connection Strings", for more information.

When used with [ndb\\_mgmd](#page-149-0), this option affects the behavior of the management node with regard to other management nodes only. Do not confuse it with the [--nowait-nodes](#page-141-1) option used with [ndbd](#page-134-0) or [ndbmtd](#page-148-0) to permit a cluster to start with fewer than its full complement of data nodes; when used with data nodes, this option affects their behavior only with regard to other data nodes.

Multiple management node IDs may be passed to this option as a comma-separated list. Each node ID must be no less than 1 and no greater than 255. In practice, it is quite rare to use more than two management servers for the same NDB Cluster (or to have any need for doing so); in most cases you need to pass to this option only the single node ID for the one management server that you do not wish to use when starting the cluster.

![](_page_157_Picture_6.jpeg)

#### **Note**

When you later start the "missing" management server, its configuration must match that of the management server that is already in use by the cluster. Otherwise, it fails the configuration check performed by the existing management server, and does not start.

<span id="page-157-1"></span>• [--print-defaults](#page-157-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-157-2"></span>• [--print-full-config](#page-157-2), -P

| Command-Line Format | print-full-config |
|---------------------|-------------------|
|---------------------|-------------------|

Shows extended information regarding the configuration of the cluster. With this option on the command line the [ndb\\_mgmd](#page-149-0) process prints information about the cluster setup including an extensive list of the cluster configuration sections as well as parameters and their values. Normally used together with the [--config-file](#page-150-2) (-f) option.

<span id="page-157-0"></span>• [--reload](#page-157-0)

| Command-Line Format | reload |
|---------------------|--------|
|---------------------|--------|

NDB Cluster configuration data is stored internally rather than being read from the cluster global configuration file each time the management server is started (see Section 25.4.3, "NDB Cluster Configuration Files"). Using this option forces the management server to check its internal data store against the cluster configuration file and to reload the configuration if it finds that the configuration file does not match the cache. Existing configuration cache files are preserved, but not used.

This differs in two ways from the [--initial](#page-152-0) option. First, --initial causes all cache files to be deleted. Second, --initial forces the management server to re-read the global configuration file and construct a new cache.

If the management server cannot find a global configuration file, then the --reload option is ignored.

When --reload is used, the management server must be able to communicate with data nodes and any other management servers in the cluster before it attempts to read the global configuration file; otherwise, the management server fails to start. This can happen due to changes in the networking environment, such as new IP addresses for nodes or an altered firewall configuration. In such cases, you must use [--initial](#page-152-0) instead to force the existing cached configuration to be discarded and reloaded from the file. See Section 25.6.5, "Performing a Rolling Restart of an NDB Cluster", for additional information.

<span id="page-158-0"></span>• [--remove\[=name\]](#page-158-0)

| Command-Line Format | remove[=name] |
|---------------------|---------------|
| Platform Specific   | Windows       |
| Type                | String        |
| Default Value       | ndb_mgmd      |

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-158-1"></span>• [--skip-config-file](#page-158-1)

| Command-Line Format | skip-config-file |
|---------------------|------------------|
|---------------------|------------------|

Do not read cluster configuration file; ignore [--initial](#page-152-0) and [--reload](#page-157-0) options if specified.

<span id="page-158-2"></span>• [--usage](#page-158-2)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-158-3"></span>• [--verbose](#page-158-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-158-4"></span>• [--version](#page-158-4)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

It is not strictly necessary to specify a connection string when starting the management server. However, if you are using more than one management server, a connection string should be provided and each node in the cluster should specify its node ID explicitly. 4129 See Section 25.4.3.3, "NDB Cluster Connection Strings", for information about using connection strings. [Section 25.5.4, "ndb\\_mgmd — The NDB Cluster Management Server Daemon"](#page-149-0), describes other options for [ndb\\_mgmd](#page-149-0).

The following files are created or used by [ndb\\_mgmd](#page-149-0) in its starting directory, and are placed in the DataDir as specified in the config.ini configuration file. In the list that follows, node\_id is the unique node identifier.

- config.ini is the configuration file for the cluster as a whole. This file is created by the user and read by the management server. Section 25.4, "Configuration of NDB Cluster", discusses how to set up this file.
- ndb\_node\_id\_cluster.log is the cluster events log file. Examples of such events include checkpoint startup and completion, node startup events, node failures, and levels of memory usage. A complete listing of cluster events with descriptions may be found in Section 25.6, "Management of NDB Cluster".

By default, when the size of the cluster log reaches one million bytes, the file is renamed to ndb\_node\_id\_cluster.log.seq\_id, where seq\_id is the sequence number of the cluster log file. (For example: If files with the sequence numbers 1, 2, and 3 already exist, the next log file is named using the number 4.) You can change the size and number of files, and other characteristics of the cluster log, using the LogDestination configuration parameter.

- ndb\_node\_id\_out.log is the file used for stdout and stderr when running the management server as a daemon.
- ndb\_node\_id.pid is the process ID file used when running the management server as a daemon.

## <span id="page-159-0"></span>**25.5.5 ndb\_mgm — The NDB Cluster Management Client**

The [ndb\\_mgm](#page-159-0) management client process is actually not needed to run the cluster. Its value lies in providing a set of commands for checking the cluster's status, starting backups, and performing other administrative functions. The management client accesses the management server using a C API. Advanced users can also employ this API for programming dedicated management processes to perform tasks similar to those performed by [ndb\\_mgm](#page-159-0).

To start the management client, it is necessary to supply the host name and port number of the management server:

```
$> ndb_mgm [host_name [port_num]]
```

For example:

```
$> ndb_mgm ndb_mgmd.mysql.com 1186
```

The default host name and port number are localhost and 1186, respectively.

All options that can be used with [ndb\\_mgm](#page-159-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-159-1"></span>• [--backup-password-from-stdin\[=TRUE|FALSE\]](#page-159-1)

| Command-Line Format | backup-password-from-stdin |
|---------------------|----------------------------|

This option enables input of the backup password from the system shell (stdin) when using - execute "START BACKUP" or similar to create a backup. Use of this option requires use of [-](#page-161-0) [execute](#page-161-0) as well.

<span id="page-159-2"></span>• [--character-sets-dir](#page-159-2)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|                     |                         |

Directory containing character sets.

#### <span id="page-160-0"></span>• [--connect-retries=](#page-160-0)#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 3                 |
| Minimum Value       | 0                 |
| Maximum Value       | 4294967295        |

This option specifies the number of times following the first attempt to retry a connection before giving up (the client always tries the connection at least once). The length of time to wait per attempt is set using [--connect-retry-delay](#page-151-1).

This option is synonymous with the [--try-reconnect](#page-163-0) option, which is now deprecated.

#### <span id="page-160-1"></span>• [--connect-retry-delay](#page-160-1)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-160-2"></span>• [--connect-string](#page-160-2)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-162-0).

#### <span id="page-160-3"></span>• [--core-file](#page-160-3)

| Command-Line Format | core-file |
|---------------------|-----------|
|                     |           |

Write core file on error; used in debugging.

#### <span id="page-160-4"></span>• [--defaults-extra-file](#page-160-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

#### <span id="page-160-5"></span>• [--defaults-file](#page-160-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-161-1"></span>• [--defaults-group-suffix](#page-161-1)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-161-2"></span>• [--encrypt-backup](#page-161-2)

| Command-Line Format | encrypt-backup |
|---------------------|----------------|

When used, this option causes all backups to be encrypted. To make this happen whenever [ndb\\_mgm](#page-159-0) is run, put the option in the [ndb\_mgm] section of the my.cnf file.

<span id="page-161-0"></span>• [--execute=command](#page-161-0), -e command

| Command-Line Format | execute=command |
|---------------------|-----------------|

This option can be used to send a command to the NDB Cluster management client from the system shell. For example, either of the following is equivalent to executing SHOW in the management client:

```
$> ndb_mgm -e "SHOW"
$> ndb_mgm --execute="SHOW"
```

This is analogous to how the --execute or -e option works with the mysql command-line client. See Section 6.2.2.1, "Using Options on the Command Line".

![](_page_161_Picture_13.jpeg)

#### **Note**

If the management client command to be passed using this option contains any space characters, then the command must be enclosed in quotation marks. Either single or double quotation marks may be used. If the management client command contains no space characters, the quotation marks are optional.

<span id="page-161-3"></span>• [--help](#page-161-3)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-161-4"></span>• [--login-path](#page-161-4)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-161-5"></span>• [--no-login-paths](#page-161-5)

| Command-Line Format | no-login-paths |
|---------------------|----------------|

Skips reading options from the login path file.

#### <span id="page-162-0"></span>• [--ndb-connectstring](#page-162-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

#### <span id="page-162-1"></span>• [--ndb-nodeid](#page-162-1)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-162-0).

#### <span id="page-162-2"></span>• [--ndb-mgm-tls](#page-162-2)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

### <span id="page-162-3"></span>• [--ndb-mgmd-host](#page-162-3)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-162-0).

#### <span id="page-162-4"></span>• [--ndb-optimized-node-selection](#page-162-4)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|                     |                              |

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-162-5"></span>• [--ndb-tls-search-path](#page-162-5)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-163-1"></span>• [--no-defaults](#page-163-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-163-2"></span>• [--print-defaults](#page-163-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-163-3"></span>• [--test-tls](#page-163-3)

| Command-Line Format | test-tls |
|---------------------|----------|
|---------------------|----------|

Connect using TLS, then exit. Output if successful is similar to what is shown here:

```
>$ ndb_mgm --test-tls
Connected to Management Server at: sakila:1186
>$
```

See Section 25.6.19.5, "TLS Link Encryption for NDB Cluster", for more information.

<span id="page-163-0"></span>• [--try-reconnect=](#page-163-0)number

| Command-Line Format | try-reconnect=# |
|---------------------|-----------------|
| Deprecated          | Yes             |
| Type                | Numeric         |
| Type                | Integer         |
| Default Value       | 12              |
| Default Value       | 3               |
| Minimum Value       | 0               |
| Maximum Value       | 4294967295      |

If the connection to the management server is broken, the node tries to reconnect to it every 5 seconds until it succeeds. By using this option, it is possible to limit the number of attempts to number before giving up and reporting an error instead.

This option is deprecated and subject to removal in a future release. Use [--connect-retries](#page-160-0), instead.

<span id="page-164-0"></span>• [--usage](#page-164-0)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-161-3).

<span id="page-164-1"></span>• [--version](#page-164-1)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

Additional information about using [ndb\\_mgm](#page-159-0) can be found in Section 25.6.1, "Commands in the NDB Cluster Management Client".

# <span id="page-164-2"></span>**25.5.6 ndb\_blob\_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables**

This tool can be used to check for and remove orphaned BLOB column parts from NDB tables, as well as to generate a file listing any orphaned parts. It is sometimes useful in diagnosing and repairing corrupted or damaged NDB tables containing BLOB or TEXT columns.

The basic syntax for [ndb\\_blob\\_tool](#page-164-2) is shown here:

```
ndb_blob_tool [options] table [column, ...]
```

Unless you use the [--help](#page-166-0) option, you must specify an action to be performed by including one or more of the options [--check-orphans](#page-165-0), [--delete-orphans](#page-166-1), or [--dump-file](#page-166-2). These options cause [ndb\\_blob\\_tool](#page-164-2) to check for orphaned BLOB parts, remove any orphaned BLOB parts, and generate a dump file listing orphaned BLOB parts, respectively, and are described in more detail later in this section.

You must also specify the name of a table when invoking [ndb\\_blob\\_tool](#page-164-2). In addition, you can optionally follow the table name with the (comma-separated) names of one or more BLOB or TEXT columns from that table. If no columns are listed, the tool works on all of the table's BLOB and TEXT columns. If you need to specify a database, use the [--database](#page-165-1) (-d) option.

The [--verbose](#page-168-0) option provides additional information in the output about the tool's progress.

All options that can be used with [ndb\\_mgmd](#page-149-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-164-3"></span>• [--add-missing](#page-164-3)

| Command-Line Format | add-missing |
|---------------------|-------------|
|---------------------|-------------|

For each inline part in NDB Cluster tables which has no corresponding BLOB part, write a dummy BLOB part of the required length, consisting of spaces.

<span id="page-164-4"></span>• [--character-sets-dir](#page-164-4)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-164-5"></span>• [--check-missing](#page-164-5)

| Command-Line Format | check-missing |
|---------------------|---------------|
|---------------------|---------------|

Check for inline parts in NDB Cluster tables which have no corresponding BLOB parts.

<span id="page-165-0"></span>• [--check-orphans](#page-165-0)

| Command-Line Format | check-orphans |
|---------------------|---------------|
|---------------------|---------------|

Check for BLOB parts in NDB Cluster tables which have no corresponding inline parts.

<span id="page-165-2"></span>• [--connect-retries](#page-165-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-165-3"></span>• [--connect-retry-delay](#page-165-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-165-4"></span>• [--connect-string](#page-165-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-166-3).

<span id="page-165-5"></span>• [--core-file](#page-165-5)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-165-1"></span>• [--database=](#page-165-1)db\_name, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [none]        |

Specify the database to find the table in.

<span id="page-165-6"></span>• [--defaults-extra-file](#page-165-6)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read given file after global files are read.

<span id="page-166-4"></span>• [--defaults-file](#page-166-4)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-166-5"></span>• [--defaults-group-suffix](#page-166-5)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-166-1"></span>• [--delete-orphans](#page-166-1)

| Command-Line Format | delete-orphans |
|---------------------|----------------|
|---------------------|----------------|

Remove BLOB parts from NDB Cluster tables which have no corresponding inline parts.

<span id="page-166-2"></span>• [--dump-file=](#page-166-2)file

| Command-Line Format | dump-file=file |
|---------------------|----------------|
| Type                | File name      |
| Default Value       | [none]         |

Writes a list of orphaned BLOB column parts to file. The information written to the file includes the table key and BLOB part number for each orphaned BLOB part.

<span id="page-166-0"></span>• [--help](#page-166-0)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-166-6"></span>• [--login-path](#page-166-6)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-166-7"></span>• [--no-login-paths](#page-166-7)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-166-3"></span>• [--ndb-connectstring](#page-166-3)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-167-0"></span>• [--ndb-mgm-tls](#page-167-0)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-167-1"></span>• [--ndb-mgmd-host](#page-167-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-166-3).

<span id="page-167-2"></span>• [--ndb-nodeid](#page-167-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-167-3"></span>• [--ndb-optimized-node-selection](#page-167-3)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-167-4"></span>• [--ndb-tls-search-path](#page-167-4)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-168-1"></span>• [--no-defaults](#page-168-1)

| Command-Line Format<br>no-defaults |  |
|------------------------------------|--|
|------------------------------------|--|

Do not read default options from any option file other than login file.

<span id="page-168-2"></span>• [--print-defaults](#page-168-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-168-3"></span>• [--usage](#page-168-3)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-168-0"></span>• [--verbose](#page-168-0)

| Command-Line Format | verbose |
|---------------------|---------|

Provide extra information in the tool's output regarding its progress.

<span id="page-168-4"></span>• [--version](#page-168-4)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

## **Example**

First we create an NDB table in the test database, using the CREATE TABLE statement shown here:

```
USE test;
CREATE TABLE btest (
 c0 BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 c1 TEXT,
 c2 BLOB
) ENGINE=NDB;
```

Then we insert a few rows into this table, using a series of statements similar to this one:

```
INSERT INTO btest VALUES (NULL, 'x', REPEAT('x', 1000));
```

When run with [--check-orphans](#page-165-0) against this table, [ndb\\_blob\\_tool](#page-164-2) generates the following output:

```
$> ndb_blob_tool --check-orphans --verbose -d test btest
connected
```

```
processing 2 blobs
processing blob #0 c1 NDB$BLOB_19_1
NDB$BLOB_19_1: nextResult: res=1
total parts: 0
orphan parts: 0
processing blob #1 c2 NDB$BLOB_19_2
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=1
total parts: 10
orphan parts: 0
disconnected
```

The tool reports that there are no NDB BLOB column parts associated with column c1, even though c1 is a TEXT column. This is due to the fact that, in an NDB table, only the first 256 bytes of a BLOB or TEXT column value are stored inline, and only the excess, if any, is stored separately; thus, if there are no values using more than 256 bytes in a given column of one of these types, no BLOB column parts are created by NDB for this column. See Section 13.7, "Data Type Storage Requirements", for more information.

## <span id="page-169-0"></span>**25.5.7 ndb\_config — Extract NDB Cluster Configuration Information**

This tool extracts current configuration information for data nodes, SQL nodes, and API nodes from one of a number of sources: an NDB Cluster management node, or its config.ini or my.cnf file. By default, the management node is the source for the configuration data; to override the default, execute ndb\_config with the [--config-file](#page-171-0) or [--mycnf](#page-174-0) option. It is also possible to use a data node as the source by specifying its node ID with [--config\\_from\\_node=](#page-171-1)node\_id.

[ndb\\_config](#page-169-0) can also provide an offline dump of all configuration parameters which can be used, along with their default, maximum, and minimum values and other information. The dump can be produced in either text or XML format; for more information, see the discussion of the [--configinfo](#page-170-0) and [--xml](#page-177-0) options later in this section).

You can filter the results by section (DB, SYSTEM, or CONNECTIONS) using one of the options [-](#page-176-0) [nodes](#page-176-0), [--system](#page-177-1), or [--connections](#page-172-0).

All options that can be used with [ndb\\_config](#page-169-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-169-1"></span>• [--character-sets-dir](#page-169-1)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-169-2"></span>• [cluster-config-suffix](#page-169-2)

| Command-Line Format | cluster-config-suffix=name |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | [none]                     |

Override defaults group suffix when reading cluster configuration sections in my.cnf; used in testing.

<span id="page-170-0"></span>• [--configinfo](#page-170-0)

The --configinfo option causes [ndb\\_config](#page-169-0) to dump a list of each NDB Cluster configuration parameter supported by the NDB Cluster distribution of which [ndb\\_config](#page-169-0) is a part, including the following information:

- A brief description of each parameter's purpose, effects, and usage
- The section of the config.ini file where the parameter may be used
- The parameter's data type or unit of measurement
- Where applicable, the parameter's default, minimum, and maximum values
- NDB Cluster release version and build information

By default, this output is in text format. Part of this output is shown here:

```
$> ndb_config --configinfo
****** SYSTEM ******
Name (String)
Name of system (NDB Cluster)
MANDATORY
PrimaryMGMNode (Non-negative Integer)
Node id of Primary ndb_mgmd(MGM) node
Default: 0 (Min: 0, Max: 4294967039)
ConfigGenerationNumber (Non-negative Integer)
Configuration generation number
Default: 0 (Min: 0, Max: 4294967039)
****** DB ******
MaxNoOfSubscriptions (Non-negative Integer)
Max no of subscriptions (default 0 == MaxNoOfTables)
Default: 0 (Min: 0, Max: 4294967039)
MaxNoOfSubscribers (Non-negative Integer)
Max no of subscribers (default 0 == 2 * MaxNoOfTables)
Default: 0 (Min: 0, Max: 4294967039)
```

Use this option together with the [--xml](#page-177-0) option to obtain output in XML format.

<span id="page-170-1"></span>• [--config-binary-file=](#page-170-1)path-to-file

| Command-Line Format | config-binary-file=path/to/file |
|---------------------|---------------------------------|
| Type                | File name                       |
| Default Value       |                                 |

Gives the path to the management server's cached binary configuration file (ndb\_nodeID\_config.bin.seqno). This may be a relative or absolute path. If the management server and the [ndb\\_config](#page-169-0) binary used reside on different hosts, you must use an absolute path.

This example demonstrates combining --config-binary-file with other [ndb\\_config](#page-169-0) options to obtain useful output:

```
$> ndb_config --config-binary-file=../mysql-cluster/ndb_50_config.bin.1 --diff-default --type=ndbd
config of [DB] node id 5 that is different from default 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
NodeId,5,(mandatory) 
BackupDataDir,/local/data/8.4,(null)
```

```
DataDir,/local/data/8.4,. 
DataMemory,2G,98M 
FileSystemPath,/local/data/8.4,(null) 
HostName,127.0.0.1,localhost 
Nodegroup,0,(null) 
ThreadConfig,,(null) 
config of [DB] node id 6 that is different from default 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
NodeId,6,(mandatory) 
BackupDataDir,/local/data/8.4,(null) 
DataDir,/local/data/8.4. 
DataMemory,2G,98M 
FileSystemPath,/local/data/8.4,(null) 
HostName,127.0.0.1,localhost 
Nodegroup,0,(null) 
ThreadConfig,,(null)
$> ndb_config --config-binary-file=../mysql-cluster/ndb_50_config.bin.1 --diff-default --system
config of [SYSTEM] system 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
Name,MC_20220906060042,(mandatory) 
ConfigGenerationNumber,1,0 
PrimaryMGMNode,50,0
```

The relevant portions of the config.ini file are shown here:

```
[ndbd default]
DataMemory= 2G
NoOfReplicas= 2
[ndb_mgmd]
NodeId= 50
HostName= 127.0.0.1
[ndbd]
NodeId= 5
HostName= 127.0.0.1
DataDir= /local/data/8.4
[ndbd]
NodeId= 6
HostName= 127.0.0.1
DataDir= /local/data/8.4
```

By comparing the output with the configuration file, you can see that all of the settings in the file have been written by the management server to the binary cache, and thus, applied to the cluster.

<span id="page-171-0"></span>• [--config-file=](#page-171-0)path-to-file

| Command-Line Format | config-file=file_name |
|---------------------|-----------------------|
| Type                | File name             |
| Default Value       |                       |

Gives the path to the cluster configuration file (config.ini). This may be a relative or absolute path. If the management server and the [ndb\\_config](#page-169-0) binary used reside on different hosts, you must use an absolute path.

<span id="page-171-1"></span>• [--config\\_from\\_node=#](#page-171-1)

| Command-Line Format | config-from-node=# |
|---------------------|--------------------|
| Type                | Numeric            |
| Default Value       | none               |
| Minimum Value       | 1                  |

| Maximum Value | 48 |  |
|---------------|----|--|
|---------------|----|--|

Obtain the cluster's configuration data from the data node that has this ID.

If the node having this ID is not a data node, [ndb\\_config](#page-169-0) fails with an error. (To obtain configuration data from the management node instead, simply omit this option.)

#### <span id="page-172-1"></span>• [--connect-retries](#page-172-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

#### <span id="page-172-2"></span>• [--connect-retry-delay](#page-172-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-172-3"></span>• [--connect-string](#page-172-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-174-1).

#### <span id="page-172-0"></span>• [--connections](#page-172-0)

| Command-Line Format | connections |
|---------------------|-------------|
|---------------------|-------------|

Tells [ndb\\_config](#page-169-0) to print CONNECTIONS information only—that is, information about parameters found in the [tcp], [tcp default], [shm], or [shm default] sections of the cluster configuration file (see [Section 25.4.3.10, "NDB Cluster TCP/IP Connections",](#page-114-3) and [Section 25.4.3.12,](#page-122-0) ["NDB Cluster Shared-Memory Connections"](#page-122-0), for more information).

This option is mutually exclusive with [--nodes](#page-176-0) and [--system](#page-177-1); only one of these 3 options can be used.

#### <span id="page-172-4"></span>• [--core-file](#page-172-4)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

#### <span id="page-172-5"></span>• [--defaults-extra-file](#page-172-5)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
|---------------------|--------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read given file after global files are read.

<span id="page-173-0"></span>• [--defaults-file](#page-173-0)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-173-1"></span>• [--defaults-group-suffix](#page-173-1)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-173-2"></span>• [--diff-default](#page-173-2)

| Command-Line Format | diff-default |
|---------------------|--------------|
|---------------------|--------------|

Print only configuration parameters that have non-default values.

<span id="page-173-3"></span>• [--fields=](#page-173-3)delimiter, -f delimiter

| Command-Line Format | fields=string |
|---------------------|---------------|
| Type                | String        |
| Default Value       |               |

Specifies a delimiter string used to separate the fields in the result. The default is , (the comma character).

![](_page_173_Picture_15.jpeg)

#### **Note**

If the delimiter contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

<span id="page-173-4"></span>• [--help](#page-173-4)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-173-5"></span>• --host=[hostname](#page-173-5)

| Command-Line Format | host=name |
|---------------------|-----------|
| Type                | String    |

Default Value

Specifies the host name of the node for which configuration information is to be obtained.

![](_page_174_Picture_3.jpeg)

#### **Note**

While the hostname localhost usually resolves to the IP address 127.0.0.1, this may not necessarily be true for all operating platforms and configurations. This means that it is possible, when localhost is used in config.ini, for [ndb\\_config --host=localhost](#page-169-0) to fail if [ndb\\_config](#page-169-0) is run on a different host where localhost resolves to a different address (for example, on some versions of SUSE Linux, this is 127.0.0.2). In general, for best results, you should use numeric IP addresses for all NDB Cluster configuration values relating to hosts, or verify that all NDB Cluster hosts handle localhost in the same fashion.

#### <span id="page-174-2"></span>• [--login-path](#page-174-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

#### <span id="page-174-0"></span>• [--mycnf](#page-174-0)

| Command-Line Format | mycnf |
|---------------------|-------|
|---------------------|-------|

Read configuration data from the my.cnf file.

<span id="page-174-1"></span>• [--ndb-connectstring=](#page-174-1)connection\_string, -c connection\_string

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Specifies the connection string to use in connecting to the management server. The format for the connection string is the same as described in Section 25.4.3.3, "NDB Cluster Connection Strings", and defaults to localhost:1186.

#### <span id="page-174-3"></span>• [--ndb-mgm-tls](#page-174-3)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

#### <span id="page-174-4"></span>• [--ndb-mgmd-host](#page-174-4)

| Command-Line Format | ndb-mgmd-host=connection_string |  |
|---------------------|---------------------------------|--|
|---------------------|---------------------------------|--|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Same as [--ndb-connectstring](#page-174-1).

<span id="page-175-0"></span>• [--ndb-nodeid](#page-175-0)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-174-1).

<span id="page-175-1"></span>• [--ndb-optimized-node-selection](#page-175-1)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-175-2"></span>• [--ndb-tls-search-path](#page-175-2)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-175-3"></span>• [--no-defaults](#page-175-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-175-4"></span>• [--no-login-paths](#page-175-4)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-175-5"></span>• [--nodeid=](#page-175-5)node\_id

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Specify the node ID of the node for which configuration information is to be obtained.

<span id="page-176-0"></span>• [--nodes](#page-176-0)

| Command-Line Format | nodes |
|---------------------|-------|
|---------------------|-------|

Tells [ndb\\_config](#page-169-0) to print information relating only to parameters defined in an [ndbd] or [ndbd default] section of the cluster configuration file (see Section 25.4.3.6, "Defining NDB Cluster Data Nodes").

This option is mutually exclusive with [--connections](#page-172-0) and [--system](#page-177-1); only one of these 3 options can be used.

<span id="page-176-1"></span>• [--print-defaults](#page-176-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-176-2"></span>• --query=[query-options](#page-176-2), -q query-options

| Command-Line Format | query=string |
|---------------------|--------------|
| Type                | String       |
| Default Value       |              |

This is a comma-delimited list of query options—that is, a list of one or more node attributes to be returned. These include nodeid (node ID), type (node type—that is, ndbd, mysqld, or ndb\_mgmd), and any configuration parameters whose values are to be obtained.

For example, --query=nodeid,type,datamemory,datadir returns the node ID, node type, DataMemory, and DataDir for each node.

![](_page_176_Picture_14.jpeg)

## **Note**

If a given parameter is not applicable to a certain type of node, than an empty string is returned for the corresponding value. See the examples later in this section for more information.

<span id="page-176-3"></span>• [--query-all](#page-176-3), -a

| Command-Line Format | query-all |
|---------------------|-----------|
| Type                | String    |
| Default Value       |           |

Returns a comma-delimited list of all query options (node attributes; note that this list is a single string.

<span id="page-176-4"></span>• --rows=[separator](#page-176-4), -r separator

| Command-Line Format | rows=string |
|---------------------|-------------|
| Type                | String      |
| Default Value       |             |

Specifies a separator string used to separate the rows in the result. The default is a space character.

![](_page_177_Picture_1.jpeg)

#### **Note**

If the separator contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

<span id="page-177-1"></span>• [--system](#page-177-1)

| Command-Line Format | system |
|---------------------|--------|
|---------------------|--------|

Tells [ndb\\_config](#page-169-0) to print SYSTEM information only. This consists of system variables that cannot be changed at run time; thus, there is no corresponding section of the cluster configuration file for them. They can be seen (prefixed with \*\*\*\*\*\* SYSTEM \*\*\*\*\*\*) in the output of [ndb\\_config](#page-169-0) [-](#page-170-0) [configinfo](#page-170-0).

This option is mutually exclusive with [--nodes](#page-176-0) and [--connections](#page-172-0); only one of these 3 options can be used.

<span id="page-177-2"></span>• --type=[node\\_type](#page-177-2)

| Command-Line Format | type=name   |
|---------------------|-------------|
| Type                | Enumeration |
| Default Value       | [none]      |
| Valid Values        | ndbd        |
|                     | mysqld      |
|                     | ndb_mgmd    |

Filters results so that only configuration values applying to nodes of the specified node\_type (ndbd, mysqld, or ndb\_mgmd) are returned.

<span id="page-177-3"></span>• [--usage](#page-177-3), --help, or -?

| Command-Line Format |      |
|---------------------|------|
|                     | help |

Causes [ndb\\_config](#page-169-0) to print a list of available options, and then exit.

<span id="page-177-4"></span>• [--version](#page-177-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Causes [ndb\\_config](#page-169-0) to print a version information string, and then exit.

<span id="page-177-0"></span>• --configinfo [--xml](#page-177-0)

```
Command-Line Format --configinfo --xml
```

Cause [ndb\\_config](#page-169-0) [--configinfo](#page-170-0) to provide output as XML by adding this option. A portion of such output is shown in this example:

```
$> ndb_config --configinfo --xml
<configvariables protocolversion="1" ndbversionstring="5.7.44-ndb-7.5.36"
 ndbversion="460032" ndbversionmajor="7" ndbversionminor="5"
 ndbversionbuild="0">
 <section name="SYSTEM">
 <param name="Name" comment="Name of system (NDB Cluster)" type="string"
 mandatory="true"/>
 <param name="PrimaryMGMNode" comment="Node id of Primary ndb_mgmd(MGM) node"
 type="unsigned" default="0" min="0" max="4294967039"/>
```

```
 <param name="ConfigGenerationNumber" comment="Configuration generation number"
 type="unsigned" default="0" min="0" max="4294967039"/>
 </section>
 <section name="MYSQLD" primarykeys="NodeId">
 <param name="wan" comment="Use WAN TCP setting as default" type="bool"
 default="false"/>
 <param name="HostName" comment="Name of computer for this node"
 type="string" default=""/>
 <param name="Id" comment="NodeId" type="unsigned" mandatory="true"
 min="1" max="255" deprecated="true"/>
 <param name="NodeId" comment="Number identifying application node (mysqld(API))"
 type="unsigned" mandatory="true" min="1" max="255"/>
 <param name="ExecuteOnComputer" comment="HostName" type="string"
 deprecated="true"/>
 …
 </section>
 …
</configvariables>
```

![](_page_178_Picture_2.jpeg)

#### **Note**

Normally, the XML output produced by [ndb\\_config](#page-169-0) --configinfo --xml is formatted using one line per element; we have added extra whitespace in the previous example, as well as the next one, for reasons of legibility. This should not make any difference to applications using this output, since most XML processors either ignore nonessential whitespace as a matter of course, or can be instructed to do so.

The XML output also indicates when changing a given parameter requires that data nodes be restarted using the [--initial](#page-137-0) option. This is shown by the presence of an initial="true" attribute in the corresponding <param> element. In addition, the restart type (system or node) is also shown; if a given parameter requires a system restart, this is indicated by the presence of a restart="system" attribute in the corresponding <param> element. For example, changing the value set for the Diskless parameter requires a system initial restart, as shown here (with the restart and initial attributes highlighted for visibility):

```
<param name="Diskless" comment="Run wo/ disk" type="bool" default="false"
 restart="system" initial="true"/>
```

Currently, no initial attribute is included in the XML output for <param> elements corresponding to parameters which do not require initial restarts; in other words, initial="false" is the default, and the value false should be assumed if the attribute is not present. Similarly, the default restart type is node (that is, an online or "rolling" restart of the cluster), but the restart attribute is included only if the restart type is system (meaning that all cluster nodes must be shut down at the same time, then restarted).

Deprecated parameters are indicated in the XML output by the deprecated attribute, as shown here:

```
<param name="NoOfDiskPagesToDiskAfterRestartACC" comment="DiskCheckpointSpeed"
 type="unsigned" default="20" min="1" max="4294967039" deprecated="true"/>
```

In such cases, the comment refers to one or more parameters that supersede the deprecated parameter. Similarly to initial, the deprecated attribute is indicated only when the parameter is deprecated, with deprecated="true", and does not appear at all for parameters which are not deprecated. (Bug #21127135)

Parameters that are required are indicated with mandatory="true", as shown here:

```
<param name="NodeId"
 comment="Number identifying application node (mysqld(API))"
```

```
 type="unsigned" mandatory="true" min="1" max="255"/>
```

In much the same way that the initial or deprecated attribute is displayed only for a parameter that requires an initial restart or that is deprecated, the mandatory attribute is included only if the given parameter is actually required.

![](_page_179_Picture_3.jpeg)

#### **Important**

The --xml option can be used only with the --configinfo option. Using --xml without --configinfo fails with an error.

Unlike the options used with this program to obtain current configuration data, --configinfo and --xml use information obtained from the NDB Cluster sources when [ndb\\_config](#page-169-0) was compiled. For this reason, no connection to a running NDB Cluster or access to a config.ini or my.cnf file is required for these two options.

Combining other [ndb\\_config](#page-169-0) options (such as [--query](#page-176-2) or [--type](#page-177-2)) with --configinfo (with or without the --xml option is not supported. Currently, if you attempt to do so, the usual result is that all other options besides --configinfo or --xml are simply ignored. However, this behavior is not guaranteed and is subject to change at any time. In addition, since [ndb\\_config](#page-169-0), when used with the --configinfo option, does not access the NDB Cluster or read any files, trying to specify additional options such as --ndb-connectstring or --config-file with --configinfo serves no purpose.

## **Examples**

1. To obtain the node ID and type of each node in the cluster:

```
$> ./ndb_config --query=nodeid,type --fields=':' --rows='\n'
1:ndbd
2:ndbd
3:ndbd
4:ndbd
5:ndb_mgmd
6:mysqld
7:mysqld
8:mysqld
9:mysqld
```

In this example, we used the [--fields](#page-173-3) options to separate the ID and type of each node with a colon character (:), and the [--rows](#page-176-4) options to place the values for each node on a new line in the output.

2. To produce a connection string that can be used by data, SQL, and API nodes to connect to the management server:

```
$> ./ndb_config --config-file=usr/local/mysql/cluster-data/config.ini \
--query=hostname,portnumber --fields=: --rows=, --type=ndb_mgmd
198.51.100.179:1186
```

3. This invocation of [ndb\\_config](#page-169-0) checks only data nodes (using the [--type](#page-177-2) option), and shows the values for each node's ID and host name, as well as the values set for its DataMemory and DataDir parameters:

```
$> ./ndb_config --type=ndbd --query=nodeid,host,datamemory,datadir -f ' : ' -r '\n'
1 : 198.51.100.193 : 83886080 : /usr/local/mysql/cluster-data
2 : 198.51.100.112 : 83886080 : /usr/local/mysql/cluster-data
3 : 198.51.100.176 : 83886080 : /usr/local/mysql/cluster-data
4 : 198.51.100.119 : 83886080 : /usr/local/mysql/cluster-data
```

In this example, we used the short options -f and -r for setting the field delimiter and row separator, respectively, as well as the short option -q to pass a list of parameters to be obtained.

4. To exclude results from any host except one in particular, use the [--host](#page-173-5) option:

```
$> ./ndb_config --host=198.51.100.176 -f : -r '\n' -q id,type
3:ndbd
5:ndb_mgmd
```

In this example, we also used the short form -q to determine the attributes to be queried.

Similarly, you can limit results to a node with a specific ID using the [--nodeid](#page-175-5) option.

## <span id="page-180-0"></span>**25.5.8 ndb\_delete\_all — Delete All Rows from an NDB Table**

[ndb\\_delete\\_all](#page-180-0) deletes all rows from the given NDB table. In some cases, this can be much faster than DELETE or even TRUNCATE TABLE.

## **Usage**

```
ndb_delete_all -c connection_string tbl_name -d db_name
```

This deletes all rows from the table named tbl\_name in the database named db\_name. It is exactly equivalent to executing TRUNCATE db\_name.tbl\_name in MySQL.

Options that can be used with [ndb\\_delete\\_all](#page-180-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-180-1"></span>• [--character-sets-dir](#page-180-1)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-180-2"></span>• [--connect-retries](#page-180-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-180-3"></span>• [--connect-retry-delay](#page-180-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-180-4"></span>• [--connect-string](#page-180-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

#### Same as [--ndb-connectstring](#page-182-0).

<span id="page-181-0"></span>• [--core-file](#page-181-0)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-181-1"></span>• [--database](#page-181-1), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database containing the table to delete from.

<span id="page-181-2"></span>• [--defaults-extra-file](#page-181-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-181-3"></span>• [--defaults-file](#page-181-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-181-4"></span>• [--defaults-group-suffix](#page-181-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-181-5"></span>• [--diskscan](#page-181-5)

| Command-Line Format | diskscan |
|---------------------|----------|

Run a disk scan.

<span id="page-181-6"></span>• [--help](#page-181-6)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-181-7"></span>• [--login-path](#page-181-7)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read given path from login file.

<span id="page-182-1"></span>• [--no-login-paths](#page-182-1)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-182-0"></span>• [--ndb-connectstring](#page-182-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-182-2"></span>• [--ndb-mgm-tls](#page-182-2)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-182-3"></span>• [--ndb-mgmd-host](#page-182-3)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-182-0).

<span id="page-182-4"></span>• [--ndb-nodeid](#page-182-4)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-182-0).

<span id="page-182-5"></span>• [--ndb-optimized-node-selection](#page-182-5)

| Command-Line Format | ndb-optimized-node-selection | 4153 |
|---------------------|------------------------------|------|
|                     |                              |      |

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-183-0"></span>• [--ndb-tls-search-path](#page-183-0)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-183-1"></span>• [--no-defaults](#page-183-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-183-2"></span>• [--print-defaults](#page-183-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-183-3"></span>• [--transactional](#page-183-3), -t

Use of this option causes the delete operation to be performed as a single transaction.

![](_page_183_Picture_14.jpeg)

#### **Warning**

With very large tables, using this option may cause the number of operations available to the cluster to be exceeded.

<span id="page-183-4"></span>• [--tupscan](#page-183-4)

Run a tuple scan.

<span id="page-183-5"></span>• [--usage](#page-183-5)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-181-6).

<span id="page-183-6"></span>• [--version](#page-183-6)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-183-7"></span>**25.5.9 ndb\_desc — Describe NDB Tables**

[ndb\\_desc](#page-183-7) provides a detailed description of one or more NDB tables.

## **Usage**

```
ndb_desc -c connection_string tbl_name -d db_name [options]
ndb_desc -c connection_string index_name -d db_name -t tbl_name
```

Additional options that can be used with [ndb\\_desc](#page-183-7) are listed later in this section.

## **Sample Output**

MySQL table creation and population statements:

```
USE test;
CREATE TABLE fish (
 id INT NOT NULL AUTO_INCREMENT,
 name VARCHAR(20) NOT NULL,
 length_mm INT NOT NULL,
 weight_gm INT NOT NULL,
 PRIMARY KEY pk (id),
 UNIQUE KEY uk (name)
) ENGINE=NDB;
INSERT INTO fish VALUES
 (NULL, 'guppy', 35, 2), (NULL, 'tuna', 2500, 150000),
 (NULL, 'shark', 3000, 110000), (NULL, 'manta ray', 1500, 50000),
 (NULL, 'grouper', 900, 125000), (NULL ,'puffer', 250, 2500);
```

#### Output from [ndb\\_desc](#page-183-7):

```
$> ./ndb_desc -c localhost fish -d test -p
-- fish --
Version: 2
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 4
Number of primary keys: 1
Length of frm data: 337
Max Rows: 0
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
PartitionCount: 2
FragmentCount: 2
PartitionBalance: FOR_RP_BY_LDM
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options:
HashMap: DEFAULT-HASHMAP-3840-2
-- Attributes --
id Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
name Varchar(20;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY DYNAMIC
length_mm Int NOT NULL AT=FIXED ST=MEMORY DYNAMIC
weight_gm Int NOT NULL AT=FIXED ST=MEMORY DYNAMIC
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
uk(name) - OrderedIndex
uk$unique(name) - UniqueHashIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory Extent_space Free extent_space
0 2 2 32768 32768 0 0
```

```
1 4 4 32768 32768 0 0
```

Information about multiple tables can be obtained in a single invocation of [ndb\\_desc](#page-183-7) by using their names, separated by spaces. All of the tables must be in the same database.

You can obtain additional information about a specific index using the --table (short form: -t) option and supplying the name of the index as the first argument to [ndb\\_desc](#page-183-7), as shown here:

```
$> ./ndb_desc uk -d test -t fish
-- uk --
Version: 2
Base table: fish
Number of attributes: 1
Logging: 0
Index type: OrderedIndex
Index status: Retrieved
-- Attributes --
name Varchar(20;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
-- IndexTable 10/uk --
Version: 2
Fragment type: FragUndefined
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: yes
Number of attributes: 2
Number of primary keys: 1
Length of frm data: 0
Max Rows: 0
Row Checksum: 1
Row GCI: 1
SingleUserMode: 2
ForceVarPart: 0
PartitionCount: 2
FragmentCount: 2
FragmentCountType: ONE_PER_LDM_PER_NODE
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options:
-- Attributes --
name Varchar(20;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
NDB$TNODE Unsigned [64] PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY
-- Indexes --
PRIMARY KEY(NDB$TNODE) - UniqueHashIndex
```

When an index is specified in this way, the [--extra-partition-info](#page-190-0) and [--extra-node-info](#page-190-1) options have no effect.

The Version column in the output contains the table's schema object version. For information about interpreting this value, see [NDB Schema Object Versions](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-schema-object-versions.md).

Three of the table properties that can be set using NDB\_TABLE comments embedded in CREATE TABLE and ALTER TABLE statements are also visible in [ndb\\_desc](#page-183-7) output. The table's FRAGMENT\_COUNT\_TYPE is always shown in the FragmentCountType column. READ\_ONLY and FULLY\_REPLICATED, if set to 1, are shown in the Table options column. You can see this after executing the following ALTER TABLE statement in the mysql client:

```
mysql> ALTER TABLE fish COMMENT='NDB_TABLE=READ_ONLY=1,FULLY_REPLICATED=1';
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
+---------+------+---------------------------------------------------------------------------------------------------------+
| Level | Code | Message |
+---------+------+---------------------------------------------------------------------------------------------------------+
| Warning | 1296 | Got error 4503 'Table property is FRAGMENT_COUNT_TYPE=ONE_PER_LDM_PER_NODE but not in comment' from NDB |
+---------+------+---------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

The warning is issued because READ\_ONLY=1 requires that the table's fragment count type is (or be set to) ONE\_PER\_LDM\_PER\_NODE\_GROUP; NDB sets this automatically in such cases. You can check that the ALTER TABLE statement has the desired effect using SHOW CREATE TABLE:

```
mysql> SHOW CREATE TABLE fish\G
*************************** 1. row ***************************
 Table: fish
Create Table: CREATE TABLE `fish` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(20) NOT NULL,
 `length_mm` int(11) NOT NULL,
 `weight_gm` int(11) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `uk` (`name`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='NDB_TABLE=READ_BACKUP=1,FULLY_REPLICATED=1'
1 row in set (0.01 sec)
```

Because FRAGMENT\_COUNT\_TYPE was not set explicitly, its value is not shown in the comment text printed by SHOW CREATE TABLE. [ndb\\_desc](#page-183-7), however, displays the updated value for this attribute. The Table options column shows the binary properties just enabled. You can see this in the output shown here (emphasized text):

```
$> ./ndb_desc -c localhost fish -d test -p
-- fish --
Version: 4
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 4
Number of primary keys: 1
Length of frm data: 380
Max Rows: 0
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
PartitionCount: 1
FragmentCount: 1
FragmentCountType: ONE_PER_LDM_PER_NODE_GROUP
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options: readbackup, fullyreplicated
HashMap: DEFAULT-HASHMAP-3840-1
-- Attributes --
id Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
name Varchar(20;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY DYNAMIC
length_mm Int NOT NULL AT=FIXED ST=MEMORY DYNAMIC
weight_gm Int NOT NULL AT=FIXED ST=MEMORY DYNAMIC
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
uk(name) - OrderedIndex
uk$unique(name) - UniqueHashIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory Extent_space Free extent_space
```

For more information about these table properties, see Section 15.1.20.12, "Setting NDB Comment Options".

The Extent\_space and Free extent\_space columns are applicable only to NDB tables having columns on disk; for tables having only in-memory columns, these columns always contain the value 0.

To illustrate their use, we modify the previous example. First, we must create the necessary Disk Data objects, as shown here:

```
CREATE LOGFILE GROUP lg_1
```

```
 ADD UNDOFILE 'undo_1.log'
 INITIAL_SIZE 16M
 UNDO_BUFFER_SIZE 2M
 ENGINE NDB;
ALTER LOGFILE GROUP lg_1
 ADD UNDOFILE 'undo_2.log'
 INITIAL_SIZE 12M
 ENGINE NDB;
CREATE TABLESPACE ts_1
 ADD DATAFILE 'data_1.dat'
 USE LOGFILE GROUP lg_1
 INITIAL_SIZE 32M
 ENGINE NDB;
ALTER TABLESPACE ts_1
 ADD DATAFILE 'data_2.dat'
 INITIAL_SIZE 48M
 ENGINE NDB;
```

(For more information on the statements just shown and the objects created by them, see Section 25.6.11.1, "NDB Cluster Disk Data Objects", as well as Section 15.1.16, "CREATE LOGFILE GROUP Statement", and Section 15.1.21, "CREATE TABLESPACE Statement".)

Now we can create and populate a version of the fish table that stores 2 of its columns on disk (deleting the previous version of the table first, if it already exists):

```
DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
 id INT NOT NULL AUTO_INCREMENT,
 name VARCHAR(20) NOT NULL,
 length_mm INT NOT NULL,
 weight_gm INT NOT NULL,
 PRIMARY KEY pk (id),
 UNIQUE KEY uk (name)
) TABLESPACE ts_1 STORAGE DISK
ENGINE=NDB;
INSERT INTO fish VALUES
 (NULL, 'guppy', 35, 2), (NULL, 'tuna', 2500, 150000),
 (NULL, 'shark', 3000, 110000), (NULL, 'manta ray', 1500, 50000),
 (NULL, 'grouper', 900, 125000), (NULL ,'puffer', 250, 2500);
```

When run against this version of the table, [ndb\\_desc](#page-183-7) displays the following output:

```
$> ./ndb_desc -c localhost fish -d test -p
-- fish --
Version: 1
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 4
Number of primary keys: 1
Length of frm data: 1001
Max Rows: 0
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
PartitionCount: 2
FragmentCount: 2
PartitionBalance: FOR_RP_BY_LDM
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options: readbackup
```

```
HashMap: DEFAULT-HASHMAP-3840-2
Tablespace id: 16
Tablespace: ts_1
-- Attributes --
id Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
name Varchar(80;utf8mb4_0900_ai_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
length_mm Int NOT NULL AT=FIXED ST=DISK
weight_gm Int NOT NULL AT=FIXED ST=DISK
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
uk(name) - OrderedIndex
uk$unique(name) - UniqueHashIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory Extent_space Free extent_space
0 2 2 32768 32768 1048576 1044440
1 4 4 32768 32768 1048576 1044400
```

This means that 1048576 bytes are allocated from the tablespace for this table on each partition, of which 1044440 bytes remain free for additional storage. In other words, 1048576 - 1044440 = 4136 bytes per partition is currently being used to store the data from this table's disk-based columns. The number of bytes shown as Free extent\_space is available for storing on-disk column data from the fish table only; for this reason, it is not visible when selecting from the Information Schema FILES table.

Tablespace id and Tablespace are also displayed for Disk Data tables.

For fully replicated tables, [ndb\\_desc](#page-183-7) shows only the nodes holding primary partition fragment replicas; nodes with copy fragment replicas (only) are ignored. You can obtain such information, using the mysql client, from the table\_distribution\_status, table\_fragments, table\_info, and table\_replicas tables in the ndbinfo database.

All options that can be used with [ndb\\_desc](#page-183-7) are shown in the following table. Additional descriptions follow the table.

<span id="page-188-0"></span>• [--auto-inc](#page-188-0), -a

Show the next value for a table's AUTO\_INCREMENT column, if it has one.

<span id="page-188-1"></span>• [--blob-info](#page-188-1), -b

Include information about subordinate BLOB and TEXT columns.

Use of this option also requires the use of the [--extra-partition-info](#page-190-0) (-p) option.

<span id="page-188-2"></span>• [--character-sets-dir](#page-188-2)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|                     |                         |

Directory containing character sets.

<span id="page-188-3"></span>• [--connect-retries](#page-188-3)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-188-4"></span>• [--connect-retry-delay](#page-188-4)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-189-0"></span>• [--connect-string](#page-189-0)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-190-2).

<span id="page-189-1"></span>• [--context](#page-189-1), -x

Show additional contextual information for the table such as schema, database name, table name, and the table's internal ID.

<span id="page-189-2"></span>• [--core-file](#page-189-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-189-3"></span>• [--database=](#page-189-3)db\_name, -d

Specify the database in which the table should be found.

<span id="page-189-4"></span>• [--defaults-extra-file](#page-189-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-189-5"></span>• [--defaults-file](#page-189-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-189-6"></span>• [--defaults-group-suffix](#page-189-6)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

#### <span id="page-190-1"></span>• [--extra-node-info](#page-190-1), -n

Include information about the mappings between table partitions and the data nodes upon which they reside. This information can be useful for verifying distribution awareness mechanisms and supporting more efficient application access to the data stored in NDB Cluster.

Use of this option also requires the use of the [--extra-partition-info](#page-190-0) (-p) option.

<span id="page-190-0"></span>• [--extra-partition-info](#page-190-0), -p

Print additional information about the table's partitions.

<span id="page-190-3"></span>• [--help](#page-190-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-190-4"></span>• [--login-path](#page-190-4)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-190-5"></span>• [--no-login-paths](#page-190-5)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-190-2"></span>• [--ndb-connectstring](#page-190-2)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-190-6"></span>• [--ndb-mgm-tls](#page-190-6)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-190-7"></span>• [--ndb-mgmd-host](#page-190-7)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
|---------------------|---------------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Same as [--ndb-connectstring](#page-190-2).

<span id="page-191-0"></span>• [--ndb-nodeid](#page-191-0)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-190-2).

<span id="page-191-1"></span>• [--ndb-optimized-node-selection](#page-191-1)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-191-2"></span>• [--ndb-tls-search-path](#page-191-2)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-191-3"></span>• [--no-defaults](#page-191-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|                     |             |

Do not read default options from any option file other than login file.

<span id="page-191-4"></span>• [--print-defaults](#page-191-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-191-5"></span>• [--retries=](#page-191-5)#, -r

Try to connect this many times before giving up. One connect attempt is made per second.

<span id="page-191-6"></span>• [--table=](#page-191-6)tbl\_name, -t

Specify the table in which to look for an index.

<span id="page-192-0"></span>• [--unqualified](#page-192-0), -u

Use unqualified table names.

<span id="page-192-1"></span>• [--usage](#page-192-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-190-3).

<span id="page-192-2"></span>• [--version](#page-192-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

Table indexes listed in the output are ordered by ID.

## <span id="page-192-3"></span>**25.5.10 ndb\_drop\_index — Drop Index from an NDB Table**

[ndb\\_drop\\_index](#page-192-3) drops the specified index from an NDB table. It is recommended that you use this utility only as an example for writing NDB API applications—see the Warning later in this section for details.

## **Usage**

```
ndb_drop_index -c connection_string table_name index -d db_name
```

The statement shown above drops the index named index from the table in the database.

Options that can be used with [ndb\\_drop\\_index](#page-192-3) are shown in the following table. Additional descriptions follow the table.

<span id="page-192-4"></span>• [--character-sets-dir](#page-192-4)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-192-5"></span>• [--connect-retries](#page-192-5)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-192-6"></span>• [--connect-retry-delay](#page-192-6)

| Command-Line Format | connect-retry-delay=# | 4163 |
|---------------------|-----------------------|------|
| Type                | Integer               |      |

| Default Value | 5 |
|---------------|---|
| Minimum Value | 0 |
| Maximum Value | 5 |

Number of seconds to wait between attempts to contact management server.

<span id="page-193-0"></span>• [--connect-string](#page-193-0)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-194-0).

<span id="page-193-1"></span>• [--core-file](#page-193-1)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-193-2"></span>• [--database](#page-193-2), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

<span id="page-193-3"></span>• [--defaults-extra-file](#page-193-3)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-193-4"></span>• [--defaults-file](#page-193-4)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-193-5"></span>• [--defaults-group-suffix](#page-193-5)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-193-6"></span>• [--help](#page-193-6)

| Command-Line Format | help |
|---------------------|------|

#### Display help text and exit.

<span id="page-194-1"></span>• [--login-path](#page-194-1)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

#### Read given path from login file.

<span id="page-194-2"></span>• [--no-login-paths](#page-194-2)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-194-0"></span>• [--ndb-connectstring](#page-194-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-194-3"></span>• [--ndb-mgm-tls](#page-194-3)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-194-4"></span>• [--ndb-mgmd-host](#page-194-4)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-194-0).

<span id="page-194-5"></span>• [--ndb-nodeid](#page-194-5)

| Command-Line Format | ndb-nodeid=#   |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | [none]<br>4165 |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-194-0).

<span id="page-195-0"></span>• [--ndb-optimized-node-selection](#page-195-0)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-195-1"></span>• [--ndb-tls-search-path](#page-195-1)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-195-2"></span>• [--no-defaults](#page-195-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-195-3"></span>• [--print-defaults](#page-195-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-195-4"></span>• [--usage](#page-195-4)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-193-6).

<span id="page-195-5"></span>• [--version](#page-195-5)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

![](_page_195_Picture_21.jpeg)

#### **Warning**

Operations performed on Cluster table indexes using the NDB API are not visible to MySQL and make the table unusable by a MySQL server. If you use this program to drop an index, then try to access the table from an SQL node, an error results, as shown here:

```
$> ./ndb_drop_index -c localhost dogs ix -d ctest1
Dropping index dogs/idx...OK
$> ./mysql -u jon -p ctest1
Enter password: *******
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 7 to server version: 5.7.44-ndb-7.5.36
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> SHOW TABLES;
+------------------+
| Tables_in_ctest1 |
+------------------+
| a |
| bt1 |
| bt2 |
| dogs |
| employees |
| fish |
+------------------+
6 rows in set (0.00 sec)
mysql> SELECT * FROM dogs;
ERROR 1296 (HY000): Got error 4243 'Index not found' from NDBCLUSTER
```

In such a case, your only option for making the table available to MySQL again is to drop the table and re-create it. You can use either the SQL statementDROP TABLE or the [ndb\\_drop\\_table](#page-196-0) utility (see [Section 25.5.11, "ndb\\_drop\\_table — Drop an NDB Table"](#page-196-0)) to drop the table.

## <span id="page-196-0"></span>**25.5.11 ndb\_drop\_table — Drop an NDB Table**

[ndb\\_drop\\_table](#page-196-0) drops the specified NDB table. (If you try to use this on a table created with a storage engine other than NDB, the attempt fails with the error 723: No such table exists.) This operation is extremely fast; in some cases, it can be an order of magnitude faster than using a MySQL DROP TABLE statement on an NDB table.

## **Usage**

```
ndb_drop_table -c connection_string tbl_name -d db_name
```

Options that can be used with [ndb\\_drop\\_table](#page-196-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-196-1"></span>• [--character-sets-dir](#page-196-1)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-196-2"></span>• [--connect-retries](#page-196-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

#### <span id="page-197-0"></span>• [--connect-retry-delay](#page-197-0)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-197-1"></span>• [--connect-string](#page-197-1)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-198-0).

<span id="page-197-2"></span>• [--core-file](#page-197-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-197-3"></span>• [--database](#page-197-3), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

<span id="page-197-4"></span>• [--defaults-extra-file](#page-197-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-197-5"></span>• [--defaults-file](#page-197-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

• [--defaults-group-suffix](#page-197-6)

<span id="page-197-6"></span>

| 4168 |  |
|------|--|

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Also read groups with concat(group, suffix).

<span id="page-198-1"></span>• [--help](#page-198-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-198-2"></span>• [--login-path](#page-198-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-198-3"></span>• [--no-login-paths](#page-198-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-198-0"></span>• [--ndb-connectstring](#page-198-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to [ndb\\_mgmd](#page-149-0). Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-198-4"></span>• [--ndb-mgm-tls](#page-198-4)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-198-5"></span>• [--ndb-mgmd-host](#page-198-5)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-198-0).

<span id="page-198-6"></span>• [--ndb-nodeid](#page-198-6)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-198-0).

<span id="page-199-0"></span>• [--ndb-optimized-node-selection](#page-199-0)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-199-1"></span>• [--ndb-tls-search-path](#page-199-1)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-199-2"></span>• [--no-defaults](#page-199-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-199-3"></span>• [--print-defaults](#page-199-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-199-4"></span>• [--usage](#page-199-4)

| Command-Line Format | usage |
|---------------------|-------|

Display help text and exit; same as [--help](#page-198-1).

<span id="page-199-5"></span>• [--version](#page-199-5)

| Command-Line Format |         |
|---------------------|---------|
|                     | version |

Display version information and exit.

# <span id="page-0-0"></span>**25.5.12 ndb\_error\_reporter — NDB Error-Reporting Utility**

[ndb\\_error\\_reporter](#page-0-0) creates an archive from data node and management node log files that can be used to help diagnose bugs or other problems with a cluster. It is highly recommended that you make use of this utility when filing reports of bugs in NDB Cluster.

Options that can be used with [ndb\\_error\\_reporter](#page-0-0) are shown in the following table. Additional descriptions follow the table.

### **Usage**

ndb\_error\_reporter path/to/config-file [username] [options]

This utility is intended for use on a management node host, and requires the path to the management host configuration file (usually named config.ini). Optionally, you can supply the name of a user that is able to access the cluster's data nodes using SSH, to copy the data node log files. [ndb\\_error\\_reporter](#page-0-0) then includes all of these files in archive that is created in the same directory in which it is run. The archive is named ndb\_error\_report\_YYYYMMDDhhmmss.tar.bz2, where YYYYMMDDhhmmss is a datetime string.

[ndb\\_error\\_reporter](#page-0-0) also accepts the options listed here:

<span id="page-0-1"></span>• [--connection-timeout=](#page-0-1)timeout

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Wait this many seconds when trying to connect to nodes before timing out.

<span id="page-0-2"></span>• [--dry-scp](#page-0-2)

| Command-Line Format | dry-scp |
|---------------------|---------|

Run [ndb\\_error\\_reporter](#page-0-0) without using scp from remote hosts. Used for testing only.

<span id="page-0-3"></span>• [--help](#page-0-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-0-4"></span>• [--fs](#page-0-4)

| Command-Line Format | fs |
|---------------------|----|

Copy the data node file systems to the management host and include them in the archive.

Because data node file systems can be extremely large, even after being compressed, we ask that you please do not send archives created using this option to Oracle unless you are specifically requested to do so.

<span id="page-0-5"></span>• [--skip-nodegroup=](#page-0-5)nodegroup\_id

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Skip all nodes belong to the node group having the supplied node group ID.

# <span id="page-1-0"></span>**25.5.13 ndb\_import — Import CSV Data Into NDB**

[ndb\\_import](#page-1-0) imports CSV-formatted data, such as that produced by mysqldump --tab, directly into NDB using the NDB API. [ndb\\_import](#page-1-0) requires a connection to an NDB management server (ndb\_mgmd) to function; it does not require a connection to a MySQL Server.

## **Usage**

```
ndb_import db_name file_name options
```

[ndb\\_import](#page-1-0) requires two arguments. db\_name is the name of the database where the table into which to import the data is found; file\_name is the name of the CSV file from which to read the data; this must include the path to this file if it is not in the current directory. The name of the file must match that of the table; the file's extension, if any, is not taken into consideration. Options supported by [ndb\\_import](#page-1-0) include those for specifying field separators, escapes, and line terminators, and are described later in this section.

[ndb\\_import](#page-1-0) rejects any empty lines which it reads from the CSV file, except when importing a single column, in which case an empty value can be used as the column value. [ndb\\_import](#page-1-0) handles this in the same manner as a LOAD DATA statement does.

[ndb\\_import](#page-1-0) must be able to connect to an NDB Cluster management server; for this reason, there must be an unused [api] slot in the cluster config.ini file.

To duplicate an existing table that uses a different storage engine, such as InnoDB, as an NDB table, use the mysql client to perform a SELECT INTO OUTFILE statement to export the existing table to a CSV file, then to execute a CREATE TABLE LIKE statement to create a new table having the same structure as the existing table, then perform ALTER TABLE ... ENGINE=NDB on the new table; after this, from the system shell, invoke [ndb\\_import](#page-1-0) to load the data into the new NDB table. For example, an existing InnoDB table named myinnodb\_table in a database named myinnodb can be exported into an NDB table named myndb\_table in a database named myndb as shown here, assuming that you are already logged in as a MySQL user with the appropriate privileges:

1. In the mysql client:

```
mysql> USE myinnodb;
mysql> SELECT * INTO OUTFILE '/tmp/myndb_table.csv'
 > FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
 > LINES TERMINATED BY '\n'
 > FROM myinnodbtable;
mysql> CREATE DATABASE myndb;
mysql> USE myndb;
mysql> CREATE TABLE myndb_table LIKE myinnodb.myinnodb_table;
mysql> ALTER TABLE myndb_table ENGINE=NDB;
mysql> EXIT;
Bye
$>
```

Once the target database and table have been created, a running mysqld is no longer required. You can stop it using mysqladmin shutdown or another method before proceeding, if you wish.

2. In the system shell:

```
# if you are not already in the MySQL bin directory:
$> cd path-to-mysql-bin-dir
```

```
$> ndb_import myndb /tmp/myndb_table.csv --fields-optionally-enclosed-by='"' \
 --fields-terminated-by="," --fields-escaped-by='\\'
```

The output should resemble what is shown here:

```
job-1 import myndb.myndb_table from /tmp/myndb_table.csv
job-1 [running] import myndb.myndb_table from /tmp/myndb_table.csv
job-1 [success] import myndb.myndb_table from /tmp/myndb_table.csv
job-1 imported 19984 rows in 0h0m9s at 2277 rows/s
jobs summary: defined: 1 run: 1 with success: 1 with failure: 0
$>
```

All options that can be used with [ndb\\_import](#page-1-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-2-0"></span>• [--abort-on-error](#page-2-0)

| Command-Line Format | abort-on-error |
|---------------------|----------------|
|                     |                |

Dump core on any fatal error; used for debugging only.

<span id="page-2-1"></span>• [--ai-increment](#page-2-1)=#

| Command-Line Format | ai-increment=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 1              |
| Minimum Value       | 1              |
| Maximum Value       | 4294967295     |

For a table with a hidden primary key, specify the autoincrement increment, like the auto\_increment\_increment system variable does in the MySQL Server.

<span id="page-2-2"></span>• [--ai-offset](#page-2-2)=#

| Command-Line Format | ai-offset=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 1           |
| Minimum Value       | 1           |
| Maximum Value       | 4294967295  |

For a table with hidden primary key, specify the autoincrement offset. Similar to the auto\_increment\_offset system variable.

<span id="page-2-3"></span>• [--ai-prefetch-sz](#page-2-3)=#

| Command-Line Format | ai-prefetch-sz=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 1024             |
| Minimum Value       | 1                |
| Maximum Value       | 4294967295       |

For a table with a hidden primary key, specify the number of autoincrement values that are prefetched. Behaves like the ndb\_autoincrement\_prefetch\_sz system variable does in the MySQL Server.

<span id="page-2-4"></span>• [--character-sets-dir](#page-2-4)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

#### Directory containing character sets.

#### <span id="page-3-0"></span>• [--connections](#page-3-0)=#

| Command-Line Format | connections=# |
|---------------------|---------------|
| Type                | Integer       |
| Default Value       | 1             |
| Minimum Value       | 1             |
| Maximum Value       | 4294967295    |

#### Number of cluster connections to create.

#### <span id="page-3-1"></span>• [--connect-retries](#page-3-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

#### Number of times to retry connection before giving up.

#### <span id="page-3-2"></span>• [--connect-retry-delay](#page-3-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-3-3"></span>• [--connect-string](#page-3-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

### Same as [--ndb-connectstring](#page-8-0).

#### <span id="page-3-4"></span>• [--continue](#page-3-4)

| Command-Line Format | continue |
|---------------------|----------|
|---------------------|----------|

When a job fails, continue to the next job.

### <span id="page-3-5"></span>• [--core-file](#page-3-5)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-4-0"></span>• [--csvopt](#page-4-0)=string

| Command-Line Format | csvopt=opts |
|---------------------|-------------|
| Type                | String      |
| Default Value       | [none]      |

Provides a shortcut method for setting typical CSV import options. The argument to this option is a string consisting of one or more of the following parameters:

- c: Fields terminated by comma
- d: Use defaults, except where overridden by another parameter
- n: Lines terminated by \n
- q: Fields optionally enclosed by double quote characters (")
- r: Line terminated by \r

The order of parameters used in the argument to this option is handled such that the rightmost parameter always takes precedence over any potentially conflicting parameters which have already been used in the same argument value. This also applies to any duplicate instances of a given parameter.

This option is intended for use in testing under conditions in which it is difficult to transmit escapes or quotation marks.

<span id="page-4-1"></span>• [--db-workers](#page-4-1)=#

| Command-Line Format | db-workers=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 4            |
| Minimum Value       | 1            |
| Maximum Value       | 4294967295   |

Number of threads, per data node, executing database operations.

<span id="page-4-2"></span>• [--defaults-file](#page-4-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-4-3"></span>• [--defaults-extra-file](#page-4-3)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-4-4"></span>• [--defaults-group-suffix](#page-4-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
|---------------------|------------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Also read groups with concat(group, suffix).

<span id="page-5-0"></span>• [--errins-type](#page-5-0)=name

| Command-Line Format | errins-type=name |
|---------------------|------------------|
| Type                | Enumeration      |
| Default Value       | [none]           |
| Valid Values        | stopjob          |
|                     | stopall          |
|                     | sighup           |
|                     | sigint           |
|                     | list             |

Error insert type; use list as the name value to obtain all possible values. This option is used for testing purposes only.

<span id="page-5-1"></span>• [--errins-delay](#page-5-1)=#

| Command-Line Format | errins-delay=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 1000           |
| Minimum Value       | 0              |
| Maximum Value       | 4294967295     |
| Unit                | ms             |

Error insert delay in milliseconds; random variation is added. This option is used for testing purposes only.

<span id="page-5-2"></span>• [--fields-enclosed-by](#page-5-2)=char

| Command-Line Format | fields-enclosed-by=char |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

This works in the same way as the FIELDS ENCLOSED BY option does for the LOAD DATA statement, specifying a character to be interpreted as quoting field values. For CSV input, this is the same as [--fields-optionally-enclosed-by](#page-5-3).

<span id="page-5-4"></span>• [--fields-escaped-by](#page-5-4)=name

| Command-Line Format | fields-escaped-by=char |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       | \                      |

Specify an escape character in the same way as the FIELDS ESCAPED BY option does for the SQL LOAD DATA statement.

<span id="page-5-3"></span>• [--fields-optionally-enclosed-by](#page-5-3)=char

| Command-Line Format | fields-optionally-enclosed-by=char |
|---------------------|------------------------------------|
| Type                | String                             |
| Default Value       | [none]                             |

This works in the same way as the FIELDS OPTIONALLY ENCLOSED BY option does for the LOAD DATA statement, specifying a character to be interpreted as optionally quoting field values. For CSV input, this is the same as [--fields-enclosed-by](#page-5-2).

<span id="page-6-0"></span>• [--fields-terminated-by](#page-6-0)=char

| Command-Line Format | fields-terminated-by=char |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | \t                        |

This works in the same way as the FIELDS TERMINATED BY option does for the LOAD DATA statement, specifying a character to be interpreted as the field separator.

<span id="page-6-1"></span>• [--help](#page-6-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-6-2"></span>• [--idlesleep](#page-6-2)=#

| Command-Line Format | idlesleep=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 1           |
| Minimum Value       | 1           |
| Maximum Value       | 4294967295  |
| Unit                | ms          |

Number of milliseconds to sleep waiting for more work to perform.

<span id="page-6-3"></span>• [--idlespin](#page-6-3)=#

| Command-Line Format | idlespin=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |

Number of times to retry before sleeping.

<span id="page-6-4"></span>• [--ignore-lines](#page-6-4)=#

| Command-Line Format | ignore-lines=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 0              |
| Minimum Value       | 0<br>4177      |

| Maximum Value | 4294967295 |
|---------------|------------|
|---------------|------------|

Cause ndb\_import to ignore the first # lines of the input file. This can be employed to skip a file header that does not contain any data.

<span id="page-7-0"></span>• [--input-type](#page-7-0)=name

| Command-Line Format | input-type=name |
|---------------------|-----------------|
| Type                | Enumeration     |
| Default Value       | csv             |
| Valid Values        | random          |
|                     | csv             |

Set the type of input type. The default is csv; random is intended for testing purposes only. .

<span id="page-7-1"></span>• [--input-workers](#page-7-1)=#

| Command-Line Format | input-workers=# |
|---------------------|-----------------|
| Type                | Integer         |
| Default Value       | 4               |
| Minimum Value       | 1               |
| Maximum Value       | 4294967295      |

Set the number of threads processing input.

<span id="page-7-2"></span>• [--keep-state](#page-7-2)

| Command-Line Format | keep-state |
|---------------------|------------|
|---------------------|------------|

By default, ndb\_import removes all state files (except non-empty \*.rej files) when it completes a job. Specify this option (nor argument is required) to force the program to retain all state files instead.

<span id="page-7-3"></span>• [--lines-terminated-by](#page-7-3)=name

| Command-Line Format | lines-terminated-by=char |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | \n                       |

This works in the same way as the LINES TERMINATED BY option does for the LOAD DATA statement, specifying a character to be interpreted as end-of-line.

<span id="page-7-4"></span>• [--log-level](#page-7-4)=#

4178

| Command-Line Format | log-level=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 0           |
| Minimum Value       | 0           |
| Maximum Value       | 2           |

Performs internal logging at the given level. This option is intended primarily for internal and development use.

In debug builds of NDB only, the logging level can be set using this option to a maximum of 4.

### <span id="page-8-1"></span>• [--login-path](#page-8-1)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-8-2"></span>• [--no-login-paths](#page-8-2)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-8-3"></span>• [--max-rows](#page-8-3)=#

| Command-Line Format | max-rows=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Import only this number of input data rows; the default is 0, which imports all rows.

<span id="page-8-4"></span>• [--missing-ai-column](#page-8-4)

| Command-Line Format | missing-ai-column='name' |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

This option can be employed when importing a single table, or multiple tables. When used, it indicates that the CSV file being imported does not contain any values for an AUTO\_INCREMENT column, and that [ndb\\_import](#page-1-0) should supply them; if the option is used and the AUTO\_INCREMENT column contains any values, the import operation cannot proceed.

<span id="page-8-5"></span>• [--monitor](#page-8-5)=#

| Command-Line Format | monitor=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 2          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Periodically print the status of a running job if something has changed (status, rejected rows, temporary errors). Set to 0 to disable this reporting. Setting to 1 prints any change that is seen. Higher values reduce the frequency of this status reporting.

<span id="page-8-0"></span>• [--ndb-connectstring](#page-8-0)

| Command-Line Format | ndb                             |  |
|---------------------|---------------------------------|--|
|                     | connectstring=connection_string |  |

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-9-0"></span>• [--ndb-mgm-tls](#page-9-0)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-9-1"></span>• [--ndb-mgmd-host](#page-9-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-8-0).

<span id="page-9-2"></span>• [--ndb-nodeid](#page-9-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-8-0).

<span id="page-9-3"></span>• [--ndb-optimized-node-selection](#page-9-3)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|                     |                              |

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-9-4"></span>• [--ndb-tls-search-path](#page-9-4)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-10-0"></span>• [--no-asynch](#page-10-0)

| Command-Line Format | no-asynch |
|---------------------|-----------|
|---------------------|-----------|

Run database operations as batches, in single transactions.

#### <span id="page-10-1"></span>• [--no-defaults](#page-10-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

#### <span id="page-10-2"></span>• [--no-hint](#page-10-2)

| Command-Line Format | no-hint |
|---------------------|---------|
|---------------------|---------|

Do not use distribution key hinting to select a data node.

#### <span id="page-10-3"></span>• [--opbatch](#page-10-3)=#

| Command-Line Format | opbatch=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 256        |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of operations (including blob operations), and thus the number of asynchronous transactions, per execution batch.

### <span id="page-10-4"></span>• [--opbytes](#page-10-4)=#

| Command-Line Format | opbytes=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of bytes per execution batch. Use 0 for no limit.

#### <span id="page-10-5"></span>• [--output-type](#page-10-5)=name

| Command-Line Format | output-type=name |
|---------------------|------------------|

| Type          | Enumeration |
|---------------|-------------|
| Default Value | ndb         |
| Valid Values  | null        |

Set the output type. ndb is the default. null is used only for testing.

<span id="page-11-0"></span>• [--output-workers](#page-11-0)=#

| Command-Line Format | output-workers=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 2                |
| Minimum Value       | 1                |
| Maximum Value       | 4294967295       |

Set the number of threads processing output or relaying database operations.

<span id="page-11-1"></span>• [--pagesize](#page-11-1)=#

| Command-Line Format | pagesize=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 4096       |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Align I/O buffers to the given size.

<span id="page-11-2"></span>• [--pagecnt](#page-11-2)=#

| Command-Line Format | pagecnt=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 64         |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |

Set the size of I/O buffers as multiple of page size. The CSV input worker allocates buffer that is doubled in size.

<span id="page-11-3"></span>• [--polltimeout](#page-11-3)=#

| Command-Line Format | polltimeout=# |
|---------------------|---------------|
| Type                | Integer       |
| Default Value       | 1000          |
| Minimum Value       | 1             |
| Maximum Value       | 4294967295    |
| Unit                | ms            |

Set a timeout per poll for completed asynchronous transactions; polling continues until all polls are completed, or until an error occurs.

### <span id="page-12-0"></span>• [--print-defaults](#page-12-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

#### <span id="page-12-1"></span>• [--rejects](#page-12-1)=#

| Command-Line Format | rejects=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |

Limit the number of rejected rows (rows with permanent errors) in the data load. The default is 0, which means that any rejected row causes a fatal error. Any rows causing the limit to be exceeded are added to the .rej file.

The limit imposed by this option is effective for the duration of the current run. A run restarted using [--resume](#page-12-2) is considered a "new" run for this purpose.

#### <span id="page-12-2"></span>• [--resume](#page-12-2)

| Command-Line Format | resume |
|---------------------|--------|
|---------------------|--------|

If a job is aborted (due to a temporary db error or when interrupted by the user), resume with any rows not yet processed.

#### <span id="page-12-3"></span>• [--rowbatch](#page-12-3)=#

| Command-Line Format | rowbatch=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | rows       |

Set a limit on the number of rows per row queue. Use 0 for no limit.

#### <span id="page-12-4"></span>• [--rowbytes](#page-12-4)=#

| Command-Line Format | rowbytes=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 262144     |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of bytes per row queue. Use 0 for no limit.

#### <span id="page-13-0"></span>• [--stats](#page-13-0)

| Command-Line Format | stats |
|---------------------|-------|
|---------------------|-------|

Save information about options related to performance and other internal statistics in files named \*.sto and \*.stt. These files are always kept on successful completion (even if [--keep-state](#page-7-2) is not also specified).

#### <span id="page-13-1"></span>• [--state-dir](#page-13-1)=name

| Command-Line Format | state-dir=path |
|---------------------|----------------|
| Type                | String         |
| Default Value       |                |

Where to write the state files (tbl\_name.map, tbl\_name.rej, tbl\_name.res, and tbl\_name.stt) produced by a run of the program; the default is the current directory.

#### <span id="page-13-2"></span>• [--table=](#page-13-2)name

| Command-Line Format | table=name             |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       | [input file base name] |

By default, [ndb\\_import](#page-1-0) attempts to import data into a table whose name is the base name of the CSV file from which the data is being read. You can override the choice of table name by specifying it with the --table option (short form -t).

### <span id="page-13-3"></span>• [--tempdelay](#page-13-3)=#

| Command-Line Format | tempdelay=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 10          |
| Minimum Value       | 0           |
| Maximum Value       | 4294967295  |
| Unit                | ms          |

Number of milliseconds to sleep between temporary errors.

#### <span id="page-13-4"></span>• [--temperrors](#page-13-4)=#

| Command-Line Format | temperrors=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 0            |
| Minimum Value       | 0            |
| Maximum Value       | 4294967295   |

Number of times a transaction can fail due to a temporary error, per execution batch. The default is 0, which means that any temporary error is fatal. Temporary errors do not cause any rows to be added to the .rej file.

### <span id="page-13-5"></span>• [--verbose](#page-13-5), -v

| Command-Line Format | verbose[=#] |
|---------------------|-------------|
| Type                | Boolean     |

| Default Value | false |
|---------------|-------|
|---------------|-------|

Enable verbose output.

<span id="page-14-0"></span>• [--usage](#page-14-0)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-6-1).

<span id="page-14-1"></span>• [--version](#page-14-1)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

As with LOAD DATA, options for field and line formatting much match those used to create the CSV file, whether this was done using SELECT INTO ... OUTFILE, or by some other means. There is no equivalent to the LOAD DATA statement STARTING WITH option.

# <span id="page-14-2"></span>**25.5.14 ndb\_index\_stat — NDB Index Statistics Utility**

[ndb\\_index\\_stat](#page-14-2) provides per-fragment statistical information about indexes on NDB tables. This includes cache version and age, number of index entries per partition, and memory consumption by indexes.

## **Usage**

To obtain basic index statistics about a given NDB table, invoke [ndb\\_index\\_stat](#page-14-2) as shown here, with the name of the table as the first argument and the name of the database containing this table specified immediately following it, using the [--database](#page-16-0) (-d) option:

```
ndb_index_stat table -d database
```

In this example, we use [ndb\\_index\\_stat](#page-14-2) to obtain such information about an NDB table named mytable in the test database:

```
$> ndb_index_stat -d test mytable
table:City index:PRIMARY fragCount:2
sampleVersion:3 loadTime:1399585986 sampleCount:1994 keyBytes:7976
query cache: valid:1 sampleCount:1994 totalBytes:27916
times in ms: save: 7.133 sort: 1.974 sort per sample: 0.000
```

sampleVersion is the version number of the cache from which the statistics data is taken. Running [ndb\\_index\\_stat](#page-14-2) with the [--update](#page-20-0) option causes sampleVersion to be incremented.

loadTime shows when the cache was last updated. This is expressed as seconds since the Unix Epoch.

sampleCount is the number of index entries found per partition. You can estimate the total number of entries by multiplying this by the number of fragments (shown as fragCount).

sampleCount can be compared with the cardinality of SHOW INDEX or INFORMATION\_SCHEMA.STATISTICS, although the latter two provide a view of the table as a whole, while [ndb\\_index\\_stat](#page-14-2) provides a per-fragment average.

keyBytes is the number of bytes used by the index. In this example, the primary key is an integer, which requires four bytes for each index, so keyBytes can be calculated in this case as shown here:

```
 keyBytes = sampleCount * (4 bytes per index) = 1994 * 4 = 7976
```

This information can also be obtained using the corresponding column definitions from INFORMATION\_SCHEMA.COLUMNS (this requires a MySQL Server and a MySQL client application). totalBytes is the total memory consumed by all indexes on the table, in bytes.

Timings shown in the preceding examples are specific to each invocation of [ndb\\_index\\_stat](#page-14-2).

The [--verbose](#page-20-1) option provides some additional output, as shown here:

```
$> ndb_index_stat -d test mytable --verbose
random seed 1337010518
connected
loop 1 of 1
table:mytable index:PRIMARY fragCount:4
sampleVersion:2 loadTime:1336751773 sampleCount:0 keyBytes:0
read stats
query cache created
query cache: valid:1 sampleCount:0 totalBytes:0
times in ms: save: 20.766 sort: 0.001
disconnected
$>
```

If the output from the program is empty, this may indicate that no statistics yet exist. To force them to be created (or updated if they already exist), invoke [ndb\\_index\\_stat](#page-14-2) with the [--update](#page-20-0) option, or execute ANALYZE TABLE on the table in the mysql client.

### **Options**

The following table includes options that are specific to the NDB Cluster [ndb\\_index\\_stat](#page-14-2) utility. Additional descriptions are listed following the table.

<span id="page-15-0"></span>• [--character-sets-dir](#page-15-0)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-15-1"></span>• [--connect-retries](#page-15-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-15-2"></span>• [--connect-retry-delay](#page-15-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-15-3"></span>• [--connect-string](#page-15-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |

Default Value [none]

Same as [--ndb-connectstring](#page-17-0).

<span id="page-16-1"></span>• [--core-file](#page-16-1)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-16-0"></span>• [--database=](#page-16-0)name, -d name

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [none]        |
| Minimum Value       |               |
| Maximum Value       |               |

The name of the database that contains the table being queried.

<span id="page-16-2"></span>• [--defaults-extra-file](#page-16-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-16-3"></span>• [--defaults-file](#page-16-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-16-4"></span>• [--defaults-group-suffix](#page-16-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-16-5"></span>• [--delete](#page-16-5)

| Command-Line Format | delete |
|---------------------|--------|
|---------------------|--------|

Delete the index statistics for the given table, stopping any auto-update that was previously configured.

<span id="page-16-6"></span>• [--dump](#page-16-6)

| Command-Line Format | dump |
|---------------------|------|

Dump the contents of the query cache.

#### <span id="page-17-1"></span>• [--help](#page-17-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-17-2"></span>• [--login-path](#page-17-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-17-3"></span>• [--no-login-paths](#page-17-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-17-4"></span>• [--loops=](#page-17-4)#

| Command-Line Format | loops=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 0       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

Repeat commands this number of times (for use in testing).

<span id="page-17-0"></span>• [--ndb-connectstring](#page-17-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-17-5"></span>• [--ndb-mgm-tls](#page-17-5)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not 4188 required; strict means that TLS is required to connect.

### <span id="page-18-0"></span>• [--ndb-mgmd-host](#page-18-0)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-17-0).

#### <span id="page-18-1"></span>• [--ndb-nodeid](#page-18-1)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-17-0).

<span id="page-18-2"></span>• [--ndb-optimized-node-selection](#page-18-2)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-18-3"></span>• [--ndb-tls-search-path](#page-18-3)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-18-4"></span>• [--no-defaults](#page-18-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

### <span id="page-18-5"></span>• [--print-defaults](#page-18-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-18-6"></span>• [--query=](#page-18-6)#

| Command-Line Format | query=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 0       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

Perform random range queries on first key attribute (must be int unsigned).

<span id="page-19-0"></span>• [--sys-drop](#page-19-0)

| Command-Line Format | sys-drop |
|---------------------|----------|

Drop all statistics tables and events in the NDB kernel. This causes all statistics to be lost.

<span id="page-19-1"></span>• [--sys-create](#page-19-1)

| Command-Line Format | sys-create |
|---------------------|------------|
|---------------------|------------|

Create all statistics tables and events in the NDB kernel. This works only if none of them exist previously.

<span id="page-19-2"></span>• [--sys-create-if-not-exist](#page-19-2)

| Command-Line Format | sys-create-if-not-exist |
|---------------------|-------------------------|
|---------------------|-------------------------|

Create any NDB system statistics tables or events (or both) that do not already exist when the program is invoked.

<span id="page-19-3"></span>• [--sys-create-if-not-valid](#page-19-3)

| Command-Line Format | sys-create-if-not-valid |
|---------------------|-------------------------|
|---------------------|-------------------------|

Create any NDB system statistics tables or events that do not already exist, after dropping any that are invalid.

<span id="page-19-4"></span>• [--sys-check](#page-19-4)

| Command-Line Format | sys-check |
|---------------------|-----------|
|---------------------|-----------|

Verify that all required system statistics tables and events exist in the NDB kernel.

<span id="page-19-5"></span>• [--sys-skip-tables](#page-19-5)

| Command-Line Format | sys-skip-tables |
|---------------------|-----------------|
|---------------------|-----------------|

Do not apply any --sys-\* options to any statistics tables.

<span id="page-19-6"></span>• [--sys-skip-events](#page-19-6)

| Command-Line Format | sys-skip-events |
|---------------------|-----------------|
|---------------------|-----------------|

Do not apply any --sys-\* options to any events.

<span id="page-20-0"></span>• [--update](#page-20-0)

| Command-Line Format | update |
|---------------------|--------|
|---------------------|--------|

Update the index statistics for the given table, and restart any auto-update that was previously configured.

<span id="page-20-2"></span>• [--usage](#page-20-2)

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Display help text and exit; same as [--help](#page-17-1).

<span id="page-20-1"></span>• [--verbose](#page-20-1)

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Turn on verbose output.

<span id="page-20-3"></span>• [--version](#page-20-3)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-20-5"></span>**ndb\_index\_stat system options.** The following options are used to generate and update the statistics tables in the NDB kernel. None of these options can be mixed with statistics options (see [ndb\\_index\\_stat statistics options\)](#page-20-4).

- [--sys-drop](#page-19-0)
- [--sys-create](#page-19-1)
- [--sys-create-if-not-exist](#page-19-2)
- [--sys-create-if-not-valid](#page-19-3)
- [--sys-check](#page-19-4)
- [--sys-skip-tables](#page-19-5)
- [--sys-skip-events](#page-19-6)

<span id="page-20-4"></span>**ndb\_index\_stat statistics options.** The options listed here are used to generate index statistics. They work with a given table and database. They cannot be mixed with system options (see [ndb\\_index\\_stat system options](#page-20-5)).

- [--database](#page-16-0)
- [--delete](#page-16-5)
- [--update](#page-20-0)
- [--dump](#page-16-6)
- [--query](#page-18-6)

# <span id="page-20-6"></span>**25.5.15 ndb\_move\_data — NDB Data Copy Utility**

### **Usage**

The program is invoked with the names of the source and target tables; either or both of these may be qualified optionally with the database name. Both tables must use the NDB storage engine.

ndb\_move\_data options source target

Options that can be used with [ndb\\_move\\_data](#page-20-6) are shown in the following table. Additional descriptions follow the table.

<span id="page-21-0"></span>• [--abort-on-error](#page-21-0)

| Command-Line Format | abort-on-error |
|---------------------|----------------|
|---------------------|----------------|

Dump core on permanent error (debug option).

<span id="page-21-1"></span>• [--character-sets-dir](#page-21-1)=name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

Directory where character sets are.

<span id="page-21-2"></span>• [--connect-retry-delay](#page-21-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-21-3"></span>• [--connect-retries](#page-21-3)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-21-4"></span>• [--connect-string](#page-21-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-23-0).

<span id="page-21-5"></span>• [--core-file](#page-21-5)

| Command-Line Format | core-file |
|---------------------|-----------|
|                     |           |

Write core file on error; used in debugging.

<span id="page-22-0"></span>• [--database](#page-22-0)=dbname, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table is found.

<span id="page-22-1"></span>• [--defaults-extra-file](#page-22-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-22-2"></span>• [--defaults-file](#page-22-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-22-3"></span>• [--defaults-group-suffix](#page-22-3)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-22-4"></span>• [--drop-source](#page-22-4)

| Command-Line Format | drop-source |
|---------------------|-------------|
|---------------------|-------------|

Drop source table after all rows have been moved.

<span id="page-22-5"></span>• [--error-insert](#page-22-5)

| Command-Line Format | error-insert |
|---------------------|--------------|
|---------------------|--------------|

Insert random temporary errors (testing option).

<span id="page-22-6"></span>• [--exclude-missing-columns](#page-22-6)

| Command-Line Format | exclude-missing-columns |
|---------------------|-------------------------|

Ignore extra columns in source or target table.

<span id="page-23-1"></span>• [--help](#page-23-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-23-2"></span>• [--login-path](#page-23-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-23-3"></span>• [--no-login-paths](#page-23-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|                     |                |

Skips reading options from the login path file.

<span id="page-23-4"></span>• [--lossy-conversions](#page-23-4), -l

| Command-Line Format | lossy-conversions |
|---------------------|-------------------|
|---------------------|-------------------|

Allow attribute data to be truncated when converted to a smaller type.

<span id="page-23-0"></span>• [--ndb-connectstring](#page-23-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-23-5"></span>• [--ndb-mgm-tls](#page-23-5)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-23-6"></span>• [--ndb-mgmd-host](#page-23-6)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-23-0).

### <span id="page-24-0"></span>• [--ndb-nodeid](#page-24-0)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-23-0).

<span id="page-24-1"></span>• [--ndb-optimized-node-selection](#page-24-1)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-24-2"></span>• [--ndb-tls-search-path](#page-24-2)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-24-3"></span>• [--no-defaults](#page-24-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-24-4"></span>• [--print-defaults](#page-24-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-24-5"></span>• [--promote-attributes](#page-24-5), -A

| Command-Line Format | promote-attributes |
|---------------------|--------------------|
|---------------------|--------------------|

Command-Line Format --staging-tries=x[,y[,z]]

Allow attribute data to be converted to a larger type.

<span id="page-24-6"></span>• [--staging-tries](#page-24-6)=x[,y[,z]]

4195

| Type          | String       |
|---------------|--------------|
| Default Value | 0,1000,60000 |

Specify tries on temporary errors. Format is x[,y[,z]] where x=max tries (0=no limit), y=min delay (ms), z=max delay (ms).

<span id="page-25-0"></span>• [--usage](#page-25-0)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-23-1).

<span id="page-25-1"></span>• [--verbose](#page-25-1)

| Command-Line Format | verbose |
|---------------------|---------|

Enable verbose messages.

<span id="page-25-2"></span>• [--version](#page-25-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-25-3"></span>**25.5.16 ndb\_perror — Obtain NDB Error Message Information**

[ndb\\_perror](#page-25-3) shows information about an NDB error, given its error code. This includes the error message, the type of error, and whether the error is permanent or temporary. This is intended as a drop-in replacement for perror [--ndb](https://dev.mysql.com/doc/refman/8.0/en/perror.md#option_perror_ndb), which is no longer supported.

### **Usage**

```
ndb_perror [options] error_code
```

[ndb\\_perror](#page-25-3) does not need to access a running NDB Cluster, or any nodes (including SQL nodes). To view information about a given NDB error, invoke the program, using the error code as an argument, like this:

```
$> ndb_perror 323
NDB error code 323: Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

To display only the error message, invoke [ndb\\_perror](#page-25-3) with the [--silent](#page-27-0) option (short form -s), as shown here:

```
$> ndb_perror -s 323
Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

Like perror, [ndb\\_perror](#page-25-3) accepts multiple error codes:

```
$> ndb_perror 321 1001
NDB error code 321: Invalid nodegroup id: Permanent error: Application error
NDB error code 1001: Illegal connect string
```

Additional program options for [ndb\\_perror](#page-25-3) are described later in this section.

[ndb\\_perror](#page-25-3) replaces perror --ndb, which is no longer supported by NDB Cluster. To make substitution easier in scripts and other applications that might depend on perror for obtaining NDB error information, [ndb\\_perror](#page-25-3) supports its own "dummy" [--ndb](#page-26-0) option, which does nothing.

The following table includes all options that are specific to the NDB Cluster program [ndb\\_perror](#page-25-3). Additional descriptions follow the table.

### <span id="page-26-1"></span>**Additional Options**

• [--defaults-extra-file](#page-26-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-26-2"></span>• [--defaults-file](#page-26-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-26-3"></span>• [--defaults-group-suffix](#page-26-3)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-26-4"></span>• [--help](#page-26-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display program help text and exit.

<span id="page-26-5"></span>• [--login-path](#page-26-5)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-26-6"></span>• [--no-login-paths](#page-26-6)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-26-0"></span>• [--ndb](#page-26-0)

For compatibility with applications depending on old versions of perror that use that program's [-](https://dev.mysql.com/doc/refman/8.0/en/perror.md#option_perror_ndb) [ndb](https://dev.mysql.com/doc/refman/8.0/en/perror.md#option_perror_ndb) option. The option when used with [ndb\\_perror](#page-25-3) does nothing, and is ignored by it.

<span id="page-26-7"></span>• [--no-defaults](#page-26-7)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-27-1"></span>• [--print-defaults](#page-27-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-27-0"></span>• [--silent](#page-27-0), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Show error message only.

<span id="page-27-2"></span>• [--version](#page-27-2), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Print program version information and exit.

<span id="page-27-3"></span>• [--verbose](#page-27-3), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose output; disable with [--silent](#page-27-0).

## <span id="page-27-4"></span>**25.5.17 ndb\_print\_backup\_file — Print NDB Backup File Contents**

[ndb\\_print\\_backup\\_file](#page-27-4) obtains diagnostic information from a cluster backup file.

### **Usage**

```
ndb_print_backup_file [-P password] file_name
```

file\_name is the name of a cluster backup file. This can be any of the files (.Data, .ctl, or .log file) found in a cluster backup directory. These files are found in the data node's backup directory under the subdirectory BACKUP-#, where # is the sequence number for the backup. For more information about cluster backup files and their contents, see [Section 25.6.8.1, "NDB Cluster Backup Concepts".](#page-151-0)

Like [ndb\\_print\\_schema\\_file](#page-33-0) and [ndb\\_print\\_sys\\_file](#page-33-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_backup\\_file](#page-27-4) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

This program can also be used to read undo log files.

### <span id="page-27-5"></span>**Options**

[ndb\\_print\\_backup\\_file](#page-27-4) supports the options described in the following list.

• [--backup-key](#page-27-5), -K

| Command-Line Format | backup-key=key |
|---------------------|----------------|
|---------------------|----------------|

Specify the key needed to decrypt an encrypted backup.

<span id="page-27-6"></span>• [--backup-key-from-stdin](#page-27-6)

Allow input of the decryption key from standard input, similar to entering a password after invoking mysql --password with no password supplied.

#### <span id="page-28-0"></span>• [--backup-password](#page-28-0)

| Command-Line Format | backup-password=password |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Specify the password needed to decrypt an encrypted backup.

<span id="page-28-1"></span>• [--backup-password-from-stdin](#page-28-1)

Allow input of the password from standard input, similar to entering a password after invoking mysql --password with no password supplied.

<span id="page-28-2"></span>• [--control-directory-number](#page-28-2)

| Command-Line Format | control-directory-number=# |
|---------------------|----------------------------|
| Type                | Integer                    |
| Default Value       | 0                          |

Control file directory number. Used together with [--print-restored-rows](#page-29-0).

<span id="page-28-3"></span>• [--defaults-extra-file](#page-28-3)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-28-4"></span>• [--defaults-file](#page-28-4)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-28-5"></span>• [--defaults-group-suffix](#page-28-5)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-28-6"></span>• [--fragment-id](#page-28-6)

| Command-Line Format | fragment-id=# |
|---------------------|---------------|

| Type          | Integer |
|---------------|---------|
| Default Value | 0       |

Fragment ID. Used together with [--print-restored-rows](#page-29-0).

<span id="page-29-1"></span>• [--help](#page-29-1)

| Command-Line Format | help  |
|---------------------|-------|
|                     | usage |

Print program usage information.

<span id="page-29-2"></span>• [--login-path](#page-29-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-29-3"></span>• [--no-login-paths](#page-29-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-29-4"></span>• [--no-defaults](#page-29-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-29-5"></span>• [--no-print-rows](#page-29-5)

| Command-Line Format | no-print-rows |
|---------------------|---------------|

Do not include rows in output.

<span id="page-29-6"></span>• [--print-defaults](#page-29-6)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-29-7"></span>• [--print-header-words](#page-29-7)

| Command-Line Format | print-header-words |
|---------------------|--------------------|
|---------------------|--------------------|

Include header words in output.

<span id="page-29-0"></span>• [--print-restored-rows](#page-29-0)

| Command-Line Format | print-restored-rows |
|---------------------|---------------------|

Include restored rows in output, using the file LCP/c/TtFf.ctl, for which the values are set as follows:

• c is the control file number set using [--control-directory-number](#page-28-2)

- t is the table ID set using [--table-id](#page-30-0)
- f is the fragment ID set using [--fragment-id](#page-28-6)
- <span id="page-30-1"></span>• [--print-rows](#page-30-1)

| Command-Line Format | print-rows |
|---------------------|------------|
|---------------------|------------|

Print rows. This option is enabled by default; to disable it, use [--no-print-rows](#page-29-5).

<span id="page-30-2"></span>• [--print-rows-per-page](#page-30-2)

| Command-Line Format | print-rows-per-page |
|---------------------|---------------------|
|                     |                     |

Print rows per page.

<span id="page-30-3"></span>• [--rowid-file](#page-30-3)

| Command-Line Format | rowid-file=path |
|---------------------|-----------------|
| Type                | File name       |
| Default Value       | [none]          |

File to check for row ID.

<span id="page-30-4"></span>• [--show-ignored-rows](#page-30-4)

| Command-Line Format | show-ignored-rows |
|---------------------|-------------------|
|---------------------|-------------------|

Show ignored rows.

<span id="page-30-0"></span>• [--table-id](#page-30-0)

| Command-Line Format | table-id=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | [none]     |

Table ID. Used together with [--print-restored-rows](#page-29-0).

<span id="page-30-5"></span>• [--usage](#page-30-5)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-29-1).

<span id="page-30-6"></span>• [--verbose](#page-30-6)

| Command-Line Format | verbose[=#] |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 0           |

Verbosity level of output. A greater value indicates increased verbosity.

<span id="page-30-7"></span>• [--version](#page-30-7)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-31-0"></span>**25.5.18 ndb\_print\_file — Print NDB Disk Data File Contents**

[ndb\\_print\\_file](#page-31-0) obtains information from an NDB Cluster Disk Data file.

### **Usage**

ndb\_print\_file [-v] [-q] file\_name+

file\_name is the name of an NDB Cluster Disk Data file. Multiple filenames are accepted, separated by spaces.

Like [ndb\\_print\\_schema\\_file](#page-33-0) and [ndb\\_print\\_sys\\_file](#page-33-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_file](#page-31-0) must be run on an NDB Cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

### **Options**

[ndb\\_print\\_file](#page-31-0) supports the following options:

<span id="page-31-1"></span>• [--file-key](#page-31-1), -K

| Command-Line Format | file-key=hex_data |
|---------------------|-------------------|
|---------------------|-------------------|

Supply file system encryption or decryption key from stdin, tty, or a my.cnf file.

<span id="page-31-2"></span>• [--file-key-from-stdin](#page-31-2)

| Command-Line Format | file-key-from-stdin |
|---------------------|---------------------|
| Type                | Boolean             |
| Default Value       | FALSE               |
| Valid Values        | TRUE                |

Supply file system encryption or decryption key from stdin.

<span id="page-31-3"></span>• [--help](#page-31-3), -h, -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Print help message and exit.

<span id="page-31-4"></span>• [--quiet](#page-31-4), -q

| Command-Line Format | quiet |
|---------------------|-------|
|---------------------|-------|

Suppress output (quiet mode).

<span id="page-31-5"></span>• [--usage](#page-31-5), -?

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Print help message and exit.

<span id="page-31-6"></span>• [--verbose](#page-31-6), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Make output verbose.

<span id="page-32-0"></span>• [--version](#page-32-0), -v

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Print version information and exit.

For more information, see [Section 25.6.11, "NDB Cluster Disk Data Tables"](#page-159-0).

# <span id="page-32-1"></span>**25.5.19 ndb\_print\_frag\_file — Print NDB Fragment List File Contents**

[ndb\\_print\\_frag\\_file](#page-32-1) obtains information from a cluster fragment list file. It is intended for use in helping to diagnose issues with data node restarts.

### **Usage**

```
ndb_print_frag_file file_name
```

file\_name is the name of a cluster fragment list file, which matches the pattern SX.FragList, where X is a digit in the range 2-9 inclusive, and are found in the data node file system of the data node having the node ID nodeid, in directories named ndb\_nodeid\_fs/DN/DBDIH/, where N is 1 or 2. Each fragment file contains records of the fragments belonging to each NDB table. For more information about cluster fragment files, see [NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md).

Like [ndb\\_print\\_backup\\_file](#page-27-4), [ndb\\_print\\_sys\\_file](#page-33-1), and [ndb\\_print\\_schema\\_file](#page-33-0) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server), [ndb\\_print\\_frag\\_file](#page-32-1) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

### **Additional Options**

None.

### **Sample Output**

```
$> ndb_print_frag_file /usr/local/mysqld/data/ndb_3_fs/D1/DBDIH/S2.FragList
Filename: /usr/local/mysqld/data/ndb_3_fs/D1/DBDIH/S2.FragList with size 8192
noOfPages = 1 noOfWords = 182
Table Data
----------
Num Frags: 2 NoOfReplicas: 2 hashpointer: 4294967040
kvalue: 6 mask: 0x00000000 method: HashMap
Storage is on Logged and checkpointed, survives SR
------ Fragment with FragId: 0 --------
Preferred Primary: 2 numStoredReplicas: 2 numOldStoredReplicas: 0 distKey: 0 LogPartId: 0
-------Stored Replica----------
Replica node is: 2 initialGci: 2 numCrashedReplicas = 0 nextLcpNo = 1
LcpNo[0]: maxGciCompleted: 1 maxGciStarted: 2 lcpId: 1 lcpStatus: valid
LcpNo[1]: maxGciCompleted: 0 maxGciStarted: 0 lcpId: 0 lcpStatus: invalid
-------Stored Replica----------
Replica node is: 3 initialGci: 2 numCrashedReplicas = 0 nextLcpNo = 1
LcpNo[0]: maxGciCompleted: 1 maxGciStarted: 2 lcpId: 1 lcpStatus: valid
LcpNo[1]: maxGciCompleted: 0 maxGciStarted: 0 lcpId: 0 lcpStatus: invalid
------ Fragment with FragId: 1 --------
Preferred Primary: 3 numStoredReplicas: 2 numOldStoredReplicas: 0 distKey: 0 LogPartId: 1
-------Stored Replica----------
Replica node is: 3 initialGci: 2 numCrashedReplicas = 0 nextLcpNo = 1
LcpNo[0]: maxGciCompleted: 1 maxGciStarted: 2 lcpId: 1 lcpStatus: valid
LcpNo[1]: maxGciCompleted: 0 maxGciStarted: 0 lcpId: 0 lcpStatus: invalid
-------Stored Replica----------
Replica node is: 2 initialGci: 2 numCrashedReplicas = 0 nextLcpNo = 1
```

```
LcpNo[0]: maxGciCompleted: 1 maxGciStarted: 2 lcpId: 1 lcpStatus: valid
LcpNo[1]: maxGciCompleted: 0 maxGciStarted: 0 lcpId: 0 lcpStatus: invalid
```

## <span id="page-33-0"></span>**25.5.20 ndb\_print\_schema\_file — Print NDB Schema File Contents**

[ndb\\_print\\_schema\\_file](#page-33-0) obtains diagnostic information from a cluster schema file.

### **Usage**

```
ndb_print_schema_file file_name
```

file\_name is the name of a cluster schema file. For more information about cluster schema files, see [NDB Cluster Data Node File System Directory.](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md)

Like [ndb\\_print\\_backup\\_file](#page-27-4) and [ndb\\_print\\_sys\\_file](#page-33-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_schema\\_file](#page-33-0) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

### **Additional Options**

None.

## <span id="page-33-1"></span>**25.5.21 ndb\_print\_sys\_file — Print NDB System File Contents**

[ndb\\_print\\_sys\\_file](#page-33-1) obtains diagnostic information from an NDB Cluster system file.

## **Usage**

```
ndb_print_sys_file file_name
```

file\_name is the name of a cluster system file (sysfile). Cluster system files are located in a data node's data directory (DataDir); the path under this directory to system files matches the pattern ndb\_#\_fs/D#/DBDIH/P#.sysfile. In each case, the # represents a number (not necessarily the same number). For more information, see [NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md).

Like [ndb\\_print\\_backup\\_file](#page-27-4) and [ndb\\_print\\_schema\\_file](#page-33-0) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_backup\\_file](#page-27-4) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

### **Additional Options**

None.

# <span id="page-33-2"></span>**25.5.22 ndb\_redo\_log\_reader — Check and Print Content of Cluster Redo Log**

Reads a redo log file, checking it for errors, printing its contents in a human-readable format, or both. [ndb\\_redo\\_log\\_reader](#page-33-2) is intended for use primarily by NDB Cluster developers and Support personnel in debugging and diagnosing problems.

This utility remains under development, and its syntax and behavior are subject to change in future NDB Cluster releases.

The C++ source files for [ndb\\_redo\\_log\\_reader](#page-33-2) can be found in the directory /storage/ndb/src/ kernel/blocks/dblqh/redoLogReader.

Options that can be used with [ndb\\_redo\\_log\\_reader](#page-33-2) are shown in the following table. Additional descriptions follow the table.

### **Usage**

ndb\_redo\_log\_reader file\_name [options]

file\_name is the name of a cluster redo log file. redo log files are located in the numbered directories under the data node's data directory (DataDir); the path under this directory to the redo log files matches the pattern ndb\_nodeid\_fs/D#/DBLQH/S#.FragLog. nodeid is the data node's node ID. The two instances of # each represent a number (not necessarily the same number); the number following D is in the range 8-39 inclusive; the range of the number following S varies according to the value of the NoOfFragmentLogFiles configuration parameter, whose default value is 16; thus, the default range of the number in the file name is 0-15 inclusive. For more information, see [NDB Cluster](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md) [Data Node File System Directory.](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md)

The name of the file to be read may be followed by one or more of the options listed here:

<span id="page-34-0"></span>• [-dump](#page-34-0)

| Command-Line Format<br>-dump |
|------------------------------|
|------------------------------|

Print dump info.

<span id="page-34-1"></span>• [--file-key](#page-34-1), -K

| Command-Line Format | file-key=key |
|---------------------|--------------|
|---------------------|--------------|

Supply file decryption key using stdin, tty, or a my.cnf file.

<span id="page-34-2"></span>• [--file-key-from-stdin](#page-34-2)

| Command-Line Format | file-key-from-stdin |
|---------------------|---------------------|
|---------------------|---------------------|

Supply file decryption key using stdin.

<span id="page-34-3"></span>

| •<br>Command-Line Format<br>-filedescriptors |  |
|----------------------------------------------|--|
|----------------------------------------------|--|

[-filedescriptors](#page-34-3): Print file descriptors only.

<span id="page-34-4"></span>

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

[--help](#page-34-4): Print usage information.

<span id="page-34-5"></span>• [-lap](#page-34-5)

| Command-Line Format | -lap |
|---------------------|------|

Provide lap info, with max GCI started and completed.

<span id="page-34-6"></span>

| • | Command-Line Format | -mbyte # |
|---|---------------------|----------|
|   | Type                | Numeric  |
|   | Default Value       | 0        |
|   | Minimum Value       | 0        |
|   | Maximum Value       | 15       |

[-mbyte](#page-34-6) #: Starting megabyte.

# is an integer in the range 0 to 15, inclusive.

<span id="page-35-0"></span>

| Command-Line Format | -mbyteheaders |
|---------------------|---------------|
|---------------------|---------------|

[-mbyteheaders](#page-35-0): Show only the first page header of every megabyte in the file.

<span id="page-35-1"></span>

| •<br>Command-Line Format | -noprint |
|--------------------------|----------|
|--------------------------|----------|

[-noprint](#page-35-1): Do not print the contents of the log file.

<span id="page-35-2"></span>

| •<br>Command-Line Format<br>-nocheck |  |
|--------------------------------------|--|
|--------------------------------------|--|

[-nocheck](#page-35-2): Do not check the log file for errors.

<span id="page-35-3"></span>

| • | Command-Line Format | -page # |
|---|---------------------|---------|
|   | Type                | Integer |
|   | Default Value       | 0       |
|   | Minimum Value       | 0       |
|   | Maximum Value       | 31      |

[-page](#page-35-3) #: Start at this page.

# is an integer in the range 0 to 31, inclusive.

<span id="page-35-4"></span>

| •<br>Command-Line Format | -pageheaders |  |
|--------------------------|--------------|--|
|--------------------------|--------------|--|

[-pageheaders](#page-35-4): Show page headers only.

<span id="page-35-5"></span>

| • | Command-Line Format | -pageindex # |
|---|---------------------|--------------|
|   | Type                | Integer      |
|   | Default Value       | 12           |
|   | Minimum Value       | 12           |
|   | Maximum Value       | 8191         |

[<sup>-</sup>pageindex](#page-35-5) #: Start at this page index.

# is an integer between 12 and 8191, inclusive.

<span id="page-35-6"></span>• [-twiddle](#page-35-6)

Bit-shifted dump.

Like [ndb\\_print\\_backup\\_file](#page-27-4) and [ndb\\_print\\_schema\\_file](#page-33-0) (and unlike most of the NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_redo\\_log\\_reader](#page-33-2) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

# <span id="page-35-7"></span>**25.5.23 ndb\_restore — Restore an NDB Cluster Backup**

The NDB Cluster restoration program is implemented as a separate command-line utility [ndb\\_restore](#page-35-7), which can normally be found in the MySQL bin directory. This program reads the files created as a result of the backup and inserts the stored information into the database.

[ndb\\_restore](#page-35-7) must be executed once for each of the backup files that were created by the [START](#page-151-1) [BACKUP](#page-151-1) command used to create the backup (see [Section 25.6.8.2, "Using The NDB Cluster](#page-151-1) [Management Client to Create a Backup"](#page-151-1)). This is equal to the number of data nodes in the cluster at the time that the backup was created.

![](_page_36_Picture_2.jpeg)

#### **Note**

Before using [ndb\\_restore](#page-35-7), it is recommended that the cluster be running in single user mode, unless you are restoring multiple data nodes in parallel. See [Section 25.6.6, "NDB Cluster Single User Mode"](#page-139-0), for more information.

Options that can be used with [ndb\\_restore](#page-35-7) are shown in the following table. Additional descriptions follow the table.

<span id="page-36-0"></span>• [--allow-pk-changes](#page-36-0)

| Command-Line Format | allow-pk-changes[=0 1] |
|---------------------|------------------------|
| Type                | Integer                |
| Default Value       | 0                      |
| Minimum Value       | 0                      |
| Maximum Value       | 1                      |

When this option is set to 1, [ndb\\_restore](#page-35-7) allows the primary keys in a table definition to differ from that of the same table in the backup. This may be desirable when backing up and restoring between different schema versions with primary key changes on one or more tables, and it appears that performing the restore operation using ndb\_restore is simpler or more efficient than issuing many ALTER TABLE statements after restoring table schemas and data.

The following changes in primary key definitions are supported by --allow-pk-changes:

• **Extending the primary key**: A non-nullable column that exists in the table schema in the backup becomes part of the table's primary key in the database.

![](_page_36_Picture_11.jpeg)

#### **Important**

When extending a table's primary key, any columns which become part of primary key must not be updated while the backup is being taken; any such updates discovered by [ndb\\_restore](#page-35-7) cause the restore operation to fail, even when no change in value takes place. In some cases, it may be possible to override this behavior using the [--ignore-extended-pk](#page-43-0)[updates](#page-43-0) option; see the description of this option for more information.

- **Contracting the primary key (1)**: A column that is already part of the table's primary key in the backup schema is no longer part of the primary key, but remains in the table.
- **Contracting the primary key (2)**: A column that is already part of the table's primary key in the backup schema is removed from the table entirely.

These differences can be combined with other schema differences supported by [ndb\\_restore](#page-35-7), including changes to blob and text columns requiring the use of staging tables.

Basic steps in a typical scenario using primary key schema changes are listed here:

- 1. Restore table schemas using [ndb\\_restore](#page-35-7) [--restore-meta](#page-53-0)
- 2. Alter schema to that desired, or create it
- 3. Back up the desired schema

- 4. Run [ndb\\_restore](#page-35-7) [--disable-indexes](#page-40-0) using the backup from the previous step, to drop indexes and constraints
- 5. Run [ndb\\_restore](#page-35-7) [--allow-pk-changes](#page-36-0) (possibly along with [--ignore-extended-pk](#page-43-0)[updates](#page-43-0), [--disable-indexes](#page-40-0), and possibly other options as needed) to restore all data
- 6. Run [ndb\\_restore](#page-35-7) [--rebuild-indexes](#page-52-0) using the backup made with the desired schema, to rebuild indexes and constraints

When extending the primary key, it may be necessary for [ndb\\_restore](#page-35-7) to use a temporary secondary unique index during the restore operation to map from the old primary key to the new one. Such an index is created only when necessary to apply events from the backup log to a table which has an extended primary key. This index is named NDB\$RESTORE\_PK\_MAPPING, and is created on each table requiring it; it can be shared, if necessary, by multiple instances of [ndb\\_restore](#page-35-7) instances running in parallel. (Running [ndb\\_restore](#page-35-7) [--rebuild-indexes](#page-52-0) at the end of the restore process causes this index to be dropped.)

<span id="page-37-0"></span>• [--append](#page-37-0)

| Command-Line Format | append |
|---------------------|--------|
|---------------------|--------|

When used with the [--tab](#page-56-0) and [--print-data](#page-50-0) options, this causes the data to be appended to any existing files having the same names.

<span id="page-37-1"></span>• [--backup-path](#page-37-1)=dir\_name

| Command-Line Format | backup-path=path |
|---------------------|------------------|
| Type                | Directory name   |
| Default Value       | ./               |

The path to the backup directory is required; this is supplied to [ndb\\_restore](#page-35-7) using the --backuppath option, and must include the subdirectory corresponding to the ID backup of the backup to be restored. For example, if the data node's DataDir is /var/lib/mysql-cluster, then the backup directory is /var/lib/mysql-cluster/BACKUP, and the backup files for the backup with the ID 3 can be found in /var/lib/mysql-cluster/BACKUP/BACKUP-3. The path may be absolute or relative to the directory in which the [ndb\\_restore](#page-35-7) executable is located, and may be optionally prefixed with backup-path=.

It is possible to restore a backup to a database with a different configuration than it was created from. For example, suppose that a backup with backup ID 12, created in a cluster with two storage nodes having the node IDs 2 and 3, is to be restored to a cluster with four nodes. Then [ndb\\_restore](#page-35-7) must be run twice—once for each storage node in the cluster where the backup was taken. However, [ndb\\_restore](#page-35-7) cannot always restore backups made from a cluster running one version of MySQL to a cluster running a different MySQL version. See Section 25.3.7, "Upgrading and Downgrading NDB Cluster", for more information.

![](_page_37_Picture_12.jpeg)

#### **Important**

It is not possible to restore a backup made from a newer version of NDB Cluster using an older version of [ndb\\_restore](#page-35-7). You can restore a backup made from a newer version of MySQL to an older cluster, but you must use a copy of [ndb\\_restore](#page-35-7) from the newer NDB Cluster version to do so.

For example, to restore a cluster backup taken from a cluster running NDB Cluster 8.4.7 to a cluster running NDB Cluster 8.0.44, you must use the [ndb\\_restore](#page-35-7) that comes with the NDB Cluster 8.0.44 distribution.

For more rapid restoration, the data may be restored in parallel, provided that there is a sufficient number of cluster connections available. That is, when restoring to multiple nodes in parallel, you must have an [api] or [mysqld] section in the cluster config.ini file available for each concurrent [ndb\\_restore](#page-35-7) process. However, the data files must always be applied before the logs.

<span id="page-38-0"></span>• [--backup-password=](#page-38-0)password

| Command-Line Format | backup-password=password |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

This option specifies a password to be used when decrypting an encrypted backup with the [-](#page-39-0) [decrypt](#page-39-0) option. This must be the same password that was used to encrypt the backup.

The password must be 1 to 256 characters in length, and must be enclosed by single or double quotation marks. It can contain any of the ASCII characters having character codes 32, 35, 38, 40-91, 93, 95, and 97-126; in other words, it can use any printable ASCII characters except for !, ', ", \$, %, \, and ^.

It is possible to omit the password, in which case [ndb\\_restore](#page-35-7) waits for it to be supplied from stdin, as when using [--backup-password-from-stdin](#page-38-1).

<span id="page-38-1"></span>• [--backup-password-from-stdin\[=TRUE|FALSE\]](#page-38-1)

| Command-Line Format | backup-password-from-stdin |
|---------------------|----------------------------|
|---------------------|----------------------------|

When used in place of [--backup-password](#page-38-0), this option enables input of the backup password from the system shell (stdin), similar to how this is done when supplying the password interactively to mysql when using the --password without supplying the password on the command line.

<span id="page-38-2"></span>• [--backupid](#page-38-2)=#, -b

| Command-Line Format | backupid=# |
|---------------------|------------|
| Type                | Numeric    |
| Default Value       | none       |

This option is required; it is used to specify the ID or sequence number of the backup, and is the same number shown by the management client in the Backup backup\_id completed message displayed upon completion of a backup. (See [Section 25.6.8.2, "Using The NDB Cluster](#page-151-1) [Management Client to Create a Backup"](#page-151-1).)

![](_page_38_Picture_15.jpeg)

#### **Important**

When restoring cluster backups, you must be sure to restore all data nodes from backups having the same backup ID. Using files from different backups results at best in restoring the cluster to an inconsistent state, and is likely to fail altogether.

<span id="page-38-3"></span>• [--character-sets-dir](#page-38-3)

Directory containing character sets.

<span id="page-39-1"></span>• [--connect](#page-39-1), -c

| Command-Line Format | connect=connection_string |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | localhost:1186            |

Alias for [--ndb-connectstring](#page-46-0).

<span id="page-39-2"></span>• [--connect-retries](#page-39-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-39-3"></span>• [--connect-retry-delay](#page-39-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-39-4"></span>• [--connect-string](#page-39-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-46-0).

<span id="page-39-5"></span>• [--core-file](#page-39-5)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-39-0"></span>• [--decrypt](#page-39-0)

| Command-Line Format | decrypt |
|---------------------|---------|
|---------------------|---------|

Decrypt an encrypted backup using the password supplied by the [--backup-password](#page-38-0) option.

<span id="page-39-6"></span>• [--defaults-extra-file](#page-39-6)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |

| Default Value | [none] |  |
|---------------|--------|--|
|---------------|--------|--|

Read given file after global files are read.

<span id="page-40-1"></span>• [--defaults-file](#page-40-1)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-40-2"></span>• [--defaults-group-suffix](#page-40-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-40-0"></span>• [--disable-indexes](#page-40-0)

| Command-Line Format | disable-indexes |
|---------------------|-----------------|
|---------------------|-----------------|

Disable restoration of indexes during restoration of the data from a native NDB backup. Afterwards, you can restore indexes for all tables at once with multithreaded building of indexes using [-](#page-52-0) [rebuild-indexes](#page-52-0), which should be faster than rebuilding indexes concurrently for very large tables.

This option also drops any foreign keys specified in the backup.

MySQL can open an NDB table for which one or more indexes cannot be found, provided the query does not use any of the affected indexes; otherwise the query is rejected with [ER\\_NOT\\_KEYFILE](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_not_keyfile). In the latter case, you can temporarily work around the problem by executing an ALTER TABLE statement such as this one:

```
ALTER TABLE tbl ALTER INDEX idx INVISIBLE;
```

This causes MySQL to ignore the index idx on table tbl. See Primary Keys and Indexes, for more information, as well as Section 10.3.12, "Invisible Indexes".

<span id="page-40-3"></span>• [--dont-ignore-systab-0](#page-40-3), -f

| Command-Line Format | dont-ignore-systab-0 |
|---------------------|----------------------|

Normally, when restoring table data and metadata, [ndb\\_restore](#page-35-7) ignores the copy of the NDB system table that is present in the backup. --dont-ignore-systab-0 causes the system table to be restored. This option is intended for experimental and development use only, and is not recommended in a production environment.

<span id="page-40-4"></span>• [--exclude-databases](#page-40-4)=db-list

| Command-Line Format | exclude-databases=list |
|---------------------|------------------------|
| Type                | String                 |

| Default Value |  |
|---------------|--|
|---------------|--|

Comma-delimited list of one or more databases which should not be restored.

This option is often used in combination with [--exclude-tables](#page-41-0); see that option's description for further information and examples.

<span id="page-41-1"></span>• [--exclude-intermediate-sql-tables\[](#page-41-1)=TRUE|FALSE]

| Command-Line Format | exclude-intermediate-sql<br>tables[=TRUE FALSE] |
|---------------------|-------------------------------------------------|
| Type                | Boolean                                         |
| Default Value       | TRUE                                            |

When performing copying ALTER TABLE operations, mysqld creates intermediate tables (whose names are prefixed with #sql-). When TRUE, the --exclude-intermediate-sql-tables option keeps [ndb\\_restore](#page-35-7) from restoring such tables that may have been left over from these operations. This option is TRUE by default.

<span id="page-41-2"></span>• [--exclude-missing-columns](#page-41-2)

| Command-Line Format | exclude-missing-columns |
|---------------------|-------------------------|
|---------------------|-------------------------|

It is possible to restore only selected table columns using this option, which causes [ndb\\_restore](#page-35-7) to ignore any columns missing from tables being restored as compared to the versions of those tables found in the backup. This option applies to all tables being restored. If you wish to apply this option only to selected tables or databases, you can use it in combination with one or more of the - include-\* or --exclude-\* options described elsewhere in this section to do so, then restore data to the remaining tables using a complementary set of these options.

<span id="page-41-3"></span>• [--exclude-missing-tables](#page-41-3)

| Command-Line Format | exclude-missing-tables |
|---------------------|------------------------|
|---------------------|------------------------|

It is possible to restore only selected tables using this option, which causes [ndb\\_restore](#page-35-7) to ignore any tables from the backup that are not found in the target database.

<span id="page-41-0"></span>• [--exclude-tables](#page-41-0)=table-list

| Command-Line Format | exclude-tables=list |
|---------------------|---------------------|
| Type                | String              |

| Default Value |  |
|---------------|--|
|---------------|--|

List of one or more tables to exclude; each table reference must include the database name. Often used together with [--exclude-databases](#page-40-4).

When [--exclude-databases](#page-40-4) or --exclude-tables is used, only those databases or tables named by the option are excluded; all other databases and tables are restored by [ndb\\_restore](#page-35-7).

This table shows several invocations of [ndb\\_restore](#page-35-7) using --exclude-\* options (other options possibly required have been omitted for clarity), and the effects these options have on restoring from an NDB Cluster backup:

**Table 25.23 Several invocations of ndb\_restore using --exclude-\* options, and the effects these options have on restoring from an NDB Cluster backup.**

| Option                                                                             | Result                                                                                                                                                                                                           |
|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| exclude-databases=db1                                                              | All tables in all databases except db1 are<br>restored; no tables in db1 are restored                                                                                                                            |
| exclude-databases=db1,db2 (or<br>exclude-databases=db1exclude<br>databases=db2)    | All tables in all databases except db1 and<br>db2 are restored; no tables in db1 or db2 are<br>restored                                                                                                          |
| exclude-tables=db1.t1                                                              | All tables except t1 in database db1 are<br>restored; all other tables in db1 are restored; all<br>tables in all other databases are restored                                                                    |
| exclude-tables=db1.t2,db2.t1 (or<br>exclude-tables=db1.t2exclude<br>tables=db2.t1) | All tables in database db1 except for t2 and<br>all tables in database db2 except for table t1<br>are restored; no other tables in db1 or db2 are<br>restored; all tables in all other databases are<br>restored |

You can use these two options together. For example, the following causes all tables in all databases except for databases db1 and db2, and tables t1 and t2 in database db3, to be restored:

```
$> ndb_restore [...] --exclude-databases=db1,db2 --exclude-tables=db3.t1,db3.t2
```

(Again, we have omitted other possibly necessary options in the interest of clarity and brevity from the example just shown.)

You can use --include-\* and --exclude-\* options together, subject to the following rules:

- The actions of all --include-\* and --exclude-\* options are cumulative.
- All --include-\* and --exclude-\* options are evaluated in the order passed to ndb\_restore, from right to left.
- In the event of conflicting options, the first (rightmost) option takes precedence. In other words, the first option (going from right to left) that matches against a given database or table "wins".

For example, the following set of options causes [ndb\\_restore](#page-35-7) to restore all tables from database db1 except db1.t1, while restoring no other tables from any other databases:

```
--include-databases=db1 --exclude-tables=db1.t1
```

However, reversing the order of the options just given simply causes all tables from database db1 to be restored (including db1.t1, but no tables from any other database), because the [--include](#page-44-0)[databases](#page-44-0) option, being farthest to the right, is the first match against database db1 and thus takes precedence over any other option that matches db1 or any tables in db1:

### <span id="page-43-1"></span>• [--fields-enclosed-by](#page-43-1)=char

| Command-Line Format | fields-enclosed-by=char |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       |                         |

Each column value is enclosed by the string passed to this option (regardless of data type; see the description of [--fields-optionally-enclosed-by](#page-43-2)).

#### <span id="page-43-2"></span>• [--fields-optionally-enclosed-by](#page-43-2)

| Command-Line Format | fields-optionally-enclosed-by |
|---------------------|-------------------------------|
| Type                | String                        |
| Default Value       |                               |

The string passed to this option is used to enclose column values containing character data (such as CHAR, VARCHAR, BINARY, TEXT, or ENUM).

#### <span id="page-43-3"></span>• [--fields-terminated-by](#page-43-3)=char

| Command-Line Format | fields-terminated-by=char |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | \t (tab)                  |

The string passed to this option is used to separate column values. The default value is a tab character (\t).

#### <span id="page-43-4"></span>• [--help](#page-43-4)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

#### <span id="page-43-5"></span>• [--hex](#page-43-5)

| Command-Line Format | hex |
|---------------------|-----|

If this option is used, all binary values are output in hexadecimal format.

#### <span id="page-43-0"></span>• [--ignore-extended-pk-updates](#page-43-0)

| Command-Line Format | ignore-extended-pk-updates[=0 1] |
|---------------------|----------------------------------|
| Type                | Integer                          |
| Default Value       | 0                                |
| Minimum Value       | 0                                |
| Maximum Value       | 1                                |

When using [--allow-pk-changes](#page-36-0), columns which become part of a table's primary key must not be updated while the backup is being taken; such columns should keep the same values from the time values are inserted into them until the rows containing the values are deleted. If [ndb\\_restore](#page-35-7) encounters updates to these columns when restoring a backup, the restore fails. Because some applications may set values for all columns when updating a row, even when some column values are not changed, the backup may include log events appearing to update columns which are not in fact modified. In such cases you can set --ignore-extended-pk-updates to 1, forcing [ndb\\_restore](#page-35-7) to ignore such updates.

![](_page_44_Picture_1.jpeg)

#### **Important**

When causing these updates to be ignored, the user is responsible for ensuring that there are no updates to the values of any columns that become part of the primary key.

For more information, see the description of [--allow-pk-changes](#page-36-0).

<span id="page-44-0"></span>• [--include-databases](#page-44-0)=db-list

| Command-Line Format | include-databases=list |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       |                        |

Comma-delimited list of one or more databases to restore. Often used together with [--include](#page-44-1)[tables](#page-44-1); see the description of that option for further information and examples.

<span id="page-44-2"></span>• [--include-stored-grants](#page-44-2)

| Command-Line Format | include-stored-grants |
|---------------------|-----------------------|
|---------------------|-----------------------|

[ndb\\_restore](#page-35-7) does not by default restore shared users and grants (see [Section 25.6.13, "Privilege](#page-168-0) [Synchronization and NDB\\_STORED\\_USER"](#page-168-0)) to the ndb\_sql\_metadata table. Specifying this option causes it to do so.

<span id="page-44-1"></span>• [--include-tables](#page-44-1)=table-list

| Command-Line Format | include-tables=list |
|---------------------|---------------------|
| Type                | String              |
| Default Value       |                     |

Comma-delimited list of tables to restore; each table reference must include the database name.

When --include-databases or [--include-tables](#page-44-1) is used, only those databases or tables named by the option are restored; all other databases and tables are excluded by [ndb\\_restore](#page-35-7), and are not restored.

The following table shows several invocations of [ndb\\_restore](#page-35-7) using --include-\* options (other options possibly required have been omitted for clarity), and the effects these have on restoring from an NDB Cluster backup:

**Table 25.24 Several invocations of ndb\_restore using --include-\* options, and their effects on restoring from an NDB Cluster backup.**

| Option                                                                             | Result                                                                                                                                                 |
|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| include-databases=db1                                                              | Only tables in database db1 are restored; all<br>tables in all other databases are ignored                                                             |
| include-databases=db1,db2 (or<br>include-databases=db1include<br>databases=db2)    | Only tables in databases db1 and db2 are<br>restored; all tables in all other databases are<br>ignored                                                 |
| include-tables=db1.t1                                                              | Only table t1 in database db1 is restored; no<br>other tables in db1 or in any other database are<br>restored                                          |
| include-tables=db1.t2,db2.t1 (or<br>include-tables=db1.t2include<br>tables=db2.t1) | Only the table t2 in database db1 and the table<br>t1 in database db2 are restored; no other tables<br>in db1, db2, or any other database are restored |

You can also use these two options together. For example, the following causes all tables in databases db1 and db2, together with the tables t1 and t2 in database db3, to be restored (and no other databases or tables):

```
$> ndb_restore [...] --include-databases=db1,db2 --include-tables=db3.t1,db3.t2
```

(Again we have omitted other, possibly required, options in the example just shown.)

It also possible to restore only selected databases, or selected tables from a single database, without any --include-\* (or --exclude-\*) options, using the syntax shown here:

```
ndb_restore other_options db_name,[db_name[,...] | tbl_name[,tbl_name][,...]]
```

In other words, you can specify either of the following to be restored:

- All tables from one or more databases
- One or more tables from a single database
- <span id="page-45-0"></span>• [--lines-terminated-by](#page-45-0)=char

| Command-Line Format | lines-terminated-by=char |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | \n (linebreak)           |

Specifies the string used to end each line of output. The default is a linefeed character (\n).

<span id="page-45-1"></span>• [--login-path](#page-45-1)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-45-2"></span>• [--no-login-paths](#page-45-2)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-45-3"></span>• [--lossy-conversions](#page-45-3), -L

| Command-Line Format | lossy-conversions |
|---------------------|-------------------|
|---------------------|-------------------|

This option is intended to complement the [--promote-attributes](#page-51-0) option. Using --lossyconversions allows lossy conversions of column values (type demotions or changes in sign) when restoring data from backup. With some exceptions, the rules governing demotion are the same as for MySQL replication; see Replication of Columns Having Different Data Types, for information about specific type conversions currently supported by attribute demotion.

This option also makes it possible to restore a NULL column as NOT NULL. The column must not contain any NULL entries; otherwise [ndb\\_restore](#page-35-7) stops with an error.

[ndb\\_restore](#page-35-7) reports any truncation of data that it performs during lossy conversions once per attribute and column.

#### <span id="page-46-1"></span>• [--no-binlog](#page-46-1)

| Command-Line Format | no-binlog |
|---------------------|-----------|
|                     |           |

This option prevents any connected SQL nodes from writing data restored by [ndb\\_restore](#page-35-7) to their binary logs.

<span id="page-46-2"></span>• [--no-restore-disk-objects](#page-46-2), -d

| Command-Line Format | no-restore-disk-objects |
|---------------------|-------------------------|
|---------------------|-------------------------|

This option stops [ndb\\_restore](#page-35-7) from restoring any NDB Cluster Disk Data objects, such as tablespaces and log file groups; see [Section 25.6.11, "NDB Cluster Disk Data Tables"](#page-159-0), for more information about these.

<span id="page-46-3"></span>• [--no-upgrade](#page-46-3), -u

| Command-Line Format | no-upgrade |
|---------------------|------------|
|---------------------|------------|

When using [ndb\\_restore](#page-35-7) to restore a backup, VARCHAR columns created using the old fixed format are resized and recreated using the variable-width format now employed. This behavior can be overridden by specifying --no-upgrade.

<span id="page-46-0"></span>• [--ndb-connectstring](#page-46-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
|                     |                                 |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-46-4"></span>• [--ndb-mgm-tls](#page-46-4)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-46-5"></span>• [--ndb-mgmd-host](#page-46-5)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-46-0).

<span id="page-46-6"></span>• [--ndb-nodegroup-map](#page-46-6)=map, -z

| Command-Line Format | ndb-nodegroup-map=map |
|---------------------|-----------------------|

Any value set for this option is ignored, and the option itself does nothing.

#### <span id="page-47-0"></span>• [--ndb-nodeid](#page-47-0)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-46-0).

<span id="page-47-1"></span>• [--ndb-optimized-node-selection](#page-47-1)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-47-2"></span>• [--ndb-tls-search-path](#page-47-2)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-47-3"></span>• [--no-defaults](#page-47-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-47-4"></span>• [--nodeid](#page-47-4)=#, -n

| Command-Line Format | nodeid=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | none     |

Specify the node ID of the data node on which the backup was taken; required.

When restoring to a cluster with different number of data nodes from that where the backup was taken, this information helps identify the correct set or sets of files to be restored to a given node. (In such cases, multiple files usually need to be restored to a single data node.) See [Restoring to a](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-different-number-nodes.md) [different number of data nodes](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-different-number-nodes.md), for additional information and examples.

<span id="page-48-0"></span>• [--num-slices](#page-48-0)=#

| Command-Line Format | num-slices=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 1            |
| Minimum Value       | 1            |
| Maximum Value       | 1024         |

When restoring a backup by slices, this option sets the number of slices into which to divide the backup. This allows multiple instances of [ndb\\_restore](#page-35-7) to restore disjoint subsets in parallel, potentially reducing the amount of time required to perform the restore operation.

A slice is a subset of the data in a given backup; that is, it is a set of fragments having the same slice ID, specified using the [--slice-id](#page-55-0) option. The two options must always be used together, and the value set by --slice-id must always be less than the number of slices.

[ndb\\_restore](#page-35-7) encounters fragments and assigns each one a fragment counter. When restoring by slices, a slice ID is assigned to each fragment; this slice ID is in the range 0 to 1 less than the number of slices. For a table that is not a BLOB table, the slice to which a given fragment belongs is determined using the formula shown here:

```
[slice_ID] = [fragment_counter] % [number_of_slices]
```

For a BLOB table, a fragment counter is not used; the fragment number is used instead, along with the ID of the main table for the BLOB table (recall that NDB stores BLOB values in a separate table internally). In this case, the slice ID for a given fragment is calculated as shown here:

```
[slice_ID] =
([main_table_ID] + [fragment_ID]) % [number_of_slices]
```

Thus, restoring by N slices means running N instances of [ndb\\_restore](#page-35-7), all with --num-slices=N (along with any other necessary options) and one each with [--slice-id=1](#page-55-0), --slice-id=2, - slice-id=3, and so on through slice-id=N-1.

**Example.** Assume that you want to restore a backup named BACKUP-1, found in the default directory /var/lib/mysql-cluster/BACKUP/BACKUP-3 on the node file system on each data node, to a cluster with four data nodes having the node IDs 1, 2, 3, and 4. To perform this operation using five slices, execute the sets of commands shown in the following list:

1. Restore the cluster metadata using [ndb\\_restore](#page-35-7) as shown here:

```
$> ndb_restore -b 1 -n 1 -m --disable-indexes --backup-path=/home/ndbuser/backups
```

2. Restore the cluster data to the data nodes invoking [ndb\\_restore](#page-35-7) as shown here:

```
$> ndb_restore -b 1 -n 1 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 1 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 1 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 1 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 1 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 2 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 2 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 2 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 2 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 2 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

```
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

All of the commands just shown in this step can be executed in parallel, provided there are enough slots for connections to the cluster (see the description for the [--backup-path](#page-37-1) option).

3. Restore indexes as usual, as shown here:

```
$> ndb_restore -b 1 -n 1 --rebuild-indexes --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

4. Finally, restore the epoch, using the command shown here:

```
$> ndb_restore -b 1 -n 1 --restore-epoch --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

You should use slicing to restore the cluster data only; it is not necessary to employ [--num-slices](#page-48-0) or [--slice-id](#page-55-0) when restoring the metadata, indexes, or epoch information. If either or both of these options are used with the [ndb\\_restore](#page-35-7) options controlling restoration of these, the program ignores them.

The effects of using the [--parallelism](#page-49-0) option on the speed of restoration are independent of those produced by slicing or parallel restoration using multiple instances of [ndb\\_restore](#page-35-7) (- parallelism specifies the number of parallel transactions executed by a single [ndb\\_restore](#page-35-7) thread), but it can be used together with either or both of these. You should be aware that increasing --parallelism causes [ndb\\_restore](#page-35-7) to impose a greater load on the cluster; if the system can handle this, restoration should complete even more quickly.

The value of --num-slices is not directly dependent on values relating to hardware such as number of CPUs or CPU cores, amount of RAM, and so forth, nor does it depend on the number of LDMs.

It is possible to employ different values for this option on different data nodes as part of the same restoration; doing so should not in and of itself produce any ill effects.

<span id="page-49-0"></span>• [--parallelism](#page-49-0)=#, -p

| Command-Line Format | parallelism=# |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 128           |
| Minimum Value       | 1             |
| Maximum Value       | 1024          |

[ndb\\_restore](#page-35-7) uses single-row transactions to apply many rows concurrently. This parameter determines the number of parallel transactions (concurrent rows) that an instance of [ndb\\_restore](#page-35-7) tries to use. By default, this is 128; the minimum is 1, and the maximum is 1024.

The work of performing the inserts is parallelized across the threads in the data nodes involved. This mechanism is employed for restoring bulk data from the .Data file—that is, the fuzzy snapshot of the data; it is not used for building or rebuilding indexes. The change log is applied serially; index drops and builds are DDL operations and handled separately. There is no thread-level parallelism on the client side of the restore.

<span id="page-50-1"></span>• [--preserve-trailing-spaces](#page-50-1), -P

| Command-Line Format | preserve-trailing-spaces |
|---------------------|--------------------------|
|---------------------|--------------------------|

Cause trailing spaces to be preserved when promoting a fixed-width character data type to its variable-width equivalent—that is, when promoting a CHAR column value to VARCHAR, or a BINARY column value to VARBINARY. Otherwise, any trailing spaces are dropped from such column values when they are inserted into the new columns.

![](_page_50_Picture_4.jpeg)

#### **Note**

Although you can promote CHAR columns to VARCHAR and BINARY columns to VARBINARY, you cannot promote VARCHAR columns to CHAR or VARBINARY columns to BINARY.

<span id="page-50-2"></span>• [--print](#page-50-2)

| Command-Line Format | print |
|---------------------|-------|
|---------------------|-------|

Causes [ndb\\_restore](#page-35-7) to print all data, metadata, and logs to stdout. Equivalent to using the [-](#page-50-0) [print-data](#page-50-0), [--print-meta](#page-50-3), and [--print-log](#page-50-4) options together.

![](_page_50_Picture_10.jpeg)

#### **Note**

Use of --print or any of the --print\_\* options is in effect performing a dry run. Including one or more of these options causes any output to be redirected to stdout; in such cases, [ndb\\_restore](#page-35-7) makes no attempt to restore data or metadata to an NDB Cluster.

<span id="page-50-0"></span>• [--print-data](#page-50-0)

| Command-Line Format | print-data |
|---------------------|------------|
|---------------------|------------|

Cause [ndb\\_restore](#page-35-7) to direct its output to stdout. Often used together with one or more of [--tab](#page-56-0), [--fields-enclosed-by](#page-43-1), [--fields-optionally-enclosed-by](#page-43-2), [--fields-terminated](#page-43-3)[by](#page-43-3), [--hex](#page-43-5), and [--append](#page-37-0).

TEXT and BLOB column values are always truncated. Such values are truncated to the first 256 bytes in the output. This cannot currently be overridden when using --print-data.

<span id="page-50-5"></span>• [--print-defaults](#page-50-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-50-4"></span>• [--print-log](#page-50-4)

| Command-Line Format | print-log |
|---------------------|-----------|

Cause [ndb\\_restore](#page-35-7) to output its log to stdout.

<span id="page-50-3"></span>• [--print-meta](#page-50-3)

| Command-Line Format | print-meta |  |
|---------------------|------------|--|
|                     |            |  |
|                     |            |  |

Print all metadata to stdout.

<span id="page-51-1"></span>• [print-sql-log](#page-51-1)

| Command-Line Format | print-sql-log |
|---------------------|---------------|
|---------------------|---------------|

Log SQL statements to stdout. Use the option to enable; normally this behavior is disabled. The option checks before attempting to log whether all the tables being restored have explicitly defined primary keys; queries on a table having only the hidden primary key implemented by NDB cannot be converted to valid SQL.

This option does not work with tables having BLOB columns.

<span id="page-51-2"></span>• [--progress-frequency](#page-51-2)=N

| Command-Line Format | progress-frequency=# |
|---------------------|----------------------|
| Type                | Numeric              |
| Default Value       | 0                    |
| Minimum Value       | 0                    |
| Maximum Value       | 65535                |

Print a status report each N seconds while the backup is in progress. 0 (the default) causes no status reports to be printed. The maximum is 65535.

<span id="page-51-0"></span>• [--promote-attributes](#page-51-0), -A

| Command-Line Format | promote-attributes |
|---------------------|--------------------|
|---------------------|--------------------|

[ndb\\_restore](#page-35-7) supports limited attribute promotion in much the same way that it is supported by MySQL replication; that is, data backed up from a column of a given type can generally be restored to a column using a "larger, similar" type. For example, data from a CHAR(20) column can be restored to a column declared as VARCHAR(20), VARCHAR(30), or CHAR(30); data from a MEDIUMINT column can be restored to a column of type INT or BIGINT. See Replication of Columns Having Different Data Types, for a table of type conversions currently supported by attribute promotion.

This option also makes it possible to restore a NOT NULL column as NULL.

Attribute promotion by [ndb\\_restore](#page-35-7) must be enabled explicitly, as follows:

- 1. Prepare the table to which the backup is to be restored. [ndb\\_restore](#page-35-7) cannot be used to recreate the table with a different definition from the original; this means that you must either create the table manually, or alter the columns which you wish to promote using ALTER TABLE after restoring the table metadata but before restoring the data.
- 2. Invoke [ndb\\_restore](#page-35-7) with the [--promote-attributes](#page-51-0) option (short form -A) when restoring the table data. Attribute promotion does not occur if this option is not used; instead, the restore operation fails with an error.

When converting between character data types and TEXT or BLOB, only conversions between character types (CHAR and VARCHAR) and binary types (BINARY and VARBINARY) can be performed at the same time. For example, you cannot promote an INT column to BIGINT while promoting a VARCHAR column to TEXT in the same invocation of [ndb\\_restore](#page-35-7).

Converting between TEXT columns using different character sets is not supported, and is expressly disallowed.

When performing conversions of character or binary types to TEXT or BLOB with [ndb\\_restore](#page-35-7), you 4222 may notice that it creates and uses one or more staging tables named table\_name\$STnode\_id.

These tables are not needed afterwards, and are normally deleted by [ndb\\_restore](#page-35-7) following a successful restoration.

<span id="page-52-0"></span>• [--rebuild-indexes](#page-52-0)

| Command-Line Format | rebuild-indexes |
|---------------------|-----------------|
|---------------------|-----------------|

Enable multithreaded rebuilding of the ordered indexes while restoring a native NDB backup. The number of threads used for building ordered indexes by [ndb\\_restore](#page-35-7) with this option is controlled by the BuildIndexThreads data node configuration parameter and the number of LDMs.

It is necessary to use this option only for the first run of [ndb\\_restore](#page-35-7); this causes all ordered indexes to be rebuilt without using --rebuild-indexes again when restoring subsequent nodes. You should use this option prior to inserting new rows into the database; otherwise, it is possible for a row to be inserted that later causes a unique constraint violation when trying to rebuild the indexes.

Building of ordered indices is parallelized with the number of LDMs by default. Offline index builds performed during node and system restarts can be made faster using the BuildIndexThreads data node configuration parameter; this parameter has no effect on dropping and rebuilding of indexes by [ndb\\_restore](#page-35-7), which is performed online.

Rebuilding of unique indexes uses disk write bandwidth for redo logging and local checkpointing. An insufficient amount of this bandwidth can lead to redo buffer overload or log overload errors. In such cases you can run [ndb\\_restore](#page-35-7) --rebuild-indexes again; the process resumes at the point where the error occurred. You can also do this when you have encountered temporary errors. You can repeat execution of [ndb\\_restore](#page-35-7) --rebuild-indexes indefinitely; you may be able to stop such errors by reducing the value of [--parallelism](#page-49-0). If the problem is insufficient space, you can increase the size of the redo log (FragmentLogFileSize node configuration parameter), or you can increase the speed at which LCPs are performed (MaxDiskWriteSpeed and related parameters), in order to free space more quickly.

<span id="page-52-1"></span>• [--remap-column=](#page-52-1)db.tbl.col:fn:args

| Command-Line Format | remap-column=string |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | [none]              |

When used together with [--restore-data](#page-53-1), this option applies a function to the value of the indicated column. Values in the argument string are listed here:

- db: Database name, following any renames performed by [--rewrite-database](#page-54-0).
- tbl: Table name.
- col: Name of the column to be updated. This column must be of type INT or BIGINT. The column can also be but is not required to be UNSIGNED.
- fn: Function name; currently, the only supported name is offset.
- args: Arguments supplied to the function. Currently, only a single argument, the size of the offset to be added by the offset function, is supported. Negative values are supported. The size of the argument cannot exceed that of the signed variant of the column's type; for example, if col is an INT column, then the allowed range of the argument passed to the offset function is -2147483648 to 2147483647 (see Section 13.1.2, "Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT").

If applying the offset value to the column would cause an overflow or underflow, the restore operation fails. This could happen, for example, if the column is a BIGINT, and the option

attempts to apply an offset value of 8 on a row in which the column value is 4294967291, since 4294967291 + 8 = 4294967299 > 4294967295.

This option can be useful when you wish to merge data stored in multiple source instances of NDB Cluster (all using the same schema) into a single destination NDB Cluster, using NDB native backup (see [Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup"](#page-151-1)) and [ndb\\_restore](#page-35-7) to merge the data, where primary and unique key values are overlapping between source clusters, and it is necessary as part of the process to remap these values to ranges that do not overlap. It may also be necessary to preserve other relationships between tables. To fulfill such requirements, it is possible to use the option multiple times in the same invocation of [ndb\\_restore](#page-35-7) to remap columns of different tables, as shown here:

```
$> ndb_restore --restore-data --remap-column=hr.employee.id:offset:1000 \
 --remap-column=hr.manager.id:offset:1000 --remap-column=hr.firstaiders.id:offset:1000
```

(Other options not shown here may also be used.)

--remap-column can also be used to update multiple columns of the same table. Combinations of multiple tables and columns are possible. Different offset values can also be used for different columns of the same table, like this:

```
$> ndb_restore --restore-data --remap-column=hr.employee.salary:offset:10000 \
 --remap-column=hr.employee.hours:offset:-10
```

When source backups contain duplicate tables which should not be merged, you can handle this by using [--exclude-tables](#page-41-0), [--exclude-databases](#page-40-4), or by some other means in your application.

Information about the structure and other characteristics of tables to be merged can obtained using SHOW CREATE TABLE; the ndb\_desc tool; and MAX(), MIN(), LAST\_INSERT\_ID(), and other MySQL functions.

Replication of changes from merged to unmerged tables, or from unmerged to merged tables, in separate instances of NDB Cluster is not supported.

<span id="page-53-1"></span>• [--restore-data](#page-53-1), -r

| Command-Line Format | restore-data |
|---------------------|--------------|
|---------------------|--------------|

Output NDB table data and logs.

<span id="page-53-2"></span>• [--restore-epoch](#page-53-2), -e

| Command-Line Format | restore-epoch |
|---------------------|---------------|
|                     |               |

Add (or restore) epoch information to the cluster replication status table. This is useful for starting replication on an NDB Cluster replica. When this option is used, the row in the mysql.ndb\_apply\_status having 0 in the id column is updated if it already exists; such a row is inserted if it does not already exist. (See Section 25.7.9, "NDB Cluster Backups With NDB Cluster Replication".)

<span id="page-53-0"></span>• [--restore-meta](#page-53-0), -m

| Command-Line Format | restore-meta |
|---------------------|--------------|
|---------------------|--------------|

This option causes [ndb\\_restore](#page-35-7) to print NDB table metadata.

The first time you run the [ndb\\_restore](#page-35-7) restoration program, you also need to restore the metadata. In other words, you must re-create the database tables—this can be done by running it with the --

restore-meta (-m) option. Restoring the metadata need be done only on a single data node; this is sufficient to restore it to the entire cluster.

[ndb\\_restore](#page-35-7) uses the default number of partitions for the target cluster, unless the number of local data manager threads is also changed from what it was for data nodes in the original cluster.

When using this option, it is recommended that auto synchronization be disabled by setting ndb\_metadata\_check=OFF until [ndb\\_restore](#page-35-7) has completed restoring the metadata, after which it can it turned on again to synchronize objects newly created in the NDB dictionary.

![](_page_54_Picture_4.jpeg)

#### **Note**

The cluster should have an empty database when starting to restore a backup. (In other words, you should start the data nodes with --initial prior to performing the restore.)

<span id="page-54-1"></span>• [--restore-privilege-tables](#page-54-1)

| Command-Line Format | restore-privilege-tables |
|---------------------|--------------------------|
| Deprecated          | Yes                      |

No longer used.

<span id="page-54-0"></span>• [--rewrite-database](#page-54-0)=olddb,newdb

| Command-Line Format | rewrite-database=string |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | none                    |

This option makes it possible to restore to a database having a different name from that used in the backup. For example, if a backup is made of a database named products, you can restore the data it contains to a database named inventory, use this option as shown here (omitting any other options that might be required):

\$> ndb\_restore --rewrite-database=product,inventory

The option can be employed multiple times in a single invocation of [ndb\\_restore](#page-35-7). Thus it is possible to restore simultaneously from a database named db1 to a database named db2 and from a database named db3 to one named db4 using --rewrite-database=db1,db2 --rewritedatabase=db3,db4. Other [ndb\\_restore](#page-35-7) options may be used between multiple occurrences of --rewrite-database.

In the event of conflicts between multiple --rewrite-database options, the last --rewritedatabase option used, reading from left to right, is the one that takes effect. For example, if --rewrite-database=db1,db2 --rewrite-database=db1,db3 is used, only - rewrite-database=db1,db3 is honored, and --rewrite-database=db1,db2 is ignored. It is also possible to restore from multiple databases to a single database, so that --rewritedatabase=db1,db3 --rewrite-database=db2,db3 restores all tables and data from databases db1 and db2 into database db3.

![](_page_54_Picture_16.jpeg)

#### **Important**

When restoring from multiple backup databases into a single target database using --rewrite-database, no check is made for collisions between table or other object names, and the order in which rows are restored is not guaranteed. This means that it is possible in such cases for rows to be overwritten and updates to be lost.

<span id="page-55-1"></span>• [--skip-broken-objects](#page-55-1)

| Command-Line Format | skip-broken-objects |
|---------------------|---------------------|
|---------------------|---------------------|

This option causes [ndb\\_restore](#page-35-7) to ignore corrupt tables while reading a native NDB backup, and to continue restoring any remaining tables (that are not also corrupted). Currently, the --skipbroken-objects option works only in the case of missing blob parts tables.

<span id="page-55-2"></span>• [--skip-fk-checks](#page-55-2)

| Command-Line Format | skip-fk-checks  |
|---------------------|-----------------|
| Introduced          | 8.4.8-ndb-8.4.8 |

This option modifies the behavior of [ndb\\_restore](#page-35-7) [--rebuild-indexes](#page-52-0) so that, when foreign keys are re-enabled, the existing data in the table is not checked for consistency.

<span id="page-55-3"></span>• [--skip-table-check](#page-55-3), -s

| Command-Line Format | skip-table-check |
|---------------------|------------------|
|---------------------|------------------|

It is possible to restore data without restoring table metadata. By default when doing this, [ndb\\_restore](#page-35-7) fails with an error if a mismatch is found between the table data and the table schema; this option overrides that behavior.

Some of the restrictions on mismatches in column definitions when restoring data using [ndb\\_restore](#page-35-7) are relaxed; when one of these types of mismatches is encountered, [ndb\\_restore](#page-35-7) does not stop with an error as it did previously, but rather accepts the data and inserts it into the target table while issuing a warning to the user that this is being done. This behavior occurs whether or not either of the options --skip-table-check or [--promote-attributes](#page-51-0) is in use. These differences in column definitions are of the following types:

- Different COLUMN\_FORMAT settings (FIXED, DYNAMIC, DEFAULT)
- Different STORAGE settings (MEMORY, DISK)
- Different default values
- Different distribution key settings
- <span id="page-55-4"></span>• [--skip-unknown-objects](#page-55-4)

| Command-Line Format | skip-unknown-objects |
|---------------------|----------------------|
|---------------------|----------------------|

This option causes [ndb\\_restore](#page-35-7) to ignore any schema objects it does not recognize while reading a native NDB backup. This can be used for restoring a backup made from a cluster running (for example) NDB 7.6 to a cluster running NDB Cluster 7.5.

<span id="page-55-0"></span>• [--slice-id](#page-55-0)=#

| Command-Line Format | slice-id=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |

| Maximum Value | 1023 |  |
|---------------|------|--|
|---------------|------|--|

When restoring by slices, this is the ID of the slice to restore. This option is always used together with [--num-slices](#page-48-0), and its value must be always less than that of --num-slices.

For more information, see the description of the [--num-slices](#page-48-0) elsewhere in this section.

<span id="page-56-0"></span>• [--tab](#page-56-0)=dir\_name, -T dir\_name

| Command-Line Format | tab=path       |
|---------------------|----------------|
| Type                | Directory name |

Causes [--print-data](#page-50-0) to create dump files, one per table, each named tbl\_name.txt. It requires as its argument the path to the directory where the files should be saved; use . for the current directory.

• --timestamp-printouts

| Command-Line Format | timestamp-printouts{=true false} |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | true                             |

Causes info, error, and debug log messages to be prefixed with timestamps.

This option is enabled by default. Disable it with --timestamp-printouts=false.

<span id="page-56-1"></span>• [--usage](#page-56-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-43-4).

<span id="page-56-2"></span>• [--verbose](#page-56-2)=#

| Command-Line Format | verbose=# |
|---------------------|-----------|
| Type                | Numeric   |
| Default Value       | 1         |
| Minimum Value       | 0         |
| Maximum Value       | 255       |

Sets the level for the verbosity of the output. The minimum is 0; the maximum is 255. The default value is 1.

<span id="page-56-3"></span>• [--version](#page-56-3)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

<span id="page-57-0"></span>• [--with-apply-status](#page-57-0)

| Command-Line Format | with-apply-status |
|---------------------|-------------------|
|                     |                   |

Restore all rows from the backup's ndb\_apply\_status table (except for the row having server\_id = 0, which is generated using [--restore-epoch](#page-53-2)). This option requires that [-](#page-53-1) [restore-data](#page-53-1) also be used.

If the ndb\_apply\_status table from the backup already contains a row with server\_id = 0, [ndb\\_restore](#page-35-7) --with-apply-status deletes it. For this reason, we recommend that you use [ndb\\_restore](#page-35-7) --restore-epoch after invoking [ndb\\_restore](#page-35-7) with the --with-applystatus option. You can also use --restore-epoch concurrently with the last of any invocations of [ndb\\_restore](#page-35-7) --with-apply-status used to restore the cluster.

For more information, see ndb\_apply\_status Table.

Typical options for this utility are shown here:

```
ndb_restore [-c connection_string] -n node_id -b backup_id \
 [-m] -r --backup-path=/path/to/backup/files
```

Normally, when restoring from an NDB Cluster backup, [ndb\\_restore](#page-35-7) requires at a minimum the [-](#page-47-4) [nodeid](#page-47-4) (short form: -n), [--backupid](#page-38-2) (short form: -b), and [--backup-path](#page-37-1) options.

The -c option is used to specify a connection string which tells ndb\_restore where to locate the cluster management server (see Section 25.4.3.3, "NDB Cluster Connection Strings"). If this option is not used, then [ndb\\_restore](#page-35-7) attempts to connect to a management server on localhost:1186. This utility acts as a cluster API node, and so requires a free connection "slot" to connect to the cluster management server. This means that there must be at least one [api] or [mysqld] section that can be used by it in the cluster config.ini file. It is a good idea to keep at least one empty [api] or [mysqld] section in config.ini that is not being used for a MySQL server or other application for this reason (see Section 25.4.3.7, "Defining SQL and Other API Nodes in an NDB Cluster").

[ndb\\_restore](#page-35-7) can decrypt an encrypted backup using [--decrypt](#page-39-0) and [--backup-password](#page-38-0). Both options must be specified to perform decryption. See the documentation for the [START BACKUP](#page-151-1) management client command for information on creating encrypted backups.

You can verify that [ndb\\_restore](#page-35-7) is connected to the cluster by using the [SHOW](#page-102-0) command in the ndb\_mgm management client. You can also accomplish this from a system shell, as shown here:

```
$> ndb_mgm -e "SHOW"
```

#### **Error reporting.**

[ndb\\_restore](#page-35-7) reports both temporary and permanent errors. In the case of temporary errors, it may able to recover from them, and reports Restore successful, but encountered temporary error, please look at configuration in such cases.

![](_page_57_Picture_15.jpeg)

#### **Important**

After using [ndb\\_restore](#page-35-7) to initialize an NDB Cluster for use in circular replication, binary logs on the SQL node acting as the replica are not automatically created, and you must cause them to be created manually. To cause the binary logs to be created, issue a SHOW TABLES statement on that SQL node before running START REPLICA. This is a known issue in NDB Cluster.

# <span id="page-57-1"></span>**25.5.24 ndb\_secretsfile\_reader — Obtain Key Information from an Encrypted NDB Data File**

[ndb\\_secretsfile\\_reader](#page-57-1) gets the encryption key from an NDB encryption secrets file, given the password.

### **Usage**

ndb\_secretsfile\_reader options file

The options must include one of [--filesystem-password](#page-58-0) or [--filesystem-password-from](#page-58-1)[stdin](#page-58-1), and the encryption password must be supplied, as shown here:

> **ndb\_secretsfile\_reader --filesystem-password=54kl14 ndb\_5\_fs/D1/NDBCNTR/S0.sysfile** ndb\_secretsfile\_reader: [Warning] Using a password on the command line interface can be insecure. cac256e18b2ddf6b5ef82d99a72f18e864b78453cc7fa40bfaf0c40b91122d18

These and other options that can be used with [ndb\\_secretsfile\\_reader](#page-57-1) are shown in the following table. Additional descriptions follow the table.

<span id="page-58-2"></span>• [--defaults-extra-file](#page-58-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-58-3"></span>• [--defaults-file](#page-58-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-58-4"></span>• [--defaults-group-suffix](#page-58-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-58-0"></span>• [--filesystem-password](#page-58-0)

| Command-Line Format | filesystem-password=password |
|---------------------|------------------------------|

Pass the filesystem encryption and decryption password to [ndb\\_secretsfile\\_reader](#page-57-1) using stdin, tty, or the my.cnf file.

<span id="page-58-1"></span>• [--filesystem-password-from-stdin](#page-58-1)

| Command-Line Format | filesystem-password-from |
|---------------------|--------------------------|
|                     | stdin={TRUE FALSE}       |

Pass the filesystem encryption and decryption password to [ndb\\_secretsfile\\_reader](#page-57-1) from stdin (only).

<span id="page-58-5"></span>• [--help](#page-58-5)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

### <span id="page-59-0"></span>• [--login-path](#page-59-0)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-59-1"></span>• [--no-login-paths](#page-59-1)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-59-2"></span>• [--no-defaults](#page-59-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-59-3"></span>• [--print-defaults](#page-59-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-59-4"></span>• [--usage](#page-59-4)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-59-5"></span>• [--version](#page-59-5)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-59-6"></span>**25.5.25 ndb\_select\_all — Print Rows from an NDB Table**

[ndb\\_select\\_all](#page-59-6) prints all rows from an NDB table to stdout.

## **Usage**

```
ndb_select_all -c connection_string tbl_name -d db_name [> file_name]
```

Options that can be used with [ndb\\_select\\_all](#page-59-6) are shown in the following table. Additional descriptions follow the table.

<span id="page-59-7"></span>• [--character-sets-dir](#page-59-7)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-59-8"></span>• [--connect-retries](#page-59-8)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
|---------------------|-------------------|

| Type          | Integer |
|---------------|---------|
| Default Value | 12      |
| Minimum Value | 0       |
| Maximum Value | 12      |

Number of times to retry connection before giving up.

#### <span id="page-60-0"></span>• [--connect-retry-delay](#page-60-0)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-60-1"></span>• [--connect-string](#page-60-1)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-62-0).

#### <span id="page-60-2"></span>• [--core-file](#page-60-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-60-3"></span>• [--database=](#page-60-3)dbname, -d dbname

Name of the database in which the table is found. The default value is TEST\_DB.

<span id="page-60-4"></span>• [--descending](#page-60-4), -z

Sorts the output in descending order. This option can be used only in conjunction with the -o ([-](#page-63-0) [order](#page-63-0)) option.

### <span id="page-60-5"></span>• [--defaults-extra-file](#page-60-5)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

#### <span id="page-60-6"></span>• [--defaults-file](#page-60-6)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

### <span id="page-61-0"></span>• [--defaults-group-suffix](#page-61-0)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-61-1"></span>• [--delimiter=](#page-61-1)character, -D character

Causes the character to be used as a column delimiter. Only table data columns are separated by this delimiter.

The default delimiter is the tab character.

<span id="page-61-2"></span>• [--disk](#page-61-2)

Adds a disk reference column to the output. The column is nonempty only for Disk Data tables having nonindexed columns.

<span id="page-61-3"></span>• [--gci](#page-61-3)

Adds a GCI column to the output showing the global checkpoint at which each row was last updated. See Section 25.2, "NDB Cluster Overview", and [Section 25.6.3.2, "NDB Cluster Log Events"](#page-127-0), for more information about checkpoints.

<span id="page-61-4"></span>• [--gci64](#page-61-4)

Adds a ROW\$GCI64 column to the output showing the global checkpoint at which each row was last updated, as well as the number of the epoch in which this update occurred.

<span id="page-61-5"></span>• [--help](#page-61-5)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-61-6"></span>• --lock=[lock\\_type](#page-61-6), -l lock\_type

Employs a lock when reading the table. Possible values for lock\_type are:

- 0: Read lock
- 1: Read lock with hold
- 2: Exclusive read lock

There is no default value for this option.

<span id="page-61-7"></span>• [--login-path](#page-61-7)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-61-8"></span>• [--no-login-paths](#page-61-8)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|                     |                |

Skips reading options from the login path file.

<span id="page-62-1"></span>• [--header=FALSE](#page-62-1)

Excludes column headers from the output.

<span id="page-62-2"></span>• [--nodata](#page-62-2)

Causes any table data to be omitted.

<span id="page-62-0"></span>• [--ndb-connectstring](#page-62-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-62-3"></span>• [--ndb-mgm-tls](#page-62-3)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-62-4"></span>• [--ndb-mgmd-host](#page-62-4)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-62-0).

<span id="page-62-5"></span>• [--ndb-nodeid](#page-62-5)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-62-0).

<span id="page-62-6"></span>• [--ndb-optimized-node-selection](#page-62-6)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

<span id="page-63-1"></span>• [--ndb-tls-search-path](#page-63-1)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-63-2"></span>• [--no-defaults](#page-63-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-63-0"></span>• --order=[index\\_name](#page-63-0), -o index\_name

Orders the output according to the index named index\_name.

![](_page_63_Picture_11.jpeg)

#### **Note**

This is the name of an index, not of a column; the index must have been explicitly named when created.

<span id="page-63-3"></span>• [parallelism=](#page-63-3)#, -p #

Specifies the degree of parallelism.

<span id="page-63-4"></span>• [--print-defaults](#page-63-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-63-5"></span>• [--rowid](#page-63-5)

Adds a ROWID column providing information about the fragments in which rows are stored.

<span id="page-63-6"></span>• [--tupscan](#page-63-6), -t

Scan the table in the order of the tuples.

• [--usage](#page-63-7)

<span id="page-63-7"></span>

| 4234 | Command-Line Format | usage |
|------|---------------------|-------|

Display help text and exit; same as [--help](#page-61-5).

<span id="page-64-0"></span>• [--useHexFormat](#page-64-0) -x

Causes all numeric values to be displayed in hexadecimal format. This does not affect the output of numerals contained in strings or datetime values.

<span id="page-64-1"></span>• [--version](#page-64-1)

```
Command-Line Format --version
```

Display version information and exit.

### **Sample Output**

Output from a MySQL SELECT statement:

```
mysql> SELECT * FROM ctest1.fish;
+----+-----------+
| id | name |
+----+-----------+
| 3 | shark |
| 6 | puffer |
| 2 | tuna |
| 4 | manta ray |
| 5 | grouper |
| 1 | guppy |
+----+-----------+
6 rows in set (0.04 sec)
```

Output from the equivalent invocation of [ndb\\_select\\_all](#page-59-6):

```
$> ./ndb_select_all -c localhost fish -d ctest1
id name
3 [shark]
6 [puffer]
2 [tuna]
4 [manta ray]
5 [grouper]
1 [guppy]
6 rows returned
```

All string values are enclosed by square brackets ([...]) in the output of [ndb\\_select\\_all](#page-59-6). For another example, consider the table created and populated as shown here:

```
CREATE TABLE dogs (
 id INT(11) NOT NULL AUTO_INCREMENT,
 name VARCHAR(25) NOT NULL,
 breed VARCHAR(50) NOT NULL,
 PRIMARY KEY pk (id),
 KEY ix (name)
)
TABLESPACE ts STORAGE DISK
ENGINE=NDBCLUSTER;
INSERT INTO dogs VALUES
 ('', 'Lassie', 'collie'),
 ('', 'Scooby-Doo', 'Great Dane'),
 ('', 'Rin-Tin-Tin', 'Alsatian'),
 ('', 'Rosscoe', 'Mutt');
```

This demonstrates the use of several additional [ndb\\_select\\_all](#page-59-6) options:

```
$> ./ndb_select_all -d ctest1 dogs -o ix -z --gci --disk
GCI id name breed DISK_REF
834461 2 [Scooby-Doo] [Great Dane] [ m_file_no: 0 m_page: 98 m_page_idx: 0 ]
834878 4 [Rosscoe] [Mutt] [ m_file_no: 0 m_page: 98 m_page_idx: 16 ]
834463 3 [Rin-Tin-Tin] [Alsatian] [ m_file_no: 0 m_page: 34 m_page_idx: 0 ]
835657 1 [Lassie] [Collie] [ m_file_no: 0 m_page: 66 m_page_idx: 0 ]
4 rows returned
```

# <span id="page-65-0"></span>**25.5.26 ndb\_select\_count — Print Row Counts for NDB Tables**

[ndb\\_select\\_count](#page-65-0) prints the number of rows in one or more NDB tables. With a single table, the result is equivalent to that obtained by using the MySQL statement SELECT COUNT(\*) FROM tbl\_name.

### **Usage**

ndb\_select\_count [-c connection\_string] -ddb\_name tbl\_name[, tbl\_name2[, ...]]

Options that can be used with [ndb\\_select\\_count](#page-65-0) are shown in the following table. Additional descriptions follow the table.

<span id="page-65-1"></span>• [--character-sets-dir](#page-65-1)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-65-2"></span>• [--connect-retries](#page-65-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-65-3"></span>• [--connect-retry-delay](#page-65-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-65-4"></span>• [--connect-string](#page-65-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-66-0).

<span id="page-65-5"></span>• [--core-file](#page-65-5)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-65-6"></span>• [--defaults-file](#page-65-6)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read default options from given file only.

<span id="page-66-1"></span>• [--defaults-extra-file](#page-66-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-66-2"></span>• [--defaults-group-suffix](#page-66-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-66-3"></span>• [--login-path](#page-66-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-66-4"></span>• [--no-login-paths](#page-66-4)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-66-5"></span>• [--help](#page-66-5)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-66-0"></span>• [--ndb-connectstring](#page-66-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-66-6"></span>• [--ndb-mgm-tls](#page-66-6)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |

| Default Value | relaxed |
|---------------|---------|
| Valid Values  | relaxed |
|               | strict  |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

#### <span id="page-67-0"></span>• [--ndb-mgmd-host](#page-67-0)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-66-0).

#### <span id="page-67-1"></span>• [--ndb-nodeid](#page-67-1)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-66-0).

#### <span id="page-67-2"></span>• [--ndb-optimized-node-selection](#page-67-2)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-67-3"></span>• [--ndb-tls-search-path](#page-67-3)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-67-4"></span>• [--no-defaults](#page-67-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-68-0"></span>• [--print-defaults](#page-68-0)

Print program argument list and exit.

<span id="page-68-1"></span>• [--usage](#page-68-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-66-5).

<span id="page-68-2"></span>• [--version](#page-68-2)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

You can obtain row counts from multiple tables in the same database by listing the table names separated by spaces when invoking this command, as shown under **Sample Output**.

### **Sample Output**

```
$> ./ndb_select_count -c localhost -d ctest1 fish dogs
6 records in table fish
4 records in table dogs
```

## <span id="page-68-3"></span>**25.5.27 ndb\_show\_tables — Display List of NDB Tables**

[ndb\\_show\\_tables](#page-68-3) displays a list of all NDB database objects in the cluster. By default, this includes not only both user-created tables and NDB system tables, but NDB-specific indexes, internal triggers, and NDB Cluster Disk Data objects as well.

Options that can be used with [ndb\\_show\\_tables](#page-68-3) are shown in the following table. Additional descriptions follow the table.

### <span id="page-68-4"></span>**Usage**

ndb\_show\_tables [-c connection\_string]

• [--character-sets-dir](#page-68-4)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-68-5"></span>• [--connect-retries](#page-68-5)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

#### <span id="page-69-0"></span>• [--connect-retry-delay](#page-69-0)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-69-1"></span>• [--connect-string](#page-69-1)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-70-0).

#### <span id="page-69-2"></span>• [--core-file](#page-69-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

#### <span id="page-69-3"></span>• [--database](#page-69-3), -d

Specifies the name of the database in which the desired table is found. If this option is given, the name of a table must follow the database name.

If this option has not been specified, and no tables are found in the TEST\_DB database, [ndb\\_show\\_tables](#page-68-3) issues a warning.

### <span id="page-69-4"></span>• [--defaults-extra-file](#page-69-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

### <span id="page-69-5"></span>• [--defaults-file](#page-69-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

#### <span id="page-69-6"></span>• [--defaults-group-suffix](#page-69-6)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-70-1"></span>• [--help](#page-70-1)

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display help text and exit.

<span id="page-70-2"></span>• [--login-path](#page-70-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-70-3"></span>• [--no-login-paths](#page-70-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-70-4"></span>• [--loops](#page-70-4), -l

Specifies the number of times the utility should execute. This is 1 when this option is not specified, but if you do use the option, you must supply an integer argument for it.

<span id="page-70-0"></span>• [--ndb-connectstring](#page-70-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-70-5"></span>• [--ndb-mgm-tls](#page-70-5)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |
| Default Value       | relaxed           |
| Valid Values        | relaxed           |
|                     | strict            |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

<span id="page-70-6"></span>• [--ndb-mgmd-host](#page-70-6)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-70-0).

<span id="page-70-7"></span>• [--ndb-nodeid](#page-70-7)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-70-0).

<span id="page-71-0"></span>• [--ndb-optimized-node-selection](#page-71-0)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-71-1"></span>• [--ndb-tls-search-path](#page-71-1)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

<span id="page-71-2"></span>• [--no-defaults](#page-71-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-71-3"></span>• [--parsable](#page-71-3), -p

Using this option causes the output to be in a format suitable for use with LOAD DATA.

<span id="page-71-4"></span>• [--print-defaults](#page-71-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-71-5"></span>• [--show-temp-status](#page-71-5)

If specified, this causes temporary tables to be displayed.

<span id="page-71-6"></span>• [--type](#page-71-6), -t

Can be used to restrict the output to one type of object, specified by an integer type code as shown here:

- 1: System table
- 2: User-created table
- 3: Unique hash index

Any other value causes all NDB database objects to be listed (the default).

<span id="page-72-0"></span>• [--unqualified](#page-72-0), -u

If specified, this causes unqualified object names to be displayed.

<span id="page-72-1"></span>• [--usage](#page-72-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-70-1).

<span id="page-72-2"></span>• [--version](#page-72-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

![](_page_72_Picture_13.jpeg)

#### **Note**

Only user-created NDB Cluster tables may be accessed from MySQL; system tables such as SYSTAB\_0 are not visible to mysqld. However, you can examine the contents of system tables using NDB API applications such as [ndb\\_select\\_all](#page-59-6) (see [Section 25.5.25, "ndb\\_select\\_all — Print Rows from an](#page-59-6) [NDB Table"](#page-59-6)).

# <span id="page-72-3"></span>**25.5.28 ndb\_sign\_keys — Create, Sign, and Manage TLS Keys and Certificates for NDB Cluster**

Management of TLS keys and certificates in implemented in NDB Cluster as the executable utility program [ndb\\_sign\\_keys](#page-72-3), which can normally be found in the MySQL bin directory. The program performs such functions as creating, signing, and retiring keys and certificates, and normally works as follows:

- 1. [ndb\\_sign\\_keys](#page-72-3) connects to ndb\_mgmd and fetches the cluster' configuration.
- 2. For each cluster node that is configured to run on the local machine, [ndb\\_sign\\_keys](#page-72-3) finds the node' private key and sign it, creating an active node certificate.

Some additional tasks that can be performed by [ndb\\_sign\\_keys](#page-72-3) are listed here:

- Obtaining configuration information from a config.ini file rather than a running ndb\_mgmd
- Creating the cluster' certificate authority (CA) if it does not yet exist
- Creating private keys
- Saving keys and certificates as pending rather than active
- Signing the key for a single node as specified using command-line options described later in this section
- Requesting a CA located on a remote host to sign a local key

Options that can be used with [ndb\\_sign\\_keys](#page-72-3) are shown in the following table. Additional descriptions follow the table.

#### <span id="page-73-0"></span>• [--bind-host](#page-73-0)

| Command-Line Format | bind-host=host |
|---------------------|----------------|
| Type                | String         |
| Default Value       | mgmd, api      |

Create a certificate bound to a hostname list of node types that should have certificate hostname bindings, from the set (mgmd,db,api).

#### <span id="page-73-1"></span>• [--bound-hostname](#page-73-1)

| Command-Line Format | bound-hostname=hostname |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

Create a certificate bound to the hostname passed to this option.

#### <span id="page-73-2"></span>• [--CA-cert](#page-73-2)

| Command-Line Format | CA-cert=name     |
|---------------------|------------------|
| Type                | File name        |
| Default Value       | NDB-Cluster-cert |

Use the name passed to this option for the CA Certificate file.

### <span id="page-73-3"></span>• [--CA-days](#page-73-3)

| Command-Line Format | CA-days=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 1461       |
| Minimum Value       | -1         |
| Maximum Value       | 2147483647 |

Set the lifetime of the certificate to this many days. The default is equivalent to 4 years plus 1 day. -1 means the certificate never expires.

This option was added in NDB 8.4.1.

#### <span id="page-73-4"></span>• [--CA-key](#page-73-4)

| Command-Line Format | CA-key=name             |
|---------------------|-------------------------|
| Type                | File name               |
| Default Value       | NDB-Cluster-private-key |

Use the name passed to this option for the CA private key file.

### <span id="page-73-5"></span>• [--CA-ordinal](#page-73-5)

|  | Command-Line Format | CA-ordinal=name |
|--|---------------------|-----------------|
|  | Type                | String          |
|  | Default Value       | [none]          |
|  | Valid Values        | First           |

Second

Set the ordinal CA name; defaults to First for [--create-CA](#page-75-0) and Second for [--rotate-CA](#page-79-0). The Common Name in the CA certificate is "MySQL NDB Cluster ordinal Certificate", where ordinal is the ordinal name passed to this option.

#### <span id="page-74-0"></span>• [--CA-search-path](#page-74-0)

| Command-Line Format | CA-search-path=name |
|---------------------|---------------------|
| Type                | File name           |
| Default Value       | [none]              |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path is limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \$HOMEPATH\ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This default can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-74-1"></span>• [--CA-tool](#page-74-1)

| Command-Line Format | CA-tool=name |
|---------------------|--------------|
| Type                | File name    |
| Default Value       | [none]       |

Designate an executable helper tool, including the path.

#### <span id="page-74-2"></span>• [--check](#page-74-2)

| Command-Line Format | check |
|---------------------|-------|
|---------------------|-------|

Check certificate expiry dates.

#### <span id="page-74-3"></span>• [--config-file](#page-74-3)

| Command-Line Format | config-file=file |
|---------------------|------------------|
| Disabled by         | no-config        |
| Type                | File name        |
| Default Value       | [none]           |

Supply the path to the cluster configuration file (usually config.ini).

#### <span id="page-74-4"></span>• [--connect-retries](#page-74-4)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | -1                |

| Maximum Value | 12 |
|---------------|----|
|---------------|----|

Set the number of times that [ndb\\_sign\\_keys](#page-72-3) attempts to connect to the cluster. If you use -1, the program keeps trying to connect until it succeeds or is forced to stop.

#### <span id="page-75-1"></span>• [--connect-retry-delay](#page-75-1)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Set the number of seconds after a failed connection attempt which [ndb\\_sign\\_keys](#page-72-3) waits before trying again, up to the number of times determined by [--connect-retries](#page-74-4).

#### <span id="page-75-0"></span>• [--create-CA](#page-75-0)

Create the CA key and certificate.

#### <span id="page-75-2"></span>• [--create-key](#page-75-2)

| Command-Line Format | create-key |
|---------------------|------------|
|---------------------|------------|

Create or replace private keys.

#### <span id="page-75-3"></span>• [--curve](#page-75-3)

| Command-Line Format | curve=name |
|---------------------|------------|
| Type                | String     |
| Default Value       | P-256      |

Use the named curve for encrypting node keys.

### <span id="page-75-4"></span>• [--defaults-extra-file](#page-75-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read this option file after the global files are read.

### <span id="page-75-5"></span>• [--defaults-file](#page-75-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read this option file only.

#### <span id="page-75-6"></span>• [--defaults-group-suffix](#page-75-6)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
|---------------------|------------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read not only the usual option groups, but also groups with the usual names and a suffix of string.

#### <span id="page-76-0"></span>• [--duration](#page-76-0)

| Command-Line Format | duration=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | -500000    |
| Maximum Value       | 0          |
| Unit                | seconds    |

Set the lifetime of certificates or signing requests, in seconds.

#### <span id="page-76-1"></span>• [--help](#page-76-1)

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Print help text and exit.

#### <span id="page-76-2"></span>• [--keys-to-dir](#page-76-2)

| Command-Line Format | keys-to-dir=dirname |
|---------------------|---------------------|
| Type                | Directory name      |
| Default Value       | [none]              |

Specify output directory for private keys (only); for this purpose, it overrides any value set for [--to](#page-80-0)[dir](#page-80-0).

#### <span id="page-76-3"></span>• [--login-path](#page-76-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read this path from the login file.

#### <span id="page-76-4"></span>• [--ndb-connectstring](#page-76-4)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set the connection string to use for connecting to ndb\_mgmd, using the syntax [nodeid=id;] [host=]hostname[:port]. If this option is set, it overrides the value set for NDB\_CONNECTSTRING (if any), as well as any value set in a my.cnf. file.

#### <span id="page-76-5"></span>• [--ndb-mgm-tls](#page-76-5)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |

| Default Value | relaxed |
|---------------|---------|
| Valid Values  | relaxed |
|               | strict  |

Sets the level of TLS support required for the ndb\_mgm client; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

#### <span id="page-77-0"></span>• [--ndb-tls-search-path](#page-77-0)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories containing TLS keys and certificates.

For syntax, see the description of the [--CA-search-path](#page-74-0) option.

#### <span id="page-77-1"></span>• [--no-config](#page-77-1)

| Command-Line Format | no-config |
|---------------------|-----------|
|---------------------|-----------|

Do not obtain the cluster configuration; create a single certificate based on the options supplied (including defaults for those not specified).

#### <span id="page-77-2"></span>• [--no-defaults](#page-77-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than the login file.

#### <span id="page-77-3"></span>• [--no-login-paths](#page-77-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Do not read login paths from the login path file.

#### <span id="page-77-4"></span>• [--passphrase](#page-77-4)

| Command-Line Format | passphrase=phrase |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | [none]            |

Specify a CA key pass phrase.

#### <span id="page-77-5"></span>• [--node-id](#page-77-5)

| Command-Line Format | node-id=# |
|---------------------|-----------|
| Type                | Integer   |
| Default Value       | 0         |
| Minimum Value       | 0         |
| Maximum Value       | 255       |

Create or sign a key for the node having the specified node ID.

### <span id="page-78-0"></span>• [--node-type](#page-78-0)

| Command-Line Format | node-type=set |
|---------------------|---------------|
| Type                | Set           |
| Default Value       | mgmd,db,api   |

Create or sign keys for the specified type or types from the set (mgmd,db,api).

<span id="page-78-1"></span>• [--pending](#page-78-1)

| Command-Line Format | pending |
|---------------------|---------|
|---------------------|---------|

Save keys and certificates as pending, rather than active.

<span id="page-78-2"></span>• [--print-defaults](#page-78-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program argument list, then exit.

<span id="page-78-3"></span>• [--promote](#page-78-3)

| Command-Line Format | promote |
|---------------------|---------|
|---------------------|---------|

Promote pending files to active, then exit.

<span id="page-78-4"></span>• [--remote-CA-host](#page-78-4)

| Command-Line Format | remote-CA-host=hostname |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

Specify the address or hostname of a remote CA host.

<span id="page-78-5"></span>• [--remote-exec-path](#page-78-5)

| Command-Line Format | remote-exec-path |
|---------------------|------------------|
| Type                | Path name        |
| Default Value       | [none]           |

Provide the full path to an executable on the remote CA host specified with [--remote-CA-host](#page-78-4).

<span id="page-78-6"></span>• [--remote-openssl](#page-78-6)

| Command-Line Format | remote-openssl |
|---------------------|----------------|

Use OpenSSL for signing of keys on the remote CA host specified with [--remote-CA-host](#page-78-4).

<span id="page-78-7"></span>• [--replace-by](#page-78-7)

| Command-Line Format | replace-by=#    |
|---------------------|-----------------|
| Type                | 4249<br>Integer |
| Default Value       | -10             |
| Minimum Value       | -128            |

| Maximum Value | 127 |
|---------------|-----|
|---------------|-----|

Suggest a certificate replacement date for periodic checks, as a number of days after the CA expiration date. Use a negative number to indicate days before expiration.

<span id="page-79-0"></span>• [--rotate-CA](#page-79-0)

| Command-Line Format | rotate-CA |
|---------------------|-----------|
|---------------------|-----------|

Replace an older CA with a newer one. The new CA can be created using OpenSSL, or you can allow [ndb\\_sign\\_keys](#page-72-3) to create the new one, in which case the new CA is created with an intermediate CA certificate, signed by the old CA.

<span id="page-79-1"></span>• [--schedule](#page-79-1)

| Command-Line Format | schedule=list       |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | 120,10,130,10,150,0 |

Assign a schedule of expiration dates to certificates. The schedule is defined as a comma-delimited list of six integers, in the format shown here:

```
api_valid,api_extra,dn_valid,dn_extra,mgm_valid,mgm_extra
```

These values are defined as follows:

• api\_valid: A fixed number of days of validity for client certificates.

api\_extra: A number of extra days for client certificates.

dn\_valid: A fixed number of days of validity for client certificates for data node certificates.

dn\_extra: A number of extra days for data node certificates.

mgm\_valid: A fixed number of days of validity for management server certificates.

mgm\_extra: A number of extra days for management server certificates.

In other words, for each node type (API node, data node, management node), certificates are created with a lifetime equal to a whole fixed number of days, plus some random amount of time less than or equal to the number of extra days. The default schedule is shown here:

```
--schedule=120,10,130,10,150,0
```

Following the default schedule, client certificates begin expiring on the 120th day, and expire at random intervals over the next 10 days; data node certificates expire at random times between the 130th and 140th days; and management node certificates expire on the 150th day (with no random interval following).

<span id="page-79-2"></span>• [--sign](#page-79-2)

| Command-Line Format | sign      |
|---------------------|-----------|
| Disabled by         | skip-sign |

Create signed certificates; enabled by default. Use [--skip-sign](#page-79-3) to create certificate signing requests instead.

<span id="page-79-3"></span>• [--skip-sign](#page-79-3)

| Command-Line Format | skip-sign |
|---------------------|-----------|

Create certificate signing requests instead of signed certificates.

<span id="page-80-1"></span>• [--stdio](#page-80-1)

| Command-Line Format | stdio |
|---------------------|-------|
|---------------------|-------|

Read certificate signing requests from stdin, and write X.509 to stdout.

<span id="page-80-0"></span>• [--to-dir](#page-80-0)

| Command-Line Format | to-dir=dirname |
|---------------------|----------------|
| Type                | Directory name |
| Default Value       | [none]         |

Specify the output directory for created files. For private key files, this can be overriden using [-](#page-76-2) [keys-to-dir](#page-76-2).

<span id="page-80-2"></span>• [--usage](#page-80-2)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Print help text, then exit (alias for [--help](#page-76-1)).

<span id="page-80-3"></span>• [--version](#page-80-3)

| Command-Line Format | version |
|---------------------|---------|
|                     |         |

Print version information, then exit.

## <span id="page-80-4"></span>**25.5.29 ndb\_size.pl — NDBCLUSTER Size Requirement Estimator**

This is a Perl script that can be used to estimate the amount of space that would be required by a MySQL database if it were converted to use the NDBCLUSTER storage engine. Unlike the other utilities discussed in this section, it does not require access to an NDB Cluster (in fact, there is no reason for it to do so). However, it does need to access the MySQL server on which the database to be tested resides.

![](_page_80_Picture_16.jpeg)

#### **Note**

[ndb\\_size.pl](#page-80-4) is deprecated, and no longer supported, in NDB 8.4.3 and later. You should expect it to be removed from a future version of the NDB Cluster distribution, and modify any dependent applications accordingly.

### **Requirements**

- A running MySQL server. The server instance does not have to provide support for NDB Cluster.
- A working installation of Perl.
- The DBI module, which can be obtained from CPAN if it is not already part of your Perl installation. (Many Linux and other operating system distributions provide their own packages for this library.)
- A MySQL user account having the necessary privileges. If you do not wish to use an existing account, then creating one using GRANT USAGE ON db\_name.\*—where db\_name is the name of the database to be examined—is sufficient for this purpose.

ndb\_size.pl can also be found in the MySQL sources in storage/ndb/tools.

Options that can be used with [ndb\\_size.pl](#page-80-4) are shown in the following table. Additional descriptions follow the table.

### **Usage**

```
perl ndb_size.pl [--database={db_name|ALL}] [--hostname=host[:port]] [--socket=socket] \
 [--user=user] [--password=password] \
 [--help|-h] [--format={html|text}] \
 [--loadqueries=file_name] [--savequeries=file_name]
```

By default, this utility attempts to analyze all databases on the server. You can specify a single database using the --database option; the default behavior can be made explicit by using ALL for the name of the database. You can also exclude one or more databases by using the --excludedbs option with a comma-separated list of the names of the databases to be skipped. Similarly, you can cause specific tables to be skipped by listing their names, separated by commas, following the optional --excludetables option. A host name can be specified using --hostname; the default is localhost. You can specify a port in addition to the host using host:port format for the value of - hostname. The default port number is 3306. If necessary, you can also specify a socket; the default is /var/lib/mysql.sock. A MySQL user name and password can be specified the corresponding options shown. It also possible to control the format of the output using the --format option; this can take either of the values html or text, with text being the default. An example of the text output is shown here:

```
$> ndb_size.pl --database=test --socket=/tmp/mysql.sock
ndb_size.pl report for database: 'test' (1 tables)
--------------------------------------------------
Connected to: DBI:mysql:host=localhost;mysql_socket=/tmp/mysql.sock
Including information for versions: 4.1, 5.0, 5.1
test.t1
-------
DataMemory for Columns (* means varsized DataMemory):
 Column Name Type Varsized Key 4.1 5.0 5.1
 HIDDEN_NDB_PKEY bigint PRI 8 8 8
 c2 varchar(50) Y 52 52 4*
 c1 int(11) 4 4 4
 -- -- --
Fixed Size Columns DM/Row 64 64 12
 Varsize Columns DM/Row 0 0 4
DataMemory for Indexes:
 Index Name Type 4.1 5.0 5.1
 PRIMARY BTREE 16 16 16
 -- -- --
 Total Index DM/Row 16 16 16
IndexMemory for Indexes:
 Index Name 4.1 5.0 5.1
 PRIMARY 33 16 16
 -- -- --
 Indexes IM/Row 33 16 16
Summary (for THIS table):
 4.1 5.0 5.1
 Fixed Overhead DM/Row 12 12 16
 NULL Bytes/Row 4 4 4
 DataMemory/Row 96 96 48
 (Includes overhead, bitmap and indexes)
 Varsize Overhead DM/Row 0 0 8
 Varsize NULL Bytes/Row 0 0 4
 Avg Varside DM/Row 0 0 16
 No. Rows 0 0 0
 Rows/32kb DM Page 340 340 680
Fixedsize DataMemory (KB) 0 0 0
Rows/32kb Varsize DM Page 0 0 2040
```

| Varsize DataMemory (KB)          | 0       | 0   | 0   |     |  |
|----------------------------------|---------|-----|-----|-----|--|
| Rows/8kb IM Page                 | 248     | 512 | 512 |     |  |
| IndexMemory (KB)                 | 0       | 0   | 0   |     |  |
| Parameter Minimum Requirements   |         |     |     |     |  |
|                                  |         |     |     |     |  |
| * indicates greater than default |         |     |     |     |  |
| Parameter                        | Default | 4.1 | 5.0 | 5.1 |  |
| DataMemory (KB)                  | 81920   | 0   | 0   | 0   |  |
| NoOfOrderedIndexes               | 128     | 1   | 1   | 1   |  |
| NoOfTables                       | 128     | 1   | 1   | 1   |  |
| IndexMemory (KB)                 | 18432   | 0   | 0   | 0   |  |
| NoOfUniqueHashIndexes            | 64      | 0   | 0   | 0   |  |
| NoOfAttributes                   | 1000    | 3   | 3   | 3   |  |
| NoOfTriggers                     | 768     | 5   | 5   | 5   |  |

For debugging purposes, the Perl arrays containing the queries run by this script can be read from the file specified using can be saved to a file using --savequeries; a file containing such arrays to be read during script execution can be specified using --loadqueries. Neither of these options has a default value.

To produce output in HTML format, use the --format option and redirect the output to a file, as shown here:

```
$> ndb_size.pl --database=test --socket=/tmp/mysql.sock --format=html > ndb_size.html
```

(Without the redirection, the output is sent to stdout.)

The output from this script includes the following information:

- Minimum values for the DataMemory, IndexMemory, MaxNoOfTables, MaxNoOfAttributes, MaxNoOfOrderedIndexes, and MaxNoOfTriggers configuration parameters required to accommodate the tables analyzed.
- Memory requirements for all of the tables, attributes, ordered indexes, and unique hash indexes defined in the database.
- The IndexMemory and DataMemory required per table and table row.

# <span id="page-82-0"></span>**25.5.30 ndb\_top — View CPU usage information for NDB threads**

[ndb\\_top](#page-82-0) displays running information in the terminal about CPU usage by NDB threads on an NDB Cluster data node. Each thread is represented by two rows in the output, the first showing system statistics, the second showing the measured statistics for the thread.

[ndb\\_top](#page-82-0) is available beginning with MySQL NDB Cluster 7.6.3.

### **Usage**

```
ndb_top [-h hostname] [-t port] [-u user] [-p pass] [-n node_id]
```

[ndb\\_top](#page-82-0) connects to a MySQL Server running as an SQL node of the cluster. By default, it attempts to connect to a mysqld running on localhost and port 3306, as the MySQL root user with no password specified. You can override the default host and port using, respectively, [--host](#page-84-0) (-h) and [--port](#page-85-0) (-t). To specify a MySQL user and password, use the [--user](#page-86-0) (-u) and [--passwd](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-programs-ndb-top.md#option_ndb_top_passwd) (-p) options. This user must be able to read tables in the [ndbinfo](#page-181-0) database ([ndb\\_top](#page-82-0) uses information from ndbinfo.cpustat and related tables).

For more information about MySQL user accounts and passwords, see Section 8.2, "Access Control and Account Management".

Output is available as plain text or an ASCII graph; you can specify this using the [--text](#page-86-1) (-x) and [-](#page-84-1) [graph](#page-84-1) (-g) options, respectively. These two display modes provide the same information; they can be used concurrently. At least one display mode must be in use.

Color display of the graph is supported and enabled by default ([--color](#page-83-0) or -c option). With color support enabled, the graph display shows OS user time in blue, OS system time in green, and idle time as blank. For measured load, blue is used for execution time, yellow for send time, red for time spent in send buffer full waits, and blank spaces for idle time. The percentage shown in the graph display is the sum of percentages for all threads which are not idle. Colors are not currently configurable; you can use grayscale instead by using --skip-color.

The sorted view ([--sort](#page-85-1), -r) is based on the maximum of the measured load and the load reported by the OS. Display of these can be enabled and disabled using the [--measured-load](#page-84-2) (-m) and [-](#page-85-2) [os-load](#page-85-2) (-o) options. Display of at least one of these loads must be enabled.

The program tries to obtain statistics from a data node having the node ID given by the [--node-id](#page-84-3) ( n) option; if unspecified, this is 1. [ndb\\_top](#page-82-0) cannot provide information about other types of nodes.

The view adjusts itself to the height and width of the terminal window; the minimum supported width is 76 characters.

Once started, [ndb\\_top](#page-82-0) runs continuously until forced to exit; you can quit the program using Ctrl-C. The display updates once per second; to set a different delay interval, use [--sleep-time](#page-85-3) (-s).

![](_page_83_Picture_7.jpeg)

#### **Note**

[ndb\\_top](#page-82-0) is available on macOS, Linux, and Solaris. It is not currently supported on Windows platforms.

The following table includes all options that are specific to the NDB Cluster program [ndb\\_top](#page-82-0). Additional descriptions follow the table.

### <span id="page-83-0"></span>**Additional Options**

• [--color](#page-83-0), -c

| Command-Line Format | color |
|---------------------|-------|
|---------------------|-------|

Show ASCII graphs in color; use --skip-colors to disable.

<span id="page-83-1"></span>• [--defaults-extra-file](#page-83-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-83-2"></span>• [--defaults-file](#page-83-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-83-3"></span>• [--defaults-group-suffix](#page-83-3)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-84-1"></span>• [--graph](#page-84-1), -g

| Command-Line Format | graph |
|---------------------|-------|
|---------------------|-------|

Display data using graphs; use --skip-graphs to disable. This option or [--text](#page-86-1) must be true; both options may be true.

<span id="page-84-4"></span>• [--help](#page-84-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Show program usage information.

<span id="page-84-0"></span>• [--host\[](#page-84-0)=name], -h

| Command-Line Format | host=string |
|---------------------|-------------|
| Type                | String      |
| Default Value       | localhost   |

Host name or IP address of MySQL Server to connect to.

<span id="page-84-5"></span>• [--login-path](#page-84-5)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-84-6"></span>• [--no-login-paths](#page-84-6)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-84-2"></span>• [--measured-load](#page-84-2), -m

| Command-Line Format | measured-load |
|---------------------|---------------|

Show measured load by thread. This option or [--os-load](#page-85-2) must be true; both options may be true.

<span id="page-84-7"></span>• [--no-defaults](#page-84-7)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-84-3"></span>• [--node-id\[](#page-84-3)=#], -n

| Command-Line Format | node-id=# |
|---------------------|-----------|

| Type          | Integer |
|---------------|---------|
| Default Value | 1       |

Watch the data node having this node ID.

<span id="page-85-2"></span>• [--os-load](#page-85-2), -o

| Command-Line Format | os-load |
|---------------------|---------|
|---------------------|---------|

Show load measured by operating system. This option or [--measured-load](#page-84-2) must be true; both options may be true.

<span id="page-85-4"></span>• [--password\[](#page-85-4)=password], -p

| Command-Line Format | password=password |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | NULL              |

Connect to a MySQL Server using this password and the MySQL user specified by [--user](#page-86-0).

This password is associated with a MySQL user account only, and is not related in any way to the password used with encrypted NDB backups.

<span id="page-85-0"></span>• [--port\[](#page-85-0)=#], -P

| Command-Line Format | port=#  |
|---------------------|---------|
| Type                | Integer |
| Default Value       | 3306    |

Port number to use when connecting to MySQL Server.

(Formerly, the short form for this option was -t, which was repurposed as the short form of [--text](#page-86-1).)

<span id="page-85-5"></span>• [--print-defaults](#page-85-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-85-3"></span>• [--sleep-time\[](#page-85-3)=seconds], -s

| Command-Line Format | sleep-time=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 1            |

Time to wait between display refreshes, in seconds.

<span id="page-85-6"></span>• --socket=[path/to/file](#page-85-6), -S

| Command-Line Format | socket=path |
|---------------------|-------------|
| Type                | Path name   |
| Default Value       | [none]      |

Use the specified socket file for the connection.

<span id="page-85-1"></span>• [--sort](#page-85-1), -r

Sort threads by usage; use --skip-sort to disable.

<span id="page-86-1"></span>• [--text](#page-86-1), -t

| Command-Line Format | text |
|---------------------|------|
|---------------------|------|

Display data using text. This option or [--graph](#page-84-1) must be true; both options may be true.

(The short form for this option was -x in previous versions of NDB Cluster, but this is no longer supported.)

<span id="page-86-2"></span>• [--usage](#page-86-2)

| Command-Line Format | usage |
|---------------------|-------|

Display help text and exit; same as [--help](#page-84-4).

<span id="page-86-0"></span>• [--user\[](#page-86-0)=name], -u

| Command-Line Format | user=name |
|---------------------|-----------|
| Type                | String    |
| Default Value       | root      |

Connect as this MySQL user. Normally requires a password supplied by the [--password](#page-85-4) option.

**Sample Output.** The next figure shows [ndb\\_top](#page-82-0) running in a terminal window on a Linux system with an ndbmtd data node under a moderate load. Here, the program has been invoked using [ndb\\_top](#page-82-0) [-n8](#page-84-3) [-x](#page-86-1) to provide both text and graph output:

**Figure 25.5 ndb\_top Running in Terminal**

![](_page_87_Picture_2.jpeg)

[ndb\\_top](#page-82-0) also shows spin times for threads, displayed in green.

# <span id="page-87-0"></span>**25.5.31 ndb\_waiter — Wait for NDB Cluster to Reach a Given Status**

[ndb\\_waiter](#page-87-0) repeatedly (each 100 milliseconds) prints out the status of all cluster data nodes until either the cluster reaches a given status or the [--timeout](#page-91-0) limit is exceeded, then exits. By default, it waits for the cluster to achieve STARTED status, in which all nodes have started and connected to the cluster. This can be overridden using the [--no-contact](#page-90-0) and [--not-started](#page-91-1) options.

The node states reported by this utility are as follows:

- NO\_CONTACT: The node cannot be contacted.
- UNKNOWN: The node can be contacted, but its status is not yet known. Usually, this means that the node has received a [START](#page-104-0) or [RESTART](#page-102-1) command from the management server, but has not yet acted on it.
- NOT\_STARTED: The node has stopped, but remains in contact with the cluster. This is seen when restarting the node using the management client's RESTART command.
- STARTING: The node's ndbd process has started, but the node has not yet joined the cluster.
- STARTED: The node is operational, and has joined the cluster.
- SHUTTING\_DOWN: The node is shutting down.

• SINGLE USER MODE: This is shown for all cluster data nodes when the cluster is in single user mode.

Options that can be used with [ndb\\_waiter](#page-87-0) are shown in the following table. Additional descriptions follow the table.

### **Usage**

ndb\_waiter [-c connection\_string]

### <span id="page-88-0"></span>**Additional Options**

• [--character-sets-dir](#page-88-0)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-88-1"></span>• [--connect-retries](#page-88-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-88-2"></span>• [--connect-retry-delay](#page-88-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-88-3"></span>• [--connect-string](#page-88-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-89-0).

<span id="page-88-4"></span>• [--core-file](#page-88-4)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-88-5"></span>• [--defaults-extra-file](#page-88-5)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
|---------------------|--------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read given file after global files are read.

<span id="page-89-1"></span>• [--defaults-file](#page-89-1)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-89-2"></span>• [--defaults-group-suffix](#page-89-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-89-3"></span>• [--login-path](#page-89-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-89-4"></span>• [--no-login-paths](#page-89-4)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-89-5"></span>• [--help](#page-89-5)

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display help text and exit.

<span id="page-89-0"></span>• [--ndb-connectstring](#page-89-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connection string for connecting to ndb\_mgmd. Syntax: [nodeid=id;] [host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-89-6"></span>• [--ndb-mgm-tls](#page-89-6)

| Command-Line Format | ndb-mgm-tls=level |
|---------------------|-------------------|
| Type                | Enumeration       |

| Default Value | relaxed |
|---------------|---------|
| Valid Values  | relaxed |
|               | strict  |

Sets the level of TLS support required to connect to the management server; one of relaxed or strict. relaxed (the default) means that a TLS connection is attempted, but success is not required; strict means that TLS is required to connect.

#### <span id="page-90-1"></span>• [--ndb-mgmd-host](#page-90-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as --[ndb-connectstring](#page-89-0).

#### <span id="page-90-2"></span>• [--ndb-nodeid](#page-90-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-89-0).

#### <span id="page-90-3"></span>• [--ndb-optimized-node-selection](#page-90-3)

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-90-4"></span>• [--ndb-tls-search-path](#page-90-4)

| Command-Line Format     | ndb-tls-search-path=list |
|-------------------------|--------------------------|
| Type                    | Path name                |
| Default Value (Unix)    | \$HOME/ndb-tls           |
| Default Value (Windows) | \$HOMEDIR/ndb-tls        |

Specify a list of directories to search for a CA file. On Unix platforms, the directory names are separated by colons (:); on Windows systems, the semicolon character (;) is used as the separator. A directory reference may be relative or absolute; it may contain one or more environment variables, each denoted by a prefixed dollar sign (\$), and expanded prior to use.

Searching begins with the leftmost named directory and proceeds from left to right until a file is found. An empty string denotes an empty search path, which causes all searches to fail. A string consisting of a single dot (.) indicates that the search path limited to the current working directory.

If no search path is supplied, the compiled-in default value is used. This value depends on the platform used: On Windows, this is \ndb-tls; on other platforms (including Linux), it is \$HOME/ndb-tls. This can be overridden by compiling NDB Cluster using - DWITH\_NDB\_TLS\_SEARCH\_PATH.

#### <span id="page-90-0"></span>• [--no-contact](#page-90-0), -n

Instead of waiting for the STARTED state, [ndb\\_waiter](#page-87-0) continues running until the cluster reaches NO\_CONTACT status before exiting.

<span id="page-91-2"></span>• [--no-defaults](#page-91-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-91-1"></span>• [--not-started](#page-91-1)

Instead of waiting for the STARTED state, [ndb\\_waiter](#page-87-0) continues running until the cluster reaches NOT\_STARTED status before exiting.

<span id="page-91-3"></span>• [--nowait-nodes=](#page-91-3)list

When this option is used, [ndb\\_waiter](#page-87-0) does not wait for the nodes whose IDs are listed. The list is comma-delimited; ranges can be indicated by dashes, as shown here:

\$> **ndb\_waiter --nowait-nodes=1,3,7-9**

![](_page_91_Picture_9.jpeg)

#### **Important**

Do not use this option together with the [--wait-nodes](#page-92-0) option.

<span id="page-91-4"></span>• [--print-defaults](#page-91-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-91-0"></span>• [--timeout=](#page-91-0)seconds, -t seconds

Time to wait. The program exits if the desired state is not achieved within this number of seconds. The default is 120 seconds (1200 reporting cycles).

<span id="page-91-5"></span>• [--single-user](#page-91-5)

The program waits for the cluster to enter single user mode.

<span id="page-91-6"></span>• [--usage](#page-91-6)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-89-5).

<span id="page-91-7"></span>• [--verbose](#page-91-7)

| Command-Line Format | verbose=# |
|---------------------|-----------|
| Type                | Integer   |
| Default Value       | 2         |
| Minimum Value       | 0         |
| Maximum Value       | 2         |

Controls verbosity level of printout. Possible levels and their effects are listed here:

- 0: Do not print (return exit code only; see following for exit codes).
- 1: Print final connection status only.
- 2: Print status each time it is checked.

This is the same behavior as in versions of NDB Cluster previous to 8.4.

Exit codes returned by [ndb\\_waiter](#page-87-0) are listed here, with their meanings:

- 0: Success.
- 1: Wait timed out.
- 2: Parameter error, such as an invalid node ID.
- 3: Failed to connect to the management server.
- <span id="page-92-1"></span>• [--version](#page-92-1)

```
Command-Line Format --version
```

Display version information and exit.

<span id="page-92-0"></span>• [--wait-nodes=](#page-92-0)list, -w list

When this option is used, [ndb\\_waiter](#page-87-0) waits only for the nodes whose IDs are listed. The list is comma-delimited; ranges can be indicated by dashes, as shown here:

```
$> ndb_waiter --wait-nodes=2,4-6,10
```

![](_page_92_Picture_12.jpeg)

#### **Important**

Do not use this option together with the [--nowait-nodes](#page-91-3) option.

**Sample Output.** Shown here is the output from [ndb\\_waiter](#page-87-0) when run against a 4-node cluster in which two nodes have been shut down and then started again manually. Duplicate reports (indicated by ...) are omitted.

```
$> ./ndb_waiter -c localhost
Connecting to mgmsrv at (localhost)
State node 1 STARTED
State node 2 NO_CONTACT
State node 3 STARTED
State node 4 NO_CONTACT
Waiting for cluster enter state STARTED
...
State node 1 STARTED
State node 2 UNKNOWN
State node 3 STARTED
State node 4 NO_CONTACT
Waiting for cluster enter state STARTED
...
State node 1 STARTED
State node 2 STARTING
State node 3 STARTED
State node 4 NO_CONTACT
Waiting for cluster enter state STARTED
...
State node 1 STARTED
State node 2 STARTING
State node 3 STARTED
State node 4 UNKNOWN
Waiting for cluster enter state STARTED
...
```

```
State node 1 STARTED
State node 2 STARTING
State node 3 STARTED
State node 4 STARTING
Waiting for cluster enter state STARTED
...
State node 1 STARTED
State node 2 STARTED
State node 3 STARTED
State node 4 STARTING
Waiting for cluster enter state STARTED
...
State node 1 STARTED
State node 2 STARTED
State node 3 STARTED
State node 4 STARTED
Waiting for cluster enter state STARTED
```

![](_page_93_Picture_2.jpeg)

#### **Note**

If no connection string is specified, then [ndb\\_waiter](#page-87-0) tries to connect to a management on localhost, and reports Connecting to mgmsrv at (null).

# <span id="page-93-0"></span>**25.5.32 ndbxfrm — Compress, Decompress, Encrypt, and Decrypt Files Created by NDB Cluster**

The [ndbxfrm](#page-93-0) utility can be used to decompress, decrypt, and output information about files created by NDB Cluster that are compressed, encrypted, or both. It can also be used to compress or encrypt files.

### **Usage**

```
ndbxfrm --info file[ file ...]
ndbxfrm --compress input_file output_file
ndbxfrm --decrypt-password=password input_file output_file
ndbxfrm [--encrypt-ldf-iter-count=#] --encrypt-password=password input_file output_file
```

input\_file and output\_file cannot be the same file.

## <span id="page-93-1"></span>**Options**

• [--compress](#page-93-1), -c

| Command-Line Format | compress |
|---------------------|----------|

Compresses the input file, using the same compression method as is used for compressing NDB Cluster backups, and writes the output to an output file. To decompress a compressed NDB backup file that is not encrypted, it is necessary only to invoke [ndbxfrm](#page-93-0) using the names of the compressed file and an output file (with no options required).

<span id="page-93-2"></span>• [--decrypt-key=](#page-93-2)key, -K key

| Command-Line Format | decrypt-key=key |
|---------------------|-----------------|

Decrypts a file encrypted by NDB using the supplied key.

![](_page_94_Picture_1.jpeg)

#### **Note**

This option cannot be used together with [--decrypt-password](#page-94-0).

<span id="page-94-1"></span>• [--decrypt-key-from-stdin](#page-94-1)

| Command-Line Format | decrypt-key-from-stdin |
|---------------------|------------------------|
|---------------------|------------------------|

Decrypts a file encrypted by NDB using the key supplied from stdin.

<span id="page-94-0"></span>• [--decrypt-password=](#page-94-0)password

| Command-Line Format | decrypt-password=password |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | [none]                    |

Decrypts a file encrypted by NDB using the password supplied.

![](_page_94_Picture_10.jpeg)

#### **Note**

This option cannot be used together with [--decrypt-key](#page-93-2).

<span id="page-94-2"></span>• [--decrypt-password-from-stdin\[=TRUE|FALSE\]](#page-94-2)

| Command-Line Format | decrypt-password-from-stdin |
|---------------------|-----------------------------|
|---------------------|-----------------------------|

Decrypts a file encrypted by NDB, using a password supplied from standard input. This is similar to entering a password after invoking mysql --password with no password following the option.

<span id="page-94-3"></span>• [--defaults-extra-file](#page-94-3)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-94-4"></span>• [--defaults-file](#page-94-4)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-94-5"></span>• [--defaults-group-suffix](#page-94-5)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

#### <span id="page-95-0"></span>• [--detailed-info](#page-95-0)

| Command-Line Format | encrypt-block-size=# |
|---------------------|----------------------|
| Type                | Boolean              |
| Default Value       | FALSE                |

Print out file information like [--info](#page-97-0), but include the file's header and trailer.

### Example:

```
$> ndbxfrm --detailed-info S0.sysfile
File=/var/lib/cluster-data/ndb_7_fs/D1/NDBCNTR/S0.sysfile, compression=no, encryption=yes
header: {
 fixed_header: {
 magic: {
 magic: { 78, 68, 66, 88, 70, 82, 77, 49 },
 endian: 18364758544493064720,
 header_size: 32768,
 fixed_header_size: 160,
 zeros: { 0, 0 }
 },
 flags: 73728,
 flag_extended: 0,
 flag_zeros: 0,
 flag_file_checksum: 0,
 flag_data_checksum: 0,
 flag_compress: 0,
 flag_compress_method: 0,
 flag_compress_padding: 0,
 flag_encrypt: 18,
 flag_encrypt_cipher: 2,
 flag_encrypt_krm: 1,
 flag_encrypt_padding: 0,
 flag_encrypt_key_selection_mode: 0,
 dbg_writer_ndb_version: 524320,
 octets_size: 32,
 file_block_size: 32768,
 trailer_max_size: 80,
 file_checksum: { 0, 0, 0, 0 },
 data_checksum: { 0, 0, 0, 0 },
 zeros01: { 0 },
 compress_dbg_writer_header_version: { ... },
 compress_dbg_writer_library_version: { ... },
 encrypt_dbg_writer_header_version: { ... },
 encrypt_dbg_writer_library_version: { ... },
 encrypt_key_definition_iterator_count: 100000,
 encrypt_krm_keying_material_size: 32,
 encrypt_krm_keying_material_count: 1,
 encrypt_key_data_unit_size: 32768,
 encrypt_krm_keying_material_position_in_octets: 0,
 },
 octets: {
 102, 68, 56, 125, 78, 217, 110, 94, 145, 121, 203, 234, 26, 164, 137, 180,
 100, 224, 7, 88, 173, 123, 209, 110, 185, 227, 85, 174, 109, 123, 96, 156,
 }
}
trailer: {
 fixed_trailer: {
 flags: 48,
 flag_extended: 0,
 flag_zeros: 0,
 flag_file_checksum: 0,
 flag_data_checksum: 3,
 data_size: 512,
 file_checksum: { 0, 0, 0, 0 },
 data_checksum: { 226, 223, 102, 207 },
 magic: {
 zeros: { 0, 0 }
 fixed_trailer_size: 56,
```

```
 trailer_size: 32256,
 endian: 18364758544493064720,
 magic: { 78, 68, 66, 88, 70, 82, 77, 49 },
 },
 }
}
```

<span id="page-96-0"></span>• [--encrypt-block-size=](#page-96-0)#

| Command-Line Format | encrypt-block-size=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |
| Minimum Value       | 0                    |
| Maximum Value       | 2147483647           |

Size of input data chunks that are encrypted as a unit. Used with XTS; set to 0 (the default) for CBC mode.

<span id="page-96-1"></span>• [--encrypt-cipher=](#page-96-1)#

| Command-Line Format | encrypt-cipher=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 1                |
| Minimum Value       | 0                |
| Maximum Value       | 2147483647       |

Cipher used for encryption. Set to 1 for CBC mode (the default), or 2 for XTS.

<span id="page-96-2"></span>• [--encrypt-kdf-iter-count=](#page-96-2)#, -k #

| Command-Line Format | encrypt-kdf-iter-count=# |
|---------------------|--------------------------|
| Type                | Integer                  |
| Default Value       | 0                        |
| Minimum Value       | 0                        |
| Maximum Value       | 2147483647               |

When encrypting a file, specifies the number of iterations to use for the encryption key. Requires the [--encrypt-password](#page-96-3) option.

<span id="page-96-4"></span>• [--encrypt-key=](#page-96-4)key

| Command-Line Format | encrypt-key=key |
|---------------------|-----------------|
|---------------------|-----------------|

Encrypts a file using the supplied key.

![](_page_96_Picture_14.jpeg)

#### **Note**

This option cannot be used together with [--encrypt-password](#page-96-3).

<span id="page-96-5"></span>• [--encrypt-key-from-stdin](#page-96-5)

| Command-Line Format | encrypt-key-from-stdin |
|---------------------|------------------------|
|                     |                        |

Encrypt a file using the key supplied from stdin.

<span id="page-96-3"></span>• [--encrypt-password=](#page-96-3)password

| Command-Line Format | encrypt-password=password |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | [none]                    |

Encrypts the backup file using the password supplied by the option. The password must meet the requirements listed here:

- Uses any of the printable ASCII characters except !, ', ", \$, %, \, `, and ^
- Is no more than 256 characters in length
- Is enclosed by single or double quotation marks

![](_page_97_Picture_6.jpeg)

#### **Note**

This option cannot be used together with [--encrypt-key](#page-96-4).

<span id="page-97-1"></span>• [--encrypt-password-from-stdin\[=TRUE|FALSE\]](#page-97-1)

| Command-Line Format | encrypt-password-from-stdin |
|---------------------|-----------------------------|
|---------------------|-----------------------------|

Encrypts a file using a password supplied from standard input. This is similar to entering a password is entered after invoking mysql --password with no password following the option.

<span id="page-97-2"></span>• [--help](#page-97-2), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Prints usage information for the program.

<span id="page-97-0"></span>• [--info](#page-97-0), -i

| Command-Line Format | info |
|---------------------|------|
|---------------------|------|

Prints the following information about one or more input files:

- The name of the file
- Whether the file is compressed (compression=yes or compression=no)
- Whether the file is encrypted (encryption=yes or encryption=no)

### Example:

```
$> ndbxfrm -i BACKUP-10-0.5.Data BACKUP-10.5.ctl BACKUP-10.5.log
File=BACKUP-10-0.5.Data, compression=no, encryption=yes
File=BACKUP-10.5.ctl, compression=no, encryption=yes
File=BACKUP-10.5.log, compression=no, encryption=yes
```

You can also see the file's header and trailer using the [--detailed-info](#page-95-0) option.

<span id="page-97-3"></span>• [--login-path](#page-97-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

<span id="page-98-0"></span>• [--no-login-paths](#page-98-0)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

<span id="page-98-1"></span>• [--no-defaults](#page-98-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-98-2"></span>• [--print-defaults](#page-98-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-98-3"></span>• [--usage](#page-98-3), -?

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Synonym for [--help](#page-97-2).

<span id="page-98-4"></span>• [--version](#page-98-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Prints out version information.

[ndbxfrm](#page-93-0) can encrypt backups created by any version of NDB Cluster. The .Data, .ctl, and .log files comprising the backup must be encrypted separately, and these files must be encrypted separately for each data node. Once encrypted, such backups can be decrypted only by [ndbxfrm](#page-93-0), [ndb\\_restore](#page-35-7), or ndb\_print\_backup.

An encrypted file can be re-encrypted with a new password using the [--encrypt-password](#page-96-3) and [-](#page-94-0) [decrypt-password](#page-94-0) options together, like this:

```
ndbxfrm --decrypt-password=old --encrypt-password=new input_file output_file
```

In the example just shown, old and new are the old and new passwords, respectively; both of these must be quoted. The input file is decrypted and then encrypted as the output file. The input file itself is not changed; if you do not want it to be accessible using the old password, you must remove the input file manually.