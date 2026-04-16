---
source: MySQL 5.7 Reference
title: 00_Overview
---

See the files sql/opt\_trace\*, starting with sql/opt\_trace.h. A trace is started by creating an instance of Opt\_trace\_start; information is added to this trace by creating instances of Opt\_trace\_object and Opt\_trace\_array, and by using the add() methods of these classes.

# Chapter 9 Language Structure

# **Table of Contents**

| 9.1 Literal Values 1539                         |      |
|-------------------------------------------------|------|
| 9.1.1 String Literals 1539                      |      |
| 9.1.2 Numeric Literals 1542                     |      |
| 9.1.3 Date and Time Literals 1542               |      |
| 9.1.4 Hexadecimal Literals 1544                 |      |
| 9.1.5 Bit-Value Literals 1546                   |      |
| 9.1.6 Boolean Literals 1547                     |      |
| 9.1.7 NULL Values 1548                          |      |
| 9.2 Schema Object Names 1548                    |      |
| 9.2.1 Identifier Length Limits 1549             |      |
| 9.2.2 Identifier Qualifiers 1550                |      |
| 9.2.3 Identifier Case Sensitivity 1552          |      |
| 9.2.4 Mapping of Identifiers to File Names 1554 |      |
| 9.2.5 Function Name Parsing and Resolution 1556 |      |
| 9.3 Keywords and Reserved Words 1560            |      |
| 9.4 User-Defined Variables 1582                 |      |
| 9.5 Expressions 1585                            |      |
| 9.6 Comments                                    | 1589 |
|                                                 |      |

This chapter discusses the rules for writing the following elements of SQL statements when using MySQL:

- Literal values such as strings and numbers
- Identifiers such as database, table, and column names
- Keywords and reserved words
- User-defined and system variables
- Expressions
- Comments

# <span id="page-166-0"></span>**9.1 Literal Values**

This section describes how to write literal values in MySQL. These include strings, numbers, hexadecimal and bit values, boolean values, and NULL. The section also covers various nuances that you may encounter when dealing with these basic types in MySQL.

# <span id="page-166-1"></span>**9.1.1 String Literals**

A string is a sequence of bytes or characters, enclosed within either single quote (') or double quote (") characters. Examples:

```
'a string'
"another string"
```

Quoted strings placed next to each other are concatenated to a single string. The following lines are equivalent:

```
'a string'
'a' ' ' 'string'
```

If the ANSI\_QUOTES SQL mode is enabled, string literals can be quoted only within single quotation marks because a string quoted within double quotation marks is interpreted as an identifier.

A binary string is a string of bytes. Every binary string has a character set and collation named binary. A nonbinary string is a string of characters. It has a character set other than binary and a collation that is compatible with the character set.

For both types of strings, comparisons are based on the numeric values of the string unit. For binary strings, the unit is the byte; comparisons use numeric byte values. For nonbinary strings, the unit is the character and some character sets support multibyte characters; comparisons use numeric character code values. Character code ordering is a function of the string collation. (For more information, see Section 10.8.5, "The binary Collation Compared to \_bin Collations".)

![](_page_167_Picture_4.jpeg)

#### **Note**

Within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

A character string literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name]'string' [COLLATE collation_name]
```

#### Examples:

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8'string' COLLATE utf8_danish_ci;
```

You can use N'literal' (or n'literal') to create a string in the national character set. These statements are equivalent:

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

For information about these forms of string syntax, see Section 10.3.7, "The National Character Set", and Section 10.3.8, "Character Set Introducers".

Within a string, certain sequences have special meaning unless the NO\_BACKSLASH\_ESCAPES SQL mode is enabled. Each of these sequences begins with a backslash (\), known as the escape character. MySQL recognizes the escape sequences shown in [Table 9.1, "Special Character Escape](#page-167-0) [Sequences"](#page-167-0). For all other escape sequences, backslash is ignored. That is, the escaped character is interpreted as if it was not escaped. For example, \x is just x. These sequences are case-sensitive. For example, \b is interpreted as a backspace, but \B is interpreted as B. Escape processing is done according to the character set indicated by the character\_set\_connection system variable. This is true even for strings that are preceded by an introducer that indicates a different character set, as discussed in Section 10.3.6, "Character String Literal Character Set and Collation".

**Table 9.1 Special Character Escape Sequences**

<span id="page-167-0"></span>

| Escape Sequence | Character Represented by Sequence |
|-----------------|-----------------------------------|
| \0              | An ASCII NUL (X'00') character    |
| \'              | A single quote (') character      |
| \"              | A double quote (") character      |
| \b              | A backspace character             |
| \n              | A newline (linefeed) character    |
| \r              | A carriage return character       |

| Escape Sequence | Character Represented by Sequence                  |
|-----------------|----------------------------------------------------|
| \t              | A tab character                                    |
| \Z              | ASCII 26 (Control+Z); see note following the table |
| \\              | A backslash (\) character                          |
| \%              | A % character; see note following the table        |
| \_              | A _ character; see note following the table        |

The ASCII 26 character can be encoded as \Z to enable you to work around the problem that ASCII 26 stands for END-OF-FILE on Windows. ASCII 26 within a file causes problems if you try to use mysql db\_name < file\_name.

The \% and \\_ sequences are used to search for literal instances of % and \_ in pattern-matching contexts where they would otherwise be interpreted as wildcard characters. See the description of the LIKE operator in Section 12.8.1, "String Comparison Functions and Operators". If you use \% or \\_ outside of pattern-matching contexts, they evaluate to the strings \% and \\_, not to % and \_.

There are several ways to include quote characters within a string:

- A ' inside a string quoted with ' may be written as ''.
- A " inside a string quoted with " may be written as "".
- Precede the quote character by an escape character (\).
- A ' inside a string quoted with " needs no special treatment and need not be doubled or escaped. In the same way, " inside a string quoted with ' needs no special treatment.

The following SELECT statements demonstrate how quoting and escaping work:

```
mysql> SELECT 'hello', '"hello"', '""hello""', 'hel''lo', '\'hello';
+-------+---------+-----------+--------+--------+
| hello | "hello" | ""hello"" | hel'lo | 'hello |
+-------+---------+-----------+--------+--------+
mysql> SELECT "hello", "'hello'", "''hello''", "hel""lo", "\"hello";
+-------+---------+-----------+--------+--------+
| hello | 'hello' | ''hello'' | hel"lo | "hello |
+-------+---------+-----------+--------+--------+
mysql> SELECT 'This\nIs\nFour\nLines';
+--------------------+
| This
Is
Four
Lines |
+--------------------+
mysql> SELECT 'disappearing\ backslash';
+------------------------+
| disappearing backslash |
+------------------------+
```

To insert binary data into a string column (such as a BLOB column), you should represent certain characters by escape sequences. Backslash (\) and the quote character used to quote the string must be escaped. In certain client environments, it may also be necessary to escape NUL or Control +Z. The mysql client truncates quoted strings containing NUL characters if they are not escaped, and Control+Z may be taken for END-OF-FILE on Windows if not escaped. For the escape sequences that represent each of these characters, see [Table 9.1, "Special Character Escape Sequences"](#page-167-0).

When writing application programs, any string that might contain any of these special characters must be properly escaped before the string is used as a data value in an SQL statement that is sent to the MySQL server. You can do this in two ways:

- Process the string with a function that escapes the special characters. In a C program, you can use the [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-escape-string-quote.md) C API function to escape characters. See [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-escape-string-quote.md). Within SQL statements that construct other SQL statements, you can use the QUOTE() function. The Perl DBI interface provides a quote method to convert special characters to the proper escape sequences. See Section 27.9, "MySQL Perl API". Other language interfaces may provide a similar capability.
- As an alternative to explicitly escaping special characters, many MySQL APIs provide a placeholder capability that enables you to insert special markers into a statement string, and then bind data values to them when you issue the statement. In this case, the API takes care of escaping special characters in the values for you.

# <span id="page-169-0"></span>**9.1.2 Numeric Literals**

Number literals include exact-value (integer and DECIMAL) literals and approximate-value (floatingpoint) literals.

Integers are represented as a sequence of digits. Numbers may include . as a decimal separator. Numbers may be preceded by - or + to indicate a negative or positive value, respectively. Numbers represented in scientific notation with a mantissa and exponent are approximate-value numbers.

Exact-value numeric literals have an integer part or fractional part, or both. They may be signed. Examples: 1, .2, 3.4, -5, -6.78, +9.10.

Approximate-value numeric literals are represented in scientific notation with a mantissa and exponent. Either or both parts may be signed. Examples: 1.2E3, 1.2E-3, -1.2E3, -1.2E-3.

Two numbers that look similar may be treated differently. For example, 2.34 is an exact-value (fixedpoint) number, whereas 2.34E0 is an approximate-value (floating-point) number.

The DECIMAL data type is a fixed-point type and calculations are exact. In MySQL, the DECIMAL type has several synonyms: NUMERIC, DEC, FIXED. The integer types also are exact-value types. For more information about exact-value calculations, see Section 12.21, "Precision Math".

The FLOAT and DOUBLE data types are floating-point types and calculations are approximate. In MySQL, types that are synonymous with FLOAT or DOUBLE are DOUBLE PRECISION and REAL.

An integer may be used in floating-point context; it is interpreted as the equivalent floating-point number.

## <span id="page-169-1"></span>**9.1.3 Date and Time Literals**

- [Standard SQL and ODBC Date and Time Literals](#page-169-2)
- [String and Numeric Literals in Date and Time Context](#page-170-0)

Date and time values can be represented in several formats, such as quoted strings or as numbers, depending on the exact type of the value and other factors. For example, in contexts where MySQL expects a date, it interprets any of '2015-07-21', '20150721', and 20150721 as a date.

This section describes the acceptable formats for date and time literals. For more information about the temporal data types, such as the range of permitted values, see Section 11.2, "Date and Time Data Types".

### <span id="page-169-2"></span>**Standard SQL and ODBC Date and Time Literals**

Standard SQL requires temporal literals to be specified using a type keyword and a string. The space between the keyword and string is optional.

```
DATE 'str'
TIME 'str'
```

```
TIMESTAMP 'str'
```

MySQL recognizes but, unlike standard SQL, does not require the type keyword. Applications that are to be standard-compliant should include the type keyword for temporal literals.

MySQL also recognizes the ODBC syntax corresponding to the standard SQL syntax:

```
{ d 'str' }
{ t 'str' }
{ ts 'str' }
```

MySQL uses the type keywords and the ODBC constructions to produce DATE, TIME, and DATETIME values, respectively, including a trailing fractional seconds part if specified. The TIMESTAMP syntax produces a DATETIME value in MySQL because DATETIME has a range that more closely corresponds to the standard SQL TIMESTAMP type, which has a year range from 0001 to 9999. (The MySQL TIMESTAMP year range is 1970 to 2038.)

## <span id="page-170-0"></span>**String and Numeric Literals in Date and Time Context**

MySQL recognizes DATE values in these formats:

- As a string in either 'YYYY-MM-DD' or 'YY-MM-DD' format. A "relaxed" syntax is permitted: Any punctuation character may be used as the delimiter between date parts. For example, '2012-12-31', '2012/12/31', '2012^12^31', and '2012@12@31' are equivalent.
- As a string with no delimiters in either 'YYYYMMDD' or 'YYMMDD' format, provided that the string makes sense as a date. For example, '20070523' and '070523' are interpreted as '2007-05-23', but '071332' is illegal (it has nonsensical month and day parts) and becomes '0000-00-00'.
- As a number in either YYYYMMDD or YYMMDD format, provided that the number makes sense as a date. For example, 19830905 and 830905 are interpreted as '1983-09-05'.

MySQL recognizes DATETIME and TIMESTAMP values in these formats:

• As a string in either 'YYYY-MM-DD hh:mm:ss' or 'YY-MM-DD hh:mm:ss' format. A "relaxed" syntax is permitted here, too: Any punctuation character may be used as the delimiter between date parts or time parts. For example, '2012-12-31 11:30:45', '2012^12^31 11+30+45', '2012/12/31 11\*30\*45', and '2012@12@31 11^30^45' are equivalent.

The only delimiter recognized between a date and time part and a fractional seconds part is the decimal point.

The date and time parts can be separated by T rather than a space. For example, '2012-12-31 11:30:45' '2012-12-31T11:30:45' are equivalent.

- As a string with no delimiters in either 'YYYYMMDDhhmmss' or 'YYMMDDhhmmss' format, provided that the string makes sense as a date. For example, '20070523091528' and '070523091528' are interpreted as '2007-05-23 09:15:28', but '071122129015' is illegal (it has a nonsensical minute part) and becomes '0000-00-00 00:00:00'.
- As a number in either YYYYMMDDhhmmss or YYMMDDhhmmss format, provided that the number makes sense as a date. For example, 19830905132800 and 830905132800 are interpreted as '1983-09-05 13:28:00'.

A DATETIME or TIMESTAMP value can include a trailing fractional seconds part in up to microseconds (6 digits) precision. The fractional part should always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is recognized. For information about fractional seconds support in MySQL, see Section 11.2.7, "Fractional Seconds in Time Values".

Dates containing two-digit year values are ambiguous because the century is unknown. MySQL interprets two-digit year values using these rules:

- Year values in the range 70-99 become 1970-1999.
- Year values in the range 00-69 become 2000-2069.

See also Section 11.2.10, "2-Digit Years in Dates".

For values specified as strings that include date part delimiters, it is unnecessary to specify two digits for month or day values that are less than 10. '2015-6-9' is the same as '2015-06-09'. Similarly, for values specified as strings that include time part delimiters, it is unnecessary to specify two digits for hour, minute, or second values that are less than 10. '2015-10-30 1:2:3' is the same as '2015-10-30 01:02:03'.

Values specified as numbers should be 6, 8, 12, or 14 digits long. If a number is 8 or 14 digits long, it is assumed to be in YYYYMMDD or YYYYMMDDhhmmss format and that the year is given by the first 4 digits. If the number is 6 or 12 digits long, it is assumed to be in YYMMDD or YYMMDDhhmmss format and that the year is given by the first 2 digits. Numbers that are not one of these lengths are interpreted as though padded with leading zeros to the closest length.

Values specified as nondelimited strings are interpreted according their length. For a string 8 or 14 characters long, the year is assumed to be given by the first 4 characters. Otherwise, the year is assumed to be given by the first 2 characters. The string is interpreted from left to right to find year, month, day, hour, minute, and second values, for as many parts as are present in the string. This means you should not use strings that have fewer than 6 characters. For example, if you specify '9903', thinking that represents March, 1999, MySQL converts it to the "zero" date value. This occurs because the year and month values are 99 and 03, but the day part is completely missing. However, you can explicitly specify a value of zero to represent missing month or day parts. For example, to insert the value '1999-03-00', use '990300'.

MySQL recognizes TIME values in these formats:

- As a string in 'D hh:mm:ss' format. You can also use one of the following "relaxed" syntaxes: 'hh:mm:ss', 'hh:mm', 'D hh:mm', 'D hh', or 'ss'. Here D represents days and can have a value from 0 to 34.
- As a string with no delimiters in 'hhmmss' format, provided that it makes sense as a time. For example, '101112' is understood as '10:11:12', but '109712' is illegal (it has a nonsensical minute part) and becomes '00:00:00'.
- As a number in hhmmss format, provided that it makes sense as a time. For example, 101112 is understood as '10:11:12'. The following alternative formats are also understood: ss, mmss, or hhmmss.

A trailing fractional seconds part is recognized in the 'D hh:mm:ss.fraction', 'hh:mm:ss.fraction', 'hhmmss.fraction', and hhmmss.fraction time formats, where fraction is the fractional part in up to microseconds (6 digits) precision. The fractional part should always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is recognized. For information about fractional seconds support in MySQL, see Section 11.2.7, "Fractional Seconds in Time Values".

For TIME values specified as strings that include a time part delimiter, it is unnecessary to specify two digits for hours, minutes, or seconds values that are less than 10. '8:3:2' is the same as '08:03:02'.

## <span id="page-171-0"></span>**9.1.4 Hexadecimal Literals**

Hexadecimal literal values are written using X'val' or 0xval notation, where val contains hexadecimal digits (0..9, A..F). Lettercase of the digits and of any leading X does not matter. A leading 0x is case-sensitive and cannot be written as 0X.

Legal hexadecimal literals:

X'01AF'

```
X'01af'
x'01AF'
x'01af'
0x01AF
0x01af
```

#### Illegal hexadecimal literals:

```
X'0G' (G is not a hexadecimal digit)
0X01AF (0X must be written as 0x)
```

Values written using X'val' notation must contain an even number of digits or a syntax error occurs. To correct the problem, pad the value with a leading zero:

```
mysql> SET @s = X'FFF';
ERROR 1064 (42000): You have an error in your SQL syntax;
check the manual that corresponds to your MySQL server
version for the right syntax to use near 'X'FFF''
mysql> SET @s = X'0FFF';
Query OK, 0 rows affected (0.00 sec)
```

Values written using 0xval notation that contain an odd number of digits are treated as having an extra leading 0. For example, 0xaaa is interpreted as 0x0aaa.

By default, a hexadecimal literal is a binary string, where each pair of hexadecimal digits represents a character:

```
mysql> SELECT X'4D7953514C', CHARSET(X'4D7953514C');
+---------------+------------------------+
| X'4D7953514C' | CHARSET(X'4D7953514C') |
+---------------+------------------------+
| MySQL | binary |
+---------------+------------------------+
mysql> SELECT 0x5461626c65, CHARSET(0x5461626c65);
+--------------+-----------------------+
| 0x5461626c65 | CHARSET(0x5461626c65) |
+--------------+-----------------------+
| Table | binary |
+--------------+-----------------------+
```

A hexadecimal literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name] X'val' [COLLATE collation_name]
```

#### Examples:

```
SELECT _latin1 X'4D7953514C';
SELECT _utf8 0x4D7953514C COLLATE utf8_danish_ci;
```

The examples use X'val' notation, but 0xval notation permits introducers as well. For information about introducers, see Section 10.3.8, "Character Set Introducers".

In numeric contexts, MySQL treats a hexadecimal literal like a BIGINT UNSIGNED (64-bit unsigned integer). To ensure numeric treatment of a hexadecimal literal, use it in numeric context. Ways to do this include adding 0 or using CAST(... AS UNSIGNED). For example, a hexadecimal literal assigned to a user-defined variable is a binary string by default. To assign the value as a number, use it in numeric context:

```
mysql> SET @v1 = X'41';
mysql> SET @v2 = X'41'+0;
mysql> SET @v3 = CAST(X'41' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
+------+------+------+
| A | 65 | 65 |
+------+------+------+
```

An empty hexadecimal value (X'') evaluates to a zero-length binary string. Converted to a number, it produces 0:

```
mysql> SELECT CHARSET(X''), LENGTH(X'');
+--------------+-------------+
| CHARSET(X'') | LENGTH(X'') |
+--------------+-------------+
| binary | 0 |
+--------------+-------------+
mysql> SELECT X''+0;
+-------+
| X''+0 |
+-------+
| 0 |
+-------+
```

The X'val' notation is based on standard SQL. The 0x notation is based on ODBC, for which hexadecimal strings are often used to supply values for BLOB columns.

To convert a string or a number to a string in hexadecimal format, use the HEX() function:

```
mysql> SELECT HEX('cat');
+------------+
| HEX('cat') |
+------------+
| 636174 |
+------------+
mysql> SELECT X'636174';
+-----------+
| X'636174' |
+-----------+
| cat |
+-----------+
```

## <span id="page-173-0"></span>**9.1.5 Bit-Value Literals**

Bit-value literals are written using b'val' or 0bval notation. val is a binary value written using zeros and ones. Lettercase of any leading b does not matter. A leading 0b is case-sensitive and cannot be written as 0B.

Legal bit-value literals:

```
b'01'
B'01'
0b01
```

Illegal bit-value literals:

```
b'2' (2 is not a binary digit)
0B01 (0B must be written as 0b)
```

By default, a bit-value literal is a binary string:

```
mysql> SELECT b'1000001', CHARSET(b'1000001');
+------------+---------------------+
| b'1000001' | CHARSET(b'1000001') |
+------------+---------------------+
| A | binary |
+------------+---------------------+
mysql> SELECT 0b1100001, CHARSET(0b1100001);
+-----------+--------------------+
| 0b1100001 | CHARSET(0b1100001) |
+-----------+--------------------+
| a | binary |
+-----------+--------------------+
```

A bit-value literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name] b'val' [COLLATE collation_name]
```

#### Examples:

```
SELECT _latin1 b'1000001';
SELECT _utf8 0b1000001 COLLATE utf8_danish_ci;
```

The examples use b'val' notation, but 0bval notation permits introducers as well. For information about introducers, see Section 10.3.8, "Character Set Introducers".

In numeric contexts, MySQL treats a bit literal like an integer. To ensure numeric treatment of a bit literal, use it in numeric context. Ways to do this include adding 0 or using CAST(... AS UNSIGNED). For example, a bit literal assigned to a user-defined variable is a binary string by default. To assign the value as a number, use it in numeric context:

```
mysql> SET @v1 = b'1100001';
mysql> SET @v2 = b'1100001'+0;
mysql> SET @v3 = CAST(b'1100001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
+------+------+------+
| a | 97 | 97 |
+------+------+------+
```

An empty bit value (b'') evaluates to a zero-length binary string. Converted to a number, it produces 0:

```
mysql> SELECT CHARSET(b''), LENGTH(b'');
+--------------+-------------+
| CHARSET(b'') | LENGTH(b'') |
+--------------+-------------+
| binary | 0 |
+--------------+-------------+
mysql> SELECT b''+0;
+-------+
| b''+0 |
+-------+
| 0 |
+-------+
```

Bit-value notation is convenient for specifying values to be assigned to BIT columns:

```
mysql> CREATE TABLE t (b BIT(8));
mysql> INSERT INTO t SET b = b'11111111';
mysql> INSERT INTO t SET b = b'1010';
mysql> INSERT INTO t SET b = b'0101';
```

Bit values in result sets are returned as binary values, which may not display well. To convert a bit value to printable form, use it in numeric context or use a conversion function such as BIN() or HEX(). High-order 0 digits are not displayed in the converted value.

```
mysql> SELECT b+0, BIN(b), OCT(b), HEX(b) FROM t;
+------+----------+--------+--------+
| b+0 | BIN(b) | OCT(b) | HEX(b) |
+------+----------+--------+--------+
| 255 | 11111111 | 377 | FF |
| 10 | 1010 | 12 | A |
| 5 | 101 | 5 | 5 |
+------+----------+--------+--------+
```

## <span id="page-174-0"></span>**9.1.6 Boolean Literals**

The constants TRUE and FALSE evaluate to 1 and 0, respectively. The constant names can be written in any lettercase.

```
mysql> SELECT TRUE, true, FALSE, false;
 -> 1, 1, 0, 0
```

## <span id="page-175-1"></span>**9.1.7 NULL Values**

The NULL value means "no data." NULL can be written in any lettercase. A synonym is \N (casesensitive). Treatment of \N as a synonym for NULL in SQL statements is deprecated as of MySQL 5.7.18 and is removed in MySQL 8.0; use NULL instead.

Be aware that the NULL value is different from values such as 0 for numeric types or the empty string for string types. For more information, see Section B.3.4.3, "Problems with NULL Values".

For text file import or export operations performed with LOAD DATA or SELECT ... INTO OUTFILE, NULL is represented by the \N sequence. See Section 13.2.6, "LOAD DATA Statement". Use of \N in text files is unaffected by the deprecation of \N in SQL statements.

For sorting with ORDER BY, NULL values sort before other values for ascending sorts, after other values for descending sorts.

# <span id="page-175-0"></span>**9.2 Schema Object Names**

Certain objects within MySQL, including database, table, index, column, alias, view, stored procedure, partition, tablespace, and other object names are known as identifiers. This section describes the permissible syntax for identifiers in MySQL. [Section 9.2.1, "Identifier Length Limits",](#page-176-0) indicates the maximum length of each type of identifier. [Section 9.2.3, "Identifier Case Sensitivity",](#page-179-0) describes which types of identifiers are case-sensitive and under what conditions.

An identifier may be quoted or unquoted. If an identifier contains special characters or is a reserved word, you must quote it whenever you refer to it. (Exception: A reserved word that follows a period in a qualified name must be an identifier, so it need not be quoted.) Reserved words are listed at [Section 9.3, "Keywords and Reserved Words".](#page-187-0)

Internally, identifiers are converted to and are stored as Unicode (UTF-8). The permissible Unicode characters in identifiers are those in the Basic Multilingual Plane (BMP). Supplementary characters are not permitted. Identifiers thus may contain these characters:

- Permitted characters in unquoted identifiers:
  - ASCII: [0-9,a-z,A-Z\$\_] (basic Latin letters, digits 0-9, dollar, underscore)
  - Extended: U+0080 .. U+FFFF
- Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP), except U+0000:
  - ASCII: U+0001 .. U+007F
  - Extended: U+0080 .. U+FFFF
- ASCII NUL (U+0000) and supplementary characters (U+10000 and higher) are not permitted in quoted or unquoted identifiers.
- Identifiers may begin with a digit but unless quoted may not consist solely of digits.
- Database, table, and column names cannot end with space characters.

The identifier quote character is the backtick (`):

```
mysql> SELECT * FROM `select` WHERE `select`.id > 100;
```

If the ANSI\_QUOTES SQL mode is enabled, it is also permissible to quote identifiers within double quotation marks:

```
mysql> CREATE TABLE "test" (col INT);
ERROR 1064: You have an error in your SQL syntax...
```

```
mysql> SET sql_mode='ANSI_QUOTES';
mysql> CREATE TABLE "test" (col INT);
Query OK, 0 rows affected (0.00 sec)
```

The ANSI\_QUOTES mode causes the server to interpret double-quoted strings as identifiers. Consequently, when this mode is enabled, string literals must be enclosed within single quotation marks. They cannot be enclosed within double quotation marks. The server SQL mode is controlled as described in Section 5.1.10, "Server SQL Modes".

Identifier quote characters can be included within an identifier if you quote the identifier. If the character to be included within the identifier is the same as that used to quote the identifier itself, then you need to double the character. The following statement creates a table named a`b that contains a column named c"d:

```
mysql> CREATE TABLE `a``b` (`c"d` INT);
```

In the select list of a query, a quoted column alias can be specified using identifier or string quoting characters:

```
mysql> SELECT 1 AS `one`, 2 AS 'two';
+-----+-----+
| one | two |
+-----+-----+
| 1 | 2 |
+-----+-----+
```

Elsewhere in the statement, quoted references to the alias must use identifier quoting or the reference is treated as a string literal.

It is recommended that you do not use names that begin with Me or MeN, where M and N are integers. For example, avoid using 1e as an identifier, because an expression such as 1e+3 is ambiguous. Depending on context, it might be interpreted as the expression 1e + 3 or as the number 1e+3.

Be careful when using MD5() to produce table names because it can produce names in illegal or ambiguous formats such as those just described.

A user variable cannot be used directly in an SQL statement as an identifier or as part of an identifier. See Section 9.4, "User-Defined Variables", for more information and examples of workarounds.

Special characters in database and table names are encoded in the corresponding file system names as described in [Section 9.2.4, "Mapping of Identifiers to File Names".](#page-181-0) If you have databases or tables from an older version of MySQL that contain special characters and for which the underlying directory names or file names have not been updated to use the new encoding, the server displays their names with a prefix of #mysql50#. For information about referring to such names or converting them to the newer encoding, see that section.

# <span id="page-176-0"></span>**9.2.1 Identifier Length Limits**

The following table describes the maximum length for each type of identifier.

| Identifier Type | Maximum Length (characters) |
|-----------------|-----------------------------|
| Database        | 64 (NDB storage engine: 63) |
| Table           | 64 (NDB storage engine: 63) |
| Column          | 64                          |
| Index           | 64                          |
| Constraint      | 64                          |
| Stored Program  | 64                          |
| View            | 64                          |
| Tablespace      | 64                          |

| Identifier Type          | Maximum Length (characters)         |
|--------------------------|-------------------------------------|
| Server                   | 64                                  |
| Log File Group           | 64                                  |
| Alias                    | 256 (see exception following table) |
| Compound Statement Label | 16                                  |
| User-Defined Variable    | 64                                  |

Aliases for column names in CREATE VIEW statements are checked against the maximum column length of 64 characters (not the maximum alias length of 256 characters).

For constraint definitions that include no constraint name, the server internally generates a name derived from the associated table name. For example, internally generated foreign key constraint names consist of the table name plus \_ibfk\_ and a number. If the table name is close to the length limit for constraint names, the additional characters required for the constraint name may cause that name to exceed the limit, resulting in an error.

Identifiers are stored using Unicode (UTF-8). This applies to identifiers in table definitions that are stored in .frm files and to identifiers stored in the grant tables in the mysql database. The sizes of the identifier string columns in the grant tables are measured in characters. You can use multibyte characters without reducing the number of characters permitted for values stored in these columns.

NDB Cluster imposes a maximum length of 63 characters for names of databases and tables. See Section 21.2.7.5, "Limits Associated with Database Objects in NDB Cluster".

Values such as user name and host names in MySQL account names are strings rather than identifiers. For information about the maximum length of such values as stored in grant tables, see Grant Table Scope Column Properties.

## <span id="page-177-0"></span>**9.2.2 Identifier Qualifiers**

Object names may be unqualified or qualified. An unqualified name is permitted in contexts where interpretation of the name is unambiguous. A qualified name includes at least one qualifier to clarify the interpretive context by overriding a default context or providing missing context.

For example, this statement creates a table using the unqualified name t1:

```
CREATE TABLE t1 (i INT);
```

Because t1 includes no qualifier to specify a database, the statement creates the table in the default database. If there is no default database, an error occurs.

This statement creates a table using the qualified name db1.t1:

```
CREATE TABLE db1.t1 (i INT);
```

Because db1.t1 includes a database qualifier db1, the statement creates t1 in the database named db1, regardless of the default database. The qualifier must be specified if there is no default database. The qualifier may be specified if there is a default database, to specify a database different from the default, or to make the database explicit if the default is the same as the one specified.

Qualifiers have these characteristics:

- An unqualified name consists of a single identifier. A qualified name consists of multiple identifiers.
- The components of a multiple-part name must be separated by period (.) characters. The initial parts of a multiple-part name act as qualifiers that affect the context within which to interpret the final identifier.
- The qualifier character is a separate token and need not be contiguous with the associated identifiers. For example, tbl\_name.col\_name and tbl\_name . col\_name are equivalent.

- If any components of a multiple-part name require quoting, quote them individually rather than quoting the name as a whole. For example, write `my-table`.`my-column`, not `mytable.my-column`.
- A reserved word that follows a period in a qualified name must be an identifier, so in that context it need not be quoted.
- The syntax .tbl\_name means the table tbl\_name in the default database.

![](_page_178_Picture_4.jpeg)

#### **Note**

This syntax is deprecated as of MySQL 5.7.20; expect it to be removed in a future version of MySQL.

The permitted qualifiers for object names depend on the object type:

• A database name is fully qualified and takes no qualifier:

```
CREATE DATABASE db1;
```

• A table, view, or stored program name may be given a database-name qualifier. Examples of unqualified and qualified names in CREATE statements:

```
CREATE TABLE mytable ...;
CREATE VIEW myview ...;
CREATE PROCEDURE myproc ...;
CREATE FUNCTION myfunc ...;
CREATE EVENT myevent ...;
CREATE TABLE mydb.mytable ...;
CREATE VIEW mydb.myview ...;
CREATE PROCEDURE mydb.myproc ...;
CREATE FUNCTION mydb.myfunc ...;
CREATE EVENT mydb.myevent ...;
```

• A trigger is associated with a table, so any qualifier applies to the table name:

```
CREATE TRIGGER mytrigger ... ON mytable ...;
CREATE TRIGGER mytrigger ... ON mydb.mytable ...;
```

• A column name may be given multiple qualifiers to indicate context in statements that reference it, as shown in the following table.

| Column Reference          | Meaning                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------|
| col_name                  | Column col_name from whichever table used in<br>the statement contains a column of that name |
| tbl_name.col_name         | Column col_name from table tbl_name of the<br>default database                               |
| db_name.tbl_name.col_name | Column col_name from table tbl_name of the<br>database db_name                               |

In other words, a column name may be given a table-name qualifier, which itself may be given a database-name qualifier. Examples of unqualified and qualified column references in SELECT statements:

```
SELECT c1 FROM mytable
WHERE c2 > 100;
SELECT mytable.c1 FROM mytable
WHERE mytable.c2 > 100;
SELECT mydb.mytable.c1 FROM mydb.mytable
```

```
WHERE mydb.mytable.c2 > 100;
```

You need not specify a qualifier for an object reference in a statement unless the unqualified reference is ambiguous. Suppose that column c1 occurs only in table t1, c2 only in t2, and c in both t1 and t2. Any unqualified reference to c is ambiguous in a statement that refers to both tables and must be qualified as t1.c or t2.c to indicate which table you mean:

```
SELECT c1, c2, t1.c FROM t1 INNER JOIN t2
WHERE t2.c > 100;
```

Similarly, to retrieve from a table t in database db1 and from a table t in database db2 in the same statement, you must qualify the table references: For references to columns in those tables, qualifiers are required only for column names that appear in both tables. Suppose that column c1 occurs only in table db1.t, c2 only in db2.t, and c in both db1.t and db2.t. In this case, c is ambiguous and must be qualified but c1 and c2 need not be:

```
SELECT c1, c2, db1.t.c FROM db1.t INNER JOIN db2.t
WHERE db2.t.c > 100;
```

Table aliases enable qualified column references to be written more simply:

```
SELECT c1, c2, t1.c FROM db1.t AS t1 INNER JOIN db2.t AS t2
WHERE t2.c > 100;
```

# <span id="page-179-0"></span>**9.2.3 Identifier Case Sensitivity**

In MySQL, databases correspond to directories within the data directory. Each table within a database corresponds to at least one file within the database directory (and possibly more, depending on the storage engine). Triggers also correspond to files. Consequently, the case sensitivity of the underlying operating system plays a part in the case sensitivity of database, table, and trigger names. This means such names are not case-sensitive in Windows, but are case-sensitive in most varieties of Unix. One notable exception is macOS, which is Unix-based but uses a default file system type (HFS+) that is not case-sensitive. However, macOS also supports UFS volumes, which are case-sensitive just as on any Unix. See Section 1.6.1, "MySQL Extensions to Standard SQL". The lower\_case\_table\_names system variable also affects how the server handles identifier case sensitivity, as described later in this section.

![](_page_179_Picture_10.jpeg)

### **Note**

Although database, table, and trigger names are not case-sensitive on some platforms, you should not refer to one of these using different cases within the same statement. The following statement would not work because it refers to a table both as my\_table and as MY\_TABLE:

```
mysql> SELECT * FROM my_table WHERE MY_TABLE.col=1;
```

Column, index, stored routine, and event names are not case-sensitive on any platform, nor are column aliases.

However, names of logfile groups are case-sensitive. This differs from standard SQL.

By default, table aliases are case-sensitive on Unix, but not so on Windows or macOS. The following statement would not work on Unix, because it refers to the alias both as a and as A:

```
mysql> SELECT col_name FROM tbl_name AS a
 WHERE a.col_name = 1 OR A.col_name = 2;
```

However, this same statement is permitted on Windows. To avoid problems caused by such differences, it is best to adopt a consistent convention, such as always creating and referring to databases and tables using lowercase names. This convention is recommended for maximum portability and ease of use.

How table and database names are stored on disk and used in MySQL is affected by the lower\_case\_table\_names system variable, which you can set when starting mysqld. lower\_case\_table\_names can take the values shown in the following table. This variable does not affect case sensitivity of trigger identifiers. On Unix, the default value of lower\_case\_table\_names is 0. On Windows, the default value is 1. On macOS, the default value is 2.

| Value | Meaning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0     | Table and database names are stored on disk<br>using the lettercase specified in the CREATE<br>TABLE or CREATE DATABASE statement. Name<br>comparisons are case-sensitive. You should not<br>set this variable to 0 if you are running MySQL<br>on a system that has case-insensitive file names<br>(such as Windows or macOS). If you force this<br>variable to 0 withlower-case-table<br>names=0 on a case-insensitive file system and<br>access MyISAM tablenames using different<br>lettercases, index corruption may result. |
| 1     | Table names are stored in lowercase on disk<br>and name comparisons are not case-sensitive.<br>MySQL converts all table names to lowercase on<br>storage and lookup. This behavior also applies to<br>database names and table aliases.                                                                                                                                                                                                                                                                                           |
| 2     | Table and database names are stored on disk<br>using the lettercase specified in the CREATE<br>TABLE or CREATE DATABASE statement, but<br>MySQL converts them to lowercase on lookup.<br>Name comparisons are not case-sensitive.<br>This works only on file systems that are not<br>case-sensitive! InnoDB table names and<br>view names are stored in lowercase, as for<br>lower_case_table_names=1.                                                                                                                            |

If you are using MySQL on only one platform, you do not normally have to change the lower\_case\_table\_names variable from its default value. However, you may encounter difficulties if you want to transfer tables between platforms that differ in file system case sensitivity. For example, on Unix, you can have two different tables named my\_table and MY\_TABLE, but on Windows these two names are considered identical. To avoid data transfer problems arising from lettercase of database or table names, you have two options:

- Use lower\_case\_table\_names=1 on all systems. The main disadvantage with this is that when you use SHOW TABLES or SHOW DATABASES, you do not see the names in their original lettercase.
- Use lower\_case\_table\_names=0 on Unix and lower\_case\_table\_names=2 on Windows. This preserves the lettercase of database and table names. The disadvantage of this is that you must ensure that your statements always refer to your database and table names with the correct lettercase on Windows. If you transfer your statements to Unix, where lettercase is significant, they do not work if the lettercase is incorrect.

**Exception**: If you are using InnoDB tables and you are trying to avoid these data transfer problems, you should set lower\_case\_table\_names to 1 on all platforms to force names to be converted to lowercase.

If you plan to set the lower\_case\_table\_names system variable to 1 on Unix, you must first convert your old database and table names to lowercase before stopping mysqld and restarting it with the new variable setting. To do this for an individual table, use RENAME TABLE:

```
RENAME TABLE T1 TO t1;
```

To convert one or more entire databases, dump them before setting lower\_case\_table\_names, then drop the databases, and reload them after setting lower\_case\_table\_names:

1. Use mysqldump to dump each database:

```
mysqldump --databases db1 > db1.sql
mysqldump --databases db2 > db2.sql
...
```

Do this for each database that must be recreated.

- 2. Use DROP DATABASE to drop each database.
- 3. Stop the server, set lower\_case\_table\_names, and restart the server.
- 4. Reload the dump file for each database. Because lower\_case\_table\_names is set, each database and table name is converted to lowercase as it is re-created:

```
mysql < db1.sql
mysql < db2.sql
...
```

Object names may be considered duplicates if their uppercase forms are equal according to a binary collation. That is true for names of cursors, conditions, procedures, functions, savepoints, stored routine parameters, stored program local variables, and plugins. It is not true for names of columns, constraints, databases, partitions, statements prepared with PREPARE, tables, triggers, users, and user-defined variables.

File system case sensitivity can affect searches in string columns of INFORMATION\_SCHEMA tables. For more information, see Section 10.8.7, "Using Collation in INFORMATION\_SCHEMA Searches".

# <span id="page-181-0"></span>**9.2.4 Mapping of Identifiers to File Names**

There is a correspondence between database and table identifiers and names in the file system. For the basic structure, MySQL represents each database as a directory in the data directory, and each table by one or more files in the appropriate database directory. For the table format files (.FRM), the data is always stored in this structure and location.

For the data and index files, the exact representation on disk is storage engine specific. These files may be stored in the same location as the FRM files, or the information may be stored in a separate file. InnoDB data is stored in the InnoDB data files. If you are using tablespaces with InnoDB, then the specific tablespace files you create are used instead.

Any character is legal in database or table identifiers except ASCII NUL (X'00'). MySQL encodes any characters that are problematic in the corresponding file system objects when it creates database directories or table files:

- Basic Latin letters (a..zA..Z), digits (0..9) and underscore (\_) are encoded as is. Consequently, their case sensitivity directly depends on file system features.
- All other national letters from alphabets that have uppercase/lowercase mapping are encoded as shown in the following table. Values in the Code Range column are UCS-2 values.

| Code Range | Pattern     | Number    | Used | Unused | Blocks                                         |
|------------|-------------|-----------|------|--------|------------------------------------------------|
| 00C0017F   | [@][04][gz] | 5*20= 100 | 97   | 3      | Latin-1<br>Supplement +<br>Latin Extended<br>A |
| 037003FF   | [@][59][gz] | 5*20= 100 | 88   | 12     | Greek and<br>Coptic                            |
| 0400052F   | [@][gz][06] | 20*7= 140 | 137  | 3      | Cyrillic<br>+ Cyrillic<br>Supplement           |

| Code Range | Pattern     | Number    | Used | Unused | Blocks                                  |
|------------|-------------|-----------|------|--------|-----------------------------------------|
| 0530058F   | [@][gz][78] | 20*2= 40  | 38   | 2      | Armenian                                |
| 2160217F   | [@][gz][9]  | 20*1= 20  | 16   | 4      | Number Forms                            |
| 018002AF   | [@][gz][ak] | 20*11=220 | 203  | 17     | Latin Extended<br>B + IPA<br>Extensions |
| 1E001EFF   | [@][gz][lr] | 20*7= 140 | 136  | 4      | Latin Extended<br>Additional            |
| 1F001FFF   | [@][gz][sz] | 20*8= 160 | 144  | 16     | Greek<br>Extended                       |
|            | [@][af][gz] | 6*20= 120 | 0    | 120    | RESERVED                                |
| 24B624E9   | [@][@][az]  | 26        | 26   | 0      | Enclosed<br>Alphanumerics               |
| FF21FF5A   | [@][az][@]  | 26        | 26   | 0      | Halfwidth and<br>Fullwidth forms        |

One of the bytes in the sequence encodes lettercase. For example: LATIN CAPITAL LETTER A WITH GRAVE is encoded as @0G, whereas LATIN SMALL LETTER A WITH GRAVE is encoded as @0g. Here the third byte (G or g) indicates lettercase. (On a case-insensitive file system, both letters are treated as the same.)

For some blocks, such as Cyrillic, the second byte determines lettercase. For other blocks, such as Latin1 Supplement, the third byte determines lettercase. If two bytes in the sequence are letters (as in Greek Extended), the leftmost letter character stands for lettercase. All other letter bytes must be in lowercase.

• All nonletter characters except underscore (\_), as well as letters from alphabets that do not have uppercase/lowercase mapping (such as Hebrew) are encoded using hexadecimal representation using lowercase letters for hexadecimal digits a..f:

```
0x003F -> @003f
0xFFFF -> @ffff
```

The hexadecimal values correspond to character values in the ucs2 double-byte character set.

On Windows, some names such as nul, prn, and aux are encoded by appending @@@ to the name when the server creates the corresponding file or directory. This occurs on all platforms for portability of the corresponding database object between platforms.

If you have databases or tables from a version of MySQL older than 5.1.6 that contain special characters and for which the underlying directory names or file names have not been updated to use the new encoding, the server displays their names with a prefix of #mysql50# in the output from INFORMATION\_SCHEMA tables or SHOW statements. For example, if you have a table named a@b and its name encoding has not been updated, SHOW TABLES displays it like this:

```
mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| #mysql50#a@b |
+----------------+
```

To refer to such a name for which the encoding has not been updated, you must supply the #mysql50# prefix:

```
mysql> SHOW COLUMNS FROM `a@b`;
ERROR 1146 (42S02): Table 'test.a@b' doesn't exist
mysql> SHOW COLUMNS FROM `#mysql50#a@b`;
```

|              | +++++++                    |  |                              |      |
|--------------|----------------------------|--|------------------------------|------|
| Field   Type |                            |  | Null   Key   Default   Extra |      |
| i            | +++++++<br>  int(11)   YES |  | NULL                         | <br> |
|              | +++++++                    |  |                              |      |

To update old names to eliminate the need to use the special prefix to refer to them, re-encode them with mysqlcheck. The following commands update all names to the new encoding:

```
mysqlcheck --check-upgrade --all-databases
mysqlcheck --fix-db-names --fix-table-names --all-databases
```

To check only specific databases or tables, omit --all-databases and provide the appropriate database or table arguments. For information about mysqlcheck invocation syntax, see Section 4.5.3, "mysqlcheck — A Table Maintenance Program".

![](_page_183_Picture_5.jpeg)

#### **Note**

The #mysql50# prefix is intended only to be used internally by the server. You should not create databases or tables with names that use this prefix.

Also, mysqlcheck cannot fix names that contain literal instances of the @ character that is used for encoding special characters. If you have databases or tables that contain this character, use mysqldump to dump them before upgrading to MySQL 5.1.6 or later, and then reload the dump file after upgrading.

![](_page_183_Picture_9.jpeg)

#### **Note**

Conversion of pre-MySQL 5.1 database names containing special characters to 5.1 format with the addition of a #mysql50# prefix is deprecated; expect it to be removed in a future version of MySQL. Because such conversions are deprecated, the --fix-db-names and --fix-table-names options for mysqlcheck and the UPGRADE DATA DIRECTORY NAME clause for the ALTER DATABASE statement are also deprecated.

Upgrades are supported only from one release series to another (for example, 5.0 to 5.1, or 5.1 to 5.5), so there should be little remaining need for conversion of older 5.0 database names to current versions of MySQL. As a workaround, upgrade a MySQL 5.0 installation to MySQL 5.1 before upgrading to a more recent release.

# <span id="page-183-0"></span>**9.2.5 Function Name Parsing and Resolution**

MySQL supports built-in (native) functions, loadable functions, and stored functions. This section describes how the server recognizes whether the name of a built-in function is used as a function call or as an identifier, and how the server determines which function to use in cases when functions of different types exist with a given name.

- [Built-In Function Name Parsing](#page-183-1)
- [Function Name Resolution](#page-186-0)

## <span id="page-183-1"></span>**Built-In Function Name Parsing**

The parser uses default rules for parsing names of built-in functions. These rules can be changed by enabling the IGNORE\_SPACE SQL mode.

When the parser encounters a word that is the name of a built-in function, it must determine whether the name signifies a function call or is instead a nonexpression reference to an identifier such as a table or column name. For example, in the following statements, the first reference to count is a function call, whereas the second reference is a table name:

```
SELECT COUNT(*) FROM mytable;
CREATE TABLE count (i INT);
```

The parser should recognize the name of a built-in function as indicating a function call only when parsing what is expected to be an expression. That is, in nonexpression context, function names are permitted as identifiers.

However, some built-in functions have special parsing or implementation considerations, so the parser uses the following rules by default to distinguish whether their names are being used as function calls or as identifiers in nonexpression context:

- To use the name as a function call in an expression, there must be no whitespace between the name and the following ( parenthesis character.
- Conversely, to use the function name as an identifier, it must not be followed immediately by a parenthesis.

The requirement that function calls be written with no whitespace between the name and the parenthesis applies only to the built-in functions that have special considerations. COUNT is one such name. The sql/lex.h source file lists the names of these special functions for which following whitespace determines their interpretation: names defined by the SYM\_FN() macro in the symbols[] array.

The following list names the functions in MySQL 5.7 that are affected by the IGNORE\_SPACE setting and listed as special in the sql/lex.h source file. You may find it easiest to treat the no-whitespace requirement as applying to all function calls.

- ADDDATE
- BIT\_AND
- BIT\_OR
- BIT\_XOR
- CAST
- COUNT
- CURDATE
- CURTIME
- DATE\_ADD
- DATE\_SUB
- EXTRACT
- GROUP\_CONCAT
- MAX
- MID
- MIN
- NOW
- POSITION
- SESSION\_USER
- STD

- STDDEV
- STDDEV\_POP
- STDDEV\_SAMP
- SUBDATE
- SUBSTR
- SUBSTRING
- SUM
- SYSDATE
- SYSTEM\_USER
- TRIM
- VARIANCE
- VAR\_POP
- VAR\_SAMP

For functions not listed as special in sql/lex.h, whitespace does not matter. They are interpreted as function calls only when used in expression context and may be used freely as identifiers otherwise. ASCII is one such name. However, for these nonaffected function names, interpretation may vary in expression context: func\_name () is interpreted as a built-in function if there is one with the given name; if not, func\_name () is interpreted as a loadable function or stored function if one exists with that name.

The IGNORE\_SPACE SQL mode can be used to modify how the parser treats function names that are whitespace-sensitive:

• With IGNORE\_SPACE disabled, the parser interprets the name as a function call when there is no whitespace between the name and the following parenthesis. This occurs even when the function name is used in nonexpression context:

```
mysql> CREATE TABLE count(i INT);
ERROR 1064 (42000): You have an error in your SQL syntax ...
near 'count(i INT)'
```

To eliminate the error and cause the name to be treated as an identifier, either use whitespace following the name or write it as a quoted identifier (or both):

```
CREATE TABLE count (i INT);
CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);
```

• With IGNORE\_SPACE enabled, the parser loosens the requirement that there be no whitespace between the function name and the following parenthesis. This provides more flexibility in writing function calls. For example, either of the following function calls are legal:

```
SELECT COUNT(*) FROM mytable;
SELECT COUNT (*) FROM mytable;
```

However, enabling IGNORE\_SPACE also has the side effect that the parser treats the affected function names as reserved words (see [Section 9.3, "Keywords and Reserved Words"](#page-187-0)). This means that a space following the name no longer signifies its use as an identifier. The name can be used in function calls with or without following whitespace, but causes a syntax error in nonexpression context unless it is quoted. For example, with IGNORE\_SPACE enabled, both of the following statements fail with a syntax error because the parser interprets count as a reserved word:

```
CREATE TABLE count(i INT);
CREATE TABLE count (i INT);
```

To use the function name in nonexpression context, write it as a quoted identifier:

```
CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);
```

To enable the IGNORE\_SPACE SQL mode, use this statement:

```
SET sql_mode = 'IGNORE_SPACE';
```

IGNORE\_SPACE is also enabled by certain other composite modes such as ANSI that include it in their value:

```
SET sql_mode = 'ANSI';
```

Check Section 5.1.10, "Server SQL Modes", to see which composite modes enable IGNORE\_SPACE.

To minimize the dependency of SQL code on the IGNORE\_SPACE setting, use these guidelines:

- Avoid creating loadable functions or stored functions that have the same name as a built-in function.
- Avoid using function names in nonexpression context. For example, these statements use count (one of the affected function names affected by IGNORE\_SPACE), so they fail with or without whitespace following the name if IGNORE\_SPACE is enabled:

```
CREATE TABLE count(i INT);
CREATE TABLE count (i INT);
```

If you must use a function name in nonexpression context, write it as a quoted identifier:

```
CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);
```

### <span id="page-186-0"></span>**Function Name Resolution**

The following rules describe how the server resolves references to function names for function creation and invocation:

• Built-in functions and loadable functions

An error occurs if you try to create a loadable function with the same name as a built-in function.

• Built-in functions and stored functions

It is possible to create a stored function with the same name as a built-in function, but to invoke the stored function it is necessary to qualify it with a schema name. For example, if you create a stored function named PI in the test schema, invoke it as test.PI() because the server resolves PI() without a qualifier as a reference to the built-in function. The server generates a warning if the stored function name collides with a built-in function name. The warning can be displayed with SHOW WARNINGS.

• Loadable functions and stored functions

Loadable functions and stored functions share the same namespace, so you cannot create a loadable function and a stored function with the same name.

The preceding function name resolution rules have implications for upgrading to versions of MySQL that implement new built-in functions:

• If you have already created a loadable function with a given name and upgrade MySQL to a version that implements a new built-in function with the same name, the loadable function becomes inaccessible. To correct this, use DROP FUNCTION to drop the loadable function and CREATE FUNCTION to re-create the loadable function with a different nonconflicting name. Then modify any affected code to use the new name.

• If a new version of MySQL implements a built-in function with the same name as an existing stored function, you have two choices: Rename the stored function to use a nonconflicting name, or change calls to the function so that they use a schema qualifier (that is, use schema\_name.func\_name() syntax). In either case, modify any affected code accordingly.

# <span id="page-187-0"></span>**9.3 Keywords and Reserved Words**

Keywords are words that have significance in SQL. Certain keywords, such as SELECT, DELETE, or BIGINT, are reserved and require special treatment for use as identifiers such as table and column names. This may also be true for the names of built-in functions.

Nonreserved keywords are permitted as identifiers without quoting. Reserved words are permitted as identifiers if you quote them as described in [Section 9.2, "Schema Object Names"](#page-175-0):

```
mysql> CREATE TABLE interval (begin INT, end INT);
ERROR 1064 (42000): You have an error in your SQL syntax ...
near 'interval (begin INT, end INT)'
```

BEGIN and END are keywords but not reserved, so their use as identifiers does not require quoting. INTERVAL is a reserved keyword and must be quoted to be used as an identifier:

```
mysql> CREATE TABLE `interval` (begin INT, end INT);
Query OK, 0 rows affected (0.01 sec)
```

Exception: A word that follows a period in a qualified name must be an identifier, so it need not be quoted even if it is reserved:

```
mysql> CREATE TABLE mydb.interval (begin INT, end INT);
Query OK, 0 rows affected (0.01 sec)
```

Names of built-in functions are permitted as identifiers but may require care to be used as such. For example, COUNT is acceptable as a column name. However, by default, no whitespace is permitted in function invocations between the function name and the following ( character. This requirement enables the parser to distinguish whether the name is used in a function call or in nonfunction context. For further details on recognition of function names, see [Section 9.2.5, "Function Name Parsing and](#page-183-0) [Resolution".](#page-183-0)

- [MySQL 5.7 Keywords and Reserved Words](#page-187-1)
- MySQL 5.7 New Keywords and Reserved Words
- MySQL 5.7 Removed Keywords and Reserved Words

# <span id="page-187-1"></span>**MySQL 5.7 Keywords and Reserved Words**

The following list shows the keywords and reserved words in MySQL 5.7, along with changes to individual words from version to version. Reserved keywords are marked with (R). In addition, \_FILENAME is reserved.

At some point, you might upgrade to a higher version, so it is a good idea to have a look at future reserved words, too. You can find these in the manuals that cover higher versions of MySQL. Most of the reserved words in the list are forbidden by standard SQL as column or table names (for example, GROUP). A few are reserved because MySQL needs them and uses a yacc parser.

[A](#page-187-2) | [B](#page-188-0) | [C](#page-189-0) | [D](#page-191-0) | [E](#page-192-0) | [F](#page-193-0) | [G](#page-193-1) | [H](#page-194-0) | [I](#page-194-1) | [J](#page-195-0) | [K](#page-195-1) | [L](#page-195-2) | [M](#page-196-0) | [N](#page-198-0) | [O](#page-199-0) | [P](#page-199-1) | Q | R | S | T | U | V | W | X | Y | Z

<span id="page-187-2"></span>A

- ACCESSIBLE (R)
- ACCOUNT; added in 5.7.6 (nonreserved)
- ACTION
- ADD (R)
- AFTER
- AGAINST
- AGGREGATE
- ALGORITHM
- ALL (R)
- ALTER (R)
- ALWAYS; added in 5.7.6 (nonreserved)
- ANALYSE
- ANALYZE (R)
- AND (R)
- ANY
- AS (R)
- ASC (R)
- ASCII
- ASENSITIVE (R)
- AT
- AUTOEXTEND\_SIZE
- AUTO\_INCREMENT
- AVG
- AVG\_ROW\_LENGTH

#### <span id="page-188-0"></span>B

- BACKUP
- BEFORE (R)
- BEGIN
- BETWEEN (R)
- BIGINT (R)
- BINARY (R)
- BINLOG
- BIT

- BLOB (R)
- BLOCK
- BOOL
- BOOLEAN
- BOTH (R)
- BTREE
- BY (R)
- BYTE

<span id="page-189-0"></span>C

- CACHE
- CALL (R)
- CASCADE (R)
- CASCADED
- CASE (R)
- CATALOG\_NAME
- CHAIN
- CHANGE (R)
- CHANGED
- CHANNEL; added in 5.7.6 (nonreserved)
- CHAR (R)
- CHARACTER (R)
- CHARSET
- CHECK (R)
- CHECKSUM
- CIPHER
- CLASS\_ORIGIN
- CLIENT
- CLOSE
- COALESCE
- CODE
- COLLATE (R)
- COLLATION
- COLUMN (R)

- COLUMNS
- COLUMN\_FORMAT
- COLUMN\_NAME
- COMMENT
- COMMIT
- COMMITTED
- COMPACT
- COMPLETION
- COMPRESSED
- COMPRESSION; added in 5.7.8 (nonreserved)
- CONCURRENT
- CONDITION (R)
- CONNECTION
- CONSISTENT
- CONSTRAINT (R)
- CONSTRAINT\_CATALOG
- CONSTRAINT\_NAME
- CONSTRAINT\_SCHEMA
- CONTAINS
- CONTEXT
- CONTINUE (R)
- CONVERT (R)
- CPU
- CREATE (R)
- CROSS (R)
- CUBE
- CURRENT
- CURRENT\_DATE (R)
- CURRENT\_TIME (R)
- CURRENT\_TIMESTAMP (R)
- CURRENT\_USER (R)
- CURSOR (R)
- CURSOR\_NAME

#### <span id="page-191-0"></span>D

- DATA
- DATABASE (R)
- DATABASES (R)
- DATAFILE
- DATE
- DATETIME
- DAY
- DAY\_HOUR (R)
- DAY\_MICROSECOND (R)
- DAY\_MINUTE (R)
- DAY\_SECOND (R)
- DEALLOCATE
- DEC (R)
- DECIMAL (R)
- DECLARE (R)
- DEFAULT (R)
- DEFAULT\_AUTH
- DEFINER
- DELAYED (R)
- DELAY\_KEY\_WRITE
- DELETE (R)
- DESC (R)
- DESCRIBE (R)
- DES\_KEY\_FILE
- DETERMINISTIC (R)
- DIAGNOSTICS
- DIRECTORY
- DISABLE
- DISCARD
- DISK
- DISTINCT (R)
- DISTINCTROW (R)

- DIV (R)
- DO
- DOUBLE (R)
- DROP (R)
- DUAL (R)
- DUMPFILE
- DUPLICATE
- DYNAMIC

<span id="page-192-0"></span>E

- EACH (R)
- ELSE (R)
- ELSEIF (R)
- ENABLE
- ENCLOSED (R)
- ENCRYPTION; added in 5.7.11 (nonreserved)
- END
- ENDS
- ENGINE
- ENGINES
- ENUM
- ERROR
- ERRORS
- ESCAPE
- ESCAPED (R)
- EVENT
- EVENTS
- EVERY
- EXCHANGE
- EXECUTE
- EXISTS (R)
- EXIT (R)
- EXPANSION
- EXPIRE

- EXPLAIN (R)
- EXPORT
- EXTENDED
- EXTENT\_SIZE

<span id="page-193-0"></span>F

- FALSE (R)
- FAST
- FAULTS
- FETCH (R)
- FIELDS
- FILE
- FILE\_BLOCK\_SIZE; added in 5.7.6 (nonreserved)
- FILTER; added in 5.7.3 (nonreserved)
- FIRST
- FIXED
- FLOAT (R)
- FLOAT4 (R)
- FLOAT8 (R)
- FLUSH
- FOLLOWS; added in 5.7.2 (nonreserved)
- FOR (R)
- FORCE (R)
- FOREIGN (R)
- FORMAT
- FOUND
- FROM (R)
- FULL
- FULLTEXT (R)
- FUNCTION

<span id="page-193-1"></span>G

- GENERAL
- GENERATED (R); added in 5.7.6 (reserved)
- GEOMETRY

<span id="page-194-0"></span>• GEOMETRYCOLLECTION • GET (R) • GET\_FORMAT • GLOBAL • GRANT (R) • GRANTS • GROUP (R) • GROUP\_REPLICATION; added in 5.7.6 (nonreserved) H • HANDLER • HASH • HAVING (R) • HELP • HIGH\_PRIORITY (R) • HOST • HOSTS • HOUR • HOUR\_MICROSECOND (R) • HOUR\_MINUTE (R) • HOUR\_SECOND (R) I • IDENTIFIED • IF (R) • IGNORE (R) • IGNORE\_SERVER\_IDS • IMPORT • IN (R) • INDEX (R) • INDEXES • INFILE (R) • INITIAL\_SIZE • INNER (R)

<span id="page-194-1"></span>• INOUT (R)

```
• INSENSITIVE (R)
• INSERT (R)
• INSERT_METHOD
• INSTALL
• INSTANCE; added in 5.7.11 (nonreserved)
• INT (R)
• INT1 (R)
• INT2 (R)
• INT3 (R)
• INT4 (R)
• INT8 (R)
• INTEGER (R)
• INTERVAL (R)
• INTO (R)
• INVOKER
• IO
• IO_AFTER_GTIDS (R)
• IO_BEFORE_GTIDS (R)
• IO_THREAD
• IPC
• IS (R)
• ISOLATION
• ISSUER
• ITERATE (R)
J
• JOIN (R)
• JSON; added in 5.7.8 (nonreserved)
K
• KEY (R)
• KEYS (R)
• KEY_BLOCK_SIZE
• KILL (R)
```

<span id="page-195-2"></span><span id="page-195-1"></span><span id="page-195-0"></span>L

- LANGUAGE
- LAST
- LEADING (R)
- LEAVE (R)
- LEAVES
- LEFT (R)
- LESS
- LEVEL
- LIKE (R)
- LIMIT (R)
- LINEAR (R)
- LINES (R)
- LINESTRING
- LIST
- LOAD (R)
- LOCAL
- LOCALTIME (R)
- LOCALTIMESTAMP (R)
- LOCK (R)
- LOCKS
- LOGFILE
- LOGS
- LONG (R)
- LONGBLOB (R)
- LONGTEXT (R)
- LOOP (R)
- LOW\_PRIORITY (R)

### <span id="page-196-0"></span>M

- MASTER
- MASTER\_AUTO\_POSITION
- MASTER\_BIND (R)
- MASTER\_CONNECT\_RETRY
- MASTER\_DELAY

- MASTER\_HEARTBEAT\_PERIOD
- MASTER\_HOST
- MASTER\_LOG\_FILE
- MASTER\_LOG\_POS
- MASTER\_PASSWORD
- MASTER\_PORT
- MASTER\_RETRY\_COUNT
- MASTER\_SERVER\_ID
- MASTER\_SSL
- MASTER\_SSL\_CA
- MASTER\_SSL\_CAPATH
- MASTER\_SSL\_CERT
- MASTER\_SSL\_CIPHER
- MASTER\_SSL\_CRL
- MASTER\_SSL\_CRLPATH
- MASTER\_SSL\_KEY
- MASTER\_SSL\_VERIFY\_SERVER\_CERT (R)
- MASTER\_TLS\_VERSION; added in 5.7.10 (nonreserved)
- MASTER\_USER
- MATCH (R)
- MAXVALUE (R)
- MAX\_CONNECTIONS\_PER\_HOUR
- MAX\_QUERIES\_PER\_HOUR
- MAX\_ROWS
- MAX\_SIZE
- MAX\_STATEMENT\_TIME; added in 5.7.4 (nonreserved); removed in 5.7.8
- MAX\_UPDATES\_PER\_HOUR
- MAX\_USER\_CONNECTIONS
- MEDIUM
- MEDIUMBLOB (R)
- MEDIUMINT (R)
- MEDIUMTEXT (R)
- MEMORY

- MERGE
- MESSAGE\_TEXT
- MICROSECOND
- MIDDLEINT (R)
- MIGRATE
- MINUTE
- MINUTE\_MICROSECOND (R)
- MINUTE\_SECOND (R)
- MIN\_ROWS
- MOD (R)
- MODE
- MODIFIES (R)
- MODIFY
- MONTH
- MULTILINESTRING
- MULTIPOINT
- MULTIPOLYGON
- MUTEX
- MYSQL\_ERRNO

#### <span id="page-198-0"></span>N

- NAME
- NAMES
- NATIONAL
- NATURAL (R)
- NCHAR
- NDB
- NDBCLUSTER
- NEVER; added in 5.7.4 (nonreserved)
- NEW
- NEXT
- NO
- NODEGROUP
- NONBLOCKING; removed in 5.7.6

- NONE
- NOT (R)
- NO\_WAIT
- NO\_WRITE\_TO\_BINLOG (R)
- NULL (R)
- NUMBER
- NUMERIC (R)
- NVARCHAR

#### <span id="page-199-0"></span>O

- OFFSET
- OLD\_PASSWORD; removed in 5.7.5
- ON (R)
- ONE
- ONLY
- OPEN
- OPTIMIZE (R)
- OPTIMIZER\_COSTS (R); added in 5.7.5 (reserved)
- OPTION (R)
- OPTIONALLY (R)
- OPTIONS
- OR (R)
- ORDER (R)
- OUT (R)
- OUTER (R)
- OUTFILE (R)
- OWNER

#### <span id="page-199-1"></span>P

- PACK\_KEYS
- PAGE
- PARSER
- PARSE\_GCOL\_EXPR; added in 5.7.6 (reserved); became nonreserved in 5.7.8
- PARTIAL
- PARTITION (R)

- PARTITIONING
- PARTITIONS
- PASSWORD
- PHASE
- PLUGIN
- PLUGINS
- PLUGIN\_DIR
- POINT
- POLYGON
- PORT
- PRECEDES; added in 5.7.2 (nonreserved)
- PRECISION (R)
- PREPARE
- PRESERVE
- PREV
- PRIMARY (R)
- PRIVILEGES
- PROCEDURE (R)
- PROCESSLIST
- PROFILE
- PROFILES
- PROXY
- PURGE (R)

### Q

- QUARTER
- QUERY
- QUICK

### R

- RANGE (R)
- READ (R)
- READS (R)
- READ\_ONLY
- READ\_WRITE (R)

- REAL (R)
- REBUILD
- RECOVER
- REDOFILE
- REDO\_BUFFER\_SIZE
- REDUNDANT
- REFERENCES (R)
- REGEXP (R)
- RELAY
- RELAYLOG
- RELAY\_LOG\_FILE
- RELAY\_LOG\_POS
- RELAY\_THREAD
- RELEASE (R)
- RELOAD
- REMOVE
- RENAME (R)
- REORGANIZE
- REPAIR
- REPEAT (R)
- REPEATABLE
- REPLACE (R)
- REPLICATE\_DO\_DB; added in 5.7.3 (nonreserved)
- REPLICATE\_DO\_TABLE; added in 5.7.3 (nonreserved)
- REPLICATE\_IGNORE\_DB; added in 5.7.3 (nonreserved)
- REPLICATE\_IGNORE\_TABLE; added in 5.7.3 (nonreserved)
- REPLICATE\_REWRITE\_DB; added in 5.7.3 (nonreserved)
- REPLICATE\_WILD\_DO\_TABLE; added in 5.7.3 (nonreserved)
- REPLICATE\_WILD\_IGNORE\_TABLE; added in 5.7.3 (nonreserved)
- REPLICATION
- REQUIRE (R)
- RESET
- RESIGNAL (R)

- RESTORE
- RESTRICT (R)
- RESUME
- RETURN (R)
- RETURNED\_SQLSTATE
- RETURNS
- REVERSE
- REVOKE (R)
- RIGHT (R)
- RLIKE (R)
- ROLLBACK
- ROLLUP
- ROTATE; added in 5.7.11 (nonreserved)
- ROUTINE
- ROW
- ROWS
- ROW\_COUNT
- ROW\_FORMAT
- RTREE

S

- SAVEPOINT
- SCHEDULE
- SCHEMA (R)
- SCHEMAS (R)
- SCHEMA\_NAME
- SECOND
- SECOND\_MICROSECOND (R)
- SECURITY
- SELECT (R)
- SENSITIVE (R)
- SEPARATOR (R)
- SERIAL
- SERIALIZABLE

- SERVER
- SESSION
- SET (R)
- SHARE
- SHOW (R)
- SHUTDOWN
- SIGNAL (R)
- SIGNED
- SIMPLE
- SLAVE
- SLOW
- SMALLINT (R)
- SNAPSHOT
- SOCKET
- SOME
- SONAME
- SOUNDS
- SOURCE
- SPATIAL (R)
- SPECIFIC (R)
- SQL (R)
- SQLEXCEPTION (R)
- SQLSTATE (R)
- SQLWARNING (R)
- SQL\_AFTER\_GTIDS
- SQL\_AFTER\_MTS\_GAPS
- SQL\_BEFORE\_GTIDS
- SQL\_BIG\_RESULT (R)
- SQL\_BUFFER\_RESULT
- SQL\_CACHE
- SQL\_CALC\_FOUND\_ROWS (R)
- SQL\_NO\_CACHE
- SQL\_SMALL\_RESULT (R)

- SQL\_THREAD
- SQL\_TSI\_DAY
- SQL\_TSI\_HOUR
- SQL\_TSI\_MINUTE
- SQL\_TSI\_MONTH
- SQL\_TSI\_QUARTER
- SQL\_TSI\_SECOND
- SQL\_TSI\_WEEK
- SQL\_TSI\_YEAR
- SSL (R)
- STACKED
- START
- STARTING (R)
- STARTS
- STATS\_AUTO\_RECALC
- STATS\_PERSISTENT
- STATS\_SAMPLE\_PAGES
- STATUS
- STOP
- STORAGE
- STORED (R); added in 5.7.6 (reserved)
- STRAIGHT\_JOIN (R)
- STRING
- SUBCLASS\_ORIGIN
- SUBJECT
- SUBPARTITION
- SUBPARTITIONS
- SUPER
- SUSPEND
- SWAPS
- SWITCHES

T

• TABLE (R)

- TABLES
- TABLESPACE
- TABLE\_CHECKSUM
- TABLE\_NAME
- TEMPORARY
- TEMPTABLE
- TERMINATED (R)
- TEXT
- THAN
- THEN (R)
- TIME
- TIMESTAMP
- TIMESTAMPADD
- TIMESTAMPDIFF
- TINYBLOB (R)
- TINYINT (R)
- TINYTEXT (R)
- TO (R)
- TRAILING (R)
- TRANSACTION
- TRIGGER (R)
- TRIGGERS
- TRUE (R)
- TRUNCATE
- TYPE
- TYPES

#### U

- UNCOMMITTED
- UNDEFINED
- UNDO (R)
- UNDOFILE
- UNDO\_BUFFER\_SIZE
- UNICODE

- UNINSTALL
- UNION (R)
- UNIQUE (R)
- UNKNOWN
- UNLOCK (R)
- UNSIGNED (R)
- UNTIL
- UPDATE (R)
- UPGRADE
- USAGE (R)
- USE (R)
- USER
- USER\_RESOURCES
- USE\_FRM
- USING (R)
- UTC\_DATE (R)
- UTC\_TIME (R)
- UTC\_TIMESTAMP (R)

### V

- VALIDATION; added in 5.7.5 (nonreserved)
- VALUE
- VALUES (R)
- VARBINARY (R)
- VARCHAR (R)
- VARCHARACTER (R)
- VARIABLES
- VARYING (R)
- VIEW
- VIRTUAL (R); added in 5.7.6 (reserved)

### W

- WAIT
- WARNINGS
- WEEK

• WEIGHT\_STRING • WHEN (R) • WHERE (R) • WHILE (R) • WITH (R) • WITHOUT; added in 5.7.5 (nonreserved) • WORK • WRAPPER • WRITE (R) X • X509 • XA • XID; added in 5.7.5 (nonreserved) • XML • XOR (R) Y • YEAR • YEAR\_MONTH (R)

# **MySQL 5.7 New Keywords and Reserved Words**

The following list shows the keywords and reserved words that are added in MySQL 5.7, compared to MySQL 5.6. Reserved keywords are marked with (R).

#### [A](#page-7-0) | [C](#page-7-1) | [E](#page-7-2) | [F](#page-7-3) | [G](#page-8-0) | [I](#page-8-1) | [J](#page-8-2) | [M](#page-8-3) | [N](#page-8-4) | [O](#page-8-5) | [P](#page-8-6) | [R](#page-8-7) | [S](#page-8-8) | [V](#page-8-9) | [W](#page-9-0) | [X](#page-9-1)

### <span id="page-7-0"></span>A

Z

• ACCOUNT

• ZEROFILL (R)

• ALWAYS

#### <span id="page-7-1"></span>C

- CHANNEL
- COMPRESSION

#### <span id="page-7-2"></span>E

• ENCRYPTION

<span id="page-7-3"></span>F

```
• FILE_BLOCK_SIZE
• FILTER
• FOLLOWS
G
• GENERATED (R)
• GROUP_REPLICATION
I
• INSTANCE
J
• JSON
M
• MASTER_TLS_VERSION
N
• NEVER
O
• OPTIMIZER_COSTS (R)
P
• PARSE_GCOL_EXPR
• PRECEDES
R
• REPLICATE_DO_DB
• REPLICATE_DO_TABLE
• REPLICATE_IGNORE_DB
• REPLICATE_IGNORE_TABLE
• REPLICATE_REWRITE_DB
• REPLICATE_WILD_DO_TABLE
• REPLICATE_WILD_IGNORE_TABLE
• ROTATE
S
• STACKED
• STORED (R)
V
```

- VALIDATION
- VIRTUAL (R)

<span id="page-9-0"></span>W

• WITHOUT

X

• XID

## <span id="page-9-1"></span>**MySQL 5.7 Removed Keywords and Reserved Words**

The following list shows the keywords and reserved words that are removed in MySQL 5.7, compared to MySQL 5.6. Reserved keywords are marked with (R).

• OLD\_PASSWORD

# <span id="page-9-2"></span>**9.4 User-Defined Variables**

You can store a value in a user-defined variable in one statement and refer to it later in another statement. This enables you to pass values from one statement to another.

User variables are written as @var\_name, where the variable name var\_name consists of alphanumeric characters, ., \_, and \$. A user variable name can contain other characters if you quote it as a string or identifier (for example, @'my-var', @"my-var", or @`my-var`).

User-defined variables are session specific. A user variable defined by one client cannot be seen or used by other clients. (Exception: A user with access to the Performance Schema user\_variables\_by\_thread table can see all user variables for all sessions.) All variables for a given client session are automatically freed when that client exits.

User variable names are not case-sensitive. Names have a maximum length of 64 characters.

One way to set a user-defined variable is by issuing a SET statement:

```
SET @var_name = expr [, @var_name = expr] ...
```

For SET, either = or := can be used as the assignment operator.

User variables can be assigned a value from a limited set of data types: integer, decimal, floating-point, binary or nonbinary string, or NULL value. Assignment of decimal and real values does not preserve the precision or scale of the value. A value of a type other than one of the permissible types is converted to a permissible type. For example, a value having a temporal or spatial data type is converted to a binary string. A value having the [JSON](#page-146-0) data type is converted to a string with a character set of utf8mb4 and a collation of utf8mb4\_bin.

If a user variable is assigned a nonbinary (character) string value, it has the same character set and collation as the string. The coercibility of user variables is implicit. (This is the same coercibility as for table column values.)

Hexadecimal or bit values assigned to user variables are treated as binary strings. To assign a hexadecimal or bit value as a number to a user variable, use it in numeric context. For example, add 0 or use CAST(... AS UNSIGNED):

```
mysql> SET @v1 = X'41';
mysql> SET @v2 = X'41'+0;
mysql> SET @v3 = CAST(X'41' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
```

```
+------+------+------+
| A | 65 | 65 |
+------+------+------+
mysql> SET @v1 = b'1000001';
mysql> SET @v2 = b'1000001'+0;
mysql> SET @v3 = CAST(b'1000001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
+------+------+------+
| A | 65 | 65 |
+------+------+------+
```

If the value of a user variable is selected in a result set, it is returned to the client as a string.

If you refer to a variable that has not been initialized, it has a value of NULL and a type of string.

User variables may be used in most contexts where expressions are permitted. This does not currently include contexts that explicitly require a literal value, such as in the LIMIT clause of a SELECT statement, or the IGNORE N LINES clause of a LOAD DATA statement.

It is also possible to assign a value to a user variable in statements other than SET. (This functionality is deprecated in MySQL 8.0 and subject to removal in a subsequent release.) When making an assignment in this way, the assignment operator must be := and not = because the latter is treated as the comparison operator [=](#page-194-0) in statements other than SET:

```
mysql> SET @t1=1, @t2=2, @t3:=4;
mysql> SELECT @t1, @t2, @t3, @t4 := @t1+@t2+@t3;
+------+------+------+--------------------+
| @t1 | @t2 | @t3 | @t4 := @t1+@t2+@t3 |
+------+------+------+--------------------+
| 1 | 2 | 4 | 7 |
+------+------+------+--------------------+
```

As a general rule, other than in SET statements, you should never assign a value to a user variable and read the value within the same statement. For example, to increment a variable, this is okay:

```
SET @a = @a + 1;
```

For other statements, such as SELECT, you might get the results you expect, but this is not guaranteed. In the following statement, you might think that MySQL evaluates @a first and then does an assignment second:

```
SELECT @a, @a:=@a+1, ...;
```

However, the order of evaluation for expressions involving user variables is undefined.

Another issue with assigning a value to a variable and reading the value within the same non-SET statement is that the default result type of a variable is based on its type at the start of the statement. The following example illustrates this:

```
mysql> SET @a='test';
mysql> SELECT @a,(@a:=20) FROM tbl_name;
```

For this SELECT statement, MySQL reports to the client that column one is a string and converts all accesses of @a to strings, even though @a is set to a number for the second row. After the SELECT statement executes, @a is regarded as a number for the next statement.

To avoid problems with this behavior, either do not assign a value to and read the value of the same variable within a single statement, or else set the variable to 0, 0.0, or '' to define its type before you use it.

In a SELECT statement, each select expression is evaluated only when sent to the client. This means that in a HAVING, GROUP BY, or ORDER BY clause, referring to a variable that is assigned a value in the select expression list does not work as expected:

```
mysql> SELECT (@aa:=id) AS a, (@aa+3) AS b FROM tbl_name HAVING b=5;
```

The reference to b in the HAVING clause refers to an alias for an expression in the select list that uses @aa. This does not work as expected: @aa contains the value of id from the previous selected row, not from the current row.

User variables are intended to provide data values. They cannot be used directly in an SQL statement as an identifier or as part of an identifier, such as in contexts where a table or database name is expected, or as a reserved word such as SELECT. This is true even if the variable is quoted, as shown in the following example:

```
mysql> SELECT c1 FROM t;
+----+
| c1 |
+----+
| 0 |
+----+
| 1 |
+----+
2 rows in set (0.00 sec)
mysql> SET @col = "c1";
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| c1 |
+------+
1 row in set (0.00 sec)
mysql> SELECT `@col` FROM t;
ERROR 1054 (42S22): Unknown column '@col' in 'field list'
mysql> SET @col = "`c1`";
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| `c1` |
+------+
1 row in set (0.00 sec)
```

An exception to this principle that user variables cannot be used to provide identifiers, is when you are constructing a string for use as a prepared statement to execute later. In this case, user variables can be used to provide any part of the statement. The following example illustrates how this can be done:

```
mysql> SET @c = "c1";
Query OK, 0 rows affected (0.00 sec)
mysql> SET @s = CONCAT("SELECT ", @c, " FROM t");
Query OK, 0 rows affected (0.00 sec)
mysql> PREPARE stmt FROM @s;
Query OK, 0 rows affected (0.04 sec)
Statement prepared
mysql> EXECUTE stmt;
+----+
| c1 |
+----+
| 0 |
+----+
| 1 |
+----+
2 rows in set (0.00 sec)
```

```
mysql> DEALLOCATE PREPARE stmt;
Query OK, 0 rows affected (0.00 sec)
```

See Section 13.5, "Prepared Statements", for more information.

A similar technique can be used in application programs to construct SQL statements using program variables, as shown here using PHP 5:

```
<?php
 $mysqli = new mysqli("localhost", "user", "pass", "test");
 if( mysqli_connect_errno() )
 die("Connection failed: %s\n", mysqli_connect_error());
 $col = "c1";
 $query = "SELECT $col FROM t";
 $result = $mysqli->query($query);
 while($row = $result->fetch_assoc())
 {
 echo "<p>" . $row["$col"] . "</p>\n";
 }
 $result->close();
 $mysqli->close();
?>
```

Assembling an SQL statement in this fashion is sometimes known as "Dynamic SQL".