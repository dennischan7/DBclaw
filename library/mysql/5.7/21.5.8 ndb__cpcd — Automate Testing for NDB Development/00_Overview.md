---
source: MySQL 5.7 Reference
title: 00_Overview
---

A utility having this name was formerly part of an internal automated test framework used in testing and debugging NDB Cluster. It is no longer included in NDB Cluster distributions provided by Oracle.

# <span id="page-21-0"></span>**21.5.9 ndb\_delete\_all — Delete All Rows from an NDB Table**

[ndb\\_delete\\_all](#page-21-0) deletes all rows from the given NDB table. In some cases, this can be much faster than DELETE or even TRUNCATE TABLE.

# **Usage**

```
ndb_delete_all -c connection_string tbl_name -d db_name
```

This deletes all rows from the table named tbl\_name in the database named db\_name. It is exactly equivalent to executing TRUNCATE db\_name.tbl\_name in MySQL.

Options that can be used with [ndb\\_delete\\_all](#page-21-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.28 Command-line options used with the program ndb\_delete\_all**

| Format                     | Description                                             | Added, Deprecated, or<br>Removed                      |
|----------------------------|---------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path | Directory containing character<br>sets                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#          | Number of times to retry<br>connection before giving up | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| connect-retry-delay=#                   | Number of seconds to wait<br>between attempts to contact<br>management server                                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string,    | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| core-file                               | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                          | Name of the database in which<br>the table is found                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                                 |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                      | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| diskscan                                | Perform disk scan                                                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                                   | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                      |                                                                                                                                               |                                                       |
| login-path=path                         | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.                                                                                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    | Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                  |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format               | Description                                                                                 | Added, Deprecated, or<br>Removed                      |
|----------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------|
| transactional,<br>-t | Perform delete in one single<br>transaction; possible to run out of<br>operations when used | (Supported in all NDB releases<br>based on MySQL 5.7) |
| tupscan              | Perform tuple scan                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,<br>-?         | Display help text and exit; same<br>ashelp                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| version,<br>-V       | Display version information and<br>exit                                                     | (Supported in all NDB releases<br>based on MySQL 5.7) |

<span id="page-23-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-23-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-23-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-23-3"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as --ndb-connectstring.

<span id="page-23-4"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|                     |           |

# • --database, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database containing the table to delete from.

## <span id="page-24-0"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

## <span id="page-24-1"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

## <span id="page-24-2"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |  |
|---------------------|------------------------------|--|
| Type                | String                       |  |
| Default Value       | [none]                       |  |

Also read groups with concat(group, suffix).

## • --diskscan

| Command-Line Format | diskscan |
|---------------------|----------|
|---------------------|----------|

Run a disk scan.

## <span id="page-24-3"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

# <span id="page-24-4"></span>• --login-path

| Command-Line Format | login-path=path |  |
|---------------------|-----------------|--|
| Type                | String          |  |
| Default Value       | [none]          |  |

Read given path from login file.

# <span id="page-24-5"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |  |
|---------------------|---------------------------------|--|
|                     | connectstring=connection_string |  |

| Type          | String |
|---------------|--------|
| Default Value | [none] |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-25-0"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |  |
|---------------------|---------------------------------|--|
| Type                | String                          |  |
| Default Value       | [none]                          |  |

Same as --ndb-connectstring.

<span id="page-25-1"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |  |
|---------------------|--------------|--|
| Type                | Integer      |  |
| Default Value       | [none]       |  |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

<span id="page-25-2"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-25-3"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-25-4"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

<span id="page-25-5"></span>• --transactional, -t

Use of this option causes the delete operation to be performed as a single transaction.

![](_page_25_Picture_20.jpeg)

#### **Warning**

With very large tables, using this option may cause the number of operations available to the cluster to be exceeded.

• --tupscan

Run a tuple scan.

<span id="page-25-6"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|                     |       |

Display help text and exit; same as --help.

<span id="page-26-0"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-26-1"></span>**21.5.10 ndb\_desc — Describe NDB Tables**

[ndb\\_desc](#page-26-1) provides a detailed description of one or more NDB tables.

# **Usage**

```
ndb_desc -c connection_string tbl_name -d db_name [options]
ndb_desc -c connection_string index_name -d db_name -t tbl_name
```

Additional options that can be used with [ndb\\_desc](#page-26-1) are listed later in this section.

# **Sample Output**

MySQL table creation and population statements:

```
USE test;
CREATE TABLE fish (
 id INT(11) NOT NULL AUTO_INCREMENT,
 name VARCHAR(20) NOT NULL,
 length_mm INT(11) NOT NULL,
 weight_gm INT(11) NOT NULL,
 PRIMARY KEY pk (id),
 UNIQUE KEY uk (name)
) ENGINE=NDB;
INSERT INTO fish VALUES
 (NULL, 'guppy', 35, 2), (NULL, 'tuna', 2500, 150000),
 (NULL, 'shark', 3000, 110000), (NULL, 'manta ray', 1500, 50000),
 (NULL, 'grouper', 900, 125000), (NULL ,'puffer', 250, 2500);
```

# Output from [ndb\\_desc](#page-26-1):

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
```

```
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
uk(name) - OrderedIndex
uk$unique(name) - UniqueHashIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory Extent_space Free extent_space
0 2 2 32768 32768 0 0
1 4 4 32768 32768 0 0
NDBT_ProgramExit: 0 - OK
```

Information about multiple tables can be obtained in a single invocation of [ndb\\_desc](#page-26-1) by using their names, separated by spaces. All of the tables must be in the same database.

You can obtain additional information about a specific index using the --table (short form: -t) option and supplying the name of the index as the first argument to [ndb\\_desc](#page-26-1), as shown here:

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
NDBT_ProgramExit: 0 - OK
```

When an index is specified in this way, the [--extra-partition-info](#page-33-0) and [--extra-node-info](#page-33-1) options have no effect.

The Version column in the output contains the table's schema object version. For information about interpreting this value, see [NDB Schema Object Versions](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-schema-object-versions.md).

Three of the table properties that can be set using NDB\_TABLE comments embedded in CREATE TABLE and ALTER TABLE statements are also visible in [ndb\\_desc](#page-26-1) output. The table's FRAGMENT\_COUNT\_TYPE is always shown in the FragmentCountType column. READ\_ONLY and FULLY\_REPLICATED, if set to 1, are shown in the Table options column. You can see this after executing the following ALTER TABLE statement in the mysql client:

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
) ENGINE=ndbcluster DEFAULT CHARSET=latin1
COMMENT='NDB_TABLE=READ_BACKUP=1,FULLY_REPLICATED=1'
1 row in set (0.01 sec)
```

Because FRAGMENT\_COUNT\_TYPE was not set explicitly, its value is not shown in the comment text printed by SHOW CREATE TABLE. [ndb\\_desc](#page-26-1), however, displays the updated value for this attribute. The Table options column shows the binary properties just enabled. You can see this in the output shown here (emphasized text):

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

```
NDBT_ProgramExit: 0 - OK
```

For more information about these table properties, see Section 13.1.18.9, "Setting NDB Comment Options".

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

(For more information on the statements just shown and the objects created by them, see [Section 21.6.11.1, "NDB Cluster Disk Data Objects"](#page-198-0), as well as Section 13.1.15, "CREATE LOGFILE GROUP Statement", and Section 13.1.19, "CREATE TABLESPACE Statement".)

Now we can create and populate a version of the fish table that stores 2 of its columns on disk (deleting the previous version of the table first, if it already exists):

```
CREATE TABLE fish (
 id INT(11) NOT NULL AUTO_INCREMENT,
 name VARCHAR(20) NOT NULL,
 length_mm INT(11) NOT NULL,
 weight_gm INT(11) NOT NULL,
 PRIMARY KEY pk (id),
 UNIQUE KEY uk (name)
) TABLESPACE ts_1 STORAGE DISK
ENGINE=NDB;
INSERT INTO fish VALUES
 (NULL, 'guppy', 35, 2), (NULL, 'tuna', 2500, 150000),
 (NULL, 'shark', 3000, 110000), (NULL, 'manta ray', 1500, 50000),
 (NULL, 'grouper', 900, 125000), (NULL ,'puffer', 250, 2500);
```

When run against this version of the table, [ndb\\_desc](#page-26-1) displays the following output:

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
Length of frm data: 346
Max Rows: 0
Row Checksum: 1
```

```
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
PartitionCount: 2
FragmentCount: 2
FragmentCountType: ONE_PER_LDM_PER_NODE
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options:
HashMap: DEFAULT-HASHMAP-3840-2
-- Attributes --
id Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
name Varchar(20;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
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
NDBT_ProgramExit: 0 - OK
```

This means that 1048576 bytes are allocated from the tablespace for this table on each partition, of which 1044440 bytes remain free for additional storage. In other words, 1048576 - 1044440 = 4136 bytes per partition is currently being used to store the data from this table's disk-based columns. The number of bytes shown as Free extent\_space is available for storing on-disk column data from the fish table only; for this reason, it is not visible when selecting from the Information Schema FILES table.

For fully replicated tables, [ndb\\_desc](#page-26-1) shows only the nodes holding primary partition fragment replicas; nodes with copy fragment replicas (only) are ignored. Beginning with NDB 7.5.4, you can obtain such information, using the mysql client, from the table\_distribution\_status, table\_fragments, table\_info, and table\_replicas tables in the ndbinfo database.

Options that can be used with [ndb\\_desc](#page-26-1) are shown in the following table. Additional descriptions follow the table.

**Table 21.29 Command-line options used with the program ndb\_desc**

| Format                               | Description                                                                                             | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| auto-inc,<br>-a                      | Show next value for<br>AUTO_INCREMENT oolumn if<br>table has one                                        | ADDED: NDB 7.6.14                                     |
| blob-info,<br>-b                     | Include partition information for<br>BLOB tables in output. Requires<br>that the -p option also be used | (Supported in all NDB releases<br>based on MySQL 5.7) |
| character-sets<br>dir=path           | Directory containing character<br>sets                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                                                 | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format                                  | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| -c connection_string                    |                                                                                                                                               |                                                       |
| context,<br>-x                          | Show extra information for table<br>such as database, schema,                                                                                 | ADDED: NDB 7.6.14                                     |
|                                         | name, and internal ID                                                                                                                         |                                                       |
| core-file                               | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                          | Name of database containing<br>table                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                                 |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path             | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                      | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string         | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| extra-node-info,                        | Include partition-to-data-node<br>mappings in output; requires                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -n                                      | extra-partition-info                                                                                                                          |                                                       |
| extra-partition-info,                   | Display information about<br>partitions                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -p                                      |                                                                                                                                               |                                                       |
| help,<br>-?                             | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| login-path=path                         | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string, | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd<br>host=connection_string,     | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                    |                                                                                                                                               |                                                       |
| ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection         | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                             | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                          | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |

| Format       | Description                                                         | Added, Deprecated, or<br>Removed                      |
|--------------|---------------------------------------------------------------------|-------------------------------------------------------|
| retries=#,   | Number of times to retry the<br>connection (once per second)        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -r #         |                                                                     |                                                       |
| table=name,  | Specify the table in which to find<br>an index. When this option is | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -t name      | used, -p and -n have no effect<br>and are ignored                   |                                                       |
| unqualified, | Use unqualified table names                                         | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -u           |                                                                     |                                                       |
| usage,       | Display help text and exit; same<br>ashelp                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?           |                                                                     |                                                       |
| version,     | Display version information and<br>exit                             | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V           |                                                                     |                                                       |

<span id="page-32-0"></span>• --auto-inc, -a

Show the next value for a table's AUTO\_INCREMENT column, if it has one.

<span id="page-32-1"></span>• --blob-info, -b

Include information about subordinate BLOB and TEXT columns.

Use of this option also requires the use of the [--extra-partition-info](#page-33-0) (-p) option.

<span id="page-32-2"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-32-3"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-32-4"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-32-5"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as --ndb-connectstring.

<span id="page-33-2"></span>• --context, -x

Show additional contextual information for the table such as schema, database name, table name, and the table's internal ID.

<span id="page-33-3"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

<span id="page-33-4"></span>• --database=db\_name, -d

Specify the database in which the table should be found.

<span id="page-33-5"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

<span id="page-33-6"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-33-7"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-33-1"></span>• --extra-node-info, -n

Include information about the mappings between table partitions and the data nodes upon which they reside. This information can be useful for verifying distribution awareness mechanisms and supporting more efficient application access to the data stored in NDB Cluster.

Use of this option also requires the use of the [--extra-partition-info](#page-33-0) (-p) option.

<span id="page-33-0"></span>• --extra-partition-info, -p

## <span id="page-34-0"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

## <span id="page-34-1"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

## <span id="page-34-2"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

## <span id="page-34-3"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as --ndb-connectstring.

## <span id="page-34-4"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by --ndb-connectstring.

## <span id="page-34-5"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|                     |                              |

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

## <span id="page-34-6"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read default options from any option file other than login file.

## <span id="page-34-7"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-35-0"></span>• --retries=#, -r

Try to connect this many times before giving up. One connect attempt is made per second.

<span id="page-35-1"></span>• --table=tbl\_name, -t

Specify the table in which to look for an index.

<span id="page-35-2"></span>• --unqualified, -u

Use unqualified table names.

<span id="page-35-3"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as --help.

<span id="page-35-4"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

In NDB 7.5.3 and later, table indexes listed in the output are ordered by ID. Previously, this was not deterministic and could vary between platforms. (Bug #81763, Bug #23547742)

# <span id="page-35-5"></span>**21.5.11 ndb\_drop\_index — Drop Index from an NDB Table**

[ndb\\_drop\\_index](#page-35-5) drops the specified index from an NDB table. It is recommended that you use this utility only as an example for writing NDB API applications—see the Warning later in this section for details.

# **Usage**

```
ndb_drop_index -c connection_string table_name index -d db_name
```

The statement shown above drops the index named index from the table in the database.

Options that can be used with [ndb\\_drop\\_index](#page-35-5) are shown in the following table. Additional descriptions follow the table.

**Table 21.30 Command-line options used with the program ndb\_drop\_index**

| Format                               | Description                                                                   | Added, Deprecated, or<br>Removed                      |
|--------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|
| character-sets<br>dir=path           | Directory containing character<br>sets                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retries=#                    | Number of times to retry<br>connection before giving up                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect-retry-delay=#                | Number of seconds to wait<br>between attempts to contact<br>management server | (Supported in all NDB releases<br>based on MySQL 5.7) |
| connect<br>string=connection_string, | Same asndb-connectstring                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                 |                                                                               |                                                       |

| Format                              | Description                                                                                                                                   | Added, Deprecated, or<br>Removed                      |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| core-file                           | Write core file on error; used in<br>debugging                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| database=name,                      | Name of database in which table<br>is found                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -d name                             |                                                                                                                                               |                                                       |
| defaults-extra<br>file=path         | Read given file after global files<br>are read                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-file=path                  | Read default options from given<br>file only                                                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| defaults-group<br>suffix=string     | Also read groups with<br>concat(group, suffix)                                                                                                | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,                               | Display help text and exit                                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                  |                                                                                                                                               |                                                       |
| login-path=path                     | Read given path from login file                                                                                                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb                                 | Set connect string for                                                                                                                        | (Supported in all NDB releases                        |
| connectstring=connection_string,    | connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]                                                                                              | based on MySQL 5.7)                                   |
| -c connection_string                | [host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf                                                           |                                                       |
| ndb-mgmd<br>host=connection_string, | Same asndb-connectstring                                                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string                |                                                                                                                                               |                                                       |
| ndb-nodeid=#                        | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection     | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                         | Do not read default options from<br>any option file other than login<br>file                                                                  | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                      | Print program argument list and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,                              | Display help text and exit; same<br>ashelp                                                                                                    | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?                                  |                                                                                                                                               |                                                       |
| version,                            | Display version information and<br>exit                                                                                                       | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                                  |                                                                                                                                               |                                                       |

<span id="page-37-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

Directory containing character sets.

<span id="page-37-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

Number of times to retry connection before giving up.

<span id="page-37-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 5                     |
| Minimum Value       | 0                     |
| Maximum Value       | 5                     |

Number of seconds to wait between attempts to contact management server.

<span id="page-37-3"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-38-4).

<span id="page-37-4"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

• --database, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

• --defaults-extra-file

<span id="page-37-5"></span>

| 3410 |  |
|------|--|

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

Read given file after global files are read.

<span id="page-38-0"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

<span id="page-38-1"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

<span id="page-38-2"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-38-3"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-38-4"></span>• --ndb-connectstring

| Command-Line Format | ndb                             |
|---------------------|---------------------------------|
|                     | connectstring=connection_string |
| Type                | String                          |
| Default Value       | [none]                          |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-38-5"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-38-4).

<span id="page-38-6"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
|---------------------|--------------|

| Type          | Integer |
|---------------|---------|
| Default Value | [none]  |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-38-4).

<span id="page-39-0"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-39-1"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-39-2"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print program argument list and exit.

<span id="page-39-3"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-38-2).

<span id="page-39-4"></span>• --version

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

![](_page_39_Picture_18.jpeg)

#### **Warning**

Operations performed on Cluster table indexes using the NDB API are not visible to MySQL and make the table unusable by a MySQL server. If you use this program to drop an index, then try to access the table from an SQL node, an error results, as shown here:

```
$> ./ndb_drop_index -c localhost dogs ix -d ctest1
Dropping index dogs/idx...OK
NDBT_ProgramExit: 0 - OK
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
```

```
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

In such a case, your only option for making the table available to MySQL again is to drop the table and re-create it. You can use either the SQL statementDROP TABLE or the [ndb\\_drop\\_table](#page-40-0) utility (see [Section 21.5.12, "ndb\\_drop\\_table — Drop an NDB Table"](#page-40-0)) to drop the table.

# <span id="page-40-0"></span>**21.5.12 ndb\_drop\_table — Drop an NDB Table**

[ndb\\_drop\\_table](#page-40-0) drops the specified NDB table. (If you try to use this on a table created with a storage engine other than NDB, the attempt fails with the error 723: No such table exists.) This operation is extremely fast; in some cases, it can be an order of magnitude faster than using a MySQL DROP TABLE statement on an NDB table.

# **Usage**

```
ndb_drop_table -c connection_string tbl_name -d db_name
```

Options that can be used with [ndb\\_drop\\_table](#page-40-0) are shown in the following table. Additional descriptions follow the table.

**Table 21.31 Command-line options used with the program ndb\_drop\_table**

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
| -?                                   |                                                                               |                                                       |

| Format                                                          | Description                                                                                                                                                       | Added, Deprecated, or<br>Removed                      |
|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| login-path=path                                                 | Read given path from login file                                                                                                                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb<br>connectstring=connection_string,<br>-c connection_string | Set connect string for<br>connecting to ndb_mgmd.<br>Syntax: "[nodeid=id;]<br>[host=]hostname[:port]".<br>Overrides entries in<br>NDB_CONNECTSTRING and<br>my.cnf | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-mgmd<br>host=connection_string,                             | Same asndb-connectstring                                                                                                                                          | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -c connection_string<br>ndb-nodeid=#                            | Set node ID for this node,<br>overriding any ID set byndb<br>connectstring                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| ndb-optimized-node<br>selection                                 | Enable optimizations for<br>selection of nodes for<br>transactions. Enabled by default;<br>useskip-ndb-optimized-node<br>selection to disable                     | (Supported in all NDB releases<br>based on MySQL 5.7) |
| no-defaults                                                     | Do not read default options from<br>any option file other than login<br>file                                                                                      | (Supported in all NDB releases<br>based on MySQL 5.7) |
| print-defaults                                                  | Print program argument list and<br>exit                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| usage,                                                          | Display help text and exit; same<br>ashelp                                                                                                                        | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -?<br>version,                                                  | Display version information and<br>exit                                                                                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| -V                                                              |                                                                                                                                                                   |                                                       |

# <span id="page-41-0"></span>• --character-sets-dir

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
|---------------------|-------------------------|

#### Directory containing character sets.

# <span id="page-41-1"></span>• --connect-retries

| Command-Line Format | connect-retries=# |
|---------------------|-------------------|
| Type                | Integer           |
| Default Value       | 12                |
| Minimum Value       | 0                 |
| Maximum Value       | 12                |

#### Number of times to retry connection before giving up.

## <span id="page-41-2"></span>• --connect-retry-delay

| Command-Line Format | connect-retry-delay=# |
|---------------------|-----------------------|
|---------------------|-----------------------|

| Type          | Integer |
|---------------|---------|
| Default Value | 5       |
| Minimum Value | 0       |
| Maximum Value | 5       |

Number of seconds to wait between attempts to contact management server.

## <span id="page-42-0"></span>• --connect-string

| Command-Line Format | connect-string=connection_string |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | [none]                           |

Same as [--ndb-connectstring](#page-43-1).

## <span id="page-42-1"></span>• --core-file

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

Write core file on error; used in debugging.

## • --database, -d

| Command-Line Format | database=name |
|---------------------|---------------|
| Type                | String        |
| Default Value       | TEST_DB       |

Name of the database in which the table resides.

# <span id="page-42-2"></span>• --defaults-extra-file

| Command-Line Format | defaults-extra-file=path |
|---------------------|--------------------------|
| Type                | String                   |
| Default Value       | [none]                   |

Read given file after global files are read.

## <span id="page-42-3"></span>• --defaults-file

| Command-Line Format | defaults-file=path |
|---------------------|--------------------|
| Type                | String             |
| Default Value       | [none]             |

Read default options from given file only.

# <span id="page-42-4"></span>• --defaults-group-suffix

| Command-Line Format | defaults-group-suffix=string |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | [none]                       |

Also read groups with concat(group, suffix).

## <span id="page-42-5"></span>• --help

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display help text and exit.

<span id="page-43-0"></span>• --login-path

| Command-Line Format | login-path=path |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | [none]          |

Read given path from login file.

<span id="page-43-1"></span>• --ndb-connectstring

| Command-Line Format | ndb<br>connectstring=connection_string |
|---------------------|----------------------------------------|
| Type                | String                                 |
| Default Value       | [none]                                 |

Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf.

<span id="page-43-2"></span>• --ndb-mgmd-host

| Command-Line Format | ndb-mgmd-host=connection_string |
|---------------------|---------------------------------|
| Type                | String                          |
| Default Value       | [none]                          |

Same as [--ndb-connectstring](#page-43-1).

<span id="page-43-3"></span>• --ndb-nodeid

| Command-Line Format | ndb-nodeid=# |
|---------------------|--------------|
| Type                | Integer      |
| Default Value       | [none]       |

Set node ID for this node, overriding any ID set by [--ndb-connectstring](#page-43-1).

<span id="page-43-4"></span>• --ndb-optimized-node-selection

| Command-Line Format | ndb-optimized-node-selection |
|---------------------|------------------------------|

Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndboptimized-node-selection to disable.

<span id="page-43-5"></span>• --no-defaults

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read default options from any option file other than login file.

<span id="page-43-6"></span>• --print-defaults

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print program argument list and exit.

# <span id="page-44-0"></span>• --usage

| Command-Line Format | usage |
|---------------------|-------|
|---------------------|-------|

Display help text and exit; same as [--help](#page-42-5).

## <span id="page-44-1"></span>• --version

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-44-2"></span>**21.5.13 ndb\_error\_reporter — NDB Error-Reporting Utility**

[ndb\\_error\\_reporter](#page-44-2) creates an archive from data node and management node log files that can be used to help diagnose bugs or other problems with a cluster. It is highly recommended that you make use of this utility when filing reports of bugs in NDB Cluster.

Options that can be used with [ndb\\_error\\_reporter](#page-44-2) are shown in the following table. Additional descriptions follow the table.

**Table 21.32 Command-line options used with the program ndb\_error\_reporter**

| Format               | Description                                                                          | Added, Deprecated, or<br>Removed                      |
|----------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------|
| connection-timeout=# | Number of seconds to wait when<br>connecting to nodes before<br>timing out           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| dry-scp              | Disable scp with remote hosts;<br>used in testing only                               | (Supported in all NDB releases<br>based on MySQL 5.7) |
| fs                   | Include file system data in error<br>report; can use a large amount of<br>disk space | (Supported in all NDB releases<br>based on MySQL 5.7) |
| help,<br>-?          | Display help text and exit                                                           | (Supported in all NDB releases<br>based on MySQL 5.7) |
| skip-nodegroup=#     | Skip all nodes in the node group<br>having this ID                                   | (Supported in all NDB releases<br>based on MySQL 5.7) |

# **Usage**

```
ndb_error_reporter path/to/config-file [username] [options]
```

This utility is intended for use on a management node host, and requires the path to the management host configuration file (usually named config.ini). Optionally, you can supply the name of a user that is able to access the cluster's data nodes using SSH, to copy the data node log files. [ndb\\_error\\_reporter](#page-44-2) then includes all of these files in archive that is created in the same directory in which it is run. The archive is named ndb\_error\_report\_YYYYMMDDhhmmss.tar.bz2, where YYYYMMDDhhmmss is a datetime string.

[ndb\\_error\\_reporter](#page-44-2) also accepts the options listed here:

# <span id="page-44-3"></span>• --connection-timeout=timeout

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Wait this many seconds when trying to connect to nodes before timing out.

<span id="page-45-0"></span>• --dry-scp

| Command-Line Format | dry-scp |
|---------------------|---------|

Run [ndb\\_error\\_reporter](#page-44-2) without using scp from remote hosts. Used for testing only.

<span id="page-45-1"></span>• --fs

| Command-Line Format | fs |
|---------------------|----|
|---------------------|----|

Copy the data node file systems to the management host and include them in the archive.

Because data node file systems can be extremely large, even after being compressed, we ask that you please do not send archives created using this option to Oracle unless you are specifically requested to do so.

<span id="page-45-2"></span>• --help

| Command-Line Format | help |
|---------------------|------|

Display help text and exit.

<span id="page-45-3"></span>• --skip-nodegroup=nodegroup\_id

| Command-Line Format | connection-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |

Skip all nodes belong to the node group having the supplied node group ID.

# <span id="page-45-4"></span>**21.5.14 ndb\_import — Import CSV Data Into NDB**

[ndb\\_import](#page-45-4) imports CSV-formatted data, such as that produced by mysqldump --tab, directly into NDB using the NDB API. [ndb\\_import](#page-45-4) requires a connection to an NDB management server (ndb\_mgmd) to function; it does not require a connection to a MySQL Server.

# **Usage**

```
ndb_import db_name file_name options
```

[ndb\\_import](#page-45-4) requires two arguments. db\_name is the name of the database where the table into which to import the data is found; file\_name is the name of the CSV file from which to read the data; this must include the path to this file if it is not in the current directory. The name of the file must match that of the table; the file's extension, if any, is not taken into consideration. Options supported by [ndb\\_import](#page-45-4) include those for specifying field separators, escapes, and line terminators, and are described later in this section.

[ndb\\_import](#page-45-4) rejects any empty lines read from the CSV file.

[ndb\\_import](#page-45-4) must be able to connect to an NDB Cluster management server; for this reason, there must be an unused [api] slot in the cluster config.ini file.

To duplicate an existing table that uses a different storage engine, such as InnoDB, as an NDB table, use the mysql client to perform a SELECT INTO OUTFILE statement to export the existing table to a CSV file, then to execute a CREATE TABLE LIKE statement to create a new table having the same structure as the existing table, then perform ALTER TABLE ... ENGINE=NDB on the new table; after this, from the system shell, invoke [ndb\\_import](#page-45-4) to load the data into the new NDB table. For example, an existing InnoDB table named myinnodb\_table in a database named myinnodb can be exported into an NDB table named myndb\_table in a database named myndb as shown here, assuming that you are already logged in as a MySQL user with the appropriate privileges: