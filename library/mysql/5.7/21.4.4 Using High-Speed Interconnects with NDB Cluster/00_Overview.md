---
source: MySQL 5.7 Reference
title: 00_Overview
---

Even before design of NDBCLUSTER began in 1996, it was evident that one of the major problems to be encountered in building parallel databases would be communication between the nodes in the network. For this reason, NDBCLUSTER was designed from the very beginning to permit the use of a number of different data transport mechanisms, or transporters.

NDB Cluster 7.5 and 7.6 support three of these (see Section 21.2.1, "NDB Cluster Core Concepts"). A fourth transporter, Scalable Coherent Interface (SCI), was also supported in very old versions of NDB. This required specialized hardware, software, and MySQL binaries that are no longer available.

# <span id="page-171-1"></span>**21.5 NDB Cluster Programs**

Using and managing an NDB Cluster requires several specialized programs, which we describe in this chapter. We discuss the purposes of these programs in an NDB Cluster, how to use the programs, and what startup options are available for each of them.

These programs include the NDB Cluster data, management, and SQL node processes ([ndbd](#page-171-0), [ndbmtd](#page-187-0), [ndb\\_mgmd](#page-188-0), and mysqld) and the management client ([ndb\\_mgm](#page-199-0)).

For information about using mysqld as an NDB Cluster process, see Section 21.6.10, "MySQL Server Usage for NDB Cluster".

Other NDB utility, diagnostic, and example programs are included with the NDB Cluster distribution. These include ndb\_restore, ndb\_show\_tables, and ndb\_config. These programs are also covered in this section.

The final portion of this section contains tables of options that are common to all the various NDB Cluster programs.

# <span id="page-171-0"></span>**21.5.1 ndbd — The NDB Cluster Data Node Daemon**

The [ndbd](#page-171-0) binary provides the single-threaded version of the process that is used to handle all the data in tables employing the NDBCLUSTER storage engine. This data node process enables a data node to accomplish distributed transaction handling, node recovery, checkpointing to disk, online backup, and related tasks. In NDB 7.6.31 and later, when started, [ndbd](#page-171-0) logs a warning similar to that shown here:

```
2024-05-28 13:32:16 [ndbd] WARNING -- Running ndbd with a single thread of
signal execution. For multi-threaded signal execution run the ndbmtd binary.
```

[ndbmtd](#page-187-0) is the multi-threaded version of this binary.

In an NDB Cluster, a set of [ndbd](#page-171-0) processes cooperate in handling data. These processes can execute on the same computer (host) or on different computers. The correspondences between data nodes and Cluster hosts is completely configurable.

Options that can be used with [ndbd](#page-171-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.22 Command-line options used with the program ndbd**

| Format                               | Description                                                                                                                                                  | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| bind-address=name                    | Local bind address                                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| character-sets<br>dir=path           | Directory containing character<br>sets                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-delay=#                      | Obsolete synonym forconnect<br>retry-delay, which should be<br>used instead of this option                                                                   | REMOVED: NDB 7.5.25, NDB<br>7.6.21                    |
| connect-retries=#                    | Set the number of times to retry<br>a connection before giving up;<br>0 means 1 attempt only (and<br>no retries); -1 means continue<br>retrying indefinitely | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Time to wait between attempts<br>to contact a management server,<br>in seconds; 0 means do not wait<br>between attempts                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                                                                                                              |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| daemon,                              | Start ndbd as daemon (default);<br>override withnodaemon                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d                                   |                                                                                                                                                              |                                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                   | Read default options from given<br>file only                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| foreground                           | Run ndbd in foreground,<br>provided for debugging purposes<br>(impliesnodaemon)                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                | Display help text and exit                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                   |                                                                                                                                                              |                                                       |
| initial                              | Perform initial start of ndbd,<br>including file system cleanup;<br>consult documentation before<br>using this option                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| initial-start                        | Perform partial initial start<br>(requiresnowait-nodes)                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| install[=name]                       | Used to install data node process<br>as Windows service; does not<br>apply on other platforms                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                                          | Description                                                                                                                                                       | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| logbuffer-size=#                                                | Control size of log buffer; for<br>use when debugging with many<br>log messages being generated;<br>default is sufficient for normal<br>operations                | ADDED: NDB 7.6.6                                      |
| login-path=path                                                 | Read given path from login file                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-mgmd<br>host=connection_string,                             | Same asndb-connectstring                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nodaemon                                                        | Do not start ndbd as daemon;<br>provided for testing purposes                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nostart,<br>-n                                                  | Do not start ndbd immediately;<br>ndbd waits for command to start<br>from ndb_mgm                                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nowait-nodes=list                                               | Do not wait for these data nodes<br>to start (takes comma-separated<br>list of node IDs); requiresndb<br>nodeid                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                                                  | Print program argument list and<br>exit                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| remove[=name]                                                   | Used to remove data node<br>process that was previously<br>installed as Windows service;<br>does not apply on other<br>platforms                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,<br>-?                                                    | Display help text and exit; same<br>ashelp                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| verbose,                                                        | Write extra debugging<br>information to node log                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -v                                                              |                                                                                                                                                                   |                                                       |

| Format   | Description                             | Added, Deprecated, or<br>Removed                      |
|----------|-----------------------------------------|-------------------------------------------------------|
| version, | Display version information and<br>exit | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V       |                                         |                                                       |

![](_page_174_Picture_2.jpeg)

### **Note**

All of these options also apply to the multithreaded version of this program ([ndbmtd](#page-187-0)) and you may substitute "[ndbmtd](#page-187-0)" for "[ndbd](#page-171-0)" wherever the latter occurs in this section.

### <span id="page-174-0"></span>• --bind-address

| Command-Line Format | bind-address=name |
|---------------------|-------------------|
| Type                | String            |
| Default Value       |                   |

Causes [ndbd](#page-171-0) to bind to a specific network interface (host name or IP address). This option has no default value.

### <span id="page-174-1"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

### <span id="page-174-2"></span>• --connect-delay=#

Determines the time to wait between attempts to contact a management server when starting (the number of attempts is controlled by the [--connect-retries](#page-174-3) option). The default is 5 seconds.

This option is deprecated, and is subject to removal in a future release of NDB Cluster. Use [-](#page-174-4) [connect-retry-delay](#page-174-4) instead.

# <span id="page-174-3"></span>• --connect-retries=#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 12                |
| Minimum Value       | -1                |
| Minimum Value       | -1                |
| Minimum Value       | 0                 |
| Maximum Value       | 65535             |

Set the number of times to retry a connection before giving up; 0 means 1 attempt only (and no retries). The default is 12 attempts. The time to wait between attempts is controlled by the [-](#page-174-4) [connect-retry-delay](#page-174-4) option.

Beginning with NDB 7.5.25 and NDB 7.6.21, you can set this option to -1, in which case, the data node process continues indefinitely to try to connect.

### <span id="page-174-4"></span>• --connect-retry-delay=#

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Numeric               |

| Default Value | 5          |
|---------------|------------|
| Minimum Value | 0          |
| Maximum Value | 4294967295 |

Determines the time to wait between attempts to contact a management server when starting (the time between attempts is controlled by the [--connect-retries](#page-174-3) option). The default is 5 seconds.

This option takes the place of the [--connect-delay](#page-174-2) option, which is now deprecated and subject to removal in a future release of NDB Cluster.

The short form -r for this option is deprecated as of NDB 7.5.25 and NDB 7.6.21, and subject to removal in a future release of NDB Cluster. Use the long form instead.

### <span id="page-175-0"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-178-2).

### <span id="page-175-1"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

### <span id="page-175-2"></span>• --daemon, -d

| Command-Line Format | daemon |
|---------------------|--------|
|---------------------|--------|

Instructs [ndbd](#page-171-0) or [ndbmtd](#page-187-0) to execute as a daemon process. This is the default behavior. [-](#page-179-1) [nodaemon](#page-179-1) can be used to prevent the process from running as a daemon.

This option has no effect when running [ndbd](#page-171-0) or [ndbmtd](#page-187-0) on Windows platforms.

## <span id="page-175-3"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

### <span id="page-175-4"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

# <span id="page-175-5"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |

Default Value [none]

Also read groups with concat(group, suffix).

<span id="page-176-1"></span>• --foreground

| Command-Line Format | foreground |
|---------------------|------------|
|---------------------|------------|

Causes [ndbd](#page-171-0) or [ndbmtd](#page-187-0) to execute as a foreground process, primarily for debugging purposes. This option implies the [--nodaemon](#page-179-1) option.

This option has no effect when running [ndbd](#page-171-0) or [ndbmtd](#page-187-0) on Windows platforms.

<span id="page-176-2"></span>• --help

Display help text and exit.

<span id="page-176-0"></span>• --initial

Instructs [ndbd](#page-171-0) to perform an initial start. An initial start erases any files created for recovery purposes by earlier instances of [ndbd](#page-171-0). It also re-creates recovery log files. On some operating systems, this process can take a substantial amount of time.

An [--initial](#page-176-0) start is to be used only when starting the [ndbd](#page-171-0) process under very special circumstances; this is because this option causes all files to be removed from the NDB Cluster file system and all redo log files to be re-created. These circumstances are listed here:

- When performing a software upgrade which has changed the contents of any files.
- When restarting the node with a new version of [ndbd](#page-171-0).
- As a measure of last resort when for some reason the node restart or system restart repeatedly fails. In this case, be aware that this node can no longer be used to restore data due to the destruction of the data files.

![](_page_176_Picture_17.jpeg)

#### **Warning**

To avoid the possibility of eventual data loss, it is recommended that you not use the --initial option together with StopOnError = 0. Instead, set StopOnError to 0 in config.ini only after the cluster has been started, then restart the data nodes normally—that is, without the --initial option. See the description of the [StopOnError](#page-45-1) parameter for a detailed explanation of this issue. (Bug #24945638)

Use of this option prevents the [StartPartialTimeout](#page-47-0) and [StartPartitionedTimeout](#page-47-1) configuration parameters from having any effect.

![](_page_177_Picture_3.jpeg)

#### **Important**

This option does not affect either of the following types of files:

- Backup files that have already been created by the affected node
- NDB Cluster Disk Data files (see Section 21.6.11, "NDB Cluster Disk Data Tables").

This option also has no effect on recovery of data by a data node that is just starting (or restarting) from data nodes that are already running. This recovery of data occurs automatically, and requires no user intervention in an NDB Cluster that is running normally.

It is permissible to use this option when starting the cluster for the very first time (that is, before any data node files have been created); however, it is not necessary to do so.

<span id="page-177-0"></span>• --initial-start

| Command-Line Format | initial-start |
|---------------------|---------------|
|---------------------|---------------|

This option is used when performing a partial initial start of the cluster. Each node should be started with this option, as well as [--nowait-nodes](#page-179-0).

Suppose that you have a 4-node cluster whose data nodes have the IDs 2, 3, 4, and 5, and you wish to perform a partial initial start using only nodes 2, 4, and 5—that is, omitting node 3:

```
$> ndbd --ndb-nodeid=2 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=4 --nowait-nodes=3 --initial-start
$> ndbd --ndb-nodeid=5 --nowait-nodes=3 --initial-start
```

When using this option, you must also specify the node ID for the data node being started with the [--ndb-nodeid](#page-178-4) option.

![](_page_177_Picture_16.jpeg)

#### **Important**

Do not confuse this option with the [--nowait-nodes](#page-196-0) option for [ndb\\_mgmd](#page-188-0), which can be used to enable a cluster configured with multiple management servers to be started without all management servers being online.

<span id="page-177-1"></span>• --install[=name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndbd           |

Causes [ndbd](#page-171-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndbd. Although it is preferable to specify other [ndbd](#page-171-0) program options in a my.ini or my.cnf configuration file, it is possible to use together with --

install. However, in such cases, the --install option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-176-0) option, since this causes the data node file system to be wiped and rebuilt every time the service is stopped and started. Extreme care should also be taken if you intend to use any of the other [ndbd](#page-171-0) options that affect the starting of data nodes—including [--initial-start](#page-177-0), [--nostart](#page-179-3), and [--nowait-nodes](#page-179-0) together with [--install](#page-177-1), and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-177-1) option has no effect on non-Windows platforms.

### <span id="page-178-0"></span>• --logbuffer-size=#

| Command-Line Format | logbuffer-size=# |
|---------------------|------------------|
| Type                | Integer          |
| Default Value       | 32768            |
| Minimum Value       | 2048             |
| Maximum Value       | 4294967295       |

Sets the size of the data node log buffer. When debugging with high amounts of extra logging, it is possible for the log buffer to run out of space if there are too many log messages, in which case some log messages can be lost. This should not occur during normal operations.

### <span id="page-178-1"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

### <span id="page-178-2"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |  |  |
|---------------------|---------------------------------|--|--|
|                     | connectstring=connection_string |  |  |
| Type                | String                          |  |  |
|                     |                                 |  |  |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

### <span id="page-178-3"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |  |  |
|---------------------|---------------------------------|--|--|
| Type                | String                          |  |  |
| Default Value       | [none]                          |  |  |

Same as [--ndb-connectstring](#page-178-2).

# <span id="page-178-4"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |  |
|---------------------|--------------|--|
| Type                | Integer      |  |
| Default Value       | [none]       |  |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-178-2).

<span id="page-179-4"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-179-1"></span>• --nodaemon

| Command-Line Format | nodaemon |
|---------------------|----------|
|---------------------|----------|

Prevents [ndbd](#page-171-0) or [ndbmtd](#page-187-0) from executing as a daemon process. This option overrides the [-](#page-175-2) [daemon](#page-175-2) option. This is useful for redirecting output to the screen when debugging the binary.

The default behavior for [ndbd](#page-171-0) and [ndbmtd](#page-187-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms, where it has no effect.

<span id="page-179-2"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-179-3"></span>• --nostart, -n

| Command-Line Format | nostart |
|---------------------|---------|
|---------------------|---------|

Instructs [ndbd](#page-171-0) not to start automatically. When this option is used, [ndbd](#page-171-0) connects to the management server, obtains configuration data from it, and initializes communication objects. However, it does not actually start the execution engine until specifically requested to do so by the management server. This can be accomplished by issuing the proper START command in the management client (see Section 21.6.1, "Commands in the NDB Cluster Management Client").

<span id="page-179-0"></span>• --nowait-nodes=node\_id\_1[, node\_id\_2[, ...]]

| Command-Line Format | nowait-nodes=list |  |
|---------------------|-------------------|--|
| Type                | String            |  |
| Default Value       |                   |  |

This option takes a list of data nodes which for which the cluster does not wait for before starting.

This can be used to start the cluster in a partitioned state. For example, to start the cluster with only half of the data nodes (nodes 2, 3, 4, and 5) running in a 4-node cluster, you can start each [ndbd](#page-171-0) process with --nowait-nodes=3,5. In this case, the cluster starts as soon as nodes 2 and 4 connect, and does not wait [StartPartitionedTimeout](#page-47-1) milliseconds for nodes 3 and 5 to connect as it would otherwise.

If you wanted to start up the same cluster as in the previous example without one [ndbd](#page-171-0) (say, for example, that the host machine for node 3 has suffered a hardware failure) then start nodes 2, 4, and 5 with --nowait-nodes=3. Then the cluster starts as soon as nodes 2, 4, and 5 connect and does not wait for node 3 to start.

<span id="page-180-0"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|                     |                |

Print program argument list and exit.

<span id="page-180-1"></span>• [--remove\[=](#page-180-1)name]

| Command-Line Format | remove[=name] |  |  |
|---------------------|---------------|--|--|
| Platform Specific   | Windows       |  |  |
| Type                | String        |  |  |
| Default Value       | ndbd          |  |  |

Causes an [ndbd](#page-171-0) process that was previously installed as a Windows service to be removed. Optionally, you can specify a name for the service to be uninstalled; if not set, the service name defaults to ndbd.

The [--remove](#page-180-1) option has no effect on non-Windows platforms.

<span id="page-180-2"></span>• --usage

Display help text and exit; same as [--help](#page-176-2).

<span id="page-180-3"></span>• --verbose, -v

Causes extra debug output to be written to the node log.

In NDB 7.6, you can also use NODELOG DEBUG ON and NODELOG DEBUG OFF to enable and disable this extra logging while the data node is running.

<span id="page-180-4"></span>• --version

| Command-Line Format<br>version |  |
|--------------------------------|--|
|--------------------------------|--|

Display version information and exit.

[ndbd](#page-171-0) generates a set of log files which are placed in the directory specified by [DataDir](#page-15-1) in the config.ini configuration file.

These log files are listed below. node\_id is and represents the node's unique identifier. For example, ndb\_2\_error.log is the error log generated by the data node whose node ID is 2.

• ndb\_node\_id\_error.log is a file containing records of all crashes which the referenced [ndbd](#page-171-0) process has encountered. Each record in this file contains a brief error string and a reference to a trace file for this crash. A typical entry in this file might appear as shown here:

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

Listings of possible [ndbd](#page-171-0) exit codes and messages generated when a data node process shuts down prematurely can be found in [Data Node Error Messages.](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md)

![](_page_181_Picture_1.jpeg)

#### **Important**

The last entry in the error log file is not necessarily the newest one (nor is it likely to be). Entries in the error log are not listed in chronological order; rather, they correspond to the order of the trace files as determined in the ndb\_node\_id\_trace.log.next file (see below). Error log entries are thus overwritten in a cyclical and not sequential fashion.

• ndb\_node\_id\_trace.log.trace\_id is a trace file describing exactly what happened just before the error occurred. This information is useful for analysis by the NDB Cluster development team.

It is possible to configure the number of these trace files that are created before old files are overwritten. trace\_id is a number which is incremented for each successive trace file.

- ndb\_node\_id\_trace.log.next is the file that keeps track of the next trace file number to be assigned.
- ndb\_node\_id\_out.log is a file containing any data output by the [ndbd](#page-171-0) process. This file is created only if [ndbd](#page-171-0) is started as a daemon, which is the default behavior.
- ndb\_node\_id.pid is a file containing the process ID of the [ndbd](#page-171-0) process when started as a daemon. It also functions as a lock file to avoid the starting of nodes with the same identifier.
- ndb\_node\_id\_signal.log is a file used only in debug versions of [ndbd](#page-171-0), where it is possible to trace all incoming, outgoing, and internal messages with their data in the [ndbd](#page-171-0) process.

It is recommended not to use a directory mounted through NFS because in some environments this can cause problems whereby the lock on the .pid file remains in effect even after the process has terminated.

To start [ndbd](#page-171-0), it may also be necessary to specify the host name of the management server and the port on which it is listening. Optionally, one may also specify the node ID that the process is to use.

```
$> ndbd --connect-string="nodeid=2;host=ndb_mgmd.mysql.com:1186"
```

See Section 21.4.3.3, "NDB Cluster Connection Strings", for additional information about this issue. For more information about data node configuration parameters, see [Section 21.4.3.6, "Defining NDB](#page-10-0) [Cluster Data Nodes".](#page-10-0)

When [ndbd](#page-171-0) starts, it actually initiates two processes. The first of these is called the "angel process"; its only job is to discover when the execution process has been completed, and then to restart the [ndbd](#page-171-0) process if it is configured to do so. Thus, if you attempt to kill [ndbd](#page-171-0) using the Unix kill command, it is necessary to kill both processes, beginning with the angel process. The preferred method of terminating an [ndbd](#page-171-0) process is to use the management client and stop the process from there.

The execution process uses one thread for reading, writing, and scanning data, as well as all other activities. This thread is implemented asynchronously so that it can easily handle thousands of concurrent actions. In addition, a watch-dog thread supervises the execution thread to make sure that it does not hang in an endless loop. A pool of threads handles file I/O, with each thread able to handle one open file. Threads can also be used for transporter connections by the transporters in the [ndbd](#page-171-0) process. In a multi-processor system performing a large number of operations (including updates), the [ndbd](#page-171-0) process can consume up to 2 CPUs if permitted to do so.

For a machine with many CPUs it is possible to use several [ndbd](#page-171-0) processes which belong to different node groups; however, such a configuration is still considered experimental and is not supported for MySQL 5.7 in a production setting. See Section 21.2.7, "Known Limitations of NDB Cluster".

# <span id="page-181-0"></span>**21.5.2 ndbinfo\_select\_all — Select From ndbinfo Tables**

[ndbinfo\\_select\\_all](#page-181-0) is a client program that selects all rows and columns from one or more tables in the ndbinfo database

Not all ndbinfo tables available in the mysql client can be read by this program (see later in this section). In addition, [ndbinfo\\_select\\_all](#page-181-0) can show information about some tables internal to ndbinfo which cannot be accessed using SQL, including the tables and columns metadata tables.

To select from one or more ndbinfo tables using [ndbinfo\\_select\\_all](#page-181-0), it is necessary to supply the names of the tables when invoking the program as shown here:

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
|     |                  |   |   |                                             |          |      |      |

Options that can be used with [ndbinfo\\_select\\_all](#page-181-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.23 Command-line options used with the program ndbinfo\_select\_all**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection-string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=db_name,                    | Name of database where table is<br>located                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d                                   |                                                                               |                                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                           | Description                                                                                                                                                       | Added, Deprecated, or<br>Removed                      |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| defaults-file=path                               | Read default options from given<br>file only                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string                  | Also read groups with<br>concat(group, suffix)                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| delay=#                                          | Set delay in seconds between<br>loops                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                            | Display help text and exit                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>login-path=path                            | Read given path from login file                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| loops=#,<br>-l                                   | Set number of times to perform<br>select                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection<br>string,<br>-c | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-mgmd<br>host=connection-string,              | Same asndb-connectstring                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c<br>ndb-nodeid=#                               | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                                      | Do not read default options from<br>any option file other than login<br>file                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection                  | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| parallelism=#,                                   | Set degree of parallelism                                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -p<br>print-defaults                             | Print program argument list and<br>exit                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,                                           | Display help text and exit; same<br>ashelp                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                               |                                                                                                                                                                   |                                                       |
| version,                                         | Display version information and<br>exit                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                                               |                                                                                                                                                                   |                                                       |

### <span id="page-184-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

### <span id="page-184-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

### <span id="page-184-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

### <span id="page-184-3"></span>• --connect-string

| Command-Line Format | connect-string=connection-string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-185-5).

### <span id="page-184-4"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

### <span id="page-184-5"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

### <span id="page-184-6"></span>• --defaults-file

| Command-Line Format | 3357<br>defaults-file=path |
|---------------------|----------------------------|
| Type                | String                     |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read default options from given file only.

<span id="page-185-0"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-185-1"></span>• --delay=seconds

| Command-Line Format | delay=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 5       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of seconds to wait between executing loops. Has no effect if [--loops](#page-185-4) is set to 0 or 1.

<span id="page-185-2"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-185-3"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-185-4"></span>• --loops=number, -l number

| Command-Line Format | loops=# |
|---------------------|---------|
| Type                | Numeric |
| Default Value       | 1       |
| Minimum Value       | 0       |
| Maximum Value       | MAX_INT |

This option sets the number of times to execute the select. Use [--delay](#page-185-1) to set the time between loops.

<span id="page-185-5"></span>• --ndb-connectstring

| Command-Line Format | ndb-connectstring=connection<br>string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-186-0"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection-string |  |
|---------------------|---------------------------------|--|
| Type                | String                          |  |
| Default Value       | [none]                          |  |

Same as [--ndb-connectstring](#page-185-5).

<span id="page-186-1"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |  |
|---------------------|--------------|--|
| Type                | Integer      |  |
| Default Value       | [none]       |  |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-185-5).

<span id="page-186-3"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-186-2"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-186-4"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-186-5"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-185-2).

<span id="page-186-6"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

[ndbinfo\\_select\\_all](#page-181-0) is unable to read the following tables:

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

# <span id="page-187-0"></span>**21.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)**

[ndbmtd](#page-187-0) is a multithreaded version of [ndbd](#page-171-0), the process that is used to handle all the data in tables using the NDBCLUSTER storage engine. [ndbmtd](#page-187-0) is intended for use on host computers having multiple CPU cores. Except where otherwise noted, [ndbmtd](#page-187-0) functions in the same way as [ndbd](#page-171-0); therefore, in this section, we concentrate on the ways in which [ndbmtd](#page-187-0) differs from [ndbd](#page-171-0), and you should consult [Section 21.5.1, "ndbd — The NDB Cluster Data Node Daemon",](#page-171-0) for additional information about running NDB Cluster data nodes that apply to both the single-threaded and multithreaded versions of the data node process.

Command-line options and configuration parameters used with [ndbd](#page-171-0) also apply to [ndbmtd](#page-187-0). For more information about these options and parameters, see [Section 21.5.1, "ndbd — The NDB Cluster Data](#page-171-0) [Node Daemon",](#page-171-0) and [Section 21.4.3.6, "Defining NDB Cluster Data Nodes",](#page-10-0) respectively.

[ndbmtd](#page-187-0) is also file system-compatible with [ndbd](#page-171-0). In other words, a data node running [ndbd](#page-171-0) can be stopped, the binary replaced with [ndbmtd](#page-187-0), and then restarted without any loss of data. (However, when doing this, you must make sure that [MaxNoOfExecutionThreads](#page-75-0) is set to an apppriate value before restarting the node if you wish for [ndbmtd](#page-187-0) to run in multithreaded fashion.) Similarly, an [ndbmtd](#page-187-0) binary can be replaced with [ndbd](#page-171-0) simply by stopping the node and then starting [ndbd](#page-171-0) in place of the multithreaded binary. It is not necessary when switching between the two to start the data node binary using [--initial](#page-176-0).

Using [ndbmtd](#page-187-0) differs from using [ndbd](#page-171-0) in two key respects:

- 1. Because [ndbmtd](#page-187-0) runs by default in single-threaded mode (that is, it behaves like [ndbd](#page-171-0)), you must configure it to use multiple threads. This can be done by setting an appropriate value in the config.ini file for the [MaxNoOfExecutionThreads](#page-75-0) configuration parameter or the [ThreadConfig](#page-80-0) configuration parameter. Using MaxNoOfExecutionThreads is simpler, but ThreadConfig offers more flexibility. For more information about these configuration parameters and their use, see [Multi-Threading Configuration Parameters \(ndbmtd\)](#page-75-1).
- 2. Trace files are generated by critical errors in [ndbmtd](#page-187-0) processes in a somewhat different fashion from how these are generated by [ndbd](#page-171-0) failures. These differences are discussed in more detail in the next few paragraphs.

Like [ndbd](#page-171-0), [ndbmtd](#page-187-0) generates a set of log files which are placed in the directory specified by [DataDir](#page-15-1) in the config.ini configuration file. Except for trace files, these are generated in the same way and have the same names as those generated by [ndbd](#page-171-0).

In the event of a critical error, [ndbmtd](#page-187-0) generates trace files describing what happened just prior to the error' occurrence. These files, which can be found in the data node's [DataDir](#page-15-1), are useful for analysis of problems by the NDB Cluster Development and Support teams. One trace file is generated for each [ndbmtd](#page-187-0) thread. The names of these files have the following pattern:

```
ndb_node_id_trace.log.trace_id_tthread_id,
```

In this pattern, node\_id stands for the data node's unique node ID in the cluster, trace\_id is a trace sequence number, and thread\_id is the thread ID. For example, in the event of the failure of an [ndbmtd](#page-187-0) process running as an NDB Cluster data node having the node ID 3 and with [MaxNoOfExecutionThreads](#page-75-0) equal to 4, four trace files are generated in the data node's data directory. If the is the first time this node has failed, then these files are named ndb\_3\_trace.log.1\_t1, ndb\_3\_trace.log.1\_t2, ndb\_3\_trace.log.1\_t3, and ndb\_3\_trace.log.1\_t4. Internally, these trace files follow the same format as [ndbd](#page-171-0) trace files.

The [ndbd](#page-171-0) exit codes and messages that are generated when a data node process shuts down prematurely are also used by [ndbmtd](#page-187-0). See [Data Node Error Messages](https://dev.mysql.com/doc/ndb-internals/en/ndb-node-error-messages.md), for a listing of these.

![](_page_188_Picture_4.jpeg)

#### **Note**

It is possible to use [ndbd](#page-171-0) and [ndbmtd](#page-187-0) concurrently on different data nodes in the same NDB Cluster. However, such configurations have not been tested extensively; thus, we cannot recommend doing so in a production setting at this time.

# <span id="page-188-0"></span>**21.5.4 ndb\_mgmd — The NDB Cluster Management Server Daemon**

The management server is the process that reads the cluster configuration file and distributes this information to all nodes in the cluster that request it. It also maintains a log of cluster activities. Management clients can connect to the management server and check the cluster's status.

Options that can be used with [ndb\\_mgmd](#page-188-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.24 Command-line options used with the program ndb\_mgmd**

| Format                                       | Description                                                                                                          | Added, Deprecated, or<br>Removed                      |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| bind-address=host                            | Local bind address                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| character-sets<br>dir=path                   | Directory containing character<br>sets                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| config-cache[=TRUE <br>FALSE]                | Enable management server<br>configuration cache; true by<br>default                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| config-file=file,<br>-f file                 | Specify cluster configuration file;<br>also specifyreload orinitial to<br>override configuration cache if<br>present | (Supported in all NDB releases<br>based on MySQL 5.7) |
| configdir=directory,<br>config-dir=directory | Specify cluster management<br>server configuration cache<br>directory                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                            | Number of times to retry<br>connection before giving up                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                        | Number of seconds to wait<br>between attempts to contact<br>management server                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string,         | Same asndb-connectstring                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                         |                                                                                                                      |                                                       |

| Format                              | Description                                                                                                           | Added, Deprecated, or<br>Removed                      |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| core-file                           | Write core file on error; used in<br>debugging                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| daemon,                             | Run ndb_mgmd in daemon<br>mode (default)                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d                                  |                                                                                                                       |                                                       |
| defaults-extra<br>file=path         | Read given file after global files<br>are read                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                  | Read default options from given<br>file only                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string     | Also read groups with<br>concat(group, suffix)                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                               | Display help text and exit                                                                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                  |                                                                                                                       |                                                       |
| initial                             | Causes management server to<br>reload configuration data from<br>configuration file, bypassing<br>configuration cache | (Supported in all NDB releases<br>based on MySQL 5.7) |
| install[=name]                      | Used to install management<br>server process as Windows<br>service; does not apply on other<br>platforms              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| interactive                         | Run ndb_mgmd in interactive<br>mode (not officially supported in<br>production; for testing purposes<br>only)         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| log-name=name                       | Name to use when writing cluster<br>log messages applying to this<br>node                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| login-path=path                     | Read given path from login file                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| mycnf                               | Read cluster configuration data<br>from my.cnf file                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb                                 | Set connect string for                                                                                                | (Supported in all NDB releases                        |
| connectstring=connection_string,    | connecting to ndb_mgmd.                                                                                               | based on MySQL 5.7)                                   |
| -c connection_string                | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf          |                                                       |
| ndb-mgmd<br>host=connection_string, | Same asndb-connectstring                                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                |                                                                                                                       |                                                       |
| ndb-nodeid=#                        | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection     | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;                               | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format             | Description                                                                                                                                                                                         | Added, Deprecated, or<br>Removed                      |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|                    | useskip-ndb-optimized-node<br>selection to disable                                                                                                                                                  |                                                       |
| no-defaults        | Do not read default options from<br>any option file other than login<br>file                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-nodeid-checks   | Do not perform any node ID<br>checks                                                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nodaemon           | Do not run ndb_mgmd as a<br>daemon                                                                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nowait-nodes=list  | Do not wait for management<br>nodes specified when starting<br>this management server;<br>requiresndb-nodeid option                                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults     | Print program argument list and<br>exit                                                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-full-config, | Print full configuration and exit                                                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -P<br>reload       | Causes management server to<br>compare configuration file with<br>configuration cache                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| remove[=name]      | Used to remove management<br>server process that was<br>previously installed as Windows<br>service, optionally specifying<br>name of service to be removed;<br>does not apply on other<br>platforms | (Supported in all NDB releases<br>based on MySQL 5.7) |
| skip-config-file   | Do not use configuration file                                                                                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,             | Display help text and exit; same<br>ashelp                                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>verbose,     | Write additional information to<br>log                                                                                                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -v<br>version,     | Display version information and                                                                                                                                                                     | (Supported in all NDB releases                        |
| -V                 | exit                                                                                                                                                                                                | based on MySQL 5.7)                                   |

# <span id="page-190-0"></span>• --bind-address=host

| Command-Line Format | bind-address=host |  |
|---------------------|-------------------|--|
| Type                | String            |  |
| Default Value       | [none]            |  |

Causes the management server to bind to a specific network interface (host name or IP address). This option has no default value.

<span id="page-191-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-191-1"></span>• --config-cache

| Command-Line Format | config-cache[=TRUE FALSE] |  |
|---------------------|---------------------------|--|
| Type                | Boolean                   |  |
| Default Value       | TRUE                      |  |

This option, whose default value is 1 (or TRUE, or ON), can be used to disable the management server's configuration cache, so that it reads its configuration from config.ini every time it starts (see Section 21.4.3, "NDB Cluster Configuration Files"). You can do this by starting the [ndb\\_mgmd](#page-188-0) process with any one of the following options:

- --config-cache=0
- --config-cache=FALSE
- --config-cache=OFF
- --skip-config-cache

Using one of the options just listed is effective only if the management server has no stored configuration at the time it is started. If the management server finds any configuration cache files, then the --config-cache option or the --skip-config-cache option is ignored. Therefore, to disable configuration caching, the option should be used the first time that the management server is started. Otherwise—that is, if you wish to disable configuration caching for a management server that has already created a configuration cache—you must stop the management server, delete any existing configuration cache files manually, then restart the management server with --skipconfig-cache (or with --config-cache set equal to 0, OFF, or FALSE).

Configuration cache files are normally created in a directory named mysql-cluster under the installation directory (unless this location has been overridden using the [--configdir](#page-192-1) option). Each time the management server updates its configuration data, it writes a new cache file. The files are named sequentially in order of creation using the following format:

```
ndb_node-id_config.bin.seq-number
```

node-id is the management server's node ID; seq-number is a sequence number, beginning with 1. For example, if the management server's node ID is 5, then the first three configuration cache files would, when they are created, be named ndb\_5\_config.bin.1, ndb\_5\_config.bin.2, and ndb\_5\_config.bin.3.

If your intent is to purge or reload the configuration cache without actually disabling caching, you should start [ndb\\_mgmd](#page-188-0) with one of the options [--reload](#page-197-2) or [--initial](#page-193-6) instead of --skipconfig-cache.

To re-enable the configuration cache, simply restart the management server, but without the --config-cache or --skip-config-cache option that was used previously to disable the configuration cache.

[ndb\\_mgmd](#page-188-0) does not check for the configuration directory ([--configdir](#page-192-1)) or attempts to create one when --skip-config-cache is used. (Bug #13428853)

### <span id="page-192-0"></span>• --config-file=filename, -f filename

| Command-Line Format | config-file=file |
|---------------------|------------------|
| Disabled by         | skip-config-file |
| Type                | File name        |
| Default Value       | [none]           |

Instructs the management server as to which file it should use for its configuration file. By default, the management server looks for a file named config.ini in the same directory as the [ndb\\_mgmd](#page-188-0) executable; otherwise the file name and location must be specified explicitly.

This option has no default value, and is ignored unless the management server is forced to read the configuration file, either because [ndb\\_mgmd](#page-188-0) was started with the [--reload](#page-197-2) or [--initial](#page-193-6) option, or because the management server could not find any configuration cache.

The [--config-file](#page-192-0) option is also read if [ndb\\_mgmd](#page-188-0) was started with [--config-cache=OFF](#page-191-1). See Section 21.4.3, "NDB Cluster Configuration Files", for more information.

### <span id="page-192-1"></span>• --configdir=dir\_name

| Command-Line Format | configdir=directory        |
|---------------------|----------------------------|
|                     | config-dir=directory       |
| Type                | File name                  |
| Default Value       | \$INSTALLDIR/mysql-cluster |

Specifies the cluster management server's configuration cache directory. --config-dir is an alias for this option.

### <span id="page-192-2"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

### <span id="page-192-3"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

# <span id="page-192-4"></span>• --connect-string

| Command-Line Format | connect-string=connection_string<br>3365 |
|---------------------|------------------------------------------|
| Type                | String                                   |

Default Value [none]

Same as [--ndb-connectstring](#page-195-1).

<span id="page-193-0"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-193-1"></span>• --daemon, -d

| Command-Line Format | daemon |
|---------------------|--------|
|---------------------|--------|

Instructs [ndb\\_mgmd](#page-188-0) to start as a daemon process. This is the default behavior.

This option has no effect when running [ndb\\_mgmd](#page-188-0) on Windows platforms.

<span id="page-193-2"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-193-3"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-193-4"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-193-5"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-193-6"></span>• --initial

| Command-Line Format | initial |
|---------------------|---------|

Configuration data is cached internally, rather than being read from the cluster global configuration file each time the management server is started (see Section 21.4.3, "NDB Cluster Configuration Files"). Using the --initial option overrides this behavior, by forcing the management server to delete any existing cache files, and then to re-read the configuration data from the cluster configuration file and to build a new cache.

This differs in two ways from the [--reload](#page-197-2) option. First, --reload forces the server to check the configuration file against the cache and reload its data only if the contents of the file are different from the cache. Second, --reload does not delete any existing cache files.

If [ndb\\_mgmd](#page-188-0) is invoked with --initial but cannot find a global configuration file, the management server cannot start.

When a management server starts, it checks for another management server in the same NDB Cluster and tries to use the other management server's configuration data. This behavior has implications when performing a rolling restart of an NDB Cluster with multiple management nodes. See Section 21.6.5, "Performing a Rolling Restart of an NDB Cluster", for more information.

When used together with the [--config-file](#page-192-0) option, the cache is cleared only if the configuration file is actually found.

### <span id="page-194-0"></span>• --install[=name]

| Command-Line Format | install[=name] |
|---------------------|----------------|
| Platform Specific   | Windows        |
| Type                | String         |
| Default Value       | ndb_mgmd       |

Causes [ndb\\_mgmd](#page-188-0) to be installed as a Windows service. Optionally, you can specify a name for the service; if not set, the service name defaults to ndb\_mgmd. Although it is preferable to specify other [ndb\\_mgmd](#page-188-0) program options in a my.ini or my.cnf configuration file, it is possible to use them together with [--install](#page-194-0). However, in such cases, the [--install](#page-194-0) option must be specified first, before any other options are given, for the Windows service installation to succeed.

It is generally not advisable to use this option together with the [--initial](#page-176-0) option, since this causes the configuration cache to be wiped and rebuilt every time the service is stopped and started. Care should also be taken if you intend to use any other [ndb\\_mgmd](#page-188-0) options that affect the starting of the management server, and you should make absolutely certain you fully understand and allow for any possible consequences of doing so.

The [--install](#page-194-0) option has no effect on non-Windows platforms.

# <span id="page-194-1"></span>• --interactive

| Command-Line Format | interactive |
|---------------------|-------------|
|---------------------|-------------|

Starts [ndb\\_mgmd](#page-188-0) in interactive mode; that is, an [ndb\\_mgm](#page-199-0) client session is started as soon as the management server is running. This option does not start any other NDB Cluster nodes.

### <span id="page-194-3"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

### <span id="page-194-2"></span>• --log-name=name

| Command-Line Format | log-name=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | MgmtSrvr      |

Provides a name to be used for this node in the cluster log.

<span id="page-195-0"></span>• --mycnf

| Command-Line Format | mycnf |
|---------------------|-------|
|---------------------|-------|

Read configuration data from the my.cnf file.

<span id="page-195-1"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connection string. Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf; ignored if [--config-file](#page-192-0) is specified.

<span id="page-195-2"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-195-1).

<span id="page-195-3"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-195-1).

<span id="page-195-4"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-195-5"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-195-6"></span>• --no-nodeid-checks

| Command-Line Format | no-nodeid-checks |
|---------------------|------------------|
|---------------------|------------------|

Do not perform any checks of node IDs.

<span id="page-195-7"></span>• --nodaemon

| Command-Line Format | nodaemon |
|---------------------|----------|
|                     |          |

Instructs [ndb\\_mgmd](#page-188-0) not to start as a daemon process.

The default behavior for [ndb\\_mgmd](#page-188-0) on Windows is to run in the foreground, making this option unnecessary on Windows platforms.

### <span id="page-196-0"></span>• --nowait-nodes

| Command-Line Format | nowait-nodes=list |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | [none]            |
| Minimum Value       | 1                 |
| Maximum Value       | 255               |

When starting an NDB Cluster is configured with two management nodes, each management server normally checks to see whether the other [ndb\\_mgmd](#page-188-0) is also operational and whether the other management server's configuration is identical to its own. However, it is sometimes desirable to start the cluster with only one management node (and perhaps to allow the other [ndb\\_mgmd](#page-188-0) to be started later). This option causes the management node to bypass any checks for any other management nodes whose node IDs are passed to this option, permitting the cluster to start as though configured to use only the management node that was started.

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

Assume that you wish to start this cluster using only the management server having node ID 10 and running on the host having the IP address 198.51.100.150. (Suppose, for example, that the host computer on which you intend to the other management server is temporarily unavailable due to

a hardware failure, and you are waiting for it to be repaired.) To start the cluster in this way, use a command line on the machine at 198.51.100.150 to enter the following command:

```
$> ndb_mgmd --ndb-nodeid=10 --nowait-nodes=11
```

As shown in the preceding example, when using [--nowait-nodes](#page-196-0), you must also use the [--ndb](#page-195-3)[nodeid](#page-195-3) option to specify the node ID of this [ndb\\_mgmd](#page-188-0) process.

You can then start each of the cluster's data nodes in the usual way. If you wish to start and use the second management server in addition to the first management server at a later time without restarting the data nodes, you must start each data node with a connection string that references both management servers, like this:

```
$> ndbd -c 198.51.100.150,198.51.100.151
```

The same is true with regard to the connection string used with any mysqld processes that you wish to start as NDB Cluster SQL nodes connected to this cluster. See Section 21.4.3.3, "NDB Cluster Connection Strings", for more information.

When used with [ndb\\_mgmd](#page-188-0), this option affects the behavior of the management node with regard to other management nodes only. Do not confuse it with the [--nowait-nodes](#page-179-0) option used with [ndbd](#page-171-0) or [ndbmtd](#page-187-0) to permit a cluster to start with fewer than its full complement of data nodes; when used with data nodes, this option affects their behavior only with regard to other data nodes.

Multiple management node IDs may be passed to this option as a comma-separated list. Each node ID must be no less than 1 and no greater than 255. In practice, it is quite rare to use more than two management servers for the same NDB Cluster (or to have any need for doing so); in most cases you need to pass to this option only the single node ID for the one management server that you do not wish to use when starting the cluster.

![](_page_197_Picture_9.jpeg)

#### **Note**

When you later start the "missing" management server, its configuration must match that of the management server that is already in use by the cluster. Otherwise, it fails the configuration check performed by the existing management server, and does not start.

<span id="page-197-0"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-197-1"></span>• --print-full-config, -P

| Command-Line Format | print-full-config |
|---------------------|-------------------|
|---------------------|-------------------|

Shows extended information regarding the configuration of the cluster. With this option on the command line the [ndb\\_mgmd](#page-188-0) process prints information about the cluster setup including an extensive list of the cluster configuration sections as well as parameters and their values. Normally used together with the [--config-file](#page-192-0) (-f) option.

<span id="page-197-2"></span>• --reload

| Command-Line Format | reload |
|---------------------|--------|
|---------------------|--------|

NDB Cluster configuration data is stored internally rather than being read from the cluster global configuration file each time the management server is started (see Section 21.4.3, "NDB Cluster 3370 Configuration Files"). Using this option forces the management server to check its internal data store against the cluster configuration file and to reload the configuration if it finds that the configuration file does not match the cache. Existing configuration cache files are preserved, but not used.

This differs in two ways from the [--initial](#page-193-6) option. First, --initial causes all cache files to be deleted. Second, --initial forces the management server to re-read the global configuration file and construct a new cache.

If the management server cannot find a global configuration file, then the --reload option is ignored.

When --reload is used, the management server must be able to communicate with data nodes and any other management servers in the cluster before it attempts to read the global configuration file; otherwise, the management server fails to start. This can happen due to changes in the networking environment, such as new IP addresses for nodes or an altered firewall configuration. In such cases, you must use [--initial](#page-193-6) instead to force the exsiting cached configuration to be discarded and reloaded from the file. See Section 21.6.5, "Performing a Rolling Restart of an NDB Cluster", for additional information.

<span id="page-198-0"></span>• --remove{=name]

| Command-Line Format | remove[=name] |  |
|---------------------|---------------|--|
| Platform Specific   | Windows       |  |
| Type                | String        |  |
| Default Value       | ndb_mgmd      |  |

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-198-1"></span>• --skip-config-file

| Command-Line Format | skip-config-file |
|---------------------|------------------|
|---------------------|------------------|

Do not read cluster configuration file; ignore [--initial](#page-193-6) and [--reload](#page-197-2) options if specified.

<span id="page-198-2"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-193-5).

<span id="page-198-3"></span>• --verbose, -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Remove a management server process that has been installed as a Windows service, optionally specifying the name of the service to be removed. Applies only to Windows platforms.

<span id="page-198-4"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

It is not strictly necessary to specify a connection string when starting the management server. However, if you are using more than one management server, a connection string should be provided and each node in the cluster should specify its node ID explicitly. 3371 See Section 21.4.3.3, "NDB Cluster Connection Strings", for information about using connection strings. [Section 21.5.4, "ndb\\_mgmd — The NDB Cluster Management Server Daemon"](#page-188-0), describes other options for [ndb\\_mgmd](#page-188-0).

The following files are created or used by [ndb\\_mgmd](#page-188-0) in its starting directory, and are placed in the [DataDir](#page-15-1) as specified in the config.ini configuration file. In the list that follows, node\_id is the unique node identifier.

- config.ini is the configuration file for the cluster as a whole. This file is created by the user and read by the management server. Section 21.4, "Configuration of NDB Cluster", discusses how to set up this file.
- ndb\_node\_id\_cluster.log is the cluster events log file. Examples of such events include checkpoint startup and completion, node startup events, node failures, and levels of memory usage. A complete listing of cluster events with descriptions may be found in Section 21.6, "Management of NDB Cluster".

By default, when the size of the cluster log reaches one million bytes, the file is renamed to ndb\_node\_id\_cluster.log.seq\_id, where seq\_id is the sequence number of the cluster log file. (For example: If files with the sequence numbers 1, 2, and 3 already exist, the next log file is named using the number 4.) You can change the size and number of files, and other characteristics of the cluster log, using the [LogDestination](#page-5-0) configuration parameter.

- ndb\_node\_id\_out.log is the file used for stdout and stderr when running the management server as a daemon.
- ndb\_node\_id.pid is the process ID file used when running the management server as a daemon.

# <span id="page-199-0"></span>**21.5.5 ndb\_mgm — The NDB Cluster Management Client**

The [ndb\\_mgm](#page-199-0) management client process is actually not needed to run the cluster. Its value lies in providing a set of commands for checking the cluster's status, starting backups, and performing other administrative functions. The management client accesses the management server using a C API. Advanced users can also employ this API for programming dedicated management processes to perform tasks similar to those performed by [ndb\\_mgm](#page-199-0).

To start the management client, it is necessary to supply the host name and port number of the management server:

```
$> ndb_mgm [host_name [port_num]]
```

For example:

```
$> ndb_mgm ndb_mgmd.mysql.com 1186
```

The default host name and port number are localhost and 1186, respectively.

Options that can be used with [ndb\\_mgm](#page-199-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.25 Command-line options used with the program ndb\_mgm**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -c connection_string                    |                                                                                                                                               |                                                       |
| core-file                               | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                      | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| execute=command,                        | Execute command and exit                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -e command                              |                                                                                                                                               |                                                       |
| help,                                   | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>login-path=path                   | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| try-reconnect=#,                        | Set number of times to retry<br>connection before giving up;                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -t #                                    | synonym forconnect-retries                                                                                                                    |                                                       |
| usage,                                  | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                      |                                                                                                                                               |                                                       |
| version,                                | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                                      |                                                                                                                                               |                                                       |

• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-1-5"></span>• --connect-retries=#

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Numeric           |
| Default Value       | 3                 |
| Minimum Value       | 0                 |
| Maximum Value       | 4294967295        |

This option specifies the number of times following the first attempt to retry a connection before giving up (the client always tries the connection at least once). The length of time to wait per attempt is set using [--connect-retry-delay](#page-1-4).

This option is synonymous with the [--try-reconnect](#page-3-5) option, which is now deprecated.

<span id="page-1-4"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-1-0"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-2-4).

<span id="page-1-1"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-1-2"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-1-3"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read default options from given file only.

<span id="page-2-0"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-2-1"></span>• --execute=command, -e command

| Command-Line Format | execute=command |
|---------------------|-----------------|
|---------------------|-----------------|

This option can be used to send a command to the NDB Cluster management client from the system shell. For example, either of the following is equivalent to executing [SHOW](#page-143-0) in the management client:

```
$> ndb_mgm -e "SHOW"
$> ndb_mgm --execute="SHOW"
```

This is analogous to how the --execute or -e option works with the mysql command-line client. See Section 4.2.2.1, "Using Options on the Command Line".

![](_page_2_Picture_11.jpeg)

#### **Note**

If the management client command to be passed using this option contains any space characters, then the command must be enclosed in quotation marks. Either single or double quotation marks may be used. If the management client command contains no space characters, the quotation marks are optional.

<span id="page-2-2"></span>• --help

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-2-3"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-2-4"></span>• --ndb-connectstring

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: [nodeid=id;][host=]hostname[:port]. Overrides entries in NDB\_CONNECTSTRING and my.cnf.

# <span id="page-3-0"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-2-4).

## <span id="page-3-1"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-2-4).

<span id="page-3-2"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

## <span id="page-3-3"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

## <span id="page-3-4"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

## <span id="page-3-5"></span>• --try-reconnect=number

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

This option is deprecated and subject to removal in a future release. Use [--connect-retries](#page-1-5), instead. <sup>3376</sup>

# <span id="page-4-0"></span>• --usage

Display help text and exit; same as [--help](#page-2-2).

## <span id="page-4-1"></span>• --version

|  | Command-Line Format | version |
|--|---------------------|---------|
|--|---------------------|---------|

Display version information and exit.

Additional information about using ndb\_mgm can be found in [Section 21.6.1, "Commands in the NDB](#page-140-0) [Cluster Management Client"](#page-140-0).

# <span id="page-4-2"></span>**21.5.6 ndb\_blob\_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables**

This tool can be used to check for and remove orphaned BLOB column parts from NDB tables, as well as to generate a file listing any orphaned parts. It is sometimes useful in diagnosing and repairing corrupted or damaged NDB tables containing BLOB or TEXT columns.

The basic syntax for [ndb\\_blob\\_tool](#page-4-2) is shown here:

```
ndb_blob_tool [options] table [column, ...]
```

Unless you use the [--help](#page-8-0) option, you must specify an action to be performed by including one or more of the options [--check-orphans](#page-6-0), [--delete-orphans](#page-7-0), or [--dump-file](#page-8-1). These options cause [ndb\\_blob\\_tool](#page-4-2) to check for orphaned BLOB parts, remove any orphaned BLOB parts, and generate a dump file listing orphaned BLOB parts, respectively, and are described in more detail later in this section.

You must also specify the name of a table when invoking [ndb\\_blob\\_tool](#page-4-2). In addition, you can optionally follow the table name with the (comma-separated) names of one or more BLOB or TEXT columns from that table. If no columns are listed, the tool works on all of the table's BLOB and TEXT columns. If you need to specify a database, use the [--database](#page-7-1) (-d) option.

The [--verbose](#page-9-0) option provides additional information in the output about the tool's progress.

Options that can be used with [ndb\\_blob\\_tool](#page-4-2) are shown in the following table. Additional descriptions follow the table.

**Table 21.26 Command-line options used with the program ndb\_blob\_tool**

| Format                     | Description                                                                              | Added, Deprecated, or<br>Removed                      |
|----------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------|
| add-missing                | Write dummy blob parts to take<br>place of those which are missing                       | ADDED: NDB 7.5.18, NDB<br>7.6.14                      |
| character-sets<br>dir=path | Directory containing character<br>sets                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| check-missing              | Check for blobs having inline<br>parts but missing one or more<br>parts from parts table | ADDED: NDB 7.5.18, NDB<br>7.6.14                      |
| check-orphans              | Check for blob parts having no<br>corresponding inline parts                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#          | Number of times to retry<br>connection before giving up                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                               | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                       | Database to find the table in                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                              |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                   | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| delete-orphans                       | Delete blob parts having no<br>corresponding inline parts                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| dump-file=file                       | Write orphan keys to specified<br>file                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                   |                                                                                                                                               |                                                       |
| login-path=path                      | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb                                  | Set connect string for                                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,     | connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                                              | based on MySQL 5.7)                                   |
| -c connection_string                 | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd<br>host=connection_string,  | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                                                                                               |                                                       |
| ndb-nodeid=#                         | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection      | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                          | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format         | Description                                | Added, Deprecated, or<br>Removed                      |
|----------------|--------------------------------------------|-------------------------------------------------------|
| print-defaults | Print program argument list and<br>exit    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,<br>-?   | Display help text and exit; same<br>ashelp | (Supported in all NDB releases<br>based on MySQL 5.7) |
| verbose,       | Verbose output                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -v<br>version, | Display version information and<br>exit    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V             |                                            |                                                       |

## <span id="page-6-1"></span>• --add-missing

| Command-Line Format | add-missing |
|---------------------|-------------|
|---------------------|-------------|

For each inline part in NDB Cluster tables which has no corresponding BLOB part, write a dummy BLOB part of the required length, consisting of spaces.

## <span id="page-6-2"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

## <span id="page-6-3"></span>• --check-missing

| Command-Line Format | check-missing |
|---------------------|---------------|
|---------------------|---------------|

Check for inline parts in NDB Cluster tables which have no corresponding BLOB parts.

# <span id="page-6-0"></span>• --check-orphans

| Command-Line Format | check-orphans |
|---------------------|---------------|
|---------------------|---------------|

Check for BLOB parts in NDB Cluster tables which have no corresponding inline parts.

## <span id="page-6-4"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

## <span id="page-6-5"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |

| Maximum Value | 5 |
|---------------|---|
|---------------|---|

Number of seconds to wait between attempts to contact management server.

<span id="page-7-2"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-8-3).

<span id="page-7-3"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-7-1"></span>• --database=db\_name, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [none]        |

Specify the database to find the table in.

<span id="page-7-4"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-7-5"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-7-6"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

• --delete-orphans

<span id="page-7-0"></span>

| Command-Line Format | delete-orphans |
|---------------------|----------------|
|---------------------|----------------|

# <span id="page-8-1"></span>• --dump-file=file

| Command-Line Format | dump-file=file |
|---------------------|----------------|
| Type                | File name      |
| Default Value       | [none]         |

Writes a list of orphaned BLOB column parts to file. The information written to the file includes the table key and BLOB part number for each orphaned BLOB part.

## <span id="page-8-0"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

## <span id="page-8-2"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

## <span id="page-8-3"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

## <span id="page-8-4"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-8-3).

## <span id="page-8-5"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-8-3).

<span id="page-8-6"></span>• --ndb-optimized-node-selection

|                     |                              | 3381 |
|---------------------|------------------------------|------|
| Command-Line Format | ndb-optimized-node-selection |      |

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-

<span id="page-9-1"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-9-2"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-9-3"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-8-0).

<span id="page-9-0"></span>• --verbose

```
Command-Line Format --verbose
```

Provide extra information in the tool's output regarding its progress.

<span id="page-9-4"></span>• --version

```
Command-Line Format --version
```

Display version information and exit.

# **Example**

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

When run with [--check-orphans](#page-6-0) against this table, [ndb\\_blob\\_tool](#page-4-2) generates the following output:

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
```

```
NDB$BLOB_19_2: nextResult: res=1
total parts: 10
orphan parts: 0
disconnected
NDBT_ProgramExit: 0 - OK
```

The tool reports that there are no NDB BLOB column parts associated with column c1, even though c1 is a TEXT column. This is due to the fact that, in an NDB table, only the first 256 bytes of a BLOB or TEXT column value are stored inline, and only the excess, if any, is stored separately; thus, if there are no values using more than 256 bytes in a given column of one of these types, no BLOB column parts are created by NDB for this column. See Section 11.7, "Data Type Storage Requirements", for more information.

# <span id="page-10-0"></span>**21.5.7 ndb\_config — Extract NDB Cluster Configuration Information**

This tool extracts current configuration information for data nodes, SQL nodes, and API nodes from one of a number of sources: an NDB Cluster management node, or its config.ini or my.cnf file. By default, the management node is the source for the configuration data; to override the default, execute ndb\_config with the [--config-file](#page-13-0) or [--mycnf](#page-16-0) option. It is also possible to use a data node as the source by specifying its node ID with [--config\\_from\\_node=](#page-13-1)node\_id.

[ndb\\_config](#page-10-0) can also provide an offline dump of all configuration parameters which can be used, along with their default, maximum, and minimum values and other information. The dump can be produced in either text or XML format; for more information, see the discussion of the [--configinfo](#page-13-2) and [--xml](#page-19-0) options later in this section).

You can filter the results by section (DB, SYSTEM, or CONNECTIONS) using one of the options [-](#page-17-0) [nodes](#page-17-0), [--system](#page-18-0), or [--connections](#page-14-0).

Options that can be used with [ndb\\_config](#page-10-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.27 Command-line options used with the program ndb\_config**

| Format                     | Description                                                                                                                                                                                                            | Added, Deprecated, or<br>Removed                      |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path | Directory containing character<br>sets                                                                                                                                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| config-file=file_name      | Set the path to config.ini file                                                                                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| config-from-node=#         | Obtain configuration data from<br>the node having this ID (must be<br>a data node)                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| configinfo                 | Dumps information about all<br>NDB configuration parameters<br>in text format with default,<br>maximum, and minimum values.<br>Use withxml to obtain XML<br>output                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connections                | Print information only about<br>connections specified in [tcp],<br>[tcp default], [sci], [sci default],<br>[shm], or [shm default] sections<br>of cluster configuration file.<br>Cannot be used withsystem or<br>nodes | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#          | Number of times to retry<br>connection before giving up                                                                                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                               | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                   | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| diff-default                         | Print only configuration<br>parameters that have non-default<br>values                                                                        | ADDED: NDB 7.5.7, NDB 7.6.3                           |
| fields=string,                       | Field separator                                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -f                                   |                                                                                                                                               |                                                       |
| help,                                | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>host=name                      | Specify host                                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| login-path=path                      | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| mycnf                                | Read configuration data from<br>my.cnf file                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb                                  | Set connect string for                                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,     | connecting to ndb_mgmd.                                                                                                                       | based on MySQL 5.7)                                   |
| -c connection_string                 | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                  |                                                       |
| ndb-mgmd<br>host=connection_string,  | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                                                                                               |                                                       |
| ndb-nodeid=#                         | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection      | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format         | Description                                                                                                                                        | Added, Deprecated, or<br>Removed                      |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| no-defaults    | Do not read default options from<br>any option file other than login<br>file                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nodeid=#       | Get configuration of node with<br>this ID                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nodes          | Print node information ([ndbd] or<br>[ndbd default] section of cluster<br>configuration file) only. Cannot<br>be used withsystem or<br>connections | (Supported in all NDB releases<br>based on MySQL 5.7) |
| query=string,  | One or more query options<br>(attributes)                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -q string      |                                                                                                                                                    |                                                       |
| query-all,     | Dumps all parameters and<br>values to a single comma                                                                                               | ADDED: NDB 7.4.16, NDB 7.5.7                          |
| -a             | delimited string                                                                                                                                   |                                                       |
| print-defaults | Print program argument list and<br>exit                                                                                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| rows=string,   | Row separator                                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -r string      |                                                                                                                                                    |                                                       |
| system         | Print SYSTEM section<br>information only (see ndb_config<br>configinfo output). Cannot<br>be used withnodes or<br>connections                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| type=name      | Specify node type                                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,         | Display help text and exit; same<br>ashelp                                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?             |                                                                                                                                                    |                                                       |
| version,       | Display version information and<br>exit                                                                                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V             |                                                                                                                                                    |                                                       |
| configinfoxml  | Usexml withconfiginfo<br>to obtain a dump of all NDB<br>configuration parameters in XML<br>format with default, maximum,<br>and minimum values     | (Supported in all NDB releases<br>based on MySQL 5.7) |

<span id="page-12-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|                     |                         |

Directory containing character sets.

# <span id="page-13-2"></span>• --configinfo

The --configinfo option causes [ndb\\_config](#page-10-0) to dump a list of each NDB Cluster configuration parameter supported by the NDB Cluster distribution of which [ndb\\_config](#page-10-0) is a part, including the following information:

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
…
```

Use this option together with the [--xml](#page-19-0) option to obtain output in XML format.

<span id="page-13-0"></span>• --config-file=path-to-file

| Command-Line Format | config-file=file_name |
|---------------------|-----------------------|
| Type                | File name             |
| Default Value       |                       |

Gives the path to the management server's configuration file (config.ini). This may be a relative or absolute path. If the management node resides on a different host from the one on which [ndb\\_config](#page-10-0) is invoked, then an absolute path must be used.

<span id="page-13-1"></span>• --config\_from\_node=#

| Command-Line Format | config-from-node=# |
|---------------------|--------------------|
| Type                | Numeric            |
| Default Value       | none               |

| Minimum Value | 1  |
|---------------|----|
| Maximum Value | 48 |

Obtain the cluster's configuration data from the data node that has this ID.

If the node having this ID is not a data node, [ndb\\_config](#page-10-0) fails with an error. (To obtain configuration data from the management node instead, simply omit this option.)

## <span id="page-14-0"></span>• --connections

| Command-Line Format | connections |
|---------------------|-------------|
|---------------------|-------------|

Tells [ndb\\_config](#page-10-0) to print CONNECTIONS information only—that is, information about parameters found in the [tcp], [tcp default], [shm], or [shm default] sections of the cluster configuration file (see Section 21.4.3.10, "NDB Cluster TCP/IP Connections", and Section 21.4.3.12, "NDB Cluster Shared Memory Connections", for more information).

This option is mutually exclusive with [--nodes](#page-17-0) and [--system](#page-18-0); only one of these 3 options can be used.

# <span id="page-14-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

# <span id="page-14-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

## <span id="page-14-3"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-16-2).

# <span id="page-14-4"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|

Write core file on error; used in debugging.

# <span id="page-14-5"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-15-0"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-15-1"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-15-2"></span>• --diff-default

| Command-Line Format | diff-default |
|---------------------|--------------|
|                     |              |

Print only configuration parameters that have non-default values.

<span id="page-15-3"></span>• --fields=delimiter, -f delimiter

| Command-Line Format | fields=string |
|---------------------|---------------|
| Type                | String        |
| Default Value       |               |

Specifies a delimiter string used to separate the fields in the result. The default is , (the comma character).

![](_page_15_Picture_15.jpeg)

## **Note**

If the delimiter contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

<span id="page-15-4"></span>• --help

Display help text and exit.

<span id="page-15-5"></span>• --host=hostname

| Command-Line Format | host=name |
|---------------------|-----------|
| Type                | String    |
| Default Value       |           |

Specifies the host name of the node for which configuration information is to be obtained.

![](_page_16_Picture_1.jpeg)

### **Note**

While the hostname localhost usually resolves to the IP address 127.0.0.1, this may not necessarily be true for all operating platforms and configurations. This means that it is possible, when localhost is used in config.ini, for [ndb\\_config --host=localhost](#page-10-0) to fail if [ndb\\_config](#page-10-0) is run on a different host where localhost resolves to a different address (for example, on some versions of SUSE Linux, this is 127.0.0.2). In general, for best results, you should use numeric IP addresses for all NDB Cluster configuration values relating to hosts, or verify that all NDB Cluster hosts handle localhost in the same fashion.

## <span id="page-16-1"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-16-0"></span>• --mycnf

Read configuration data from the my.cnf file.

<span id="page-16-2"></span>• --ndb-connectstring=connection\_string, -c connection\_string

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
|                     |                                 |

Specifies the connection string to use in connecting to the management server. The format for the connection string is the same as described in Section 21.4.3.3, "NDB Cluster Connection Strings", and defaults to localhost:1186.

<span id="page-16-3"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-16-2).

<span id="page-16-4"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-16-2).

<span id="page-16-5"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-17-1"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-17-2"></span>• --nodeid=node\_id

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Specify the node ID of the node for which configuration information is to be obtained. Formerly, - id could be used as a synonym for this option; in NDB 7.5 and later, the only form accepted is - nodeid.

<span id="page-17-0"></span>• --nodes

Tells [ndb\\_config](#page-10-0) to print information relating only to parameters defined in an [ndbd] or [ndbd default] section of the cluster configuration file (see Section 21.4.3.6, "Defining NDB Cluster Data Nodes").

This option is mutually exclusive with [--connections](#page-14-0) and [--system](#page-18-0); only one of these 3 options can be used.

<span id="page-17-3"></span>• --query=query-options, -q query-options

| Command-Line Format | query=string |
|---------------------|--------------|
| Type                | String       |
| Default Value       |              |

This is a comma-delimited list of query options—that is, a list of one or more node attributes to be returned. These include nodeid (node ID), type (node type—that is, ndbd, mysqld, or ndb\_mgmd), and any configuration parameters whose values are to be obtained.

For example, --query=nodeid,type,datamemory,datadir returns the node ID, node type, DataMemory, and DataDir for each node.

Formerly, id was accepted as a synonym for nodeid, but has been removed in NDB 7.5 and later.

![](_page_17_Picture_17.jpeg)

# **Note**

If a given parameter is not applicable to a certain type of node, than an empty string is returned for the corresponding value. See the examples later in this section for more information.

• --query-all, -a

<span id="page-17-4"></span>

|      | Command-Line Format | query-all |
|------|---------------------|-----------|
| 3390 | Type                | String    |

| Default Value |  |
|---------------|--|
|---------------|--|

Returns a comma-delimited list of all query options (node attributes; note that this list is a single string.

This option was introduced in NDB 7.5.7 (Bug #60095, Bug #11766869).

<span id="page-18-1"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-18-2"></span>• --rows=separator, -r separator

| Command-Line Format | rows=string |
|---------------------|-------------|
| Type                | String      |
| Default Value       |             |

Specifies a separator string used to separate the rows in the result. The default is a space character.

![](_page_18_Picture_10.jpeg)

#### **Note**

If the separator contains spaces or escapes (such as \n for the linefeed character), then it must be quoted.

<span id="page-18-0"></span>• --system

| Command-Line Format | system |
|---------------------|--------|
|---------------------|--------|

Tells [ndb\\_config](#page-10-0) to print SYSTEM information only. This consists of system variables that cannot be changed at run time; thus, there is no corresponding section of the cluster configuration file for them. They can be seen (prefixed with \*\*\*\*\*\* SYSTEM \*\*\*\*\*\*) in the output of [ndb\\_config](#page-10-0) [-](#page-13-2) [configinfo](#page-13-2).

This option is mutually exclusive with [--nodes](#page-17-0) and [--connections](#page-14-0); only one of these 3 options can be used.

<span id="page-18-3"></span>• --type=node\_type

| Command-Line Format | type=name   |
|---------------------|-------------|
| Type                | Enumeration |
| Default Value       | [none]      |
| Valid Values        | ndbd        |
|                     | mysqld      |
|                     | ndb_mgmd    |

Filters results so that only configuration values applying to nodes of the specified node\_type (ndbd, mysqld, or ndb\_mgmd) are returned.

<span id="page-18-4"></span>• --usage, --help, or -?

| Command-Line Format | help |
|---------------------|------|

Causes [ndb\\_config](#page-10-0) to print a list of available options, and then exit. Synonym for [--help](#page-15-4).

<span id="page-19-1"></span>• --version, -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Causes [ndb\\_config](#page-10-0) to print a version information string, and then exit.

<span id="page-19-0"></span>• --configinfo --xml

```
Command-Line Format --configinfo --xml
```

Cause [ndb\\_config](#page-10-0) [--configinfo](#page-13-2) to provide output as XML by adding this option. A portion of such output is shown in this example:

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

![](_page_19_Picture_8.jpeg)

# **Note**

Normally, the XML output produced by [ndb\\_config](#page-10-0) --configinfo --xml is formatted using one line per element; we have added extra whitespace in the previous example, as well as the next one, for reasons of legibility. This should not make any difference to applications using this output, since most XML processors either ignore nonessential whitespace as a matter of course, or can be instructed to do so.

The XML output also indicates when changing a given parameter requires that data nodes be restarted using the --initial option. This is shown by the presence of an initial="true" attribute in the corresponding <param> element. In addition, the restart type (system or node) is also shown; if a given parameter requires a system restart, this is indicated by the presence of a restart="system" attribute in the corresponding <param> element. For example, changing the value set for the Diskless parameter requires a system initial restart, as shown here (with the restart and initial attributes highlighted for visibility):

```
<param name="Diskless" comment="Run wo/ disk" type="bool" default="false"
```

```
 restart="system" initial="true"/>
```

Currently, no initial attribute is included in the XML output for <param> elements corresponding to parameters which do not require initial restarts; in other words, initial="false" is the default, and the value false should be assumed if the attribute is not present. Similarly, the default restart type is node (that is, an online or "rolling" restart of the cluster), but the restart attribute is included only if the restart type is system (meaning that all cluster nodes must be shut down at the same time, then restarted).

Deprecated parameters are indicated in the XML output by the deprecated attribute, as shown here:

```
<param name="NoOfDiskPagesToDiskAfterRestartACC" comment="DiskCheckpointSpeed"
 type="unsigned" default="20" min="1" max="4294967039" deprecated="true"/>
```

In such cases, the comment refers to one or more parameters that supersede the deprecated parameter. Similarly to initial, the deprecated attribute is indicated only when the parameter is deprecated, with deprecated="true", and does not appear at all for parameters which are not deprecated. (Bug #21127135)

Beginning with NDB 7.5.0, parameters that are required are indicated with mandatory="true", as shown here:

```
<param name="NodeId"
 comment="Number identifying application node (mysqld(API))"
 type="unsigned" mandatory="true" min="1" max="255"/>
```

In much the same way that the initial or deprecated attribute is displayed only for a parameter that requires an intial restart or that is deprecated, the mandatory attribute is included only if the given parameter is actually required.

![](_page_20_Picture_9.jpeg)

## **Important**

The --xml option can be used only with the --configinfo option. Using --xml without --configinfo fails with an error.

Unlike the options used with this program to obtain current configuration data, --configinfo and --xml use information obtained from the NDB Cluster sources when [ndb\\_config](#page-10-0) was compiled. For this reason, no connection to a running NDB Cluster or access to a config.ini or my.cnf file is required for these two options.

Combining other [ndb\\_config](#page-10-0) options (such as [--query](#page-17-3) or [--type](#page-18-3)) with --configinfo (with or without the --xml option is not supported. Currently, if you attempt to do so, the usual result is that all other options besides --configinfo or --xml are simply ignored. However, this behavior is not guaranteed and is subject to change at any time. In addition, since [ndb\\_config](#page-10-0), when used with the --configinfo option, does not access the NDB Cluster or read any files, trying to specify additional options such as --ndb-connectstring or --config-file with --configinfo serves no purpose.

# **Examples**

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

In this example, we used the [--fields](#page-15-3) options to separate the ID and type of each node with a colon character (:), and the [--rows](#page-18-2) options to place the values for each node on a new line in the output.

2. To produce a connection string that can be used by data, SQL, and API nodes to connect to the management server:

```
$> ./ndb_config --config-file=usr/local/mysql/cluster-data/config.ini \
--query=hostname,portnumber --fields=: --rows=, --type=ndb_mgmd
198.51.100.179:1186
```

3. This invocation of [ndb\\_config](#page-10-0) checks only data nodes (using the [--type](#page-18-3) option), and shows the values for each node's ID and host name, as well as the values set for its DataMemory and DataDir parameters:

```
$> ./ndb_config --type=ndbd --query=nodeid,host,datamemory,datadir -f ' : ' -r '\n'
1 : 198.51.100.193 : 83886080 : /usr/local/mysql/cluster-data
2 : 198.51.100.112 : 83886080 : /usr/local/mysql/cluster-data
3 : 198.51.100.176 : 83886080 : /usr/local/mysql/cluster-data
4 : 198.51.100.119 : 83886080 : /usr/local/mysql/cluster-data
```

In this example, we used the short options -f and -r for setting the field delimiter and row separator, respectively, as well as the short option -q to pass a list of parameters to be obtained.

4. To exclude results from any host except one in particular, use the [--host](#page-15-5) option:

```
$> ./ndb_config --host=198.51.100.176 -f : -r '\n' -q id,type
3:ndbd
5:ndb_mgmd
```

In this example, we also used the short form -q to determine the attributes to be queried.

Similarly, you can limit results to a node with a specific ID using the [--nodeid](#page-17-2) option.