---
source: MySQL 8.0 Reference
title: 00_Overview
---

The functions listed in this section are used for controlling position-based synchronization of source and replica servers in MySQL Replication.

**Table 14.28 Positional Synchronization Functions**

| Name              | Description                                                                                 | Deprecated |
|-------------------|---------------------------------------------------------------------------------------------|------------|
| MASTER_POS_WAIT() | Block until the replica has read<br>and applied all updates up to the<br>specified position | Yes        |
| SOURCE_POS_WAIT() | Block until the replica has read<br>and applied all updates up to the<br>specified position |            |

<span id="page-179-1"></span>• [MASTER\\_POS\\_WAIT\(](#page-179-1)log\_name,log\_pos[,timeout][,channel])

This function is for control of source-replica synchronization. It blocks until the replica has read and applied all updates up to the specified position in the source's binary log. From MySQL 8.0.26, [MASTER\\_POS\\_WAIT\(\)](#page-179-1) is deprecated and the alias [SOURCE\\_POS\\_WAIT\(\)](#page-180-0) should be used instead. In releases before MySQL 8.0.26, use [MASTER\\_POS\\_WAIT\(\)](#page-179-1).

The return value is the number of log events the replica had to wait for to advance to the specified position. The function returns NULL if the replication SQL thread is not started, the replica's source information is not initialized, the arguments are incorrect, or an error occurs. It returns -1 if the timeout has been exceeded. If the replication SQL thread stops while [MASTER\\_POS\\_WAIT\(\)](#page-179-1) is waiting, the function returns NULL. If the replica is past the specified position, the function returns immediately.

If the binary log file position has been marked as invalid, the function waits until a valid file position is known. The binary log file position can be marked as invalid when the CHANGE REPLICATION SOURCE TO option GTID\_ONLY is set for the replication channel, and the server is restarted or replication is stopped. The file position becomes valid after a transaction is successfully applied past the given file position. If the applier does not reach the stated position, the function waits until the timeout. Use a SHOW REPLICA STATUS statement to check if the binary log file position has been marked as invalid.

On a multithreaded replica, the function waits until expiry of the limit set by the replica\_checkpoint\_group, slave\_checkpoint\_group, replica\_checkpoint\_period or slave\_checkpoint\_period system variable, when the checkpoint operation is called to update the status of the replica. Depending on the setting for the system variables, the function might therefore return some time after the specified position was reached.

If binary log transaction compression is in use and the transaction payload at the specified position is compressed (as a Transaction\_payload\_event), the function waits until the whole transaction has been read and applied, and the positions have updated.

If a timeout value is specified, [MASTER\\_POS\\_WAIT\(\)](#page-179-1) stops waiting when timeout seconds have elapsed. timeout must be greater than or equal to 0. (When the server is running in strict SQL mode, a negative timeout value is immediately rejected with [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments); otherwise the function returns **NULL**, and raises a warning.)

The optional channel value enables you to name which replication channel the function applies to. See Section 19.2.2, "Replication Channels" for more information.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-180-0"></span>• [SOURCE\\_POS\\_WAIT\(](#page-180-0)log\_name,log\_pos[,timeout][,channel])

This function is for control of source-replica synchronization. It blocks until the replica has read and applied all updates up to the specified position in the source's binary log. From MySQL 8.0.26, use [SOURCE\\_POS\\_WAIT\(\)](#page-180-0) in place of [MASTER\\_POS\\_WAIT\(\)](#page-179-1), which is deprecated from that release. In releases before MySQL 8.0.26, use [MASTER\\_POS\\_WAIT\(\)](#page-179-1).

The return value is the number of log events the replica had to wait for to advance to the specified position. The function returns NULL if the replication SQL thread is not started, the replica's source information is not initialized, the arguments are incorrect, or an error occurs. It returns -1 if the timeout has been exceeded. If the replication SQL thread stops while [SOURCE\\_POS\\_WAIT\(\)](#page-180-0) is waiting, the function returns NULL. If the replica is past the specified position, the function returns immediately.

If the binary log file position has been marked as invalid, the function waits until a valid file position is known. The binary log file position can be marked as invalid when the CHANGE REPLICATION SOURCE TO option GTID\_ONLY is set for the replication channel, and the server is restarted or replication is stopped. The file position becomes valid after a transaction is successfully applied past the given file position. If the applier does not reach the stated position, the function waits until the timeout. Use a SHOW REPLICA STATUS statement to check if the binary log file position has been marked as invalid.

On a multithreaded replica, the function waits until expiry of the limit set by the replica\_checkpoint\_group or replica\_checkpoint\_period system variable, when the checkpoint operation is called to update the status of the replica. Depending on the setting for the system variables, the function might therefore return some time after the specified position was reached.

If binary log transaction compression is in use and the transaction payload at the specified position is compressed (as a Transaction\_payload\_event), the function waits until the whole transaction has been read and applied, and the positions have updated.

If a timeout value is specified, [SOURCE\\_POS\\_WAIT\(\)](#page-180-0) stops waiting when timeout seconds have elapsed. timeout must be greater than or equal to 0. (In strict SQL mode, a negative timeout value is immediately rejected with [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments); otherwise the function returns NULL, and raises a warning.)

The optional channel value enables you to name which replication channel the function applies to. See Section 19.2.2, "Replication Channels" for more information.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

# <span id="page-181-1"></span>**14.19 Aggregate Functions**

Aggregate functions operate on sets of values. They are often used with a GROUP BY clause to group values into subsets. This section describes most aggregate functions. For information about aggregate functions that operate on geometry values, see [Section 14.16.12, "Spatial Aggregate Functions".](#page-112-0)

# <span id="page-181-0"></span>**14.19.1 Aggregate Function Descriptions**

This section describes aggregate functions that operate on sets of values. They are often used with a GROUP BY clause to group values into subsets.

**Table 14.29 Aggregate Functions**

| Name             | Description                                      |
|------------------|--------------------------------------------------|
| AVG()            | Return the average value of the argument         |
| BIT_AND()        | Return bitwise AND                               |
| BIT_OR()         | Return bitwise OR                                |
| BIT_XOR()        | Return bitwise XOR                               |
| COUNT()          | Return a count of the number of rows returned    |
| COUNT(DISTINCT)  | Return the count of a number of different values |
| GROUP_CONCAT()   | Return a concatenated string                     |
| JSON_ARRAYAGG()  | Return result set as a single JSON array         |
| JSON_OBJECTAGG() | Return result set as a single JSON object        |
| MAX()            | Return the maximum value                         |
| MIN()            | Return the minimum value                         |
| STD()            | Return the population standard deviation         |
| STDDEV()         | Return the population standard deviation         |
| STDDEV_POP()     | Return the population standard deviation         |
| STDDEV_SAMP()    | Return the sample standard deviation             |
| SUM()            | Return the sum                                   |
| VAR_POP()        | Return the population standard variance          |

| Name       | Description                             |
|------------|-----------------------------------------|
| VAR_SAMP() | Return the sample variance              |
| VARIANCE() | Return the population standard variance |

Unless otherwise stated, aggregate functions ignore NULL values.

If you use an aggregate function in a statement containing no GROUP BY clause, it is equivalent to grouping on all rows. For more information, see [Section 14.19.3, "MySQL Handling of GROUP BY"](#page-197-0).

Most aggregate functions can be used as window functions. Those that can be used this way are signified in their syntax description by [over\_clause], representing an optional OVER clause. over\_clause is described in Section 14.20.2, "Window Function Concepts and Syntax", which also includes other information about window function usage.

For numeric arguments, the variance and standard deviation functions return a DOUBLE value. The [SUM\(\)](#page-191-0) and [AVG\(\)](#page-182-1) functions return a DECIMAL value for exact-value arguments (integer or DECIMAL), and a DOUBLE value for approximate-value arguments (FLOAT or DOUBLE).

The [SUM\(\)](#page-191-0) and [AVG\(\)](#page-182-1) aggregate functions do not work with temporal values. (They convert the values to numbers, losing everything after the first nonnumeric character.) To work around this problem, convert to numeric units, perform the aggregate operation, and convert back to a temporal value. Examples:

```
SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_col))) FROM tbl_name;
SELECT FROM_DAYS(SUM(TO_DAYS(date_col))) FROM tbl_name;
```

Functions such as [SUM\(\)](#page-191-0) or [AVG\(\)](#page-182-1) that expect a numeric argument cast the argument to a number if necessary. For SET or ENUM values, the cast operation causes the underlying numeric value to be used.

The [BIT\\_AND\(\)](#page-182-0), [BIT\\_OR\(\)](#page-183-0), and [BIT\\_XOR\(\)](#page-184-0) aggregate functions perform bit operations. Prior to MySQL 8.0, bit functions and operators required BIGINT (64-bit integer) arguments and returned BIGINT values, so they had a maximum range of 64 bits. Non-BIGINT arguments were converted to BIGINT prior to performing the operation and truncation could occur.

In MySQL 8.0, bit functions and operators permit binary string type arguments (BINARY, VARBINARY, and the BLOB types) and return a value of like type, which enables them to take arguments and produce return values larger than 64 bits. For discussion about argument evaluation and result types for bit operations, see the introductory discussion in [Section 14.12, "Bit Functions and Operators".](#page-35-0)

<span id="page-182-1"></span>• [AVG\(\[DISTINCT\]](#page-182-1) expr) [over\_clause]

Returns the average value of expr. The DISTINCT option can be used to return the average of the distinct values of expr.

If there are no matching rows, [AVG\(\)](#page-182-1) returns NULL. The function also returns NULL if expr is NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax"; it cannot be used with DISTINCT.

```
mysql> SELECT student_name, AVG(test_score)
 FROM student
 GROUP BY student_name;
```

<span id="page-182-0"></span>• BIT\_AND(expr) [[over\\_clause](#page-182-0)]

Returns the bitwise AND of all bits in expr.

The result type depends on whether the function argument values are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the argument values have a binary string type, and the argument is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument value conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the argument values. If argument values have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. If the argument size exceeds 511 bytes, an [ER\\_INVALID\\_BITWISE\\_AGGREGATE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_aggregate_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

If there are no matching rows, [BIT\\_AND\(\)](#page-182-0) returns a neutral value (all bits set to 1) having the same length as the argument values.

NULL values do not affect the result unless all values are NULL. In that case, the result is a neutral value having the same length as the argument values.

For more information discussion about argument evaluation and result types, see the introductory discussion in [Section 14.12, "Bit Functions and Operators".](#page-35-0)

If [BIT\\_AND\(\)](#page-182-0) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

As of MySQL 8.0.12, this function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-183-0"></span>• BIT\_OR(expr) [[over\\_clause](#page-183-0)]

Returns the bitwise OR of all bits in expr.

The result type depends on whether the function argument values are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the argument values have a binary string type, and the argument is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument value conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the argument values. If argument values have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. If the argument size exceeds 511 bytes, an [ER\\_INVALID\\_BITWISE\\_AGGREGATE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_aggregate_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

If there are no matching rows, [BIT\\_OR\(\)](#page-183-0) returns a neutral value (all bits set to 0) having the same length as the argument values.

NULL values do not affect the result unless all values are NULL. In that case, the result is a neutral value having the same length as the argument values.

For more information discussion about argument evaluation and result types, see the introductory discussion in [Section 14.12, "Bit Functions and Operators".](#page-35-0)

If [BIT\\_OR\(\)](#page-183-0) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

As of MySQL 8.0.12, this function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-184-0"></span>• BIT\_XOR(expr) [[over\\_clause](#page-184-0)]

Returns the bitwise XOR of all bits in expr.

The result type depends on whether the function argument values are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the argument values have a binary string type, and the argument is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument value conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the argument values. If argument values have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. If the argument size exceeds 511 bytes, an [ER\\_INVALID\\_BITWISE\\_AGGREGATE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_aggregate_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

If there are no matching rows, [BIT\\_XOR\(\)](#page-184-0) returns a neutral value (all bits set to 0) having the same length as the argument values.

NULL values do not affect the result unless all values are NULL. In that case, the result is a neutral value having the same length as the argument values.

For more information discussion about argument evaluation and result types, see the introductory discussion in [Section 14.12, "Bit Functions and Operators".](#page-35-0)

If [BIT\\_XOR\(\)](#page-184-0) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

As of MySQL 8.0.12, this function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-184-1"></span>• COUNT(expr) [[over\\_clause](#page-184-1)]

Returns a count of the number of non-NULL values of expr in the rows retrieved by a SELECT statement. The result is a BIGINT value.

If there are no matching rows, [COUNT\(\)](#page-184-1) returns 0. COUNT(NULL) returns 0.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

```
mysql> SELECT student.student_name,COUNT(*)
 FROM student,course
 WHERE student.student_id=course.student_id
```

```
 GROUP BY student_name;
```

[COUNT\(\\*\)](#page-184-1) is somewhat different in that it returns a count of the number of rows retrieved, whether or not they contain NULL values.

For transactional storage engines such as InnoDB, storing an exact row count is problematic. Multiple transactions may be occurring at the same time, each of which may affect the count.

InnoDB does not keep an internal count of rows in a table because concurrent transactions might "see" different numbers of rows at the same time. Consequently, SELECT COUNT(\*) statements only count rows visible to the current transaction.

As of MySQL 8.0.13, SELECT COUNT(\*) FROM tbl\_name query performance for InnoDB tables is optimized for single-threaded workloads if there are no extra clauses such as WHERE or GROUP BY.

InnoDB processes SELECT COUNT(\*) statements by traversing the smallest available secondary index unless an index or optimizer hint directs the optimizer to use a different index. If a secondary index is not present, InnoDB processes SELECT COUNT(\*) statements by scanning the clustered index.

Processing of SELECT COUNT(\*) statements takes some time if index records are not entirely in the buffer pool. For a faster count, create a counter table and let your application update it according to the inserts and deletes it does. However, this method may not scale well in situations where thousands of concurrent transactions are initiating updates to the same counter table. If an approximate row count is sufficient, use SHOW TABLE STATUS.

InnoDB handles SELECT COUNT(\*) and SELECT COUNT(1) operations in the same way. There is no performance difference.

For MyISAM tables, [COUNT\(\\*\)](#page-184-1) is optimized to return very quickly if the SELECT retrieves from one table, no other columns are retrieved, and there is no WHERE clause. For example:

```
mysql> SELECT COUNT(*) FROM student;
```

This optimization only applies to MyISAM tables, because an exact row count is stored for this storage engine and can be accessed very quickly. COUNT(1) is only subject to the same optimization if the first column is defined as NOT NULL.

<span id="page-185-0"></span>• [COUNT\(DISTINCT](#page-184-1) expr,[expr...])

Returns a count of the number of rows with different non-NULL expr values.

If there are no matching rows, [COUNT\(DISTINCT\)](#page-184-1) returns 0.

```
mysql> SELECT COUNT(DISTINCT results) FROM student;
```

In MySQL, you can obtain the number of distinct expression combinations that do not contain NULL by giving a list of expressions. In standard SQL, you would have to do a concatenation of all expressions inside [COUNT\(DISTINCT ...\)](#page-184-1).

<span id="page-185-1"></span>• [GROUP\\_CONCAT\(](#page-185-1)expr)

This function returns a string result with the concatenated non-NULL values from a group. It returns NULL if there are no non-NULL values. The full syntax is as follows:

```
GROUP_CONCAT([DISTINCT] expr [,expr ...]
 [ORDER BY {unsigned_integer | col_name | expr}
 [ASC | DESC] [,col_name ...]]
 [SEPARATOR str_val])
```

```
mysql> SELECT student_name,
 GROUP_CONCAT(test_score) 2556
```

```
 FROM student
 GROUP BY student_name;
```

Or:

```
mysql> SELECT student_name,
 GROUP_CONCAT(DISTINCT test_score
 ORDER BY test_score DESC SEPARATOR ' ')
 FROM student
 GROUP BY student_name;
```

In MySQL, you can get the concatenated values of expression combinations. To eliminate duplicate values, use the DISTINCT clause. To sort values in the result, use the ORDER BY clause. To sort in reverse order, add the DESC (descending) keyword to the name of the column you are sorting by in the ORDER BY clause. The default is ascending order; this may be specified explicitly using the ASC keyword. The default separator between values in a group is comma (,). To specify a separator explicitly, use SEPARATOR followed by the string literal value that should be inserted between group values. To eliminate the separator altogether, specify SEPARATOR ''.

The result is truncated to the maximum length that is given by the group\_concat\_max\_len system variable, which has a default value of 1024. The value can be set higher, although the effective maximum length of the return value is constrained by the value of max\_allowed\_packet. The syntax to change the value of group\_concat\_max\_len at runtime is as follows, where val is an unsigned integer:

```
SET [GLOBAL | SESSION] group_concat_max_len = val;
```

![](_page_186_Picture_7.jpeg)

### **Important**

When setting the value for group\_concat\_max\_len, consider the following:

- Estimate the maximum length required for [GROUP\\_CONCAT\(\)](#page-185-1) output and set the value accordingly.
- Setting the value excessively high can negatively affect performance and lead to out-of-memory (OOM) errors.
- In MySQL HeatWave, the maximum column length is 4 MB, so setting a value higher than this causes the output to be truncated. To avoid this, set a value under 4 MB.

The return value is a nonbinary or binary string, depending on whether the arguments are nonbinary or binary strings. The result type is TEXT or BLOB unless group\_concat\_max\_len is less than or equal to 512, in which case the result type is VARCHAR or VARBINARY.

If [GROUP\\_CONCAT\(\)](#page-185-1) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

See also CONCAT() and CONCAT\_WS(): Section 14.8, "String Functions and Operators".

<span id="page-186-0"></span>• [JSON\\_ARRAYAGG\(](#page-186-0)col\_or\_expr) [over\_clause]

Aggregates a result set as a single JSON array whose elements consist of the rows. The order of elements in this array is undefined. The function acts on a column or an expression that evaluates to a single value. Returns NULL if the result contains no rows, or in the event of an error. If col\_or\_expr is NULL, the function returns an array of JSON [null] elements.

As of MySQL 8.0.14, this function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

```
mysql> SELECT o_id, attribute, value FROM t3;
+------+-----------+-------+
```

```
| o_id | attribute | value |
+------+-----------+-------+
| 2 | color | red |
| 2 | fabric | silk |
| 3 | color | green |
| 3 | shape | square|
+------+-----------+-------+
4 rows in set (0.00 sec)
mysql> SELECT o_id, JSON_ARRAYAGG(attribute) AS attributes
 -> FROM t3 GROUP BY o_id;
+------+---------------------+
| o_id | attributes |
+------+---------------------+
| 2 | ["color", "fabric"] |
| 3 | ["color", "shape"] |
+------+---------------------+
2 rows in set (0.00 sec)
```

<span id="page-187-0"></span>• [JSON\\_OBJECTAGG\(](#page-187-0)key, value) [over\_clause]

Takes two column names or expressions as arguments, the first of these being used as a key and the second as a value, and returns a JSON object containing key-value pairs. Returns NULL if the result contains no rows, or in the event of an error. An error occurs if any key name is NULL or the number of arguments is not equal to 2.

As of MySQL 8.0.14, this function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

```
mysql> SELECT o_id, attribute, value FROM t3;
+------+-----------+-------+
| o_id | attribute | value |
+------+-----------+-------+
| 2 | color | red |
| 2 | fabric | silk |
| 3 | color | green |
| 3 | shape | square|
+------+-----------+-------+
4 rows in set (0.00 sec)
mysql> SELECT o_id, JSON_OBJECTAGG(attribute, value)
 -> FROM t3 GROUP BY o_id;
+------+---------------------------------------+
| o_id | JSON_OBJECTAGG(attribute, value) |
+------+---------------------------------------+
| 2 | {"color": "red", "fabric": "silk"} |
| 3 | {"color": "green", "shape": "square"} |
+------+---------------------------------------+
2 rows in set (0.00 sec)
```

**Duplicate key handling.** When the result of this function is normalized, values having duplicate keys are discarded. In keeping with the MySQL JSON data type specification that does not permit duplicate keys, only the last value encountered is used with that key in the returned object ("last duplicate key wins"). This means that the result of using this function on columns from a SELECT can depend on the order in which the rows are returned, which is not guaranteed.

When used as a window function, if there are duplicate keys within a frame, only the last value for the key is present in the result. The value for the key from the last row in the frame is deterministic if the ORDER BY specification guarantees that the values have a specific order. If not, the resulting value of the key is nondeterministic.

Consider the following:

```
mysql> CREATE TABLE t(c VARCHAR(10), i INT);
Query OK, 0 rows affected (0.33 sec)
mysql> INSERT INTO t VALUES ('key', 3), ('key', 4), ('key', 5);
Query OK, 3 rows affected (0.10 sec)
```

```
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT c, i FROM t;
+------+------+
| c | i |
+------+------+
| key | 3 |
| key | 4 |
| key | 5 |
+------+------+
3 rows in set (0.00 sec)
mysql> SELECT JSON_OBJECTAGG(c, i) FROM t;
+----------------------+
| JSON_OBJECTAGG(c, i) |
+----------------------+
| {"key": 5} |
+----------------------+
1 row in set (0.00 sec)
mysql> DELETE FROM t;
Query OK, 3 rows affected (0.08 sec)
mysql> INSERT INTO t VALUES ('key', 3), ('key', 5), ('key', 4);
Query OK, 3 rows affected (0.06 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT c, i FROM t;
+------+------+
| c | i |
+------+------+
| key | 3 |
| key | 5 |
| key | 4 |
+------+------+
3 rows in set (0.00 sec)
mysql> SELECT JSON_OBJECTAGG(c, i) FROM t;
+----------------------+
| JSON_OBJECTAGG(c, i) |
+----------------------+
| {"key": 4} |
+----------------------+
1 row in set (0.00 sec)
```

The key chosen from the last query is nondeterministic. If the query does not use GROUP BY (which usually imposes its own ordering regardless) and you prefer a particular key ordering, you can invoke JSON\_OBJECTAGG() as a window function by including an OVER clause with an ORDER BY specification to impose a particular order on frame rows. The following examples show what happens with and without ORDER BY for a few different frame specifications.

Without ORDER BY, the frame is the entire partition:

```
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER () AS json_object FROM t;
+-------------+
| json_object |
+-------------+
| {"key": 4} |
| {"key": 4} |
| {"key": 4} |
+-------------+
```

With ORDER BY, where the frame is the default of RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (in both ascending and descending order):

```
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER (ORDER BY i) AS json_object FROM t;
+-------------+
| json_object |
```

```
+-------------+
| {"key": 3} |
| {"key": 4} |
| {"key": 5} |
+-------------+
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER (ORDER BY i DESC) AS json_object FROM t;
+-------------+
| json_object |
+-------------+
| {"key": 5} |
| {"key": 4} |
| {"key": 3} |
+-------------+
```

With ORDER BY and an explicit frame of the entire partition:

```
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER (ORDER BY i
 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
 AS json_object
 FROM t;
+-------------+
| json_object |
+-------------+
| {"key": 5} |
| {"key": 5} |
| {"key": 5} |
+-------------+
```

To return a particular key value (such as the smallest or largest), include a LIMIT clause in the appropriate query. For example:

```
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER (ORDER BY i) AS json_object FROM t LIMIT 1;
+-------------+
| json_object |
+-------------+
| {"key": 3} |
+-------------+
mysql> SELECT JSON_OBJECTAGG(c, i)
 OVER (ORDER BY i DESC) AS json_object FROM t LIMIT 1;
+-------------+
| json_object |
+-------------+
| {"key": 5} |
+-------------+
```

See Normalization, Merging, and Autowrapping of JSON Values, for additional information and examples.

<span id="page-189-0"></span>• [MAX\(\[DISTINCT\]](#page-189-0) expr) [over\_clause]

Returns the maximum value of expr. [MAX\(\)](#page-189-0) may take a string argument; in such cases, it returns the maximum string value. See Section 10.3.1, "How MySQL Uses Indexes". The DISTINCT keyword can be used to find the maximum of the distinct values of expr, however, this produces the same result as omitting DISTINCT.

If there are no matching rows, or if expr is NULL, [MAX\(\)](#page-189-0) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax"; it cannot be used with DISTINCT.

```
mysql> SELECT student_name, MIN(test_score), MAX(test_score)
 FROM student
```

```
 GROUP BY student_name;
```

For [MAX\(\)](#page-189-0), MySQL currently compares ENUM and SET columns by their string value rather than by the string's relative position in the set. This differs from how ORDER BY compares them.

<span id="page-190-0"></span>• [MIN\(\[DISTINCT\]](#page-190-0) expr) [over\_clause]

Returns the minimum value of expr. [MIN\(\)](#page-190-0) may take a string argument; in such cases, it returns the minimum string value. See Section 10.3.1, "How MySQL Uses Indexes". The DISTINCT keyword can be used to find the minimum of the distinct values of expr, however, this produces the same result as omitting DISTINCT.

If there are no matching rows, or if expr is NULL, [MIN\(\)](#page-190-0) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax"; it cannot be used with DISTINCT.

```
mysql> SELECT student_name, MIN(test_score), MAX(test_score)
 FROM student
 GROUP BY student_name;
```

For [MIN\(\)](#page-190-0), MySQL currently compares ENUM and SET columns by their string value rather than by the string's relative position in the set. This differs from how ORDER BY compares them.

<span id="page-190-1"></span>• STD(expr) [[over\\_clause](#page-190-1)]

Returns the population standard deviation of expr. [STD\(\)](#page-190-1) is a synonym for the standard SQL function [STDDEV\\_POP\(\)](#page-190-3), provided as a MySQL extension.

If there are no matching rows, or if expr is NULL, [STD\(\)](#page-190-1) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-190-2"></span>• STDDEV(expr) [[over\\_clause](#page-190-2)]

Returns the population standard deviation of expr. [STDDEV\(\)](#page-190-2) is a synonym for the standard SQL function [STDDEV\\_POP\(\)](#page-190-3), provided for compatibility with Oracle.

If there are no matching rows, or if expr is NULL, [STDDEV\(\)](#page-190-2) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-190-3"></span>• [STDDEV\\_POP\(](#page-190-3)expr) [over\_clause]

Returns the population standard deviation of expr (the square root of [VAR\\_POP\(\)](#page-191-1)). You can also use [STD\(\)](#page-190-1) or [STDDEV\(\)](#page-190-2), which are equivalent but not standard SQL.

If there are no matching rows, or if expr is NULL, [STDDEV\\_POP\(\)](#page-190-3) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-190-4"></span>• [STDDEV\\_SAMP\(](#page-190-4)expr) [over\_clause]

Returns the sample standard deviation of expr (the square root of [VAR\\_SAMP\(\)](#page-191-2).

If there are no matching rows, or if expr is NULL, [STDDEV\\_SAMP\(\)](#page-190-4) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-191-0"></span>• [SUM\(\[DISTINCT\]](#page-191-0) expr) [over\_clause]

Returns the sum of expr. If the return set has no rows, [SUM\(\)](#page-191-0) returns NULL. The DISTINCT keyword can be used to sum only the distinct values of expr.

If there are no matching rows, or if expr is NULL, [SUM\(\)](#page-191-0) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax"; it cannot be used with DISTINCT.

<span id="page-191-1"></span>• VAR\_POP(expr) [[over\\_clause](#page-191-1)]

Returns the population standard variance of expr. It considers rows as the whole population, not as a sample, so it has the number of rows as the denominator. You can also use [VARIANCE\(\)](#page-191-3), which is equivalent but is not standard SQL.

If there are no matching rows, or if expr is NULL, [VAR\\_POP\(\)](#page-191-1) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-191-2"></span>• VAR\_SAMP(expr) [[over\\_clause](#page-191-2)]

Returns the sample variance of expr. That is, the denominator is the number of rows minus one.

If there are no matching rows, or if expr is NULL, [VAR\\_SAMP\(\)](#page-191-2) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".

<span id="page-191-3"></span>• VARIANCE(expr) [[over\\_clause](#page-191-3)]

Returns the population standard variance of expr. [VARIANCE\(\)](#page-191-3) is a synonym for the standard SQL function [VAR\\_POP\(\)](#page-191-1), provided as a MySQL extension.

If there are no matching rows, or if expr is NULL, [VARIANCE\(\)](#page-191-3) returns NULL.

This function executes as a window function if over\_clause is present. over\_clause is as described in Section 14.20.2, "Window Function Concepts and Syntax".