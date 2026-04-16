---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section discusses the characteristics of the DECIMAL data type (and its synonyms), with particular regard to the following topics:

- Maximum number of digits
- Storage format
- Storage requirements
- The nonstandard MySQL extension to the upper range of DECIMAL columns

The declaration syntax for a DECIMAL column is DECIMAL(M,D). The ranges of values for the arguments are as follows:

- M is the maximum number of digits (the precision). It has a range of 1 to 65.
- D is the number of digits to the right of the decimal point (the scale). It has a range of 0 to 30 and must be no larger than M.

If D is omitted, the default is 0. If M is omitted, the default is 10.

The maximum value of 65 for M means that calculations on DECIMAL values are accurate up to 65 digits. This limit of 65 digits of precision also applies to exact-value numeric literals, so the maximum range of such literals differs from before. (There is also a limit on how long the text of DECIMAL literals can be; see [Section 14.24.3, "Expression Handling".](#page-38-0))

Values for DECIMAL columns are stored using a binary format that packs nine decimal digits into 4 bytes. The storage requirements for the integer and fractional parts of each value are determined separately. Each multiple of nine digits requires 4 bytes, and any remaining digits left over require some fraction of 4 bytes. The storage required for remaining digits is given by the following table.

| Leftover Digits | Number of Bytes |
|-----------------|-----------------|
| 0               | 0               |
| 1–2             | 1               |
| 3–4             | 2               |
| 5–6             | 3               |
| 7–9             | 4               |

For example, a DECIMAL(18,9) column has nine digits on either side of the decimal point, so the integer part and the fractional part each require 4 bytes. A DECIMAL(20,6) column has fourteen integer digits and six fractional digits. The integer digits require four bytes for nine of the digits and 3 bytes for the remaining five digits. The six fractional digits require 3 bytes.

DECIMAL columns do not store a leading + character or - character or leading 0 digits. If you insert +0003.1 into a DECIMAL(5,1) column, it is stored as 3.1. For negative numbers, a literal character is not stored.

DECIMAL columns do not permit values larger than the range implied by the column definition. For example, a DECIMAL(3,0) column supports a range of -999 to 999. A DECIMAL(M,D) column permits up to M - D digits to the left of the decimal point.

The SQL standard requires that the precision of NUMERIC(M,D) be exactly M digits. For DECIMAL(M,D), the standard requires a precision of at least M digits but permits more. In MySQL, DECIMAL(M,D) and NUMERIC(M,D) are the same, and both have a precision of exactly M digits.

For a full explanation of the internal format of DECIMAL values, see the file strings/decimal.c in a MySQL source distribution. The format is explained (with an example) in the decimal2bin() function.

# <span id="page-38-0"></span>**14.24.3 Expression Handling**

With precision math, exact-value numbers are used as given whenever possible. For example, numbers in comparisons are used exactly as given without a change in value. In strict SQL mode, for INSERT into a column with an exact data type (DECIMAL or integer), a number is inserted with its exact value if it is within the column range. When retrieved, the value should be the same as what was inserted. (If strict SQL mode is not enabled, truncation for INSERT is permissible.)

Handling of a numeric expression depends on what kind of values the expression contains:

- If any approximate values are present, the expression is approximate and is evaluated using floatingpoint arithmetic.
- If no approximate values are present, the expression contains only exact values. If any exact value contains a fractional part (a value following the decimal point), the expression is evaluated using DECIMAL exact arithmetic and has a precision of 65 digits. The term "exact" is subject to the limits of what can be represented in binary. For example, 1.0/3.0 can be approximated in decimal notation as .333..., but not written as an exact number, so (1.0/3.0)\*3.0 does not evaluate to exactly 1.0.
- Otherwise, the expression contains only integer values. The expression is exact and is evaluated using integer arithmetic and has a precision the same as BIGINT (64 bits).

If a numeric expression contains any strings, they are converted to double-precision floating-point values and the expression is approximate.

Inserts into numeric columns are affected by the SQL mode, which is controlled by the sql\_mode system variable. (See Section 7.1.11, "Server SQL Modes".) The following discussion mentions strict mode (selected by the STRICT\_ALL\_TABLES or STRICT\_TRANS\_TABLES mode values) and ERROR\_FOR\_DIVISION\_BY\_ZERO. To turn on all restrictions, you can simply use TRADITIONAL mode, which includes both strict mode values and ERROR\_FOR\_DIVISION\_BY\_ZERO:

```
SET sql_mode='TRADITIONAL';
```

If a number is inserted into an exact type column (DECIMAL or integer), it is inserted with its exact value if it is within the column range and precision.

If the value has too many digits in the fractional part, rounding occurs and a note is generated. Rounding is done as described in [Section 14.24.4, "Rounding Behavior"](#page-40-0). Truncation due to rounding of the fractional part is not an error, even in strict mode.

If the value has too many digits in the integer part, it is too large (out of range) and is handled as follows:

- If strict mode is not enabled, the value is truncated to the nearest legal value and a warning is generated.
- If strict mode is enabled, an overflow error occurs.

Prior to MySQL 8.0.31, for DECIMAL literals, in addition to the precision limit of 65 digits, there is a limit on how long the text of the literal can be. If the value exceeds approximately 80 characters, unexpected results can occur. For example:

```
mysql> SELECT
 CAST(0000000000000000000000000000000000000000000000000000000000000000000000000000000020.01 AS DECIMAL(15,2)) as val;
+------------------+
| val |
+------------------+
| 9999999999999.99 |
+------------------+
1 row in set, 2 warnings (0.00 sec)
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------+
| Level | Code | Message |
+---------+------+----------------------------------------------+
| Warning | 1292 | Truncated incorrect DECIMAL value: '20' |
| Warning | 1264 | Out of range value for column 'val' at row 1 |
+---------+------+----------------------------------------------+
2 rows in set (0.00 sec)
```

As of MySQL 8.0.31, this should no longer be an issue, as shown here:

```
mysql> SELECT
 CAST(0000000000000000000000000000000000000000000000000000000000000000000000000000000020.01 AS DECIMAL(15,2)) as val;
+-------+
| val |
+-------+
| 20.01 |
+-------+
1 row in set (0.00 sec)
```

Underflow is not detected, so underflow handling is undefined.

For inserts of strings into numeric columns, conversion from string to number is handled as follows if the string has nonnumeric contents:

• A string that does not begin with a number cannot be used as a number and produces an error in strict mode, or a warning otherwise. This includes the empty string.

• A string that begins with a number can be converted, but the trailing nonnumeric portion is truncated. If the truncated portion contains anything other than spaces, this produces an error in strict mode, or a warning otherwise.

By default, division by zero produces a result of NULL and no warning. By setting the SQL mode appropriately, division by zero can be restricted.

With the ERROR\_FOR\_DIVISION\_BY\_ZERO SQL mode enabled, MySQL handles division by zero differently:

- If strict mode is not enabled, a warning occurs.
- If strict mode is enabled, inserts and updates involving division by zero are prohibited, and an error occurs.

In other words, inserts and updates involving expressions that perform division by zero can be treated as errors, but this requires ERROR\_FOR\_DIVISION\_BY\_ZERO in addition to strict mode.

Suppose that we have this statement:

```
INSERT INTO t SET i = 1/0;
```

This is what happens for combinations of strict and ERROR\_FOR\_DIVISION\_BY\_ZERO modes.

| sql_mode Value                    | Result                                  |
|-----------------------------------|-----------------------------------------|
| '' (Default)                      | No warning, no error; i is set to NULL. |
| strict                            | No warning, no error; i is set to NULL. |
| ERROR_FOR_DIVISION_BY_ZERO        | Warning, no error; i is set to NULL.    |
| strict,ERROR_FOR_DIVISION_BY_ZERO | Error condition; no row is inserted.    |

# <span id="page-40-0"></span>**14.24.4 Rounding Behavior**

This section discusses precision math rounding for the ROUND() function and for inserts into columns with exact-value types (DECIMAL and integer).

The ROUND() function rounds differently depending on whether its argument is exact or approximate:

- For exact-value numbers, ROUND() uses the "round half up" rule: A value with a fractional part of .5 or greater is rounded up to the next integer if positive or down to the next integer if negative. (In other words, it is rounded away from zero.) A value with a fractional part less than .5 is rounded down to the next integer if positive or up to the next integer if negative. (In other words, it is rounded toward zero.)
- For approximate-value numbers, the result depends on the C library. On many systems, this means that ROUND() uses the "round to nearest even" rule: A value with a fractional part exactly half way between two integers is rounded to the nearest even integer.

The following example shows how rounding differs for exact and approximate values:

```
mysql> SELECT ROUND(2.5), ROUND(25E-1);
+------------+--------------+
| ROUND(2.5) | ROUND(25E-1) |
+------------+--------------+
| 3 | 2 |
+------------+--------------+
```

For inserts into a DECIMAL or integer column, the target is an exact data type, so rounding uses "round half away from zero," regardless of whether the value to be inserted is exact or approximate:

```
mysql> CREATE TABLE t (d DECIMAL(10,0));
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> INSERT INTO t VALUES(2.5),(2.5E0);
Query OK, 2 rows affected, 2 warnings (0.00 sec)
Records: 2 Duplicates: 0 Warnings: 2
mysql> SHOW WARNINGS;
+-------+------+----------------------------------------+
| Level | Code | Message |
+-------+------+----------------------------------------+
| Note | 1265 | Data truncated for column 'd' at row 1 |
| Note | 1265 | Data truncated for column 'd' at row 2 |
+-------+------+----------------------------------------+
2 rows in set (0.00 sec)
mysql> SELECT d FROM t;
+------+
| d |
+------+
| 3 |
| 3 |
+------+
2 rows in set (0.00 sec)
```

The SHOW WARNINGS statement displays the notes that are generated by truncation due to rounding of the fractional part. Such truncation is not an error, even in strict SQL mode (see [Section 14.24.3,](#page-38-0) ["Expression Handling"](#page-38-0)).