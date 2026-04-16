# Oracle 11g - statements_1010
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_1010.htm

Semantics

schema

Specify the schema containing the index. If you omit `schema`, then Oracle Database assumes the index is in your own schema.

index

Specify the name of the index to be altered.

Restrictions on Modifying Indexes The modification of indexes is subject to the following restrictions:

* If `index` is a domain index, then you can specify only the `PARAMETERS` clause, the `RENAME` clause, the `rebuild_clause` (with or without the `PARAMETERS` clause), the `parallel_clause`, or the `UNUSABLE` clause. No other clauses are valid.
* You cannot alter or rename a domain index that is marked `LOADING` or `FAILED`. If an index is marked `FAILED`, then the only clause you can specify is `REBUILD`.

deallocate\_unused\_clause

Use the `deallocate_unused_clause` to explicitly deallocate unused space at the end of the index and make the freed space available for other segments in the tablespace.

If `index` is range-partitioned or hash-partitioned, then Oracle Database deallocates unused space from each index partition. If `index` is a local index on a composite-partitioned table, then Oracle Database deallocates unused space from each index subpartition.

Restrictions on Deallocating Space Deallocation of space is subject to the following restrictions:

Refer to [deallocate\_unused\_clause](clauses003.md#g1056929) for a full description of this clause.

KEEP integer The `KEEP` clause lets you specify the number of bytes above the high water mark that the index will have after deallocation. If the number of remaining extents is less than `MINEXTENTS`, then `MINEXTENTS` is set to the current number of extents. If the initial extent becomes smaller than `INITIAL`, then `INITIAL` is set to the value of the current initial extent. If you omit `KEEP`, then all unused space is freed.

Refer to [ALTER TABLE](statements_3001.md#CJAHHIBI) for a complete description of this clause.

allocate\_extent\_clause

The `allocate_extent_clause` lets you explicitly allocate a new extent for the index. For a local index on a hash-partitioned table, Oracle Database allocates a new extent for each partition of the index.

Restriction on Allocating Extents You cannot specify this clause for an index on a temporary table or for a range-partitioned or composite-partitioned index.

Refer to [allocate\_extent\_clause](clauses001.md#g1053419) for a full description of this clause.

shrink\_clause

Use this clause to compact the index segments. Specifying `ALTER` `INDEX` ... `SHRINK` `SPACE` `COMPACT` is equivalent to specifying `ALTER` `INDEX` ... `COALESCE`.

For complete information on this clause, refer to [shrink\_clause](statements_3001.md#i2192484) in the documentation on `CREATE` `TABLE`.

Restriction on Shrinking Index Segments You cannot specify this clause for for a bitmap join index or for a function-based index.

parallel\_clause

Use the `PARALLEL` clause to change the default degree of parallelism for queries and DML on the index.

Restriction on Parallelizing Indexes You cannot specify this clause for an index on a temporary table.

For complete information on this clause, refer to [parallel\_clause](statements_7002.md#i2159323) in the documentation on `CREATE` `TABLE`.

physical\_attributes\_clause

Use the `physical_attributes_clause` to change the values of parameters for a nonpartitioned index, all partitions and subpartitions of a partitioned index, a specified partition, or all subpartitions of a specified partition.

Restrictions on Index Physical Attributes Index physical attributes are subject to the following restrictions:

* You cannot specify this clause for an index on a temporary table.
* You cannot specify the `PCTUSED` parameter at all when altering an index.
* You can specify the `PCTFREE` parameter only as part of the `rebuild_clause`, the `modify_index_default_attrs` clause, or the `split_index_partition` clause.

storage\_clause

Use the `storage_clause` to change the storage parameters for a nonpartitioned index, index partition, or all partitions of a partitioned index, or default values of these parameters for a partitioned index. Refer to [storage\_clause](clauses007.md#i1026834) for complete information on this clause.

logging\_clause

Use the `logging_clause` to change the logging attribute of the index. If you also specify the `REBUILD` clause, then this new setting affects the rebuild operation. If you specify a different value for logging in the `REBUILD` clause, then Oracle Database uses the last logging value specified as the logging attribute of the index and of the rebuild operation.

An index segment can have logging attributes different from those of the base table and different from those of other index segments for the same base table.

Restriction on Index Logging You cannot specify this clause for an index on a temporary table.

RECOVERABLE | UNRECOVERABLE

These keywords are deprecated and have been replaced with `LOGGING` and `NOLOGGING`, respectively. Although `RECOVERABLE` and `UNRECOVERABLE` are supported for backward compatibility, Oracle strongly recommends that you use the `LOGGING` and `NOLOGGING` keywords.

`RECOVERABLE` is not a valid keyword for creating partitioned tables or LOB storage characteristics. `UNRECOVERABLE` is not a valid keyword for creating partitioned or index-organized tables. Also, it can be specified only with the `AS` subquery clause of `CREATE` `INDEX`.

rebuild\_clause

Use the `rebuild_clause` to re-create an existing index or one of its partitions or subpartitions. If index is marked `UNUSABLE`, then a successful rebuild will mark it `USABLE`. For a function-based index, this clause also enables the index. If the function on which the index is based does not exist, then the rebuild statement will fail.

Note:

When you rebuild the secondary index of an index-organized table, Oracle Database preserves the primary key columns contained in the logical rowid when the index was created. Therefore, if the index was created with the

`COMPATIBLE`

initialization parameter set to less than 10.0.0, the rebuilt index will contain the index key and any of the primary key columns of the table that are not also in the index key. If the index was created with the

`COMPATIBLE`

initialization parameter set to 10.0.0 or greater, then the rebuilt index will contain the index key and all the primary key columns of the table, including those also in the index key.

Restrictions on Rebuilding Indexes The rebuilding of indexes is subject to the following restrictions:

* You cannot rebuild an index on a temporary table.
* You cannot rebuild a bitmap index that is marked `INVALID`. Instead, you must drop and then re-create it.
* You cannot rebuild an entire partitioned index. You must rebuild each partition or subpartition, as described for the `PARTITION` clause.
* You cannot specify the `deallocate_unused_clause` in the same statement as the `rebuild_clause`.
* You cannot change the value of the `PCTFREE` parameter for the index as a whole (`ALTER` `INDEX`) or for a partition (`ALTER` `INDEX` ... `MODIFY` `PARTITION`). You can specify `PCTFREE` in all other forms of the `ALTER` `INDEX` statement.
* For a domain index:

  + You can specify only the `PARAMETERS` clause (either for the index or for a partition of the index) or the `parallel_clause`. No other rebuild clauses are valid.
  + You can rebuild an index only if the index is not marked `IN_PROGRESS`.
  + You can rebuild an index partition only if the index is not marked `IN_PROGRESS` or `FAILED` and the partition is not marked `IN_PROGRESS`.
* You cannot rebuild a local index, but you can rebuild a partition of a local index (`ALTER` `INDEX` ... `REBUILD` `PARTITION`).
* For a local index on a hash partition or subpartition, the only parameter you can specify is `TABLESPACE`.
* You cannot rebuild an online index that is used to enforce a deferrable unique constraint.

PARTITION Clause

Use the `PARTITION` clause to rebuild one partition of an index. You can also use this clause to move an index partition to another tablespace or to change a create-time physical attribute.

The storage of partitioned database entities in tablespaces of different block sizes is subject to several restrictions. Refer to [Oracle Database VLDB and Partitioning Guide](../../server.112/e25523/part_admin001.md#VLDBG00306) for a discussion of these restrictions.

Restriction on Rebuilding Partitions You cannot specify this clause for a local index on a composite-partitioned table. Instead, use the `REBUILD` `SUBPARTITION` clause.

SUBPARTITION Clause

Use the `SUBPARTITION` clause to rebuild one subpartition of an index. You can also use this clause to move an index subpartition to another tablespace. If you do not specify `TABLESPACE`, then the subpartition is rebuilt in the same tablespace.

The storage of partitioned database entities in tablespaces of different block sizes is subject to several restrictions. Refer to [Oracle Database VLDB and Partitioning Guide](../../server.112/e25523/part_admin001.md#VLDBG00306) for a discussion of these restrictions.

Restriction on Modifying Index Subpartitions The only parameters you can specify for a subpartition are `TABLESPACE`, `ONLINE`, and the `parallel_clause`.

REVERSE | NOREVERSE

Indicate whether the bytes of the index block are stored in reverse order:

* `REVERSE` stores the bytes of the index block in reverse order and excludes the rowid when the index is rebuilt.
* `NOREVERSE` stores the bytes of the index block without reversing the order when the index is rebuilt. Rebuilding a `REVERSE` index without the `NOREVERSE` keyword produces a rebuilt, reverse-keyed index.

Restrictions on Reverse Indexes Reverse indexes are subject to the following restrictions:

parallel\_clause

Use the `parallel_clause` to parallelize the rebuilding of the index and to change the degree of parallelism for the index itself. All subsequent operations on the index will be executed with the degree of parallelism specified by this clause, unless overridden by a subsequent data definition language (DDL) statement with the `parallel_clause`. The following exceptions apply:

* If `ALTER` `SESSION` `DISABLE` `PARALLEL` `DDL` was specified before rebuilding the index, then the index will be rebuilt serially and the degree of parallelism for the index will be changed to 1.
* If `ALTER` `SESSION` `FORCE` `PARALLEL` `DDL` was specified before rebuilding the index, then the index will be rebuilt in parallel and the degree of parallelism for the index will be changed to the value that was specified in the `ALTER` `SESSION` statement, or `DEFAULT` if no value was specified.

TABLESPACE Clause

Specify the tablespace where the rebuilt index, index partition, or index subpartition will be stored. The default is the default tablespace where the index or partition resided before you rebuilt it.

key\_compression

Specify `COMPRESS` to enable key compression, which eliminates repeated occurrence of key column values. Use `integer` to specify the prefix length (number of prefix columns to compress).

* For unique indexes, the range of valid prefix length values is from 1 to the number of key columns minus 1. The default prefix length is the number of key columns minus 1.
* For nonunique indexes, the range of valid prefix length values is from 1 to the number of key columns. The default prefix length is number of key columns.

Oracle Database compresses indexes that are nonunique or unique indexes of at least two columns. If you want to use compression for a partitioned index, then the index must have compression enabled at the index level.

Specify `NOCOMPRESS` to disable key compression. This is the default.

Restriction on Key Compression You cannot specify `COMPRESS` for a bitmap index.

ONLINE Clause

Specify `ONLINE` to allow DML operations on the table or partition during rebuilding of the index.

Restrictions on Online Indexes Online indexes are subject to the following restrictions:

* Parallel DML is not supported during online index building. If you specify `ONLINE` and subsequently issue parallel DML statements, then Oracle Database returns an error.
* You cannot specify `ONLINE` for a bitmap join index or a cluster index.
* For a nonunique secondary index on an index-organized table, the number of index key columns plus the number of primary key columns that are included in the logical rowid in the index-organized table cannot exceed 32. The logical rowid excludes columns that are part of the index key.

logging\_clause

Specify whether the `ALTER` `INDEX` ... `REBUILD` operation will be logged.

Refer to the [logging\_clause](clauses005.md#i999782) for a full description of this clause.

PARAMETERS Clause

This clause is valid only for domain indexes in a top-level `ALTER` `INDEX` statement and in the `rebuild_clause`. This clause specifies the parameter string that is passed uninterpreted to the appropriate ODCI indextype routine.

The maximum length of the parameter string is 1000 characters.

If you are altering or rebuilding an entire index, then the string must refer to index-level parameters. If you are rebuilding a partition of the index, then the string must refer to partition-level parameters.

If `index` is marked `UNUSABLE`, then modifying the parameters alone does not make it `USABLE`. You must also rebuild the `UNUSABLE` index to make it usable.

If you have installed Oracle Text, then you can rebuild your Oracle Text domain indexes using parameters specific to that product. For more information on those parameters, refer to [Oracle Text Reference](../../text.112/e24436/csql.md#CCREF0101).

Restriction on the PARAMETERS Clause You can modify index partitions only if `index` is not marked `IN_PROGRESS` or `FAILED`, no index partitions are marked `IN_PROGRESS`, and the partition being modified is not marked `FAILED`.

XMLIndex\_parameters\_clause

This clause is valid only for XMLIndex indexes. This clause specifies the parameter string that defines the XMLIndex implementation.

The maximum length of the parameter string is 1000 characters.

If you are altering or rebuilding an entire index, then the string must refer to index-level parameters. If you are rebuilding a partition of the index, then the string must refer to partition-level parameters.

If `index` is marked `UNUSABLE`, then modifying the parameters alone does not make it `USABLE`. You must also rebuild the `UNUSABLE` index to make it usable.

Restriction on the XMLIndex\_paramaters\_clause You can modify index partitions only if `index` is not marked `IN_PROGRESS` or `FAILED`, no index partitions are marked `IN_PROGRESS`, and the partition being modified is not marked `FAILED`.

COMPILE Clause

This clause is valid only for domain indexes. Use this clause to recompile an invalid domain index explicitly. This clause is useful primarily when the underlying indextype has been altered to support system-managed domain indexes, so that the existing domain index has been marked `INVALID`. In this situation, this `ALTER` `INDEX` statement migrates the domain index from a user-managed domain index to a system-managed domain index.

ENABLE Clause

`ENABLE` applies only to a function-based index that has been disabled, either by an `ALTER` `INDEX` ... `DISABLE` statement, or because a user-defined function used by the index was dropped or replaced. This clause enables such an index if these conditions are true:

* The function is currently valid.
* The signature of the current function matches the signature of the function when the index was created.
* The function is currently marked as `DETERMINISTIC`.

Restrictions on Enabling Function-based Indexes The `ENABLE` clause is subject to the following restrictions:

* You cannot specify any other clauses of `ALTER` `INDEX` in the same statement with `ENABLE`.
* You cannot specify this clause for an index on a temporary table. Instead, you must drop and recreate the index. You can retrieve the creation DDL for the index using the `DBMS_METADATA` package.

DISABLE Clause

`DISABLE` applies only to a function-based index. This clause lets you disable the use of a function-based index. You might want to do so, for example, while working on the body of the function. Afterward you can either rebuild the index or specify another `ALTER` `INDEX` statement with the `ENABLE` keyword.

UNUSABLE

Specify `UNUSABLE` to mark the index or index partition(s) or index subpartition(s) `UNUSABLE`. The space allocated for an index or index partition or subpartition is freed immediately when the object is marked `UNUSABLE`. An unusable index must be rebuilt, or dropped and re-created, before it can be used. While one partition is marked `UNUSABLE`, the other partitions of the index are still valid. You can execute statements that require the index if the statements do not access the unusable partition. You can also split or rename the unusable partition before rebuilding it. Refer to `CREATE` `INDEX` ... [UNUSABLE](statements_5012.md#BABCHJDH) for more information.

Restriction on Marking Indexes Unusable You cannot specify this clause for an index on a temporary table.

VISIBLE | INVISIBLE

Use this clause to specify whether the index is visible or invisible to the optimizer. Refer to ["VISIBLE | INVISIBLE"](statements_5012.md#BABBCCAA) in `CREATE` `INDEX` for a full description of this clause.

RENAME Clause

Use this clause to rename an index. The `new_index_name` is a single identifier and does not include the schema name.

Restriction on Renaming Indexes For a domain index, neither `index` nor any partitions of `index` can be marked `IN_PROGRESS` or `FAILED`.

COALESCE Clause

Specify `COALESCE` to instruct Oracle Database to merge the contents of index blocks where possible to free blocks for reuse.

Restrictions on Coalescing Index Blocks Coalescing of index blocks is subject to the following restrictions:

MONITORING USAGE | NOMONITORING USAGE

Use this clause to determine whether Oracle Database should monitor index use.

* Specify `MONITORING` `USAGE` to begin monitoring the index. Oracle Database first clears existing information on index use, and then monitors the index for use until a subsequent `ALTER` `INDEX` ... `NOMONITORING` `USAGE` statement is executed.
* To terminate monitoring of the index, specify `NOMONITORING` `USAGE`.

To see whether the index has been used since this `ALTER` `INDEX` ... `NOMONITORING` `USAGE` statement was issued, query the `USED` column of the `V$OBJECT_USAGE` dynamic performance view.

UPDATE BLOCK REFERENCES Clause

The `UPDATE` `BLOCK` `REFERENCES` clause is valid only for normal and domain indexes on index-organized tables. Specify this clause to update all the stale guess data block addresses stored as part of the index row with the correct database address for the corresponding block identified by the primary key.

For a domain index, Oracle Database executes the `ODCIIndexAlter` routine with the `alter_option` parameter set to `AlterIndexUpdBlockRefs`. This routine enables the cartridge code to update the stale guess data block addresses in the index.

Restriction on UPDATE BLOCK REFERENCES You cannot combine this clause with any other clause of `ALTER` `INDEX`.

alter\_index\_partitioning

The partitioning clauses of the `ALTER` `INDEX` statement are valid only for partitioned indexes.

The storage of partitioned database entities in tablespaces of different block sizes is subject to several restrictions. Refer to [Oracle Database VLDB and Partitioning Guide](../../server.112/e25523/part_admin001.md#VLDBG00306) for a discussion of these restrictions.

Restrictions on Modifying Index Partitions Modifying index partitions is subject to the following restrictions:

* You cannot specify any of these clauses for an index on a temporary table.
* You can combine several operations on the base index into one `ALTER` `INDEX` statement (except `RENAME` and `REBUILD`), but you cannot combine partition operations with other partition operations or with operations on the base index.

modify\_index\_default\_attrs

Specify new values for the default attributes of a partitioned index.

Restriction on Modifying Partition Default Attributes The only attribute you can specify for a hash-partitioned global index or for an index on a hash-partitioned table is `TABLESPACE`.

TABLESPACE Specify the default tablespace for new partitions of an index or subpartitions of an index partition.

logging\_clause Specify the default logging attribute of a partitioned index or an index partition.

Refer to [logging\_clause](clauses005.md#i999782) for a full description of this clause.

FOR PARTITION Use the `FOR` `PARTITION` clause to specify the default attributes for the subpartitions of a partition of a local index on a composite-partitioned table.

Restriction on FOR PARTITION You cannot specify `FOR` `PARTITION` for a list partition.

add\_hash\_index\_partition

Use this clause to add a partition to a global hash-partitioned index. Oracle Database adds hash partitions and populates them with index entries rehashed from an existing hash partition of the index, as determined by the hash function. If you omit the partition name, then Oracle Database assigns a name of the form `SYS_P``n`. If you omit the `TABLESPACE` clause, then Oracle Database places the partition in the tablespace specified for the index. If no tablespace is specified for the index, then Oracle Database places the partition in the default tablespace of the user, if one has been specified, or in the system default tablespace.

modify\_index\_partition

Use the `modify_index_partition` clause to modify the real physical attributes, logging attribute, or storage characteristics of index partition `partition` or its subpartitions. For a hash-partitioned global index, the only subclause of this clause you can specify is `UNUSABLE`.

COALESCE Specify this clause to merge the contents of index partition blocks where possible to free blocks for reuse.

UPDATE BLOCK REFERENCES The `UPDATE` `BLOCK` `REFERENCES` clause is valid only for normal indexes on index-organized tables. Use this clause to update all stale guess data block addresses stored in the secondary index partition.

Restrictions on UPDATE BLOCK REFERENCES This clause is subject to the following restrictions:

Note:

If the index is a local index on a composite-partitioned table, then the changes you specify here will override any attributes specified earlier for the subpartitions of index, as well as establish default values of attributes for future subpartitions of that partition. To change the default attributes of the partition without overriding the attributes of subpartitions, use

`ALTER` `TABLE`

...

`MODIFY` `DEFAULT` `ATTRIBUTES` `FOR` `PARTITION`

.

UNUSABLE Clause This clause has the same function for index partitions that it has for the index as a whole. Refer to ["UNUSABLE"](#i2160588).

key\_compression This clause is relevant for composite-partitioned indexes. Use this clause to change the compression attribute for the partition and every subpartition in that partition. Oracle Database marks each index subpartition in the partition `UNUSABLE` and you must then rebuild these subpartitions. Key compression must already have been specified for the table before you can specify key compression for a partition. You can specify this clause only at the partition level. You cannot change the compression attribute for an individual subpartition.

You can use this clause for noncomposite index partitions. However, it is more efficient to use the `rebuild_clause` for noncomposite partitions, which lets you rebuild and set the compression attribute in one step.

rename\_index\_partition

Use the `rename_index_partition` clauses to rename index `partition` or `subpartition` to `new_name`.

Restrictions on Renaming Index Partitions Renaming index partitions is subject to the following restrictions:

* You cannot rename the subpartition of a list partition.
* For a partition of a domain index, `index` cannot be marked `IN_PROGRESS` or `FAILED`, none of the partitions can be marked `IN_PROGRESS`, and the partition you are renaming cannot be marked `FAILED`.

drop\_index\_partition

Use the `drop_index_partition` clause to remove a partition and the data in it from a partitioned global index. When you drop a partition of a global index, Oracle Database marks the next index partition `UNUSABLE`. You cannot drop the highest partition of a global index.

split\_index\_partition

Use the `split_index_partition` clause to split a partition of a global range-partitioned index into two partitions, adding a new partition to the index. This clause is not valid for hash-partitioned global indexes. Instead, use the `add_hash_index_partition` clause.

Splitting a partition marked `UNUSABLE` results in two partitions, both marked `UNUSABLE`. You must rebuild the partitions before you can use them.

Splitting a usable partition results in two partitions populated with index data. Both new partitions are usable.

AT Clause Specify the new noninclusive upper bound for `split_partition_1`. The `value_list` must evaluate to less than the presplit partition bound for `partition_name_old` and greater than the partition bound for the next lowest partition (if there is one).

INTO Clause Specify (optionally) the name and physical attributes of each of the two partitions resulting from the split.

coalesce\_index\_partition

This clause is valid only for hash-partitioned global indexes. Oracle Database reduces by one the number of index partitions. Oracle Database selects the partition to coalesce based on the requirements of the hash function. Use this clause if you want to distribute index entries of a selected partition into one of the remaining partitions and then remove the selected partition.

modify\_index\_subpartition

Use the `modify_index_subpartition` clause to mark `UNUSABLE` or allocate or deallocate storage for a subpartition of a local index on a composite-partitioned table. All other attributes of such a subpartition are inherited from partition-level default attributes.