---
source: MySQL 5.7 Reference
title: 00_Overview
---

MySQL NDB Cluster 7.5 and 7.6 support online table schema changes using ALTER TABLE ... ALGORITHM=DEFAULT|INPLACE|COPY. NDB Cluster handles COPY and INPLACE as described in the next few paragraphs.

For ALGORITHM=COPY, the mysqld NDB Cluster handler performs the following actions:

- Tells the data nodes to create an empty copy of the table, and to make the required schema changes to this copy.
- Reads rows from the original table, and writes them to the copy.
- Tells the data nodes to drop the original table and then to rename the copy.

We sometimes refer to this as a "copying" or "offline" ALTER TABLE.

DML operations are not permitted concurrently with a copying ALTER TABLE.

The mysqld on which the copying ALTER TABLE statement is issued takes a metadata lock, but this is in effect only on that mysqld. Other NDB clients can modify row data during a copying ALTER TABLE, resulting in inconsistency.

For ALGORITHM=INPLACE, the NDB Cluster handler tells the data nodes to make the required changes, and does not perform any copying of data.

We also refer to this as a "non-copying" or "online" ALTER TABLE.

A non-copying ALTER TABLE allows concurrent DML operations.

Regardless of the algorithm used, the mysqld takes a Global Schema Lock (GSL) while executing ALTER TABLE; this prevents execution of any (other) DDL or backups concurrently on this or any other SQL node in the cluster. This is normally not problematic, unless the ALTER TABLE takes a very long time.

![](_page_4_Picture_20.jpeg)

### **Note**

Some older releases of NDB Cluster used a syntax specific to NDB for online ALTER TABLE operations. That syntax has since been removed.

Operations that add and drop indexes on variable-width columns of NDB tables occur online. Online operations are noncopying; that is, they do not require that indexes be re-created. They do not lock the table being altered from access by other API nodes in an NDB Cluster (but see [Limitations of NDB](#page-6-0) [online operations](#page-6-0), later in this section). Such operations do not require single user mode for NDB table alterations made in an NDB cluster with multiple API nodes; transactions can continue uninterrupted during online DDL operations.

ALGORITHM=INPLACE can be used to perform online ADD COLUMN, ADD INDEX (including CREATE INDEX statements), and DROP INDEX operations on NDB tables. Online renaming of NDB tables is also supported.

Disk-based columns cannot be added to NDB tables online. This means that, if you wish to add an inmemory column to an NDB table that uses a table-level STORAGE DISK option, you must declare the new column as using memory-based storage explicitly. For example—assuming that you have already created tablespace ts1—suppose that you create table t1 as follows:

```
mysql> CREATE TABLE t1 (
 > c1 INT NOT NULL PRIMARY KEY,
 > c2 VARCHAR(30)
 > )
 > TABLESPACE ts1 STORAGE DISK
 > ENGINE NDB;
Query OK, 0 rows affected (1.73 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

You can add a new in-memory column to this table online as shown here:

```
mysql> ALTER TABLE t1
 > ADD COLUMN c3 INT COLUMN_FORMAT DYNAMIC STORAGE MEMORY,
 > ALGORITHM=INPLACE;
Query OK, 0 rows affected (1.25 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

This statement fails if the STORAGE MEMORY option is omitted:

```
mysql> ALTER TABLE t1
 > ADD COLUMN c4 INT COLUMN_FORMAT DYNAMIC,
 > ALGORITHM=INPLACE;
ERROR 1846 (0A000): ALGORITHM=INPLACE is not supported. Reason:
Adding column(s) or add/reorganize partition not supported online. Try
ALGORITHM=COPY.
```

If you omit the COLUMN\_FORMAT DYNAMIC option, the dynamic column format is employed automatically, but a warning is issued, as shown here:

```
mysql> ALTER ONLINE TABLE t1 ADD COLUMN c4 INT STORAGE MEMORY;
Query OK, 0 rows affected, 1 warning (1.17 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1478
Message: DYNAMIC column c4 with STORAGE DISK is not supported, column will
become FIXED
mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
 Table: t1
Create Table: CREATE TABLE `t1` (
 `c1` int(11) NOT NULL,
 `c2` varchar(30) DEFAULT NULL,
 `c3` int(11) /*!50606 STORAGE MEMORY */ /*!50606 COLUMN_FORMAT DYNAMIC */ DEFAULT NULL,
 `c4` int(11) /*!50606 STORAGE MEMORY */ DEFAULT NULL,
 PRIMARY KEY (`c1`)
) /*!50606 TABLESPACE ts_1 STORAGE DISK */ ENGINE=ndbcluster DEFAULT CHARSET=latin1
1 row in set (0.03 sec)
```

![](_page_5_Picture_10.jpeg)

### **Note**

The STORAGE and COLUMN\_FORMAT keywords are supported only in NDB Cluster; in any other version of MySQL, attempting to use either of these keywords in a CREATE TABLE or ALTER TABLE statement results in an error. It is also possible to use the statement ALTER TABLE ... REORGANIZE PARTITION, ALGORITHM=INPLACE with no partition\_names INTO (partition\_definitions) option on NDB tables. This can be used to redistribute NDB Cluster data among new data nodes that have been added to the cluster online. This does not perform any defragmentation, which requires an OPTIMIZE TABLE or null ALTER TABLE statement. For more information, see Section 21.6.7, "Adding NDB Cluster Data Nodes Online".

# <span id="page-6-0"></span>**Limitations of NDB online operations**

Online DROP COLUMN operations are not supported.

Online ALTER TABLE, CREATE INDEX, or DROP INDEX statements that add columns or add or drop indexes are subject to the following limitations:

- A given online ALTER TABLE can use only one of ADD COLUMN, ADD INDEX, or DROP INDEX. One or more columns can be added online in a single statement; only one index may be created or dropped online in a single statement.
- The table being altered is not locked with respect to API nodes other than the one on which an online ALTER TABLE ADD COLUMN, ADD INDEX, or DROP INDEX operation (or CREATE INDEX or DROP INDEX statement) is run. However, the table is locked against any other operations originating on the same API node while the online operation is being executed.
- The table to be altered must have an explicit primary key; the hidden primary key created by the NDB storage engine is not sufficient for this purpose.
- The storage engine used by the table cannot be changed online.
- The tablespace used by the table cannot be changed online. (Bug #99269, Bug #31180526)
- When used with NDB Cluster Disk Data tables, it is not possible to change the storage type (DISK or MEMORY) of a column online. This means, that when you add or drop an index in such a way that the operation would be performed online, and you want the storage type of the column or columns to be changed, you must use ALGORITHM=COPY in the statement that adds or drops the index.

Columns to be added online cannot use the BLOB or TEXT type, and must meet the following criteria:

- The columns must be dynamic; that is, it must be possible to create them using COLUMN\_FORMAT DYNAMIC. If you omit the COLUMN\_FORMAT DYNAMIC option, the dynamic column format is employed automatically.
- The columns must permit NULL values and not have any explicit default value other than NULL. Columns added online are automatically created as DEFAULT NULL, as can be seen here:

```
mysql> CREATE TABLE t2 (
 > c1 INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 > ) ENGINE=NDB;
Query OK, 0 rows affected (1.44 sec)
mysql> ALTER TABLE t2
 > ADD COLUMN c2 INT,
 > ADD COLUMN c3 INT,
 > ALGORITHM=INPLACE;
Query OK, 0 rows affected, 2 warnings (0.93 sec)
mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
 Table: t1
Create Table: CREATE TABLE `t2` (
 `c1` int(11) NOT NULL AUTO_INCREMENT,
 `c2` int(11) DEFAULT NULL,
 `c3` int(11) DEFAULT NULL,
 PRIMARY KEY (`c1`)
) ENGINE=ndbcluster DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
```

- The columns must be added following any existing columns. If you attempt to add a column online before any existing columns or using the FIRST keyword, the statement fails with an error.
- Existing table columns cannot be reordered online.

For online ALTER TABLE operations on NDB tables, fixed-format columns are converted to dynamic when they are added online, or when indexes are created or dropped online, as shown here (repeating the CREATE TABLE and ALTER TABLE statements just shown for the sake of clarity):

```
mysql> CREATE TABLE t2 (
 > c1 INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 > ) ENGINE=NDB;
Query OK, 0 rows affected (1.44 sec)
mysql> ALTER TABLE t2
 > ADD COLUMN c2 INT,
 > ADD COLUMN c3 INT,
 > ALGORITHM=INPLACE;
Query OK, 0 rows affected, 2 warnings (0.93 sec)
mysql> SHOW WARNINGS;
*************************** 1. row ***************************
 Level: Warning
 Code: 1478
Message: Converted FIXED field 'c2' to DYNAMIC to enable online ADD COLUMN
*************************** 2. row ***************************
 Level: Warning
 Code: 1478
Message: Converted FIXED field 'c3' to DYNAMIC to enable online ADD COLUMN
2 rows in set (0.00 sec)
```

Only the column or columns to be added online must be dynamic. Existing columns need not be; this includes the table's primary key, which may also be FIXED, as shown here:

```
mysql> CREATE TABLE t3 (
 > c1 INT NOT NULL AUTO_INCREMENT PRIMARY KEY COLUMN_FORMAT FIXED
 > ) ENGINE=NDB;
Query OK, 0 rows affected (2.10 sec)
mysql> ALTER TABLE t3 ADD COLUMN c2 INT, ALGORITHM=INPLACE;
Query OK, 0 rows affected, 1 warning (0.78 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW WARNINGS;
*************************** 1. row ***************************
 Level: Warning
 Code: 1478
Message: Converted FIXED field 'c2' to DYNAMIC to enable online ADD COLUMN
1 row in set (0.00 sec)
```

Columns are not converted from FIXED to DYNAMIC column format by renaming operations. For more information about COLUMN\_FORMAT, see Section 13.1.18, "CREATE TABLE Statement".

The KEY, CONSTRAINT, and IGNORE keywords are supported in ALTER TABLE statements using ALGORITHM=INPLACE.

Beginning with NDB Cluster 7.5.7, setting MAX\_ROWS to 0 using an online ALTER TABLE statement is disallowed. You must use a copying ALTER TABLE to perform this operation. (Bug #21960004)

# <span id="page-7-0"></span>**21.6.13 Distributed Privileges Using Shared Grant Tables**

NDB Cluster supports distribution of MySQL users and privileges across all SQL nodes in an NDB Cluster. This support is not enabled by default; you should follow the procedure outlined in this section in order to do so.

Normally, each MySQL server's user privilege tables in the mysql database must use the MyISAM storage engine, which means that a user account and its associated privileges created on one SQL node are not available on the cluster's other SQL nodes. An SQL file ndb\_dist\_priv.sql provided with the NDB Cluster distribution can be found in the share directory in the MySQL installation directory.

The first step in enabling distributed privileges is to load this script into a MySQL Server that functions as an SQL node (which we refer to after this as the target SQL node or MySQL Server). You can do this by executing the following command from the system shell on the target SQL node after changing to its MySQL installation directory (where options stands for any additional options needed to connect to this SQL node):

```
$> mysql options -uroot < share/ndb_dist_priv.sql
```

Importing ndb\_dist\_priv.sql creates a number of stored routines (six stored procedures and one stored function) in the mysql database on the target SQL node. After connecting to the SQL node in the mysql client (as the MySQL root user), you can verify that these were created as shown here:

```
mysql> SELECT ROUTINE_NAME, ROUTINE_SCHEMA, ROUTINE_TYPE
 -> FROM INFORMATION_SCHEMA.ROUTINES
 -> WHERE ROUTINE_NAME LIKE 'mysql_cluster%'
 -> ORDER BY ROUTINE_TYPE;
+---------------------------------------------+----------------+--------------+
| ROUTINE_NAME | ROUTINE_SCHEMA | ROUTINE_TYPE |
+---------------------------------------------+----------------+--------------+
| mysql_cluster_privileges_are_distributed | mysql | FUNCTION |
| mysql_cluster_backup_privileges | mysql | PROCEDURE |
| mysql_cluster_move_grant_tables | mysql | PROCEDURE |
| mysql_cluster_move_privileges | mysql | PROCEDURE |
| mysql_cluster_restore_local_privileges | mysql | PROCEDURE |
| mysql_cluster_restore_privileges | mysql | PROCEDURE |
| mysql_cluster_restore_privileges_from_local | mysql | PROCEDURE |
+---------------------------------------------+----------------+--------------+
7 rows in set (0.01 sec)
```

The stored procedure named mysql\_cluster\_move\_privileges creates backup copies of the existing privilege tables, then converts them to NDB.

mysql\_cluster\_move\_privileges performs the backup and conversion in two steps. The first step is to call mysql\_cluster\_backup\_privileges, which creates two sets of copies in the mysql database:

- A set of local copies that use the MyISAM storage engine. Their names are generated by adding the suffix \_backup to the original privilege table names.
- A set of distributed copies that use the NDBCLUSTER storage engine. These tables are named by prefixing ndb\_ and appending \_backup to the names of the original tables.

After the copies are created, mysql\_cluster\_move\_privileges invokes mysql\_cluster\_move\_grant\_tables, which contains the ALTER TABLE ... ENGINE = NDB statements that convert the mysql system tables to NDB.

Normally, you should not invoke either mysql\_cluster\_backup\_privileges or mysql\_cluster\_move\_grant\_tables manually; these stored procedures are intended only for use by mysql\_cluster\_move\_privileges.

Although the original privilege tables are backed up automatically, it is always a good idea to create backups manually of the existing privilege tables on all affected SQL nodes before proceeding. You can do this using mysqldump in a manner similar to what is shown here:

```
$> mysqldump options -uroot \
 mysql user db tables_priv columns_priv procs_priv proxies_priv > backup_file
```

To perform the conversion, you must be connected to the target SQL node using the mysql client (again, as the MySQL root user). Invoke the stored procedure like this:

```
mysql> CALL mysql.mysql_cluster_move_privileges();
Query OK, 0 rows affected (22.32 sec)
```

Depending on the number of rows in the privilege tables, this procedure may take some time to execute. If some of the privilege tables are empty, you may see one or more No data - zero rows fetched, selected, or processed warnings when mysql\_cluster\_move\_privileges returns. In such cases, the warnings may be safely ignored. To verify that the conversion was successful, you can use the stored function mysql\_cluster\_privileges\_are\_distributed as shown here:

```
mysql> SELECT CONCAT(
 -> 'Conversion ',
 -> IF(mysql.mysql_cluster_privileges_are_distributed(), 'succeeded', 'failed'),
 -> '.')
 -> AS Result;
+-----------------------+
| Result |
+-----------------------+
| Conversion succeeded. |
+-----------------------+
1 row in set (0.00 sec)
```

mysql\_cluster\_privileges\_are\_distributed checks for the existence of the distributed privilege tables and returns 1 if all of the privilege tables are distributed; otherwise, it returns 0.

You can verify that the backups have been created using a query such as this one:

```
mysql> SELECT TABLE_NAME, ENGINE FROM INFORMATION_SCHEMA.TABLES
 -> WHERE TABLE_SCHEMA = 'mysql' AND TABLE_NAME LIKE '%backup'
 -> ORDER BY ENGINE;
+-------------------------+------------+
| TABLE_NAME | ENGINE |
+-------------------------+------------+
| db_backup | MyISAM |
| user_backup | MyISAM |
| columns_priv_backup | MyISAM |
| tables_priv_backup | MyISAM |
| proxies_priv_backup | MyISAM |
| procs_priv_backup | MyISAM |
| ndb_columns_priv_backup | ndbcluster |
| ndb_user_backup | ndbcluster |
| ndb_tables_priv_backup | ndbcluster |
| ndb_proxies_priv_backup | ndbcluster |
| ndb_procs_priv_backup | ndbcluster |
| ndb_db_backup | ndbcluster |
+-------------------------+------------+
12 rows in set (0.00 sec)
```

Once the conversion to distributed privileges has been made, any time a MySQL user account is created, dropped, or has its privileges updated on any SQL node, the changes take effect immediately on all other MySQL servers attached to the cluster. Once privileges are distributed, any new MySQL Servers that connect to the cluster automatically participate in the distribution.

![](_page_9_Picture_8.jpeg)

### **Note**

For clients connected to SQL nodes at the time that mysql\_cluster\_move\_privileges is executed, you may need to execute FLUSH PRIVILEGES on those SQL nodes, or to disconnect and then reconnect the clients, in order for those clients to be able to see the changes in privileges.

All MySQL user privileges are distributed across all connected MySQL Servers. This includes any privileges associated with views and stored routines, even though distribution of views and stored routines themselves is not currently supported.

In the event that an SQL node becomes disconnected from the cluster while mysql\_cluster\_move\_privileges is running, you must drop its privilege tables after reconnecting to the cluster, using a statement such as DROP TABLE IF EXISTS mysql.user mysql.db mysql.tables\_priv mysql.columns\_priv mysql.procs\_priv. This causes the SQL node to use the shared privilege tables rather than its own local versions of them. This is not needed when connecting a new SQL node to the cluster for the first time.

In the event of an initial restart of the entire cluster (all data nodes shut down, then started again with --initial), the shared privilege tables are lost. If this happens, you can restore them using the original target SQL node either from the backups made by mysql\_cluster\_move\_privileges or from a dump file created with mysqldump. If you need to use a new MySQL Server to perform the restoration, you should start it with --skip-grant-tables when connecting to the cluster for the first time; after this, you can restore the privilege tables locally, then distribute them again using mysql\_cluster\_move\_privileges. After restoring and distributing the tables, you should restart this MySQL Server without the --skip-grant-tables option.

You can also restore the distributed tables using ndb\_restore --restore-privilege-tables from a backup made using START BACKUP in the ndb\_mgm client. (The MyISAM tables created by mysql\_cluster\_move\_privileges are not backed up by the START BACKUP command.) ndb\_restore does not restore the privilege tables by default; the --restore-privilege-tables option causes it to do so.

You can restore the SQL node's local privileges using either of two procedures. mysql\_cluster\_restore\_privileges works as follows:

- 1. If copies of the mysql.ndb\_\*\_backup tables are available, attempt to restore the system tables from these.
- 2. Otherwise, attempt to restore the system tables from the local backups named \*\_backup (without the ndb\_ prefix).

The other procedure, named mysql\_cluster\_restore\_local\_privileges, restores the system tables from the local backups only, without checking the ndb\_\* backups.

The system tables re-created by mysql\_cluster\_restore\_privileges or mysql\_cluster\_restore\_local\_privileges use the MySQL server default storage engine; they are not shared or distributed in any way, and do not use NDB Cluster's NDB storage engine.

The additional stored procedure mysql\_cluster\_restore\_privileges\_from\_local is intended for the use of mysql\_cluster\_restore\_privileges and mysql\_cluster\_restore\_local\_privileges. It should not be invoked directly.

![](_page_10_Picture_10.jpeg)

### **Important**

Applications that access NDB Cluster data directly, including NDB API and ClusterJ applications, are not subject to the MySQL privilege system. This means that, once you have distributed the grant tables, they can be freely accessed by such applications, just as they can any other NDB tables. In particular, you should keep in mind that NDB API and ClusterJ applications can read and write user names, host names, password hashes, and any other contents of the distributed grant tables without any restrictions.

# <span id="page-10-0"></span>**21.6.14 NDB API Statistics Counters and Variables**

A number of types of statistical counters relating to actions performed by or affecting [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects are available. Such actions include starting and closing (or aborting) transactions; primary key and unique key operations; table, range, and pruned scans; threads blocked while waiting for the completion of various operations; and data and events sent and received by NDBCLUSTER. The counters are incremented inside the NDB kernel whenever NDB API calls are made or data is sent to or received by the data nodes. mysqld exposes these counters as system status variables; their values can be read in the output of SHOW STATUS, or by querying the Information Schema SESSION\_STATUS or GLOBAL\_STATUS table. By comparing the values before and after statements operating on NDB tables, you can observe the corresponding actions taken on the API level, and thus the cost of performing the statement.

You can list all of these status variables using the following SHOW STATUS statement:

```
mysql> SHOW STATUS LIKE 'ndb_api%';
+----------------------------------------------+-------------+
| Variable_name | Value |
+----------------------------------------------+-------------+
| Ndb_api_wait_exec_complete_count | 2 |
| Ndb_api_wait_scan_result_count | 3 |
| Ndb_api_wait_meta_request_count | 101 |
| Ndb_api_wait_nanos_count | 83664697215 |
| Ndb_api_bytes_sent_count | 13608 |
| Ndb_api_bytes_received_count | 142800 |
| Ndb_api_trans_start_count | 2 |
| Ndb_api_trans_commit_count | 1 |
| Ndb_api_trans_abort_count | 0 |
| Ndb_api_trans_close_count | 2 |
| Ndb_api_pk_op_count | 1 |
| Ndb_api_uk_op_count | 0 |
| Ndb_api_table_scan_count | 1 |
| Ndb_api_range_scan_count | 0 |
| Ndb_api_pruned_scan_count | 0 |
| Ndb_api_scan_batch_count | 0 |
| Ndb_api_read_row_count | 1 |
| Ndb_api_trans_local_read_row_count | 1 |
| Ndb_api_adaptive_send_forced_count | 0 |
| Ndb_api_adaptive_send_unforced_count | 3 |
| Ndb_api_adaptive_send_deferred_count | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
| Ndb_api_wait_exec_complete_count_slave | 0 |
| Ndb_api_wait_scan_result_count_slave | 0 |
| Ndb_api_wait_meta_request_count_slave | 0 |
| Ndb_api_wait_nanos_count_slave | 0 |
| Ndb_api_bytes_sent_count_slave | 0 |
| Ndb_api_bytes_received_count_slave | 0 |
| Ndb_api_trans_start_count_slave | 0 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_abort_count_slave | 0 |
| Ndb_api_trans_close_count_slave | 0 |
| Ndb_api_pk_op_count_slave | 0 |
| Ndb_api_uk_op_count_slave | 0 |
| Ndb_api_table_scan_count_slave | 0 |
| Ndb_api_range_scan_count_slave | 0 |
| Ndb_api_pruned_scan_count_slave | 0 |
| Ndb_api_scan_batch_count_slave | 0 |
| Ndb_api_read_row_count_slave | 0 |
| Ndb_api_trans_local_read_row_count_slave | 0 |
| Ndb_api_adaptive_send_forced_count_slave | 0 |
| Ndb_api_adaptive_send_unforced_count_slave | 0 |
| Ndb_api_adaptive_send_deferred_count_slave | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
```

```
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+-------------+
69 rows in set (0.00 sec)
```

These status variables are also available from the SESSION\_STATUS and GLOBAL\_STATUS tables of the INFORMATION\_SCHEMA database, as shown here:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.SESSION_STATUS 
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%';
+----------------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+----------------------------------------------+----------------+
| Ndb_api_wait_exec_complete_count | 2 |
| Ndb_api_wait_scan_result_count | 3 |
| Ndb_api_wait_meta_request_count | 101 |
| Ndb_api_wait_nanos_count | 74890499869 |
| Ndb_api_bytes_sent_count | 13608 |
| Ndb_api_bytes_received_count | 142800 |
| Ndb_api_trans_start_count | 2 |
| Ndb_api_trans_commit_count | 1 |
| Ndb_api_trans_abort_count | 0 |
| Ndb_api_trans_close_count | 2 |
| Ndb_api_pk_op_count | 1 |
| Ndb_api_uk_op_count | 0 |
| Ndb_api_table_scan_count | 1 |
| Ndb_api_range_scan_count | 0 |
| Ndb_api_pruned_scan_count | 0 |
| Ndb_api_scan_batch_count | 0 |
| Ndb_api_read_row_count | 1 |
| Ndb_api_trans_local_read_row_count | 1 |
| Ndb_api_adaptive_send_forced_count | 0 |
| Ndb_api_adaptive_send_unforced_count | 3 |
| Ndb_api_adaptive_send_deferred_count | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
| Ndb_api_wait_exec_complete_count_slave | 0 |
| Ndb_api_wait_scan_result_count_slave | 0 |
| Ndb_api_wait_meta_request_count_slave | 0 |
| Ndb_api_wait_nanos_count_slave | 0 |
| Ndb_api_bytes_sent_count_slave | 0 |
| Ndb_api_bytes_received_count_slave | 0 |
| Ndb_api_trans_start_count_slave | 0 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_abort_count_slave | 0 |
| Ndb_api_trans_close_count_slave | 0 |
| Ndb_api_pk_op_count_slave | 0 |
| Ndb_api_uk_op_count_slave | 0 |
| Ndb_api_table_scan_count_slave | 0 |
| Ndb_api_range_scan_count_slave | 0 |
| Ndb_api_pruned_scan_count_slave | 0 |
| Ndb_api_scan_batch_count_slave | 0 |
| Ndb_api_read_row_count_slave | 0 |
| Ndb_api_trans_local_read_row_count_slave | 0 |
| Ndb_api_adaptive_send_forced_count_slave | 0 |
| Ndb_api_adaptive_send_unforced_count_slave | 0 |
| Ndb_api_adaptive_send_deferred_count_slave | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
```

```
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+----------------+
69 rows in set (0.00 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.GLOBAL_STATUS
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%';
+----------------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+----------------------------------------------+----------------+
| Ndb_api_wait_exec_complete_count | 2 |
| Ndb_api_wait_scan_result_count | 3 |
| Ndb_api_wait_meta_request_count | 101 |
| Ndb_api_wait_nanos_count | 13640285623 |
| Ndb_api_bytes_sent_count | 13608 |
| Ndb_api_bytes_received_count | 142800 |
| Ndb_api_trans_start_count | 2 |
| Ndb_api_trans_commit_count | 1 |
| Ndb_api_trans_abort_count | 0 |
| Ndb_api_trans_close_count | 2 |
| Ndb_api_pk_op_count | 1 |
| Ndb_api_uk_op_count | 0 |
| Ndb_api_table_scan_count | 1 |
| Ndb_api_range_scan_count | 0 |
| Ndb_api_pruned_scan_count | 0 |
| Ndb_api_scan_batch_count | 0 |
| Ndb_api_read_row_count | 1 |
| Ndb_api_trans_local_read_row_count | 1 |
| Ndb_api_adaptive_send_forced_count | 0 |
| Ndb_api_adaptive_send_unforced_count | 3 |
| Ndb_api_adaptive_send_deferred_count | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
| Ndb_api_wait_exec_complete_count_slave | 0 |
| Ndb_api_wait_scan_result_count_slave | 0 |
| Ndb_api_wait_meta_request_count_slave | 0 |
| Ndb_api_wait_nanos_count_slave | 0 |
| Ndb_api_bytes_sent_count_slave | 0 |
| Ndb_api_bytes_received_count_slave | 0 |
| Ndb_api_trans_start_count_slave | 0 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_abort_count_slave | 0 |
| Ndb_api_trans_close_count_slave | 0 |
| Ndb_api_pk_op_count_slave | 0 |
| Ndb_api_uk_op_count_slave | 0 |
| Ndb_api_table_scan_count_slave | 0 |
| Ndb_api_range_scan_count_slave | 0 |
| Ndb_api_pruned_scan_count_slave | 0 |
| Ndb_api_scan_batch_count_slave | 0 |
| Ndb_api_read_row_count_slave | 0 |
| Ndb_api_trans_local_read_row_count_slave | 0 |
| Ndb_api_adaptive_send_forced_count_slave | 0 |
| Ndb_api_adaptive_send_unforced_count_slave | 0 |
| Ndb_api_adaptive_send_deferred_count_slave | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
```

```
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+----------------+
69 rows in set (0.01 sec)
```

Each [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object has its own counters. NDB API applications can read the values of the counters for use in optimization or monitoring. For multithreaded clients which use more than one [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object concurrently, it is also possible to obtain a summed view of counters from all [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects belonging to a given [Ndb\\_cluster\\_connection](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md).

Four sets of these counters are exposed. One set applies to the current session only; the other 3 are global. This is in spite of the fact that their values can be obtained as either session or global status variables in the mysql client. This means that specifying the SESSION or GLOBAL keyword with SHOW STATUS has no effect on the values reported for NDB API statistics status variables, and the value for each of these variables is the same whether the value is obtained from the equivalent column of the SESSION\_STATUS or the GLOBAL\_STATUS table.

• Session counters (session specific)

Session counters relate to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects in use by (only) the current session. Use of such objects by other MySQL clients does not influence these counts.

In order to minimize confusion with standard MySQL session variables, we refer to the variables that correspond to these NDB API session counters as "\_session variables", with a leading underscore.

• Replica counters (global)

This set of counters relates to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects used by the replicat SQL thread, if any. If this mysqld does not act as a replica, or does not use NDB tables, then all of these counts are 0.

We refer to the related status variables as "\_slave variables" (with a leading underscore).

• Injector counters (global)

Injector counters relate to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object used to listen to cluster events by the binary log injector thread. Even when not writing a binary log, mysqld processes attached to an NDB Cluster continue to listen for some events, such as schema changes.

We refer to the status variables that correspond to NDB API injector counters as "\_injector variables" (with a leading underscore).

• Server (Global) counters (global)

This set of counters relates to all [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects currently used by this mysqld. This includes all MySQL client applications, the replica SQL thread (if any), the binlog injector, and the NDB utility thread.

We refer to the status variables that correspond to these counters as "global variables" or "mysqldlevel variables".

You can obtain values for a particular set of variables by additionally filtering for the substring session, slave, or injector in the variable name (along with the common prefix Ndb\_api). For \_session variables, this can be done as shown here:

```
mysql> SHOW STATUS LIKE 'ndb_api%session';
+--------------------------------------------+---------+
| Variable_name | Value |
+--------------------------------------------+---------+
| Ndb_api_wait_exec_complete_count_session | 2 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 1 |
| Ndb_api_wait_nanos_count_session | 8144375 |
| Ndb_api_bytes_sent_count_session | 68 |
| Ndb_api_bytes_received_count_session | 84 |
| Ndb_api_trans_start_count_session | 1 |
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 1 |
| Ndb_api_pk_op_count_session | 1 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 1 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+---------+
18 rows in set (0.50 sec)
```

To obtain a listing of the NDB API mysqld-level status variables, filter for variable names beginning with ndb\_api and ending in \_count, like this:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.SESSION_STATUS
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%count';
+------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+------------------------------------+----------------+
| NDB_API_WAIT_EXEC_COMPLETE_COUNT | 4 |
| NDB_API_WAIT_SCAN_RESULT_COUNT | 3 |
| NDB_API_WAIT_META_REQUEST_COUNT | 28 |
| NDB_API_WAIT_NANOS_COUNT | 53756398 |
| NDB_API_BYTES_SENT_COUNT | 1060 |
| NDB_API_BYTES_RECEIVED_COUNT | 9724 |
| NDB_API_TRANS_START_COUNT | 3 |
| NDB_API_TRANS_COMMIT_COUNT | 2 |
| NDB_API_TRANS_ABORT_COUNT | 0 |
| NDB_API_TRANS_CLOSE_COUNT | 3 |
| NDB_API_PK_OP_COUNT | 2 |
| NDB_API_UK_OP_COUNT | 0 |
| NDB_API_TABLE_SCAN_COUNT | 1 |
| NDB_API_RANGE_SCAN_COUNT | 0 |
| NDB_API_PRUNED_SCAN_COUNT | 0 |
| NDB_API_SCAN_BATCH_COUNT | 0 |
| NDB_API_READ_ROW_COUNT | 2 |
| NDB_API_TRANS_LOCAL_READ_ROW_COUNT | 2 |
| NDB_API_EVENT_DATA_COUNT | 0 |
| NDB_API_EVENT_NONDATA_COUNT | 0 |
| NDB_API_EVENT_BYTES_COUNT | 0 |
+------------------------------------+----------------+
21 rows in set (0.09 sec)
```

Not all counters are reflected in all 4 sets of status variables. For the event counters DataEventsRecvdCount, NondataEventsRecvdCount, and EventBytesRecvdCount, only \_injector and mysqld-level NDB API status variables are available:

```
mysql> SHOW STATUS LIKE 'ndb_api%event%';
```

```
+--------------------------------------+-------+
| Variable_name | Value |
+--------------------------------------+-------+
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
+--------------------------------------+-------+
6 rows in set (0.00 sec)
```

\_injector status variables are not implemented for any other NDB API counters, as shown here:

```
mysql> SHOW STATUS LIKE 'ndb_api%injector%';
+--------------------------------------+-------+
| Variable_name | Value |
+--------------------------------------+-------+
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
+--------------------------------------+-------+
3 rows in set (0.00 sec)
```

The names of the status variables can easily be associated with the names of the corresponding counters. Each NDB API statistics counter is listed in the following table with a description as well as the names of any MySQL server status variables corresponding to this counter.

**Table 21.61 NDB API statistics counters**

| Counter Name          | Description                                                                               | Status Variables (by statistic<br>type):      |
|-----------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------|
|                       |                                                                                           | •<br>Session                                  |
|                       |                                                                                           | •<br>Slave (replica)                          |
|                       |                                                                                           | •<br>Injector                                 |
|                       |                                                                                           | •<br>Server                                   |
| WaitExecCompleteCount | Number of times thread has<br>been blocked while waiting                                  | •<br>Ndb_api_wait_exec_complete_count_session |
|                       | for execution of an operation                                                             | •<br>Ndb_api_wait_exec_complete_count_slave   |
|                       | to complete. Includes all<br>execute() calls as well                                      | •<br>[none]                                   |
|                       | as implicit executes for blob<br>operations and auto-increment<br>not visible to clients. | •<br>Ndb_api_wait_exec_complete_count         |
| WaitScanResultCount   | Number of times thread has                                                                | •<br>Ndb_api_wait_scan_result_count_session   |
|                       | been blocked while waiting for a<br>scan-based signal, such waiting                       | •<br>Ndb_api_wait_scan_result_count_slave     |
|                       | for additional results, or for a<br>scan to close.                                        | •<br>[none]                                   |
|                       |                                                                                           | •<br>Ndb_api_wait_scan_result_count           |
| WaitMetaRequestCount  | Number of times thread has<br>been blocked waiting for a                                  | •<br>Ndb_api_wait_meta_request_count_session  |
|                       | metadata-based signal; this can                                                           | •<br>Ndb_api_wait_meta_request_count_slave    |
|                       | occur when waiting for a DDL<br>operation or for an epoch to be                           | •<br>[none]                                   |
|                       | started (or ended).                                                                       | •<br>Ndb_api_wait_meta_request_count          |

| Counter Name     | Description                                                        | Status Variables (by statistic<br>type):  |
|------------------|--------------------------------------------------------------------|-------------------------------------------|
|                  |                                                                    | •<br>Session                              |
|                  |                                                                    | •<br>Slave (replica)                      |
|                  |                                                                    | •<br>Injector                             |
|                  |                                                                    | •<br>Server                               |
| WaitNanosCount   | Total time (in nanoseconds)                                        | •<br>Ndb_api_wait_nanos_count_session     |
|                  | spent waiting for some type of<br>signal from the data nodes.      | •<br>Ndb_api_wait_nanos_count_slave       |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_wait_nanos_count             |
| BytesSentCount   | Amount of data (in bytes) sent to<br>the data nodes                | •<br>Ndb_api_bytes_sent_count_session     |
|                  |                                                                    | •<br>Ndb_api_bytes_sent_count_slave       |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_bytes_sent_count             |
| BytesRecvdCount  | Amount of data (in bytes)<br>received from the data nodes          | •<br>Ndb_api_bytes_received_count_session |
|                  |                                                                    | •<br>Ndb_api_bytes_received_count_slave   |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_bytes_received_count         |
| TransStartCount  | Number of transactions started.                                    | •<br>Ndb_api_trans_start_count_session    |
|                  |                                                                    | •<br>Ndb_api_trans_start_count_slave      |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_trans_start_count            |
| TransCommitCount | Number of transactions<br>committed.                               | •<br>Ndb_api_trans_commit_count_session   |
|                  |                                                                    | •<br>Ndb_api_trans_commit_count_slave     |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_trans_commit_count           |
| TransAbortCount  | Number of transactions aborted.                                    | •<br>Ndb_api_trans_abort_count_session    |
|                  |                                                                    | •<br>Ndb_api_trans_abort_count_slave      |
|                  |                                                                    | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_trans_abort_count            |
| TransCloseCount  | Number of transactions aborted.<br>(This value may be greater than | •<br>Ndb_api_trans_close_count_session    |
|                  | the sum of TransCommitCount                                        | •<br>Ndb_api_trans_close_count_slave      |
|                  | and TransAbortCount.)                                              | •<br>[none]                               |
|                  |                                                                    | •<br>Ndb_api_trans_close_count            |
|                  |                                                                    |                                           |

| Counter Name    | Description                                                      | Status Variables (by statistic<br>type):                               |  |  |
|-----------------|------------------------------------------------------------------|------------------------------------------------------------------------|--|--|
|                 |                                                                  | •<br>Session                                                           |  |  |
|                 |                                                                  | •<br>Slave (replica)                                                   |  |  |
|                 |                                                                  | •<br>Injector                                                          |  |  |
|                 |                                                                  | •<br>Server                                                            |  |  |
| PkOpCount       | Number of operations based                                       | •<br>Ndb_api_pk_op_count_session                                       |  |  |
|                 | on or using primary keys. This<br>count includes blob-part table | •<br>Ndb_api_pk_op_count_slave                                         |  |  |
|                 | operations, implicit unlocking                                   | •<br>[none]                                                            |  |  |
|                 | operations, and auto-increment<br>operations, as well as primary |                                                                        |  |  |
|                 | key operations normally visible to<br>MySQL clients.             | •<br>Ndb_api_pk_op_count                                               |  |  |
| UkOpCount       | Number of operations based on                                    | •<br>Ndb_api_uk_op_count_session                                       |  |  |
|                 | or using unique keys.                                            | •<br>Ndb_api_uk_op_count_slave                                         |  |  |
|                 |                                                                  | •<br>[none]                                                            |  |  |
|                 |                                                                  | •                                                                      |  |  |
| TableScanCount  | Number of table scans that                                       | Ndb_api_uk_op_count<br>•<br>Ndb_api_table_scan_count_session           |  |  |
|                 | have been started. This includes                                 | •<br>Ndb_api_table_scan_count_slave                                    |  |  |
|                 | scans of internal tables.                                        |                                                                        |  |  |
|                 |                                                                  | •<br>[none]                                                            |  |  |
| RangeScanCount  | Number of range scans that have                                  | •<br>Ndb_api_table_scan_count<br>•<br>Ndb_api_range_scan_count_session |  |  |
|                 | been started.                                                    |                                                                        |  |  |
|                 |                                                                  | •<br>Ndb_api_range_scan_count_slave                                    |  |  |
|                 |                                                                  | •<br>[none]                                                            |  |  |
|                 |                                                                  | •<br>Ndb_api_range_scan_count                                          |  |  |
| PrunedScanCount | Number of scans that have been<br>pruned to a single partition.  | •<br>Ndb_api_pruned_scan_count_session                                 |  |  |
|                 |                                                                  | •<br>Ndb_api_pruned_scan_count_slave                                   |  |  |
|                 |                                                                  | •<br>[none]                                                            |  |  |
|                 |                                                                  | •<br>Ndb_api_pruned_scan_count                                         |  |  |
| ScanBatchCount  | Number of batches of rows<br>received. (A batch in this context  | •<br>Ndb_api_scan_batch_count_session                                  |  |  |
|                 | is a set of scan results from a                                  | •<br>Ndb_api_scan_batch_count_slave                                    |  |  |
|                 | single fragment.)                                                | •<br>[none]                                                            |  |  |
|                 |                                                                  | •<br>Ndb_api_scan_batch_count                                          |  |  |
| ReadRowCount    | Total number of rows that have<br>been read. Includes rows read  | •<br>Ndb_api_read_row_count_session                                    |  |  |
|                 | using primary key, unique key,                                   | •<br>Ndb_api_read_row_count_slave                                      |  |  |
|                 | and scan operations.                                             | •<br>[none]                                                            |  |  |

| Counter Name            | Description                                                 | Status Variables (by statistic<br>type):        |
|-------------------------|-------------------------------------------------------------|-------------------------------------------------|
|                         |                                                             | •<br>Session                                    |
|                         |                                                             | •<br>Slave (replica)                            |
|                         |                                                             | •<br>Injector                                   |
|                         |                                                             | •<br>Server                                     |
|                         |                                                             | •<br>Ndb_api_read_row_count                     |
| TransLocalReadRowCount  | Number of rows read from the<br>data same node on which the | •<br>Ndb_api_trans_local_read_row_count_session |
|                         | transaction was being run.                                  | •<br>Ndb_api_trans_local_read_row_count_slave   |
|                         |                                                             | •<br>[none]                                     |
|                         |                                                             | •<br>Ndb_api_trans_local_read_row_count         |
| DataEventsRecvdCount    | Number of row change events<br>received.                    | •<br>[none]                                     |
|                         |                                                             | •<br>[none]                                     |
|                         |                                                             | •<br>Ndb_api_event_data_count_injector          |
|                         |                                                             | •<br>Ndb_api_event_data_count                   |
| NondataEventsRecvdCount | Number of events received, other<br>than row change events. | •<br>[none]                                     |
|                         |                                                             | •<br>[none]                                     |
|                         |                                                             | •<br>Ndb_api_event_nondata_count_injector       |
|                         |                                                             | •<br>Ndb_api_event_nondata_count                |
| EventBytesRecvdCount    | Number of bytes of events                                   | •<br>[none]                                     |
|                         | received.                                                   | •<br>[none]                                     |
|                         |                                                             | •<br>Ndb_api_event_bytes_count_injector         |
|                         |                                                             | •<br>Ndb_api_event_bytes_count                  |
|                         |                                                             |                                                 |

To see all counts of committed transactions—that is, all TransCommitCount counter status variables —you can filter the results of SHOW STATUS for the substring trans\_commit\_count, like this:

```
mysql> SHOW STATUS LIKE '%trans_commit_count%';
+------------------------------------+-------+
| Variable_name | Value |
+------------------------------------+-------+
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_commit_count | 2 |
+------------------------------------+-------+
3 rows in set (0.00 sec)
```

From this you can determine that 1 transaction has been committed in the current mysql client session, and 2 transactions have been committed on this mysqld since it was last restarted.

You can see how various NDB API counters are incremented by a given SQL statement by comparing the values of the corresponding \_session status variables immediately before and after performing the statement. In this example, after getting the initial values from SHOW STATUS, we create in the test database an NDB table, named t, that has a single column:

```
mysql> SHOW STATUS LIKE 'ndb_api%session%';
```

```
+--------------------------------------------+--------+
| Variable_name | Value |
+--------------------------------------------+--------+
| Ndb_api_wait_exec_complete_count_session | 2 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 3 |
| Ndb_api_wait_nanos_count_session | 820705 |
| Ndb_api_bytes_sent_count_session | 132 |
| Ndb_api_bytes_received_count_session | 372 |
| Ndb_api_trans_start_count_session | 1 |
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 1 |
| Ndb_api_pk_op_count_session | 1 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 1 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+--------+
18 rows in set (0.00 sec)
mysql> USE test;
Database changed
mysql> CREATE TABLE t (c INT) ENGINE NDBCLUSTER;
Query OK, 0 rows affected (0.85 sec)
```

Now you can execute a new SHOW STATUS statement and observe the changes, as shown here (with the changed rows highlighted in the output):

```
mysql> SHOW STATUS LIKE 'ndb_api%session%';
+--------------------------------------------+-----------+
| Variable_name | Value |
+--------------------------------------------+-----------+
| Ndb_api_wait_exec_complete_count_session | 8 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 17 |
| Ndb_api_wait_nanos_count_session | 706871709 |
| Ndb_api_bytes_sent_count_session | 2376 |
| Ndb_api_bytes_received_count_session | 3844 |
| Ndb_api_trans_start_count_session | 4 |
| Ndb_api_trans_commit_count_session | 4 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 4 |
| Ndb_api_pk_op_count_session | 6 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 2 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+-----------+
18 rows in set (0.00 sec)
```

Similarly, you can see the changes in the NDB API statistics counters caused by inserting a row into t: Insert the row, then run the same SHOW STATUS statement used in the previous example, as shown here:

```
mysql> INSERT INTO t VALUES (100);
Query OK, 1 row affected (0.00 sec)
mysql> SHOW STATUS LIKE 'ndb_api%session%';
+--------------------------------------------+-----------+
| Variable_name | Value |
+--------------------------------------------+-----------+
| Ndb_api_wait_exec_complete_count_session | 11 |
| Ndb_api_wait_scan_result_count_session | 6 |
| Ndb_api_wait_meta_request_count_session | 20 |
```

```
| Ndb_api_wait_nanos_count_session | 707370418 |
| Ndb_api_bytes_sent_count_session | 2724 |
| Ndb_api_bytes_received_count_session | 4116 |
| Ndb_api_trans_start_count_session | 7 |
| Ndb_api_trans_commit_count_session | 6 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 7 |
| Ndb_api_pk_op_count_session | 8 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 1 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 3 |
| Ndb_api_trans_local_read_row_count_session | 2 |
+--------------------------------------------+-----------+
18 rows in set (0.00 sec)
```

We can make a number of observations from these results:

- Although we created t with no explicit primary key, 5 primary key operations were performed in doing so (the difference in the "before" and "after" values of Ndb\_api\_pk\_op\_count\_session, or 6 minus 1). This reflects the creation of the hidden primary key that is a feature of all tables using the NDB storage engine.
- By comparing successive values for Ndb\_api\_wait\_nanos\_count\_session, we can see that the NDB API operations implementing the CREATE TABLE statement waited much longer (706871709 - 820705 = 706051004 nanoseconds, or approximately 0.7 second) for responses from the data nodes than those executed by the INSERT (707370418 - 706871709 = 498709 ns or roughly .0005 second). The execution times reported for these statements in the mysql client correlate roughly with these figures.

On platforms without sufficient (nanosecond) time resolution, small changes in the value of the WaitNanosCount NDB API counter due to SQL statements that execute very quickly may not always be visible in the values of Ndb\_api\_wait\_nanos\_count\_session, Ndb\_api\_wait\_nanos\_count\_slave, or Ndb\_api\_wait\_nanos\_count.

• The INSERT statement incremented both the ReadRowCount and TransLocalReadRowCount NDB API statistics counters, as reflected by the increased values of Ndb\_api\_read\_row\_count\_session and Ndb\_api\_trans\_local\_read\_row\_count\_session.

# <span id="page-21-0"></span>**21.6.15 ndbinfo: The NDB Cluster Information Database**

ndbinfo is a database containing information specific to NDB Cluster.

This database contains a number of tables, each providing a different sort of data about NDB Cluster node status, resource usage, and operations. You can find more detailed information about each of these tables in the next several sections.

ndbinfo is included with NDB Cluster support in the MySQL Server; no special compilation or configuration steps are required; the tables are created by the MySQL Server when it connects to the cluster. You can verify that ndbinfo support is active in a given MySQL Server instance using SHOW PLUGINS; if ndbinfo support is enabled, you should see a row containing ndbinfo in the Name column and ACTIVE in the Status column, as shown here (emphasized text):

| mysql> SHOW PLUGINS;<br>++++++ |               |                         |      |                   |
|--------------------------------|---------------|-------------------------|------|-------------------|
| Name                           | Status   Type |                         |      | Library   License |
| ++++++<br>  binlog             |               | ACTIVE   STORAGE ENGINE | NULL | GPL<br>           |
| mysql_native_password          |               | ACTIVE   AUTHENTICATION | NULL | GPL<br>           |
| sha256_password                |               | ACTIVE   AUTHENTICATION | NULL | GPL<br>           |
| MRG_MYISAM                     |               | ACTIVE   STORAGE ENGINE | NULL | GPL<br>           |
| MEMORY                         |               | ACTIVE   STORAGE ENGINE | NULL | GPL<br>           |

```
| CSV | ACTIVE | STORAGE ENGINE | NULL | GPL |
| MyISAM | ACTIVE | STORAGE ENGINE | NULL | GPL |
| InnoDB | ACTIVE | STORAGE ENGINE | NULL | GPL |
| INNODB_TRX | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_LOCKS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_LOCK_WAITS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP_RESET | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMPMEM | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMPMEM_RESET | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP_PER_INDEX | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP_PER_INDEX_RESET | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_PAGE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_PAGE_LRU | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_POOL_STATS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_TEMP_TABLE_INFO | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_METRICS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_DEFAULT_STOPWORD | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_DELETED | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_BEING_DELETED | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_CONFIG | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_INDEX_CACHE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_INDEX_TABLE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_TABLES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_TABLESTATS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_INDEXES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_COLUMNS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_FIELDS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_FOREIGN | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_FOREIGN_COLS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_TABLESPACES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_DATAFILES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SYS_VIRTUAL | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| PERFORMANCE_SCHEMA | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndbCluster | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndbinfo | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndb_transid_mysql_connection_map | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| BLACKHOLE | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ARCHIVE | ACTIVE | STORAGE ENGINE | NULL | GPL |
| partition | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ngram | ACTIVE | FTPARSER | NULL | GPL |
+----------------------------------+--------+--------------------+---------+---------+
46 rows in set (0.00 sec)
```

You can also do this by checking the output of SHOW ENGINES for a line including ndbinfo in the Engine column and YES in the Support column, as shown here (emphasized text):

```
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
 Engine: ndbcluster
 Support: YES
 Comment: Clustered, fault-tolerant tables
Transactions: YES
 XA: NO
 Savepoints: NO
*************************** 2. row ***************************
 Engine: CSV
 Support: YES
 Comment: CSV storage engine
Transactions: NO
 XA: NO
 Savepoints: NO
*************************** 3. row ***************************
 Engine: InnoDB
 Support: DEFAULT
 Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
 XA: YES
 Savepoints: YES
*************************** 4. row ***************************
 Engine: BLACKHOLE
 Support: YES
```

```
Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
        XA: NO
 Savepoints: NO
                ****** 5. row **************
    Engine: MyISAM
    Support: YES
    Comment: MyISAM storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
             ******* 6. row **************
    Engine: MRG MYISAM
    Support: YES
   Comment: Collection of identical MyISAM tables
Transactions: NO
 Savepoints: NO
                 ****** 7. row **************
    Engine: ARCHIVE
    Support: YES
   Comment: Archive storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
                 ****** 8. row ***************
    Engine: ndbinfo
    Support: YES
    Comment: NDB Cluster system information storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
         ************ 9. row **************
     Engine: PERFORMANCE SCHEMA
   Support: YES
   Comment: Performance Schema
Transactions: NO
        XA: NO
 Savepoints: NO
               ******* 10. row **************
    Engine: MEMORY
   Support: YES
   Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
        XA: NO
 Savepoints: NO
10 rows in set (0.00 sec)
```

If ndbinfo support is enabled, then you can access ndbinfo using SQL statements in mysql or another MySQL client. For example, you can see ndbinfo listed in the output of SHOW DATABASES, as shown here (emphasized text):

```
mysql> SHOW DATABASES;
+------+
| Database
```

If the <code>mysqld</code> process was not started with the <code>--ndbcluster</code> option, <code>ndbinfo</code> is not available and is not displayed by <code>SHOW DATABASES</code>. If <code>mysqld</code> was formerly connected to an NDB Cluster but the cluster becomes unavailable (due to events such as cluster shutdown, loss of network connectivity, and so forth), <code>ndbinfo</code> and its tables remain visible, but an attempt to access any tables (other than <code>blocks or config\_params</code>) fails with <code>Got error 157 'Connection to NDB failed' from NDBINFO</code>.

With the exception of the [blocks](#page-27-0) and [config\\_params](#page-32-0) tables, what we refer to as ndbinfo "tables" are actually views generated from internal NDB tables not normally visible to the MySQL Server. You can make these tables visible by setting the ndbinfo\_show\_hidden system variable to ON (or 1), but this is normally not necessary.

All ndbinfo tables are read-only, and are generated on demand when queried. Because many of them are generated in parallel by the data nodes while other are specific to a given SQL node, they are not guaranteed to provide a consistent snapshot.

In addition, pushing down of joins is not supported on ndbinfo tables; so joining large ndbinfo tables can require transfer of a large amount of data to the requesting API node, even when the query makes use of a WHERE clause.

ndbinfo tables are not included in the query cache. (Bug #59831)

You can select the ndbinfo database with a USE statement, and then issue a SHOW TABLES statement to obtain a list of tables, just as for any other database, like this:

```
mysql> USE ndbinfo;
Database changed
mysql> SHOW TABLES;
+---------------------------------+
| Tables_in_ndbinfo |
+---------------------------------+
| arbitrator_validity_detail |
| arbitrator_validity_summary |
| blocks |
| cluster_locks |
| cluster_operations |
| cluster_transactions |
| config_nodes |
| config_params |
| config_values |
| counters |
| cpustat |
| cpustat_1sec |
| cpustat_20sec |
| cpustat_50ms |
| dict_obj_info |
| dict_obj_types |
| disk_write_speed_aggregate |
| disk_write_speed_aggregate_node |
| disk_write_speed_base |
| diskpagebuffer |
| error_messages |
| locks_per_fragment |
| logbuffers |
| logspaces |
| membership |
| memory_per_fragment |
| memoryusage |
| nodes |
| operations_per_fragment |
| processes |
| resources |
| restart_info |
| server_locks |
| server_operations |
| server_transactions |
| table_distribution_status |
| table_fragments |
| table_info |
| table_replicas |
| tc_time_track_stats |
| threadblocks |
| threads |
| threadstat |
| transporters |
```

```
+---------------------------------+
44 rows in set (0.00 sec)
```

In NDB 7.5.0 (and later), all ndbinfo tables use the NDB storage engine; however, an ndbinfo entry still appears in the output of SHOW ENGINES and SHOW PLUGINS as described previously.

The [config\\_values](#page-33-0) table was added in NDB 7.5.0.

The [cpustat](#page-37-0), [cpustat\\_50ms](#page-38-0), [cpustat\\_1sec](#page-39-0), [cpustat\\_20sec](#page-40-0), and [threads](#page-86-0) tables were added in NDB 7.5.2.

The [cluster\\_locks](#page-27-1), [locks\\_per\\_fragment](#page-47-0), and [server\\_locks](#page-75-0) tables were added in NDB 7.5.3.

The [dict\\_obj\\_info](#page-40-1), [table\\_distribution\\_status](#page-80-0), [table\\_fragments](#page-81-0), [table\\_info](#page-82-0), and [table\\_replicas](#page-83-0) tables were added in NDB 7.5.4.

The [config\\_nodes](#page-31-0) and [processes](#page-69-0) tables were added in NDB 7.5.7.

The [error\\_messages](#page-45-0) table was added in NDB 7.6.

You can execute SELECT statements against these tables, just as you would normally expect:

```
mysql> SELECT * FROM memoryusage;
+---------+---------------------+--------+------------+------------+-------------+
| node_id | memory_type | used | used_pages | total | total_pages |
+---------+---------------------+--------+------------+------------+-------------+
| 5 | Data memory | 753664 | 23 | 1073741824 | 32768 |
| 5 | Index memory | 163840 | 20 | 1074003968 | 131104 |
| 5 | Long message buffer | 2304 | 9 | 67108864 | 262144 |
| 6 | Data memory | 753664 | 23 | 1073741824 | 32768 |
| 6 | Index memory | 163840 | 20 | 1074003968 | 131104 |
| 6 | Long message buffer | 2304 | 9 | 67108864 | 262144 |
+---------+---------------------+--------+------------+------------+-------------+
6 rows in set (0.02 sec)
```

More complex queries, such as the two following SELECT statements using the [memoryusage](#page-52-0) table, are possible:

```
mysql> SELECT SUM(used) as 'Data Memory Used, All Nodes'
 > FROM memoryusage
 > WHERE memory_type = 'Data memory';
+-----------------------------+
| Data Memory Used, All Nodes |
+-----------------------------+
| 6460 |
+-----------------------------+
1 row in set (0.37 sec)
mysql> SELECT SUM(max) as 'Total IndexMemory Available'
 > FROM memoryusage
 > WHERE memory_type = 'Index memory';
+-----------------------------+
| Total IndexMemory Available |
+-----------------------------+
| 25664 |
+-----------------------------+
1 row in set (0.33 sec)
```

ndbinfo table and column names are case-sensitive (as is the name of the ndbinfo database itself). These identifiers are in lowercase. Trying to use the wrong lettercase results in an error, as shown in this example:

```
mysql> SELECT * FROM nodes;
+---------+--------+---------+-------------+
| node_id | uptime | status | start_phase |
+---------+--------+---------+-------------+
| 1 | 13602 | STARTED | 0 |
| 2 | 16 | STARTED | 0 |
```

```
+---------+--------+---------+-------------+
2 rows in set (0.04 sec)
mysql> SELECT * FROM Nodes;
ERROR 1146 (42S02): Table 'ndbinfo.Nodes' doesn't exist
```

mysqldump ignores the ndbinfo database entirely, and excludes it from any output. This is true even when using the --databases or --all-databases option.

NDB Cluster also maintains tables in the INFORMATION\_SCHEMA information database, including the FILES table which contains information about files used for NDB Cluster Disk Data storage, and the ndb\_transid\_mysql\_connection\_map table, which shows the relationships between transactions, transaction coordinators, and NDB Cluster API nodes. For more information, see the descriptions of the tables or [Section 21.6.16, "INFORMATION\\_SCHEMA Tables for NDB Cluster".](#page-90-0)