# Oracle 21c - allocate_extent_clause
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/allocate_extent_clause.html

Purpose

Use the `allocate_extent_clause` clause to explicitly allocate a new extent for a database object.

Explicitly allocating an extent with this clause does not change the values of the `NEXT` and `PCTINCREASE` storage parameters, so does not affect the size of the next extent to be allocated implicitly by Oracle Database. Refer to [storage\_clause](storage_clause.md#GUID-C5A67610-3160-41E9-8D48-03206BD5ED15) for information about the `NEXT` and `PCTINCREASE` storage parameters.

You can allocate an extent in the following SQL statements:

* `ALTER` `CLUSTER` (see [ALTER CLUSTER](ALTER-CLUSTER.md#GUID-A4E03C13-7690-4567-9B0A-DA6A21173B4D))
* `ALTER` `INDEX`: to allocate an extent to the index, an index partition, or an index subpartition (see [ALTER INDEX](ALTER-INDEX.md#GUID-D8F648E7-8C07-4C89-BB71-862512536558))
* `ALTER` `MATERIALIZED` `VIEW`: to allocate an extent to the materialized view, one of its partitions or subpartitions, or the overflow segment of an index-organized materialized view (see [ALTER MATERIALIZED VIEW](ALTER-MATERIALIZED-VIEW.md#GUID-29EE5682-AE42-4879-ABAD-E34E66ADD233))
* `ALTER` `MATERIALIZED` `VIEW` `LOG` (see [ALTER MATERIALIZED VIEW LOG](ALTER-MATERIALIZED-VIEW-LOG.md#GUID-4DAD5E6F-E30A-43D0-B023-634752E0E627))
* `ALTER` `TABLE`: to allocate an extent to the table, a table partition, a table subpartition, the mapping table of an index-organized table, the overflow segment of an index-organized table, or a LOB storage segment (see [ALTER TABLE](ALTER-TABLE.md#GUID-552E7373-BF93-477D-9DA3-B2C9386F2877))

Semantics

This section describes the parameters of the `allocate_extent_clause`. For additional information, refer to the SQL statement in which you set or reset these parameters for a particular database object.

You cannot specify the `allocate_extent_clause` and the `deallocate_unused_clause` in the same statement.

SIZE

Specify the size of the extent in bytes. The value of `integer` can be 0 through 2147483647. To specify a larger extent size, use an integer within this range with `K`, `M`, `G`, or `T` to specify the extent size in kilobytes, megabytes, gigabytes, or terabytes.

For a table, index, materialized view, or materialized view log, if you omit `SIZE`, then Oracle Database determines the size based on the values of the storage parameters of the object. However, for a cluster, Oracle does not evaluate the cluster's storage parameters, so you must specify `SIZE` if you do not want Oracle to use a default value.

DATAFILE 'filename'

Specify one of the data files in the tablespace of the table, cluster, index, materialized view, or materialized view log to contain the new extent. If you omit `DATAFILE`, then Oracle chooses the data file.

INSTANCE integer

Use this parameter only if you are using Oracle Real Application Clusters.

Specifying `INSTANCE` `integer` makes the new extent available to the freelist group associated with the specified instance. If the instance number exceeds the maximum number of freelist groups, then Oracle divides the specified number by the maximum number and uses the remainder to identify the freelist group to be used. An instance is identified by the value of its initialization parameter `INSTANCE_NUMBER`.

If you omit this parameter, then the space is allocated to the table, cluster, index, materialized view, or materialized view log but is not drawn from any particular freelist group. Instead, Oracle uses the master freelist and allocates space as needed.

Note:

If you are using automatic segment-space management, then the `INSTANCE` parameter of the `allocate_extent_clause` may not reserve the newly allocated space for the specified instance, because automatic segment-space management does not maintain rigid affinity between extents and instances.