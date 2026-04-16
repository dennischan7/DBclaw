---
source: MySQL 8.0 Reference
title: 00_Overview
---

Using and managing an NDB Cluster requires several specialized programs, which we describe in this chapter. We discuss the purposes of these programs in an NDB Cluster, how to use the programs, and what startup options are available for each of them.

These programs include the NDB Cluster data, management, and SQL node processes ([ndbd](#page-53-0), [ndbmtd](#page-69-0), [ndb\\_mgmd](#page-70-0), and mysqld) and the management client ([ndb\\_mgm](#page-81-0)).

For information about using mysqld as an NDB Cluster process, see Section 25.6.10, "MySQL Server Usage for NDB Cluster".

Other NDB utility, diagnostic, and example programs are included with the NDB Cluster distribution. These include [ndb\\_restore](#page-170-0), ndb\_show\_tables, and [ndb\\_config](#page-92-0). These programs are also covered in this section.

## <span id="page-53-0"></span>**25.5.1 ndbd — The NDB Cluster Data Node Daemon**

The [ndbd](#page-53-0) binary provides the single-threaded version of the process that is used to handle all the data in tables employing the NDBCLUSTER storage engine. This data node process enables a data node to accomplish distributed transaction handling, node recovery, checkpointing to disk, online backup, and related tasks. In NDB 8.0.38 and later, when started, [ndbd](#page-53-0) logs a warning similar to that shown here:

```
2024-05-28 13:32:16 [ndbd] WARNING -- Running ndbd with a single thread of
signal execution. For multi-threaded signal execution run the ndbmtd binary.
```

[ndbmtd](#page-69-0) is the multi-threaded version of this binary.

In an NDB Cluster, a set of [ndbd](#page-53-0) processes cooperate in handling data. These processes can execute on the same computer (host) or on different computers. The correspondences between data nodes and Cluster hosts is completely configurable.

Options that can be used with [ndbd](#page-53-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.24 Command-line options used with the program ndbd**

| Format                                         | Description                                                                                                                                                  | Added, Deprecated, or<br>Removed                      |
|------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| bind-address=name                              | Local bind address                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| character-sets<br>dir=path                     | Directory containing character<br>sets                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-delay=#                                | Obsolete synonym forconnect<br>retry-delay, which should be<br>used instead of this option                                                                   | REMOVED: NDB 8.0.28                                   |
| connect-retries=#                              | Set the number of times to retry<br>a connection before giving up;<br>0 means 1 attempt only (and<br>no retries); -1 means continue<br>retrying indefinitely | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                          | Time to wait between attempts<br>to contact a management server,<br>in seconds; 0 means do not wait<br>between attempts                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string,           | Same asndb-connectstring                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                           |                                                                                                                                                              |                                                       |
| core-file                                      | Write core file on error; used in<br>debugging                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| daemon,<br>-d                                  | Start ndbd as daemon (default);<br>override withnodaemon                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-extra<br>file=path                    | Read given file after global files<br>are read                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                             | Read default options from given<br>file only                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string                | Also read groups with<br>concat(group, suffix)                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| filesystem<br>password=password                | Password for node file system<br>encryption; can be passed from<br>stdin, tty, or my.cnf file                                                                | ADDED: NDB 8.0.31                                     |
| filesystem-password<br>from-stdin={TRUE FALSE} | Get password for node file<br>system encryption, passed from<br>stdin                                                                                        | ADDED: NDB 8.0.31                                     |
| foreground                                     | Run ndbd in foreground,<br>provided for debugging purposes<br>(impliesnodaemon)                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                          | Display help text and exit                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                             |                                                                                                                                                              |                                                       |

| Format                                                          | Description                                                                                                                                             | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| initial                                                         | Perform initial start of ndbd,<br>including file system cleanup;<br>consult documentation before<br>using this option                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| initial-start                                                   | Perform partial initial start<br>(requiresnowait-nodes)                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| install[=name]                                                  | Used to install data node process<br>as Windows service; does not<br>apply on other platforms                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| logbuffer-size=#                                                | Control size of log buffer; for<br>use when debugging with many<br>log messages being generated;<br>default is sufficient for normal<br>operations      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                                                 | Read given path from login file                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-mgmd<br>host=connection_string,                             | my.cnf<br>Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                                            |                                                                                                                                                         |                                                       |
| ndb-nodeid=#                                                    | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nodaemon                                                        | Do not start ndbd as daemon;<br>provided for testing purposes                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nostart,<br>-n                                                  | Do not start ndbd immediately;<br>ndbd waits for command to start<br>from ndb_mgm                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nowait-nodes=list                                               | Do not wait for these data nodes<br>to start (takes comma-separated<br>list of node IDs); requiresndb<br>nodeid                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable           | REMOVED: 8.0.31                                       |
| print-defaults                                                  | Print program argument list and<br>exit                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| remove[=name]                                                   | Used to remove data node<br>process that was previously                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format   | Description                                                           | Added, Deprecated, or<br>Removed |
|----------|-----------------------------------------------------------------------|----------------------------------|
|          | installed as Windows service;<br>does not apply on other<br>platforms |                                  |
| usage,   | Display help text and exit; same                                      | (Supported in all NDB releases   |
| -?       | ashelp                                                                | based on MySQL 8.0)              |
| verbose, | Write extra debugging                                                 | (Supported in all NDB releases   |
| -v       | information to node log                                               | based on MySQL 8.0)              |
| version, | Display version information and                                       | (Supported in all NDB releases   |
| -V       | exit                                                                  | based on MySQL 8.0)              |

![](_page_56_Picture_2.jpeg)

#### **Note**

All of these options also apply to the multithreaded version of this program ([ndbmtd](#page-69-0)) and you may substitute "[ndbmtd](#page-69-0)" for "[ndbd](#page-53-0)" wherever the latter occurs in this section.

#### <span id="page-56-0"></span>• [--bind-address](#page-56-0)

| Command-Line Format | bind-address=name |
|---------------------|-------------------|
| Type                | String            |
| Default Value       |                   |

Causes [ndbd](#page-53-0) to bind to a specific network interface (host name or IP address). This option has no default value.

<span id="page-56-1"></span>• [--character-sets-dir](#page-56-1)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-56-2"></span>• [--connect-delay=](#page-56-2)#

Determines the time to wait between attempts to contact a management server when starting (the number of attempts is controlled by the [--connect-retries](#page-56-3) option). The default is 5 seconds.

This option is deprecated, and is subject to removal in a future release of NDB Cluster. Use [-](#page-57-0) [connect-retry-delay](#page-57-0) instead.

## <span id="page-56-3"></span>• [--connect-retries=](#page-56-3)#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 12                |
| Minimum Value       | -1                |
| Maximum Value       | 65535             |

Set the number of times to retry a connection before giving up; 0 means 1 attempt only (and no retries). The default is 12 attempts. The time to wait between attempts is controlled by the [--](#page-57-0)

Beginning with NDB 8.0.28, you can set this option to -1, in which case, the data node process continues indefinitely to try to connect.

<span id="page-57-0"></span>• [--connect-retry-delay=](#page-57-0)#

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Numeric               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 4294967295            |

Determines the time to wait between attempts to contact a management server when starting (the time between attempts is controlled by the [--connect-retries](#page-56-3) option). The default is 5 seconds.

This option takes the place of the [--connect-delay](#page-56-2) option, which is now deprecated and subject to removal in a future release of NDB Cluster.

The short form -r for this option is deprecated as of NDB 8.0.28, and subject to removal in a future release of NDB Cluster. Use the long form instead.

<span id="page-57-1"></span>• [--connect-string](#page-57-1)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-61-0).

<span id="page-57-2"></span>• [--core-file](#page-57-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-57-3"></span>• [--daemon](#page-57-3), -d

| Command-Line Format | daemon |
|---------------------|--------|
|---------------------|--------|

Instructs [ndbd](#page-53-0) or [ndbmtd](#page-69-0) to execute as a daemon process. This is the default behavior. [-](#page-61-3) [nodaemon](#page-61-3) can be used to prevent the process from running as a daemon.

This option has no effect when running [ndbd](#page-53-0) or [ndbmtd](#page-69-0) on Windows platforms.

<span id="page-57-4"></span>• [--defaults-extra-file](#page-57-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-57-5"></span>• [--defaults-file](#page-57-5)

|  | Type                | String             |
|--|---------------------|--------------------|
|  | Command-Line Format | defaults-file=path |

| Default Value | [none] |  |
|---------------|--------|--|
|---------------|--------|--|

Read default options from given file only.

<span id="page-58-0"></span>• [--defaults-group-suffix](#page-58-0)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-58-1"></span>• [--filesystem-password](#page-58-1)

| Command-Line Format | filesystem-password=password |
|---------------------|------------------------------|
|                     |                              |

Pass the filesystem encryption and decryption password to the data node process using stdin, tty, or the my.cnf file.

Requires EncryptedFileSystem = 1.

For more information, see Section 25.6.14, "File System Encryption for NDB Cluster".

<span id="page-58-2"></span>• [--filesystem-password-from-stdin](#page-58-2)

| Command-Line Format | filesystem-password-from |
|---------------------|--------------------------|
|                     | stdin={TRUE FALSE}       |

Pass the filesystem encryption and decryption password to the data node process from stdin (only).

Requires EncryptedFileSystem = 1.

For more information, see Section 25.6.14, "File System Encryption for NDB Cluster".

<span id="page-58-3"></span>• [--foreground](#page-58-3)

| Command-Line Format | foreground |
|---------------------|------------|
|---------------------|------------|

Causes [ndbd](#page-53-0) or [ndbmtd](#page-69-0) to execute as a foreground process, primarily for debugging purposes. This option implies the [--nodaemon](#page-61-3) option.

This option has no effect when running [ndbd](#page-53-0) or [ndbmtd](#page-69-0) on Windows platforms.

<span id="page-58-4"></span>• [--help](#page-58-4)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-59-0"></span>• [--initial](#page-59-0)

| Command-Line Format | initial |
|---------------------|---------|
|---------------------|---------|

Instructs [ndbd](#page-53-0) to perform an initial start. An initial start erases any files created for recovery purposes by earlier instances of [ndbd](#page-53-0). It also re-creates recovery log files. On some operating systems, this process can take a substantial amount of time.

An [--initial](#page-59-0) start is to be used only when starting the [ndbd](#page-53-0) process under very special circumstances; this is because this option causes all files to be removed from the NDB Cluster file system and all redo log files to be re-created. These circumstances are listed here:

- When performing a software upgrade which has changed the contents of any files.
- When restarting the node with a new version of [ndbd](#page-53-0).
- As a measure of last resort when for some reason the node restart or system restart repeatedly fails. In this case, be aware that this node can no longer be used to restore data due to the destruction of the data files.

![](_page_59_Picture_8.jpeg)

#### **Warning**

To avoid the possibility of eventual data loss, it is recommended that you not use the --initial option together with StopOnError = 0. Instead, set StopOnError to 0 in config.ini only after the cluster has been started, then restart the data nodes normally—that is, without the --initial option. See the description of the StopOnError parameter for a detailed explanation of this issue. (Bug #24945638)

Use of this option prevents the StartPartialTimeout and StartPartitionedTimeout configuration parameters from having any effect.

![](_page_59_Picture_12.jpeg)

#### **Important**

This option does not affect backup files that have already been created by the affected node.

Prior to NDB 8.0.21, the --initial option also did not affect any Disk Data files. In NDB 8.0.21 and later, when used to perform an initial restart of the cluster, the option causes the removal of all data files associated with Disk Data tablespaces and undo log files associated with log file groups that existed previously on this data node (see Section 25.6.11, "NDB Cluster Disk Data Tables").

This option also has no effect on recovery of data by a data node that is just starting (or restarting) from data nodes that are already running (unless they also were started with --initial, as part of an initial restart). This recovery of data occurs automatically, and requires no user intervention in an NDB Cluster that is running normally.

It is permissible to use this option when starting the cluster for the very first time (that is, before any data node files have been created); however, it is not necessary to do so.

#### <span id="page-60-0"></span>• [--initial-start](#page-60-0)

| Command-Line Format | initial-start |
|---------------------|---------------|

This option is used when performing a partial initial start of the cluster. Each node should be started with this option, as well as [--nowait-nodes](#page-62-0).

Suppose that you have a 4-node cluster whose data nodes have the IDs 2, 3, 4, and 5, and you wish to perform a partial initial start using only nodes 2, 4, and 5—that is, omitting node 3:

```
$> ndbd --ndb-nodeid=2 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=4 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=5 --nowait-nodes=3 --initial-start
```

When using this option, you must also specify the node ID for the data node being started with the [--ndb-nodeid](#page-61-2) option.

![](_page_60_Picture_7.jpeg)

#### **Important**

Do not confuse this option with the [--nowait-nodes](#page-78-0) option for [ndb\\_mgmd](#page-70-0), which can be used to enable a cluster configured with multiple management servers to be started without all management servers being online.

#### <span id="page-60-1"></span>• [--install\[=](#page-60-1)name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndbd           |

Causes [ndbd](#page-53-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndbd. Although it is preferable to specify other [ndbd](#page-53-0) program options in a my.ini or my.cnf configuration file, it is possible to use together with - install. However, in such cases, the --install option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-59-0) option, since this causes the data node file system to be wiped and rebuilt every time the service is stopped and started. Extreme care should also be taken if you intend to use any of the other [ndbd](#page-53-0) options that affect the starting of data nodes—including [--initial-start](#page-60-0), [--nostart](#page-61-5), and [--nowait-nodes](#page-62-0) together with [--install](#page-60-1), and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-60-1) option has no effect on non-Windows platforms.

#### <span id="page-60-2"></span>• [--logbuffer-size=](#page-60-2)#

| Command-Line Format | logbuffer-size=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 32768            |
| Minimum Value       | 2048             |
| Maximum Value       | 4294967295       |

Sets the size of the data node log buffer. When debugging with high amounts of extra logging, it is possible for the log buffer to run out of space if there are too many log messages, in which case some log messages can be lost. This should not occur during normal operations.

<span id="page-60-3"></span>• [--login-path](#page-60-3)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-61-0"></span>• [--ndb-connectstring](#page-61-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-61-1"></span>• [--ndb-mgmd-host](#page-61-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-61-0).

<span id="page-61-2"></span>• [--ndb-nodeid](#page-61-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-61-6"></span>• [--ndb-optimized-node-selection](#page-61-6)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-61-3"></span>• [--nodaemon](#page-61-3)

| Command-Line Format | nodaemon |
|---------------------|----------|
|---------------------|----------|

Prevents [ndbd](#page-53-0) or [ndbmtd](#page-69-0) from executing as a daemon process. This option overrides the [-](#page-57-3) [daemon](#page-57-3) option. This is useful for redirecting output to the screen when debugging the binary.

The default behavior for [ndbd](#page-53-0) and [ndbmtd](#page-69-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms, where it has no effect.

<span id="page-61-4"></span>• [--no-defaults](#page-61-4)

Do not read default options from any option file other than login file.

<span id="page-61-5"></span>• [--nostart](#page-61-5), -n

| Command-Line Format | nostart |
|---------------------|---------|
|---------------------|---------|

Instructs [ndbd](#page-53-0) not to start automatically. When this option is used, [ndbd](#page-53-0) connects to the management server, obtains configuration data from it, and initializes communication objects. However, it does not actually start the execution engine until specifically requested to do so by the management server. This can be accomplished by issuing the proper START command in the management client (see Section 25.6.1, "Commands in the NDB Cluster Management Client").

<span id="page-62-0"></span>• [--nowait-nodes=](#page-62-0)node\_id\_1[, node\_id\_2[, ...]]

| Command-Line Format | nowait-nodes=list |
|---------------------|-------------------|
| Type                | String            |
| Default Value       |                   |

This option takes a list of data nodes for which the cluster does not wait, prior to starting.

This can be used to start the cluster in a partitioned state. For example, to start the cluster with only half of the data nodes (nodes 2, 3, 4, and 5) running in a 4-node cluster, you can start each [ndbd](#page-53-0) process with --nowait-nodes=3,5. In this case, the cluster starts as soon as nodes 2 and 4 connect, and does not wait StartPartitionedTimeout milliseconds for nodes 3 and 5 to connect as it would otherwise.

If you wanted to start up the same cluster as in the previous example without one [ndbd](#page-53-0) (say, for example, that the host machine for node 3 has suffered a hardware failure) then start nodes 2, 4, and 5 with --nowait-nodes=3. Then the cluster starts as soon as nodes 2, 4, and 5 connect, and does not wait for node 3 to start.

<span id="page-62-1"></span>• [--print-defaults](#page-62-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-62-2"></span>• [--remove\[=](#page-62-2)name]

| Command-Line Format | remove[=name] |  |
|---------------------|---------------|--|
| Platform Specific   | Windows       |  |
| Type                | String        |  |
| Default Value       | ndbd          |  |

Causes an [ndbd](#page-53-0) process that was previously installed as a Windows service to be removed. Optionally, you can specify a name for the service to be uninstalled; if not set, the service name defaults to ndbd.

The [--remove](#page-62-2) option has no effect on non-Windows platforms.

<span id="page-62-3"></span>• [--usage](#page-62-3)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-62-4"></span>• [--verbose](#page-62-4), -v

Causes extra debug output to be written to the node log.

You can also use NODELOG DEBUG ON and NODELOG DEBUG OFF to enable and disable this extra logging while the data node is running.

<span id="page-62-5"></span>• [--version](#page-62-5)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

[ndbd](#page-53-0) generates a set of log files which are placed in the directory specified by DataDir in the config.ini configuration file.

These log files are listed below. node\_id is and represents the node's unique identifier. For example, ndb\_2\_error.log is the error log generated by the data node whose node ID is 2.

• ndb\_node\_id\_error.log is a file containing records of all crashes which the referenced [ndbd](#page-53-0) process has encountered. Each record in this file contains a brief error string and a reference to a trace file for this crash. A typical entry in this file might appear as shown here:

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

Listings of possible [ndbd](#page-53-0) exit codes and messages generated when a data node process shuts down prematurely can be found in [Data Node Error Messages.](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md)

![](_page_63_Picture_8.jpeg)

#### **Important**

The last entry in the error log file is not necessarily the newest one (nor is it likely to be). Entries in the error log are not listed in chronological order; rather, they correspond to the order of the trace files as determined in the ndb\_node\_id\_trace.log.next file (see below). Error log entries are thus overwritten in a cyclical and not sequential fashion.

• ndb\_node\_id\_trace.log.trace\_id is a trace file describing exactly what happened just before the error occurred. This information is useful for analysis by the NDB Cluster development team.

It is possible to configure the number of these trace files that are created before old files are overwritten. trace\_id is a number which is incremented for each successive trace file.

- ndb\_node\_id\_trace.log.next is the file that keeps track of the next trace file number to be assigned.
- ndb\_node\_id\_out.log is a file containing any data output by the [ndbd](#page-53-0) process. This file is created only if [ndbd](#page-53-0) is started as a daemon, which is the default behavior.
- ndb\_node\_id.pid is a file containing the process ID of the [ndbd](#page-53-0) process when started as a daemon. It also functions as a lock file to avoid the starting of nodes with the same identifier.
- ndb\_node\_id\_signal.log is a file used only in debug versions of [ndbd](#page-53-0), where it is possible to trace all incoming, outgoing, and internal messages with their data in the [ndbd](#page-53-0) process.

It is recommended not to use a directory mounted through NFS because in some environments this can cause problems whereby the lock on the .pid file remains in effect even after the process has terminated.

To start [ndbd](#page-53-0), it may also be necessary to specify the host name of the management server and the port on which it is listening. Optionally, one may also specify the node ID that the process is to use.

```
$> ndbd --connect-string="nodeid=2;host=ndb_mgmd.mysql.com:1186"
```

See Section 25.4.3.3, "NDB Cluster Connection Strings", for additional information about this issue. For more information about data node configuration parameters, see Section 25.4.3.6, "Defining NDB Cluster Data Nodes".

When [ndbd](#page-53-0) starts, it actually initiates two processes. The first of these is called the "angel process"; its only job is to discover when the execution process has been completed, and then to restart the [ndbd](#page-53-0) process if it is configured to do so. Thus, if you attempt to kill [ndbd](#page-53-0) using the Unix kill command, it is necessary to kill both processes, beginning with the angel process. The preferred method of terminating an [ndbd](#page-53-0) process is to use the management client and stop the process from there.

The execution process uses one thread for reading, writing, and scanning data, as well as all other activities. This thread is implemented asynchronously so that it can easily handle thousands of concurrent actions. In addition, a watch-dog thread supervises the execution thread to make sure that it does not hang in an endless loop. A pool of threads handles file I/O, with each thread able to handle one open file. Threads can also be used for transporter connections by the transporters in the [ndbd](#page-53-0) process. In a multi-processor system performing a large number of operations (including updates), the [ndbd](#page-53-0) process can consume up to 2 CPUs if permitted to do so.

For a machine with many CPUs it is possible to use several [ndbd](#page-53-0) processes which belong to different node groups; however, such a configuration is still considered experimental and is not supported for MySQL 8.0 in a production setting. See Section 25.2.7, "Known Limitations of NDB Cluster".

## <span id="page-64-0"></span>**25.5.2 ndbinfo\_select\_all — Select From ndbinfo Tables**

[ndbinfo\\_select\\_all](#page-64-0) is a client program that selects all rows and columns from one or more tables in the ndbinfo database

Not all ndbinfo tables available in the mysql client can be read by this program (see later in this section). In addition, [ndbinfo\\_select\\_all](#page-64-0) can show information about some tables internal to ndbinfo which cannot be accessed using SQL, including the tables and columns metadata tables.

To select from one or more ndbinfo tables using [ndbinfo\\_select\\_all](#page-64-0), it is necessary to supply the names of the tables when invoking the program as shown here:

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

Options that can be used with [ndbinfo\\_select\\_all](#page-64-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.25 Command-line options used with the program ndbinfo\_select\_all**

| Format                                     | Description                                                                                            | Added, Deprecated, or<br>Removed                      |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path                 | Directory containing character<br>sets                                                                 | REMOVED: 8.0.31                                       |
| connect-retries=#                          | Number of times to retry<br>connection before giving up                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                      | Number of seconds to wait<br>between attempts to contact<br>management server                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection-string,       | Same asndb-connectstring                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                       |                                                                                                        |                                                       |
| core-file                                  | Write core file on error; used in<br>debugging                                                         | REMOVED: 8.0.31                                       |
| database=db_name,<br>-d                    | Name of database where table is<br>located                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-extra<br>file=path                | Read given file after global files<br>are read                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                         | Read default options from given<br>file only                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string            | Also read groups with<br>concat(group, suffix)                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| delay=#                                    | Set delay in seconds between<br>loops                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                      | Display help text and exit                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>login-path=path                      | Read given path from login file                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| loops=#,                                   | Set number of times to perform<br>select                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -l                                         |                                                                                                        |                                                       |
| ndb<br>connectstring=connection<br>string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]". | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c                                         | Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                |                                                       |
| ndb-mgmd<br>host=connection-string,        | Same asndb-connectstring                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c<br>ndb-nodeid=#                         | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                             | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                          | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| parallelism=#,<br>-p            | Set degree of parallelism                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,                          | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>version,<br>-V            | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |

#### <span id="page-66-0"></span>• [--character-sets-dir](#page-66-0)

Directory containing character sets.

<span id="page-66-4"></span>• [--core-file](#page-66-4)

Write core file on error; used in debugging.

<span id="page-66-1"></span>• [--connect-retries](#page-66-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-66-2"></span>• [--connect-retry-delay](#page-66-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-66-3"></span>• [--connect-string](#page-66-3)

| Command-Line Format | connect-string=connection-string |
|---------------------|----------------------------------|
| Type                | String                           |

#### ndbinfo\_select\_all — Select From ndbinfo Tables

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Same as [--ndb-connectstring](#page-68-1).

<span id="page-67-0"></span>• [--defaults-extra-file](#page-67-0)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-67-1"></span>• [--defaults-file](#page-67-1)

| Command-Line Format | defaults-file=path |  |
|---------------------|--------------------|--|
| Type                | String             |  |
| Default Value       | [none]             |  |

Read default options from given file only.

<span id="page-67-2"></span>• [--defaults-group-suffix](#page-67-2)

| Command-Line Format | defaults-group-suffix=string |  |
|---------------------|------------------------------|--|
| Type                | String                       |  |
| Default Value       | [none]                       |  |

Also read groups with concat(group, suffix).

<span id="page-67-3"></span>• [--delay=seconds](#page-67-3)

| Command-Line Format | delay=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 5       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of seconds to wait between executing loops. Has no effect if [--loops](#page-68-0) is set to 0 or 1.

<span id="page-67-4"></span>• [--help](#page-67-4)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-67-5"></span>• [--login-path](#page-67-5)

| Command-Line Format | login-path=path |  |
|---------------------|-----------------|--|
| Type                | String          |  |
| Default Value       | [none]          |  |

<span id="page-68-0"></span>• [--loops=number](#page-68-0), -l number

| Command-Line Format | loops=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 1       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of times to execute the select. Use [--delay](#page-67-3) to set the time between loops.

<span id="page-68-1"></span>• [--ndb-connectstring](#page-68-1)

| Command-Line Format | ndb-connectstring=connection<br>string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-68-2"></span>• [--ndb-mgmd-host](#page-68-2)

| Command-Line Format | ndb-mgmd-host=connection-string |  |
|---------------------|---------------------------------|--|
| Type                | String                          |  |
| Default Value       | [none]                          |  |

Same as [--ndb-connectstring](#page-68-1).

<span id="page-68-3"></span>• [--ndb-nodeid](#page-68-3)

| Command-Line Format | ndb-nodeid=# |  |
|---------------------|--------------|--|
| Type                | Integer      |  |
| Default Value       | [none]       |  |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-68-5"></span>• [--ndb-optimized-node-selection](#page-68-5)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-68-4"></span>• [--no-defaults](#page-68-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-68-6"></span>• [--print-defaults](#page-68-6)

| Command-Line Format | print-defaults |
|---------------------|----------------|

<span id="page-69-1"></span>• [--usage](#page-69-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-69-2"></span>• [--version](#page-69-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

[ndbinfo\\_select\\_all](#page-64-0) is unable to read the following tables:

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

# <span id="page-69-0"></span>**25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)**

[ndbmtd](#page-69-0) is a multithreaded version of [ndbd](#page-53-0), the process that is used to handle all the data in tables using the NDBCLUSTER storage engine. [ndbmtd](#page-69-0) is intended for use on host computers having multiple CPU cores. Except where otherwise noted, [ndbmtd](#page-69-0) functions in the same way as [ndbd](#page-53-0); therefore, in this section, we concentrate on the ways in which [ndbmtd](#page-69-0) differs from [ndbd](#page-53-0), and you should consult [Section 25.5.1, "ndbd — The NDB Cluster Data Node Daemon",](#page-53-0) for additional information about running NDB Cluster data nodes that apply to both the single-threaded and multithreaded versions of the data node process.

Command-line options and configuration parameters used with [ndbd](#page-53-0) also apply to [ndbmtd](#page-69-0). For more information about these options and parameters, see [Section 25.5.1, "ndbd — The NDB Cluster Data](#page-53-0) [Node Daemon",](#page-53-0) and Section 25.4.3.6, "Defining NDB Cluster Data Nodes", respectively.

[ndbmtd](#page-69-0) is also file system-compatible with [ndbd](#page-53-0). In other words, a data node running [ndbd](#page-53-0) can be stopped, the binary replaced with [ndbmtd](#page-69-0), and then restarted without any loss of data. (However, when doing this, you must make sure that MaxNoOfExecutionThreads is set to an appropriate value before restarting the node if you wish for [ndbmtd](#page-69-0) to run in multithreaded fashion.) Similarly, an [ndbmtd](#page-69-0) binary can be replaced with [ndbd](#page-53-0) simply by stopping the node and then starting [ndbd](#page-53-0) in place of the multithreaded binary. It is not necessary when switching between the two to start the data node binary using [--initial](#page-59-0).

Using [ndbmtd](#page-69-0) differs from using [ndbd](#page-53-0) in two key respects:

- 1. Because [ndbmtd](#page-69-0) runs by default in single-threaded mode (that is, it behaves like [ndbd](#page-53-0)), you must configure it to use multiple threads. This can be done by setting an appropriate value in the config.ini file for the MaxNoOfExecutionThreads configuration parameter or the ThreadConfig configuration parameter. Using MaxNoOfExecutionThreads is simpler, but ThreadConfig offers more flexibility. For more information about these configuration parameters and their use, see Multi-Threading Configuration Parameters (ndbmtd).
- 2. Trace files are generated by critical errors in [ndbmtd](#page-69-0) processes in a somewhat different fashion from how these are generated by [ndbd](#page-53-0) failures. These differences are discussed in more detail in the next few paragraphs.

Like [ndbd](#page-53-0), [ndbmtd](#page-69-0) generates a set of log files which are placed in the directory specified by DataDir in the config.ini configuration file. Except for trace files, these are generated in the same way and have the same names as those generated by [ndbd](#page-53-0).

In the event of a critical error, [ndbmtd](#page-69-0) generates trace files describing what happened just prior to the error' occurrence. These files, which can be found in the data node's DataDir, are useful for analysis of problems by the NDB Cluster Development and Support teams. One trace file is generated for each [ndbmtd](#page-69-0) thread. The names of these files have the following pattern:

```
ndb_node_id_trace.log.trace_id_tthread_id,
```

In this pattern, node\_id stands for the data node's unique node ID in the cluster, trace\_id is a trace sequence number, and thread\_id is the thread ID. For example, in the event of the failure of an [ndbmtd](#page-69-0) process running as an NDB Cluster data node having the node ID 3 and with MaxNoOfExecutionThreads equal to 4, four trace files are generated in the data node's data directory. If the is the first time this node has failed, then these files are named ndb\_3\_trace.log.1\_t1, ndb\_3\_trace.log.1\_t2, ndb\_3\_trace.log.1\_t3, and ndb\_3\_trace.log.1\_t4. Internally, these trace files follow the same format as [ndbd](#page-53-0) trace files.

The [ndbd](#page-53-0) exit codes and messages that are generated when a data node process shuts down prematurely are also used by [ndbmtd](#page-69-0). See [Data Node Error Messages](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md), for a listing of these.

![](_page_70_Picture_9.jpeg)

### **Note**

It is possible to use [ndbd](#page-53-0) and [ndbmtd](#page-69-0) concurrently on different data nodes in the same NDB Cluster. However, such configurations have not been tested extensively; thus, we cannot recommend doing so in a production setting at this time.

# <span id="page-70-0"></span>**25.5.4 ndb\_mgmd — The NDB Cluster Management Server Daemon**

The management server is the process that reads the cluster configuration file and distributes this information to all nodes in the cluster that request it. It also maintains a log of cluster activities. Management clients can connect to the management server and check the cluster's status.

All options that can be used with [ndb\\_mgmd](#page-70-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.26 Command-line options used with the program ndb\_mgmd**

| Format                        | Description                                                   | Added, Deprecated, or<br>Removed                      |
|-------------------------------|---------------------------------------------------------------|-------------------------------------------------------|
| bind-address=host             | Local bind address                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| character-sets<br>dir=path    | Directory containing character<br>sets                        | REMOVED: 8.0.31                                       |
| cluster-config<br>suffix=name | Override defaults group suffix<br>when reading cluster_config | ADDED: 8.0.24                                         |

| Format                                       | Description                                                                                                           | Added, Deprecated, or<br>Removed                      |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|                                              | sections in my.cnf file; used in<br>testing                                                                           |                                                       |
| config-cache[=TRUE <br>FALSE]                | Enable management server<br>configuration cache; true by<br>default                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| config-file=file,<br>-f file                 | Specify cluster configuration file;<br>also specifyreload orinitial to<br>override configuration cache if             | (Supported in all NDB releases<br>based on MySQL 8.0) |
|                                              | present                                                                                                               |                                                       |
| configdir=directory,<br>config-dir=directory | Specify cluster management<br>server configuration cache<br>directory                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retries=#                            | Number of times to retry<br>connection before giving up                                                               | REMOVED: 8.0.31                                       |
| connect-retry-delay=#                        | Number of seconds to wait<br>between attempts to contact<br>management server                                         | REMOVED: 8.0.31                                       |
| connect<br>string=connection_string,         | Same asndb-connectstring                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                         |                                                                                                                       |                                                       |
| core-file                                    | Write core file on error; used in<br>debugging                                                                        | REMOVED: 8.0.31                                       |
| daemon,                                      | Run ndb_mgmd in daemon<br>mode (default)                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d                                           |                                                                                                                       |                                                       |
| defaults-extra<br>file=path                  | Read given file after global files<br>are read                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                           | Read default options from given<br>file only                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string              | Also read groups with<br>concat(group, suffix)                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                        | Display help text and exit                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                           |                                                                                                                       |                                                       |
| initial                                      | Causes management server to<br>reload configuration data from<br>configuration file, bypassing<br>configuration cache | (Supported in all NDB releases<br>based on MySQL 8.0) |
| install[=name]                               | Used to install management<br>server process as Windows<br>service; does not apply on other<br>platforms              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| interactive                                  | Run ndb_mgmd in interactive<br>mode (not officially supported in<br>production; for testing purposes<br>only)         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| log-name=name                                | Name to use when writing cluster<br>log messages applying to this<br>node                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                  | Description                                                                                                                                                                                         | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| login-path=path                         | Read given path from login file                                                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| mycnf                                   | Read cluster configuration data<br>from my.cnf file                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                                                                                 |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    |                                                                                                                                                                                                     |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                                                       | REMOVED: 8.0.31                                       |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-nodeid-checks                        | Do not perform any node ID<br>checks                                                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nodaemon                                | Do not run ndb_mgmd as a<br>daemon                                                                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nowait-nodes=list                       | Do not wait for management<br>nodes specified when starting<br>this management server;<br>requiresndb-nodeid option                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-full-config,                      | Print full configuration and exit                                                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -P                                      |                                                                                                                                                                                                     |                                                       |
| reload                                  | Causes management server to<br>compare configuration file with<br>configuration cache                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| remove[=name]                           | Used to remove management<br>server process that was<br>previously installed as Windows<br>service, optionally specifying<br>name of service to be removed;<br>does not apply on other<br>platforms | (Supported in all NDB releases<br>based on MySQL 8.0) |
| skip-config-file                        | Do not use configuration file                                                                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format               | Description                                | Added, Deprecated, or<br>Removed                      |
|----------------------|--------------------------------------------|-------------------------------------------------------|
| usage,<br>-?         | Display help text and exit; same<br>ashelp | (Supported in all NDB releases<br>based on MySQL 8.0) |
| verbose,             | Write additional information to<br>log     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -v<br>version,<br>-V | Display version information and<br>exit    | (Supported in all NDB releases<br>based on MySQL 8.0) |

#### <span id="page-73-0"></span>• [--bind-address=](#page-73-0)host

| Command-Line Format | bind-address=host |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | [none]            |

Causes the management server to bind to a specific network interface (host name or IP address). This option has no default value.

<span id="page-73-1"></span>• [--character-sets-dir](#page-73-1)

Directory containing character sets.

<span id="page-73-2"></span>• [cluster-config-suffix](#page-73-2)

| Command-Line Format | cluster-config-suffix=name |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | [none]                     |

Override defaults group suffix when reading cluster configuration sections in my.cnf; used in testing.

<span id="page-73-3"></span>• [--config-cache](#page-73-3)

| Command-Line Format | config-cache[=TRUE FALSE] |
|---------------------|---------------------------|
| Type                | Boolean                   |
| Default Value       | TRUE                      |

This option, whose default value is 1 (or TRUE, or ON), can be used to disable the management server's configuration cache, so that it reads its configuration from config.ini every time it starts (see Section 25.4.3, "NDB Cluster Configuration Files"). You can do this by starting the [ndb\\_mgmd](#page-70-0) process with any one of the following options:

- --config-cache=0
- --config-cache=FALSE
- --config-cache=OFF
- <span id="page-73-4"></span>• [--skip-config-cache](#page-73-4)

Using one of the options just listed is effective only if the management server has no stored configuration at the time it is started. If the management server finds any configuration cache files, then the --config-cache option or the --skip-config-cache option is ignored. Therefore, to disable configuration caching, the option should be used the first time that the management server

is started. Otherwise—that is, if you wish to disable configuration caching for a management server that has already created a configuration cache—you must stop the management server, delete any existing configuration cache files manually, then restart the management server with --skipconfig-cache (or with --config-cache set equal to 0, OFF, or FALSE).

Configuration cache files are normally created in a directory named mysql-cluster under the installation directory (unless this location has been overridden using the [--configdir](#page-74-1) option). Each time the management server updates its configuration data, it writes a new cache file. The files are named sequentially in order of creation using the following format:

```
ndb_node-id_config.bin.seq-number
```

node-id is the management server's node ID; seq-number is a sequence number, beginning with 1. For example, if the management server's node ID is 5, then the first three configuration cache files would, when they are created, be named ndb\_5\_config.bin.1, ndb\_5\_config.bin.2, and ndb\_5\_config.bin.3.

If your intent is to purge or reload the configuration cache without actually disabling caching, you should start [ndb\\_mgmd](#page-70-0) with one of the options [--reload](#page-80-1) or [--initial](#page-76-1) instead of --skipconfig-cache.

To re-enable the configuration cache, simply restart the management server, but without the --config-cache or --skip-config-cache option that was used previously to disable the configuration cache.

[ndb\\_mgmd](#page-70-0) does not check for the configuration directory ([--configdir](#page-74-1)) or attempts to create one when --skip-config-cache is used. (Bug #13428853)

<span id="page-74-0"></span>• [--config-file=](#page-74-0)filename, -f filename

| Command-Line Format | config-file=file |
|---------------------|------------------|
| Disabled by         | skip-config-file |
| Type                | File name        |
| Default Value       | [none]           |

Instructs the management server as to which file it should use for its configuration file. By default, the management server looks for a file named config.ini in the same directory as the [ndb\\_mgmd](#page-70-0) executable; otherwise the file name and location must be specified explicitly.

This option has no default value, and is ignored unless the management server is forced to read the configuration file, either because [ndb\\_mgmd](#page-70-0) was started with the [--reload](#page-80-1) or [--initial](#page-76-1) option, or because the management server could not find any configuration cache. Beginning with NDB 8.0.26, [ndb\\_mgmd](#page-70-0) refuses to start if [--config-file](#page-74-0) is specified without either of [--initial](#page-76-1) or [--reload](#page-80-1).

The [--config-file](#page-74-0) option is also read if [ndb\\_mgmd](#page-70-0) was started with [--config-cache=OFF](#page-73-3). See Section 25.4.3, "NDB Cluster Configuration Files", for more information.

<span id="page-74-1"></span>• [--configdir=](#page-74-1)dir\_name

| Type                | File name            |
|---------------------|----------------------|
|                     | config-dir=directory |
| Command-Line Format | configdir=directory  |

## Default Value \$INSTALLDIR/mysql-cluster

Specifies the cluster management server's configuration cache directory. --config-dir is an alias for this option.

In NDB 8.0.27 and later, this must be an absolute path. Otherwise, the management server refuses to start.

<span id="page-75-0"></span>• [--connect-retries](#page-75-0)

Number of times to retry connection before giving up.

<span id="page-75-1"></span>• [--connect-retry-delay](#page-75-1)

Number of seconds to wait between attempts to contact management server.

<span id="page-75-2"></span>• [--connect-string](#page-75-2)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as --ndb-connectstring.

<span id="page-75-3"></span>• [--core-file](#page-75-3)

Write core file on error; used in debugging.

<span id="page-75-4"></span>• [--daemon](#page-75-4), -d

| Command-Line Format<br>daemon |
|-------------------------------|
|-------------------------------|

Instructs [ndb\\_mgmd](#page-70-0) to start as a daemon process. This is the default behavior.

This option has no effect when running [ndb\\_mgmd](#page-70-0) on Windows platforms.

<span id="page-75-5"></span>• [--defaults-extra-file](#page-75-5)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-75-6"></span>• [--defaults-file](#page-75-6)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-75-7"></span>• [--defaults-group-suffix](#page-75-7)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-76-0"></span>• [--help](#page-76-0)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-76-1"></span>• [--initial](#page-76-1)

| Command-Line Format | initial |
|---------------------|---------|
|                     |         |

Configuration data is cached internally, rather than being read from the cluster global configuration file each time the management server is started (see Section 25.4.3, "NDB Cluster Configuration Files"). Using the --initial option overrides this behavior, by forcing the management server to delete any existing cache files, and then to re-read the configuration data from the cluster configuration file and to build a new cache.

This differs in two ways from the [--reload](#page-80-1) option. First, --reload forces the server to check the configuration file against the cache and reload its data only if the contents of the file are different from the cache. Second, --reload does not delete any existing cache files.

If [ndb\\_mgmd](#page-70-0) is invoked with --initial but cannot find a global configuration file, the management server cannot start.

When a management server starts, it checks for another management server in the same NDB Cluster and tries to use the other management server's configuration data. This behavior has implications when performing a rolling restart of an NDB Cluster with multiple management nodes. See Section 25.6.5, "Performing a Rolling Restart of an NDB Cluster", for more information.

When used together with the [--config-file](#page-74-0) option, the cache is cleared only if the configuration file is actually found.

<span id="page-76-2"></span>• [--install\[=](#page-76-2)name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndb_mgmd       |

Causes [ndb\\_mgmd](#page-70-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndb\_mgmd. Although it is preferable to specify other [ndb\\_mgmd](#page-70-0) program options in a my.ini or my.cnf configuration file, it is possible to use them together with [--install](#page-76-2). However, in such cases, the [--install](#page-76-2) option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-59-0) option, since this causes the configuration cache to be wiped and rebuilt every time the service is stopped and started. Care should also be taken if you intend to use any other [ndb\\_mgmd](#page-70-0) options that affect the starting of the management server, and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-76-2) option has no effect on non-Windows platforms.

### <span id="page-77-0"></span>• [--interactive](#page-77-0)

| Command-Line Format | interactive |
|---------------------|-------------|
|---------------------|-------------|

Starts [ndb\\_mgmd](#page-70-0) in interactive mode; that is, an [ndb\\_mgm](#page-81-0) client session is started as soon as the management server is running. This option does not start any other NDB Cluster nodes.

#### <span id="page-77-1"></span>• [--log-name=](#page-77-1)name

| Command-Line Format | log-name=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | MgmtSrvr      |

Provides a name to be used for this node in the cluster log.

#### <span id="page-77-2"></span>• [--login-path](#page-77-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

#### <span id="page-77-3"></span>• [--mycnf](#page-77-3)

| Command-Line Format | mycnf |
|---------------------|-------|
|---------------------|-------|

Read configuration data from the my.cnf file.

#### <span id="page-77-4"></span>• [--ndb-connectstring](#page-77-4)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string. Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf. Ignored if [--config-file](#page-74-0) is specified; beginning with NDB 8.0.27, a warning is issued when both options are used.

#### <span id="page-77-5"></span>• [--ndb-mgmd-host](#page-77-5)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as --ndb-connectstring.

#### <span id="page-77-6"></span>• [--ndb-nodeid](#page-77-6)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

<span id="page-78-1"></span>• [--ndb-optimized-node-selection](#page-78-1)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-78-3"></span>• [--no-nodeid-checks](#page-78-3)

| Command-Line Format | no-nodeid-checks |
|---------------------|------------------|
|---------------------|------------------|

Do not perform any checks of node IDs.

<span id="page-78-4"></span>• [--nodaemon](#page-78-4)

| Command-Line Format | nodaemon |
|---------------------|----------|
|---------------------|----------|

Instructs [ndb\\_mgmd](#page-70-0) not to start as a daemon process.

The default behavior for [ndb\\_mgmd](#page-70-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms.

<span id="page-78-2"></span>• [--no-defaults](#page-78-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-78-0"></span>• [--nowait-nodes](#page-78-0)

| Command-Line Format | nowait-nodes=list |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | [none]            |
| Minimum Value       | 1                 |
| Maximum Value       | 255               |

When starting an NDB Cluster is configured with two management nodes, each management server normally checks to see whether the other [ndb\\_mgmd](#page-70-0) is also operational and whether the other management server's configuration is identical to its own. However, it is sometimes desirable to start the cluster with only one management node (and perhaps to allow the other [ndb\\_mgmd](#page-70-0) to be started later). This option causes the management node to bypass any checks for any other management nodes whose node IDs are passed to this option, permitting the cluster to start as though configured to use only the management node that was started.

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
                                                                                              4449
```

```
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

As shown in the preceding example, when using [--nowait-nodes](#page-78-0), you must also use the [--ndb](#page-77-6)[nodeid](#page-77-6) option to specify the node ID of this [ndb\\_mgmd](#page-70-0) process.

You can then start each of the cluster's data nodes in the usual way. If you wish to start and use the second management server in addition to the first management server at a later time without restarting the data nodes, you must start each data node with a connection string that references both management servers, like this:

```
$> ndbd -c 198.51.100.150,198.51.100.151
```

The same is true with regard to the connection string used with any mysqld processes that you wish to start as NDB Cluster SQL nodes connected to this cluster. See Section 25.4.3.3, "NDB Cluster Connection Strings", for more information.

When used with [ndb\\_mgmd](#page-70-0), this option affects the behavior of the management node with regard to other management nodes only. Do not confuse it with the [--nowait-nodes](#page-62-0) option used with [ndbd](#page-53-0) or [ndbmtd](#page-69-0) to permit a cluster to start with fewer than its full complement of data nodes; when used with data nodes, this option affects their behavior only with regard to other data nodes.

Multiple management node IDs may be passed to this option as a comma-separated list. Each node ID must be no less than 1 and no greater than 255. In practice, it is quite rare to use more than two management servers for the same NDB Cluster (or to have any need for doing so); in most cases you need to pass to this option only the single node ID for the one management server that you do not wish to use when starting the cluster.

![](_page_79_Picture_10.jpeg)

#### **Note**

When you later start the "missing" management server, its configuration must match that of the management server that is already in use by the cluster. Otherwise, it fails the configuration check performed by the existing management server, and does not start.

<span id="page-79-0"></span>• [--print-defaults](#page-79-0)

| Command-Line Format<br>print-defaults |
|---------------------------------------|
|---------------------------------------|

Print program argument list and exit.

<span id="page-80-0"></span>• [--print-full-config](#page-80-0), -P

| Command-Line Format | print-full-config |
|---------------------|-------------------|
|---------------------|-------------------|

Shows extended information regarding the configuration of the cluster. With this option on the command line the [ndb\\_mgmd](#page-70-0) process prints information about the cluster setup including an extensive list of the cluster configuration sections as well as parameters and their values. Normally used together with the [--config-file](#page-74-0) (-f) option.

<span id="page-80-1"></span>• [--reload](#page-80-1)

| Command-Line Format | reload |
|---------------------|--------|
|---------------------|--------|

NDB Cluster configuration data is stored internally rather than being read from the cluster global configuration file each time the management server is started (see Section 25.4.3, "NDB Cluster Configuration Files"). Using this option forces the management server to check its internal data store against the cluster configuration file and to reload the configuration if it finds that the configuration file does not match the cache. Existing configuration cache files are preserved, but not used.

This differs in two ways from the [--initial](#page-76-1) option. First, --initial causes all cache files to be deleted. Second, --initial forces the management server to re-read the global configuration file and construct a new cache.

If the management server cannot find a global configuration file, then the --reload option is ignored.

When --reload is used, the management server must be able to communicate with data nodes and any other management servers in the cluster before it attempts to read the global configuration file; otherwise, the management server fails to start. This can happen due to changes in the networking environment, such as new IP addresses for nodes or an altered firewall configuration. In such cases, you must use [--initial](#page-76-1) instead to force the existing cached configuration to be discarded and reloaded from the file. See Section 25.6.5, "Performing a Rolling Restart of an NDB Cluster", for additional information.

<span id="page-80-2"></span>• [--remove\[=name\]](#page-80-2)

| Command-Line Format | remove[=name] |
|---------------------|---------------|
| Platform Specific   | Windows       |
| Type                | String        |
| Default Value       | ndb_mgmd      |

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-80-3"></span>• [--skip-config-file](#page-80-3)

| Command-Line Format | skip-config-file |
|---------------------|------------------|

Do not read cluster configuration file; ignore [--initial](#page-76-1) and [--reload](#page-80-1) options if specified.

<span id="page-80-4"></span>• [--usage](#page-80-4)

| Command-Line Format | usage |
|---------------------|-------|

<span id="page-81-1"></span>• [--verbose](#page-81-1), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-81-2"></span>• [--version](#page-81-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

It is not strictly necessary to specify a connection string when starting the management server. However, if you are using more than one management server, a connection string should be provided and each node in the cluster should specify its node ID explicitly.

See Section 25.4.3.3, "NDB Cluster Connection Strings", for information about using connection strings. [Section 25.5.4, "ndb\\_mgmd — The NDB Cluster Management Server Daemon"](#page-70-0), describes other options for [ndb\\_mgmd](#page-70-0).

The following files are created or used by [ndb\\_mgmd](#page-70-0) in its starting directory, and are placed in the DataDir as specified in the config.ini configuration file. In the list that follows, node\_id is the unique node identifier.

- config.ini is the configuration file for the cluster as a whole. This file is created by the user and read by the management server. Section 25.4, "Configuration of NDB Cluster", discusses how to set up this file.
- ndb\_node\_id\_cluster.log is the cluster events log file. Examples of such events include checkpoint startup and completion, node startup events, node failures, and levels of memory usage. A complete listing of cluster events with descriptions may be found in Section 25.6, "Management of NDB Cluster".

By default, when the size of the cluster log reaches one million bytes, the file is renamed to ndb\_node\_id\_cluster.log.seq\_id, where seq\_id is the sequence number of the cluster log file. (For example: If files with the sequence numbers 1, 2, and 3 already exist, the next log file is named using the number 4.) You can change the size and number of files, and other characteristics of the cluster log, using the LogDestination configuration parameter.

- ndb\_node\_id\_out.log is the file used for stdout and stderr when running the management server as a daemon.
- ndb\_node\_id.pid is the process ID file used when running the management server as a daemon.

# <span id="page-81-0"></span>**25.5.5 ndb\_mgm — The NDB Cluster Management Client**

The [ndb\\_mgm](#page-81-0) management client process is actually not needed to run the cluster. Its value lies in providing a set of commands for checking the cluster's status, starting backups, and performing other administrative functions. The management client accesses the management server using a C API. Advanced users can also employ this API for programming dedicated management processes to perform tasks similar to those performed by [ndb\\_mgm](#page-81-0).

To start the management client, it is necessary to supply the host name and port number of the management server:

```
$> ndb_mgm [host_name [port_num]]
```

For example:

```
$> ndb_mgm ndb_mgmd.mysql.com 1186
```

The default host name and port number are localhost and 1186, respectively.

All options that can be used with [ndb\\_mgm](#page-81-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.27 Command-line options used with the program ndb\_mgm**

| Format                               | Description                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| backup-password-from<br>stdin        | Get decryption password in a<br>secure fashion from STDIN;<br>use together withexecute and<br>ndb_mgm START BACKUP<br>command | ADDED: NDB 8.0.24                                     |
| character-sets<br>dir=path           | Directory containing character<br>sets                                                                                        | REMOVED: 8.0.31                                       |
| connect-retries=#                    | Set number of times to retry<br>connection before giving up; 0<br>means 1 attempt only (and no<br>retries)                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                 |                                                                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                                                                | REMOVED: 8.0.31                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                   | Read default options from given<br>file only                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| encrypt-backup                       | Cause START BACKUP to<br>encrypt whenever making a<br>backup, prompting for password<br>if not supplied by user               | ADDED: NDB 8.0.24                                     |
| execute=command,                     | Execute command and exit                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -e command<br>help,                  | Display help text and exit                                                                                                    | (Supported in all NDB releases                        |
| -?                                   |                                                                                                                               | based on MySQL 8.0)                                   |
| login-path=path                      | Read given path from login file                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb                                  | Set connect string for                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,     | connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                              | based on MySQL 8.0)                                   |
| -c connection_string                 | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                           |                                                       |
| ndb-mgmd<br>host=connection_string,  | Same asndb-connectstring                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                          | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -c connection_string            |                                                                                                                                               |                                                       |
| ndb-nodeid=#                    | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| try-reconnect=#,                | Set number of times to retry<br>connection before giving up;                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -t #                            | synonym forconnect-retries                                                                                                                    |                                                       |
| usage,                          | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                              |                                                                                                                                               |                                                       |
| version,                        | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                              |                                                                                                                                               |                                                       |

<span id="page-83-0"></span>• [--backup-password-from-stdin\[=TRUE|FALSE\]](#page-83-0)

| Command-Line Format | backup-password-from-stdin |
|---------------------|----------------------------|
|---------------------|----------------------------|

This option enables input of the backup password from the system shell (stdin) when using - execute "START BACKUP" or similar to create a backup. Use of this option requires use of [-](#page-84-6) [execute](#page-84-6) as well.

<span id="page-83-1"></span>• [--character-sets-dir](#page-83-1)

Directory containing character sets.

<span id="page-83-2"></span>• [--connect-retries=](#page-83-2)#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 3                 |
| Minimum Value       | 0                 |
| Maximum Value       | 4294967295        |

This option specifies the number of times following the first attempt to retry a connection before giving up (the client always tries the connection at least once). The length of time to wait per attempt is set using [--connect-retry-delay](#page-75-1).

This option is synonymous with the [--try-reconnect](#page-86-3) option, which is now deprecated.

<span id="page-83-3"></span>• [--connect-retry-delay](#page-83-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
|---------------------|-----------------------|

| Type          | Integer |
|---------------|---------|
| Default Value | 5       |
| Minimum Value | 0       |
| Maximum Value | 5       |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-84-0"></span>• [--connect-string](#page-84-0)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-85-2).

<span id="page-84-1"></span>• [--core-file](#page-84-1)

Write core file on error; used in debugging.

<span id="page-84-2"></span>• [--defaults-extra-file](#page-84-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-84-3"></span>• [--defaults-file](#page-84-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-84-4"></span>• [--defaults-group-suffix](#page-84-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-84-5"></span>• [--encrypt-backup](#page-84-5)

| Command-Line Format | encrypt-backup |
|---------------------|----------------|
|---------------------|----------------|

When used, this option causes all backups to be encrypted. To make this happen whenever [ndb\\_mgm](#page-81-0) is run, put the option in the [ndb\_mgm] section of the my.cnf file.

<span id="page-84-6"></span>• [--execute=command](#page-84-6), -e command

| Command-Line Format | execute=command |
|---------------------|-----------------|

This option can be used to send a command to the NDB Cluster management client from the system shell. For example, either of the following is equivalent to executing SHOW in the management client:

```
$> ndb_mgm -e "SHOW"
$> ndb_mgm --execute="SHOW"
```

This is analogous to how the --execute or -e option works with the mysql command-line client. See Section 6.2.2.1, "Using Options on the Command Line".

![](_page_85_Picture_3.jpeg)

#### **Note**

If the management client command to be passed using this option contains any space characters, then the command must be enclosed in quotation marks. Either single or double quotation marks may be used. If the management client command contains no space characters, the quotation marks are optional.

<span id="page-85-0"></span>• [--help](#page-85-0)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-85-1"></span>• [--login-path](#page-85-1)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-85-2"></span>• [--ndb-connectstring](#page-85-2)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to [ndb\\_mgmd](#page-70-0). Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-85-4"></span>• [--ndb-nodeid](#page-85-4)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-85-2).

<span id="page-85-3"></span>• [--ndb-mgmd-host](#page-85-3)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

<span id="page-86-0"></span>• [--ndb-optimized-node-selection](#page-86-0)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-86-1"></span>• [--no-defaults](#page-86-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-86-2"></span>• [--print-defaults](#page-86-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-86-3"></span>• [--try-reconnect=](#page-86-3)number

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

This option is deprecated and subject to removal in a future release. Use [--connect-retries](#page-83-2), instead.

<span id="page-86-4"></span>• [--usage](#page-86-4)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-85-0).

<span id="page-86-5"></span>• [--version](#page-86-5)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

Additional information about using [ndb\\_mgm](#page-81-0) can be found in Section 25.6.1, "Commands in the NDB Cluster Management Client".

# <span id="page-86-6"></span>**25.5.6 ndb\_blob\_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables**

This tool can be used to check for and remove orphaned BLOB column parts from NDB tables, as well as to generate a file listing any orphaned parts. It is sometimes useful in diagnosing and repairing corrupted or damaged NDB tables containing BLOB or TEXT columns.

The basic syntax for [ndb\\_blob\\_tool](#page-86-6) is shown here:

```
ndb_blob_tool [options] table [column, ...]
```

Unless you use the [--help](#page-90-0) option, you must specify an action to be performed by including one or more of the options [--check-orphans](#page-89-0), [--delete-orphans](#page-90-1), or [--dump-file](#page-90-2). These options cause [ndb\\_blob\\_tool](#page-86-6) to check for orphaned BLOB parts, remove any orphaned BLOB parts, and generate a dump file listing orphaned BLOB parts, respectively, and are described in more detail later in this section.

You must also specify the name of a table when invoking [ndb\\_blob\\_tool](#page-86-6). In addition, you can optionally follow the table name with the (comma-separated) names of one or more BLOB or TEXT columns from that table. If no columns are listed, the tool works on all of the table's BLOB and TEXT columns. If you need to specify a database, use the [--database](#page-89-1) (-d) option.

The [--verbose](#page-91-0) option provides additional information in the output about the tool's progress.

All options that can be used with [ndb\\_mgmd](#page-70-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.28 Command-line options used with the program ndb\_blob\_tool**

| Format                                 | Description                                                                              | Added, Deprecated, or<br>Removed                      |
|----------------------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------|
| add-missing                            | Write dummy blob parts to take<br>place of those which are missing                       | ADDED: NDB 8.0.20                                     |
| character-sets<br>dir=path             | Directory containing character<br>sets                                                   | REMOVED: 8.0.31                                       |
| check-missing                          | Check for blobs having inline<br>parts but missing one or more<br>parts from parts table | ADDED: NDB 8.0.20                                     |
| check-orphans                          | Check for blob parts having no<br>corresponding inline parts                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retries=#                      | Number of times to retry<br>connection before giving up                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                  | Number of seconds to wait<br>between attempts to contact<br>management server            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string,   | Same asndb-connectstring                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>core-file      | Write core file on error; used in<br>debugging                                           | REMOVED: 8.0.31                                       |
| database=name,                         | Database to find the table in                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name<br>defaults-extra<br>file=path | Read given file after global files<br>are read                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                     | Read default options from given<br>file only                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string        | Also read groups with<br>concat(group, suffix)                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| delete-orphans                         | Delete blob parts having no<br>corresponding inline parts                                | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                                          | Description                                                                                                                                             | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| dump-file=file                                                  | Write orphan keys to specified<br>file                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                                           | Display help text and exit                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>login-path=path                                           | Read given path from login file                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-mgmd<br>host=connection_string,                             | my.cnf<br>Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable           | REMOVED: 8.0.31                                       |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                                                  | Print program argument list and<br>exit                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,                                                          | Display help text and exit; same<br>ashelp                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>verbose,                                                  | Verbose output                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -v<br>version,                                                  | Display version information and<br>exit                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                                                              |                                                                                                                                                         |                                                       |

<span id="page-88-0"></span>• [--add-missing](#page-88-0)

| Command-Line Format | add-missing |
|---------------------|-------------|
|---------------------|-------------|

For each inline part in NDB Cluster tables which has no corresponding BLOB part, write a dummy BLOB part of the required length, consisting of spaces.

<span id="page-88-1"></span>• [--character-sets-dir](#page-88-1)

Directory containing character sets.

<span id="page-89-2"></span>• [--check-missing](#page-89-2)

| Command-Line Format | check-missing |
|---------------------|---------------|
|---------------------|---------------|

Check for inline parts in NDB Cluster tables which have no corresponding BLOB parts.

<span id="page-89-0"></span>• [--check-orphans](#page-89-0)

| Command-Line Format | check-orphans |
|---------------------|---------------|
|---------------------|---------------|

Check for BLOB parts in NDB Cluster tables which have no corresponding inline parts.

<span id="page-89-3"></span>• [--connect-retries](#page-89-3)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-89-4"></span>• [--connect-retry-delay](#page-89-4)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-89-5"></span>• [--connect-string](#page-89-5)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-90-6).

<span id="page-89-6"></span>• [--core-file](#page-89-6)

Write core file on error; used in debugging.

<span id="page-89-1"></span>• [--database=](#page-89-1)db\_name, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [none]        |

Specify the database to find the table in.

<span id="page-89-7"></span>• [--defaults-extra-file](#page-89-7)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read given file after global files are read.

#### <span id="page-90-3"></span>• [--defaults-file](#page-90-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

#### <span id="page-90-4"></span>• [--defaults-group-suffix](#page-90-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

#### <span id="page-90-1"></span>• [--delete-orphans](#page-90-1)

| Command-Line Format |                |
|---------------------|----------------|
|                     | delete-orphans |

Remove BLOB parts from NDB Cluster tables which have no corresponding inline parts.

#### <span id="page-90-2"></span>• [--dump-file=](#page-90-2)file

| Command-Line Format | dump-file=file |  |
|---------------------|----------------|--|
| Type                | File name      |  |
| Default Value       | [none]         |  |

Writes a list of orphaned BLOB column parts to file. The information written to the file includes the table key and BLOB part number for each orphaned BLOB part.

#### <span id="page-90-0"></span>• [--help](#page-90-0)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

#### <span id="page-90-5"></span>• [--login-path](#page-90-5)

| Command-Line Format | login-path=path |  |
|---------------------|-----------------|--|
| Type                | String          |  |
| Default Value       | [none]          |  |

Read given path from login file.

#### <span id="page-90-6"></span>• [--ndb-connectstring](#page-90-6)

| Command-Line Format | ndb<br>connectstring=connection_string |  |
|---------------------|----------------------------------------|--|
| Type                | String                                 |  |

Default Value [none]

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-91-1"></span>• [--ndb-mgmd-host](#page-91-1)

| Command-Line Format | ndb-mgmd-host=connection_string |  |
|---------------------|---------------------------------|--|
| Type                | String                          |  |
| Default Value       | [none]                          |  |

Same as [--ndb-connectstring](#page-90-6).

<span id="page-91-2"></span>• [--ndb-nodeid](#page-91-2)

| Command-Line Format | ndb-nodeid=# |  |
|---------------------|--------------|--|
| Type                | Integer      |  |
| Default Value       | [none]       |  |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-91-3"></span>• [--ndb-optimized-node-selection](#page-91-3)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-91-4"></span>• [--no-defaults](#page-91-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-91-5"></span>• [--print-defaults](#page-91-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-91-6"></span>• [--usage](#page-91-6)

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Display help text and exit; same as --help.

<span id="page-91-0"></span>• [--verbose](#page-91-0)

| Command-Line Format | verbose |
|---------------------|---------|

Provide extra information in the tool's output regarding its progress.

<span id="page-91-7"></span>• [--version](#page-91-7)

| Command-Line Format | version |
|---------------------|---------|
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

When run with [--check-orphans](#page-89-0) against this table, [ndb\\_blob\\_tool](#page-86-6) generates the following output:

```
$> ndb_blob_tool --check-orphans --verbose -d test btest
connected
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

# <span id="page-92-0"></span>**25.5.7 ndb\_config — Extract NDB Cluster Configuration Information**

This tool extracts current configuration information for data nodes, SQL nodes, and API nodes from one of a number of sources: an NDB Cluster management node, or its config.ini or my.cnf file. By default, the management node is the source for the configuration data; to override the default, execute ndb\_config with the [--config-file](#page-97-0) or [--mycnf](#page-98-0) option. It is also possible to use a data node as the source by specifying its node ID with [--config\\_from\\_node=](#page-97-1)node\_id.

[ndb\\_config](#page-92-0) can also provide an offline dump of all configuration parameters which can be used, along with their default, maximum, and minimum values and other information. The dump can be produced in either text or XML format; for more information, see the discussion of the [--configinfo](#page-95-0) and [--xml](#page-100-0) options later in this section).

You can filter the results by section (DB, SYSTEM, or CONNECTIONS) using one of the options [-](#page-99-0) [nodes](#page-99-0), [--system](#page-100-1), or [--connections](#page-97-2).

All options that can be used with [ndb\\_config](#page-92-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.29 Command-line options used with the program ndb\_config**

| Format                               | Description                                                                                                                                                                                                            | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                                                                                                                                                                 | REMOVED: 8.0.31                                       |
| cluster-config<br>suffix=name        | Override defaults group suffix<br>when reading cluster_config<br>sections in my.cnf file; used in<br>testing                                                                                                           | ADDED: NDB 8.0.24                                     |
| config-binary<br>file=path/to/file   | Read this binary configuration file ADDED: NDB 8.0.32                                                                                                                                                                  |                                                       |
| config-file=file_name                | Set the path to config.ini file                                                                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| config-from-node=#                   | Obtain configuration data from<br>the node having this ID (must be<br>a data node)                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| configinfo                           | Dumps information about all<br>NDB configuration parameters<br>in text format with default,<br>maximum, and minimum values.<br>Use withxml to obtain XML<br>output                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connections                          | Print information only about<br>connections specified in [tcp],<br>[tcp default], [sci], [sci default],<br>[shm], or [shm default] sections<br>of cluster configuration file.<br>Cannot be used withsystem or<br>nodes | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                                                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                 |                                                                                                                                                                                                                        |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                                                                                                                                                         | REMOVED: 8.0.31                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                                                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                   | Read default options from given<br>file only                                                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                                                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| diff-default                         | Print only configuration<br>parameters that have non-default<br>values                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields=string,                       | Field separator                                                                                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -f                                   |                                                                                                                                                                                                                        |                                                       |

| Format                                                          | Description                                                                                                                                             | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| help,<br>-?                                                     | Display help text and exit                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| host=name                                                       | Specify host                                                                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                                                 | Read given path from login file                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| mycnf                                                           | Read configuration data from<br>my.cnf file                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-mgmd<br>host=connection_string,                             | my.cnf<br>Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                              | REMOVED: 8.0.31                                       |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable           | REMOVED: 8.0.31                                       |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nodeid=#                                                        | Get configuration of node with<br>this ID                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| nodes                                                           | Print node information ([ndbd] or<br>[ndbd default] section of cluster<br>configuration file) only. Cannot<br>be used withsystem or<br>connections      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| query=string,                                                   | One or more query options<br>(attributes)                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -q string<br>query-all,                                         | Dumps all parameters and<br>values to a single comma                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -a                                                              | delimited string                                                                                                                                        |                                                       |
| print-defaults                                                  | Print program argument list and<br>exit                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| rows=string,                                                    | Row separator                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -r string                                                       |                                                                                                                                                         |                                                       |
| system                                                          | Print SYSTEM section<br>information only (see ndb_config                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format         | Description                                                                                                                                    | Added, Deprecated, or<br>Removed                      |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|                | configinfo output). Cannot<br>be used withnodes or<br>connections                                                                              |                                                       |
| type=name      | Specify node type                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,<br>-?   | Display help text and exit; same<br>ashelp                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| version,<br>-V | Display version information and<br>exit                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| configinfoxml  | Usexml withconfiginfo<br>to obtain a dump of all NDB<br>configuration parameters in XML<br>format with default, maximum,<br>and minimum values | (Supported in all NDB releases<br>based on MySQL 8.0) |

<span id="page-95-1"></span>• [cluster-config-suffix](#page-95-1)

| Command-Line Format | cluster-config-suffix=name |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | [none]                     |

Override defaults group suffix when reading cluster configuration sections in my.cnf; used in testing.

<span id="page-95-0"></span>• [--configinfo](#page-95-0)

The --configinfo option causes [ndb\\_config](#page-92-0) to dump a list of each NDB Cluster configuration parameter supported by the NDB Cluster distribution of which [ndb\\_config](#page-92-0) is a part, including the following information:

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
```

```
Default: 0 (Min: 0, Max: 4294967039)
****** DB ******
MaxNoOfSubscriptions (Non-negative Integer)
Max no of subscriptions (default 0 == MaxNoOfTables)
Default: 0 (Min: 0, Max: 4294967039)
MaxNoOfSubscribers (Non-negative Integer)
Max no of subscribers (default 0 == 2 * MaxNoOfTables)
Default: 0 (Min: 0, Max: 4294967039)
…
```

Use this option together with the [--xml](#page-100-0) option to obtain output in XML format.

<span id="page-96-0"></span>• [--config-binary-file=](#page-96-0)path-to-file

| Command-Line Format | config-binary-file=path/to/file |
|---------------------|---------------------------------|
| Type                | File name                       |
| Default Value       |                                 |

Gives the path to the management server's cached binary configuration file (ndb\_nodeID\_config.bin.seqno). This may be a relative or absolute path. If the management server and the [ndb\\_config](#page-92-0) binary used reside on different hosts, you must use an absolute path.

This example demonstrates combining --config-binary-file with other [ndb\\_config](#page-92-0) options to obtain useful output:

```
> ndb_config --config-binary-file=ndb_50_config.bin.1 --diff-default --type=ndbd
config of [DB] node id 5 that is different from default 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
NodeId,5,(mandatory) 
BackupDataDir,/home/jon/data/8.0,(null) 
DataDir,/home/jon/data/8.0,. 
DataMemory,2G,98M 
FileSystemPath,/home/jon/data/8.0,(null) 
HostName,127.0.0.1,localhost 
Nodegroup,0,(null) 
ThreadConfig,,(null) 
config of [DB] node id 6 that is different from default 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
NodeId,6,(mandatory) 
BackupDataDir,/home/jon/data/8.0,(null) 
DataDir,/home/jon/data/8.0,. 
DataMemory,2G,98M 
FileSystemPath,/home/jon/data/8.0,(null) 
HostName,127.0.0.1,localhost 
Nodegroup,0,(null) 
ThreadConfig,,(null)
> ndb_config --config-binary-file=ndb_50_config.bin.1 --diff-default --system
config of [SYSTEM] system 
CONFIG_PARAMETER,ACTUAL_VALUE,DEFAULT_VALUE 
Name,MC_20220216092809,(mandatory) 
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
```

```
[ndbd]
NodeId= 5
HostName= 127.0.0.1
DataDir= /home/jon/data/8.0
[ndbd]
NodeId= 6
HostName= 127.0.0.1
DataDir= /home/jon/data/8.0
```

By comparing the output with the configuration file, you can see that all of the settings in the file have been written by the management server to the binary cache, and thus, applied to the cluster.

#### <span id="page-97-0"></span>• [--config-file=](#page-97-0)path-to-file

| Command-Line Format | config-file=file_name |
|---------------------|-----------------------|
| Type                | File name             |
| Default Value       |                       |

Gives the path to the cluster configuration file (config.ini). This may be a relative or absolute path. If the management server and the [ndb\\_config](#page-92-0) binary used reside on different hosts, you must use an absolute path.

### <span id="page-97-1"></span>• [--config\\_from\\_node=#](#page-97-1)

| Command-Line Format | config-from-node=# |
|---------------------|--------------------|
| Type                | Numeric            |
| Default Value       | none               |
| Minimum Value       | 1                  |
| Maximum Value       | 48                 |

Obtain the cluster's configuration data from the data node that has this ID.

If the node having this ID is not a data node, [ndb\\_config](#page-92-0) fails with an error. (To obtain configuration data from the management node instead, simply omit this option.)

#### <span id="page-97-2"></span>• [--connections](#page-97-2)

| Command-Line Format | connections |
|---------------------|-------------|
|---------------------|-------------|

Tells [ndb\\_config](#page-92-0) to print CONNECTIONS information only—that is, information about parameters found in the [tcp], [tcp default], [shm], or [shm default] sections of the cluster configuration file (see [Section 25.4.3.10, "NDB Cluster TCP/IP Connections",](#page-33-6) and [Section 25.4.3.12,](#page-41-1) ["NDB Cluster Shared-Memory Connections"](#page-41-1), for more information).

This option is mutually exclusive with [--nodes](#page-99-0) and [--system](#page-100-1); only one of these 3 options can be used.

#### <span id="page-97-3"></span>• [--diff-default](#page-97-3)

| Command-Line Format | diff-default |
|---------------------|--------------|
|---------------------|--------------|

Print only configuration parameters that have non-default values.

#### <span id="page-97-4"></span>• [--fields=](#page-97-4)delimiter, -f delimiter

| Command-Line Format | fields=string |
|---------------------|---------------|
| Type                | String        |

| Default Value |  |
|---------------|--|
|---------------|--|

Specifies a delimiter string used to separate the fields in the result. The default is , (the comma character).

![](_page_98_Picture_3.jpeg)

#### **Note**

If the delimiter contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

#### <span id="page-98-1"></span>• --host=[hostname](#page-98-1)

| Command-Line Format | host=name |
|---------------------|-----------|
| Type                | String    |
| Default Value       |           |

Specifies the host name of the node for which configuration information is to be obtained.

![](_page_98_Picture_9.jpeg)

#### **Note**

While the hostname localhost usually resolves to the IP address 127.0.0.1, this may not necessarily be true for all operating platforms and configurations. This means that it is possible, when localhost is used in config.ini, for [ndb\\_config --host=localhost](#page-92-0) to fail if [ndb\\_config](#page-92-0) is run on a different host where localhost resolves to a different address (for example, on some versions of SUSE Linux, this is 127.0.0.2). In general, for best results, you should use numeric IP addresses for all NDB Cluster configuration values relating to hosts, or verify that all NDB Cluster hosts handle localhost in the same fashion.

#### <span id="page-98-0"></span>• [--mycnf](#page-98-0)

| Command-Line Format | mycnf |
|---------------------|-------|
|---------------------|-------|

Read configuration data from the my.cnf file.

<span id="page-98-2"></span>• [--ndb-connectstring=](#page-98-2)connection\_string, -c connection\_string

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Specifies the connection string to use in connecting to the management server. The format for the connection string is the same as described in Section 25.4.3.3, "NDB Cluster Connection Strings", and defaults to localhost:1186.

<span id="page-98-3"></span>• [--no-defaults](#page-98-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-98-4"></span>• [--nodeid=](#page-98-4)node\_id

#### <span id="page-99-0"></span>• [--nodes](#page-99-0)

| Command-Line Format | nodes |
|---------------------|-------|
|---------------------|-------|

Tells [ndb\\_config](#page-92-0) to print information relating only to parameters defined in an [ndbd] or [ndbd default] section of the cluster configuration file (see Section 25.4.3.6, "Defining NDB Cluster Data Nodes").

This option is mutually exclusive with [--connections](#page-97-2) and [--system](#page-100-1); only one of these 3 options can be used.

<span id="page-99-1"></span>• --query=[query-options](#page-99-1), -q query-options

| Command-Line Format | query=string |
|---------------------|--------------|
| Type                | String       |
| Default Value       |              |

This is a comma-delimited list of query options—that is, a list of one or more node attributes to be returned. These include nodeid (node ID), type (node type—that is, ndbd, mysqld, or ndb\_mgmd), and any configuration parameters whose values are to be obtained.

For example, --query=nodeid,type,datamemory,datadir returns the node ID, node type, DataMemory, and DataDir for each node.

![](_page_99_Picture_9.jpeg)

#### **Note**

If a given parameter is not applicable to a certain type of node, than an empty string is returned for the corresponding value. See the examples later in this section for more information.

<span id="page-99-2"></span>• [--query-all](#page-99-2), -a

| Command-Line Format | query-all |
|---------------------|-----------|
| Type                | String    |
| Default Value       |           |

Returns a comma-delimited list of all query options (node attributes; note that this list is a single string.

<span id="page-99-3"></span>• --rows=[separator](#page-99-3), -r separator

| Command-Line Format | rows=string |
|---------------------|-------------|
| Type                | String      |
| Default Value       |             |

Specifies a separator string used to separate the rows in the result. The default is a space character.

![](_page_99_Picture_18.jpeg)

#### **Note**

If the separator contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

<span id="page-100-1"></span>• [--system](#page-100-1)

| Command-Line Format | system |
|---------------------|--------|
|---------------------|--------|

Tells [ndb\\_config](#page-92-0) to print SYSTEM information only. This consists of system variables that cannot be changed at run time; thus, there is no corresponding section of the cluster configuration file for them. They can be seen (prefixed with \*\*\*\*\*\* SYSTEM \*\*\*\*\*\*) in the output of [ndb\\_config](#page-92-0) [-](#page-95-0) [configinfo](#page-95-0).

This option is mutually exclusive with [--nodes](#page-99-0) and [--connections](#page-97-2); only one of these 3 options can be used.

<span id="page-100-2"></span>• --type=[node\\_type](#page-100-2)

| Command-Line Format | type=name   |
|---------------------|-------------|
| Type                | Enumeration |
| Default Value       | [none]      |
| Valid Values        | ndbd        |
|                     | mysqld      |
|                     | ndb_mgmd    |

Filters results so that only configuration values applying to nodes of the specified node\_type (ndbd, mysqld, or ndb\_mgmd) are returned.

<span id="page-100-3"></span>• [--usage](#page-100-3), --help, or -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Causes [ndb\\_config](#page-92-0) to print a list of available options, and then exit.

<span id="page-100-4"></span>• [--version](#page-100-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Causes [ndb\\_config](#page-92-0) to print a version information string, and then exit.

<span id="page-100-0"></span>• --configinfo [--xml](#page-100-0)

| Command-Line Format | configinfoxml |
|---------------------|---------------|
|---------------------|---------------|

Cause [ndb\\_config](#page-92-0) [--configinfo](#page-95-0) to provide output as XML by adding this option. A portion of such output is shown in this example:

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
 <param name="ConfigGenerationNumber" comment="Configuration generation number"
 type="unsigned" default="0" min="0" max="4294967039"/>
 </section>
 <section name="MYSQLD" primarykeys="NodeId">
 <param name="wan" comment="Use WAN TCP setting as default" type="bool"
 default="false"/>
 <param name="HostName" comment="Name of computer for this node"
```

```
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

![](_page_101_Picture_2.jpeg)

#### **Note**

Normally, the XML output produced by [ndb\\_config](#page-92-0) --configinfo --xml is formatted using one line per element; we have added extra whitespace in the previous example, as well as the next one, for reasons of legibility. This should not make any difference to applications using this output, since most XML processors either ignore nonessential whitespace as a matter of course, or can be instructed to do so.

The XML output also indicates when changing a given parameter requires that data nodes be restarted using the [--initial](#page-59-0) option. This is shown by the presence of an initial="true" attribute in the corresponding <param> element. In addition, the restart type (system or node) is also shown; if a given parameter requires a system restart, this is indicated by the presence of a restart="system" attribute in the corresponding <param> element. For example, changing the value set for the Diskless parameter requires a system initial restart, as shown here (with the restart and initial attributes highlighted for visibility):

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

![](_page_102_Picture_3.jpeg)

#### **Important**

The --xml option can be used only with the --configinfo option. Using --xml without --configinfo fails with an error.

Unlike the options used with this program to obtain current configuration data, --configinfo and --xml use information obtained from the NDB Cluster sources when [ndb\\_config](#page-92-0) was compiled. For this reason, no connection to a running NDB Cluster or access to a config.ini or my.cnf file is required for these two options.

#### <span id="page-102-5"></span>• [--print-defaults](#page-102-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

#### <span id="page-102-1"></span>• [--defaults-file](#page-102-1)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

### <span id="page-102-0"></span>• [--defaults-extra-file](#page-102-0)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

#### <span id="page-102-2"></span>• [--defaults-group-suffix](#page-102-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

#### <span id="page-102-4"></span>• [--login-path](#page-102-4)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

#### <span id="page-102-3"></span>• [--help](#page-102-3)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-103-3"></span>• [--connect-string](#page-103-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-98-2).

<span id="page-103-5"></span>• [--ndb-mgmd-host](#page-103-5)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-98-2).

<span id="page-103-6"></span>• [--ndb-nodeid](#page-103-6)

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-98-2).

<span id="page-103-4"></span>• [--core-file](#page-103-4)

Write core file on error; used in debugging.

<span id="page-103-0"></span>• [--character-sets-dir](#page-103-0)

Directory containing character sets.

<span id="page-103-1"></span>• [--connect-retries](#page-103-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-103-2"></span>• [--connect-retry-delay](#page-103-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-103-7"></span>• [--ndb-optimized-node-selection](#page-103-7)

Combining other [ndb\\_config](#page-92-0) options (such as [--query](#page-99-1) or [--type](#page-100-2)) with --configinfo (with or without the --xml option is not supported. Currently, if you attempt to do so, the usual result is that all other options besides --configinfo or --xml are simply ignored. However, this behavior is not guaranteed and is subject to change at any time. In addition, since [ndb\\_config](#page-92-0), when used with the --configinfo option, does not access the NDB Cluster or read any files, trying to specify additional options such as --ndb-connectstring or --config-file with --configinfo serves no purpose.

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

In this example, we used the [--fields](#page-97-4) options to separate the ID and type of each node with a colon character (:), and the [--rows](#page-99-3) options to place the values for each node on a new line in the output.

2. To produce a connection string that can be used by data, SQL, and API nodes to connect to the management server:

```
$> ./ndb_config --config-file=usr/local/mysql/cluster-data/config.ini \
--query=hostname,portnumber --fields=: --rows=, --type=ndb_mgmd
198.51.100.179:1186
```

3. This invocation of [ndb\\_config](#page-92-0) checks only data nodes (using the [--type](#page-100-2) option), and shows the values for each node's ID and host name, as well as the values set for its DataMemory and DataDir parameters:

```
$> ./ndb_config --type=ndbd --query=nodeid,host,datamemory,datadir -f ' : ' -r '\n'
1 : 198.51.100.193 : 83886080 : /usr/local/mysql/cluster-data
2 : 198.51.100.112 : 83886080 : /usr/local/mysql/cluster-data
3 : 198.51.100.176 : 83886080 : /usr/local/mysql/cluster-data
4 : 198.51.100.119 : 83886080 : /usr/local/mysql/cluster-data
```

In this example, we used the short options -f and -r for setting the field delimiter and row separator, respectively, as well as the short option -q to pass a list of parameters to be obtained.

4. To exclude results from any host except one in particular, use the [--host](#page-98-1) option:

```
$> ./ndb_config --host=198.51.100.176 -f : -r '\n' -q id,type
3:ndbd
5:ndb_mgmd
```

In this example, we also used the short form -q to determine the attributes to be queried.

Similarly, you can limit results to a node with a specific ID using the [--nodeid](#page-98-4) option.

## <span id="page-104-0"></span>**25.5.8 ndb\_delete\_all — Delete All Rows from an NDB Table**

[ndb\\_delete\\_all](#page-104-0) deletes all rows from the given NDB table. In some cases, this can be much faster than DELETE or even TRUNCATE TABLE.

## **Usage**

```
ndb_delete_all -c connection_string tbl_name -d db_name
```

This deletes all rows from the table named tbl\_name in the database named db\_name. It is exactly equivalent to executing TRUNCATE db\_name.tbl\_name in MySQL.

Options that can be used with [ndb\\_delete\\_all](#page-104-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.30 Command-line options used with the program ndb\_delete\_all**

| Format                              | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|-------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets                      | Directory containing character                                                | REMOVED: 8.0.31                                       |
| dir=path                            | sets                                                                          |                                                       |
| connect-retries=#                   | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#               | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect                             | Same asndb-connectstring                                                      | (Supported in all NDB releases                        |
| string=connection_string,           |                                                                               | based on MySQL 8.0)                                   |
| -c connection_string                |                                                                               |                                                       |
| core-file                           | Write core file on error; used in<br>debugging                                | REMOVED: 8.0.31                                       |
| database=name,                      | Name of the database in which<br>the table is found                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name                             |                                                                               |                                                       |
| defaults-extra<br>file=path         | Read given file after global files<br>are read                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                  | Read default options from given<br>file only                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string     | Also read groups with<br>concat(group, suffix)                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| diskscan                            | Perform disk scan                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,<br>-?                         | Display help text and exit                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                     | Read given path from login file                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb                                 | Set connect string for                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,    | connecting to ndb_mgmd.                                                       | based on MySQL 8.0)                                   |
| -c connection_string                | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in     |                                                       |
|                                     | NDB_CONNECTSTRING and<br>my.cnf                                               |                                                       |
| ndb-mgmd<br>host=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
|                                     |                                                                               |                                                       |
| -c connection_string                |                                                                               |                                                       |
| ndb-nodeid=#                        | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring    | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                          | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| transactional,<br>-t            | Perform delete in one single<br>transaction; possible to run out of<br>operations when used                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| tupscan                         | Perform tuple scan                                                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,                          | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>version,<br>-V            | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |

#### <span id="page-106-0"></span>• [--character-sets-dir](#page-106-0)

Directory containing character sets.

## <span id="page-106-1"></span>• [--connect-retries](#page-106-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

#### <span id="page-106-2"></span>• [--connect-retry-delay](#page-106-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-106-3"></span>• [--connect-string](#page-106-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-108-0).

<span id="page-107-0"></span>• [--core-file](#page-107-0)

Write core file on error; used in debugging.

<span id="page-107-6"></span>• [--database](#page-107-6), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database containing the table to delete from.

<span id="page-107-1"></span>• [--defaults-extra-file](#page-107-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-107-2"></span>• [--defaults-file](#page-107-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-107-3"></span>• [--defaults-group-suffix](#page-107-3)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-107-7"></span>• [--diskscan](#page-107-7)

| Command-Line Format | diskscan |
|---------------------|----------|
|---------------------|----------|

Run a disk scan.

<span id="page-107-4"></span>• [--help](#page-107-4)

| Command-Line Format<br>help |  |
|-----------------------------|--|
|-----------------------------|--|

Display help text and exit.

<span id="page-107-5"></span>• [--login-path](#page-107-5)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-108-0"></span>• [--ndb-connectstring](#page-108-0)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                |                                 |
|                     | String                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-108-1"></span>• [--ndb-mgmd-host](#page-108-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-108-0).

<span id="page-108-2"></span>• [--ndb-nodeid](#page-108-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-108-0).

<span id="page-108-3"></span>• [--ndb-optimized-node-selection](#page-108-3)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-108-4"></span>• [--no-defaults](#page-108-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-108-5"></span>• [--print-defaults](#page-108-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-108-6"></span>• [--transactional](#page-108-6), -t

Use of this option causes the delete operation to be performed as a single transaction.

![](_page_108_Picture_21.jpeg)

#### **Warning**

With very large tables, using this option may cause the number of operations available to the cluster to be exceeded.

<span id="page-108-7"></span>• [--tupscan](#page-108-7) 4479

Run a tuple scan.

<span id="page-109-0"></span>• [--usage](#page-109-0)

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Display help text and exit; same as [--help](#page-107-4).

<span id="page-109-1"></span>• [--version](#page-109-1)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

In NDB 7.6 and earlier, this program printed NDBT\_ProgramExit - status upon completion of its run, due to an unnecessary dependency on the NDBT testing library. This dependency has been removed in NDB 8.0, eliminating the extraneous output.

## <span id="page-109-2"></span>**25.5.9 ndb\_desc — Describe NDB Tables**

[ndb\\_desc](#page-109-2) provides a detailed description of one or more NDB tables.

## **Usage**

```
ndb_desc -c connection_string tbl_name -d db_name [options]
ndb_desc -c connection_string index_name -d db_name -t tbl_name
```

Additional options that can be used with [ndb\\_desc](#page-109-2) are listed later in this section.

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

#### Output from [ndb\\_desc](#page-109-2):

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
```

```
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
1 4 4 32768 32768 0 0
```

Information about multiple tables can be obtained in a single invocation of [ndb\\_desc](#page-109-2) by using their names, separated by spaces. All of the tables must be in the same database.

You can obtain additional information about a specific index using the --table (short form: -t) option and supplying the name of the index as the first argument to [ndb\\_desc](#page-109-2), as shown here:

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

When an index is specified in this way, the [--extra-partition-info](#page-117-0) and [--extra-node-info](#page-116-0) options have no effect.

The Version column in the output contains the table's schema object version. For information about interpreting this value, see [NDB Schema Object Versions](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-schema-object-versions.md).

Three of the table properties that can be set using NDB\_TABLE comments embedded in CREATE TABLE and ALTER TABLE statements are also visible in [ndb\\_desc](#page-109-2) output. The table's FRAGMENT\_COUNT\_TYPE is always shown in the FragmentCountType column. READ\_ONLY and FULLY\_REPLICATED, if set to 1, are shown in the Table options column. You can see this after executing the following ALTER TABLE statement in the mysql client:

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

Because FRAGMENT\_COUNT\_TYPE was not set explicitly, its value is not shown in the comment text printed by SHOW CREATE TABLE. [ndb\\_desc](#page-109-2), however, displays the updated value for this attribute. The Table options column shows the binary properties just enabled. You can see this in the output shown here (emphasized text):

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
```

```
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

When run against this version of the table, [ndb\\_desc](#page-109-2) displays the following output:

```
$> ./ndb_desc -c localhost fish -d test -p
-- fish --
Version: 1
Fragment type: HashMapPartition
K Value: 6
```

```
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

Tablespace id and Tablespace are displayed for Disk Data tables beginning with NDB 8.0.21.

For fully replicated tables, [ndb\\_desc](#page-109-2) shows only the nodes holding primary partition fragment replicas; nodes with copy fragment replicas (only) are ignored. You can obtain such information, using the mysql client, from the table\_distribution\_status, table\_fragments, table\_info, and table\_replicas tables in the ndbinfo database.

All options that can be used with [ndb\\_desc](#page-109-2) are shown in the following table. Additional descriptions follow the table.

**Table 25.31 Command-line options used with the program ndb\_desc**

| Format                     | Description                                                                                             | Added, Deprecated, or<br>Removed                      |
|----------------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| auto-inc,<br>-a            | Show next value for<br>AUTO_INCREMENT oolumn if<br>table has one                                        | ADDED: NDB 8.0.21                                     |
| blob-info,<br>-b           | Include partition information for<br>BLOB tables in output. Requires<br>that the -p option also be used | (Supported in all NDB releases<br>based on MySQL 8.0) |
| character-sets<br>dir=path | Directory containing character<br>sets                                                                  | REMOVED: 8.0.31                                       |

| Format                                  | Description                                                                             | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retries=#                       | Number of times to retry<br>connection before giving up                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                   | Number of seconds to wait<br>between attempts to contact<br>management server           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string,    | Same asndb-connectstring                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    |                                                                                         |                                                       |
| context,<br>-x                          | Show extra information for table<br>such as database, schema,<br>name, and internal ID  | ADDED: NDB 8.0.21                                     |
| core-file                               | Write core file on error; used in<br>debugging                                          | REMOVED: 8.0.31                                       |
| database=name,                          | Name of database containing<br>table                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name<br>defaults-extra<br>file=path  | Read given file after global files<br>are read                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                      | Read default options from given<br>file only                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| extra-node-info,<br>-n                  | Include partition-to-data-node<br>mappings in output; requires<br>extra-partition-info  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| extra-partition-info,                   | Display information about<br>partitions                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -p<br>help,                             | Display help text and exit                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                      |                                                                                         |                                                       |
| login-path=path                         | Read given path from login file                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf     |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    |                                                                                         |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default; | REMOVED: 8.0.31                                       |

| Format         | Description                                                                  | Added, Deprecated, or<br>Removed                      |
|----------------|------------------------------------------------------------------------------|-------------------------------------------------------|
|                | useskip-ndb-optimized-node<br>selection to disable                           |                                                       |
| no-defaults    | Do not read default options from<br>any option file other than login<br>file | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults | Print program argument list and<br>exit                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| retries=#,     | Number of times to retry the<br>connection (once per second)                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -r #           |                                                                              |                                                       |
| table=name,    | Specify the table in which to find<br>an index. When this option is          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -t name        | used, -p and -n have no effect<br>and are ignored                            |                                                       |
| unqualified,   | Use unqualified table names                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -u             |                                                                              |                                                       |
| usage,         | Display help text and exit; same<br>ashelp                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?             |                                                                              |                                                       |
| version,       | Display version information and<br>exit                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V             |                                                                              |                                                       |

<span id="page-115-0"></span>• [--auto-inc](#page-115-0), -a

Show the next value for a table's AUTO\_INCREMENT column, if it has one.

<span id="page-115-1"></span>• [--blob-info](#page-115-1), -b

Include information about subordinate BLOB and TEXT columns.

Use of this option also requires the use of the [--extra-partition-info](#page-117-0) (-p) option.

<span id="page-115-2"></span>• [--character-sets-dir](#page-115-2)

Directory containing character sets.

<span id="page-115-3"></span>• [--connect-retries](#page-115-3)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-115-4"></span>• [--connect-retry-delay](#page-115-4)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |

| Minimum Value | 0 |
|---------------|---|
| Maximum Value | 5 |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-116-1"></span>• [--connect-string](#page-116-1)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-117-3).

<span id="page-116-2"></span>• [--context](#page-116-2), -x

Show additional contextual information for the table such as schema, database name, table name, and the table's internal ID.

<span id="page-116-3"></span>• [--core-file](#page-116-3)

Write core file on error; used in debugging.

<span id="page-116-4"></span>• [--database=](#page-116-4)db\_name, -d

Specify the database in which the table should be found.

<span id="page-116-5"></span>• [--defaults-extra-file](#page-116-5)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-116-6"></span>• [--defaults-file](#page-116-6)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-116-7"></span>• [--defaults-group-suffix](#page-116-7)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-116-0"></span>• [--extra-node-info](#page-116-0), -n

Include information about the mappings between table partitions and the data nodes upon which they reside. This information can be useful for verifying distribution awareness mechanisms and supporting more efficient application access to the data stored in NDB Cluster.

Use of this option also requires the use of the [--extra-partition-info](#page-117-0) (-p) option.

<span id="page-117-0"></span>• [--extra-partition-info](#page-117-0), -p

Print additional information about the table's partitions.

<span id="page-117-1"></span>• [--help](#page-117-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-117-2"></span>• [--login-path](#page-117-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-117-3"></span>• [--ndb-connectstring](#page-117-3)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-117-4"></span>• [--ndb-mgmd-host](#page-117-4)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-117-3).

<span id="page-117-5"></span>• [--ndb-nodeid](#page-117-5)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-117-3).

<span id="page-117-6"></span>• [--ndb-optimized-node-selection](#page-117-6)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-117-7"></span>• [--no-defaults](#page-117-7)

| Command-Line Format | no-defaults |
|---------------------|-------------|

<span id="page-118-0"></span>• [--print-defaults](#page-118-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-118-1"></span>• [--retries=](#page-118-1)#, -r

Try to connect this many times before giving up. One connect attempt is made per second.

<span id="page-118-2"></span>• [--table=](#page-118-2)tbl\_name, -t

Specify the table in which to look for an index.

<span id="page-118-3"></span>• [--unqualified](#page-118-3), -u

Use unqualified table names.

<span id="page-118-4"></span>• [--usage](#page-118-4)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-117-1).

<span id="page-118-5"></span>• [--version](#page-118-5)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

Table indexes listed in the output are ordered by ID.

# <span id="page-118-6"></span>**25.5.10 ndb\_drop\_index — Drop Index from an NDB Table**

[ndb\\_drop\\_index](#page-118-6) drops the specified index from an NDB table. It is recommended that you use this utility only as an example for writing NDB API applications—see the Warning later in this section for details.

## **Usage**

```
ndb_drop_index -c connection_string table_name index -d db_name
```

The statement shown above drops the index named index from the table in the database.

Options that can be used with [ndb\\_drop\\_index](#page-118-6) are shown in the following table. Additional descriptions follow the table.

**Table 25.32 Command-line options used with the program ndb\_drop\_index**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | REMOVED: 8.0.31                                       |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                              | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -c connection_string                |                                                                                                                                               |                                                       |
| core-file                           | Write core file on error; used in<br>debugging                                                                                                | REMOVED: 8.0.31                                       |
| database=name,                      | Name of database in which table<br>is found                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name                             |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path         | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                  | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string     | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                               | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                  |                                                                                                                                               |                                                       |
| login-path=path                     | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb                                 | Set connect string for                                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,    | connecting to ndb_mgmd.                                                                                                                       | based on MySQL 8.0)                                   |
| -c connection_string                | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and                                            |                                                       |
|                                     | my.cnf                                                                                                                                        |                                                       |
| ndb-mgmd<br>host=connection_string, | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                |                                                                                                                                               |                                                       |
| ndb-nodeid=#                        | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection     | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| no-defaults                         | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                      | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,                              | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                  |                                                                                                                                               |                                                       |
| version,                            | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                                  |                                                                                                                                               |                                                       |

<span id="page-119-0"></span>• [--character-sets-dir](#page-119-0)

Directory containing character sets.

### <span id="page-120-0"></span>• [--connect-retries](#page-120-0)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

### <span id="page-120-1"></span>• [--connect-retry-delay](#page-120-1)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

#### <span id="page-120-2"></span>• [--connect-string](#page-120-2)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-121-3).

<span id="page-120-3"></span>• [--core-file](#page-120-3)

Write core file on error; used in debugging.

#### <span id="page-120-6"></span>• [--database](#page-120-6), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

#### <span id="page-120-4"></span>• [--defaults-extra-file](#page-120-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

#### <span id="page-120-5"></span>• [--defaults-file](#page-120-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

#### Read default options from given file only.

<span id="page-121-0"></span>• [--defaults-group-suffix](#page-121-0)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-121-1"></span>• [--help](#page-121-1)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-121-2"></span>• [--login-path](#page-121-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-121-3"></span>• [--ndb-connectstring](#page-121-3)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-121-4"></span>• [--ndb-mgmd-host](#page-121-4)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-121-3).

<span id="page-121-5"></span>• [--ndb-nodeid](#page-121-5)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-121-3).

<span id="page-121-6"></span>• [--ndb-optimized-node-selection](#page-121-6)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-121-7"></span>• [--no-defaults](#page-121-7)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-122-0"></span>• [--print-defaults](#page-122-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-122-1"></span>• [--usage](#page-122-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-121-1).

<span id="page-122-2"></span>• [--version](#page-122-2)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

![](_page_122_Picture_12.jpeg)

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

<span id="page-122-3"></span>In such a case, your only option for making the table available to MySQL again is to drop the table and re-create it. You can use either the SQL statementDROP TABLE or the [ndb\\_drop\\_table](#page-122-3) utility (see [Section 25.5.11, "ndb\\_drop\\_table — Drop an NDB Table"](#page-122-3)) to drop the table.

[ndb\\_drop\\_table](#page-122-3) drops the specified NDB table. (If you try to use this on a table created with a storage engine other than NDB, the attempt fails with the error 723: No such table exists.) This operation is extremely fast; in some cases, it can be an order of magnitude faster than using a MySQL DROP TABLE statement on an NDB table.

## **Usage**

ndb\_drop\_table -c connection\_string tbl\_name -d db\_name

Options that can be used with [ndb\\_drop\\_table](#page-122-3) are shown in the following table. Additional descriptions follow the table.

**Table 25.33 Command-line options used with the program ndb\_drop\_table**

| Format                              | Description                                                                         | Added, Deprecated, or<br>Removed                      |
|-------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets                      | Directory containing character                                                      | REMOVED: 8.0.31                                       |
| dir=path                            | sets                                                                                |                                                       |
| connect-retries=#                   | Number of times to retry<br>connection before giving up                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#               | Number of seconds to wait<br>between attempts to contact<br>management server       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect                             | Same asndb-connectstring                                                            | (Supported in all NDB releases                        |
| string=connection_string,           |                                                                                     | based on MySQL 8.0)                                   |
| -c connection_string                |                                                                                     |                                                       |
| core-file                           | Write core file on error; used in<br>debugging                                      | REMOVED: 8.0.31                                       |
| database=name,                      | Name of database in which table<br>is found                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name                             |                                                                                     |                                                       |
| defaults-extra<br>file=path         | Read given file after global files<br>are read                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                  | Read default options from given<br>file only                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string     | Also read groups with<br>concat(group, suffix)                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                               | Display help text and exit                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                  |                                                                                     |                                                       |
| login-path=path                     | Read given path from login file                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb                                 | Set connect string for                                                              | (Supported in all NDB releases                        |
| connectstring=connection_string,    | connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                    | based on MySQL 8.0)                                   |
| -c connection_string                | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf |                                                       |
| ndb-mgmd<br>host=connection_string, | Same asndb-connectstring                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                |                                                                                     |                                                       |

| Format                          | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| ndb-nodeid=#                    | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,<br>-?                    | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| version,                        | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                              |                                                                                                                                               |                                                       |

#### <span id="page-124-0"></span>• [--character-sets-dir](#page-124-0)

Directory containing character sets.

<span id="page-124-1"></span>• [--connect-retries](#page-124-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-124-2"></span>• [--connect-retry-delay](#page-124-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-124-3"></span>• [--connect-string](#page-124-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

<span id="page-125-0"></span>• [--core-file](#page-125-0)

Write core file on error; used in debugging.

<span id="page-125-7"></span>• [--database](#page-125-7), -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

<span id="page-125-1"></span>• [--defaults-extra-file](#page-125-1)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-125-2"></span>• [--defaults-file](#page-125-2)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-125-3"></span>• [--defaults-group-suffix](#page-125-3)

| Command-Line Format | defaults-group-suffix=string |  |
|---------------------|------------------------------|--|
| Type                | String                       |  |
| Default Value       | [none]                       |  |

Also read groups with concat(group, suffix).

<span id="page-125-4"></span>• [--help](#page-125-4)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-125-5"></span>• [--login-path](#page-125-5)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-125-6"></span>• [--ndb-connectstring](#page-125-6)

| Type                | connectstring=connection_string<br>String |
|---------------------|-------------------------------------------|
| Command-Line Format | ndb                                       |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-126-0"></span>• [--ndb-mgmd-host](#page-126-0)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-125-6).

<span id="page-126-1"></span>• [--ndb-nodeid](#page-126-1)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-125-6).

<span id="page-126-2"></span>• [--ndb-optimized-node-selection](#page-126-2)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-126-3"></span>• [--no-defaults](#page-126-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-126-4"></span>• [--print-defaults](#page-126-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-126-5"></span>• [--usage](#page-126-5)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-125-4).

<span id="page-126-6"></span>• [--version](#page-126-6)

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

# <span id="page-126-7"></span>**25.5.12 ndb\_error\_reporter — NDB Error-Reporting Utility**

[ndb\\_error\\_reporter](#page-126-7) creates an archive from data node and management node log files that can be used to help diagnose bugs or other problems with a cluster. It is highly recommended that you make use of this utility when filing reports of bugs in NDB Cluster.

Options that can be used with [ndb\\_error\\_reporter](#page-126-7) are shown in the following table. Additional descriptions follow the table.

**Table 25.34 Command-line options used with the program ndb\_error\_reporter**

| Format               | Description                                                                          | Added, Deprecated, or<br>Removed                      |
|----------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------|
| connection-timeout=# | Number of seconds to wait when<br>connecting to nodes before<br>timing out           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| dry-scp              | Disable scp with remote hosts;<br>used in testing only                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fs                   | Include file system data in error<br>report; can use a large amount of<br>disk space | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,<br>-?          | Display help text and exit                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| skip-nodegroup=#     | Skip all nodes in the node group<br>having this ID                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |

## **Usage**

ndb\_error\_reporter path/to/config-file [username] [options]

This utility is intended for use on a management node host, and requires the path to the management host configuration file (usually named config.ini). Optionally, you can supply the name of a user that is able to access the cluster's data nodes using SSH, to copy the data node log files. [ndb\\_error\\_reporter](#page-126-7) then includes all of these files in archive that is created in the same directory in which it is run. The archive is named ndb\_error\_report\_YYYYMMDDhhmmss.tar.bz2, where YYYYMMDDhhmmss is a datetime string.

[ndb\\_error\\_reporter](#page-126-7) also accepts the options listed here:

<span id="page-127-0"></span>• [--connection-timeout=](#page-127-0)timeout

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Wait this many seconds when trying to connect to nodes before timing out.

<span id="page-127-1"></span>• [--dry-scp](#page-127-1)

|  | Command-Line Format | dry-scp |
|--|---------------------|---------|
|--|---------------------|---------|

Run [ndb\\_error\\_reporter](#page-126-7) without using scp from remote hosts. Used for testing only.

<span id="page-127-3"></span>• [--help](#page-127-3)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-127-2"></span>• [--fs](#page-127-2)

| Command-Line Format | fs |
|---------------------|----|

Because data node file systems can be extremely large, even after being compressed, we ask that you please do not send archives created using this option to Oracle unless you are specifically requested to do so.

<span id="page-128-0"></span>• [--skip-nodegroup=](#page-128-0)nodegroup\_id

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Skip all nodes belong to the node group having the supplied node group ID.

## <span id="page-128-1"></span>**25.5.13 ndb\_import — Import CSV Data Into NDB**

[ndb\\_import](#page-128-1) imports CSV-formatted data, such as that produced by mysqldump --tab, directly into NDB using the NDB API. [ndb\\_import](#page-128-1) requires a connection to an NDB management server ([ndb\\_mgmd](#page-70-0)) to function; it does not require a connection to a MySQL Server.

## **Usage**

```
ndb_import db_name file_name options
```

[ndb\\_import](#page-128-1) requires two arguments. db\_name is the name of the database where the table into which to import the data is found; file\_name is the name of the CSV file from which to read the data; this must include the path to this file if it is not in the current directory. The name of the file must match that of the table; the file's extension, if any, is not taken into consideration. Options supported by [ndb\\_import](#page-128-1) include those for specifying field separators, escapes, and line terminators, and are described later in this section.

Prior to NDB 8.0.30, [ndb\\_import](#page-128-1) rejects any empty lines which it reads from the CSV file. Beginning with NDB 8.0.30, when importing a single column, an empty value that can be used as the column value, ndb\_import handles it in the same manner as a LOAD DATA statement does.

[ndb\\_import](#page-128-1) must be able to connect to an NDB Cluster management server; for this reason, there must be an unused [api] slot in the cluster config.ini file.

To duplicate an existing table that uses a different storage engine, such as InnoDB, as an NDB table, use the mysql client to perform a SELECT INTO OUTFILE statement to export the existing table to a CSV file, then to execute a CREATE TABLE LIKE statement to create a new table having the same structure as the existing table, then perform ALTER TABLE ... ENGINE=NDB on the new table; after this, from the system shell, invoke [ndb\\_import](#page-128-1) to load the data into the new NDB table. For example, an existing InnoDB table named myinnodb\_table in a database named myinnodb can be exported into an NDB table named myndb\_table in a database named myndb as shown here, assuming that you are already logged in as a MySQL user with the appropriate privileges:

### 1. In the mysql client:

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
```

```
mysql> EXIT;
Bye
$>
```

Once the target database and table have been created, a running mysqld is no longer required. You can stop it using mysqladmin shutdown or another method before proceeding, if you wish.

#### 2. In the system shell:

```
# if you are not already in the MySQL bin directory:
$> cd path-to-mysql-bin-dir
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

All options that can be used with [ndb\\_import](#page-128-1) are shown in the following table. Additional descriptions follow the table.

**Table 25.35 Command-line options used with the program ndb\_import**

| Format                     | Description                                                                                            | Added, Deprecated, or<br>Removed                      |
|----------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| abort-on-error             | Dump core on any fatal error;<br>used for debugging                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ai-increment=#             | For table with hidden PK, specify<br>autoincrement increment. See<br>mysqld                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ai-offset=#                | For table with hidden PK, specify<br>autoincrement offset. See<br>mysqld                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ai-prefetch-sz=#           | For table with hidden PK, specify<br>number of autoincrement values<br>that are prefetched. See mysqld | (Supported in all NDB releases<br>based on MySQL 8.0) |
| character-sets<br>dir=path | Directory containing character<br>sets                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retries=#          | Number of times to retry<br>connection before giving up                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#      | Number of seconds to wait<br>between attempts to contact<br>management server                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect                    | Same asndb-connectstring                                                                               | (Supported in all NDB releases                        |
| string=connection_string,  |                                                                                                        | based on MySQL 8.0)                                   |
| -c connection_string       |                                                                                                        |                                                       |
| connections=#              | Number of cluster connections to<br>create                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| continue                   | When job fails, continue to next<br>job                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| core-file                  | Write core file on error; used in<br>debugging                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                | Description                                                                                                                              | Added, Deprecated, or<br>Removed                      |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| csvopt=opts                           | Shorthand option for setting<br>typical CSV option values. See<br>documentation for syntax and<br>other information                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| db-workers=#                          | Number of threads, per data<br>node, executing database<br>operations                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-extra<br>file=path           | Read given file after global files<br>are read                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                    | Read default options from given<br>file only                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string       | Also read groups with<br>concat(group, suffix)                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| errins-type=name                      | Error insert type, for testing<br>purposes; use "list" to obtain all<br>possible values                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| errins-delay=#                        | Error insert delay in milliseconds;<br>random variation is added                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-enclosed<br>by=char            | Same as FIELDS ENCLOSED<br>BY option for LOAD DATA<br>statements. For CSV input this is<br>same as usingfields-optionally<br>enclosed-by | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-escaped-by=char                | Same as FIELDS ESCAPED<br>BY option for LOAD DATA<br>statements                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-optionally<br>enclosed-by=char | Same as FIELDS OPTIONALLY<br>ENCLOSED BY option for LOAD<br>DATA statements                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-terminated<br>by=char          | Same as FIELDS TERMINATED<br>BY option for LOAD DATA<br>statements                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                 | Display help text and exit                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>idlesleep=#                     | Number of milliseconds to sleep<br>waiting for more to do                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| idlespin=#                            | Number of times to retry before<br>idlesleep                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ignore-lines=#                        | Ignore first # lines in input file.<br>Used to skip a non-data header                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| input-type=name                       | Input type: random or csv                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| input-workers=#                       | Number of threads processing<br>input. Must be 2 or more if<br>input-type is csv                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| keep-state                            | State files (except non-empty<br>*.rej files) are normally removed<br>on job completion. Using this                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                                          | Description                                                                                                                                                                                                                                                            | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|                                                                 | option causes all state files to be<br>preserved instead                                                                                                                                                                                                               |                                                       |
| lines-terminated<br>by=char                                     | Same as LINES TERMINATED<br>BY option for LOAD DATA<br>statements                                                                                                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                                                 | Read given path from login file                                                                                                                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| max-rows=#                                                      | Import only this number of input<br>data rows; default is 0, which<br>imports all rows                                                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| missing-ai<br>column='name'                                     | Indicates that auto-increment<br>values are missing from CSV file<br>to be imported.                                                                                                                                                                                   | ADDED: NDB 8.0.30                                     |
| monitor=#                                                       | Periodically print status of<br>running job if something has<br>changed (status, rejected<br>rows, temporary errors). Value<br>0 disables. Value 1 prints<br>any change seen. Higher<br>values reduce status printing<br>exponentially up to some pre<br>defined limit | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-mgmd<br>host=connection_string,                             | Same asndb-connectstring                                                                                                                                                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-asynch                                                       | Run database operations as<br>batches, in single transactions                                                                                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-hint                                                         | Tells transaction coordinator not<br>to use distribution key hint when<br>selecting data node                                                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| opbatch=#                                                       | A db execution batch is a set of<br>transactions and operations sent                                                                                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                 | Description                                                                                                                                                                                                       | Added, Deprecated, or<br>Removed                      |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|                        | to NDB kernel. This option limits<br>NDB operations (including blob<br>operations) in a db execution<br>batch. Therefore it also limits<br>number of asynch transactions.<br>Value 0 is not valid                 |                                                       |
| opbytes=#              | Limit bytes in execution batch<br>(default 0 = no limit)                                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| output-type=name       | Output type: ndb is default, null<br>used for testing                                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| output-workers=#       | Number of threads processing<br>output or relaying database<br>operations                                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| pagesize=#             | Align I/O buffers to given size                                                                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| pagecnt=#              | Size of I/O buffers as multiple<br>of page size. CSV input worker<br>allocates double-sized buffer                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| polltimeout=#          | Timeout per poll for completed<br>asynchonous transactions;<br>polling continues until all polls<br>are completed, or error occurs                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults         | Print program argument list and<br>exit                                                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| rejects=#              | Limit number of rejected rows<br>(rows with permanent error) in<br>data load. Default is 0 which<br>means that any rejected row<br>causes a fatal error. The row<br>exceeding the limit is also added<br>to *.rej | (Supported in all NDB releases<br>based on MySQL 8.0) |
| resume                 | If job aborted (temporary error,<br>user interrupt), resume with rows<br>not yet processed                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| rowbatch=#             | Limit rows in row queues (default<br>0 = no limit); must be 1 or more if<br>input-type is random                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| rowbytes=#             | Limit bytes in row queues (0 = no<br>limit)                                                                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| state-dir=path         | Where to write state files; currect<br>directory is default                                                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| stats                  | Save performance related<br>options and internal statistics<br>in *.sto and *.stt files. These<br>files are kept on successful<br>completion even ifkeep-state is<br>not used                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| table=name,<br>-t name | Name of target to import data<br>into; default is base name of<br>input file                                                                                                                                      | ADDED: NDB 8.0.28                                     |

| Format                 | Description                                                                                                                                                                                             | Added, Deprecated, or<br>Removed                      |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| tempdelay=#            | Number of milliseconds to sleep<br>between temporary errors                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| temperrors=#           | Number of times a transaction<br>can fail due to a temporary error,<br>per execution batch; 0 means<br>any temporary error is fatal. Such<br>errors do not cause any rows to<br>be written to .rej file | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,<br>-?           | Display help text and exit; same<br>ashelp                                                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| verbose[=#],<br>-v [#] | Enable verbose output                                                                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| version,<br>-V         | Display version information and<br>exit                                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |

<span id="page-133-0"></span>• [--abort-on-error](#page-133-0)

| Command-Line Format | abort-on-error |
|---------------------|----------------|
|---------------------|----------------|

Dump core on any fatal error; used for debugging only.

<span id="page-133-1"></span>• [--ai-increment](#page-133-1)=#

| Command-Line Format | ai-increment=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 1              |
| Minimum Value       | 1              |
| Maximum Value       | 4294967295     |

For a table with a hidden primary key, specify the autoincrement increment, like the auto\_increment\_increment system variable does in the MySQL Server.

<span id="page-133-2"></span>• [--ai-offset](#page-133-2)=#

| Command-Line Format | ai-offset=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 1           |
| Minimum Value       | 1           |
| Maximum Value       | 4294967295  |

For a table with hidden primary key, specify the autoincrement offset. Similar to the auto\_increment\_offset system variable.

• [--ai-prefetch-sz](#page-133-3)=#

<span id="page-133-3"></span>

|      | Command-Line Format | ai-prefetch-sz=# |
|------|---------------------|------------------|
|      | Type                | Integer          |
| 4504 | Default Value       | 1024             |

| Minimum Value | 1          |
|---------------|------------|
| Maximum Value | 4294967295 |

For a table with a hidden primary key, specify the number of autoincrement values that are prefetched. Behaves like the ndb\_autoincrement\_prefetch\_sz system variable does in the MySQL Server.

<span id="page-134-0"></span>• [--character-sets-dir](#page-134-0)

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-134-4"></span>• [--connections](#page-134-4)=#

| Command-Line Format | connections=# |
|---------------------|---------------|
| Type                | Integer       |
| Default Value       | 1             |
| Minimum Value       | 1             |
| Maximum Value       | 4294967295    |

Number of cluster connections to create.

<span id="page-134-1"></span>• [--connect-retries](#page-134-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-134-2"></span>• [--connect-retry-delay](#page-134-2)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-134-3"></span>• [--connect-string](#page-134-3)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-140-0).

#### <span id="page-135-0"></span>• [--continue](#page-135-0)

| Command-Line Format | continue |
|---------------------|----------|
|---------------------|----------|

When a job fails, continue to the next job.

<span id="page-135-1"></span>• [--core-file](#page-135-1)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-135-2"></span>• [--csvopt](#page-135-2)=string

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

In NDB 8.0.28 and later, the order of parameters used in the argument to this option is handled such that the rightmost parameter always takes precedence over any potentially conflicting parameters which have already been used in the same argument value. This also applies to any duplicate instances of a given parameter. Prior to NDB 8.0.28, the order of the parameters made no difference, other than that, when both n and r were specified, the one occurring last (rightmost) was the parameter which actually took effect.

This option is intended for use in testing under conditions in which it is difficult to transmit escapes or quotation marks.

<span id="page-135-3"></span>• [--db-workers](#page-135-3)=#

| Command-Line Format | db-workers=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 4            |
| Minimum Value       | 1            |
| Maximum Value       | 4294967295   |

Number of threads, per data node, executing database operations.

• [--defaults-file](#page-135-4)

<span id="page-135-4"></span>

|      | Command-Line Format | defaults-file=path |
|------|---------------------|--------------------|
| 4506 | Type                | String             |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read default options from given file only.

<span id="page-136-0"></span>• [--defaults-extra-file](#page-136-0)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-136-1"></span>• [--defaults-group-suffix](#page-136-1)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-136-2"></span>• [--errins-type](#page-136-2)=name

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

<span id="page-136-3"></span>• [--errins-delay](#page-136-3)=#

| Command-Line Format | errins-delay=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 1000           |
| Minimum Value       | 0              |
| Maximum Value       | 4294967295     |
| Unit                | ms             |

Error insert delay in milliseconds; random variation is added. This option is used for testing purposes only.

<span id="page-136-4"></span>• [--fields-enclosed-by](#page-136-4)=char

| Command-Line Format | fields-enclosed-by=char | 4507 |
|---------------------|-------------------------|------|
| Type                | String                  |      |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

This works in the same way as the FIELDS ENCLOSED BY option does for the LOAD DATA statement, specifying a character to be interpreted as quoting field values. For CSV input, this is the same as [--fields-optionally-enclosed-by](#page-137-1).

<span id="page-137-0"></span>• [--fields-escaped-by](#page-137-0)=name

| Command-Line Format | fields-escaped-by=char |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       | \                      |

Specify an escape character in the same way as the FIELDS ESCAPED BY option does for the SQL LOAD DATA statement.

<span id="page-137-1"></span>• [--fields-optionally-enclosed-by](#page-137-1)=char

| Command-Line Format | fields-optionally-enclosed-by=char |
|---------------------|------------------------------------|
| Type                | String                             |
| Default Value       | [none]                             |

This works in the same way as the FIELDS OPTIONALLY ENCLOSED BY option does for the LOAD DATA statement, specifying a character to be interpreted as optionally quoting field values. For CSV input, this is the same as [--fields-enclosed-by](#page-136-4).

<span id="page-137-2"></span>• [--fields-terminated-by](#page-137-2)=char

| Command-Line Format | fields-terminated-by=char |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | \t                        |

This works in the same way as the FIELDS TERMINATED BY option does for the LOAD DATA statement, specifying a character to be interpreted as the field separator.

<span id="page-137-3"></span>• [--help](#page-137-3)

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-137-4"></span>• [--idlesleep](#page-137-4)=#

| Command-Line Format | idlesleep=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 1           |
| Minimum Value       | 1           |
| Maximum Value       | 4294967295  |
| Unit                | ms          |

Number of milliseconds to sleep waiting for more work to perform.

<span id="page-137-5"></span>• [--idlespin](#page-137-5)=#

| Command-Line Format | idlespin=# |
|---------------------|------------|
| Type                | Integer    |

| Default Value | 0          |
|---------------|------------|
| Minimum Value | 0          |
| Maximum Value | 4294967295 |

Number of times to retry before sleeping.

<span id="page-138-0"></span>• [--ignore-lines](#page-138-0)=#

| Command-Line Format | ignore-lines=# |
|---------------------|----------------|
| Type                | Integer        |
| Default Value       | 0              |
| Minimum Value       | 0              |
| Maximum Value       | 4294967295     |

Cause ndb\_import to ignore the first # lines of the input file. This can be employed to skip a file header that does not contain any data.

<span id="page-138-1"></span>• [--input-type](#page-138-1)=name

| Command-Line Format | input-type=name |
|---------------------|-----------------|
| Type                | Enumeration     |
| Default Value       | csv             |
| Valid Values        | random          |
|                     | csv             |

Set the type of input type. The default is csv; random is intended for testing purposes only. .

<span id="page-138-2"></span>• [--input-workers](#page-138-2)=#

| Command-Line Format | input-workers=# |
|---------------------|-----------------|
| Type                | Integer         |
| Default Value       | 4               |
| Minimum Value       | 1               |
| Maximum Value       | 4294967295      |

Set the number of threads processing input.

<span id="page-138-3"></span>• [--keep-state](#page-138-3)

| Command-Line Format | keep-state |
|---------------------|------------|
|---------------------|------------|

By default, ndb\_import removes all state files (except non-empty \*.rej files) when it completes a job. Specify this option (nor argument is required) to force the program to retain all state files instead.

<span id="page-138-4"></span>• [--lines-terminated-by](#page-138-4)=name

| Command-Line Format | lines-terminated-by=char |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | \n                       |

4509

### <span id="page-139-4"></span>• [--log-level](#page-139-4)=#

| Command-Line Format | log-level=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 0           |
| Minimum Value       | 0           |
| Maximum Value       | 2           |

Performs internal logging at the given level. This option is intended primarily for internal and development use.

In debug builds of NDB only, the logging level can be set using this option to a maximum of 4.

#### <span id="page-139-0"></span>• [--login-path](#page-139-0)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

#### <span id="page-139-1"></span>• [--max-rows](#page-139-1)=#

| Command-Line Format | max-rows=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Import only this number of input data rows; the default is 0, which imports all rows.

#### <span id="page-139-2"></span>• [--missing-ai-column](#page-139-2)

| Command-Line Format | missing-ai-column='name' |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

This option can be employed when importing a single table, or multiple tables. When used, it indicates that the CSV file being imported does not contain any values for an AUTO\_INCREMENT column, and that [ndb\\_import](#page-128-1) should supply them; if the option is used and the AUTO\_INCREMENT column contains any values, the import operation cannot proceed.

#### • [--monitor](#page-139-3)=#

<span id="page-139-3"></span>

|      | Command-Line Format | monitor=#  |
|------|---------------------|------------|
|      | Type                | Integer    |
|      | Default Value       | 2          |
|      | Minimum Value       | 0          |
| 4510 | Maximum Value       | 4294967295 |

| Unit | bytes |
|------|-------|
|------|-------|

Periodically print the status of a running job if something has changed (status, rejected rows, temporary errors). Set to 0 to disable this reporting. Setting to 1 prints any change that is seen. Higher values reduce the frequency of this status reporting.

#### <span id="page-140-0"></span>• [--ndb-connectstring](#page-140-0)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

#### <span id="page-140-1"></span>• [--ndb-mgmd-host](#page-140-1)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-140-0).

#### <span id="page-140-2"></span>• [--ndb-nodeid](#page-140-2)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-140-0).

### <span id="page-140-3"></span>• [--ndb-optimized-node-selection](#page-140-3)

| Command-Line Format<br>ndb-optimized-node-selection |
|-----------------------------------------------------|
|-----------------------------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-140-4"></span>• [--no-asynch](#page-140-4)

| Command-Line Format | no-asynch |
|---------------------|-----------|

Run database operations as batches, in single transactions.

#### <span id="page-140-5"></span>• [--no-defaults](#page-140-5)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

#### <span id="page-140-6"></span>• [--no-hint](#page-140-6)

| Command-Line Format | no-hint |
|---------------------|---------|

Do not use distribution key hinting to select a data node.

### <span id="page-140-7"></span>• [--opbatch](#page-140-7)=#

| Command-Line Format | opbatch=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 256        |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of operations (including blob operations), and thus the number of asynchronous transactions, per execution batch.

#### <span id="page-141-0"></span>• [--opbytes](#page-141-0)=#

| Command-Line Format | opbytes=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of bytes per execution batch. Use 0 for no limit.

#### <span id="page-141-1"></span>• [--output-type](#page-141-1)=name

| Command-Line Format | output-type=name |
|---------------------|------------------|
| Type                | Enumeration      |
| Default Value       | ndb              |
| Valid Values        | null             |

Set the output type. ndb is the default. null is used only for testing.

#### <span id="page-141-2"></span>• [--output-workers](#page-141-2)=#

| Command-Line Format | output-workers=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 2                |
| Minimum Value       | 1                |
| Maximum Value       | 4294967295       |

Set the number of threads processing output or relaying database operations.

#### <span id="page-141-3"></span>• [--pagesize](#page-141-3)=#

| Command-Line Format | pagesize=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 4096       |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Align I/O buffers to the given size.

### <span id="page-142-0"></span>• [--pagecnt](#page-142-0)=#

| Command-Line Format | pagecnt=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 64         |
| Minimum Value       | 1          |
| Maximum Value       | 4294967295 |

Set the size of I/O buffers as multiple of page size. The CSV input worker allocates buffer that is doubled in size.

#### <span id="page-142-1"></span>• [--polltimeout](#page-142-1)=#

| Command-Line Format | polltimeout=# |
|---------------------|---------------|
| Type                | Integer       |
| Default Value       | 1000          |
| Minimum Value       | 1             |
| Maximum Value       | 4294967295    |
| Unit                | ms            |

Set a timeout per poll for completed asynchronous transactions; polling continues until all polls are completed, or until an error occurs.

#### <span id="page-142-2"></span>• [--print-defaults](#page-142-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

#### <span id="page-142-3"></span>• [--rejects](#page-142-3)=#

| Command-Line Format | rejects=#  |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |

Limit the number of rejected rows (rows with permanent errors) in the data load. The default is 0, which means that any rejected row causes a fatal error. Any rows causing the limit to be exceeded are added to the .rej file.

The limit imposed by this option is effective for the duration of the current run. A run restarted using [--resume](#page-142-4) is considered a "new" run for this purpose.

#### <span id="page-142-4"></span>• [--resume](#page-142-4)

| Command-Line Format | resume |
|---------------------|--------|
|---------------------|--------|

If a job is aborted (due to a temporary db error or when interrupted by the user), resume with any rows not yet processed.

#### <span id="page-142-5"></span>• [--rowbatch](#page-142-5)=#

| Command-Line Format | rowbatch=# |
|---------------------|------------|
|---------------------|------------|

| Type          | Integer    |
|---------------|------------|
| Default Value | 0          |
| Minimum Value | 0          |
| Maximum Value | 4294967295 |
| Unit          | rows       |

Set a limit on the number of rows per row queue. Use 0 for no limit.

<span id="page-143-0"></span>• [--rowbytes](#page-143-0)=#

| Command-Line Format | rowbytes=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 262144     |
| Minimum Value       | 0          |
| Maximum Value       | 4294967295 |
| Unit                | bytes      |

Set a limit on the number of bytes per row queue. Use 0 for no limit.

<span id="page-143-2"></span>• [--stats](#page-143-2)

| Command-Line Format | stats |
|---------------------|-------|

Save information about options related to performance and other internal statistics in files named \*.sto and \*.stt. These files are always kept on successful completion (even if [--keep-state](#page-138-3) is not also specified).

<span id="page-143-1"></span>• [--state-dir](#page-143-1)=name

| Command-Line Format | state-dir=path |
|---------------------|----------------|
| Type                | String         |
| Default Value       |                |

Where to write the state files (tbl\_name.map, tbl\_name.rej, tbl\_name.res, and tbl\_name.stt) produced by a run of the program; the default is the current directory.

<span id="page-143-3"></span>• [--table=](#page-143-3)name

| Command-Line Format | table=name             |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       | [input file base name] |

By default, [ndb\\_import](#page-128-1) attempts to import data into a table whose name is the base name of the CSV file from which the data is being read. Beginning with NDB 8.0.28, you can override the choice of table name by specifying it using the --table option (short form -t).

<span id="page-143-4"></span>• [--tempdelay](#page-143-4)=#

| Command-Line Format | tempdelay=# |
|---------------------|-------------|
| Type                | Integer     |
| Default Value       | 10          |
| Minimum Value       | 0           |

| Maximum Value | 4294967295 |
|---------------|------------|
| Unit          | ms         |

Number of milliseconds to sleep between temporary errors.

#### <span id="page-144-0"></span>• [--temperrors](#page-144-0)=#

| Command-Line Format | temperrors=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 0            |
| Minimum Value       | 0            |
| Maximum Value       | 4294967295   |

Number of times a transaction can fail due to a temporary error, per execution batch. The default is 0, which means that any temporary error is fatal. Temporary errors do not cause any rows to be added to the .rej file.

#### <span id="page-144-2"></span>• [--verbose](#page-144-2), -v

| Command-Line Format | verbose[=#] |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | false       |

Enable verbose output.

#### <span id="page-144-1"></span>• [--usage](#page-144-1)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-137-3).

#### <span id="page-144-3"></span>• [--version](#page-144-3)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

As with LOAD DATA, options for field and line formatting much match those used to create the CSV file, whether this was done using SELECT INTO ... OUTFILE, or by some other means. There is no equivalent to the LOAD DATA statement STARTING WITH option.

# <span id="page-144-4"></span>**25.5.14 ndb\_index\_stat — NDB Index Statistics Utility**

[ndb\\_index\\_stat](#page-144-4) provides per-fragment statistical information about indexes on NDB tables. This includes cache version and age, number of index entries per partition, and memory consumption by indexes.

## **Usage**

To obtain basic index statistics about a given NDB table, invoke [ndb\\_index\\_stat](#page-144-4) as shown here, with the name of the table as the first argument and the name of the database containing this table specified immediately following it, using the [--database](#page-148-0) (-d) option:

```
ndb_index_stat table -d database
```

In this example, we use [ndb\\_index\\_stat](#page-144-4) to obtain such information about an NDB table named mytable in the test database:

```
$> ndb_index_stat -d test mytable
table:City index:PRIMARY fragCount:2
sampleVersion:3 loadTime:1399585986 sampleCount:1994 keyBytes:7976
query cache: valid:1 sampleCount:1994 totalBytes:27916
times in ms: save: 7.133 sort: 1.974 sort per sample: 0.000
```

sampleVersion is the version number of the cache from which the statistics data is taken. Running [ndb\\_index\\_stat](#page-144-4) with the [--update](#page-151-0) option causes sampleVersion to be incremented.

loadTime shows when the cache was last updated. This is expressed as seconds since the Unix Epoch.

sampleCount is the number of index entries found per partition. You can estimate the total number of entries by multiplying this by the number of fragments (shown as fragCount).

sampleCount can be compared with the cardinality of SHOW INDEX or INFORMATION\_SCHEMA.STATISTICS, although the latter two provide a view of the table as a whole, while [ndb\\_index\\_stat](#page-144-4) provides a per-fragment average.

keyBytes is the number of bytes used by the index. In this example, the primary key is an integer, which requires four bytes for each index, so keyBytes can be calculated in this case as shown here:

```
 keyBytes = sampleCount * (4 bytes per index) = 1994 * 4 = 7976
```

This information can also be obtained using the corresponding column definitions from INFORMATION\_SCHEMA.COLUMNS (this requires a MySQL Server and a MySQL client application).

totalBytes is the total memory consumed by all indexes on the table, in bytes.

Timings shown in the preceding examples are specific to each invocation of [ndb\\_index\\_stat](#page-144-4).

The [--verbose](#page-151-1) option provides some additional output, as shown here:

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

If the output from the program is empty, this may indicate that no statistics yet exist. To force them to be created (or updated if they already exist), invoke [ndb\\_index\\_stat](#page-144-4) with the [--update](#page-151-0) option, or execute ANALYZE TABLE on the table in the mysql client.

## **Options**

The following table includes options that are specific to the NDB Cluster [ndb\\_index\\_stat](#page-144-4) utility. Additional descriptions are listed following the table.

**Table 25.36 Command-line options used with the program ndb\_index\_stat**

| Format                     | Description                                             | Added, Deprecated, or<br>Removed                      |
|----------------------------|---------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path | Directory containing character<br>sets                  | REMOVED: 8.0.31                                       |
| connect-retries=#          | Number of times to retry<br>connection before giving up | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                                          | Description                                                                                                                                                       | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retry-delay=#                                           | Number of seconds to wait<br>between attempts to contact<br>management server                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string,                            | Same asndb-connectstring                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                                            |                                                                                                                                                                   |                                                       |
| core-file                                                       | Write core file on error; used in<br>debugging                                                                                                                    | REMOVED: 8.0.31                                       |
| database=name,                                                  | Name of database containing<br>table                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name<br>defaults-extra<br>file=path                          | Read given file after global files<br>are read                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                                              | Read default options from given<br>file only                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string                                 | Also read groups with<br>concat(group, suffix)                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| delete                                                          | Delete index statistics for table,<br>stopping any auto-update<br>previously configured                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| dump                                                            | Print query cache                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,<br>-?                                                     | Display help text and exit                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                                                 | Read given path from login file                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| loops=#                                                         | Set the number of times to<br>perform given command; default<br>is 0                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-mgmd<br>host=connection_string,                             | Same asndb-connectstring                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                     | REMOVED: 8.0.31                                       |

| Format                     | Description                                                                                                                      | Added, Deprecated, or<br>Removed                      |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| no-defaults                | Do not read default options from<br>any option file other than login<br>file                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults             | Print program argument list and<br>exit                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| query=#                    | Perform random range queries<br>on first key attr (must be int<br>unsigned)                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-drop                   | Drop any statistics tables<br>and events in NDB kernel (all<br>statistics are lost)                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-create                 | Create all statistics tables and<br>events in NDB kernel, if none of<br>them already exist                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-create-if-not<br>exist | Create any statistics tables and<br>events in NDB kernel that do not<br>already exist                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-create-if-not<br>valid | Create any statistics tables or<br>events that do not already exist<br>in the NDB kernel, after dropping<br>any that are invalid | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-check                  | Verify that NDB system index<br>statistics and event tables exist                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-skip-tables            | Do not apply sys-* options to<br>tables                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| sys-skip-events            | Do not apply sys-* options to<br>events                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| update                     | Update index statistics for table,<br>restarting any auto-update<br>previously configured                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,                     | Display help text and exit; same<br>ashelp                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?<br>verbose,             | Turn on verbose output                                                                                                           | (Supported in all NDB releases                        |
|                            |                                                                                                                                  | based on MySQL 8.0)                                   |
| -v<br>version,             | Display version information and                                                                                                  | (Supported in all NDB releases                        |
| -V                         | exit                                                                                                                             | based on MySQL 8.0)                                   |

## <span id="page-147-0"></span>• [--character-sets-dir](#page-147-0)

Directory containing character sets.

#### <span id="page-147-1"></span>• [--connect-retries](#page-147-1)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |

| Maximum Value | 12 |  |
|---------------|----|--|
|---------------|----|--|

Number of times to retry connection before giving up.

<span id="page-148-1"></span>• [--connect-retry-delay](#page-148-1)

| Command-Line Format | connect-retry-delay=# |  |
|---------------------|-----------------------|--|
| Type                | Integer               |  |
| Default Value       | 5                     |  |
| Minimum Value       | 0                     |  |
| Maximum Value       | 5                     |  |

Number of seconds to wait between attempts to contact management server.

<span id="page-148-2"></span>• [--connect-string](#page-148-2)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-149-6).

<span id="page-148-3"></span>• [--core-file](#page-148-3)

Write core file on error; used in debugging.

<span id="page-148-0"></span>• [--database=](#page-148-0)name, -d name

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [none]        |
| Minimum Value       |               |
| Maximum Value       |               |

The name of the database that contains the table being queried.

<span id="page-148-4"></span>• [--defaults-extra-file](#page-148-4)

| Command-Line Format | defaults-extra-file=path |  |
|---------------------|--------------------------|--|
| Type                | String                   |  |
| Default Value       | [none]                   |  |

Read given file after global files are read.

<span id="page-148-5"></span>• [--defaults-file](#page-148-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

<span id="page-149-0"></span>• [--defaults-group-suffix](#page-149-0)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-149-1"></span>• [--delete](#page-149-1)

| Command-Line Format | delete |
|---------------------|--------|
|---------------------|--------|

Delete the index statistics for the given table, stopping any auto-update that was previously configured.

<span id="page-149-2"></span>• [--dump](#page-149-2)

| Command-Line Format | dump |
|---------------------|------|
|---------------------|------|

Dump the contents of the query cache.

<span id="page-149-3"></span>• [--help](#page-149-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-149-4"></span>• [--login-path](#page-149-4)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-149-5"></span>• [--loops=](#page-149-5)#

| Command-Line Format | loops=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 0       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

Repeat commands this number of times (for use in testing).

<span id="page-149-6"></span>• [--ndb-connectstring](#page-149-6)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-149-7"></span>• [--ndb-mgmd-host](#page-149-7)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-149-6).

<span id="page-150-0"></span>• [--ndb-nodeid](#page-150-0)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-149-6).

<span id="page-150-1"></span>• [--ndb-optimized-node-selection](#page-150-1)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-150-2"></span>• [--no-defaults](#page-150-2)

| Command-Line Format<br>no-defaults |
|------------------------------------|
|------------------------------------|

Do not read default options from any option file other than login file.

<span id="page-150-3"></span>• [--print-defaults](#page-150-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-150-4"></span>• [--query=](#page-150-4)#

| Command-Line Format | query=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 0       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

Perform random range queries on first key attribute (must be int unsigned).

<span id="page-150-5"></span>• [--sys-drop](#page-150-5)

| Command-Line Format | sys-drop |
|---------------------|----------|

Drop all statistics tables and events in the NDB kernel. This causes all statistics to be lost.

<span id="page-150-6"></span>• [--sys-create](#page-150-6)

| Command-Line Format | sys-create |
|---------------------|------------|

Create all statistics tables and events in the NDB kernel. This works only if none of them exist previously. 4521 <span id="page-151-2"></span>• [--sys-create-if-not-exist](#page-151-2)

Create any NDB system statistics tables or events (or both) that do not already exist when the program is invoked.

<span id="page-151-3"></span>• [--sys-create-if-not-valid](#page-151-3)

Create any NDB system statistics tables or events that do not already exist, after dropping any that are invalid.

<span id="page-151-4"></span>• [--sys-check](#page-151-4)

| Command-Line Format | sys-check |
|---------------------|-----------|
|---------------------|-----------|

Verify that all required system statistics tables and events exist in the NDB kernel.

<span id="page-151-5"></span>• [--sys-skip-tables](#page-151-5)

| Command-Line Format | sys-skip-tables |
|---------------------|-----------------|
|                     |                 |

Do not apply any --sys-\* options to any statistics tables.

<span id="page-151-6"></span>• [--sys-skip-events](#page-151-6)

| Command-Line Format | sys-skip-events |
|---------------------|-----------------|
|---------------------|-----------------|

Do not apply any --sys-\* options to any events.

<span id="page-151-0"></span>• [--update](#page-151-0)

| Command-Line Format | update |
|---------------------|--------|
|---------------------|--------|

Update the index statistics for the given table, and restart any auto-update that was previously configured.

<span id="page-151-7"></span>• [--usage](#page-151-7)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-149-3).

<span id="page-151-1"></span>• [--verbose](#page-151-1)

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Turn on verbose output.

<span id="page-151-8"></span>• [--version](#page-151-8)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-151-9"></span>**ndb\_index\_stat system options.** The following options are used to generate and update the statistics tables in the NDB kernel. None of these options can be mixed with statistics options (see [ndb\\_index\\_stat statistics options\)](#page-152-0).

- [--sys-drop](#page-150-5)
- [--sys-create](#page-150-6)
- [--sys-create-if-not-exist](#page-151-2)
- [--sys-create-if-not-valid](#page-151-3)
- [--sys-check](#page-151-4)
- [--sys-skip-tables](#page-151-5)
- [--sys-skip-events](#page-151-6)

<span id="page-152-0"></span>**ndb\_index\_stat statistics options.** The options listed here are used to generate index statistics. They work with a given table and database. They cannot be mixed with system options (see [ndb\\_index\\_stat system options](#page-151-9)).

- [--database](#page-148-0)
- [--delete](#page-149-1)
- [--update](#page-151-0)
- [--dump](#page-149-2)
- [--query](#page-150-4)

## <span id="page-152-1"></span>**25.5.15 ndb\_move\_data — NDB Data Copy Utility**

[ndb\\_move\\_data](#page-152-1) copies data from one NDB table to another.

## **Usage**

The program is invoked with the names of the source and target tables; either or both of these may be qualified optionally with the database name. Both tables must use the NDB storage engine.

```
ndb_move_data options source target
```

Options that can be used with [ndb\\_move\\_data](#page-152-1) are shown in the following table. Additional descriptions follow the table.

**Table 25.37 Command-line options used with the program ndb\_move\_data**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| abort-on-error                       | Dump core on permanent error<br>(debug option)                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| character-sets<br>dir=path           | Directory where character sets<br>are                                         | REMOVED: 8.0.31                                       |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string<br>core-file    | Write core file on error; used in<br>debugging                                | REMOVED: 8.0.31                                       |

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| database=name,                          | Name of database in which table<br>is found                                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d name                                 |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                      | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| drop-source                             | Drop source table after all rows<br>have been moved                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| error-insert                            | Insert random temporary errors<br>(used in testing)                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-missing<br>columns              | Ignore extra columns in source<br>or target table                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                   | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                      |                                                                                                                                               |                                                       |
| login-path=path                         | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| lossy-conversions,                      | Allow attribute data to be<br>truncated when converted to                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -l                                      | smaller type                                                                                                                                  |                                                       |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd                                | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases                        |
| host=connection_string,                 |                                                                                                                                               | based on MySQL 8.0)                                   |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | REMOVED: 8.0.31                                       |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| promote-attributes,                     | Allow attribute data to be<br>converted to larger type                                                                                        | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -A                                      |                                                                                                                                               |                                                       |

| Format                     | Description                                                                                                                        | Added, Deprecated, or<br>Removed                      |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| staging<br>tries=x[,y[,z]] | Specify tries on temporary errors;<br>format is x[,y[,z]] where x=max<br>tries (0=no limit), y=min delay<br>(ms), z=max delay (ms) | (Supported in all NDB releases<br>based on MySQL 8.0) |
| usage,<br>-?               | Display help text and exit; same<br>ashelp                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| verbose                    | Enable verbose messages                                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| version,<br>-V             | Display version information and<br>exit                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |

<span id="page-154-0"></span>• [--abort-on-error](#page-154-0)

| Command-Line Format | abort-on-error |
|---------------------|----------------|
|---------------------|----------------|

Dump core on permanent error (debug option).

<span id="page-154-1"></span>• [--character-sets-dir](#page-154-1)=name

Directory where character sets are.

<span id="page-154-3"></span>• [--connect-retry-delay](#page-154-3)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-154-2"></span>• [--connect-retries](#page-154-2)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-154-4"></span>• [--connect-string](#page-154-4)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

<span id="page-155-0"></span>• [--core-file](#page-155-0)

Write core file on error; used in debugging.

<span id="page-155-1"></span>• [--database](#page-155-1)=dbname, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table is found.

<span id="page-155-2"></span>• [--defaults-extra-file](#page-155-2)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-155-3"></span>• [--defaults-file](#page-155-3)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-155-4"></span>• [--defaults-group-suffix](#page-155-4)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-155-5"></span>• [--drop-source](#page-155-5)

| Command-Line Format | drop-source |
|---------------------|-------------|

Drop source table after all rows have been moved.

<span id="page-155-6"></span>• [--error-insert](#page-155-6)

| Command-Line Format | error-insert |
|---------------------|--------------|
|---------------------|--------------|

Insert random temporary errors (testing option).

<span id="page-155-7"></span>• [--exclude-missing-columns](#page-155-7)

| Command-Line Format | exclude-missing-columns |
|---------------------|-------------------------|
|---------------------|-------------------------|

Ignore extra columns in source or target table.

<span id="page-155-8"></span>• [--help](#page-155-8)

| Command-Line Format | help |
|---------------------|------|

#### Display help text and exit.

#### <span id="page-156-0"></span>• [--login-path](#page-156-0)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

#### Read given path from login file.

<span id="page-156-1"></span>• [--lossy-conversions](#page-156-1), -l

| Command-Line Format | lossy-conversions |
|---------------------|-------------------|
|---------------------|-------------------|

Allow attribute data to be truncated when converted to a smaller type.

#### <span id="page-156-2"></span>• [--ndb-connectstring](#page-156-2)

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

#### <span id="page-156-3"></span>• [--ndb-mgmd-host](#page-156-3)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-156-2).

#### <span id="page-156-4"></span>• [--ndb-nodeid](#page-156-4)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-156-2).

#### <span id="page-156-5"></span>• [--ndb-optimized-node-selection](#page-156-5)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

## <span id="page-156-6"></span>• [--no-defaults](#page-156-6)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

#### <span id="page-156-7"></span>• [--print-defaults](#page-156-7)

Print program argument list and exit.

<span id="page-157-0"></span>• [--promote-attributes](#page-157-0), -A

| Command-Line Format | promote-attributes |
|---------------------|--------------------|
|---------------------|--------------------|

Allow attribute data to be converted to a larger type.

<span id="page-157-1"></span>• [--staging-tries](#page-157-1)=x[,y[,z]]

| Command-Line Format | staging-tries=x[,y[,z]] |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | 0,1000,60000            |

Specify tries on temporary errors. Format is x[,y[,z]] where x=max tries (0=no limit), y=min delay (ms), z=max delay (ms).

<span id="page-157-2"></span>• [--usage](#page-157-2)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-155-8).

<span id="page-157-3"></span>• [--verbose](#page-157-3)

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Enable verbose messages.

<span id="page-157-4"></span>• [--version](#page-157-4)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-157-5"></span>**25.5.16 ndb\_perror — Obtain NDB Error Message Information**

[ndb\\_perror](#page-157-5) shows information about an NDB error, given its error code. This includes the error message, the type of error, and whether the error is permanent or temporary. This is intended as a drop-in replacement for perror --ndb, which is no longer supported.

## **Usage**

```
ndb_perror [options] error_code
```

[ndb\\_perror](#page-157-5) does not need to access a running NDB Cluster, or any nodes (including SQL nodes). To view information about a given NDB error, invoke the program, using the error code as an argument, like this:

```
$> ndb_perror 323
NDB error code 323: Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

To display only the error message, invoke [ndb\\_perror](#page-157-5) with the [--silent](#page-159-0) option (short form -s), as shown here:

```
$> ndb_perror -s 323
Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

Like perror, [ndb\\_perror](#page-157-5) accepts multiple error codes:

```
$> ndb_perror 321 1001
```

```
NDB error code 321: Invalid nodegroup id: Permanent error: Application error
NDB error code 1001: Illegal connect string
```

Additional program options for [ndb\\_perror](#page-157-5) are described later in this section.

[ndb\\_perror](#page-157-5) replaces perror --ndb, which is no longer supported by NDB Cluster. To make substitution easier in scripts and other applications that might depend on perror for obtaining NDB error information, [ndb\\_perror](#page-157-5) supports its own "dummy" [--ndb](#page-159-1) option, which does nothing.

The following table includes all options that are specific to the NDB Cluster program [ndb\\_perror](#page-157-5). Additional descriptions follow the table.

**Table 25.38 Command-line options used with the program ndb\_perror**

| Format                          | Description                                                                                 | Added, Deprecated, or<br>Removed                      |
|---------------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------|
| defaults-extra<br>file=path     | Read given file after global files<br>are read                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path              | Read default options from given<br>file only                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string | Also read groups with<br>concat(group, suffix)                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,<br>-?                     | Display help text                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                 | Read given path from login file                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb                             | For compatibility with<br>applications depending on old<br>versions of perror; does nothing | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| silent,                         | Show error message only                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -s                              |                                                                                             |                                                       |
| version,                        | Print program version information<br>and exit                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                              |                                                                                             |                                                       |
| verbose,                        | Verbose output; disable with<br>silent                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -v                              |                                                                                             |                                                       |

## <span id="page-158-0"></span>**Additional Options**

• [--defaults-extra-file](#page-158-0)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-158-1"></span>• [--defaults-file](#page-158-1)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-159-2"></span>• [--defaults-group-suffix](#page-159-2)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-159-3"></span>• [--help](#page-159-3), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display program help text and exit.

<span id="page-159-4"></span>• [--login-path](#page-159-4)

| Command-Line Format | login-path=path |  |
|---------------------|-----------------|--|
| Type                | String          |  |
| Default Value       | [none]          |  |

Read given path from login file.

<span id="page-159-1"></span>• [--ndb](#page-159-1)

| Command-Line Format | ndb |
|---------------------|-----|
|                     |     |

For compatibility with applications depending on old versions of perror that use that program's - ndb option. The option when used with [ndb\\_perror](#page-157-5) does nothing, and is ignored by it.

<span id="page-159-5"></span>• [--no-defaults](#page-159-5)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-159-6"></span>• [--print-defaults](#page-159-6)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-159-0"></span>• [--silent](#page-159-0), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Show error message only.

<span id="page-159-7"></span>• [--version](#page-159-7), -V

| Command-Line Format | version |
|---------------------|---------|

Print program version information and exit.

<span id="page-160-0"></span>• [--verbose](#page-160-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose output; disable with [--silent](#page-159-0).

## <span id="page-160-1"></span>**25.5.17 ndb\_print\_backup\_file — Print NDB Backup File Contents**

[ndb\\_print\\_backup\\_file](#page-160-1) obtains diagnostic information from a cluster backup file.

**Table 25.39 Command-line options used with the program ndb\_print\_backup\_file**

| Format                          | Description                                                                  | Added, Deprecated, or<br>Removed                      |
|---------------------------------|------------------------------------------------------------------------------|-------------------------------------------------------|
| backup-key=key,                 | Use this password to decrypt file                                            | ADDED: NDB 8.0.31                                     |
| -K password                     |                                                                              |                                                       |
| backup-key-from-stdin           | Get decryption key in a secure<br>fashion from STDIN                         | ADDED: NDB 8.0.31                                     |
| backup<br>password=password,    | Use this password to decrypt file                                            | ADDED: NDB 8.0.22                                     |
| -P password                     |                                                                              |                                                       |
| backup-password-from<br>stdin   | Get decryption password in a<br>secure fashion from STDIN                    | ADDED: NDB 8.0.24                                     |
| control-directory<br>number=#,  | Control directory number                                                     | ADDED: NDB 8.0.24                                     |
| -c #                            |                                                                              |                                                       |
| defaults-extra<br>file=path     | Read given file after global files<br>are read                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path              | Read default options from given<br>file only                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string | Also read groups with<br>concat(group, suffix)                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fragment-id=#,                  | Fragment ID                                                                  | ADDED: NDB 8.0.24                                     |
| -f #                            |                                                                              |                                                       |
| help,                           | Print usage information                                                      | ADDED: NDB 8.0.24                                     |
| usage,                          |                                                                              |                                                       |
| -h,                             |                                                                              |                                                       |
| -?                              |                                                                              |                                                       |
| login-path=path                 | Read given path from login file                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-print-rows,                  | Do not print rows                                                            | ADDED: NDB 8.0.24                                     |
| -u                              |                                                                              |                                                       |
|                                 |                                                                              |                                                       |

| Format              | Description                                                  | Added, Deprecated, or<br>Removed                      |
|---------------------|--------------------------------------------------------------|-------------------------------------------------------|
| print-defaults      | Print program argument list and<br>exit                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-header-words, | Print header words                                           | ADDED: NDB 8.0.24                                     |
| -h                  |                                                              |                                                       |
| print-restored-rows | Print restored rows                                          | ADDED: NDB 8.0.24                                     |
| print-rows,         | Print rows. Enabled by default;<br>disable withno-print-rows | ADDED: NDB 8.0.24                                     |
| -U                  |                                                              |                                                       |
| print-rows-per-page | Print rows per page                                          | ADDED: NDB 8.0.24                                     |
| rowid-file=path,    | File containing row ID to check<br>for                       | ADDED: NDB 8.0.24                                     |
| -n path             |                                                              |                                                       |
| show-ignored-rows,  | Show ignored rows                                            | ADDED: NDB 8.0.24                                     |
| -i                  |                                                              |                                                       |
| table-id=#,         | Table ID; used withprint<br>restored rows                    | ADDED: NDB 8.0.24                                     |
| -t #                |                                                              |                                                       |
| usage,              | Display help text and exit; same<br>ashelp                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                  |                                                              |                                                       |
| verbose[=#],        | Verbosity level                                              | ADDED: NDB 8.0.24                                     |
| -v                  |                                                              |                                                       |
| version,            | Display version information and<br>exit                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                  |                                                              |                                                       |

## **Usage**

ndb\_print\_backup\_file [-P password] file\_name

file\_name is the name of a cluster backup file. This can be any of the files (.Data, .ctl, or .log file) found in a cluster backup directory. These files are found in the data node's backup directory under the subdirectory BACKUP-#, where # is the sequence number for the backup. For more information about cluster backup files and their contents, see Section 25.6.8.1, "NDB Cluster Backup Concepts".

Like [ndb\\_print\\_schema\\_file](#page-167-0) and [ndb\\_print\\_sys\\_file](#page-167-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_backup\\_file](#page-160-1) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

In NDB 8.0, this program can also be used to read undo log files.

## **Options**

Prior to NDB 8.0.24, [ndb\\_print\\_backup\\_file](#page-160-1) supported only the -P option. Beginning with NDB 8.0.24, the program supports a number of options, which are described in the following list.

<span id="page-161-0"></span>• [--backup-key](#page-161-0), -K

| Command-Line Format | backup-key=key |
|---------------------|----------------|
|---------------------|----------------|

Specify the key needed to decrypt an encrypted backup.

<span id="page-162-0"></span>• [--backup-key-from-stdin](#page-162-0)

| Command-Line Format | backup-key-from-stdin |
|---------------------|-----------------------|
|---------------------|-----------------------|

Allow input of the decryption key from standard input, similar to entering a password after invoking mysql --password with no password supplied.

<span id="page-162-1"></span>• [--backup-password](#page-162-1)

| Command-Line Format | backup-password=password |  |
|---------------------|--------------------------|--|
| Type                | String                   |  |
| Default Value       | [none]                   |  |

Specify the password needed to decrypt an encrypted backup.

The long form of this option is available beginning with NDB 8.0.24.

<span id="page-162-2"></span>• [--backup-password-from-stdin](#page-162-2)

| Command-Line Format | backup-password-from-stdin |
|---------------------|----------------------------|
|---------------------|----------------------------|

Allow input of the password from standard input, similar to entering a password after invoking mysql --password with no password supplied.

<span id="page-162-3"></span>• [--control-directory-number](#page-162-3)

| Command-Line Format | control-directory-number=# |  |
|---------------------|----------------------------|--|
| Type                | Integer                    |  |
| Default Value       | 0                          |  |

Control file directory number. Used together with [--print-restored-rows](#page-163-7).

<span id="page-162-4"></span>• [--defaults-extra-file](#page-162-4)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-162-5"></span>• [--defaults-file](#page-162-5)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-162-6"></span>• [--defaults-group-suffix](#page-162-6)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-163-0"></span>• [--fragment-id](#page-163-0)

| Command-Line Format | fragment-id=# |
|---------------------|---------------|
| Type                | Integer       |
| Default Value       | 0             |

Fragment ID. Used together with [--print-restored-rows](#page-163-7).

<span id="page-163-1"></span>• [--help](#page-163-1)

| Command-Line Format | help  |
|---------------------|-------|
|                     | usage |

Print program usage information.

<span id="page-163-2"></span>• [--login-path](#page-163-2)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-163-3"></span>• [--no-defaults](#page-163-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-163-4"></span>• [--no-print-rows](#page-163-4)

| Command-Line Format | no-print-rows |
|---------------------|---------------|
|---------------------|---------------|

Do not include rows in output.

<span id="page-163-5"></span>• [--print-defaults](#page-163-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-163-6"></span>• [--print-header-words](#page-163-6)

| Command-Line Format<br>print-header-words |
|-------------------------------------------|
|-------------------------------------------|

Include header words in output.

<span id="page-163-7"></span>• [--print-restored-rows](#page-163-7)

| Command-Line Format | print-restored-rows |
|---------------------|---------------------|
|---------------------|---------------------|

Include restored rows in output, using the file LCP/c/TtFf.ctl, for which the values are set as follows:

• c is the control file number set using [--control-directory-number](#page-162-3)

- t is the table ID set using [--table-id](#page-164-4)
- f is the fragment ID set using [--fragment-id](#page-163-0)
- <span id="page-164-0"></span>• [--print-rows](#page-164-0)

| Command-Line Format | print-rows |
|---------------------|------------|
|---------------------|------------|

Print rows. This option is enabled by default; to disable it, use [--no-print-rows](#page-163-4).

<span id="page-164-1"></span>• [--print-rows-per-page](#page-164-1)

| Command-Line Format | print-rows-per-page |
|---------------------|---------------------|
|                     |                     |

Print rows per page.

<span id="page-164-2"></span>• [--rowid-file](#page-164-2)

| Command-Line Format | rowid-file=path |
|---------------------|-----------------|
| Type                | File name       |
| Default Value       | [none]          |

File to check for row ID.

<span id="page-164-3"></span>• [--show-ignored-rows](#page-164-3)

| Command-Line Format | show-ignored-rows |
|---------------------|-------------------|
|---------------------|-------------------|

Show ignored rows.

<span id="page-164-4"></span>• [--table-id](#page-164-4)

| Command-Line Format | table-id=# |  |
|---------------------|------------|--|
| Type                | Integer    |  |
| Default Value       | [none]     |  |

Table ID. Used together with [--print-restored-rows](#page-163-7).

<span id="page-164-5"></span>• [--usage](#page-164-5)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-163-1).

<span id="page-164-6"></span>• [--verbose](#page-164-6)

| Command-Line Format | verbose[=#] |  |
|---------------------|-------------|--|
| Type                | Integer     |  |
| Default Value       | 0           |  |

Verbosity level of output. A greater value indicates increased verbosity.

<span id="page-164-7"></span>• [--version](#page-164-7)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

## <span id="page-165-0"></span>**25.5.18 ndb\_print\_file — Print NDB Disk Data File Contents**

[ndb\\_print\\_file](#page-165-0) obtains information from an NDB Cluster Disk Data file.

## **Usage**

```
ndb_print_file [-v] [-q] file_name+
```

file\_name is the name of an NDB Cluster Disk Data file. Multiple filenames are accepted, separated by spaces.

Like [ndb\\_print\\_schema\\_file](#page-167-0) and [ndb\\_print\\_sys\\_file](#page-167-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_file](#page-165-0) must be run on an NDB Cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

## **Options**

**Table 25.40 Command-line options used with the program ndb\_print\_file**

| Format              | Description                                               | Added, Deprecated, or<br>Removed                      |
|---------------------|-----------------------------------------------------------|-------------------------------------------------------|
| file-key=hex_data,  | Supply encryption key using<br>stdin, tty, or my.cnf file | ADDED: NDB 8.0.31                                     |
| -K hex_data         |                                                           |                                                       |
| file-key-from-stdin | Supply encryption key using<br>stdin                      | ADDED: NDB 8.0.31                                     |
| help,               | Display help text and exit; same<br>asusage               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                  |                                                           |                                                       |
| quiet,              | Reduce verbosity of output                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -q                  |                                                           |                                                       |
| usage,              | Display help text and exit; same<br>ashelp                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                  |                                                           |                                                       |
| verbose,            | Increase verbosity of output                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -v                  |                                                           |                                                       |
| version,            | Display version information and<br>exit                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                  |                                                           |                                                       |

[ndb\\_print\\_file](#page-165-0) supports the following options:

<span id="page-165-1"></span>• [--file-key](#page-165-1), -K

| Command-Line Format | file-key=hex_data |
|---------------------|-------------------|

Supply file system encryption or decryption key from stdin, tty, or a my.cnf file.

<span id="page-165-2"></span>• [--file-key-from-stdin](#page-165-2)

| Command-Line Format | file-key-from-stdin |  |
|---------------------|---------------------|--|
| Type                | Boolean             |  |
| Default Value       | FALSE               |  |

Valid Values TRUE

Supply file system encryption or decryption key from stdin.

<span id="page-166-0"></span>• [--help](#page-166-0), -h, -?

Command-Line Format --help

Print help message and exit.

<span id="page-166-1"></span>• [--quiet](#page-166-1), -q

| Command-Line Format | quiet |
|---------------------|-------|
|---------------------|-------|

Suppress output (quiet mode).

<span id="page-166-2"></span>• [--usage](#page-166-2), -?

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Print help message and exit.

<span id="page-166-3"></span>• [--verbose](#page-166-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Make output verbose.

<span id="page-166-4"></span>• [--version](#page-166-4), -v

| Command-Line Format | version |
|---------------------|---------|
|                     |         |

Print version information and exit.

For more information, see Section 25.6.11, "NDB Cluster Disk Data Tables".

# <span id="page-166-5"></span>**25.5.19 ndb\_print\_frag\_file — Print NDB Fragment List File Contents**

[ndb\\_print\\_frag\\_file](#page-166-5) obtains information from a cluster fragment list file. It is intended for use in helping to diagnose issues with data node restarts.

## **Usage**

```
ndb_print_frag_file file_name
```

file\_name is the name of a cluster fragment list file, which matches the pattern SX.FragList, where X is a digit in the range 2-9 inclusive, and are found in the data node file system of the data node having the node ID nodeid, in directories named ndb\_nodeid\_fs/DN/DBDIH/, where N is 1 or 2. Each fragment file contains records of the fragments belonging to each NDB table. For more information about cluster fragment files, see [NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md).

Like [ndb\\_print\\_backup\\_file](#page-160-1), [ndb\\_print\\_sys\\_file](#page-167-1), and [ndb\\_print\\_schema\\_file](#page-167-0) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server), [ndb\\_print\\_frag\\_file](#page-166-5) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

## **Additional Options**

None.

## **Sample Output**

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
LcpNo[0]: maxGciCompleted: 1 maxGciStarted: 2 lcpId: 1 lcpStatus: valid
LcpNo[1]: maxGciCompleted: 0 maxGciStarted: 0 lcpId: 0 lcpStatus: invalid
```

# <span id="page-167-0"></span>**25.5.20 ndb\_print\_schema\_file — Print NDB Schema File Contents**

[ndb\\_print\\_schema\\_file](#page-167-0) obtains diagnostic information from a cluster schema file.

## **Usage**

```
ndb_print_schema_file file_name
```

file\_name is the name of a cluster schema file. For more information about cluster schema files, see [NDB Cluster Data Node File System Directory.](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md)

Like [ndb\\_print\\_backup\\_file](#page-160-1) and [ndb\\_print\\_sys\\_file](#page-167-1) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_schema\\_file](#page-167-0) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

## **Additional Options**

None.

# <span id="page-167-1"></span>**25.5.21 ndb\_print\_sys\_file — Print NDB System File Contents**

[ndb\\_print\\_sys\\_file](#page-167-1) obtains diagnostic information from an NDB Cluster system file.

## **Usage**

```
ndb_print_sys_file file_name
```

file\_name is the name of a cluster system file (sysfile). Cluster system files are located in a data node's data directory (DataDir); the path under this directory to system files matches the pattern ndb\_#\_fs/D#/DBDIH/P#.sysfile. In each case, the # represents a number (not necessarily the same number). For more information, see [NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md).

Like [ndb\\_print\\_backup\\_file](#page-160-1) and [ndb\\_print\\_schema\\_file](#page-167-0) (and unlike most of the other NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_print\\_backup\\_file](#page-160-1) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

## **Additional Options**

None.

# <span id="page-168-0"></span>**25.5.22 ndb\_redo\_log\_reader — Check and Print Content of Cluster Redo Log**

Reads a redo log file, checking it for errors, printing its contents in a human-readable format, or both. [ndb\\_redo\\_log\\_reader](#page-168-0) is intended for use primarily by NDB Cluster developers and Support personnel in debugging and diagnosing problems.

This utility remains under development, and its syntax and behavior are subject to change in future NDB Cluster releases.

The C++ source files for [ndb\\_redo\\_log\\_reader](#page-168-0) can be found in the directory /storage/ndb/src/ kernel/blocks/dblqh/redoLogReader.

Options that can be used with [ndb\\_redo\\_log\\_reader](#page-168-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.41 Command-line options used with the program ndb\_redo\_log\_reader**

| Format              | Description                                             | Added, Deprecated, or<br>Removed                      |
|---------------------|---------------------------------------------------------|-------------------------------------------------------|
| -dump               | Print dump info                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| file-key=key,       | Supply decryption key                                   | ADDED: NDB 8.0.31                                     |
| -K key              |                                                         |                                                       |
| file-key-from-stdin | Supply decryption key using<br>stdin                    | ADDED: NDB 8.0.31                                     |
| -filedescriptors    | Print file descriptors only                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help                | Print usage information (has no<br>short form)          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -lap                | Provide lap info, with max GCI<br>started and completed | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -mbyte #            | Starting megabyte                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -mbyteheaders       | Show only first page header of<br>each megabyte in file | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -nocheck            | Do not check records for errors                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -noprint            | Do not print records                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -page #             | Start with this page                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -pageheaders        | Show page headers only                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format       | Description                | Added, Deprecated, or<br>Removed                      |
|--------------|----------------------------|-------------------------------------------------------|
| -pageindex # | Start with this page index | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -twiddle     | Bit-shifted dump           | (Supported in all NDB releases<br>based on MySQL 8.0) |

## **Usage**

ndb\_redo\_log\_reader file\_name [options]

file\_name is the name of a cluster redo log file. redo log files are located in the numbered directories under the data node's data directory (DataDir); the path under this directory to the redo log files matches the pattern ndb\_nodeid\_fs/D#/DBLQH/S#.FragLog. nodeid is the data node's node ID. The two instances of # each represent a number (not necessarily the same number); the number following D is in the range 8-39 inclusive; the range of the number following S varies according to the value of the NoOfFragmentLogFiles configuration parameter, whose default value is 16; thus, the default range of the number in the file name is 0-15 inclusive. For more information, see [NDB Cluster](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md) [Data Node File System Directory.](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md)

The name of the file to be read may be followed by one or more of the options listed here:

<span id="page-169-0"></span>• [-dump](#page-169-0)

| Command-Line Format | -dump |
|---------------------|-------|
|---------------------|-------|

Print dump info.

<span id="page-169-1"></span>• [--file-key](#page-169-1), -K

| Command-Line Format | file-key=key |
|---------------------|--------------|
|---------------------|--------------|

Supply file decryption key using stdin, tty, or a my.cnf file.

<span id="page-169-2"></span>• [--file-key-from-stdin](#page-169-2)

| Command-Line Format |                     |
|---------------------|---------------------|
|                     | file-key-from-stdin |

Supply file decryption key using stdin.

<span id="page-169-3"></span>

| • | Command-Line Format | -filedescriptors |
|---|---------------------|------------------|
|   |                     |                  |

[-filedescriptors](#page-169-3): Print file descriptors only.

<span id="page-169-4"></span>

| • | Command-Line Format | help |  |
|---|---------------------|------|--|
|   |                     |      |  |

[--help](#page-169-4): Print usage information.

<span id="page-169-5"></span>• [-lap](#page-169-5)

| Command-Line Format | -lap |
|---------------------|------|
|---------------------|------|

Provide lap info, with max GCI started and completed.

<span id="page-169-6"></span>

| • | Command-Line Format | -mbyte # |
|---|---------------------|----------|
|   | Type                | Numeric  |
|   | Default Value       | 0        |

| Minimum Value | 0  |
|---------------|----|
| Maximum Value | 15 |

[-mbyte](#page-169-6) #: Starting megabyte.

# is an integer in the range 0 to 15, inclusive.

<span id="page-170-1"></span>• Command-Line Format -mbyteheaders

[-mbyteheaders](#page-170-1): Show only the first page header of every megabyte in the file.

<span id="page-170-3"></span>• Command-Line Format -noprint

[-noprint](#page-170-3): Do not print the contents of the log file.

<span id="page-170-2"></span>• Command-Line Format -nocheck

[-nocheck](#page-170-2): Do not check the log file for errors.

<span id="page-170-4"></span>

| • | Command-Line Format | -page # |
|---|---------------------|---------|
|   | Type                | Integer |
|   | Default Value       | 0       |
|   | Minimum Value       | 0       |
|   | Maximum Value       | 31      |

[-page](#page-170-4) #: Start at this page.

# is an integer in the range 0 to 31, inclusive.

<span id="page-170-5"></span>

| Command-Line Format | -pageheaders |
|---------------------|--------------|
|---------------------|--------------|

[-pageheaders](#page-170-5): Show page headers only.

<span id="page-170-6"></span>

| • | Command-Line Format | -pageindex # |
|---|---------------------|--------------|
|   | Type                | Integer      |
|   | Default Value       | 12           |
|   | Minimum Value       | 12           |
|   | Maximum Value       | 8191         |

[-pageindex](#page-170-6) #: Start at this page index.

# is an integer between 12 and 8191, inclusive.

<span id="page-170-7"></span>• [-twiddle](#page-170-7)

| Command-Line Format<br>-twiddle |  |
|---------------------------------|--|
|---------------------------------|--|

Bit-shifted dump.

Like [ndb\\_print\\_backup\\_file](#page-160-1) and [ndb\\_print\\_schema\\_file](#page-167-0) (and unlike most of the NDB utilities that are intended to be run on a management server host or to connect to a management server) [ndb\\_redo\\_log\\_reader](#page-168-0) must be run on a cluster data node, since it accesses the data node file system directly. Because it does not make use of the management server, this utility can be used when the management server is not running, and even when the cluster has been completely shut down.

# <span id="page-170-0"></span>**25.5.23 ndb\_restore — Restore an NDB Cluster Backup**

The NDB Cluster restoration program is implemented as a separate command-line utility [ndb\\_restore](#page-170-0), which can normally be found in the MySQL bin directory. This program reads the files created as a result of the backup and inserts the stored information into the database.

In NDB 7.6 and earlier, this program printed NDBT\_ProgramExit - status upon completion of its run, due to an unnecessary dependency on the NDBT testing library. This dependency has been removed in NDB 8.0, eliminating the extraneous output.

[ndb\\_restore](#page-170-0) must be executed once for each of the backup files that were created by the START BACKUP command used to create the backup (see Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup"). This is equal to the number of data nodes in the cluster at the time that the backup was created.

![](_page_171_Picture_4.jpeg)

#### **Note**

Before using [ndb\\_restore](#page-170-0), it is recommended that the cluster be running in single user mode, unless you are restoring multiple data nodes in parallel. See Section 25.6.6, "NDB Cluster Single User Mode", for more information.

Options that can be used with [ndb\\_restore](#page-170-0) are shown in the following table. Additional descriptions follow the table.

**Table 25.42 Command-line options used with the program ndb\_restore**

| Format                               | Description                                                                                                      | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| allow-pk-changes[=0 1]               | Allow changes to set of columns<br>making up table's primary key                                                 | ADDED: NDB 8.0.21                                     |
| append                               | Append data to tab-delimited file                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| backup<br>password=password          | Supply a password for decrypting<br>an encrypted backup with<br>decrypt; see documentation for<br>allowed values | ADDED: NDB 8.0.22                                     |
| backup-password-from<br>stdin        | Get decryption password in a<br>secure fashion from STDIN; use<br>together withdecrypt option                    | ADDED: NDB 8.0.24                                     |
| backup-path=path                     | Path to backup files directory                                                                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| backupid=#,                          | Restore from backup having this<br>ID                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -b #                                 |                                                                                                                  |                                                       |
| character-sets<br>dir=path           | Directory containing character<br>sets                                                                           | REMOVED: 8.0.31                                       |
| <br>connect=connection_string,       | Alias forconnectstring                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                 |                                                                                                                  |                                                       |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                 |                                                                                                                  |                                                       |

| Format                                          | Description                                                                                                                                                                              | Added, Deprecated, or<br>Removed                      |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| core-file                                       | Write core file on error; used in<br>debugging                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| decrypt                                         | Decrypt an encrypted backup;<br>requiresbackup-password                                                                                                                                  | ADDED: NDB 8.0.22                                     |
| defaults-extra<br>file=path                     | Read given file after global files<br>are read                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-file=path                              | Read default options from given<br>file only                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| defaults-group<br>suffix=string                 | Also read groups with<br>concat(group, suffix)                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 8.0) |
| disable-indexes                                 | Causes indexes from backup to<br>be ignored; may decrease time<br>needed to restore data                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| dont-ignore-systab-0,<br>-f                     | Do not ignore system table<br>during restore; experimental<br>only; not for production use                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-databases=list                          | List of one or more databases<br>to exclude (includes those not<br>named)                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-intermediate<br>sql-tables[=TRUE FALSE] | Do not restore any intermediate<br>tables (having names prefixed<br>with '#sql-') that were left over<br>from copying ALTER TABLE<br>operations; specify FALSE to<br>restore such tables | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-missing<br>columns                      | Causes columns from backup<br>version of table that are missing<br>from version of table in database<br>to be ignored                                                                    | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-missing-tables                          | Causes tables from backup that<br>are missing from database to be<br>ignored                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| exclude-tables=list                             | List of one or more tables to<br>exclude (includes those in same<br>database that are not named);<br>each table reference must<br>include database name                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-enclosed<br>by=char                      | Fields are enclosed by this<br>character                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-optionally<br>enclosed-by                | Fields are optionally enclosed by<br>this character                                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| fields-terminated<br>by=char                    | Fields are terminated by this<br>character                                                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| help,                                           | Display help text and exit                                                                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                                              |                                                                                                                                                                                          |                                                       |
| hex                                             | Print binary types in hexadecimal<br>format                                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                                  | Description                                                                                                                                             | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| ignore-extended-pk<br>updates[=0 1]     | Ignore log entries containing<br>updates to columns now included<br>in extended primary key                                                             | ADDED: NDB 8.0.21                                     |
| include-databases=list                  | List of one or more databases<br>to restore (excludes those not<br>named)                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| include-stored-grants                   | Restore shared users and grants<br>to ndb_sql_metadata table                                                                                            | ADDED: NDB 8.0.19                                     |
| include-tables=list                     | List of one or more tables to<br>restore (excludes those in same<br>database that are not named);<br>each table reference must<br>include database name | (Supported in all NDB releases<br>based on MySQL 8.0) |
| lines-terminated<br>by=char             | Lines are terminated by this<br>character                                                                                                               | (Supported in all NDB releases<br>based on MySQL 8.0) |
| login-path=path                         | Read given path from login file                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| lossy-conversions,<br>-L                | Allow lossy conversions of<br>column values (type demotions<br>or changes in sign) when<br>restoring data from backup                                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-binlog                               | If mysqld is connected and<br>using binary logging, do not log<br>restored data                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| no-restore-disk<br>objects,             | Do not restore objects relating to<br>Disk Data                                                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -d                                      |                                                                                                                                                         |                                                       |
| no-upgrade,<br>-u                       | Do not upgrade array type for<br>varsize attributes which do not<br>already resize VAR data, and do<br>not change column attributes                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                              | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                                     |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -c connection_string                    |                                                                                                                                                         |                                                       |
| ndb-nodegroup-map=map,<br>-z            | Specify node group map;<br>unused, unsupported                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                          | Description                                                                                                                                                         | Added, Deprecated, or<br>Removed                      |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| ndb-nodeid=#                    | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                       | REMOVED: 8.0.31                                       |
| nodeid=#,                       | ID of node where backup was<br>taken                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -n #                            |                                                                                                                                                                     |                                                       |
| num-slices=#                    | Number of slices to apply when<br>restoring by slice                                                                                                                | ADDED: NDB 8.0.20                                     |
| parallelism=#,<br>-p #          | Number of parallel transactions<br>to use while restoring data                                                                                                      | (Supported in all NDB releases<br>based on MySQL 8.0) |
| preserve-trailing               | Allow preservation of trailing                                                                                                                                      | (Supported in all NDB releases                        |
| spaces,                         | spaces (including padding) when<br>promoting fixed-width string                                                                                                     | based on MySQL 8.0)                                   |
| -P                              | types to variable-width types                                                                                                                                       |                                                       |
| print                           | Print metadata, data, and log to<br>stdout (equivalent toprint-meta<br>print-dataprint-log)                                                                         | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-data                      | Print data to stdout                                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-defaults                  | Print program argument list and<br>exit                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-log                       | Print log to stdout                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-meta                      | Print metadata to stdout                                                                                                                                            | (Supported in all NDB releases<br>based on MySQL 8.0) |
| print-sql-log                   | Write SQL log to stdout                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| progress-frequency=#            | Print status of restore each given<br>number of seconds                                                                                                             | (Supported in all NDB releases<br>based on MySQL 8.0) |
| promote-attributes,             | Allow attributes to be promoted<br>when restoring data from backup                                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -A                              |                                                                                                                                                                     |                                                       |
| rebuild-indexes                 | Causes multithreaded rebuilding<br>of ordered indexes found in<br>backup; number of threads<br>used is determined by setting<br>BuildIndexThreads                   | (Supported in all NDB releases<br>based on MySQL 8.0) |
| remap-column=string             | Apply offset to value of specified<br>column using indicated function<br>and arguments. Format is<br>[db].[tbl].[col]:[fn]:[args]; see<br>documentation for details | ADDED: NDB 8.0.21                                     |
| restore-data,                   | Restore table data and logs into<br>NDB Cluster using NDB API                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |

| Format                      | Description                                                                                                                                      | Added, Deprecated, or<br>Removed                      |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -r                          |                                                                                                                                                  |                                                       |
| restore-epoch,              | Restore epoch info into<br>status table; useful on replica                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -e                          | cluster for starting replication;<br>updates or inserts row in<br>mysql.ndb_apply_status with ID<br>0                                            |                                                       |
| restore-meta,               | Restore metadata to NDB<br>Cluster using NDB API                                                                                                 | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -m                          |                                                                                                                                                  |                                                       |
| restore-privilege<br>tables | Restore MySQL privilege tables<br>that were previously moved to<br>NDB                                                                           | DEPRECATED: NDB 8.0.16                                |
| rewrite<br>database=string  | Restore to differently named<br>database; format is olddb,newdb                                                                                  | (Supported in all NDB releases<br>based on MySQL 8.0) |
| skip-broken-objects         | Ignore missing blob tables in<br>backup file                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| skip-fk-checks              | Skips foreign key consistency<br>scan during index rebuild                                                                                       | ADDED: NDB 8.0.45                                     |
| skip-table-check,           | Skip table structure check during<br>restore                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -s                          |                                                                                                                                                  |                                                       |
| skip-unknown-objects        | Causes schema objects not<br>recognized by ndb_restore to be<br>ignored when restoring backup<br>made from newer NDB version to<br>older version | (Supported in all NDB releases<br>based on MySQL 8.0) |
| slice-id=#                  | Slice ID, when restoring by slices ADDED: NDB 8.0.20                                                                                             |                                                       |
| tab=path,                   | Creates a tab-separated .txt file                                                                                                                | (Supported in all NDB releases                        |
| -T path                     | for each table in path provided                                                                                                                  | based on MySQL 8.0)                                   |
| timestamp                   | Prefix all info, error, and debug                                                                                                                | ADDED: NDB 8.0.33                                     |
| printouts{=true false}      | log messages with timestamps                                                                                                                     |                                                       |
| usage,                      | Display help text and exit; same<br>ashelp                                                                                                       | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -?                          |                                                                                                                                                  |                                                       |
| verbose=#                   | Level of verbosity in output                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 8.0) |
| version,                    | Display version information and<br>exit                                                                                                          | (Supported in all NDB releases<br>based on MySQL 8.0) |
| -V                          |                                                                                                                                                  |                                                       |
| with-apply-status           | Restore the ndb_apply_status<br>table. Requiresrestore-data                                                                                      | ADDED: NDB 8.0.29                                     |

#### <span id="page-175-0"></span>• [--allow-pk-changes](#page-175-0)

| Command-Line Format | allow-pk-changes[=0 1] |
|---------------------|------------------------|
| Type                | Integer                |
| Default Value       | 0                      |
| Minimum Value       | 0                      |

| Maximum Value | 1 |
|---------------|---|
|---------------|---|

When this option is set to 1, [ndb\\_restore](#page-170-0) allows the primary keys in a table definition to differ from that of the same table in the backup. This may be desirable when backing up and restoring between different schema versions with primary key changes on one or more tables, and it appears that performing the restore operation using ndb\_restore is simpler or more efficient than issuing many ALTER TABLE statements after restoring table schemas and data.

The following changes in primary key definitions are supported by --allow-pk-changes:

• **Extending the primary key**: A non-nullable column that exists in the table schema in the backup becomes part of the table's primary key in the database.

![](_page_176_Picture_5.jpeg)

#### **Important**

When extending a table's primary key, any columns which become part of primary key must not be updated while the backup is being taken; any such updates discovered by [ndb\\_restore](#page-170-0) cause the restore operation to fail, even when no change in value takes place. In some cases, it may be possible to override this behavior using the [--ignore-extended-pk](#page-183-2)[updates](#page-183-2) option; see the description of this option for more information.

- **Contracting the primary key (1)**: A column that is already part of the table's primary key in the backup schema is no longer part of the primary key, but remains in the table.
- **Contracting the primary key (2)**: A column that is already part of the table's primary key in the backup schema is removed from the table entirely.

These differences can be combined with other schema differences supported by [ndb\\_restore](#page-170-0), including changes to blob and text columns requiring the use of staging tables.

Basic steps in a typical scenario using primary key schema changes are listed here:

- 1. Restore table schemas using [ndb\\_restore](#page-170-0) [--restore-meta](#page-192-2)
- 2. Alter schema to that desired, or create it
- 3. Back up the desired schema
- 4. Run [ndb\\_restore](#page-170-0) [--disable-indexes](#page-180-0) using the backup from the previous step, to drop indexes and constraints
- 5. Run [ndb\\_restore](#page-170-0) [--allow-pk-changes](#page-175-0) (possibly along with [--ignore-extended-pk](#page-183-2)[updates](#page-183-2), [--disable-indexes](#page-180-0), and possibly other options as needed) to restore all data
- 6. Run [ndb\\_restore](#page-170-0) [--rebuild-indexes](#page-191-0) using the backup made with the desired schema, to rebuild indexes and constraints

When extending the primary key, it may be necessary for [ndb\\_restore](#page-170-0) to use a temporary secondary unique index during the restore operation to map from the old primary key to the new one. Such an index is created only when necessary to apply events from the backup log to a table which has an extended primary key. This index is named NDB\$RESTORE\_PK\_MAPPING, and is created on each table requiring it; it can be shared, if necessary, by multiple instances of [ndb\\_restore](#page-170-0) instances running in parallel. (Running [ndb\\_restore](#page-170-0) [--rebuild-indexes](#page-191-0) at the end of the restore process causes this index to be dropped.)

#### <span id="page-177-0"></span>• [--append](#page-177-0)

| Command-Line Format | append |
|---------------------|--------|

When used with the [--tab](#page-195-1) and [--print-data](#page-189-2) options, this causes the data to be appended to any existing files having the same names.

#### <span id="page-177-2"></span>• [--backup-path](#page-177-2)=dir\_name

| Command-Line Format | backup-path=path |
|---------------------|------------------|
| Type                | Directory name   |
| Default Value       | ./               |

The path to the backup directory is required; this is supplied to [ndb\\_restore](#page-170-0) using the --backuppath option, and must include the subdirectory corresponding to the ID backup of the backup to be restored. For example, if the data node's DataDir is /var/lib/mysql-cluster, then the backup directory is /var/lib/mysql-cluster/BACKUP, and the backup files for the backup with the ID 3 can be found in /var/lib/mysql-cluster/BACKUP/BACKUP-3. The path may be absolute or relative to the directory in which the [ndb\\_restore](#page-170-0) executable is located, and may be optionally prefixed with backup-path=.

It is possible to restore a backup to a database with a different configuration than it was created from. For example, suppose that a backup with backup ID 12, created in a cluster with two storage nodes having the node IDs 2 and 3, is to be restored to a cluster with four nodes. Then [ndb\\_restore](#page-170-0) must be run twice—once for each storage node in the cluster where the backup was taken. However, [ndb\\_restore](#page-170-0) cannot always restore backups made from a cluster running one version of MySQL to a cluster running a different MySQL version. See Section 25.3.7, "Upgrading and Downgrading NDB Cluster", for more information.

![](_page_177_Picture_8.jpeg)

#### **Important**

It is not possible to restore a backup made from a newer version of NDB Cluster using an older version of [ndb\\_restore](#page-170-0). You can restore a backup made from a newer version of MySQL to an older cluster, but you must use a copy of [ndb\\_restore](#page-170-0) from the newer NDB Cluster version to do so.

For example, to restore a cluster backup taken from a cluster running NDB Cluster 8.0.44 to a cluster running NDB Cluster 7.6.36, you must use the [ndb\\_restore](#page-170-0) that comes with the NDB Cluster 7.6.36 distribution.

For more rapid restoration, the data may be restored in parallel, provided that there is a sufficient number of cluster connections available. That is, when restoring to multiple nodes in parallel, you must have an [api] or [mysqld] section in the cluster config.ini file available for each concurrent [ndb\\_restore](#page-170-0) process. However, the data files must always be applied before the logs.

#### <span id="page-177-1"></span>• [--backup-password=](#page-177-1)password

| Command-Line Format | backup-password=password |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

This option specifies a password to be used when decrypting an encrypted backup with the [-](#page-179-2) [decrypt](#page-179-2) option. This must be the same password that was used to encrypt the backup.

The password must be 1 to 256 characters in length, and must be enclosed by single or double quotation marks. It can contain any of the ASCII characters having character codes 32, 35, 38, 40-91, 93, 95, and 97-126; in other words, it can use any printable ASCII characters except for !, ', ", \$, %, \, and ^.

In MySQL 8.0.24 and later, it is possible to omit the password, in which case [ndb\\_restore](#page-170-0) waits for it to be supplied from stdin, as when using [--backup-password-from-stdin](#page-178-0).

<span id="page-178-0"></span>• [--backup-password-from-stdin\[=TRUE|FALSE\]](#page-178-0)

| Command-Line Format | backup-password-from-stdin |
|---------------------|----------------------------|
|---------------------|----------------------------|

When used in place of [--backup-password](#page-177-1), this option enables input of the backup password from the system shell (stdin), similar to how this is done when supplying the password interactively to mysql when using the --password without supplying the password on the command line.

<span id="page-178-1"></span>• [--backupid](#page-178-1)=#, -b

| Command-Line Format | backupid=# |
|---------------------|------------|
| Type                | Numeric    |
| Default Value       | none       |

This option is used to specify the ID or sequence number of the backup, and is the same number shown by the management client in the Backup backup\_id completed message displayed upon completion of a backup. (See Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup".)

![](_page_178_Picture_8.jpeg)

#### **Important**

When restoring cluster backups, you must be sure to restore all data nodes from backups having the same backup ID. Using files from different backups results at best in restoring the cluster to an inconsistent state, and is likely to fail altogether.

In NDB 8.0, this option is required.

<span id="page-178-2"></span>• [--character-sets-dir](#page-178-2)

Directory containing character sets.

<span id="page-178-3"></span>• [--connect](#page-178-3), -c

| Command-Line Format | connect=connection_string |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | localhost:1186            |

Alias for [--ndb-connectstring](#page-186-1).

<span id="page-178-4"></span>• [--connect-retries](#page-178-4)

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-178-5"></span>• [--connect-retry-delay](#page-178-5)

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|

#### ndb\_restore — Restore an NDB Cluster Backup

| Type          | Integer |
|---------------|---------|
| Default Value | 5       |
| Minimum Value | 0       |
| Maximum Value | 5       |

Number of seconds to wait between attempts to contact management server.

<span id="page-179-0"></span>• [--connect-string](#page-179-0)

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-186-1).

<span id="page-179-1"></span>• [--core-file](#page-179-1)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-179-2"></span>• [--decrypt](#page-179-2)

| Command-Line Format | decrypt |
|---------------------|---------|
|---------------------|---------|

Decrypt an encrypted backup using the password supplied by the [--backup-password](#page-177-1) option.

<span id="page-179-3"></span>• [--defaults-extra-file](#page-179-3)

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-179-4"></span>• [--defaults-file](#page-179-4)

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-179-5"></span>• [--defaults-group-suffix](#page-179-5)

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-180-0"></span>• [--disable-indexes](#page-180-0)

| Command-Line Format | disable-indexes |
|---------------------|-----------------|
|---------------------|-----------------|

Disable restoration of indexes during restoration of the data from a native NDB backup. Afterwards, you can restore indexes for all tables at once with multithreaded building of indexes using [-](#page-191-0) [rebuild-indexes](#page-191-0), which should be faster than rebuilding indexes concurrently for very large tables.

In NDB 8.0.27 and later, this option also drops any foreign keys specified in the backup.

Prior to NDB 8.0.29, attempting to access from MySQL an NDB table for which one or more indexes could not be found was always rejected with error [4243](https://dev.mysql.com/doc/ndbapi/en/ndb-error-codes-application-error.md#ndberrno-4243) Index not found. Beginning with NDB 8.0.29, it is possible for MySQL to open such a table, provided the query does not use any of the affected indexes; otherwise the query is rejected with [ER\\_NOT\\_KEYFILE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_keyfile). In the latter case, you can temporarily work around the problem by executing an ALTER TABLE statement such as this one:

```
ALTER TABLE tbl ALTER INDEX idx INVISIBLE;
```

This causes MySQL to ignore the index idx on table tbl. See Primary Keys and Indexes, for more information.

<span id="page-180-1"></span>• [--dont-ignore-systab-0](#page-180-1), -f

| Command-Line Format | dont-ignore-systab-0 |
|---------------------|----------------------|
|---------------------|----------------------|

Normally, when restoring table data and metadata, [ndb\\_restore](#page-170-0) ignores the copy of the NDB system table that is present in the backup. --dont-ignore-systab-0 causes the system table to be restored. This option is intended for experimental and development use only, and is not recommended in a production environment.

<span id="page-180-2"></span>• [--exclude-databases](#page-180-2)=db-list

| Command-Line Format | exclude-databases=list |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       |                        |

Comma-delimited list of one or more databases which should not be restored.

This option is often used in combination with [--exclude-tables](#page-181-2); see that option's description for further information and examples.

<span id="page-180-3"></span>• [--exclude-intermediate-sql-tables\[](#page-180-3)=TRUE|FALSE]

| Command-Line Format | exclude-intermediate-sql<br>tables[=TRUE FALSE] |
|---------------------|-------------------------------------------------|
| Type                | Boolean                                         |
| Default Value       | TRUE                                            |

When performing copying ALTER TABLE operations, mysqld creates intermediate tables (whose names are prefixed with #sql-). When TRUE, the --exclude-intermediate-sql-tables option keeps [ndb\\_restore](#page-170-0) from restoring such tables that may have been left over from these operations. This option is TRUE by default.

<span id="page-181-0"></span>• [--exclude-missing-columns](#page-181-0)

| Command-Line Format | exclude-missing-columns |
|---------------------|-------------------------|
|---------------------|-------------------------|

It is possible to restore only selected table columns using this option, which causes [ndb\\_restore](#page-170-0) to ignore any columns missing from tables being restored as compared to the versions of those tables found in the backup. This option applies to all tables being restored. If you wish to apply this option only to selected tables or databases, you can use it in combination with one or more of the - include-\* or --exclude-\* options described elsewhere in this section to do so, then restore data to the remaining tables using a complementary set of these options.

<span id="page-181-1"></span>• [--exclude-missing-tables](#page-181-1)

| Command-Line Format | exclude-missing-tables |
|---------------------|------------------------|
|---------------------|------------------------|

It is possible to restore only selected tables using this option, which causes [ndb\\_restore](#page-170-0) to ignore any tables from the backup that are not found in the target database.

<span id="page-181-2"></span>• [--exclude-tables](#page-181-2)=table-list

| Command-Line Format | exclude-tables=list |
|---------------------|---------------------|
| Type                | String              |
| Default Value       |                     |

List of one or more tables to exclude; each table reference must include the database name. Often used together with [--exclude-databases](#page-180-2).

When [--exclude-databases](#page-180-2) or --exclude-tables is used, only those databases or tables named by the option are excluded; all other databases and tables are restored by [ndb\\_restore](#page-170-0).

This table shows several invocations of [ndb\\_restore](#page-170-0) using --exclude-\* options (other options possibly required have been omitted for clarity), and the effects these options have on restoring from an NDB Cluster backup:

**Table 25.43 Several invocations of ndb\_restore using --exclude-\* options, and the effects these options have on restoring from an NDB Cluster backup.**

| Option                                                                             | Result                                                                                                                                            |
|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| exclude-databases=db1                                                              | All tables in all databases except db1 are<br>restored; no tables in db1 are restored                                                             |
| exclude-databases=db1,db2 (or<br>exclude-databases=db1exclude<br>databases=db2)    | All tables in all databases except db1 and<br>db2 are restored; no tables in db1 or db2 are<br>restored                                           |
| exclude-tables=db1.t1                                                              | All tables except t1 in database db1 are<br>restored; all other tables in db1 are restored; all<br>tables in all other databases are restored     |
| exclude-tables=db1.t2,db2.t1 (or<br>exclude-tables=db1.t2exclude<br>tables=db2.t1) | All tables in database db1 except for t2 and<br>all tables in database db2 except for table t1<br>are restored; no other tables in db1 or db2 are |

| Option | Result                                          |
|--------|-------------------------------------------------|
|        | restored; all tables in all other databases are |
|        | restored                                        |

You can use these two options together. For example, the following causes all tables in all databases except for databases db1 and db2, and tables t1 and t2 in database db3, to be restored:

```
$> ndb_restore [...] --exclude-databases=db1,db2 --exclude-tables=db3.t1,db3.t2
```

(Again, we have omitted other possibly necessary options in the interest of clarity and brevity from the example just shown.)

You can use --include-\* and --exclude-\* options together, subject to the following rules:

- The actions of all --include-\* and --exclude-\* options are cumulative.
- All --include-\* and --exclude-\* options are evaluated in the order passed to ndb\_restore, from right to left.
- In the event of conflicting options, the first (rightmost) option takes precedence. In other words, the first option (going from right to left) that matches against a given database or table "wins".

For example, the following set of options causes [ndb\\_restore](#page-170-0) to restore all tables from database db1 except db1.t1, while restoring no other tables from any other databases:

```
--include-databases=db1 --exclude-tables=db1.t1
```

However, reversing the order of the options just given simply causes all tables from database db1 to be restored (including db1.t1, but no tables from any other database), because the [--include](#page-183-3)[databases](#page-183-3) option, being farthest to the right, is the first match against database db1 and thus takes precedence over any other option that matches db1 or any tables in db1:

```
--exclude-tables=db1.t1 --include-databases=db1
```

<span id="page-182-0"></span>• [--fields-enclosed-by](#page-182-0)=char

| Command-Line Format | fields-enclosed-by=char |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       |                         |

Each column value is enclosed by the string passed to this option (regardless of data type; see the description of [--fields-optionally-enclosed-by](#page-182-1)).

<span id="page-182-1"></span>• [--fields-optionally-enclosed-by](#page-182-1)

| Command-Line Format | fields-optionally-enclosed-by |
|---------------------|-------------------------------|
| Type                | String                        |
| Default Value       |                               |

The string passed to this option is used to enclose column values containing character data (such as CHAR, VARCHAR, BINARY, TEXT, or ENUM).

<span id="page-182-2"></span>• [--fields-terminated-by](#page-182-2)=char

| Command-Line Format | fields-terminated-by=char |
|---------------------|---------------------------|
| Type                | String                    |

| Default Value | \t (tab) |  |
|---------------|----------|--|
|               |          |  |

The string passed to this option is used to separate column values. The default value is a tab character (\t).

<span id="page-183-0"></span>• [--help](#page-183-0)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-183-1"></span>• [--hex](#page-183-1)

| Command-Line Format | hex |
|---------------------|-----|
|---------------------|-----|

If this option is used, all binary values are output in hexadecimal format.

<span id="page-183-2"></span>• [--ignore-extended-pk-updates](#page-183-2)

| Command-Line Format | ignore-extended-pk-updates[=0 1] |
|---------------------|----------------------------------|
| Type                | Integer                          |
| Default Value       | 0                                |
| Minimum Value       | 0                                |
| Maximum Value       | 1                                |

When using [--allow-pk-changes](#page-175-0), columns which become part of a table's primary key must not be updated while the backup is being taken; such columns should keep the same values from the time values are inserted into them until the rows containing the values are deleted. If [ndb\\_restore](#page-170-0) encounters updates to these columns when restoring a backup, the restore fails. Because some applications may set values for all columns when updating a row, even when some column values are not changed, the backup may include log events appearing to update columns which are not in fact modified. In such cases you can set --ignore-extended-pk-updates to 1, forcing [ndb\\_restore](#page-170-0) to ignore such updates.

![](_page_183_Picture_12.jpeg)

#### **Important**

When causing these updates to be ignored, the user is responsible for ensuring that there are no updates to the values of any columns that become part of the primary key.

For more information, see the description of [--allow-pk-changes](#page-175-0).

<span id="page-183-3"></span>• [--include-databases](#page-183-3)=db-list

| Command-Line Format | include-databases=list |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       |                        |

Comma-delimited list of one or more databases to restore. Often used together with [--include](#page-184-1)[tables](#page-184-1); see the description of that option for further information and examples.

<span id="page-184-0"></span>• [--include-stored-grants](#page-184-0)

| Command-Line Format | include-stored-grants |
|---------------------|-----------------------|
|---------------------|-----------------------|

In NDB 8.0, [ndb\\_restore](#page-170-0) does not by default restore shared users and grants (see Section 25.6.13, "Privilege Synchronization and NDB\_STORED\_USER") to the ndb\_sql\_metadata table. Specifying this option causes it to do so.

<span id="page-184-1"></span>• [--include-tables](#page-184-1)=table-list

| Command-Line Format | include-tables=list |
|---------------------|---------------------|
| Type                | String              |
| Default Value       |                     |

Comma-delimited list of tables to restore; each table reference must include the database name.

When --include-databases or [--include-tables](#page-184-1) is used, only those databases or tables named by the option are restored; all other databases and tables are excluded by [ndb\\_restore](#page-170-0), and are not restored.

The following table shows several invocations of [ndb\\_restore](#page-170-0) using --include-\* options (other options possibly required have been omitted for clarity), and the effects these have on restoring from an NDB Cluster backup:

**Table 25.44 Several invocations of ndb\_restore using --include-\* options, and their effects on restoring from an NDB Cluster backup.**

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

<span id="page-185-0"></span>• [--lines-terminated-by](#page-185-0)=char

| Command-Line Format | lines-terminated-by=char |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | \n (linebreak)           |

Specifies the string used to end each line of output. The default is a linefeed character (\n).

<span id="page-185-1"></span>• [--login-path](#page-185-1)

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-185-2"></span>• [--lossy-conversions](#page-185-2), -L

| Command-Line Format | lossy-conversions |
|---------------------|-------------------|
|---------------------|-------------------|

This option is intended to complement the [--promote-attributes](#page-190-2) option. Using --lossyconversions allows lossy conversions of column values (type demotions or changes in sign) when restoring data from backup. With some exceptions, the rules governing demotion are the same as for MySQL replication; see Replication of Columns Having Different Data Types, for information about specific type conversions currently supported by attribute demotion.

Beginning with NDB 8.0.26, this option also makes it possible to restore a NULL column as NOT NULL. The column must not contain any NULL entries; otherwise [ndb\\_restore](#page-170-0) stops with an error.

[ndb\\_restore](#page-170-0) reports any truncation of data that it performs during lossy conversions once per attribute and column.

<span id="page-185-3"></span>• [--no-binlog](#page-185-3)

| Command-Line Format | no-binlog |
|---------------------|-----------|
|---------------------|-----------|

This option prevents any connected SQL nodes from writing data restored by [ndb\\_restore](#page-170-0) to their binary logs.

<span id="page-185-4"></span>• [--no-restore-disk-objects](#page-185-4), -d

| Command-Line Format | no-restore-disk-objects |
|---------------------|-------------------------|
|---------------------|-------------------------|

This option stops [ndb\\_restore](#page-170-0) from restoring any NDB Cluster Disk Data objects, such as tablespaces and log file groups; see Section 25.6.11, "NDB Cluster Disk Data Tables", for more information about these.

<span id="page-185-5"></span>• [--no-upgrade](#page-185-5), -u

| Command-Line Format | no-upgrade |
|---------------------|------------|
|---------------------|------------|

When using [ndb\\_restore](#page-170-0) to restore a backup, VARCHAR columns created using the old fixed format are resized and recreated using the variable-width format now employed. This behavior can be overridden by specifying --no-upgrade. 4556

#### <span id="page-186-1"></span>• [--ndb-connectstring](#page-186-1)

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                |                                 |
|                     | String                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

#### <span id="page-186-2"></span>• [--ndb-mgmd-host](#page-186-2)

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-186-1).

<span id="page-186-3"></span>• [--ndb-nodegroup-map](#page-186-3)=map, -z

| Command-Line Format | ndb-nodegroup-map=map |
|---------------------|-----------------------|
|---------------------|-----------------------|

Intended for restoring a backup taken from one node group to a different node group, but never completely implemented; unsupported.

All code supporting this option was removed in NDB 8.0.27; in this and later versions, any value set for it is ignored, and the option itself does nothing.

### <span id="page-186-4"></span>• [--ndb-nodeid](#page-186-4)

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-186-1).

<span id="page-186-5"></span>• [--ndb-optimized-node-selection](#page-186-5)

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

#### <span id="page-186-0"></span>• [--no-defaults](#page-186-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

#### <span id="page-186-6"></span>• [--nodeid](#page-186-6)=#, -n

| Command-Line Format | nodeid=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | none     |

Specify the node ID of the data node on which the backup was taken.

When restoring to a cluster with different number of data nodes from that where the backup was taken, this information helps identify the correct set or sets of files to be restored to a given node. (In such cases, multiple files usually need to be restored to a single data node.) See [Section 25.5.23.2,](#page-198-0) ["Restoring to a different number of data nodes",](#page-198-0) for additional information and examples.

In NDB 8.0, this option is required.

<span id="page-187-0"></span>• [--num-slices](#page-187-0)=#

| Command-Line Format | num-slices=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 1            |
| Minimum Value       | 1            |
| Maximum Value       | 1024         |

When restoring a backup by slices, this option sets the number of slices into which to divide the backup. This allows multiple instances of [ndb\\_restore](#page-170-0) to restore disjoint subsets in parallel, potentially reducing the amount of time required to perform the restore operation.

A slice is a subset of the data in a given backup; that is, it is a set of fragments having the same slice ID, specified using the [--slice-id](#page-195-0) option. The two options must always be used together, and the value set by --slice-id must always be less than the number of slices.

[ndb\\_restore](#page-170-0) encounters fragments and assigns each one a fragment counter. When restoring by slices, a slice ID is assigned to each fragment; this slice ID is in the range 0 to 1 less than the number of slices. For a table that is not a BLOB table, the slice to which a given fragment belongs is determined using the formula shown here:

```
[slice_ID] = [fragment_counter] % [number_of_slices]
```

For a BLOB table, a fragment counter is not used; the fragment number is used instead, along with the ID of the main table for the BLOB table (recall that NDB stores BLOB values in a separate table internally). In this case, the slice ID for a given fragment is calculated as shown here:

```
[slice_ID] =
([main_table_ID] + [fragment_ID]) % [number_of_slices]
```

Thus, restoring by N slices means running N instances of [ndb\\_restore](#page-170-0), all with --num-slices=N (along with any other necessary options) and one each with [--slice-id=1](#page-195-0), --slice-id=2, - slice-id=3, and so on through slice-id=N-1.

**Example.** Assume that you want to restore a backup named BACKUP-1, found in the default directory /var/lib/mysql-cluster/BACKUP/BACKUP-3 on the node file system on each data node, to a cluster with four data nodes having the node IDs 1, 2, 3, and 4. To perform this operation using five slices, execute the sets of commands shown in the following list:

1. Restore the cluster metadata using [ndb\\_restore](#page-170-0) as shown here:

```
$> ndb_restore -b 1 -n 1 -m --disable-indexes --backup-path=/home/ndbuser/backups
```

2. Restore the cluster data to the data nodes invoking [ndb\\_restore](#page-170-0) as shown here:

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
```

```
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 3 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=0 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=1 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=2 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=3 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
$> ndb_restore -b 1 -n 4 -r --num-slices=5 --slice-id=4 --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

All of the commands just shown in this step can be executed in parallel, provided there are enough slots for connections to the cluster (see the description for the [--backup-path](#page-177-2) option).

3. Restore indexes as usual, as shown here:

```
$> ndb_restore -b 1 -n 1 --rebuild-indexes --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

4. Finally, restore the epoch, using the command shown here:

```
$> ndb_restore -b 1 -n 1 --restore-epoch --backup-path=/var/lib/mysql-cluster/BACKUP/BACKUP-1
```

You should use slicing to restore the cluster data only; it is not necessary to employ [--num-slices](#page-187-0) or [--slice-id](#page-195-0) when restoring the metadata, indexes, or epoch information. If either or both of these options are used with the [ndb\\_restore](#page-170-0) options controlling restoration of these, the program ignores them.

The effects of using the [--parallelism](#page-188-0) option on the speed of restoration are independent of those produced by slicing or parallel restoration using multiple instances of [ndb\\_restore](#page-170-0) (- parallelism specifies the number of parallel transactions executed by a single [ndb\\_restore](#page-170-0) thread), but it can be used together with either or both of these. You should be aware that increasing --parallelism causes [ndb\\_restore](#page-170-0) to impose a greater load on the cluster; if the system can handle this, restoration should complete even more quickly.

The value of --num-slices is not directly dependent on values relating to hardware such as number of CPUs or CPU cores, amount of RAM, and so forth, nor does it depend on the number of LDMs.

It is possible to employ different values for this option on different data nodes as part of the same restoration; doing so should not in and of itself produce any ill effects.

<span id="page-188-0"></span>• [--parallelism](#page-188-0)=#, -p

| Command-Line Format | parallelism=# |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 128           |
| Minimum Value       | 1             |
| Maximum Value       | 1024          |

[ndb\\_restore](#page-170-0) uses single-row transactions to apply many rows concurrently. This parameter determines the number of parallel transactions (concurrent rows) that an instance of [ndb\\_restore](#page-170-0) tries to use. By default, this is 128; the minimum is 1, and the maximum is 1024.

The work of performing the inserts is parallelized across the threads in the data nodes involved. This mechanism is employed for restoring bulk data from the .Data file—that is, the fuzzy snapshot of the data; it is not used for building or rebuilding indexes. The change log is applied serially; index drops and builds are DDL operations and handled separately. There is no thread-level parallelism on the client side of the restore.

<span id="page-189-0"></span>• [--preserve-trailing-spaces](#page-189-0), -P

| Command-Line Format | preserve-trailing-spaces |
|---------------------|--------------------------|
|---------------------|--------------------------|

Cause trailing spaces to be preserved when promoting a fixed-width character data type to its variable-width equivalent—that is, when promoting a CHAR column value to VARCHAR, or a BINARY column value to VARBINARY. Otherwise, any trailing spaces are dropped from such column values when they are inserted into the new columns.

![](_page_189_Picture_4.jpeg)

#### **Note**

Although you can promote CHAR columns to VARCHAR and BINARY columns to VARBINARY, you cannot promote VARCHAR columns to CHAR or VARBINARY columns to BINARY.

<span id="page-189-1"></span>• [--print](#page-189-1)

| Command-Line Format | print |
|---------------------|-------|
|---------------------|-------|

Causes [ndb\\_restore](#page-170-0) to print all data, metadata, and logs to stdout. Equivalent to using the [-](#page-189-2) [print-data](#page-189-2), [--print-meta](#page-189-5), and [--print-log](#page-189-4) options together.

![](_page_189_Picture_10.jpeg)

#### **Note**

Use of --print or any of the --print\_\* options is in effect performing a dry run. Including one or more of these options causes any output to be redirected to stdout; in such cases, [ndb\\_restore](#page-170-0) makes no attempt to restore data or metadata to an NDB Cluster.

<span id="page-189-2"></span>• [--print-data](#page-189-2)

| Command-Line Format | print-data |
|---------------------|------------|
|---------------------|------------|

Cause [ndb\\_restore](#page-170-0) to direct its output to stdout. Often used together with one or more of [--tab](#page-195-1), [--fields-enclosed-by](#page-182-0), [--fields-optionally-enclosed-by](#page-182-1), [--fields-terminated](#page-182-2)[by](#page-182-2), [--hex](#page-183-1), and [--append](#page-177-0).

TEXT and BLOB column values are always truncated. Such values are truncated to the first 256 bytes in the output. This cannot currently be overridden when using --print-data.

<span id="page-189-3"></span>• [--print-defaults](#page-189-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-189-4"></span>• [--print-log](#page-189-4)

| Command-Line Format | print-log |
|---------------------|-----------|

Cause [ndb\\_restore](#page-170-0) to output its log to stdout.

<span id="page-189-5"></span>• [--print-meta](#page-189-5)

| Command-Line Format | print-meta |
|---------------------|------------|
|                     |            |

<span id="page-190-0"></span>• print-sql-log

| Command-Line Format | print-sql-log |
|---------------------|---------------|
|---------------------|---------------|

Log SQL statements to stdout. Use the option to enable; normally this behavior is disabled. The option checks before attempting to log whether all the tables being restored have explicitly defined primary keys; queries on a table having only the hidden primary key implemented by NDB cannot be converted to valid SQL.

This option does not work with tables having BLOB columns.

<span id="page-190-1"></span>• --progress-frequency=N

| Command-Line Format | progress-frequency=# |
|---------------------|----------------------|
| Туре                | Numeric              |
| Default Value       | 0                    |
| Minimum Value       | 0                    |
| Maximum Value       | 65535                |

Print a status report each N seconds while the backup is in progress. 0 (the default) causes no status reports to be printed. The maximum is 65535.

<span id="page-190-2"></span>• --promote-attributes, -A

| Command-Line Format | promote-attributes |
|---------------------|--------------------|
|---------------------|--------------------|

ndb\_restore supports limited attribute promotion in much the same way that it is supported by MySQL replication; that is, data backed up from a column of a given type can generally be restored to a column using a "larger, similar" type. For example, data from a CHAR (20) column can be restored to a column declared as VARCHAR (20), VARCHAR (30), or CHAR (30); data from a MEDIUMINT column can be restored to a column of type INT or BIGINT. See Replication of Columns Having Different Data Types, for a table of type conversions currently supported by attribute promotion.

Beginning with NDB 8.0.26, this option also makes it possible to restore a  ${\tt NOT}$   ${\tt NULL}$  column as  ${\tt NULL}$ .

Attribute promotion by ndb restore must be enabled explicitly, as follows:

- 1. Prepare the table to which the backup is to be restored. ndb\_restore cannot be used to recreate the table with a different definition from the original; this means that you must either create the table manually, or alter the columns which you wish to promote using ALTER TABLE after restoring the table metadata but before restoring the data.
- 2. Invoke ndb\_restore with the --promote-attributes option (short form -A) when restoring the table data. Attribute promotion does not occur if this option is not used; instead, the restore operation fails with an error.

When converting between character data types and TEXT or BLOB, only conversions between character types (CHAR and VARCHAR) and binary types (BINARY and VARBINARY) can be performed at the same time. For example, you cannot promote an INT column to BIGINT while promoting a VARCHAR column to TEXT in the same invocation of ndb restore.

Converting between TEXT columns using different character sets is not supported, and is expressly disallowed.

When performing conversions of character or binary types to TEXT or BLOB with ndb\_restore, may notice that it creates and uses one or more staging tables named table name\$STnode id.

These tables are not needed afterwards, and are normally deleted by [ndb\\_restore](#page-170-0) following a successful restoration.

<span id="page-191-0"></span>• [--rebuild-indexes](#page-191-0)

| Command-Line Format | rebuild-indexes |
|---------------------|-----------------|
|---------------------|-----------------|

Enable multithreaded rebuilding of the ordered indexes while restoring a native NDB backup. The number of threads used for building ordered indexes by [ndb\\_restore](#page-170-0) with this option is controlled by the BuildIndexThreads data node configuration parameter and the number of LDMs.

It is necessary to use this option only for the first run of [ndb\\_restore](#page-170-0); this causes all ordered indexes to be rebuilt without using --rebuild-indexes again when restoring subsequent nodes. You should use this option prior to inserting new rows into the database; otherwise, it is possible for a row to be inserted that later causes a unique constraint violation when trying to rebuild the indexes.

Building of ordered indices is parallelized with the number of LDMs by default. Offline index builds performed during node and system restarts can be made faster using the BuildIndexThreads data node configuration parameter; this parameter has no effect on dropping and rebuilding of indexes by [ndb\\_restore](#page-170-0), which is performed online.

Rebuilding of unique indexes uses disk write bandwidth for redo logging and local checkpointing. An insufficient amount of this bandwidth can lead to redo buffer overload or log overload errors. In such cases you can run [ndb\\_restore](#page-170-0) --rebuild-indexes again; the process resumes at the point where the error occurred. You can also do this when you have encountered temporary errors. You can repeat execution of [ndb\\_restore](#page-170-0) --rebuild-indexes indefinitely; you may be able to stop such errors by reducing the value of [--parallelism](#page-188-0). If the problem is insufficient space, you can increase the size of the redo log (FragmentLogFileSize node configuration parameter), or you can increase the speed at which LCPs are performed (MaxDiskWriteSpeed and related parameters), in order to free space more quickly.

<span id="page-191-1"></span>• [--remap-column=](#page-191-1)db.tbl.col:fn:args

| Command-Line Format | remap-column=string |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | [none]              |

When used together with [--restore-data](#page-192-0), this option applies a function to the value of the indicated column. Values in the argument string are listed here:

- db: Database name, following any renames performed by [--rewrite-database](#page-193-1).
- tbl: Table name.
- col: Name of the column to be updated. This column must be of type INT or BIGINT. The column can also be but is not required to be UNSIGNED.
- fn: Function name; currently, the only supported name is offset.
- args: Arguments supplied to the function. Currently, only a single argument, the size of the offset to be added by the offset function, is supported. Negative values are supported. The size of the argument cannot exceed that of the signed variant of the column's type; for example, if col is an INT column, then the allowed range of the argument passed to the offset function is -2147483648 to 2147483647 (see Section 13.1.2, "Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT").

If applying the offset value to the column would cause an overflow or underflow, the restore operation fails. This could happen, for example, if the column is a BIGINT, and the option

attempts to apply an offset value of 8 on a row in which the column value is 4294967291, since 4294967291 + 8 = 4294967299 > 4294967295.

This option can be useful when you wish to merge data stored in multiple source instances of NDB Cluster (all using the same schema) into a single destination NDB Cluster, using NDB native backup (see Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup") and [ndb\\_restore](#page-170-0) to merge the data, where primary and unique key values are overlapping between source clusters, and it is necessary as part of the process to remap these values to ranges that do not overlap. It may also be necessary to preserve other relationships between tables. To fulfill such requirements, it is possible to use the option multiple times in the same invocation of [ndb\\_restore](#page-170-0) to remap columns of different tables, as shown here:

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

When source backups contain duplicate tables which should not be merged, you can handle this by using [--exclude-tables](#page-181-2), [--exclude-databases](#page-180-2), or by some other means in your application.

Information about the structure and other characteristics of tables to be merged can obtained using SHOW CREATE TABLE; the [ndb\\_desc](#page-109-2) tool; and MAX(), MIN(), LAST\_INSERT\_ID(), and other MySQL functions.

Replication of changes from merged to unmerged tables, or from unmerged to merged tables, in separate instances of NDB Cluster is not supported.

<span id="page-192-0"></span>• [--restore-data](#page-192-0), -r

| Command-Line Format | restore-data |
|---------------------|--------------|
|---------------------|--------------|

Output NDB table data and logs.

<span id="page-192-1"></span>• [--restore-epoch](#page-192-1), -e

| Command-Line Format | restore-epoch |
|---------------------|---------------|
|                     |               |

Add (or restore) epoch information to the cluster replication status table. This is useful for starting replication on an NDB Cluster replica. When this option is used, the row in the mysql.ndb\_apply\_status having 0 in the id column is updated if it already exists; such a row is inserted if it does not already exist. (See Section 25.7.9, "NDB Cluster Backups With NDB Cluster Replication".)

<span id="page-192-2"></span>• [--restore-meta](#page-192-2), -m

| Command-Line Format | restore-meta |
|---------------------|--------------|
|---------------------|--------------|

This option causes [ndb\\_restore](#page-170-0) to print NDB table metadata.

The first time you run the [ndb\\_restore](#page-170-0) restoration program, you also need to restore the metadata. In other words, you must re-create the database tables—this can be done by running it with the --

restore-meta (-m) option. Restoring the metadata need be done only on a single data node; this is sufficient to restore it to the entire cluster.

In older versions of NDB Cluster, tables whose schemas were restored using this option used the same number of partitions as they did on the original cluster, even if it had a differing number of data nodes from the new cluster. In NDB 8.0, when restoring metadata, this is no longer an issue; [ndb\\_restore](#page-170-0) now uses the default number of partitions for the target cluster, unless the number of local data manager threads is also changed from what it was for data nodes in the original cluster.

When using this option in NDB 8.0, it is recommended that auto synchronization be disabled by setting ndb\_metadata\_check=OFF until [ndb\\_restore](#page-170-0) has completed restoring the metadata, after which it can it turned on again to synchronize objects newly created in the NDB dictionary.

![](_page_193_Picture_4.jpeg)

#### **Note**

The cluster should have an empty database when starting to restore a backup. (In other words, you should start the data nodes with [--initial](#page-59-0) prior to performing the restore.)

<span id="page-193-0"></span>• [--restore-privilege-tables](#page-193-0)

| Command-Line Format | restore-privilege-tables |
|---------------------|--------------------------|
| Deprecated          | Yes                      |

[ndb\\_restore](#page-170-0) does not by default restore distributed MySQL privilege tables created in releases of NDB Cluster prior to version 8.0, which does not support distributed privileges as implemented in NDB 7.6 and earlier. This option causes [ndb\\_restore](#page-170-0) to restore them.

In NDB 8.0, such tables are not used for access control; as part of the MySQL server's upgrade process, the server creates InnoDB copies of these tables local to itself. For more information, see Section 25.3.7, "Upgrading and Downgrading NDB Cluster", as well as Section 8.2.3, "Grant Tables".

<span id="page-193-1"></span>• [--rewrite-database](#page-193-1)=olddb,newdb

| Command-Line Format | rewrite-database=string |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | none                    |

This option makes it possible to restore to a database having a different name from that used in the backup. For example, if a backup is made of a database named products, you can restore the data it contains to a database named inventory, use this option as shown here (omitting any other options that might be required):

\$> ndb\_restore --rewrite-database=product,inventory

The option can be employed multiple times in a single invocation of [ndb\\_restore](#page-170-0). Thus it is possible to restore simultaneously from a database named db1 to a database named db2 and from a database named db3 to one named db4 using --rewrite-database=db1,db2 --rewritedatabase=db3,db4. Other [ndb\\_restore](#page-170-0) options may be used between multiple occurrences of --rewrite-database.

In the event of conflicts between multiple --rewrite-database options, the last --rewritedatabase option used, reading from left to right, is the one that takes effect. For example, if --rewrite-database=db1,db2 --rewrite-database=db1,db3 is used, only - rewrite-database=db1,db3 is honored, and --rewrite-database=db1,db2 is ignored. It is also possible to restore from multiple databases to a single database, so that --rewritedatabase=db1,db3 --rewrite-database=db2,db3 restores all tables and data from databases db1 and db2 into database db3.

![](_page_194_Picture_2.jpeg)

#### **Important**

When restoring from multiple backup databases into a single target database using --rewrite-database, no check is made for collisions between table or other object names, and the order in which rows are restored is not guaranteed. This means that it is possible in such cases for rows to be overwritten and updates to be lost.

<span id="page-194-0"></span>• [--skip-broken-objects](#page-194-0)

| Command-Line Format | skip-broken-objects |
|---------------------|---------------------|
|---------------------|---------------------|

This option causes [ndb\\_restore](#page-170-0) to ignore corrupt tables while reading a native NDB backup, and to continue restoring any remaining tables (that are not also corrupted). Currently, the --skipbroken-objects option works only in the case of missing blob parts tables.

<span id="page-194-1"></span>• [--skip-fk-checks](#page-194-1)

| Command-Line Format | skip-fk-checks    |
|---------------------|-------------------|
| Introduced          | 8.0.45-ndb-8.0.45 |

This option modifies the behavior of [ndb\\_restore](#page-170-0) [--rebuild-indexes](#page-191-0) so that, when foreign keys are re-enabled, the existing data in the table is not checked for consistency.

<span id="page-194-2"></span>• [--skip-table-check](#page-194-2), -s

| Command-Line Format | skip-table-check |
|---------------------|------------------|
|---------------------|------------------|

It is possible to restore data without restoring table metadata. By default when doing this, [ndb\\_restore](#page-170-0) fails with an error if a mismatch is found between the table data and the table schema; this option overrides that behavior.

Some of the restrictions on mismatches in column definitions when restoring data using [ndb\\_restore](#page-170-0) are relaxed; when one of these types of mismatches is encountered, [ndb\\_restore](#page-170-0) does not stop with an error as it did previously, but rather accepts the data and inserts it into the target table while issuing a warning to the user that this is being done. This behavior occurs whether or not either of the options --skip-table-check or [--promote-attributes](#page-190-2) is in use. These differences in column definitions are of the following types:

- Different COLUMN\_FORMAT settings (FIXED, DYNAMIC, DEFAULT)
- Different STORAGE settings (MEMORY, DISK)
- Different default values
- Different distribution key settings
- <span id="page-194-3"></span>• [--skip-unknown-objects](#page-194-3)

| Command-Line Format<br>skip-unknown-objects |
|---------------------------------------------|
|---------------------------------------------|

This option causes [ndb\\_restore](#page-170-0) to ignore any schema objects it does not recognize while reading a native NDB backup. This can be used for restoring a backup made from a cluster running (for example) NDB 7.6 to a cluster running NDB Cluster 7.5.

### <span id="page-195-0"></span>• [--slice-id](#page-195-0)=#

| Command-Line Format | slice-id=# |
|---------------------|------------|
| Type                | Integer    |
| Default Value       | 0          |
| Minimum Value       | 0          |
| Maximum Value       | 1023       |

When restoring by slices, this is the ID of the slice to restore. This option is always used together with [--num-slices](#page-187-0), and its value must be always less than that of --num-slices.

For more information, see the description of the [--num-slices](#page-187-0) elsewhere in this section.

<span id="page-195-1"></span>• [--tab](#page-195-1)=dir\_name, -T dir\_name

| Command-Line Format | tab=path       |
|---------------------|----------------|
| Type                | Directory name |

Causes [--print-data](#page-189-2) to create dump files, one per table, each named tbl\_name.txt. It requires as its argument the path to the directory where the files should be saved; use . for the current directory.

#### <span id="page-195-2"></span>• --timestamp-printouts

| Command-Line Format | timestamp-printouts{=true false} |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | true                             |

Causes info, error, and debug log messages to be prefixed with timestamps.

This option is enabled by default in NDB 8.0. Disable it with --timestamp-printouts=false.

#### <span id="page-195-3"></span>• [--usage](#page-195-3)

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-183-0).

#### <span id="page-195-4"></span>• [--verbose](#page-195-4)=#

| Command-Line Format | verbose=# |
|---------------------|-----------|
| Type                | Numeric   |
| Default Value       | 1         |
| Minimum Value       | 0         |
| Maximum Value       | 255       |

Sets the level for the verbosity of the output. The minimum is 0; the maximum is 255. The default value is 1.

#### <span id="page-195-5"></span>• [--version](#page-195-5)

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-195-6"></span>• [--with-apply-status](#page-195-6)

| Command-Line Format | with-apply-status |
|---------------------|-------------------|
|---------------------|-------------------|

Restore all rows from the backup's ndb\_apply\_status table (except for the row having server\_id = 0, which is generated using [--restore-epoch](#page-192-1)). This option requires that [-](#page-192-0) [restore-data](#page-192-0) also be used.

If the ndb\_apply\_status table from the backup already contains a row with server\_id = 0, [ndb\\_restore](#page-170-0) --with-apply-status deletes it. For this reason, we recommend that you use [ndb\\_restore](#page-170-0) --restore-epoch after invoking [ndb\\_restore](#page-170-0) with the --with-applystatus option. You can also use --restore-epoch concurrently with the last of any invocations of [ndb\\_restore](#page-170-0) --with-apply-status used to restore the cluster.

For more information, see ndb\_apply\_status Table.

Typical options for this utility are shown here:

```
ndb_restore [-c connection_string] -n node_id -b backup_id \
 [-m] -r --backup-path=/path/to/backup/files
```

Normally, when restoring from an NDB Cluster backup, [ndb\\_restore](#page-170-0) requires at a minimum the [-](#page-186-6) [nodeid](#page-186-6) (short form: -n), [--backupid](#page-178-1) (short form: -b), and [--backup-path](#page-177-2) options.

The -c option is used to specify a connection string which tells ndb\_restore where to locate the cluster management server (see Section 25.4.3.3, "NDB Cluster Connection Strings"). If this option is not used, then [ndb\\_restore](#page-170-0) attempts to connect to a management server on localhost:1186. This utility acts as a cluster API node, and so requires a free connection "slot" to connect to the cluster management server. This means that there must be at least one [api] or [mysqld] section that can be used by it in the cluster config.ini file. It is a good idea to keep at least one empty [api] or [mysqld] section in config.ini that is not being used for a MySQL server or other application for this reason (see Section 25.4.3.7, "Defining SQL and Other API Nodes in an NDB Cluster").

In NDB 8.0.22 and later, [ndb\\_restore](#page-170-0) can decrypt an encrypted backup using [--decrypt](#page-179-2) and [-](#page-177-1) [backup-password](#page-177-1). Both options must be specified to perform decryption. See the documentation for the START BACKUP management client command for information on creating encrypted backups.

You can verify that [ndb\\_restore](#page-170-0) is connected to the cluster by using the SHOW command in the [ndb\\_mgm](#page-81-0) management client. You can also accomplish this from a system shell, as shown here:

```
$> ndb_mgm -e "SHOW"
```

#### **Error reporting.**

[ndb\\_restore](#page-170-0) reports both temporary and permanent errors. In the case of temporary errors, it may able to recover from them, and reports Restore successful, but encountered temporary error, please look at configuration in such cases.

![](_page_196_Picture_14.jpeg)

#### **Important**

After using [ndb\\_restore](#page-170-0) to initialize an NDB Cluster for use in circular replication, binary logs on the SQL node acting as the replica are not automatically created, and you must cause them to be created manually. To cause the binary logs to be created, issue a SHOW TABLES statement on that SQL node before running START SLAVE. This is a known issue in NDB Cluster.