---
source: MySQL 8.0 Reference
title: 00_Overview
---

Beginning with MySQL 8.0.30, MySQL supports generated invisible primary keys for any InnoDB table that is created without an explicit primary key. When the sql\_generate\_invisible\_primary\_key server system variable is set to ON, the MySQL server automatically adds a generated invisible primary key (GIPK) to any such table. This setting has no effect on tables created using any other storage engine than InnoDB.

By default, the value of sql\_generate\_invisible\_primary\_key is OFF, meaning that the automatic addition of GIPKs is disabled. To illustrate how this affects table creation, we begin by creating two identical tables, neither having a primary key, the only difference being that the first (table auto\_0) is created with sql\_generate\_invisible\_primary\_key set to OFF, and the second (auto\_1) after setting it to ON, as shown here:

```
mysql> SELECT @@sql_generate_invisible_primary_key;
+--------------------------------------+
| @@sql_generate_invisible_primary_key |
+--------------------------------------+
| 0 |
+--------------------------------------+
1 row in set (0.00 sec)
mysql> CREATE TABLE auto_0 (c1 VARCHAR(50), c2 INT);
Query OK, 0 rows affected (0.02 sec)
mysql> SET sql_generate_invisible_primary_key=ON;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@sql_generate_invisible_primary_key;
+--------------------------------------+
| @@sql_generate_invisible_primary_key |
+--------------------------------------+
| 1 |
+--------------------------------------+
1 row in set (0.00 sec)
mysql> CREATE TABLE auto_1 (c1 VARCHAR(50), c2 INT);
Query OK, 0 rows affected (0.04 sec)
```

Compare the output of these SHOW CREATE TABLE statements to see the difference in how the tables were actually created:

```
mysql> SHOW CREATE TABLE auto_0\G
*************************** 1. row ***************************
 Table: auto_0
Create Table: CREATE TABLE `auto_0` (
 `c1` varchar(50) DEFAULT NULL,
 `c2` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> SHOW CREATE TABLE auto_1\G
*************************** 1. row ***************************
 Table: auto_1
Create Table: CREATE TABLE `auto_1` (
 `my_row_id` bigint unsigned NOT NULL AUTO_INCREMENT /*!80023 INVISIBLE */,
 `c1` varchar(50) DEFAULT NULL,
 `c2` int DEFAULT NULL,
 PRIMARY KEY (`my_row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

Since auto\_1 had no primary key specified by the CREATE TABLE statement used to create it, setting sql\_generate\_invisible\_primary\_key = ON causes MySQL to add both the invisible column my\_row\_id to this table and a primary key on that column. Since sql\_generate\_invisible\_primary\_key was OFF at the time that auto\_0 was created, no such additions were performed on that table.

When a primary key is added to a table by the server, the column and key name is always my\_row\_id. For this reason, when enabling generated invisible primary keys in this way, you cannot create a table having a column named my\_row\_id unless the table creation statement also specifies an explicit primary key. (You are not required to name the column or key my\_row\_id in such cases.)

my\_row\_id is an invisible column, which means it is not shown in the output of SELECT \* or TABLE; the column must be selected explicitly by name. See [Section 15.1.20.10, "Invisible Columns"](#page-168-0).

When GIPKs are enabled, a generated primary key cannot be altered other than to switch it between VISIBLE and INVISIBLE. To make the generated invisible primary key on auto\_1 visible, execute this [ALTER TABLE](#page-64-1) statement:

```
mysql> ALTER TABLE auto_1 ALTER COLUMN my_row_id SET VISIBLE;
Query OK, 0 rows affected (0.02 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW CREATE TABLE auto_1\G
*************************** 1. row ***************************
 Table: auto_1
Create Table: CREATE TABLE `auto_1` (
 `my_row_id` bigint unsigned NOT NULL AUTO_INCREMENT,
 `c1` varchar(50) DEFAULT NULL,
 `c2` int DEFAULT NULL,
 PRIMARY KEY (`my_row_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.01 sec)
```

To make this generated primary key invisible again, issue ALTER TABLE auto\_1 ALTER COLUMN my\_row\_id SET INVISIBLE.

A generated invisible primary key is always invisible by default.

Whenever GIPKs are enabled, you cannot drop a generated primary key if either of the following 2 conditions would result:

- The table is left with no primary key.
- The primary key is dropped, but not the primary key column.

The effects of sql\_generate\_invisible\_primary\_key apply to tables using the InnoDB storage engine only. You can use an [ALTER TABLE](#page-64-1) statement to change the storage engine used by a table that has a generated invisible primary key; in this case, the primary key and column remain in place, but the table and key no longer receive any special treatment.

By default, GIPKs are shown in the output of SHOW CREATE TABLE, SHOW COLUMNS, and SHOW INDEX, and are visible in the Information Schema COLUMNS and STATISTICS tables. You can cause generated invisible primary keys to be hidden instead in such cases by setting the show\_gipk\_in\_create\_table\_and\_information\_schema system variable to OFF. By default, this variable is ON, as shown here:

```
mysql> SELECT @@show_gipk_in_create_table_and_information_schema;
+----------------------------------------------------+
| @@show_gipk_in_create_table_and_information_schema |
+----------------------------------------------------+
| 1 |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

As can be seen from the following query against the COLUMNS table, my\_row\_id is visible among the columns of auto\_1:

```
mysql> SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, COLUMN_KEY
 -> FROM INFORMATION_SCHEMA.COLUMNS
 -> WHERE TABLE_NAME = "auto_1";
+-------------+------------------+-----------+------------+
| COLUMN_NAME | ORDINAL_POSITION | DATA_TYPE | COLUMN_KEY |
+-------------+------------------+-----------+------------+
| my_row_id | 1 | bigint | PRI |
| c1 | 2 | varchar | |
| c2 | 3 | int | |
+-------------+------------------+-----------+------------+
3 rows in set (0.01 sec)
```

After show\_gipk\_in\_create\_table\_and\_information\_schema is set to OFF, my\_row\_id can no longer be seen in the COLUMNS table, as shown here:

```
mysql> SET show_gipk_in_create_table_and_information_schema = OFF;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@show_gipk_in_create_table_and_information_schema;
+----------------------------------------------------+
| @@show_gipk_in_create_table_and_information_schema |
+----------------------------------------------------+
| 0 |
+----------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, COLUMN_KEY
 -> FROM INFORMATION_SCHEMA.COLUMNS
 -> WHERE TABLE_NAME = "auto_1";
+-------------+------------------+-----------+------------+
| COLUMN_NAME | ORDINAL_POSITION | DATA_TYPE | COLUMN_KEY |
+-------------+------------------+-----------+------------+
| c1 | 2 | varchar | |
| c2 | 3 | int | |
+-------------+------------------+-----------+------------+
2 rows in set (0.00 sec)
```

The setting for sql\_generate\_invisible\_primary\_key is not replicated, and is ignored by replication applier threads. This means that the setting of this variable on the source has no effect on the replica. In MySQL 8.0.32 and later, you can cause the replica to add a GIPK for tables replicated without primary keys on a given replication channel using REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK = GENERATE as part of a CHANGE REPLICATION SOURCE TO statement.

GIPKs work with row-based replication of [CREATE TABLE ... SELECT](#page-149-0); the information written to the binary log for this statement in such cases includes the GIPK definition, and thus is replicated correctly. Statement-based replication of CREATE TABLE ... SELECT is not supported with sql\_generate\_invisible\_primary\_key = ON.

When creating or importing backups of installations where GIPKs are in use, it is possible to exclude generated invisible primary key columns and values. The --skip-generated-invisibleprimary-key option for mysqldump causes GIPK information to be excluded in the program's output. If you are importing a dump file that contains generated invisible primary keys and values, you can also use --skip-generated-invisible-primary-key with mysqlpump to cause these to be suppressed (and thus not imported).

# <span id="page-174-0"></span>**15.1.20.12 Setting NDB Comment Options**

- [NDB\\_COLUMN Options](#page-175-0)
- [NDB\\_TABLE Options](#page-178-0)

 It is possible to set a number of options specific to NDB Cluster in the table comment or column comments of an NDB table. Table-level options for controlling read from any replica and partition balance can be embedded in a table comment using NDB\_TABLE.

NDB\_COLUMN can be used in a column comment to set the size of the blob parts table column used for storing parts of blob values by NDB to its maximum. This works for BLOB, MEDIUMBLOB, LONGBLOB, TEXT, MEDIUMTEXT, LONGTEXT, and JSON columns. Beginning with NDB 8.0.30, a column comment can also be used to control the inline size of a blob column. NDB\_COLUMN comments do not support TINYBLOB or TINYTEXT columns, since these have an inline part (only) of fixed size, and no separate parts to store elsewhere.

NDB\_TABLE can be used in a table comment to set options relating to partition balance and whether the table is fully replicated, among others.

The remainder of this section describes these options and their use.

#### <span id="page-175-0"></span>**NDB\_COLUMN Options**

 In NDB Cluster, a column comment in a CREATE TABLE or [ALTER TABLE](#page-64-1) statement can also be used to specify an NDB\_COLUMN option. Beginning with version 8.0.30, NDB supports two column comment options BLOB\_INLINE\_SIZE and MAX\_BLOB\_PART\_SIZE. (Prior to NDB 8.0.30, only MAX\_BLOB\_PART\_SIZE is supported.) Syntax for this option is shown here:

```
COMMENT 'NDB_COLUMN=speclist'
speclist := spec[,spec]
spec := 
 BLOB_INLINE_SIZE=value
 | MAX_BLOB_PART_SIZE[={0|1}]
```

BLOB\_INLINE\_SIZE specifies the number of bytes to be stored inline by the column; its expected value is an integer in the range 1 - 29980, inclusive. Setting a value greater than 29980 raises an error; setting a value less than 1 is allowed, but causes the default inline size for the column type to be used.

You should be aware that the maximum value for this option is actually the maximum number of bytes that can be stored in one row of an NDB table; every column in the row contributes to this total.

You should also keep in mind, especially when working with TEXT columns, that the value set by MAX\_BLOB\_PART\_SIZE or BLOB\_INLINE\_SIZE represents column size in bytes. It does not indicate the number of characters, which varies according to the character set and collation used by the column.

To see the effects of this option, first create a table with two BLOB columns, one (b1) with no extra options, and another (b2) with a setting for BLOB\_INLINE\_SIZE, as shown here:

```
mysql> CREATE TABLE t1 (
 -> a INT NOT NULL PRIMARY KEY,
 -> b1 BLOB,
 -> b2 BLOB COMMENT 'NDB_COLUMN=BLOB_INLINE_SIZE=8000'
 -> ) ENGINE NDB;
Query OK, 0 rows affected (0.32 sec)
```

You can see the BLOB\_INLINE\_SIZE settings for the BLOB columns by querying the ndbinfo.blobs table, like this:

```
mysql> SELECT
 -> column_name AS 'Column Name',
 -> inline_size AS 'Inline Size',
 -> part_size AS 'Blob Part Size'
 -> FROM ndbinfo.blobs
 -> WHERE table_name = 't1';
+-------------+-------------+----------------+
| Column Name | Inline Size | Blob Part Size |
+-------------+-------------+----------------+
| b1 | 256 | 2000 |
| b2 | 8000 | 2000 |
+-------------+-------------+----------------+
2 rows in set (0.01 sec)
```

You can also check the output from the ndb\_desc utility, as shown here, with the relevant lines displayed using emphasized text:

```
$> ndb_desc -d test t1
-- t --
Version: 1
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 3
Number of primary keys: 1
```

```
Length of frm data: 945
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
-- Attributes --
a Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY
b1 Blob(256,2000,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_64_1
b2 Blob(8000,2000,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_64_2
-- Indexes -- 
PRIMARY KEY(a) - UniqueHashIndex
PRIMARY(a) - OrderedIndex
```

BLOB\_INLINE\_SIZE has no effect on TINYBLOB columns. In NDB 8.0.41 and later, it is disallowed with TINYBLOB, and causes a warning if used.

For MAX\_BLOB\_PART\_SIZE, the = sign and the value following it are optional. Using any value other than 0 or 1 results in a syntax error.

The effect of using MAX\_BLOB\_PART\_SIZE in a column comment is to set the blob part size of a TEXT or BLOB column to the maximum number of bytes supported for this by NDB (13948). This option can be applied to any blob column type supported by MySQL except TINYBLOB or TINYTEXT (BLOB, MEDIUMBLOB, LONGBLOB, TEXT, MEDIUMTEXT, LONGTEXT). Unlike BLOB\_INLINE\_SIZE, MAX\_BLOB\_PART\_SIZE has no effect on JSON columns.

To see the effects of this option, we first run the following SQL statement in the mysql client to create a table with two BLOB columns, one (c1) with no extra options, and another (c2) with MAX\_BLOB\_PART\_SIZE:

```
mysql> CREATE TABLE test.t2 (
 -> p INT PRIMARY KEY,
 -> c1 BLOB,
 -> c2 BLOB COMMENT 'NDB_COLUMN=MAX_BLOB_PART_SIZE'
 -> ) ENGINE NDB;
Query OK, 0 rows affected (0.32 sec)
```

From the system shell, run the ndb\_desc utility to obtain information about the table just created, as shown in this example:

```
$> ndb_desc -d test t2
-- t --
Version: 1
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 3
Number of primary keys: 1
Length of frm data: 324
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
FragmentCount: 2
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
HashMap: DEFAULT-HASHMAP-3840-2
-- Attributes --
```

```
p Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY
c1 Blob(256,2000,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_22_1
c2 Blob(256,13948,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_22_2
-- Indexes -- 
PRIMARY KEY(p) - UniqueHashIndex
PRIMARY(p) - OrderedIndex
```

Column information in the output is listed under Attributes; for columns c1 and c2 it is displayed here in emphasized text. For c1, the blob part size is 2000, the default value; for c2, it is 13948, as set by MAX\_BLOB\_PART\_SIZE.

You can also query the ndbinfo.blobs table to see this, as shown here:

```
mysql> SELECT
 -> column_name AS 'Column Name',
 -> inline_size AS 'Inline Size',
 -> part_size AS 'Blob Part Size'
 -> FROM ndbinfo.blobs
 -> WHERE table_name = 't2';
+-------------+-------------+----------------+
| Column Name | Inline Size | Blob Part Size |
+-------------+-------------+----------------+
| c1 | 256 | 2000 |
| c2 | 256 | 13948 |
+-------------+-------------+----------------+
2 rows in set (0.00 sec)
```

You can change the blob part size for a given blob column of an NDB table using an ALTER TABLE statement such as this one, and verifying the changes afterwards using SHOW CREATE TABLE:

```
mysql> ALTER TABLE test.t2 
 -> DROP COLUMN c1, 
 -> ADD COLUMN c1 BLOB COMMENT 'NDB_COLUMN=MAX_BLOB_PART_SIZE',
 -> CHANGE COLUMN c2 c2 BLOB AFTER c1;
Query OK, 0 rows affected (0.47 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW CREATE TABLE test.t2\G
*************************** 1. row ***************************
 Table: t
Create Table: CREATE TABLE `t2` (
 `p` int(11) NOT NULL,
 `c1` blob COMMENT 'NDB_COLUMN=MAX_BLOB_PART_SIZE',
 `c2` blob,
 PRIMARY KEY (`p`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> EXIT
Bye
```

The output of ndb\_desc shows that the blob part sizes of the columns have been changed as expected:

```
$> ndb_desc -d test t2
-- t --
Version: 16777220
Fragment type: HashMapPartition
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 3
Number of primary keys: 1
Length of frm data: 324
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
FragmentCount: 2
```

```
ExtraRowGciBits: 0
ExtraRowAuthorBits: 0
TableStatus: Retrieved
HashMap: DEFAULT-HASHMAP-3840-2
-- Attributes --
p Int PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY
c1 Blob(256,13948,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_26_1
c2 Blob(256,2000,0) NULL AT=MEDIUM_VAR ST=MEMORY BV=2 BT=NDB$BLOB_26_2
-- Indexes -- 
PRIMARY KEY(p) - UniqueHashIndex
PRIMARY(p) - OrderedIndex
```

You can also see the change by running the query against ndbinfo.blobs again:

```
mysql> SELECT
 -> column_name AS 'Column Name',
 -> inline_size AS 'Inline Size',
 -> part_size AS 'Blob Part Size'
 -> FROM ndbinfo.blobs
 -> WHERE table_name = 't2';
+-------------+-------------+----------------+
| Column Name | Inline Size | Blob Part Size |
+-------------+-------------+----------------+
| c1 | 256 | 13948 |
| c2 | 256 | 2000 |
+-------------+-------------+----------------+
2 rows in set (0.00 sec)
```

It is possible to set both BLOB\_INLINE\_SIZE and MAX\_BLOB\_PART\_SIZE for a blob column, as shown in this CREATE TABLE statement:

```
mysql> CREATE TABLE test.t3 (
 -> p INT NOT NULL PRIMARY KEY,
 -> c1 JSON,
 -> c2 JSON COMMENT 'NDB_COLUMN=BLOB_INLINE_SIZE=5000,MAX_BLOB_PART_SIZE'
 -> ) ENGINE NDB;
Query OK, 0 rows affected (0.28 sec)
```

Querying the blobs table shows us that the statement worked as expected:

```
mysql> SELECT
 -> column_name AS 'Column Name',
 -> inline_size AS 'Inline Size',
 -> part_size AS 'Blob Part Size'
 -> FROM ndbinfo.blobs
 -> WHERE table_name = 't3';
+-------------+-------------+----------------+
| Column Name | Inline Size | Blob Part Size |
+-------------+-------------+----------------+
| c1 | 4000 | 8100 |
| c2 | 5000 | 8100 |
+-------------+-------------+----------------+
2 rows in set (0.00 sec)
```

You can also verify that the statement worked by checking the output of ndb\_desc.

Changing a column's blob part size must be done using a copying ALTER TABLE; this operation cannot be performed online (see Section 25.6.12, "Online Operations with ALTER TABLE in NDB Cluster").

For more information about how NDB stores columns of blob types, see String Type Storage Requirements.

# <span id="page-178-0"></span>**NDB\_TABLE Options**

 For an NDB Cluster table, the table comment in a CREATE TABLE or [ALTER TABLE](#page-64-1) statement can also be used to specify an NDB\_TABLE option, which consists of one or more name-value pairs, separated by commas if need be, following the string NDB\_TABLE=. Complete syntax for names and values syntax is shown here:

```
COMMENT="NDB_TABLE=ndb_table_option[,ndb_table_option[,...]]"
ndb_table_option: {
 NOLOGGING={1 | 0}
 | READ_BACKUP={1 | 0}
 | PARTITION_BALANCE={FOR_RP_BY_NODE | FOR_RA_BY_NODE | FOR_RP_BY_LDM
 | FOR_RA_BY_LDM | FOR_RA_BY_LDM_X_2
 | FOR_RA_BY_LDM_X_3 | FOR_RA_BY_LDM_X_4}
 | FULLY_REPLICATED={1 | 0}
}
```

Spaces are not permitted within the quoted string. The string is case-insensitive.

The four NDB table options that can be set as part of a comment in this way are described in more detail in the next few paragraphs.

NOLOGGING: By default, NDB tables are logged, and checkpointed. This makes them durable to whole cluster failures. Using NOLOGGING when creating or altering a table means that this table is not redo logged or included in local checkpoints. In this case, the table is still replicated across the data nodes for high availability, and updated using transactions, but changes made to it are not recorded in the data node's redo logs, and its content is not checkpointed to disk; when recovering from a cluster failure, the cluster retains the table definition, but none of its rows—that is, the table is empty.

Using such nonlogging tables reduces the data node's demands on disk I/O and storage, as well as CPU for checkpointing CPU. This may be suitable for short-lived data which is frequently updated, and where the loss of all data in the unlikely event of a total cluster failure is acceptable.

It is also possible to use the ndb\_table\_no\_logging system variable to cause any NDB tables created or altered while this variable is in effect to behave as though it had been created with the NOLOGGING comment. Unlike when using the comment directly, there is nothing in this case in the output of SHOW CREATE TABLE to indicate that it is a nonlogging table. Using the table comment approach is recommended since it offers per-table control of the feature, and this aspect of the table schema is embedded in the table creation statement where it can be found easily by SQL-based tools.

READ\_BACKUP: Setting this option to 1 has the same effect as though ndb\_read\_backup were enabled; enables reading from any replica. Doing so greatly improves the performance of reads from the table at a relatively small cost to write performance. Beginning with NDB 8.0.19, 1 is the default for READ\_BACKUP, and the default for ndb\_read\_backup is ON (previously, read from any replica was disabled by default).

You can set READ\_BACKUP for an existing table online, using an ALTER TABLE statement similar to one of those shown here:

```
ALTER TABLE ... ALGORITHM=INPLACE, COMMENT="NDB_TABLE=READ_BACKUP=1";
ALTER TABLE ... ALGORITHM=INPLACE, COMMENT="NDB_TABLE=READ_BACKUP=0";
```

For more information about the ALGORITHM option for ALTER TABLE, see Section 25.6.12, "Online Operations with ALTER TABLE in NDB Cluster".

PARTITION\_BALANCE: Provides additional control over assignment and placement of partitions. The following four schemes are supported:

1. FOR\_RP\_BY\_NODE: One partition per node.

Only one LDM on each node stores a primary partition. Each partition is stored in the same LDM (same ID) on all nodes.

2. FOR\_RA\_BY\_NODE: One partition per node group.

Each node stores a single partition, which can be either a primary replica or a backup replica. Each partition is stored in the same LDM on all nodes.

3. FOR\_RP\_BY\_LDM: One partition for each LDM on each node; the default.

This is the setting used if READ\_BACKUP is set to 1.

4. FOR\_RA\_BY\_LDM: One partition per LDM in each node group.

These partitions can be primary or backup partitions.

5. FOR\_RA\_BY\_LDM\_X\_2: Two partitions per LDM in each node group.

These partitions can be primary or backup partitions.

6. FOR\_RA\_BY\_LDM\_X\_3: Three partitions per LDM in each node group.

These partitions can be primary or backup partitions.

7. FOR\_RA\_BY\_LDM\_X\_4: Four partitions per LDM in each node group.

These partitions can be primary or backup partitions.

PARTITION\_BALANCE is the preferred interface for setting the number of partitions per table. Using MAX\_ROWS to force the number of partitions is deprecated but continues to be supported for backward compatibility; it is subject to removal in a future release of MySQL NDB Cluster. (Bug #81759, Bug #23544301)

FULLY\_REPLICATED controls whether the table is fully replicated, that is, whether each data node has a complete copy of the table. To enable full replication of the table, use FULLY\_REPLICATED=1.

This setting can also be controlled using the ndb\_fully\_replicated system variable. Setting it to ON enables the option by default for all new NDB tables; the default is OFF. The ndb\_data\_node\_neighbour system variable is also used for fully replicated tables, to ensure that when a fully replicated table is accessed, we access the data node which is local to this MySQL Server.

An example of a CREATE TABLE statement using such a comment when creating an NDB table is shown here:

```
mysql> CREATE TABLE t1 (
 > c1 INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 > c2 VARCHAR(100),
 > c3 VARCHAR(100) )
 > ENGINE=NDB
 >
COMMENT="NDB_TABLE=READ_BACKUP=0,PARTITION_BALANCE=FOR_RP_BY_NODE";
```

The comment is displayed as part of the output of SHOW CREATE TABLE. The text of the comment is also available from querying the MySQL Information Schema TABLES table, as in this example:

```
mysql> SELECT TABLE_NAME, TABLE_SCHEMA, TABLE_COMMENT
 > FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME="t1"\G
*************************** 1. row ***************************
 TABLE_NAME: t1
 TABLE_SCHEMA: test
TABLE_COMMENT: NDB_TABLE=READ_BACKUP=0,PARTITION_BALANCE=FOR_RP_BY_NODE
1 row in set (0.01 sec)
```

This comment syntax is also supported with [ALTER TABLE](#page-64-1) statements for NDB tables, as shown here:

```
mysql> ALTER TABLE t1 COMMENT="NDB_TABLE=PARTITION_BALANCE=FOR_RA_BY_NODE";
Query OK, 0 rows affected (0.40 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

Beginning with NDB 8.0.21, the TABLE\_COMMENT column displays the comment that is required to recreate the table as it is following the ALTER TABLE statement, like this:

```
mysql> SELECT TABLE_NAME, TABLE_SCHEMA, TABLE_COMMENT
 -> FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME="t1"\G
```

```
*************************** 1. row ***************************
 TABLE_NAME: t1
 TABLE_SCHEMA: test
TABLE_COMMENT: NDB_TABLE=READ_BACKUP=0,PARTITION_BALANCE=FOR_RP_BY_NODE
1 row in set (0.01 sec)
mysql> SELECT TABLE_NAME, TABLE_SCHEMA, TABLE_COMMENT
 > FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME="t1";
+------------+--------------+--------------------------------------------------+
| TABLE_NAME | TABLE_SCHEMA | TABLE_COMMENT |
+------------+--------------+--------------------------------------------------+
| t1 | c | NDB_TABLE=PARTITION_BALANCE=FOR_RA_BY_NODE |
| t1 | d | |
+------------+--------------+--------------------------------------------------+
```

Keep in mind that a table comment used with ALTER TABLE replaces any existing comment which the table might have.

```
mysql> ALTER TABLE t1 COMMENT="NDB_TABLE=PARTITION_BALANCE=FOR_RA_BY_NODE";
Query OK, 0 rows affected (0.40 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SELECT TABLE_NAME, TABLE_SCHEMA, TABLE_COMMENT
 > FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME="t1";
+------------+--------------+--------------------------------------------------+
| TABLE_NAME | TABLE_SCHEMA | TABLE_COMMENT |
+------------+--------------+--------------------------------------------------+
| t1 | c | NDB_TABLE=PARTITION_BALANCE=FOR_RA_BY_NODE |
| t1 | d | |
+------------+--------------+--------------------------------------------------+
2 rows in set (0.01 sec)
```

Prior to NDB 8.0.21, the table comment used with ALTER TABLE replaced any existing comment which the table might have had. This meant that (for example) the READ\_BACKUP value was not carried over to the new comment set by the ALTER TABLE statement, and that any unspecified values reverted to their defaults. (BUG#30428829) There was thus no longer any way using SQL to retrieve the value previously set for the comment. To keep comment values from reverting to their defaults, it was necessary to preserve any such values from the existing comment string and include them in the comment passed to ALTER TABLE.

You can also see the value of the PARTITION\_BALANCE option in the output of ndb\_desc. ndb\_desc also shows whether the READ\_BACKUP and FULLY\_REPLICATED options are set for the table. See the description of this program for more information.

# <span id="page-181-0"></span>**15.1.21 CREATE TABLESPACE Statement**

2 rows in set (0.01 sec)

```
CREATE [UNDO] TABLESPACE tablespace_name
 InnoDB and NDB:
 [ADD DATAFILE 'file_name']
 [AUTOEXTEND_SIZE [=] value]
 InnoDB only:
 [FILE_BLOCK_SIZE = value]
 [ENCRYPTION [=] {'Y' | 'N'}]
 NDB only:
 USE LOGFILE GROUP logfile_group
 [EXTENT_SIZE [=] extent_size]
 [INITIAL_SIZE [=] initial_size]
 [MAX_SIZE [=] max_size]
 [NODEGROUP [=] nodegroup_id]
 [WAIT]
 [COMMENT [=] 'string']
 InnoDB and NDB:
 [ENGINE [=] engine_name]
```

```
 Reserved for future use:
 [ENGINE_ATTRIBUTE [=] 'string']
```

This statement is used to create a tablespace. The precise syntax and semantics depend on the storage engine used. In standard MySQL releases, this is always an InnoDB tablespace. MySQL NDB Cluster also supports tablespaces using the NDB storage engine.

- [Considerations for InnoDB](#page-182-0)
- [Considerations for NDB Cluster](#page-182-1)
- [Options](#page-183-0)
- [Notes](#page-186-0)
- [InnoDB Examples](#page-187-0)
- [NDB Example](#page-187-1)

# <span id="page-182-0"></span>**Considerations for InnoDB**

[CREATE TABLESPACE](#page-181-0) syntax is used to create general tablespaces or undo tablespaces. The UNDO keyword, introduced in MySQL 8.0.14, must be specified to create an undo tablespace.

A general tablespace is a shared tablespace. It can hold multiple tables, and supports all table row formats. General tablespaces can be created in a location relative to or independent of the data directory.

After creating an InnoDB general tablespace, use CREATE TABLE tbl\_name [... TABLESPACE](#page-121-0) [=] [tablespace\\_name](#page-121-0) or ALTER TABLE tbl\_name [TABLESPACE \[=\]](#page-64-1) tablespace\_name to add tables to the tablespace. For more information, see Section 17.6.3.3, "General Tablespaces".

Undo tablespaces contain undo logs. Undo tablespaces can be created in a chosen location by specifying a fully qualified data file path. For more information, see Section 17.6.3.4, "Undo Tablespaces".

# <span id="page-182-1"></span>**Considerations for NDB Cluster**

This statement is used to create a tablespace, which can contain one or more data files, providing storage space for NDB Cluster Disk Data tables (see Section 25.6.11, "NDB Cluster Disk Data Tables"). One data file is created and added to the tablespace using this statement. Additional data files may be added to the tablespace by using the [ALTER TABLESPACE](#page-87-0) statement (see [Section 15.1.10, "ALTER TABLESPACE Statement"\)](#page-87-0).

![](_page_182_Picture_16.jpeg)

#### **Note**

All NDB Cluster Disk Data objects share the same namespace. This means that each Disk Data object must be uniquely named (and not merely each Disk Data object of a given type). For example, you cannot have a tablespace and a log file group with the same name, or a tablespace and a data file with the same name.

A log file group of one or more UNDO log files must be assigned to the tablespace to be created with the USE LOGFILE GROUP clause. logfile\_group must be an existing log file group created with [CREATE LOGFILE GROUP](#page-109-0) (see [Section 15.1.16, "CREATE LOGFILE GROUP Statement"](#page-109-0)). Multiple tablespaces may use the same log file group for UNDO logging.

When setting EXTENT\_SIZE or INITIAL\_SIZE, you may optionally follow the number with a oneletter abbreviation for an order of magnitude, similar to those used in my.cnf. Generally, this is one of the letters M (for megabytes) or G (for gigabytes).

INITIAL\_SIZE and EXTENT\_SIZE are subject to rounding as follows:

- EXTENT\_SIZE is rounded up to the nearest whole multiple of 32K.
- INITIAL\_SIZE is rounded down to the nearest whole multiple of 32K; this result is rounded up to the nearest whole multiple of EXTENT\_SIZE (after any rounding).

![](_page_183_Picture_4.jpeg)

#### **Note**

NDB reserves 4% of a tablespace for data node restart operations. This reserved space cannot be used for data storage.

The rounding just described is done explicitly, and a warning is issued by the MySQL Server when any such rounding is performed. The rounded values are also used by the NDB kernel for calculating INFORMATION\_SCHEMA.FILES column values and other purposes. However, to avoid an unexpected result, we suggest that you always use whole multiples of 32K in specifying these options.

When [CREATE TABLESPACE](#page-181-0) is used with ENGINE [=] NDB, a tablespace and associated data file are created on each Cluster data node. You can verify that the data files were created and obtain information about them by querying the Information Schema FILES table. (See the example later in this section.)

(See Section 28.3.15, "The INFORMATION\_SCHEMA FILES Table".)

# <span id="page-183-0"></span>**Options**

• ADD DATAFILE: Defines the name of a tablespace data file. This option is always required when creating an NDB tablespace; for InnoDB in MySQL 8.0.14 and later, it is required only when creating an undo tablespace. The file\_name, including any specified path, must be quoted with single or double quotation marks. File names (not counting the file extension) and directory names must be at least one byte in length. Zero length file names and directory names are not supported.

Because there are considerable differences in how InnoDB and NDB treat data files, the two storage engines are covered separately in the discussion that follows.

**InnoDB data files.** An InnoDB tablespace supports only a single data file, whose name must include a .ibd extension.

To place an InnoDB general tablespace data file in a location outside of the data directory, include a fully qualified path or a path relative to the data directory. Only a fully qualified path is permitted for undo tablespaces. If you do not specify a path, a general tablespace is created in the data directory. An undo tablespace created without specifying a path is created in the directory defined by the innodb\_undo\_directory variable. If the innodb\_undo\_directory variable is undefined, undo tablespaces are created in the data directory.

To avoid conflicts with implicitly created file-per-table tablespaces, creating an InnoDB general tablespace in a subdirectory under the data directory is not supported. When creating a general tablespace or undo tablespace outside of the data directory, the directory must exist and must be known to InnoDB prior to creating the tablespace. To make a directory known to InnoDB, add it to the innodb\_directories value or to one of the variables whose values are appended to the innodb\_directories value. innodb\_directories is a read-only variable. Configuring it requires restarting the server.

If the ADD DATAFILE clause is not specified when creating an InnoDB tablespace, a tablespace data file with a unique file name is created implicitly. The unique file name is a 128 bit UUID formatted into five groups of hexadecimal numbers separated by dashes (aaaaaaaa-bbbb-ccccdddd-eeeeeeeeeeee). A file extension is added if required by the storage engine. An .ibd file extension is added for InnoDB general tablespace data files. In a replication environment, the data file name created on the replication source server is not the same as the data file name created on the replica.

As of MySQL 8.0.17, the ADD DATAFILE clause does not permit circular directory references when creating an InnoDB tablespace. For example, the circular directory reference (/../) in the following statement is not permitted:

```
CREATE TABLESPACE ts1 ADD DATAFILE ts1.ibd 'any_directory/../ts1.ibd';
```

An exception to this restriction exists on Linux, where a circular directory reference is permitted if the preceding directory is a symbolic link. For example, the data file path in the example above is permitted if any\_directory is a symbolic link. (It is still permitted for data file paths to begin with '../'.)

**NDB data files.** An NDB tablespace supports multiple data files which can have any legal file names; more data files can be added to an NDB Cluster tablespace following its creation by using an [ALTER TABLESPACE](#page-87-0) statement.

An NDB tablespace data file is created by default in the data node file system directory—that is, the directory named ndb\_nodeid\_fs/TS under the data node's data directory (DataDir), where nodeid is the data node's NodeId. To place the data file in a location other than the default, include an absolute directory path or a path relative to the default location. If the directory specified does not exist, NDB attempts to create it; the system user account under which the data node process is running must have the appropriate permissions to do so.

![](_page_184_Picture_6.jpeg)

#### **Note**

When determining the path used for a data file, NDB does not expand the ~ (tilde) character.

When multiple data nodes are run on the same physical host, the following considerations apply:

- You cannot specify an absolute path when creating a data file.
- It is not possible to create tablespace data files outside the data node file system directory, unless each data node has a separate data directory.
- If each data node has its own data directory, data files can be created anywhere within this directory.
- If each data node has its own data directory, it may also be possible to create a data file outside the node's data directory using a relative path, as long as this path resolves to a unique location on the host file system for each data node running on that host.
- FILE\_BLOCK\_SIZE: This option—which is specific to InnoDB general tablespaces, and is ignored by NDB—defines the block size for the tablespace data file. Values can be specified in bytes or kilobytes. For example, an 8 kilobyte file block size can be specified as 8192 or 8K. If you do not specify this option, FILE\_BLOCK\_SIZE defaults to the innodb\_page\_size value. FILE\_BLOCK\_SIZE is required when you intend to use the tablespace for storing compressed InnoDB tables (ROW\_FORMAT=COMPRESSED). In this case, you must define the tablespace FILE\_BLOCK\_SIZE when creating the tablespace.

If FILE\_BLOCK\_SIZE is equal the innodb\_page\_size value, the tablespace can contain only tables having an uncompressed row format (COMPACT, REDUNDANT, and DYNAMIC). Tables with a COMPRESSED row format have a different physical page size than uncompressed tables. Therefore, compressed tables cannot coexist in the same tablespace as uncompressed tables.

For a general tablespace to contain compressed tables, FILE\_BLOCK\_SIZE must be specified, and the FILE\_BLOCK\_SIZE value must be a valid compressed page size in relation to the innodb\_page\_size value. Also, the physical page size of the compressed table (KEY\_BLOCK\_SIZE) must be equal to FILE\_BLOCK\_SIZE/1024. For example, if innodb\_page\_size=16K, and FILE\_BLOCK\_SIZE=8K, the KEY\_BLOCK\_SIZE of the table must be 8. For more information, see Section 17.6.3.3, "General Tablespaces".

- USE LOGFILE GROUP: Required for NDB, this is the name of a log file group previously created using [CREATE LOGFILE GROUP](#page-109-0). Not supported for InnoDB, where it fails with an error.
- EXTENT\_SIZE: This option is specific to NDB, and is not supported by InnoDB, where it fails with an error. EXTENT\_SIZE sets the size, in bytes, of the extents used by any files belonging to the tablespace. The default value is 1M. The minimum size is 32K, and theoretical maximum is 2G, although the practical maximum size depends on a number of factors. In most cases, changing the extent size does not have any measurable effect on performance, and the default value is recommended for all but the most unusual situations.

An extent is a unit of disk space allocation. One extent is filled with as much data as that extent can contain before another extent is used. In theory, up to 65,535 (64K) extents may used per data file; however, the recommended maximum is 32,768 (32K). The recommended maximum size for a single data file is 32G—that is, 32K extents × 1 MB per extent. In addition, once an extent is allocated to a given partition, it cannot be used to store data from a different partition; an extent cannot store data from more than one partition. This means, for example that a tablespace having a single datafile whose INITIAL\_SIZE (described in the following item) is 256 MB and whose EXTENT\_SIZE is 128M has just two extents, and so can be used to store data from at most two different disk data table partitions.

You can see how many extents remain free in a given data file by querying the Information Schema FILES table, and so derive an estimate for how much space remains free in the file. For further discussion and examples, see Section 28.3.15, "The INFORMATION\_SCHEMA FILES Table".

• INITIAL\_SIZE: This option is specific to NDB, and is not supported by InnoDB, where it fails with an error.

The INITIAL\_SIZE parameter sets the total size in bytes of the data file that was specific using ADD DATATFILE. Once this file has been created, its size cannot be changed; however, you can add more data files to the tablespace using [ALTER TABLESPACE ... ADD DATAFILE](#page-87-0).

INITIAL\_SIZE is optional; its default value is 134217728 (128 MB).

On 32-bit systems, the maximum supported value for INITIAL\_SIZE is 4294967296 (4 GB).

• AUTOEXTEND\_SIZE: Ignored by MySQL prior to MySQL 8.0.23; From MySQL 8.0.23, defines the amount by which InnoDB extends the size of the tablespace when it becomes full. The setting must be a multiple of 4MB. The default setting is 0, which causes the tablespace to be extended according to the implicit default behavior. For more information, see Section 17.6.3.9, "Tablespace AUTOEXTEND\_SIZE Configuration".

Has no effect in any release of MySQL NDB Cluster 8.0, regardless of the storage engine used.

- MAX\_SIZE: Currently ignored by MySQL; reserved for possible future use. Has no effect in any release of MySQL 8.0 or MySQL NDB Cluster 8.0, regardless of the storage engine used.
- NODEGROUP: Currently ignored by MySQL; reserved for possible future use. Has no effect in any release of MySQL 8.0 or MySQL NDB Cluster 8.0, regardless of the storage engine used.
- WAIT: Currently ignored by MySQL; reserved for possible future use. Has no effect in any release of MySQL 8.0 or MySQL NDB Cluster 8.0, regardless of the storage engine used.
- COMMENT: Currently ignored by MySQL; reserved for possible future use. Has no effect in any release of MySQL 8.0 or MySQL NDB Cluster 8.0, regardless of the storage engine used.
- The ENCRYPTION clause enables or disables page-level data encryption for an InnoDB general tablespace. Encryption support for general tablespaces was introduced in MySQL 8.0.13.

As of MySQL 8.0.16, if the ENCRYPTION clause is not specified, the default\_table\_encryption setting controls whether encryption is enabled. The ENCRYPTION clause overrides the default\_table\_encryption setting. However, if the table\_encryption\_privilege\_check

variable is enabled, the TABLE\_ENCRYPTION\_ADMIN privilege is required to use an ENCRYPTION clause setting that differs from the default\_table\_encryption setting.

A keyring plugin must be installed and configured before an encryption-enabled tablespace can be created.

When a general tablespace is encrypted, all tables residing in the tablespace are encrypted. Likewise, a table created in an encrypted tablespace is encrypted.

For more information, see Section 17.13, "InnoDB Data-at-Rest Encryption"

- ENGINE: Defines the storage engine which uses the tablespace, where engine\_name is the name of the storage engine. Currently, only the InnoDB storage engine is supported by standard MySQL 8.0 releases. MySQL NDB Cluster supports both NDB and InnoDB tablespaces. The value of the default\_storage\_engine system variable is used for ENGINE if the option is not specified.
- The ENGINE\_ATTRIBUTE option (available as of MySQL 8.0.21) is used to specify tablespace attributes for primary storage engines. The option is reserved for future use.

Permitted values are a string literal containing a valid JSON document or an empty string (''). Invalid JSON is rejected.

```
CREATE TABLESPACE ts1 ENGINE_ATTRIBUTE='{"key":"value"}';
```

ENGINE\_ATTRIBUTE values can be repeated without error. In this case, the last specified value is used.

ENGINE\_ATTRIBUTE values are not checked by the server, nor are they cleared when the table's storage engine is changed.

# <span id="page-186-0"></span>**Notes**

- For the rules covering the naming of MySQL tablespaces, see Section 11.2, "Schema Object Names". In addition to these rules, the slash character ("/") is not permitted, nor can you use names beginning with innodb\_, as this prefix is reserved for system use.
- Creation of temporary general tablespaces is not supported.
- General tablespaces do not support temporary tables.
- The TABLESPACE option may be used with [CREATE TABLE](#page-121-0) or [ALTER TABLE](#page-64-1) to assign an InnoDB table partition or subpartition to a file-per-table tablespace. All partitions must belong to the same storage engine. Assigning table partitions to shared InnoDB tablespaces is not supported. Shared tablespaces include the InnoDB system tablespace and general tablespaces.
- General tablespaces support the addition of tables of any row format using [CREATE TABLE ...](#page-121-0) [TABLESPACE](#page-121-0). innodb\_file\_per\_table does not need to be enabled.
- innodb\_strict\_mode is not applicable to general tablespaces. Tablespace management rules are strictly enforced independently of innodb\_strict\_mode. If CREATE TABLESPACE parameters are incorrect or incompatible, the operation fails regardless of the innodb\_strict\_mode setting. When a table is added to a general tablespace using [CREATE TABLE ... TABLESPACE](#page-121-0) or [ALTER](#page-64-1) [TABLE ... TABLESPACE](#page-64-1), innodb\_strict\_mode is ignored but the statement is evaluated as if innodb\_strict\_mode is enabled.
- Use DROP TABLESPACE to remove a tablespace. All tables must be dropped from a tablespace using [DROP TABLE](#page-198-0) prior to dropping the tablespace. Before dropping an NDB Cluster tablespace you must also remove all its data files using one or more [ALTER TABLESPACE ... DROP](#page-87-0) [DATATFILE](#page-87-0) statements. See Section 25.6.11.1, "NDB Cluster Disk Data Objects".
- All parts of an InnoDB table added to an InnoDB general tablespace reside in the general tablespace, including indexes and BLOB pages.

For an NDB table assigned to a tablespace, only those columns which are not indexed are stored on disk, and actually use the tablespace data files. Indexes and indexed columns for all NDB tables are always kept in memory.

- Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is for file-per-table tablespaces.
- A general tablespace is not associated with any database or schema.
- [ALTER TABLE ... DISCARD TABLESPACE](#page-64-1) and [ALTER TABLE ...IMPORT TABLESPACE](#page-64-1) are not supported for tables that belong to a general tablespace.
- The server uses tablespace-level metadata locking for DDL that references general tablespaces. By comparison, the server uses table-level metadata locking for DDL that references file-per-table tablespaces.
- A generated or existing tablespace cannot be changed to a general tablespace.
- There is no conflict between general tablespace names and file-per-table tablespace names. The "/" character, which is present in file-per-table tablespace names, is not permitted in general tablespace names.
- mysqldump and mysqlpump do not dump InnoDB [CREATE TABLESPACE](#page-181-0) statements.

# <span id="page-187-0"></span>**InnoDB Examples**

This example demonstrates creating a general tablespace and adding three uncompressed tables of different row formats.

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' ENGINE=INNODB;
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 ROW_FORMAT=REDUNDANT;
mysql> CREATE TABLE t2 (c1 INT PRIMARY KEY) TABLESPACE ts1 ROW_FORMAT=COMPACT;
mysql> CREATE TABLE t3 (c1 INT PRIMARY KEY) TABLESPACE ts1 ROW_FORMAT=DYNAMIC;
```

This example demonstrates creating a general tablespace and adding a compressed table. The example assumes a default innodb\_page\_size value of 16K. The FILE\_BLOCK\_SIZE of 8192 requires that the compressed table have a KEY\_BLOCK\_SIZE of 8.

```
mysql> CREATE TABLESPACE `ts2` ADD DATAFILE 'ts2.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;
mysql> CREATE TABLE t4 (c1 INT PRIMARY KEY) TABLESPACE ts2 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
```

This example demonstrates creating a general tablespace without specifying the ADD DATAFILE clause, which is optional as of MySQL 8.0.14.

```
mysql> CREATE TABLESPACE `ts3` ENGINE=INNODB;
```

This example demonstrates creating an undo tablespace.

```
mysql> CREATE UNDO TABLESPACE undo_003 ADD DATAFILE 'undo_003.ibu';
```

# <span id="page-187-1"></span>**NDB Example**

Suppose that you wish to create an NDB Cluster Disk Data tablespace named myts using a datafile named mydata-1.dat. An NDB tablespace always requires the use of a log file group consisting of one or more undo log files. For this example, we first create a log file group named mylg that contains one undo long file named myundo-1.dat, using the [CREATE LOGFILE GROUP](#page-109-0) statement shown here:

```
mysql> CREATE LOGFILE GROUP myg1
 -> ADD UNDOFILE 'myundo-1.dat'
 -> ENGINE=NDB;
Query OK, 0 rows affected (3.29 sec)
```

Now you can create the tablespace previously described using the following statement:

```
mysql> CREATE TABLESPACE myts
 -> ADD DATAFILE 'mydata-1.dat'
 -> USE LOGFILE GROUP mylg
 -> ENGINE=NDB;
Query OK, 0 rows affected (2.98 sec)
```

You can now create a Disk Data table using a [CREATE TABLE](#page-121-0) statement with the TABLESPACE and STORAGE DISK options, similar to what is shown here:

```
mysql> CREATE TABLE mytable (
 -> id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> lname VARCHAR(50) NOT NULL,
 -> fname VARCHAR(50) NOT NULL,
 -> dob DATE NOT NULL,
 -> joined DATE NOT NULL,
 -> INDEX(last_name, first_name)
 -> )
 -> TABLESPACE myts STORAGE DISK
 -> ENGINE=NDB;
Query OK, 0 rows affected (1.41 sec)
```

It is important to note that only the dob and joined columns from mytable are actually stored on disk, due to the fact that the id, lname, and fname columns are all indexed.

As mentioned previously, when CREATE TABLESPACE is used with ENGINE [=] NDB, a tablespace and associated data file are created on each NDB Cluster data node. You can verify that the data files were created and obtain information about them by querying the Information Schema FILES table, as shown here:

```
mysql> SELECT FILE_NAME, FILE_TYPE, LOGFILE_GROUP_NAME, STATUS, EXTRA
 -> FROM INFORMATION_SCHEMA.FILES
 -> WHERE TABLESPACE_NAME = 'myts';
+--------------+------------+--------------------+--------+----------------+
| file_name | file_type | logfile_group_name | status | extra |
+--------------+------------+--------------------+--------+----------------+
| mydata-1.dat | DATAFILE | mylg | NORMAL | CLUSTER_NODE=5 |
| mydata-1.dat | DATAFILE | mylg | NORMAL | CLUSTER_NODE=6 |
| NULL | TABLESPACE | mylg | NORMAL | NULL |
+--------------+------------+--------------------+--------+----------------+
3 rows in set (0.01 sec)
```

For additional information and examples, see Section 25.6.11.1, "NDB Cluster Disk Data Objects".

# <span id="page-188-0"></span>**15.1.22 CREATE TRIGGER Statement**

```
CREATE
 [DEFINER = user]
 TRIGGER [IF NOT EXISTS] trigger_name
 trigger_time trigger_event
 ON tbl_name FOR EACH ROW
 [trigger_order]
 trigger_body
trigger_time: { BEFORE | AFTER }
trigger_event: { INSERT | UPDATE | DELETE }
trigger_order: { FOLLOWS | PRECEDES } other_trigger_name
```

This statement creates a new trigger. A trigger is a named database object that is associated with a table, and that activates when a particular event occurs for the table. The trigger becomes associated with the table named tbl\_name, which must refer to a permanent table. You cannot associate a trigger with a TEMPORARY table or a view.

Trigger names exist in the schema namespace, meaning that all triggers must have unique names within a schema. Triggers in different schemas can have the same name.

IF NOT EXISTS prevents an error from occurring if a trigger having the same name, on the same table, exists in the same schema. This option is supported with CREATE TRIGGER beginning with MySQL 8.0.29.

This section describes [CREATE TRIGGER](#page-188-0) syntax. For additional discussion, see Section 27.3.1, "Trigger Syntax and Examples".

[CREATE TRIGGER](#page-188-0) requires the TRIGGER privilege for the table associated with the trigger. If the DEFINER clause is present, the privileges required depend on the user value, as discussed in Section 27.6, "Stored Object Access Control". If binary logging is enabled, [CREATE TRIGGER](#page-188-0) might require the SUPER privilege, as discussed in Section 27.7, "Stored Program Binary Logging".

The DEFINER clause determines the security context to be used when checking access privileges at trigger activation time, as described later in this section.

trigger\_time is the trigger action time. It can be BEFORE or AFTER to indicate that the trigger activates before or after each row to be modified.

Basic column value checks occur prior to trigger activation, so you cannot use BEFORE triggers to convert values inappropriate for the column type to valid values.

trigger\_event indicates the kind of operation that activates the trigger. These trigger\_event values are permitted:

- INSERT: The trigger activates whenever a new row is inserted into the table (for example, through INSERT, LOAD DATA, and REPLACE statements).
- UPDATE: The trigger activates whenever a row is modified (for example, through UPDATE statements).
- DELETE: The trigger activates whenever a row is deleted from the table (for example, through DELETE and REPLACE statements). [DROP TABLE](#page-198-0) and TRUNCATE TABLE statements on the table do not activate this trigger, because they do not use DELETE. Dropping a partition does not activate DELETE triggers, either.

The trigger\_event does not represent a literal type of SQL statement that activates the trigger so much as it represents a type of table operation. For example, an INSERT trigger activates not only for INSERT statements but also LOAD DATA statements because both statements insert rows into a table.

A potentially confusing example of this is the INSERT INTO ... ON DUPLICATE KEY UPDATE ... syntax: a BEFORE INSERT trigger activates for every row, followed by either an AFTER INSERT trigger or both the BEFORE UPDATE and AFTER UPDATE triggers, depending on whether there was a duplicate key for the row.

![](_page_189_Picture_15.jpeg)

#### **Note**

Cascaded foreign key actions do not activate triggers.

It is possible to define multiple triggers for a given table that have the same trigger event and action time. For example, you can have two BEFORE UPDATE triggers for a table. By default, triggers that have the same trigger event and action time activate in the order they were created. To affect trigger order, specify a trigger\_order clause that indicates FOLLOWS or PRECEDES and the name of an existing trigger that also has the same trigger event and action time. With FOLLOWS, the new trigger activates after the existing trigger. With PRECEDES, the new trigger activates before the existing trigger. trigger\_body is the statement to execute when the trigger activates. To execute multiple statements, use the BEGIN ... END compound statement construct. This also enables you to use the same statements that are permitted within stored routines. See Section 15.6.1, "BEGIN ... END Compound Statement". Some statements are not permitted in triggers; see Section 27.8, "Restrictions on Stored Programs".

Within the trigger body, you can refer to columns in the subject table (the table associated with the trigger) by using the aliases OLD and NEW. OLD.col\_name refers to a column of an existing row before it is updated or deleted. NEW.col\_name refers to the column of a new row to be inserted or an existing row after it is updated.

Triggers cannot use NEW.col\_name or use OLD.col\_name to refer to generated columns. For information about generated columns, see [Section 15.1.20.8, "CREATE TABLE and Generated](#page-162-0) [Columns".](#page-162-0)

MySQL stores the sql\_mode system variable setting in effect when a trigger is created, and always executes the trigger body with this setting in force, regardless of the current server SQL mode when the trigger begins executing.

The DEFINER clause specifies the MySQL account to be used when checking access privileges at trigger activation time. If the DEFINER clause is present, the user value should be a MySQL account specified as 'user\_name'@'host\_name', CURRENT\_USER, or CURRENT\_USER(). The permitted user values depend on the privileges you hold, as discussed in Section 27.6, "Stored Object Access Control". Also see that section for additional information about trigger security.

If the DEFINER clause is omitted, the default definer is the user who executes the [CREATE TRIGGER](#page-188-0) statement. This is the same as specifying DEFINER = CURRENT\_USER explicitly.

MySQL takes the DEFINER user into account when checking trigger privileges as follows:

- At [CREATE TRIGGER](#page-188-0) time, the user who issues the statement must have the TRIGGER privilege.
- At trigger activation time, privileges are checked against the DEFINER user. This user must have these privileges:
  - The TRIGGER privilege for the subject table.
  - The SELECT privilege for the subject table if references to table columns occur using OLD.col\_name or NEW.col\_name in the trigger body.
  - The UPDATE privilege for the subject table if table columns are targets of SET NEW.col\_name = value assignments in the trigger body.
  - Whatever other privileges normally are required for the statements executed by the trigger.

Within a trigger body, the CURRENT\_USER function returns the account used to check privileges at trigger activation time. This is the DEFINER user, not the user whose actions caused the trigger to be activated. For information about user auditing within triggers, see Section 8.2.23, "SQL-Based Account Activity Auditing".

If you use LOCK TABLES to lock a table that has triggers, the tables used within the trigger are also locked, as described in LOCK TABLES and Triggers.

For additional discussion of trigger use, see Section 27.3.1, "Trigger Syntax and Examples".

# <span id="page-190-0"></span>**15.1.23 CREATE VIEW Statement**

```
CREATE
 [OR REPLACE]
 [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]
 [DEFINER = user]
```

```
 [SQL SECURITY { DEFINER | INVOKER }]
 VIEW view_name [(column_list)]
 AS select_statement
 [WITH [CASCADED | LOCAL] CHECK OPTION]
```

The [CREATE VIEW](#page-190-0) statement creates a new view, or replaces an existing view if the OR REPLACE clause is given. If the view does not exist, [CREATE OR REPLACE VIEW](#page-190-0) is the same as [CREATE VIEW](#page-190-0). If the view does exist, [CREATE OR REPLACE VIEW](#page-190-0) replaces it.

For information about restrictions on view use, see Section 27.9, "Restrictions on Views".

The select\_statement is a SELECT statement that provides the definition of the view. (Selecting from the view selects, in effect, using the SELECT statement.) The select\_statement can select from base tables or from other views. Beginning with MySQL 8.0.19, the SELECT statement can use a VALUES statement as its source, or can be replaced with a TABLE statement, as with [CREATE](#page-149-0) [TABLE ... SELECT](#page-149-0).

The view definition is "frozen" at creation time and is not affected by subsequent changes to the definitions of the underlying tables. For example, if a view is defined as SELECT \* on a table, new columns added to the table later do not become part of the view, and columns dropped from the table result in an error when selecting from the view.

The ALGORITHM clause affects how MySQL processes the view. The DEFINER and SQL SECURITY clauses specify the security context to be used when checking access privileges at view invocation time. The WITH CHECK OPTION clause can be given to constrain inserts or updates to rows in tables referenced by the view. These clauses are described later in this section.

The [CREATE VIEW](#page-190-0) statement requires the CREATE VIEW privilege for the view, and some privilege for each column selected by the SELECT statement. For columns used elsewhere in the SELECT statement, you must have the SELECT privilege. If the OR REPLACE clause is present, you must also have the DROP privilege for the view. If the DEFINER clause is present, the privileges required depend on the user value, as discussed in Section 27.6, "Stored Object Access Control".

When a view is referenced, privilege checking occurs as described later in this section.

A view belongs to a database. By default, a new view is created in the default database. To create the view explicitly in a given database, use db\_name.view\_name syntax to qualify the view name with the database name:

```
CREATE VIEW test.v AS SELECT * FROM t;
```

Unqualified table or view names in the SELECT statement are also interpreted with respect to the default database. A view can refer to tables or views in other databases by qualifying the table or view name with the appropriate database name.

Within a database, base tables and views share the same namespace, so a base table and a view cannot have the same name.

Columns retrieved by the SELECT statement can be simple references to table columns, or expressions that use functions, constant values, operators, and so forth.

A view must have unique column names with no duplicates, just like a base table. By default, the names of the columns retrieved by the SELECT statement are used for the view column names. To define explicit names for the view columns, specify the optional column\_list clause as a list of comma-separated identifiers. The number of names in column\_list must be the same as the number of columns retrieved by the SELECT statement.

A view can be created from many kinds of SELECT statements. It can refer to base tables or other views. It can use joins, UNION, and subqueries. The SELECT need not even refer to any tables:

```
CREATE VIEW v_today (today) AS SELECT CURRENT_DATE;
```

The following example defines a view that selects two columns from another table as well as an expression calculated from those columns:

```
mysql> CREATE TABLE t (qty INT, price INT);
mysql> INSERT INTO t VALUES(3, 50);
mysql> CREATE VIEW v AS SELECT qty, price, qty*price AS value FROM t;
mysql> SELECT * FROM v;
+------+-------+-------+
| qty | price | value |
+------+-------+-------+
| 3 | 50 | 150 |
+------+-------+-------+
```

A view definition is subject to the following restrictions:

- The SELECT statement cannot refer to system variables or user-defined variables.
- Within a stored program, the SELECT statement cannot refer to program parameters or local variables.
- The SELECT statement cannot refer to prepared statement parameters.
- Any table or view referred to in the definition must exist. If, after the view has been created, a table or view that the definition refers to is dropped, use of the view results in an error. To check a view definition for problems of this kind, use the CHECK TABLE statement.
- The definition cannot refer to a TEMPORARY table, and you cannot create a TEMPORARY view.
- You cannot associate a trigger with a view.
- Aliases for column names in the SELECT statement are checked against the maximum column length of 64 characters (not the maximum alias length of 256 characters).

ORDER BY is permitted in a view definition, but it is ignored if you select from a view using a statement that has its own ORDER BY.

For other options or clauses in the definition, they are added to the options or clauses of the statement that references the view, but the effect is undefined. For example, if a view definition includes a LIMIT clause, and you select from the view using a statement that has its own LIMIT clause, it is undefined which limit applies. This same principle applies to options such as ALL, DISTINCT, or SQL\_SMALL\_RESULT that follow the SELECT keyword, and to clauses such as INTO, FOR UPDATE, FOR SHARE, LOCK IN SHARE MODE, and PROCEDURE.

The results obtained from a view may be affected if you change the query processing environment by changing system variables:

```
mysql> CREATE VIEW v (mycol) AS SELECT 'abc';
Query OK, 0 rows affected (0.01 sec)
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT "mycol" FROM v;
+-------+
| mycol |
+-------+
| mycol |
+-------+
1 row in set (0.01 sec)
mysql> SET sql_mode = 'ANSI_QUOTES';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT "mycol" FROM v;
+-------+
| mycol |
```

```
+-------+
| abc |
+-------+
1 row in set (0.00 sec)
```

The DEFINER and SQL SECURITY clauses determine which MySQL account to use when checking access privileges for the view when a statement is executed that references the view. The valid SQL SECURITY characteristic values are DEFINER (the default) and INVOKER. These indicate that the required privileges must be held by the user who defined or invoked the view, respectively.

If the DEFINER clause is present, the user value should be a MySQL account specified as 'user\_name'@'host\_name', CURRENT\_USER, or CURRENT\_USER(). The permitted user values depend on the privileges you hold, as discussed in Section 27.6, "Stored Object Access Control". Also see that section for additional information about view security.

If the DEFINER clause is omitted, the default definer is the user who executes the [CREATE VIEW](#page-190-0) statement. This is the same as specifying DEFINER = CURRENT\_USER explicitly.

Within a view definition, the CURRENT\_USER function returns the view's DEFINER value by default. For views defined with the SQL SECURITY INVOKER characteristic, CURRENT\_USER returns the account for the view's invoker. For information about user auditing within views, see Section 8.2.23, "SQL-Based Account Activity Auditing".

Within a stored routine that is defined with the SQL SECURITY DEFINER characteristic, CURRENT\_USER returns the routine's DEFINER value. This also affects a view defined within such a routine, if the view definition contains a DEFINER value of CURRENT\_USER.

MySQL checks view privileges like this:

- At view definition time, the view creator must have the privileges needed to use the top-level objects accessed by the view. For example, if the view definition refers to table columns, the creator must have some privilege for each column in the select list of the definition, and the SELECT privilege for each column used elsewhere in the definition. If the definition refers to a stored function, only the privileges needed to invoke the function can be checked. The privileges required at function invocation time can be checked only as it executes: For different invocations, different execution paths within the function might be taken.
- The user who references a view must have appropriate privileges to access it (SELECT to select from it, INSERT to insert into it, and so forth.)
- When a view has been referenced, privileges for objects accessed by the view are checked against the privileges held by the view DEFINER account or invoker, depending on whether the SQL SECURITY characteristic is DEFINER or INVOKER, respectively.
- If reference to a view causes execution of a stored function, privilege checking for statements executed within the function depend on whether the function SQL SECURITY characteristic is DEFINER or INVOKER. If the security characteristic is DEFINER, the function runs with the privileges of the DEFINER account. If the characteristic is INVOKER, the function runs with the privileges determined by the view's SQL SECURITY characteristic.

Example: A view might depend on a stored function, and that function might invoke other stored routines. For example, the following view invokes a stored function f():

```
CREATE VIEW v AS SELECT * FROM t WHERE t.id = f(t.name);
```

Suppose that f() contains a statement such as this:

```
IF name IS NULL then
 CALL p1();
ELSE
 CALL p2();
END IF;
```

The privileges required for executing statements within f() need to be checked when f() executes. This might mean that privileges are needed for p1() or p2(), depending on the execution path within f(). Those privileges must be checked at runtime, and the user who must possess the privileges is determined by the SQL SECURITY values of the view v and the function f().

The DEFINER and SQL SECURITY clauses for views are extensions to standard SQL. In standard SQL, views are handled using the rules for SQL SECURITY DEFINER. The standard says that the definer of the view, which is the same as the owner of the view's schema, gets applicable privileges on the view (for example, SELECT) and may grant them. MySQL has no concept of a schema "owner", so MySQL adds a clause to identify the definer. The DEFINER clause is an extension where the intent is to have what the standard has; that is, a permanent record of who defined the view. This is why the default DEFINER value is the account of the view creator.

The optional ALGORITHM clause is a MySQL extension to standard SQL. It affects how MySQL processes the view. ALGORITHM takes three values: MERGE, TEMPTABLE, or UNDEFINED. For more information, see Section 27.5.2, "View Processing Algorithms", as well as Section 10.2.2.4, "Optimizing Derived Tables, View References, and Common Table Expressions with Merging or Materialization".

Some views are updatable. That is, you can use them in statements such as UPDATE, DELETE, or INSERT to update the contents of the underlying table. For a view to be updatable, there must be a one-to-one relationship between the rows in the view and the rows in the underlying table. There are also certain other constructs that make a view nonupdatable.

A generated column in a view is considered updatable because it is possible to assign to it. However, if such a column is updated explicitly, the only permitted value is DEFAULT. For information about generated columns, see [Section 15.1.20.8, "CREATE TABLE and Generated Columns"](#page-162-0).

The WITH CHECK OPTION clause can be given for an updatable view to prevent inserts or updates to rows except those for which the WHERE clause in the select\_statement is true.

In a WITH CHECK OPTION clause for an updatable view, the LOCAL and CASCADED keywords determine the scope of check testing when the view is defined in terms of another view. The LOCAL keyword restricts the CHECK OPTION only to the view being defined. CASCADED causes the checks for underlying views to be evaluated as well. When neither keyword is given, the default is CASCADED.

For more information about updatable views and the WITH CHECK OPTION clause, see Section 27.5.3, "Updatable and Insertable Views", and Section 27.5.4, "The View WITH CHECK OPTION Clause".

# <span id="page-194-0"></span>**15.1.24 DROP DATABASE Statement**

DROP {DATABASE | SCHEMA} [IF EXISTS] db\_name

[DROP DATABASE](#page-194-0) drops all tables in the database and deletes the database. Be very careful with this statement! To use [DROP DATABASE](#page-194-0), you need the DROP privilege on the database. [DROP SCHEMA](#page-194-0) is a synonym for [DROP DATABASE](#page-194-0).

![](_page_194_Picture_12.jpeg)

#### **Important**

When a database is dropped, privileges granted specifically for the database are not automatically dropped. They must be dropped manually. See Section 15.7.1.6, "GRANT Statement".

IF EXISTS is used to prevent an error from occurring if the database does not exist.

If the default database is dropped, the default database is unset (the DATABASE() function returns NULL).

If you use [DROP DATABASE](#page-194-0) on a symbolically linked database, both the link and the original database are deleted.

[DROP DATABASE](#page-194-0) returns the number of tables that were removed.

The [DROP DATABASE](#page-194-0) statement removes from the given database directory those files and directories that MySQL itself may create during normal operation. This includes all files with the extensions shown in the following list:

- .BAK
- .DAT
- .HSH
- .MRG
- .MYD
- .MYI
- .cfg
- .db
- .ibd
- .ndb

If other files or directories remain in the database directory after MySQL removes those just listed, the database directory cannot be removed. In this case, you must remove any remaining files or directories manually and issue the [DROP DATABASE](#page-194-0) statement again.

Dropping a database does not remove any TEMPORARY tables that were created in that database. TEMPORARY tables are automatically removed when the session that created them ends. See [Section 15.1.20.2, "CREATE TEMPORARY TABLE Statement".](#page-147-1)

You can also drop databases with mysqladmin. See Section 6.5.2, "mysqladmin — A MySQL Server Administration Program".

# <span id="page-195-0"></span>**15.1.25 DROP EVENT Statement**

```
DROP EVENT [IF EXISTS] event_name
```

This statement drops the event named event\_name. The event immediately ceases being active, and is deleted completely from the server.

If the event does not exist, the error ERROR 1517 (HY000): Unknown event 'event\_name' results. You can override this and cause the statement to generate a warning for nonexistent events instead using IF EXISTS.

This statement requires the EVENT privilege for the schema to which the event to be dropped belongs.

# <span id="page-195-1"></span>**15.1.26 DROP FUNCTION Statement**

The [DROP FUNCTION](#page-195-1) statement is used to drop stored functions and loadable functions:

- For information about dropping stored functions, see [Section 15.1.29, "DROP PROCEDURE and](#page-196-1) [DROP FUNCTION Statements"](#page-196-1).
- For information about dropping loadable functions, see Section 15.7.4.2, "DROP FUNCTION Statement for Loadable Functions".

# <span id="page-195-2"></span>**15.1.27 DROP INDEX Statement**

```
DROP INDEX index_name ON tbl_name
 [algorithm_option | lock_option] ...
algorithm_option:
 ALGORITHM [=] {DEFAULT | INPLACE | COPY}
lock_option:
 LOCK [=] {DEFAULT | NONE | SHARED | EXCLUSIVE}
```

[DROP INDEX](#page-195-2) drops the index named index\_name from the table tbl\_name. This statement is mapped to an [ALTER TABLE](#page-64-1) statement to drop the index. See [Section 15.1.9, "ALTER TABLE](#page-64-1) [Statement".](#page-64-1)

To drop a primary key, the index name is always PRIMARY, which must be specified as a quoted identifier because PRIMARY is a reserved word:

```
DROP INDEX `PRIMARY` ON t;
```

Indexes on variable-width columns of NDB tables are dropped online; that is, without any table copying. The table is not locked against access from other NDB Cluster API nodes, although it is locked against other operations on the same API node for the duration of the operation. This is done automatically by the server whenever it determines that it is possible to do so; you do not have to use any special SQL syntax or server options to cause it to happen.

ALGORITHM and LOCK clauses may be given to influence the table copying method and level of concurrency for reading and writing the table while its indexes are being modified. They have the same meaning as for the [ALTER TABLE](#page-64-1) statement. For more information, see [Section 15.1.9, "ALTER](#page-64-1) [TABLE Statement"](#page-64-1)

MySQL NDB Cluster supports online operations using the same ALGORITHM=INPLACE syntax supported in the standard MySQL Server. See Section 25.6.12, "Online Operations with ALTER TABLE in NDB Cluster", for more information.

# <span id="page-196-0"></span>**15.1.28 DROP LOGFILE GROUP Statement**

```
DROP LOGFILE GROUP logfile_group
 ENGINE [=] engine_name
```

This statement drops the log file group named logfile\_group. The log file group must already exist or an error results. (For information on creating log file groups, see [Section 15.1.16, "CREATE](#page-109-0) [LOGFILE GROUP Statement"](#page-109-0).)

![](_page_196_Picture_11.jpeg)

#### **Important**

Before dropping a log file group, you must drop all tablespaces that use that log file group for UNDO logging.

The required ENGINE clause provides the name of the storage engine used by the log file group to be dropped. Currently, the only permitted values for engine\_name are NDB and NDBCLUSTER.

[DROP LOGFILE GROUP](#page-196-0) is useful only with Disk Data storage for NDB Cluster. See Section 25.6.11, "NDB Cluster Disk Data Tables".

# <span id="page-196-1"></span>**15.1.29 DROP PROCEDURE and DROP FUNCTION Statements**

```
DROP {PROCEDURE | FUNCTION} [IF EXISTS] sp_name
```

These statements are used to drop a stored routine (a stored procedure or function). That is, the specified routine is removed from the server. (DROP FUNCTION is also used to drop loadable functions; see Section 15.7.4.2, "DROP FUNCTION Statement for Loadable Functions".)

To drop a stored routine, you must have the ALTER ROUTINE privilege for it. (If the automatic\_sp\_privileges system variable is enabled, that privilege and EXECUTE are granted automatically to the routine creator when the routine is created and dropped from the creator when the routine is dropped. See Section 27.2.2, "Stored Routines and MySQL Privileges".)

In addition, if the definer of the routine has the SYSTEM\_USER privilege, the user dropping it must also have this privilege. This is enforced in MySQL 8.0.16 and later.

The IF EXISTS clause is a MySQL extension. It prevents an error from occurring if the procedure or function does not exist. A warning is produced that can be viewed with SHOW WARNINGS.

[DROP FUNCTION](#page-195-1) is also used to drop loadable functions (see Section 15.7.4.2, "DROP FUNCTION Statement for Loadable Functions").

# <span id="page-197-0"></span>**15.1.30 DROP SERVER Statement**

```
DROP SERVER [ IF EXISTS ] server_name
```

Drops the server definition for the server named server\_name. The corresponding row in the mysql.servers table is deleted. This statement requires the SUPER privilege.

Dropping a server for a table does not affect any FEDERATED tables that used this connection information when they were created. See [Section 15.1.18, "CREATE SERVER Statement"](#page-116-0).

DROP SERVER causes an implicit commit. See Section 15.3.3, "Statements That Cause an Implicit Commit".

DROP SERVER is not written to the binary log, regardless of the logging format that is in use.

# <span id="page-197-1"></span>**15.1.31 DROP SPATIAL REFERENCE SYSTEM Statement**

```
DROP SPATIAL REFERENCE SYSTEM
 [IF EXISTS]
 srid
srid: 32-bit unsigned integer
```

This statement removes a spatial reference system (SRS) definition from the data dictionary. It requires the SUPER privilege.

#### Example:

```
DROP SPATIAL REFERENCE SYSTEM 4120;
```

If no SRS definition with the SRID value exists, an error occurs unless IF EXISTS is specified. In that case, a warning occurs rather than an error.

If the SRID value is used by some column in an existing table, an error occurs. For example:

```
mysql> DROP SPATIAL REFERENCE SYSTEM 4326;
ERROR 3716 (SR005): Can't modify SRID 4326. There is at
least one column depending on it.
```

To identify which column or columns use the SRID, use this query:

```
SELECT * FROM INFORMATION_SCHEMA.ST_GEOMETRY_COLUMNS WHERE SRS_ID=4326;
```

SRID values must be in the range of 32-bit unsigned integers, with these restrictions:

- SRID 0 is a valid SRID but cannot be used with [DROP SPATIAL REFERENCE SYSTEM](#page-197-1).
- If the value is in a reserved SRID range, a warning occurs. Reserved ranges are [0, 32767] (reserved by EPSG), [60,000,000, 69,999,999] (reserved by EPSG), and [2,000,000,000, 2,147,483,647] (reserved by MySQL). EPSG stands for the [European Petroleum Survey Group.](http://epsg.org)

• Users should not drop SRSs with SRIDs in the reserved ranges. If system-installed SRSs are dropped, the SRS definitions may be recreated for MySQL upgrades.

# <span id="page-198-0"></span>**15.1.32 DROP TABLE Statement**

```
DROP [TEMPORARY] TABLE [IF EXISTS]
 tbl_name [, tbl_name] ...
 [RESTRICT | CASCADE]
```

[DROP TABLE](#page-198-0) removes one or more tables. You must have the DROP privilege for each table.

Be careful with this statement! For each table, it removes the table definition and all table data. If the table is partitioned, the statement removes the table definition, all its partitions, all data stored in those partitions, and all partition definitions associated with the dropped table.

Dropping a table also drops any triggers for the table.

[DROP TABLE](#page-198-0) causes an implicit commit, except when used with the TEMPORARY keyword. See Section 15.3.3, "Statements That Cause an Implicit Commit".

![](_page_198_Picture_8.jpeg)

#### **Important**

When a table is dropped, privileges granted specifically for the table are not automatically dropped. They must be dropped manually. See Section 15.7.1.6, "GRANT Statement".

If any tables named in the argument list do not exist, [DROP TABLE](#page-198-0) behavior depends on whether the IF EXISTS clause is given:

- Without IF EXISTS, the statement fails with an error indicating which nonexisting tables it was unable to drop, and no changes are made.
- With IF EXISTS, no error occurs for nonexisting tables. The statement drops all named tables that do exist, and generates a NOTE diagnostic for each nonexistent table. These notes can be displayed with SHOW WARNINGS. See Section 15.7.7.42, "SHOW WARNINGS Statement".

IF EXISTS can also be useful for dropping tables in unusual circumstances under which there is an entry in the data dictionary but no table managed by the storage engine. (For example, if an abnormal server exit occurs after removal of the table from the storage engine but before removal of the data dictionary entry.)

The TEMPORARY keyword has the following effects:

- The statement drops only TEMPORARY tables.
- The statement does not cause an implicit commit.
- No access rights are checked. A TEMPORARY table is visible only with the session that created it, so no check is necessary.

Including the TEMPORARY keyword is a good way to prevent accidentally dropping non-TEMPORARY tables.

The RESTRICT and CASCADE keywords do nothing. They are permitted to make porting easier from other database systems.

[DROP TABLE](#page-198-0) is not supported with all innodb\_force\_recovery settings. See Section 17.21.3, "Forcing InnoDB Recovery".

# <span id="page-198-1"></span>**15.1.33 DROP TABLESPACE Statement**

DROP [UNDO] TABLESPACE tablespace\_name

```
 [ENGINE [=] engine_name]
```

This statement drops a tablespace that was previously created using [CREATE TABLESPACE](#page-181-0). It is supported by the NDB and InnoDB storage engines.

The UNDO keyword, introduced in MySQL 8.0.14, must be specified to drop an undo tablespace. Only undo tablespaces created using [CREATE UNDO TABLESPACE](#page-181-0) syntax can be dropped. An undo tablespace must be in an empty state before it can be dropped. For more information, see Section 17.6.3.4, "Undo Tablespaces".

ENGINE sets the storage engine that uses the tablespace, where engine\_name is the name of the storage engine. Currently, the values InnoDB and NDB are supported. If not set, the value of default\_storage\_engine is used. If it is not the same as the storage engine used to create the tablespace, the DROP TABLESPACE statement fails.

tablespace\_name is a case-sensitive identifier in MySQL.

For an InnoDB general tablespace, all tables must be dropped from the tablespace prior to a DROP TABLESPACE operation. If the tablespace is not empty, DROP TABLESPACE returns an error.

An NDB tablespace to be dropped must not contain any data files; in other words, before you can drop an NDB tablespace, you must first drop each of its data files using [ALTER TABLESPACE ... DROP](#page-87-0) [DATAFILE](#page-87-0).

# **Notes**

- A general InnoDB tablespace is not deleted automatically when the last table in the tablespace is dropped. The tablespace must be dropped explicitly using DROP TABLESPACE tablespace\_name.
- A [DROP DATABASE](#page-194-0) operation can drop tables that belong to a general tablespace but it cannot drop the tablespace, even if the operation drops all tables that belong to the tablespace. The tablespace must be dropped explicitly using DROP TABLESPACE tablespace\_name.
- Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is for file-per-table tablespaces.

# **InnoDB Examples**

This example demonstrates how to drop an InnoDB general tablespace. The general tablespace ts1 is created with a single table. Before dropping the tablespace, the table must be dropped.

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 Engine=InnoDB;
mysql> DROP TABLE t1;
mysql> DROP TABLESPACE ts1;
```

This example demonstrates dropping an undo tablespace. An undo tablespace must be in an empty state before it can be dropped. For more information, see Section 17.6.3.4, "Undo Tablespaces".

```
mysql> DROP UNDO TABLESPACE undo_003;
```

# **NDB Example**

This example shows how to drop an NDB tablespace myts having a data file named mydata-1.dat after first creating the tablespace, and assumes the existence of a log file group named mylg (see [Section 15.1.16, "CREATE LOGFILE GROUP Statement"](#page-109-0)).

```
mysql> CREATE TABLESPACE myts
```

```
 -> ADD DATAFILE 'mydata-1.dat'
 -> USE LOGFILE GROUP mylg
 -> ENGINE=NDB;
```

You must remove all data files from the tablespace using ALTER TABLESPACE, as shown here, before it can be dropped:

```
mysql> ALTER TABLESPACE myts
 -> DROP DATAFILE 'mydata-1.dat'
 -> ENGINE=NDB;
mysql> DROP TABLESPACE myts;
```

# <span id="page-0-0"></span>**15.1.34 DROP TRIGGER Statement**

```
DROP TRIGGER [IF EXISTS] [schema_name.]trigger_name
```

This statement drops a trigger. The schema (database) name is optional. If the schema is omitted, the trigger is dropped from the default schema. [DROP TRIGGER](#page-0-0) requires the TRIGGER privilege for the table associated with the trigger.

Use IF EXISTS to prevent an error from occurring for a trigger that does not exist. A NOTE is generated for a nonexistent trigger when using IF EXISTS. See Section 15.7.7.42, "SHOW WARNINGS Statement".

Triggers for a table are also dropped if you drop the table.

# <span id="page-0-1"></span>**15.1.35 DROP VIEW Statement**

```
DROP VIEW [IF EXISTS]
 view_name [, view_name] ...
 [RESTRICT | CASCADE]
```

[DROP VIEW](#page-0-1) removes one or more views. You must have the DROP privilege for each view.

If any views named in the argument list do not exist, the statement fails with an error indicating by name which nonexisting views it was unable to drop, and no changes are made.

![](_page_0_Picture_13.jpeg)

#### **Note**

In MySQL 5.7 and earlier, [DROP VIEW](#page-0-1) returns an error if any views named in the argument list do not exist, but also drops all views in the list that do exist. Due to the change in behavior in MySQL 8.0, a partially completed [DROP VIEW](#page-0-1) operation on a MySQL 5.7 replication source server fails when replicated on a MySQL 8.0 replica. To avoid this failure scenario, use IF EXISTS syntax in [DROP VIEW](#page-0-1) statements to prevent an error from occurring for views that do not exist. For more information, see Section 15.1.1, "Atomic Data Definition Statement Support".

The IF EXISTS clause prevents an error from occurring for views that don't exist. When this clause is given, a NOTE is generated for each nonexistent view. See Section 15.7.7.42, "SHOW WARNINGS Statement".

RESTRICT and CASCADE, if given, are parsed and ignored.

# <span id="page-0-2"></span>**15.1.36 RENAME TABLE Statement**

```
RENAME TABLE
 tbl_name TO new_tbl_name
 [, tbl_name2 TO new_tbl_name2] ...
```

[RENAME TABLE](#page-0-2) renames one or more tables. You must have ALTER and DROP privileges for the original table, and CREATE and INSERT privileges for the new table.

For example, to rename a table named old\_table to new\_table, use this statement:

```
RENAME TABLE old_table TO new_table;
```

That statement is equivalent to the following ALTER TABLE statement:

```
ALTER TABLE old_table RENAME new_table;
```

RENAME TABLE, unlike ALTER TABLE, can rename multiple tables within a single statement:

```
RENAME TABLE old_table1 TO new_table1,
 old_table2 TO new_table2,
 old_table3 TO new_table3;
```

Renaming operations are performed left to right. Thus, to swap two table names, do this (assuming that a table with the intermediary name tmp\_table does not already exist):

```
RENAME TABLE old_table TO tmp_table,
 new_table TO old_table,
 tmp_table TO new_table;
```

Metadata locks on tables are acquired in name order, which in some cases can make a difference in operation outcome when multiple transactions execute concurrently. See Section 10.11.4, "Metadata Locking".

As of MySQL 8.0.13, you can rename tables locked with a [LOCK TABLES](#page-111-0) statement, provided that they are locked with a WRITE lock or are the product of renaming WRITE-locked tables from earlier steps in a multiple-table rename operation. For example, this is permitted:

```
LOCK TABLE old_table1 WRITE;
RENAME TABLE old_table1 TO new_table1,
 new_table1 TO new_table2;
```

This is not permitted:

```
LOCK TABLE old_table1 READ;
RENAME TABLE old_table1 TO new_table1,
 new_table1 TO new_table2;
```

Prior to MySQL 8.0.13, to execute RENAME TABLE, there must be no tables locked with LOCK TABLES.

With the transaction table locking conditions satisfied, the rename operation is done atomically; no other session can access any of the tables while the rename is in progress.

If any errors occur during a RENAME TABLE, the statement fails and no changes are made.

You can use RENAME TABLE to move a table from one database to another:

```
RENAME TABLE current_db.tbl_name TO other_db.tbl_name;
```

Using this method to move all tables from one database to a different one in effect renames the database (an operation for which MySQL has no single statement), except that the original database continues to exist, albeit with no tables.

Like RENAME TABLE, ALTER TABLE ... RENAME can also be used to move a table to a different database. Regardless of the statement used, if the rename operation would move the table to a database located on a different file system, the success of the outcome is platform specific and depends on the underlying operating system calls used to move table files.

If a table has triggers, attempts to rename the table into a different database fail with a Trigger in wrong schema ([ER\\_TRG\\_IN\\_WRONG\\_SCHEMA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_trg_in_wrong_schema)) error.

An unencrypted table can be moved to an encryption-enabled database and vice versa. However, if the table\_encryption\_privilege\_check variable is enabled, the TABLE\_ENCRYPTION\_ADMIN privilege is required if the table encryption setting differs from the default database encryption.

To rename TEMPORARY tables, RENAME TABLE does not work. Use ALTER TABLE instead.

RENAME TABLE works for views, except that views cannot be renamed into a different database.

Any privileges granted specifically for a renamed table or view are not migrated to the new name. They must be changed manually.

RENAME TABLE tbl\_name TO new\_tbl\_name changes internally generated foreign key constraint names and user-defined foreign key constraint names that begin with the string "tbl\_name\_ibfk\_" to reflect the new table name. InnoDB interprets foreign key constraint names that begin with the string "tbl name ibfk" as internally generated names.

Foreign key constraint names that point to the renamed table are automatically updated unless there is a conflict, in which case the statement fails with an error. A conflict occurs if the renamed constraint name already exists. In such cases, you must drop and re-create the foreign keys for them to function properly.

RENAME TABLE tbl\_name TO new\_tbl\_name changes internally generated and user-defined CHECK constraint names that begin with the string "tbl\_name\_chk\_" to reflect the new table name. MySQL interprets CHECK constraint names that begin with the string "tbl\_name\_chk\_" as internally generated names. Example:

```
mysql> SHOW CREATE TABLE t1\G
                      ****** 1. row **************
      Table: t1
Create Table: CREATE TABLE `t1` (
  `i1` int(11) DEFAULT NULL,
  `i2` int(11) DEFAULT NULL,
 CONSTRAINT `t1_chk_1` CHECK ((`i1` > 0)),
CONSTRAINT `t1_chk_2` CHECK ((`i2` < 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4 0900 ai ci
1 row in set (0.02 sec)
mysql> RENAME TABLE t1 TO t3;
Query OK, 0 rows affected (0.03 sec)
mysql> SHOW CREATE TABLE t3\G
              *********** 1. row ***************
      Table: t.3
Create Table: CREATE TABLE `t3` (
  `i1` int(11) DEFAULT NULL,
  `i2` int(11) DEFAULT NULL,
 CONSTRAINT `t3_chk_1` CHECK ((`i1` > 0)),
CONSTRAINT `t3 chk_2` CHECK ((`i2` < 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4 0900 ai ci
1 row in set (0.01 sec)
```

#### <span id="page-2-0"></span>15.1.37 TRUNCATE TABLE Statement

```
TRUNCATE [TABLE] tbl_name
```

TRUNCATE TABLE empties a table completely. It requires the DROP privilege. Logically, TRUNCATE TABLE is similar to a DELETE statement that deletes all rows, or a sequence of DROP TABLE and CREATE TABLE statements.

To achieve high performance, TRUNCATE TABLE bypasses the DML method of deleting data. Thus, it does not cause ON DELETE triggers to fire, it cannot be performed for InnoDB tables with parent-child foreign key relationships, and it cannot be rolled back like a DML operation. However, TRUNCATE TABLE operations on tables that use a storage engine which supports atomic DDL are either fully committed or rolled back if the server halts during their operation. For more information, see Section 15.1.1, "Atomic Data Definition Statement Support".

Although [TRUNCATE TABLE](#page-2-0) is similar to [DELETE](#page-5-0), it is classified as a DDL statement rather than a DML statement. It differs from [DELETE](#page-5-0) in the following ways:

- Truncate operations drop and re-create the table, which is much faster than deleting rows one by one, particularly for large tables.
- Truncate operations cause an implicit commit, and so cannot be rolled back. See [Section 15.3.3,](#page-109-0) ["Statements That Cause an Implicit Commit".](#page-109-0)
- Truncation operations cannot be performed if the session holds an active table lock.
- [TRUNCATE TABLE](#page-2-0) fails for an InnoDB table or NDB table if there are any FOREIGN KEY constraints from other tables that reference the table. Foreign key constraints between columns of the same table are permitted.
- Truncation operations do not return a meaningful value for the number of deleted rows. The usual result is "0 rows affected," which should be interpreted as "no information."
- As long as the table definition is valid, the table can be re-created as an empty table with [TRUNCATE](#page-2-0) [TABLE](#page-2-0), even if the data or index files have become corrupted.
- Any AUTO\_INCREMENT value is reset to its start value. This is true even for MyISAM and InnoDB, which normally do not reuse sequence values.
- When used with partitioned tables, [TRUNCATE TABLE](#page-2-0) preserves the partitioning; that is, the data and index files are dropped and re-created, while the partition definitions are unaffected.
- The [TRUNCATE TABLE](#page-2-0) statement does not invoke ON DELETE triggers.
- Truncating a corrupted InnoDB table is supported.

[TRUNCATE TABLE](#page-2-0) is treated for purposes of binary logging and replication as DDL rather than DML, and is always logged as a statement.

[TRUNCATE TABLE](#page-2-0) for a table closes all handlers for the table that were opened with [HANDLER OPEN](#page-11-0).

In MySQL 5.7 and earlier, on a system with a large buffer pool and innodb\_adaptive\_hash\_index enabled, a TRUNCATE TABLE operation could cause a temporary drop in system performance due to an LRU scan that occurred when removing the table's adaptive hash index entries (Bug #68184). The remapping of [TRUNCATE TABLE](#page-2-0) to DROP TABLE and CREATE TABLE in MySQL 8.0 avoids the problematic LRU scan.

[TRUNCATE TABLE](#page-2-0) can be used with Performance Schema summary tables, but the effect is to reset the summary columns to 0 or NULL, not to remove rows. See Section 29.12.20, "Performance Schema Summary Tables".

Truncating an InnoDB table that resides in a file-per-table tablespace drops the existing tablespace and creates a new one. As of MySQL 8.0.21, if the tablespace was created with an earlier version and resides in an unknown directory, InnoDB creates the new tablespace in the default location and writes the following warning to the error log: The DATA DIRECTORY location must be in a known directory. The DATA DIRECTORY location will be ignored and the file will be put into the default datadir location. Known directories are those defined by the datadir, innodb\_data\_home\_dir, and innodb\_directories variables. To have [TRUNCATE](#page-2-0) [TABLE](#page-2-0) create the tablespace in its current location, add the directory to the innodb\_directories setting before running [TRUNCATE TABLE](#page-2-0).