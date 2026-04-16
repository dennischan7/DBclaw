# Oracle 21c - shard_chunk_id-operator
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/shard_chunk_id-operator.html

You can use the SQL operator `SHARD_CHUNK_ID` to get the chunk ID in a sharding environment. You must provide the table family ID and the sharding key as input.

This operator can be used in all three sharding types: system, user-defined, and composite. You can run the operator from the catalog and the shard.

Syntax

```
SELECT SHARD_CHUNK_ID( table_family, sharding_key1 [, sharding_key2 ...]) FROM table_name ...
```

Semantics

`table_family`

The first operand `table_family` refers to the identifier of the table family. It can be:

* The table family id that can be queried from the `GSMADMIN_INTERNAL.TABLE_FAMILY` table, or
* The name of the root table in the form of `SCHEMA_NAME.TABLE_NAME` .

If there is only one table family across the entire sharding environment, `table_family` can take NULL as input. This will default to the existing single table family.

`sharding_key`

The second operand `sharding_key` refers to a list of sharding keys. It can be a constant value or column name.

You must order the list of sharding keys as follows:

1. List of super-sharding keys in the order they are defined.
2. List of sharding keys in the order they are defined. For this refer to `GSMADMIN_INTERNAL.SHARDKEY_COLUMNS` .

In system and user-defined sharding environments, where super-sharding keys are not used, you only need to supply sharding keys.

Example

Given the composite sharded table `customers` defined as follows:

```
CREATE SHARDED TABLE customers (
    custno         NUMBER NOT NULL,
    name           VARCHAR2(50) NOT NULL,
    signup         DATE DEFAULT NULL,
    class          VARCHAR2(3) NOT NULL,
CONSTRAINT cust_pk PRIMARY KEY(custno,name))
PARTITIONSET BY LIST (class)
PARTITION BY CONSISTENT HASH (custno,name)
PARTITIONS AUTO
(PARTITIONSET gold VALUES ('gld') TABLESPACE SET tbs1,
 PARTITIONSET silver VALUES ('slv') TABLESPACE SET tbs2)
;
```

You can query it for the chunk ID with the following statement:

```
SELECT SHARD_CHUNK_ID(null, class, custno, name) FROM customers;
```