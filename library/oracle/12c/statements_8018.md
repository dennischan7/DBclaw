# Oracle 12c - statements_8018
Source: https://docs.oracle.com/database/121/SQLRF/statements_8018.htm

Purpose

Use the `DROP` `INDEX` statement to remove an index or domain index from the database.

When you drop a global partitioned index, a range-partitioned index, or a hash-partitioned index, all the index partitions are also dropped. If you drop a composite-partitioned index, then all the index partitions and subpartitions are also dropped.

In addition, when you drop a domain index:

* Oracle Database invokes the appropriate routine.
* If any statistics are associated with the domain index, then Oracle Database disassociates the statistics types with the `FORCE` clause and removes the user-defined statistics collected with the statistics type.

Semantics

schema

Specify the schema containing the index. If you omit `schema`, then Oracle Database assumes the index is in your own schema.

index

Specify the name of the index to be dropped. When the index is dropped, all data blocks allocated to the index are returned to the tablespace that contained the index.

ONLINE

Specify `ONLINE` to indicate that DML operations on the table or partition will be allowed while dropping the index.

FORCE

`FORCE` applies only to domain indexes. This clause drops the domain index even if the indextype routine invocation returns an error or the index is marked `IN` `PROGRESS`. Without `FORCE`, you cannot drop a domain index if its indextype routine invocation returns an error or the index is marked `IN` `PROGRESS`.

Restrictions on Dropping Indexes The following restrictions apply to dropping indexes:

* You cannot drop a domain index if the index or any of its index partitions is marked `IN_PROGRESS`.
* You cannot specify the `ONLINE` clause when dropping a domain index, a cluster index, or an index on a queue table.