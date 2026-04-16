# Oracle 21c - DROP-INDEX
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/DROP-INDEX.html

Purpose

Use the `DROP` `INDEX` statement to remove an index or domain index from the database.

When you drop a global partitioned index, a range-partitioned index, or a hash-partitioned index, all the index partitions are also dropped. If you drop a composite-partitioned index, then all the index partitions and subpartitions are also dropped.

In addition, when you drop a domain index:

* Oracle Database invokes the appropriate routine.
* If any statistics are associated with the domain index, then Oracle Database disassociates the statistics types with the `FORCE` clause and removes the user-defined statistics collected with the statistics type.

Prerequisites

The index must be in your own schema or you must have the `DROP` `ANY` `INDEX` system privilege.

schema

Specify the schema containing the index. If you omit `schema`, then Oracle Database assumes the index is in your own schema.

index

Specify the name of the index to be dropped. When the index is dropped, all data blocks allocated to the index are returned to the tablespace that contained the index.

ONLINE

Specify `ONLINE` to indicate that DML operations on the table or partition will be allowed while dropping the index.

FORCE

`FORCE` applies only to domain indexes. This clause drops the domain index even if the indextype routine invocation returns an error or the index is marked `IN` `PROGRESS`. Without `FORCE`, you cannot drop a domain index if its indextype routine invocation returns an error or the index is marked `IN` `PROGRESS`.

Note:

When dropping a domain index with `FORCE` option, the index will be dropped regardless of any errors happening in the indextype routine. The errors raised by the indextype routine are not reported.

Only use the `FORCE` option when the index or index partitions are marked `IN PROGRESS` or when `DROP INDEX` has already failed.

Restrictions on Dropping Indexes

The following restrictions apply to dropping indexes:

* You cannot drop a domain index if the index or any of its index partitions is marked `IN_PROGRESS`.
* You cannot specify the `ONLINE` clause when dropping a domain index, a cluster index, or an index on a queue table.

Examples

Dropping an Index: Example

This statement drops an index named `ord_customer_ix_demo`, which was created in "[Compressing an Index: Example](CREATE-INDEX.md#GUID-1F89BBC0-825F-4215-AF71-7588E31D8BFE__I2129467)":

```
DROP INDEX ord_customer_ix_demo;
```