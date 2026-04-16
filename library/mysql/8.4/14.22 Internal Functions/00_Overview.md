---
source: MySQL 8.4 Reference
title: 00_Overview
---

#### **Table 14.32 Internal Functions**

| Name                                 | Description       |
|--------------------------------------|-------------------|
| CAN_ACCESS_COLUMN()                  | Internal use only |
| CAN_ACCESS_DATABASE()                | Internal use only |
| CAN_ACCESS_TABLE()                   | Internal use only |
| CAN_ACCESS_USER()                    | Internal use only |
| CAN_ACCESS_VIEW()                    | Internal use only |
| GET_DD_COLUMN_PRIVILEGES()           | Internal use only |
| GET_DD_CREATE_OPTIONS()              | Internal use only |
| GET_DD_INDEX_SUB_PART_LENGTH()       | Internal use only |
| INTERNAL_AUTO_INCREMENT()            | Internal use only |
| INTERNAL_AVG_ROW_LENGTH()            | Internal use only |
| INTERNAL_CHECK_TIME()                | Internal use only |
| INTERNAL_CHECKSUM()                  | Internal use only |
| INTERNAL_DATA_FREE()                 | Internal use only |
| INTERNAL_DATA_LENGTH()               | Internal use only |
| INTERNAL_DD_CHAR_LENGTH()            | Internal use only |
| INTERNAL_GET_COMMENT_OR_ERROR()      | Internal use only |
| INTERNAL_GET_ENABLED_ROLE_JSON()     | Internal use only |
| INTERNAL_GET_HOSTNAME()              | Internal use only |
| INTERNAL_GET_USERNAME()              | Internal use only |
| INTERNAL_GET_VIEW_WARNING_OR_ERROR() | Internal use only |
| INTERNAL_INDEX_COLUMN_CARDINALITY()  | Internal use only |
| INTERNAL_INDEX_LENGTH()              | Internal use only |
| INTERNAL_IS_ENABLED_ROLE()           | Internal use only |
| INTERNAL_IS_MANDATORY_ROLE()         | Internal use only |
| INTERNAL_KEYS_DISABLED()             | Internal use only |
| INTERNAL_MAX_DATA_LENGTH()           | Internal use only |
| INTERNAL_TABLE_ROWS()                | Internal use only |
| INTERNAL_UPDATE_TIME()               | Internal use only |

The functions listed in this section are intended only for internal use by the server. Attempts by users to invoke them result in an error.

- <span id="page-48-0"></span>• [CAN\\_ACCESS\\_COLUMN\(](#page-48-0)ARGS)
- <span id="page-48-1"></span>• [CAN\\_ACCESS\\_DATABASE\(](#page-48-1)ARGS)

- <span id="page-49-0"></span>• [CAN\\_ACCESS\\_TABLE\(](#page-49-0)ARGS)
- <span id="page-49-1"></span>• [CAN\\_ACCESS\\_USER\(](#page-49-1)ARGS)
- <span id="page-49-2"></span>• [CAN\\_ACCESS\\_VIEW\(](#page-49-2)ARGS)
- <span id="page-49-3"></span>• [GET\\_DD\\_COLUMN\\_PRIVILEGES\(](#page-49-3)ARGS)
- <span id="page-49-4"></span>• [GET\\_DD\\_CREATE\\_OPTIONS\(](#page-49-4)ARGS)
- <span id="page-49-5"></span>• [GET\\_DD\\_INDEX\\_SUB\\_PART\\_LENGTH\(](#page-49-5)ARGS)
- <span id="page-49-6"></span>• [INTERNAL\\_AUTO\\_INCREMENT\(](#page-49-6)ARGS)
- <span id="page-49-7"></span>• [INTERNAL\\_AVG\\_ROW\\_LENGTH\(](#page-49-7)ARGS)
- <span id="page-49-8"></span>• [INTERNAL\\_CHECK\\_TIME\(](#page-49-8)ARGS)
- <span id="page-49-9"></span>• [INTERNAL\\_CHECKSUM\(](#page-49-9)ARGS)
- <span id="page-49-10"></span>• [INTERNAL\\_DATA\\_FREE\(](#page-49-10)ARGS)
- <span id="page-49-11"></span>• [INTERNAL\\_DATA\\_LENGTH\(](#page-49-11)ARGS)
- <span id="page-49-12"></span>• [INTERNAL\\_DD\\_CHAR\\_LENGTH\(](#page-49-12)ARGS)
- <span id="page-49-13"></span>• [INTERNAL\\_GET\\_COMMENT\\_OR\\_ERROR\(](#page-49-13)ARGS)
- <span id="page-49-14"></span>• [INTERNAL\\_GET\\_ENABLED\\_ROLE\\_JSON\(](#page-49-14)ARGS)
- <span id="page-49-15"></span>• [INTERNAL\\_GET\\_HOSTNAME\(](#page-49-15)ARGS)
- <span id="page-49-16"></span>• [INTERNAL\\_GET\\_USERNAME\(](#page-49-16)ARGS)
- <span id="page-49-17"></span>• [INTERNAL\\_GET\\_VIEW\\_WARNING\\_OR\\_ERROR\(](#page-49-17)ARGS)
- <span id="page-49-18"></span>• [INTERNAL\\_INDEX\\_COLUMN\\_CARDINALITY\(](#page-49-18)ARGS)
- <span id="page-49-19"></span>• [INTERNAL\\_INDEX\\_LENGTH\(](#page-49-19)ARGS)
- <span id="page-49-20"></span>• [INTERNAL\\_IS\\_ENABLED\\_ROLE\(](#page-49-20)ARGS)
- <span id="page-49-21"></span>• [INTERNAL\\_IS\\_MANDATORY\\_ROLE\(](#page-49-21)ARGS)
- <span id="page-49-22"></span>• [INTERNAL\\_KEYS\\_DISABLED\(](#page-49-22)ARGS)
- <span id="page-49-23"></span>• [INTERNAL\\_MAX\\_DATA\\_LENGTH\(](#page-49-23)ARGS)
- <span id="page-49-24"></span>• [INTERNAL\\_TABLE\\_ROWS\(](#page-49-24)ARGS)
- [INTERNAL\\_UPDATE\\_TIME\(](#page-49-25)ARGS)
- [IS\\_VISIBLE\\_DD\\_OBJECT\(](#page-49-26)ARGS)

# <span id="page-49-26"></span><span id="page-49-25"></span>**14.23 Miscellaneous Functions**

### **Table 14.33 Miscellaneous Functions**

| Name          | Description                                    |
|---------------|------------------------------------------------|
| ANY_VALUE()   | Suppress ONLY_FULL_GROUP_BY value<br>rejection |
| BIN_TO_UUID() | Convert binary UUID to string                  |

| Name          | Description                                                  |
|---------------|--------------------------------------------------------------|
| DEFAULT()     | Return the default value for a table column                  |
| GROUPING()    | Distinguish super-aggregate ROLLUP rows from<br>regular rows |
| INET_ATON()   | Return the numeric value of an IP address                    |
| INET_NTOA()   | Return the IP address from a numeric value                   |
| IS_UUID()     | Whether argument is a valid UUID                             |
| NAME_CONST()  | Cause the column to have the given name                      |
| SLEEP()       | Sleep for a number of seconds                                |
| UUID()        | Return a Universal Unique Identifier (UUID)                  |
| UUID_SHORT()  | Return an integer-valued universal identifier                |
| UUID_TO_BIN() | Convert string UUID to binary                                |
| VALUES()      | Define the values to be used during an INSERT                |

### <span id="page-50-0"></span>• [ANY\\_VALUE\(](#page-50-0)arg)

This function is useful for GROUP BY queries when the ONLY\_FULL\_GROUP\_BY SQL mode is enabled, for cases when MySQL rejects a query that you know is valid for reasons that MySQL cannot determine. The function return value and type are the same as the return value and type of its argument, but the function result is not checked for the ONLY\_FULL\_GROUP\_BY SQL mode.

For example, if name is a nonindexed column, the following query fails with ONLY\_FULL\_GROUP\_BY enabled:

```
mysql> SELECT name, address, MAX(age) FROM t GROUP BY name;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP
BY clause and contains nonaggregated column 'mydb.t.address' which
is not functionally dependent on columns in GROUP BY clause; this
is incompatible with sql_mode=only_full_group_by
```

The failure occurs because address is a nonaggregated column that is neither named among GROUP BY columns nor functionally dependent on them. As a result, the address value for rows within each name group is nondeterministic. There are multiple ways to cause MySQL to accept the query:

- Alter the table to make name a primary key or a unique NOT NULL column. This enables MySQL to determine that address is functionally dependent on name; that is, address is uniquely determined by name. (This technique is inapplicable if NULL must be permitted as a valid name value.)
- Use [ANY\\_VALUE\(\)](#page-50-0) to refer to address:

```
SELECT name, ANY_VALUE(address), MAX(age) FROM t GROUP BY name;
```

In this case, MySQL ignores the nondeterminism of address values within each name group and accepts the query. This may be useful if you simply do not care which value of a nonaggregated column is chosen for each group. [ANY\\_VALUE\(\)](#page-50-0) is not an aggregate function, unlike functions such as [SUM\(\)](#page-16-4) or [COUNT\(\)](#page-10-0). It simply acts to suppress the test for nondeterminism.

• Disable ONLY\_FULL\_GROUP\_BY. This is equivalent to using [ANY\\_VALUE\(\)](#page-50-0) with ONLY\_FULL\_GROUP\_BY enabled, as described in the previous item.

[ANY\\_VALUE\(\)](#page-50-0) is also useful if functional dependence exists between columns but MySQL cannot determine it. The following query is valid because age is functionally dependent on the grouping column age-1, but MySQL cannot tell that and rejects the query with ONLY\_FULL\_GROUP\_BY enabled:

```
SELECT age FROM t GROUP BY age-1;
```

To cause MySQL to accept the query, use [ANY\\_VALUE\(\)](#page-50-0):

```
SELECT ANY_VALUE(age) FROM t GROUP BY age-1;
```

[ANY\\_VALUE\(\)](#page-50-0) can be used for queries that refer to aggregate functions in the absence of a GROUP BY clause:

```
mysql> SELECT name, MAX(age) FROM t;
ERROR 1140 (42000): In aggregated query without GROUP BY, expression
#1 of SELECT list contains nonaggregated column 'mydb.t.name'; this
is incompatible with sql_mode=only_full_group_by
```

Without GROUP BY, there is a single group and it is nondeterministic which name value to choose for the group. [ANY\\_VALUE\(\)](#page-50-0) tells MySQL to accept the query:

```
SELECT ANY_VALUE(name), MAX(age) FROM t;
```

It may be that, due to some property of a given data set, you know that a selected nonaggregated column is effectively functionally dependent on a GROUP BY column. For example, an application may enforce uniqueness of one column with respect to another. In this case, using [ANY\\_VALUE\(\)](#page-50-0) for the effectively functionally dependent column may make sense.

For additional discussion, see [Section 14.19.3, "MySQL Handling of GROUP BY"](#page-23-0).

<span id="page-51-0"></span>• [BIN\\_TO\\_UUID\(](#page-51-0)binary\_uuid), [BIN\\_TO\\_UUID\(](#page-51-0)binary\_uuid, swap\_flag)

[BIN\\_TO\\_UUID\(\)](#page-51-0) is the inverse of [UUID\\_TO\\_BIN\(\)](#page-61-1). It converts a binary UUID to a string UUID and returns the result. The binary value should be a UUID as a VARBINARY(16) value. The return value is a string of five hexadecimal numbers separated by dashes. (For details about this format, see the [UUID\(\)](#page-60-0) function description.) If the UUID argument is NULL, the return value is NULL. If any argument is invalid, an error occurs.

[BIN\\_TO\\_UUID\(\)](#page-51-0) takes one or two arguments:

- The one-argument form takes a binary UUID value. The UUID value is assumed not to have its time-low and time-high parts swapped. The string result is in the same order as the binary argument.
- The two-argument form takes a binary UUID value and a swap-flag value:
  - If swap\_flag is 0, the two-argument form is equivalent to the one-argument form. The string result is in the same order as the binary argument.
  - If swap\_flag is 1, the UUID value is assumed to have its time-low and time-high parts swapped. These parts are swapped back to their original position in the result value.

For usage examples and information about time-part swapping, see the [UUID\\_TO\\_BIN\(\)](#page-61-1) function description.

<span id="page-51-1"></span>• [DEFAULT\(](#page-51-1)col\_name)

Returns the default value for a table column. An error results if the column has no default value.

The use of [DEFAULT\(](#page-51-1)col\_name) to specify the default value for a named column is permitted only for columns that have a literal default value, not for columns that have an expression default value.

```
mysql> UPDATE t SET i = DEFAULT(i)+1 WHERE id < 100;
```

### • FORMAT(X,D)

Formats the number X to a format like '#,###,###.##', rounded to D decimal places, and returns the result as a string. For details, see Section 14.8, "String Functions and Operators".

<span id="page-52-0"></span>• [GROUPING\(](#page-52-0)expr [, expr] ...)

For GROUP BY queries that include a WITH ROLLUP modifier, the ROLLUP operation produces super-aggregate output rows where NULL represents the set of all values. The [GROUPING\(\)](#page-52-0) function enables you to distinguish NULL values for super-aggregate rows from NULL values in regular grouped rows.

[GROUPING\(\)](#page-52-0) is permitted in the select list, HAVING clause, and ORDER BY clause.

Each argument to [GROUPING\(\)](#page-52-0) must be an expression that exactly matches an expression in the GROUP BY clause. The expression cannot be a positional specifier. For each expression, [GROUPING\(\)](#page-52-0) produces 1 if the expression value in the current row is a NULL representing a superaggregate value. Otherwise, [GROUPING\(\)](#page-52-0) produces 0, indicating that the expression value is a NULL for a regular result row or is not NULL.

Suppose that table t1 contains these rows, where NULL indicates something like "other" or "unknown":

```
mysql> SELECT * FROM t1;
+------+-------+----------+
| name | size | quantity |
+------+-------+----------+
| ball | small | 10 |
| ball | large | 20 |
| ball | NULL | 5 |
| hoop | small | 15 |
| hoop | large | 5 |
| hoop | NULL | 3 |
+------+-------+----------+
```

A summary of the table without WITH ROLLUP looks like this:

```
mysql> SELECT name, size, SUM(quantity) AS quantity
 FROM t1
 GROUP BY name, size;
+------+-------+----------+
| name | size | quantity |
+------+-------+----------+
| ball | small | 10 |
| ball | large | 20 |
| ball | NULL | 5 |
| hoop | small | 15 |
| hoop | large | 5 |
| hoop | NULL | 3 |
+------+-------+----------+
```

The result contains NULL values, but those do not represent super-aggregate rows because the query does not include WITH ROLLUP.

Adding WITH ROLLUP produces super-aggregate summary rows containing additional NULL values. However, without comparing this result to the previous one, it is not easy to see which NULL values occur in super-aggregate rows and which occur in regular grouped rows:

```
mysql> SELECT name, size, SUM(quantity) AS quantity
 FROM t1
 GROUP BY name, size WITH ROLLUP;
+------+-------+----------+
| name | size | quantity |
+------+-------+----------+
| ball | NULL | 5 |
| ball | large | 20 |
| ball | small | 10 |
```

```
| ball | NULL | 35 |
| hoop | NULL | 3 |
| hoop | large | 5 |
| hoop | small | 15 |
| hoop | NULL | 23 |
| NULL | NULL | 58 |
+------+-------+----------+
```

To distinguish NULL values in super-aggregate rows from those in regular grouped rows, use [GROUPING\(\)](#page-52-0), which returns 1 only for super-aggregate NULL values:

```
mysql> SELECT
 name, size, SUM(quantity) AS quantity,
 GROUPING(name) AS grp_name,
 GROUPING(size) AS grp_size
 FROM t1
 GROUP BY name, size WITH ROLLUP;
+------+-------+----------+----------+----------+
| name | size | quantity | grp_name | grp_size |
+------+-------+----------+----------+----------+
| ball | NULL | 5 | 0 | 0 |
| ball | large | 20 | 0 | 0 |
| ball | small | 10 | 0 | 0 |
| ball | NULL | 35 | 0 | 1 |
| hoop | NULL | 3 | 0 | 0 |
| hoop | large | 5 | 0 | 0 |
| hoop | small | 15 | 0 | 0 |
| hoop | NULL | 23 | 0 | 1 |
| NULL | NULL | 58 | 1 | 1 |
+------+-------+----------+----------+----------+
```

Common uses for [GROUPING\(\)](#page-52-0):

• Substitute a label for super-aggregate NULL values:

```
mysql> SELECT
 IF(GROUPING(name) = 1, 'All items', name) AS name,
 IF(GROUPING(size) = 1, 'All sizes', size) AS size,
 SUM(quantity) AS quantity
 FROM t1
 GROUP BY name, size WITH ROLLUP;
+-----------+-----------+----------+
| name | size | quantity |
+-----------+-----------+----------+
| ball | NULL | 5 |
| ball | large | 20 |
| ball | small | 10 |
| ball | All sizes | 35 |
| hoop | NULL | 3 |
| hoop | large | 5 |
| hoop | small | 15 |
| hoop | All sizes | 23 |
| All items | All sizes | 58 |
+-----------+-----------+----------+
```

• Return only super-aggregate lines by filtering out the regular grouped lines:

```
mysql> SELECT name, size, SUM(quantity) AS quantity
 FROM t1
 GROUP BY name, size WITH ROLLUP
 HAVING GROUPING(name) = 1 OR GROUPING(size) = 1;
+------+------+----------+
| name | size | quantity |
+------+------+----------+
| ball | NULL | 35 |
| hoop | NULL | 23 |
| NULL | NULL | 58 |
```

+------+------+----------+

[GROUPING\(\)](#page-52-0) permits multiple expression arguments. In this case, the [GROUPING\(\)](#page-52-0) return value represents a bitmask combined from the results for each expression, where the lowest-order bit corresponds to the result for the rightmost expression. For example, with three expression arguments, [GROUPING\(](#page-52-0)expr1, expr2, expr3) is evaluated like this:

```
 result for GROUPING(expr3)
+ result for GROUPING(expr2) << 1
+ result for GROUPING(expr1) << 2
```

The following query shows how [GROUPING\(\)](#page-52-0) results for single arguments combine for a multipleargument call to produce a bitmask value:

```
mysql> SELECT
 name, size, SUM(quantity) AS quantity,
 GROUPING(name) AS grp_name,
 GROUPING(size) AS grp_size,
 GROUPING(name, size) AS grp_all
 FROM t1
 GROUP BY name, size WITH ROLLUP;
+------+-------+----------+----------+----------+---------+
| name | size | quantity | grp_name | grp_size | grp_all |
+------+-------+----------+----------+----------+---------+
| ball | NULL | 5 | 0 | 0 | 0 |
| ball | large | 20 | 0 | 0 | 0 |
| ball | small | 10 | 0 | 0 | 0 |
| ball | NULL | 35 | 0 | 1 | 1 |
| hoop | NULL | 3 | 0 | 0 | 0 |
| hoop | large | 5 | 0 | 0 | 0 |
| hoop | small | 15 | 0 | 0 | 0 |
| hoop | NULL | 23 | 0 | 1 | 1 |
| NULL | NULL | 58 | 1 | 1 | 3 |
+------+-------+----------+----------+----------+---------+
```

With multiple expression arguments, the [GROUPING\(\)](#page-52-0) return value is nonzero if any expression represents a super-aggregate value. Multiple-argument [GROUPING\(\)](#page-52-0) syntax thus provides a simpler way to write the earlier query that returned only super-aggregate rows, by using a single multipleargument [GROUPING\(\)](#page-52-0) call rather than multiple single-argument calls:

```
mysql> SELECT name, size, SUM(quantity) AS quantity
 FROM t1
 GROUP BY name, size WITH ROLLUP
 HAVING GROUPING(name, size) <> 0;
+------+------+----------+
| name | size | quantity |
+------+------+----------+
| ball | NULL | 35 |
| hoop | NULL | 23 |
| NULL | NULL | 58 |
+------+------+----------+
```

Use of [GROUPING\(\)](#page-52-0) is subject to these limitations:

• Do not use subquery GROUP BY expressions as [GROUPING\(\)](#page-52-0) arguments because matching might fail. For example, matching fails for this query:

```
mysql> SELECT GROUPING((SELECT MAX(name) FROM t1))
 FROM t1
 GROUP BY (SELECT MAX(name) FROM t1) WITH ROLLUP;
ERROR 3580 (HY000): Argument #1 of GROUPING function is not in GROUP BY
```

• GROUP BY literal expressions should not be used within a HAVING clause as [GROUPING\(\)](#page-52-0) arguments. Due to differences between when the optimizer evaluates GROUP BY and HAVING, matching may succeed but [GROUPING\(\)](#page-52-0) evaluation does not produce the expected result. Consider this query:

```
SELECT a AS f1, 'w' AS f2
FROM t
GROUP BY f1, f2 WITH ROLLUP
HAVING GROUPING(f2) = 1;
```

[GROUPING\(\)](#page-52-0) is evaluated earlier for the literal constant expression than for the HAVING clause as a whole and returns 0. To check whether a query such as this is affected, use EXPLAIN and look for Impossible having in the Extra column.

For more information about WITH ROLLUP and [GROUPING\(\)](#page-52-0), see [Section 14.19.2, "GROUP BY](#page-17-3) [Modifiers".](#page-17-3)

<span id="page-55-0"></span>• [INET\\_ATON\(](#page-55-0)expr)

Given the dotted-quad representation of an IPv4 network address as a string, returns an integer that represents the numeric value of the address in network byte order (big endian). [INET\\_ATON\(\)](#page-55-0) returns NULL if it does not understand its argument, or if expr is NULL.

```
mysql> SELECT INET_ATON('10.0.5.9');
 -> 167773449
```

For this example, the return value is calculated as 10×256<sup>3</sup> + 0×256<sup>2</sup> + 5×256 + 9.

[INET\\_ATON\(\)](#page-55-0) may or may not return a non-NULL result for short-form IP addresses (such as '127.1' as a representation of '127.0.0.1'). Because of this, [INET\\_ATON\(\)](#page-55-0)a should not be used for such addresses.

![](_page_55_Picture_10.jpeg)

#### **Note**

To store values generated by [INET\\_ATON\(\)](#page-55-0), use an INT UNSIGNED column rather than INT, which is signed. If you use a signed column, values corresponding to IP addresses for which the first octet is greater than 127 cannot be stored correctly. See Section 13.1.7, "Out-of-Range and Overflow Handling".

<span id="page-55-1"></span>• [INET\\_NTOA\(](#page-55-1)expr)

Given a numeric IPv4 network address in network byte order, returns the dotted-quad string representation of the address as a string in the connection character set. [INET\\_NTOA\(\)](#page-55-1) returns NULL if it does not understand its argument.

```
mysql> SELECT INET_NTOA(167773449);
 -> '10.0.5.9'
```

<span id="page-55-2"></span>• [INET6\\_ATON\(](#page-55-2)expr)

Given an IPv6 or IPv4 network address as a string, returns a binary string that represents the numeric value of the address in network byte order (big endian). Because numeric-format IPv6 addresses require more bytes than the largest integer type, the representation returned by this function has the VARBINARY data type: VARBINARY(16) for IPv6 addresses and VARBINARY(4) for IPv4 addresses. If the argument is not a valid address, or if it is NULL, [INET6\\_ATON\(\)](#page-55-2) returns NULL.

The following examples use HEX() to display the [INET6\\_ATON\(\)](#page-55-2) result in printable form:

```
mysql> SELECT HEX(INET6_ATON('fdfe::5a55:caff:fefa:9089'));
 -> 'FDFE0000000000005A55CAFFFEFA9089'
mysql> SELECT HEX(INET6_ATON('10.0.5.9'));
```

```
 -> '0A000509'
```

INET6\_ATON() observes several constraints on valid arguments. These are given in the following list along with examples.

- A trailing zone ID is not permitted, as in fe80::3%1 or fe80::3%eth0.
- A trailing network mask is not permitted, as in 2001:45f:3:ba::/64 or 198.51.100.0/24.
- For values representing IPv4 addresses, only classless addresses are supported. Classful addresses such as 198.51.1 are rejected. A trailing port number is not permitted, as in 198.51.100.2:8080. Hexadecimal numbers in address components are not permitted, as in 198.0xa0.1.2. Octal numbers are not supported: 198.51.010.1 is treated as 198.51.10.1, not 198.51.8.1. These IPv4 constraints also apply to IPv6 addresses that have IPv4 address parts, such as IPv4-compatible or IPv4-mapped addresses.

To convert an IPv4 address expr represented in numeric form as an INT value to an IPv6 address represented in numeric form as a VARBINARY value, use this expression:

```
INET6_ATON(INET_NTOA(expr))
```

For example:

```
mysql> SELECT HEX(INET6_ATON(INET_NTOA(167773449)));
 -> '0A000509'
```

If [INET6\\_ATON\(\)](#page-55-2) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-56-0"></span>• [INET6\\_NTOA\(](#page-56-0)expr)

Given an IPv6 or IPv4 network address represented in numeric form as a binary string, returns the string representation of the address as a string in the connection character set. If the argument is not a valid address, or if it is NULL, [INET6\\_NTOA\(\)](#page-56-0) returns NULL.

[INET6\\_NTOA\(\)](#page-56-0) has these properties:

- It does not use operating system functions to perform conversions, thus the output string is platform independent.
- The return string has a maximum length of 39 (4 x 8 + 7). Given this statement:

```
CREATE TABLE t AS SELECT INET6_NTOA(expr) AS c1;
```

The resulting table would have this definition:

```
CREATE TABLE t (c1 VARCHAR(39) CHARACTER SET utf8mb3 DEFAULT NULL);
```

• The return string uses lowercase letters for IPv6 addresses.

```
mysql> SELECT INET6_NTOA(INET6_ATON('fdfe::5a55:caff:fefa:9089'));
 -> 'fdfe::5a55:caff:fefa:9089'
mysql> SELECT INET6_NTOA(INET6_ATON('10.0.5.9'));
 -> '10.0.5.9'
mysql> SELECT INET6_NTOA(UNHEX('FDFE0000000000005A55CAFFFEFA9089'));
 -> 'fdfe::5a55:caff:fefa:9089'
mysql> SELECT INET6_NTOA(UNHEX('0A000509'));
 -> '10.0.5.9'
```

If [INET6\\_NTOA\(\)](#page-56-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

### <span id="page-57-0"></span>• [IS\\_IPV4\(](#page-57-0)expr)

Returns 1 if the argument is a valid IPv4 address specified as a string, 0 otherwise. Returns NULL if expr is NULL.

```
mysql> SELECT IS_IPV4('10.0.5.9'), IS_IPV4('10.0.5.256');
 -> 1, 0
```

For a given argument, if [IS\\_IPV4\(\)](#page-57-0) returns 1, [INET\\_ATON\(\)](#page-55-0) (and [INET6\\_ATON\(\)](#page-55-2)) returns non-NULL. The converse statement is not true: In some cases, [INET\\_ATON\(\)](#page-55-0) returns non-NULL when [IS\\_IPV4\(\)](#page-57-0) returns 0.

As implied by the preceding remarks, [IS\\_IPV4\(\)](#page-57-0) is more strict than [INET\\_ATON\(\)](#page-55-0) about what constitutes a valid IPv4 address, so it may be useful for applications that need to perform strong checks against invalid values. Alternatively, use [INET6\\_ATON\(\)](#page-55-2) to convert IPv4 addresses to internal form and check for a NULL result (which indicates an invalid address). [INET6\\_ATON\(\)](#page-55-2) is equally strong as [IS\\_IPV4\(\)](#page-57-0) about checking IPv4 addresses.

<span id="page-57-1"></span>• [IS\\_IPV4\\_COMPAT\(](#page-57-1)expr)

This function takes an IPv6 address represented in numeric form as a binary string, as returned by [INET6\\_ATON\(\)](#page-55-2). It returns 1 if the argument is a valid IPv4-compatible IPv6 address, 0 otherwise (unless expr is NULL, in which case the function returns NULL). IPv4-compatible addresses have the form ::ipv4\_address.

```
mysql> SELECT IS_IPV4_COMPAT(INET6_ATON('::10.0.5.9'));
 -> 1
mysql> SELECT IS_IPV4_COMPAT(INET6_ATON('::ffff:10.0.5.9'));
 -> 0
```

The IPv4 part of an IPv4-compatible address can also be represented using hexadecimal notation. For example, 198.51.100.1 has this raw hexadecimal value:

```
mysql> SELECT HEX(INET6_ATON('198.51.100.1'));
 -> 'C6336401'
```

Expressed in IPv4-compatible form, ::198.51.100.1 is equivalent to ::c0a8:0001 or (without leading zeros) ::c0a8:1

```
mysql> SELECT
 -> IS_IPV4_COMPAT(INET6_ATON('::198.51.100.1')),
 -> IS_IPV4_COMPAT(INET6_ATON('::c0a8:0001')),
 -> IS_IPV4_COMPAT(INET6_ATON('::c0a8:1'));
 -> 1, 1, 1
```

<span id="page-57-2"></span>• [IS\\_IPV4\\_MAPPED\(](#page-57-2)expr)

This function takes an IPv6 address represented in numeric form as a binary string, as returned by [INET6\\_ATON\(\)](#page-55-2). It returns 1 if the argument is a valid IPv4-mapped IPv6 address, 0 otherwise, unless expr is NULL, in which case the function returns NULL. IPv4-mapped addresses have the form ::ffff:ipv4\_address.

```
mysql> SELECT IS_IPV4_MAPPED(INET6_ATON('::10.0.5.9'));
 -> 0
mysql> SELECT IS_IPV4_MAPPED(INET6_ATON('::ffff:10.0.5.9'));
 -> 1
```

As with IS\_IPV4\_COMPAT() the IPv4 part of an IPv4-mapped address can also be represented using hexadecimal notation:

```
mysql> SELECT
 -> IS_IPV4_MAPPED(INET6_ATON('::ffff:198.51.100.1')),
 -> IS_IPV4_MAPPED(INET6_ATON('::ffff:c0a8:0001')),
 -> IS_IPV4_MAPPED(INET6_ATON('::ffff:c0a8:1'));
 -> 1, 1, 1
```

<span id="page-58-1"></span>• [IS\\_IPV6\(](#page-58-1)expr)

Returns 1 if the argument is a valid IPv6 address specified as a string, 0 otherwise, unless expr is NULL, in which case the function returns NULL. This function does not consider IPv4 addresses to be valid IPv6 addresses.

```
mysql> SELECT IS_IPV6('10.0.5.9'), IS_IPV6('::1');
 -> 0, 1
```

For a given argument, if [IS\\_IPV6\(\)](#page-58-1) returns 1, [INET6\\_ATON\(\)](#page-55-2) returns non-NULL.

<span id="page-58-0"></span>• IS\_UUID([string\\_uuid](#page-58-0))

Returns 1 if the argument is a valid string-format UUID, 0 if the argument is not a valid UUID, and NULL if the argument is NULL.

"Valid" means that the value is in a format that can be parsed. That is, it has the correct length and contains only the permitted characters (hexadecimal digits in any lettercase and, optionally, dashes and curly braces). This format is most common:

```
aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
```

These other formats are also permitted:

```
aaaaaaaabbbbccccddddeeeeeeeeeeee
{aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee}
```

For the meanings of fields within the value, see the [UUID\(\)](#page-60-0) function description.

```
mysql> SELECT IS_UUID('6ccd780c-baba-1026-9564-5b8c656024db');
+-------------------------------------------------+
| IS_UUID('6ccd780c-baba-1026-9564-5b8c656024db') |
+-------------------------------------------------+
| 1 |
+-------------------------------------------------+
mysql> SELECT IS_UUID('6CCD780C-BABA-1026-9564-5B8C656024DB');
+-------------------------------------------------+
| IS_UUID('6CCD780C-BABA-1026-9564-5B8C656024DB') |
+-------------------------------------------------+
| 1 |
+-------------------------------------------------+
mysql> SELECT IS_UUID('6ccd780cbaba102695645b8c656024db');
+---------------------------------------------+
| IS_UUID('6ccd780cbaba102695645b8c656024db') |
+---------------------------------------------+
| 1 |
+---------------------------------------------+
mysql> SELECT IS_UUID('{6ccd780c-baba-1026-9564-5b8c656024db}');
+---------------------------------------------------+
| IS_UUID('{6ccd780c-baba-1026-9564-5b8c656024db}') |
+---------------------------------------------------+
| 1 |
+---------------------------------------------------+
mysql> SELECT IS_UUID('6ccd780c-baba-1026-9564-5b8c6560');
+---------------------------------------------+
| IS_UUID('6ccd780c-baba-1026-9564-5b8c6560') |
+---------------------------------------------+
| 0 |
+---------------------------------------------+
mysql> SELECT IS_UUID(RAND());
+-----------------+
| IS_UUID(RAND()) |
+-----------------+
| 0 |
+-----------------+
```

<span id="page-59-0"></span>• [NAME\\_CONST\(](#page-59-0)name,value)

Returns the given value. When used to produce a result set column, [NAME\\_CONST\(\)](#page-59-0) causes the column to have the given name. The arguments should be constants.

```
mysql> SELECT NAME_CONST('myname', 14);
+--------+
| myname |
+--------+
| 14 |
+--------+
```

This function is for internal use only. The server uses it when writing statements from stored programs that contain references to local program variables, as described in Section 27.7, "Stored Program Binary Logging". You might see this function in the output from mysqlbinlog.

For your applications, you can obtain exactly the same result as in the example just shown by using simple aliasing, like this:

```
mysql> SELECT 14 AS myname;
+--------+
| myname |
+--------+
| 14 |
+--------+
1 row in set (0.00 sec)
```

See Section 15.2.13, "SELECT Statement", for more information about column aliases.

<span id="page-59-1"></span>• SLEEP([duration](#page-59-1))

Sleeps (pauses) for the number of seconds given by the duration argument, then returns 0. The duration may have a fractional part. If the argument is NULL or negative, [SLEEP\(\)](#page-59-1) produces a warning, or an error in strict SQL mode.

When sleep returns normally (without interruption), it returns 0:

```
mysql> SELECT SLEEP(1000);
+-------------+
| SLEEP(1000) |
+-------------+
| 0 |
+-------------+
```

When [SLEEP\(\)](#page-59-1) is the only thing invoked by a query that is interrupted, it returns 1 and the query itself returns no error. This is true whether the query is killed or times out:

• This statement is interrupted using KILL QUERY from another session:

```
mysql> SELECT SLEEP(1000);
+-------------+
| SLEEP(1000) |
+-------------+
| 1 |
+-------------+
```

• This statement is interrupted by timing out:

```
mysql> SELECT /*+ MAX_EXECUTION_TIME(1) */ SLEEP(1000);
+-------------+
| SLEEP(1000) |
+-------------+
| 1 |
```

+-------------+

When [SLEEP\(\)](#page-59-1) is only part of a query that is interrupted, the query returns an error:

• This statement is interrupted using KILL QUERY from another session:

```
mysql> SELECT 1 FROM t1 WHERE SLEEP(1000);
ERROR 1317 (70100): Query execution was interrupted
```

• This statement is interrupted by timing out:

```
mysql> SELECT /*+ MAX_EXECUTION_TIME(1000) */ 1 FROM t1 WHERE SLEEP(1000);
ERROR 3024 (HY000): Query execution was interrupted, maximum statement
execution time exceeded
```

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-60-0"></span>• [UUID\(\)](#page-60-0)

Returns a Universal Unique Identifier (UUID) generated according to RFC 4122, "A Universally Unique IDentifier (UUID) URN Namespace" [\(http://www.ietf.org/rfc/rfc4122.txt\)](http://www.ietf.org/rfc/rfc4122.txt).

A UUID is designed as a number that is globally unique in space and time. Two calls to [UUID\(\)](#page-60-0) are expected to generate two different values, even if these calls are performed on two separate devices not connected to each other.

![](_page_60_Picture_11.jpeg)

#### **Warning**

Although [UUID\(\)](#page-60-0) values are intended to be unique, they are not necessarily unguessable or unpredictable. If unpredictability is required, UUID values should be generated some other way.

[UUID\(\)](#page-60-0) returns a value that conforms to UUID version 1 as described in RFC 4122. The value is a 128-bit number represented as a utf8mb3 string of five hexadecimal numbers in aaaaaaaa-bbbbcccc-dddd-eeeeeeeeeeee format:

- The first three numbers are generated from the low, middle, and high parts of a timestamp. The high part also includes the UUID version number.
- The fourth number preserves temporal uniqueness in case the timestamp value loses monotonicity (for example, due to daylight saving time).
- The fifth number is an IEEE 802 node number that provides spatial uniqueness. A random number is substituted if the latter is not available (for example, because the host device has no Ethernet card, or it is unknown how to find the hardware address of an interface on the host operating system). In this case, spatial uniqueness cannot be guaranteed. Nevertheless, a collision should have very low probability.

The MAC address of an interface is taken into account only on FreeBSD, Linux, and Windows. On other operating systems, MySQL uses a randomly generated 48-bit number.

```
mysql> SELECT UUID();
 -> '6ccd780c-baba-1026-9564-5b8c656024db'
```

To convert between string and binary UUID values, use the [UUID\\_TO\\_BIN\(\)](#page-61-1) and [BIN\\_TO\\_UUID\(\)](#page-51-0) functions. To check whether a string is a valid UUID value, use the [IS\\_UUID\(\)](#page-58-0) function.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-61-0"></span>• [UUID\\_SHORT\(\)](#page-61-0)

Returns a "short" universal identifier as a 64-bit unsigned integer. Values returned by [UUID\\_SHORT\(\)](#page-61-0) differ from the string-format 128-bit identifiers returned by the [UUID\(\)](#page-60-0) function and have different uniqueness properties. The value of [UUID\\_SHORT\(\)](#page-61-0) is guaranteed to be unique if the following conditions hold:

- The server\_id value of the current server is between 0 and 255 and is unique among your set of source and replica servers
- You do not set back the system time for your server host between mysqld restarts
- You invoke [UUID\\_SHORT\(\)](#page-61-0) on average fewer than 16 million times per second between mysqld restarts

The [UUID\\_SHORT\(\)](#page-61-0) return value is constructed this way:

```
 (server_id & 255) << 56
+ (server_startup_time_in_seconds << 24)
+ incremented_variable++;
mysql> SELECT UUID_SHORT();
```

![](_page_61_Picture_8.jpeg)

#### **Note**

-> 92395783831158784

[UUID\\_SHORT\(\)](#page-61-0) does not work with statement-based replication.

<span id="page-61-1"></span>• [UUID\\_TO\\_BIN\(](#page-61-1)string\_uuid), [UUID\\_TO\\_BIN\(](#page-61-1)string\_uuid, swap\_flag)

Converts a string UUID to a binary UUID and returns the result. (The [IS\\_UUID\(\)](#page-58-0) function description lists the permitted string UUID formats.) The return binary UUID is a VARBINARY(16) value. If the UUID argument is NULL, the return value is NULL. If any argument is invalid, an error occurs.

[UUID\\_TO\\_BIN\(\)](#page-61-1) takes one or two arguments:

- The one-argument form takes a string UUID value. The binary result is in the same order as the string argument.
- The two-argument form takes a string UUID value and a flag value:
  - If swap\_flag is 0, the two-argument form is equivalent to the one-argument form. The binary result is in the same order as the string argument.
  - If swap\_flag is 1, the format of the return value differs: The time-low and time-high parts (the first and third groups of hexadecimal digits, respectively) are swapped. This moves the more rapidly varying part to the right and can improve indexing efficiency if the result is stored in an indexed column.

Time-part swapping assumes the use of UUID version 1 values, such as are generated by the [UUID\(\)](#page-60-0) function. For UUID values produced by other means that do not follow version 1 format, time-part swapping provides no benefit. For details about version 1 format, see the [UUID\(\)](#page-60-0) function description.

Suppose that you have the following string UUID value:

```
mysql> SET @uuid = '6ccd780c-baba-1026-9564-5b8c656024db';
```

To convert the string UUID to binary with or without time-part swapping, use [UUID\\_TO\\_BIN\(\)](#page-61-1):

```
mysql> SELECT HEX(UUID_TO_BIN(@uuid));
+----------------------------------+
| HEX(UUID_TO_BIN(@uuid)) |
+----------------------------------+
| 6CCD780CBABA102695645B8C656024DB |
+----------------------------------+
mysql> SELECT HEX(UUID_TO_BIN(@uuid, 0));
+----------------------------------+
| HEX(UUID_TO_BIN(@uuid, 0)) |
+----------------------------------+
| 6CCD780CBABA102695645B8C656024DB |
+----------------------------------+
mysql> SELECT HEX(UUID_TO_BIN(@uuid, 1));
+----------------------------------+
| HEX(UUID_TO_BIN(@uuid, 1)) |
+----------------------------------+
| 1026BABA6CCD780C95645B8C656024DB |
+----------------------------------+
```

To convert a binary UUID returned by [UUID\\_TO\\_BIN\(\)](#page-61-1) to a string UUID, use [BIN\\_TO\\_UUID\(\)](#page-51-0). If you produce a binary UUID by calling [UUID\\_TO\\_BIN\(\)](#page-61-1) with a second argument of 1 to swap time parts, you should also pass a second argument of 1 to [BIN\\_TO\\_UUID\(\)](#page-51-0) to unswap the time parts when converting the binary UUID back to a string UUID:

```
mysql> SELECT BIN_TO_UUID(UUID_TO_BIN(@uuid));
+--------------------------------------+
| BIN_TO_UUID(UUID_TO_BIN(@uuid)) |
+--------------------------------------+
| 6ccd780c-baba-1026-9564-5b8c656024db |
+--------------------------------------+
mysql> SELECT BIN_TO_UUID(UUID_TO_BIN(@uuid,0),0);
+--------------------------------------+
| BIN_TO_UUID(UUID_TO_BIN(@uuid,0),0) |
+--------------------------------------+
| 6ccd780c-baba-1026-9564-5b8c656024db |
+--------------------------------------+
mysql> SELECT BIN_TO_UUID(UUID_TO_BIN(@uuid,1),1);
+--------------------------------------+
| BIN_TO_UUID(UUID_TO_BIN(@uuid,1),1) |
+--------------------------------------+
| 6ccd780c-baba-1026-9564-5b8c656024db |
+--------------------------------------+
```

If the use of time-part swapping is not the same for the conversion in both directions, the original UUID is not recovered properly:

```
mysql> SELECT BIN_TO_UUID(UUID_TO_BIN(@uuid,0),1);
+--------------------------------------+
| BIN_TO_UUID(UUID_TO_BIN(@uuid,0),1) |
+--------------------------------------+
| baba1026-780c-6ccd-9564-5b8c656024db |
+--------------------------------------+
mysql> SELECT BIN_TO_UUID(UUID_TO_BIN(@uuid,1),0);
+--------------------------------------+
| BIN_TO_UUID(UUID_TO_BIN(@uuid,1),0) |
+--------------------------------------+
| 1026baba-6ccd-780c-9564-5b8c656024db |
+--------------------------------------+
```

If [UUID\\_TO\\_BIN\(\)](#page-61-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-62-0"></span>• VALUES([col\\_name](#page-62-0))

In an INSERT ... ON DUPLICATE KEY UPDATE statement, you can use the VALUES(col\_name) function in the UPDATE clause to refer to column values from the INSERT portion of the statement. In other words, VALUES(col\_name) in the UPDATE clause refers to the value of col\_name that would be inserted, had no duplicate-key conflict occurred. This function is especially useful in multiple-row inserts. The [VALUES\(\)](#page-62-0) function is meaningful only in the ON DUPLICATE KEY UPDATE clause of INSERT statements and returns NULL otherwise. See Section 15.2.7.2, "INSERT ... ON DUPLICATE KEY UPDATE Statement".

```
mysql> INSERT INTO table (a,b,c) VALUES (1,2,3),(4,5,6)
 -> ON DUPLICATE KEY UPDATE c=VALUES(a)+VALUES(b);
```

![](_page_63_Picture_3.jpeg)

#### **Important**

This usage is deprecated, and subject to removal in a future release of MySQL. Use a row alias, or row and column aliases, instead. For more information and examples, see Section 15.2.7.2, "INSERT ... ON DUPLICATE KEY UPDATE Statement".