# Oracle 12c - release_changes
Source: https://docs.oracle.com/database/121/SQLRF/release_changes.htm

* The In-Memory Column Store (IM column store) is an optional, static SGA pool that stores copies of tables and partitions in a special columnar format optimized for rapid scans.

  See the [inmemory\_table\_clause](statements_7002.md#CEGBCAAE) of `CREATE` `TABLE`, the [inmemory\_clause](statements_7003.md#CEGCFHJD) of `CREATE` `TABLESPACE`, and the [inmemory\_table\_clause](statements_6002.md#CACHGBGI) of `CREATE` `MATERIALIZED` `VIEW`

  See the following hints:
* Oracle Database now supports JavaScript Object Notation (JSON).

  See the following conditions:

  See the following functions:

  See ["JSON Object Access Expressions"](expressions010.md#CHDCEFHI)
* Attribute clustering lets you cluster table data in close physical proximity based on the content of specified columns.

  See the [attribute\_clustering\_clause](statements_7002.md#CEGIDCDI) of `CREATE` `TABLE` and the [attribute\_clustering\_clause](statements_3001.md#CIHFJJFI) of `ALTER` `TABLE`

  See the following hints:
* Zone maps let you reduce the I/O and CPU costs of table scans by tracking the sets of contiguous data blocks, or zones, in which certain column values are stored. You can use zone maps with or without attribute clustering.

  See the statements [CREATE MATERIALIZED ZONEMAP](statements_6004.md#CACECJCC), [ALTER MATERIALIZED ZONEMAP](statements_2004.md#BGBBBEDH), and [DROP MATERIALIZED ZONEMAP](statements_8024.md#CEGFDBJJ), and the [zonemap\_clause](statements_7002.md#CEGDJAGF) of `CREATE` `TABLE`

  See the [NO\_ZONEMAP Hint](sql_elements006.md#CHDGDJEC) and the function [SYS\_OP\_ZONE\_ID](functions203.md#CJABIIAF)
* You can now create range-partitioned hash clusters.

  See the [cluster\_range\_partitions](statements_5002.md#CACGBDJH) clause of `CREATE` `CLUSTER` and the [allocate\_extent\_clause](statements_1005.md#i2085931) of `ALTER` `CLUSTER`
* The new function `APPROX_COUNT_DISTINCT` returns the approximate number of distinct values for a column. This function is an alternative to the `COUNT` function. It processes large amounts of data significantly faster than `COUNT`, with negligible deviation from the exact result.

  See [APPROX\_COUNT\_DISTINCT](functions013.md#CJAEJAGD)
* A new type of index compression called advanced index compression lets you improve compression ratios significantly while still providing efficient access to indexes.

  See the [advanced\_index\_compression](statements_5013.md#CACIEEBC) clause of `CREATE` `INDEX`
* For tables compressed with Hybrid Columnar Compression, you can now control whether row-level locking is used during DML operations.

  See the [[NO] ROW LEVEL LOCKING](statements_7002.md#CEGEFDAC) clause of `CREATE` `TABLE`
* The database now supports force full database caching mode, which allows you to designate the entire database, including NOCACHE LOBs, as eligible for caching in the buffer cache.

  See the [[NO] FORCE FULL DATABASE CACHING](statements_1006.md#BGBCFJGI) clause of `ALTER` `DATABASE`
* When you grant a database role to a user who is responsible for CBAC grants, you can now specify `WITH` `DELEGATE` `OPTION` in the `GRANT` statement to prevent giving the grantee additional privileges on the role. `WITH` `DELEGATE` `OPTION` is an alternative to `WITH` `ADMIN` `OPTION`. It enables a role to be granted to program units, but it does not permit the granting of the role to other principals or the administration of the role itself.

  See the [WITH DELEGATE OPTION](statements_9014.md#BGBFHJJI) clause of `GRANT`
* The new `READ` object privilege and `READ` `ANY` `TABLE` system privilege allow users to query tables, materialized views, views, and their synonyms.

  The `READ` object privilege is an alternative to the `SELECT` object privilege. In addition to querying objects, the `SELECT` object privilege allows users lock rows of a table with the `LOCK` `TABLE` and `SELECT` ... `FOR` `UPDATE` statements. The `READ` object privilege only allows users to query objects. See [Table 18-2](statements_9014.md#BGBCIIEG) for more information.

  The `READ` `ANY` `TABLE` system privilege is an alternative to the `SELECT` `ANY` `TABLE` system privilege. In addition to querying objects, the `SELECT` `ANY` `TABLE` privilege allows users to lock rows of a table with the `SELECT` ... `FOR` `UPDATE` statement. The `READ` `ANY` `TABLE` privilege only allows users to query objects. See [Table 18-1](statements_9014.md#BABEFFEE) for more information.