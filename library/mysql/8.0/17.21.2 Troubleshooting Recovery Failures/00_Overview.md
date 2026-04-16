---
source: MySQL 8.0 Reference
title: 00_Overview
---

From MySQL 8.0.26, checkpoints and advancing the checkpoint LSN are not permitted until redo log recovery is complete and data dictionary dynamic metadata (srv\_dict\_metadata) is transferred to data dictionary table (dict\_table\_t) objects. Should the redo log run out of space during recovery or after recovery (but before data dictionary dynamic metadata is transferred to data dictionary table objects) as a result of this change, an [innodb\\_force\\_recovery](#page-30-0) restart may be required, starting with at least the SRV\_FORCE\_NO\_IBUF\_MERGE setting or, in case that fails, the SRV\_FORCE\_NO\_LOG\_REDO setting. If an [innodb\\_force\\_recovery](#page-30-0) restart fails in this scenario, recovery from backup may be necessary. (Bug #32200595)

# <span id="page-163-0"></span>**17.21.3 Forcing InnoDB Recovery**

To investigate database page corruption, you might dump your tables from the database with SELECT ... INTO OUTFILE. Usually, most of the data obtained in this way is intact. Serious corruption might cause SELECT \* FROM tbl\_name statements or InnoDB background operations to unexpectedly exit or assert, or even cause InnoDB roll-forward recovery to crash. In such cases, you can use the [innodb\\_force\\_recovery](#page-30-0) option to force the InnoDB storage engine to start up while preventing background operations from running, so that you can dump your tables. For example, you can add the following line to the [mysqld] section of your option file before restarting the server:

```
[mysqld]
innodb_force_recovery = 1
```

For information about using option files, see Section 6.2.2.2, "Using Option Files".

![](_page_164_Picture_1.jpeg)

#### **Warning**

Only set [innodb\\_force\\_recovery](#page-30-0) to a value greater than 0 in an emergency situation, so that you can start InnoDB and dump your tables. Before doing so, ensure that you have a backup copy of your database in case you need to recreate it. Values of 4 or greater can permanently corrupt data files. Only use an [innodb\\_force\\_recovery](#page-30-0) setting of 4 or greater on a production server instance after you have successfully tested the setting on a separate physical copy of your database. When forcing InnoDB recovery, you should always start with [innodb\\_force\\_recovery=1](#page-30-0) and only increase the value incrementally, as necessary.

[innodb\\_force\\_recovery](#page-30-0) is 0 by default (normal startup without forced recovery). The permissible nonzero values for [innodb\\_force\\_recovery](#page-30-0) are 1 to 6. A larger value includes the functionality of lesser values. For example, a value of 3 includes all of the functionality of values 1 and 2.

If you are able to dump your tables with an [innodb\\_force\\_recovery](#page-30-0) value of 3 or less, then you are relatively safe that only some data on corrupt individual pages is lost. A value of 4 or greater is considered dangerous because data files can be permanently corrupted. A value of 6 is considered drastic because database pages are left in an obsolete state, which in turn may introduce more corruption into B-trees and other database structures.

As a safety measure, InnoDB prevents INSERT, UPDATE, or DELETE operations when [innodb\\_force\\_recovery](#page-30-0) is greater than 0. An [innodb\\_force\\_recovery](#page-30-0) setting of 4 or greater places InnoDB in read-only mode.

• 1 (SRV\_FORCE\_IGNORE\_CORRUPT)

Lets the server run even if it detects a corrupt page. Tries to make SELECT \* FROM tbl\_name jump over corrupt index records and pages, which helps in dumping tables.

• 2 (SRV\_FORCE\_NO\_BACKGROUND)

Prevents the master thread and any purge threads from running. If an unexpected exit would occur during the purge operation, this recovery value prevents it.

• 3 (SRV\_FORCE\_NO\_TRX\_UNDO)

Does not run transaction rollbacks after crash recovery.

• 4 (SRV\_FORCE\_NO\_IBUF\_MERGE)

Prevents insert buffer merge operations. If they would cause a crash, does not do them. Does not calculate table statistics. This value can permanently corrupt data files. After using this value, be prepared to drop and recreate all secondary indexes. Sets InnoDB to read-only.

• 5 (SRV\_FORCE\_NO\_UNDO\_LOG\_SCAN)

Does not look at undo logs when starting the database: InnoDB treats even incomplete transactions as committed. This value can permanently corrupt data files. Sets InnoDB to read-only.

• 6 (SRV\_FORCE\_NO\_LOG\_REDO)

Does not do the redo log roll-forward in connection with recovery. This value can permanently corrupt data files. Leaves database pages in an obsolete state, which in turn may introduce more corruption into B-trees and other database structures. Sets InnoDB to read-only.

You can SELECT from tables to dump them. With an [innodb\\_force\\_recovery](#page-30-0) value of 3 or less you can DROP or CREATE tables. DROP TABLE is also supported with an [innodb\\_force\\_recovery](#page-30-0) value greater than 3. DROP TABLE is not permitted with an [innodb\\_force\\_recovery](#page-30-0) value greater than 4.

If you know that a given table is causing an unexpected exit on rollback, you can drop it. If you encounter a runaway rollback caused by a failing mass import or ALTER TABLE, you can kill the mysqld process and set [innodb\\_force\\_recovery](#page-30-0) to 3 to bring the database up without the rollback, and then DROP the table that is causing the runaway rollback.

If corruption within the table data prevents you from dumping the entire table contents, a query with an ORDER BY primary\_key DESC clause might be able to dump the portion of the table after the corrupted part.

If a high [innodb\\_force\\_recovery](#page-30-0) value is required to start InnoDB, there may be corrupted data structures that could cause complex queries (queries containing WHERE, ORDER BY, or other clauses) to fail. In this case, you may only be able to run basic SELECT \* FROM t queries.

## <span id="page-165-0"></span>**17.21.4 Troubleshooting InnoDB Data Dictionary Operations**

Information about table definitions is stored in the InnoDB data dictionary. If you move data files around, dictionary data can become inconsistent.

If a data dictionary corruption or consistency issue prevents you from starting InnoDB, see [Section 17.21.3, "Forcing InnoDB Recovery"](#page-163-0) for information about manual recovery.

## **Cannot Open Datafile**

With [innodb\\_file\\_per\\_table](#page-23-1) enabled (the default), the following messages may appear at startup if a file-per-table tablespace file (.ibd file) is missing:

```
[ERROR] InnoDB: Operating system error number 2 in a file operation.
[ERROR] InnoDB: The error means the system cannot find the path specified.
[ERROR] InnoDB: Cannot open datafile for read-only: './test/t1.ibd' OS error: 71
[Warning] InnoDB: Ignoring tablespace `test/t1` because it could not be opened.
```

To address these messages, issue DROP TABLE statement to remove data about the missing table from the data dictionary.

## **Restoring Orphan File-Per-Table ibd Files**

This procedure describes how to restore orphan file-per-table .ibd files to another MySQL instance. You might use this procedure if the system tablespace is lost or unrecoverable and you want to restore .ibd file backups on a new MySQL instance.

The procedure is not supported for general tablespace .ibd files.

The procedure assumes that you only have .ibd file backups, you are recovering to the same version of MySQL that initially created the orphan .ibd files, and that .ibd file backups are clean. See Section 17.6.1.4, "Moving or Copying InnoDB Tables" for information about creating clean backups.

Table import limitations outlined in Section 17.6.1.3, "Importing InnoDB Tables" are applicable to this procedure.

1. On the new MySQL instance, recreate the table in a database of the same name.

```
mysql> CREATE DATABASE sakila;
mysql> USE sakila;
mysql> CREATE TABLE actor (
 actor_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 first_name VARCHAR(45) NOT NULL,
 last_name VARCHAR(45) NOT NULL,
 last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (actor_id),
 KEY idx_actor_last_name (last_name)
 )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

2. Discard the tablespace of the newly created table.

```
mysql> ALTER TABLE sakila.actor DISCARD TABLESPACE;
```

3. Copy the orphan .ibd file from your backup directory to the new database directory.

```
$> cp /backup_directory/actor.ibd path/to/mysql-5.7/data/sakila/
```

- 4. Ensure that the .ibd file has the necessary file permissions.
- 5. Import the orphan .ibd file. A warning is issued indicating that InnoDB is attempting to import the file without schema verification.

```
mysql> ALTER TABLE sakila.actor IMPORT TABLESPACE; SHOW WARNINGS;
Query OK, 0 rows affected, 1 warning (0.15 sec)
Warning | 1810 | InnoDB: IO Read error: (2, No such file or directory)
Error opening './sakila/actor.cfg', will attempt to import
without schema verification
```

6. Query the table to verify that the .ibd file was successfully restored.

```
mysql> SELECT COUNT(*) FROM sakila.actor;
+----------+
| count(*) |
+----------+
| 200 |
+----------+
```

## <span id="page-166-0"></span>**17.21.5 InnoDB Error Handling**

The following items describe how InnoDB performs error handling. InnoDB sometimes rolls back only the statement that failed, other times it rolls back the entire transaction.

- If you run out of file space in a tablespace, a MySQL Table is full error occurs and InnoDB rolls back the SQL statement.
- A transaction deadlock causes InnoDB to roll back the entire transaction. Retry the entire transaction when this happens.

A lock wait timeout causes InnoDB to roll back the current statement (the statement that was waiting for the lock and encountered the timeout). To have the entire transaction roll back, start the server with [--innodb-rollback-on-timeout](#page-60-0) enabled. Retry the statement if using the default behavior, or the entire transaction if [--innodb-rollback-on-timeout](#page-60-0) is enabled.

Both deadlocks and lock wait timeouts are normal on busy servers and it is necessary for applications to be aware that they may happen and handle them by retrying. You can make them less likely by doing as little work as possible between the first change to data during a transaction and the commit, so the locks are held for the shortest possible time and for the smallest possible number of rows. Sometimes splitting work between different transactions may be practical and helpful.

- A duplicate-key error rolls back the SQL statement, if you have not specified the IGNORE option in your statement.
- A row too long error rolls back the SQL statement.
- Other errors are mostly detected by the MySQL layer of code (above the InnoDB storage engine level), and they roll back the corresponding SQL statement. Locks are not released in a rollback of a single SQL statement.

During implicit rollbacks, as well as during the execution of an explicit ROLLBACK SQL statement, SHOW PROCESSLIST displays Rolling back in the State column for the relevant connection.

# <span id="page-166-1"></span>**17.22 InnoDB Limits**

This section describes limits for InnoDB tables, indexes, tablespaces, and other aspects of the InnoDB storage engine.

- A table can contain a maximum of 1017 columns. Virtual generated columns are included in this limit.
- A table can contain a maximum of 64 secondary indexes.
- The index key prefix length limit is 3072 bytes for InnoDB tables that use DYNAMIC or COMPRESSED row format.

The index key prefix length limit is 767 bytes for InnoDB tables that use the REDUNDANT or COMPACT row format. For example, you might hit this limit with a column prefix index of more than 191 characters on a TEXT or VARCHAR column, assuming a utf8mb4 character set and the maximum of 4 bytes for each character.

Attempting to use an index key prefix length that exceeds the limit returns an error.

If you reduce the InnoDB page size to 8KB or 4KB by specifying the [innodb\\_page\\_size](#page-52-0) option when creating the MySQL instance, the maximum length of the index key is lowered proportionally, based on the limit of 3072 bytes for a 16KB page size. That is, the maximum index key length is 1536 bytes when the page size is 8KB, and 768 bytes when the page size is 4KB.

The limits that apply to index key prefixes also apply to full-column index keys.

• A maximum of 16 columns is permitted for multicolumn indexes. Exceeding the limit returns an error.

```
ERROR 1070 (42000): Too many key parts specified; max 16 parts allowed
```

• The maximum row size, excluding any variable-length columns that are stored off-page, is slightly less than half of a page for 4KB, 8KB, 16KB, and 32KB page sizes. For example, the maximum row size for the default [innodb\\_page\\_size](#page-52-0) of 16KB is about 8000 bytes. However, for an InnoDB page size of 64KB, the maximum row size is approximately 16000 bytes. LONGBLOB and LONGTEXT columns must be less than 4GB, and the total row size, including BLOB and TEXT columns, must be less than 4GB.

If a row is less than half a page long, all of it is stored locally within the page. If it exceeds half a page, variable-length columns are chosen for external off-page storage until the row fits within half a page, as described in Section 17.11.2, "File Space Management".

- Although InnoDB supports row sizes larger than 65,535 bytes internally, MySQL itself imposes a row-size limit of 65,535 for the combined size of all columns. See Section 10.4.7, "Limits on Table Column Count and Row Size".
- The maximum table or tablespace size is impacted by the server file system, which can impose a maximum file size that is smaller than the internal 64 TiB size limit defined by InnoDB. For example, the ext4 file system on Linux has a maximum file size of 16 TiB, so the maximum table or tablespace size becomes 16 TiB instead of 64 TiB. Another example is the FAT32 file system, which has a maximum file size of 4 GB.

If you require a larger system tablespace, configure it using several smaller data files rather than one large data file, or distribute table data across file-per-table and general tablespace data files.

- The combined maximum size for InnoDB log files is 512GB.
- The minimum tablespace size is slightly larger than 10MB. The maximum tablespace size depends on the InnoDB page size.

**Table 17.31 InnoDB Maximum Tablespace Size**

| InnoDB Page Size | Maximum Tablespace Size |  |
|------------------|-------------------------|--|
| 4KB              | 16TB                    |  |

| InnoDB Page Size | Maximum Tablespace Size |
|------------------|-------------------------|
| 8KB              | 32TB                    |
| 16KB             | 64TB                    |
| 32KB             | 128TB                   |
| 64KB             | 256TB                   |

The maximum tablespace size is also the maximum size for a table.

- An InnoDB instance supports up to 2^32 (4294967296) tablespaces, with a small number of those tablespaces reserved for undo and temporary tables.
- Shared tablespaces support up to 2^32 (4294967296) tables.
- The path of a tablespace file, including the file name, cannot exceed the MAX\_PATH limit on Windows. Prior to Windows 10, the MAX\_PATH limit is 260 characters. As of Windows 10, version 1607, MAX\_PATH limitations are removed from common Win32 file and directory functions, but you must enable the new behavior.
- For limits associated with concurrent read-write transactions, see Section 17.6.6, "Undo Logs".