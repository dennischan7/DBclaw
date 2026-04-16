---
source: MySQL 5.7 Reference
title: 00_Overview
---

The following two sections provide information about restoring a native NDB backup to a different version of NDB Cluster from the version in which the backup was taken.

In addition, you should consult Section 21.3.7, "Upgrading and Downgrading NDB Cluster", for other issues you may encounter when attempting to restore an NDB backup to a cluster running a different version of the NDB software.

It is also advisable to review [What is New in NDB Cluster 8.0,](https://dev.mysql.com/doc/refman/8.0/en/mysql-cluster-what-is-new.md#mysql-cluster-what-is-new-8-0) as well as Section 2.10.3, "Changes in MySQL 5.7", for other changes between NDB 8.0 and previous versions of NDB Cluster that may be relevant to your particular circumstances.

# **Restoring an NDB backup to a previous version of NDB Cluster**

You may encounter issues when restoring a backup taken from a later version of NDB Cluster to a previous one, due to the use of features which do not exist in the earlier version. Some of these issues are listed here:

- Tables created in NDB 8.0 by default use the utf8mb4\_ai\_ci character set, which is not available in NDB 7.6 and earlier, and so cannot be read by an [ndb\\_restore](#page-81-3) binary from one of these earlier versions. In such cases, it is necessary to alter any tables using utf8mb4\_ai\_ci so that they use a character set supported in the older version prior to performing the backup.
- Due to changes in how the MySQL Server and NDB handle table metadata, tables created or altered using the included MySQL server binary from NDB 8.0.14 or later cannot be restored using [ndb\\_restore](#page-81-3) to an earlier version of NDB Cluster. Such tables use .sdi files which are not understood by older versions of mysqld.

A backup taken in NDB 8.0.14 or later of tables which were created in NDB 8.0.13 or earlier, and which have not been altered since upgrading to NDB 8.0.14 or later, should be restorable to older versions of NDB Cluster.

Since it is possible to restore metadata and table data separately, you can in such cases restore the table schemas from a dump made using mysqldump, or by executing the necessary CREATE TABLE statements manually, then import only the table data using [ndb\\_restore](#page-81-3) with the [-](#page-101-0) [restore-data](#page-101-0) option.

- Encrypted backups created in NDB 8.0.22 and later cannot be restored using [ndb\\_restore](#page-81-3) from NDB 8.0.21 or earlier.
- The [NDB\\_STORED\\_USER](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.md#priv_ndb-stored-user) privilege is not supported prior to NDB 8.0.18.
- NDB Cluster 8.0.18 and later supports up to 144 data nodes, while earlier versions support a maximum of only 48 data nodes. See [Restoring to Fewer Nodes Than the Original](#page-106-1), for information with situations in which this incompatibility causes an issue.

# **Restoring an NDB backup to a later version of NDB Cluster**

In general, it should be possible to restore a backup created using the ndb\_mgm client [START](#page-192-0) [BACKUP](#page-192-0) command in an older version of NDB to a newer version, provided that you use the [ndb\\_restore](#page-81-3) binary that comes with the newer version. (It may be possible to use the older version of [ndb\\_restore](#page-81-3), but this is not recommended.) Additional potential issues are listed here:

• When restoring the metadata from a backup ([--restore-meta](#page-101-2) option), [ndb\\_restore](#page-81-3) normally attempts to reproduce the captured table schema exactly as it was when the backup was taken.

Tables created in versions of NDB prior to 8.0.14 use .frm files for their metadata. These files can be read by the mysqld in NDB 8.0.14 and later, which can use the information contained therein to create the .sdi files used by the MySQL data dictionary in later versions.

- When restoring an older backup to a newer version of NDB, it may not be possible to take advantage of newer features such as hashmap partitioning, greater number of hashmap buckets, read backup, and different partitioning layouts. For this reason, it may be preferable to restore older schemas using mysqldump and the mysql client, which allows NDB to make use of the new schema features.
- Tables using the old temporal types which did not support fractional seconds (used prior to MySQL 5.6.4 and NDB 7.3.31) cannot be restored to NDB 8.0 using [ndb\\_restore](#page-81-3). You can check such tables using CHECK TABLE, and then upgrade them to the newer temporal column format, if necessary, using REPAIR TABLE in the mysql client; this must be done prior to taking the backup. See [Preparing Your Installation for Upgrade,](https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.md) for more information.

You also restore such tables using a dump created with mysqldump.

• Distributed grant tables created in NDB 7.6 and earlier are not supported in NDB 8.0. Such tables can be restored to an NDB 8.0 cluster, but they have no effect on access control.

# <span id="page-106-0"></span>**21.5.24.2 Restoring to a different number of data nodes**

It is possible to restore from an NDB backup to a cluster having a different number of data nodes than the original from which the backup was taken. The following two sections discuss, respectively, the cases where the target cluster has a lesser or greater number of data nodes than the source of the backup.

# <span id="page-106-1"></span>**Restoring to Fewer Nodes Than the Original**

You can restore to a cluster having fewer data nodes than the original provided that the larger number of nodes is an even multiple of the smaller number. In the following example, we use a backup taken on a cluster having four data nodes to a cluster having two data nodes.

1. The management server for the original cluster is on host host10. The original cluster has four data nodes, with the node IDs and host names shown in the following extract from the management server's config.ini file:

```
[ndbd]
NodeId=2
HostName=host2
[ndbd]
NodeId=4
HostName=host4
[ndbd]
NodeId=6
HostName=host6
[ndbd]
NodeId=8
HostName=host8
```

We assume that each data node was originally started with ndbmtd --ndbconnectstring=host10 or the equivalent.

- 2. Perform a backup in the normal manner. See [Section 21.6.8.2, "Using The NDB Cluster](#page-192-0) [Management Client to Create a Backup"](#page-192-0), for information about how to do this.
- 3. The files created by the backup on each data node are listed here, where N is the node ID and B is the backup ID.

- BACKUP-B-0.N.Data
- BACKUP-B.N.ctl
- BACKUP-B.N.log

These files are found under BackupDataDir/BACKUP/BACKUP-B, on each data node. For the rest of this example, we assume that the backup ID is 1.

Have all of these files available for later copying to the new data nodes (where they can be accessed on the data node's local file system by [ndb\\_restore](#page-81-3)). It is simplest to copy them all to a single location; we assume that this is what you have done.

4. The management server for the target cluster is on host host20, and the target has two data nodes, with the node IDs and host names shown, from the management server config.ini file on host20:

```
[ndbd]
NodeId=3
hostname=host3
[ndbd]
NodeId=5
hostname=host5
```

Each of the data node processes on host3 and host5 should be started with ndbmtd -c host20 --initial or the equivalent, so that the new (target) cluster starts with clean data node file systems.

- 5. Copy two different sets of two backup files to each of the target data nodes. For this example, copy the backup files from nodes 2 and 4 from the original cluster to node 3 in the target cluster. These files are listed here:
  - BACKUP-1-0.2.Data
  - BACKUP-1.2.ctl
  - BACKUP-1.2.log
  - BACKUP-1-0.4.Data
  - BACKUP-1.4.ctl
  - BACKUP-1.4.log

Then copy the backup files from nodes 6 and 8 to node 5; these files are shown in the following list:

- BACKUP-1-0.6.Data
- BACKUP-1.6.ctl
- BACKUP-1.6.log
- BACKUP-1-0.8.Data
- BACKUP-1.8.ctl
- BACKUP-1.8.log

For the remainder of this example, we assume that the respective backup files have been saved to the directory /BACKUP-1 on each of nodes 3 and 5.

6. On each of the two target data nodes, you must restore from both sets of backups. First, restore the backups from nodes 2 and 4 to node 3 by invoking [ndb\\_restore](#page-81-3) on host3 as shown here:

```
$> ndb_restore -c host20 --nodeid=2 --backupid=1 --restore-data --backup-path=/BACKUP-1
$> ndb_restore -c host20 --nodeid=4 --backupid=1 --restore-data --backup-path=/BACKUP-1
```

Then restore the backups from nodes 6 and 8 to node 5 by invoking [ndb\\_restore](#page-81-3) on host5, like this:

```
$> ndb_restore -c host20 --nodeid=6 --backupid=1 --restore-data --backup-path=/BACKUP-1
$> ndb_restore -c host20 --nodeid=8 --backupid=1 --restore-data --backup-path=/BACKUP-1
```

# **Restoring to More Nodes Than the Original**

The node ID specified for a given [ndb\\_restore](#page-81-3) command is that of the node in the original backup and not that of the data node to restore it to. When performing a backup using the method described in this section, [ndb\\_restore](#page-81-3) connects to the management server and obtains a list of data nodes in the cluster the backup is being restored to. The restored data is distributed accordingly, so that the number of nodes in the target cluster does not need to be to be known or calculated when performing the backup.

![](_page_108_Picture_7.jpeg)

#### **Note**

When changing the total number of LCP threads or LQH threads per node group, you should recreate the schema from backup created using mysqldump.

1. Create the backup of the data. You can do this by invoking the ndb\_mgm client START BACKUP command from the system shell, like this:

```
$> ndb_mgm -e "START BACKUP 1"
```

This assumes that the desired backup ID is 1.

2. Create a backup of the schema. In NDB 7.5.2 and later, this step is necessary only if the total number of LCP threads or LQH threads per node group is changed.

```
$> mysqldump --no-data --routines --events --triggers --databases > myschema.sql
```

![](_page_108_Picture_15.jpeg)

## **Important**

Once you have created the NDB native backup using ndb\_mgm, you must not make any schema changes before creating the backup of the schema, if you do so.

- 3. Copy the backup directory to the new cluster. For example if the backup you want to restore has ID 1 and BackupDataDir = /backups/node\_nodeid, then the path to the backup on this node is / backups/node\_1/BACKUP/BACKUP-1. Inside this directory there are three files, listed here:
  - BACKUP-1-0.1.Data
  - BACKUP-1.1.ctl
  - BACKUP-1.1.log

You should copy the entire directory to the new node.

If you needed to create a schema file, copy this to a location on an SQL node where it can be read by mysqld.

There is no requirement for the backup to be restored from a specific node or nodes.

To restore from the backup just created, perform the following steps:

- 1. Restore the schema.
  - If you created a separate schema backup file using mysqldump, import this file using the mysql client, similar to what is shown here:

```
$> mysql < myschema.sql
```

When importing the schema file, you may need to specify the --user and --password options (and possibly others) in addition to what is shown, in order for the mysql client to be able to connect to the MySQL server.

• If you did not need to create a schema file, you can re-create the schema using [ndb\\_restore](#page-81-3) [--restore-meta](#page-101-2) (short form -m), similar to what is shown here:

```
$> ndb_restore --nodeid=1 --backupid=1 --restore-meta --backup-path=/backups/node_1/BACKUP/BACKUP-1
```

[ndb\\_restore](#page-81-3) must be able to contact the management server; add the [--ndb](#page-95-2)[connectstring](#page-95-2) option if and as needed to make this possible.

2. Restore the data. This needs to be done once for each data node in the original cluster, each time using that data node's node ID. Assuming that there were 4 data nodes originally, the set of commands required would look something like this:

```
ndb_restore --nodeid=1 --backupid=1 --restore-data --backup-path=/backups/node_1/BACKUP/BACKUP-1 --disable-indexes
ndb_restore --nodeid=2 --backupid=1 --restore-data --backup-path=/backups/node_2/BACKUP/BACKUP-1 --disable-indexes
ndb_restore --nodeid=3 --backupid=1 --restore-data --backup-path=/backups/node_3/BACKUP/BACKUP-1 --disable-indexes
ndb_restore --nodeid=4 --backupid=1 --restore-data --backup-path=/backups/node_4/BACKUP/BACKUP-1 --disable-indexes
```

These can be run in parallel.

Be sure to add the [--ndb-connectstring](#page-95-2) option as needed.

3. Rebuild the indexes. These were disabled by the [--disable-indexes](#page-89-4) option used in the commands just shown. Recreating the indexes avoids errors due to the restore not being consistent at all points. Rebuilding the indexes can also improve performance in some cases. To rebuild the indexes, execute the following command once, on a single node:

```
$> ndb_restore --nodeid=1 --backupid=1 --backup-path=/backups/node_1/BACKUP/BACKUP-1 --rebuild-indexes
```

As mentioned previously, you may need to add the [--ndb-connectstring](#page-95-2) option, so that [ndb\\_restore](#page-81-3) can contact the management server.

# <span id="page-109-0"></span>**21.5.25 ndb\_select\_all — Print Rows from an NDB Table**

[ndb\\_select\\_all](#page-109-0) prints all rows from an NDB table to stdout.

# **Usage**

```
ndb_select_all -c connection_string tbl_name -d db_name [> file_name]
```

Options that can be used with [ndb\\_select\\_all](#page-109-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.41 Command-line options used with the program ndb\_select\_all**

| Format                     | Description                                             | Added, Deprecated, or<br>Removed                      |
|----------------------------|---------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path | Directory containing character<br>sets                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#          | Number of times to retry<br>connection before giving up | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                  | Description                                                                                                  | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retry-delay=#                   | Number of seconds to wait<br>between attempts to contact<br>management server                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string,    | Same asndb-connectstring                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                              |                                                       |
| core-file                               | Write core file on error; used in<br>debugging                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                          | Name of database in which table<br>is found                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                                 |                                                                                                              |                                                       |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                      | Read default options from given<br>file only                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| delimiter=char,                         | Set column delimiter                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -D char                                 |                                                                                                              |                                                       |
| descending,                             | Sort resultset in descending<br>order (requiresorder)                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -z<br>disk                              | Print disk references (useful<br>only for Disk Data tables having<br>unindexed columns)                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| gci                                     | Include GCI in output                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| gci64                                   | Include GCI and row epoch in<br>output                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| header[=value],                         | Print header (set to 0 FALSE to<br>disable headers in output)                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -h<br>lock=#,                           | Lock type                                                                                                    | (Supported in all NDB releases                        |
| -l #                                    |                                                                                                              | based on MySQL 5.7)                                   |
| login-path=path                         | Read given path from login file                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                   | Display help text and exit                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                      |                                                                                                              |                                                       |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.                                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                          | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -c connection_string            |                                                                                                                                               |                                                       |
| ndb-nodeid=#                    | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                     | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nodata                          | Do not print table column data                                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| order=index,                    | Sort resultset according to index<br>having this name                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -o index                        |                                                                                                                                               |                                                       |
| parallelism=#,                  | Degree of parallelism                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -p #                            |                                                                                                                                               |                                                       |
| print-defaults                  | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| rowid                           | Print row ID                                                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| tupscan,                        | Scan in tup order                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -t                              |                                                                                                                                               |                                                       |
| usage,                          | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                              |                                                                                                                                               |                                                       |
| useHexFormat,                   | Output numbers in hexadecimal<br>format                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -x                              |                                                                                                                                               |                                                       |
| version,                        | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                              |                                                                                                                                               |                                                       |

<span id="page-111-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

## Directory containing character sets.

<span id="page-111-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |

| Maximum Value | 12 |  |
|---------------|----|--|
|---------------|----|--|

Number of times to retry connection before giving up.

## <span id="page-112-0"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

## <span id="page-112-1"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-114-0).

# <span id="page-112-2"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-112-3"></span>• --database=dbname, -d dbname

Name of the database in which the table is found. The default value is TEST\_DB.

<span id="page-112-7"></span>• --descending, -z

Sorts the output in descending order. This option can be used only in conjunction with the -o ([-](#page-114-5) [order](#page-114-5)) option.

## <span id="page-112-4"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

# <span id="page-112-5"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

## <span id="page-112-6"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Also read groups with concat(group, suffix).

<span id="page-113-0"></span>• --delimiter=character, -D character

Causes the character to be used as a column delimiter. Only table data columns are separated by this delimiter.

The default delimiter is the tab character.

<span id="page-113-1"></span>• --disk

Adds a disk reference column to the output. The column is nonempty only for Disk Data tables having nonindexed columns.

<span id="page-113-2"></span>• --gci

Adds a GCI column to the output showing the global checkpoint at which each row was last updated. See Section 21.2, "NDB Cluster Overview", and [Section 21.6.3.2, "NDB Cluster Log Events"](#page-168-0), for more information about checkpoints.

<span id="page-113-3"></span>• --gci64

Adds a ROW\$GCI64 column to the output showing the global checkpoint at which each row was last updated, as well as the number of the epoch in which this update occurred.

<span id="page-113-7"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-113-5"></span>• --lock=lock\_type, -l lock\_type

Employs a lock when reading the table. Possible values for lock\_type are:

- 0: Read lock
- 1: Read lock with hold
- 2: Exclusive read lock

There is no default value for this option.

<span id="page-113-6"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-113-4"></span>• --header=FALSE

Excludes column headers from the output.

<span id="page-113-8"></span>• --nodata

Causes any table data to be omitted.

# <span id="page-114-0"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
|                     |                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-114-1"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-114-0).

<span id="page-114-2"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-114-0).

<span id="page-114-3"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-114-4"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|                     |             |

Do not read default options from any option file other than login file.

<span id="page-114-5"></span>• --order=index\_name, -o index\_name

Orders the output according to the index named index\_name.

![](_page_114_Picture_18.jpeg)

## **Note**

This is the name of an index, not of a column; the index must have been explicitly named when created.

<span id="page-114-6"></span>• parallelism=#, -p #

Specifies the degree of parallelism.

<span id="page-114-7"></span>• --print-defaults

|                     | 3487           |
|---------------------|----------------|
| Command-Line Format | print-defaults |

Print program argument list and exit.

<span id="page-115-0"></span>• --rowid

Adds a ROWID column providing information about the fragments in which rows are stored.

<span id="page-115-1"></span>• --tupscan, -t

Scan the table in the order of the tuples.

<span id="page-115-2"></span>• --usage

```
Command-Line Format --usage
```

Display help text and exit; same as [--help](#page-113-7).

<span id="page-115-3"></span>• --useHexFormat -x

Causes all numeric values to be displayed in hexadecimal format. This does not affect the output of numerals contained in strings or datetime values.

<span id="page-115-4"></span>• --version

```
Command-Line Format --version
```

Display version information and exit.

# **Sample Output**

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

Output from the equivalent invocation of [ndb\\_select\\_all](#page-109-0):

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
NDBT_ProgramExit: 0 - OK
```

All string values are enclosed by square brackets ([...]) in the output of [ndb\\_select\\_all](#page-109-0). For another example, consider the table created and populated as shown here:

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
```

```
INSERT INTO dogs VALUES
 ('', 'Lassie', 'collie'),
 ('', 'Scooby-Doo', 'Great Dane'),
 ('', 'Rin-Tin-Tin', 'Alsatian'),
 ('', 'Rosscoe', 'Mutt');
```

This demonstrates the use of several additional [ndb\\_select\\_all](#page-109-0) options:

```
$> ./ndb_select_all -d ctest1 dogs -o ix -z --gci --disk
GCI id name breed DISK_REF
834461 2 [Scooby-Doo] [Great Dane] [ m_file_no: 0 m_page: 98 m_page_idx: 0 ]
834878 4 [Rosscoe] [Mutt] [ m_file_no: 0 m_page: 98 m_page_idx: 16 ]
834463 3 [Rin-Tin-Tin] [Alsatian] [ m_file_no: 0 m_page: 34 m_page_idx: 0 ]
835657 1 [Lassie] [Collie] [ m_file_no: 0 m_page: 66 m_page_idx: 0 ]
4 rows returned
NDBT_ProgramExit: 0 - OK
```

# <span id="page-116-0"></span>**21.5.26 ndb\_select\_count — Print Row Counts for NDB Tables**

[ndb\\_select\\_count](#page-116-0) prints the number of rows in one or more NDB tables. With a single table, the result is equivalent to that obtained by using the MySQL statement SELECT COUNT(\*) FROM tbl\_name.

# **Usage**

```
ndb_select_count [-c connection_string] -ddb_name tbl_name[, tbl_name2[, ...]]
```

Options that can be used with [ndb\\_select\\_count](#page-116-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.42 Command-line options used with the program ndb\_select\_count**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                       | Name of database in which table<br>is found                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                              |                                                                               |                                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                   | Read default options from given<br>file only                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                | Display help text and exit                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                           | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -?                               |                                                                                                                                               |                                                       |
| lock=#,                          | Lock type                                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -l #                             |                                                                                                                                               |                                                       |
| login-path=path                  | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb                              | Set connect string for                                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string, | connecting to ndb_mgmd.                                                                                                                       | based on MySQL 5.7)                                   |
| -c connection_string             | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                  |                                                       |
| ndb-mgmd                         | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases                        |
| host=connection_string,          |                                                                                                                                               | based on MySQL 5.7)                                   |
| -c connection_string             |                                                                                                                                               |                                                       |
| ndb-nodeid=#                     | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection  | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                      | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| parallelism=#,                   | Degree of parallelism                                                                                                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -p #                             |                                                                                                                                               |                                                       |
| print-defaults                   | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,                           | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                               |                                                                                                                                               |                                                       |
| version,                         | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                               |                                                                                                                                               |                                                       |

## <span id="page-117-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

## <span id="page-117-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |

| Maximum Value | 12 |  |
|---------------|----|--|
|---------------|----|--|

Number of times to retry connection before giving up.

## <span id="page-118-0"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

# <span id="page-118-1"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-119-1).

## <span id="page-118-2"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

# <span id="page-118-4"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

# <span id="page-118-3"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

## <span id="page-118-5"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

# <span id="page-118-6"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read given path from login file.

<span id="page-119-0"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-119-1"></span>• --ndb-connectstring

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-119-2"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-119-1).

<span id="page-119-4"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-119-3"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-119-1).

<span id="page-119-5"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-119-6"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-119-7"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-119-0).

<span id="page-120-0"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

You can obtain row counts from multiple tables in the same database by listing the table names separated by spaces when invoking this command, as shown under **Sample Output**.

# **Sample Output**

```
$> ./ndb_select_count -c localhost -d ctest1 fish dogs
6 records in table fish
4 records in table dogs
NDBT_ProgramExit: 0 - OK
```

# <span id="page-120-1"></span>**21.5.27 ndb\_show\_tables — Display List of NDB Tables**

[ndb\\_show\\_tables](#page-120-1) displays a list of all NDB database objects in the cluster. By default, this includes not only both user-created tables and NDB system tables, but NDB-specific indexes, internal triggers, and NDB Cluster Disk Data objects as well.

Options that can be used with [ndb\\_show\\_tables](#page-120-1) are shown in the following table. Additional descriptions follow the table.

**Table 21.43 Command-line options used with the program ndb\_show\_tables**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                               |                                                       |
| core-file                            | Write core file on error; used in<br>debugging                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                       | Specifies database in which table<br>is found; database name must be          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                              | followed by table name                                                        |                                                       |
| defaults-extra<br>file=path          | Read given file after global files<br>are read                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                   | Read default options from given<br>file only                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string      | Also read groups with<br>concat(group, suffix)                                | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| login-path=path                         | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| loops=#,                                | Number of times to repeat output                                                                                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -l #<br>help,                           | Display help text and exit                                                                                                                    | (Supported in all NDB releases                        |
| -?                                      |                                                                                                                                               | based on MySQL 5.7)                                   |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                  |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| parsable,<br>-p                         | Return output suitable for<br>MySQL LOAD DATA statement                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| show-temp-status                        | Show table temporary flag                                                                                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| type=#,                                 | Limit output to objects of this<br>type                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -t #                                    |                                                                                                                                               |                                                       |
| unqualified,                            | Do not qualify table names                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -u<br>usage,                            | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>version,                          | Display version information and                                                                                                               | (Supported in all NDB releases                        |
|                                         | exit                                                                                                                                          | based on MySQL 5.7)                                   |
| -V                                      |                                                                                                                                               |                                                       |

# <span id="page-122-0"></span>**Usage**

ndb\_show\_tables [-c connection\_string]

• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-122-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-122-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-122-3"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-123-5).

<span id="page-122-4"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-122-5"></span>• --database, -d

Specifies the name of the database in which the desired table is found. If this option is given, the name of a table must follow the database name.

If this option has not been specified, and no tables are found in the TEST\_DB database, [ndb\\_show\\_tables](#page-120-1) issues a warning.

<span id="page-122-6"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read given file after global files are read.

<span id="page-123-0"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-123-1"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-123-4"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-123-2"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-123-3"></span>• --loops, -l

Specifies the number of times the utility should execute. This is 1 when this option is not specified, but if you do use the option, you must supply an integer argument for it.

<span id="page-123-5"></span>• --ndb-connectstring

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-123-6"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-123-5).

# <span id="page-124-0"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-123-5).

<span id="page-124-1"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-124-2"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-124-3"></span>• --parsable, -p

Using this option causes the output to be in a format suitable for use with LOAD DATA.

<span id="page-124-4"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-124-5"></span>• --show-temp-status

If specified, this causes temporary tables to be displayed.

<span id="page-124-6"></span>• --type, -t

Can be used to restrict the output to one type of object, specified by an integer type code as shown here:

- 1: System table
- 2: User-created table
- 3: Unique hash index

Any other value causes all NDB database objects to be listed (the default).

<span id="page-124-7"></span>• --unqualified, -u

If specified, this causes unqualified object names to be displayed.

<span id="page-124-8"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-123-4).

<span id="page-124-9"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

![](_page_125_Picture_2.jpeg)

## **Note**

Only user-created NDB Cluster tables may be accessed from MySQL; system tables such as SYSTAB\_0 are not visible to mysqld. However, you can examine the contents of system tables using NDB API applications such as [ndb\\_select\\_all](#page-109-0) (see [Section 21.5.25, "ndb\\_select\\_all — Print Rows from an](#page-109-0) [NDB Table"](#page-109-0)).

Prior to NDB 7.5.18 and 7.6.14, this program printed NDBT\_ProgramExit - status upon completion of its run, due to an unnecessary dependency on the NDBT testing library. This dependency is has now been removed, eliminating the extraneous output.

# <span id="page-125-0"></span>**21.5.28 ndb\_size.pl — NDBCLUSTER Size Requirement Estimator**

This is a Perl script that can be used to estimate the amount of space that would be required by a MySQL database if it were converted to use the NDBCLUSTER storage engine. Unlike the other utilities discussed in this section, it does not require access to an NDB Cluster (in fact, there is no reason for it to do so). However, it does need to access the MySQL server on which the database to be tested resides.

# **Requirements**

- A running MySQL server. The server instance does not have to provide support for NDB Cluster.
- A working installation of Perl.
- The DBI module, which can be obtained from CPAN if it is not already part of your Perl installation. (Many Linux and other operating system distributions provide their own packages for this library.)
- A MySQL user account having the necessary privileges. If you do not wish to use an existing account, then creating one using GRANT USAGE ON db\_name.\*—where db\_name is the name of the database to be examined—is sufficient for this purpose.

ndb\_size.pl can also be found in the MySQL sources in storage/ndb/tools.

Options that can be used with [ndb\\_size.pl](#page-125-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.44 Command-line options used with the program ndb\_size.pl**

| Format            | Description                                                                                                           | Added, Deprecated, or<br>Removed                      |
|-------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| database=string   | Database or databases to<br>examine; a comma-delimited list;<br>default is ALL (use all databases<br>found on server) | (Supported in all NDB releases<br>based on MySQL 5.7) |
| hostname=string   | Specify host and optional port in<br>host[:port] format                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| socket=path       | Specify socket to connect to                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| user=string       | Specify MySQL user name                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| password=password | Specify MySQL user password                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| format=string     | Set output format (text or HTML)                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                 | Description                                                               | Added, Deprecated, or<br>Removed                      |
|------------------------|---------------------------------------------------------------------------|-------------------------------------------------------|
| excludetables=list     | Skip any tables in comma<br>separated list                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| excludedbs=list        | Skip any databases in comma<br>separated list                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| savequeries=path       | Saves all queries on database<br>into file specified                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| loadqueries=path       | Loads all queries from file<br>specified; does not connect to<br>database | (Supported in all NDB releases<br>based on MySQL 5.7) |
| real_table_name=string | Designates table to handle<br>unique index size calculations              | (Supported in all NDB releases<br>based on MySQL 5.7) |

# **Usage**

```
perl ndb_size.pl [--database={db_name|ALL}] [--hostname=host[:port]] [--socket=socket] \
 [--user=user] [--password=password] \
 [--help|-h] [--format={html|text}] \
 [--loadqueries=file_name] [--savequeries=file_name]
```

<span id="page-126-0"></span>By default, this utility attempts to analyze all databases on the server. You can specify a single database using the --database option; the default behavior can be made explicit by using ALL for the name of the database. You can also exclude one or more databases by using the --excludedbs option with a comma-separated list of the names of the databases to be skipped. Similarly, you can cause specific tables to be skipped by listing their names, separated by commas, following the optional --excludetables option. A host name can be specified using --hostname; the default is localhost. You can specify a port in addition to the host using host:port format for the value of - hostname. The default port number is 3306. If necessary, you can also specify a socket; the default is /var/lib/mysql.sock. A MySQL user name and password can be specified the corresponding options shown. It also possible to control the format of the output using the --format option; this can take either of the values html or text, with text being the default. An example of the text output is shown here:

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
```

| Indexes IM/Row                       | 33                                      | 16  | 16   |  |
|--------------------------------------|-----------------------------------------|-----|------|--|
|                                      |                                         |     |      |  |
| Summary (for THIS table):            |                                         |     |      |  |
|                                      | 4.1                                     | 5.0 | 5.1  |  |
| Fixed Overhead DM/Row                | 12                                      | 12  | 16   |  |
| NULL Bytes/Row                       | 4                                       | 4   | 4    |  |
| DataMemory/Row                       | 96                                      | 96  | 48   |  |
|                                      | (Includes overhead, bitmap and indexes) |     |      |  |
| Varsize Overhead DM/Row              | 0                                       | 0   | 8    |  |
| Varsize NULL Bytes/Row               | 0                                       | 0   | 4    |  |
| Avg Varside DM/Row                   | 0                                       | 0   | 16   |  |
| No. Rows                             | 0                                       | 0   | 0    |  |
| Rows/32kb DM Page                    | 340                                     | 340 | 680  |  |
| Fixedsize DataMemory (KB)            | 0                                       | 0   | 0    |  |
|                                      |                                         |     |      |  |
| Rows/32kb Varsize DM Page            | 0                                       | 0   | 2040 |  |
| Varsize DataMemory (KB)              | 0                                       | 0   | 0    |  |
| Rows/8kb IM Page                     | 248                                     | 512 | 512  |  |
| IndexMemory (KB)                     | 0                                       | 0   | 0    |  |
| Parameter Minimum Requirements       |                                         |     |      |  |
| <br>* indicates greater than default |                                         |     |      |  |
| Parameter                            | Default                                 | 4.1 | 5.0  |  |
| DataMemory (KB)                      | 81920                                   | 0   | 0    |  |
| NoOfOrderedIndexes                   | 128                                     | 1   | 1    |  |
| NoOfTables                           | 128                                     | 1   | 1    |  |
| IndexMemory (KB)                     | 18432                                   | 0   | 0    |  |
| NoOfUniqueHashIndexes                | 64                                      | 0   | 0    |  |
| NoOfAttributes                       | 1000                                    | 3   | 3    |  |
| NoOfTriggers                         | 768                                     | 5   | 5    |  |
|                                      |                                         |     |      |  |

<span id="page-127-1"></span>For debugging purposes, the Perl arrays containing the queries run by this script can be read from the file specified using can be saved to a file using --savequeries; a file containing such arrays to be read during script execution can be specified using --loadqueries. Neither of these options has a default value.

<span id="page-127-0"></span>To produce output in HTML format, use the --format option and redirect the output to a file, as shown here:

```
$> ndb_size.pl --database=test --socket=/tmp/mysql.sock --format=html > ndb_size.html
```

(Without the redirection, the output is sent to stdout.)

The output from this script includes the following information:

- Minimum values for the DataMemory, IndexMemory, MaxNoOfTables, MaxNoOfAttributes, MaxNoOfOrderedIndexes, and MaxNoOfTriggers configuration parameters required to accommodate the tables analyzed.
- Memory requirements for all of the tables, attributes, ordered indexes, and unique hash indexes defined in the database.
- The IndexMemory and DataMemory required per table and table row.

# <span id="page-127-2"></span>**21.5.29 ndb\_top — View CPU usage information for NDB threads**

[ndb\\_top](#page-127-2) displays running information in the terminal about CPU usage by NDB threads on an NDB Cluster data node. Each thread is represented by two rows in the output, the first showing system statistics, the second showing the measured statistics for the thread.

[ndb\\_top](#page-127-2) is available in MySQL NDB Cluster 7.6 (and later).

# **Usage**

```
ndb_top [-h hostname] [-t port] [-u user] [-p pass] [-n node_id]
```

[ndb\\_top](#page-127-2) connects to a MySQL Server running as an SQL node of the cluster. By default, it attempts to connect to a mysqld running on localhost and port 3306, as the MySQL root user with no password specified. You can override the default host and port using, respectively, [--host](#page-130-0) (-h) and [--port](#page-131-0) (-t). To specify a MySQL user and password, use the [--user](#page-132-0) (-u) and [--passwd](#page-131-1) (-p) options. This user must be able to read tables in the ndbinfo database ([ndb\\_top](#page-127-2) uses information from ndbinfo.cpustat and related tables).

For more information about MySQL user accounts and passwords, see Section 6.2, "Access Control and Account Management".

Output is available as plain text or an ASCII graph; you can specify this using the [--text](#page-132-1) (-x) and [-](#page-130-1) [graph](#page-130-1) (-g) options, respectively. These two display modes provide the same information; they can be used concurrently. At least one display mode must be in use.

Color display of the graph is supported and enabled by default ([--color](#page-130-2) or -c option). With color support enabled, the graph display shows OS user time in blue, OS system time in green, and idle time as blank. For measured load, blue is used for execution time, yellow for send time, red for time spent in send buffer full waits, and blank spaces for idle time. The percentage shown in the graph display is the sum of percentages for all threads which are not idle. Colors are not currently configurable; you can use grayscale instead by using --skip-color.

The sorted view ([--sort](#page-132-2), -r) is based on the maximum of the measured load and the load reported by the OS. Display of these can be enabled and disabled using the [--measured-load](#page-131-2) (-m) and [-](#page-131-3) [os-load](#page-131-3) (-o) options. Display of at least one of these loads must be enabled.

The program tries to obtain statistics from a data node having the node ID given by the [--node-id](#page-131-4) ( n) option; if unspecified, this is 1. [ndb\\_top](#page-127-2) cannot provide information about other types of nodes.

The view adjusts itself to the height and width of the terminal window; the minimum supported width is 76 characters.

Once started, [ndb\\_top](#page-127-2) runs continuously until forced to exit; you can quit the program using Ctrl-C. The display updates once per second; to set a different delay interval, use [--sleep-time](#page-132-3) (-s).

![](_page_128_Picture_11.jpeg)

## **Note**

[ndb\\_top](#page-127-2) is available on macOS, Linux, and Solaris. It is not currently supported on Windows platforms.

The following table includes all options that are specific to the NDB Cluster program [ndb\\_top](#page-127-2). Additional descriptions follow the table.

**Table 21.45 Command-line options used with the program ndb\_top**

| Format                          | Description                                               | Added, Deprecated, or<br>Removed                      |
|---------------------------------|-----------------------------------------------------------|-------------------------------------------------------|
| color,                          | Show ASCII graphs in color; use<br>skip-colors to disable | ADDED: NDB 7.6.3                                      |
| -c                              |                                                           |                                                       |
| defaults-extra<br>file=path     | Read given file after global files<br>are read            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path              | Read default options from given<br>file only              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string | Also read groups with<br>concat(group, suffix)            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| graph,                          | Display data using graphs; use<br>skip-graphs to disable  | ADDED: NDB 7.6.3                                      |

| Format                 | Description                                                                  | Added, Deprecated, or<br>Removed                      |
|------------------------|------------------------------------------------------------------------------|-------------------------------------------------------|
| -g                     |                                                                              |                                                       |
| help                   | Show program usage information ADDED: NDB 7.6.3                              |                                                       |
| host=string,           | Host name or IP address of<br>MySQL Server to connect to                     | ADDED: NDB 7.6.3                                      |
| -h string              |                                                                              |                                                       |
| login-path=path        | Read given path from login file                                              | (Supported in all NDB releases<br>based on MySQL 5.7) |
| measured-load,         | Show measured load by thread                                                 | ADDED: NDB 7.6.3                                      |
| -m                     |                                                                              |                                                       |
| no-defaults            | Do not read default options from<br>any option file other than login<br>file | (Supported in all NDB releases<br>based on MySQL 5.7) |
| node-id=#,             | Watch node having this node ID                                               | ADDED: NDB 7.6.3                                      |
| -n #                   |                                                                              |                                                       |
| os-load,               | Show load measured by<br>operating system                                    | ADDED: NDB 7.6.3                                      |
| -o<br>passwd=password, | Connect using this password                                                  | ADDED: NDB 7.6.3                                      |
|                        | (same aspassword option)                                                     |                                                       |
| -p password            |                                                                              | REMOVED: NDB 7.6.4                                    |
| password=password,     | Connect using this password                                                  | ADDED: NDB 7.6.6                                      |
| -p password            |                                                                              |                                                       |
| port=#,                | Port number to use when<br>connecting to MySQL Server                        | ADDED: NDB 7.6.3                                      |
| -t # (<=7.6.5),        |                                                                              |                                                       |
| -P # (>=7.6.6)         |                                                                              |                                                       |
| print-defaults         | Print program argument list and<br>exit                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| sleep-time=#,          | Time to wait between display<br>refreshes, in seconds                        | ADDED: NDB 7.6.3                                      |
| -s #                   |                                                                              |                                                       |
| socket=path,           | Socket file to use for connection                                            | ADDED: NDB 7.6.6                                      |
| -S path                |                                                                              |                                                       |
| sort,                  | Sort threads by usage; use<br>skip-sort to disable                           | ADDED: NDB 7.6.3                                      |
| -r                     |                                                                              |                                                       |
| text,                  | Display data using text                                                      | ADDED: NDB 7.6.3                                      |
| -x (<=7.6.5),          |                                                                              |                                                       |
| -t (>=7.6.6)           |                                                                              |                                                       |
| usage                  | Show program usage<br>information; same ashelp                               | ADDED: NDB 7.6.3                                      |
| user=name,             | Connect as this MySQL user                                                   | ADDED: NDB 7.6.3                                      |
| -u name                |                                                                              |                                                       |

# <span id="page-130-2"></span>**Additional Options**

• --color, -c

| Command-Line Format | color |
|---------------------|-------|
|---------------------|-------|

Show ASCII graphs in color; use --skip-colors to disable.

<span id="page-130-3"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-130-4"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-130-5"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-130-1"></span>• --graph, -g

| Command-Line Format | graph |
|---------------------|-------|
|---------------------|-------|

Display data using graphs; use --skip-graphs to disable. This option or [--text](#page-132-1) must be true; both options may be true.

<span id="page-130-6"></span>• --help, -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Show program usage information.

<span id="page-130-0"></span>• --host[=name], -h

| Command-Line Format | host=string |
|---------------------|-------------|
| Type                | String      |
| Default Value       | localhost   |

Host name or IP address of MySQL Server to connect to.

<span id="page-130-7"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
|---------------------|-----------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Read given path from login file.

<span id="page-131-2"></span>• --measured-load, -m

| Command-Line Format | measured-load |
|---------------------|---------------|
|---------------------|---------------|

Show measured load by thread. This option or [--os-load](#page-131-3) must be true; both options may be true.

<span id="page-131-5"></span>• --no-defaults

Do not read default options from any option file other than login file.

<span id="page-131-4"></span>• --node-id[=#], -n

| Command-Line Format | node-id=# |
|---------------------|-----------|
| Type                | Integer   |
| Default Value       | 1         |

Watch the data node having this node ID.

<span id="page-131-3"></span>• --os-load, -o

| Command-Line Format | os-load |
|---------------------|---------|

Show load measured by operating system. This option or [--measured-load](#page-131-2) must be true; both options may be true.

<span id="page-131-1"></span>• --passwd[=password], -p

Connect to a MySQL Server using this password and the MySQL user specified by [--user](#page-132-0). Synonym for [--password](#page-131-6).

This password is associated with a MySQL user account only, and is not related in any way to the password used with encrypted NDB backups.

<span id="page-131-6"></span>• --password[=password], -p

| Command-Line Format | password=password |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | NULL              |

Connect to a MySQL Server using this password and the MySQL user specified by [--user](#page-132-0).

This password is associated with a MySQL user account only, and is not related in any way to the password used with encrypted NDB backups.

<span id="page-131-0"></span>• --port[=#], -P

| Command-Line Format | port=#  |
|---------------------|---------|
| Type                | Integer |

| Default Value | 3306 |
|---------------|------|
|---------------|------|

Port number to use when connecting to MySQL Server.

(Formerly, the short form for this option was -t, which was repurposed as the short form of [--text](#page-132-1).)

<span id="page-132-4"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-132-3"></span>• --sleep-time[=seconds], -s

| Command-Line Format | sleep-time=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | 1            |

Time to wait between display refreshes, in seconds.

<span id="page-132-5"></span>• --socket=path/to/file, -S

| Command-Line Format | socket=path |
|---------------------|-------------|
| Type                | Path name   |
| Default Value       | [none]      |

Use the specified socket file for the connection.

<span id="page-132-2"></span>• --sort, -r

| Command-Line Format | sort |
|---------------------|------|
|---------------------|------|

Sort threads by usage; use --skip-sort to disable.

<span id="page-132-1"></span>• --text, -t

| Command-Line Format | text |
|---------------------|------|
|---------------------|------|

Display data using text. This option or [--graph](#page-130-1) must be true; both options may be true.

(The short form for this option was -x in previous versions of NDB Cluster, but this is no longer supported.)

<span id="page-132-6"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-130-6).

<span id="page-132-0"></span>• --user[=name], -u

| Command-Line Format | user=name      |
|---------------------|----------------|
| Type                | 3505<br>String |
| Default Value       | root           |

Connect as this MySQL user. Normally requires a password supplied by the [--password](#page-131-6) option.

**Sample Output.** The next figure shows [ndb\\_top](#page-127-2) running in a terminal window on a Linux system with an ndbmtd data node under a moderate load. Here, the program has been invoked using [ndb\\_top](#page-127-2) [-n8](#page-131-4) [-x](#page-132-1) to provide both text and graph output:

**Figure 21.7 ndb\_top Running in Terminal**

![](_page_133_Picture_3.jpeg)

# <span id="page-133-0"></span>**21.5.30 ndb\_waiter — Wait for NDB Cluster to Reach a Given Status**

[ndb\\_waiter](#page-133-0) repeatedly (each 100 milliseconds) prints out the status of all cluster data nodes until either the cluster reaches a given status or the [--timeout](#page-138-0) limit is exceeded, then exits. By default, it waits for the cluster to achieve STARTED status, in which all nodes have started and connected to the cluster. This can be overridden using the [--no-contact](#page-137-0) and [--not-started](#page-137-1) options.

The node states reported by this utility are as follows:

- NO\_CONTACT: The node cannot be contacted.
- UNKNOWN: The node can be contacted, but its status is not yet known. Usually, this means that the node has received a [START](#page-145-0) or [RESTART](#page-143-1) command from the management server, but has not yet acted on it.
- NOT\_STARTED: The node has stopped, but remains in contact with the cluster. This is seen when restarting the node using the management client's RESTART command.
- STARTING: The node's ndbd process has started, but the node has not yet joined the cluster.
- STARTED: The node is operational, and has joined the cluster.

- SHUTTING\_DOWN: The node is shutting down.
- SINGLE USER MODE: This is shown for all cluster data nodes when the cluster is in single user mode.

Options that can be used with [ndb\\_waiter](#page-133-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.46 Command-line options used with the program ndb\_waiter**

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path              | Directory containing character<br>sets                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                       | Number of times to retry<br>connection before giving up                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                   | Number of seconds to wait<br>between attempts to contact<br>management server                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string,    | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| core-file                               | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                      | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                   | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                      |                                                                                                                                               |                                                       |
| login-path=path                         | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
|                                         | Syntax: "[nodeid=id;]                                                                                                                         |                                                       |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                 | Description                                                                              | Added, Deprecated, or<br>Removed                      |
|------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------|
| no-contact,<br>-n      | Wait for cluster to reach NO<br>CONTACT state                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults            | Do not read default options from<br>any option file other than login<br>file             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| not-started            | Wait for cluster to reach NOT<br>STARTED state                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| nowait-nodes=list      | List of nodes not to be waited for                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults         | Print program argument list and<br>exit                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| single-user            | Wait for cluster to enter single<br>user mode                                            | (Supported in all NDB releases<br>based on MySQL 5.7) |
| timeout=#,<br>-t #     | Wait this many seconds, then<br>exit whether or not cluster has<br>reached desired state | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,<br>-?           | Display help text and exit; same<br>ashelp                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| version,               | Display version information and<br>exit                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V<br>wait-nodes=list, | List of nodes to be waited for                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -w list                |                                                                                          |                                                       |

# **Usage**

ndb\_waiter [-c connection\_string]

# <span id="page-135-0"></span>**Additional Options**

• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-135-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-135-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
|---------------------|-----------------------|

| Type          | Integer |
|---------------|---------|
| Default Value | 5       |
| Minimum Value | 0       |
| Maximum Value | 5       |

Number of seconds to wait between attempts to contact management server.

## <span id="page-136-0"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-137-2).

## <span id="page-136-1"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

## <span id="page-136-2"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

# <span id="page-136-3"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

## <span id="page-136-4"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

# <span id="page-136-6"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-136-5"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

#### Display help text and exit.

## <span id="page-137-2"></span>• --ndb-connectstring

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

## <span id="page-137-3"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

## Same as --[ndb-connectstring](#page-137-2).

# <span id="page-137-4"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-137-2).

<span id="page-137-5"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

## <span id="page-137-0"></span>• --no-contact, -n

Instead of waiting for the STARTED state, [ndb\\_waiter](#page-133-0) continues running until the cluster reaches NO\_CONTACT status before exiting.

<span id="page-137-6"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

## <span id="page-137-1"></span>• --not-started

Instead of waiting for the STARTED state, [ndb\\_waiter](#page-133-0) continues running until the cluster reaches NOT\_STARTED status before exiting.

# <span id="page-137-7"></span>• --nowait-nodes=list

When this option is used, [ndb\\_waiter](#page-133-0) does not wait for the nodes whose IDs are listed. The list is comma-delimited; ranges can be indicated by dashes, as shown here:

\$> **ndb\_waiter --nowait-nodes=1,3,7-9**

![](_page_138_Picture_2.jpeg)

## **Important**

Do not use this option together with the [--wait-nodes](#page-138-5) option.

<span id="page-138-1"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-138-0"></span>• --timeout=seconds, -t seconds

Time to wait. The program exits if the desired state is not achieved within this number of seconds. The default is 120 seconds (1200 reporting cycles).

<span id="page-138-2"></span>• --single-user

The program waits for the cluster to enter single user mode.

<span id="page-138-3"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-136-5).

<span id="page-138-4"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-138-5"></span>• --wait-nodes=list, -w list

When this option is used, [ndb\\_waiter](#page-133-0) waits only for the nodes whose IDs are listed. The list is comma-delimited; ranges can be indicated by dashes, as shown here:

```
$> ndb_waiter --wait-nodes=2,4-6,10
```

![](_page_138_Picture_21.jpeg)

#### **Important**

Do not use this option together with the [--nowait-nodes](#page-137-7) option.

**Sample Output.** Shown here is the output from [ndb\\_waiter](#page-133-0) when run against a 4-node cluster in which two nodes have been shut down and then started again manually. Duplicate reports (indicated by ...) are omitted.

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
```

```
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

![](_page_139_Picture_2.jpeg)

#### **Note**

If no connection string is specified, then [ndb\\_waiter](#page-133-0) tries to connect to a management on localhost, and reports Connecting to mgmsrv at (null).

Prior to NDB 7.5.18 and 7.6.14, this program printed NDBT\_ProgramExit - status upon completion of its run, due to an unnecessary dependency on the NDBT testing library. This dependency is has now been removed, eliminating the extraneous output.