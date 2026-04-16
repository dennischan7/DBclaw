---
source: MySQL 8.4 Reference
title: 00_Overview
---

See the files sql/opt\_trace\*, starting with sql/opt\_trace.h. A trace is started by creating an instance of Opt\_trace\_start; information is added to this trace by creating instances of Opt\_trace\_object and Opt\_trace\_array, and by using the add() methods of these classes.

# Chapter 11 Language Structure

# **Table of Contents**

| 11.1 Literal Values 1859                         |      |
|--------------------------------------------------|------|
| 11.1.1 String Literals 1859                      |      |
| 11.1.2 Numeric Literals 1862                     |      |
| 11.1.3 Date and Time Literals 1862               |      |
| 11.1.4 Hexadecimal Literals 1867                 |      |
| 11.1.5 Bit-Value Literals                        | 1869 |
| 11.1.6 Boolean Literals 1871                     |      |
| 11.1.7 NULL Values 1871                          |      |
| 11.2 Schema Object Names 1871                    |      |
| 11.2.1 Identifier Length Limits 1873             |      |
| 11.2.2 Identifier Qualifiers 1874                |      |
| 11.2.3 Identifier Case Sensitivity 1875          |      |
| 11.2.4 Mapping of Identifiers to File Names 1877 |      |
| 11.2.5 Function Name Parsing and Resolution 1879 |      |
| 11.3 Keywords and Reserved Words 1882            |      |
| 11.4 User-Defined Variables 1910                 |      |
| 11.5 Expressions 1913                            |      |
| 11.6 Query Attributes 1917                       |      |
| 11.7 Comments 1920                               |      |

This chapter discusses the rules for writing the following elements of SQL statements when using MySQL:

- Literal values such as strings and numbers
- Identifiers such as database, table, and column names
- Keywords and reserved words
- User-defined and system variables
- Expressions
- Query attributes
- Comments

# <span id="page-88-0"></span>**11.1 Literal Values**

This section describes how to write literal values in MySQL. These include strings, numbers, hexadecimal and bit values, boolean values, and NULL. The section also covers various nuances that you may encounter when dealing with these basic types in MySQL.

# <span id="page-88-1"></span>**11.1.1 String Literals**

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

For both types of strings, comparisons are based on the numeric values of the string unit. For binary strings, the unit is the byte; comparisons use numeric byte values. For nonbinary strings, the unit is the character and some character sets support multibyte characters; comparisons use numeric character code values. Character code ordering is a function of the string collation. (For more information, see [Section 12.8.5, "The binary Collation Compared to \\_bin Collations"](#page-181-0).)

![](_page_89_Picture_4.jpeg)

#### **Note**

Within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

A character string literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name]'string' [COLLATE collation_name]
```

#### Examples:

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_danish_ci;
```

You can use N'literal' (or n'literal') to create a string in the national character set. These statements are equivalent:

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

For information about these forms of string syntax, see [Section 12.3.7, "The National Character Set",](#page-166-0) and [Section 12.3.8, "Character Set Introducers"](#page-166-1).

Within a string, certain sequences have special meaning unless the NO\_BACKSLASH\_ESCAPES SQL mode is enabled. Each of these sequences begins with a backslash (\), known as the escape character. MySQL recognizes the escape sequences shown in [Table 11.1, "Special Character Escape](#page-89-0) [Sequences"](#page-89-0). For all other escape sequences, backslash is ignored. That is, the escaped character is interpreted as if it was not escaped. For example, \x is just x. These sequences are case-sensitive. For example, \b is interpreted as a backspace, but \B is interpreted as B. Escape processing is done according to the character set indicated by the character\_set\_connection system variable. This is true even for strings that are preceded by an introducer that indicates a different character set, as discussed in [Section 12.3.6, "Character String Literal Character Set and Collation"](#page-164-0).

**Table 11.1 Special Character Escape Sequences**

<span id="page-89-0"></span>

| Escape Sequence | Character Represented by Sequence                  |
|-----------------|----------------------------------------------------|
| \0              | An ASCII NUL (X'00') character                     |
| \'              | A single quote (') character                       |
| \"              | A double quote (") character                       |
| \b              | A backspace character                              |
| \n              | A newline (linefeed) character                     |
| \r              | A carriage return character                        |
| \t              | A tab character                                    |
| \Z              | ASCII 26 (Control+Z); see note following the table |

| Escape Sequence | Character Represented by Sequence           |
|-----------------|---------------------------------------------|
| \\              | A backslash (\) character                   |
| \%              | A % character; see note following the table |
| \_              | A _ character; see note following the table |

The ASCII 26 character can be encoded as \Z to enable you to work around the problem that ASCII 26 stands for END-OF-FILE on Windows. ASCII 26 within a file causes problems if you try to use mysql db\_name < file\_name.

The \% and \\_ sequences are used to search for literal instances of % and \_ in pattern-matching contexts where they would otherwise be interpreted as wildcard characters. See the description of the LIKE operator in Section 14.8.1, "String Comparison Functions and Operators". If you use \% or \\_ outside of pattern-matching contexts, they evaluate to the strings \% and \\_, not to % and \_.

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

To insert binary data into a string column (such as a BLOB column), you should represent certain characters by escape sequences. Backslash (\) and the quote character used to quote the string must be escaped. In certain client environments, it may also be necessary to escape NUL or Control +Z. The mysql client truncates quoted strings containing NUL characters if they are not escaped, and Control+Z may be taken for END-OF-FILE on Windows if not escaped. For the escape sequences that represent each of these characters, see [Table 11.1, "Special Character Escape Sequences".](#page-89-0)

When writing application programs, any string that might contain any of these special characters must be properly escaped before the string is used as a data value in an SQL statement that is sent to the MySQL server. You can do this in two ways:

• Process the string with a function that escapes the special characters. In a C program, you can use the [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-escape-string-quote.md) C API function to escape characters. See [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-escape-string-quote.md). Within SQL statements that construct other SQL statements, you can use the QUOTE() function. The Perl DBI interface provides a quote method to convert special characters to the proper escape sequences. See Section 31.9, "MySQL Perl API". Other language interfaces may provide a similar capability.

• As an alternative to explicitly escaping special characters, many MySQL APIs provide a placeholder capability that enables you to insert special markers into a statement string, and then bind data values to them when you issue the statement. In this case, the API takes care of escaping special characters in the values for you.

# <span id="page-91-0"></span>**11.1.2 Numeric Literals**

Number literals include exact-value (integer and DECIMAL) literals and approximate-value (floatingpoint) literals.

Integers are represented as a sequence of digits. Numbers may include . as a decimal separator. Numbers may be preceded by - or + to indicate a negative or positive value, respectively. Numbers represented in scientific notation with a mantissa and exponent are approximate-value numbers.

Exact-value numeric literals have an integer part or fractional part, or both. They may be signed. Examples: 1, .2, 3.4, -5, -6.78, +9.10.

Approximate-value numeric literals are represented in scientific notation with a mantissa and exponent. Either or both parts may be signed. Examples: 1.2E3, 1.2E-3, -1.2E3, -1.2E-3.

Two numbers that look similar may be treated differently. For example, 2.34 is an exact-value (fixedpoint) number, whereas 2.34E0 is an approximate-value (floating-point) number.

The DECIMAL data type is a fixed-point type and calculations are exact. In MySQL, the DECIMAL type has several synonyms: NUMERIC, DEC, FIXED. The integer types also are exact-value types. For more information about exact-value calculations, see Section 14.24, "Precision Math".

The FLOAT and DOUBLE data types are floating-point types and calculations are approximate. In MySQL, types that are synonymous with FLOAT or DOUBLE are DOUBLE PRECISION and REAL.

An integer may be used in floating-point context; it is interpreted as the equivalent floating-point number.

### <span id="page-91-1"></span>**11.1.3 Date and Time Literals**

- [Standard SQL and ODBC Date and Time Literals](#page-91-2)
- [String and Numeric Literals in Date and Time Context](#page-92-0)

Date and time values can be represented in several formats, such as quoted strings or as numbers, depending on the exact type of the value and other factors. For example, in contexts where MySQL expects a date, it interprets any of '2015-07-21', '20150721', and 20150721 as a date.

This section describes the acceptable formats for date and time literals. For more information about the temporal data types, such as the range of permitted values, see Section 13.2, "Date and Time Data Types".

#### <span id="page-91-2"></span>**Standard SQL and ODBC Date and Time Literals**

Standard SQL requires temporal literals to be specified using a type keyword and a string. The space between the keyword and string is optional.

```
DATE 'str'
TIME 'str'
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

### <span id="page-92-0"></span>**String and Numeric Literals in Date and Time Context**

MySQL recognizes DATE values in these formats:

• As a string in either 'YYYY-MM-DD' or 'YY-MM-DD' format. A "relaxed" syntax is permitted, but is deprecated: Any punctuation character may be used as the delimiter between date parts. For example, '2012-12-31', '2012/12/31', '2012^12^31', and '2012@12@31' are equivalent. Using any character other than the dash (-) as the delimiter raises a warning, as shown here:

```
mysql> SELECT DATE'2012@12@31';
+------------------+
| DATE'2012@12@31' |
+------------------+
| 2012-12-31 |
+------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4095
Message: Delimiter '@' in position 4 in datetime value '2012@12@31' at row 1 is
deprecated. Prefer the standard '-'. 
1 row in set (0.00 sec)
```

- As a string with no delimiters in either 'YYYYMMDD' or 'YYMMDD' format, provided that the string makes sense as a date. For example, '20070523' and '070523' are interpreted as '2007-05-23', but '071332' is illegal (it has nonsensical month and day parts) and becomes '0000-00-00'.
- As a number in either YYYYMMDD or YYMMDD format, provided that the number makes sense as a date. For example, 19830905 and 830905 are interpreted as '1983-09-05'.

MySQL recognizes DATETIME and TIMESTAMP values in these formats:

• As a string in either 'YYYY-MM-DD hh:mm:ss' or 'YY-MM-DD hh:mm:ss' format. MySQL also permits a "relaxed" syntax here, although this is deprecated: Any punctuation character may be used as the delimiter between date parts or time parts. For example, '2012-12-31 11:30:45', '2012^12^31 11+30+45', '2012/12/31 11\*30\*45', and '2012@12@31 11^30^45' are equivalent. Use of any characters as delimiters in such values, other than the dash (-) for the date part and the colon (:) for the time part, raises a warning, as shown here:

```
mysql> SELECT TIMESTAMP'2012^12^31 11*30*45';
+--------------------------------+
| TIMESTAMP'2012^12^31 11*30*45' |
+--------------------------------+
| 2012-12-31 11:30:45 |
+--------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4095
Message: Delimiter '^' in position 4 in datetime value '2012^12^31 11*30*45' at
```

```
row 1 is deprecated. Prefer the standard '-'. 
1 row in set (0.00 sec)
```

The only delimiter recognized between a date and time part and a fractional seconds part is the decimal point.

The date and time parts can be separated by T rather than a space. For example, '2012-12-31 11:30:45' '2012-12-31T11:30:45' are equivalent.

Previously, MySQL supported arbitrary numbers of leading and trailing whitespace characters in date and time values, as well as between the date and time parts of DATETIME and TIMESTAMP values. In MySQL 8.4, this behavior is deprecated, and the presence of excess whitespace characters triggers a warning, as shown here:

```
mysql> SELECT TIMESTAMP'2012-12-31 11-30-45';
+----------------------------------+
| TIMESTAMP'2012-12-31 11-30-45' |
+----------------------------------+
| 2012-12-31 11:30:45 |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4096
Message: Delimiter ' ' in position 11 in datetime value '2012-12-31 11-30-45'
at row 1 is superfluous and is deprecated. Please remove. 
1 row in set (0.00 sec)
```

A warning is also raised when whitespace characters other than the space character is used, like this:

```
mysql> SELECT TIMESTAMP'2021-06-06
 '> 11:15:25';
+--------------------------------+
| TIMESTAMP'2021-06-06
 11:15:25' |
+--------------------------------+
| 2021-06-06 11:15:25 |
+--------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4095
Message: Delimiter '\n' in position 10 in datetime value '2021-06-06
11:15:25' at row 1 is deprecated. Prefer the standard ' '.
1 row in set (0.00 sec)
```

Only one such warning is raised per temporal value, even though multiple issues may exist with delimiters, whitespace, or both, as shown in the following series of statements:

```
mysql> SELECT TIMESTAMP'2012!-12-31 11:30:45';
+----------------------------------+
| TIMESTAMP'2012!-12-31 11:30:45' |
+----------------------------------+
| 2012-12-31 11:30:45 |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4095
Message: Delimiter '!' in position 4 in datetime value '2012!-12-31 11:30:45'
at row 1 is deprecated. Prefer the standard '-'. 
1 row in set (0.00 sec)
```

```
mysql> SELECT TIMESTAMP'2012-12-31 11:30:45';
+---------------------------------+
| TIMESTAMP'2012-12-31 11:30:45' |
+---------------------------------+
| 2012-12-31 11:30:45 |
+---------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 4096
Message: Delimiter ' ' in position 11 in datetime value '2012-12-31 11:30:45'
at row 1 is superfluous and is deprecated. Please remove. 
1 row in set (0.00 sec)
mysql> SELECT TIMESTAMP'2012-12-31 11:30:45';
+--------------------------------+
| TIMESTAMP'2012-12-31 11:30:45' |
+--------------------------------+
| 2012-12-31 11:30:45 |
+--------------------------------+
1 row in set (0.00 sec)
```

- As a string with no delimiters in either 'YYYYMMDDhhmmss' or 'YYMMDDhhmmss' format, provided that the string makes sense as a date. For example, '20070523091528' and '070523091528' are interpreted as '2007-05-23 09:15:28', but '071122129015' is illegal (it has a nonsensical minute part) and becomes '0000-00-00 00:00:00'.
- As a number in either YYYYMMDDhhmmss or YYMMDDhhmmss format, provided that the number makes sense as a date. For example, 19830905132800 and 830905132800 are interpreted as '1983-09-05 13:28:00'.

A DATETIME or TIMESTAMP value can include a trailing fractional seconds part in up to microseconds (6 digits) precision. The fractional part should always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is recognized. For information about fractional seconds support in MySQL, see Section 13.2.6, "Fractional Seconds in Time Values".

Dates containing two-digit year values are ambiguous because the century is unknown. MySQL interprets two-digit year values using these rules:

- Year values in the range 70-99 become 1970-1999.
- Year values in the range 00-69 become 2000-2069.

See also Section 13.2.9, "2-Digit Years in Dates".

For values specified as strings that include date part delimiters, it is unnecessary to specify two digits for month or day values that are less than 10. '2015-6-9' is the same as '2015-06-09'. Similarly, for values specified as strings that include time part delimiters, it is unnecessary to specify two digits for hour, minute, or second values that are less than 10. '2015-10-30 1:2:3' is the same as '2015-10-30 01:02:03'.

Values specified as numbers should be 6, 8, 12, or 14 digits long. If a number is 8 or 14 digits long, it is assumed to be in YYYYMMDD or YYYYMMDDhhmmss format and that the year is given by the first 4 digits. If the number is 6 or 12 digits long, it is assumed to be in YYMMDD or YYMMDDhhmmss format and that the year is given by the first 2 digits. Numbers that are not one of these lengths are interpreted as though padded with leading zeros to the closest length.

Values specified as nondelimited strings are interpreted according their length. For a string 8 or 14 characters long, the year is assumed to be given by the first 4 characters. Otherwise, the year is assumed to be given by the first 2 characters. The string is interpreted from left to right to find year, month, day, hour, minute, and second values, for as many parts as are present in the string. This means you should not use strings that have fewer than 6 characters. For example, if you specify

'9903', thinking that represents March, 1999, MySQL converts it to the "zero" date value. This occurs because the year and month values are 99 and 03, but the day part is completely missing. However, you can explicitly specify a value of zero to represent missing month or day parts. For example, to insert the value '1999-03-00', use '990300'.

MySQL recognizes TIME values in these formats:

- As a string in 'D hh:mm:ss' format. You can also use one of the following "relaxed" syntaxes: 'hh:mm:ss', 'hh:mm', 'D hh:mm', 'D hh', or 'ss'. Here D represents days and can have a value from 0 to 34.
- As a string with no delimiters in 'hhmmss' format, provided that it makes sense as a time. For example, '101112' is understood as '10:11:12', but '109712' is illegal (it has a nonsensical minute part) and becomes '00:00:00'.
- As a number in hhmmss format, provided that it makes sense as a time. For example, 101112 is understood as '10:11:12'. The following alternative formats are also understood: ss, mmss, or hhmmss.

A trailing fractional seconds part is recognized in the 'D hh:mm:ss.fraction', 'hh:mm:ss.fraction', 'hhmmss.fraction', and hhmmss.fraction time formats, where fraction is the fractional part in up to microseconds (6 digits) precision. The fractional part should always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is recognized. For information about fractional seconds support in MySQL, see Section 13.2.6, "Fractional Seconds in Time Values".

For TIME values specified as strings that include a time part delimiter, it is unnecessary to specify two digits for hours, minutes, or seconds values that are less than 10. '8:3:2' is the same as '08:03:02'.

You can specify a time zone offset when inserting TIMESTAMP and DATETIME values into a table. The offset is appended to the time part of a datetime literal, with no intravening spaces, and uses the same format used for setting the time\_zone system variable, with the following exceptions:

- For hour values less than 10, a leading zero is required.
- The value '-00:00' is rejected.
- Time zone names such as 'EET' and 'Asia/Shanghai' cannot be used; 'SYSTEM' also cannot be used in this context.

The value inserted must not have a zero for the month part, the day part, or both parts. This is enforced regardless of the server SQL mode setting.

This example illustrates inserting datetime values with time zone offsets into TIMESTAMP and DATETIME columns using different time\_zone settings, and then retrieving them:

```
mysql> CREATE TABLE ts (
 -> id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> col TIMESTAMP NOT NULL
 -> ) AUTO_INCREMENT = 1;
mysql> CREATE TABLE dt (
 -> id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> col DATETIME NOT NULL
 -> ) AUTO_INCREMENT = 1;
mysql> SET @@time_zone = 'SYSTEM';
mysql> INSERT INTO ts (col) VALUES ('2020-01-01 10:10:10'),
 -> ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');
mysql> SET @@time_zone = '+00:00';
mysql> INSERT INTO ts (col) VALUES ('2020-01-01 10:10:10'),
```

```
 -> ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');
mysql> SET @@time_zone = 'SYSTEM';
mysql> INSERT INTO dt (col) VALUES ('2020-01-01 10:10:10'),
 -> ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');
mysql> SET @@time_zone = '+00:00';
mysql> INSERT INTO dt (col) VALUES ('2020-01-01 10:10:10'),
 -> ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');
mysql> SET @@time_zone = 'SYSTEM';
mysql> SELECT @@system_time_zone;
+--------------------+
| @@system_time_zone |
+--------------------+
| EST |
+--------------------+
mysql> SELECT col, UNIX_TIMESTAMP(col) FROM dt ORDER BY id;
+---------------------+---------------------+
| col | UNIX_TIMESTAMP(col) |
+---------------------+---------------------+
| 2020-01-01 10:10:10 | 1577891410 |
| 2019-12-31 23:40:10 | 1577853610 |
| 2020-01-01 13:10:10 | 1577902210 |
| 2020-01-01 10:10:10 | 1577891410 |
| 2020-01-01 04:40:10 | 1577871610 |
| 2020-01-01 18:10:10 | 1577920210 |
+---------------------+---------------------+
mysql> SELECT col, UNIX_TIMESTAMP(col) FROM ts ORDER BY id;
+---------------------+---------------------+
| col | UNIX_TIMESTAMP(col) |
+---------------------+---------------------+
| 2020-01-01 10:10:10 | 1577891410 |
| 2019-12-31 23:40:10 | 1577853610 |
| 2020-01-01 13:10:10 | 1577902210 |
| 2020-01-01 05:10:10 | 1577873410 |
| 2019-12-31 23:40:10 | 1577853610 |
| 2020-01-01 13:10:10 | 1577902210 |
+---------------------+---------------------+
```

The offset is not displayed when selecting a datetime value, even if one was used when inserting it.

The range of supported offset values is -13:59 to +14:00, inclusive.

Datetime literals that include time zone offsets are accepted as parameter values by prepared statements.

# <span id="page-96-0"></span>**11.1.4 Hexadecimal Literals**

Hexadecimal literal values are written using X'val' or 0xval notation, where val contains hexadecimal digits (0..9, A..F). Lettercase of the digits and of any leading X does not matter. A leading 0x is case-sensitive and cannot be written as 0X.

Legal hexadecimal literals:

```
X'01AF'
X'01af'
x'01AF'
x'01af'
0x01AF
0x01af
```

#### Illegal hexadecimal literals:

```
X'0G' (G is not a hexadecimal digit)
```

```
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
SELECT _utf8mb4 0x4D7953514C COLLATE utf8mb4_danish_ci;
```

The examples use X'val' notation, but 0xval notation permits introducers as well. For information about introducers, see [Section 12.3.8, "Character Set Introducers"](#page-166-1).

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
```

```
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

For hexadecimal literals, bit operations are considered numeric context, but bit operations permit numeric or binary string arguments in MySQL 8.4 and higher. To explicitly specify binary string context for hexadecimal literals, use a \_binary introducer for at least one of the arguments:

```
mysql> SET @v1 = X'000D' | X'0BC0';
mysql> SET @v2 = _binary X'000D' | X'0BC0';
mysql> SELECT HEX(@v1), HEX(@v2);
+----------+----------+
| HEX(@v1) | HEX(@v2) |
+----------+----------+
| BCD | 0BCD |
+----------+----------+
```

The displayed result appears similar for both bit operations, but the result without \_binary is a BIGINT value, whereas the result with \_binary is a binary string. Due to the difference in result types, the displayed values differ: High-order 0 digits are not displayed for the numeric result.

### <span id="page-98-0"></span>**11.1.5 Bit-Value Literals**

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
```

```
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
SELECT _utf8mb4 0b1000001 COLLATE utf8mb4_danish_ci;
```

The examples use b'val' notation, but 0bval notation permits introducers as well. For information about introducers, see [Section 12.3.8, "Character Set Introducers"](#page-166-1).

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
```

```
| 10 | 1010 | 12 | A |
| 5 | 101 | 5 | 5 |
+------+----------+--------+--------+
```

For bit literals, bit operations are considered numeric context, but bit operations permit numeric or binary string arguments in MySQL 8.4 and higher. To explicitly specify binary string context for bit literals, use a \_binary introducer for at least one of the arguments:

```
mysql> SET @v1 = b'000010101' | b'000101010';
mysql> SET @v2 = _binary b'000010101' | _binary b'000101010';
mysql> SELECT HEX(@v1), HEX(@v2);
+----------+----------+
| HEX(@v1) | HEX(@v2) |
+----------+----------+
| 3F | 003F |
+----------+----------+
```

The displayed result appears similar for both bit operations, but the result without \_binary is a BIGINT value, whereas the result with \_binary is a binary string. Due to the difference in result types, the displayed values differ: High-order 0 digits are not displayed for the numeric result.

# <span id="page-100-1"></span>**11.1.6 Boolean Literals**

The constants TRUE and FALSE evaluate to 1 and 0, respectively. The constant names can be written in any lettercase.

```
mysql> SELECT TRUE, true, FALSE, false;
 -> 1, 1, 0, 0
```

# <span id="page-100-2"></span>**11.1.7 NULL Values**

The NULL value means "no data." NULL can be written in any lettercase.

Be aware that the NULL value is different from values such as 0 for numeric types or the empty string for string types. For more information, see Section B.3.4.3, "Problems with NULL Values".

For text file import or export operations performed with LOAD DATA or SELECT ... INTO OUTFILE, NULL is represented by the \N sequence. See Section 15.2.9, "LOAD DATA Statement".

For sorting with ORDER BY, NULL values sort before other values for ascending sorts, after other values for descending sorts.

# <span id="page-100-0"></span>**11.2 Schema Object Names**

Certain objects within MySQL, including database, table, index, column, alias, view, stored procedure, partition, tablespace, resource group and other object names are known as identifiers. This section describes the permissible syntax for identifiers in MySQL. [Section 11.2.1, "Identifier Length Limits",](#page-102-0) indicates the maximum length of each type of identifier. [Section 11.2.3, "Identifier Case Sensitivity"](#page-104-0), describes which types of identifiers are case-sensitive and under what conditions.

An identifier may be quoted or unquoted. If an identifier contains special characters or is a reserved word, you must quote it whenever you refer to it. (Exception: A reserved word that follows a period in a qualified name must be an identifier, so it need not be quoted.) Reserved words are listed at [Section 11.3, "Keywords and Reserved Words"](#page-111-0).

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
- Use of the dollar sign as the first character in the unquoted name of a database, table, view, column, stored program, or alias is deprecated, including such names used with qualifiers (see [Section 11.2.2, "Identifier Qualifiers"\)](#page-103-0). An unquoted identifier beginning with a dollar sign cannot contain any additional dollar sign characters. Otherwise, the leading dollar sign is permitted but triggers a deprecation warning.

The dollar sign can still be used as the leading character of such an identifier without producing the warning, when it is quoted according to the rules given later in this section.

The identifier quote character is the backtick (`):

```
mysql> SELECT * FROM `select` WHERE `select`.id > 100;
```

If the ANSI\_QUOTES SQL mode is enabled, it is also permissible to quote identifiers within double quotation marks:

```
mysql> CREATE TABLE "test" (col INT);
ERROR 1064: You have an error in your SQL syntax...
mysql> SET sql_mode='ANSI_QUOTES';
mysql> CREATE TABLE "test" (col INT);
Query OK, 0 rows affected (0.00 sec)
```

The ANSI\_QUOTES mode causes the server to interpret double-quoted strings as identifiers. Consequently, when this mode is enabled, string literals must be enclosed within single quotation marks. They cannot be enclosed within double quotation marks. The server SQL mode is controlled as described in Section 7.1.11, "Server SQL Modes".

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

It is also recommended that you do not use column names that begin with !hidden! to ensure that new names do not collide with names used by existing hidden columns for functional indexes.

A user variable cannot be used directly in an SQL statement as an identifier or as part of an identifier. See [Section 11.4, "User-Defined Variables",](#page-139-0) for more information and examples of workarounds.

Special characters in database and table names are encoded in the corresponding file system names as described in [Section 11.2.4, "Mapping of Identifiers to File Names"](#page-106-0).

# <span id="page-102-0"></span>**11.2.1 Identifier Length Limits**

The following table describes the maximum length for each type of identifier.

| Identifier Type          | Maximum Length (characters)         |
|--------------------------|-------------------------------------|
| Database                 | 64                                  |
| Table                    | 64                                  |
| Column                   | 64                                  |
| Index                    | 64                                  |
| Constraint               | 64                                  |
| Stored Program           | 64                                  |
| View                     | 64                                  |
| Tablespace               | 64                                  |
| Server                   | 64                                  |
| Log File Group           | 64                                  |
| Alias                    | 256 (see exception following table) |
| Compound Statement Label | 16                                  |
| User-Defined Variable    | 64                                  |
| Resource Group           | 64                                  |

Aliases for column names in CREATE VIEW statements are checked against the maximum column length of 64 characters (not the maximum alias length of 256 characters).

For constraint definitions that include no constraint name, the server internally generates a name derived from the associated table name. For example, internally generated foreign key and CHECK constraint names consist of the table name plus \_ibfk\_ or \_chk\_ and a number. If the table name is close to the length limit for constraint names, the additional characters required for the constraint name may cause that name to exceed the limit, resulting in an error.

Identifiers are stored using Unicode (UTF-8). This applies to identifiers in table definitions and to identifiers stored in the grant tables in the mysql database. The sizes of the identifier string columns in the grant tables are measured in characters. You can use multibyte characters without reducing the number of characters permitted for values stored in these columns.

Values such as user name and host names in MySQL account names are strings rather than identifiers. For information about the maximum length of such values as stored in grant tables, see Grant Table Scope Column Properties.

# <span id="page-103-0"></span>**11.2.2 Identifier Qualifiers**

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
```

```
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

# <span id="page-104-0"></span>**11.2.3 Identifier Case Sensitivity**

In MySQL, databases correspond to directories within the data directory. Each table within a database corresponds to at least one file within the database directory (and possibly more, depending on the storage engine). Triggers also correspond to files. Consequently, the case sensitivity of the underlying operating system plays a part in the case sensitivity of database, table, and trigger names. This means such names are not case-sensitive in Windows, but are case-sensitive in most varieties of Unix. One notable exception is macOS, which is Unix-based but uses a default file system type (HFS+) that is not case-sensitive. However, macOS also supports UFS volumes, which are case-sensitive just as on any Unix. See Section 1.7.1, "MySQL Extensions to Standard SQL". The lower\_case\_table\_names system variable also affects how the server handles identifier case sensitivity, as described later in this section.

![](_page_105_Picture_1.jpeg)

#### **Note**

Although database, table, and trigger names are not case-sensitive on some platforms, you should not refer to one of these using different cases within the same statement. The following statement would not work because it refers to a table both as my\_table and as MY\_TABLE:

```
mysql> SELECT * FROM my_table WHERE MY_TABLE.col=1;
```

Partition, subpartition, column, index, stored routine, event, and resource group names are not casesensitive on any platform, nor are column aliases.

However, names of logfile groups are case-sensitive. This differs from standard SQL.

By default, table aliases are case-sensitive on Unix, but not so on Windows or macOS. The following statement would not work on Unix, because it refers to the alias both as a and as A:

```
mysql> SELECT col_name FROM tbl_name AS a
 WHERE a.col_name = 1 OR A.col_name = 2;
```

However, this same statement is permitted on Windows. To avoid problems caused by such differences, it is best to adopt a consistent convention, such as always creating and referring to databases and tables using lowercase names. This convention is recommended for maximum portability and ease of use.

How table and database names are stored on disk and used in MySQL is affected by the lower\_case\_table\_names system variable. lower\_case\_table\_names can take the values shown in the following table. This variable does not affect case sensitivity of trigger identifiers. On Unix, the default value of lower\_case\_table\_names is 0. On Windows, the default value is 1. On macOS, the default value is 2.

lower\_case\_table\_names can only be configured when initializing the server. Changing the lower\_case\_table\_names setting after the server is initialized is prohibited.

| Value | Meaning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0     | Table and database names are stored on disk<br>using the lettercase specified in the CREATE<br>TABLE or CREATE DATABASE statement. Name<br>comparisons are case-sensitive. You should not<br>set this variable to 0 if you are running MySQL<br>on a system that has case-insensitive file names<br>(such as Windows or macOS). If you force this<br>variable to 0 withlower-case-table<br>names=0 on a case-insensitive file system and<br>access MyISAM tablenames using different<br>lettercases, index corruption may result. |
| 1     | Table names are stored in lowercase on disk<br>and name comparisons are not case-sensitive.<br>MySQL converts all table names to lowercase on<br>storage and lookup. This behavior also applies to<br>database names and table aliases.                                                                                                                                                                                                                                                                                           |
| 2     | Table and database names are stored on disk<br>using the lettercase specified in the CREATE<br>TABLE or CREATE DATABASE statement, but<br>MySQL converts them to lowercase on lookup.<br>Name comparisons are not case-sensitive.<br>This works only on file systems that are not<br>case-sensitive! InnoDB table names and<br>view names are stored in lowercase, as for<br>lower_case_table_names=1.                                                                                                                            |

If you are using MySQL on only one platform, you do not normally have to use a lower\_case\_table\_names setting other than the default. However, you may encounter difficulties if you want to transfer tables between platforms that differ in file system case sensitivity. For example, on Unix, you can have two different tables named my\_table and MY\_TABLE, but on Windows these two names are considered identical. To avoid data transfer problems arising from lettercase of database or table names, you have two options:

- Use lower\_case\_table\_names=1 on all systems. The main disadvantage with this is that when you use SHOW TABLES or SHOW DATABASES, you do not see the names in their original lettercase.
- Use lower\_case\_table\_names=0 on Unix and lower\_case\_table\_names=2 on Windows. This preserves the lettercase of database and table names. The disadvantage of this is that you must ensure that your statements always refer to your database and table names with the correct lettercase on Windows. If you transfer your statements to Unix, where lettercase is significant, they do not work if the lettercase is incorrect.

**Exception**: If you are using InnoDB tables and you are trying to avoid these data transfer problems, you should use lower\_case\_table\_names=1 on all platforms to force names to be converted to lowercase.

Object names may be considered duplicates if their uppercase forms are equal according to a binary collation. That is true for names of cursors, conditions, procedures, functions, savepoints, stored routine parameters, stored program local variables, and plugins. It is not true for names of columns, constraints, databases, partitions, statements prepared with PREPARE, tables, triggers, users, and user-defined variables.

File system case sensitivity can affect searches in string columns of INFORMATION\_SCHEMA tables. For more information, see [Section 12.8.7, "Using Collation in INFORMATION\\_SCHEMA Searches"](#page-184-0).

# <span id="page-106-0"></span>**11.2.4 Mapping of Identifiers to File Names**

There is a correspondence between database and table identifiers and names in the file system. For the basic structure, MySQL represents each database as a directory in the data directory, and depending upon the storage engine, each table may be represented by one or more files in the appropriate database directory.

For the data and index files, the exact representation on disk is storage engine specific. These files may be stored in the database directory, or the information may be stored in a separate file. InnoDB data is stored in the InnoDB data files. If you are using tablespaces with InnoDB, then the specific tablespace files you create are used instead.

Any character is legal in database or table identifiers except ASCII NUL (X'00'). MySQL encodes any characters that are problematic in the corresponding file system objects when it creates database directories or table files:

- Basic Latin letters (a..zA..Z), digits (0..9) and underscore (\_) are encoded as is. Consequently, their case sensitivity directly depends on file system features.
- All other national letters from alphabets that have uppercase/lowercase mapping are encoded as shown in the following table. Values in the Code Range column are UCS-2 values.

| Code Range | Pattern     | Number    | Used | Unused | Blocks                                         |
|------------|-------------|-----------|------|--------|------------------------------------------------|
| 00C0017F   | [@][04][gz] | 5*20= 100 | 97   | 3      | Latin-1<br>Supplement +<br>Latin Extended<br>A |
| 037003FF   | [@][59][gz] | 5*20= 100 | 88   | 12     | Greek and<br>Coptic                            |

| Code Range | Pattern     | Number    | Used | Unused | Blocks                                  |
|------------|-------------|-----------|------|--------|-----------------------------------------|
| 0400052F   | [@][gz][06] | 20*7= 140 | 137  | 3      | Cyrillic<br>+ Cyrillic<br>Supplement    |
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

The following names are reserved and appended with @@@ if used in schema or table names:

- CON
- PRN
- AUX
- NUL
- COM1 through COM9
- LPT1 through LPT9

CLOCK\$ is also a member of this group of reserved names, but is not appended with @@@, but @0024 instead. That is, if CLOCK\$ is used as a schema or table name, it is written to the file system as

CLOCK@0024. The same is true for any use of \$ (dollar sign) in a schema or table name; it is replaced with @0024 on the filesystem.

![](_page_108_Picture_2.jpeg)

#### **Note**

These names are also written to INNODB\_TABLES in their appended forms, but are written to TABLES in their unappended form, as entered by the user.

# <span id="page-108-0"></span>**11.2.5 Function Name Parsing and Resolution**

MySQL supports built-in (native) functions, loadable functions, and stored functions. This section describes how the server recognizes whether the name of a built-in function is used as a function call or as an identifier, and how the server determines which function to use in cases when functions of different types exist with a given name.

- [Built-In Function Name Parsing](#page-108-1)
- [Function Name Resolution](#page-111-1)

### <span id="page-108-1"></span>**Built-In Function Name Parsing**

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

The following list names the functions in MySQL 8.4 that are affected by the IGNORE\_SPACE setting and listed as special in the sql/lex.h source file. You may find it easiest to treat the no-whitespace requirement as applying to all function calls.

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

However, enabling IGNORE\_SPACE also has the side effect that the parser treats the affected function names as reserved words (see [Section 11.3, "Keywords and Reserved Words"\)](#page-111-0). This means that a space following the name no longer signifies its use as an identifier. The name can be used in function calls with or without following whitespace, but causes a syntax error in nonexpression context unless it is quoted. For example, with IGNORE\_SPACE enabled, both of the following statements fail with a syntax error because the parser interprets count as a reserved word:

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

Check Section 7.1.11, "Server SQL Modes", to see which composite modes enable IGNORE\_SPACE.

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
```

CREATE TABLE `count` (i INT);

### <span id="page-111-1"></span>**Function Name Resolution**

The following rules describe how the server resolves references to function names for function creation and invocation:

• Built-in functions and loadable functions

An error occurs if you try to create a loadable function with the same name as a built-in function.

IF NOT EXISTS has no effect in such cases. See Section 15.7.4.1, "CREATE FUNCTION Statement for Loadable Functions", for more information.

• Built-in functions and stored functions

It is possible to create a stored function with the same name as a built-in function, but to invoke the stored function it is necessary to qualify it with a schema name. For example, if you create a stored function named PI in the test schema, invoke it as test.PI() because the server resolves PI() without a qualifier as a reference to the built-in function. The server generates a warning if the stored function name collides with a built-in function name. The warning can be displayed with SHOW WARNINGS.

IF NOT EXISTS has no effect in such cases; see Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements".

• Loadable functions and stored functions

It is possible to create a stored function with the same name as an existing loadable function, or the other way around. The server generates a warning if a proposed stored function name collides with an existing loadable function name, or if a proposed loadable function name would be the same as that of an existing stored function. In either case, once both functions exist, it is necessary thereafter to qualify the stored function with a schema name when invoking it; the server assumes in such cases that the unqualified name refers to the loadable function.

MySQL 8.4 supports IF NOT EXISTS with CREATE FUNCTION statements, but it has no effect in such cases.

The preceding function name resolution rules have implications for upgrading to versions of MySQL that implement new built-in functions:

- If you have already created a loadable function with a given name and upgrade MySQL to a version that implements a new built-in function with the same name, the loadable function becomes inaccessible. To correct this, use DROP FUNCTION to drop the loadable function and CREATE FUNCTION to re-create the loadable function with a different nonconflicting name. Then modify any affected code to use the new name.
- If a new version of MySQL implements a built-in function or loadable function with the same name as an existing stored function, you have two choices: Rename the stored function to use a nonconflicting name, or change any calls to the function that do not do so already to use a schema qualifier (schema\_name.func\_name() syntax). In either case, modify any affected code accordingly.

# <span id="page-111-0"></span>**11.3 Keywords and Reserved Words**

Keywords are words that have significance in SQL. Certain keywords, such as SELECT, DELETE, or BIGINT, are reserved and require special treatment for use as identifiers such as table and column names. This may also be true for the names of built-in functions.

Most nonreserved keywords are permitted as identifiers without quoting. Some keywords which are otherwise considered nonreserved are restricted from use as unquoted identifiers for roles, stored

program labels, or, in some cases, both. See [MySQL 8.4 Restricted Keywords,](#page-137-0) for listings of these keywords.

Reserved words are permitted as identifiers if you quote them as described in [Section 11.2, "Schema](#page-100-0) [Object Names":](#page-100-0)

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

Names of built-in functions are permitted as identifiers but may require care to be used as such. For example, COUNT is acceptable as a column name. However, by default, no whitespace is permitted in function invocations between the function name and the following ( character. This requirement enables the parser to distinguish whether the name is used in a function call or in nonfunction context. For further details on recognition of function names, see [Section 11.2.5, "Function Name Parsing and](#page-108-0) [Resolution".](#page-108-0)

The INFORMATION\_SCHEMA.KEYWORDS table lists the words considered keywords by MySQL and indicates whether they are reserved. See Section 28.3.17, "The INFORMATION\_SCHEMA KEYWORDS Table".

- [MySQL 8.4 Keywords and Reserved Words](#page-112-0)
- [MySQL 8.4 New Keywords and Reserved Words](#page-135-0)
- [MySQL 8.4 Removed Keywords and Reserved Words](#page-136-0)
- [MySQL 8.4 Restricted Keywords](#page-137-0)

# <span id="page-112-0"></span>**MySQL 8.4 Keywords and Reserved Words**

The following list shows the keywords and reserved words in MySQL 8.4, along with changes to individual words from version to version. Reserved keywords are marked with (R). In addition, \_FILENAME is reserved.

At some point, you might upgrade to a higher version, so it is a good idea to have a look at future reserved words, too. You can find these in the manuals that cover higher versions of MySQL. Most of the reserved words in the list are forbidden by standard SQL as column or table names (for example, GROUP). A few are reserved because MySQL needs them and uses a yacc parser.

#### [A](#page-112-1) | [B](#page-113-0) | [C](#page-114-0) | [D](#page-116-0) | [E](#page-117-0) | [F](#page-118-0) | [G](#page-119-0) | [H](#page-120-0) | [I](#page-120-1) | [J](#page-121-0) | [K](#page-121-1) | [L](#page-122-0) | [M](#page-123-0) | [N](#page-124-0) | [O](#page-125-0) | [P](#page-125-1) | [Q](#page-127-0) | [R](#page-127-1) | [S](#page-129-0) | [T](#page-132-0) | [U](#page-133-0) | [V](#page-134-0) | [W](#page-135-1) | [X](#page-135-2) | [Y](#page-135-3) | [Z](#page-135-4)

#### <span id="page-112-1"></span>A

- ACCESSIBLE (R)
- ACCOUNT
- ACTION
- ACTIVE

- ADD (R)
- ADMIN
- AFTER
- AGAINST
- AGGREGATE
- ALGORITHM
- ALL (R)
- ALTER (R)
- ALWAYS
- ANALYZE (R)
- AND (R)
- ANY
- ARRAY
- AS (R)
- ASC (R)
- ASCII
- ASENSITIVE (R)
- AT
- ATTRIBUTE
- AUTHENTICATION
- AUTO
- AUTOEXTEND\_SIZE
- AUTO\_INCREMENT
- AVG
- AVG\_ROW\_LENGTH

#### <span id="page-113-0"></span>B

- BACKUP
- BEFORE (R)
- BEGIN
- BERNOULLI
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
- BUCKETS
- BULK
- BY (R)
- BYTE
- <span id="page-114-0"></span>C
- CACHE
- CALL (R)
- CASCADE (R)
- CASCADED
- CASE (R)
- CATALOG\_NAME
- CHAIN
- CHALLENGE\_RESPONSE
- CHANGE (R)
- CHANGED
- CHANNEL
- CHAR (R)
- CHARACTER (R)
- CHARSET
- CHECK (R)
- CHECKSUM
- CIPHER
- CLASS\_ORIGIN
- CLIENT
- CLONE

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
- COMPONENT
- COMPRESSED
- COMPRESSION
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
- CUBE (R)

- CUME\_DIST (R)
- CURRENT
- CURRENT\_DATE (R)
- CURRENT\_TIME (R)
- CURRENT\_TIMESTAMP (R)
- CURRENT\_USER (R)
- CURSOR (R)
- CURSOR\_NAME

#### <span id="page-116-0"></span>D

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
- DEFINITION
- DELAYED (R)
- DELAY\_KEY\_WRITE
- DELETE (R)
- DENSE\_RANK (R)
- DESC (R)

- DESCRIBE (R)
- DESCRIPTION
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

### <span id="page-117-0"></span>E

- EACH (R)
- ELSE (R)
- ELSEIF (R)
- EMPTY (R)
- ENABLE
- ENCLOSED (R)
- ENCRYPTION
- END
- ENDS
- ENFORCED
- ENGINE
- ENGINES
- ENGINE\_ATTRIBUTE
- ENUM

- ERROR
- ERRORS
- ESCAPE
- ESCAPED (R)
- EVENT
- EVENTS
- EVERY
- EXCEPT (R)
- EXCHANGE
- EXCLUDE
- EXECUTE
- EXISTS (R)
- EXIT (R)
- EXPANSION
- EXPIRE
- EXPLAIN (R)
- EXPORT
- EXTENDED
- EXTENT\_SIZE

<span id="page-118-0"></span>F

- FACTOR
- FAILED\_LOGIN\_ATTEMPTS
- FALSE (R)
- FAST
- FAULTS
- FETCH (R)
- FIELDS
- FILE
- FILE\_BLOCK\_SIZE
- FILTER
- FINISH
- FIRST
- FIRST\_VALUE (R)

- FIXED
- FLOAT (R)
- FLOAT4 (R)
- FLOAT8 (R)
- FLUSH
- FOLLOWING
- FOLLOWS
- FOR (R)
- FORCE (R)
- FOREIGN (R)
- FORMAT
- FOUND
- FROM (R)
- FULL
- FULLTEXT (R)
- FUNCTION (R)

#### <span id="page-119-0"></span>G

- GENERAL
- GENERATE
- GENERATED (R)
- GEOMCOLLECTION
- GEOMETRY
- GEOMETRYCOLLECTION
- GET (R)
- GET\_FORMAT
- GET\_SOURCE\_PUBLIC\_KEY
- GLOBAL
- GRANT (R)
- GRANTS
- GROUP (R)
- GROUPING (R)
- GROUPS (R)
- GROUP\_REPLICATION

- GTIDS
- <span id="page-120-0"></span>H
- HANDLER

• GTID\_ONLY

- HASH
- HAVING (R)
- HELP
- HIGH\_PRIORITY (R)
- HISTOGRAM
- HISTORY
- HOST
- HOSTS
- HOUR
- HOUR\_MICROSECOND (R)
- HOUR\_MINUTE (R)
- HOUR\_SECOND (R)
- <span id="page-120-1"></span>I
- IDENTIFIED
- IF (R)
- IGNORE (R)
- IGNORE\_SERVER\_IDS
- IMPORT
- IN (R)
- INACTIVE
- INDEX (R)
- INDEXES
- INFILE (R)
- INITIAL
- INITIAL\_SIZE
- INITIATE
- INNER (R)
- INOUT (R)
- INSENSITIVE (R)

- INSERT (R)
- INSERT\_METHOD
- INSTALL
- INSTANCE
- INT (R)
- INT1 (R)
- INT2 (R)
- INT3 (R)
- INT4 (R)
- INT8 (R)
- INTEGER (R)
- INTERSECT (R)
- INTERVAL (R)
- INTO (R)
- INVISIBLE
- INVOKER
- IO
- IO\_AFTER\_GTIDS (R)
- IO\_BEFORE\_GTIDS (R)
- IO\_THREAD
- IPC
- IS (R)
- ISOLATION
- ISSUER
- ITERATE (R)

<span id="page-121-0"></span>J

- JOIN (R)
- JSON
- JSON\_TABLE (R)
- JSON\_VALUE

<span id="page-121-1"></span>K

- KEY (R)
- KEYRING

- KEYS (R)
- KEY\_BLOCK\_SIZE
- KILL (R)

<span id="page-122-0"></span>L

- LAG (R)
- LANGUAGE
- LAST
- LAST\_VALUE (R)
- LATERAL (R)
- LEAD (R)
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
- LOCKED
- LOCKS
- LOG
- LOGFILE
- LOGS
- LONG (R)

- LONGBLOB (R)
- LONGTEXT (R)
- LOOP (R)
- LOW\_PRIORITY (R)

#### <span id="page-123-0"></span>M

- MANUAL (R)
- MASTER
- MATCH (R)
- MAXVALUE (R)
- MAX\_CONNECTIONS\_PER\_HOUR
- MAX\_QUERIES\_PER\_HOUR
- MAX\_ROWS
- MAX\_SIZE
- MAX\_UPDATES\_PER\_HOUR
- MAX\_USER\_CONNECTIONS
- MEDIUM
- MEDIUMBLOB (R)
- MEDIUMINT (R)
- MEDIUMTEXT (R)
- MEMBER
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

#### <span id="page-124-0"></span>N

- NAME
- NAMES
- NATIONAL
- NATURAL (R)
- NCHAR
- NDB
- NDBCLUSTER
- NESTED
- NETWORK\_NAMESPACE
- NEVER
- NEW
- NEXT
- NO
- NODEGROUP
- NONE
- NOT (R)
- NOWAIT
- NO\_WAIT
- NO\_WRITE\_TO\_BINLOG (R)
- NTH\_VALUE (R)
- NTILE (R)
- NULL (R)
- NULLS
- NUMBER
- NUMERIC (R)

#### • NVARCHAR

#### <span id="page-125-0"></span>O

- OF (R)
- OFF
- OFFSET
- OJ
- OLD
- ON (R)
- ONE
- ONLY
- OPEN
- OPTIMIZE (R)
- OPTIMIZER\_COSTS (R)
- OPTION (R)
- OPTIONAL
- OPTIONALLY (R)
- OPTIONS
- OR (R)
- ORDER (R)
- ORDINALITY
- ORGANIZATION
- OTHERS
- OUT (R)
- OUTER (R)
- OUTFILE (R)
- OVER (R)
- OWNER

#### <span id="page-125-1"></span>P

- PACK\_KEYS
- PAGE
- PARALLEL (R)
- PARSER
- PARSE\_TREE

- PARTIAL
- PARTITION (R)
- PARTITIONING
- PARTITIONS
- PASSWORD
- PASSWORD\_LOCK\_TIME
- PATH
- PERCENT\_RANK (R)
- PERSIST
- PERSIST\_ONLY
- PHASE
- PLUGIN
- PLUGINS
- PLUGIN\_DIR
- POINT
- POLYGON
- PORT
- PRECEDES
- PRECEDING
- PRECISION (R)
- PREPARE
- PRESERVE
- PREV
- PRIMARY (R)
- PRIVILEGES
- PRIVILEGE\_CHECKS\_USER
- PROCEDURE (R)
- PROCESS
- PROCESSLIST
- PROFILE
- PROFILES
- PROXY
- PURGE (R)

#### <span id="page-127-0"></span>Q

- QUALIFY (R)
- QUARTER
- QUERY
- QUICK

#### <span id="page-127-1"></span>R

- RANDOM
- RANGE (R)
- RANK (R)
- READ (R)
- READS (R)
- READ\_ONLY
- READ\_WRITE (R)
- REAL (R)
- REBUILD
- RECOVER
- RECURSIVE (R)
- REDO\_BUFFER\_SIZE
- REDUNDANT
- REFERENCE
- REFERENCES (R)
- REGEXP (R)
- REGISTRATION
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
- REPLICA
- REPLICAS
- REPLICATE\_DO\_DB
- REPLICATE\_DO\_TABLE
- REPLICATE\_IGNORE\_DB
- REPLICATE\_IGNORE\_TABLE
- REPLICATE\_REWRITE\_DB
- REPLICATE\_WILD\_DO\_TABLE
- REPLICATE\_WILD\_IGNORE\_TABLE
- REPLICATION
- REQUIRE (R)
- REQUIRE\_ROW\_FORMAT
- RESET
- RESIGNAL (R)
- RESOURCE
- RESPECT
- RESTART
- RESTORE
- RESTRICT (R)
- RESUME
- RETAIN
- RETURN (R)
- RETURNED\_SQLSTATE
- RETURNING
- RETURNS
- REUSE
- REVERSE
- REVOKE (R)
- RIGHT (R)

- RLIKE (R)
- ROLE
- ROLLBACK
- ROLLUP
- ROTATE
- ROUTINE
- ROW (R)
- ROWS (R)
- ROW\_COUNT
- ROW\_FORMAT
- ROW\_NUMBER (R)
- RTREE

#### <span id="page-129-0"></span>S

- S3
- SAVEPOINT
- SCHEDULE
- SCHEMA (R)
- SCHEMAS (R)
- SCHEMA\_NAME
- SECOND
- SECONDARY
- SECONDARY\_ENGINE
- SECONDARY\_ENGINE\_ATTRIBUTE
- SECONDARY\_LOAD
- SECONDARY\_UNLOAD
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
- SKIP
- SLAVE
- SLOW
- SMALLINT (R)
- SNAPSHOT
- SOCKET
- SOME
- SONAME
- SOUNDS
- SOURCE
- SOURCE\_AUTO\_POSITION
- SOURCE\_BIND
- SOURCE\_COMPRESSION\_ALGORITHMS
- SOURCE\_CONNECT\_RETRY
- SOURCE\_DELAY
- SOURCE\_HEARTBEAT\_PERIOD
- SOURCE\_HOST
- SOURCE\_LOG\_FILE
- SOURCE\_LOG\_POS
- SOURCE\_PASSWORD
- SOURCE\_PORT
- SOURCE\_PUBLIC\_KEY\_PATH
- SOURCE\_RETRY\_COUNT
- SOURCE\_SSL
- SOURCE\_SSL\_CA

- SOURCE\_SSL\_CAPATH
- SOURCE\_SSL\_CERT
- SOURCE\_SSL\_CIPHER
- SOURCE\_SSL\_CRL
- SOURCE\_SSL\_CRLPATH
- SOURCE\_SSL\_KEY
- SOURCE\_SSL\_VERIFY\_SERVER\_CERT
- SOURCE\_TLS\_CIPHERSUITES
- SOURCE\_TLS\_VERSION
- SOURCE\_USER
- SOURCE\_ZSTD\_COMPRESSION\_LEVEL
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
- SRID
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
- STORED (R)
- STRAIGHT\_JOIN (R)
- STREAM
- STRING
- SUBCLASS\_ORIGIN
- SUBJECT
- SUBPARTITION
- SUBPARTITIONS
- SUPER
- SUSPEND
- SWAPS
- SWITCHES
- SYSTEM (R)

#### <span id="page-132-0"></span>T

- TABLE (R)
- TABLES
- TABLESAMPLE (R)
- TABLESPACE
- TABLE\_CHECKSUM
- TABLE\_NAME

- TEMPORARY
- TEMPTABLE
- TERMINATED (R)
- TEXT
- THAN
- THEN (R)
- THREAD\_PRIORITY
- TIES
- TIME
- TIMESTAMP
- TIMESTAMPADD
- TIMESTAMPDIFF
- TINYBLOB (R)
- TINYINT (R)
- TINYTEXT (R)
- TLS
- TO (R)
- TRAILING (R)
- TRANSACTION
- TRIGGER (R)
- TRIGGERS
- TRUE (R)
- TRUNCATE
- TYPE
- TYPES

#### <span id="page-133-0"></span>U

- UNBOUNDED
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
- UNREGISTER
- UNSIGNED (R)
- UNTIL
- UPDATE (R)
- UPGRADE
- URL
- USAGE (R)
- USE (R)
- USER
- USER\_RESOURCES
- USE\_FRM
- USING (R)
- UTC\_DATE (R)
- UTC\_TIME (R)
- UTC\_TIMESTAMP (R)

### <span id="page-134-0"></span>V

- VALIDATION
- VALUE
- VALUES (R)
- VARBINARY (R)
- VARCHAR (R)
- VARCHARACTER (R)
- VARIABLES
- VARYING (R)
- VCPU
- VIEW
- VIRTUAL (R)
- VISIBLE

#### <span id="page-135-1"></span>W

- WAIT
- WARNINGS
- WEEK
- WEIGHT\_STRING
- WHEN (R)
- WHERE (R)
- WHILE (R)
- WINDOW (R)
- WITH (R)
- WITHOUT
- WORK
- WRAPPER
- WRITE (R)

#### <span id="page-135-2"></span>X

- X509
- XA
- XID
- XML
- XOR (R)

### <span id="page-135-3"></span>Y

- YEAR
- YEAR\_MONTH (R)

#### <span id="page-135-4"></span>Z

- ZEROFILL (R)
- ZONE

# <span id="page-135-0"></span>**MySQL 8.4 New Keywords and Reserved Words**

The following list shows the keywords and reserved words that are added in MySQL 8.4, compared to MySQL 8.0. Reserved keywords are marked with (R).

#### [A](#page-135-5) | [B](#page-135-6) | [G](#page-136-1) | [L](#page-136-2) | [M](#page-136-3) | [P](#page-136-4) | [Q](#page-136-5) | [S](#page-136-6) | [T](#page-136-7)

### <span id="page-135-5"></span>A

• AUTO

<span id="page-135-6"></span>B

```
• BERNOULLI
G
• GTIDS
L
• LOG
M
• MANUAL (R)
P
• PARALLEL (R)
• PARSE_TREE
Q
• QUALIFY (R)
S
• S3
T
```

<span id="page-136-6"></span><span id="page-136-5"></span>• TABLESAMPLE (R)

# <span id="page-136-7"></span><span id="page-136-0"></span>**MySQL 8.4 Removed Keywords and Reserved Words**

The following list shows the keywords and reserved words that are removed in MySQL 8.4, compared to MySQL 8.0. Reserved keywords are marked with (R).

```
G | M
G
• GET_MASTER_PUBLIC_KEY
M
• MASTER_AUTO_POSITION
• MASTER_BIND (R)
• MASTER_COMPRESSION_ALGORITHMS
• MASTER_CONNECT_RETRY
• MASTER_DELAY
• MASTER_HEARTBEAT_PERIOD
• MASTER_HOST
• MASTER_LOG_FILE
• MASTER_LOG_POS
• MASTER_PASSWORD
```

- MASTER\_PORT
- MASTER\_PUBLIC\_KEY\_PATH
- MASTER\_RETRY\_COUNT
- MASTER\_SSL
- MASTER\_SSL\_CA
- MASTER\_SSL\_CAPATH
- MASTER\_SSL\_CERT
- MASTER\_SSL\_CIPHER
- MASTER\_SSL\_CRL
- MASTER\_SSL\_CRLPATH
- MASTER\_SSL\_KEY
- MASTER\_SSL\_VERIFY\_SERVER\_CERT (R)
- MASTER\_TLS\_CIPHERSUITES
- MASTER\_TLS\_VERSION
- MASTER\_USER
- MASTER\_ZSTD\_COMPRESSION\_LEVEL

# <span id="page-137-0"></span>**MySQL 8.4 Restricted Keywords**

Some MySQL keywords are not reserved but even so must be quoted in certain circumstances. This section provides listings of these keywords.

- [Keywords which must be quoted when used as labels](#page-137-1)
- [Keywords which must be quoted when used as role names](#page-139-1)
- [Keywords which must be quoted when used as labels or role names](#page-139-2)

#### <span id="page-137-1"></span>**Keywords which must be quoted when used as labels**

The keywords listed here must be quoted when used as labels in MySQL stored programs:

#### [A](#page-137-2) | [B](#page-137-3) | [C](#page-137-4) | [D](#page-138-0) | [E](#page-138-1) | [F](#page-138-2) | [H](#page-138-3) | [I](#page-138-4) | [L](#page-138-5) | [N](#page-138-6) | [P](#page-138-7) | [R](#page-138-8) | [S](#page-138-9) | [T](#page-139-3) | [U](#page-139-4) | [X](#page-139-5)

#### <span id="page-137-2"></span>A

• ASCII

#### <span id="page-137-3"></span>B

- BEGIN
- BYTE

#### <span id="page-137-4"></span>C

- CACHE
- CHARSET

- CHECKSUM • CLONE • COMMENT
- CONTAINS

• COMMIT

<span id="page-138-0"></span>D

- DEALLOCATE
- DO

<span id="page-138-1"></span>E

• END

<span id="page-138-2"></span>F

- FLUSH
- FOLLOWS

<span id="page-138-3"></span>H

- HANDLER
- HELP

<span id="page-138-4"></span>I

- IMPORT
- INSTALL

<span id="page-138-5"></span>L

• LANGUAGE

<span id="page-138-6"></span>N

• NO

<span id="page-138-7"></span>P

- PRECEDES
- PREPARE

<span id="page-138-8"></span>R

- REPAIR
- RESET
- ROLLBACK

<span id="page-138-9"></span>S

- SAVEPOINT
- SIGNED

- SLAVE
- START
- STOP

<span id="page-139-3"></span>T

• TRUNCATE

<span id="page-139-4"></span>U

- UNICODE
- UNINSTALL

X

• XA

### <span id="page-139-5"></span><span id="page-139-1"></span>**Keywords which must be quoted when used as role names**

The keywords listed here must be quoted when used as names of roles:

- EVENT
- FILE
- NONE
- PROCESS
- PROXY
- RELOAD
- REPLICATION
- RESOURCE
- SUPER

#### <span id="page-139-2"></span>**Keywords which must be quoted when used as labels or role names**

The keywords listed here must be quoted when used as labels in stored programs, or as names of roles:

- EXECUTE
- RESTART
- SHUTDOWN

# <span id="page-139-0"></span>**11.4 User-Defined Variables**

You can store a value in a user-defined variable in one statement and refer to it later in another statement. This enables you to pass values from one statement to another.

User variables are written as @var\_name, where the variable name var\_name consists of alphanumeric characters, ., \_, and \$. A user variable name can contain other characters if you quote it as a string or identifier (for example, @'my-var', @"my-var", or @`my-var`).

User-defined variables are session specific. A user variable defined by one client cannot be seen or used by other clients. (Exception: A user with access to the Performance Schema

user\_variables\_by\_thread table can see all user variables for all sessions.) All variables for a given client session are automatically freed when that client exits.

User variable names are not case-sensitive. Names have a maximum length of 64 characters.

One way to set a user-defined variable is by issuing a SET statement:

```
SET @var_name = expr [, @var_name = expr] ...
```

For SET, either = or := can be used as the assignment operator.

User variables can be assigned a value from a limited set of data types: integer, decimal, floating-point, binary or nonbinary string, or NULL value. Assignment of decimal and real values does not preserve the precision or scale of the value. A value of a type other than one of the permissible types is converted to a permissible type. For example, a value having a temporal or spatial data type is converted to a binary string. A value having the JSON data type is converted to a string with a character set of utf8mb4 and a collation of utf8mb4\_bin.

If a user variable is assigned a nonbinary (character) string value, it has the same character set and collation as the string. The coercibility of user variables is implicit. (This is the same coercibility as for table column values.)

Hexadecimal or bit values assigned to user variables are treated as binary strings. To assign a hexadecimal or bit value as a number to a user variable, use it in numeric context. For example, add 0 or use CAST(... AS UNSIGNED):

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

A reference to a user variable in a prepared statement has its type determined when the statement is first prepared, and retains this type each time the statement is executed thereafter. Similarly, the type of a user variable employed in a statement within a stored procedure is determined the first time the stored procedure is invoked, and retains this type with each subsequent invocation.

User variables may be used in most contexts where expressions are permitted. This does not currently include contexts that explicitly require a literal value, such as in the LIMIT clause of a SELECT statement, or the IGNORE N LINES clause of a LOAD DATA statement.

Previous releases of MySQL made it possible to assign a value to a user variable in statements other than SET. This functionality is supported in MySQL 8.4 for backward compatibility but is subject to removal in a future release of MySQL.

When making an assignment in this way, you must use := as the assignment operator; = is treated as the comparison operator in statements other than SET.

The order of evaluation for expressions involving user variables is undefined. For example, there is no guarantee that SELECT @a, @a:=@a+1 evaluates @a first and then performs the assignment.

In addition, the default result type of a variable is based on its type at the beginning of the statement. This may have unintended effects if a variable holds a value of one type at the beginning of a statement in which it is also assigned a new value of a different type.

To avoid problems with this behavior, either do not assign a value to and read the value of the same variable within a single statement, or else set the variable to 0, 0.0, or '' to define its type before you use it.

HAVING, GROUP BY, and ORDER BY, when referring to a variable that is assigned a value in the select expression list do not work as expected because the expression is evaluated on the client and thus can use stale column values from a previous row.

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
```

```
mysql> EXECUTE stmt;
+----+
| c1 |
+----+
| 0 |
+----+
| 1 |
+----+
2 rows in set (0.00 sec)
mysql> DEALLOCATE PREPARE stmt;
Query OK, 0 rows affected (0.00 sec)
```

See Section 15.5, "Prepared Statements", for more information.

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

# <span id="page-142-0"></span>**11.5 Expressions**

This section lists the grammar rules that expressions must follow in MySQL and provides additional information about the types of terms that may appear in expressions.

- [Expression Syntax](#page-142-1)
- [Expression Term Notes](#page-144-0)
- [Temporal Intervals](#page-144-1)

# <span id="page-142-1"></span>**Expression Syntax**

The following grammar rules define expression syntax in MySQL. The grammar shown here is based on that given in the sql/sql\_yacc.yy file of MySQL source distributions. For additional information about some of the expression terms, see [Expression Term Notes.](#page-144-0)

```
expr:
 expr OR expr
 | expr || expr
 | expr XOR expr
 | expr AND expr
 | expr && expr
 | NOT expr
```

```
 | ! expr
 | boolean_primary IS [NOT] {TRUE | FALSE | UNKNOWN}
 | boolean_primary
boolean_primary:
 boolean_primary IS [NOT] NULL
 | boolean_primary <=> predicate
 | boolean_primary comparison_operator predicate
 | boolean_primary comparison_operator {ALL | ANY} (subquery)
 | predicate
comparison_operator: = | >= | > | <= | < | <> | !=
predicate:
 bit_expr [NOT] IN (subquery)
 | bit_expr [NOT] IN (expr [, expr] ...)
 | bit_expr [NOT] BETWEEN bit_expr AND predicate
 | bit_expr SOUNDS LIKE bit_expr
 | bit_expr [NOT] LIKE simple_expr [ESCAPE simple_expr]
 | bit_expr [NOT] REGEXP bit_expr
 | bit_expr
bit_expr:
 bit_expr | bit_expr
 | bit_expr & bit_expr
 | bit_expr << bit_expr
 | bit_expr >> bit_expr
 | bit_expr + bit_expr
 | bit_expr - bit_expr
 | bit_expr * bit_expr
 | bit_expr / bit_expr
 | bit_expr DIV bit_expr
 | bit_expr MOD bit_expr
 | bit_expr % bit_expr
 | bit_expr ^ bit_expr
 | bit_expr + interval_expr
 | bit_expr - interval_expr
 | simple_expr
simple_expr:
 literal
 | identifier
 | function_call
 | simple_expr COLLATE collation_name
 | param_marker
 | variable
 | simple_expr || simple_expr
 | + simple_expr
 | - simple_expr
 | ~ simple_expr
 | ! simple_expr
 | BINARY simple_expr
 | (expr [, expr] ...)
 | ROW (expr, expr [, expr] ...)
 | (subquery)
 | EXISTS (subquery)
 | {identifier expr}
 | match_expr
 | case_expr
 | interval_expr
```

For operator precedence, see Section 14.4.1, "Operator Precedence". The precedence and meaning of some operators depends on the SQL mode:

- By default, || is a logical OR operator. With PIPES\_AS\_CONCAT enabled, || is string concatenation, with a precedence between ^ and the unary operators.
- By default, ! has a higher precedence than NOT. With HIGH\_NOT\_PRECEDENCE enabled, ! and NOT have the same precedence.

See Section 7.1.11, "Server SQL Modes".

### <span id="page-144-0"></span>**Expression Term Notes**

For literal value syntax, see [Section 11.1, "Literal Values".](#page-88-0)

For identifier syntax, see [Section 11.2, "Schema Object Names"](#page-100-0).

Variables can be user variables, system variables, or stored program local variables or parameters:

- User variables: [Section 11.4, "User-Defined Variables"](#page-139-0)
- System variables: Section 7.1.9, "Using System Variables"
- Stored program local variables: Section 15.6.4.1, "Local Variable DECLARE Statement"
- Stored program parameters: Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements"

param\_marker is ? as used in prepared statements for placeholders. See Section 15.5.1, "PREPARE Statement".

(subquery) indicates a subquery that returns a single value; that is, a scalar subquery. See Section 15.2.15.1, "The Subquery as Scalar Operand".

{identifier expr} is ODBC escape syntax and is accepted for ODBC compatibility. The value is expr. The { and } curly braces in the syntax should be written literally; they are not metasyntax as used elsewhere in syntax descriptions.

match\_expr indicates a MATCH expression. See Section 14.9, "Full-Text Search Functions".

case\_expr indicates a CASE expression. See Section 14.5, "Flow Control Functions".

interval\_expr represents a temporal interval. See [Temporal Intervals.](#page-144-1)

# <span id="page-144-1"></span>**Temporal Intervals**

interval\_expr in expressions represents a temporal interval. Intervals have this syntax:

INTERVAL expr unit

expr represents a quantity. unit represents the unit for interpreting the quantity; it is a specifier such as HOUR, DAY, or WEEK. The INTERVAL keyword and the unit specifier are not case-sensitive.

The following table shows the expected form of the expr argument for each unit value.

**Table 11.2 Temporal Interval Expression and Unit Arguments**

| unit Value         | Expected expr Format           |
|--------------------|--------------------------------|
| MICROSECOND        | MICROSECONDS                   |
| SECOND             | SECONDS                        |
| MINUTE             | MINUTES                        |
| HOUR               | HOURS                          |
| DAY                | DAYS                           |
| WEEK               | WEEKS                          |
| MONTH              | MONTHS                         |
| QUARTER            | QUARTERS                       |
| YEAR               | YEARS                          |
| SECOND_MICROSECOND | 'SECONDS.MICROSECONDS'         |
| MINUTE_MICROSECOND | 'MINUTES:SECONDS.MICROSECONDS' |

| unit Value       | Expected expr Format                         |
|------------------|----------------------------------------------|
| MINUTE_SECOND    | 'MINUTES:SECONDS'                            |
| HOUR_MICROSECOND | 'HOURS:MINUTES:SECONDS.MICROSECONDS'         |
| HOUR_SECOND      | 'HOURS:MINUTES:SECONDS'                      |
| HOUR_MINUTE      | 'HOURS:MINUTES'                              |
| DAY_MICROSECOND  | 'DAYS<br>HOURS:MINUTES:SECONDS.MICROSECONDS' |
| DAY_SECOND       | 'DAYS HOURS:MINUTES:SECONDS'                 |
| DAY_MINUTE       | 'DAYS HOURS:MINUTES'                         |
| DAY_HOUR         | 'DAYS HOURS'                                 |
| YEAR_MONTH       | 'YEARS-MONTHS'                               |

MySQL permits any punctuation delimiter in the expr format. Those shown in the table are the suggested delimiters.

Temporal intervals are used for certain functions, such as DATE\_ADD() and DATE\_SUB():

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

Temporal arithmetic also can be performed in expressions using INTERVAL together with the + or operator:

```
date + INTERVAL expr unit
date - INTERVAL expr unit
```

INTERVAL expr unit is permitted on either side of the + operator if the expression on the other side is a date or datetime value. For the - operator, INTERVAL expr unit is permitted only on the right side, because it makes no sense to subtract a date or datetime value from an interval.

```
mysql> SELECT '2018-12-31 23:59:59' + INTERVAL 1 SECOND;
 -> '2019-01-01 00:00:00'
mysql> SELECT INTERVAL 1 DAY + '2018-12-31';
 -> '2019-01-01'
mysql> SELECT '2025-01-01' - INTERVAL 1 SECOND;
 -> '2024-12-31 23:59:59'
```

The EXTRACT() function uses the same kinds of unit specifiers as DATE\_ADD() or DATE\_SUB(), but extracts parts from the date rather than performing date arithmetic:

```
mysql> SELECT EXTRACT(YEAR FROM '2019-07-02');
```

```
 -> 2019
mysql> SELECT EXTRACT(YEAR_MONTH FROM '2019-07-02 01:02:03');
 -> 201907
```

Temporal intervals can be used in CREATE EVENT statements:

```
CREATE EVENT myevent
 ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 HOUR
 DO
 UPDATE myschema.mytable SET mycol = mycol + 1;
```

If you specify an interval value that is too short (does not include all the interval parts that would be expected from the unit keyword), MySQL assumes that you have left out the leftmost parts of the interval value. For example, if you specify a unit of DAY\_SECOND, the value of expr is expected to have days, hours, minutes, and seconds parts. If you specify a value like '1:10', MySQL assumes that the days and hours parts are missing and the value represents minutes and seconds. In other words, '1:10' DAY\_SECOND is interpreted in such a way that it is equivalent to '1:10' MINUTE\_SECOND. This is analogous to the way that MySQL interprets TIME values as representing elapsed time rather than as a time of day.

expr is treated as a string, so be careful if you specify a nonstring value with INTERVAL. For example, with an interval specifier of HOUR\_MINUTE, '6/4' is treated as 6 hours, four minutes, whereas 6/4 evaluates to 1.5000 and is treated as 1 hour, 5000 minutes:

```
mysql> SELECT '6/4', 6/4;
 -> 1.5000
mysql> SELECT DATE_ADD('2019-01-01', INTERVAL '6/4' HOUR_MINUTE);
 -> '2019-01-01 06:04:00'
mysql> SELECT DATE_ADD('2019-01-01', INTERVAL 6/4 HOUR_MINUTE);
 -> '2019-01-04 12:20:00'
```

To ensure interpretation of the interval value as you expect, a CAST() operation may be used. To treat 6/4 as 1 hour, 5 minutes, cast it to a DECIMAL value with a single fractional digit:

```
mysql> SELECT CAST(6/4 AS DECIMAL(3,1));
 -> 1.5
mysql> SELECT DATE_ADD('1970-01-01 12:00:00',
 -> INTERVAL CAST(6/4 AS DECIMAL(3,1)) HOUR_MINUTE);
 -> '1970-01-01 13:05:00'
```

If you add to or subtract from a date value something that contains a time part, the result is automatically converted to a datetime value:

```
mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 DAY);
 -> '2023-01-02'
mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 HOUR);
 -> '2023-01-01 01:00:00'
```

If you add MONTH, YEAR\_MONTH, or YEAR and the resulting date has a day that is larger than the maximum day for the new month, the day is adjusted to the maximum days in the new month:

```
mysql> SELECT DATE_ADD('2019-01-30', INTERVAL 1 MONTH);
 -> '2019-02-28'
```

Date arithmetic operations require complete dates and do not work with incomplete dates such as '2016-07-00' or badly malformed dates:

```
mysql> SELECT DATE_ADD('2016-07-00', INTERVAL 1 DAY);
 -> NULL
mysql> SELECT '2005-03-32' + INTERVAL 1 MONTH;
 -> NULL
```

# <span id="page-146-0"></span>**11.6 Query Attributes**

The most visible part of an SQL statement is the text of the statement. Clients can also define query attributes that apply to the next statement sent to the server for execution:

- Attributes are defined prior to sending the statement.
- Attributes exist until statement execution ends, at which point the attribute set is cleared.
- While attributes exist, they can be accessed on the server side.

Examples of the ways query attributes may be used:

- A web application produces pages that generate database queries, and for each query must track the URL of the page that generated it.
- An application passes extra processing information with each query, for use by a plugin such as an audit plugin or query rewrite plugin.

MySQL supports these capabilities without the use of workarounds such as specially formatted comments included in query strings. The remainder of this section describes how to use query attribute support, including the prerequisites that must be satisfied.

- [Defining and Accessing Query Attributes](#page-147-0)
- [Prerequisites for Using Query Attributes](#page-148-0)
- [Query Attribute Loadable Functions](#page-149-1)

### <span id="page-147-0"></span>**Defining and Accessing Query Attributes**

Applications that use the MySQL C API define query attributes by calling the [mysql\\_bind\\_param\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-bind-param.md) function. See [mysql\\_bind\\_param\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-bind-param.md). Other MySQL connectors may also provide query-attribute support. See the documentation for individual connectors.

The mysql client has a query\_attributes command that enables defining up to 32 pairs of attribute names and values. See Section 6.5.1.2, "mysql Client Commands".

Query attribute names are transmitted using the character set indicated by the character\_set\_client system variable.

To access query attributes within SQL statements for which attributes have been defined, install the query\_attributes component as described in [Prerequisites for Using Query Attributes.](#page-148-0) The component implements a [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) loadable function that takes an attribute name argument and returns the attribute value as a string, or NULL if the attribute does not exist. See [Query Attribute Loadable Functions.](#page-149-1)

The following examples use the mysql client query\_attributes command to define attribute name/ value pairs, and the [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function to access attribute values by name.

This example defines two attributes named n1 and n2. The first SELECT shows how to retrieve those attributes, and also demonstrates that retrieving a nonexistent attribute (n3) returns NULL. The second SELECT shows that attributes do not persist across statements.

```
mysql> query_attributes n1 v1 n2 v2;
mysql> SELECT
 mysql_query_attribute_string('n1') AS 'attr 1',
 mysql_query_attribute_string('n2') AS 'attr 2',
 mysql_query_attribute_string('n3') AS 'attr 3';
+--------+--------+--------+
| attr 1 | attr 2 | attr 3 |
+--------+--------+--------+
| v1 | v2 | NULL |
+--------+--------+--------+
mysql> SELECT
 mysql_query_attribute_string('n1') AS 'attr 1',
```

```
 mysql_query_attribute_string('n2') AS 'attr 2';
+--------+--------+
| attr 1 | attr 2 |
+--------+--------+
| NULL | NULL |
+--------+--------+
```

As shown by the second SELECT statement, attributes defined prior to a given statement are available only to that statement and are cleared after the statement executes. To use an attribute value across multiple statements, assign it to a variable. The following example shows how to do this, and illustrates that attribute values are available in subsequent statements by means of the variables, but not by calling [mysql\\_query\\_attribute\\_string\(\)](#page-149-2):

```
mysql> query_attributes n1 v1 n2 v2;
mysql> SET
 @attr1 = mysql_query_attribute_string('n1'),
 @attr2 = mysql_query_attribute_string('n2');
mysql> SELECT
 @attr1, mysql_query_attribute_string('n1') AS 'attr 1',
 @attr2, mysql_query_attribute_string('n2') AS 'attr 2';
+--------+--------+--------+--------+
| @attr1 | attr 1 | @attr2 | attr 2 |
+--------+--------+--------+--------+
| v1 | NULL | v2 | NULL |
+--------+--------+--------+--------+
```

Attributes can also be saved for later use by storing them in a table:

```
mysql> CREATE TABLE t1 (c1 CHAR(20), c2 CHAR(20));
mysql> query_attributes n1 v1 n2 v2;
mysql> INSERT INTO t1 (c1, c2) VALUES(
 mysql_query_attribute_string('n1'),
 mysql_query_attribute_string('n2')
 );
mysql> SELECT * FROM t1;
+------+------+
| c1 | c2 |
+------+------+
| v1 | v2 |
+------+------+
```

Query attributes are subject to these limitations and restrictions:

- If multiple attribute-definition operations occur prior to sending a statement to the server for execution, the most recent definition operation applies and replaces attributes defined in earlier operations.
- If multiple attributes are defined with the same name, attempts to retrieve the attribute value have an undefined result.
- An attribute defined with an empty name cannot be retrieved by name.
- Attributes are not available to statements prepared with PREPARE.
- The [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function cannot be used in DDL statements.
- Attributes are not replicated. Statements that invoke the [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function will not get the same value on all servers.

# <span id="page-148-0"></span>**Prerequisites for Using Query Attributes**

To access query attributes within SQL statements for which attributes have been defined, the query\_attributes component must be installed. Do so using this statement:

```
INSTALL COMPONENT "file://component_query_attributes";
```

Component installation is a one-time operation that need not be done per server startup. INSTALL COMPONENT loads the component, and also registers it in the mysql.component system table to cause it to be loaded during subsequent server startups.

The query\_attributes component accesses query attributes to implement a [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function. See Section 7.5.4, "Query Attribute Components".

To uninstall the query\_attributes component, use this statement:

```
UNINSTALL COMPONENT "file://component_query_attributes";
```

UNINSTALL COMPONENT unloads the component, and unregisters it from the mysql.component system table to cause it not to be loaded during subsequent server startups.

Because installing and uninstalling the query\_attributes component installs and uninstalls the [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function that the component implements, it is not necessary to use CREATE FUNCTION or DROP FUNCTION to do so.

### <span id="page-149-2"></span><span id="page-149-1"></span>**Query Attribute Loadable Functions**

• [mysql\\_query\\_attribute\\_string\(](#page-149-2)name)

Applications can define attributes that apply to the next query sent to the server. The [mysql\\_query\\_attribute\\_string\(\)](#page-149-2) function returns an attribute value as a string, given the attribute name. This function enables a query to access and incorporate values of the attributes that apply to it.

[mysql\\_query\\_attribute\\_string\(\)](#page-149-2) is installed by installing the query\_attributes component. See [Section 11.6, "Query Attributes",](#page-146-0) which also discusses the purpose and use of query attributes.

#### Arguments:

• name: The attribute name.

#### Return value:

Returns the attribute value as a string for success, or NULL if the attribute does not exist.

#### Example:

The following example uses the mysql client query\_attributes command to define query attributes that can be retrieved by [mysql\\_query\\_attribute\\_string\(\)](#page-149-2). The SELECT shows that retrieving a nonexistent attribute (n3) returns NULL.

```
mysql> query_attributes n1 v1 n2 v2;
mysql> SELECT
 -> mysql_query_attribute_string('n1') AS 'attr 1',
 -> mysql_query_attribute_string('n2') AS 'attr 2',
 -> mysql_query_attribute_string('n3') AS 'attr 3';
+--------+--------+--------+
| attr 1 | attr 2 | attr 3 |
+--------+--------+--------+
| v1 | v2 | NULL |
+--------+--------+--------+
```

# <span id="page-149-0"></span>**11.7 Comments**

MySQL Server supports three comment styles:

• From a # character to the end of the line.

- From a -- sequence to the end of the line. In MySQL, the -- (double-dash) comment style requires the second dash to be followed by at least one whitespace or control character, such as a space or tab. This syntax differs slightly from standard SQL comment syntax, as discussed in Section 1.7.2.4, "'--' as the Start of a Comment".
- From a /\* sequence to the following \*/ sequence, as in the C programming language. This syntax enables a comment to extend over multiple lines because the beginning and closing sequences need not be on the same line.

The following example demonstrates all three comment styles:

```
mysql> SELECT 1+1; # This comment continues to the end of line
mysql> SELECT 1+1; -- This comment continues to the end of line
mysql> SELECT 1 /* this is an in-line comment */ + 1;
mysql> SELECT 1+
/*
this is a
multiple-line comment
*/
1;
```

Nested comments are not supported, and are deprecated; expect them to be removed in a future MySQL release. (Under some conditions, nested comments might be permitted, but usually are not, and users should avoid them.)

MySQL Server supports certain variants of C-style comments. These enable you to write code that includes MySQL extensions, but is still portable, by using comments of the following form:

```
/*! MySQL-specific code */
```

In this case, MySQL Server parses and executes the code within the comment as it would any other SQL statement, but other SQL servers should ignore the extensions. For example, MySQL Server recognizes the STRAIGHT\_JOIN keyword in the following statement, but other servers should not:

```
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

If you add a version number after the ! character, the syntax within the comment is executed only if the MySQL version is greater than or equal to the specified version number. The KEY\_BLOCK\_SIZE keyword in the following comment is executed only by servers from MySQL 5.1.10 or higher:

```
CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;
```

The version number uses the format Mmmrr, where M is a major version, mm is a two-digit minor version, and rr is a two-digit release number. For example: In a statement to be run only by a MySQL server version 8.4.8 or later, use 80408 in the comment.

In MySQL 8.4, the version number can also optionally be comprised of six digits in MMmmrr format, where MM is a two-digit major version, and mm and rr are the two-digit minor version and two-digit release numbers, respectively.

The version number should be followed by at least one whitespace character (or the end of the comment). If the comment begins with six digits followed by whitespace, this is interpreted as a sixdigit version number. Otherwise, if it begins with at least five digits, these are interpreted as a five-digit version number (and any remaining characters ignored for this purpose); if it begins with fewer than five digits, the comment is handled as a normal MySQL comment.

The comment syntax just described applies to how the mysqld server parses SQL statements. The mysql client program also performs some parsing of statements before sending them to the server. (It does this to determine statement boundaries within a multiple-statement input line.) For information about differences between the server and mysql client parsers, see Section 6.5.1.6, "mysql Client Tips".

Comments in /\*!12345 ... \*/ format are not stored on the server. If this format is used to comment stored programs, the comments are not retained in the program body.

Another variant of C-style comment syntax is used to specify optimizer hints. Hint comments include a + character following the /\* comment opening sequence. Example:

```
SELECT /*+ BKA(t1) */ FROM ... ;
```

For more information, see [Section 10.9.3, "Optimizer Hints".](#page-7-0)

The use of short-form mysql commands such as \C within multiple-line /\* ... \*/ comments is not supported. Short-form commands do work within single-line /\*! ... \*/ version comments, as do / \*+ ... \*/ optimizer-hint comments, which are stored in object definitions. If there is a concern that optimizer-hint comments may be stored in object definitions so that dump files when reloaded with mysql would result in execution of such commands, either invoke mysql with the --binary-mode option or use a reload client other than mysql.

# Chapter 12 Character Sets, Collations, Unicode

# **Table of Contents**

| 12.1 Character Sets and Collations in General 1924                      |      |
|-------------------------------------------------------------------------|------|
| 12.2 Character Sets and Collations in MySQL 1925                        |      |
| 12.2.1 Character Set Repertoire 1927                                    |      |
| 12.2.2 UTF-8 for Metadata 1929                                          |      |
| 12.3 Specifying Character Sets and Collations 1930                      |      |
| 12.3.1 Collation Naming Conventions 1930                                |      |
| 12.3.2 Server Character Set and Collation 1931                          |      |
| 12.3.3 Database Character Set and Collation 1932                        |      |
| 12.3.4 Table Character Set and Collation 1933                           |      |
| 12.3.5 Column Character Set and Collation 1934                          |      |
| 12.3.6 Character String Literal Character Set and Collation 1935        |      |
| 12.3.7 The National Character Set 1937                                  |      |
| 12.3.8 Character Set Introducers 1937                                   |      |
| 12.3.9 Examples of Character Set and Collation Assignment 1939          |      |
| 12.3.10 Compatibility with Other DBMSs 1940                             |      |
| 12.4 Connection Character Sets and Collations 1940                      |      |
| 12.5 Configuring Application Character Set and Collation 1945           |      |
| 12.6 Error Message Character Set 1947                                   |      |
| 12.7 Column Character Set Conversion 1948                               |      |
| 12.8 Collation Issues 1949                                              |      |
| 12.8.1 Using COLLATE in SQL Statements 1949                             |      |
| 12.8.2 COLLATE Clause Precedence 1950                                   |      |
| 12.8.3 Character Set and Collation Compatibility 1950                   |      |
| 12.8.4 Collation Coercibility in Expressions 1950                       |      |
| 12.8.5 The binary Collation Compared to _bin Collations                 | 1952 |
| 12.8.6 Examples of the Effect of Collation 1954                         |      |
| 12.8.7 Using Collation in INFORMATION_SCHEMA Searches 1955              |      |
| 12.9 Unicode Support 1957                                               |      |
| 12.9.1 The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding) 1959   |      |
| 12.9.2 The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding) 1960   |      |
|                                                                         |      |
| 12.9.3 The utf8 Character Set (Deprecated alias for utf8mb3)            | 1961 |
| 12.9.4 The ucs2 Character Set (UCS-2 Unicode Encoding) 1961             |      |
| 12.9.5 The utf16 Character Set (UTF-16 Unicode Encoding) 1961           |      |
| 12.9.6 The utf16le Character Set (UTF-16LE Unicode Encoding) 1962       |      |
| 12.9.7 The utf32 Character Set (UTF-32 Unicode Encoding) 1962           |      |
| 12.9.8 Converting Between 3-Byte and 4-Byte Unicode Character Sets 1962 |      |
| 12.10 Supported Character Sets and Collations 1965                      |      |
| 12.10.1 Unicode Character Sets 1965                                     |      |
| 12.10.2 West European Character Sets 1973                               |      |
| 12.10.3 Central European Character Sets 1974                            |      |
| 12.10.4 South European and Middle East Character Sets 1975              |      |
| 12.10.5 Baltic Character Sets 1976                                      |      |
| 12.10.6 Cyrillic Character Sets 1976                                    |      |
| 12.10.7 Asian Character Sets 1977                                       |      |
| 12.10.8 The Binary Character Set 1981                                   |      |
| 12.11 Restrictions on Character Sets 1982                               |      |
| 12.12 Setting the Error Message Language 1982                           |      |
| 12.13 Adding a Character Set 1983                                       |      |
| 12.13.1 Character Definition Arrays 1985                                |      |
| 12.13.2 String Collating Support for Complex Character Sets 1986        |      |
| 12.13.3 Multi-Byte Character Support for Complex Character Sets 1986    |      |
| 12.14 Adding a Collation to a Character Set                             | 1986 |

| 12.14.1 Collation Implementation Types 1987                      |  |
|------------------------------------------------------------------|--|
| 12.14.2 Choosing a Collation ID 1990                             |  |
| 12.14.3 Adding a Simple Collation to an 8-Bit Character Set 1991 |  |
| 12.14.4 Adding a UCA Collation to a Unicode Character Set 1992   |  |
| 12.15 Character Set Configuration 1998                           |  |
| 12.16 MySQL Server Locale Support 1999                           |  |

MySQL includes character set support that enables you to store data using a variety of character sets and perform comparisons according to a variety of collations. The default MySQL server character set and collation are utf8mb4 and utf8mb4\_0900\_ai\_ci, but you can specify character sets at the server, database, table, column, and string literal levels. To maximize interoperability and futureproofing of your data and applications, we recommend that you use the utf8mb4 character set whenever possible.

![](_page_153_Picture_3.jpeg)

#### **Note**

UTF8 is a deprecated synonym for utf8mb3, and you should expect it to be removed in a future version of MySQL. Specify utfmb3 or (preferably) utfmb4 instead.

This chapter discusses the following topics:

- What are character sets and collations?
- The multiple-level default system for character set assignment.
- Syntax for specifying character sets and collations.
- Affected functions and operations.
- Unicode support.
- The character sets and collations that are available, with notes.
- Selecting the language for error messages.
- Selecting the locale for day and month names.

Character set issues affect not only data storage, but also communication between client programs and the MySQL server. If you want the client program to communicate with the server using a character set different from the default, you need to indicate which one. For example, to use the latin1 Unicode character set, issue this statement after connecting to the server:

```
SET NAMES 'latin1';
```

For more information about configuring character sets for application use and character set-related issues in client/server communication, see [Section 12.5, "Configuring Application Character Set and](#page-174-0) [Collation"](#page-174-0), and [Section 12.4, "Connection Character Sets and Collations"](#page-169-1).

# <span id="page-153-0"></span>**12.1 Character Sets and Collations in General**

A character set is a set of symbols and encodings. A collation is a set of rules for comparing characters in a character set. Let's make the distinction clear with an example of an imaginary character set.

Suppose that we have an alphabet with four letters: A, B, a, b. We give each letter a number: A = 0, B = 1, a = 2, b = 3. The letter A is a symbol, the number 0 is the encoding for A, and the combination of all four letters and their encodings is a character set.

Suppose that we want to compare two string values, A and B. The simplest way to do this is to look at the encodings: 0 for A and 1 for B. Because 0 is less than 1, we say A is less than B. What we've just

done is apply a collation to our character set. The collation is a set of rules (only one rule in this case): "compare the encodings." We call this simplest of all possible collations a binary collation.

But what if we want to say that the lowercase and uppercase letters are equivalent? Then we would have at least two rules: (1) treat the lowercase letters a and b as equivalent to A and B; (2) then compare the encodings. We call this a case-insensitive collation. It is a little more complex than a binary collation.

In real life, most character sets have many characters: not just A and B but whole alphabets, sometimes multiple alphabets or eastern writing systems with thousands of characters, along with many special symbols and punctuation marks. Also in real life, most collations have many rules, not just for whether to distinguish lettercase, but also for whether to distinguish accents (an "accent" is a mark attached to a character as in German Ö), and for multiple-character mappings (such as the rule that Ö = OE in one of the two German collations).

MySQL can do these things for you:

- Store strings using a variety of character sets.
- Compare strings using a variety of collations.
- Mix strings with different character sets or collations in the same server, the same database, or even the same table.
- Enable specification of character set and collation at any level.

To use these features effectively, you must know what character sets and collations are available, how to change the defaults, and how they affect the behavior of string operators and functions.

# <span id="page-154-0"></span>**12.2 Character Sets and Collations in MySQL**

MySQL Server supports multiple character sets, including several Unicode character sets. To display the available character sets, use the INFORMATION\_SCHEMA CHARACTER\_SETS table or the SHOW CHARACTER SET statement. A partial listing follows. For more complete information, see [Section 12.10, "Supported Character Sets and Collations"](#page-194-0).

```
mysql> SHOW CHARACTER SET;
+----------+---------------------------------+---------------------+--------+
| Charset | Description | Default collation | Maxlen |
+----------+---------------------------------+---------------------+--------+
| big5 | Big5 Traditional Chinese | big5_chinese_ci | 2 |
| binary | Binary pseudo charset | binary | 1 |
...
| latin1 | cp1252 West European | latin1_swedish_ci | 1 |
...
| ucs2 | UCS-2 Unicode | ucs2_general_ci | 2 |
...
| utf8mb3 | UTF-8 Unicode | utf8mb3_general_ci | 3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_0900_ai_ci | 4 |
...
```

By default, the SHOW CHARACTER SET statement displays all available character sets. It takes an optional LIKE or WHERE clause that indicates which character set names to match. The following example shows some of the Unicode character sets (those based on Unicode Transformation Format):

```
mysql> SHOW CHARACTER SET LIKE 'utf%';
+---------+------------------+--------------------+--------+
| Charset | Description | Default collation | Maxlen |
+---------+------------------+--------------------+--------+
| utf16 | UTF-16 Unicode | utf16_general_ci | 4 |
| utf16le | UTF-16LE Unicode | utf16le_general_ci | 4 |
| utf32 | UTF-32 Unicode | utf32_general_ci | 4 |
| utf8mb3 | UTF-8 Unicode | utf8mb3_general_ci | 3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_0900_ai_ci | 4 |
+---------+------------------+--------------------+--------+
```

A given character set always has at least one collation, and most character sets have several. To list the display collations for a character set, use the INFORMATION\_SCHEMA COLLATIONS table or the SHOW COLLATION statement.

By default, the SHOW COLLATION statement displays all available collations. It takes an optional LIKE or WHERE clause that indicates which collation names to display. For example, to see the collations for the default character set, utf8mb4, use this statement:

| Collation                                        |                                    |  |              |      | ++++++++<br>  Charset   Id   Default   Compiled   Sortlen   Pad_attribute |
|--------------------------------------------------|------------------------------------|--|--------------|------|---------------------------------------------------------------------------|
| ++++++++                                         |                                    |  |              |      |                                                                           |
| utf8mb4_0900_ai_ci                               | utf8mb4   255   Yes                |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_0900_as_ci                               | utf8mb4   305                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_0900_as_cs                               | utf8mb4   278                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_0900_bin                                 | utf8mb4   309                      |  | Yes          |      | 1   NO PAD                                                                |
| utf8mb4_bin                                      | utf8mb4   46                       |  | Yes          |      | 1   PAD SPACE                                                             |
| utf8mb4_croatian_ci                              | utf8mb4   245                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_cs_0900_ai_ci                            | utf8mb4   266                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_cs_0900_as_cs                            | utf8mb4   289                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_czech_ci                                 | utf8mb4   234                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_danish_ci                                | utf8mb4   235                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_da_0900_ai_ci                            | utf8mb4   267                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_da_0900_as_cs                            | utf8mb4   290                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_de_pb_0900_ai_ci                         | utf8mb4   256                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_de_pb_0900_as_cs                         | utf8mb4   279                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_eo_0900_ai_ci                            | utf8mb4   273                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_eo_0900_as_cs                            | utf8mb4   296                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_esperanto_ci                             | utf8mb4   241                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_estonian_ci                              | utf8mb4   230                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_es_0900_ai_ci                            | utf8mb4   263                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_es_0900_as_cs                            | utf8mb4   286                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_es_trad_0900_ai_ci   utf8mb4   270       |                                    |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_es_trad_0900_as_cs   utf8mb4   293       |                                    |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_et_0900_ai_ci<br>  utf8mb4_et_0900_as_cs | utf8mb4   262  <br>  utf8mb4   285 |  | Yes<br>  Yes | <br> | 0   NO PAD<br>0   NO PAD                                                  |
| utf8mb4_general_ci                               | utf8mb4   45                       |  | Yes          |      | 1   PAD SPACE                                                             |
| utf8mb4_german2_ci                               | utf8mb4   244                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_hr_0900_ai_ci                            | utf8mb4   275                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_hr_0900_as_cs                            | utf8mb4   298                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_hungarian_ci                             | utf8mb4   242                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_hu_0900_ai_ci                            | utf8mb4   274                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_hu_0900_as_cs                            | utf8mb4   297                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_icelandic_ci                             | utf8mb4   225                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_is_0900_ai_ci                            | utf8mb4   257                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_is_0900_as_cs                            | utf8mb4   280                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_ja_0900_as_cs                            | utf8mb4   303                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_ja_0900_as_cs_ks                         | utf8mb4   304                      |  | Yes          |      | 24   NO PAD                                                               |
| utf8mb4_latvian_ci                               | utf8mb4   226                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_la_0900_ai_ci                            | utf8mb4   271                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_la_0900_as_cs                            | utf8mb4   294                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_lithuanian_ci                            | utf8mb4   236                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_lt_0900_ai_ci                            | utf8mb4   268                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_lt_0900_as_cs                            | utf8mb4   291                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_lv_0900_ai_ci                            | utf8mb4   258                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_lv_0900_as_cs                            | utf8mb4   281                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_persian_ci                               | utf8mb4   240                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_pl_0900_ai_ci                            | utf8mb4   261                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_pl_0900_as_cs                            | utf8mb4   284                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_polish_ci                                | utf8mb4   229                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_romanian_ci                              | utf8mb4   227                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_roman_ci                                 | utf8mb4   239                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_ro_0900_ai_ci                            | utf8mb4   259                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_ro_0900_as_cs                            | utf8mb4   282                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_ru_0900_ai_ci                            | utf8mb4   306                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_ru_0900_as_cs                            | utf8mb4   307                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_sinhala_ci                               | utf8mb4   243                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_sk_0900_ai_ci                            | utf8mb4   269                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_sk_0900_as_cs                            | utf8mb4   292                      |  | Yes          |      | 0   NO PAD                                                                |
| utf8mb4_slovak_ci                                | utf8mb4   237                      |  | Yes          |      | 8   PAD SPACE                                                             |
| utf8mb4_slovenian_ci                             | utf8mb4   228                      |  | Yes          |      | 8   PAD SPACE                                                             |

| utf8mb4_sl_0900_ai_ci  | utf8mb4   260 | Yes<br> | 0   NO PAD    |  |
|------------------------|---------------|---------|---------------|--|
| utf8mb4_sl_0900_as_cs  | utf8mb4   283 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_spanish2_ci    | utf8mb4   238 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_spanish_ci     | utf8mb4   231 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_sv_0900_ai_ci  | utf8mb4   264 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_sv_0900_as_cs  | utf8mb4   287 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_swedish_ci     | utf8mb4   232 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_tr_0900_ai_ci  | utf8mb4   265 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_tr_0900_as_cs  | utf8mb4   288 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_turkish_ci     | utf8mb4   233 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_unicode_520_ci | utf8mb4   246 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_unicode_ci     | utf8mb4   224 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_vietnamese_ci  | utf8mb4   247 | Yes<br> | 8   PAD SPACE |  |
| utf8mb4_vi_0900_ai_ci  | utf8mb4   277 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_vi_0900_as_cs  | utf8mb4   300 | Yes<br> | 0   NO PAD    |  |
| utf8mb4_zh_0900_as_cs  | utf8mb4   308 | Yes<br> | 0   NO PAD    |  |
| ++++++++               |               |         |               |  |

For more information about those collations, see [Section 12.10.1, "Unicode Character Sets".](#page-194-1)

Collations have these general characteristics:

- Two different character sets cannot have the same collation.
- Each character set has a default collation. For example, the default collations for utf8mb4 and latin1 are utf8mb4\_0900\_ai\_ci and latin1\_swedish\_ci, respectively. The INFORMATION\_SCHEMA CHARACTER\_SETS table and the SHOW CHARACTER SET statement indicate the default collation for each character set. The INFORMATION\_SCHEMA COLLATIONS table and the SHOW COLLATION statement have a column that indicates for each collation whether it is the default for its character set (Yes if so, empty if not).
- Collation names start with the name of the character set with which they are associated, generally followed by one or more suffixes indicating other collation characteristics. For additional information about naming conventions, see [Section 12.3.1, "Collation Naming Conventions".](#page-159-1)

When a character set has multiple collations, it might not be clear which collation is most suitable for a given application. To avoid choosing an inappropriate collation, perform some comparisons with representative data values to make sure that a given collation sorts values the way you expect.

# <span id="page-156-0"></span>**12.2.1 Character Set Repertoire**

The repertoire of a character set is the collection of characters in the set.

String expressions have a repertoire attribute, which can have two values:

- ASCII: The expression can contain only ASCII characters; that is, characters in the Unicode range U +0000 to U+007F.
- UNICODE: The expression can contain characters in the Unicode range U+0000 to U+10FFFF. This includes characters in the Basic Multilingual Plane (BMP) range (U+0000 to U+FFFF) and supplementary characters outside the BMP range (U+10000 to U+10FFFF).

The ASCII range is a subset of UNICODE range, so a string with ASCII repertoire can be converted safely without loss of information to the character set of any string with UNICODE repertoire. It can also be converted safely to any character set that is a superset of the ascii character set. (All MySQL character sets are supersets of ascii with the exception of swe7, which reuses some punctuation characters for Swedish accented characters.)

The use of repertoire enables character set conversion in expressions for many cases where MySQL would otherwise return an "illegal mix of collations" error when the rules for collation coercibility are insufficient to resolve ambiguities. (For information about coercibility, see [Section 12.8.4, "Collation](#page-179-2) [Coercibility in Expressions"](#page-179-2).)

The following discussion provides examples of expressions and their repertoires, and describes how the use of repertoire changes string expression evaluation:

• The repertoire for a string constant depends on string content and may differ from the repertoire of the string character set. Consider these statements:

```
SET NAMES utf8mb4; SELECT 'abc';
SELECT _utf8mb4'def';
```

Although the character set is utf8mb4 in each of the preceding cases, the strings do not actually contain any characters outside the ASCII range, so their repertoire is ASCII rather than UNICODE.

• A column having the ascii character set has ASCII repertoire because of its character set. In the following table, c1 has ASCII repertoire:

```
CREATE TABLE t1 (c1 CHAR(1) CHARACTER SET ascii);
```

The following example illustrates how repertoire enables a result to be determined in a case where an error occurs without repertoire:

```
CREATE TABLE t1 (
 c1 CHAR(1) CHARACTER SET latin1,
 c2 CHAR(1) CHARACTER SET ascii
);
INSERT INTO t1 VALUES ('a','b');
SELECT CONCAT(c1,c2) FROM t1;
```

Without repertoire, this error occurs:

```
ERROR 1267 (HY000): Illegal mix of collations (latin1_swedish_ci,IMPLICIT)
and (ascii_general_ci,IMPLICIT) for operation 'concat'
```

Using repertoire, subset to superset (ascii to latin1) conversion can occur and a result is returned:

```
+---------------+
| CONCAT(c1,c2) |
+---------------+
| ab |
+---------------+
```

- Functions with one string argument inherit the repertoire of their argument. The result of UPPER(\_utf8mb4'abc') has ASCII repertoire because its argument has ASCII repertoire. (Despite the \_utf8mb4 introducer, the string 'abc' contains no characters outside the ASCII range.)
- For functions that return a string but do not have string arguments and use character\_set\_connection as the result character set, the result repertoire is ASCII if character\_set\_connection is ascii, and UNICODE otherwise:

```
FORMAT(numeric_column, 4);
```

Use of repertoire changes how MySQL evaluates the following example:

```
SET NAMES ascii;
CREATE TABLE t1 (a INT, b VARCHAR(10) CHARACTER SET latin1);
INSERT INTO t1 VALUES (1,'b');
SELECT CONCAT(FORMAT(a, 4), b) FROM t1;
```

Without repertoire, this error occurs:

```
ERROR 1267 (HY000): Illegal mix of collations (ascii_general_ci,COERCIBLE)
and (latin1_swedish_ci,IMPLICIT) for operation 'concat'
```

With repertoire, a result is returned:

```
+-------------------------+
| CONCAT(FORMAT(a, 4), b) |
+-------------------------+
| 1.0000b |
```

+-------------------------+

• Functions with two or more string arguments use the "widest" argument repertoire for the result repertoire, where UNICODE is wider than ASCII. Consider the following CONCAT() calls:

```
CONCAT(_ucs2 X'0041', _ucs2 X'0042')
CONCAT(_ucs2 X'0041', _ucs2 X'00C2')
```

For the first call, the repertoire is ASCII because both arguments are within the ASCII range. For the second call, the repertoire is UNICODE because the second argument is outside the ASCII range.

• The repertoire for function return values is determined based on the repertoire of only those arguments that affect the result's character set and collation.

```
IF(column1 < column2, 'smaller', 'greater')
```

The result repertoire is ASCII because the two string arguments (the second argument and the third argument) both have ASCII repertoire. The first argument does not matter for the result repertoire, even if the expression uses string values.

### <span id="page-158-0"></span>**12.2.2 UTF-8 for Metadata**

Metadata is "the data about the data." Anything that describes the database—as opposed to being the contents of the database—is metadata. Thus column names, database names, user names, version names, and most of the string results from SHOW are metadata. This is also true of the contents of tables in INFORMATION\_SCHEMA because those tables by definition contain information about database objects.

Representation of metadata must satisfy these requirements:

- All metadata must be in the same character set. Otherwise, neither the SHOW statements nor SELECT statements for tables in INFORMATION\_SCHEMA would work properly because different rows in the same column of the results of these operations would be in different character sets.
- Metadata must include all characters in all languages. Otherwise, users would not be able to name columns and tables using their own languages.

To satisfy both requirements, MySQL stores metadata in a Unicode character set, namely UTF-8. This does not cause any disruption if you never use accented or non-Latin characters. But if you do, you should be aware that metadata is in UTF-8.

The metadata requirements mean that the return values of the USER(), CURRENT\_USER(), SESSION\_USER(), SYSTEM\_USER(), DATABASE(), and VERSION() functions have the UTF-8 character set by default.

The server sets the character\_set\_system system variable to the name of the metadata character set:

```
mysql> SHOW VARIABLES LIKE 'character_set_system';
+----------------------+---------+
| Variable_name | Value |
+----------------------+---------+
| character_set_system | utf8mb3 |
+----------------------+---------+
```

Storage of metadata using Unicode does not mean that the server returns headers of columns and the results of DESCRIBE functions in the character\_set\_system character set by default. When you use SELECT column1 FROM t, the name column1 itself is returned from the server to the client in the character set determined by the value of the character\_set\_results system variable, which has a default value of utf8mb4. If you want the server to pass metadata results back in a different character set, use the SET NAMES statement to force the server to perform character set conversion. SET NAMES sets the character\_set\_results and other related system variables. (See [Section 12.4, "Connection Character Sets and Collations"](#page-169-1).) Alternatively, a client program can perform

the conversion after receiving the result from the server. It is more efficient for the client to perform the conversion, but this option is not always available for all clients.

If character\_set\_results is set to NULL, no conversion is performed and the server returns metadata using its original character set (the set indicated by character\_set\_system).

Error messages returned from the server to the client are converted to the client character set automatically, as with metadata.

If you are using (for example) the USER() function for comparison or assignment within a single statement, don't worry. MySQL performs some automatic conversion for you.

```
SELECT * FROM t1 WHERE USER() = latin1_column;
```

This works because the contents of latin1\_column are automatically converted to UTF-8 before the comparison.

```
INSERT INTO t1 (latin1_column) SELECT USER();
```

This works because the contents of USER() are automatically converted to latin1 before the assignment.

Although automatic conversion is not in the SQL standard, the standard does say that every character set is (in terms of supported characters) a "subset" of Unicode. Because it is a well-known principle that "what applies to a superset can apply to a subset," we believe that a collation for Unicode can apply for comparisons with non-Unicode strings. For more information about coercion of strings, see [Section 12.8.4, "Collation Coercibility in Expressions".](#page-179-2)

# <span id="page-159-0"></span>**12.3 Specifying Character Sets and Collations**

There are default settings for character sets and collations at four levels: server, database, table, and column. The description in the following sections may appear complex, but it has been found in practice that multiple-level defaulting leads to natural and obvious results.

CHARACTER SET is used in clauses that specify a character set. CHARSET can be used as a synonym for CHARACTER SET.

Character set issues affect not only data storage, but also communication between client programs and the MySQL server. If you want the client program to communicate with the server using a character set different from the default, you need to indicate which one. For example, to use the latin1 Unicode character set, issue this statement after connecting to the server:

```
SET NAMES 'latin1';
```

For more information about character set-related issues in client/server communication, see [Section 12.4, "Connection Character Sets and Collations"](#page-169-1).

# <span id="page-159-1"></span>**12.3.1 Collation Naming Conventions**

MySQL collation names follow these conventions:

- A collation name starts with the name of the character set with which it is associated, generally followed by one or more suffixes indicating other collation characteristics. For example, utf8mb4\_0900\_ai\_ci and latin1\_swedish\_ci are collations for the utf8mb4 and latin1 character sets, respectively. The binary character set has a single collation, also named binary, with no suffixes.
- A language-specific collation includes a locale code or language name. For example, utf8mb4\_tr\_0900\_ai\_ci and utf8mb4\_hu\_0900\_ai\_ci sort characters for the utf8mb4 character set using the rules of Turkish and Hungarian, respectively. utf8mb4\_turkish\_ci and utf8mb4\_hungarian\_ci are similar but based on a less recent version of the Unicode Collation Algorithm.

• Collation suffixes indicate whether a collation is case-sensitive, accent-sensitive, or kana-sensitive (or some combination thereof), or binary. The following table shows the suffixes used to indicate these characteristics.

**Table 12.1 Collation Suffix Meanings**

| Suffix | Meaning            |
|--------|--------------------|
| _ai    | Accent-insensitive |
| _as    | Accent-sensitive   |
| _ci    | Case-insensitive   |
| _cs    | Case-sensitive     |
| _ks    | Kana-sensitive     |
| _bin   | Binary             |

For nonbinary collation names that do not specify accent sensitivity, it is determined by case sensitivity. If a collation name does not contain \_ai or \_as, \_ci in the name implies \_ai and \_cs in the name implies \_as. For example, latin1\_general\_ci is explicitly case-insensitive and implicitly accent-insensitive, latin1\_general\_cs is explicitly case-sensitive and implicitly accentsensitive, and utf8mb4\_0900\_ai\_ci is explicitly case-insensitive and accent-insensitive.

For Japanese collations, the \_ks suffix indicates that a collation is kana-sensitive; that is, it distinguishes Katakana characters from Hiragana characters. Japanese collations without the \_ks suffix are not kana-sensitive and treat Katakana and Hiragana characters equal for sorting.

For the binary collation of the binary character set, comparisons are based on numeric byte values. For the \_bin collation of a nonbinary character set, comparisons are based on numeric character code values, which differ from byte values for multibyte characters. For information about the differences between the binary collation of the binary character set and the \_bin collations of nonbinary character sets, see [Section 12.8.5, "The binary Collation Compared to \\_bin Collations".](#page-181-0)

- Collation names for Unicode character sets may include a version number to indicate the version of the Unicode Collation Algorithm (UCA) on which the collation is based. UCA-based collations without a version number in the name use the version-4.0.0 UCA weight keys. For example:
  - utf8mb4\_0900\_ai\_ci is based on UCA 9.0.0 weight keys ([http://www.unicode.org/Public/](http://www.unicode.org/Public/UCA/9.0.0/allkeys.txt) [UCA/9.0.0/allkeys.txt\)](http://www.unicode.org/Public/UCA/9.0.0/allkeys.txt).
  - utf8mb4\_unicode\_520\_ci is based on UCA 5.2.0 weight keys ([http://www.unicode.org/Public/](http://www.unicode.org/Public/UCA/5.2.0/allkeys.txt) [UCA/5.2.0/allkeys.txt\)](http://www.unicode.org/Public/UCA/5.2.0/allkeys.txt).
  - utf8mb4\_unicode\_ci (with no version named) is based on UCA 4.0.0 weight keys [\(http://](http://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt) [www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt\)](http://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt).
- For Unicode character sets, the xxx\_general\_mysql500\_ci collations preserve the pre-5.1.24 ordering of the original xxx\_general\_ci collations and permit upgrades for tables created before MySQL 5.1.24 (Bug #27877).

### <span id="page-160-0"></span>**12.3.2 Server Character Set and Collation**

MySQL Server has a server character set and a server collation. By default, these are utf8mb4 and utf8mb4\_0900\_ai\_ci, but they can be set explicitly at server startup on the command line or in an option file and changed at runtime.

Initially, the server character set and collation depend on the options that you use when you start mysqld. You can use --character-set-server for the character set. Along with it, you can add --collation-server for the collation. If you don't specify a character set, that is the same as saying --character-set-server=utf8mb4. If you specify only a character set (for example, utf8mb4) but not a collation, that is the same as saying --character-set-server=utf8mb4

--collation-server=utf8mb4\_0900\_ai\_ci because utf8mb4\_0900\_ai\_ci is the default collation for utf8mb4. Therefore, the following three commands all have the same effect:

```
mysqld
mysqld --character-set-server=utf8mb4
mysqld --character-set-server=utf8mb4 \
 --collation-server=utf8mb4_0900_ai_ci
```

One way to change the settings is by recompiling. To change the default server character set and collation when building from sources, use the DEFAULT\_CHARSET and DEFAULT\_COLLATION options for CMake. For example:

```
cmake . -DDEFAULT_CHARSET=latin1
```

#### Or:

```
cmake . -DDEFAULT_CHARSET=latin1 \
 -DDEFAULT_COLLATION=latin1_german1_ci
```

Both mysqld and CMake verify that the character set/collation combination is valid. If not, each program displays an error message and terminates.

The server character set and collation are used as default values if the database character set and collation are not specified in CREATE DATABASE statements. They have no other purpose.

The current server character set and collation can be determined from the values of the character\_set\_server and collation\_server system variables. These variables can be changed at runtime.

# <span id="page-161-0"></span>**12.3.3 Database Character Set and Collation**

Every database has a database character set and a database collation. The CREATE DATABASE and ALTER DATABASE statements have optional clauses for specifying the database character set and collation:

```
CREATE DATABASE db_name
 [[DEFAULT] CHARACTER SET charset_name]
 [[DEFAULT] COLLATE collation_name]
ALTER DATABASE db_name
 [[DEFAULT] CHARACTER SET charset_name]
 [[DEFAULT] COLLATE collation_name]
```

The keyword SCHEMA can be used instead of DATABASE.

The CHARACTER SET and COLLATE clauses make it possible to create databases with different character sets and collations on the same MySQL server.

Database options are stored in the data dictionary and can be examined by checking the Information Schema SCHEMATA table.

#### Example:

```
CREATE DATABASE db_name CHARACTER SET latin1 COLLATE latin1_swedish_ci;
```

MySQL chooses the database character set and database collation in the following manner:

- If both CHARACTER SET charset\_name and COLLATE collation\_name are specified, character set charset\_name and collation collation\_name are used.
- If CHARACTER SET charset\_name is specified without COLLATE, character set charset\_name and its default collation are used. To see the default collation for each character set, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table.
- If COLLATE collation\_name is specified without CHARACTER SET, the character set associated with collation\_name and collation collation\_name are used.

• Otherwise (neither CHARACTER SET nor COLLATE is specified), the server character set and server collation are used.

The character set and collation for the default database can be determined from the values of the character\_set\_database and collation\_database system variables. The server sets these variables whenever the default database changes. If there is no default database, the variables have the same value as the corresponding server-level system variables, character\_set\_server and collation\_server.

To see the default character set and collation for a given database, use these statements:

```
USE db_name;
SELECT @@character_set_database, @@collation_database;
```

Alternatively, to display the values without changing the default database:

```
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

The database character set and collation affect these aspects of server operation:

- For CREATE TABLE statements, the database character set and collation are used as default values for table definitions if the table character set and collation are not specified. To override this, provide explicit CHARACTER SET and COLLATE table options.
- For LOAD DATA statements that include no CHARACTER SET clause, the server uses the character set indicated by the character\_set\_database system variable to interpret the information in the file. To override this, provide an explicit CHARACTER SET clause.
- For stored routines (procedures and functions), the database character set and collation in effect at routine creation time are used as the character set and collation of character data parameters for which the declaration includes no CHARACTER SET or a COLLATE attribute. To override this, provide CHARACTER SET and COLLATE explicitly.

### <span id="page-162-0"></span>**12.3.4 Table Character Set and Collation**

Every table has a table character set and a table collation. The CREATE TABLE and ALTER TABLE statements have optional clauses for specifying the table character set and collation:

```
CREATE TABLE tbl_name (column_list)
 [[DEFAULT] CHARACTER SET charset_name]
 [COLLATE collation_name]]
ALTER TABLE tbl_name
 [[DEFAULT] CHARACTER SET charset_name]
 [COLLATE collation_name]
```

#### Example:

```
CREATE TABLE t1 ( ... )
CHARACTER SET latin1 COLLATE latin1_danish_ci;
```

MySQL chooses the table character set and collation in the following manner:

- If both CHARACTER SET charset\_name and COLLATE collation\_name are specified, character set charset\_name and collation collation\_name are used.
- If CHARACTER SET charset\_name is specified without COLLATE, character set charset\_name and its default collation are used. To see the default collation for each character set, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table.
- If COLLATE collation\_name is specified without CHARACTER SET, the character set associated with collation\_name and collation collation\_name are used.
- Otherwise (neither CHARACTER SET nor COLLATE is specified), the database character set and collation are used.

The table character set and collation are used as default values for column definitions if the column character set and collation are not specified in individual column definitions. The table character set and collation are MySQL extensions; there are no such things in standard SQL.

# <span id="page-163-0"></span>**12.3.5 Column Character Set and Collation**

Every "character" column (that is, a column of type CHAR, VARCHAR, a TEXT type, or any synonym) has a column character set and a column collation. Column definition syntax for CREATE TABLE and ALTER TABLE has optional clauses for specifying the column character set and collation:

```
col_name {CHAR | VARCHAR | TEXT} (col_length)
 [CHARACTER SET charset_name]
 [COLLATE collation_name]
```

These clauses can also be used for ENUM and SET columns:

```
col_name {ENUM | SET} (val_list)
 [CHARACTER SET charset_name]
 [COLLATE collation_name]
```

#### Examples:

```
CREATE TABLE t1
(
 col1 VARCHAR(5)
 CHARACTER SET latin1
 COLLATE latin1_german1_ci
);
ALTER TABLE t1 MODIFY
 col1 VARCHAR(5)
 CHARACTER SET latin1
 COLLATE latin1_swedish_ci;
```

MySQL chooses the column character set and collation in the following manner:

• If both CHARACTER SET charset\_name and COLLATE collation\_name are specified, character set charset\_name and collation collation\_name are used.

```
CREATE TABLE t1
(
 col1 CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) CHARACTER SET latin1 COLLATE latin1_bin;
```

The character set and collation are specified for the column, so they are used. The column has character set utf8mb4 and collation utf8mb4\_unicode\_ci.

• If CHARACTER SET charset\_name is specified without COLLATE, character set charset\_name and its default collation are used.

```
CREATE TABLE t1
(
 col1 CHAR(10) CHARACTER SET utf8mb4
) CHARACTER SET latin1 COLLATE latin1_bin;
```

The character set is specified for the column, but the collation is not. The column has character set utf8mb4 and the default collation for utf8mb4, which is utf8mb4\_0900\_ai\_ci. To see the default collation for each character set, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table.

• If COLLATE collation\_name is specified without CHARACTER SET, the character set associated with collation\_name and collation collation\_name are used.

```
CREATE TABLE t1
(
 col1 CHAR(10) COLLATE utf8mb4_polish_ci
```

```
) CHARACTER SET latin1 COLLATE latin1_bin;
```

The collation is specified for the column, but the character set is not. The column has collation utf8mb4\_polish\_ci and the character set is the one associated with the collation, which is utf8mb4.

• Otherwise (neither CHARACTER SET nor COLLATE is specified), the table character set and collation are used.

```
CREATE TABLE t1
(
 col1 CHAR(10)
) CHARACTER SET latin1 COLLATE latin1_bin;
```

Neither the character set nor collation is specified for the column, so the table defaults are used. The column has character set latin1 and collation latin1\_bin.

The CHARACTER SET and COLLATE clauses are standard SQL.

If you use ALTER TABLE to convert a column from one character set to another, MySQL attempts to map the data values, but if the character sets are incompatible, there may be data loss.

# <span id="page-164-0"></span>**12.3.6 Character String Literal Character Set and Collation**

Every character string literal has a character set and a collation.

For the simple statement SELECT 'string', the string has the connection default character set and collation defined by the character\_set\_connection and collation\_connection system variables.

A character string literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name]'string' [COLLATE collation_name]
```

The \_charset\_name expression is formally called an introducer. It tells the parser, "the string that follows uses character set charset\_name." An introducer does not change the string to the introducer character set like CONVERT() would do. It does not change the string value, although padding may occur. The introducer is just a signal. See [Section 12.3.8, "Character Set Introducers".](#page-166-1)

#### Examples:

```
SELECT 'abc';
SELECT _latin1'abc';
SELECT _binary'abc';
SELECT _utf8mb4'abc' COLLATE utf8mb4_danish_ci;
```

Character set introducers and the COLLATE clause are implemented according to standard SQL specifications.

MySQL determines the character set and collation of a character string literal in the following manner:

- If both \_charset\_name and COLLATE collation\_name are specified, character set charset\_name and collation collation\_name are used. collation\_name must be a permitted collation for charset\_name.
- If \_charset\_name is specified but COLLATE is not specified, character set charset\_name and its default collation are used. To see the default collation for each character set, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table.
- If \_charset\_name is not specified but COLLATE collation\_name is specified, the connection default character set given by the character\_set\_connection system variable and collation collation\_name are used. collation\_name must be a permitted collation for the connection default character set.

• Otherwise (neither \_charset\_name nor COLLATE collation\_name is specified), the connection default character set and collation given by the character\_set\_connection and collation\_connection system variables are used.

#### Examples:

• A nonbinary string with latin1 character set and latin1\_german1\_ci collation:

```
SELECT _latin1'Müller' COLLATE latin1_german1_ci;
```

• A nonbinary string with utf8mb4 character set and its default collation (that is, utf8mb4\_0900\_ai\_ci):

```
SELECT _utf8mb4'Müller';
```

• A binary string with binary character set and its default collation (that is, binary):

```
SELECT _binary'Müller';
```

• A nonbinary string with the connection default character set and utf8mb4\_0900\_ai\_ci collation (fails if the connection character set is not utf8mb4):

```
SELECT 'Müller' COLLATE utf8mb4_0900_ai_ci;
```

• A string with the connection default character set and collation:

```
SELECT 'Müller';
```

An introducer indicates the character set for the following string, but does not change how the parser performs escape processing within the string. Escapes are always interpreted by the parser according to the character set given by character\_set\_connection.

The following examples show that escape processing occurs using character\_set\_connection even in the presence of an introducer. The examples use SET NAMES (which changes character\_set\_connection, as discussed in [Section 12.4, "Connection Character Sets and](#page-169-1) [Collations"](#page-169-1)), and display the resulting strings using the HEX() function so that the exact string contents can be seen.

#### Example 1:

```
mysql> SET NAMES latin1;
mysql> SELECT HEX('à\n'), HEX(_sjis'à\n');
+------------+-----------------+
| HEX('à\n') | HEX(_sjis'à\n') |
+------------+-----------------+
| E00A | E00A |
+------------+-----------------+
```

Here, à (hexadecimal value E0) is followed by \n, the escape sequence for newline. The escape sequence is interpreted using the character\_set\_connection value of latin1 to produce a literal newline (hexadecimal value 0A). This happens even for the second string. That is, the \_sjis introducer does not affect the parser's escape processing.

#### Example 2:

```
mysql> SET NAMES sjis;
mysql> SELECT HEX('à\n'), HEX(_latin1'à\n');
+------------+-------------------+
| HEX('à\n') | HEX(_latin1'à\n') |
+------------+-------------------+
| E05C6E | E05C6E |
+------------+-------------------+
```

Here, character\_set\_connection is sjis, a character set in which the sequence of à followed by \ (hexadecimal values 05 and 5C) is a valid multibyte character. Hence, the first two bytes of the string are interpreted as a single sjis character, and the \ is not interpreted as an escape character. The

following n (hexadecimal value 6E) is not interpreted as part of an escape sequence. This is true even for the second string; the \_latin1 introducer does not affect escape processing.

# <span id="page-166-0"></span>**12.3.7 The National Character Set**

Standard SQL defines NCHAR or NATIONAL CHAR as a way to indicate that a CHAR column should use some predefined character set. MySQL uses utf8 as this predefined character set. For example, these data type declarations are equivalent:

```
CHAR(10) CHARACTER SET utf8
NATIONAL CHARACTER(10)
NCHAR(10)
```

#### As are these:

```
VARCHAR(10) CHARACTER SET utf8
NATIONAL VARCHAR(10)
NVARCHAR(10)
NCHAR VARCHAR(10)
NATIONAL CHARACTER VARYING(10)
NATIONAL CHAR VARYING(10)
```

You can use N'literal' (or n'literal') to create a string in the national character set. These statements are equivalent:

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

MySQL 8.4 interprets the national character set as utf8mb3, which is now deprecated. Thus, using NATIONAL CHARACTER or one of its synonyms to define the character set for a database, table, or column raises a warning similar to this one:

```
NATIONAL/NCHAR/NVARCHAR implies the character set UTF8MB3, which will be
replaced by UTF8MB4 in a future release. Please consider using CHAR(x) CHARACTER
SET UTF8MB4 in order to be unambiguous.
```

### <span id="page-166-1"></span>**12.3.8 Character Set Introducers**

A character string literal, hexadecimal literal, or bit-value literal may have an optional character set introducer and COLLATE clause, to designate it as a string that uses a particular character set and collation:

```
[_charset_name] literal [COLLATE collation_name]
```

The \_charset\_name expression is formally called an introducer. It tells the parser, "the string that follows uses character set charset\_name." An introducer does not change the string to the introducer character set like CONVERT() would do. It does not change the string value, although padding may occur. The introducer is just a signal.

For character string literals, space between the introducer and the string is permitted but optional.

For character set literals, an introducer indicates the character set for the following string, but does not change how the parser performs escape processing within the string. Escapes are always interpreted by the parser according to the character set given by character\_set\_connection. For additional discussion and examples, see [Section 12.3.6, "Character String Literal Character Set and Collation".](#page-164-0)

#### Examples:

```
SELECT 'abc';
SELECT _latin1'abc';
SELECT _binary'abc';
SELECT _utf8mb4'abc' COLLATE utf8mb4_danish_ci;
SELECT _latin1 X'4D7953514C';
SELECT _utf8mb4 0x4D7953514C COLLATE utf8mb4_danish_ci;
```

```
SELECT _latin1 b'1000001';
SELECT _utf8mb4 0b1000001 COLLATE utf8mb4_danish_ci;
```

Character set introducers and the COLLATE clause are implemented according to standard SQL specifications.

Character string literals can be designated as binary strings by using the \_binary introducer. Hexadecimal literals and bit-value literals are binary strings by default, so \_binary is permitted, but normally unnecessary. \_binary may be useful to preserve a hexadecimal or bit literal as a binary string in contexts for which the literal is otherwise treated as a number. For example, bit operations permit numeric or binary string arguments in MySQL 8.4 and higher, but treat hexadecimal and bit literals as numbers by default. To explicitly specify binary string context for such literals, use a \_binary introducer for at least one of the arguments:

```
mysql> SET @v1 = X'000D' | X'0BC0';
mysql> SET @v2 = _binary X'000D' | X'0BC0';
mysql> SELECT HEX(@v1), HEX(@v2);
+----------+----------+
| HEX(@v1) | HEX(@v2) |
+----------+----------+
| BCD | 0BCD |
+----------+----------+
```

The displayed result appears similar for both bit operations, but the result without \_binary is a BIGINT value, whereas the result with \_binary is a binary string. Due to the difference in result types, the displayed values differ: High-order 0 digits are not displayed for the numeric result.

MySQL determines the character set and collation of a character string literal, hexadecimal literal, or bit-value literal in the following manner:

- If both \_charset\_name and COLLATE collation\_name are specified, character set charset\_name and collation collation\_name are used. collation\_name must be a permitted collation for charset\_name.
- If \_charset\_name is specified but COLLATE is not specified, character set charset\_name and its default collation are used. To see the default collation for each character set, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table.
- If \_charset\_name is not specified but COLLATE collation\_name is specified:
  - For a character string literal, the connection default character set given by the character\_set\_connection system variable and collation collation\_name are used. collation\_name must be a permitted collation for the connection default character set.
  - For a hexadecimal literal or bit-value literal, the only permitted collation is binary because these types of literals are binary strings by default.
- Otherwise (neither \_charset\_name nor COLLATE collation\_name is specified):
  - For a character string literal, the connection default character set and collation given by the character\_set\_connection and collation\_connection system variables are used.
  - For a hexadecimal literal or bit-value literal, the character set and collation are binary.

#### Examples:

• Nonbinary strings with latin1 character set and latin1\_german1\_ci collation:

```
SELECT _latin1'Müller' COLLATE latin1_german1_ci;
SELECT _latin1 X'0A0D' COLLATE latin1_german1_ci;
SELECT _latin1 b'0110' COLLATE latin1_german1_ci;
```

• Nonbinary strings with utf8mb4 character set and its default collation (that is, utf8mb4\_0900\_ai\_ci):

```
SELECT _utf8mb4'Müller';
SELECT _utf8mb4 X'0A0D';
SELECT _utf8mb4 b'0110';
```

• Binary strings with binary character set and its default collation (that is, binary):

```
SELECT _binary'Müller';
SELECT X'0A0D';
SELECT b'0110';
```

The hexadecimal literal and bit-value literal need no introducer because they are binary strings by default.

• A nonbinary string with the connection default character set and utf8mb4\_0900\_ai\_ci collation (fails if the connection character set is not utf8mb4):

```
SELECT 'Müller' COLLATE utf8mb4_0900_ai_ci;
```

This construction (COLLATE only) does not work for hexadecimal literals or bit literals because their character set is binary no matter the connection character set, and binary is not compatible with the utf8mb4\_0900\_ai\_ci collation. The only permitted COLLATE clause in the absence of an introducer is COLLATE binary.

• A string with the connection default character set and collation:

```
SELECT 'Müller';
```

# <span id="page-168-0"></span>**12.3.9 Examples of Character Set and Collation Assignment**

The following examples show how MySQL determines default character set and collation values.

#### **Example 1: Table and Column Definition**

```
CREATE TABLE t1
(
 c1 CHAR(10) CHARACTER SET latin1 COLLATE latin1_german1_ci
) DEFAULT CHARACTER SET latin2 COLLATE latin2_bin;
```

Here we have a column with a latin1 character set and a latin1\_german1\_ci collation. The definition is explicit, so that is straightforward. Notice that there is no problem with storing a latin1 column in a latin2 table.

#### **Example 2: Table and Column Definition**

```
CREATE TABLE t1
(
 c1 CHAR(10) CHARACTER SET latin1
) DEFAULT CHARACTER SET latin1 COLLATE latin1_danish_ci;
```

This time we have a column with a latin1 character set and a default collation. Although it might seem natural, the default collation is not taken from the table level. Instead, because the default collation for latin1 is always latin1\_swedish\_ci, column c1 has a collation of latin1\_swedish\_ci (not latin1\_danish\_ci).

#### **Example 3: Table and Column Definition**

```
CREATE TABLE t1
(
 c1 CHAR(10)
) DEFAULT CHARACTER SET latin1 COLLATE latin1_danish_ci;
```

We have a column with a default character set and a default collation. In this circumstance, MySQL checks the table level to determine the column character set and collation. Consequently, the character set for column c1 is latin1 and its collation is latin1\_danish\_ci.

#### **Example 4: Database, Table, and Column Definition**

```
CREATE DATABASE d1
 DEFAULT CHARACTER SET latin2 COLLATE latin2_czech_cs;
USE d1;
CREATE TABLE t1
(
 c1 CHAR(10)
);
```

We create a column without specifying its character set and collation. We're also not specifying a character set and a collation at the table level. In this circumstance, MySQL checks the database level to determine the table settings, which thereafter become the column settings.) Consequently, the character set for column c1 is latin2 and its collation is latin2\_czech\_cs.

# <span id="page-169-0"></span>**12.3.10 Compatibility with Other DBMSs**

For MaxDB compatibility these two statements are the same:

```
CREATE TABLE t1 (f1 CHAR(N) UNICODE);
CREATE TABLE t1 (f1 CHAR(N) CHARACTER SET ucs2);
```

Both the UNICODE attribute and the ucs2 character set are deprecated; you should expect them to be removed in a future version of MySQL.

# <span id="page-169-1"></span>**12.4 Connection Character Sets and Collations**

A "connection" is what a client program makes when it connects to the server, to begin a session within which it interacts with the server. The client sends SQL statements, such as queries, over the session connection. The server sends responses, such as result sets or error messages, over the connection back to the client.

- [Connection Character Set and Collation System Variables](#page-169-2)
- [Impermissible Client Character Sets](#page-170-0)
- [Client Program Connection Character Set Configuration](#page-171-0)
- [SQL Statements for Connection Character Set Configuration](#page-172-0)
- [Connection Character Set Error Handling](#page-173-0)

# <span id="page-169-2"></span>**Connection Character Set and Collation System Variables**

Several character set and collation system variables relate to a client's interaction with the server. Some of these have been mentioned in earlier sections:

- The character\_set\_server and collation\_server system variables indicate the server character set and collation. See [Section 12.3.2, "Server Character Set and Collation"](#page-160-0).
- The character\_set\_database and collation\_database system variables indicate the character set and collation of the default database. See [Section 12.3.3, "Database Character Set and](#page-161-0) [Collation"](#page-161-0).

Additional character set and collation system variables are involved in handling traffic for the connection between a client and the server. Every client has session-specific connection-related character set and collation system variables. These session system variable values are initialized at connect time, but can be changed within the session.

Several questions about character set and collation handling for client connections can be answered in terms of system variables:

• What character set are statements in when they leave the client?

The server takes the character\_set\_client system variable to be the character set in which statements are sent by the client.

![](_page_170_Picture_1.jpeg)

#### **Note**

Some character sets cannot be used as the client character set. See [Impermissible Client Character Sets.](#page-170-0)

• What character set should the server translate statements to after receiving them?

To determine this, the server uses the character\_set\_connection and collation\_connection system variables:

- The server converts statements sent by the client from character\_set\_client to character\_set\_connection. Exception: For string literals that have an introducer such as \_utf8mb4 or \_latin2, the introducer determines the character set. See [Section 12.3.8,](#page-166-1) ["Character Set Introducers"](#page-166-1).
- collation\_connection is important for comparisons of literal strings. For comparisons of strings with column values, collation\_connection does not matter because columns have their own collation, which has a higher collation precedence (see [Section 12.8.4, "Collation](#page-179-2) [Coercibility in Expressions"](#page-179-2)).
- What character set should the server translate query results to before shipping them back to the client?

The character\_set\_results system variable indicates the character set in which the server returns query results to the client. This includes result data such as column values, result metadata such as column names, and error messages.

To tell the server to perform no conversion of result sets or error messages, set character\_set\_results to NULL or binary:

```
SET character_set_results = NULL;
SET character_set_results = binary;
```

For more information about character sets and error messages, see [Section 12.6, "Error Message](#page-176-0) [Character Set"](#page-176-0).

To see the values of the character set and collation system variables that apply to the current session, use this statement:

```
SELECT * FROM performance_schema.session_variables
WHERE VARIABLE_NAME IN (
 'character_set_client', 'character_set_connection',
 'character_set_results', 'collation_connection'
) ORDER BY VARIABLE_NAME;
```

The following simpler statements also display the connection variables, but include other related variables as well. They can be useful to see all character set and collation system variables:

```
SHOW SESSION VARIABLES LIKE 'character\_set\_%';
SHOW SESSION VARIABLES LIKE 'collation\_%';
```

Clients can fine-tune the settings for these variables, or depend on the defaults (in which case, you can skip the rest of this section). If you do not use the defaults, you must change the character settings for each connection to the server.

# <span id="page-170-0"></span>**Impermissible Client Character Sets**

The character\_set\_client system variable cannot be set to certain character sets:

```
ucs2
utf16
utf16le
utf32
```

Attempting to use any of those character sets as the client character set produces an error:

```
mysql> SET character_set_client = 'ucs2';
ERROR 1231 (42000): Variable 'character_set_client'
can't be set to the value of 'ucs2'
```

The same error occurs if any of those character sets are used in the following contexts, all of which result in an attempt to set character\_set\_client to the named character set:

- The --default-character-set=charset\_name command option used by MySQL client programs such as mysql and mysqladmin.
- The SET NAMES 'charset\_name' statement.
- The SET CHARACTER SET 'charset\_name' statement.

# <span id="page-171-0"></span>**Client Program Connection Character Set Configuration**

When a client connects to the server, it indicates which character set it wants to use for communication with the server. (Actually, the client indicates the default collation for that character set, from which the server can determine the character set.) The server uses this information to set the character\_set\_client, character\_set\_results, character\_set\_connection system variables to the character set, and collation\_connection to the character set default collation. In effect, the server performs the equivalent of a SET NAMES operation.

If the server does not support the requested character set or collation, it falls back to using the server character set and collation to configure the connection. For additional detail about this fallback behavior, see [Connection Character Set Error Handling](#page-173-0).

The mysql, mysqladmin, mysqlcheck, mysqlimport, and mysqlshow client programs determine the default character set to use as follows:

- In the absence of other information, each client uses the compiled-in default character set, usually utf8mb4.
- Each client can autodetect which character set to use based on the operating system setting, such as the value of the LANG or LC\_ALL locale environment variable on Unix systems or the code page setting on Windows systems. For systems on which the locale is available from the OS, the client uses it to set the default character set rather than using the compiled-in default. For example, setting LANG to ru\_RU.KOI8-R causes the koi8r character set to be used. Thus, users can configure the locale in their environment for use by MySQL clients.

The OS character set is mapped to the closest MySQL character set if there is no exact match. If the client does not support the matching character set, it uses the compiled-in default. For example, utf8 and utf-8 map to utf8mb4, and ucs2 is not supported as a connection character set, so it maps to the compiled-in default.

C applications can use character set autodetection based on the OS setting by invoking [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) as follows before connecting to the server:

```
mysql_options(mysql,
 MYSQL_SET_CHARSET_NAME,
 MYSQL_AUTODETECT_CHARSET_NAME);
```

• Each client supports a --default-character-set option, which enables users to specify the character set explicitly to override whatever default the client otherwise determines.

![](_page_171_Picture_17.jpeg)

#### **Note**

Some character sets cannot be used as the client character set. Attempting to use them with --default-character-set produces an error. See [Impermissible Client Character Sets.](#page-170-0)

With the mysql client, to use a character set different from the default, you could explicitly execute a SET NAMES statement every time you connect to the server (see [Client Program Connection Character](#page-171-0) [Set Configuration](#page-171-0)). To accomplish the same result more easily, specify the character set in your option file. For example, the following option file setting changes the three connection-related character set system variables set to koi8r each time you invoke mysql:

```
[mysql]
default-character-set=koi8r
```

If you are using the mysql client with auto-reconnect enabled (which is not recommended), it is preferable to use the charset command rather than SET NAMES. For example:

```
mysql> charset koi8r
Charset changed
```

The charset command issues a SET NAMES statement, and also changes the default character set that mysql uses when it reconnects after the connection has dropped.

When configuration client programs, you must also consider the environment within which they execute. See [Section 12.5, "Configuring Application Character Set and Collation"](#page-174-0).

# <span id="page-172-0"></span>**SQL Statements for Connection Character Set Configuration**

After a connection has been established, clients can change the character set and collation system variables for the current session. These variables can be changed individually using SET statements, but two more convenient statements affect the connection-related character set system variables as a group:

• SET NAMES 'charset\_name' [COLLATE 'collation\_name']

SET NAMES indicates what character set the client uses to send SQL statements to the server. Thus, SET NAMES 'cp1251' tells the server, "future incoming messages from this client are in character set cp1251." It also specifies the character set that the server should use for sending results back to the client. (For example, it indicates what character set to use for column values if you use a SELECT statement that produces a result set.)

A SET NAMES 'charset\_name' statement is equivalent to these three statements:

```
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET character_set_connection = charset_name;
```

Setting character\_set\_connection to charset\_name also implicitly sets collation\_connection to the default collation for charset\_name. It is unnecessary to set that collation explicitly. To specify a particular collation to use for collation\_connection, add a COLLATE clause:

```
SET NAMES 'charset_name' COLLATE 'collation_name'
```

• SET CHARACTER SET 'charset\_name'

SET CHARACTER SET is similar to SET NAMES but sets character\_set\_connection and collation\_connection to character\_set\_database and collation\_database (which, as mentioned previously, indicate the character set and collation of the default database).

A SET CHARACTER SET charset\_name statement is equivalent to these three statements:

```
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET collation_connection = @@collation_database;
```

Setting collation\_connection also implicitly sets character\_set\_connection to the character set associated with the collation (equivalent to executing SET

character\_set\_connection = @@character\_set\_database). It is unnecessary to set character\_set\_connection explicitly.

![](_page_173_Picture_2.jpeg)

#### **Note**

Some character sets cannot be used as the client character set. Attempting to use them with SET NAMES or SET CHARACTER SET produces an error. See [Impermissible Client Character Sets.](#page-170-0)

Example: Suppose that column1 is defined as CHAR(5) CHARACTER SET latin2. If you do not say SET NAMES or SET CHARACTER SET, then for SELECT column1 FROM t, the server sends back all the values for column1 using the character set that the client specified when it connected. On the other hand, if you say SET NAMES 'latin1' or SET CHARACTER SET 'latin1' before issuing the SELECT statement, the server converts the latin2 values to latin1 just before sending results back. Conversion may be lossy for characters that are not in both character sets.

# <span id="page-173-0"></span>**Connection Character Set Error Handling**

Attempts to use an inappropriate connection character set or collation can produce an error, or cause the server to fall back to its default character set and collation for a given connection. This section describes problems that can occur when configuring the connection character set. These problems can occur when establishing a connection or when changing the character set within an established connection.

- [Connect-Time Error Handling](#page-173-1)
- [Runtime Error Handling](#page-174-1)

### <span id="page-173-1"></span>**Connect-Time Error Handling**

Some character sets cannot be used as the client character set; see [Impermissible Client Character](#page-170-0) [Sets](#page-170-0). If you specify a character set that is valid but not permitted as a client character set, the server returns an error:

```
$> mysql --default-character-set=ucs2
ERROR 1231 (42000): Variable 'character_set_client' can't be set to
the value of 'ucs2'
```

If you specify a character set that the client does not recognize, it produces an error:

```
$> mysql --default-character-set=bogus
mysql: Character set 'bogus' is not a compiled character set and is
not specified in the '/usr/local/mysql/share/charsets/Index.xml' file
ERROR 2019 (HY000): Can't initialize character set bogus
(path: /usr/local/mysql/share/charsets/)
```

If you specify a character set that the client recognizes but the server does not, the server falls back to its default character set and collation. Suppose that the server is configured to use latin1 and latin1\_swedish\_ci as its defaults, and that it does not recognize gb18030 as a valid character set. A client that specifies --default-character-set=gb18030 is able to connect to the server, but the resulting character set is not what the client wants:

```
mysql> SHOW SESSION VARIABLES LIKE 'character\_set\_%';
+--------------------------+--------+
| Variable_name | Value |
+--------------------------+--------+
| character_set_client | latin1 |
| character_set_connection | latin1 |
...
| character_set_results | latin1 |
...
+--------------------------+--------+
mysql> SHOW SESSION VARIABLES LIKE 'collation_connection';
+----------------------+-------------------+
| Variable_name | Value |
+----------------------+-------------------+
```

```
| collation_connection | latin1_swedish_ci |
+----------------------+-------------------+
```

You can see that the connection system variables have been set to reflect a character set and collation of latin1 and latin1\_swedish\_ci. This occurs because the server cannot satisfy the client character set request and falls back to its defaults.

In this case, the client cannot use the character set that it wants because the server does not support it. The client must either be willing to use a different character set, or connect to a different server that supports the desired character set.

The same problem occurs when the client tells the server to use a character set that the server recognizes, but the default collation for that character set on the client side is not known on the server side.

### <span id="page-174-1"></span>**Runtime Error Handling**

Within an established connection, the client can request a change of connection character set and collation with SET NAMES or SET CHARACTER SET.

Some character sets cannot be used as the client character set; see [Impermissible Client Character](#page-170-0) [Sets](#page-170-0). If you specify a character set that is valid but not permitted as a client character set, the server returns an error:

```
mysql> SET NAMES 'ucs2';
ERROR 1231 (42000): Variable 'character_set_client' can't be set to
the value of 'ucs2'
```

If the server does not recognize the character set (or the collation), it produces an error:

```
mysql> SET NAMES 'bogus';
ERROR 1115 (42000): Unknown character set: 'bogus'
mysql> SET NAMES 'utf8mb4' COLLATE 'bogus';
ERROR 1273 (HY000): Unknown collation: 'bogus'
```

![](_page_174_Picture_11.jpeg)

#### **Tip**

A client that wants to verify whether its requested character set was honored by the server can execute the following statement after connecting and checking that the result is the expected character set:

SELECT @@character\_set\_client;

# <span id="page-174-0"></span>**12.5 Configuring Application Character Set and Collation**

For applications that store data using the default MySQL character set and collation (utf8mb4, utf8mb4\_0900\_ai\_ci), no special configuration should be needed. If applications require data storage using a different character set or collation, you can configure character set information several ways:

- Specify character settings per database. For example, applications that use one database might use the default of utf8mb4, whereas applications that use another database might use sjis.
- Specify character settings at server startup. This causes the server to use the given settings for all applications that do not make other arrangements.
- Specify character settings at configuration time, if you build MySQL from source. This causes the server to use the given settings as the defaults for all applications, without having to specify them at server startup.

When different applications require different character settings, the per-database technique provides a good deal of flexibility. If most or all applications use the same character set, specifying character settings at server startup or configuration time may be most convenient.

For the per-database or server-startup techniques, the settings control the character set for data storage. Applications must also tell the server which character set to use for client/server communications, as described in the following instructions.

The examples shown here assume use of the latin1 character set and latin1\_swedish\_ci collation in particular contexts as an alternative to the defaults of utf8mb4 and utf8mb4\_0900\_ai\_ci.

• **Specify character settings per database.** To create a database such that its tables use a given default character set and collation for data storage, use a CREATE DATABASE statement like this:

```
CREATE DATABASE mydb
 CHARACTER SET latin1
 COLLATE latin1_swedish_ci;
```

Tables created in the database use latin1 and latin1\_swedish\_ci by default for any character columns.

Applications that use the database should also configure their connection to the server each time they connect. This can be done by executing a SET NAMES 'latin1' statement after connecting. The statement can be used regardless of connection method (the mysql client, PHP scripts, and so forth).

In some cases, it may be possible to configure the connection to use the desired character set some other way. For example, to connect using mysql, you can specify the --default-characterset=latin1 command-line option to achieve the same effect as SET NAMES 'latin1'.

For more information about configuring client connections, see [Section 12.4, "Connection Character](#page-169-1) [Sets and Collations"](#page-169-1).

![](_page_175_Picture_9.jpeg)

#### **Note**

If you use ALTER DATABASE to change the database default character set or collation, existing stored routines in the database that use those defaults must be dropped and recreated so that they use the new defaults. (In a stored routine, variables with character data types use the database defaults if the character set or collation are not specified explicitly. See Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements".)

• **Specify character settings at server startup.** To select a character set and collation at server startup, use the --character-set-server and --collation-server options. For example, to specify the options in an option file, include these lines:

```
[mysqld]
character-set-server=latin1
collation-server=latin1_swedish_ci
```

These settings apply server-wide and apply as the defaults for databases created by any application, and for tables created in those databases.

It is still necessary for applications to configure their connection using SET NAMES or equivalent after they connect, as described previously. You might be tempted to start the server with the --init\_connect="SET NAMES 'latin1'" option to cause SET NAMES to be executed automatically for each client that connects. However, this may yield inconsistent results because the init\_connect value is not executed for users who have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

• **Specify character settings at MySQL configuration time.** To select a character set and collation if you configure and build MySQL from source, use the DEFAULT\_CHARSET and DEFAULT\_COLLATION CMake options:

```
cmake . -DDEFAULT_CHARSET=latin1 \
```

```
 -DDEFAULT_COLLATION=latin1_swedish_ci
```

The resulting server uses latin1 and latin1\_swedish\_ci as the default for databases and tables and for client connections. It is unnecessary to use --character-set-server and --collation-server to specify those defaults at server startup. It is also unnecessary for applications to configure their connection using SET NAMES or equivalent after they connect to the server.

Regardless of how you configure the MySQL character set for application use, you must also consider the environment within which those applications execute. For example, if you intend to send statements using UTF-8 text taken from a file that you create in an editor, you should edit the file with the locale of your environment set to UTF-8 so that the file encoding is correct and so that the operating system handles it correctly. If you use the mysql client from within a terminal window, the window must be configured to use UTF-8 or characters may not display properly. For a script that executes in a Web environment, the script must handle character encoding properly for its interaction with the MySQL server, and it must generate pages that correctly indicate the encoding so that browsers know how to display the content of the pages. For example, you can include this <meta> tag within your <head> element:

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

# <span id="page-176-0"></span>**12.6 Error Message Character Set**

This section describes how the MySQL server uses character sets for constructing error messages. For information about the language of error messages (rather than the character set), see Section 12.12, "Setting the Error Message Language". For general information about configuring error logging, see Section 7.4.2, "The Error Log".

- [Character Set for Error Message Construction](#page-176-1)
- [Character Set for Error Message Disposition](#page-176-2)

# <span id="page-176-1"></span>**Character Set for Error Message Construction**

The server constructs error messages as follows:

- The message template uses UTF-8 (utf8mb3).
- Parameters in the message template are replaced with values that apply to a specific error occurrence:
  - Identifiers such as table or column names use UTF-8 internally so they are copied as is.
  - Character (nonbinary) string values are converted from their character set to UTF-8.
  - Binary string values are copied as is for bytes in the range 0x20 to 0x7E, and using \x hexadecimal encoding for bytes outside that range. For example, if a duplicate-key error occurs for an attempt to insert 0x41CF9F into a VARBINARY unique column, the resulting error message uses UTF-8 with some bytes hexadecimal encoded:

Duplicate entry 'A\xCF\x9F' for key 1

# <span id="page-176-2"></span>**Character Set for Error Message Disposition**

An error message, once constructed, can be written by the server to the error log or sent to clients:

- If the server writes the error message to the error log, it writes it in UTF-8, as constructed, without conversion to another character set.
- If the server sends the error message to a client program, the server converts it from UTF-8 to the character set specified by the character\_set\_results system variable. If

character\_set\_results has a value of NULL or binary, no conversion occurs. No conversion occurs if the variable value is utf8mb3 or utf8mb4, either, because those character sets have a repertoire that includes all UTF-8 characters used in message construction.

If characters cannot be represented in character\_set\_results, some encoding may occur during the conversion. The encoding uses Unicode code point values:

- Characters in the Basic Multilingual Plane (BMP) range (0x0000 to 0xFFFF) are written using \nnnn notation.
- Characters outside the BMP range (0x10000 to 0x10FFFF) are written using \+nnnnnn notation.

Clients can set character\_set\_results to control the character set in which they receive error messages. The variable can be set directly, or indirectly by means such as SET NAMES. For more information about character\_set\_results, see [Section 12.4, "Connection Character Sets and](#page-169-1) [Collations"](#page-169-1).

# <span id="page-177-0"></span>**12.7 Column Character Set Conversion**

To convert a binary or nonbinary string column to use a particular character set, use ALTER TABLE. For successful conversion to occur, one of the following conditions must apply:

- If the column has a binary data type (BINARY, VARBINARY, BLOB), all the values that it contains must be encoded using a single character set (the character set you're converting the column to). If you use a binary column to store information in multiple character sets, MySQL has no way to know which values use which character set and cannot convert the data properly.
- If the column has a nonbinary data type (CHAR, VARCHAR, TEXT), its contents should be encoded in the column character set, not some other character set. If the contents are encoded in a different character set, you can convert the column to use a binary data type first, and then to a nonbinary column with the desired character set.

Suppose that a table t has a binary column named col1 defined as VARBINARY(50). Assuming that the information in the column is encoded using a single character set, you can convert it to a nonbinary column that has that character set. For example, if col1 contains binary data representing characters in the greek character set, you can convert it as follows:

```
ALTER TABLE t MODIFY col1 VARCHAR(50) CHARACTER SET greek;
```

If your original column has a type of BINARY(50), you could convert it to CHAR(50), but the resulting values are padded with 0x00 bytes at the end, which may be undesirable. To remove these bytes, use the TRIM() function:

```
UPDATE t SET col1 = TRIM(TRAILING 0x00 FROM col1);
```

Suppose that table t has a nonbinary column named col1 defined as CHAR(50) CHARACTER SET latin1 but you want to convert it to use utf8mb4 so that you can store values from many languages. The following statement accomplishes this:

```
ALTER TABLE t MODIFY col1 CHAR(50) CHARACTER SET utf8mb4;
```

Conversion may be lossy if the column contains characters that are not in both character sets.

A special case occurs if you have old tables from before MySQL 4.1 where a nonbinary column contains values that actually are encoded in a character set different from the server's default character set. For example, an application might have stored sjis values in a column, even though MySQL's default character set was different. It is possible to convert the column to use the proper character set but an additional step is required. Suppose that the server's default character set was latin1 and col1 is defined as CHAR(50) but its contents are sjis values. The first step is to convert the column to a binary data type, which removes the existing character set information without performing any character conversion:

```
ALTER TABLE t MODIFY col1 BLOB;
```

The next step is to convert the column to a nonbinary data type with the proper character set:

```
ALTER TABLE t MODIFY col1 CHAR(50) CHARACTER SET sjis;
```

This procedure requires that the table not have been modified already with statements such as INSERT or UPDATE after an upgrade to MySQL 4.1 or higher. In that case, MySQL would store new values in the column using latin1, and the column would contain a mix of sjis and latin1 values and cannot be converted properly.

If you specified attributes when creating a column initially, you should also specify them when altering the table with ALTER TABLE. For example, if you specified NOT NULL and an explicit DEFAULT value, you should also provide them in the ALTER TABLE statement. Otherwise, the resulting column definition does not include those attributes.

To convert all character columns in a table, the ALTER TABLE ... CONVERT TO CHARACTER SET charset statement may be useful. See Section 15.1.9, "ALTER TABLE Statement".

![](_page_178_Picture_7.jpeg)

#### **Note**

ALTER TABLE statements which make changes in table or column character sets or collations must be performed using ALGORITHM=COPY. For more information, see Section 17.12.1, "Online DDL Operations".

# <span id="page-178-0"></span>**12.8 Collation Issues**

The following sections discuss various aspects of character set collations.

# <span id="page-178-1"></span>**12.8.1 Using COLLATE in SQL Statements**

With the COLLATE clause, you can override whatever the default collation is for a comparison. COLLATE may be used in various parts of SQL statements. Here are some examples:

• With ORDER BY:

```
SELECT k
FROM t1
ORDER BY k COLLATE latin1_german2_ci;
```

• With AS:

```
SELECT k COLLATE latin1_german2_ci AS k1
FROM t1
ORDER BY k1;
```

• With GROUP BY:

```
SELECT k
FROM t1
GROUP BY k COLLATE latin1_german2_ci;
```

• With aggregate functions:

```
SELECT MAX(k COLLATE latin1_german2_ci)
FROM t1;
```

• With DISTINCT:

```
SELECT DISTINCT k COLLATE latin1_german2_ci
FROM t1;
```

• With WHERE:

```
SELECT *
```

```
FROM t1
WHERE _latin1 'Müller' COLLATE latin1_german2_ci = k;
SELECT *
FROM t1
WHERE k LIKE _latin1 'Müller' COLLATE latin1_german2_ci;
```

• With HAVING:

```
SELECT k
FROM t1
GROUP BY k
HAVING k = _latin1 'Müller' COLLATE latin1_german2_ci;
```

# <span id="page-179-0"></span>**12.8.2 COLLATE Clause Precedence**

The COLLATE clause has high precedence (higher than ||), so the following two expressions are equivalent:

```
x || y COLLATE z
x || (y COLLATE z)
```

# <span id="page-179-1"></span>**12.8.3 Character Set and Collation Compatibility**

Each character set has one or more collations, but each collation is associated with one and only one character set. Therefore, the following statement causes an error message because the latin2\_bin collation is not legal with the latin1 character set:

```
mysql> SELECT _latin1 'x' COLLATE latin2_bin;
ERROR 1253 (42000): COLLATION 'latin2_bin' is not valid
for CHARACTER SET 'latin1'
```

# <span id="page-179-2"></span>**12.8.4 Collation Coercibility in Expressions**

In the great majority of statements, it is obvious what collation MySQL uses to resolve a comparison operation. For example, in the following cases, it should be clear that the collation is the collation of column x:

```
SELECT x FROM T ORDER BY x;
SELECT x FROM T WHERE x = x;
SELECT DISTINCT x FROM T;
```

However, with multiple operands, there can be ambiguity. For example, this statement performs a comparison between the column x and the string literal 'Y':

```
SELECT x FROM T WHERE x = 'Y';
```

If x and 'Y' have the same collation, there is no ambiguity about the collation to use for the comparison. But if they have different collations, should the comparison use the collation of x, or of 'Y'? Both x and 'Y' have collations, so which collation takes precedence?

A mix of collations may also occur in contexts other than comparison. For example, a multipleargument concatenation operation such as CONCAT(x,'Y') combines its arguments to produce a single string. What collation should the result have?

To resolve questions like these, MySQL checks whether the collation of one item can be coerced to the collation of the other. MySQL assigns coercibility values as follows:

- An explicit COLLATE clause has a coercibility of 0 (not coercible at all).
- The concatenation of two strings with different collations has a coercibility of 1.
- The collation of a column or a stored routine parameter or local variable has a coercibility of 2.

- A "system constant" (the string returned by functions such as USER() or VERSION()) has a coercibility of 3.
- The collation of a literal has a coercibility of 4.
- The collation of a numeric or temporal value has a coercibility of 5.
- NULL or an expression that is derived from NULL has a coercibility of 6.

MySQL uses coercibility values with the following rules to resolve ambiguities:

- Use the collation with the lowest coercibility value.
- If both sides have the same coercibility, then:
  - If both sides are Unicode, or both sides are not Unicode, it is an error.
  - If one of the sides has a Unicode character set, and another side has a non-Unicode character set, the side with Unicode character set wins, and automatic character set conversion is applied to the non-Unicode side. For example, the following statement does not return an error:

```
SELECT CONCAT(utf8mb4_column, latin1_column) FROM t1;
```

It returns a result that has a character set of utf8mb4 and the same collation as utf8mb4\_column. Values of latin1\_column are automatically converted to utf8mb4 before concatenating.

• For an operation with operands from the same character set but that mix a \_bin collation and a \_ci or \_cs collation, the \_bin collation is used. This is similar to how operations that mix nonbinary and binary strings evaluate the operands as binary strings, applied to collations rather than data types.

Although automatic conversion is not in the SQL standard, the standard does say that every character set is (in terms of supported characters) a "subset" of Unicode. Because it is a well-known principle that "what applies to a superset can apply to a subset," we believe that a collation for Unicode can apply for comparisons with non-Unicode strings. More generally, MySQL uses the concept of character set repertoire, which can sometimes be used to determine subset relationships among character sets and enable conversion of operands in operations that would otherwise produce an error. See [Section 12.2.1, "Character Set Repertoire"](#page-156-0).

The following table illustrates some applications of the preceding rules.

| Comparison                        | Collation Used                 |
|-----------------------------------|--------------------------------|
| column1 = 'A'                     | Use collation of column1       |
| column1 = 'A' COLLATE x           | Use collation of 'A' COLLATE x |
| column1 COLLATE x = 'A' COLLATE y | Error                          |

To determine the coercibility of a string expression, use the COERCIBILITY() function (see Section 14.15, "Information Functions"):

```
mysql> SELECT COERCIBILITY(_utf8mb4'A' COLLATE utf8mb4_bin);
 -> 0
mysql> SELECT COERCIBILITY(VERSION());
 -> 3
mysql> SELECT COERCIBILITY('A');
 -> 4
mysql> SELECT COERCIBILITY(1000);
 -> 5
mysql> SELECT COERCIBILITY(NULL);
 -> 6
```

For implicit conversion of a numeric or temporal value to a string, such as occurs for the argument 1 in the expression CONCAT(1, 'abc'), the result is a character (nonbinary) string that has a character

set and collation determined by the character\_set\_connection and collation\_connection system variables. See Section 14.3, "Type Conversion in Expression Evaluation".

### <span id="page-181-0"></span>**12.8.5 The binary Collation Compared to \_bin Collations**

This section describes how the binary collation for binary strings compares to \_bin collations for nonbinary strings.

Binary strings (as stored using the BINARY, VARBINARY, and BLOB data types) have a character set and collation named binary. Binary strings are sequences of bytes and the numeric values of those bytes determine comparison and sort order. See Section 12.10.8, "The Binary Character Set".

Nonbinary strings (as stored using the CHAR, VARCHAR, and TEXT data types) have a character set and collation other than binary. A given nonbinary character set can have several collations, each of which defines a particular comparison and sort order for the characters in the set. For most character sets, one of these is the binary collation, indicated by a \_bin suffix in the collation name. For example, the binary collations for latin1 and big5 are named latin1\_bin and big5\_bin, respectively. utf8mb4 is an exception that has two binary collations, utf8mb4\_bin and utf8mb4\_0900\_bin; see [Section 12.10.1, "Unicode Character Sets".](#page-194-1)

The binary collation differs from \_bin collations in several respects, discussed in the following sections:

- [The Unit for Comparison and Sorting](#page-181-1)
- [Character Set Conversion](#page-181-2)
- [Lettercase Conversion](#page-182-0)
- [Trailing Space Handling in Comparisons](#page-182-1)
- [Trailing Space Handling for Inserts and Retrievals](#page-183-1)

#### <span id="page-181-1"></span>**The Unit for Comparison and Sorting**

Binary strings are sequences of bytes. For the binary collation, comparison and sorting are based on numeric byte values. Nonbinary strings are sequences of characters, which might be multibyte. Collations for nonbinary strings define an ordering of the character values for comparison and sorting. For \_bin collations, this ordering is based on numeric character code values, which is similar to ordering for binary strings except that character code values might be multibyte.

#### <span id="page-181-2"></span>**Character Set Conversion**

A nonbinary string has a character set and is automatically converted to another character set in many cases, even when the string has a \_bin collation:

• When assigning column values to another column that has a different character set:

```
UPDATE t1 SET utf8mb4_bin_column=latin1_column;
INSERT INTO t1 (latin1_column) SELECT utf8mb4_bin_column FROM t2;
```

• When assigning column values for INSERT or UPDATE using a string literal:

```
SET NAMES latin1;
INSERT INTO t1 (utf8mb4_bin_column) VALUES ('string-in-latin1');
```

• When sending results from the server to a client:

```
SET NAMES latin1;
SELECT utf8mb4_bin_column FROM t2;
```

For binary string columns, no conversion occurs. For cases similar to those preceding, the string value is copied byte-wise.

### <span id="page-182-0"></span>**Lettercase Conversion**

Collations for nonbinary character sets provide information about lettercase of characters, so characters in a nonbinary string can be converted from one lettercase to another, even for \_bin collations that ignore lettercase for ordering:

```
mysql> SET NAMES utf8mb4 COLLATE utf8mb4_bin;
mysql> SELECT LOWER('aA'), UPPER('zZ');
+-------------+-------------+
| LOWER('aA') | UPPER('zZ') |
+-------------+-------------+
| aa | ZZ |
+-------------+-------------+
```

The concept of lettercase does not apply to bytes in a binary string. To perform lettercase conversion, the string must first be converted to a nonbinary string using a character set appropriate for the data stored in the string:

```
mysql> SET NAMES binary;
mysql> SELECT LOWER('aA'), LOWER(CONVERT('aA' USING utf8mb4));
+-------------+------------------------------------+
| LOWER('aA') | LOWER(CONVERT('aA' USING utf8mb4)) |
+-------------+------------------------------------+
| aA | aa |
+-------------+------------------------------------+
```

#### <span id="page-182-1"></span>**Trailing Space Handling in Comparisons**

MySQL collations have a pad attribute, which has a value of PAD SPACE or NO PAD:

- Most MySQL collations have a pad attribute of PAD SPACE.
- The Unicode collations based on UCA 9.0.0 and higher have a pad attribute of NO PAD; see [Section 12.10.1, "Unicode Character Sets".](#page-194-1)

For nonbinary strings (CHAR, VARCHAR, and TEXT values), the string collation pad attribute determines treatment in comparisons of trailing spaces at the end of strings:

- For PAD SPACE collations, trailing spaces are insignificant in comparisons; strings are compared without regard to trailing spaces.
- NO PAD collations treat trailing spaces as significant in comparisons, like any other character.

The differing behaviors can be demonstrated using the two utf8mb4 binary collations, one of which is PAD SPACE, the other of which is NO PAD. The example also shows how to use the INFORMATION\_SCHEMA COLLATIONS table to determine the pad attribute for collations.

```
mysql> SELECT COLLATION_NAME, PAD_ATTRIBUTE
 FROM INFORMATION_SCHEMA.COLLATIONS
 WHERE COLLATION_NAME LIKE 'utf8mb4%bin';
+------------------+---------------+
| COLLATION_NAME | PAD_ATTRIBUTE |
+------------------+---------------+
| utf8mb4_bin | PAD SPACE |
| utf8mb4_0900_bin | NO PAD |
+------------------+---------------+
mysql> SET NAMES utf8mb4 COLLATE utf8mb4_bin;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |
+------------+
| 1 |
+------------+
mysql> SET NAMES utf8mb4 COLLATE utf8mb4_0900_bin;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |
```

+------------+ | 0 | +------------+

![](_page_183_Picture_2.jpeg)

#### **Note**

"Comparison" in this context does not include the LIKE pattern-matching operator, for which trailing spaces are significant, regardless of collation.

For binary strings (BINARY, VARBINARY, and BLOB values), all bytes are significant in comparisons, including trailing spaces:

```
mysql> SET NAMES binary;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |
+------------+
| 0 |
+------------+
```

#### <span id="page-183-1"></span>**Trailing Space Handling for Inserts and Retrievals**

CHAR(N) columns store nonbinary strings N characters long. For inserts, values shorter than N characters are extended with spaces. For retrievals, trailing spaces are removed.

BINARY(N) columns store binary strings N bytes long. For inserts, values shorter than N bytes are extended with 0x00 bytes. For retrievals, nothing is removed; a value of the declared length is always returned.

```
mysql> CREATE TABLE t1 (
 a CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
 b BINARY(10)
 );
mysql> INSERT INTO t1 VALUES ('x','x');
mysql> INSERT INTO t1 VALUES ('x ','x ');
mysql> SELECT a, b, HEX(a), HEX(b) FROM t1;
+------+------------------------+--------+----------------------+
| a | b | HEX(a) | HEX(b) |
+------+------------------------+--------+----------------------+
| x | 0x78000000000000000000 | 78 | 78000000000000000000 |
| x | 0x78200000000000000000 | 78 | 78200000000000000000 |
+------+------------------------+--------+----------------------+
```

# <span id="page-183-0"></span>**12.8.6 Examples of the Effect of Collation**

#### **Example 1: Sorting German Umlauts**

Suppose that column X in table T has these latin1 column values:

```
Muffler
Müller
MX Systems
MySQL
```

Suppose also that the column values are retrieved using the following statement:

```
SELECT X FROM T ORDER BY X COLLATE collation_name;
```

The following table shows the resulting order of the values if we use ORDER BY with different collations.

| latin1_swedish_ci | latin1_german1_ci | latin1_german2_ci |
|-------------------|-------------------|-------------------|
| Muffler           | Muffler           | Müller            |
| MX Systems        | Müller            | Muffler           |
| Müller            | MX Systems        | MX Systems        |
| MySQL             | MySQL             | MySQL             |

The character that causes the different sort orders in this example is ü (German "U-umlaut").

- The first column shows the result of the SELECT using the Swedish/Finnish collating rule, which says that U-umlaut sorts with Y.
- The second column shows the result of the SELECT using the German DIN-1 rule, which says that Uumlaut sorts with U.
- The third column shows the result of the SELECT using the German DIN-2 rule, which says that Uumlaut sorts with UE.

#### **Example 2: Searching for German Umlauts**

Suppose that you have three tables that differ only by the character set and collation used:

```
mysql> SET NAMES utf8mb4;
mysql> CREATE TABLE german1 (
 c CHAR(10)
 ) CHARACTER SET latin1 COLLATE latin1_german1_ci;
mysql> CREATE TABLE german2 (
 c CHAR(10)
 ) CHARACTER SET latin1 COLLATE latin1_german2_ci;
mysql> CREATE TABLE germanutf8 (
 c CHAR(10)
 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Each table contains two records:

```
mysql> INSERT INTO german1 VALUES ('Bar'), ('Bär');
mysql> INSERT INTO german2 VALUES ('Bar'), ('Bär');
mysql> INSERT INTO germanutf8 VALUES ('Bar'), ('Bär');
```

Two of the above collations have an A = Ä equality, and one has no such equality (latin1\_german2\_ci). For that reason, comparisons yield the results shown here:

```
mysql> SELECT * FROM german1 WHERE c = 'Bär';
+------+
| c |
+------+
| Bar |
| Bär |
+------+
mysql> SELECT * FROM german2 WHERE c = 'Bär';
+------+
| c |
+------+
| Bär |
+------+
mysql> SELECT * FROM germanutf8 WHERE c = 'Bär';
+------+
| c |
+------+
| Bar |
| Bär |
+------+
```

This is not a bug but rather a consequence of the sorting properties of latin1\_german1\_ci and utf8mb4\_unicode\_ci (the sorting shown is done according to the German DIN 5007 standard).

# <span id="page-184-0"></span>**12.8.7 Using Collation in INFORMATION\_SCHEMA Searches**

String columns in INFORMATION\_SCHEMA tables have a collation of utf8mb3\_general\_ci, which is case-insensitive. However, for values that correspond to objects that are represented in the file system, such as databases and tables, searches in INFORMATION\_SCHEMA string columns can be casesensitive or case-insensitive, depending on the characteristics of the underlying file system and the lower\_case\_table\_names system variable setting. For example, searches may be case-sensitive if the file system is case-sensitive. This section describes this behavior and how to modify it if necessary.

Suppose that a query searches the SCHEMATA.SCHEMA\_NAME column for the test database. On Linux, file systems are case-sensitive, so comparisons of SCHEMATA.SCHEMA\_NAME with 'test' match, but comparisons with 'TEST' do not:

```
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test |
+-------------+
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'TEST';
Empty set (0.00 sec)
```

These results occur with the lower\_case\_table\_names system variable set to 0. A lower\_case\_table\_names setting of 1 or 2 causes the second query to return the same (nonempty) result as the first query.

![](_page_185_Picture_4.jpeg)

#### **Note**

It is prohibited to start the server with a lower\_case\_table\_names setting that is different from the setting used when the server was initialized.

On Windows or macOS, file systems are not case-sensitive, so comparisons match both 'test' and 'TEST':

```
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test |
+-------------+
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'TEST';
+-------------+
| SCHEMA_NAME |
+-------------+
| TEST |
+-------------+
```

The value of lower\_case\_table\_names makes no difference in this context.

The preceding behavior occurs because the utf8mb3\_general\_ci collation is not used for INFORMATION\_SCHEMA queries when searching for values that correspond to objects represented in the file system.

If the result of a string operation on an INFORMATION\_SCHEMA column differs from expectations, a workaround is to use an explicit COLLATE clause to force a suitable collation (see [Section 12.8.1,](#page-178-1) ["Using COLLATE in SQL Statements"](#page-178-1)). For example, to perform a case-insensitive search, use COLLATE with the INFORMATION\_SCHEMA column name:

```
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME COLLATE utf8mb3_general_ci = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test |
+-------------+
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME COLLATE utf8mb3_general_ci = 'TEST';
+-------------+
| SCHEMA_NAME |
```

```
+-------------+
| test |
+-------------+
```

You can also use the UPPER() or LOWER() function:

```
WHERE UPPER(SCHEMA_NAME) = 'TEST'
WHERE LOWER(SCHEMA_NAME) = 'test'
```

Although a case-insensitive comparison can be performed even on platforms with case-sensitive file systems, as just shown, it is not necessarily always the right thing to do. On such platforms, it is possible to have multiple objects with names that differ only in lettercase. For example, tables named city, CITY, and City can all exist simultaneously. Consider whether a search should match all such names or just one and write queries accordingly. The first of the following comparisons (with utf8mb3\_bin) is case-sensitive; the others are not:

```
WHERE TABLE_NAME COLLATE utf8mb3_bin = 'City'
WHERE TABLE_NAME COLLATE utf8mb3_general_ci = 'city'
WHERE UPPER(TABLE_NAME) = 'CITY'
WHERE LOWER(TABLE_NAME) = 'city'
```

Searches in INFORMATION\_SCHEMA string columns for values that refer to INFORMATION\_SCHEMA itself do use the utf8mb3\_general\_ci collation because INFORMATION\_SCHEMA is a "virtual" database not represented in the file system. For example, comparisons with SCHEMATA.SCHEMA\_NAME match 'information\_schema' or 'INFORMATION\_SCHEMA' regardless of platform:

```
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'information_schema';
+--------------------+
| SCHEMA_NAME |
+--------------------+
| information_schema |
+--------------------+
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'INFORMATION_SCHEMA';
+--------------------+
| SCHEMA_NAME |
+--------------------+
| information_schema |
+--------------------+
```

# <span id="page-186-0"></span>**12.9 Unicode Support**

The Unicode Standard includes characters from the Basic Multilingual Plane (BMP) and supplementary characters that lie outside the BMP. This section describes support for Unicode in MySQL. For information about the Unicode Standard itself, visit the [Unicode Consortium website.](http://www.unicode.org/)

BMP characters have these characteristics:

- Their code point values are between 0 and 65535 (or U+0000 and U+FFFF).
- They can be encoded in a variable-length encoding using 8, 16, or 24 bits (1 to 3 bytes).
- They can be encoded in a fixed-length encoding using 16 bits (2 bytes).
- They are sufficient for almost all characters in major languages.

Supplementary characters lie outside the BMP:

- Their code point values are between U+10000 and U+10FFFF).
- Unicode support for supplementary characters requires character sets that have a range outside BMP characters and therefore take more space than BMP characters (up to 4 bytes per character).

The UTF-8 (Unicode Transformation Format with 8-bit units) method for encoding Unicode data is implemented according to RFC 3629, which describes encoding sequences that take from one to four bytes. The idea of UTF-8 is that various Unicode characters are encoded using byte sequences of different lengths:

- Basic Latin letters, digits, and punctuation signs use one byte.
- Most European and Middle East script letters fit into a 2-byte sequence: extended Latin letters (with tilde, macron, acute, grave and other accents), Cyrillic, Greek, Armenian, Hebrew, Arabic, Syriac, and others.
- Korean, Chinese, and Japanese ideographs use 3-byte or 4-byte sequences.

MySQL supports these Unicode character sets:

- utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.
- utf8mb3: A UTF-8 encoding of the Unicode character set using one to three bytes per character. This character set is deprecated andsubject to removal in a future release; use utf8mb4 instead.
- utf8: A deprecated alias for utf8mb3; use utf8mb4 instead.

![](_page_187_Picture_9.jpeg)

#### **Note**

utf8 is expected in a future version of MySQL to become an alias for utf8mb4.

- ucs2: The UCS-2 encoding of the Unicode character set using two bytes per character. Deprecated; expect support for this character set to be removed in a future release.
- utf16: The UTF-16 encoding for the Unicode character set using two or four bytes per character. Like ucs2 but with an extension for supplementary characters.
- utf16le: The UTF-16LE encoding for the Unicode character set. Like utf16 but little-endian rather than big-endian.
- utf32: The UTF-32 encoding for the Unicode character set using four bytes per character.

![](_page_187_Picture_16.jpeg)

#### **Note**

The utf8mb3 character set is deprecated and you should expect it to be removed in a future MySQL release. Please use utf8mb4 instead. utf8 is currently an alias for utf8mb3, but it is now deprecated as such, and utf8 is expected subsequently to become a reference to utf8mb4. MySQL 8.4 also displays utf8mb3 in place of utf8 in the columns of Information Schema tables, and in the output of SQL SHOW statements.

In addition, you should be aware that collations using the utf8\_ prefix in older releases of MySQL have since been renamed using the prefix utf8mb3\_, instead.

To avoid ambiguity about the meaning of utf8, consider specifying utf8mb4 explicitly for character set references.

[Table 12.2, "Unicode Character Set General Characteristics",](#page-187-0) summarizes the general characteristics of Unicode character sets supported by MySQL.

**Table 12.2 Unicode Character Set General Characteristics**

<span id="page-187-0"></span>

| Character Set              | Supported Characters | Required Storage Per<br>Character |
|----------------------------|----------------------|-----------------------------------|
| utf8mb3, utf8 (deprecated) | BMP only             | 1, 2, or 3 bytes                  |

| Character Set | Supported Characters  | Required Storage Per<br>Character |
|---------------|-----------------------|-----------------------------------|
| ucs2          | BMP only              | 2 bytes                           |
| utf8mb4       | BMP and supplementary | 1, 2, 3, or 4 bytes               |
| utf16         | BMP and supplementary | 2 or 4 bytes                      |
| utf16le       | BMP and supplementary | 2 or 4 bytes                      |
| utf32         | BMP and supplementary | 4 bytes                           |

Characters outside the BMP compare as REPLACEMENT CHARACTER and convert to '?' when converted to a Unicode character set that supports only BMP characters (utf8mb3 or ucs2).

If you use character sets that support supplementary characters and thus are "wider" than the BMPonly utf8mb3 and ucs2 character sets, there are potential incompatibility issues for your applications; see [Section 12.9.8, "Converting Between 3-Byte and 4-Byte Unicode Character Sets".](#page-191-2) That section also describes how to convert tables from the (3-byte) utf8mb3 to the (4-byte) utf8mb4, and what constraints may apply in doing so.

A similar set of collations is available for most Unicode character sets. For example, each has a Danish collation, the names of which are utf8mb4\_danish\_ci, utf8mb3\_danish\_ci (deprecated), utf8\_danish\_ci (deprecated), ucs2\_danish\_ci, utf16\_danish\_ci, and utf32\_danish\_ci. The exception is utf16le, which has only two collations. For information about Unicode collations and their differentiating properties, including collation properties for supplementary characters, see [Section 12.10.1, "Unicode Character Sets".](#page-194-1)

The MySQL implementation of UCS-2, UTF-16, and UTF-32 stores characters in big-endian byte order and does not use a byte order mark (BOM) at the beginning of values. Other database systems might use little-endian byte order or a BOM. In such cases, conversion of values needs to be performed when transferring data between those systems and MySQL. The implementation of UTF-16LE is little-endian.

MySQL uses no BOM for UTF-8 values.

Client applications that communicate with the server using Unicode should set the client character set accordingly (for example, by issuing a SET NAMES 'utf8mb4' statement). Some character sets cannot be used as the client character set. Attempting to use them with SET NAMES or SET CHARACTER SET produces an error. See [Impermissible Client Character Sets](#page-170-0).

The following sections provide additional detail on the Unicode character sets in MySQL.

# <span id="page-188-0"></span>**12.9.1 The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding)**

The utf8mb4 character set has these characteristics:

- Supports BMP and supplementary characters.
- Requires a maximum of four bytes per multibyte character.

utf8mb4 contrasts with the utf8mb3 character set, which supports only BMP characters and uses a maximum of three bytes per character:

- For a BMP character, utf8mb4 and utf8mb3 have identical storage characteristics: same code values, same encoding, same length.
- For a supplementary character, utf8mb4 requires four bytes to store it, whereas utf8mb3 cannot store the character at all. When converting utf8mb3 columns to utf8mb4, you need not worry about converting supplementary characters because there are none.

utf8mb4 is a superset of utf8mb3, so for an operation such as the following concatenation, the result has character set utf8mb4 and the collation of utf8mb4\_col:

SELECT CONCAT(utf8mb3\_col, utf8mb4\_col);

Similarly, the following comparison in the WHERE clause works according to the collation of utf8mb4\_col:

```
SELECT * FROM utf8mb3_tbl, utf8mb4_tbl
WHERE utf8mb3_tbl.utf8mb3_col = utf8mb4_tbl.utf8mb4_col;
```

For information about data type storage as it relates to multibyte character sets, see String Type Storage Requirements.

# <span id="page-189-0"></span>**12.9.2 The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding)**

The utf8mb3 character set has these characteristics:

- Supports BMP characters only (no support for supplementary characters)
- Requires a maximum of three bytes per multibyte character.

Applications that use UTF-8 data but require supplementary character support should use utf8mb4 rather than utf8mb3 (see [Section 12.9.1, "The utf8mb4 Character Set \(4-Byte UTF-8 Unicode](#page-188-0) [Encoding\)"](#page-188-0)).

Exactly the same set of characters is available in utf8mb3 and ucs2. That is, they have the same repertoire.

![](_page_189_Picture_10.jpeg)

#### **Note**

The recommended character set for MySQL is utf8mb4. All new applications should use utf8mb4.

The utf8mb3 character set is deprecated. utf8mb3 remains supported for the lifetimes of the MySQL 8.0.x and MySQL 8.4.x LTS release series.

Expect utf8mb3 to be removed in a future major release of MySQL.

Since changing character sets can be a complex and time-consuming task, you should begin to prepare for this change now by using utf8mb4 for new applications. For guidance in converting existing applications which use utfmb3, see [Section 12.9.8, "Converting Between 3-Byte and 4-Byte Unicode Character](#page-191-2) [Sets".](#page-191-2)

utf8mb3 can be used in CHARACTER SET clauses, and utf8mb3\_collation\_substring in COLLATE clauses, where collation\_substring is bin, czech\_ci, danish\_ci, esperanto\_ci, estonian\_ci, and so forth. For example:

```
CREATE TABLE t (s1 CHAR(1)) CHARACTER SET utf8mb3;
SELECT * FROM t WHERE s1 COLLATE utf8mb3_general_ci = 'x';
DECLARE x VARCHAR(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_danish_ci;
SELECT CAST('a' AS CHAR CHARACTER SET utf8mb4) COLLATE utf8mb4_czech_ci;
```

In statements such as SHOW CREATE TABLE or SELECT CHARACTER\_SET\_NAME FROM INFORMATION\_SCHEMA.COLUMNS or SELECT COLLATION\_NAME FROM INFORMATION\_SCHEMA.COLUMNS, character sets or collation names prefixed with utf8 or utf8\_ are displayed using utf8mb3 or utf8mb3\_, respectively.

utf8mb3 is also valid (but deprecated) in contexts other than CHARACTER SET clauses. For example:

```
mysqld --character-set-server=utf8mb3
SET NAMES 'utf8mb3'; /* and other SET statements that have similar effect */
SELECT _utf8mb3 'a';
```

For information about data type storage as it relates to multibyte character sets, see String Type Storage Requirements.

# <span id="page-190-0"></span>**12.9.3 The utf8 Character Set (Deprecated alias for utf8mb3)**

utf8 has been used by MySQL in the past as an alias for the utf8mb3 character set, but this usage is now deprecated; in MySQL 8.4, SHOW statements and columns of INFORMATION\_SCHEMA tables display utf8mb3 instead. For more information, see [Section 12.9.2, "The utf8mb3 Character Set \(3-](#page-189-0) [Byte UTF-8 Unicode Encoding\)".](#page-189-0)

![](_page_190_Picture_3.jpeg)

#### **Note**

The recommended character set for MySQL is utf8mb4. All new applications should use utf8mb4.

The utf8mb3 character set is deprecated. utf8mb3 remains supported for the lifetimes of the MySQL 8.0.x and MySQL 8.4.x LTS release series.

Expect utf8mb3 to be removed in a future major release of MySQL.

Since changing character sets can be a complex and time-consuming task, you should begin to prepare for this change now by using utf8mb4 for new applications. For guidance in converting existing applications which use utfmb3, see [Section 12.9.8, "Converting Between 3-Byte and 4-Byte Unicode Character](#page-191-2) [Sets".](#page-191-2)

# <span id="page-190-1"></span>**12.9.4 The ucs2 Character Set (UCS-2 Unicode Encoding)**

![](_page_190_Picture_10.jpeg)

#### **Note**

The ucs2 character set is deprecated; expect it to be removed in a future MySQL release. You should use utf8mb4 instead.

In UCS-2, every character is represented by a 2-byte Unicode code with the most significant byte first. For example: LATIN CAPITAL LETTER A has the code 0x0041 and it is stored as a 2-byte sequence: 0x00 0x41. CYRILLIC SMALL LETTER YERU (Unicode 0x044B) is stored as a 2 byte sequence: 0x04 0x4B. For Unicode characters and their codes, please refer to the [Unicode](http://www.unicode.org/) [Consortium website.](http://www.unicode.org/)

The ucs2 character set has these characteristics:

- Supports BMP characters only (no support for supplementary characters)
- Uses a fixed-length 16-bit encoding and requires two bytes per character.

# <span id="page-190-2"></span>**12.9.5 The utf16 Character Set (UTF-16 Unicode Encoding)**

The utf16 character set is the ucs2 character set with an extension that enables encoding of supplementary characters:

- For a BMP character, utf16 and ucs2 have identical storage characteristics: same code values, same encoding, same length.
- For a supplementary character, utf16 has a special sequence for representing the character using 32 bits. This is called the "surrogate" mechanism: For a number greater than 0xffff, take 10 bits and add them to 0xd800 and put them in the first 16-bit word, take 10 more bits and add them to 0xdc00 and put them in the next 16-bit word. Consequently, all supplementary characters require 32 bits, where the first 16 bits are a number between 0xd800 and 0xdbff, and the last 16 bits are a number between 0xdc00 and 0xdfff. Examples are in Section [15.5 Surrogates Area](http://www.unicode.org/versions/Unicode4.0.0/ch15.pdf) of the Unicode 4.0 document.

Because utf16 supports surrogates and ucs2 does not, there is a validity check that applies only in utf16: You cannot insert a top surrogate without a bottom surrogate, or vice versa. For example:

```
INSERT INTO t (ucs2_column) VALUES (0xd800); /* legal */
INSERT INTO t (utf16_column)VALUES (0xd800); /* illegal */
```

There is no validity check for characters that are technically valid but are not true Unicode (that is, characters that Unicode considers to be "unassigned code points" or "private use" characters or even "illegals" like 0xffff). For example, since U+F8FF is the Apple Logo, this is legal:

```
INSERT INTO t (utf16_column)VALUES (0xf8ff); /* legal */
```

Such characters cannot be expected to mean the same thing to everyone.

Because MySQL must allow for the worst case (that one character requires four bytes) the maximum length of a utf16 column or index is only half of the maximum length for a ucs2 column or index. For example, the maximum length of a MEMORY table index key is 3072 bytes, so these statements create tables with the longest permitted indexes for ucs2 and utf16 columns:

```
CREATE TABLE tf (s1 VARCHAR(1536) CHARACTER SET ucs2) ENGINE=MEMORY;
CREATE INDEX i ON tf (s1);
CREATE TABLE tg (s1 VARCHAR(768) CHARACTER SET utf16) ENGINE=MEMORY;
CREATE INDEX i ON tg (s1);
```

# <span id="page-191-0"></span>**12.9.6 The utf16le Character Set (UTF-16LE Unicode Encoding)**

This is the same as utf16 but is little-endian rather than big-endian.

## <span id="page-191-1"></span>**12.9.7 The utf32 Character Set (UTF-32 Unicode Encoding)**

The utf32 character set is fixed length (like ucs2 and unlike utf16). utf32 uses 32 bits for every character, unlike ucs2 (which uses 16 bits for every character), and unlike utf16 (which uses 16 bits for some characters and 32 bits for others).

utf32 takes twice as much space as ucs2 and more space than utf16, but utf32 has the same advantage as ucs2 that it is predictable for storage: The required number of bytes for utf32 equals the number of characters times 4. Also, unlike utf16, there are no tricks for encoding in utf32, so the stored value equals the code value.

To demonstrate how the latter advantage is useful, here is an example that shows how to determine a utf8mb4 value given the utf32 code value:

```
/* Assume code value = 100cc LINEAR B WHEELED CHARIOT */
CREATE TABLE tmp (utf32_col CHAR(1) CHARACTER SET utf32,
 utf8mb4_col CHAR(1) CHARACTER SET utf8mb4);
INSERT INTO tmp VALUES (0x000100cc,NULL);
UPDATE tmp SET utf8mb4_col = utf32_col;
SELECT HEX(utf32_col),HEX(utf8mb4_col) FROM tmp;
```

MySQL is very forgiving about additions of unassigned Unicode characters or private-use-area characters. There is in fact only one validity check for utf32: No code value may be greater than 0x10ffff. For example, this is illegal:

```
INSERT INTO t (utf32_column) VALUES (0x110000); /* illegal */
```

# <span id="page-191-2"></span>**12.9.8 Converting Between 3-Byte and 4-Byte Unicode Character Sets**

This section describes issues that you may face when converting character data between the utf8mb3 and utf8mb4 character sets.

![](_page_191_Picture_18.jpeg)

#### **Note**

This discussion focuses primarily on converting between utf8mb3 and utf8mb4, but similar principles apply to converting between the ucs2 character set and character sets such as utf16 or utf32.

The utf8mb3 and utf8mb4 character sets differ as follows:

- utf8mb3 supports only characters in the Basic Multilingual Plane (BMP). utf8mb4 additionally supports supplementary characters that lie outside the BMP.
- utf8mb3 uses a maximum of three bytes per character. utf8mb4 uses a maximum of four bytes per character.

![](_page_192_Picture_3.jpeg)

#### **Note**

This discussion refers to the utf8mb3 and utf8mb4 character set names to be explicit about referring to 3-byte and 4-byte UTF-8 character set data.

One advantage of converting from utf8mb3 to utf8mb4 is that this enables applications to use supplementary characters. One tradeoff is that this may increase data storage space requirements.

In terms of table content, conversion from utf8mb3 to utf8mb4 presents no problems:

- For a BMP character, utf8mb4 and utf8mb3 have identical storage characteristics: same code values, same encoding, same length.
- For a supplementary character, utf8mb4 requires four bytes to store it, whereas utf8mb3 cannot store the character at all. When converting utf8mb3 columns to utf8mb4, you need not worry about converting supplementary characters because there are none.

In terms of table structure, these are the primary potential incompatibilities:

- For the variable-length character data types (VARCHAR and the TEXT types), the maximum permitted length in characters is less for utf8mb4 columns than for utf8mb3 columns.
- For all character data types (CHAR, VARCHAR, and the TEXT types), the maximum number of characters that can be indexed is less for utf8mb4 columns than for utf8mb3 columns.

Consequently, to convert tables from utf8mb3 to utf8mb4, it may be necessary to change some column or index definitions.

Tables can be converted from utf8mb3 to utf8mb4 by using ALTER TABLE. Suppose that a table has this definition:

```
CREATE TABLE t1 (
 col1 CHAR(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
 col2 CHAR(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL
) CHARACTER SET utf8mb3;
```

The following statement converts t1 to use utf8mb4:

```
ALTER TABLE t1
 DEFAULT CHARACTER SET utf8mb4,
 MODIFY col1 CHAR(10)
 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
 MODIFY col2 CHAR(10)
 CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;
```

The catch when converting from utf8mb3 to utf8mb4 is that the maximum length of a column or index key is unchanged in terms of bytes. Therefore, it is smaller in terms of characters because the maximum length of a character is four bytes instead of three. For the CHAR, VARCHAR, and TEXT data types, watch for these issues when converting your MySQL tables:

- Check all definitions of utf8mb3 columns and make sure they do not exceed the maximum length for the storage engine.
- Check all indexes on utf8mb3 columns and make sure they do not exceed the maximum length for the storage engine. Sometimes the maximum can change due to storage engine enhancements.

If the preceding conditions apply, you must either reduce the defined length of columns or indexes, or continue to use utf8mb3 rather than utf8mb4.

Here are some examples where structural changes may be needed:

• A TINYTEXT column can hold up to 255 bytes, so it can hold up to 85 3-byte or 63 4-byte characters. Suppose that you have a TINYTEXT column that uses utf8mb3 but must be able to contain more than 63 characters. You cannot convert it to utf8mb4 unless you also change the data type to a longer type such as TEXT.

Similarly, a very long VARCHAR column may need to be changed to one of the longer TEXT types if you want to convert it from utf8mb3 to utf8mb4.

• InnoDB has a maximum index length of 767 bytes for tables that use COMPACT or REDUNDANT row format, so for utf8mb3 or utf8mb4 columns, you can index a maximum of 255 or 191 characters, respectively. If you currently have utf8mb3 columns with indexes longer than 191 characters, you must index a smaller number of characters.

In an InnoDB table that uses COMPACT or REDUNDANT row format, these column and index definitions are legal:

```
col1 VARCHAR(500) CHARACTER SET utf8mb3, INDEX (col1(255))
```

To use utf8mb4 instead, the index must be smaller:

col1 VARCHAR(500) CHARACTER SET utf8mb4, INDEX (col1(191))

![](_page_193_Picture_9.jpeg)

#### **Note**

For InnoDB tables that use COMPRESSED or DYNAMIC row format, index key prefixes longer than 767 bytes (up to 3072 bytes) are permitted. Tables created with these row formats enable you to index a maximum of 1024 or 768 characters for utf8mb3 or utf8mb4 columns, respectively. For related information, see Section 17.21, "InnoDB Limits", and DYNAMIC Row Format.

The preceding types of changes are most likely to be required only if you have very long columns or indexes. Otherwise, you should be able to convert your tables from utf8mb3 to utf8mb4 without problems, using ALTER TABLE as described previously.

The following items summarize other potential incompatibilities:

- SET NAMES 'utf8mb4' causes use of the 4-byte character set for connection character sets. As long as no 4-byte characters are sent from the server, there should be no problems. Otherwise, applications that expect to receive a maximum of three bytes per character may have problems. Conversely, applications that expect to send 4-byte characters must ensure that the server understands them.
- For replication, if character sets that support supplementary characters are to be used on the source, all replicas must understand them as well.

Also, keep in mind the general principle that if a table has different definitions on the source and replica, this can lead to unexpected results. For example, the differences in maximum index key length make it risky to use utf8mb3 on the source and utf8mb4 on the replica.

If you have converted to utf8mb4, utf16, utf16le, or utf32, and then decide to convert back to utf8mb3 or ucs2 (for example, to downgrade to an older version of MySQL), these considerations apply:

- utf8mb3 and ucs2 data should present no problems.
- The server must be recent enough to recognize definitions referring to the character set from which you are converting.
- For object definitions that refer to the utf8mb4 character set, you can dump them with mysqldump prior to downgrading, edit the dump file to change instances of utf8mb4 to utf8, and reload the file

in the older server, as long as there are no 4-byte characters in the data. The older server sees utf8 in the dump file object definitions and create new objects that use the (3-byte) utf8 character set.

# <span id="page-194-0"></span>**12.10 Supported Character Sets and Collations**

This section indicates which character sets MySQL supports. There is one subsection for each group of related character sets. For each character set, the permissible collations are listed.

To list the available character sets and their default collations, use the SHOW CHARACTER SET statement or query the INFORMATION\_SCHEMA CHARACTER\_SETS table. For example:

|                 | Charset   Description                                          | +++++<br>  Default collation           | Maxlen            |
|-----------------|----------------------------------------------------------------|----------------------------------------|-------------------|
|                 | +++++<br>  armscii8   ARMSCII-8 Armenian                       | armscii8_general_ci                    | 1                 |
| ascii           | US ASCII                                                       | ascii_general_ci                       | <br>1             |
| big5            | Big5 Traditional Chinese                                       | big5_chinese_ci                        | <br>2             |
| binary          | Binary pseudo charset                                          | binary                                 | <br>1             |
| cp1250          | Windows Central European                                       | cp1250_general_ci                      | <br>1             |
| cp1251          | Windows Cyrillic                                               | cp1251_general_ci                      | <br>1             |
| cp1256          | Windows Arabic                                                 | cp1256_general_ci                      | <br>1             |
| cp1257          | Windows Baltic                                                 | cp1257_general_ci                      | <br>1             |
| cp850           | DOS West European                                              | cp850_general_ci                       | <br>1             |
| cp852           | DOS Central European                                           | cp852_general_ci                       | <br>1             |
| cp866           | DOS Russian                                                    | cp866_general_ci                       | <br>1             |
| cp932           | SJIS for Windows Japanese                                      | cp932_japanese_ci                      | <br>2             |
| dec8            | DEC West European                                              | dec8_swedish_ci                        | <br>1             |
|                 | eucjpms   UJIS for Windows Japanese                            | eucjpms_japanese_ci                    | 3                 |
| euckr           | EUC-KR Korean                                                  | euckr_korean_ci                        | <br>2             |
|                 | gb18030   China National Standard GB18030   gb18030_chinese_ci |                                        | 4                 |
| gb2312          | GB2312 Simplified Chinese                                      | gb2312_chinese_ci                      | <br>2             |
| gbk             | GBK Simplified Chinese                                         | gbk_chinese_ci                         | <br>2             |
|                 | geostd8   GEOSTD8 Georgian                                     | geostd8_general_ci                     | 1                 |
| greek           | ISO 8859-7 Greek                                               | greek_general_ci                       | <br>1             |
| hebrew          | ISO 8859-8 Hebrew                                              | hebrew_general_ci                      | <br>1             |
| hp8             | HP West European                                               | hp8_english_ci                         | <br>1             |
|                 | keybcs2   DOS Kamenicky Czech-Slovak                           | keybcs2_general_ci                     | 1                 |
| koi8r           | KOI8-R Relcom Russian                                          | koi8r_general_ci                       | <br>1             |
| koi8u           | KOI8-U Ukrainian                                               | koi8u_general_ci                       | <br>1             |
| latin1          | cp1252 West European                                           | latin1_swedish_ci                      | <br>1             |
| latin2          | ISO 8859-2 Central European                                    | latin2_general_ci                      | <br>1             |
| latin5          | ISO 8859-9 Turkish                                             | latin5_turkish_ci                      | <br>1             |
| latin7          | ISO 8859-13 Baltic                                             | latin7_general_ci                      | <br>1             |
| macce           | Mac Central European                                           | macce_general_ci                       | <br>1             |
|                 | macroman   Mac West European                                   | macroman_general_ci                    | 1                 |
| sjis            | Shift-JIS Japanese                                             | sjis_japanese_ci                       | <br>2             |
| swe7            | 7bit Swedish                                                   | swe7_swedish_ci                        | <br>1             |
| tis620          | TIS620 Thai                                                    | tis620_thai_ci                         | <br>1             |
| ucs2            | UCS-2 Unicode                                                  | ucs2_general_ci                        | <br>2             |
|                 |                                                                |                                        |                   |
| ujis<br>  utf16 | EUC-JP Japanese<br>  UTF-16 Unicode                            | ujis_japanese_ci<br>  utf16_general_ci | <br>3  <br> <br>4 |
|                 |                                                                |                                        |                   |
|                 | utf16le   UTF-16LE Unicode                                     | utf16le_general_ci                     | 4                 |
| utf32           | UTF-32 Unicode                                                 | utf32_general_ci                       | <br>4             |
|                 | utf8mb3   UTF-8 Unicode                                        | utf8mb3_general_ci                     | 3                 |
|                 | utf8mb4   UTF-8 Unicode                                        | utf8mb4_0900_ai_ci                     | 4                 |

In cases where a character set has multiple collations, it might not be clear which collation is most suitable for a given application. To avoid choosing the wrong collation, it can be helpful to perform some comparisons with representative data values to make sure that a given collation sorts values the way you expect.

### <span id="page-194-1"></span>**12.10.1 Unicode Character Sets**

This section describes the collations available for Unicode character sets and their differentiating properties. For general information about Unicode, see [Section 12.9, "Unicode Support"](#page-186-0).

MySQL supports multiple Unicode character sets:

- utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.
- utf8mb3: A UTF-8 encoding of the Unicode character set using one to three bytes per character. This character set is deprecated; please use utf8mb4 instead.
- utf8: A deprecated alias for utf8mb3. Use utf8mb4 instead.

![](_page_195_Picture_5.jpeg)

#### **Note**

utf8 is expected in a future release to become an alias for utf8mb4.

- ucs2: The UCS-2 encoding of the Unicode character set using two bytes per character. Deprecated; expect support for this character set to be removed in a future version of MySQL.
- utf16: The UTF-16 encoding for the Unicode character set using two or four bytes per character. Like ucs2 but with an extension for supplementary characters.
- utf16le: The UTF-16LE encoding for the Unicode character set. Like utf16 but little-endian rather than big-endian.
- utf32: The UTF-32 encoding for the Unicode character set using four bytes per character.

![](_page_195_Picture_12.jpeg)

#### **Note**

The utf8mb3 character set is deprecated and you should expect it to be removed in a future MySQL release. Please use utf8mb4 instead. utf8 is currently an alias for utf8mb3, but it is now deprecated as such, and utf8 is expected subsequently to become a reference to utf8mb4. utf8mb3 is also displayed in place of utf8 in columns of Information Schema tables, and in the output of SQL SHOW statements.

To avoid ambiguity about the meaning of utf8, consider specifying utf8mb4 explicitly for character set references.

utf8mb4, utf16, utf16le, and utf32 support Basic Multilingual Plane (BMP) characters and supplementary characters that lie outside the BMP. utf8mb3 and ucs2 support only BMP characters.

Most Unicode character sets have a general collation (indicated by \_general in the name or by the absence of a language specifier), a binary collation (indicated by \_bin in the name), and several language-specific collations (indicated by language specifiers). For example, for utf8mb4, utf8mb4\_general\_ci and utf8mb4\_bin are its general and binary collations, and utf8mb4\_danish\_ci is one of its language-specific collations.

Most character sets have a single binary collation. utf8mb4 is an exception that has two: utf8mb4\_bin and utf8mb4\_0900\_bin. These two binary collations have the same sort order but are distinguished by their pad attribute and collating weight characteristics. See [Collation Pad](#page-196-0) [Attributes](#page-196-0), and Character Collating Weights.

Collation support for utf16le is limited. The only collations available are utf16le\_general\_ci and utf16le\_bin. These are similar to utf16\_general\_ci and utf16\_bin.

- [Unicode Collation Algorithm \(UCA\) Versions](#page-196-1)
- [Collation Pad Attributes](#page-196-0)
- [Language-Specific Collations](#page-197-0)
- [\\_general\\_ci Versus \\_unicode\\_ci Collations](#page-199-0)
- Character Collating Weights

• Miscellaneous Information

### <span id="page-196-1"></span>**Unicode Collation Algorithm (UCA) Versions**

MySQL implements the xxx\_unicode\_ci collations according to the Unicode Collation Algorithm (UCA) described at <http://www.unicode.org/reports/tr10/>. The collation uses the version-4.0.0 UCA weight keys: [http://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt.](http://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt) The xxx\_unicode\_ci collations have only partial support for the Unicode Collation Algorithm. Some characters are not supported, and combining marks are not fully supported. This affects languages such as Vietnamese, Yoruba, and Navajo. A combined character is considered different from the same character written with a single unicode character in string comparisons, and the two characters are considered to have a different length (for example, as returned by the CHAR\_LENGTH() function or in result set metadata).

Unicode collations based on UCA versions higher than 4.0.0 include the version in the collation name. Examples:

- utf8mb4\_unicode\_520\_ci is based on UCA 5.2.0 weight keys ([http://www.unicode.org/Public/](http://www.unicode.org/Public/UCA/5.2.0/allkeys.txt) [UCA/5.2.0/allkeys.txt\)](http://www.unicode.org/Public/UCA/5.2.0/allkeys.txt),
- utf8mb4\_0900\_ai\_ci is based on UCA 9.0.0 weight keys ([http://www.unicode.org/Public/](http://www.unicode.org/Public/UCA/9.0.0/allkeys.txt) [UCA/9.0.0/allkeys.txt\)](http://www.unicode.org/Public/UCA/9.0.0/allkeys.txt).

The LOWER() and UPPER() functions perform case folding according to the collation of their argument. A character that has uppercase and lowercase versions only in a Unicode version higher than 4.0.0 is converted by these functions only if the argument collation uses a high enough UCA version.

### <span id="page-196-0"></span>**Collation Pad Attributes**

Collations based on UCA 9.0.0 and higher are faster than collations based on UCA versions prior to 9.0.0. They also have a pad attribute of NO PAD, in contrast to PAD SPACE as used in collations based on UCA versions prior to 9.0.0. For comparison of nonbinary strings, NO PAD collations treat spaces at the end of strings like any other character (see [Trailing Space Handling in Comparisons\)](#page-182-1).

To determine the pad attribute for a collation, use the INFORMATION\_SCHEMA COLLATIONS table, which has a PAD\_ATTRIBUTE column. For example:

```
mysql> SELECT COLLATION_NAME, PAD_ATTRIBUTE
 FROM INFORMATION_SCHEMA.COLLATIONS
 WHERE CHARACTER_SET_NAME = 'utf8mb4';
+----------------------------+---------------+
| COLLATION_NAME | PAD_ATTRIBUTE |
+----------------------------+---------------+
| utf8mb4_general_ci | PAD SPACE |
| utf8mb4_bin | PAD SPACE |
| utf8mb4_unicode_ci | PAD SPACE |
| utf8mb4_icelandic_ci | PAD SPACE |
...
| utf8mb4_0900_ai_ci | NO PAD |
| utf8mb4_de_pb_0900_ai_ci | NO PAD |
| utf8mb4_is_0900_ai_ci | NO PAD |
...
| utf8mb4_ja_0900_as_cs | NO PAD |
| utf8mb4_ja_0900_as_cs_ks | NO PAD |
| utf8mb4_0900_as_ci | NO PAD |
| utf8mb4_ru_0900_ai_ci | NO PAD |
| utf8mb4_ru_0900_as_cs | NO PAD |
| utf8mb4_zh_0900_as_cs | NO PAD |
| utf8mb4_0900_bin | NO PAD |
+----------------------------+---------------+
```

Comparison of nonbinary string values (CHAR, VARCHAR, and TEXT) that have a NO PAD collation differ from other collations with respect to trailing spaces. For example, 'a' and 'a ' compare as different strings, not the same string. This can be seen using the binary collations for utf8mb4. The pad attribute for utf8mb4\_bin is PAD SPACE, whereas for utf8mb4\_0900\_bin it is NO PAD.

Consequently, operations involving utf8mb4\_0900\_bin do not add trailing spaces, and comparisons involving strings with trailing spaces may differ for the two collations:

```
mysql> CREATE TABLE t1 (c CHAR(10) COLLATE utf8mb4_bin);
Query OK, 0 rows affected (0.03 sec)
mysql> INSERT INTO t1 VALUES('a');
Query OK, 1 row affected (0.01 sec)
mysql> SELECT * FROM t1 WHERE c = 'a ';
+------+
| c |
+------+
| a |
+------+
1 row in set (0.00 sec)
mysql> ALTER TABLE t1 MODIFY c CHAR(10) COLLATE utf8mb4_0900_bin;
Query OK, 0 rows affected (0.02 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SELECT * FROM t1 WHERE c = 'a ';
Empty set (0.00 sec)
```

### <span id="page-197-0"></span>**Language-Specific Collations**

MySQL implements language-specific Unicode collations if the ordering based only on the Unicode Collation Algorithm (UCA) does not work well for a language. Language-specific collations are UCAbased, with additional language tailoring rules. Examples of such rules appear later in this section. For questions about particular language orderings,<http://unicode.org> provides Common Locale Data Repository (CLDR) collation charts at <http://www.unicode.org/cldr/charts/30/collation/index.html>.

For example, the nonlanguage-specific utf8mb4\_0900\_ai\_ci and language-specific utf8mb4\_LOCALE\_0900\_ai\_ci Unicode collations each have these characteristics:

- The collation is based on UCA 9.0.0 and CLDR v30, is accent-insensitive and case-insensitive. These characteristics are indicated by \_0900, \_ai, and \_ci in the collation name. Exception: utf8mb4\_la\_0900\_ai\_ci is not based on CLDR because Classical Latin is not defined in CLDR.
- The collation works for all characters in the range [U+0, U+10FFFF].
- If the collation is not language specific, it sorts all characters, including supplementary characters, in default order (described following). If the collation is language specific, it sorts characters of the language correctly according to language-specific rules, and characters not in the language in default order.
- By default, the collation sorts characters having a code point listed in the DUCET table (Default Unicode Collation Element Table) according to the weight value assigned in the table. The collation sorts characters not having a code point listed in the DUCET table using their implicit weight value, which is constructed according to the UCA.
- For non-language-specific collations, characters in contraction sequences are treated as separate characters. For language-specific collations, contractions might change character sorting order.

A collation name that includes a locale code or language name shown in the following table is a language-specific collation. Unicode character sets may include collations for one or more of these languages.

**Table 12.3 Unicode Collation Language Specifiers**

| Language  | Language Specifier |
|-----------|--------------------|
| Bosnian   | bs                 |
| Bulgarian | bg                 |

| Language                | Language Specifier  |  |
|-------------------------|---------------------|--|
| Chinese                 | zh                  |  |
| Classical Latin         | la or roman         |  |
| Croatian                | hr or croatian      |  |
| Czech                   | cs or czech         |  |
| Danish                  | da or danish        |  |
| Esperanto               | eo or esperanto     |  |
| Estonian                | et or estonian      |  |
| Galician                | gl                  |  |
| German phone book order | de_pb or german2    |  |
| Hungarian               | hu or hungarian     |  |
| Icelandic               | is or icelandic     |  |
| Japanese                | ja                  |  |
| Latvian                 | lv or latvian       |  |
| Lithuanian              | lt or lithuanian    |  |
| Mongolian               | mn                  |  |
| Norwegian / Bokmål      | nb                  |  |
| Norwegian / Nynorsk     | nn                  |  |
| Persian                 | persian             |  |
| Polish                  | pl or polish        |  |
| Romanian                | ro or romanian      |  |
| Russian                 | ru                  |  |
| Serbian                 | sr                  |  |
| Sinhala                 | sinhala             |  |
| Slovak                  | sk or slovak        |  |
| Slovenian               | sl or slovenian     |  |
| Modern Spanish          | es or spanish       |  |
| Traditional Spanish     | es_trad or spanish2 |  |
| Swedish                 | sv or swedish       |  |
| Turkish                 | tr or turkish       |  |
| Vietnamese              | vi or vietnamese    |  |

MySQL provides the Bulgarian collations utf8mb4\_bg\_0900\_ai\_ci and utf8mb4\_bg\_0900\_as\_cs.

Croatian collations are tailored for these Croatian letters: Č, Ć, Dž, Đ, Lj, Nj, Š, Ž.

MySQL provides the utf8mb4\_sr\_latn\_0900\_ai\_ci and utf8mb4\_sr\_latn\_0900\_as\_cs collations for Serbian and the utf8mb4\_bs\_0900\_ai\_ci and utf8mb4\_bs\_0900\_as\_cs collations for Bosnian, when these languages are written with the Latin alphabet.

MySQL provides collations for both major varieties of Norwegian: for Bokmål, you can use utf8mb4\_nb\_0900\_ai\_ci and utf8mb4\_nb\_0900\_as\_cs; for Nynorsk, MySQL now provides utf8mb4\_nn\_0900\_ai\_ci and utf8mb4\_nn\_0900\_as\_cs.

For Japanese, the utf8mb4 character set includes utf8mb4\_ja\_0900\_as\_cs and utf8mb4\_ja\_0900\_as\_cs\_ks collations. Both collations are accent-sensitive and case-sensitive. utf8mb4\_ja\_0900\_as\_cs\_ks is also kana-sensitive and distinguishes Katakana characters from Hiragana characters, whereas utf8mb4\_ja\_0900\_as\_cs treats Katakana and Hiragana characters as equal for sorting. Applications that require a Japanese collation but not kana sensitivity may use utf8mb4\_ja\_0900\_as\_cs for better sort performance. utf8mb4\_ja\_0900\_as\_cs uses three weight levels for sorting; utf8mb4\_ja\_0900\_as\_cs\_ks uses four.

For Classical Latin collations that are accent-insensitive, I and J compare as equal, and U and V compare as equal. I and J, and U and V compare as equal on the base letter level. In other words, J is regarded as an accented I, and U is regarded as an accented V.

MySQL provides collations for the Mongolian language when written with Cyrillic characters, utf8mb4\_mn\_cyrl\_0900\_ai\_ci and utf8mb4\_mn\_cyrl\_0900\_as\_cs.

Spanish collations are available for modern and traditional Spanish. For both, ñ (n-tilde) is a separate letter between n and o. In addition, for traditional Spanish, ch is a separate letter between c and d, and ll is a separate letter between l and m.

Traditional Spanish collations may also be used for Asturian and Galician. MySQL also provides utf8mb4\_gl\_0900\_ai\_ci and utf8mb4\_gl\_0900\_as\_cs collations for Galician. (These are the same collations as utf8mb4\_es\_0900\_ai\_ci and utf8mb4\_es\_0900\_as\_cs, respectively.)

Swedish collations include Swedish rules. For example, in Swedish, the following relationship holds, which is not something expected by a German or French speaker:

Ü = Y < Ö

#### <span id="page-199-0"></span>**\_general\_ci Versus \_unicode\_ci Collations**

For any Unicode character set, operations performed using the xxx\_general\_ci collation are faster than those for the xxx\_unicode\_ci collation. For example, comparisons for the utf8mb4\_general\_ci collation are faster, but slightly less correct, than comparisons for utf8mb4\_unicode\_ci. The reason is that utf8mb4\_unicode\_ci supports mappings such as expansions; that is, when one character compares as equal to combinations of other characters. For example, ß is equal to ss in German and some other languages. utf8mb4\_unicode\_ci also supports contractions and ignorable characters. utf8mb4\_general\_ci is a legacy collation that does not support expansions, contractions, or ignorable characters. It can make only one-to-one comparisons between characters.

To further illustrate, the following equalities hold in both utf8mb4\_general\_ci and utf8mb4\_unicode\_ci (for the effect of this in comparisons or searches, see [Section 12.8.6,](#page-183-0) ["Examples of the Effect of Collation"\)](#page-183-0):

```
Ä = A
Ö = O
Ü = U
```

A difference between the collations is that this is true for utf8mb4\_general\_ci:

```
ß = s
```

Whereas this is true for utf8mb4\_unicode\_ci, which supports the German DIN-1 ordering (also known as dictionary order):

```
ß = ss
```

MySQL implements language-specific Unicode collations if the ordering with utf8mb4\_unicode\_ci does not work well for a language. For example, utf8mb4\_unicode\_ci works fine for German dictionary order and French, so there is no need to create special utf8mb4 collations.

utf8mb4\_general\_ci also is satisfactory for both German and French, except that ß is equal to s, and not to ss. If this is acceptable for your application, you should use utf8mb4\_general\_ci because it is faster. If this is not acceptable (for example, if you require German dictionary order), use utf8mb4\_unicode\_ci because it is more accurate.

If you require German DIN-2 (phone book) ordering, use the utf8mb4\_german2\_ci collation, which compares the following sets of characters equal:

```
Ä = Æ = AE
Ö = Œ = OE
Ü = UE
ß = ss
```

utf8mb4\_german2\_ci is similar to latin1\_german2\_ci, but the latter does not compare Æ equal to AE or Œ equal to OE. There is no utf8mb4\_german\_ci corresponding to latin1\_german\_ci for German dictionary order because utf8mb4\_general\_ci suffices.

## **Character Collating Weights**

A character's collating weight is determined as follows:

- For all Unicode collations except the \_bin (binary) collations, MySQL performs a table lookup to find a character's collating weight.
- For \_bin collations except utf8mb4\_0900\_bin, the weight is based on the code point, possibly with leading zero bytes added.
- For utf8mb4\_0900\_bin, the weight is the utf8mb4 encoding bytes. The sort order is the same as for utf8mb4\_bin, but much faster.

Collating weights can be displayed using the [WEIGHT\\_STRING\(\)](#page-199-0) function. (See [Section 14.8, "String](#page-186-0) [Functions and Operators"](#page-186-0).) If a collation uses a weight lookup table, but a character is not in the table (for example, because it is a "new" character), collating weight determination becomes more complex:

- For BMP characters in general collations (xxx\_general\_ci), the weight is the code point.
- For BMP characters in UCA collations (for example, xxx\_unicode\_ci and language-specific collations), the following algorithm applies:

```
if (code >= 0x3400 && code <= 0x4DB5)
 base= 0xFB80; /* CJK Ideograph Extension */
else if (code >= 0x4E00 && code <= 0x9FA5)
 base= 0xFB40; /* CJK Ideograph */
else
 base= 0xFBC0; /* All other characters */
aaaa= base + (code >> 15);
bbbb= (code & 0x7FFF) | 0x8000;
```

The result is a sequence of two collating elements, aaaa followed by bbbb. For example:

```
mysql> SELECT HEX(WEIGHT_STRING(_ucs2 0x04CF COLLATE ucs2_unicode_ci));
+----------------------------------------------------------+
| HEX(WEIGHT_STRING(_ucs2 0x04CF COLLATE ucs2_unicode_ci)) |
+----------------------------------------------------------+
| FBC084CF |
+----------------------------------------------------------+
```

Thus, U+04cf CYRILLIC SMALL LETTER PALOCHKA (ӏ) is, with all UCA 4.0.0 collations, greater than U+04c0 CYRILLIC LETTER PALOCHKA (Ӏ). With UCA 5.2.0 collations, all palochkas sort together.

• For supplementary characters in general collations, the weight is the weight for 0xfffd REPLACEMENT CHARACTER. For supplementary characters in UCA 4.0.0 collations, their collating weight is 0xfffd. That is, to MySQL, all supplementary characters are equal to each other, and greater than almost all BMP characters.

An example with Deseret characters and COUNT(DISTINCT):

```
CREATE TABLE t (s1 VARCHAR(5) CHARACTER SET utf32 COLLATE utf32_unicode_ci);
INSERT INTO t VALUES (0xfffd); /* REPLACEMENT CHARACTER */
INSERT INTO t VALUES (0x010412); /* DESERET CAPITAL LETTER BEE */
```

```
INSERT INTO t VALUES (0x010413); /* DESERET CAPITAL LETTER TEE */
SELECT COUNT(DISTINCT s1) FROM t;
```

The result is 2 because in the MySQL xxx\_unicode\_ci collations, the replacement character has a weight of 0x0dc6, whereas Deseret Bee and Deseret Tee both have a weight of 0xfffd. (Were the utf32\_general\_ci collation used instead, the result is 1 because all three characters have a weight of 0xfffd in that collation.)

An example with cuneiform characters and [WEIGHT\\_STRING\(\)](#page-199-0):

```
/*
The four characters in the INSERT string are
00000041 # LATIN CAPITAL LETTER A
0001218F # CUNEIFORM SIGN KAB
000121A7 # CUNEIFORM SIGN KISH
00000042 # LATIN CAPITAL LETTER B
*/
CREATE TABLE t (s1 CHAR(4) CHARACTER SET utf32 COLLATE utf32_unicode_ci);
INSERT INTO t VALUES (0x000000410001218f000121a700000042);
SELECT HEX(WEIGHT_STRING(s1)) FROM t;
```

#### The result is:

```
0E33 FFFD FFFD 0E4A
```

0E33 and 0E4A are primary weights as in [UCA 4.0.0](ftp://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt). FFFD is the weight for KAB and also for KISH.

The rule that all supplementary characters are equal to each other is nonoptimal but is not expected to cause trouble. These characters are very rare, so it is very rare that a multi-character string consists entirely of supplementary characters. In Japan, since the supplementary characters are obscure Kanji ideographs, the typical user does not care what order they are in, anyway. If you really want rows sorted by the MySQL rule and secondarily by code point value, it is easy:

```
ORDER BY s1 COLLATE utf32_unicode_ci, s1 COLLATE utf32_bin
```

• For supplementary characters based on UCA versions higher than 4.0.0 (for example, xxx\_unicode\_520\_ci), supplementary characters do not necessarily all have the same collating weight. Some have explicit weights from the UCA allkeys.txt file. Others have weights calculated from this algorithm:

```
aaaa= base + (code >> 15);
bbbb= (code & 0x7FFF) | 0x8000;
```

There is a difference between "ordering by the character's code value" and "ordering by the character's binary representation," a difference that appears only with utf16\_bin, because of surrogates.

Suppose that utf16\_bin (the binary collation for utf16) was a binary comparison "byte by byte" rather than "character by character." If that were so, the order of characters in utf16\_bin would differ from the order in utf8mb4\_bin. For example, the following chart shows two rare characters. The first character is in the range E000-FFFF, so it is greater than a surrogate but less than a supplementary. The second character is a supplementary.

```
Code point Character utf8mb4 utf16
---------- --------- ------- -----
0FF9D HALFWIDTH KATAKANA LETTER N EF BE 9D FF 9D
10384 UGARITIC LETTER DELTA F0 90 8E 84 D8 00 DF 84
```

The two characters in the chart are in order by code point value because 0xff9d < 0x10384. And they are in order by utf8mb4 value because 0xef < 0xf0. But they are not in order by utf16 value, if we use byte-by-byte comparison, because 0xff > 0xd8.

So MySQL's utf16\_bin collation is not "byte by byte." It is "by code point." When MySQL sees a supplementary-character encoding in utf16, it converts to the character's code-point value, and then compares. Therefore, utf8mb4\_bin and utf16\_bin are the same ordering. This is consistent with

the SQL:2008 standard requirement for a UCS\_BASIC collation: "UCS\_BASIC is a collation in which the ordering is determined entirely by the Unicode scalar values of the characters in the strings being sorted. It is applicable to the UCS character repertoire. Since every character repertoire is a subset of the UCS repertoire, the UCS\_BASIC collation is potentially applicable to every character set. NOTE 11: The Unicode scalar value of a character is its code point treated as an unsigned integer."

If the character set is ucs2, comparison is byte-by-byte, but ucs2 strings should not contain surrogates, anyway.

### **Miscellaneous Information**

The xxx\_general\_mysql500\_ci collations preserve the pre-5.1.24 ordering of the original xxx\_general\_ci collations and permit upgrades for tables created before MySQL 5.1.24 (Bug #27877).