# Oracle 11g - clauses007
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/clauses007.htm

Semantics

This section describes the parameters of the `physical_attributes_clause`. For additional information, refer to the SQL statement in which you set or reset these parameters for a particular database object.

PCTFREE integer

Specify a whole number representing the percentage of space in each data block of the database object reserved for future updates to rows of the object. The value of `PCTFREE` must be a value from 0 to 99. A value of 0 means that the entire block can be filled by inserts of new rows. The default value is 10. This value reserves 10% of each block for updates to existing rows and allows inserts of new rows to fill a maximum of 90% of each block.

`PCTFREE` has the same function in the statements that create and alter tables, partitions, clusters, indexes, materialized views, and materialized view logs. The combination of `PCTFREE` and `PCTUSED` determines whether new rows will be inserted into existing data blocks or into new blocks. See ["How PCTFREE and PCTUSED Work Together"](#BABCJFCF).

Restriction on the PCTFREE Clause When altering an index, you can specify this parameter only in the `modify_index_default_attrs` clause and the `split_index_partition` clause.

PCTUSED integer

Specify a whole number representing the minimum percentage of used space that Oracle maintains for each data block of the database object. `PCTUSED` is specified as a positive integer from 0 to 99 and defaults to 40.

`PCTUSED` has the same function in the statements that create and alter tables, partitions, clusters, materialized views, and materialized view logs.

`PCTUSED` is not a valid table storage characteristic for an index-organized table.

The sum of `PCTFREE` and `PCTUSED` must be equal to or less than 100. You can use `PCTFREE` and `PCTUSED` together to utilize space within a database object more efficiently. See ["How PCTFREE and PCTUSED Work Together"](#BABCJFCF).

Restrictions on the PCTUSED Clause The `PCTUSED` parameter is subject to the following restrictions:

How PCTFREE and PCTUSED Work Together

In a newly allocated data block, the space available for inserts is the block size minus the sum of the block overhead and free space (`PCTFREE`). Updates to existing data can use any available space in the block. Therefore, updates can reduce the available space of a block to less than `PCTFREE`.

After a data block is filled to the limit determined by `PCTFREE`, Oracle Database considers the block unavailable for the insertion of new rows until the percentage of that block falls beneath the parameter `PCTUSED`. Until this value is achieved, Oracle Database uses the free space of the data block only for updates to rows already contained in the data block. A block becomes a candidate for row insertion when its used space falls below `PCTUSED`.

See Also:

[FREELISTS](clauses009.md#BABECDAG)

for information on how

`PCTUSED`

and

`PCTFREE`

work with freelist segment space management

INITRANS integer

Specify the initial number of concurrent transaction entries allocated within each data block allocated to the database object. This value can range from 1 to 255 and defaults to 1, with the following exceptions:

* The default `INITRANS` value for a cluster is 2 or the default `INITRANS` value of the tablespace in which the cluster resides, whichever is greater.
* The default value for an index is 2.

In general, you should not change the `INITRANS` value from its default.

Each transaction that updates a block requires a transaction entry in the block. This parameter ensures that a minimum number of concurrent transactions can update the block and helps avoid the overhead of dynamically allocating a transaction entry.

The `INITRANS` parameter serves the same purpose in the statements that create and alter tables, partitions, clusters, indexes, materialized views, and materialized view logs.

MAXTRANS Parameter

In earlier releases, the `MAXTRANS` parameter determined the maximum number of concurrent update transactions allowed for each data block in the segment. This parameter has been deprecated. Oracle now automatically allows up to 255 concurrent update transactions for any data block, depending on the available space in the block.

Existing objects for which a value of `MAXTRANS` has already been set retain that setting. However, if you attempt to change the value for `MAXTRANS`, Oracle ignores the new specification and substitutes the value 255 without returning an error.

storage\_clause

The `storage_clause` lets you specify storage characteristics for the table, object table `OIDINDEX`, partition, LOB data segment, or index-organized table overflow data segment. This clause has performance ramifications for large tables. Storage should be allocated to minimize dynamic allocation of additional space. Refer to the [storage\_clause](clauses009.md#i997450) for more information.