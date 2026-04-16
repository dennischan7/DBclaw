---
source: MySQL 5.7 Reference
title: 00_Overview
---

To generate execution plans, the optimizer uses a cost model that is based on estimates of the cost of various operations that occur during query execution. The optimizer has a set of compiled-in default "cost constants" available to it to make decisions regarding execution plans.

The optimizer also has a database of cost estimates to use during execution plan construction. These estimates are stored in the server\_cost and engine\_cost tables in the mysql system database

and are configurable at any time. The intent of these tables is to make it possible to easily adjust the cost estimates that the optimizer uses when it attempts to arrive at query execution plans.

- [Cost Model General Operation](#page-99-0)
- [The Cost Model Database](#page-99-1)
- [Making Changes to the Cost Model Database](#page-101-0)

## <span id="page-99-0"></span>**Cost Model General Operation**

The configurable optimizer cost model works like this:

- The server reads the cost model tables into memory at startup and uses the in-memory values at runtime. Any non-NULL cost estimate specified in the tables takes precedence over the corresponding compiled-in default cost constant. Any NULL estimate indicates to the optimizer to use the compiled-in default.
- At runtime, the server may re-read the cost tables. This occurs when a storage engine is dynamically loaded or when a FLUSH OPTIMIZER\_COSTS statement is executed.
- Cost tables enable server administrators to easily adjust cost estimates by changing entries in the tables. It is also easy to revert to a default by setting an entry's cost to NULL. The optimizer uses the in-memory cost values, so changes to the tables should be followed by FLUSH OPTIMIZER\_COSTS to take effect.
- The in-memory cost estimates that are current when a client session begins apply throughout that session until it ends. In particular, if the server re-reads the cost tables, any changed estimates apply only to subsequently started sessions. Existing sessions are unaffected.
- Cost tables are specific to a given server instance. The server does not replicate cost table changes to replicas.

## <span id="page-99-1"></span>**The Cost Model Database**

The optimizer cost model database consists of two tables in the mysql system database that contain cost estimate information for operations that occur during query execution:

- server\_cost: Optimizer cost estimates for general server operations
- engine\_cost: Optimizer cost estimates for operations specific to particular storage engines

The server\_cost table contains these columns:

• cost\_name

The name of a cost estimate used in the cost model. The name is not case-sensitive. If the server does not recognize the cost name when it reads this table, it writes a warning to the error log.

• cost\_value

The cost estimate value. If the value is non-NULL, the server uses it as the cost. Otherwise, it uses the default estimate (the compiled-in value). DBAs can change a cost estimate by updating this column. If the server finds that the cost value is invalid (nonpositive) when it reads this table, it writes a warning to the error log.

To override a default cost estimate (for an entry that specifies NULL), set the cost to a non-NULL value. To revert to the default, set the value to NULL. Then execute FLUSH OPTIMIZER\_COSTS to tell the server to re-read the cost tables.

• last\_update

The time of the last row update.

• comment

A descriptive comment associated with the cost estimate. DBAs can use this column to provide information about why a cost estimate row stores a particular value.

The primary key for the server\_cost table is the cost\_name column, so it is not possible to create multiple entries for any cost estimate.

The server recognizes these cost\_name values for the server\_cost table:

• disk\_temptable\_create\_cost (default 40.0), disk\_temptable\_row\_cost (default 1.0)

The cost estimates for internally created temporary tables stored in a disk-based storage engine (either InnoDB or MyISAM). Increasing these values increases the cost estimate of using internal temporary tables and makes the optimizer prefer query plans with less use of them. For information about such tables, see [Section 8.4.4, "Internal Temporary Table Use in MySQL".](#page-48-0)

The larger default values for these disk parameters compared to the default values for the corresponding memory parameters (memory\_temptable\_create\_cost, memory\_temptable\_row\_cost) reflects the greater cost of processing disk-based tables.

• key\_compare\_cost (default 0.1)

The cost of comparing record keys. Increasing this value causes a query plan that compares many keys to become more expensive. For example, a query plan that performs a filesort becomes relatively more expensive compared to a query plan that avoids sorting by using an index.

• memory\_temptable\_create\_cost (default 2.0), memory\_temptable\_row\_cost (default 0.2)

The cost estimates for internally created temporary tables stored in the MEMORY storage engine. Increasing these values increases the cost estimate of using internal temporary tables and makes the optimizer prefer query plans with less use of them. For information about such tables, see [Section 8.4.4, "Internal Temporary Table Use in MySQL"](#page-48-0).

The smaller default values for these memory parameters compared to the default values for the corresponding disk parameters (disk\_temptable\_create\_cost, disk\_temptable\_row\_cost) reflects the lesser cost of processing memory-based tables.

• row\_evaluate\_cost (default 0.2)

The cost of evaluating record conditions. Increasing this value causes a query plan that examines many rows to become more expensive compared to a query plan that examines fewer rows. For example, a table scan becomes relatively more expensive compared to a range scan that reads fewer rows.

The engine\_cost table contains these columns:

• engine\_name

The name of the storage engine to which this cost estimate applies. The name is not case-sensitive. If the value is default, it applies to all storage engines that have no named entry of their own. If the server does not recognize the engine name when it reads this table, it writes a warning to the error log.

• device\_type

The device type to which this cost estimate applies. The column is intended for specifying different cost estimates for different storage device types, such as hard disk drives versus solid state drives. Currently, this information is not used and 0 is the only permitted value.

• cost\_name

Same as in the server\_cost table.

• cost\_value

Same as in the server\_cost table.

• last\_update

Same as in the server\_cost table.

• comment

Same as in the server\_cost table.

The primary key for the engine\_cost table is a tuple comprising the (cost\_name, engine\_name, device\_type) columns, so it is not possible to create multiple entries for any combination of values in those columns.

The server recognizes these cost\_name values for the engine\_cost table:

• io\_block\_read\_cost (default 1.0)

The cost of reading an index or data block from disk. Increasing this value causes a query plan that reads many disk blocks to become more expensive compared to a query plan that reads fewer disk blocks. For example, a table scan becomes relatively more expensive compared to a range scan that reads fewer blocks.

• memory\_block\_read\_cost (default 1.0)

Similar to io\_block\_read\_cost, but represents the cost of reading an index or data block from an in-memory database buffer.

If the io\_block\_read\_cost and memory\_block\_read\_cost values differ, the execution plan may change between two runs of the same query. Suppose that the cost for memory access is less than the cost for disk access. In that case, at server startup before data has been read into the buffer pool, you may get a different plan than after the query has been run because then the data is in memory.

### <span id="page-101-0"></span>**Making Changes to the Cost Model Database**

For DBAs who wish to change the cost model parameters from their defaults, try doubling or halving the value and measuring the effect.

Changes to the io\_block\_read\_cost and memory\_block\_read\_cost parameters are most likely to yield worthwhile results. These parameter values enable cost models for data access methods to take into account the costs of reading information from different sources; that is, the cost of reading information from disk versus reading information already in a memory buffer. For example, all other things being equal, setting io\_block\_read\_cost to a value larger than memory\_block\_read\_cost causes the optimizer to prefer query plans that read information already held in memory to plans that must read from disk.

This example shows how to change the default value for io\_block\_read\_cost:

```
UPDATE mysql.engine_cost
 SET cost_value = 2.0
 WHERE cost_name = 'io_block_read_cost';
FLUSH OPTIMIZER_COSTS;
```

This example shows how to change the value of io\_block\_read\_cost only for the InnoDB storage engine:

```
INSERT INTO mysql.engine_cost
```

```
 VALUES ('InnoDB', 0, 'io_block_read_cost', 3.0,
 CURRENT_TIMESTAMP, 'Using a slower disk for InnoDB');
FLUSH OPTIMIZER_COSTS;
```