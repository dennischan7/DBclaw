# Oracle 11g - statements_9003
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_9003.htm

Specify the schema containing the table. If you omit `schema`, then Oracle Database assumes the table is in your own schema.

Specify the name of the table to be dropped. Oracle Database automatically performs the following operations:

* All rows from the table are dropped.
* All table indexes and domain indexes are dropped, as well as any triggers defined on the table, regardless of who created them or whose schema contains them. If `table` is partitioned, then any corresponding local index partitions are also dropped.
* All the storage tables of nested tables and LOBs of `table` are dropped.
* When you drop a range-, hash-, or list-partitioned table, then the database drops all the table partitions. If you drop a composite-partitioned table, then all the partitions and subpartitions are also dropped.
* When you drop a partitioned table with the `PURGE` keyword, the statement executes as a series of subtransactions, each of which drops a subset of partitions or subpartitions and their metadata. This division of the drop operation into subtransactions optimizes the processing of internal system resource consumption (for example, the library cache), especially for the dropping of very large partitioned tables. As soon as the first subtransaction commits, the table is marked `UNUSABLE`. If any of the subtransactions fails, then the only operation allowed on the table is another `DROP` `TABLE` ... `PURGE` statement. Such a statement will resume work from where the previous `DROP` `TABLE` statement failed, assuming that you have corrected any errors that the previous operation encountered.

  You can list the tables marked `UNUSABLE` by such a drop operation by querying the `status` column of the `*_TABLES`, `*_PART_TABLES`, `*_ALL_TABLES`, or `*_OBJECT_TABLES` data dictionary views, as appropriate.
* For an index-organized table, any mapping tables defined on the index-organized table are dropped.
* For a domain index, the appropriate drop routines are invoked. Refer to [Oracle Database Data Cartridge Developer's Guide](../../appdev.112/e10765/ext_idx_ref.md#ADDCI4200) for more information on these routines.
* If any statistics types are associated with the table, then the database disassociates the statistics types with the `FORCE` clause and removes any user-defined statistics collected with the statistics type.
* If the table is not part of a cluster, then the database returns all data blocks allocated to the table and its indexes to the tablespaces containing the table and its indexes.

  To drop a cluster and all its the tables, use the `DROP` `CLUSTER` statement with the `INCLUDING` `TABLES` clause to avoid dropping each table individually. See [DROP CLUSTER](statements_8007.md#i2066309).
* If the table is a base table for a view, a container or master table of a materialized view, or if it is referenced in a stored procedure, function, or package, then the database invalidates these dependent objects but does not drop them. You cannot use these objects unless you re-create the table or drop and re-create the objects so that they no longer depend on the table.

  If you choose to re-create the table, then it must contain all the columns selected by the subqueries originally used to define the materialized views and all the columns referenced in the stored procedures, functions, or packages. Any users previously granted object privileges on the views, stored procedures, functions, or packages need not be regranted these privileges.

  If the table is a master table for a materialized view, then the materialized view can still be queried, but it cannot be refreshed unless the table is re-created so that it contains all the columns selected by the defining query of the materialized view.

  If the table has a materialized view log, then the database drops this log and any other direct-path `INSERT` refresh information associated with the table.

Using this clause is equivalent to first dropping the table and then purging it from the recycle bin. This clause lets you save one step in the process. It also provides enhanced security if you want to prevent sensitive material from appearing in the recycle bin.