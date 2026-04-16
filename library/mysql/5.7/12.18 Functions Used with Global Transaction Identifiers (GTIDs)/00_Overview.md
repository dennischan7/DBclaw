---
source: MySQL 5.7 Reference
title: 00_Overview
---

The functions described in this section are used with GTID-based replication. It is important to keep in mind that all of these functions take string representations of GTID sets as arguments. As such, the GTID sets must always be quoted when used with them. See GTID Sets for more information.

The union of two GTID sets is simply their representations as strings, joined together with an interposed comma. In other words, you can define a very simple function for obtaining the union of two GTID sets, similar to that created here:

```
CREATE FUNCTION GTID_UNION(g1 TEXT, g2 TEXT)
 RETURNS TEXT DETERMINISTIC
 RETURN CONCAT(g1,',',g2);
```

For more information about GTIDs and how these GTID functions are used in practice, see Section 16.1.3, "Replication with Global Transaction Identifiers".

### **Table 12.24 GTID Functions**

| Name                                | Description                                                             |
|-------------------------------------|-------------------------------------------------------------------------|
| GTID_SUBSET()                       | Return true if all GTIDs in subset are also in set;<br>otherwise false. |
| GTID_SUBTRACT()                     | Return all GTIDs in set that are not in subset.                         |
| WAIT_FOR_EXECUTED_GTID_SET()        | Wait until the given GTIDs have executed on the<br>replica.             |
| WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS() | Use WAIT_FOR_EXECUTED_GTID_SET().                                       |

<span id="page-193-0"></span>• [GTID\\_SUBSET\(](#page-193-0)set1,set2)

Given two sets of global transaction identifiers set1 and set2, returns true if all GTIDs in set1 are also in set2. Returns false otherwise.

The GTID sets used with this function are represented as strings, as shown in the following examples:

```
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 1
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23-25',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23-25',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 1
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 0
1 row in set (0.00 sec)
```

<span id="page-194-0"></span>• [GTID\\_SUBTRACT\(](#page-194-0)set1,set2)

Given two sets of global transaction identifiers set1 and set2, returns only those GTIDs from set1 that are not in set2.

All GTID sets used with this function are represented as strings and must be quoted, as shown in these examples:

```
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:22-57
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:26-57
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:23-24')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:23-24'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:21-22:25-57
1 row in set (0.01 sec)
```

Subtracting a GTID set from itself produces an empty set, as shown here:

```
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 
1 row in set (0.00 sec)
```

<span id="page-195-0"></span>• [WAIT\\_FOR\\_EXECUTED\\_GTID\\_SET\(](#page-195-0)gtid\_set[, timeout])

Wait until the server has applied all of the transactions whose global transaction identifiers are contained in gtid\_set; that is, until the condition GTID\_SUBSET(gtid\_subset, @@GLOBAL.gtid\_executed) holds. See Section 16.1.3.1, "GTID Format and Storage" for a definition of GTID sets.

If a timeout is specified, and timeout seconds elapse before all of the transactions in the GTID set have been applied, the function stops waiting. timeout is optional, and the default timeout is 0 seconds, in which case the function always waits until all of the transactions in the GTID set have been applied. timeout must be greater than or equal to 0; as of MySQL 5.7.18, when running in strict SQL mode, a negative timeout value is immediately rejected with an error; otherwise the function returns NULL, and raises a warning.

WAIT\_FOR\_EXECUTED\_GTID\_SET() monitors all the GTIDs that are applied on the server, including transactions that arrive from all replication channels and user clients. It does not take into account whether replication channels have been started or stopped.

For more information, see Section 16.1.3, "Replication with Global Transaction Identifiers".

GTID sets used with this function are represented as strings and so must be quoted as shown in the following example:

```
mysql> SELECT WAIT_FOR_EXECUTED_GTID_SET('3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5');
 -> 0
```

For a syntax description for GTID sets, see Section 16.1.3.1, "GTID Format and Storage".

For WAIT\_FOR\_EXECUTED\_GTID\_SET(), the return value is the state of the query, where 0 represents success, and 1 represents timeout. Any other failures generate an error.

gtid\_mode cannot be changed to OFF while any client is using this function to wait for GTIDs to be applied.

<span id="page-195-1"></span>• [WAIT\\_UNTIL\\_SQL\\_THREAD\\_AFTER\\_GTIDS\(](#page-195-1)gtid\_set[, timeout][,channel])

WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() is similar to WAIT\_FOR\_EXECUTED\_GTID\_SET() in that it waits until all of the transactions whose global transaction identifiers are contained in gtid\_set have been applied, or until timeout seconds have elapsed, whichever occurs first. However, WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() applies to a specific replication channel, and stops only after the transactions have been applied on the specified channel, for which the applier must be running. In contrast, WAIT\_FOR\_EXECUTED\_GTID\_SET() stops after the transactions have been applied, regardless of where they were applied (on any replication channel or any user client), and whether or not any replication channels are running.

timeout must be greater than or equal to 0; as of MySQL 5.7.18, when running in strict SQL mode, a negative timeout value is immediately rejected with an error ([ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_wrong_arguments)); otherwise WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() returns NULL, and raises a warning.

The channel option names which replication channel the function applies to. If no channel is named and no channels other than the default replication channel exist, the function applies to the default replication channel. If multiple replication channels exist, you must specify a channel as otherwise it is not known which replication channel the function applies to. See Section 16.2.2, "Replication Channels" for more information on replication channels.

![](_page_195_Picture_15.jpeg)

## **Note**

Because WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() applies to a specific replication channel, if an expected transaction arrives on a different replication channel or from a user client, for example in a failover or manual recovery situation, the function can hang indefinitely if no timeout is set. Use WAIT\_FOR\_EXECUTED\_GTID\_SET() instead to ensure correct handling of transactions in these situations.

GTID sets used with WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() are represented as strings and must be quoted in the same way as for WAIT\_FOR\_EXECUTED\_GTID\_SET(). For WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS(), the return value for the function is an arbitrary positive number. If GTID-based replication is not active (that is, if the value of the gtid\_mode variable is OFF), then this value is undefined and WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() returns NULL. If the replica is not running then the function also returns NULL.

gtid\_mode cannot be changed to OFF while any client is using this function to wait for GTIDs to be applied.

# <span id="page-196-1"></span>**12.19 Aggregate Functions**

Aggregate functions operate on sets of values. They are often used with a GROUP BY clause to group values into subsets.

## <span id="page-196-0"></span>**12.19.1 Aggregate Function Descriptions**

This section describes aggregate functions that operate on sets of values. They are often used with a GROUP BY clause to group values into subsets.

**Table 12.25 Aggregate Functions**

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
| VAR_SAMP()       | Return the sample variance                       |
| VARIANCE()       | Return the population standard variance          |

Unless otherwise stated, aggregate functions ignore NULL values.

If you use an aggregate function in a statement containing no GROUP BY clause, it is equivalent to grouping on all rows. For more information, see Section 12.19.3, "MySQL Handling of GROUP BY". For numeric arguments, the variance and standard deviation functions return a DOUBLE value. The SUM() and [AVG\(\)](#page-197-3) functions return a DECIMAL value for exact-value arguments (integer or DECIMAL), and a DOUBLE value for approximate-value arguments (FLOAT or DOUBLE).

The SUM() and [AVG\(\)](#page-197-3) aggregate functions do not work with temporal values. (They convert the values to numbers, losing everything after the first nonnumeric character.) To work around this problem, convert to numeric units, perform the aggregate operation, and convert back to a temporal value. Examples:

```
SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_col))) FROM tbl_name;
SELECT FROM_DAYS(SUM(TO_DAYS(date_col))) FROM tbl_name;
```

Functions such as SUM() or [AVG\(\)](#page-197-3) that expect a numeric argument cast the argument to a number if necessary. For SET or ENUM values, the cast operation causes the underlying numeric value to be used.

The [BIT\\_AND\(\)](#page-197-0), [BIT\\_OR\(\)](#page-197-1), and [BIT\\_XOR\(\)](#page-197-2) aggregate functions perform bit operations. They require BIGINT (64-bit integer) arguments and return BIGINT values. Arguments of other types are converted to BIGINT and truncation might occur. For information about a change in MySQL 8.0 that permits bit operations to take binary string type arguments (BINARY, VARBINARY, and the BLOB types), see [Section 12.12, "Bit Functions and Operators".](#page-105-3)

<span id="page-197-3"></span>• [AVG\(\[DISTINCT\]](#page-197-3) expr)

Returns the average value of expr. The DISTINCT option can be used to return the average of the distinct values of expr.

If there are no matching rows, [AVG\(\)](#page-197-3) returns NULL.

```
mysql> SELECT student_name, AVG(test_score)
 FROM student
 GROUP BY student_name;
```

<span id="page-197-0"></span>• [BIT\\_AND\(](#page-197-0)expr)

Returns the bitwise AND of all bits in expr. The calculation is performed with 64-bit (BIGINT) precision.

If there are no matching rows, [BIT\\_AND\(\)](#page-197-0) returns a neutral value (all bits set to 1).

<span id="page-197-1"></span>• [BIT\\_OR\(](#page-197-1)expr)

Returns the bitwise OR of all bits in expr. The calculation is performed with 64-bit (BIGINT) precision.

If there are no matching rows, [BIT\\_OR\(\)](#page-197-1) returns a neutral value (all bits set to 0).

<span id="page-197-2"></span>• [BIT\\_XOR\(](#page-197-2)expr)

Returns the bitwise [XOR](#page-0-1) of all bits in expr. The calculation is performed with 64-bit (BIGINT) precision.

If there are no matching rows, [BIT\\_XOR\(\)](#page-197-2) returns a neutral value (all bits set to 0).

<span id="page-197-4"></span>• [COUNT\(](#page-197-4)expr)

Returns a count of the number of non-NULL values of expr in the rows retrieved by a SELECT statement. The result is a BIGINT value.

If there are no matching rows, [COUNT\(\)](#page-197-4) returns 0.

```
mysql> SELECT student.student_name,COUNT(*)
 FROM student,course
 WHERE student.student_id=course.student_id
```

```
 GROUP BY student_name;
```

[COUNT\(\\*\)](#page-197-4) is somewhat different in that it returns a count of the number of rows retrieved, whether or not they contain NULL values.

For transactional storage engines such as InnoDB, storing an exact row count is problematic. Multiple transactions may be occurring at the same time, each of which may affect the count.

InnoDB does not keep an internal count of rows in a table because concurrent transactions might "see" different numbers of rows at the same time. Consequently, SELECT COUNT(\*) statements only count rows visible to the current transaction.

Prior to MySQL 5.7.18, InnoDB processes SELECT COUNT(\*) statements by scanning the clustered index. As of MySQL 5.7.18, InnoDB processes SELECT COUNT(\*) statements by traversing the smallest available secondary index unless an index or optimizer hint directs the optimizer to use a different index. If a secondary index is not present, the clustered index is scanned.

Processing SELECT COUNT(\*) statements takes some time if index records are not entirely in the buffer pool. For a faster count, create a counter table and let your application update it according to the inserts and deletes it does. However, this method may not scale well in situations where thousands of concurrent transactions are initiating updates to the same counter table. If an approximate row count is sufficient, use SHOW TABLE STATUS.

InnoDB handles SELECT COUNT(\*) and SELECT COUNT(1) operations in the same way. There is no performance difference.

For MyISAM tables, [COUNT\(\\*\)](#page-197-4) is optimized to return very quickly if the SELECT retrieves from one table, no other columns are retrieved, and there is no WHERE clause. For example:

```
mysql> SELECT COUNT(*) FROM student;
```

This optimization only applies to MyISAM tables, because an exact row count is stored for this storage engine and can be accessed very quickly. COUNT(1) is only subject to the same optimization if the first column is defined as NOT NULL.

<span id="page-198-0"></span>• [COUNT\(DISTINCT](#page-197-4) expr,[expr...])

Returns a count of the number of rows with different non-NULL expr values.

If there are no matching rows, [COUNT\(DISTINCT\)](#page-197-4) returns 0.

```
mysql> SELECT COUNT(DISTINCT results) FROM student;
```

In MySQL, you can obtain the number of distinct expression combinations that do not contain NULL by giving a list of expressions. In standard SQL, you would have to do a concatenation of all expressions inside [COUNT\(DISTINCT ...\)](#page-197-4).

<span id="page-198-1"></span>• [GROUP\\_CONCAT\(](#page-198-1)expr)

This function returns a string result with the concatenated non-NULL values from a group. It returns NULL if there are no non-NULL values. The full syntax is as follows:

```
GROUP_CONCAT([DISTINCT] expr [,expr ...]
 [ORDER BY {unsigned_integer | col_name | expr}
 [ASC | DESC] [,col_name ...]]
 [SEPARATOR str_val])
```

```
mysql> SELECT student_name,
 GROUP_CONCAT(test_score)
 FROM student
```

```
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

The return value is a nonbinary or binary string, depending on whether the arguments are nonbinary or binary strings. The result type is TEXT or BLOB unless group\_concat\_max\_len is less than or equal to 512, in which case the result type is VARCHAR or VARBINARY.

If [GROUP\\_CONCAT\(\)](#page-198-1) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

See also [CONCAT\(\)](#page-39-0) and [CONCAT\\_WS\(\)](#page-40-0): [Section 12.8, "String Functions and Operators"](#page-36-0).

<span id="page-199-0"></span>• [JSON\\_ARRAYAGG\(](#page-199-0)col\_or\_expr)

Aggregates a result set as a single JSON array whose elements consist of the rows. The order of elements in this array is undefined. The function acts on a column or an expression that evaluates to a single value. Returns NULL if the result contains no rows, or in the event of an error.

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

Added in MySQL 5.7.22.

<span id="page-0-0"></span>• [JSON\\_OBJECTAGG\(](#page-0-0)key, value)

Takes two column names or expressions as arguments, the first of these being used as a key and the second as a value, and returns a JSON object containing key-value pairs. Returns NULL if the result contains no rows, or in the event of an error. An error occurs if any key name is NULL or the number of arguments is not equal to 2.

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

Consider the following:

```
mysql> CREATE TABLE t(c VARCHAR(10), i INT);
Query OK, 0 rows affected (0.33 sec)
mysql> INSERT INTO t VALUES ('key', 3), ('key', 4), ('key', 5);
Query OK, 3 rows affected (0.10 sec)
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
```

```
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

See Normalization, Merging, and Autowrapping of JSON Values, for additional information and examples.

Added in MySQL 5.7.22.

<span id="page-1-0"></span>• [MAX\(\[DISTINCT\]](#page-1-0) expr)

Returns the maximum value of expr. [MAX\(\)](#page-1-0) may take a string argument; in such cases, it returns the maximum string value. See Section 8.3.1, "How MySQL Uses Indexes". The DISTINCT keyword can be used to find the maximum of the distinct values of expr, however, this produces the same result as omitting DISTINCT.

If there are no matching rows, [MAX\(\)](#page-1-0) returns NULL.

```
mysql> SELECT student_name, MIN(test_score), MAX(test_score)
 FROM student
 GROUP BY student_name;
```

For [MAX\(\)](#page-1-0), MySQL currently compares ENUM and SET columns by their string value rather than by the string's relative position in the set. This differs from how ORDER BY compares them.

<span id="page-1-1"></span>• [MIN\(\[DISTINCT\]](#page-1-1) expr)

Returns the minimum value of expr. [MIN\(\)](#page-1-1) may take a string argument; in such cases, it returns the minimum string value. See Section 8.3.1, "How MySQL Uses Indexes". The DISTINCT keyword can be used to find the minimum of the distinct values of expr, however, this produces the same result as omitting DISTINCT.

If there are no matching rows, [MIN\(\)](#page-1-1) returns NULL.

```
mysql> SELECT student_name, MIN(test_score), MAX(test_score)
 FROM student
 GROUP BY student_name;
```

For [MIN\(\)](#page-1-1), MySQL currently compares ENUM and SET columns by their string value rather than by the string's relative position in the set. This differs from how ORDER BY compares them.

<span id="page-1-2"></span>• [STD\(](#page-1-2)expr)

Returns the population standard deviation of expr. [STD\(\)](#page-1-2) is a synonym for the standard SQL function [STDDEV\\_POP\(\)](#page-2-0), provided as a MySQL extension.

If there are no matching rows, [STD\(\)](#page-1-2) returns NULL.

<span id="page-2-1"></span>• [STDDEV\(](#page-2-1)expr)

Returns the population standard deviation of expr. [STDDEV\(\)](#page-2-1) is a synonym for the standard SQL function [STDDEV\\_POP\(\)](#page-2-0), provided for compatibility with Oracle.

If there are no matching rows, [STDDEV\(\)](#page-2-1) returns NULL.

<span id="page-2-0"></span>• [STDDEV\\_POP\(](#page-2-0)expr)

Returns the population standard deviation of expr (the square root of [VAR\\_POP\(\)](#page-2-2)). You can also use [STD\(\)](#page-1-2) or [STDDEV\(\)](#page-2-1), which are equivalent but not standard SQL.

If there are no matching rows, [STDDEV\\_POP\(\)](#page-2-0) returns NULL.

<span id="page-2-3"></span>• [STDDEV\\_SAMP\(](#page-2-3)expr)

Returns the sample standard deviation of expr (the square root of [VAR\\_SAMP\(\)](#page-2-4).

If there are no matching rows, [STDDEV\\_SAMP\(\)](#page-2-3) returns NULL.

<span id="page-2-5"></span>• [SUM\(\[DISTINCT\]](#page-2-5) expr)

Returns the sum of expr. If the return set has no rows, [SUM\(\)](#page-2-5) returns NULL. The DISTINCT keyword can be used to sum only the distinct values of expr.

If there are no matching rows, [SUM\(\)](#page-2-5) returns NULL.

<span id="page-2-2"></span>• [VAR\\_POP\(](#page-2-2)expr)

Returns the population standard variance of expr. It considers rows as the whole population, not as a sample, so it has the number of rows as the denominator. You can also use [VARIANCE\(\)](#page-2-6), which is equivalent but is not standard SQL.

If there are no matching rows, [VAR\\_POP\(\)](#page-2-2) returns NULL.

<span id="page-2-4"></span>• [VAR\\_SAMP\(](#page-2-4)expr)

Returns the sample variance of expr. That is, the denominator is the number of rows minus one.

If there are no matching rows, [VAR\\_SAMP\(\)](#page-2-4) returns NULL.

<span id="page-2-6"></span>• [VARIANCE\(](#page-2-6)expr)

Returns the population standard variance of expr. [VARIANCE\(\)](#page-2-6) is a synonym for the standard SQL function [VAR\\_POP\(\)](#page-2-2), provided as a MySQL extension.

If there are no matching rows, [VARIANCE\(\)](#page-2-6) returns NULL.

## <span id="page-2-7"></span>**12.19.2 GROUP BY Modifiers**

The GROUP BY clause permits a WITH ROLLUP modifier that causes summary output to include extra rows that represent higher-level (that is, super-aggregate) summary operations. ROLLUP thus enables you to answer questions at multiple levels of analysis with a single query. For example, ROLLUP can be used to provide support for OLAP (Online Analytical Processing) operations.

Suppose that a sales table has year, country, product, and profit columns for recording sales profitability:

```
CREATE TABLE sales
(
 year INT,
 country VARCHAR(20),
 product VARCHAR(32),
```

```
 profit INT
);
```

To summarize table contents per year, use a simple GROUP BY like this:

```
mysql> SELECT year, SUM(profit) AS profit
 FROM sales
 GROUP BY year;
+------+--------+
| year | profit |
+------+--------+
| 2000 | 4525 |
| 2001 | 3010 |
+------+--------+
```

The output shows the total (aggregate) profit for each year. To also determine the total profit summed over all years, you must add up the individual values yourself or run an additional query. Or you can use ROLLUP, which provides both levels of analysis with a single query. Adding a WITH ROLLUP modifier to the GROUP BY clause causes the query to produce another (super-aggregate) row that shows the grand total over all year values:

```
mysql> SELECT year, SUM(profit) AS profit
 FROM sales
 GROUP BY year WITH ROLLUP;
+------+--------+
| year | profit |
+------+--------+
| 2000 | 4525 |
| 2001 | 3010 |
| NULL | 7535 |
+------+--------+
```

The NULL value in the year column identifies the grand total super-aggregate line.

ROLLUP has a more complex effect when there are multiple GROUP BY columns. In this case, each time there is a change in value in any but the last grouping column, the query produces an extra superaggregate summary row.

For example, without ROLLUP, a summary of the sales table based on year, country, and product might look like this, where the output indicates summary values only at the year/country/product level of analysis:

```
mysql> SELECT year, country, product, SUM(profit) AS profit
 FROM sales
 GROUP BY year, country, product;
+------+---------+------------+--------+
| year | country | product | profit |
+------+---------+------------+--------+
| 2000 | Finland | Computer | 1500 |
| 2000 | Finland | Phone | 100 |
| 2000 | India | Calculator | 150 |
| 2000 | India | Computer | 1200 |
| 2000 | USA | Calculator | 75 |
| 2000 | USA | Computer | 1500 |
| 2001 | Finland | Phone | 10 |
| 2001 | USA | Calculator | 50 |
| 2001 | USA | Computer | 2700 |
| 2001 | USA | TV | 250 |
+------+---------+------------+--------+
```

With ROLLUP added, the query produces several extra rows:

```
mysql> SELECT year, country, product, SUM(profit) AS profit
 FROM sales
 GROUP BY year, country, product WITH ROLLUP;
+------+---------+------------+--------+
| year | country | product | profit |
```

|             |                        | +++++                     |  |      |
|-------------|------------------------|---------------------------|--|------|
|             |                        | 2000   Finland   Computer |  | 1500 |
|             | 2000   Finland   Phone |                           |  | 100  |
|             | 2000   Finland   NULL  |                           |  | 1600 |
|             | 2000   India           | Calculator                |  | 150  |
|             | 2000   India           | Computer                  |  | 1200 |
|             | 2000   India           | NULL                      |  | 1350 |
| 2000   USA  |                        | Calculator                |  | 75   |
| 2000   USA  |                        | Computer                  |  | 1500 |
| 2000   USA  |                        | NULL                      |  | 1575 |
| 2000   NULL |                        | NULL                      |  | 4525 |
|             | 2001   Finland   Phone |                           |  | 10   |
|             | 2001   Finland   NULL  |                           |  | 10   |
| 2001   USA  |                        | Calculator                |  | 50   |
| 2001   USA  |                        | Computer                  |  | 2700 |
| 2001   USA  |                        | TV                        |  | 250  |
| 2001   USA  |                        | NULL                      |  | 3000 |
| 2001   NULL |                        | NULL                      |  | 3010 |
| NULL   NULL |                        | NULL                      |  | 7535 |
|             |                        | +++++                     |  |      |

Now the output includes summary information at four levels of analysis, not just one:

- Following each set of product rows for a given year and country, an extra super-aggregate summary row appears showing the total for all products. These rows have the product column set to NULL.
- Following each set of rows for a given year, an extra super-aggregate summary row appears showing the total for all countries and products. These rows have the country and products columns set to NULL.
- Finally, following all other rows, an extra super-aggregate summary row appears showing the grand total for all years, countries, and products. This row has the year, country, and products columns set to NULL.

The NULL indicators in each super-aggregate row are produced when the row is sent to the client. The server looks at the columns named in the GROUP BY clause following the leftmost one that has changed value. For any column in the result set with a name that matches any of those names, its value is set to NULL. (If you specify grouping columns by column position, the server identifies which columns to set to NULL by position.)

Because the NULL values in the super-aggregate rows are placed into the result set at such a late stage in query processing, you can test them as NULL values only in the select list or HAVING clause. You cannot test them as NULL values in join conditions or the WHERE clause to determine which rows to select. For example, you cannot add WHERE product IS NULL to the query to eliminate from the output all but the super-aggregate rows.

The NULL values do appear as NULL on the client side and can be tested as such using any MySQL client programming interface. However, at this point, you cannot distinguish whether a NULL represents a regular grouped value or a super-aggregate value. In MySQL 8.0, you can use the [GROUPING\(\)](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.md#function_grouping) function to test the distinction.

## **Other Considerations When using ROLLUP**

The following discussion lists some behaviors specific to the MySQL implementation of ROLLUP.

When you use ROLLUP, you cannot also use an ORDER BY clause to sort the results. In other words, ROLLUP and ORDER BY are mutually exclusive in MySQL. However, you still have some control over sort order. To work around the restriction that prevents using ROLLUP with ORDER BY and achieve a specific sort order of grouped results, generate the grouped result set as a derived table and apply ORDER BY to it. For example:

```
mysql> SELECT * FROM
 (SELECT year, SUM(profit) AS profit
```

```
 FROM sales GROUP BY year WITH ROLLUP) AS dt
 ORDER BY year DESC;
+------+--------+
| year | profit |
+------+--------+
| 2001 | 3010 |
| 2000 | 4525 |
| NULL | 7535 |
+------+--------+
```

In this case, the super-aggregate summary rows sort with the rows from which they are calculated, and their placement depends on sort order (at the beginning for ascending sort, at the end for descending sort).

LIMIT can be used to restrict the number of rows returned to the client. LIMIT is applied after ROLLUP, so the limit applies against the extra rows added by ROLLUP. For example:

```
mysql> SELECT year, country, product, SUM(profit) AS profit
 FROM sales
 GROUP BY year, country, product WITH ROLLUP
 LIMIT 5;
+------+---------+------------+--------+
| year | country | product | profit |
+------+---------+------------+--------+
| 2000 | Finland | Computer | 1500 |
| 2000 | Finland | Phone | 100 |
| 2000 | Finland | NULL | 1600 |
| 2000 | India | Calculator | 150 |
| 2000 | India | Computer | 1200 |
+------+---------+------------+--------+
```

Using LIMIT with ROLLUP may produce results that are more difficult to interpret, because there is less context for understanding the super-aggregate rows.

A MySQL extension permits a column that does not appear in the GROUP BY list to be named in the select list. (For information about nonaggregated columns and GROUP BY, see [Section 12.19.3,](#page-6-0) ["MySQL Handling of GROUP BY".](#page-6-0)) In this case, the server is free to choose any value from this nonaggregated column in summary rows, and this includes the extra rows added by WITH ROLLUP. For example, in the following query, country is a nonaggregated column that does not appear in the GROUP BY list and values chosen for this column are nondeterministic:

```
mysql> SELECT year, country, SUM(profit) AS profit
 FROM sales
 GROUP BY year WITH ROLLUP;
+------+---------+--------+
| year | country | profit |
+------+---------+--------+
| 2000 | India | 4525 |
| 2001 | USA | 3010 |
| NULL | USA | 7535 |
+------+---------+--------+
```

This behavior is permitted when the ONLY\_FULL\_GROUP\_BY SQL mode is not enabled. If that mode is enabled, the server rejects the query as illegal because country is not listed in the GROUP BY clause. With ONLY\_FULL\_GROUP\_BY enabled, you can still execute the query by using the [ANY\\_VALUE\(\)](#page-13-0) function for nondeterministic-value columns:

```
mysql> SELECT year, ANY_VALUE(country) AS country, SUM(profit) AS profit
 FROM sales
 GROUP BY year WITH ROLLUP;
+------+---------+--------+
| year | country | profit |
+------+---------+--------+
| 2000 | India | 4525 |
| 2001 | USA | 3010 |
| NULL | USA | 7535 |
+------+---------+--------+
```

## <span id="page-6-0"></span>**12.19.3 MySQL Handling of GROUP BY**

SQL-92 and earlier does not permit queries for which the select list, HAVING condition, or ORDER BY list refer to nonaggregated columns that are not named in the GROUP BY clause. For example, this query is illegal in standard SQL-92 because the nonaggregated name column in the select list does not appear in the GROUP BY:

```
SELECT o.custid, c.name, MAX(o.payment)
 FROM orders AS o, customers AS c
 WHERE o.custid = c.custid
 GROUP BY o.custid;
```

For the query to be legal in SQL-92, the name column must be omitted from the select list or named in the GROUP BY clause.

SQL:1999 and later permits such nonaggregates per optional feature T301 if they are functionally dependent on GROUP BY columns: If such a relationship exists between name and custid, the query is legal. This would be the case, for example, were custid a primary key of customers.

MySQL 5.7.5 and later implements detection of functional dependence. If the ONLY\_FULL\_GROUP\_BY SQL mode is enabled (which it is by default), MySQL rejects queries for which the select list, HAVING condition, or ORDER BY list refer to nonaggregated columns that are neither named in the GROUP BY clause nor are functionally dependent on them. (Before 5.7.5, MySQL does not detect functional dependency and ONLY\_FULL\_GROUP\_BY is not enabled by default.)

MySQL 5.7.5 and later also permits a nonaggregate column not named in a GROUP BY clause when ONLY\_FULL\_GROUP\_BY SQL mode is enabled, provided that this column is limited to a single value, as shown in the following example:

```
mysql> CREATE TABLE mytable (
 -> id INT UNSIGNED NOT NULL PRIMARY KEY,
 -> a VARCHAR(10),
 -> b INT
 -> );
mysql> INSERT INTO mytable
 -> VALUES (1, 'abc', 1000),
 -> (2, 'abc', 2000),
 -> (3, 'def', 4000);
mysql> SET SESSION sql_mode = sys.list_add(@@session.sql_mode, 'ONLY_FULL_GROUP_BY');
mysql> SELECT a, SUM(b) FROM mytable WHERE a = 'abc';
+------+--------+
| a | SUM(b) |
+------+--------+
| abc | 3000 |
+------+--------+
```

It is also possible to have more than one nonaggregate column in the [SELECT](#page-180-0) list when employing ONLY\_FULL\_GROUP\_BY. In this case, every such column must be limited to a single value, and all such limiting conditions must be joined by logical AND, as shown here:

```
mysql> DROP TABLE IF EXISTS mytable;
mysql> CREATE TABLE mytable (
 -> id INT UNSIGNED NOT NULL PRIMARY KEY,
 -> a VARCHAR(10),
 -> b VARCHAR(10),
 -> c INT
 -> );
mysql> INSERT INTO mytable
 -> VALUES (1, 'abc', 'qrs', 1000),
 -> (2, 'abc', 'tuv', 2000),
```

```
 -> (3, 'def', 'qrs', 4000),
 -> (4, 'def', 'tuv', 8000),
 -> (5, 'abc', 'qrs', 16000),
 -> (6, 'def', 'tuv', 32000);
mysql> SELECT @@session.sql_mode;
+---------------------------------------------------------------+
| @@session.sql_mode |
+---------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+---------------------------------------------------------------+
mysql> SELECT a, b, SUM(c) FROM mytable
 -> WHERE a = 'abc' AND b = 'qrs';
+------+------+--------+
| a | b | SUM(c) |
+------+------+--------+
| abc | qrs | 17000 |
+------+------+--------+
```

If ONLY\_FULL\_GROUP\_BY is disabled, a MySQL extension to the standard SQL use of GROUP BY permits the select list, HAVING condition, or ORDER BY list to refer to nonaggregated columns even if the columns are not functionally dependent on GROUP BY columns. This causes MySQL to accept the preceding query. In this case, the server is free to choose any value from each group, so unless they are the same, the values chosen are nondeterministic, which is probably not what you want. Furthermore, the selection of values from each group cannot be influenced by adding an ORDER BY clause. Result set sorting occurs after values have been chosen, and ORDER BY does not affect which value within each group the server chooses. Disabling ONLY\_FULL\_GROUP\_BY is useful primarily when you know that, due to some property of the data, all values in each nonaggregated column not named in the GROUP BY are the same for each group.

You can achieve the same effect without disabling ONLY\_FULL\_GROUP\_BY by using [ANY\\_VALUE\(\)](#page-13-0) to refer to the nonaggregated column.

The following discussion demonstrates functional dependence, the error message MySQL produces when functional dependence is absent, and ways of causing MySQL to accept a query in the absence of functional dependence.

This query might be invalid with ONLY\_FULL\_GROUP\_BY enabled because the nonaggregated address column in the select list is not named in the GROUP BY clause:

```
SELECT name, address, MAX(age) FROM t GROUP BY name;
```

The query is valid if name is a primary key of t or is a unique NOT NULL column. In such cases, MySQL recognizes that the selected column is functionally dependent on a grouping column. For example, if name is a primary key, its value determines the value of address because each group has only one value of the primary key and thus only one row. As a result, there is no randomness in the choice of address value in a group and no need to reject the query.

The query is invalid if name is not a primary key of t or a unique NOT NULL column. In this case, no functional dependency can be inferred and an error occurs:

```
mysql> SELECT name, address, MAX(age) FROM t GROUP BY name;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP
BY clause and contains nonaggregated column 'mydb.t.address' which
is not functionally dependent on columns in GROUP BY clause; this
is incompatible with sql_mode=only_full_group_by
```

If you know that, for a given data set, each name value in fact uniquely determines the address value, address is effectively functionally dependent on name. To tell MySQL to accept the query, you can use the [ANY\\_VALUE\(\)](#page-13-0) function:

```
SELECT name, ANY_VALUE(address), MAX(age) FROM t GROUP BY name;
```

Alternatively, disable ONLY\_FULL\_GROUP\_BY.

The preceding example is quite simple, however. In particular, it is unlikely you would group on a single primary key column because every group would contain only one row. For addtional examples demonstrating functional dependence in more complex queries, see [Section 12.19.4, "Detection of](#page-9-0) [Functional Dependence".](#page-9-0)

If a query has aggregate functions and no GROUP BY clause, it cannot have nonaggregated columns in the select list, HAVING condition, or ORDER BY list with ONLY\_FULL\_GROUP\_BY enabled:

```
mysql> SELECT name, MAX(age) FROM t;
ERROR 1140 (42000): In aggregated query without GROUP BY, expression
#1 of SELECT list contains nonaggregated column 'mydb.t.name'; this
is incompatible with sql_mode=only_full_group_by
```

Without GROUP BY, there is a single group and it is nondeterministic which name value to choose for the group. Here, too, [ANY\\_VALUE\(\)](#page-13-0) can be used, if it is immaterial which name value MySQL chooses:

```
SELECT ANY_VALUE(name), MAX(age) FROM t;
```

In MySQL 5.7.5 and later, ONLY\_FULL\_GROUP\_BY also affects handling of queries that use DISTINCT and ORDER BY. Consider the case of a table t with three columns c1, c2, and c3 that contains these rows:

```
c1 c2 c3
1 2 A
3 4 B
1 2 C
```

Suppose that we execute the following query, expecting the results to be ordered by c3:

```
SELECT DISTINCT c1, c2 FROM t ORDER BY c3;
```

To order the result, duplicates must be eliminated first. But to do so, should we keep the first row or the third? This arbitrary choice influences the retained value of c3, which in turn influences ordering and makes it arbitrary as well. To prevent this problem, a query that has DISTINCT and ORDER BY is rejected as invalid if any ORDER BY expression does not satisfy at least one of these conditions:

- The expression is equal to one in the select list
- All columns referenced by the expression and belonging to the query's selected tables are elements of the select list

Another MySQL extension to standard SQL permits references in the HAVING clause to aliased expressions in the select list. For example, the following query returns name values that occur only once in table orders:

```
SELECT name, COUNT(name) FROM orders
 GROUP BY name
 HAVING COUNT(name) = 1;
```

The MySQL extension permits the use of an alias in the HAVING clause for the aggregated column:

```
SELECT name, COUNT(name) AS c FROM orders
 GROUP BY name
 HAVING c = 1;
```

![](_page_8_Picture_18.jpeg)

#### **Note**

Before MySQL 5.7.5, enabling ONLY\_FULL\_GROUP\_BY disables this extension, thus requiring the HAVING clause to be written using unaliased expressions.

Standard SQL permits only column expressions in GROUP BY clauses, so a statement such as this is invalid because FLOOR(value/100) is a noncolumn expression:

```
SELECT id, FLOOR(value/100)
 FROM tbl_name
 GROUP BY id, FLOOR(value/100);
```

MySQL extends standard SQL to permit noncolumn expressions in GROUP BY clauses and considers the preceding statement valid.

Standard SQL also does not permit aliases in GROUP BY clauses. MySQL extends standard SQL to permit aliases, so another way to write the query is as follows:

```
SELECT id, FLOOR(value/100) AS val
 FROM tbl_name
 GROUP BY id, val;
```

The alias val is considered a column expression in the GROUP BY clause.

In the presence of a noncolumn expression in the GROUP BY clause, MySQL recognizes equality between that expression and expressions in the select list. This means that with ONLY\_FULL\_GROUP\_BY SQL mode enabled, the query containing GROUP BY id, FLOOR(value/100) is valid because that same FLOOR() expression occurs in the select list. However, MySQL does not try to recognize functional dependence on GROUP BY noncolumn expressions, so the following query is invalid with ONLY\_FULL\_GROUP\_BY enabled, even though the third selected expression is a simple formula of the id column and the FLOOR() expression in the GROUP BY clause:

```
SELECT id, FLOOR(value/100), id+FLOOR(value/100)
 FROM tbl_name
 GROUP BY id, FLOOR(value/100);
```

A workaround is to use a derived table:

```
SELECT id, F, id+F
 FROM
 (SELECT id, FLOOR(value/100) AS F
 FROM tbl_name
 GROUP BY id, FLOOR(value/100)) AS dt;
```

## <span id="page-9-0"></span>**12.19.4 Detection of Functional Dependence**

The following discussion provides several examples of the ways in which MySQL detects functional dependencies. The examples use this notation:

```
{X} -> {Y}
```

Understand this as "X uniquely determines Y," which also means that Y is functionally dependent on X.

The examples use the world database, which can be downloaded from [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/index-other.md) [index-other.html.](https://dev.mysql.com/doc/index-other.md) You can find details on how to install the database on the same page.

- [Functional Dependencies Derived from Keys](#page-10-0)
- [Functional Dependencies Derived from Multiple-Column Keys and from Equalities](#page-10-1)
- [Functional Dependency Special Cases](#page-10-2)
- [Functional Dependencies and Views](#page-11-0)
- [Combinations of Functional Dependencies](#page-12-0)

## <span id="page-10-0"></span>**Functional Dependencies Derived from Keys**

The following query selects, for each country, a count of spoken languages:

```
SELECT co.Name, COUNT(*)
FROM countrylanguage cl, country co
WHERE cl.CountryCode = co.Code
GROUP BY co.Code;
```

co.Code is a primary key of co, so all columns of co are functionally dependent on it, as expressed using this notation:

```
{co.Code} -> {co.*}
```

Thus, co.name is functionally dependent on GROUP BY columns and the query is valid.

A UNIQUE index over a NOT NULL column could be used instead of a primary key and the same functional dependence would apply. (This is not true for a UNIQUE index that permits NULL values because it permits multiple NULL values and in that case uniqueness is lost.)

## <span id="page-10-1"></span>**Functional Dependencies Derived from Multiple-Column Keys and from Equalities**

This query selects, for each country, a list of all spoken languages and how many people speak them:

```
SELECT co.Name, cl.Language,
cl.Percentage * co.Population / 100.0 AS SpokenBy
FROM countryLanguage cl, country co
WHERE cl.CountryCode = co.Code
GROUP BY cl.CountryCode, cl.Language;
```

The pair (cl.CountryCode, cl.Language) is a two-column composite primary key of cl, so that column pair uniquely determines all columns of cl:

```
{cl.CountryCode, cl.Language} -> {cl.*}
```

Moreover, because of the equality in the WHERE clause:

```
{cl.CountryCode} -> {co.Code}
```

And, because co.Code is primary key of co:

```
{co.Code} -> {co.*}
```

"Uniquely determines" relationships are transitive, therefore:

```
{cl.CountryCode, cl.Language} -> {cl.*,co.*}
```

As a result, the query is valid.

As with the previous example, a UNIQUE key over NOT NULL columns could be used instead of a primary key.

An INNER JOIN condition can be used instead of WHERE. The same functional dependencies apply:

```
SELECT co.Name, cl.Language,
cl.Percentage * co.Population/100.0 AS SpokenBy
FROM countrylanguage cl INNER JOIN country co
ON cl.CountryCode = co.Code
GROUP BY cl.CountryCode, cl.Language;
```

### <span id="page-10-2"></span>**Functional Dependency Special Cases**

Whereas an equality test in a WHERE condition or INNER JOIN condition is symmetric, an equality test in an outer join condition is not, because tables play different roles.

Assume that referential integrity has been accidentally broken and there exists a row of countrylanguage without a corresponding row in country. Consider the same query as in the previous example, but with a LEFT JOIN:

```
SELECT co.Name, cl.Language,
cl.Percentage * co.Population/100.0 AS SpokenBy
FROM countrylanguage cl LEFT JOIN country co
ON cl.CountryCode = co.Code
GROUP BY cl.CountryCode, cl.Language;
```

For a given value of cl.CountryCode, the value of co.Code in the join result is either found in a matching row (determined by cl.CountryCode) or is NULL-complemented if there is no match (also determined by cl.CountryCode). In each case, this relationship applies:

```
{cl.CountryCode} -> {co.Code}
```

cl.CountryCode is itself functionally dependent on {cl.CountryCode, cl.Language} which is a primary key.

If in the join result co.Code is NULL-complemented, co.Name is as well. If co.Code is not NULLcomplemented, then because co.Code is a primary key, it determines co.Name. Therefore, in all cases:

```
{co.Code} -> {co.Name}
```

Which yields:

```
{cl.CountryCode, cl.Language} -> {cl.*,co.*}
```

As a result, the query is valid.

However, suppose that the tables are swapped, as in this query:

```
SELECT co.Name, cl.Language,
cl.Percentage * co.Population/100.0 AS SpokenBy
FROM country co LEFT JOIN countrylanguage cl
ON cl.CountryCode = co.Code
GROUP BY cl.CountryCode, cl.Language;
```

Now this relationship does not apply:

```
{cl.CountryCode, cl.Language} -> {cl.*,co.*}
```

All NULL-complemented rows made for cl are put into a single group (they have both GROUP BY columns equal to NULL), and inside this group the value of co.Name can vary. The query is invalid and MySQL rejects it.

Functional dependence in outer joins is thus linked to whether determinant columns belong to the left or right side of the LEFT JOIN. Determination of functional dependence becomes more complex if there are nested outer joins or the join condition does not consist entirely of equality comparisons.

### <span id="page-11-0"></span>**Functional Dependencies and Views**

Suppose that a view on countries produces their code, their name in uppercase, and how many different official languages they have:

```
CREATE VIEW country2 AS
SELECT co.Code, UPPER(co.Name) AS UpperName,
COUNT(cl.Language) AS OfficialLanguages
FROM country AS co JOIN countrylanguage AS cl
ON cl.CountryCode = co.Code
WHERE cl.isOfficial = 'T'
GROUP BY co.Code;
```

This definition is valid because:

```
{co.Code} -> {co.*}
```

In the view result, the first selected column is co.Code, which is also the group column and thus determines all other selected expressions:

```
{country2.Code} -> {country2.*}
```

MySQL understands this and uses this information, as described following.

This query displays countries, how many different official languages they have, and how many cities they have, by joining the view with the city table:

```
SELECT co2.Code, co2.UpperName, co2.OfficialLanguages,
COUNT(*) AS Cities
FROM country2 AS co2 JOIN city ci
ON ci.CountryCode = co2.Code
GROUP BY co2.Code;
```

This query is valid because, as seen previously:

```
{co2.Code} -> {co2.*}
```

MySQL is able to discover a functional dependency in the result of a view and use that to validate a query which uses the view. The same would be true if country2 were a derived table, as in:

```
SELECT co2.Code, co2.UpperName, co2.OfficialLanguages,
COUNT(*) AS Cities
FROM
(
 SELECT co.Code, UPPER(co.Name) AS UpperName,
 COUNT(cl.Language) AS OfficialLanguages
 FROM country AS co JOIN countrylanguage AS cl
 ON cl.CountryCode=co.Code
 WHERE cl.isOfficial='T'
 GROUP BY co.Code
) AS co2
JOIN city ci ON ci.CountryCode = co2.Code
GROUP BY co2.Code;
```

## <span id="page-12-0"></span>**Combinations of Functional Dependencies**

MySQL is able to combine all of the preceding types of functional dependencies (key based, equality based, view based) to validate more complex queries.