---
source: MySQL 8.4 Reference
title: 00_Overview
---

Checkpoints and advancing the checkpoint LSN are not permitted until redo log recovery is complete and data dictionary dynamic metadata (srv\_dict\_metadata) is transferred to data dictionary table (dict\_table\_t) objects. Should the redo log run out of space during recovery or after recovery (but before data dictionary dynamic metadata is transferred to data dictionary table objects) as a result of this change, an [innodb\\_force\\_recovery](#page-18-2) restart may be required, starting with at least the SRV\_FORCE\_NO\_IBUF\_MERGE setting or, in case that fails, the SRV\_FORCE\_NO\_LOG\_REDO setting. If an [innodb\\_force\\_recovery](#page-18-2) restart fails in this scenario, recovery from backup may be necessary.

# <span id="page-118-0"></span>**17.20.3 Forcing InnoDB Recovery**

To investigate database page corruption, you might dump your tables from the database with SELECT ... INTO OUTFILE. Usually, most of the data obtained in this way is intact. Serious corruption might cause SELECT \* FROM tbl\_name statements or InnoDB background operations to unexpectedly exit or assert, or even cause InnoDB roll-forward recovery to crash. In such cases, you can use the [innodb\\_force\\_recovery](#page-18-2) option to force the InnoDB storage engine to start up while preventing background operations from running, so that you can dump your tables. For example, you can add the following line to the [mysqld] section of your option file before restarting the server:

```
[mysqld]
innodb_force_recovery = 1
```

For information about using option files, see Section 6.2.2.2, "Using Option Files".

![](_page_118_Picture_16.jpeg)

### **Warning**

Only set [innodb\\_force\\_recovery](#page-18-2) to a value greater than 0 in an emergency situation, so that you can start InnoDB and dump your tables. Before doing so, ensure that you have a backup copy of your database in case you need to recreate it. Values of 4 or greater can permanently corrupt data files. Only use an [innodb\\_force\\_recovery](#page-18-2) setting of 4 or greater on a production server instance after you have successfully tested the setting on a separate physical copy of your database. When forcing InnoDB recovery, you should always start with [innodb\\_force\\_recovery=1](#page-18-2) and only increase the value incrementally, as necessary.

[innodb\\_force\\_recovery](#page-18-2) is 0 by default (normal startup without forced recovery). The permissible nonzero values for [innodb\\_force\\_recovery](#page-18-2) are 1 to 6. A larger value includes the functionality of lesser values. For example, a value of 3 includes all of the functionality of values 1 and 2.

If you are able to dump your tables with an [innodb\\_force\\_recovery](#page-18-2) value of 3 or less, then you are relatively safe that only some data on corrupt individual pages is lost. A value of 4 or greater is considered dangerous because data files can be permanently corrupted. A value of 6 is considered drastic because database pages are left in an obsolete state, which in turn may introduce more corruption into B-trees and other database structures.

As a safety measure, InnoDB prevents INSERT, UPDATE, or DELETE operations when [innodb\\_force\\_recovery](#page-18-2) is greater than 0. An [innodb\\_force\\_recovery](#page-18-2) setting of 4 or greater places InnoDB in read-only mode.

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

You can SELECT from tables to dump them. With an [innodb\\_force\\_recovery](#page-18-2) value of 3 or less you can DROP or CREATE tables. DROP TABLE is also supported with an [innodb\\_force\\_recovery](#page-18-2) value greater than 3. DROP TABLE is not permitted with an [innodb\\_force\\_recovery](#page-18-2) value greater than 4.

If you know that a given table is causing an unexpected exit on rollback, you can drop it. If you encounter a runaway rollback caused by a failing mass import or ALTER TABLE, you can kill the mysqld process and set [innodb\\_force\\_recovery](#page-18-2) to 3 to bring the database up without the rollback, and then DROP the table that is causing the runaway rollback.

If corruption within the table data prevents you from dumping the entire table contents, a query with an ORDER BY primary\_key DESC clause might be able to dump the portion of the table after the corrupted part.

If a high [innodb\\_force\\_recovery](#page-18-2) value is required to start InnoDB, there may be corrupted data structures that could cause complex queries (queries containing WHERE, ORDER BY, or other clauses) to fail. In this case, you may only be able to run basic SELECT \* FROM t queries.

# <span id="page-120-0"></span>**17.20.4 Troubleshooting InnoDB Data Dictionary Operations**

Information about table definitions is stored in the InnoDB data dictionary. If you move data files around, dictionary data can become inconsistent.

If a data dictionary corruption or consistency issue prevents you from starting InnoDB, see [Section 17.20.3, "Forcing InnoDB Recovery"](#page-118-0) for information about manual recovery.

## **Cannot Open Datafile**

With [innodb\\_file\\_per\\_table](#page-12-1) enabled (the default), the following messages may appear at startup if a file-per-table tablespace file (.ibd file) is missing:

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
 -> actor_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 -> first_name VARCHAR(45) NOT NULL,
 -> last_name VARCHAR(45) NOT NULL,
 -> last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 -> PRIMARY KEY (actor_id),
 -> KEY idx_actor_last_name (last_name)
 -> )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
```

```
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

# <span id="page-121-0"></span>**17.20.5 InnoDB Error Handling**

The following items describe how InnoDB performs error handling. InnoDB sometimes rolls back only the statement that failed, other times it rolls back the entire transaction.

- If you run out of file space in a tablespace, a MySQL Table is full error occurs and InnoDB rolls back the SQL statement.
- A transaction deadlock causes InnoDB to roll back the entire transaction. Retry the entire transaction when this happens.

A lock wait timeout causes InnoDB to roll back the current statement (the statement that was waiting for the lock and encountered the timeout). To have the entire transaction roll back, start the server with [--innodb-rollback-on-timeout](#page-49-0) enabled. Retry the statement if using the default behavior, or the entire transaction if [--innodb-rollback-on-timeout](#page-49-0) is enabled.

Both deadlocks and lock wait timeouts are normal on busy servers and it is necessary for applications to be aware that they may happen and handle them by retrying. You can make them less likely by doing as little work as possible between the first change to data during a transaction and the commit, so the locks are held for the shortest possible time and for the smallest possible number of rows. Sometimes splitting work between different transactions may be practical and helpful.

- A duplicate-key error rolls back the SQL statement, if you have not specified the IGNORE option in your statement.
- A row too long error rolls back the SQL statement.
- Other errors are mostly detected by the MySQL layer of code (above the InnoDB storage engine level), and they roll back the corresponding SQL statement. Locks are not released in a rollback of a single SQL statement.

During implicit rollbacks, as well as during the execution of an explicit ROLLBACK SQL statement, SHOW PROCESSLIST displays Rolling back in the State column for the relevant connection.