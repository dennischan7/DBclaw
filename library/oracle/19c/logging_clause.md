# Oracle 19c - logging_clause
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/logging_clause.html

Purpose

The `logging_clause` lets you specify whether certain DML operations will be logged in the redo log file (`LOGGING`) or not (`NOLOGGING`).

You can specify the `logging_clause` in the following statements:

* `CREATE` `TABLE` and `ALTER` `TABLE`: for logging of the table, a table partition, a LOB segment, or the overflow segment of an index-organized table (see [CREATE TABLE](CREATE-TABLE.md#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6) and [ALTER TABLE](ALTER-TABLE.md#GUID-552E7373-BF93-477D-9DA3-B2C9386F2877)).

  Note:

  Logging specified for a LOB column can differ from logging set at the table level. If you specify `LOGGING` at the table level and `NOLOGGING` for a LOB column, then DML changes to the base table row are logged, but DML changes to the LOB data are not logged.
* `CREATE` `INDEX` and `ALTER` `INDEX`: for logging of the index or an index partition (see [CREATE INDEX](CREATE-INDEX.md#GUID-1F89BBC0-825F-4215-AF71-7588E31D8BFE) and [ALTER INDEX](ALTER-INDEX.md#GUID-D8F648E7-8C07-4C89-BB71-862512536558)).
* `CREATE` `MATERIALIZED` `VIEW` and `ALTER` `MATERIALIZED` `VIEW`: for logging of the materialized view, one of its partitions, or a LOB segment (see [CREATE MATERIALIZED VIEW](CREATE-MATERIALIZED-VIEW.md#GUID-EE262CA4-01E5-4618-B659-6165D993CA1B) and [ALTER MATERIALIZED VIEW](ALTER-MATERIALIZED-VIEW.md#GUID-29EE5682-AE42-4879-ABAD-E34E66ADD233)).
* `CREATE` `MATERIALIZED` `VIEW` `LOG` and `ALTER` `MATERIALIZED` `VIEW` `LOG`: for logging of the materialized view log or one of its partitions (see [CREATE MATERIALIZED VIEW LOG](CREATE-MATERIALIZED-VIEW-LOG.md#GUID-13902019-D044-4B79-9EB4-1F60652D037B) and [ALTER MATERIALIZED VIEW LOG](ALTER-MATERIALIZED-VIEW-LOG.md#GUID-4DAD5E6F-E30A-43D0-B023-634752E0E627)).
* `CREATE` `TABLESPACE` and `ALTER` `TABLESPACE`: to set or modify the default logging characteristics for all objects created in the tablespace (see [CREATE TABLESPACE](CREATE-TABLESPACE.md#GUID-51F07BF5-EFAF-4910-9040-C473B86A8BF9) and [ALTER TABLESPACE](ALTER-TABLESPACE.md#GUID-CA074861-55D3-4768-8995-43D4DA26365D)).
* `CREATE` `PLUGGABLE` `DATABASE` and `ALTER` `PLUGGABLE` `DATABASE`: to set or modify the default logging characteristics for all tablespaces created in the pluggable database (PDB) (see [CREATE PLUGGABLE DATABASE](CREATE-PLUGGABLE-DATABASE.md#GUID-F2DBA8DD-EEA8-4BB7-A07F-78DC04DB1FFC) and [ALTER PLUGGABLE DATABASE](ALTER-PLUGGABLE-DATABASE.md#GUID-A29491AD-8F0F-4E52-9D94-57FC3FF8FBC7)).

You can also specify `LOGGING` or `NOLOGGING` for the following operations:

Semantics

This section describes the semantics of the `logging_clause`. For additional information, refer to the SQL statement in which you set or reset logging characteristics for a particular database object.

* If you specify `LOGGING`, then the creation of a database object, as well as subsequent inserts into the object, will be logged in the redo log file.
* If you specify `NOLOGGING`, then the creation of a database object, as well as subsequent conventional inserts, will be logged in the redo log file. Direct-path inserts will not be logged.

  + For a nonpartitioned object, the value specified for this clause is the actual physical attribute of the segment associated with the object.
  + For partitioned objects, the value specified for this clause is the default physical attribute of the segments associated with all partitions specified in the `CREATE` statement (and in subsequent `ALTER` ... `ADD` `PARTITION` statements), unless you specify the logging attribute in the `PARTITION` description.
  + For SecureFiles LOBs, the `NOLOGGING` setting is converted internally to `FILESYSTEM_LIKE_LOGGING`.
  + `CACHE` `NOLOGGING` is not allowed for BasicFiles LOBs.
* The `FILESYSTEM_LIKE_LOGGING` clause is valid only for logging of SecureFiles LOB segments. You cannot specify this setting for BasicFiles LOBs. Specify this setting if you want to log only metadata changes. This setting is similar to the metadata journaling of file systems, which reduces mean time to recovery from failures. The `LOGGING` setting, for SecureFiles LOBs, is similar to the data journaling of file systems. Both the `LOGGING` and `FILESYSTEM_LIKE_LOGGING` settings provide a complete transactional file system by way of SecureFiles.

Note:

For LOB segments, with the `NOLOGGING` and `FILESYSTEM_LIKE_LOGGING` settings it is possible for data to be changed on disk during a backup operation, resulting in an inconsistent backup. To avoid this situation, ensure that changes to LOB segments are saved in the redo log file by setting `LOGGING` for LOB storage. Alternatively, change the database to `FORCE` `LOGGING` mode so that changes to all LOB segments are saved in the redo.

If the object for which you are specifying the logging attributes resides in a database or tablespace in force logging mode, then Oracle Database ignores any `NOLOGGING` setting until the database or tablespace is taken out of force logging mode.

If the database is running in `ARCHIVELOG` mode, then media recovery from a backup made before the `LOGGING` operation re-creates the object. However, media recovery from a backup made before the `NOLOGGING` operation does not re-create the object.

The size of a redo log generated for an operation in `NOLOGGING` mode is significantly smaller than the log generated in `LOGGING` mode.

In `NOLOGGING` mode, data is modified with minimal logging (to mark new extents `INVALID` and to record dictionary changes). When applied during media recovery, the extent invalidation records mark a range of blocks as logically corrupt, because the redo data is not fully logged. Therefore, if you cannot afford to lose the database object, then you should take a backup after the `NOLOGGING` operation.

`NOLOGGING` is supported in only a subset of the locations that support `LOGGING`. Only the following operations support the `NOLOGGING` mode:

DML:

* Direct-path `INSERT` (serial or parallel) resulting either from an `INSERT` or a `MERGE` statement. `NOLOGGING` is not applicable to any `UPDATE` operations resulting from the `MERGE` statement.
* Direct Loader (SQL\*Loader)

DDL:

* `CREATE` `TABLE` ... `AS` `SELECT` (In `NOLOGGING` mode, the creation of the table will be logged, but direct-path inserts will not be logged.)
* `CREATE` `TABLE` ... `LOB_storage_clause` ... `LOB_parameters` ... `CACHE` | `NOCACHE` | `CACHE` `READS`
* `ALTER` `TABLE` ... `LOB_storage_clause` ... `LOB_parameters` ... `CACHE` | `NOCACHE` | `CACHE` `READS` (to specify logging of newly created LOB columns)
* `ALTER` `TABLE` ... `modify_LOB_storage_clause` ... `modify_LOB_parameters` ... `CACHE` | `NOCACHE` | `CACHE` `READS` (to change logging of existing LOB columns)
* `ALTER` `TABLE` ... `MOVE`
* `ALTER` `TABLE` ... (all partition operations that involve data movement)

  + `ALTER` `TABLE` ... `ADD` `PARTITION` (hash partition only)
  + `ALTER` `TABLE` ... `MERGE` `PARTITIONS`
  + `ALTER` `TABLE` ... `SPLIT` `PARTITION`
  + `ALTER` `TABLE` ... `MOVE` `PARTITION`
  + `ALTER` `TABLE` ... `MODIFY` `PARTITION` ... `ADD SUBPARTITION`
  + `ALTER` `TABLE` ... `MODIFY` `PARTITION` ... `COALESCE` `SUBPARTITION`
* `CREATE` `INDEX`
* `ALTER` `INDEX` ... `REBUILD`
* `ALTER` `INDEX` ... `REBUILD` `[SUB]PARTITION`
* `ALTER` `INDEX` ... `SPLIT` `PARTITION`

For objects other than LOBs, if you omit this clause, then the logging attribute of the object defaults to the logging attribute of the tablespace in which it resides.

For LOBs, if you omit this clause, then:

* If you specify `CACHE`, then `LOGGING` is used (because you cannot have `CACHE` `NOLOGGING`).
* If you specify `NOCACHE` or `CACHE` `READS`, then the logging attribute defaults to the logging attribute of the tablespace in which it resides.

`NOLOGGING` does not apply to LOBs that are stored internally (in the table with row data). If you specify `NOLOGGING` for LOBs with values less than 4000 bytes and you have not disabled `STORAGE` `IN` `ROW`, then Oracle ignores the `NOLOGGING` specification and treats the LOB data the same as other table data.