---
source: MySQL 8.4 Reference
title: 00_Overview
---

mysqld is the traditional MySQL server process. To be used with NDB Cluster, mysqld needs to be built with support for the NDB storage engine, as it is in the precompiled binaries available from <https://dev.mysql.com/downloads/>. If you build MySQL from source, you must invoke CMake with the - DWITH\_NDB=1 or (deprecated) -DWITH\_NDBCLUSTER=1 option to include support for NDB.

For more information about compiling NDB Cluster from source, see Section 25.3.1.4, "Building NDB Cluster from Source on Linux", and Section 25.3.2.2, "Compiling and Installing NDB Cluster from Source on Windows".

(For information about mysqld options and variables, in addition to those discussed in this section, which are relevant to NDB Cluster, see Section 25.4.3.9, "MySQL Server Options and Variables for NDB Cluster".)

If the mysqld binary has been built with Cluster support, the NDBCLUSTER storage engine is still disabled by default. You can use either of two possible options to enable this engine:

- Use --ndbcluster as a startup option on the command line when starting mysqld.
- Insert a line containing ndbcluster in the [mysqld] section of your my.cnf file.

An easy way to verify that your server is running with the NDBCLUSTER storage engine enabled is to issue the SHOW ENGINES statement in the MySQL Monitor (mysql). You should see the value YES as the Support value in the row for NDBCLUSTER. If you see NO in this row or if there is no such row displayed in the output, you are not running an NDB-enabled version of MySQL. If you see DISABLED in this row, you need to enable it in either one of the two ways just described.

To read cluster configuration data, the MySQL server requires at a minimum three pieces of information:

- The MySQL server's own cluster node ID
- The host name or IP address for the management server
- The number of the TCP/IP port on which it can connect to the management server

Node IDs can be allocated dynamically, so it is not strictly necessary to specify them explicitly.

The mysqld parameter ndb-connectstring is used to specify the connection string either on the command line when starting mysqld or in my.cnf. The connection string contains the host name or IP address where the management server can be found, as well as the TCP/IP port it uses.

In the following example, ndb\_mgmd.mysql.com is the host where the management server resides, and the management server listens for cluster messages on port 1186:

```
$> mysqld --ndbcluster --ndb-connectstring=ndb_mgmd.mysql.com:1186
```

See Section 25.4.3.3, "NDB Cluster Connection Strings", for more information on connection strings.

Given this information, the MySQL server can act as a full participant in the cluster. (We often refer to a mysqld process running in this manner as an SQL node.) It is fully aware of all cluster data nodes as well as their status, and establishes connections to all data nodes. In this case, it is able to use any data node as a transaction coordinator and to read and update node data.

You can see in the mysql client whether a MySQL server is connected to the cluster using SHOW PROCESSLIST. If the MySQL server is connected to the cluster, and you have the PROCESS privilege, then the first row of the output is as shown here:

```
mysql> SHOW PROCESSLIST \G
*************************** 1. row ***************************
 Id: 1
 User: system user
 Host:
 db:
Command: Daemon
 Time: 1
 State: Waiting for event from ndbcluster
 Info: NULL
```

![](_page_158_Picture_18.jpeg)

#### **Important**

To participate in an NDB Cluster, the mysqld process must be started with both the options --ndbcluster and --ndb-connectstring (or their equivalents in my.cnf). If mysqld is started with only the --ndbcluster option, or if it

is unable to contact the cluster, it is not possible to work with NDB tables, nor is it possible to create any new tables regardless of storage engine. The latter restriction is a safety measure intended to prevent the creation of tables having the same names as NDB tables while the SQL node is not connected to the cluster. If you wish to create tables using a different storage engine while the mysqld process is not participating in an NDB Cluster, you must restart the server without the --ndbcluster option.

## <span id="page-159-0"></span>**25.6.11 NDB Cluster Disk Data Tables**

NDB Cluster supports storing nonindexed columns of NDB tables on disk, rather than in RAM. Column data and logging metadata are kept in data files and undo log files, conceptualized as tablespaces and log file groups, as described in the next section—see [Section 25.6.11.1, "NDB Cluster Disk Data](#page-159-1) [Objects"](#page-159-1).

NDB Cluster Disk Data performance can be influenced by a number of configuration parameters. For information about these parameters and their effects, see Disk Data Configuration Parameters, and Disk Data and GCP Stop errors.

You should also set the DiskDataUsingSameDisk data node configuration parameter to false when using separate disks for Disk Data files.

For more information, see the following:

- Disk Data file system parameters.
- Disk Data latency parameters
- Section 25.6.15.32, "The ndbinfo diskstat Table"
- Section 25.6.15.33, "The ndbinfo diskstats\_1sec Table"
- Section 25.6.15.50, "The ndbinfo pgman\_time\_track\_stats Table"

### <span id="page-159-1"></span>**25.6.11.1 NDB Cluster Disk Data Objects**

NDB Cluster Disk Data storage is implemented using the following objects:

- Tablespace: Acts as containers for other Disk Data objects. A tablespace contains one or more data files and one or more undo log file groups.
- Data file: Stores column data. A data file is assigned directly to a tablespace.
- Undo log file: Contains undo information required for rolling back transactions. Assigned to an undo log file group.
- log file group: Contains one or more undo log files. Assigned to a tablespace.

Undo log files and data files are actual files in the file system of each data node; by default they are placed in ndb\_node\_id\_fs in the DataDir specified in the NDB Cluster config.ini file, and where node\_id is the data node's node ID. It is possible to place these elsewhere by specifying either an absolute or relative path as part of the filename when creating the undo log or data file. Statements that create these files are shown later in this section.

Undo log files are used only by Disk Data tables, and are not needed or used by NDB tables that are stored in memory only.

NDB Cluster tablespaces and log file groups are not implemented as files.

Although not all Disk Data objects are implemented as files, they all share the same namespace. This means that each Disk Data object must be uniquely named (and not merely each Disk Data object of a given type). For example, you cannot have a tablespace and a log file group both named dd1.

Assuming that you have already set up an NDB Cluster with all nodes (including management and SQL nodes), the basic steps for creating an NDB Cluster table on disk are as follows:

- 1. Create a log file group, and assign one or more undo log files to it (an undo log file is also sometimes referred to as an undofile).
- 2. Create a tablespace; assign the log file group, as well as one or more data files, to the tablespace.
- 3. Create a Disk Data table that uses this tablespace for data storage.

Each of these tasks can be accomplished using SQL statements in the mysql client or other MySQL client application, as shown in the example that follows.

1. We create a log file group named lg\_1 using CREATE LOGFILE GROUP. This log file group is to be made up of two undo log files, which we name undo\_1.log and undo\_2.log, whose initial sizes are 16 MB and 12 MB, respectively. (The default initial size for an undo log file is 128 MB.) Optionally, you can also specify a size for the log file group's undo buffer, or permit it to assume the default value of 8 MB. In this example, we set the UNDO buffer's size at 2 MB. A log file group must be created with an undo log file; so we add undo\_1.log to lg\_1 in this CREATE LOGFILE GROUP statement:

```
CREATE LOGFILE GROUP lg_1
 ADD UNDOFILE 'undo_1.log'
 INITIAL_SIZE 16M
 UNDO_BUFFER_SIZE 2M
 ENGINE NDBCLUSTER;
```

To add undo\_2.log to the log file group, use the following ALTER LOGFILE GROUP statement:

```
ALTER LOGFILE GROUP lg_1
 ADD UNDOFILE 'undo_2.log'
 INITIAL_SIZE 12M
 ENGINE NDBCLUSTER;
```

#### Some items of note:

- The .log file extension used here is not required. We employ it merely to make the log files easily recognizable.
- Every CREATE LOGFILE GROUP and ALTER LOGFILE GROUP statement must include an ENGINE option. The only permitted values for this option are NDBCLUSTER and NDB.

![](_page_160_Picture_13.jpeg)

#### **Important**

There can exist at most one log file group in the same NDB Cluster at any given time.

- When you add an undo log file to a log file group using ADD UNDOFILE 'filename', a file with the name filename is created in the ndb\_node\_id\_fs directory within the DataDir of each data node in the cluster, where node\_id is the node ID of the data node. Each undo log file is of the size specified in the SQL statement. For example, if an NDB Cluster has 4 data nodes, then the ALTER LOGFILE GROUP statement just shown creates 4 undo log files, 1 each on in the data directory of each of the 4 data nodes; each of these files is named undo\_2.log and each file is 12 MB in size.
- UNDO\_BUFFER\_SIZE is limited by the amount of system memory available.
- See Section 15.1.16, "CREATE LOGFILE GROUP Statement", and Section 15.1.6, "ALTER LOGFILE GROUP Statement", for more information about these statements.
- 2. Now we can create a tablespace—an abstract container for files used by Disk Data tables to store data. A tablespace is associated with a particular log file group; when creating a new tablespace, you must specify the log file group it uses for undo logging. You must also specify at least one data

file; you can add more data files to the tablespace after the tablespace is created. It is also possible to drop data files from a tablespace (see example later in this section).

Assume that we wish to create a tablespace named ts\_1 which uses lg\_1 as its log file group. We want the tablespace to contain two data files, named data\_1.dat and data\_2.dat, whose initial sizes are 32 MB and 48 MB, respectively. (The default value for INITIAL\_SIZE is 128 MB.) We can do this using two SQL statements, as shown here:

```
CREATE TABLESPACE ts_1
 ADD DATAFILE 'data_1.dat'
 USE LOGFILE GROUP lg_1
 INITIAL_SIZE 32M
 ENGINE NDBCLUSTER;
ALTER TABLESPACE ts_1
 ADD DATAFILE 'data_2.dat'
 INITIAL_SIZE 48M;
```

The CREATE TABLESPACE statement creates a tablespace ts\_1 with the data file data\_1.dat, and associates ts\_1 with log file group lg\_1. The ALTER TABLESPACE adds the second data file (data\_2.dat).

#### Some items of note:

- As is the case with the .log file extension used in this example for undo log files, there is no special significance for the .dat file extension; it is used merely for easy recognition.
- When you add a data file to a tablespace using ADD DATAFILE 'filename', a file with the name filename is created in the ndb\_node\_id\_fs directory within the DataDir of each data node in the cluster, where node\_id is the node ID of the data node. Each data file is of the size specified in the SQL statement. For example, if an NDB Cluster has 4 data nodes, then the ALTER TABLESPACE statement just shown creates 4 data files, 1 each in the data directory of each of the 4 data nodes; each of these files is named data\_2.dat, and each file is 48 MB in size.
- NDB reserves 4% of each tablespace for use during data node restarts. This space is not available for storing data.
- CREATE TABLESPACE statements must contain an ENGINE clause; only tables using the same storage engine as the tablespace can be created in the tablespace. For NDB tablespaces, ALTER TABLESPACE accepts an ENGINE clause only for ALTER TABLESPACE ... ADD DATAFILE; ENGINE is rejected for any other ALTER TABLESPACE statement. For NDB tablespaces, the only permitted values for the ENGINE option are NDBCLUSTER and NDB.
- Allocation of extents is performed in round-robin fashion among all data files used by a given tablespace.
- For more information about the CREATE TABLESPACE and ALTER TABLESPACE statements, see Section 15.1.21, "CREATE TABLESPACE Statement", and Section 15.1.10, "ALTER TABLESPACE Statement".
- 3. Now it is possible to create a table whose unindexed columns are stored on disk using files in tablespace ts\_1:

```
CREATE TABLE dt_1 (
 member_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 last_name VARCHAR(50) NOT NULL,
 first_name VARCHAR(50) NOT NULL,
 dob DATE NOT NULL,
 joined DATE NOT NULL,
 INDEX(last_name, first_name)
 )
 TABLESPACE ts_1 STORAGE DISK
 ENGINE NDBCLUSTER;
```

TABLESPACE ts\_1 STORAGE DISK tells the NDB storage engine to use tablespace ts\_1 for data storage on disk.

Once table ts\_1 has been created as shown, you can perform INSERT, SELECT, UPDATE, and DELETE statements on it just as you would with any other MySQL table.

It is also possible to specify whether an individual column is stored on disk or in memory by using a STORAGE clause as part of the column's definition in a CREATE TABLE or ALTER TABLE statement. STORAGE DISK causes the column to be stored on disk, and STORAGE MEMORY causes in-memory storage to be used. See Section 15.1.20, "CREATE TABLE Statement", for more information.

You can obtain information about the NDB disk data files and undo log files just created by querying the FILES table in the INFORMATION\_SCHEMA database, as shown here:

```
mysql> SELECT
 FILE_NAME AS File, FILE_TYPE AS Type,
 TABLESPACE_NAME AS Tablespace, TABLE_NAME AS Name,
 LOGFILE_GROUP_NAME AS 'File group',
 FREE_EXTENTS AS Free, TOTAL_EXTENTS AS Total
 FROM INFORMATION_SCHEMA.FILES
 WHERE ENGINE='ndbcluster';
+--------------+----------+------------+------+------------+------+---------+
| File | Type | Tablespace | Name | File group | Free | Total |
+--------------+----------+------------+------+------------+------+---------+
| ./undo_1.log | UNDO LOG | lg_1 | NULL | lg_1 | 0 | 4194304 |
| ./undo_2.log | UNDO LOG | lg_1 | NULL | lg_1 | 0 | 3145728 |
| ./data_1.dat | DATAFILE | ts_1 | NULL | lg_1 | 32 | 32 |
| ./data_2.dat | DATAFILE | ts_1 | NULL | lg_1 | 48 | 48 |
+--------------+----------+------------+------+------------+------+---------+
4 rows in set (0.00 sec)
```

For more information and examples, see Section 28.3.15, "The INFORMATION\_SCHEMA FILES Table".

**Indexing of columns implicitly stored on disk.** For table dt\_1 as defined in the example just shown, only the dob and joined columns are stored on disk. This is because there are indexes on the id, last\_name, and first\_name columns, and so data belonging to these columns is stored in RAM. Only nonindexed columns can be held on disk; indexes and indexed column data continue to be stored in memory. This tradeoff between the use of indexes and conservation of RAM is something you must keep in mind as you design Disk Data tables.

You cannot add an index to a column that has been explicitly declared STORAGE DISK, without first changing its storage type to MEMORY; any attempt to do so fails with an error. A column which implicitly uses disk storage can be indexed; when this is done, the column's storage type is changed to MEMORY automatically. By "implicitly", we mean a column whose storage type is not declared, but which is which inherited from the parent table. In the following CREATE TABLE statement (using the tablespace ts\_1 defined previously), columns c2 and c3 use disk storage implicitly:

```
mysql> CREATE TABLE ti (
 -> c1 INT PRIMARY KEY,
 -> c2 INT,
 -> c3 INT,
 -> c4 INT
 -> )
 -> STORAGE DISK
 -> TABLESPACE ts_1
 -> ENGINE NDBCLUSTER;
Query OK, 0 rows affected (1.31 sec)
```

Because c2, c3, and c4 are themselves not declared with STORAGE DISK, it is possible to index them. Here, we add indexes to c2 and c3, using, respectively, CREATE INDEX and ALTER TABLE:

```
mysql> CREATE INDEX i1 ON ti(c2);
```

```
Query OK, 0 rows affected (2.72 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> ALTER TABLE ti ADD INDEX i2(c3);
Query OK, 0 rows affected (0.92 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

SHOW CREATE TABLE confirms that the indexes were added.

```
mysql> SHOW CREATE TABLE ti\G
*************************** 1. row ***************************
 Table: ti
Create Table: CREATE TABLE `ti` (
 `c1` int(11) NOT NULL,
 `c2` int(11) DEFAULT NULL,
 `c3` int(11) DEFAULT NULL,
 `c4` int(11) DEFAULT NULL,
 PRIMARY KEY (`c1`),
 KEY `i1` (`c2`),
 KEY `i2` (`c3`)
) /*!50100 TABLESPACE `ts_1` STORAGE DISK */ ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

You can see using ndb\_desc that the indexed columns (emphasized text) now use in-memory rather than on-disk storage:

```
$> ./ndb_desc -d test t1
-- t1 --
Version: 33554433
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 4
Number of primary keys: 1
Length of frm data: 317
Max Rows: 0
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
PartitionCount: 4
FragmentCount: 4
PartitionBalance: FOR_RP_BY_LDM
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
Table options:
HashMap: DEFAULT-HASHMAP-3840-4
-- Attributes --
c1 Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY
c2 Int NULL AT=FIXED ST=MEMORY
c3 Int NULL AT=FIXED ST=MEMORY
c4 Int NULL AT=FIXED ST=DISK
-- Indexes --
PRIMARY KEY(c1) - UniqueHashIndex
i2(c3) - OrderedIndex
PRIMARY(c1) - OrderedIndex
i1(c2) - OrderedIndex
```

**Performance note.** The performance of a cluster using Disk Data storage is greatly improved if Disk Data files are kept on a separate physical disk from the data node file system. This must be done for each data node in the cluster to derive any noticeable benefit.

You can use absolute and relative file system paths with ADD UNDOFILE and ADD DATAFILE; relative paths are calculated with respect to the data node's data directory.

A log file group, a tablespace, and any Disk Data tables using these must be created in a particular order. This is also true for dropping these objects, subject to the following constraints:

- A log file group cannot be dropped as long as any tablespaces use it.
- A tablespace cannot be dropped as long as it contains any data files.
- You cannot drop any data files from a tablespace as long as there remain any tables which are using the tablespace.
- It is not possible to drop files created in association with a different tablespace other than the one with which the files were created.

For example, to drop all the objects created so far in this section, you can use the following statements:

```
mysql> DROP TABLE dt_1;
mysql> ALTER TABLESPACE ts_1
 -> DROP DATAFILE 'data_2.dat';
mysql> ALTER TABLESPACE ts_1
 -> DROP DATAFILE 'data_1.dat';
mysql> DROP TABLESPACE ts_1;
mysql> DROP LOGFILE GROUP lg_1;
```

These statements must be performed in the order shown, except that the two ALTER TABLESPACE ... DROP DATAFILE statements may be executed in either order.

![](_page_164_Picture_8.jpeg)

#### **Note**

Older versions of NDB Cluster used an ENGINE clause with ALTER TABLESPACE ... DROP DATAFILE and DROP TABLESPACE. In NDB 8.4 and later, it is no longer supported with either of these statements.

### **25.6.11.2 NDB Cluster Disk Data Storage Requirements**

The following items apply to Disk Data storage requirements:

• Variable-length columns of Disk Data tables take up a fixed amount of space. For each row, this is equal to the space required to store the largest possible value for that column.

For general information about calculating these values, see Section 13.7, "Data Type Storage Requirements".

You can obtain an estimate the amount of space available in data files and undo log files by querying the Information Schema FILES table. For more information and examples, see Section 28.3.15, "The INFORMATION\_SCHEMA FILES Table".

![](_page_164_Picture_16.jpeg)

### **Note**

The OPTIMIZE TABLE statement does not have any effect on Disk Data tables.

- In a Disk Data table, the first 256 bytes of a TEXT or BLOB column are stored in memory; only the remainder is stored on disk.
- Each row in a Disk Data table uses 8 bytes in memory to point to the data stored on disk. This means that, in some cases, converting an in-memory column to the disk-based format can actually result in greater memory usage. For example, converting a CHAR(4) column from memory-based to disk-based format increases the amount of DataMemory used per row from 4 to 8 bytes.

![](_page_164_Picture_21.jpeg)

#### **Important**

Starting the cluster with the --initial option does not remove Disk Data files. You must remove these manually prior to performing an initial restart of the cluster.

Performance of Disk Data tables can be improved by minimizing the number of disk seeks by making sure that DiskPageBufferMemory is of sufficient size. You can query the diskpagebuffer table to help determine whether the value for this parameter needs to be increased.