---
source: MySQL 5.7 Reference
title: 00_Overview
---

**Table 12.8 Numeric Functions and Operators**

| Name            | Description                                                       |
|-----------------|-------------------------------------------------------------------|
| %, MOD          | Modulo operator                                                   |
| *               | Multiplication operator                                           |
| +               | Addition operator                                                 |
| -               | Minus operator                                                    |
| -               | Change the sign of the argument                                   |
| /               | Division operator                                                 |
| ABS()           | Return the absolute value                                         |
| ACOS()          | Return the arc cosine                                             |
| ASIN()          | Return the arc sine                                               |
| ATAN()          | Return the arc tangent                                            |
| ATAN2(), ATAN() | Return the arc tangent of the two arguments                       |
| CEIL()          | Return the smallest integer value not less than the<br>argument   |
| CEILING()       | Return the smallest integer value not less than the<br>argument   |
| CONV()          | Convert numbers between different number bases                    |
| COS()           | Return the cosine                                                 |
| COT()           | Return the cotangent                                              |
| CRC32()         | Compute a cyclic redundancy check value                           |
| DEGREES()       | Convert radians to degrees                                        |
| DIV             | Integer division                                                  |
| EXP()           | Raise to the power of                                             |
| FLOOR()         | Return the largest integer value not greater than<br>the argument |
| LN()            | Return the natural logarithm of the argument                      |
| LOG()           | Return the natural logarithm of the first argument                |
| LOG10()         | Return the base-10 logarithm of the argument                      |
| LOG2()          | Return the base-2 logarithm of the argument                       |
| MOD()           | Return the remainder                                              |
| PI()            | Return the value of pi                                            |
| POW()           | Return the argument raised to the specified power                 |
| POWER()         | Return the argument raised to the specified power                 |
| RADIANS()       | Return argument converted to radians                              |
| RAND()          | Return a random floating-point value                              |
| ROUND()         | Round the argument                                                |
| SIGN()          | Return the sign of the argument                                   |
| SIN()           | Return the sine of the argument                                   |
| SQRT()          | Return the square root of the argument                            |
| TAN()           | Return the tangent of the argument                                |

| Name       | Description                                    |
|------------|------------------------------------------------|
| TRUNCATE() | Truncate to specified number of decimal places |

## <span id="page-5-2"></span>**12.6.1 Arithmetic Operators**

### **Table 12.9 Arithmetic Operators**

| Name   | Description                     |
|--------|---------------------------------|
| %, MOD | Modulo operator                 |
| *      | Multiplication operator         |
| +      | Addition operator               |
| -      | Minus operator                  |
| -      | Change the sign of the argument |
| /      | Division operator               |
| DIV    | Integer division                |

The usual arithmetic operators are available. The result is determined according to the following rules:

- In the case of [-](#page-5-1), [+](#page-5-0), and [\\*](#page-6-1), the result is calculated with BIGINT (64-bit) precision if both operands are integers.
- If both operands are integers and any of them are unsigned, the result is an unsigned integer. For subtraction, if the NO\_UNSIGNED\_SUBTRACTION SQL mode is enabled, the result is signed even if any operand is unsigned.
- If any of the operands of a [+](#page-5-0), [-](#page-5-1), [/](#page-6-3), [\\*](#page-6-1), [%](#page-6-0) is a real or string value, the precision of the result is the precision of the operand with the maximum precision.
- In division performed with [/](#page-6-3), the scale of the result when using two exact-value operands is the scale of the first operand plus the value of the div\_precision\_increment system variable (which is 4 by default). For example, the result of the expression 5.05 / 0.014 has a scale of six decimal places (360.714286).

These rules are applied for each operation, such that nested calculations imply the precision of each component. Hence, (14620 / 9432456) / (24250 / 9432456), resolves first to (0.0014) / (0.0026), with the final result having 8 decimal places (0.60288653).

Because of these rules and the way they are applied, care should be taken to ensure that components and subcomponents of a calculation use the appropriate level of precision. See [Section 12.10, "Cast](#page-88-0) [Functions and Operators"](#page-88-0).

For information about handling of overflow in numeric expression evaluation, see Section 11.1.7, "Outof-Range and Overflow Handling".

Arithmetic operators apply to numbers. For other types of values, alternative operations may be available. For example, to add date values, use [DATE\\_ADD\(\)](#page-19-0); see [Section 12.7, "Date and Time](#page-15-2) [Functions".](#page-15-2)

<span id="page-5-0"></span>• [+](#page-5-0)

#### Addition:

```
mysql> SELECT 3+5;
 -> 8
```

<span id="page-5-1"></span>• [-](#page-5-1)

#### Subtraction:

```
mysql> SELECT 3-5;
```

-> -2

<span id="page-6-2"></span>• [-](#page-6-2)

Unary minus. This operator changes the sign of the operand.

```
mysql> SELECT - 2;
 -> -2
```

![](_page_6_Picture_5.jpeg)

#### **Note**

If this operator is used with a BIGINT, the return value is also a BIGINT. This means that you should avoid using - on integers that may have the value of −2 63 .

<span id="page-6-1"></span>• [\\*](#page-6-1)

#### Multiplication:

```
mysql> SELECT 3*5;
 -> 15
mysql> SELECT 18014398509481984*18014398509481984.0;
 -> 324518553658426726783156020576256.0
mysql> SELECT 18014398509481984*18014398509481984;
 -> out-of-range error
```

The last expression produces an error because the result of the integer multiplication exceeds the 64-bit range of BIGINT calculations. (See Section 11.1, "Numeric Data Types".)

<span id="page-6-3"></span>• [/](#page-6-3)

Division:

```
mysql> SELECT 3/5;
 -> 0.60
```

Division by zero produces a NULL result:

```
mysql> SELECT 102/(1-1);
 -> NULL
```

A division is calculated with BIGINT arithmetic only if performed in a context where its result is converted to an integer.

<span id="page-6-4"></span>• [DIV](#page-6-4)

Integer division. Discards from the division result any fractional part to the right of the decimal point.

If either operand has a noninteger type, the operands are converted to DECIMAL and divided using DECIMAL arithmetic before converting the result to BIGINT. If the result exceeds BIGINT range, an error occurs.

```
mysql> SELECT 5 DIV 2, -5 DIV 2, 5 DIV -2, -5 DIV -2;
 -> 2, -2, -2, 2
```

<span id="page-6-0"></span>• N [%](#page-6-0) M, N [MOD](#page-6-0) M

Modulo operation. Returns the remainder of N divided by M. For more information, see the description for the [MOD\(\)](#page-11-2) function in [Section 12.6.2, "Mathematical Functions"](#page-7-1).

## <span id="page-7-1"></span>**12.6.2 Mathematical Functions**

**Table 12.10 Mathematical Functions**

| Name            | Description                                                       |  |  |
|-----------------|-------------------------------------------------------------------|--|--|
| ABS()           | Return the absolute value                                         |  |  |
| ACOS()          | Return the arc cosine                                             |  |  |
| ASIN()          | Return the arc sine                                               |  |  |
| ATAN()          | Return the arc tangent                                            |  |  |
| ATAN2(), ATAN() | Return the arc tangent of the two arguments                       |  |  |
| CEIL()          | Return the smallest integer value not less than the<br>argument   |  |  |
| CEILING()       | Return the smallest integer value not less than the<br>argument   |  |  |
| CONV()          | Convert numbers between different number bases                    |  |  |
| COS()           | Return the cosine                                                 |  |  |
| COT()           | Return the cotangent                                              |  |  |
| CRC32()         | Compute a cyclic redundancy check value                           |  |  |
| DEGREES()       | Convert radians to degrees                                        |  |  |
| EXP()           | Raise to the power of                                             |  |  |
| FLOOR()         | Return the largest integer value not greater than<br>the argument |  |  |
| LN()            | Return the natural logarithm of the argument                      |  |  |
| LOG()           | Return the natural logarithm of the first argument                |  |  |
| LOG10()         | Return the base-10 logarithm of the argument                      |  |  |
| LOG2()          | Return the base-2 logarithm of the argument                       |  |  |
| MOD()           | Return the remainder                                              |  |  |
| PI()            | Return the value of pi                                            |  |  |
| POW()           | Return the argument raised to the specified power                 |  |  |
| POWER()         | Return the argument raised to the specified power                 |  |  |
| RADIANS()       | Return argument converted to radians                              |  |  |
| RAND()          | Return a random floating-point value                              |  |  |
| ROUND()         | Round the argument                                                |  |  |
| SIGN()          | Return the sign of the argument                                   |  |  |
| SIN()           | Return the sine of the argument                                   |  |  |
| SQRT()          | Return the square root of the argument                            |  |  |
| TAN()           | Return the tangent of the argument                                |  |  |
| TRUNCATE()      | Truncate to specified number of decimal places                    |  |  |

All mathematical functions return NULL in the event of an error.

<span id="page-7-0"></span>• [ABS\(](#page-7-0)X)

Returns the absolute value of X, or NULL if X is NULL.

The result type is derived from the argument type. An implication of this is that [ABS\(-9223372036854775808\)](#page-7-0) produces an error because the result cannot be stored in a signed BIGINT value.

```
mysql> SELECT ABS(2);
 -> 2
mysql> SELECT ABS(-32);
 -> 32
```

This function is safe to use with BIGINT values.

<span id="page-8-0"></span>• [ACOS\(](#page-8-0)X)

Returns the arc cosine of X, that is, the value whose cosine is X. Returns NULL if X is not in the range -1 to 1.

```
mysql> SELECT ACOS(1);
 -> 0
mysql> SELECT ACOS(1.0001);
 -> NULL
mysql> SELECT ACOS(0);
 -> 1.5707963267949
```

<span id="page-8-1"></span>• [ASIN\(](#page-8-1)X)

Returns the arc sine of X, that is, the value whose sine is X. Returns NULL if X is not in the range -1 to 1.

```
mysql> SELECT ASIN(0.2);
 -> 0.20135792079033
mysql> SELECT ASIN('foo');
+-------------+
| ASIN('foo') |
+-------------+
| 0 |
+-------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------+
| Level | Code | Message |
+---------+------+-----------------------------------------+
| Warning | 1292 | Truncated incorrect DOUBLE value: 'foo' |
+---------+------+-----------------------------------------+
```

<span id="page-8-2"></span>• [ATAN\(](#page-8-2)X)

Returns the arc tangent of X, that is, the value whose tangent is X.

```
mysql> SELECT ATAN(2);
 -> 1.1071487177941
mysql> SELECT ATAN(-2);
 -> -1.1071487177941
```

<span id="page-8-3"></span>• [ATAN\(](#page-8-3)Y,X), [ATAN2\(](#page-8-3)Y,X)

Returns the arc tangent of the two variables X and Y. It is similar to calculating the arc tangent of Y / X, except that the signs of both arguments are used to determine the quadrant of the result.

```
mysql> SELECT ATAN(-2,2);
 -> -0.78539816339745
mysql> SELECT ATAN2(PI(),0);
 -> 1.5707963267949
```

<span id="page-8-4"></span>• [CEIL\(](#page-8-4)X)

[CEIL\(\)](#page-8-4) is a synonym for [CEILING\(\)](#page-8-5).

<span id="page-8-5"></span>• [CEILING\(](#page-8-5)X)

Returns the smallest integer value not less than X.

```
mysql> SELECT CEILING(1.23);
 -> 2
mysql> SELECT CEILING(-1.23);
 -> -1
```

For exact-value numeric arguments, the return value has an exact-value numeric type. For string or floating-point arguments, the return value has a floating-point type.

<span id="page-9-0"></span>• CONV(N,[from\\_base](#page-9-0),to\_base)

Converts numbers between different number bases. Returns a string representation of the number N, converted from base from\_base to base to\_base. Returns NULL if any argument is NULL. The argument N is interpreted as an integer, but may be specified as an integer or a string. The minimum base is 2 and the maximum base is 36. If from\_base is a negative number, N is regarded as a signed number. Otherwise, N is treated as unsigned. [CONV\(\)](#page-9-0) works with 64-bit precision.

```
mysql> SELECT CONV('a',16,2);
 -> '1010'
mysql> SELECT CONV('6E',18,8);
 -> '172'
mysql> SELECT CONV(-17,10,-18);
 -> '-H'
mysql> SELECT CONV(10+'10'+'10'+X'0a',10,10);
 -> '40'
```

<span id="page-9-1"></span>• [COS\(](#page-9-1)X)

Returns the cosine of X, where X is given in radians.

```
mysql> SELECT COS(PI());
 -> -1
```

<span id="page-9-2"></span>• [COT\(](#page-9-2)X)

Returns the cotangent of X.

```
mysql> SELECT COT(12);
 -> -1.5726734063977
mysql> SELECT COT(0);
 -> out-of-range error
```

<span id="page-9-3"></span>• [CRC32\(](#page-9-3)expr)

Computes a cyclic redundancy check value and returns a 32-bit unsigned value. The result is NULL if the argument is NULL. The argument is expected to be a string and (if possible) is treated as one if it is not.

```
mysql> SELECT CRC32('MySQL');
 -> 3259397556
mysql> SELECT CRC32('mysql');
 -> 2501908538
```

<span id="page-9-4"></span>• [DEGREES\(](#page-9-4)X)

Returns the argument X, converted from radians to degrees.

```
mysql> SELECT DEGREES(PI());
 -> 180
mysql> SELECT DEGREES(PI() / 2);
 -> 90
```

### <span id="page-10-0"></span>• [EXP\(](#page-10-0)X)

Returns the value of e (the base of natural logarithms) raised to the power of X. The inverse of this function is [LOG\(\)](#page-10-3) (using a single argument only) or [LN\(\)](#page-10-2).

```
mysql> SELECT EXP(2);
 -> 7.3890560989307
mysql> SELECT EXP(-2);
 -> 0.13533528323661
mysql> SELECT EXP(0);
 -> 1
```

### <span id="page-10-1"></span>• [FLOOR\(](#page-10-1)X)

Returns the largest integer value not greater than X.

```
mysql> SELECT FLOOR(1.23), FLOOR(-1.23);
 -> 1, -2
```

For exact-value numeric arguments, the return value has an exact-value numeric type. For string or floating-point arguments, the return value has a floating-point type.

• [FORMAT\(](#page-41-0)X,D)

Formats the number X to a format like '#,###,###.##', rounded to D decimal places, and returns the result as a string. For details, see [Section 12.8, "String Functions and Operators".](#page-36-0)

• [HEX\(N\\_or\\_S\)](#page-41-1)

This function can be used to obtain a hexadecimal representation of a decimal number or a string; the manner in which it does so varies according to the argument's type. See this function's description in [Section 12.8, "String Functions and Operators"](#page-36-0), for details.

<span id="page-10-2"></span>• [LN\(](#page-10-2)X)

Returns the natural logarithm of X; that is, the base-e logarithm of X. If X is less than or equal to 0.0E0, the function returns NULL and a warning "Invalid argument for logarithm" is reported.

```
mysql> SELECT LN(2);
 -> 0.69314718055995
mysql> SELECT LN(-2);
 -> NULL
```

This function is synonymous with [LOG\(](#page-10-3)X). The inverse of this function is the [EXP\(\)](#page-10-0) function.

<span id="page-10-3"></span>• [LOG\(](#page-10-3)X), [LOG\(](#page-10-3)B,X)

If called with one parameter, this function returns the natural logarithm of X. If X is less than or equal to 0.0E0, the function returns NULL and a warning "Invalid argument for logarithm" is reported.

The inverse of this function (when called with a single argument) is the [EXP\(\)](#page-10-0) function.

```
mysql> SELECT LOG(2);
 -> 0.69314718055995
mysql> SELECT LOG(-2);
 -> NULL
```

If called with two parameters, this function returns the logarithm of X to the base B. If X is less than or equal to 0, or if B is less than or equal to 1, then NULL is returned.

```
mysql> SELECT LOG(2,65536);
 -> 16
mysql> SELECT LOG(10,100);
 -> 2
mysql> SELECT LOG(1,100);
 -> NULL
```

[LOG\(](#page-10-3)B,X) is equivalent to LOG(X[\) / LOG\(](#page-10-3)B).

<span id="page-11-1"></span>• [LOG2\(](#page-11-1)X)

Returns the base-2 logarithm of X. If X is less than or equal to 0.0E0, the function returns NULL and a warning "Invalid argument for logarithm" is reported.

```
mysql> SELECT LOG2(65536);
 -> 16
mysql> SELECT LOG2(-100);
 -> NULL
```

[LOG2\(\)](#page-11-1) is useful for finding out how many bits a number requires for storage. This function is approximately equivalent to the expression LOG(X[\) / LOG\(2\)](#page-10-3).

<span id="page-11-0"></span>• [LOG10\(](#page-11-0)X)

Returns the base-10 logarithm of X. If X is less than or equal to 0.0E0, the function returns NULL and a warning "Invalid argument for logarithm" is reported.

```
mysql> SELECT LOG10(2);
 -> 0.30102999566398
mysql> SELECT LOG10(100);
 -> 2
mysql> SELECT LOG10(-100);
 -> NULL
```

[LOG10\(](#page-11-0)X) is approximately equivalent to [LOG\(10,](#page-10-3)X).

<span id="page-11-2"></span>• [MOD\(](#page-11-2)N,M), N [%](#page-6-0) M, N [MOD](#page-6-0) M

Modulo operation. Returns the remainder of N divided by M.

```
mysql> SELECT MOD(234, 10);
 -> 4
mysql> SELECT 253 % 7;
 -> 1
mysql> SELECT MOD(29,9);
 -> 2
mysql> SELECT 29 MOD 9;
 -> 2
```

This function is safe to use with BIGINT values.

[MOD\(\)](#page-11-2) also works on values that have a fractional part and returns the exact remainder after division:

```
mysql> SELECT MOD(34.5,3);
 -> 1.5
MOD(N,0) returns NULL.
```

<span id="page-11-3"></span>• [PI\(\)](#page-11-3)

Returns the value of π (pi). The default number of decimal places displayed is seven, but MySQL uses the full double-precision value internally.

Because the return value of this function is a double-precision value, its exact representation may vary between platforms or implementations. This also applies to any expressions making use of PI(). See Section 11.1.4, "Floating-Point Types (Approximate Value) - FLOAT, DOUBLE".

```
mysql> SELECT PI();
 -> 3.141593
mysql> SELECT PI()+0.000000000000000000;
 -> 3.141592653589793000
```

<span id="page-12-0"></span>• [POW\(](#page-12-0)X,Y)

Returns the value of X raised to the power of Y.

```
mysql> SELECT POW(2,2);
 -> 4
mysql> SELECT POW(2,-2);
 -> 0.25
```

<span id="page-12-1"></span>• [POWER\(](#page-12-1)X,Y)

This is a synonym for [POW\(\)](#page-12-0).

<span id="page-12-2"></span>• [RADIANS\(](#page-12-2)X)

Returns the argument X, converted from degrees to radians. (Note that π radians equals 180 degrees.)

```
mysql> SELECT RADIANS(90);
 -> 1.5707963267949
```

<span id="page-12-3"></span>• [RAND\(\[](#page-12-3)N])

Returns a random floating-point value v in the range 0 <= v < 1.0. To obtain a random integer R in the range i <= R < j, use the expression FLOOR(i [+ RAND\(\) \\* \(](#page-10-1)j − i)). For example, to obtain a random integer in the range the range 7 <= R < 12, use the following statement:

```
SELECT FLOOR(7 + (RAND() * 5));
```

If an integer argument N is specified, it is used as the seed value:

- With a constant initializer argument, the seed is initialized once when the statement is prepared, prior to execution.
- With a nonconstant initializer argument (such as a column name), the seed is initialized with the value for each invocation of [RAND\(\)](#page-12-3).

One implication of this behavior is that for equal argument values, [RAND\(](#page-12-3)N) returns the same value each time, and thus produces a repeatable sequence of column values. In the following example, the sequence of values produced by RAND(3) is the same both places it occurs.

```
mysql> CREATE TABLE t (i INT);
Query OK, 0 rows affected (0.42 sec)
mysql> INSERT INTO t VALUES(1),(2),(3);
Query OK, 3 rows affected (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT i, RAND() FROM t;
+------+------------------+
| i | RAND() |
+------+------------------+
| 1 | 0.61914388706828 |
| 2 | 0.93845168309142 |
| 3 | 0.83482678498591 |
+------+------------------+
3 rows in set (0.00 sec)
mysql> SELECT i, RAND(3) FROM t;
+------+------------------+
| i | RAND(3) |
+------+------------------+
| 1 | 0.90576975597606 |
| 2 | 0.37307905813035 |
| 3 | 0.14808605345719 |
+------+------------------+
3 rows in set (0.00 sec)
```

```
mysql> SELECT i, RAND() FROM t;
+------+------------------+
| i | RAND() |
+------+------------------+
| 1 | 0.35877890638893 |
| 2 | 0.28941420772058 |
| 3 | 0.37073435016976 |
+------+------------------+
3 rows in set (0.00 sec)
mysql> SELECT i, RAND(3) FROM t;
+------+------------------+
| i | RAND(3) |
+------+------------------+
| 1 | 0.90576975597606 |
| 2 | 0.37307905813035 |
| 3 | 0.14808605345719 |
+------+------------------+
3 rows in set (0.01 sec)
```

[RAND\(\)](#page-12-3) in a WHERE clause is evaluated for every row (when selecting from one table) or combination of rows (when selecting from a multiple-table join). Thus, for optimizer purposes, [RAND\(\)](#page-12-3) is not a constant value and cannot be used for index optimizations. For more information, see Section 8.2.1.18, "Function Call Optimization".

Use of a column with [RAND\(\)](#page-12-3) values in an ORDER BY or GROUP BY clause may yield unexpected results because for either clause a [RAND\(\)](#page-12-3) expression can be evaluated multiple times for the same row, each time returning a different result. If the goal is to retrieve rows in random order, you can use a statement like this:

```
SELECT * FROM tbl_name ORDER BY RAND();
```

To select a random sample from a set of rows, combine ORDER BY RAND() with LIMIT:

```
SELECT * FROM table1, table2 WHERE a=b AND c<d ORDER BY RAND() LIMIT 1000;
```

[RAND\(\)](#page-12-3) is not meant to be a perfect random generator. It is a fast way to generate random numbers on demand that is portable between platforms for the same MySQL version.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-13-0"></span>• [ROUND\(](#page-13-0)X), [ROUND\(](#page-13-0)X,D)

Rounds the argument X to D decimal places. The rounding algorithm depends on the data type of X. D defaults to 0 if not specified. D can be negative to cause D digits left of the decimal point of the value X to become zero. The maximum absolute value for D is 30; any digits in excess of 30 (or -30) are truncated.

```
mysql> SELECT ROUND(-1.23);
 -> -1
mysql> SELECT ROUND(-1.58);
 -> -2
mysql> SELECT ROUND(1.58);
 -> 2
mysql> SELECT ROUND(1.298, 1);
 -> 1.3
mysql> SELECT ROUND(1.298, 0);
 -> 1
mysql> SELECT ROUND(23.298, -1);
 -> 20
mysql> SELECT ROUND(.12345678901234567890123456789012345, 35);
```

```
 -> 0.123456789012345678901234567890
```

The return value has the same type as the first argument (assuming that it is integer, double, or decimal). This means that for an integer argument, the result is an integer (no decimal places):

```
mysql> SELECT ROUND(150.000,2), ROUND(150,2);
+------------------+--------------+
| ROUND(150.000,2) | ROUND(150,2) |
+------------------+--------------+
| 150.00 | 150 |
+------------------+--------------+
```

[ROUND\(\)](#page-13-0) uses the following rules depending on the type of the first argument:

- For exact-value numbers, [ROUND\(\)](#page-13-0) uses the "round half away from zero" or "round toward nearest" rule: A value with a fractional part of .5 or greater is rounded up to the next integer if positive or down to the next integer if negative. (In other words, it is rounded away from zero.) A value with a fractional part less than .5 is rounded down to the next integer if positive or up to the next integer if negative.
- For approximate-value numbers, the result depends on the C library. On many systems, this means that [ROUND\(\)](#page-13-0) uses the "round to nearest even" rule: A value with a fractional part exactly halfway between two integers is rounded to the nearest even integer.

The following example shows how rounding differs for exact and approximate values:

```
mysql> SELECT ROUND(2.5), ROUND(25E-1);
+------------+--------------+
| ROUND(2.5) | ROUND(25E-1) |
+------------+--------------+
| 3 | 2 |
+------------+--------------+
```

For more information, see Section 12.21, "Precision Math".

<span id="page-14-0"></span>• [SIGN\(](#page-14-0)X)

Returns the sign of the argument as -1, 0, or 1, depending on whether X is negative, zero, or positive.

```
mysql> SELECT SIGN(-32);
 -> -1
mysql> SELECT SIGN(0);
 -> 0
mysql> SELECT SIGN(234);
 -> 1
```

<span id="page-14-1"></span>• [SIN\(](#page-14-1)X)

Returns the sine of X, where X is given in radians.

```
mysql> SELECT SIN(PI());
 -> 1.2246063538224e-16
mysql> SELECT ROUND(SIN(PI()));
 -> 0
```

<span id="page-14-2"></span>• [SQRT\(](#page-14-2)X)

Returns the square root of a nonnegative number X.

```
mysql> SELECT SQRT(4);
 -> 2
mysql> SELECT SQRT(20);
 -> 4.4721359549996
mysql> SELECT SQRT(-16);
 -> NULL
```

### <span id="page-15-0"></span>• [TAN\(](#page-15-0)X)

Returns the tangent of X, where X is given in radians.

```
mysql> SELECT TAN(PI());
 -> -1.2246063538224e-16
mysql> SELECT TAN(PI()+1);
 -> 1.5574077246549
```

### <span id="page-15-1"></span>• [TRUNCATE\(](#page-15-1)X,D)

Returns the number X, truncated to D decimal places. If D is 0, the result has no decimal point or fractional part. D can be negative to cause D digits left of the decimal point of the value X to become zero.

```
mysql> SELECT TRUNCATE(1.223,1);
 -> 1.2
mysql> SELECT TRUNCATE(1.999,1);
 -> 1.9
mysql> SELECT TRUNCATE(1.999,0);
 -> 1
mysql> SELECT TRUNCATE(-1.999,1);
 -> -1.9
mysql> SELECT TRUNCATE(122,-2);
 -> 100
mysql> SELECT TRUNCATE(10.28*100,0);
 -> 1028
```

All numbers are rounded toward zero.

# <span id="page-15-2"></span>**12.7 Date and Time Functions**

This section describes the functions that can be used to manipulate temporal values. See Section 11.2, "Date and Time Data Types", for a description of the range of values each date and time type has and the valid formats in which values may be specified.

**Table 12.11 Date and Time Functions**

| Name                                   | Description                                               |  |
|----------------------------------------|-----------------------------------------------------------|--|
| ADDDATE()                              | Add time values (intervals) to a date value               |  |
| ADDTIME()                              | Add time                                                  |  |
| CONVERT_TZ()                           | Convert from one time zone to another                     |  |
| CURDATE()                              | Return the current date                                   |  |
| CURRENT_DATE(), CURRENT_DATE           | Synonyms for CURDATE()                                    |  |
| CURRENT_TIME(), CURRENT_TIME           | Synonyms for CURTIME()                                    |  |
| CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP | Synonyms for NOW()                                        |  |
| CURTIME()                              | Return the current time                                   |  |
| DATE()                                 | Extract the date part of a date or datetime<br>expression |  |
| DATE_ADD()                             | Add time values (intervals) to a date value               |  |
| DATE_FORMAT()                          | Format date as specified                                  |  |
| DATE_SUB()                             | Subtract a time value (interval) from a date              |  |
| DATEDIFF()                             | Subtract two dates                                        |  |
| DAY()                                  | Synonym for DAYOFMONTH()                                  |  |
| DAYNAME()                              | Return the name of the weekday                            |  |
| DAYOFMONTH()                           | Return the day of the month (0-31)                        |  |
| DAYOFWEEK()                            | Return the weekday index of the argument                  |  |

| Name                             | Description                                                                                                                       |  |  |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|--|--|
| DAYOFYEAR()                      | Return the day of the year (1-366)                                                                                                |  |  |
| EXTRACT()                        | Extract part of a date                                                                                                            |  |  |
| FROM_DAYS()                      | Convert a day number to a date                                                                                                    |  |  |
| FROM_UNIXTIME()                  | Format Unix timestamp as a date                                                                                                   |  |  |
| GET_FORMAT()                     | Return a date format string                                                                                                       |  |  |
| HOUR()                           | Extract the hour                                                                                                                  |  |  |
| LAST_DAY                         | Return the last day of the month for the argument                                                                                 |  |  |
| LOCALTIME(), LOCALTIME           | Synonym for NOW()                                                                                                                 |  |  |
| LOCALTIMESTAMP, LOCALTIMESTAMP() | Synonym for NOW()                                                                                                                 |  |  |
| MAKEDATE()                       | Create a date from the year and day of year                                                                                       |  |  |
| MAKETIME()                       | Create time from hour, minute, second                                                                                             |  |  |
| MICROSECOND()                    | Return the microseconds from argument                                                                                             |  |  |
| MINUTE()                         | Return the minute from the argument                                                                                               |  |  |
| MONTH()                          | Return the month from the date passed                                                                                             |  |  |
| MONTHNAME()                      | Return the name of the month                                                                                                      |  |  |
| NOW()                            | Return the current date and time                                                                                                  |  |  |
| PERIOD_ADD()                     | Add a period to a year-month                                                                                                      |  |  |
| PERIOD_DIFF()                    | Return the number of months between periods                                                                                       |  |  |
| QUARTER()                        | Return the quarter from a date argument                                                                                           |  |  |
| SEC_TO_TIME()                    | Converts seconds to 'hh:mm:ss' format                                                                                             |  |  |
| SECOND()                         | Return the second (0-59)                                                                                                          |  |  |
| STR_TO_DATE()                    | Convert a string to a date                                                                                                        |  |  |
| SUBDATE()                        | Synonym for DATE_SUB() when invoked with<br>three arguments                                                                       |  |  |
| SUBTIME()                        | Subtract times                                                                                                                    |  |  |
| SYSDATE()                        | Return the time at which the function executes                                                                                    |  |  |
| TIME()                           | Extract the time portion of the expression passed                                                                                 |  |  |
| TIME_FORMAT()                    | Format as time                                                                                                                    |  |  |
| TIME_TO_SEC()                    | Return the argument converted to seconds                                                                                          |  |  |
| TIMEDIFF()                       | Subtract time                                                                                                                     |  |  |
| TIMESTAMP()                      | With a single argument, this function returns the<br>date or datetime expression; with two arguments,<br>the sum of the arguments |  |  |
| TIMESTAMPADD()                   | Add an interval to a datetime expression                                                                                          |  |  |
| TIMESTAMPDIFF()                  | Return the difference of two datetime expressions,<br>using the units specified                                                   |  |  |
| TO_DAYS()                        | Return the date argument converted to days                                                                                        |  |  |
| TO_SECONDS()                     | Return the date or datetime argument converted<br>to seconds since Year 0                                                         |  |  |
|                                  |                                                                                                                                   |  |  |
| UNIX_TIMESTAMP()                 | Return a Unix timestamp                                                                                                           |  |  |
| UTC_DATE()                       | Return the current UTC date                                                                                                       |  |  |

| Name            | Description                                 |  |
|-----------------|---------------------------------------------|--|
| UTC_TIMESTAMP() | Return the current UTC date and time        |  |
| WEEK()          | Return the week number                      |  |
| WEEKDAY()       | Return the weekday index                    |  |
| WEEKOFYEAR()    | Return the calendar week of the date (1-53) |  |
| YEAR()          | Return the year                             |  |
| YEARWEEK()      | Return the year and week                    |  |

Here is an example that uses date functions. The following query selects all rows with a date\_col value from within the last 30 days:

```
mysql> SELECT something FROM tbl_name
 -> WHERE DATE_SUB(CURDATE(),INTERVAL 30 DAY) <= date_col;
```

The query also selects rows with dates that lie in the future.

Functions that expect date values usually accept datetime values and ignore the time part. Functions that expect time values usually accept datetime values and ignore the date part.

Functions that return the current date or time each are evaluated only once per query at the start of query execution. This means that multiple references to a function such as [NOW\(\)](#page-25-4) within a single query always produce the same result. (For our purposes, a single query also includes a call to a stored program (stored routine, trigger, or event) and all subprograms called by that program.) This principle also applies to [CURDATE\(\)](#page-18-2), [CURTIME\(\)](#page-19-1), [UTC\\_DATE\(\)](#page-34-0), [UTC\\_TIME\(\)](#page-34-1), [UTC\\_TIMESTAMP\(\)](#page-34-2), and to any of their synonyms.

The [CURRENT\\_TIMESTAMP\(\)](#page-18-5), [CURRENT\\_TIME\(\)](#page-18-4), [CURRENT\\_DATE\(\)](#page-18-3), and [FROM\\_UNIXTIME\(\)](#page-22-7) functions return values in the current session time zone, which is available as the session value of the time\_zone system variable. In addition, [UNIX\\_TIMESTAMP\(\)](#page-32-1) assumes that its argument is a datetime value in the session time zone. See Section 5.1.13, "MySQL Server Time Zone Support".

Some date functions can be used with "zero" dates or incomplete dates such as '2001-11-00', whereas others cannot. Functions that extract parts of dates typically work with incomplete dates and thus can return 0 when you might otherwise expect a nonzero value. For example:

```
mysql> SELECT DAYOFMONTH('2001-11-00'), MONTH('2005-00-00');
 -> 0, 0
```

Other functions expect complete dates and return NULL for incomplete dates. These include functions that perform date arithmetic or that map parts of dates to names. For example:

```
mysql> SELECT DATE_ADD('2006-05-00',INTERVAL 1 DAY);
 -> NULL
mysql> SELECT DAYNAME('2006-05-00');
 -> NULL
```

Several functions are strict when passed a [DATE\(\)](#page-19-2) function value as their argument and reject incomplete dates with a day part of zero: [CONVERT\\_TZ\(\)](#page-18-1), [DATE\\_ADD\(\)](#page-19-0), [DATE\\_SUB\(\)](#page-21-0), [DAYOFYEAR\(\)](#page-22-4), [TIMESTAMPDIFF\(\)](#page-30-2), [TO\\_DAYS\(\)](#page-31-2), [TO\\_SECONDS\(\)](#page-32-0), [WEEK\(\)](#page-34-3), [WEEKDAY\(\)](#page-35-0), [WEEKOFYEAR\(\)](#page-35-1), [YEARWEEK\(\)](#page-36-1).

Fractional seconds for TIME, DATETIME, and TIMESTAMP values are supported, with up to microsecond precision. Functions that take temporal arguments accept values with fractional seconds. Return values from temporal functions include fractional seconds as appropriate.

<span id="page-17-0"></span>• ADDDATE(date[,INTERVAL](#page-17-0) expr unit), [ADDDATE\(](#page-17-0)expr,days)

When invoked with the INTERVAL form of the second argument, [ADDDATE\(\)](#page-17-0) is a synonym for [DATE\\_ADD\(\)](#page-19-0). The related function [SUBDATE\(\)](#page-28-0) is a synonym for [DATE\\_SUB\(\)](#page-21-0). For information on the INTERVAL unit argument, see Temporal Intervals.

```
mysql> SELECT DATE_ADD('2008-01-02', INTERVAL 31 DAY);
 -> '2008-02-02'
mysql> SELECT ADDDATE('2008-01-02', INTERVAL 31 DAY);
 -> '2008-02-02'
```

When invoked with the days form of the second argument, MySQL treats it as an integer number of days to be added to expr.

```
mysql> SELECT ADDDATE('2008-01-02', 31);
 -> '2008-02-02'
```

<span id="page-18-0"></span>• [ADDTIME\(](#page-18-0)expr1,expr2)

[ADDTIME\(\)](#page-18-0) adds expr2 to expr1 and returns the result. expr1 is a time or datetime expression, and expr2 is a time expression.

```
mysql> SELECT ADDTIME('2007-12-31 23:59:59.999999', '1 1:1:1.000002');
 -> '2008-01-02 01:01:01.000001'
mysql> SELECT ADDTIME('01:00:00.999999', '02:00:00.999998');
 -> '03:00:01.999997'
```

<span id="page-18-1"></span>• [CONVERT\\_TZ\(](#page-18-1)dt,from\_tz,to\_tz)

[CONVERT\\_TZ\(\)](#page-18-1) converts a datetime value dt from the time zone given by from\_tz to the time zone given by to\_tz and returns the resulting value. Time zones are specified as described in Section 5.1.13, "MySQL Server Time Zone Support". This function returns NULL if the arguments are invalid.

If the value falls out of the supported range of the TIMESTAMP type when converted from from\_tz to UTC, no conversion occurs. The TIMESTAMP range is described in Section 11.2.1, "Date and Time Data Type Syntax".

```
mysql> SELECT CONVERT_TZ('2004-01-01 12:00:00','GMT','MET');
 -> '2004-01-01 13:00:00'
mysql> SELECT CONVERT_TZ('2004-01-01 12:00:00','+00:00','+10:00');
 -> '2004-01-01 22:00:00'
```

![](_page_18_Picture_11.jpeg)

### **Note**

To use named time zones such as 'MET' or 'Europe/Amsterdam', the time zone tables must be properly set up. For instructions, see Section 5.1.13, "MySQL Server Time Zone Support".

<span id="page-18-2"></span>• [CURDATE\(\)](#page-18-2)

Returns the current date as a value in 'YYYY-MM-DD' or YYYYMMDD format, depending on whether the function is used in string or numeric context.

```
mysql> SELECT CURDATE();
 -> '2008-06-13'
mysql> SELECT CURDATE() + 0;
 -> 20080613
```

<span id="page-18-3"></span>• [CURRENT\\_DATE](#page-18-3), [CURRENT\\_DATE\(\)](#page-18-3)

[CURRENT\\_DATE](#page-18-3) and [CURRENT\\_DATE\(\)](#page-18-3) are synonyms for [CURDATE\(\)](#page-18-2).

<span id="page-18-4"></span>• [CURRENT\\_TIME](#page-18-4), [CURRENT\\_TIME\(\[](#page-18-4)fsp])

[CURRENT\\_TIME](#page-18-4) and [CURRENT\\_TIME\(\)](#page-18-4) are synonyms for [CURTIME\(\)](#page-19-1).

<span id="page-18-5"></span>• [CURRENT\\_TIMESTAMP](#page-18-5), [CURRENT\\_TIMESTAMP\(\[](#page-18-5)fsp])

[CURRENT\\_TIMESTAMP](#page-18-5) and [CURRENT\\_TIMESTAMP\(\)](#page-18-5) are synonyms for [NOW\(\)](#page-25-4).

### <span id="page-19-1"></span>• [CURTIME\(\[](#page-19-1)fsp])

Returns the current time as a value in 'hh:mm:ss' or hhmmss format, depending on whether the function is used in string or numeric context. The value is expressed in the session time zone.

If the fsp argument is given to specify a fractional seconds precision from 0 to 6, the return value includes a fractional seconds part of that many digits.

```
mysql> SELECT CURTIME();
 -> '23:50:26'
mysql> SELECT CURTIME() + 0;
 -> 235026.000000
```

<span id="page-19-2"></span>• [DATE\(](#page-19-2)expr)

Extracts the date part of the date or datetime expression expr.

```
mysql> SELECT DATE('2003-12-31 01:02:03');
 -> '2003-12-31'
```

<span id="page-19-3"></span>• [DATEDIFF\(](#page-19-3)expr1,expr2)

[DATEDIFF\(\)](#page-19-3) returns expr1 − expr2 expressed as a value in days from one date to the other. expr1 and expr2 are date or date-and-time expressions. Only the date parts of the values are used in the calculation.

```
mysql> SELECT DATEDIFF('2007-12-31 23:59:59','2007-12-30');
 -> 1
mysql> SELECT DATEDIFF('2010-11-30 23:59:59','2010-12-31');
 -> -31
```

<span id="page-19-0"></span>• DATE\_ADD(date[,INTERVAL](#page-19-0) expr unit), DATE\_SUB(date[,INTERVAL](#page-21-0) expr unit)

These functions perform date arithmetic. The date argument specifies the starting date or datetime value. expr is an expression specifying the interval value to be added or subtracted from the starting date. expr is evaluated as a string; it may start with a - for negative intervals. unit is a keyword indicating the units in which the expression should be interpreted.

For more information about temporal interval syntax, including a full list of unit specifiers, the expected form of the expr argument for each unit value, and rules for operand interpretation in temporal arithmetic, see Temporal Intervals.

The return value depends on the arguments:

- DATE if the date argument is a DATE value and your calculations involve only YEAR, MONTH, and DAY parts (that is, no time parts).
- DATETIME if the first argument is a DATETIME (or TIMESTAMP) value, or if the first argument is a DATE and the unit value uses HOURS, MINUTES, or SECONDS.
- String otherwise.

To ensure that the result is DATETIME, you can use [CAST\(\)](#page-89-0) to convert the first argument to DATETIME.

```
mysql> SELECT DATE_ADD('2018-05-01',INTERVAL 1 DAY);
 -> '2018-05-02'
mysql> SELECT DATE_SUB('2018-05-01',INTERVAL 1 YEAR);
 -> '2017-05-01'
mysql> SELECT DATE_ADD('2020-12-31 23:59:59',
 -> INTERVAL 1 SECOND);
 -> '2021-01-01 00:00:00'
mysql> SELECT DATE_ADD('2018-12-31 23:59:59',
 -> INTERVAL 1 DAY);
 -> '2019-01-01 23:59:59'
```

```
mysql> SELECT DATE_ADD('2100-12-31 23:59:59',
 -> INTERVAL '1:1' MINUTE_SECOND);
 -> '2101-01-01 00:01:00'
mysql> SELECT DATE_SUB('2025-01-01 00:00:00',
 -> INTERVAL '1 1:1:1' DAY_SECOND);
 -> '2024-12-30 22:58:59'
mysql> SELECT DATE_ADD('1900-01-01 00:00:00',
 -> INTERVAL '-1 10' DAY_HOUR);
 -> '1899-12-30 14:00:00'
mysql> SELECT DATE_SUB('1998-01-02', INTERVAL 31 DAY);
 -> '1997-12-02'
mysql> SELECT DATE_ADD('1992-12-31 23:59:59.000002',
 -> INTERVAL '1.999999' SECOND_MICROSECOND);
 -> '1993-01-01 00:00:01.000001'
```

When adding a MONTH interval to a DATE or DATETIME value, and the resulting date includes a day that does not exist in the given month, the day is adjusted to the last day of the month, as shown here:

```
mysql> SELECT DATE_ADD('2024-03-30', INTERVAL 1 MONTH) AS d1,
 > DATE_ADD('2024-03-31', INTERVAL 1 MONTH) AS d2;
+------------+------------+
| d1 | d2 |
+------------+------------+
| 2024-04-30 | 2024-04-30 |
+------------+------------+
1 row in set (0.00 sec)
```

<span id="page-20-0"></span>• [DATE\\_FORMAT\(](#page-20-0)date,format)

Formats the date value according to the format string.

The specifiers shown in the following table may be used in the format string. The % character is required before format specifier characters. The specifiers apply to other functions as well: [STR\\_TO\\_DATE\(\)](#page-26-5), [TIME\\_FORMAT\(\)](#page-31-0), [UNIX\\_TIMESTAMP\(\)](#page-32-1).

| Specifier | Description                                                     |
|-----------|-----------------------------------------------------------------|
| %a        | Abbreviated weekday name (SunSat)                               |
| %b        | Abbreviated month name (JanDec)                                 |
| %c        | Month, numeric (012)                                            |
| %D        | Day of the month with English suffix (0th, 1st,<br>2nd, 3rd, …) |
| %d        | Day of the month, numeric (0031)                                |
| %e        | Day of the month, numeric (031)                                 |
| %f        | Microseconds (000000999999)                                     |
| %H        | Hour (0023)                                                     |
| %h        | Hour (0112)                                                     |
| %I        | Hour (0112)                                                     |
| %i        | Minutes, numeric (0059)                                         |
| %j        | Day of year (001366)                                            |
| %k        | Hour (023)                                                      |
| %l        | Hour (112)                                                      |
| %M        | Month name (JanuaryDecember)                                    |
| %m        | Month, numeric (0012)                                           |
| %p        | AM or PM                                                        |
| %r        | Time, 12-hour (hh:mm:ss followed by AM or PM)                   |

| Specifier | Description                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------|
| %S        | Seconds (0059)                                                                                      |
| %s        | Seconds (0059)                                                                                      |
| %T        | Time, 24-hour (hh:mm:ss)                                                                            |
| %U        | Week (0053), where Sunday is the first day of<br>the week; WEEK() mode 0                            |
| %u        | Week (0053), where Monday is the first day of<br>the week; WEEK() mode 1                            |
| %V        | Week (0153), where Sunday is the first day of<br>the week; WEEK() mode 2; used with %X              |
| %v        | Week (0153), where Monday is the first day of<br>the week; WEEK() mode 3; used with %x              |
| %W        | Weekday name (SundaySaturday)                                                                       |
| %w        | Day of the week (0=Sunday6=Saturday)                                                                |
| %X        | Year for the week where Sunday is the first day<br>of the week, numeric, four digits; used with %V  |
| %x        | Year for the week, where Monday is the first day<br>of the week, numeric, four digits; used with %v |
| %Y        | Year, numeric, four digits                                                                          |
| %y        | Year, numeric (two digits)                                                                          |
| %%        | A literal % character                                                                               |
| %x        | x, for any "x" not listed above                                                                     |

Ranges for the month and day specifiers begin with zero due to the fact that MySQL permits the storing of incomplete dates such as '2014-00-00'.

The language used for day and month names and abbreviations is controlled by the value of the lc\_time\_names system variable (Section 10.16, "MySQL Server Locale Support").

For the %U, %u, %V, and %v specifiers, see the description of the [WEEK\(\)](#page-34-3) function for information about the mode values. The mode affects how week numbering occurs.

[DATE\\_FORMAT\(\)](#page-20-0) returns a string with a character set and collation given by character\_set\_connection and collation\_connection so that it can return month and weekday names containing non-ASCII characters.

```
mysql> SELECT DATE_FORMAT('2009-10-04 22:23:00', '%W %M %Y');
 -> 'Sunday October 2009'
mysql> SELECT DATE_FORMAT('2007-10-04 22:23:00', '%H:%i:%s');
 -> '22:23:00'
mysql> SELECT DATE_FORMAT('1900-10-04 22:23:00',
 -> '%D %y %a %d %m %b %j');
 -> '4th 00 Thu 04 10 Oct 277'
mysql> SELECT DATE_FORMAT('1997-10-04 22:23:00',
 -> '%H %k %I %r %T %S %w');
 -> '22 22 10 10:23:00 PM 22:23:00 00 6'
mysql> SELECT DATE_FORMAT('1999-01-01', '%X %V');
 -> '1998 52'
mysql> SELECT DATE_FORMAT('2006-06-00', '%d');
 -> '00'
```

<span id="page-21-0"></span>• DATE\_SUB(date[,INTERVAL](#page-21-0) expr unit)

See the description for [DATE\\_ADD\(\)](#page-19-0).

<span id="page-22-0"></span>• [DAY\(](#page-22-0)date)

[DAY\(\)](#page-22-0) is a synonym for [DAYOFMONTH\(\)](#page-22-2).

<span id="page-22-1"></span>• [DAYNAME\(](#page-22-1)date)

Returns the name of the weekday for date. The language used for the name is controlled by the value of the lc\_time\_names system variable (Section 10.16, "MySQL Server Locale Support").

```
mysql> SELECT DAYNAME('2007-02-03');
 -> 'Saturday'
```

<span id="page-22-2"></span>• [DAYOFMONTH\(](#page-22-2)date)

Returns the day of the month for date, in the range 1 to 31, or 0 for dates such as '0000-00-00' or '2008-00-00' that have a zero day part.

```
mysql> SELECT DAYOFMONTH('2007-02-03');
 -> 3
```

<span id="page-22-3"></span>• [DAYOFWEEK\(](#page-22-3)date)

Returns the weekday index for date (1 = Sunday, 2 = Monday, …, 7 = Saturday). These index values correspond to the ODBC standard.

```
mysql> SELECT DAYOFWEEK('2007-02-03');
 -> 7
```

<span id="page-22-4"></span>• [DAYOFYEAR\(](#page-22-4)date)

Returns the day of the year for date, in the range 1 to 366.

```
mysql> SELECT DAYOFYEAR('2007-02-03');
 -> 34
```

<span id="page-22-5"></span>• [EXTRACT\(](#page-22-5)unit FROM date)

The [EXTRACT\(\)](#page-22-5) function uses the same kinds of unit specifiers as [DATE\\_ADD\(\)](#page-19-0) or [DATE\\_SUB\(\)](#page-21-0), but extracts parts from the date rather than performing date arithmetic. For information on the unit argument, see Temporal Intervals.

```
mysql> SELECT EXTRACT(YEAR FROM '2019-07-02');
 -> 2019
mysql> SELECT EXTRACT(YEAR_MONTH FROM '2019-07-02 01:02:03');
 -> 201907
mysql> SELECT EXTRACT(DAY_MINUTE FROM '2019-07-02 01:02:03');
 -> 20102
mysql> SELECT EXTRACT(MICROSECOND
 -> FROM '2003-01-02 10:30:00.000123');
 -> 123
```

<span id="page-22-6"></span>• [FROM\\_DAYS\(](#page-22-6)N)

Given a day number N, returns a DATE value.

```
mysql> SELECT FROM_DAYS(730669);
 -> '2000-07-03'
```

Use [FROM\\_DAYS\(\)](#page-22-6) with caution on old dates. It is not intended for use with values that precede the advent of the Gregorian calendar (1582). See Section 11.2.8, "What Calendar Is Used By MySQL?".

<span id="page-22-7"></span>• [FROM\\_UNIXTIME\(](#page-22-7)unix\_timestamp[,format])

Returns a representation of unix\_timestamp as a datetime or character string value. The value returned is expressed using the session time zone. (Clients can set the session time zone as described in Section 5.1.13, "MySQL Server Time Zone Support".) unix\_timestamp is an internal timestamp value representing seconds since '1970-01-01 00:00:00' UTC, such as produced by the [UNIX\\_TIMESTAMP\(\)](#page-32-1) function.

If format is omitted, this function returns a DATETIME value.

If unix\_timestamp is an integer, the fractional seconds precision of the DATETIME is zero. When unix\_timestamp is a decimal value, the fractional seconds precision of the DATETIME is the same as the precision of the decimal value, up to a maximum of 6. When unix\_timestamp is a floating point number, the fractional seconds precision of the datetime is 6.

format is used to format the result in the same way as the format string used for the [DATE\\_FORMAT\(\)](#page-20-0) function. If format is supplied, the value returned is a VARCHAR.

```
mysql> SELECT FROM_UNIXTIME(1447430881);
 -> '2015-11-13 10:08:01'
mysql> SELECT FROM_UNIXTIME(1447430881) + 0;
 -> 20151113100801
mysql> SELECT FROM_UNIXTIME(1447430881,
 -> '%Y %D %M %h:%i:%s %x');
 -> '2015 13th November 10:08:01 2015'
```

![](_page_23_Picture_6.jpeg)

#### **Note**

If you use [UNIX\\_TIMESTAMP\(\)](#page-32-1) and [FROM\\_UNIXTIME\(\)](#page-22-7) to convert between values in a non-UTC time zone and Unix timestamp values, the conversion is lossy because the mapping is not one-to-one in both directions. For details, see the description of the [UNIX\\_TIMESTAMP\(\)](#page-32-1) function.

<span id="page-23-0"></span>• [GET\\_FORMAT\({DATE|TIME|DATETIME}, {'EUR'|'USA'|'JIS'|'ISO'|'INTERNAL'}\)](#page-23-0)

Returns a format string. This function is useful in combination with the [DATE\\_FORMAT\(\)](#page-20-0) and the [STR\\_TO\\_DATE\(\)](#page-26-5) functions.

The possible values for the first and second arguments result in several possible format strings (for the specifiers used, see the table in the [DATE\\_FORMAT\(\)](#page-20-0) function description). ISO format refers to ISO 9075, not ISO 8601.

| Function Call                   | Result              |
|---------------------------------|---------------------|
| GET_FORMAT(DATE,'USA')          | '%m.%d.%Y'          |
| GET_FORMAT(DATE,'JIS')          | '%Y-%m-%d'          |
| GET_FORMAT(DATE,'ISO')          | '%Y-%m-%d'          |
| GET_FORMAT(DATE,'EUR')          | '%d.%m.%Y'          |
| GET_FORMAT(DATE,'INTERNAL')     | '%Y%m%d'            |
| GET_FORMAT(DATETIME,'USA')      | '%Y-%m-%d %H.%i.%s' |
| GET_FORMAT(DATETIME,'JIS')      | '%Y-%m-%d %H:%i:%s' |
| GET_FORMAT(DATETIME,'ISO')      | '%Y-%m-%d %H:%i:%s' |
| GET_FORMAT(DATETIME,'EUR')      | '%Y-%m-%d %H.%i.%s' |
| GET_FORMAT(DATETIME,'INTERNAL') | '%Y%m%d%H%i%s'      |
| GET_FORMAT(TIME,'USA')          | '%h:%i:%s %p'       |
| GET_FORMAT(TIME,'JIS')          | '%H:%i:%s'          |
| GET_FORMAT(TIME,'ISO')          | '%H:%i:%s'          |
| GET_FORMAT(TIME,'EUR')          | '%H.%i.%s'          |

| Function Call               | Result   |
|-----------------------------|----------|
| GET_FORMAT(TIME,'INTERNAL') | '%H%i%s' |

TIMESTAMP can also be used as the first argument to [GET\\_FORMAT\(\)](#page-23-0), in which case the function returns the same values as for DATETIME.

```
mysql> SELECT DATE_FORMAT('2003-10-03',GET_FORMAT(DATE,'EUR'));
 -> '03.10.2003'
mysql> SELECT STR_TO_DATE('10.31.2003',GET_FORMAT(DATE,'USA'));
 -> '2003-10-31'
```

<span id="page-24-0"></span>• [HOUR\(](#page-24-0)time)

Returns the hour for time. The range of the return value is 0 to 23 for time-of-day values. However, the range of TIME values actually is much larger, so HOUR can return values greater than 23.

```
mysql> SELECT HOUR('10:05:03');
 -> 10
mysql> SELECT HOUR('272:59:59');
 -> 272
```

<span id="page-24-1"></span>• [LAST\\_DAY\(](#page-24-1)date)

Takes a date or datetime value and returns the corresponding value for the last day of the month. Returns NULL if the argument is invalid.

```
mysql> SELECT LAST_DAY('2003-02-05');
 -> '2003-02-28'
mysql> SELECT LAST_DAY('2004-02-05');
 -> '2004-02-29'
mysql> SELECT LAST_DAY('2004-01-01 01:01:01');
 -> '2004-01-31'
mysql> SELECT LAST_DAY('2003-03-32');
 -> NULL
```

<span id="page-24-2"></span>• [LOCALTIME](#page-24-2), [LOCALTIME\(\[](#page-24-2)fsp])

[LOCALTIME](#page-24-2) and [LOCALTIME\(\)](#page-24-2) are synonyms for [NOW\(\)](#page-25-4).

<span id="page-24-3"></span>• [LOCALTIMESTAMP](#page-24-3), [LOCALTIMESTAMP\(\[](#page-24-3)fsp])

[LOCALTIMESTAMP](#page-24-3) and [LOCALTIMESTAMP\(\)](#page-24-3) are synonyms for [NOW\(\)](#page-25-4).

<span id="page-24-4"></span>• [MAKEDATE\(](#page-24-4)year,dayofyear)

Returns a date, given year and day-of-year values. dayofyear must be greater than 0 or the result is NULL.

```
mysql> SELECT MAKEDATE(2011,31), MAKEDATE(2011,32);
 -> '2011-01-31', '2011-02-01'
mysql> SELECT MAKEDATE(2011,365), MAKEDATE(2014,365);
 -> '2011-12-31', '2014-12-31'
mysql> SELECT MAKEDATE(2011,0);
 -> NULL
```

<span id="page-24-5"></span>• [MAKETIME\(](#page-24-5)hour,minute,second)

Returns a time value calculated from the hour, minute, and second arguments.

The second argument can have a fractional part.

```
mysql> SELECT MAKETIME(12,15,30);
 -> '12:15:30'
```

### <span id="page-25-0"></span>• [MICROSECOND\(](#page-25-0)expr)

Returns the microseconds from the time or datetime expression expr as a number in the range from 0 to 999999.

```
mysql> SELECT MICROSECOND('12:00:00.123456');
 -> 123456
mysql> SELECT MICROSECOND('2019-12-31 23:59:59.000010');
 -> 10
```

<span id="page-25-1"></span>• [MINUTE\(](#page-25-1)time)

Returns the minute for time, in the range 0 to 59.

```
mysql> SELECT MINUTE('2008-02-03 10:05:03');
 -> 5
```

<span id="page-25-2"></span>• [MONTH\(](#page-25-2)date)

Returns the month for date, in the range 1 to 12 for January to December, or 0 for dates such as '0000-00-00' or '2008-00-00' that have a zero month part.

```
mysql> SELECT MONTH('2008-02-03');
 -> 2
```

<span id="page-25-3"></span>• [MONTHNAME\(](#page-25-3)date)

Returns the full name of the month for date. The language used for the name is controlled by the value of the lc\_time\_names system variable (Section 10.16, "MySQL Server Locale Support").

```
mysql> SELECT MONTHNAME('2008-02-03');
 -> 'February'
```

<span id="page-25-4"></span>• [NOW\(\[](#page-25-4)fsp])

Returns the current date and time as a value in 'YYYY-MM-DD hh:mm:ss' or YYYYMMDDhhmmss format, depending on whether the function is used in string or numeric context. The value is expressed in the session time zone.

If the fsp argument is given to specify a fractional seconds precision from 0 to 6, the return value includes a fractional seconds part of that many digits.

```
mysql> SELECT NOW();
 -> '2007-12-15 23:50:26'
mysql> SELECT NOW() + 0;
 -> 20071215235026.000000
```

[NOW\(\)](#page-25-4) returns a constant time that indicates the time at which the statement began to execute. (Within a stored function or trigger, [NOW\(\)](#page-25-4) returns the time at which the function or triggering statement began to execute.) This differs from the behavior for [SYSDATE\(\)](#page-28-2), which returns the exact time at which it executes.

```
mysql> SELECT NOW(), SLEEP(2), NOW();
+---------------------+----------+---------------------+
| NOW() | SLEEP(2) | NOW() |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:36 | 0 | 2006-04-12 13:47:36 |
+---------------------+----------+---------------------+
mysql> SELECT SYSDATE(), SLEEP(2), SYSDATE();
+---------------------+----------+---------------------+
| SYSDATE() | SLEEP(2) | SYSDATE() |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:44 | 0 | 2006-04-12 13:47:46 |
```

+---------------------+----------+---------------------+

In addition, the SET TIMESTAMP statement affects the value returned by [NOW\(\)](#page-25-4) but not by [SYSDATE\(\)](#page-28-2). This means that timestamp settings in the binary log have no effect on invocations of [SYSDATE\(\)](#page-28-2). Setting the timestamp to a nonzero value causes each subsequent invocation of [NOW\(\)](#page-25-4) to return that value. Setting the timestamp to zero cancels this effect so that [NOW\(\)](#page-25-4) once again returns the current date and time.

See the description for [SYSDATE\(\)](#page-28-2) for additional information about the differences between the two functions.

<span id="page-26-0"></span>• [PERIOD\\_ADD\(](#page-26-0)P,N)

Adds N months to period P (in the format YYMM or YYYYMM). Returns a value in the format YYYYMM.

![](_page_26_Picture_6.jpeg)

#### **Note**

The period argument P is not a date value.

```
mysql> SELECT PERIOD_ADD(200801,2);
 -> 200803
```

<span id="page-26-1"></span>• [PERIOD\\_DIFF\(](#page-26-1)P1,P2)

Returns the number of months between periods P1 and P2. P1 and P2 should be in the format YYMM or YYYYMM. Note that the period arguments P1 and P2 are not date values.

```
mysql> SELECT PERIOD_DIFF(200802,200703);
 -> 11
```

<span id="page-26-2"></span>• [QUARTER\(](#page-26-2)date)

Returns the quarter of the year for date, in the range 1 to 4.

```
mysql> SELECT QUARTER('2008-04-01');
 -> 2
```

<span id="page-26-4"></span>• [SECOND\(](#page-26-4)time)

Returns the second for time, in the range 0 to 59.

```
mysql> SELECT SECOND('10:05:03');
 -> 3
```

<span id="page-26-3"></span>• [SEC\\_TO\\_TIME\(](#page-26-3)seconds)

Returns the seconds argument, converted to hours, minutes, and seconds, as a TIME value. The range of the result is constrained to that of the TIME data type. A warning occurs if the argument corresponds to a value outside that range.

```
mysql> SELECT SEC_TO_TIME(2378);
 -> '00:39:38'
mysql> SELECT SEC_TO_TIME(2378) + 0;
 -> 3938
```

<span id="page-26-5"></span>• [STR\\_TO\\_DATE\(](#page-26-5)str,format)

This is the inverse of the [DATE\\_FORMAT\(\)](#page-20-0) function. It takes a string str and a format string format. [STR\\_TO\\_DATE\(\)](#page-26-5) returns a DATETIME value if the format string contains both date and time parts, or a DATE or TIME value if the string contains only date or time parts. If str or format is NULL, the function returns NULL. If the date, time, or datetime value extracted from str cannot be parsed according to the rules followed by the server, [STR\\_TO\\_DATE\(\)](#page-26-5) returns NULL and produces a warning.

The server scans str attempting to match format to it. The format string can contain literal characters and format specifiers beginning with %. Literal characters in format must match literally in str. Format specifiers in format must match a date or time part in str. For the specifiers that can be used in format, see the [DATE\\_FORMAT\(\)](#page-20-0) function description.

```
mysql> SELECT STR_TO_DATE('01,5,2013','%d,%m,%Y');
 -> '2013-05-01'
mysql> SELECT STR_TO_DATE('May 1, 2013','%M %d,%Y');
 -> '2013-05-01'
```

Scanning starts at the beginning of str and fails if format is found not to match. Extra characters at the end of str are ignored.

```
mysql> SELECT STR_TO_DATE('a09:30:17','a%h:%i:%s');
 -> '09:30:17'
mysql> SELECT STR_TO_DATE('a09:30:17','%h:%i:%s');
 -> NULL
mysql> SELECT STR_TO_DATE('09:30:17a','%h:%i:%s');
 -> '09:30:17'
```

Unspecified date or time parts have a value of 0, so incompletely specified values in str produce a result with some or all parts set to 0:

```
mysql> SELECT STR_TO_DATE('abc','abc');
 -> '0000-00-00'
mysql> SELECT STR_TO_DATE('9','%m');
 -> '0000-09-00'
mysql> SELECT STR_TO_DATE('9','%s');
 -> '00:00:09'
```

Range checking on the parts of date values is as described in Section 11.2.2, "The DATE, DATETIME, and TIMESTAMP Types". This means, for example, that "zero" dates or dates with part values of 0 are permitted unless the SQL mode is set to disallow such values.

```
mysql> SELECT STR_TO_DATE('00/00/0000', '%m/%d/%Y');
 -> '0000-00-00'
mysql> SELECT STR_TO_DATE('04/31/2004', '%m/%d/%Y');
 -> '2004-04-31'
```

If the NO\_ZERO\_DATE SQL mode is enabled, zero dates are disallowed. In that case, [STR\\_TO\\_DATE\(\)](#page-26-5) returns NULL and generates a warning:

```
mysql> SET sql_mode = '';
mysql> SELECT STR_TO_DATE('00/00/0000', '%m/%d/%Y');
+---------------------------------------+
| STR_TO_DATE('00/00/0000', '%m/%d/%Y') |
+---------------------------------------+
| 0000-00-00 |
+---------------------------------------+
mysql> SET sql_mode = 'NO_ZERO_DATE';
mysql> SELECT STR_TO_DATE('00/00/0000', '%m/%d/%Y');
+---------------------------------------+
| STR_TO_DATE('00/00/0000', '%m/%d/%Y') |
+---------------------------------------+
| NULL |
+---------------------------------------+
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1411
```

```
Message: Incorrect datetime value: '00/00/0000' for function str_to_date
```

Prior to MySQL 5.7.44, it was possible to pass an invalid date string such as '2021-11-31' to this function. In MySQL 5.7.44 and later, STR\_TO\_DATE() performs complete range checking and raises an error if the date after conversion would be invalid.

![](_page_28_Picture_3.jpeg)

#### **Note**

You cannot use format "%X%V" to convert a year-week string to a date because the combination of a year and week does not uniquely identify a year and month if the week crosses a month boundary. To convert a year-week to a date, you should also specify the weekday:

```
mysql> SELECT STR_TO_DATE('200442 Monday', '%X%V %W');
 -> '2004-10-18'
```

You should also be aware that, for dates and the date portions of datetime values, STR\_TO\_DATE() checks (only) the individual year, month, and day of month values for validity. More precisely, this means that the year is checked to be sure that it is in the range 0-9999 inclusive, the month is checked to ensure that it is in the range 1-12 inclusive, and the day of month is checked to make sure that it is in the range 1-31 inclusive, but the server does not check the values in combination. For example, SELECT STR\_TO\_DATE('23-2-31', '%Y-%m-%d') returns 2023-02-31. Enabling or disabling the ALLOW\_INVALID\_DATES server SQL mode has no effect on this behavior. See Section 11.2.2, "The DATE, DATETIME, and TIMESTAMP Types", for more information.

<span id="page-28-0"></span>• SUBDATE(date[,INTERVAL](#page-28-0) expr unit), [SUBDATE\(](#page-28-0)expr,days)

When invoked with the INTERVAL form of the second argument, [SUBDATE\(\)](#page-28-0) is a synonym for [DATE\\_SUB\(\)](#page-21-0). For information on the INTERVAL unit argument, see the discussion for [DATE\\_ADD\(\)](#page-19-0).

```
mysql> SELECT DATE_SUB('2008-01-02', INTERVAL 31 DAY);
 -> '2007-12-02'
mysql> SELECT SUBDATE('2008-01-02', INTERVAL 31 DAY);
 -> '2007-12-02'
```

The second form enables the use of an integer value for days. In such cases, it is interpreted as the number of days to be subtracted from the date or datetime expression expr.

```
mysql> SELECT SUBDATE('2008-01-02 12:00:00', 31);
 -> '2007-12-02 12:00:00'
```

<span id="page-28-1"></span>• [SUBTIME\(](#page-28-1)expr1,expr2)

[SUBTIME\(\)](#page-28-1) returns expr1 − expr2 expressed as a value in the same format as expr1. expr1 is a time or datetime expression, and expr2 is a time expression.

```
mysql> SELECT SUBTIME('2007-12-31 23:59:59.999999','1 1:1:1.000002');
 -> '2007-12-30 22:58:58.999997'
mysql> SELECT SUBTIME('01:00:00.999999', '02:00:00.999998');
 -> '-00:59:59.999999'
```

<span id="page-28-2"></span>• [SYSDATE\(\[](#page-28-2)fsp])

Returns the current date and time as a value in 'YYYY-MM-DD hh:mm:ss' or YYYYMMDDhhmmss format, depending on whether the function is used in string or numeric context.

If the fsp argument is given to specify a fractional seconds precision from 0 to 6, the return value includes a fractional seconds part of that many digits.

[SYSDATE\(\)](#page-28-2) returns the time at which it executes. This differs from the behavior for [NOW\(\)](#page-25-4), which returns a constant time that indicates the time at which the statement began to execute. (Within a stored function or trigger, [NOW\(\)](#page-25-4) returns the time at which the function or triggering statement began to execute.)

```
mysql> SELECT NOW(), SLEEP(2), NOW();
+---------------------+----------+---------------------+
| NOW() | SLEEP(2) | NOW() |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:36 | 0 | 2006-04-12 13:47:36 |
+---------------------+----------+---------------------+
mysql> SELECT SYSDATE(), SLEEP(2), SYSDATE();
+---------------------+----------+---------------------+
| SYSDATE() | SLEEP(2) | SYSDATE() |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:44 | 0 | 2006-04-12 13:47:46 |
+---------------------+----------+---------------------+
```

In addition, the SET TIMESTAMP statement affects the value returned by [NOW\(\)](#page-25-4) but not by [SYSDATE\(\)](#page-28-2). This means that timestamp settings in the binary log have no effect on invocations of [SYSDATE\(\)](#page-28-2).

Because [SYSDATE\(\)](#page-28-2) can return different values even within the same statement, and is not affected by SET TIMESTAMP, it is nondeterministic and therefore unsafe for replication if statement-based binary logging is used. If that is a problem, you can use row-based logging.

Alternatively, you can use the --sysdate-is-now option to cause [SYSDATE\(\)](#page-28-2) to be an alias for [NOW\(\)](#page-25-4). This works if the option is used on both the source and the replica.

The nondeterministic nature of [SYSDATE\(\)](#page-28-2) also means that indexes cannot be used for evaluating expressions that refer to it.

<span id="page-29-0"></span>• [TIME\(](#page-29-0)expr)

Extracts the time part of the time or datetime expression expr and returns it as a string.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

```
mysql> SELECT TIME('2003-12-31 01:02:03');
 -> '01:02:03'
mysql> SELECT TIME('2003-12-31 01:02:03.000123');
 -> '01:02:03.000123'
```

<span id="page-29-1"></span>• [TIMEDIFF\(](#page-29-1)expr1,expr2)

[TIMEDIFF\(\)](#page-29-1) returns expr1 − expr2 expressed as a time value. expr1 and expr2 are strings which are converted to TIME or DATETIME expressions; these must be of the same type following conversion.

The result returned by TIMEDIFF() is limited to the range allowed for TIME values. Alternatively, you can use either of the functions [TIMESTAMPDIFF\(\)](#page-30-2) and [UNIX\\_TIMESTAMP\(\)](#page-32-1), both of which return integers.

```
mysql> SELECT TIMEDIFF('2000:01:01 00:00:00',
 -> '2000:01:01 00:00:00.000001');
 -> '-00:00:00.000001'
mysql> SELECT TIMEDIFF('2008-12-31 23:59:59.000001',
 -> '2008-12-30 01:01:01.000002');
 -> '46:58:57.999999'
```

<span id="page-30-0"></span>• [TIMESTAMP\(](#page-30-0)expr), [TIMESTAMP\(](#page-30-0)expr1,expr2)

With a single argument, this function returns the date or datetime expression expr as a datetime value. With two arguments, it adds the time expression expr2 to the date or datetime expression expr1 and returns the result as a datetime value.

```
mysql> SELECT TIMESTAMP('2003-12-31');
 -> '2003-12-31 00:00:00'
mysql> SELECT TIMESTAMP('2003-12-31 12:00:00','12:00:00');
 -> '2004-01-01 00:00:00'
```

<span id="page-30-1"></span>• [TIMESTAMPADD\(](#page-30-1)unit,interval,datetime\_expr)

Adds the integer expression interval to the date or datetime expression datetime\_expr. The unit for interval is given by the unit argument, which should be one of the following values: MICROSECOND (microseconds), SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, or YEAR.

The unit value may be specified using one of keywords as shown, or with a prefix of SQL\_TSI\_. For example, DAY and SQL\_TSI\_DAY both are legal.

```
mysql> SELECT TIMESTAMPADD(MINUTE,1,'2003-01-02');
 -> '2003-01-02 00:01:00'
mysql> SELECT TIMESTAMPADD(WEEK,1,'2003-01-02');
 -> '2003-01-09'
```

When adding a MONTH interval to a DATE or DATETIME value, and the resulting date includes a day that does not exist in the given month, the day is adjusted to the last day of the month, as shown here:

```
mysql> SELECT TIMESTAMPADD(MONTH, 1, DATE '2024-03-30') AS t1,
 > TIMESTAMPADD(MONTH, 1, DATE '2024-03-31') AS t2;
+------------+------------+
| t1 | t2 |
+------------+------------+
| 2024-04-30 | 2024-04-30 |
+------------+------------+
1 row in set (0.00 sec)
```

<span id="page-30-2"></span>• [TIMESTAMPDIFF\(](#page-30-2)unit,datetime\_expr1,datetime\_expr2)

Returns datetime\_expr2 − datetime\_expr1, where datetime\_expr1 and datetime\_expr2 are date or datetime expressions. One expression may be a date and the other a datetime; a date value is treated as a datetime having the time part '00:00:00' where necessary. The unit for the result (an integer) is given by the unit argument. The legal values for unit are the same as those listed in the description of the [TIMESTAMPADD\(\)](#page-30-1) function.

```
mysql> SELECT TIMESTAMPDIFF(MONTH,'2003-02-01','2003-05-01');
 -> 3
mysql> SELECT TIMESTAMPDIFF(YEAR,'2002-05-01','2001-01-01');
 -> -1
mysql> SELECT TIMESTAMPDIFF(MINUTE,'2003-02-01','2003-05-01 12:05:55');
 -> 128885
```

![](_page_30_Picture_13.jpeg)

#### **Note**

The order of the date or datetime arguments for this function is the opposite of that used with the [TIMESTAMP\(\)](#page-30-0) function when invoked with 2 arguments. <span id="page-31-0"></span>• [TIME\\_FORMAT\(](#page-31-0)time,format)

This is used like the [DATE\\_FORMAT\(\)](#page-20-0) function, but the format string may contain format specifiers only for hours, minutes, seconds, and microseconds. Other specifiers produce a NULL value or 0.

If the time value contains an hour part that is greater than 23, the %H and %k hour format specifiers produce a value larger than the usual range of 0..23. The other hour format specifiers produce the hour value modulo 12.

```
mysql> SELECT TIME_FORMAT('100:00:00', '%H %k %h %I %l');
 -> '100 100 04 04 4'
```

<span id="page-31-1"></span>• [TIME\\_TO\\_SEC\(](#page-31-1)time)

Returns the time argument, converted to seconds.

```
mysql> SELECT TIME_TO_SEC('22:23:00');
 -> 80580
mysql> SELECT TIME_TO_SEC('00:39:38');
 -> 2378
```

<span id="page-31-2"></span>• [TO\\_DAYS\(](#page-31-2)date)

Given a date date, returns a day number (the number of days since year 0).

```
mysql> SELECT TO_DAYS(950501);
 -> 728779
mysql> SELECT TO_DAYS('2007-10-07');
 -> 733321
```

[TO\\_DAYS\(\)](#page-31-2) is not intended for use with values that precede the advent of the Gregorian calendar (1582), because it does not take into account the days that were lost when the calendar was changed. For dates before 1582 (and possibly a later year in other locales), results from this function are not reliable. See Section 11.2.8, "What Calendar Is Used By MySQL?", for details.

Remember that MySQL converts two-digit year values in dates to four-digit form using the rules in Section 11.2, "Date and Time Data Types". For example, '2008-10-07' and '08-10-07' are seen as identical dates:

```
mysql> SELECT TO_DAYS('2008-10-07'), TO_DAYS('08-10-07');
 -> 733687, 733687
```

In MySQL, the zero date is defined as '0000-00-00', even though this date is itself considered invalid. This means that, for '0000-00-00' and '0000-01-01', [TO\\_DAYS\(\)](#page-31-2) returns the values shown here:

```
mysql> SELECT TO_DAYS('0000-00-00');
+-----------------------+
| to_days('0000-00-00') |
+-----------------------+
| NULL |
+-----------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------+
| Level | Code | Message |
+---------+------+----------------------------------------+
| Warning | 1292 | Incorrect datetime value: '0000-00-00' |
+---------+------+----------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT TO_DAYS('0000-01-01');
+-----------------------+
| to_days('0000-01-01') |
+-----------------------+
```

```
| 1 |
+-----------------------+
1 row in set (0.00 sec)
```

This is true whether or not the ALLOW\_INVALID\_DATES SQL server mode is enabled.

<span id="page-32-0"></span>• [TO\\_SECONDS\(](#page-32-0)expr)

Given a date or datetime expr, returns the number of seconds since the year 0. If expr is not a valid date or datetime value, returns NULL.

```
mysql> SELECT TO_SECONDS(950501);
 -> 62966505600
mysql> SELECT TO_SECONDS('2009-11-29');
 -> 63426672000
mysql> SELECT TO_SECONDS('2009-11-29 13:43:32');
 -> 63426721412
mysql> SELECT TO_SECONDS( NOW() );
 -> 63426721458
```

Like [TO\\_DAYS\(\)](#page-31-2), TO\_SECONDS() is not intended for use with values that precede the advent of the Gregorian calendar (1582), because it does not take into account the days that were lost when the calendar was changed. For dates before 1582 (and possibly a later year in other locales), results from this function are not reliable. See Section 11.2.8, "What Calendar Is Used By MySQL?", for details.

Like [TO\\_DAYS\(\)](#page-31-2), TO\_SECONDS(), converts two-digit year values in dates to four-digit form using the rules in Section 11.2, "Date and Time Data Types".

In MySQL, the zero date is defined as '0000-00-00', even though this date is itself considered invalid. This means that, for '0000-00-00' and '0000-01-01', [TO\\_SECONDS\(\)](#page-32-0) returns the values shown here:

```
mysql> SELECT TO_SECONDS('0000-00-00');
+--------------------------+
| TO_SECONDS('0000-00-00') |
+--------------------------+
| NULL |
+--------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------+
| Level | Code | Message |
+---------+------+----------------------------------------+
| Warning | 1292 | Incorrect datetime value: '0000-00-00' |
+---------+------+----------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT TO_SECONDS('0000-01-01');
+--------------------------+
| TO_SECONDS('0000-01-01') |
+--------------------------+
| 86400 |
+--------------------------+
1 row in set (0.00 sec)
```

This is true whether or not the ALLOW\_INVALID\_DATES SQL server mode is enabled.

<span id="page-32-1"></span>• [UNIX\\_TIMESTAMP\(\[](#page-32-1)date])

If [UNIX\\_TIMESTAMP\(\)](#page-32-1) is called with no date argument, it returns a Unix timestamp representing seconds since '1970-01-01 00:00:00' UTC.

If [UNIX\\_TIMESTAMP\(\)](#page-32-1) is called with a date argument, it returns the value of the argument as seconds since '1970-01-01 00:00:00' UTC. The server interprets date as a value in the

session time zone and converts it to an internal Unix timestamp value in UTC. (Clients can set the session time zone as described in Section 5.1.13, "MySQL Server Time Zone Support".) The date argument may be a DATE, DATETIME, or TIMESTAMP string, or a number in YYMMDD, YYMMDDhhmmss, YYYYMMDD, or YYYYMMDDhhmmss format. If the argument includes a time part, it may optionally include a fractional seconds part.

The return value is an integer if no argument is given or the argument does not include a fractional seconds part, or DECIMAL if an argument is given that includes a fractional seconds part.

When the date argument is a TIMESTAMP column, [UNIX\\_TIMESTAMP\(\)](#page-32-1) returns the internal timestamp value directly, with no implicit "string-to-Unix-timestamp" conversion.

The valid range of argument values is the same as for the TIMESTAMP data type: '1970-01-01 00:00:01.000000' UTC to '2038-01-19 03:14:07.999999' UTC. If you pass an out-ofrange date to [UNIX\\_TIMESTAMP\(\)](#page-32-1), it returns 0.

```
mysql> SELECT UNIX_TIMESTAMP();
 -> 1447431666
mysql> SELECT UNIX_TIMESTAMP('2015-11-13 10:20:19');
 -> 1447431619
mysql> SELECT UNIX_TIMESTAMP('2015-11-13 10:20:19.012');
 -> 1447431619.012
```

If you use [UNIX\\_TIMESTAMP\(\)](#page-32-1) and [FROM\\_UNIXTIME\(\)](#page-22-7) to convert between values in a non-UTC time zone and Unix timestamp values, the conversion is lossy because the mapping is not one-toone in both directions. For example, due to conventions for local time zone changes such as Daylight Saving Time (DST), it is possible for [UNIX\\_TIMESTAMP\(\)](#page-32-1) to map two values that are distinct in a non-UTC time zone to the same Unix timestamp value. [FROM\\_UNIXTIME\(\)](#page-22-7) maps that value back to only one of the original values. Here is an example, using values that are distinct in the MET time zone:

```
mysql> SET time_zone = 'MET';
mysql> SELECT UNIX_TIMESTAMP('2005-03-27 03:00:00');
+---------------------------------------+
| UNIX_TIMESTAMP('2005-03-27 03:00:00') |
+---------------------------------------+
| 1111885200 |
+---------------------------------------+
mysql> SELECT UNIX_TIMESTAMP('2005-03-27 02:00:00');
+---------------------------------------+
| UNIX_TIMESTAMP('2005-03-27 02:00:00') |
+---------------------------------------+
| 1111885200 |
+---------------------------------------+
mysql> SELECT FROM_UNIXTIME(1111885200);
+---------------------------+
| FROM_UNIXTIME(1111885200) |
+---------------------------+
| 2005-03-27 03:00:00 |
+---------------------------+
```

![](_page_33_Picture_8.jpeg)

#### **Note**

To use named time zones such as 'MET' or 'Europe/Amsterdam', the time zone tables must be properly set up. For instructions, see Section 5.1.13, "MySQL Server Time Zone Support".

If you want to subtract [UNIX\\_TIMESTAMP\(\)](#page-32-1) columns, you might want to cast them to signed integers. See [Section 12.10, "Cast Functions and Operators"](#page-88-0).

<span id="page-34-0"></span>• [UTC\\_DATE](#page-34-0), [UTC\\_DATE\(\)](#page-34-0)

Returns the current UTC date as a value in 'YYYY-MM-DD' or YYYYMMDD format, depending on whether the function is used in string or numeric context.

```
mysql> SELECT UTC_DATE(), UTC_DATE() + 0;
 -> '2003-08-14', 20030814
```

<span id="page-34-1"></span>• [UTC\\_TIME](#page-34-1), [UTC\\_TIME\(\[](#page-34-1)fsp])

Returns the current UTC time as a value in 'hh:mm:ss' or hhmmss format, depending on whether the function is used in string or numeric context.

If the fsp argument is given to specify a fractional seconds precision from 0 to 6, the return value includes a fractional seconds part of that many digits.

```
mysql> SELECT UTC_TIME(), UTC_TIME() + 0;
 -> '18:07:53', 180753.000000
```

<span id="page-34-2"></span>• [UTC\\_TIMESTAMP](#page-34-2), [UTC\\_TIMESTAMP\(\[](#page-34-2)fsp])

Returns the current UTC date and time as a value in 'YYYY-MM-DD hh:mm:ss' or YYYYMMDDhhmmss format, depending on whether the function is used in string or numeric context.

If the fsp argument is given to specify a fractional seconds precision from 0 to 6, the return value includes a fractional seconds part of that many digits.

```
mysql> SELECT UTC_TIMESTAMP(), UTC_TIMESTAMP() + 0;
 -> '2003-08-14 18:08:04', 20030814180804.000000
```

<span id="page-34-3"></span>• [WEEK\(](#page-34-3)date[,mode])

This function returns the week number for date. The two-argument form of [WEEK\(\)](#page-34-3) enables you to specify whether the week starts on Sunday or Monday and whether the return value should be in the range from 0 to 53 or from 1 to 53. If the mode argument is omitted, the value of the default\_week\_format system variable is used. See Section 5.1.7, "Server System Variables".

The following table describes how the mode argument works.

| Mode | First day of week | Range | Week 1 is the first<br>week …    |
|------|-------------------|-------|----------------------------------|
| 0    | Sunday            | 0-53  | with a Sunday in this<br>year    |
| 1    | Monday            | 0-53  | with 4 or more days this<br>year |
| 2    | Sunday            | 1-53  | with a Sunday in this<br>year    |
| 3    | Monday            | 1-53  | with 4 or more days this<br>year |
| 4    | Sunday            | 0-53  | with 4 or more days this<br>year |
| 5    | Monday            | 0-53  | with a Monday in this<br>year    |
| 6    | Sunday            | 1-53  | with 4 or more days this<br>year |

| Mode | First day of week | Range | Week 1 is the first<br>week … |
|------|-------------------|-------|-------------------------------|
| 7    | Monday            | 1-53  | with a Monday in this<br>year |

For mode values with a meaning of "with 4 or more days this year," weeks are numbered according to ISO 8601:1988:

- If the week containing January 1 has 4 or more days in the new year, it is week 1.
- Otherwise, it is the last week of the previous year, and the next week is week 1.

```
mysql> SELECT WEEK('2008-02-20');
 -> 7
mysql> SELECT WEEK('2008-02-20',0);
 -> 7
mysql> SELECT WEEK('2008-02-20',1);
 -> 8
mysql> SELECT WEEK('2008-12-31',1);
 -> 53
```

If a date falls in the last week of the previous year, MySQL returns 0 if you do not use 2, 3, 6, or 7 as the optional mode argument:

```
mysql> SELECT YEAR('2000-01-01'), WEEK('2000-01-01',0);
 -> 2000, 0
```

One might argue that [WEEK\(\)](#page-34-3) should return 52 because the given date actually occurs in the 52nd week of 1999. [WEEK\(\)](#page-34-3) returns 0 instead so that the return value is "the week number in the given year." This makes use of the [WEEK\(\)](#page-34-3) function reliable when combined with other functions that extract a date part from a date.

If you prefer a result evaluated with respect to the year that contains the first day of the week for the given date, use 0, 2, 5, or 7 as the optional mode argument.

```
mysql> SELECT WEEK('2000-01-01',2);
 -> 52
```

Alternatively, use the [YEARWEEK\(\)](#page-36-1) function:

```
mysql> SELECT YEARWEEK('2000-01-01');
 -> 199952
mysql> SELECT MID(YEARWEEK('2000-01-01'),5,2);
 -> '52'
```

<span id="page-35-0"></span>• [WEEKDAY\(](#page-35-0)date)

Returns the weekday index for date (0 = Monday, 1 = Tuesday, … 6 = Sunday).

```
mysql> SELECT WEEKDAY('2008-02-03 22:23:00');
 -> 6
mysql> SELECT WEEKDAY('2007-11-06');
 -> 1
```

<span id="page-35-1"></span>• [WEEKOFYEAR\(](#page-35-1)date)

Returns the calendar week of the date as a number in the range from 1 to 53. [WEEKOFYEAR\(\)](#page-35-1) is a compatibility function that is equivalent to [WEEK\(](#page-34-3)date,3).

```
mysql> SELECT WEEKOFYEAR('2008-02-20');
 -> 8
```

<span id="page-35-2"></span>• [YEAR\(](#page-35-2)date)

Returns the year for date, in the range 1000 to 9999, or 0 for the "zero" date.

```
mysql> SELECT YEAR('1987-01-01');
 -> 1987
```

<span id="page-36-1"></span>• [YEARWEEK\(](#page-36-1)date), [YEARWEEK\(](#page-36-1)date,mode)

Returns year and week for a date. The year in the result may be different from the year in the date argument for the first and the last week of the year.

The mode argument works exactly like the mode argument to [WEEK\(\)](#page-34-3). For the single-argument syntax, a mode value of 0 is used. Unlike [WEEK\(\)](#page-34-3), the value of default\_week\_format does not influence [YEARWEEK\(\)](#page-36-1).

```
mysql> SELECT YEARWEEK('1987-01-01');
 -> 198652
```

The week number is different from what the [WEEK\(\)](#page-34-3) function would return (0) for optional arguments 0 or 1, as [WEEK\(\)](#page-34-3) then returns the week in the context of the given year.

# <span id="page-36-0"></span>**12.8 String Functions and Operators**

**Table 12.12 String Functions and Operators**

| Name               | Description                                                                                                                              |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| ASCII()            | Return numeric value of left-most character                                                                                              |
| BIN()              | Return a string containing binary representation of<br>a number                                                                          |
| BIT_LENGTH()       | Return length of argument in bits                                                                                                        |
| CHAR()             | Return the character for each integer passed                                                                                             |
| CHAR_LENGTH()      | Return number of characters in argument                                                                                                  |
| CHARACTER_LENGTH() | Synonym for CHAR_LENGTH()                                                                                                                |
| CONCAT()           | Return concatenated string                                                                                                               |
| CONCAT_WS()        | Return concatenate with separator                                                                                                        |
| ELT()              | Return string at index number                                                                                                            |
| EXPORT_SET()       | Return a string such that for every bit set in the<br>value bits, you get an on string and for every unset<br>bit, you get an off string |
| FIELD()            | Index (position) of first argument in subsequent<br>arguments                                                                            |
| FIND_IN_SET()      | Index (position) of first argument within second<br>argument                                                                             |
| FORMAT()           | Return a number formatted to specified number of<br>decimal places                                                                       |
| FROM_BASE64()      | Decode base64 encoded string and return result                                                                                           |
| HEX()              | Hexadecimal representation of decimal or string<br>value                                                                                 |
| INSERT()           | Insert substring at specified position up to<br>specified number of characters                                                           |
| INSTR()            | Return the index of the first occurrence of<br>substring                                                                                 |
| LCASE()            | Synonym for LOWER()                                                                                                                      |
| LEFT()             | Return the leftmost number of characters as<br>specified                                                                                 |

| Name              | Description                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------|
| LENGTH()          | Return the length of a string in bytes                                                          |
| LIKE              | Simple pattern matching                                                                         |
| LOAD_FILE()       | Load the named file                                                                             |
| LOCATE()          | Return the position of the first occurrence of<br>substring                                     |
| LOWER()           | Return the argument in lowercase                                                                |
| LPAD()            | Return the string argument, left-padded with the<br>specified string                            |
| LTRIM()           | Remove leading spaces                                                                           |
| MAKE_SET()        | Return a set of comma-separated strings that<br>have the corresponding bit in bits set          |
| MATCH()           | Perform full-text search                                                                        |
| MID()             | Return a substring starting from the specified<br>position                                      |
| NOT LIKE          | Negation of simple pattern matching                                                             |
| NOT REGEXP        | Negation of REGEXP                                                                              |
| OCT()             | Return a string containing octal representation of a<br>number                                  |
| OCTET_LENGTH()    | Synonym for LENGTH()                                                                            |
| ORD()             | Return character code for leftmost character of the<br>argument                                 |
| POSITION()        | Synonym for LOCATE()                                                                            |
| QUOTE()           | Escape the argument for use in an SQL statement                                                 |
| REGEXP            | Whether string matches regular expression                                                       |
| REPEAT()          | Repeat a string the specified number of times                                                   |
| REPLACE()         | Replace occurrences of a specified string                                                       |
| REVERSE()         | Reverse the characters in a string                                                              |
| RIGHT()           | Return the specified rightmost number of<br>characters                                          |
| RLIKE             | Whether string matches regular expression                                                       |
| RPAD()            | Append string the specified number of times                                                     |
| RTRIM()           | Remove trailing spaces                                                                          |
| SOUNDEX()         | Return a soundex string                                                                         |
| SOUNDS LIKE       | Compare sounds                                                                                  |
| SPACE()           | Return a string of the specified number of spaces                                               |
| STRCMP()          | Compare two strings                                                                             |
| SUBSTR()          | Return the substring as specified                                                               |
| SUBSTRING()       | Return the substring as specified                                                               |
| SUBSTRING_INDEX() | Return a substring from a string before the<br>specified number of occurrences of the delimiter |
| TO_BASE64()       | Return the argument converted to a base-64 string                                               |
| TRIM()            | Remove leading and trailing spaces                                                              |
| UCASE()           | Synonym for UPPER()                                                                             |

| Name            | Description                                                  |
|-----------------|--------------------------------------------------------------|
| UNHEX()         | Return a string containing hex representation of a<br>number |
| UPPER()         | Convert to uppercase                                         |
| WEIGHT_STRING() | Return the weight string for a string                        |

String-valued functions return NULL if the length of the result would be greater than the value of the max\_allowed\_packet system variable. See Section 5.1.1, "Configuring the Server".

For functions that operate on string positions, the first position is numbered 1.

For functions that take length arguments, noninteger arguments are rounded to the nearest integer.

<span id="page-38-0"></span>• [ASCII\(](#page-38-0)str)

Returns the numeric value of the leftmost character of the string str. Returns 0 if str is the empty string. Returns NULL if str is NULL. [ASCII\(\)](#page-38-0) works for 8-bit characters.

```
mysql> SELECT ASCII('2');
 -> 50
mysql> SELECT ASCII(2);
 -> 50
mysql> SELECT ASCII('dx');
 -> 100
```

See also the [ORD\(\)](#page-44-4) function.

<span id="page-38-1"></span>• [BIN\(](#page-38-1)N)

Returns a string representation of the binary value of N, where N is a longlong (BIGINT) number. This is equivalent to CONV(N[,10,2\)](#page-9-0). Returns NULL if N is NULL.

```
mysql> SELECT BIN(12);
 -> '1100'
```

<span id="page-38-2"></span>• [BIT\\_LENGTH\(](#page-38-2)str)

Returns the length of the string str in bits.

```
mysql> SELECT BIT_LENGTH('text');
 -> 32
```

<span id="page-38-3"></span>• CHAR(N[,... \[USING](#page-38-3) charset\_name])

[CHAR\(\)](#page-38-3) interprets each argument N as an integer and returns a string consisting of the characters given by the code values of those integers. NULL values are skipped.

```
mysql> SELECT CHAR(77,121,83,81,'76');
 -> 'MySQL'
mysql> SELECT CHAR(77,77.3,'77.3');
 -> 'MMM'
```

[CHAR\(\)](#page-38-3) arguments larger than 255 are converted into multiple result bytes. For example, [CHAR\(256\)](#page-38-3) is equivalent to [CHAR\(1,0\)](#page-38-3), and [CHAR\(256\\*256\)](#page-38-3) is equivalent to [CHAR\(1,0,0\)](#page-38-3):

```
mysql> SELECT HEX(CHAR(1,0)), HEX(CHAR(256));
+----------------+----------------+
| HEX(CHAR(1,0)) | HEX(CHAR(256)) |
+----------------+----------------+
| 0100 | 0100 |
+----------------+----------------+
mysql> SELECT HEX(CHAR(1,0,0)), HEX(CHAR(256*256));
+------------------+--------------------+
| HEX(CHAR(1,0,0)) | HEX(CHAR(256*256)) |
+------------------+--------------------+
```

```
| 010000 | 010000 |
+------------------+--------------------+
```

By default, [CHAR\(\)](#page-38-3) returns a binary string. To produce a string in a given character set, use the optional USING clause:

```
mysql> SELECT CHARSET(CHAR(X'65')), CHARSET(CHAR(X'65' USING utf8));
+----------------------+---------------------------------+
| CHARSET(CHAR(X'65')) | CHARSET(CHAR(X'65' USING utf8)) |
+----------------------+---------------------------------+
| binary | utf8 |
+----------------------+---------------------------------+
```

If USING is given and the result string is illegal for the given character set, a warning is issued. Also, if strict SQL mode is enabled, the result from [CHAR\(\)](#page-38-3) becomes NULL.

If [CHAR\(\)](#page-38-3) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-39-1"></span>• [CHAR\\_LENGTH\(](#page-39-1)str)

Returns the length of the string str, measured in code points. A multibyte character counts as a single code point. This means that, for a string containing two 3-byte characters, [LENGTH\(\)](#page-42-3) returns 6, whereas [CHAR\\_LENGTH\(\)](#page-39-1) returns 2, as shown here:

```
mysql> SET @dolphin:='海豚';
Query OK, 0 rows affected (0.01 sec)
mysql> SELECT LENGTH(@dolphin), CHAR_LENGTH(@dolphin);
+------------------+-----------------------+
| LENGTH(@dolphin) | CHAR_LENGTH(@dolphin) |
+------------------+-----------------------+
| 6 | 2 |
+------------------+-----------------------+
1 row in set (0.00 sec)
```

<span id="page-39-2"></span>• [CHARACTER\\_LENGTH\(](#page-39-2)str)

[CHARACTER\\_LENGTH\(\)](#page-39-2) is a synonym for [CHAR\\_LENGTH\(\)](#page-39-1).

<span id="page-39-0"></span>• [CONCAT\(](#page-39-0)str1,str2,...)

Returns the string that results from concatenating the arguments. May have one or more arguments. If all arguments are nonbinary strings, the result is a nonbinary string. If the arguments include any binary strings, the result is a binary string. A numeric argument is converted to its equivalent nonbinary string form.

[CONCAT\(\)](#page-39-0) returns NULL if any argument is NULL.

```
mysql> SELECT CONCAT('My', 'S', 'QL');
 -> 'MySQL'
mysql> SELECT CONCAT('My', NULL, 'QL');
 -> NULL
mysql> SELECT CONCAT(14.3);
 -> '14.3'
```

For quoted strings, concatenation can be performed by placing the strings next to each other:

```
mysql> SELECT 'My' 'S' 'QL';
 -> 'MySQL'
```

If [CONCAT\(\)](#page-39-0) is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-40-0"></span>• [CONCAT\\_WS\(](#page-40-0)separator,str1,str2,...)

[CONCAT\\_WS\(\)](#page-40-0) stands for Concatenate With Separator and is a special form of [CONCAT\(\)](#page-39-0). The first argument is the separator for the rest of the arguments. The separator is added between the strings to be concatenated. The separator can be a string, as can the rest of the arguments. If the separator is NULL, the result is NULL.

```
mysql> SELECT CONCAT_WS(',', 'First name', 'Second name', 'Last Name');
 -> 'First name,Second name,Last Name'
mysql> SELECT CONCAT_WS(',', 'First name', NULL, 'Last Name');
 -> 'First name,Last Name'
```

[CONCAT\\_WS\(\)](#page-40-0) does not skip empty strings. However, it does skip any NULL values after the separator argument.

<span id="page-40-1"></span>• ELT(N,str1,str2,str3[,...\)](#page-40-1)

[ELT\(\)](#page-40-1) returns the Nth element of the list of strings: str1 if N = 1, str2 if N = 2, and so on. Returns NULL if N is less than 1 or greater than the number of arguments. [ELT\(\)](#page-40-1) is the complement of [FIELD\(\)](#page-40-3).

```
mysql> SELECT ELT(1, 'Aa', 'Bb', 'Cc', 'Dd');
 -> 'Aa'
mysql> SELECT ELT(4, 'Aa', 'Bb', 'Cc', 'Dd');
 -> 'Dd'
```

<span id="page-40-2"></span>• EXPORT\_SET(bits,on,off[,separator[,[number\\_of\\_bits](#page-40-2)]])

Returns a string such that for every bit set in the value bits, you get an on string and for every bit not set in the value, you get an off string. Bits in bits are examined from right to left (from low-order to high-order bits). Strings are added to the result from left to right, separated by the separator string (the default being the comma character ,). The number of bits examined is given by number\_of\_bits, which has a default of 64 if not specified. number\_of\_bits is silently clipped to 64 if larger than 64. It is treated as an unsigned integer, so a value of −1 is effectively the same as 64.

```
mysql> SELECT EXPORT_SET(5,'Y','N',',',4);
 -> 'Y,N,Y,N'
mysql> SELECT EXPORT_SET(6,'1','0',',',10);
 -> '0,1,1,0,0,0,0,0,0,0'
```

<span id="page-40-3"></span>• [FIELD\(](#page-40-3)str,str1,str2,str3,...)

Returns the index (position) of str in the str1, str2, str3, ... list. Returns 0 if str is not found.

If all arguments to [FIELD\(\)](#page-40-3) are strings, all arguments are compared as strings. If all arguments are numbers, they are compared as numbers. Otherwise, the arguments are compared as double.

If str is NULL, the return value is 0 because NULL fails equality comparison with any value. [FIELD\(\)](#page-40-3) is the complement of [ELT\(\)](#page-40-1).

```
mysql> SELECT FIELD('Bb', 'Aa', 'Bb', 'Cc', 'Dd', 'Ff');
 -> 2
mysql> SELECT FIELD('Gg', 'Aa', 'Bb', 'Cc', 'Dd', 'Ff');
 -> 0
```

<span id="page-40-4"></span>• [FIND\\_IN\\_SET\(](#page-40-4)str,strlist)

Returns a value in the range of 1 to N if the string str is in the string list strlist consisting of N substrings. A string list is a string composed of substrings separated by , characters. If the first argument is a constant string and the second is a column of type SET, the [FIND\\_IN\\_SET\(\)](#page-40-4) function is optimized to use bit arithmetic. Returns 0 if str is not in strlist or if strlist is the empty

string. Returns NULL if either argument is NULL. This function does not work properly if the first argument contains a comma (,) character.

```
mysql> SELECT FIND_IN_SET('b','a,b,c,d');
 -> 2
```

<span id="page-41-0"></span>• [FORMAT\(](#page-41-0)X,D[,locale])

Formats the number X to a format like '#,###,###.##', rounded to D decimal places, and returns the result as a string. If D is 0, the result has no decimal point or fractional part.

The optional third parameter enables a locale to be specified to be used for the result number's decimal point, thousands separator, and grouping between separators. Permissible locale values are the same as the legal values for the lc\_time\_names system variable (see Section 10.16, "MySQL Server Locale Support"). If no locale is specified, the default is 'en\_US'.

```
mysql> SELECT FORMAT(12332.123456, 4);
 -> '12,332.1235'
mysql> SELECT FORMAT(12332.1,4);
 -> '12,332.1000'
mysql> SELECT FORMAT(12332.2,0);
 -> '12,332'
mysql> SELECT FORMAT(12332.2,2,'de_DE');
 -> '12.332,20'
```

<span id="page-41-2"></span>• [FROM\\_BASE64\(](#page-41-2)str)

Takes a string encoded with the base-64 encoded rules used by [TO\\_BASE64\(\)](#page-47-1) and returns the decoded result as a binary string. The result is NULL if the argument is NULL or not a valid base-64 string. See the description of [TO\\_BASE64\(\)](#page-47-1) for details about the encoding and decoding rules.

```
mysql> SELECT TO_BASE64('abc'), FROM_BASE64(TO_BASE64('abc'));
 -> 'JWJj', 'abc'
```

If [FROM\\_BASE64\(\)](#page-41-2) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-41-1"></span>• [HEX\(](#page-41-1)str), [HEX\(](#page-41-1)N)

For a string argument str, [HEX\(\)](#page-41-1) returns a hexadecimal string representation of str where each byte of each character in str is converted to two hexadecimal digits. (Multibyte characters therefore become more than two digits.) The inverse of this operation is performed by the [UNHEX\(\)](#page-48-1) function.

For a numeric argument N, [HEX\(\)](#page-41-1) returns a hexadecimal string representation of the value of N treated as a longlong (BIGINT) number. This is equivalent to CONV(N[,10,16\)](#page-9-0). The inverse of this operation is performed by [CONV\(HEX\(](#page-9-0)N),16,10).

```
mysql> SELECT X'616263', HEX('abc'), UNHEX(HEX('abc'));
 -> 'abc', 616263, 'abc'
mysql> SELECT HEX(255), CONV(HEX(255),16,10);
 -> 'FF', 255
```

<span id="page-41-3"></span>• [INSERT\(](#page-41-3)str,pos,len,newstr)

Returns the string str, with the substring beginning at position pos and len characters long replaced by the string newstr. Returns the original string if pos is not within the length of the string. Replaces the rest of the string from position pos if len is not within the length of the rest of the string. Returns NULL if any argument is NULL.

```
mysql> SELECT INSERT('Quadratic', 3, 4, 'What');
 -> 'QuWhattic'
mysql> SELECT INSERT('Quadratic', -1, 4, 'What');
 -> 'Quadratic'
mysql> SELECT INSERT('Quadratic', 3, 100, 'What');
```

```
 -> 'QuWhat'
```

This function is multibyte safe.

<span id="page-42-0"></span>• [INSTR\(](#page-42-0)str,substr)

Returns the position of the first occurrence of substring substr in string str. This is the same as the two-argument form of [LOCATE\(\)](#page-42-5), except that the order of the arguments is reversed.

```
mysql> SELECT INSTR('foobarbar', 'bar');
 -> 4
mysql> SELECT INSTR('xbar', 'foobar');
 -> 0
```

This function is multibyte safe, and is case-sensitive only if at least one argument is a binary string.

<span id="page-42-1"></span>• [LCASE\(](#page-42-1)str)

```
LCASE() is a synonym for LOWER().
```

LCASE() used in a view is rewritten as LOWER() when storing the view's definition. (Bug #12844279)

<span id="page-42-2"></span>• [LEFT\(](#page-42-2)str,len)

Returns the leftmost len characters from the string str, or NULL if any argument is NULL.

```
mysql> SELECT LEFT('foobarbar', 5);
 -> 'fooba'
```

This function is multibyte safe.

<span id="page-42-3"></span>• [LENGTH\(](#page-42-3)str)

Returns the length of the string str, measured in bytes. A multibyte character counts as multiple bytes. This means that for a string containing five 2-byte characters, [LENGTH\(\)](#page-42-3) returns 10, whereas [CHAR\\_LENGTH\(\)](#page-39-1) returns 5.

```
mysql> SELECT LENGTH('text');
 -> 4
```

![](_page_42_Picture_17.jpeg)

#### **Note**

The Length() OpenGIS spatial function is named [ST\\_Length\(\)](#page-149-0) in MySQL.

<span id="page-42-4"></span>• [LOAD\\_FILE\(](#page-42-4)file\_name)

Reads the file and returns the file contents as a string. To use this function, the file must be located on the server host, you must specify the full path name to the file, and you must have the FILE privilege. The file must be readable by all and its size less than max\_allowed\_packet bytes. If the secure\_file\_priv system variable is set to a nonempty directory name, the file to be loaded must be located in that directory.

If the file does not exist or cannot be read because one of the preceding conditions is not satisfied, the function returns NULL.

The character\_set\_filesystem system variable controls interpretation of file names that are given as literal strings.

```
mysql> UPDATE t
 SET blob_col=LOAD_FILE('/tmp/picture')
 WHERE id=1;
```

<span id="page-42-5"></span>• [LOCATE\(](#page-42-5)substr,str), [LOCATE\(](#page-42-5)substr,str,pos)

The first syntax returns the position of the first occurrence of substring substr in string str. The second syntax returns the position of the first occurrence of substring substr in string str, starting at position pos. Returns 0 if substr is not in str. Returns NULL if substr or str is NULL.

```
mysql> SELECT LOCATE('bar', 'foobarbar');
 -> 4
mysql> SELECT LOCATE('xbar', 'foobar');
 -> 0
mysql> SELECT LOCATE('bar', 'foobarbar', 5);
 -> 7
```

This function is multibyte safe, and is case-sensitive only if at least one argument is a binary string.

<span id="page-43-0"></span>• [LOWER\(](#page-43-0)str)

Returns the string str with all characters changed to lowercase according to the current character set mapping. The default is latin1 (cp1252 West European).

```
mysql> SELECT LOWER('QUADRATICALLY');
 -> 'quadratically'
```

[LOWER\(\)](#page-43-0) (and [UPPER\(\)](#page-48-2)) are ineffective when applied to binary strings (BINARY, VARBINARY, BLOB). To perform lettercase conversion of a binary string, first convert it to a nonbinary string using a character set appropriate for the data stored in the string:

```
mysql> SET @str = BINARY 'New York';
mysql> SELECT LOWER(@str), LOWER(CONVERT(@str USING latin1));
+-------------+-----------------------------------+
| LOWER(@str) | LOWER(CONVERT(@str USING latin1)) |
+-------------+-----------------------------------+
| New York | new york |
+-------------+-----------------------------------+
```

For collations of Unicode character sets, [LOWER\(\)](#page-43-0) and [UPPER\(\)](#page-48-2) work according to the Unicode Collation Algorithm (UCA) version in the collation name, if there is one, and UCA 4.0.0 if no version is specified. For example, utf8\_unicode\_520\_ci works according to UCA 5.2.0, whereas utf8\_unicode\_ci works according to UCA 4.0.0. See Section 10.10.1, "Unicode Character Sets".

This function is multibyte safe.

In previous versions of MySQL, LOWER() used within a view was rewritten as [LCASE\(\)](#page-42-1) when storing the view's definition. In MySQL 5.7, LOWER() is never rewritten in such cases, but LCASE() used within views is instead rewritten as LOWER(). (Bug #12844279)

<span id="page-43-1"></span>• LPAD(str,len,[padstr](#page-43-1))

Returns the string str, left-padded with the string padstr to a length of len characters. If str is longer than len, the return value is shortened to len characters.

```
mysql> SELECT LPAD('hi',4,'??');
 -> '??hi'
mysql> SELECT LPAD('hi',1,'??');
 -> 'h'
```

<span id="page-43-2"></span>• [LTRIM\(](#page-43-2)str)

Returns the string str with leading space characters removed.

```
mysql> SELECT LTRIM(' barbar');
 -> 'barbar'
```

This function is multibyte safe.

<span id="page-44-0"></span>• [MAKE\\_SET\(](#page-44-0)bits,str1,str2,...)

Returns a set value (a string containing substrings separated by , characters) consisting of the strings that have the corresponding bit in bits set. str1 corresponds to bit 0, str2 to bit 1, and so on. NULL values in str1, str2, ... are not appended to the result.

```
mysql> SELECT MAKE_SET(1,'a','b','c');
 -> 'a'
mysql> SELECT MAKE_SET(1 | 4,'hello','nice','world');
 -> 'hello,world'
mysql> SELECT MAKE_SET(1 | 4,'hello','nice',NULL,'world');
 -> 'hello'
mysql> SELECT MAKE_SET(0,'a','b','c');
 -> ''
```

- <span id="page-44-1"></span>• [MID\(](#page-44-1)str,pos), MID(str [FROM](#page-44-1) pos), [MID\(](#page-44-1)str,pos,len), MID(str [FROM](#page-44-1) pos FOR len) [MID\(](#page-44-1)str,pos,len) is a synonym for [SUBSTRING\(](#page-46-3)str,pos,len).
- <span id="page-44-2"></span>• [OCT\(](#page-44-2)N)

Returns a string representation of the octal value of N, where N is a longlong (BIGINT) number. This is equivalent to CONV(N[,10,8\)](#page-9-0). Returns NULL if N is NULL.

```
mysql> SELECT OCT(12);
 -> '14'
```

<span id="page-44-3"></span>• [OCTET\\_LENGTH\(](#page-44-3)str)

[OCTET\\_LENGTH\(\)](#page-44-3) is a synonym for [LENGTH\(\)](#page-42-3).

<span id="page-44-4"></span>• [ORD\(](#page-44-4)str)

If the leftmost character of the string str is a multibyte character, returns the code for that character, calculated from the numeric values of its constituent bytes using this formula:

```
 (1st byte code)
+ (2nd byte code * 256)
+ (3rd byte code * 256^2) ...
```

If the leftmost character is not a multibyte character, [ORD\(\)](#page-44-4) returns the same value as the [ASCII\(\)](#page-38-0) function.

```
mysql> SELECT ORD('2');
 -> 50
```

<span id="page-44-5"></span>• [POSITION\(](#page-44-5)substr IN str)

[POSITION\(](#page-44-5)substr IN str) is a synonym for [LOCATE\(](#page-42-5)substr,str).

<span id="page-44-6"></span>• [QUOTE\(](#page-44-6)str)

Quotes a string to produce a result that can be used as a properly escaped data value in an SQL statement. The string is returned enclosed by single quotation marks and with each instance of backslash (\), single quote ('), ASCII NUL, and Control+Z preceded by a backslash. If the argument is NULL, the return value is the word "NULL" without enclosing single quotation marks.

```
mysql> SELECT QUOTE('Don\'t!');
 -> 'Don\'t!'
mysql> SELECT QUOTE(NULL);
 -> NULL
```

For comparison, see the quoting rules for literal strings and within the C API in Section 9.1.1, "String Literals", and [mysql\\_real\\_escape\\_string\\_quote\(\).](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-escape-string-quote.md)

<span id="page-45-0"></span>• [REPEAT\(](#page-45-0)str,count)

Returns a string consisting of the string str repeated count times. If count is less than 1, returns an empty string. Returns NULL if str or count are NULL.

```
mysql> SELECT REPEAT('MySQL', 3);
 -> 'MySQLMySQLMySQL'
```

<span id="page-45-1"></span>• [REPLACE\(](#page-45-1)str,from\_str,to\_str)

Returns the string str with all occurrences of the string from\_str replaced by the string to\_str. [REPLACE\(\)](#page-45-1) performs a case-sensitive match when searching for from\_str.

```
mysql> SELECT REPLACE('www.mysql.com', 'w', 'Ww');
 -> 'WwWwWw.mysql.com'
```

This function is multibyte safe.

<span id="page-45-2"></span>• [REVERSE\(](#page-45-2)str)

Returns the string str with the order of the characters reversed.

```
mysql> SELECT REVERSE('abc');
 -> 'cba'
```

This function is multibyte safe.

<span id="page-45-3"></span>• [RIGHT\(](#page-45-3)str,len)

Returns the rightmost len characters from the string str, or NULL if any argument is NULL.

```
mysql> SELECT RIGHT('foobarbar', 4);
 -> 'rbar'
```

This function is multibyte safe.

<span id="page-45-4"></span>• RPAD(str,len,[padstr](#page-45-4))

Returns the string str, right-padded with the string padstr to a length of len characters. If str is longer than len, the return value is shortened to len characters.

```
mysql> SELECT RPAD('hi',5,'?');
 -> 'hi???'
mysql> SELECT RPAD('hi',1,'?');
 -> 'h'
```

This function is multibyte safe.

<span id="page-45-5"></span>• [RTRIM\(](#page-45-5)str)

Returns the string str with trailing space characters removed.

```
mysql> SELECT RTRIM('barbar ');
 -> 'barbar'
```

This function is multibyte safe.

<span id="page-45-6"></span>• [SOUNDEX\(](#page-45-6)str)

Returns a soundex string from str. Two strings that sound almost the same should have identical soundex strings. A standard soundex string is four characters long, but the [SOUNDEX\(\)](#page-45-6) function returns an arbitrarily long string. You can use [SUBSTRING\(\)](#page-46-3) on the result to get a standard soundex string. All nonalphabetic characters in str are ignored. All international alphabetic characters outside the A-Z range are treated as vowels.

![](_page_46_Picture_2.jpeg)

#### **Important**

When using [SOUNDEX\(\)](#page-45-6), you should be aware of the following limitations:

- This function, as currently implemented, is intended to work well with strings that are in the English language only. Strings in other languages may not produce reliable results.
- This function is not guaranteed to provide consistent results with strings that use multibyte character sets, including utf-8. See Bug #22638 for more information.

```
mysql> SELECT SOUNDEX('Hello');
 -> 'H400'
mysql> SELECT SOUNDEX('Quadratically');
 -> 'Q36324'
```

![](_page_46_Picture_8.jpeg)

#### **Note**

This function implements the original Soundex algorithm, not the more popular enhanced version (also described by D. Knuth). The difference is that original version discards vowels first and duplicates second, whereas the enhanced version discards duplicates first and vowels second.

<span id="page-46-0"></span>• expr1 [SOUNDS LIKE](#page-46-0) expr2

This is the same as SOUNDEX(expr1[\) = SOUNDEX\(](#page-45-6)expr2).

<span id="page-46-1"></span>• [SPACE\(](#page-46-1)N)

Returns a string consisting of N space characters.

```
mysql> SELECT SPACE(6);
 -> ' '
```

<span id="page-46-2"></span>• [SUBSTR\(](#page-46-2)str,pos), [SUBSTR\(](#page-46-2)str FROM pos), [SUBSTR\(](#page-46-2)str,pos,len), [SUBSTR\(](#page-46-2)str FROM pos [FOR](#page-46-2) len)

[SUBSTR\(\)](#page-46-2) is a synonym for [SUBSTRING\(\)](#page-46-3).

<span id="page-46-3"></span>• [SUBSTRING\(](#page-46-3)str,pos), [SUBSTRING\(](#page-46-3)str FROM pos), [SUBSTRING\(](#page-46-3)str,pos,len), [SUBSTRING\(](#page-46-3)str FROM pos FOR len)

The forms without a len argument return a substring from string str starting at position pos. The forms with a len argument return a substring len characters long from string str, starting at position pos. The forms that use FROM are standard SQL syntax. It is also possible to use a negative value for pos. In this case, the beginning of the substring is pos characters from the end of the string, rather than the beginning. A negative value may be used for pos in any of the forms of this function. A value of 0 for pos returns an empty string.

For all forms of [SUBSTRING\(\)](#page-46-3), the position of the first character in the string from which the substring is to be extracted is reckoned as 1.

```
mysql> SELECT SUBSTRING('Quadratically',5);
 -> 'ratically'
mysql> SELECT SUBSTRING('foobarbar' FROM 4);
 -> 'barbar'
mysql> SELECT SUBSTRING('Quadratically',5,6);
 -> 'ratica'
mysql> SELECT SUBSTRING('Sakila', -3);
 -> 'ila'
mysql> SELECT SUBSTRING('Sakila', -5, 3);
 -> 'aki'
```

```
mysql> SELECT SUBSTRING('Sakila' FROM -4 FOR 2);
 -> 'ki'
```

This function is multibyte safe.

If len is less than 1, the result is the empty string.

<span id="page-47-0"></span>• [SUBSTRING\\_INDEX\(](#page-47-0)str,delim,count)

Returns the substring from string str before count occurrences of the delimiter delim. If count is positive, everything to the left of the final delimiter (counting from the left) is returned. If count is negative, everything to the right of the final delimiter (counting from the right) is returned. [SUBSTRING\\_INDEX\(\)](#page-47-0) performs a case-sensitive match when searching for delim.

```
mysql> SELECT SUBSTRING_INDEX('www.mysql.com', '.', 2);
 -> 'www.mysql'
mysql> SELECT SUBSTRING_INDEX('www.mysql.com', '.', -2);
 -> 'mysql.com'
```

This function is multibyte safe.

<span id="page-47-1"></span>• [TO\\_BASE64\(](#page-47-1)str)

Converts the string argument to base-64 encoded form and returns the result as a character string with the connection character set and collation. If the argument is not a string, it is converted to a string before conversion takes place. The result is NULL if the argument is NULL. Base-64 encoded strings can be decoded using the [FROM\\_BASE64\(\)](#page-41-2) function.

```
mysql> SELECT TO_BASE64('abc'), FROM_BASE64(TO_BASE64('abc'));
 -> 'JWJj', 'abc'
```

Different base-64 encoding schemes exist. These are the encoding and decoding rules used by [TO\\_BASE64\(\)](#page-47-1) and [FROM\\_BASE64\(\)](#page-41-2):

- The encoding for alphabet value 62 is '+'.
- The encoding for alphabet value 63 is '/'.
- Encoded output consists of groups of 4 printable characters. Each 3 bytes of the input data are encoded using 4 characters. If the last group is incomplete, it is padded with '=' characters to a length of 4.
- A newline is added after each 76 characters of encoded output to divide long output into multiple lines.
- Decoding recognizes and ignores newline, carriage return, tab, and space.
- <span id="page-47-2"></span>• [TRIM\(\[{BOTH | LEADING | TRAILING} \[](#page-47-2)remstr] FROM] str), TRIM([[remstr](#page-47-2) FROM] [str](#page-47-2))

Returns the string str with all remstr prefixes or suffixes removed. If none of the specifiers BOTH, LEADING, or TRAILING is given, BOTH is assumed. remstr is optional and, if not specified, spaces are removed.

```
mysql> SELECT TRIM(' bar ');
 -> 'bar'
mysql> SELECT TRIM(LEADING 'x' FROM 'xxxbarxxx');
 -> 'barxxx'
mysql> SELECT TRIM(BOTH 'x' FROM 'xxxbarxxx');
 -> 'bar'
mysql> SELECT TRIM(TRAILING 'xyz' FROM 'barxxyz');
 -> 'barx'
```

This function is multibyte safe.

<span id="page-48-0"></span>• [UCASE\(](#page-48-0)str)

```
UCASE() is a synonym for UPPER().
```

In MySQL 5.7, UCASE() used in a view is rewritten as UPPER() when storing the view's definition. (Bug #12844279)

<span id="page-48-1"></span>• [UNHEX\(](#page-48-1)str)

For a string argument str, [UNHEX\(](#page-48-1)str) interprets each pair of characters in the argument as a hexadecimal number and converts it to the byte represented by the number. The return value is a binary string.

```
mysql> SELECT UNHEX('4D7953514C');
 -> 'MySQL'
mysql> SELECT X'4D7953514C';
 -> 'MySQL'
mysql> SELECT UNHEX(HEX('string'));
 -> 'string'
mysql> SELECT HEX(UNHEX('1267'));
 -> '1267'
```

The characters in the argument string must be legal hexadecimal digits: '0' .. '9', 'A' .. 'F', 'a' .. 'f'. If the argument contains any nonhexadecimal digits, the result is NULL:

```
mysql> SELECT UNHEX('GG');
+-------------+
| UNHEX('GG') |
+-------------+
| NULL |
+-------------+
```

A NULL result can occur if the argument to [UNHEX\(\)](#page-48-1) is a BINARY column, because values are padded with 0x00 bytes when stored but those bytes are not stripped on retrieval. For example, '41' is stored into a CHAR(3) column as '41 ' and retrieved as '41' (with the trailing pad space stripped), so [UNHEX\(\)](#page-48-1) for the column value returns X'41'. By contrast, '41' is stored into a BINARY(3) column as '41\0' and retrieved as '41\0' (with the trailing pad 0x00 byte not stripped). '\0' is not a legal hexadecimal digit, so [UNHEX\(\)](#page-48-1) for the column value returns NULL.

For a numeric argument N, the inverse of [HEX\(](#page-41-1)N) is not performed by [UNHEX\(\)](#page-48-1). Use [CONV\(HEX\(](#page-9-0)N),16,10) instead. See the description of [HEX\(\)](#page-41-1).

If [UNHEX\(\)](#page-48-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-48-2"></span>• [UPPER\(](#page-48-2)str)

Returns the string str with all characters changed to uppercase according to the current character set mapping. The default is latin1 (cp1252 West European).

```
mysql> SELECT UPPER('Hej');
 -> 'HEJ'
```

See the description of [LOWER\(\)](#page-43-0) for information that also applies to [UPPER\(\)](#page-48-2). This included information about how to perform lettercase conversion of binary strings (BINARY, VARBINARY, BLOB) for which these functions are ineffective, and information about case folding for Unicode character sets.

This function is multibyte safe.

In previous versions of MySQL, UPPER() used within a view was rewritten as [UCASE\(\)](#page-48-0) when storing the view's definition. In MySQL 5.7, UPPER() is never rewritten in such cases, but UCASE() used within views is instead rewritten as UPPER(). (Bug #12844279)

<span id="page-49-0"></span>• WEIGHT\_STRING(str [\[AS {CHAR|BINARY}\(](#page-49-0)N)] [LEVEL levels] [flags]) levels: N [ASC|DESC|REVERSE] [, N [ASC|DESC|REVERSE]] ...

This function returns the weight string for the input string. The return value is a binary string that represents the comparison and sorting value of the string. It has these properties:

- If [WEIGHT\\_STRING\(](#page-49-0)str1) = [WEIGHT\\_STRING\(](#page-49-0)str2), then str1 = str2 (str1 and str2 are considered equal)
- If [WEIGHT\\_STRING\(](#page-49-0)str1) < [WEIGHT\\_STRING\(](#page-49-0)str2), then str1 < str2 (str1 sorts before str2)

[WEIGHT\\_STRING\(\)](#page-49-0) is a debugging function intended for internal use. Its behavior can change without notice between MySQL versions. It can be used for testing and debugging of collations, especially if you are adding a new collation. See Section 10.14, "Adding a Collation to a Character Set".

This list briefly summarizes the arguments. More details are given in the discussion following the list.

• str: The input string expression.

+------+---------+------------------------+ | ab | 6162 | 6162 |

- AS clause: Optional; cast the input string to a given type and length.
- LEVEL clause: Optional; specify weight levels for the return value.
- flags: Optional; unused.

The input string, str, is a string expression. If the input is a nonbinary (character) string such as a CHAR, VARCHAR, or TEXT value, the return value contains the collation weights for the string. If the input is a binary (byte) string such as a BINARY, VARBINARY, or BLOB value, the return value is the same as the input (the weight for each byte in a binary string is the byte value). If the input is NULL, [WEIGHT\\_STRING\(\)](#page-49-0) returns NULL.

#### Examples:

```
mysql> SET @s = _latin1 'AB' COLLATE latin1_swedish_ci;
mysql> SELECT @s, HEX(@s), HEX(WEIGHT_STRING(@s));
+------+---------+------------------------+
| @s | HEX(@s) | HEX(WEIGHT_STRING(@s)) |
+------+---------+------------------------+
| AB | 4142 | 4142 |
+------+---------+------------------------+
mysql> SET @s = _latin1 'ab' COLLATE latin1_swedish_ci;
mysql> SELECT @s, HEX(@s), HEX(WEIGHT_STRING(@s));
+------+---------+------------------------+
| @s | HEX(@s) | HEX(WEIGHT_STRING(@s)) |
+------+---------+------------------------+
| ab | 6162 | 4142 |
+------+---------+------------------------+
mysql> SET @s = CAST('AB' AS BINARY);
mysql> SELECT @s, HEX(@s), HEX(WEIGHT_STRING(@s));
+------+---------+------------------------+
| @s | HEX(@s) | HEX(WEIGHT_STRING(@s)) |
+------+---------+------------------------+
| AB | 4142 | 4142 |
+------+---------+------------------------+
mysql> SET @s = CAST('ab' AS BINARY);
mysql> SELECT @s, HEX(@s), HEX(WEIGHT_STRING(@s));
+------+---------+------------------------+
| @s | HEX(@s) | HEX(WEIGHT_STRING(@s)) |
```

+------+---------+------------------------+

The preceding examples use [HEX\(\)](#page-41-1) to display the [WEIGHT\\_STRING\(\)](#page-49-0) result. Because the result is a binary value, [HEX\(\)](#page-41-1) can be especially useful when the result contains nonprinting values, to display it in printable form:

```
mysql> SET @s = CONVERT(X'C39F' USING utf8) COLLATE utf8_czech_ci;
mysql> SELECT HEX(WEIGHT_STRING(@s));
+------------------------+
| HEX(WEIGHT_STRING(@s)) |
+------------------------+
| 0FEA0FEA |
+------------------------+
```

For non-NULL return values, the data type of the value is VARBINARY if its length is within the maximum length for VARBINARY, otherwise the data type is BLOB.

The AS clause may be given to cast the input string to a nonbinary or binary string and to force it to a given length:

- AS CHAR(N) casts the string to a nonbinary string and pads it on the right with spaces to a length of N characters. N must be at least 1. If N is less than the length of the input string, the string is truncated to N characters. No warning occurs for truncation.
- AS BINARY(N) is similar but casts the string to a binary string, N is measured in bytes (not characters), and padding uses 0x00 bytes (not spaces).

```
mysql> SET NAMES 'latin1';
mysql> SELECT HEX(WEIGHT_STRING('ab' AS CHAR(4)));
+-------------------------------------+
| HEX(WEIGHT_STRING('ab' AS CHAR(4))) |
+-------------------------------------+
| 41422020 |
+-------------------------------------+
mysql> SET NAMES 'utf8';
mysql> SELECT HEX(WEIGHT_STRING('ab' AS CHAR(4)));
+-------------------------------------+
| HEX(WEIGHT_STRING('ab' AS CHAR(4))) |
+-------------------------------------+
| 0041004200200020 |
+-------------------------------------+
```

```
mysql> SELECT HEX(WEIGHT_STRING('ab' AS BINARY(4)));
+---------------------------------------+
| HEX(WEIGHT_STRING('ab' AS BINARY(4))) |
+---------------------------------------+
| 61620000 |
+---------------------------------------+
```

The LEVEL clause may be given to specify that the return value should contain weights for specific collation levels.

The levels specifier following the LEVEL keyword may be given either as a list of one or more integers separated by commas, or as a range of two integers separated by a dash. Whitespace around the punctuation characters does not matter.

#### Examples:

```
LEVEL 1
LEVEL 2, 3, 5
```

```
LEVEL 1-3
```

Any level less than 1 is treated as 1. Any level greater than the maximum for the input string collation is treated as maximum for the collation. The maximum varies per collation, but is never greater than 6.

In a list of levels, levels must be given in increasing order. In a range of levels, if the second number is less than the first, it is treated as the first number (for example, 4-2 is the same as 4-4).

If the LEVEL clause is omitted, MySQL assumes LEVEL 1 - max, where max is the maximum level for the collation.

If LEVEL is specified using list syntax (not range syntax), any level number can be followed by these modifiers:

- ASC: Return the weights without modification. This is the default.
- DESC: Return bitwise-inverted weights (for example, 0x78f0 DESC = 0x870f).
- REVERSE: Return the weights in reverse order (that is,the weights for the reversed string, with the first character last and the last first).

#### Examples:

```
mysql> SELECT HEX(WEIGHT_STRING(0x007fff LEVEL 1));
+--------------------------------------+
| HEX(WEIGHT_STRING(0x007fff LEVEL 1)) |
+--------------------------------------+
| 007FFF |
+--------------------------------------+
mysql> SELECT HEX(WEIGHT_STRING(0x007fff LEVEL 1 DESC));
+-------------------------------------------+
| HEX(WEIGHT_STRING(0x007fff LEVEL 1 DESC)) |
+-------------------------------------------+
| FF8000 |
+-------------------------------------------+
mysql> SELECT HEX(WEIGHT_STRING(0x007fff LEVEL 1 REVERSE));
+----------------------------------------------+
| HEX(WEIGHT_STRING(0x007fff LEVEL 1 REVERSE)) |
+----------------------------------------------+
| FF7F00 |
+----------------------------------------------+
mysql> SELECT HEX(WEIGHT_STRING(0x007fff LEVEL 1 DESC REVERSE));
+---------------------------------------------------+
| HEX(WEIGHT_STRING(0x007fff LEVEL 1 DESC REVERSE)) |
+---------------------------------------------------+
| 0080FF |
+---------------------------------------------------+
```

The flags clause currently is unused.

If [WEIGHT\\_STRING\(\)](#page-49-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

# <span id="page-51-0"></span>**12.8.1 String Comparison Functions and Operators**

**Table 12.13 String Comparison Functions and Operators**

| Name     | Description                         |
|----------|-------------------------------------|
| LIKE     | Simple pattern matching             |
| NOT LIKE | Negation of simple pattern matching |

| Name     | Description         |
|----------|---------------------|
| STRCMP() | Compare two strings |

If a string function is given a binary string as an argument, the resulting string is also a binary string. A number converted to a string is treated as a binary string. This affects only comparisons.

Normally, if any expression in a string comparison is case-sensitive, the comparison is performed in case-sensitive fashion.

If a string function is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-52-0"></span>• expr LIKE pat [ESCAPE '[escape\\_char](#page-52-0)']

Pattern matching using an SQL pattern. Returns 1 (TRUE) or 0 (FALSE). If either expr or pat is NULL, the result is NULL.

The pattern need not be a literal string. For example, it can be specified as a string expression or table column. In the latter case, the column must be defined as one of the MySQL string types (see Section 11.3, "String Data Types").

Per the SQL standard, [LIKE](#page-52-0) performs matching on a per-character basis, thus it can produce results different from the = comparison operator:

```
mysql> SELECT 'ä' LIKE 'ae' COLLATE latin1_german2_ci;
+-----------------------------------------+
| 'ä' LIKE 'ae' COLLATE latin1_german2_ci |
+-----------------------------------------+
| 0 |
+-----------------------------------------+
mysql> SELECT 'ä' = 'ae' COLLATE latin1_german2_ci;
+--------------------------------------+
| 'ä' = 'ae' COLLATE latin1_german2_ci |
+--------------------------------------+
| 1 |
+--------------------------------------+
```

In particular, trailing spaces are significant, which is not true for comparisons of nonbinary strings (CHAR, VARCHAR, and TEXT values) performed with the = operator:

```
mysql> SELECT 'a' = 'a ', 'a' LIKE 'a ';
+------------+---------------+
| 'a' = 'a ' | 'a' LIKE 'a ' |
+------------+---------------+
| 1 | 0 |
+------------+---------------+
1 row in set (0.00 sec)
```

With [LIKE](#page-52-0) you can use the following two wildcard characters in the pattern:

- % matches any number of characters, even zero characters.
- \_ matches exactly one character.

```
mysql> SELECT 'David!' LIKE 'David_';
 -> 1
mysql> SELECT 'David!' LIKE '%D%v%';
 -> 1
```

To test for literal instances of a wildcard character, precede it by the escape character. If you do not specify the ESCAPE character, \ is assumed, unless the NO\_BACKSLASH\_ESCAPES SQL mode is enabled. In that case, no escape character is used.

• \% matches one % character.

• \\_ matches one \_ character.

```
mysql> SELECT 'David!' LIKE 'David\_';
 -> 0
mysql> SELECT 'David_' LIKE 'David\_';
 -> 1
```

To specify a different escape character, use the ESCAPE clause:

```
mysql> SELECT 'David_' LIKE 'David|_' ESCAPE '|';
 -> 1
```

The escape sequence should be one character long to specify the escape character, or empty to specify that no escape character is used. The expression must evaluate as a constant at execution time. If the NO\_BACKSLASH\_ESCAPES SQL mode is enabled, the sequence cannot be empty.

The following statements illustrate that string comparisons are not case-sensitive unless one of the operands is case-sensitive (uses a case-sensitive collation or is a binary string):

```
mysql> SELECT 'abc' LIKE 'ABC';
 -> 1
mysql> SELECT 'abc' LIKE _latin1 'ABC' COLLATE latin1_general_cs;
 -> 0
mysql> SELECT 'abc' LIKE _latin1 'ABC' COLLATE latin1_bin;
 -> 0
mysql> SELECT 'abc' LIKE BINARY 'ABC';
 -> 0
```

As an extension to standard SQL, MySQL permits [LIKE](#page-52-0) on numeric expressions.

```
mysql> SELECT 10 LIKE '1%';
 -> 1
```

MySQL attempts in such cases to perform implicit conversion of the expression to a string. See Section 12.3, "Type Conversion in Expression Evaluation".

![](_page_53_Picture_11.jpeg)

## **Note**

MySQL uses C escape syntax in strings (for example, \n to represent the newline character). If you want a [LIKE](#page-52-0) string to contain a literal \, you must double it. (Unless the NO\_BACKSLASH\_ESCAPES SQL mode is enabled, in which case no escape character is used.) For example, to search for \n, specify it as \\n. To search for \, specify it as \\\\; this is because the backslashes are stripped once by the parser and again when the pattern match is made, leaving a single backslash to be matched against.

Exception: At the end of the pattern string, backslash can be specified as \\. At the end of the string, backslash stands for itself because there is nothing following to escape. Suppose that a table contains the following values:

```
mysql> SELECT filename FROM t1;
+--------------+
| filename |
+--------------+
| C: |
| C:\ |
| C:\Programs |
| C:\Programs\ |
+--------------+
```

To test for values that end with backslash, you can match the values using either of the following patterns:

```
mysql> SELECT filename, filename LIKE '%\\' FROM t1;
+--------------+---------------------+
```

```
| filename | filename LIKE '%\\' |
+--------------+---------------------+
| C: | 0 |
| C:\ | 1 |
| C:\Programs | 0 |
| C:\Programs\ | 1 |
+--------------+---------------------+
mysql> SELECT filename, filename LIKE '%\\\\' FROM t1;
+--------------+-----------------------+
| filename | filename LIKE '%\\\\' |
+--------------+-----------------------+
| C: | 0 |
| C:\ | 1 |
| C:\Programs | 0 |
| C:\Programs\ | 1 |
+--------------+-----------------------+
```

<span id="page-54-0"></span>• expr NOT LIKE pat [ESCAPE '[escape\\_char](#page-54-0)']

This is the same as NOT (expr LIKE pat [ESCAPE 'escape\_char']).

![](_page_54_Picture_4.jpeg)

### **Note**

Aggregate queries involving [NOT LIKE](#page-54-0) comparisons with columns containing NULL may yield unexpected results. For example, consider the following table and data:

```
CREATE TABLE foo (bar VARCHAR(10));
INSERT INTO foo VALUES (NULL), (NULL);
```

The query SELECT COUNT(\*) FROM foo WHERE bar LIKE '%baz%'; returns 0. You might assume that SELECT COUNT(\*) FROM foo WHERE bar NOT LIKE '%baz%'; would return 2. However, this is not the case: The second query returns 0. This is because NULL NOT LIKE expr always returns NULL, regardless of the value of expr. The same is true for aggregate queries involving NULL and comparisons using [NOT RLIKE](#page-55-0) or [NOT REGEXP](#page-55-0). In such cases, you must test explicitly for NOT NULL using [OR](#page-0-0) (and not AND), as shown here:

SELECT COUNT(\*) FROM foo WHERE bar NOT LIKE '%baz%' OR bar IS NULL;

<span id="page-54-1"></span>• [STRCMP\(](#page-54-1)expr1,expr2)

[STRCMP\(\)](#page-54-1) returns 0 if the strings are the same, -1 if the first argument is smaller than the second according to the current sort order, and 1 otherwise.

```
mysql> SELECT STRCMP('text', 'text2');
 -> -1
mysql> SELECT STRCMP('text2', 'text');
 -> 1
mysql> SELECT STRCMP('text', 'text');
 -> 0
```

[STRCMP\(\)](#page-54-1) performs the comparison using the collation of the arguments.

```
mysql> SET @s1 = _latin1 'x' COLLATE latin1_general_ci;
mysql> SET @s2 = _latin1 'X' COLLATE latin1_general_ci;
mysql> SET @s3 = _latin1 'x' COLLATE latin1_general_cs;
mysql> SET @s4 = _latin1 'X' COLLATE latin1_general_cs;
mysql> SELECT STRCMP(@s1, @s2), STRCMP(@s3, @s4);
+------------------+------------------+
| STRCMP(@s1, @s2) | STRCMP(@s3, @s4) |
+------------------+------------------+
| 0 | 1 |
```

+------------------+------------------+

If the collations are incompatible, one of the arguments must be converted to be compatible with the other. See Section 10.8.4, "Collation Coercibility in Expressions".

```
mysql> SELECT STRCMP(@s1, @s3);
ERROR 1267 (HY000): Illegal mix of collations (latin1_general_ci,IMPLICIT)
and (latin1_general_cs,IMPLICIT) for operation 'strcmp'
mysql> SELECT STRCMP(@s1, @s3 COLLATE latin1_general_ci);
+--------------------------------------------+
| STRCMP(@s1, @s3 COLLATE latin1_general_ci) |
+--------------------------------------------+
| 0 |
+--------------------------------------------+
```