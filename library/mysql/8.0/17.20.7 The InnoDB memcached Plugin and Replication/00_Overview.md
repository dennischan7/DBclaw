---
source: MySQL 8.0 Reference
title: 00_Overview
---

Because the daemon\_memcached plugin supports the MySQL binary log, source server through the memcached interface can be replicated for backup, balancing intensive read workloads, and high availability. All memcached commands are supported with binary logging.

You do not need to set up the daemon\_memcached plugin on replica servers. The primary advantage of this configuration is increased write throughput on the source. The speed of the replication mechanism is not affected.

The following sections show how to use the binary log capability when using the daemon\_memcached plugin with MySQL replication. It is assumed that you have completed the setup described in [Section 17.20.3, "Setting Up the InnoDB memcached Plugin"](#page-131-0).

## <span id="page-152-0"></span>**Enabling the InnoDB memcached Binary Log**

1. To use the daemon\_memcached plugin with the MySQL binary log, enable the [innodb\\_api\\_enable\\_binlog](#page-1-0) configuration option on the source server. This option can only be set at server startup. You must also enable the MySQL binary log on the source server using the --log-bin option. You can add these options to the MySQL configuration file, or on the mysqld command line.

```
mysqld ... --log-bin -–innodb_api_enable_binlog=1
```

- 2. Configure the source and replica server, as described in Section 19.1.2, "Setting Up Binary Log File Position Based Replication".
- 3. Use mysqldump to create a source data snapshot, and sync the snapshot to the replica server.

```
source $> mysqldump --all-databases --lock-all-tables > dbdump.db
replica $> mysql < dbdump.db
```

4. On the source server, issue SHOW MASTER STATUS to obtain the source binary log coordinates.

```
mysql> SHOW MASTER STATUS;
```

5. On the replica server, use a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) to set up a replica server using the source binary log coordinates.

```
mysql> CHANGE MASTER TO
 MASTER_HOST='localhost',
 MASTER_USER='root',
 MASTER_PASSWORD='',
 MASTER_PORT = 13000,
 MASTER_LOG_FILE='0.000001,
 MASTER_LOG_POS=114;
Or from MySQL 8.0.23:
mysql> CHANGE REPLICATION SOURCE TO
 SOURCE_HOST='localhost',
 SOURCE_USER='root',
 SOURCE_PASSWORD='',
 SOURCE_PORT = 13000,
 SOURCE_LOG_FILE='0.000001,
 SOURCE_LOG_POS=114;
```

6. Start the replica.

```
mysql> START SLAVE;
Or from MySQL 8.0.22:
mysql> START REPLICA;
```

If the error log prints output similar to the following, the replica is ready for replication.

```
2013-09-24T13:04:38.639684Z 49 [Note] Replication I/O thread: connected to
source 'root@localhost:13000', replication started in log '0.000001'
at position 114
```

## **Testing the InnoDB memcached Replication Configuration**

This example demonstrates how to test the InnoDB memcached replication configuration using the memcached and telnet to insert, update, and delete data. A MySQL client is used to verify results on the source and replica servers.

The example uses the demo\_test table, which was created by the innodb\_memcached\_config.sql configuration script during the initial setup of the daemon\_memcached plugin. The demo\_test table contains a single example record.

1. Use the set command to insert a record with a key of test1, a flag value of 10, an expiration value of 0, a cas value of 1, and a value of t1.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
set test1 10 0 1
t1
STORED
```

2. On the source server, check that the record was inserted into the demo\_test table. Assuming the demo\_test table was not previously modified, there should be two records. The example record with a key of AA, and the record you just inserted, with a key of test1. The c1 column maps to the key, the c2 column to the value, the c3 column to the flag value, the c4 column to the cas value, and the c5 column to the expiration time. The expiration time was set to 0, since it is unused.

```
mysql> SELECT * FROM test.demo_test;
+-------+--------------+------+------+------+
| c1 | c2 | c3 | c4 | c5 |
+-------+--------------+------+------+------+
| AA | HELLO, HELLO | 8 | 0 | 0 |
| test1 | t1 | 10 | 1 | 0 |
+-------+--------------+------+------+------+
```

3. Check to verify that the same record was replicated to the replica server.

```
mysql> SELECT * FROM test.demo_test;
+-------+--------------+------+------+------+
```

```
| c1 | c2 | c3 | c4 | c5 |
+-------+--------------+------+------+------+
| AA | HELLO, HELLO | 8 | 0 | 0 |
| test1 | t1 | 10 | 1 | 0 |
+-------+--------------+------+------+------+
```

4. Use the set command to update the key to a value of new.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
set test1 10 0 2
new
STORED
```

The update is replicated to the replica server (notice that the cas value is also updated).

```
mysql> SELECT * FROM test.demo_test;
+-------+--------------+------+------+------+
| c1 | c2 | c3 | c4 | c5 |
+-------+--------------+------+------+------+
| AA | HELLO, HELLO | 8 | 0 | 0 |
| test1 | new | 10 | 2 | 0 |
+-------+--------------+------+------+------+
```

5. Delete the test1 record using a delete command.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
delete test1
DELETED
```

When the delete operation is replicated to the replica, the test1 record on the replica is also deleted.

```
mysql> SELECT * FROM test.demo_test;
+----+--------------+------+------+------+
| c1 | c2 | c3 | c4 | c5 |
+----+--------------+------+------+------+
| AA | HELLO, HELLO | 8 | 0 | 0 |
+----+--------------+------+------+------+
```

6. Remove all rows from the table using the flush\_all command.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
flush_all
OK
mysql> SELECT * FROM test.demo_test;
Empty set (0.00 sec)
```

7. Telnet to the source server and enter two new records.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'
set test2 10 0 4
again
STORED
set test3 10 0 5
again1
STORED
```

8. Confirm that the two records were replicated to the replica server.

```
mysql> SELECT * FROM test.demo_test;
+-------+--------------+------+------+------+
| c1 | c2 | c3 | c4 | c5 |
+-------+--------------+------+------+------+
| test2 | again | 10 | 4 | 0 |
| test3 | again1 | 10 | 5 | 0 |
+-------+--------------+------+------+------+
```

9. Remove all rows from the table using the flush\_all command.

```
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
flush_all
OK
```

10. Check to ensure that the flush\_all operation was replicated on the replica server.

```
mysql> SELECT * FROM test.demo_test;
Empty set (0.00 sec)
```

## **InnoDB memcached Binary Log Notes**

### Binary Log Format:

- Most memcached operations are mapped to DML statements (analogous to insert, delete, update). Since there is no actual SQL statement being processed by the MySQL server, all memcached commands (except for flush\_all) use Row-Based Replication (RBR) logging, which is independent of any server binlog\_format setting.
- The memcached flush\_all command is mapped to the TRUNCATE TABLE command in MySQL 5.7 and earlier. Since DDL commands can only use statement-based logging, the flush\_all command is replicated by sending a TRUNCATE TABLE statement. In MySQL 8.0 and later, flush\_all is mapped to DELETE but is still replicated by sending a TRUNCATE TABLE statement.

#### Transactions:

- The concept of transactions has not typically been part of memcached applications. For performance considerations, daemon\_memcached\_r\_batch\_size and daemon\_memcached\_w\_batch\_size are used to control the batch size for read and write transactions. These settings do not affect replication. Each SQL operation on the underlying InnoDB table is replicated after successful completion.
- The default value of daemon\_memcached\_w\_batch\_size is 1, which means that each memcached write operation is committed immediately. This default setting incurs a certain amount of performance overhead to avoid inconsistencies in the data that is visible on the source and replica servers. The replicated records are always available immediately on the replica server. If you set daemon\_memcached\_w\_batch\_size to a value greater than 1, records inserted or updated through memcached are not immediately visible on the source server; to view the records on the source server before they are committed, issue SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED.

# <span id="page-155-0"></span>**17.20.8 InnoDB memcached Plugin Internals**

## **InnoDB API for the InnoDB memcached Plugin**

The InnoDB memcached engine accesses InnoDB through InnoDB APIs, most of which are directly adopted from embedded InnoDB. InnoDB API functions are passed to the InnoDB memcached engine as callback functions. InnoDB API functions access the InnoDB tables directly, and are mostly DML operations with the exception of TRUNCATE TABLE.

memcached commands are implemented through the InnoDB memcached API. The following table outlines how memcached commands are mapped to DML or DDL operations.

**Table 17.27 memcached Commands and Associated DML or DDL Operations**

| memcached Command | DML or DDL Operations                                                                  |
|-------------------|----------------------------------------------------------------------------------------|
| get               | a read/fetch command                                                                   |
| set               | a search followed by an INSERT or UPDATE<br>(depending on whether or not a key exists) |
| add               | a search followed by an INSERT or UPDATE                                               |
| replace           | a search followed by an UPDATE                                                         |
| append            | a search followed by an UPDATE (appends data to<br>the result before UPDATE)           |
| prepend           | a search followed by an UPDATE (prepends data<br>to the result before UPDATE)          |
| incr              | a search followed by an UPDATE                                                         |
| decr              | a search followed by an UPDATE                                                         |
| delete            | a search followed by a DELETE                                                          |
| flush_all         | TRUNCATE TABLE (DDL)                                                                   |

## **InnoDB memcached Plugin Configuration Tables**

This section describes configuration tables used by the daemon\_memcached plugin. The cache\_policies table, config\_options table, and containers table are created by the innodb\_memcached\_config.sql configuration script in the innodb\_memcache database.

```
mysql> USE innodb_memcache;
Database changed
mysql> SHOW TABLES;
+---------------------------+
| Tables_in_innodb_memcache |
+---------------------------+
| cache_policies |
| config_options |
| containers |
+---------------------------+
```

## **cache\_policies Table**

The cache\_policies table defines a cache policy for the InnoDB memcached installation. You can specify individual policies for get, set, delete, and flush operations, within a single cache policy. The default setting for all operations is innodb\_only.

- innodb\_only: Use InnoDB as the data store.
- cache\_only: Use the memcached engine as the data store.
- caching: Use both InnoDB and the memcached engine as data stores. In this case, if memcached cannot find a key in memory, it searches for the value in an InnoDB table.
- disable: Disable caching.

**Table 17.28 cache\_policies Columns**

| Column      | Description                                 |
|-------------|---------------------------------------------|
| policy_name | Name of the cache policy. The default cache |
|             | policy name is cache_policy.                |

| Column        | Description                                                                                                                                          |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| get_policy    | The cache policy for get operations. Valid values<br>are innodb_only, cache_only, caching, or<br>disabled. The default setting is innodb_only.       |
| set_policy    | The cache policy for set operations. Valid values<br>are innodb_only, cache_only, caching, or<br>disabled. The default setting is innodb_only.       |
| delete_policy | The cache policy for delete operations. Valid<br>values are innodb_only, cache_only,<br>caching, or disabled. The default setting is<br>innodb_only. |
| flush_policy  | The cache policy for flush operations. Valid values<br>are innodb_only, cache_only, caching, or<br>disabled. The default setting is innodb_only.     |

## **config\_options Table**

The config\_options table stores memcached-related settings that can be changed at runtime using SQL. Supported configuration options are separator and table\_map\_delimiter.

**Table 17.29 config\_options Columns**

| Column | Description                                                                                                                                                                                                                                                                                                                                                                               |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name   | Name of the memcached-related configuration<br>option. The following configuration options are<br>supported by the config_options table:                                                                                                                                                                                                                                                  |
|        | •<br>separator: Used to separate values of a<br>long string into separate values when there are<br>multiple value_columns defined. By default,<br>the separator is a   character. For example, if<br>you define col1, col2 as value columns, and<br>you define   as the separator, you can issue the<br>following memcached command to insert values<br>into col1 and col2, respectively: |
|        | set keyx 10 0 19<br>valuecolx valuecoly                                                                                                                                                                                                                                                                                                                                                   |
|        | valuecol1x is stored in col1 and<br>valuecoly is stored in col2.                                                                                                                                                                                                                                                                                                                          |
|        | •<br>table_map_delimiter: The character<br>separating the schema name and the table<br>name when you use the @@ notation in a<br>key name to access a key in a specific<br>table. For example, @@t1.some_key and<br>@@t2.some_key have the same key value, but<br>are stored in different tables.                                                                                         |
| Value  | The value assigned to the memcached-related<br>configuration option.                                                                                                                                                                                                                                                                                                                      |

## **containers Table**

The containers table is the most important of the three configuration tables. Each InnoDB table that is used to store memcached values must have an entry in the containers table. The entry provides a mapping between InnoDB table columns and container table columns, which is required for memcached to work with InnoDB tables.

The containers table contains a default entry for the test.demo\_test table, which is created by the innodb\_memcached\_config.sql configuration script. To use the daemon\_memcached plugin with your own InnoDB table, you must create an entry in the containers table.

**Table 17.30 containers Columns**

| Column             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | The name given to the container. If an InnoDB<br>table is not requested by name using @@ notation,<br>the daemon_memcached plugin uses the<br>InnoDB table with a containers.name value of<br>default. If there is no such entry, the first entry<br>in the containers table, ordered alphabetically<br>by name (ascending), determines the default<br>InnoDB table.                                                                                                                                                                                                                                                                                                               |
| db_schema          | The name of the database where the InnoDB<br>table resides. This is a required value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| db_table           | The name of the InnoDB table that stores<br>memcached values. This is a required value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| key_columns        | The column in the InnoDB table that contains<br>lookup key values for memcached operations.<br>This is a required value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| value_columns      | The InnoDB table columns (one or more) that<br>store memcached data. Multiple columns can be<br>specified using the separator character specified<br>in the innodb_memcached.config_options<br>table. By default, the separator is a pipe character<br>(" "). To specify multiple columns, separate them<br>with the defined separator character. For example:<br>col1 col2 col3. This is a required value.                                                                                                                                                                                                                                                                        |
| flags              | The InnoDB table columns that are used as<br>flags (a user-defined numeric value that is<br>stored and retrieved along with the main value)<br>for memcached. A flag value can be used as<br>a column specifier for some operations (such<br>as incr, prepend) if a memcached value is<br>mapped to multiple columns, so that an operation<br>is performed on a specified column. For example,<br>if you have mapped a value_columns to<br>three InnoDB table columns, and only want the<br>increment operation performed on one columns,<br>use the flags column to specify the column. If<br>you do not use the flags column, set a value of 0<br>to indicate that it is unused. |
| cas_column         | The InnoDB table column that stores compare<br>and-swap (cas) values. The cas_column value<br>is related to the way memcached hashes requests<br>to different servers and caches data in memory.<br>Because the InnoDB memcached plugin is tightly<br>integrated with a single memcached daemon, and<br>the in-memory caching mechanism is handled by<br>MySQL and the InnoDB buffer pool, this column is<br>rarely needed. If you do not use this column, set a<br>value of 0 to indicate that it is unused.                                                                                                                                                                      |
| expire_time_column | The InnoDB table column that stores expiration<br>values. The expire_time_column value is                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

| Column                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                        | related to the way memcached hashes requests<br>to different servers and caches data in memory.<br>Because the InnoDB memcached plugin is tightly<br>integrated with a single memcached daemon, and<br>the in-memory caching mechanism is handled<br>by MySQL and the InnoDB buffer pool, this<br>column is rarely needed. If you do not use this<br>column, set a value of 0 to indicate that the<br>column is unused. The maximum expire time is<br>defined as INT_MAX32 or 2147483647 seconds<br>(approximately 68 years). |
| unique_idx_name_on_key | The name of the index on the key column. It must<br>be a unique index. It can be the primary key or<br>a secondary index. Preferably, use the primary<br>key of the InnoDB table. Using the primary key<br>avoids a lookup that is performed when using a<br>secondary index. You cannot make a covering<br>index for memcached lookups; InnoDB returns an<br>error if you try to define a composite secondary<br>index over both the key and value columns.                                                                  |

### **containers Table Column Constraints**

- You must supply a value for db\_schema, db\_name, key\_columns, value\_columns and unique\_idx\_name\_on\_key. Specify 0 for flags, cas\_column, and expire\_time\_column if they are unused. Failing to do so could cause your setup to fail.
- key\_columns: The maximum limit for a memcached key is 250 characters, which is enforced by memcached. The mapped key must be a non-Null CHAR or VARCHAR type.
- value\_columns: Must be mapped to a CHAR, VARCHAR, or BLOB column. There is no length restriction and the value can be NULL.
- cas\_column: The cas value is a 64 bit integer. It must be mapped to a BIGINT of at least 8 bytes. If you do not use this column, set a value of 0 to indicate that it is unused.
- expiration\_time\_column: Must mapped to an INTEGER of at least 4 bytes. Expiration time is defined as a 32-bit integer for Unix time (the number of seconds since January 1, 1970, as a 32-bit value), or the number of seconds starting from the current time. For the latter, the number of seconds may not exceed 60\*60\*24\*30 (the number of seconds in 30 days). If the number sent by a client is larger, the server considers it to be a real Unix time value rather than an offset from the current time. If you do not use this column, set a value of 0 to indicate that it is unused.
- flags: Must be mapped to an INTEGER of at least 32-bits and can be NULL. If you do not use this column, set a value of 0 to indicate that it is unused.

A pre-check is performed at plugin load time to enforce column constraints. If mismatches are found, the plugin is not loaded.

### **Multiple Value Column Mapping**

- During plugin initialization, when InnoDB memcached is configured with information defined in the containers table, each mapped column defined in containers.value\_columns is verified against the mapped InnoDB table. If multiple InnoDB table columns are mapped, there is a check to ensure that each column exists and is the right type.
- At run-time, for memcached insert operations, if there are more delimited values than the number of mapped columns, only the number of mapped values are taken. For example, if there are six

mapped columns, and seven delimited values are provided, only the first six delimited values are taken. The seventh delimited value is ignored.

- If there are fewer delimited values than mapped columns, unfilled columns are set to NULL. If an unfilled column cannot be set to NULL, insert operations fail.
- If a table has more columns than mapped values, the extra columns do not affect results.

## **The demo\_test Example Table**

The innodb\_memcached\_config.sql configuration script creates a demo\_test table in the test database, which can be used to verify InnoDB memcached plugin installation immediately after setup.

The innodb\_memcached\_config.sql configuration script also creates an entry for the demo\_test table in the innodb\_memcache.containers table.

```
mysql> SELECT * FROM innodb_memcache.containers\G
*************************** 1. row ***************************
 name: aaa
 db_schema: test
 db_table: demo_test
 key_columns: c1
 value_columns: c2
 flags: c3
 cas_column: c4
 expire_time_column: c5
unique_idx_name_on_key: PRIMARY
mysql> SELECT * FROM test.demo_test;
+----+------------------+------+------+------+
| c1 | c2 | c3 | c4 | c5 |
+----+------------------+------+------+------+
| AA | HELLO, HELLO | 8 | 0 | 0 |
+----+------------------+------+------+------+
```