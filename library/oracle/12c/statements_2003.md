# Oracle 12c - statements_2003
Source: https://docs.oracle.com/database/121/SQLRF/statements_2003.htm

Semantics

FORCE

If you specify `FORCE` and any items specified with the `ADD` clause have already been specified for the materialized view log, then Oracle Database does not return an error, but silently ignores the existing elements and adds to the materialized view log any items that do not already exist in the log. Likewise, if you specify `INCLUDING` `NEW` `VALUES` and that attribute has already been specified for the materialized view log, Oracle Database ignores the redundancy and does not return an error.

schema

Specify the schema containing the master table. If you omit `schema`, then Oracle Database assumes the materialized view log is in your own schema.

table

Specify the name of the master table associated with the materialized view log to be altered.

physical\_attributes\_clause

The `physical_attributes_clause` lets you change the value of the `PCTFREE`, `PCTUSED`, and `INITRANS` parameters and the storage characteristics for the materialized view log, the partition, the overflow data segment, or the default characteristics of a partitioned materialized view log.

Restriction on Materialized View Log Physical Attributes You cannot use the `storage_clause` to modify extent parameters if the materialized view log resides in a locally managed tablespace. Refer to [CREATE TABLE](statements_7002.md#i2095331) for a description of these parameters.

add\_mv\_log\_column\_clause

When you add a column to the master table of the materialized view log, the database does not automatically add a column to the materialized view log. Therefore, use this clause to add a column to the materialized view log. Oracle Database will encrypt the newly added column if the corresponding column of the master table is encrypted.

alter\_table\_partitioning

The syntax and general functioning of the partitioning clauses is the same as described for the `ALTER` `TABLE` statement. Refer to [alter\_table\_partitioning](statements_3001.md#i2085640) in the documentation on `ALTER` `TABLE`.

Restrictions on Altering Materialized View Log Partitions Altering materialized view log partitions is subject to the following restrictions:

* You cannot use the `LOB_storage_clause` or `modify_LOB_storage_clause` when modifying partitions of a materialized view log.
* If you attempt to drop, truncate, or exchange a materialized view log partition, then Oracle Database raises an error.

parallel\_clause

The `parallel_clause` lets you specify whether parallel operations will be supported for the materialized view log.

For complete information on this clause, refer to [parallel\_clause](statements_7002.md#i2159323) in the documentation on `CREATE` `TABLE`.

logging\_clause

Specify the logging attribute of the materialized view log. Refer to the [logging\_clause](clauses005.md#g1057902) for a full description of this clause.

allocate\_extent\_clause

Use the `allocate_extent_clause` to explicitly allocate a new extent for the materialized view log. Refer to [allocate\_extent\_clause](clauses001.md#g1053419) for a full description of this clause.

shrink\_clause

Use this clause to compact the materialized view log segments. For complete information on this clause, refer to [shrink\_clause](statements_3001.md#i2192484) in the documentation on `CREATE` `TABLE`.

move\_mv\_log\_clause

Use the `MOVE` clause to move the materialized view log table to a different tablespace, to change other segment or storage attributes of the materialized view log, or to change the parallelism of the materialized view log.

Restriction on Moving Materialized View Logs The `ENCRYPT` clause of the `storage_clause` of `segment_attributes` is not valid for materialized view logs.

CACHE | NOCACHE Clause

For data that will be accessed frequently, `CACHE` specifies that the blocks retrieved for this log are placed at the most recently used end of the LRU list in the buffer cache when a full table scan is performed. This attribute is useful for small lookup tables. `NOCACHE` specifies that the blocks are placed at the least recently used end of the LRU list. Refer to ["CACHE | NOCACHE | CACHE READS"](statements_7002.md#i2215507) in the documentation on `CREATE` `TABLE` for more information about this clause.

mv\_log\_augmentation

Use the `ADD` clause to augment the materialized view log so that it records the primary key values, rowid values, object ID values, or a sequence when rows in the materialized view master table are changed. This clause can also be used to record additional columns.

To stop recording any of this information, you must first drop the materialized view log and then re-create it. Dropping the materialized view log and then re-creating it forces a complete refresh for each of the existing materialized views that depend on the master table on its next refresh.

Restriction on Augmenting Materialized View Logs You can specify only one `PRIMARY` `KEY`, one `ROWID`, one `OBJECT` `ID`, one `SEQUENCE`, and each column in the column list once for each materialized view log. You can specify only a single occurrence of `PRIMARY` `KEY`, `ROWID`, `OBJECT` `ID`, `SEQUENCE`, and column list within this `ALTER` statement. Also, if any of these values was specified at create time (either implicitly or explicitly), you cannot specify that value in this `ALTER` statement unless you use the `FORCE` option.

OBJECT ID Specify `OBJECT` `ID` if you want the appropriate object identifier of all rows that are changed to be recorded in the materialized view log.

Restriction on the OBJECT ID clause You can specify `OBJECT` `ID` only for logs on object tables, and you cannot specify it for storage tables.

PRIMARY KEY Specify `PRIMARY` `KEY` if you want the primary key values of all rows that are changed to be recorded in the materialized view log.

ROWID Specify `ROWID` if you want the rowid values of all rows that are changed to be recorded in the materialized view log.

SEQUENCE Specify `SEQUENCE` to indicate that a sequence value providing additional ordering information should be recorded in the materialized view log.

column Specify the additional columns whose values you want to be recorded in the materialized view log for all rows that are changed. Typically these columns are filter columns (non-primary-key columns referenced by subquery materialized views) and join columns (non-primary-key columns that define a join in the `WHERE` clause of the subquery).

NEW VALUES Clause

The `NEW` `VALUES` clause lets you specify whether Oracle Database saves both old and new values for update DML operations in the materialized view log. The value you set in this clause applies to all columns in the log, not only to columns you may have added in this `ALTER` `MATERIALIZED` `VIEW` `LOG` statement.

INCLUDING Specify `INCLUDING` to save both new and old values in the log. If this log is for a table on which you have a single-table materialized aggregate view, and if you want the materialized view to be eligible for fast refresh, then you must specify `INCLUDING`.

EXCLUDING Specify `EXCLUDING` to disable the recording of new values in the log. You can use this clause to avoid the overhead of recording new values.

If you have a fast-refreshable single-table materialized aggregate view defined on this table, then do not specify `EXCLUDING` `NEW` `VALUES` unless you first change the refresh mode of the materialized view to something other than `FAST`.

mv\_log\_purge\_clause

Use this clause alter the purge attributes of the materialized view log in the following ways:

* Change the purge from `IMMEDIATE` `SYNCHRONOUS` to `IMMEDIATE` `ASYNCHRONOUS` or from `IMMEDIATE` `ASYNCHRONOUS` to `IMMEDIATE` `SYNCHRONOUS`
* Change the purge from `IMMEDIATE` to scheduled or from scheduled to `IMMEDIATE`
* Specify a new start time and a new `next` time and `interval`

If you are altering purge from scheduled to `IMMEDIATE`, then the scheduled purged job associated with that materialized view log is dropped. If you are altering purge from `IMMEDIATE` to scheduled, then a purge job is created with the attributes provided. If you are altering scheduled purge attributes, then only those attributes specified will be changed in the scheduler purge job.

You must specify `FORCE` if you are altering log purge to its current state (that is, you are not making any change), unless you are changing scheduled purge attributes.

To learn whether the purge time or interval has already been set for this materialized view log, query the `*_MVIEW_LOGS` data dictionary views. See the `CREATE` `MATERIALIZED` `VIEW` `LOG` clause [mv\_log\_purge\_clause](statements_6003.md#CACCJBFD) for the full semantics of this clause.

for\_refresh\_clause

Use this clause to change the refresh method for which the materialized view log will be used.

FOR SYNCHRONOUS REFRESH Specify this clause to change from fast refresh to synchronous refresh, or complete refresh to synchronous refresh. A staging log will be created.

If you are changing from fast refresh, then ensure that the following conditions are satisfied before using this clause:

* All changes in the materialized view log have been consumed.
* Any refresh-on-demand materialized views associated with the master table have been refreshed.
* Any refresh-on-commit materialized views associated with the master table have been converted to refresh-on-demand materialized views.

After you use this clause, you cannot perform DML operations directly on the master table. You must use the procedures in the `DBMS_SYNC_REFRESH` package to prepare and execute change data operations.

FOR FAST REFRESH Specify this clause to change from synchronous refresh to fast refresh, or complete refresh to fast refresh. A materialized view log will be created.

If you are changing from synchronous refresh to fast refresh, then ensure that all changes in the staging log have been consumed before using this clause.

After you use this clause, you can perform DML operations directly on the master table.

See the `CREATE` `MATERIALIZED` `VIEW` `LOG` clause [for\_refresh\_clause](statements_6003.md#CCHIHIEB) for the full semantics of this clause.