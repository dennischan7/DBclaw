---
source: MySQL 8.0 Reference
title: 00_Overview
---

The failure of an online DDL operation is typically due to one of the following conditions:

- An ALGORITHM clause specifies an algorithm that is not compatible with the particular type of DDL operation or storage engine.
- A LOCK clause specifies a low degree of locking (SHARED or NONE) that is not compatible with the particular type of DDL operation.
- A timeout occurs while waiting for an exclusive lock on the table, which may be needed briefly during the initial and final phases of the DDL operation.
- The tmpdir or innodb\_tmpdir file system runs out of disk space, while MySQL writes temporary sort files on disk during index creation. For more information, see [Section 17.12.3, "Online DDL](#page-175-0) [Space Requirements".](#page-175-0)
- The operation takes a long time and concurrent DML modifies the table so much that the size of the temporary online log exceeds the value of the innodb\_online\_alter\_log\_max\_size configuration option. This condition causes a DB\_ONLINE\_LOG\_TOO\_BIG error.
- Concurrent DML makes changes to the table that are allowed with the original table definition, but not with the new one. The operation only fails at the very end, when MySQL tries to apply all the changes from concurrent DML statements. For example, you might insert duplicate values into a column while a unique index is being created, or you might insert NULL values into a column

while creating a primary key index on that column. The changes made by the concurrent DML take precedence, and the ALTER TABLE operation is effectively rolled back.

# <span id="page-178-1"></span>**17.12.8 Online DDL Limitations**

The following limitations apply to online DDL operations:

- The table is copied when creating an index on a TEMPORARY TABLE.
- The ALTER TABLE clause LOCK=NONE is not permitted if there are ON...CASCADE or ON...SET NULL constraints on the table.
- Before an in-place online DDL operation can finish, it must wait for transactions that hold metadata locks on the table to commit or roll back. An online DDL operation may briefly require an exclusive metadata lock on the table during its execution phase, and always requires one in the final phase of the operation when updating the table definition. Consequently, transactions holding metadata locks on the table can cause an online DDL operation to block. The transactions that hold metadata locks on the table may have been started before or during the online DDL operation. A long running or inactive transaction that holds a metadata lock on the table can cause an online DDL operation to timeout.
- When running an in-place online DDL operation, the thread that runs the ALTER TABLE statement applies an online log of DML operations that were run concurrently on the same table from other connection threads. When the DML operations are applied, it is possible to encounter a duplicate key entry error (ERROR 1062 (23000): Duplicate entry), even if the duplicate entry is only temporary and would be reverted by a later entry in the online log. This is similar to the idea of a foreign key constraint check in InnoDB in which constraints must hold during a transaction.
- OPTIMIZE TABLE for an InnoDB table is mapped to an ALTER TABLE operation to rebuild the table and update index statistics and free unused space in the clustered index. Secondary indexes are not created as efficiently because keys are inserted in the order they appeared in the primary key. OPTIMIZE TABLE is supported with the addition of online DDL support for rebuilding regular and partitioned InnoDB tables.
- Tables created before MySQL 5.6 that include temporal columns (DATE, DATETIME or TIMESTAMP) and have not been rebuilt using ALGORITHM=COPY do not support ALGORITHM=INPLACE. In this case, an ALTER TABLE ... ALGORITHM=INPLACE operation returns the following error:

```
ERROR 1846 (0A000): ALGORITHM=INPLACE is not supported.
Reason: Cannot change column type INPLACE. Try ALGORITHM=COPY.
```

- The following limitations are generally applicable to online DDL operations on large tables that involve rebuilding the table:
  - There is no mechanism to pause an online DDL operation or to throttle I/O or CPU usage for an online DDL operation.
  - Rollback of an online DDL operation can be expensive should the operation fail.
  - Long running online DDL operations can cause replication lag. An online DDL operation must finish running on the source before it is run on the replica. Also, DML that was processed concurrently on the source is only processed on the replica after the DDL operation on the replica is completed.

For additional information related to running online DDL operations on large tables, see [Section 17.12.2, "Online DDL Performance and Concurrency"](#page-172-1).

# <span id="page-178-0"></span>**17.13 InnoDB Data-at-Rest Encryption**

InnoDB supports data-at-rest encryption for file-per-table tablespaces, general tablespaces, the mysql system tablespace, redo logs, and undo logs.

As of MySQL 8.0.16, setting an encryption default for schemas and general tablespaces is also supported, which permits DBAs to control whether tables created in those schemas and tablespaces are encrypted.

InnoDB data-at-rest encryption features and capabilities are described under the following topics in this section.

- [About Data-at-Rest Encryption](#page-179-0)
- [Encryption Prerequisites](#page-180-0)
- [Defining an Encryption Default for Schemas and General Tablespaces](#page-180-1)
- [File-Per-Table Tablespace Encryption](#page-181-0)
- [General Tablespace Encryption](#page-182-1)
- [Doublewrite File Encryption](#page-182-2)
- [mysql System Tablespace Encryption](#page-182-3)
- [Redo Log Encryption](#page-182-0)
- [Undo Log Encryption](#page-183-0)
- [Master Key Rotation](#page-183-1)
- [Encryption and Recovery](#page-184-0)
- [Exporting Encrypted Tablespaces](#page-184-1)
- [Encryption and Replication](#page-184-2)
- [Identifying Encrypted Tablespaces and Schemas](#page-184-3)
- [Monitoring Encryption Progress](#page-185-0)
- [Encryption Usage Notes](#page-186-0)
- [Encryption Limitations](#page-187-0)

# <span id="page-179-0"></span>**About Data-at-Rest Encryption**

InnoDB uses a two tier encryption key architecture, consisting of a master encryption key and tablespace keys. When a tablespace is encrypted, a tablespace key is encrypted and stored in the tablespace header. When an application or authenticated user wants to access encrypted tablespace data, InnoDB uses a master encryption key to decrypt the tablespace key. The decrypted version of a tablespace key never changes, but the master encryption key can be changed as required. This action is referred to as master key rotation.

The data-at-rest encryption feature relies on a keyring component or plugin for master encryption key management.

All MySQL editions provide a component\_keyring\_file component and keyring\_file plugin, each of which stores keyring data in a file local to the server host.

MySQL Enterprise Edition offers additional keyring components and plugins:

- component\_keyring\_encrypted\_file: Stores keyring data in an encrypted, passwordprotected file local to the server host.
- keyring\_encrypted\_file: Stores keyring data in an encrypted, password-protected file local to the server host.
- keyring\_okv: A KMIP 1.1 plugin for use with KMIP-compatible back end keyring storage products. Supported KMIP-compatible products include centralized key management solutions such as

Oracle Key Vault, Gemalto KeySecure, Thales Vormetric key management server, and Fornetix Key Orchestration.

- keyring\_aws: Communicates with the Amazon Web Services Key Management Service (AWS KMS) as a back end for key generation and uses a local file for key storage.
- keyring\_hashicorp: Communicates with HashiCorp Vault for back end storage.

![](_page_180_Picture_4.jpeg)

#### **Warning**

For encryption key management, the component\_keyring\_file and component\_keyring\_encrypted\_file components, and the keyring\_file and keyring\_encrypted\_file plugins are not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

A secure and robust encryption key management solution is critical for security and for compliance with various security standards. When the data-at-rest encryption feature uses a centralized key management solution, the feature is referred to as "MySQL Enterprise Transparent Data Encryption (TDE)".

The data-at-rest encryption feature supports the Advanced Encryption Standard (AES) block-based encryption algorithm. It uses Electronic Codebook (ECB) block encryption mode for tablespace key encryption and Cipher Block Chaining (CBC) block encryption mode for data encryption.

For frequently asked questions about the data-at-rest encryption feature, see Section A.17, "MySQL 8.0 FAQ: InnoDB Data-at-Rest Encryption".

# <span id="page-180-0"></span>**Encryption Prerequisites**

• A keyring component or plugin must be installed and configured at startup. Early loading ensures that the component or plugin is available prior to initialization of the InnoDB storage engine. For keyring installation and configuration instructions, see Section 8.4.4, "The MySQL Keyring". The instructions show how to ensure that the chosen component or plugin is active.

Only one keyring component or plugin should be enabled at a time. Enabling multiple keyring components or plugins is unsupported and results may not be as anticipated.

![](_page_180_Picture_13.jpeg)

#### **Important**

Once encrypted tablespaces are created in a MySQL instance, the keyring component or plugin that was loaded when creating the encrypted tablespace must continue to be loaded at startup. Failing to do so results in errors when starting the server and during InnoDB recovery.

• When encrypting production data, ensure that you take steps to prevent loss of the master encryption key. If the master encryption key is lost, data stored in encrypted tablespace files is unrecoverable. If you use the component\_keyring\_file or component\_keyring\_encrypted\_file component, or the keyring\_file or keyring\_encrypted\_file plugin, create a backup of the keyring data file immediately after creating the first encrypted tablespace, before master key rotation, and after master key rotation. For each component, its configuration file indicates the data file location. The keyring\_file\_data configuration option defines the keyring data file location for the keyring\_file plugin. The keyring\_encrypted\_file\_data configuration option defines the keyring data file location for the keyring\_encrypted\_file plugin. If you use the keyring\_okv or keyring\_aws plugin, ensure that you have performed the necessary configuration. For instructions, see Section 8.4.4, "The MySQL Keyring".

# <span id="page-180-1"></span>**Defining an Encryption Default for Schemas and General Tablespaces**

As of MySQL 8.0.16, the default\_table\_encryption system variable defines the default encryption setting for schemas and general tablespaces. CREATE TABLESPACE and CREATE SCHEMA operations apply the default\_table\_encryption setting when an ENCRYPTION clause is not specified explicitly.

ALTER SCHEMA and ALTER TABLESPACE operations do not apply the default\_table\_encryption setting. An ENCRYPTION clause must be specified explicitly to alter the encryption of an existing schema or general tablespace.

The default\_table\_encryption variable can be set for an individual client connection or globally using SET syntax. For example, the following statement enables default schema and tablespace encryption globally:

```
mysql> SET GLOBAL default_table_encryption=ON;
```

The default encryption setting for a schema can also be defined using the DEFAULT ENCRYPTION clause when creating or altering a schema, as in this example:

```
mysql> CREATE SCHEMA test DEFAULT ENCRYPTION = 'Y';
```

If the DEFAULT ENCRYPTION clause is not specified when creating a schema, the default\_table\_encryption setting is applied. The DEFAULT ENCRYPTION clause must be specified to alter the default encryption of an existing schema. Otherwise, the schema retains its current encryption setting.

By default, a table inherits the encryption setting of the schema or general tablespace it is created in. For example, a table created in an encryption-enabled schema is encrypted by default. This behavior enables a DBA to control table encryption usage by defining and enforcing schema and general tablespace encryption defaults.

Encryption defaults are enforced by enabling the table\_encryption\_privilege\_check system variable. When table\_encryption\_privilege\_check is enabled, a privilege check occurs when creating or altering a schema or general tablespace with an encryption setting that differs from the default\_table\_encryption setting, or when creating or altering a table with an encryption setting that differs from the default schema encryption. When table\_encryption\_privilege\_check is disabled (the default), the privilege check does not occur and the previously mentioned operations are permitted to proceed with a warning.

The TABLE\_ENCRYPTION\_ADMIN privilege is required to override default encryption settings when table\_encryption\_privilege\_check is enabled. A DBA can grant this privilege to enable a user to deviate from the default\_table\_encryption setting when creating or altering a schema or general tablespace, or to deviate from the default schema encryption when creating or altering a table. This privilege does not permit deviating from the encryption of a general tablespace when creating or altering a table. A table must have the same encryption setting as the general tablespace it resides in.

# <span id="page-181-0"></span>**File-Per-Table Tablespace Encryption**

As of MySQL 8.0.16, a file-per-table tablespace inherits the default encryption of the schema in which the table is created unless an ENCRYPTION clause is specified explicitly in the CREATE TABLE statement. Prior to MySQL 8.0.16, the ENCRYPTION clause must be specified to enable encryption.

```
mysql> CREATE TABLE t1 (c1 INT) ENCRYPTION = 'Y';
```

To alter the encryption of an existing file-per-table tablespace, an ENCRYPTION clause must be specified.

```
mysql> ALTER TABLE t1 ENCRYPTION = 'Y';
```

As of MySQL 8.0.16, if the table\_encryption\_privilege\_check variable is enabled, specifying an ENCRYPTION clause with a setting that differs from the default schema encryption requires the TABLE\_ENCRYPTION\_ADMIN privilege. See [Defining an Encryption Default for Schemas and General](#page-180-1) [Tablespaces.](#page-180-1)

# <span id="page-182-1"></span>**General Tablespace Encryption**

As of MySQL 8.0.16, the default\_table\_encryption variable determines the encryption of a newly created general tablespace unless an ENCRYPTION clause is specified explicitly in the CREATE TABLESPACE statement. Prior to MySQL 8.0.16, an ENCRYPTION clause must be specified to enable encryption.

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' ENCRYPTION = 'Y' Engine=InnoDB;
```

To alter the encryption of an existing general tablespace, an ENCRYPTION clause must be specified.

```
mysql> ALTER TABLESPACE ts1 ENCRYPTION = 'Y';
```

As of MySQL 8.0.16, if the table\_encryption\_privilege\_check variable is enabled, specifying an ENCRYPTION clause with a setting that differs from the default\_table\_encryption setting requires the TABLE\_ENCRYPTION\_ADMIN privilege. See [Defining an Encryption Default for Schemas](#page-180-1) [and General Tablespaces](#page-180-1).

# <span id="page-182-2"></span>**Doublewrite File Encryption**

Encryption support for doublewrite files is available as of MySQL 8.0.23. InnoDB automatically encrypts doublewrite file pages that belong to encrypted tablespaces. No action is required. Doublewrite file pages are encrypted using the encryption key of the associated tablespace. The same encrypted page written to a tablespace data file is also written to a doublewrite file. Doublewrite file pages that belong to an unencrypted tablespace remain unencrypted.

During recovery, encrypted doublewrite file pages are unencrypted and checked for corruption.

# <span id="page-182-3"></span>**mysql System Tablespace Encryption**

Encryption support for the mysql system tablespace is available as of MySQL 8.0.16.

The mysql system tablespace contains the mysql system database and MySQL data dictionary tables. It is unencrypted by default. To enable encryption for the mysql system tablespace, specify the tablespace name and the ENCRYPTION option in an ALTER TABLESPACE statement.

```
mysql> ALTER TABLESPACE mysql ENCRYPTION = 'Y';
```

To disable encryption for the mysql system tablespace, set ENCRYPTION = 'N' using an ALTER TABLESPACE statement.

```
mysql> ALTER TABLESPACE mysql ENCRYPTION = 'N';
```

Enabling or disabling encryption for the mysql system tablespace requires the CREATE TABLESPACE privilege on all tables in the instance (CREATE TABLESPACE on \*.\*).

# <span id="page-182-0"></span>**Redo Log Encryption**

Redo log data encryption is enabled using the innodb\_redo\_log\_encrypt configuration option. Redo log encryption is disabled by default.

As with tablespace data, redo log data encryption occurs when redo log data is written to disk, and decryption occurs when redo log data is read from disk. Once redo log data is read into memory, it is in unencrypted form. Redo log data is encrypted and decrypted using the tablespace encryption key.

When innodb\_redo\_log\_encrypt is enabled, unencrypted redo log pages that are present on disk remain unencrypted, and new redo log pages are written to disk in encrypted form. Likewise, when innodb\_redo\_log\_encrypt is disabled, encrypted redo log pages that are present on disk remain encrypted, and new redo log pages are written to disk in unencrypted form.

From MySQL 8.0.30, redo log encryption metadata, including the tablespace encryption key, is stored in the header of the redo log file with the most recent checkpoint LSN. Before MySQL 8.0.30, redo log encryption metadata, including the tablespace encryption key, is stored in the header of the first

redo log file (ib\_logfile0). If the redo log file with the encryption metadata is removed, redo log encryption is disabled.

Once redo log encryption is enabled, a normal restart without the keyring component or plugin or without the encryption key is not possible, as InnoDB must be able to scan redo pages during startup, which is not possible if redo log pages are encrypted. Without the keyring component or plugin or the encryption key, only a forced startup without the redo logs (SRV\_FORCE\_NO\_LOG\_REDO) is possible. See Section 17.21.3, "Forcing InnoDB Recovery".

# <span id="page-183-0"></span>**Undo Log Encryption**

Undo log data encryption is enabled using the innodb\_undo\_log\_encrypt configuration option. Undo log encryption applies to undo logs that reside in undo tablespaces. See [Section 17.6.3.4, "Undo](#page-38-1) [Tablespaces"](#page-38-1). Undo log data encryption is disabled by default.

As with tablespace data, undo log data encryption occurs when undo log data is written to disk, and decryption occurs when undo log data is read from disk. Once undo log data is read into memory, it is in unencrypted form. Undo log data is encrypted and decrypted using the tablespace encryption key.

When innodb\_undo\_log\_encrypt is enabled, unencrypted undo log pages that are present on disk remain unencrypted, and new undo log pages are written to disk in encrypted form. Likewise, when innodb\_undo\_log\_encrypt is disabled, encrypted undo log pages that are present on disk remain encrypted, and new undo log pages are written to disk in unencrypted form.

Undo log encryption metadata, including the tablespace encryption key, is stored in the header of the undo log file.

![](_page_183_Picture_8.jpeg)

#### **Note**

When undo log encryption is disabled, the server continues to require the keyring component or plugin that was used to encrypt undo log data until the undo tablespaces that contained the encrypted undo log data are truncated. (An encryption header is only removed from an undo tablespace when the undo tablespace is truncated.) For information about truncating undo tablespaces, see [Truncating Undo Tablespaces](#page-42-0).

# <span id="page-183-1"></span>**Master Key Rotation**

The master encryption key should be rotated periodically and whenever you suspect that the key has been compromised.

Master key rotation is an atomic, instance-level operation. Each time the master encryption key is rotated, all tablespace keys in the MySQL instance are re-encrypted and saved back to their respective tablespace headers. As an atomic operation, re-encryption must succeed for all tablespace keys once a rotation operation is initiated. If master key rotation is interrupted by a server failure, InnoDB rolls the operation forward on server restart. For more information, see [Encryption and Recovery.](#page-184-0)

Rotating the master encryption key only changes the master encryption key and re-encrypts tablespace keys. It does not decrypt or re-encrypt associated tablespace data.

Rotating the master encryption key requires the ENCRYPTION\_KEY\_ADMIN privilege (or the deprecated SUPER privilege).

To rotate the master encryption key, run:

mysql> **ALTER INSTANCE ROTATE INNODB MASTER KEY;**

ALTER INSTANCE ROTATE INNODB MASTER KEY supports concurrent DML. However, it cannot be run concurrently with tablespace encryption operations, and locks are taken to prevent conflicts that could arise from concurrent execution. If an ALTER INSTANCE ROTATE INNODB MASTER KEY operation is running, it must finish before a tablespace encryption operation can proceed, and vice versa.

# <span id="page-184-0"></span>**Encryption and Recovery**

If a server failure occurs during an encryption operation, the operation is rolled forward when the server is restarted. For general tablespaces, the encryption operation is resumed in a background thread from the last processed page.

If a server failure occurs during master key rotation, InnoDB continues the operation on server restart.

The keyring component or plugin must be loaded prior to storage engine initialization so that the information necessary to decrypt tablespace data pages can be retrieved from tablespace headers before InnoDB initialization and recovery activities access tablespace data. (See [Encryption](#page-180-0) [Prerequisites](#page-180-0).)

When InnoDB initialization and recovery begin, the master key rotation operation resumes. Due to the server failure, some tablespace keys may already be encrypted using the new master encryption key. InnoDB reads the encryption data from each tablespace header, and if the data indicates that the tablespace key is encrypted using the old master encryption key, InnoDB retrieves the old key from the keyring and uses it to decrypt the tablespace key. InnoDB then re-encrypts the tablespace key using the new master encryption key and saves the re-encrypted tablespace key back to the tablespace header.

# <span id="page-184-1"></span>**Exporting Encrypted Tablespaces**

Tablespace export is only supported for file-per-table tablespaces.

When an encrypted tablespace is exported, InnoDB generates a transfer key that is used to encrypt the tablespace key. The encrypted tablespace key and transfer key are stored in a tablespace\_name.cfp file. This file together with the encrypted tablespace file is required to perform an import operation. On import, InnoDB uses the transfer key to decrypt the tablespace key in the tablespace\_name.cfp file. For related information, see [Section 17.6.1.3, "Importing InnoDB](#page-1-1) [Tables"](#page-1-1).

# <span id="page-184-2"></span>**Encryption and Replication**

- The ALTER INSTANCE ROTATE INNODB MASTER KEY statement is only supported in replication environments where the source and replica run a version of MySQL that supports tablespace encryption.
- Successful ALTER INSTANCE ROTATE INNODB MASTER KEY statements are written to the binary log for replication on replicas.
- If an ALTER INSTANCE ROTATE INNODB MASTER KEY statement fails, it is not logged to the binary log and is not replicated on replicas.
- Replication of an ALTER INSTANCE ROTATE INNODB MASTER KEY operation fails if the keyring component or plugin is installed on the source but not on the replica.
- If the keyring\_file or keyring\_encrypted\_file plugin is installed on both the source and a replica but the replica does not have a keyring data file, the replicated ALTER INSTANCE ROTATE INNODB MASTER KEY statement creates the keyring data file on the replica, assuming the keyring file data is not cached in memory. ALTER INSTANCE ROTATE INNODB MASTER KEY uses keyring file data that is cached in memory, if available.

# <span id="page-184-3"></span>**Identifying Encrypted Tablespaces and Schemas**

The Information Schema INNODB\_TABLESPACES table, introduced in MySQL 8.0.13, includes an ENCRYPTION column that can be used to identify encrypted tablespaces.

```
mysql> SELECT SPACE, NAME, SPACE_TYPE, ENCRYPTION FROM INFORMATION_SCHEMA.INNODB_TABLESPACES
 WHERE ENCRYPTION='Y'\G
*************************** 1. row ***************************
```

```
 SPACE: 4294967294
 NAME: mysql
SPACE_TYPE: General
ENCRYPTION: Y
*************************** 2. row ***************************
 SPACE: 2
 NAME: test/t1
SPACE_TYPE: Single
ENCRYPTION: Y
*************************** 3. row ***************************
 SPACE: 3
 NAME: ts1
SPACE_TYPE: General
ENCRYPTION: Y
```

When the ENCRYPTION option is specified in a CREATE TABLE or ALTER TABLE statement, it is recorded in the CREATE\_OPTIONS column of INFORMATION\_SCHEMA.TABLES. This column can be queried to identify tables that reside in encrypted file-per-table tablespaces.

```
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES
 WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';
+--------------+------------+----------------+
| TABLE_SCHEMA | TABLE_NAME | CREATE_OPTIONS |
+--------------+------------+----------------+
| test | t1 | ENCRYPTION="Y" |
+--------------+------------+----------------+
```

Query the Information Schema INNODB\_TABLESPACES table to retrieve information about the tablespace associated with a particular schema and table.

```
mysql> SELECT SPACE, NAME, SPACE_TYPE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE NAME='test/t1';
+-------+---------+------------+
| SPACE | NAME | SPACE_TYPE |
+-------+---------+------------+
| 3 | test/t1 | Single |
+-------+---------+------------+
```

You can identify encryption-enabled schemas by querying the Information Schema SCHEMATA table.

```
mysql> SELECT SCHEMA_NAME, DEFAULT_ENCRYPTION FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE DEFAULT_ENCRYPTION='YES';
+-------------+--------------------+
| SCHEMA_NAME | DEFAULT_ENCRYPTION |
+-------------+--------------------+
| test | YES |
+-------------+--------------------+
```

SHOW CREATE SCHEMA also shows the DEFAULT ENCRYPTION clause.

# <span id="page-185-0"></span>**Monitoring Encryption Progress**

You can monitor general tablespace and mysql system tablespace encryption progress using Performance Schema.

The stage/innodb/alter tablespace (encryption) stage event instrument reports WORK\_ESTIMATED and WORK\_COMPLETED information for general tablespace encryption operations.

The following example demonstrates how to enable the stage/innodb/alter tablespace (encryption) stage event instrument and related consumer tables to monitor general tablespace or mysql system tablespace encryption progress. For information about Performance Schema stage event instruments and related consumers, see Section 29.12.5, "Performance Schema Stage Event Tables".

1. Enable the stage/innodb/alter tablespace (encryption) instrument:

```
mysql> USE performance_schema;
mysql> UPDATE setup_instruments SET ENABLED = 'YES'
 WHERE NAME LIKE 'stage/innodb/alter tablespace (encryption)';
```

2. Enable the stage event consumer tables, which include events\_stages\_current, events\_stages\_history, and events\_stages\_history\_long.

```
mysql> UPDATE setup_consumers SET ENABLED = 'YES' WHERE NAME LIKE '%stages%';
```

3. Run a tablespace encryption operation. In this example, a general tablespace named ts1 is encrypted.

```
mysql> ALTER TABLESPACE ts1 ENCRYPTION = 'Y';
```

4. Check the progress of the encryption operation by querying the Performance Schema events\_stages\_current table. WORK\_ESTIMATED reports the total number of pages in the tablespace. WORK\_COMPLETED reports the number of pages processed.

```
mysql> SELECT EVENT_NAME, WORK_ESTIMATED, WORK_COMPLETED FROM events_stages_current;
+--------------------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+--------------------------------------------+----------------+----------------+
| stage/innodb/alter tablespace (encryption) | 1056 | 1407 |
+--------------------------------------------+----------------+----------------+
```

The events\_stages\_current table returns an empty set if the encryption operation has completed. In this case, you can check the events\_stages\_history table to view event data for the completed operation. For example:

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED FROM events_stages_history;
+--------------------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+--------------------------------------------+----------------+----------------+
| stage/innodb/alter tablespace (encryption) | 1407 | 1407 |
+--------------------------------------------+----------------+----------------+
```

# <span id="page-186-0"></span>**Encryption Usage Notes**

- Plan appropriately when altering an existing file-per-table tablespace with the ENCRYPTION option. Tables residing in file-per-table tablespaces are rebuilt using the COPY algorithm. The INPLACE algorithm is used when altering the ENCRYPTION attribute of a general tablespace or the mysql system tablespace. The INPLACE algorithm permits concurrent DML on tables that reside in the general tablespace. Concurrent DDL is blocked.
- When a general tablespace or the mysql system tablespace is encrypted, all tables residing in the tablespace are encrypted. Likewise, a table created in an encrypted tablespace is encrypted.
- If the server exits or is stopped during normal operation, it is recommended to restart the server using the same encryption settings that were configured previously.
- The first master encryption key is generated when the first new or existing tablespace is encrypted.
- Master key rotation re-encrypts tablespaces keys but does not change the tablespace key itself. To change a tablespace key, you must disable and re-enable encryption. For file-per-table tablespaces, re-encrypting the tablespace is an ALGORITHM=COPY operation that rebuilds the table. For general tablespaces and the mysql system tablespace, it is an ALGORITHM=INPLACE operation, which does not require rebuilding tables that reside in the tablespace.
- If a table is created with both the COMPRESSION and ENCRYPTION options, compression is performed before tablespace data is encrypted.
- If a keyring data file (the file named by keyring\_file\_data or keyring\_encrypted\_file\_data) is empty or missing, the first execution of ALTER INSTANCE ROTATE INNODB MASTER KEY creates a master encryption key.
- Uninstalling the component\_keyring\_file or component\_keyring\_encrypted\_file component does not remove an existing keyring data file. Uninstalling the keyring\_file or keyring\_encrypted\_file plugin does not remove an existing keyring data file.

- It is recommended that you not place a keyring data file under the same directory as tablespace data files.
- Modifying the keyring\_file\_data or keyring\_encrypted\_file\_data setting at runtime or when restarting the server can cause previously encrypted tablespaces to become inaccessible, resulting in lost data.
- Encryption is supported for the InnoDB FULLTEXT index tables that are created implicitly when adding a FULLTEXT index. For related information, see [InnoDB Full-Text Index Tables](#page-24-1).

# <span id="page-187-0"></span>**Encryption Limitations**

- Advanced Encryption Standard (AES) is the only supported encryption algorithm. InnoDB tablespace encryption uses Electronic Codebook (ECB) block encryption mode for tablespace key encryption and Cipher Block Chaining (CBC) block encryption mode for data encryption. Padding is not used with CBC block encryption mode. Instead, InnoDB ensures that the text to be encrypted is a multiple of the block size.
- Encryption is only supported for file-per-table tablespaces, general tablespaces, and the mysql system tablespace. Encryption support for general tablespaces was introduced in MySQL 8.0.13. Encryption support for the mysql system tablespace is available as of MySQL 8.0.16. Encryption is not supported for other tablespace types including the InnoDB system tablespace.
- You cannot move or copy a table from an encrypted file-per-table tablespace, general tablespace, or the mysql system tablespace to a tablespace type that does not support encryption.
- You cannot move or copy a table from an encrypted tablespace to an unencrypted tablespace. However, moving a table from an unencrypted tablespace to an encrypted one is permitted. For example, you can move or copy a table from a unencrypted file-per-table or general tablespace to an encrypted general tablespace.
- By default, tablespace encryption only applies to data in the tablespace. Redo log and undo log data can be encrypted by enabling innodb\_redo\_log\_encrypt and innodb\_undo\_log\_encrypt. See [Redo Log Encryption,](#page-182-0) and [Undo Log Encryption](#page-183-0). For information about binary log file and relay log file encryption, see Section 19.3.2, "Encrypting Binary Log Files and Relay Log Files".
- It is not permitted to change the storage engine of a table that resides in, or previously resided in, an encrypted tablespace.