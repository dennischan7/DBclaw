---
source: MySQL 8.4 Reference
title: 00_Overview
---

The MySQL server has a compiled-in default character set and collation. To change these defaults, use the --character-set-server and --collation-server options when you start the server. See Section 7.1.7, "Server Command Options". The collation must be a legal collation for the default character set. To determine which collations are available for each character set, use the SHOW COLLATION statement or query the INFORMATION\_SCHEMA COLLATIONS table.

If you try to use a character set that is not compiled into your binary, you might run into the following problems:

• If your program uses an incorrect path to determine where the character sets are stored (which is typically the share/mysql/charsets or share/charsets directory under the MySQL installation directory), this can be fixed by using the --character-sets-dir option when you run the program. For example, to specify a directory to be used by MySQL client programs, list it in the [client] group of your option file. The examples given here show what the setting might look like for Unix or Windows, respectively:

```
[client]
character-sets-dir=/usr/local/mysql/share/mysql/charsets
[client]
character-sets-dir="C:/Program Files/MySQL/MySQL Server 8.4/share/charsets"
```

• If the character set is a complex character set that cannot be loaded dynamically, you must recompile the program with support for the character set.

For Unicode character sets, you can define collations without recompiling by using LDML notation. See [Section 12.14.4, "Adding a UCA Collation to a Unicode Character Set".](#page-21-0)

- If the character set is a dynamic character set, but you do not have a configuration file for it, you should install the configuration file for the character set from a new MySQL distribution.
- If your character set index file (Index.xml) does not contain the name for the character set, your program displays an error message:

```
Character set 'charset_name' is not a compiled character set and is not
specified in the '/usr/share/mysql/charsets/Index.xml' file
```

To solve this problem, you should either get a new index file or manually add the name of any missing character sets to the current file.

You can force client programs to use specific character set as follows:

```
[client]
default-character-set=charset_name
```

This is normally unnecessary. However, when character\_set\_system differs from character\_set\_server or character\_set\_client, and you input characters manually (as database object identifiers, column values, or both), these may be displayed incorrectly in output from the client or the output itself may be formatted incorrectly. In such cases, starting the mysql client with --default-character-set=system\_character\_set—that is, setting the client character set to match the system character set—should fix the problem.

# <span id="page-28-0"></span>**12.16 MySQL Server Locale Support**

The locale indicated by the lc\_time\_names system variable controls the language used to display day and month names and abbreviations. This variable affects the output from the [DATE\\_FORMAT\(\)](#page-169-0), [DAYNAME\(\)](#page-171-0), and [MONTHNAME\(\)](#page-174-0) functions.

```
lc_time_names does not affect the STR_TO_DATE() or GET_FORMAT() function.
```

The lc\_time\_names value does not affect the result from [FORMAT\(\)](#page-191-0), but this function takes an optional third parameter that enables a locale to be specified to be used for the result number's decimal point, thousands separator, and grouping between separators. Permissible locale values are the same as the legal values for the lc\_time\_names system variable.

Locale names have language and region subtags listed by IANA [\(http://www.iana.org/assignments/](http://www.iana.org/assignments/language-subtag-registry) [language-subtag-registry\)](http://www.iana.org/assignments/language-subtag-registry) such as 'ja\_JP' or 'pt\_BR'. The default value is 'en\_US' regardless of your system's locale setting, but you can set the value at server startup, or set the GLOBAL value at runtime if you have privileges sufficient to set global system variables; see Section 7.1.9.1, "System Variable Privileges". Any client can examine the value of lc\_time\_names or set its SESSION value to affect the locale for its own connection.

(The first SET NAMES statement in the following example may not be necessary if no settings relating to character set and collation have been changed from their defaults; we include it for completeness.)

```
mysql> SET NAMES 'utf8mb4';
Query OK, 0 rows affected (0.09 sec)
mysql> SELECT @@lc_time_names;
+-----------------+
| @@lc_time_names |
+-----------------+
| en_US |
+-----------------+
1 row in set (0.00 sec)
mysql> SELECT DAYNAME('2020-01-01'), MONTHNAME('2020-01-01');
+-----------------------+-------------------------+
| DAYNAME('2020-01-01') | MONTHNAME('2020-01-01') |
+-----------------------+-------------------------+
| Wednesday | January |
+-----------------------+-------------------------+
1 row in set (0.00 sec)
mysql> SELECT DATE_FORMAT('2020-01-01','%W %a %M %b');
+-----------------------------------------+
| DATE_FORMAT('2020-01-01','%W %a %M %b') |
+-----------------------------------------+
| Wednesday Wed January Jan |
+-----------------------------------------+
1 row in set (0.00 sec)
mysql> SET lc_time_names = 'es_MX';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@lc_time_names;
+-----------------+
| @@lc_time_names |
+-----------------+
| es_MX |
+-----------------+
1 row in set (0.00 sec)
mysql> SELECT DAYNAME('2020-01-01'), MONTHNAME('2020-01-01');
+-----------------------+-------------------------+
| DAYNAME('2020-01-01') | MONTHNAME('2020-01-01') |
+-----------------------+-------------------------+
| miércoles | enero |
+-----------------------+-------------------------+
1 row in set (0.00 sec)
mysql> SELECT DATE_FORMAT('2020-01-01','%W %a %M %b');
+-----------------------------------------+
| DATE_FORMAT('2020-01-01','%W %a %M %b') |
+-----------------------------------------+
| miércoles mié enero ene |
+-----------------------------------------+
1 row in set (0.00 sec)
```

The day or month name for each of the affected functions is converted from utf8mb4 to the character set indicated by the character\_set\_connection system variable.

lc\_time\_names may be set to any of the following locale values. The set of locales supported by MySQL may differ from those supported by your operating system.

| Locale Value | Meaning                       |
|--------------|-------------------------------|
| ar_AE        | Arabic - United Arab Emirates |
| ar_BH        | Arabic - Bahrain              |
| ar_DZ        | Arabic - Algeria              |
| ar_EG        | Arabic - Egypt                |
| ar_IN        | Arabic - India                |
| ar_IQ        | Arabic - Iraq                 |

| Locale Value | Meaning                      |
|--------------|------------------------------|
| ar_JO        | Arabic - Jordan              |
| ar_KW        | Arabic - Kuwait              |
| ar_LB        | Arabic - Lebanon             |
| ar_LY        | Arabic - Libya               |
| ar_MA        | Arabic - Morocco             |
| ar_OM        | Arabic - Oman                |
| ar_QA        | Arabic - Qatar               |
| ar_SA        | Arabic - Saudi Arabia        |
| ar_SD        | Arabic - Sudan               |
| ar_SY        | Arabic - Syria               |
| ar_TN        | Arabic - Tunisia             |
| ar_YE        | Arabic - Yemen               |
| be_BY        | Belarusian - Belarus         |
| bg_BG        | Bulgarian - Bulgaria         |
| ca_ES        | Catalan - Spain              |
| cs_CZ        | Czech - Czech Republic       |
| da_DK        | Danish - Denmark             |
| de_AT        | German - Austria             |
| de_BE        | German - Belgium             |
| de_CH        | German - Switzerland         |
| de_DE        | German - Germany             |
| de_LU        | German - Luxembourg          |
| el_GR        | Greek - Greece               |
| en_AU        | English - Australia          |
| en_CA        | English - Canada             |
| en_GB        | English - United Kingdom     |
| en_IN        | English - India              |
| en_NZ        | English - New Zealand        |
| en_PH        | English - Philippines        |
| en_US        | English - United States      |
| en_ZA        | English - South Africa       |
| en_ZW        | English - Zimbabwe           |
| es_AR        | Spanish - Argentina          |
| es_BO        | Spanish - Bolivia            |
| es_CL        | Spanish - Chile              |
| es_CO        | Spanish - Colombia           |
| es_CR        | Spanish - Costa Rica         |
| es_DO        | Spanish - Dominican Republic |
| es_EC        | Spanish - Ecuador            |
| es_ES        | Spanish - Spain              |
| es_GT        | Spanish - Guatemala          |

| Locale Value | Meaning                      |
|--------------|------------------------------|
| es_HN        | Spanish - Honduras           |
| es_MX        | Spanish - Mexico             |
| es_NI        | Spanish - Nicaragua          |
| es_PA        | Spanish - Panama             |
| es_PE        | Spanish - Peru               |
| es_PR        | Spanish - Puerto Rico        |
| es_PY        | Spanish - Paraguay           |
| es_SV        | Spanish - El Salvador        |
| es_US        | Spanish - United States      |
| es_UY        | Spanish - Uruguay            |
| es_VE        | Spanish - Venezuela          |
| et_EE        | Estonian - Estonia           |
| eu_ES        | Basque - Spain               |
| fi_FI        | Finnish - Finland            |
| fo_FO        | Faroese - Faroe Islands      |
| fr_BE        | French - Belgium             |
| fr_CA        | French - Canada              |
| fr_CH        | French - Switzerland         |
| fr_FR        | French - France              |
| fr_LU        | French - Luxembourg          |
| gl_ES        | Galician - Spain             |
| gu_IN        | Gujarati - India             |
| he_IL        | Hebrew - Israel              |
| hi_IN        | Hindi - India                |
| hr_HR        | Croatian - Croatia           |
| hu_HU        | Hungarian - Hungary          |
| id_ID        | Indonesian - Indonesia       |
| is_IS        | Icelandic - Iceland          |
| it_CH        | Italian - Switzerland        |
| it_IT        | Italian - Italy              |
| ja_JP        | Japanese - Japan             |
| ko_KR        | Korean - Republic of Korea   |
| lt_LT        | Lithuanian - Lithuania       |
| lv_LV        | Latvian - Latvia             |
| mk_MK        | Macedonian - North Macedonia |
| mn_MN        | Mongolia - Mongolian         |
| ms_MY        | Malay - Malaysia             |
| nb_NO        | Norwegian(Bokmål) - Norway   |
| nl_BE        | Dutch - Belgium              |
| nl_NL        | Dutch - The Netherlands      |
| no_NO        | Norwegian - Norway           |

| Locale Value | Meaning               |
|--------------|-----------------------|
| pl_PL        | Polish - Poland       |
| pt_BR        | Portugese - Brazil    |
| pt_PT        | Portugese - Portugal  |
| rm_CH        | Romansh - Switzerland |
| ro_RO        | Romanian - Romania    |
| ru_RU        | Russian - Russia      |
| ru_UA        | Russian - Ukraine     |
| sk_SK        | Slovak - Slovakia     |
| sl_SI        | Slovenian - Slovenia  |
| sq_AL        | Albanian - Albania    |
| sr_RS        | Serbian - Serbia      |
| sv_FI        | Swedish - Finland     |
| sv_SE        | Swedish - Sweden      |
| ta_IN        | Tamil - India         |
| te_IN        | Telugu - India        |
| th_TH        | Thai - Thailand       |
| tr_TR        | Turkish - Turkey      |
| uk_UA        | Ukrainian - Ukraine   |
| ur_PK        | Urdu - Pakistan       |
| vi_VN        | Vietnamese - Vietnam  |
| zh_CN        | Chinese - China       |
| zh_HK        | Chinese - Hong Kong   |
| zh_TW        | Chinese - Taiwan      |

# Chapter 13 Data Types

# **Table of Contents**

| 13.1 Numeric Data Types 2006                                                     |      |
|----------------------------------------------------------------------------------|------|
| 13.1.1 Numeric Data Type Syntax 2006                                             |      |
| 13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, |      |
| BIGINT 2010                                                                      |      |
| 13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC 2010                   |      |
| 13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE                  | 2011 |
| 13.1.5 Bit-Value Type - BIT 2011                                                 |      |
| 13.1.6 Numeric Type Attributes 2011                                              |      |
| 13.1.7 Out-of-Range and Overflow Handling 2013                                   |      |
| 13.2 Date and Time Data Types 2014                                               |      |
| 13.2.1 Date and Time Data Type Syntax 2015                                       |      |
| 13.2.2 The DATE, DATETIME, and TIMESTAMP Types 2017                              |      |
| 13.2.3 The TIME Type 2019                                                        |      |
| 13.2.4 The YEAR Type 2019                                                        |      |
| 13.2.5 Automatic Initialization and Updating for TIMESTAMP and DATETIME          | 2020 |
| 13.2.6 Fractional Seconds in Time Values 2023                                    |      |
| 13.2.7 What Calendar Is Used By MySQL? 2024                                      |      |
| 13.2.8 Conversion Between Date and Time Types 2025                               |      |
| 13.2.9 2-Digit Years in Dates 2026                                               |      |
| 13.3 String Data Types 2026                                                      |      |
| 13.3.1 String Data Type Syntax 2026                                              |      |
| 13.3.2 The CHAR and VARCHAR Types 2030                                           |      |
| 13.3.3 The BINARY and VARBINARY Types 2031                                       |      |
| 13.3.4 The BLOB and TEXT Types                                                   | 2032 |
| 13.3.5 The ENUM Type                                                             | 2034 |
| 13.3.6 The SET Type 2037                                                         |      |
| 13.4 Spatial Data Types 2039                                                     |      |
|                                                                                  |      |
| 13.4.1 Spatial Data Types 2041                                                   |      |
| 13.4.2 The OpenGIS Geometry Model 2042                                           |      |
| 13.4.3 Supported Spatial Data Formats 2047                                       |      |
| 13.4.4 Geometry Well-Formedness and Validity 2050                                |      |
| 13.4.5 Spatial Reference System Support 2051                                     |      |
| 13.4.6 Creating Spatial Columns 2052                                             |      |
| 13.4.7 Populating Spatial Columns 2052                                           |      |
| 13.4.8 Fetching Spatial Data 2053                                                |      |
| 13.4.9 Optimizing Spatial Analysis 2054                                          |      |
| 13.4.10 Creating Spatial Indexes 2054                                            |      |
| 13.4.11 Using Spatial Indexes 2055                                               |      |
| 13.5 The JSON Data Type 2057                                                     |      |
| 13.6 Data Type Default Values 2072                                               |      |
| 13.7 Data Type Storage Requirements 2075                                         |      |
| 13.8 Choosing the Right Type for a Column 2079                                   |      |
| 13.9 Using Data Types from Other Database Engines 2079                           |      |

MySQL supports SQL data types in several categories: numeric types, date and time types, string (character and byte) types, spatial types, and the [JSON](#page-86-0) data type. This chapter provides an overview and more detailed description of the properties of the types in each category, and a summary of the data type storage requirements. The initial overviews are intentionally brief. Consult the more detailed descriptions for additional information about particular data types, such as the permissible formats in which you can specify values.

Data type descriptions use these conventions:

- For integer types, M indicates the maximum display width. For floating-point and fixed-point types, M is the total number of digits that can be stored (the precision). For string types, M is the maximum length. The maximum permissible value of M depends on the data type.
- D applies to floating-point and fixed-point types and indicates the number of digits following the decimal point (the scale). The maximum possible value is 30, but should be no greater than M−2.
- fsp applies to the [TIME](#page-48-0), [DATETIME](#page-46-0), and [TIMESTAMP](#page-46-0) types and represents fractional seconds precision; that is, the number of digits following the decimal point for fractional parts of seconds. The fsp value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0. (This differs from the standard SQL default of 6, for compatibility with previous MySQL versions.)
- Square brackets ([ and ]) indicate optional parts of type definitions.

# <span id="page-35-0"></span>**13.1 Numeric Data Types**

MySQL supports all standard SQL numeric data types. These types include the exact numeric data types ([INTEGER](#page-39-0), [SMALLINT](#page-39-0), [DECIMAL](#page-39-1), and [NUMERIC](#page-39-1)), as well as the approximate numeric data types ([FLOAT](#page-40-0), [REAL](#page-40-0), and [DOUBLE PRECISION](#page-40-0)). The keyword [INT](#page-39-0) is a synonym for [INTEGER](#page-39-0), and the keywords [DEC](#page-39-1) and [FIXED](#page-39-1) are synonyms for [DECIMAL](#page-39-1). MySQL treats [DOUBLE](#page-40-0) as a synonym for [DOUBLE PRECISION](#page-40-0) (a nonstandard extension). MySQL also treats [REAL](#page-40-0) as a synonym for [DOUBLE](#page-40-0) [PRECISION](#page-40-0) (a nonstandard variation), unless the REAL\_AS\_FLOAT SQL mode is enabled.

The [BIT](#page-40-1) data type stores bit values and is supported for MyISAM, MEMORY, InnoDB, and NDB tables.

For information about how MySQL handles assignment of out-of-range values to columns and overflow during expression evaluation, see [Section 13.1.7, "Out-of-Range and Overflow Handling"](#page-42-0).

For information about storage requirements of the numeric data types, see [Section 13.7, "Data Type](#page-104-0) [Storage Requirements"](#page-104-0).

For descriptions of functions that operate on numeric values, see [Section 14.6, "Numeric Functions](#page-151-0) [and Operators"](#page-151-0). The data type used for the result of a calculation on numeric operands depends on the types of the operands and the operations performed on them. For more information, see [Section 14.6.1, "Arithmetic Operators".](#page-152-0)

# <span id="page-35-1"></span>**13.1.1 Numeric Data Type Syntax**

For integer data types, M indicates the minimum display width. The maximum display width is 255. Display width is unrelated to the range of values a type can store, as described in [Section 13.1.6,](#page-40-2) ["Numeric Type Attributes".](#page-40-2)

For floating-point and fixed-point data types, M is the total number of digits that can be stored.

The display width attribute is deprecated for integer data types; you should expect support for it to be removed in a future version of MySQL.

If you specify ZEROFILL for a numeric column, MySQL automatically adds the UNSIGNED attribute to the column.

The ZEROFILL attribute is deprecated for numeric data types; you should expect support for it to be removed in a future version of MySQL. Consider using an alternative means of producing the effect of this attribute. For example, applications could use the [LPAD\(\)](#page-194-0) function to zero-pad numbers up to the desired width, or they could store the formatted numbers in [CHAR](#page-59-0) columns.

Numeric data types that permit the UNSIGNED attribute also permit SIGNED. However, these data types are signed by default, so the SIGNED attribute has no effect.

The UNSIGNED attribute is deprecated for columns of type [FLOAT](#page-40-0), [DOUBLE](#page-40-0), and [DECIMAL](#page-39-1) (and any synonyms); you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

SERIAL is an alias for BIGINT UNSIGNED NOT NULL AUTO\_INCREMENT UNIQUE.

SERIAL DEFAULT VALUE in the definition of an integer column is an alias for NOT NULL AUTO\_INCREMENT UNIQUE.

![](_page_36_Picture_4.jpeg)

#### **Warning**

When you use subtraction between integer values where one is of type UNSIGNED, the result is unsigned unless the NO\_UNSIGNED\_SUBTRACTION SQL mode is enabled. See Section 14.10, "Cast Functions and Operators".

• [BIT\[\(](#page-40-1)M)]

A bit-value type. M indicates the number of bits per value, from 1 to 64. The default is 1 if M is omitted.

• TINYINT[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

A very small integer. The signed range is -128 to 127. The unsigned range is 0 to 255.

• [BOOL](#page-39-0), [BOOLEAN](#page-39-0)

These types are synonyms for [TINYINT\(1\)](#page-39-0). A value of zero is considered false. Nonzero values are considered true:

```
mysql> SELECT IF(0, 'true', 'false');
+------------------------+
| IF(0, 'true', 'false') |
+------------------------+
| false |
+------------------------+
mysql> SELECT IF(1, 'true', 'false');
+------------------------+
| IF(1, 'true', 'false') |
+------------------------+
| true |
+------------------------+
mysql> SELECT IF(2, 'true', 'false');
+------------------------+
| IF(2, 'true', 'false') |
+------------------------+
| true |
+------------------------+
```

However, the values TRUE and FALSE are merely aliases for 1 and 0, respectively, as shown here:

```
mysql> SELECT IF(0 = FALSE, 'true', 'false');
+--------------------------------+
| IF(0 = FALSE, 'true', 'false') |
+--------------------------------+
| true |
+--------------------------------+
mysql> SELECT IF(1 = TRUE, 'true', 'false');
+-------------------------------+
| IF(1 = TRUE, 'true', 'false') |
+-------------------------------+
| true |
+-------------------------------+
mysql> SELECT IF(2 = TRUE, 'true', 'false');
+-------------------------------+
| IF(2 = TRUE, 'true', 'false') |
+-------------------------------+
```

```
| false |
+-------------------------------+
mysql> SELECT IF(2 = FALSE, 'true', 'false');
+--------------------------------+
| IF(2 = FALSE, 'true', 'false') |
+--------------------------------+
| false |
+--------------------------------+
```

The last two statements display the results shown because 2 is equal to neither 1 nor 0.

• SMALLINT[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

A small integer. The signed range is -32768 to 32767. The unsigned range is 0 to 65535.

• MEDIUMINT[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

A medium-sized integer. The signed range is -8388608 to 8388607. The unsigned range is 0 to 16777215.

• INT[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

A normal-size integer. The signed range is -2147483648 to 2147483647. The unsigned range is 0 to 4294967295.

• INTEGER[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

This type is a synonym for [INT](#page-39-0).

• BIGINT[(M[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-0)

A large integer. The signed range is -9223372036854775808 to 9223372036854775807. The unsigned range is 0 to 18446744073709551615.

SERIAL is an alias for BIGINT UNSIGNED NOT NULL AUTO\_INCREMENT UNIQUE.

Some things you should be aware of with respect to [BIGINT](#page-39-0) columns:

• All arithmetic is done using signed [BIGINT](#page-39-0) or [DOUBLE](#page-40-0) values, so you should not use unsigned big integers larger than 9223372036854775807 (63 bits) except with bit functions! If you do that, some of the last digits in the result may be wrong because of rounding errors when converting a [BIGINT](#page-39-0) value to a [DOUBLE](#page-40-0).

MySQL can handle [BIGINT](#page-39-0) in the following cases:

- When using integers to store large unsigned values in a [BIGINT](#page-39-0) column.
- In MIN(col\_name) or MAX(col\_name), where col\_name refers to a [BIGINT](#page-39-0) column.
- When using operators ([+](#page-153-0), [-](#page-153-1), [\\*](#page-154-0), and so on) where both operands are integers.
- You can always store an exact integer value in a [BIGINT](#page-39-0) column by storing it using a string. In this case, MySQL performs a string-to-number conversion that involves no intermediate doubleprecision representation.
- The [-](#page-153-1), [+](#page-153-0), and [\\*](#page-154-0) operators use [BIGINT](#page-39-0) arithmetic when both operands are integer values. This means that if you multiply two big integers (or results from functions that return integers), you may get unexpected results when the result is larger than 9223372036854775807.
- DECIMAL[(M[,D[\]\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-1)

A packed "exact" fixed-point number. M is the total number of digits (the precision) and D is the number of digits after the decimal point (the scale). The decimal point and (for negative numbers) the - sign are not counted in M. If D is 0, values have no decimal point or fractional part. The maximum number of digits (M) for [DECIMAL](#page-39-1) is 65. The maximum number of supported decimals (D) is 30. If D is omitted, the default is 0. If M is omitted, the default is 10. (There is also a limit on how long the text of [DECIMAL](#page-39-1) literals can be; see Section 14.24.3, "Expression Handling".)

UNSIGNED, if specified, disallows negative values. The UNSIGNED attribute is deprecated for columns of type [DECIMAL](#page-39-1) (and any synonyms); you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

All basic calculations (+, -, \*, /) with [DECIMAL](#page-39-1) columns are done with a precision of 65 digits.

• DEC[(M[,D[\]\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-1), NUMERIC[(M[,D[\]\)\] \[UNSIGNED\]](#page-39-1) [\[ZEROFILL\]](#page-39-1), FIXED[(M[,D[\]\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-39-1)

These types are synonyms for [DECIMAL](#page-39-1). The [FIXED](#page-39-1) synonym is available for compatibility with other database systems.

• FLOAT[(M,D[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-40-0)

A small (single-precision) floating-point number. Permissible values are -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

M is the total number of digits and D is the number of digits following the decimal point. If M and D are omitted, values are stored to the limits permitted by the hardware. A single-precision floating-point number is accurate to approximately 7 decimal places.

FLOAT(M,D) is a nonstandard MySQL extension. This syntax is deprecated, and you should expect support for it to be removed in a future version of MySQL.

UNSIGNED, if specified, disallows negative values. The UNSIGNED attribute is deprecated for columns of type [FLOAT](#page-40-0) (and any synonyms) and you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

Using [FLOAT](#page-40-0) might give you some unexpected problems because all calculations in MySQL are done with double precision. See Section B.3.4.7, "Solving Problems with No Matching Rows".

• FLOAT(p[\) \[UNSIGNED\] \[ZEROFILL\]](#page-40-0)

A floating-point number. p represents the precision in bits, but MySQL uses this value only to determine whether to use [FLOAT](#page-40-0) or [DOUBLE](#page-40-0) for the resulting data type. If p is from 0 to 24, the data type becomes [FLOAT](#page-40-0) with no M or D values. If p is from 25 to 53, the data type becomes [DOUBLE](#page-40-0) with no M or D values. The range of the resulting column is the same as for the single-precision [FLOAT](#page-40-0) or double-precision [DOUBLE](#page-40-0) data types described earlier in this section.

UNSIGNED, if specified, disallows negative values. The UNSIGNED attribute is deprecated for columns of type [FLOAT](#page-40-0) (and any synonyms) and you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

[FLOAT\(](#page-40-0)p) syntax is provided for ODBC compatibility.

• DOUBLE[(M,D[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-40-0)

A normal-size (double-precision) floating-point number. Permissible values are -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

M is the total number of digits and D is the number of digits following the decimal point. If M and D are omitted, values are stored to the limits permitted by the hardware. A double-precision floating-point number is accurate to approximately 15 decimal places.

DOUBLE(M,D) is a nonstandard MySQL extension; and is deprecated. You should expect support for this syntax to be removed in a future version of MySQL.

UNSIGNED, if specified, disallows negative values. The UNSIGNED attribute is deprecated for columns of type [DOUBLE](#page-40-0) (and any synonyms) and you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

• DOUBLE PRECISION[(M,D[\)\] \[UNSIGNED\] \[ZEROFILL\]](#page-40-0), REAL[(M,D[\)\] \[UNSIGNED\]](#page-40-0) [\[ZEROFILL\]](#page-40-0)

These types are synonyms for [DOUBLE](#page-40-0). Exception: If the REAL\_AS\_FLOAT SQL mode is enabled, [REAL](#page-40-0) is a synonym for [FLOAT](#page-40-0) rather than [DOUBLE](#page-40-0).

# <span id="page-39-0"></span>**13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT**

MySQL supports the SQL standard integer types INTEGER (or INT) and SMALLINT. As an extension to the standard, MySQL also supports the integer types TINYINT, MEDIUMINT, and BIGINT. The following table shows the required storage and range for each integer type.

| Table 13.1 Required Storage and Range for Integer Types Supported by MySQL |  |
|----------------------------------------------------------------------------|--|
|----------------------------------------------------------------------------|--|

| Type      | Storage<br>(Bytes) | Minimum<br>Value Signed | Minimum<br>Value<br>Unsigned | Maximum<br>Value Signed | Maximum<br>Value<br>Unsigned |
|-----------|--------------------|-------------------------|------------------------------|-------------------------|------------------------------|
| TINYINT   | 1                  | -128                    | 0                            | 127                     | 255                          |
| SMALLINT  | 2                  | -32768                  | 0                            | 32767                   | 65535                        |
| MEDIUMINT | 3                  | -8388608                | 0                            | 8388607                 | 16777215                     |
| INT       | 4                  | -2147483648             | 0                            | 2147483647              | 4294967295                   |
| BIGINT    | 8                  | -263                    | 0                            | 63-1<br>2               | 64-1<br>2                    |

# <span id="page-39-1"></span>**13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC**

The DECIMAL and NUMERIC types store exact numeric data values. These types are used when it is important to preserve exact precision, for example with monetary data. In MySQL, NUMERIC is implemented as DECIMAL, so the following remarks about DECIMAL apply equally to NUMERIC.

MySQL stores DECIMAL values in binary format. See Section 14.24, "Precision Math".

In a DECIMAL column declaration, the precision and scale can be (and usually is) specified. For example:

salary DECIMAL(5,2)

In this example, 5 is the precision and 2 is the scale. The precision represents the number of significant digits that are stored for values, and the scale represents the number of digits that can be stored following the decimal point.

Standard SQL requires that DECIMAL(5,2) be able to store any value with five digits and two decimals, so values that can be stored in the salary column range from -999.99 to 999.99. In standard SQL, the syntax DECIMAL(M) is equivalent to DECIMAL(M,0). Similarly, the syntax DECIMAL is equivalent to DECIMAL(M,0), where the implementation is permitted to decide the value of M. MySQL supports both of these variant forms of DECIMAL syntax. The default value of M is 10.

If the scale is 0, DECIMAL values contain no decimal point or fractional part.

The maximum number of digits for DECIMAL is 65, but the actual range for a given DECIMAL column can be constrained by the precision or scale for a given column. When such a column is assigned a value with more digits following the decimal point than are permitted by the specified scale, the value is converted to that scale. (The precise behavior is operating system-specific, but generally the effect is truncation to the permissible number of digits.)

## <span id="page-40-0"></span>**13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE**

The FLOAT and DOUBLE types represent approximate numeric data values. MySQL uses four bytes for single-precision values and eight bytes for double-precision values.

For FLOAT, the SQL standard permits an optional specification of the precision (but not the range of the exponent) in bits following the keyword FLOAT in parentheses, that is, [FLOAT\(](#page-40-0)p). MySQL also supports this optional precision specification, but the precision value in [FLOAT\(](#page-40-0)p) is used only to determine storage size. A precision from 0 to 23 results in a 4-byte single-precision FLOAT column. A precision from 24 to 53 results in an 8-byte double-precision DOUBLE column.

MySQL permits a nonstandard syntax: FLOAT(M,D) or REAL(M,D) or DOUBLE PRECISION(M,D). Here, (M,D) means than values can be stored with up to M digits in total, of which D digits may be after the decimal point. For example, a column defined as FLOAT(7,4) is displayed as -999.9999. MySQL performs rounding when storing values, so if you insert 999.00009 into a FLOAT(7,4) column, the approximate result is 999.0001.

FLOAT(M,D)and DOUBLE(M,D) are nonstandard MySQL extensions; and are deprecated. You should expect support for these variants to be removed in a future version of MySQL.

Because floating-point values are approximate and not stored as exact values, attempts to treat them as exact in comparisons may lead to problems. They are also subject to platform or implementation dependencies. For more information, see Section B.3.4.8, "Problems with Floating-Point Values".

For maximum portability, code requiring storage of approximate numeric data values should use FLOAT or DOUBLE PRECISION with no specification of precision or number of digits.

## <span id="page-40-1"></span>**13.1.5 Bit-Value Type - BIT**

The BIT data type is used to store bit values. A type of BIT(M) enables storage of M-bit values. M can range from 1 to 64.

To specify bit values, b'value' notation can be used. value is a binary value written using zeros and ones. For example, b'111' and b'10000000' represent 7 and 128, respectively. See Section 11.1.5, "Bit-Value Literals".

If you assign a value to a BIT(M) column that is less than M bits long, the value is padded on the left with zeros. For example, assigning a value of b'101' to a BIT(6) column is, in effect, the same as assigning b'000101'.

**NDB Cluster.** The maximum combined size of all BIT columns used in a given NDB table must not exceed 4096 bits.

# <span id="page-40-2"></span>**13.1.6 Numeric Type Attributes**

MySQL supports an extension for optionally specifying the display width of integer data types in parentheses following the base keyword for the type. For example, [INT\(4\)](#page-39-0) specifies an [INT](#page-39-0) with a display width of four digits. This optional display width may be used by applications to display integer values having a width less than the width specified for the column by left-padding them with spaces.

(That is, this width is present in the metadata returned with result sets. Whether it is used is up to the application.)

The display width does not constrain the range of values that can be stored in the column. Nor does it prevent values wider than the column display width from being displayed correctly. For example, a column specified as [SMALLINT\(3\)](#page-39-0) has the usual [SMALLINT](#page-39-0) range of -32768 to 32767, and values outside the range permitted by three digits are displayed in full using more than three digits.

When used in conjunction with the optional (nonstandard) ZEROFILL attribute, the default padding of spaces is replaced with zeros. For example, for a column declared as [INT\(4\) ZEROFILL](#page-39-0), a value of 5 is retrieved as 0005.

![](_page_41_Picture_4.jpeg)

### **Note**

The ZEROFILL attribute is ignored for columns involved in expressions or UNION queries.

If you store values larger than the display width in an integer column that has the ZEROFILL attribute, you may experience problems when MySQL generates temporary tables for some complicated joins. In these cases, MySQL assumes that the data values fit within the column display width.

The ZEROFILL attribute is deprecated for numeric data types, as is the display width attribute for integer data types. You should expect support for ZEROFILL and display widths for integer data types to be removed in a future version of MySQL. Consider using an alternative means of producing the effect of these attributes. For example, applications can use the [LPAD\(\)](#page-194-0) function to zero-pad numbers up to the desired width, or they can store the formatted numbers in [CHAR](#page-59-0) columns.

All integer types can have an optional (nonstandard) UNSIGNED attribute. An unsigned type can be used to permit only nonnegative numbers in a column or when you need a larger upper numeric range for the column. For example, if an [INT](#page-39-0) column is UNSIGNED, the size of the column's range is the same but its endpoints shift up, from -2147483648 and 2147483647 to 0 and 4294967295.

Floating-point and fixed-point types also can be UNSIGNED. As with integer types, this attribute prevents negative values from being stored in the column. Unlike the integer types, the upper range of column values remains the same. UNSIGNED is deprecated for columns of type [FLOAT](#page-40-0), [DOUBLE](#page-40-0), and [DECIMAL](#page-39-1) (and any synonyms) and you should expect support for it to be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such columns.

If you specify ZEROFILL for a numeric column, MySQL automatically adds the UNSIGNED attribute.

Integer or floating-point data types can have the AUTO\_INCREMENT attribute. When you insert a value of NULL into an indexed AUTO\_INCREMENT column, the column is set to the next sequence value. Typically this is value+1, where value is the largest value for the column currently in the table. (AUTO\_INCREMENT sequences begin with 1.)

Storing 0 into an AUTO\_INCREMENT column has the same effect as storing NULL, unless the NO\_AUTO\_VALUE\_ON\_ZERO SQL mode is enabled.

Inserting NULL to generate AUTO\_INCREMENT values requires that the column be declared NOT NULL. If the column is declared NULL, inserting NULL stores a NULL. When you insert any other value into an AUTO\_INCREMENT column, the column is set to that value and the sequence is reset so that the next automatically generated value follows sequentially from the inserted value.

Negative values for AUTO\_INCREMENT columns are not supported.

CHECK constraints cannot refer to columns that have the AUTO\_INCREMENT attribute, nor can the AUTO\_INCREMENT attribute be added to existing columns that are used in CHECK constraints.

AUTO\_INCREMENT for [FLOAT](#page-40-0) and [DOUBLE](#page-40-0) columns is not supported, as of MySQL 8.4.0. To upgrade an earlier version to MySQL 8.4.0, or higher, you must remove the AUTO\_INCREMENT attribute from such columns to avoid compatibility issues, or convert them to an integer type.

## <span id="page-42-0"></span>**13.1.7 Out-of-Range and Overflow Handling**

When MySQL stores a value in a numeric column that is outside the permissible range of the column data type, the result depends on the SQL mode in effect at the time:

- If strict SQL mode is enabled, MySQL rejects the out-of-range value with an error, and the insert fails, in accordance with the SQL standard.
- If no restrictive modes are enabled, MySQL clips the value to the appropriate endpoint of the column data type range and stores the resulting value instead.

When an out-of-range value is assigned to an integer column, MySQL stores the value representing the corresponding endpoint of the column data type range.

When a floating-point or fixed-point column is assigned a value that exceeds the range implied by the specified (or default) precision and scale, MySQL stores the value representing the corresponding endpoint of that range.

Suppose that a table t1 has this definition:

```
CREATE TABLE t1 (i1 TINYINT, i2 TINYINT UNSIGNED);
```

With strict SQL mode enabled, an out of range error occurs:

```
mysql> SET sql_mode = 'TRADITIONAL';
mysql> INSERT INTO t1 (i1, i2) VALUES(256, 256);
ERROR 1264 (22003): Out of range value for column 'i1' at row 1
mysql> SELECT * FROM t1;
Empty set (0.00 sec)
```

With strict SQL mode not enabled, clipping with warnings occurs:

```
mysql> SET sql_mode = '';
mysql> INSERT INTO t1 (i1, i2) VALUES(256, 256);
mysql> SHOW WARNINGS;
+---------+------+---------------------------------------------+
| Level | Code | Message |
+---------+------+---------------------------------------------+
| Warning | 1264 | Out of range value for column 'i1' at row 1 |
| Warning | 1264 | Out of range value for column 'i2' at row 1 |
+---------+------+---------------------------------------------+
mysql> SELECT * FROM t1;
+------+------+
| i1 | i2 |
+------+------+
| 127 | 255 |
+------+------+
```

When strict SQL mode is not enabled, column-assignment conversions that occur due to clipping are reported as warnings for ALTER TABLE, LOAD DATA, UPDATE, and multiple-row INSERT statements. In strict mode, these statements fail, and some or all the values are not inserted or changed, depending on whether the table is a transactional table and other factors. For details, see Section 7.1.11, "Server SQL Modes".

Overflow during numeric expression evaluation results in an error. For example, the largest signed [BIGINT](#page-39-0) value is 9223372036854775807, so the following expression produces an error:

```
mysql> SELECT 9223372036854775807 + 1;
ERROR 1690 (22003): BIGINT value is out of range in '(9223372036854775807 + 1)'
```

To enable the operation to succeed in this case, convert the value to unsigned;

```
mysql> SELECT CAST(9223372036854775807 AS UNSIGNED) + 1;
+-------------------------------------------+
| CAST(9223372036854775807 AS UNSIGNED) + 1 |
+-------------------------------------------+
| 9223372036854775808 |
```

+-------------------------------------------+

Whether overflow occurs depends on the range of the operands, so another way to handle the preceding expression is to use exact-value arithmetic because [DECIMAL](#page-39-1) values have a larger range than integers:

```
mysql> SELECT 9223372036854775807.0 + 1;
+---------------------------+
| 9223372036854775807.0 + 1 |
+---------------------------+
| 9223372036854775808.0 |
+---------------------------+
```

Subtraction between integer values, where one is of type UNSIGNED, produces an unsigned result by default. If the result would otherwise have been negative, an error results:

```
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
ERROR 1690 (22003): BIGINT UNSIGNED value is out of range in '(cast(0 as unsigned) - 1)'
```

If the NO\_UNSIGNED\_SUBTRACTION SQL mode is enabled, the result is negative:

```
mysql> SET sql_mode = 'NO_UNSIGNED_SUBTRACTION';
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
+-------------------------+
| CAST(0 AS UNSIGNED) - 1 |
+-------------------------+
| -1 |
+-------------------------+
```

If the result of such an operation is used to update an UNSIGNED integer column, the result is clipped to the maximum value for the column type, or clipped to 0 if NO\_UNSIGNED\_SUBTRACTION is enabled. If strict SQL mode is enabled, an error occurs and the column remains unchanged.

# <span id="page-43-0"></span>**13.2 Date and Time Data Types**

The date and time data types for representing temporal values are [DATE](#page-46-0), [TIME](#page-48-0), [DATETIME](#page-46-0), [TIMESTAMP](#page-46-0), and [YEAR](#page-48-1). Each temporal type has a range of valid values, as well as a "zero" value that may be used when you specify an invalid value that MySQL cannot represent. The [TIMESTAMP](#page-46-0) and [DATETIME](#page-46-0) types have special automatic updating behavior, described in [Section 13.2.5, "Automatic](#page-49-0) [Initialization and Updating for TIMESTAMP and DATETIME"](#page-49-0).

For information about storage requirements of the temporal data types, see [Section 13.7, "Data Type](#page-104-0) [Storage Requirements"](#page-104-0).

For descriptions of functions that operate on temporal values, see [Section 14.7, "Date and Time](#page-163-0) [Functions".](#page-163-0)

Keep in mind these general considerations when working with date and time types:

- MySQL retrieves values for a given date or time type in a standard output format, but it attempts to interpret a variety of formats for input values that you supply (for example, when you specify a value to be assigned to or compared to a date or time type). For a description of the permitted formats for date and time types, see Section 11.1.3, "Date and Time Literals". It is expected that you supply valid values. Unpredictable results may occur if you use values in other formats.
- Although MySQL tries to interpret values in several formats, date parts must always be given in yearmonth-day order (for example, '98-09-04'), rather than in the month-day-year or day-month-year orders commonly used elsewhere (for example, '09-04-98', '04-09-98'). To convert strings in other orders to year-month-day order, the [STR\\_TO\\_DATE\(\)](#page-176-0) function may be useful.
- Dates containing 2-digit year values are ambiguous because the century is unknown. MySQL interprets 2-digit year values using these rules:

- Year values in the range 70-99 become 1970-1999.
- Year values in the range 00-69 become 2000-2069.

See also [Section 13.2.9, "2-Digit Years in Dates"](#page-55-0).

- Conversion of values from one temporal type to another occurs according to the rules in [Section 13.2.8, "Conversion Between Date and Time Types".](#page-54-0)
- MySQL automatically converts a date or time value to a number if the value is used in numeric context and vice versa.
- By default, when MySQL encounters a value for a date or time type that is out of range or otherwise invalid for the type, it converts the value to the "zero" value for that type. The exception is that out-ofrange [TIME](#page-48-0) values are clipped to the appropriate endpoint of the [TIME](#page-48-0) range.
- By setting the SQL mode to the appropriate value, you can specify more exactly what kind of dates you want MySQL to support. (See Section 7.1.11, "Server SQL Modes".) You can get MySQL to accept certain dates, such as '2009-11-31', by enabling the ALLOW\_INVALID\_DATES SQL mode. This is useful when you want to store a "possibly wrong" value which the user has specified (for example, in a web form) in the database for future processing. Under this mode, MySQL verifies only that the month is in the range from 1 to 12 and that the day is in the range from 1 to 31.
- MySQL permits you to store dates where the day or month and day are zero in a [DATE](#page-46-0) or [DATETIME](#page-46-0) column. This is useful for applications that need to store birthdates for which you may not know the exact date. In this case, you simply store the date as '2009-00-00' or '2009-01-00'. However, with dates such as these, you should not expect to get correct results for functions such as [DATE\\_SUB\(\)](#page-170-0) or [DATE\\_ADD\(\)](#page-168-0) that require complete dates. To disallow zero month or day parts in dates, enable the NO\_ZERO\_IN\_DATE mode.
- MySQL permits you to store a "zero" value of '0000-00-00' as a "dummy date." In some cases, this is more convenient than using NULL values, and uses less data and index space. To disallow '0000-00-00', enable the NO\_ZERO\_DATE mode.
- "Zero" date or time values used through Connector/ODBC are converted automatically to NULL because ODBC cannot handle such values.

The following table shows the format of the "zero" value for each type. The "zero" values are special, but you can store or refer to them explicitly using the values shown in the table. You can also do this using the values '0' or 0, which are easier to write. For temporal types that include a date part ([DATE](#page-46-0), [DATETIME](#page-46-0), and [TIMESTAMP](#page-46-0)), use of these values may produce warning or errors. The precise behavior depends on which, if any, of the strict and NO\_ZERO\_DATE SQL modes are enabled; see Section 7.1.11, "Server SQL Modes".

| Data Type | "Zero" Value          |
|-----------|-----------------------|
| DATE      | '0000-00-00'          |
| TIME      | '00:00:00'            |
| DATETIME  | '0000-00-00 00:00:00' |
| TIMESTAMP | '0000-00-00 00:00:00' |
| YEAR      | 0000                  |

# <span id="page-44-0"></span>**13.2.1 Date and Time Data Type Syntax**

The date and time data types for representing temporal values are [DATE](#page-46-0), [TIME](#page-48-0), [DATETIME](#page-46-0), [TIMESTAMP](#page-46-0), and [YEAR](#page-48-1).

For the [DATE](#page-46-0) and [DATETIME](#page-46-0) range descriptions, "supported" means that although earlier values might work, there is no guarantee.

MySQL permits fractional seconds for [TIME](#page-48-0), [DATETIME](#page-46-0), and [TIMESTAMP](#page-46-0) values, with up to microseconds (6 digits) precision. To define a column that includes a fractional seconds part, use the syntax type\_name(fsp), where type\_name is [TIME](#page-48-0), [DATETIME](#page-46-0), or [TIMESTAMP](#page-46-0), and fsp is the fractional seconds precision. For example:

```
CREATE TABLE t1 (t TIME(3), dt DATETIME(6), ts TIMESTAMP(0));
```

The fsp value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0. (This differs from the standard SQL default of 6, for compatibility with previous MySQL versions.)

Any [TIMESTAMP](#page-46-0) or [DATETIME](#page-46-0) column in a table can have automatic initialization and updating properties; see [Section 13.2.5, "Automatic Initialization and Updating for TIMESTAMP and](#page-49-0) [DATETIME".](#page-49-0)

• [DATE](#page-46-0)

A date. The supported range is '1000-01-01' to '9999-12-31'. MySQL displays [DATE](#page-46-0) values in 'YYYY-MM-DD' format, but permits assignment of values to [DATE](#page-46-0) columns using either strings or numbers.

• [DATETIME\[\(](#page-46-0)fsp)]

A date and time combination. The supported range is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.499999'. MySQL displays [DATETIME](#page-46-0) values in 'YYYY-MM-DD hh:mm:ss[.fraction]' format, but permits assignment of values to [DATETIME](#page-46-0) columns using either strings or numbers.

An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

Automatic initialization and updating to the current date and time for [DATETIME](#page-46-0) columns can be specified using DEFAULT and ON UPDATE column definition clauses, as described in [Section 13.2.5,](#page-49-0) ["Automatic Initialization and Updating for TIMESTAMP and DATETIME".](#page-49-0)

• [TIMESTAMP\[\(](#page-46-0)fsp)]

A timestamp. The range is '1970-01-01 00:00:01.000000' UTC to '2038-01-19 03:14:07.499999' UTC. [TIMESTAMP](#page-46-0) values are stored as the number of seconds since the epoch ('1970-01-01 00:00:00' UTC). A [TIMESTAMP](#page-46-0) cannot represent the value '1970-01-01 00:00:00' because that is equivalent to 0 seconds from the epoch and the value 0 is reserved for representing '0000-00-00 00:00:00', the "zero" [TIMESTAMP](#page-46-0) value.

An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

The way the server handles TIMESTAMP definitions depends on the value of the explicit\_defaults\_for\_timestamp system variable (see Section 7.1.8, "Server System Variables").

If explicit\_defaults\_for\_timestamp is enabled, there is no automatic assignment of the DEFAULT CURRENT\_TIMESTAMP or ON UPDATE CURRENT\_TIMESTAMP attributes to any [TIMESTAMP](#page-46-0) column. They must be included explicitly in the column definition. Also, any [TIMESTAMP](#page-46-0) not explicitly declared as NOT NULL permits NULL values.

If explicit\_defaults\_for\_timestamp is disabled, the server handles TIMESTAMP as follows:

Unless specified otherwise, the first [TIMESTAMP](#page-46-0) column in a table is defined to be automatically set to the date and time of the most recent modification if not explicitly assigned a value. This makes [TIMESTAMP](#page-46-0) useful for recording the timestamp of an INSERT or UPDATE operation. You can also set any [TIMESTAMP](#page-46-0) column to the current date and time by assigning it a NULL value, unless it has been defined with the NULL attribute to permit NULL values.

Automatic initialization and updating to the current date and time can be specified using DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP column definition clauses. By default, the first [TIMESTAMP](#page-46-0) column has these properties, as previously noted. However, any [TIMESTAMP](#page-46-0) column in a table can be defined to have these properties.

• [TIME\[\(](#page-48-0)fsp)]

A time. The range is '-838:59:59.000000' to '838:59:59.000000'. MySQL displays [TIME](#page-48-0) values in 'hh:mm:ss[.fraction]' format, but permits assignment of values to [TIME](#page-48-0) columns using either strings or numbers.

An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

• [YEAR\[\(4\)\]](#page-48-1)

A year in 4-digit format. MySQL displays [YEAR](#page-48-1) values in YYYY format, but permits assignment of values to [YEAR](#page-48-1) columns using either strings or numbers. Values display as 1901 to 2155, or 0000.

For additional information about [YEAR](#page-48-1) display format and interpretation of input values, see [Section 13.2.4, "The YEAR Type"](#page-48-1).

![](_page_46_Picture_9.jpeg)

#### **Note**

The [YEAR\(4\)](#page-48-1) data type with an explicit display width is deprecated; you should expect support for it to be removed in a future version of MySQL. Instead, use [YEAR](#page-48-1) without a display width, which has the same meaning.

The SUM() and AVG() aggregate functions do not work with temporal values. (They convert the values to numbers, losing everything after the first nonnumeric character.) To work around this problem, convert to numeric units, perform the aggregate operation, and convert back to a temporal value. Examples:

```
SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_col))) FROM tbl_name;
SELECT FROM_DAYS(SUM(TO_DAYS(date_col))) FROM tbl_name;
```

## <span id="page-46-0"></span>**13.2.2 The DATE, DATETIME, and TIMESTAMP Types**

The DATE, DATETIME, and TIMESTAMP types are related. This section describes their characteristics, how they are similar, and how they differ. MySQL recognizes DATE, DATETIME, and TIMESTAMP values in several formats, described in Section 11.1.3, "Date and Time Literals". For the DATE and DATETIME range descriptions, "supported" means that although earlier values might work, there is no guarantee.

The DATE type is used for values with a date part but no time part. MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format. The supported range is '1000-01-01' to '9999-12-31'.

The DATETIME type is used for values that contain both date and time parts. MySQL retrieves and displays DATETIME values in 'YYYY-MM-DD hh:mm:ss' format. The supported range is '1000-01-01 00:00:00' to '9999-12-31 23:59:59'.

The TIMESTAMP data type is used for values that contain both date and time parts. TIMESTAMP has a range of '1970-01-01 00:00:01' UTC to '2038-01-19 03:14:07' UTC.

A DATETIME or TIMESTAMP value can include a trailing fractional seconds part in up to microseconds (6 digits) precision. In particular, any fractional part in a value inserted into a DATETIME or TIMESTAMP column is stored rather than discarded. With the fractional part included, the format for these values is 'YYYY-MM-DD hh:mm:ss[.fraction]', the range for DATETIME values is '1000-01-01

00:00:00.000000' to '9999-12-31 23:59:59.499999', and the range for TIMESTAMP values is '1970-01-01 00:00:01.000000' to '2038-01-19 03:14:07.499999'. The fractional part should always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is recognized. For information about fractional seconds support in MySQL, see [Section 13.2.6, "Fractional Seconds in Time Values".](#page-52-0)

The TIMESTAMP and DATETIME data types offer automatic initialization and updating to the current date and time. For more information, see [Section 13.2.5, "Automatic Initialization and Updating for](#page-49-0) [TIMESTAMP and DATETIME"](#page-49-0).

MySQL converts TIMESTAMP values from the current time zone to UTC for storage, and back from UTC to the current time zone for retrieval. (This does not occur for other types such as DATETIME.) By default, the current time zone for each connection is the server's time. The time zone can be set on a per-connection basis. As long as the time zone setting remains constant, you get back the same value you store. If you store a TIMESTAMP value, and then change the time zone and retrieve the value, the retrieved value is different from the value you stored. This occurs because the same time zone was not used for conversion in both directions. The current time zone is available as the value of the time\_zone system variable. For more information, see Section 7.1.15, "MySQL Server Time Zone Support".

You can specify a time zone offset when inserting a TIMESTAMP or DATETIME value into a table. See Section 11.1.3, "Date and Time Literals", for more information and examples.

Invalid DATE, DATETIME, or TIMESTAMP values are converted to the "zero" value of the appropriate type ('0000-00-00' or '0000-00-00 00:00:00'), if the SQL mode permits this conversion. The precise behavior depends on which if any of strict SQL mode and the NO\_ZERO\_DATE SQL mode are enabled; see Section 7.1.11, "Server SQL Modes".

You can convert TIMESTAMP values to UTC DATETIME values when retrieving them using CAST() with the AT TIME ZONE operator, as shown here:

```
mysql> SELECT col,
 > CAST(col AT TIME ZONE INTERVAL '+00:00' AS DATETIME) AS ut
 > FROM ts ORDER BY id;
+---------------------+---------------------+
| col | ut |
+---------------------+---------------------+
| 2020-01-01 10:10:10 | 2020-01-01 15:10:10 |
| 2019-12-31 23:40:10 | 2020-01-01 04:40:10 |
| 2020-01-01 13:10:10 | 2020-01-01 18:10:10 |
| 2020-01-01 10:10:10 | 2020-01-01 15:10:10 |
| 2020-01-01 04:40:10 | 2020-01-01 09:40:10 |
| 2020-01-01 18:10:10 | 2020-01-01 23:10:10 |
+---------------------+---------------------+
```

For complete information regarding syntax and additional examples, see the description of the CAST() function.

Be aware of certain properties of date value interpretation in MySQL:

• MySQL permits a "relaxed" format for values specified as strings, in which any punctuation character may be used as the delimiter between date parts or time parts. In some cases, this syntax can be deceiving. For example, a value such as '10:11:12' might look like a time value because of the :, but is interpreted as the year '2010-11-12' if used in date context. The value '10:45:15' is converted to '0000-00-00' because '45' is not a valid month.

The only delimiter recognized between a date and time part and a fractional seconds part is the decimal point.

• The server requires that month and day values be valid, and not merely in the range 1 to 12 and 1 to 31, respectively. With strict mode disabled, invalid dates such as '2004-04-31' are converted to '0000-00-00' and a warning is generated. With strict mode enabled, invalid dates generate

an error. To permit such dates, enable ALLOW\_INVALID\_DATES. See Section 7.1.11, "Server SQL Modes", for more information.

- MySQL does not accept TIMESTAMP values that include a zero in the day or month column or values that are not a valid date. The sole exception to this rule is the special "zero" value '0000-00-00 00:00:00', if the SQL mode permits this value. The precise behavior depends on which if any of strict SQL mode and the NO\_ZERO\_DATE SQL mode are enabled; see Section 7.1.11, "Server SQL Modes".
- Dates containing 2-digit year values are ambiguous because the century is unknown. MySQL interprets 2-digit year values using these rules:
  - Year values in the range 00-69 become 2000-2069.
  - Year values in the range 70-99 become 1970-1999.

See also [Section 13.2.9, "2-Digit Years in Dates"](#page-55-0).

# <span id="page-48-0"></span>**13.2.3 The TIME Type**

MySQL retrieves and displays TIME values in 'hh:mm:ss' format (or 'hhh:mm:ss' format for large hours values). TIME values may range from '-838:59:59' to '838:59:59'. The hours part may be so large because the TIME type can be used not only to represent a time of day (which must be less than 24 hours), but also elapsed time or a time interval between two events (which may be much greater than 24 hours, or even negative).

MySQL recognizes TIME values in several formats, some of which can include a trailing fractional seconds part in up to microseconds (6 digits) precision. See Section 11.1.3, "Date and Time Literals". For information about fractional seconds support in MySQL, see [Section 13.2.6, "Fractional](#page-52-0) [Seconds in Time Values"](#page-52-0). In particular, any fractional part in a value inserted into a TIME column is stored rather than discarded. With the fractional part included, the range for TIME values is '-838:59:59.000000' to '838:59:59.000000'.

Be careful about assigning abbreviated values to a TIME column. MySQL interprets abbreviated TIME values with colons as time of the day. That is, '11:12' means '11:12:00', not '00:11:12'. MySQL interprets abbreviated values without colons using the assumption that the two rightmost digits represent seconds (that is, as elapsed time rather than as time of day). For example, you might think of '1112' and 1112 as meaning '11:12:00' (12 minutes after 11 o'clock), but MySQL interprets them as '00:11:12' (11 minutes, 12 seconds). Similarly, '12' and 12 are interpreted as '00:00:12'.

The only delimiter recognized between a time part and a fractional seconds part is the decimal point.

By default, values that lie outside the TIME range but are otherwise valid are clipped to the closest endpoint of the range. For example, '-850:00:00' and '850:00:00' are converted to '-838:59:59' and '838:59:59'. Invalid TIME values are converted to '00:00:00'. Note that because '00:00:00' is itself a valid TIME value, there is no way to tell, from a value of '00:00:00' stored in a table, whether the original value was specified as '00:00:00' or whether it was invalid.

For more restrictive treatment of invalid TIME values, enable strict SQL mode to cause errors to occur. See Section 7.1.11, "Server SQL Modes".

# <span id="page-48-1"></span>**13.2.4 The YEAR Type**

The YEAR type is a 1-byte type used to represent year values. It can be declared as YEAR with an implicit display width of 4 characters, or equivalently as YEAR(4) with an explicit display width.

![](_page_48_Picture_16.jpeg)

#### **Note**

The [YEAR\(4\)](#page-48-1) data type using an explicit display width is deprecated and you should expect support for it to be removed in a future version of MySQL. Instead, use [YEAR](#page-48-1) without a display width, which has the same meaning.

MySQL displays YEAR values in YYYY format, with a range of 1901 to 2155, and 0000.

YEAR accepts input values in a variety of formats:

- As 4-digit strings in the range '1901' to '2155'.
- As 4-digit numbers in the range 1901 to 2155.
- As 1- or 2-digit strings in the range '0' to '99'. MySQL converts values in the ranges '0' to '69' and '70' to '99' to YEAR values in the ranges 2000 to 2069 and 1970 to 1999.
- As 1- or 2-digit numbers in the range 0 to 99. MySQL converts values in the ranges 1 to 69 and 70 to 99 to YEAR values in the ranges 2001 to 2069 and 1970 to 1999.

The result of inserting a numeric 0 has a display value of 0000 and an internal value of 0000. To insert zero and have it be interpreted as 2000, specify it as a string '0' or '00'.

• As the result of functions that return a value that is acceptable in YEAR context, such as [NOW\(\)](#page-174-1).

If strict SQL mode is not enabled, MySQL converts invalid YEAR values to 0000. In strict SQL mode, attempting to insert an invalid YEAR value produces an error.

See also [Section 13.2.9, "2-Digit Years in Dates"](#page-55-0).

## <span id="page-49-0"></span>**13.2.5 Automatic Initialization and Updating for TIMESTAMP and DATETIME**

[TIMESTAMP](#page-46-0) and [DATETIME](#page-46-0) columns can be automatically initialized and updated to the current date and time (that is, the current timestamp).

For any [TIMESTAMP](#page-46-0) or [DATETIME](#page-46-0) column in a table, you can assign the current timestamp as the default value, the auto-update value, or both:

- An auto-initialized column is set to the current timestamp for inserted rows that specify no value for the column.
- An auto-updated column is automatically updated to the current timestamp when the value of any other column in the row is changed from its current value. An auto-updated column remains unchanged if all other columns are set to their current values. To prevent an auto-updated column from updating when other columns change, explicitly set it to its current value. To update an autoupdated column even when other columns do not change, explicitly set it to the value it should have (for example, set it to [CURRENT\\_TIMESTAMP](#page-167-0)).

In addition, if the explicit\_defaults\_for\_timestamp system variable is disabled, you can initialize or update any [TIMESTAMP](#page-46-0) (but not DATETIME) column to the current date and time by assigning it a NULL value, unless it has been defined with the NULL attribute to permit NULL values.

To specify automatic properties, use the DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP clauses in column definitions. The order of the clauses does not matter. If both are present in a column definition, either can occur first. Any of the synonyms for [CURRENT\\_TIMESTAMP](#page-167-0) have the same meaning as [CURRENT\\_TIMESTAMP](#page-167-0). These are [CURRENT\\_TIMESTAMP\(\)](#page-167-0), [NOW\(\)](#page-174-1), [LOCALTIME](#page-173-0), [LOCALTIME\(\)](#page-173-0), [LOCALTIMESTAMP](#page-173-1), and [LOCALTIMESTAMP\(\)](#page-173-1).

Use of DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP is specific to [TIMESTAMP](#page-46-0) and [DATETIME](#page-46-0). The DEFAULT clause also can be used to specify a constant (nonautomatic) default value (for example, DEFAULT 0 or DEFAULT '2000-01-01 00:00:00').

![](_page_49_Picture_19.jpeg)

### **Note**

The following examples use DEFAULT 0, a default that can produce warnings or errors depending on whether strict SQL mode or the NO\_ZERO\_DATE SQL

mode is enabled. Be aware that the TRADITIONAL SQL mode includes strict mode and NO\_ZERO\_DATE. See Section 7.1.11, "Server SQL Modes".

[TIMESTAMP](#page-46-0) or [DATETIME](#page-46-0) column definitions can specify the current timestamp for both the default and auto-update values, for one but not the other, or for neither. Different columns can have different combinations of automatic properties. The following rules describe the possibilities:

• With both DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP, the column has the current timestamp for its default value and is automatically updated to the current timestamp.

```
CREATE TABLE t1 (
 ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

• With a DEFAULT clause but no ON UPDATE CURRENT\_TIMESTAMP clause, the column has the given default value and is not automatically updated to the current timestamp.

The default depends on whether the DEFAULT clause specifies CURRENT\_TIMESTAMP or a constant value. With CURRENT\_TIMESTAMP, the default is the current timestamp.

```
CREATE TABLE t1 (
 ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 dt DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

With a constant, the default is the given value. In this case, the column has no automatic properties at all.

```
CREATE TABLE t1 (
 ts TIMESTAMP DEFAULT 0,
 dt DATETIME DEFAULT 0
);
```

• With an ON UPDATE CURRENT\_TIMESTAMP clause and a constant DEFAULT clause, the column is automatically updated to the current timestamp and has the given constant default value.

```
CREATE TABLE t1 (
 ts TIMESTAMP DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP,
 dt DATETIME DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP
);
```

• With an ON UPDATE CURRENT\_TIMESTAMP clause but no DEFAULT clause, the column is automatically updated to the current timestamp but does not have the current timestamp for its default value.

The default in this case is type dependent. [TIMESTAMP](#page-46-0) has a default of 0 unless defined with the NULL attribute, in which case the default is NULL.

```
CREATE TABLE t1 (
 ts1 TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- default 0
 ts2 TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP -- default NULL
);
```

[DATETIME](#page-46-0) has a default of NULL unless defined with the NOT NULL attribute, in which case the default is 0.

```
CREATE TABLE t1 (
 dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP, -- default NULL
 dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- default 0
);
```

[TIMESTAMP](#page-46-0) and [DATETIME](#page-46-0) columns have no automatic properties unless they are specified explicitly, with this exception: If the explicit\_defaults\_for\_timestamp system variable is disabled, the first [TIMESTAMP](#page-46-0) column has both DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP if neither is specified explicitly. To suppress automatic properties for the first [TIMESTAMP](#page-46-0) column, use one of these strategies:

- Enable the explicit\_defaults\_for\_timestamp system variable. In this case, the DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP clauses that specify automatic initialization and updating are available, but are not assigned to any [TIMESTAMP](#page-46-0) column unless explicitly included in the column definition.
- Alternatively, if explicit\_defaults\_for\_timestamp is disabled, do either of the following:
  - Define the column with a DEFAULT clause that specifies a constant default value.
  - Specify the NULL attribute. This also causes the column to permit NULL values, which means that you cannot assign the current timestamp by setting the column to NULL. Assigning NULL sets the column to NULL, not the current timestamp. To assign the current timestamp, set the column to [CURRENT\\_TIMESTAMP](#page-167-0) or a synonym such as [NOW\(\)](#page-174-1).

#### Consider these table definitions:

```
CREATE TABLE t1 (
 ts1 TIMESTAMP DEFAULT 0,
 ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 ON UPDATE CURRENT_TIMESTAMP);
CREATE TABLE t2 (
 ts1 TIMESTAMP NULL,
 ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 ON UPDATE CURRENT_TIMESTAMP);
CREATE TABLE t3 (
 ts1 TIMESTAMP NULL DEFAULT 0,
 ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 ON UPDATE CURRENT_TIMESTAMP);
```

The tables have these properties:

- In each table definition, the first [TIMESTAMP](#page-46-0) column has no automatic initialization or updating.
- The tables differ in how the ts1 column handles NULL values. For t1, ts1 is NOT NULL and assigning it a value of NULL sets it to the current timestamp. For t2 and t3, ts1 permits NULL and assigning it a value of NULL sets it to NULL.
- t2 and t3 differ in the default value for ts1. For t2, ts1 is defined to permit NULL, so the default is also NULL in the absence of an explicit DEFAULT clause. For t3, ts1 permits NULL but has an explicit default of 0.

If a [TIMESTAMP](#page-46-0) or [DATETIME](#page-46-0) column definition includes an explicit fractional seconds precision value anywhere, the same value must be used throughout the column definition. This is permitted:

```
CREATE TABLE t1 (
 ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
);
```

### This is not permitted:

```
CREATE TABLE t1 (
 ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(3)
);
```

### **TIMESTAMP Initialization and the NULL Attribute**

If the explicit\_defaults\_for\_timestamp system variable is disabled, [TIMESTAMP](#page-46-0) columns by default are NOT NULL, cannot contain NULL values, and assigning NULL assigns the current timestamp. To permit a [TIMESTAMP](#page-46-0) column to contain NULL, explicitly declare it with the NULL attribute. In this case, the default value also becomes NULL unless overridden with a DEFAULT clause that specifies a different default value. DEFAULT NULL can be used to explicitly specify NULL as

the default value. (For a [TIMESTAMP](#page-46-0) column not declared with the NULL attribute, DEFAULT NULL is invalid.) If a [TIMESTAMP](#page-46-0) column permits NULL values, assigning NULL sets it to NULL, not to the current timestamp.

The following table contains several [TIMESTAMP](#page-46-0) columns that permit NULL values:

```
CREATE TABLE t
(
 ts1 TIMESTAMP NULL DEFAULT NULL,
 ts2 TIMESTAMP NULL DEFAULT 0,
 ts3 TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
);
```

A [TIMESTAMP](#page-46-0) column that permits NULL values does not take on the current timestamp at insert time except under one of the following conditions:

- Its default value is defined as [CURRENT\\_TIMESTAMP](#page-167-0) and no value is specified for the column
- [CURRENT\\_TIMESTAMP](#page-167-0) or any of its synonyms such as [NOW\(\)](#page-174-1) is explicitly inserted into the column

In other words, a [TIMESTAMP](#page-46-0) column defined to permit NULL values auto-initializes only if its definition includes DEFAULT CURRENT\_TIMESTAMP:

```
CREATE TABLE t (ts TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);
```

If the [TIMESTAMP](#page-46-0) column permits NULL values but its definition does not include DEFAULT CURRENT\_TIMESTAMP, you must explicitly insert a value corresponding to the current date and time. Suppose that tables t1 and t2 have these definitions:

```
CREATE TABLE t1 (ts TIMESTAMP NULL DEFAULT '0000-00-00 00:00:00');
CREATE TABLE t2 (ts TIMESTAMP NULL DEFAULT NULL);
```

To set the [TIMESTAMP](#page-46-0) column in either table to the current timestamp at insert time, explicitly assign it that value. For example:

```
INSERT INTO t2 VALUES (CURRENT_TIMESTAMP);
INSERT INTO t1 VALUES (NOW());
```

If the explicit\_defaults\_for\_timestamp system variable is enabled, [TIMESTAMP](#page-46-0) columns permit NULL values only if declared with the NULL attribute. Also, [TIMESTAMP](#page-46-0) columns do not permit assigning NULL to assign the current timestamp, whether declared with the NULL or NOT NULL attribute. To assign the current timestamp, set the column to [CURRENT\\_TIMESTAMP](#page-167-0) or a synonym such as [NOW\(\)](#page-174-1).

## <span id="page-52-0"></span>**13.2.6 Fractional Seconds in Time Values**

MySQL has fractional seconds support for [TIME](#page-48-0), [DATETIME](#page-46-0), and [TIMESTAMP](#page-46-0) values, with up to microseconds (6 digits) precision:

• To define a column that includes a fractional seconds part, use the syntax type\_name(fsp), where type\_name is [TIME](#page-48-0), [DATETIME](#page-46-0), or [TIMESTAMP](#page-46-0), and fsp is the fractional seconds precision. For example:

```
CREATE TABLE t1 (t TIME(3), dt DATETIME(6));
```

The fsp value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0. (This differs from the standard SQL default of 6, for compatibility with previous MySQL versions.)

• Inserting a [TIME](#page-48-0), [DATE](#page-46-0), or [TIMESTAMP](#page-46-0) value with a fractional seconds part into a column of the same type but having fewer fractional digits results in rounding. Consider a table created and populated as follows:

```
CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
```

```
INSERT INTO fractest VALUES
('17:51:04.777', '2018-09-08 17:51:04.777', '2018-09-08 17:51:04.777');
```

The temporal values are inserted into the table with rounding:

```
mysql> SELECT * FROM fractest;
+-------------+------------------------+------------------------+
| c1 | c2 | c3 |
+-------------+------------------------+------------------------+
| 17:51:04.78 | 2018-09-08 17:51:04.78 | 2018-09-08 17:51:04.78 |
+-------------+------------------------+------------------------+
```

No warning or error is given when such rounding occurs. This behavior follows the SQL standard.

To insert the values with truncation instead, enable the TIME\_TRUNCATE\_FRACTIONAL SQL mode:

```
SET @@sql_mode = sys.list_add(@@sql_mode, 'TIME_TRUNCATE_FRACTIONAL');
```

With that SQL mode enabled, the temporal values are inserted with truncation:

```
mysql> SELECT * FROM fractest;
+-------------+------------------------+------------------------+
| c1 | c2 | c3 |
+-------------+------------------------+------------------------+
| 17:51:04.77 | 2018-09-08 17:51:04.77 | 2018-09-08 17:51:04.77 |
+-------------+------------------------+------------------------+
```

- Functions that take temporal arguments accept values with fractional seconds. Return values from temporal functions include fractional seconds as appropriate. For example, [NOW\(\)](#page-174-1) with no argument returns the current date and time with no fractional part, but takes an optional argument from 0 to 6 to specify that the return value includes a fractional seconds part of that many digits.
- Syntax for temporal literals produces temporal values: DATE 'str', TIME 'str', and TIMESTAMP 'str', and the ODBC-syntax equivalents. The resulting value includes a trailing fractional seconds part if specified. Previously, the temporal type keyword was ignored and these constructs produced the string value. See Standard SQL and ODBC Date and Time Literals

# <span id="page-53-0"></span>**13.2.7 What Calendar Is Used By MySQL?**

MySQL uses what is known as a proleptic Gregorian calendar.

Every country that has switched from the Julian to the Gregorian calendar has had to discard at least ten days during the switch. To see how this works, consider the month of October 1582, when the first Julian-to-Gregorian switch occurred.

| Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
|--------|---------|-----------|----------|--------|----------|--------|
| 1      | 2       | 3         | 4        | 15     | 16       | 17     |
| 18     | 19      | 20        | 21       | 22     | 23       | 24     |
| 25     | 26      | 27        | 28       | 29     | 30       | 31     |

There are no dates between October 4 and October 15. This discontinuity is called the cutover. Any dates before the cutover are Julian, and any dates following the cutover are Gregorian. Dates during a cutover are nonexistent.

A calendar applied to dates when it was not actually in use is called proleptic. Thus, if we assume there was never a cutover and Gregorian rules always rule, we have a proleptic Gregorian calendar. This is what is used by MySQL, as is required by standard SQL. For this reason, dates prior to the cutover stored as MySQL [DATE](#page-46-0) or [DATETIME](#page-46-0) values must be adjusted to compensate for the difference. It is important to realize that the cutover did not occur at the same time in all countries, and that the later it happened, the more days were lost. For example, in Great Britain, it took place in 1752, when Wednesday September 2 was followed by Thursday September 14. Russia remained on the Julian

calendar until 1918, losing 13 days in the process, and what is popularly referred to as its "October Revolution" occurred in November according to the Gregorian calendar.

## <span id="page-54-0"></span>**13.2.8 Conversion Between Date and Time Types**

To some extent, you can convert a value from one temporal type to another. However, there may be some alteration of the value or loss of information. In all cases, conversion between temporal types is subject to the range of valid values for the resulting type. For example, although [DATE](#page-46-0), [DATETIME](#page-46-0), and [TIMESTAMP](#page-46-0) values all can be specified using the same set of formats, the types do not all have the same range of values. [TIMESTAMP](#page-46-0) values cannot be earlier than 1970 UTC or later than '2038-01-19 03:14:07' UTC. This means that a date such as '1968-01-01', while valid as a [DATE](#page-46-0) or [DATETIME](#page-46-0) value, is not valid as a [TIMESTAMP](#page-46-0) value and is converted to 0.

Conversion of [DATE](#page-46-0) values:

- Conversion to a [DATETIME](#page-46-0) or [TIMESTAMP](#page-46-0) value adds a time part of '00:00:00' because the [DATE](#page-46-0) value contains no time information.
- Conversion to a [TIME](#page-48-0) value is not useful; the result is '00:00:00'.

Conversion of [DATETIME](#page-46-0) and [TIMESTAMP](#page-46-0) values:

- Conversion to a [DATE](#page-46-0) value takes fractional seconds into account and rounds the time part. For example, '1999-12-31 23:59:59.499' becomes '1999-12-31', whereas '1999-12-31 23:59:59.500' becomes '2000-01-01'.
- Conversion to a [TIME](#page-48-0) value discards the date part because the [TIME](#page-48-0) type contains no date information.

For conversion of [TIME](#page-48-0) values to other temporal types, the value of [CURRENT\\_DATE\(\)](#page-167-1) is used for the date part. The [TIME](#page-48-0) is interpreted as elapsed time (not time of day) and added to the date. This means that the date part of the result differs from the current date if the time value is outside the range from '00:00:00' to '23:59:59'.

Suppose that the current date is '2012-01-01'. [TIME](#page-48-0) values of '12:00:00', '24:00:00', and '-12:00:00', when converted to [DATETIME](#page-46-0) or [TIMESTAMP](#page-46-0) values, result in '2012-01-01 12:00:00', '2012-01-02 00:00:00', and '2011-12-31 12:00:00', respectively.

Conversion of [TIME](#page-48-0) to [DATE](#page-46-0) is similar but discards the time part from the result: '2012-01-01', '2012-01-02', and '2011-12-31', respectively.

Explicit conversion can be used to override implicit conversion. For example, in comparison of [DATE](#page-46-0) and [DATETIME](#page-46-0) values, the [DATE](#page-46-0) value is coerced to the [DATETIME](#page-46-0) type by adding a time part of '00:00:00'. To perform the comparison by ignoring the time part of the [DATETIME](#page-46-0) value instead, use the CAST() function in the following way:

```
date_col = CAST(datetime_col AS DATE)
```

Conversion of [TIME](#page-48-0) and [DATETIME](#page-46-0) values to numeric form (for example, by adding +0) depends on whether the value contains a fractional seconds part. [TIME\(](#page-48-0)N) or [DATETIME\(](#page-46-0)N) is converted to integer when N is 0 (or omitted) and to a DECIMAL value with N decimal digits when N is greater than 0:

```
mysql> SELECT CURTIME(), CURTIME()+0, CURTIME(3)+0;
+-----------+-------------+--------------+
| CURTIME() | CURTIME()+0 | CURTIME(3)+0 |
+-----------+-------------+--------------+
| 09:28:00 | 92800 | 92800.887 |
+-----------+-------------+--------------+
mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
+---------------------+----------------+--------------------+
| NOW() | NOW()+0 | NOW(3)+0 |
+---------------------+----------------+--------------------+
| 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
+---------------------+----------------+--------------------+
```

## <span id="page-55-0"></span>**13.2.9 2-Digit Years in Dates**

Date values with 2-digit years are ambiguous because the century is unknown. Such values must be interpreted into 4-digit form because MySQL stores years internally using 4 digits.

For [DATETIME](#page-46-0), [DATE](#page-46-0), and [TIMESTAMP](#page-46-0) types, MySQL interprets dates specified with ambiguous year values using these rules:

- Year values in the range 00-69 become 2000-2069.
- Year values in the range 70-99 become 1970-1999.

For YEAR, the rules are the same, with this exception: A numeric 00 inserted into YEAR results in 0000 rather than 2000. To specify zero for YEAR and have it be interpreted as 2000, specify it as a string '0' or '00'.

Remember that these rules are only heuristics that provide reasonable guesses as to what your data values mean. If the rules used by MySQL do not produce the values you require, you must provide unambiguous input containing 4-digit year values.

ORDER BY properly sorts [YEAR](#page-48-1) values that have 2-digit years.

Some functions like MIN() and MAX() convert a [YEAR](#page-48-1) to a number. This means that a value with a 2 digit year does not work properly with these functions. The fix in this case is to convert the [YEAR](#page-48-1) to 4 digit year format.

# <span id="page-55-1"></span>**13.3 String Data Types**

The string data types are [CHAR](#page-59-0), [VARCHAR](#page-59-0), [BINARY](#page-60-0), [VARBINARY](#page-60-0), [BLOB](#page-61-0), [TEXT](#page-61-0), [ENUM](#page-63-0), and [SET](#page-66-0).

For information about storage requirements of the string data types, see [Section 13.7, "Data Type](#page-104-0) [Storage Requirements"](#page-104-0).

For descriptions of functions that operate on string values, see [Section 14.8, "String Functions and](#page-186-0) [Operators".](#page-186-0)

# <span id="page-55-2"></span>**13.3.1 String Data Type Syntax**

The string data types are [CHAR](#page-59-0), [VARCHAR](#page-59-0), [BINARY](#page-60-0), [VARBINARY](#page-60-0), [BLOB](#page-61-0), [TEXT](#page-61-0), [ENUM](#page-63-0), and [SET](#page-66-0).

In some cases, MySQL may change a string column to a type different from that given in a CREATE TABLE or ALTER TABLE statement. See Section 15.1.20.7, "Silent Column Specification Changes".

For definitions of character string columns ([CHAR](#page-59-0), [VARCHAR](#page-59-0), and the [TEXT](#page-61-0) types), MySQL interprets length specifications in character units. For definitions of binary string columns ([BINARY](#page-60-0), [VARBINARY](#page-60-0), and the [BLOB](#page-61-0) types), MySQL interprets length specifications in byte units.

Column definitions for character string data types [CHAR](#page-59-0), [VARCHAR](#page-59-0), the [TEXT](#page-61-0) types, [ENUM](#page-63-0), [SET](#page-66-0), and any synonyms) can specify the column character set and collation:

• CHARACTER SET specifies the character set. If desired, a collation for the character set can be specified with the COLLATE attribute, along with any other attributes. For example:

```
CREATE TABLE t
(
 c1 VARCHAR(20) CHARACTER SET utf8mb4,
 c2 TEXT CHARACTER SET latin1 COLLATE latin1_general_cs
);
```

This table definition creates a column named c1 that has a character set of utf8mb4 with the default collation for that character set, and a column named c2 that has a character set of latin1 and a case-sensitive (\_cs) collation.

The rules for assigning the character set and collation when either or both of CHARACTER SET and the COLLATE attribute are missing are described in Section 12.3.5, "Column Character Set and Collation".

CHARSET is a synonym for CHARACTER SET.

• Specifying the CHARACTER SET binary attribute for a character string data type causes the column to be created as the corresponding binary string data type: [CHAR](#page-59-0) becomes [BINARY](#page-60-0), [VARCHAR](#page-59-0) becomes [VARBINARY](#page-60-0), and [TEXT](#page-61-0) becomes [BLOB](#page-61-0). For the [ENUM](#page-63-0) and [SET](#page-66-0) data types, this does not occur; they are created as declared. Suppose that you specify a table using this definition:

```
CREATE TABLE t
(
 c1 VARCHAR(10) CHARACTER SET binary,
 c2 TEXT CHARACTER SET binary,
 c3 ENUM('a','b','c') CHARACTER SET binary
);
```

The resulting table has this definition:

```
CREATE TABLE t
(
 c1 VARBINARY(10),
 c2 BLOB,
 c3 ENUM('a','b','c') CHARACTER SET binary
);
```

• The BINARY attribute is a nonstandard MySQL extension that is shorthand for specifying the binary (\_bin) collation of the column character set (or of the table default character set if no column character set is specified). In this case, comparison and sorting are based on numeric character code values. Suppose that you specify a table using this definition:

```
CREATE TABLE t
(
 c1 VARCHAR(10) CHARACTER SET latin1 BINARY,
 c2 TEXT BINARY
) CHARACTER SET utf8mb4;
```

The resulting table has this definition:

```
CREATE TABLE t (
 c1 VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_bin,
 c2 TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
) CHARACTER SET utf8mb4;
```

In MySQL 8.4, the BINARY attribute is deprecated and you should expect support for it to be removed in a future version of MySQL. Applications should be adjusted to use an explicit \_bin collation instead.

The use of BINARY to specify a data type or character set remains unchanged.

- The ASCII attribute is shorthand for CHARACTER SET latin1. Supported in older MySQL releases, ASCII is deprecated; use CHARACTER SET instead.
- The UNICODE attribute is shorthand for CHARACTER SET ucs2. Supported in older MySQL releases, UNICODE is deprecated; use CHARACTER SET instead.

Character column comparison and sorting are based on the collation assigned to the column. For the [CHAR](#page-59-0), [VARCHAR](#page-59-0), [TEXT](#page-61-0), [ENUM](#page-63-0), and [SET](#page-66-0) data types, you can declare a column with a binary (\_bin) collation or the BINARY attribute to cause comparison and sorting to use the underlying character code values rather than a lexical ordering.

For additional information about use of character sets in MySQL, see Chapter 12, Character Sets, Collations, Unicode.

• [NATIONAL] CHAR[(M)] [CHARACTER SET charset\_name] [COLLATE collation\_name]

A fixed-length string that is always right-padded with spaces to the specified length when stored. M represents the column length in characters. The range of M is 0 to 255. If M is omitted, the length is 1.

![](_page_57_Picture_3.jpeg)

#### **Note**

Trailing spaces are removed when [CHAR](#page-59-0) values are retrieved unless the PAD\_CHAR\_TO\_FULL\_LENGTH SQL mode is enabled.

[CHAR](#page-59-0) is shorthand for [CHARACTER](#page-59-0). [NATIONAL CHAR](#page-59-0) (or its equivalent short form, [NCHAR](#page-59-0)) is the standard SQL way to define that a [CHAR](#page-59-0) column should use some predefined character set. MySQL uses utf8mb3 as this predefined character set. Section 12.3.7, "The National Character Set".

The [CHAR BYTE](#page-60-0) data type is an alias for the [BINARY](#page-60-0) data type. This is a compatibility feature.

MySQL permits you to create a column of type CHAR(0). This is useful primarily when you must be compliant with old applications that depend on the existence of a column but that do not actually use its value. CHAR(0) is also quite nice when you need a column that can take only two values: A column that is defined as CHAR(0) NULL occupies only one bit and can take only the values NULL and '' (the empty string).

• [NATIONAL] VARCHAR(M) [CHARACTER SET charset\_name] [COLLATE collation\_name]

A variable-length string. M represents the maximum column length in characters. The range of M is 0 to 65,535. The effective maximum length of a [VARCHAR](#page-59-0) is subject to the maximum row size (65,535 bytes, which is shared among all columns) and the character set used. For example, utf8mb3 characters can require up to three bytes per character, so a [VARCHAR](#page-59-0) column that uses the utf8mb3 character set can be declared to be a maximum of 21,844 characters. See Section 10.4.7, "Limits on Table Column Count and Row Size".

MySQL stores [VARCHAR](#page-59-0) values as a 1-byte or 2-byte length prefix plus data. The length prefix indicates the number of bytes in the value. A [VARCHAR](#page-59-0) column uses one length byte if values require no more than 255 bytes, two length bytes if values may require more than 255 bytes.

![](_page_57_Picture_12.jpeg)

#### **Note**

MySQL follows the standard SQL specification, and does not remove trailing spaces from [VARCHAR](#page-59-0) values.

[VARCHAR](#page-59-0) is shorthand for [CHARACTER VARYING](#page-59-0). [NATIONAL VARCHAR](#page-59-0) is the standard SQL way to define that a [VARCHAR](#page-59-0) column should use some predefined character set. MySQL uses utf8mb3 as this predefined character set. Section 12.3.7, "The National Character Set". [NVARCHAR](#page-59-0) is shorthand for [NATIONAL VARCHAR](#page-59-0).

• [BINARY\[\(](#page-60-0)M)]

The [BINARY](#page-60-0) type is similar to the [CHAR](#page-59-0) type, but stores binary byte strings rather than nonbinary character strings. An optional length M represents the column length in bytes. If omitted, M defaults to 1.

• [VARBINARY\(](#page-60-0)M)

The [VARBINARY](#page-60-0) type is similar to the [VARCHAR](#page-59-0) type, but stores binary byte strings rather than nonbinary character strings. M represents the maximum column length in bytes.

### • [TINYBLOB](#page-61-0)

A [BLOB](#page-61-0) column with a maximum length of 255 (2<sup>8</sup> − 1) bytes. Each [TINYBLOB](#page-61-0) value is stored using a 1-byte length prefix that indicates the number of bytes in the value.

• [TINYTEXT \[CHARACTER SET](#page-61-0) charset\_name] [COLLATE collation\_name]

A [TEXT](#page-61-0) column with a maximum length of 255 (2<sup>8</sup> − 1) characters. The effective maximum length is less if the value contains multibyte characters. Each [TINYTEXT](#page-61-0) value is stored using a 1-byte length prefix that indicates the number of bytes in the value.

• [BLOB\[\(](#page-61-0)M)]

A [BLOB](#page-61-0) column with a maximum length of 65,535 (2<sup>16</sup> − 1) bytes. Each [BLOB](#page-61-0) value is stored using a 2-byte length prefix that indicates the number of bytes in the value.

An optional length M can be given for this type. If this is done, MySQL creates the column as the smallest [BLOB](#page-61-0) type large enough to hold values M bytes long.

• TEXT[(M[\)\] \[CHARACTER SET](#page-61-0) charset\_name] [COLLATE collation\_name]

A [TEXT](#page-61-0) column with a maximum length of 65,535 (2<sup>16</sup> − 1) bytes. The effective maximum length is less if the value contains multibyte characters. Each [TEXT](#page-61-0) value is stored using a 2-byte length prefix that indicates the number of bytes in the value.

An optional length M can be given for this type. If this is done, MySQL creates the column as the smallest [TEXT](#page-61-0) type large enough to hold values M characters long.

• [MEDIUMBLOB](#page-61-0)

A [BLOB](#page-61-0) column with a maximum length of 16,777,215 (2<sup>24</sup> − 1) bytes. Each [MEDIUMBLOB](#page-61-0) value is stored using a 3-byte length prefix that indicates the number of bytes in the value.

• [MEDIUMTEXT \[CHARACTER SET](#page-61-0) charset\_name] [COLLATE collation\_name]

A [TEXT](#page-61-0) column with a maximum length of 16,777,215 (2<sup>24</sup> − 1) characters. The effective maximum length is less if the value contains multibyte characters. Each [MEDIUMTEXT](#page-61-0) value is stored using a 3 byte length prefix that indicates the number of bytes in the value.

• [LONGBLOB](#page-61-0)

A [BLOB](#page-61-0) column with a maximum length of 4,294,967,295 or 4GB (2<sup>32</sup> − 1) bytes. The effective maximum length of [LONGBLOB](#page-61-0) columns depends on the configured maximum packet size in the client/server protocol and available memory. Each [LONGBLOB](#page-61-0) value is stored using a 4-byte length prefix that indicates the number of bytes in the value.

• [LONGTEXT \[CHARACTER SET](#page-61-0) charset\_name] [COLLATE collation\_name]

A [TEXT](#page-61-0) column with a maximum length of 4,294,967,295 or 4GB (2<sup>32</sup> − 1) characters. The effective maximum length is less if the value contains multibyte characters. The effective maximum length of [LONGTEXT](#page-61-0) columns also depends on the configured maximum packet size in the client/server protocol and available memory. Each [LONGTEXT](#page-61-0) value is stored using a 4-byte length prefix that indicates the number of bytes in the value.

• ENUM('value1','value2[',...\) \[CHARACTER SET](#page-63-0) charset\_name] [COLLATE [collation\\_name](#page-63-0)]

An enumeration. A string object that can have only one value, chosen from the list of values 'value1', 'value2', ..., NULL or the special '' error value. [ENUM](#page-63-0) values are represented internally as integers.

An [ENUM](#page-63-0) column can have a maximum of 65,535 distinct elements.

The maximum supported length of an individual ENUM element is M <= 255 and (M x w) <= 1020, where M is the element literal length and w is the number of bytes required for the maximum-length character in the character set.

• SET('value1','value2[',...\) \[CHARACTER SET](#page-66-0) charset\_name] [COLLATE [collation\\_name](#page-66-0)]

A set. A string object that can have zero or more values, each of which must be chosen from the list of values 'value1', 'value2', ... [SET](#page-66-0) values are represented internally as integers.

A [SET](#page-66-0) column can have a maximum of 64 distinct members.

The maximum supported length of an individual SET element is M <= 255 and (M x w) <= 1020, where M is the element literal length and w is the number of bytes required for the maximum-length character in the character set.

## <span id="page-59-0"></span>**13.3.2 The CHAR and VARCHAR Types**

The CHAR and VARCHAR types are similar, but differ in the way they are stored and retrieved. They also differ in maximum length and in whether trailing spaces are retained.

The CHAR and VARCHAR types are declared with a length that indicates the maximum number of characters you want to store. For example, CHAR(30) can hold up to 30 characters.

The length of a CHAR column is fixed to the length that you declare when you create the table. The length can be any value from 0 to 255. When CHAR values are stored, they are right-padded with spaces to the specified length. When CHAR values are retrieved, trailing spaces are removed unless the PAD\_CHAR\_TO\_FULL\_LENGTH SQL mode is enabled.

Values in VARCHAR columns are variable-length strings. The length can be specified as a value from 0 to 65,535. The effective maximum length of a VARCHAR is subject to the maximum row size (65,535 bytes, which is shared among all columns) and the character set used. See Section 10.4.7, "Limits on Table Column Count and Row Size".

In contrast to CHAR, VARCHAR values are stored as a 1-byte or 2-byte length prefix plus data. The length prefix indicates the number of bytes in the value. A column uses one length byte if values require no more than 255 bytes, two length bytes if values may require more than 255 bytes.

If strict SQL mode is not enabled and you assign a value to a CHAR or VARCHAR column that exceeds the column's maximum length, the value is truncated to fit and a warning is generated. For truncation of nonspace characters, you can cause an error to occur (rather than a warning) and suppress insertion of the value by using strict SQL mode. See Section 7.1.11, "Server SQL Modes".

For VARCHAR columns, trailing spaces in excess of the column length are truncated prior to insertion and a warning is generated, regardless of the SQL mode in use. For CHAR columns, truncation of excess trailing spaces from inserted values is performed silently regardless of the SQL mode.

VARCHAR values are not padded when they are stored. Trailing spaces are retained when values are stored and retrieved, in conformance with standard SQL.

The following table illustrates the differences between CHAR and VARCHAR by showing the result of storing various string values into CHAR(4) and VARCHAR(4) columns (assuming that the column uses a single-byte character set such as latin1).

| Value      | CHAR(4)  | Storage Required | VARCHAR(4) | Storage Required |
|------------|----------|------------------|------------|------------------|
| ''         | '<br>'   | 4 bytes          | ''         | 1 byte           |
| 'ab'       | 'ab<br>' | 4 bytes          | 'ab'       | 3 bytes          |
| 'abcd'     | 'abcd'   | 4 bytes          | 'abcd'     | 5 bytes          |
| 'abcdefgh' | 'abcd'   | 4 bytes          | 'abcd'     | 5 bytes          |

The values shown as stored in the last row of the table apply only when not using strict SQL mode; if strict mode is enabled, values that exceed the column length are not stored, and an error results.

InnoDB encodes fixed-length fields greater than or equal to 768 bytes in length as variable-length fields, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.

If a given value is stored into the CHAR(4) and VARCHAR(4) columns, the values retrieved from the columns are not always the same because trailing spaces are removed from CHAR columns upon retrieval. The following example illustrates this difference:

```
mysql> CREATE TABLE vc (v VARCHAR(4), c CHAR(4));
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO vc VALUES ('ab ', 'ab ');
Query OK, 1 row affected (0.00 sec)
mysql> SELECT CONCAT('(', v, ')'), CONCAT('(', c, ')') FROM vc;
+---------------------+---------------------+
| CONCAT('(', v, ')') | CONCAT('(', c, ')') |
+---------------------+---------------------+
| (ab ) | (ab) |
+---------------------+---------------------+
1 row in set (0.06 sec)
```

Values in CHAR, VARCHAR, and TEXT columns are sorted and compared according to the character set collation assigned to the column.

MySQL collations have a pad attribute of PAD SPACE, other than Unicode collations based on UCA 9.0.0 and higher, which have a pad attribute of NO PAD. (see Section 12.10.1, "Unicode Character Sets").

To determine the pad attribute for a collation, use the INFORMATION\_SCHEMA COLLATIONS table, which has a PAD\_ATTRIBUTE column.

For nonbinary strings (CHAR, VARCHAR, and TEXT values), the string collation pad attribute determines treatment in comparisons of trailing spaces at the end of strings. NO PAD collations treat trailing spaces as significant in comparisons, like any other character. PAD SPACE collations treat trailing spaces as insignificant in comparisons; strings are compared without regard to trailing spaces. See Trailing Space Handling in Comparisons. The server SQL mode has no effect on comparison behavior with respect to trailing spaces.

![](_page_60_Picture_9.jpeg)

## **Note**

For more information about MySQL character sets and collations, see Chapter 12, Character Sets, Collations, Unicode. For additional information about storage requirements, see [Section 13.7, "Data Type Storage](#page-104-0) [Requirements".](#page-104-0)

For those cases where trailing pad characters are stripped or comparisons ignore them, if a column has an index that requires unique values, inserting into the column values that differ only in number of trailing pad characters results in a duplicate-key error. For example, if a table contains 'a', an attempt to store 'a ' causes a duplicate-key error.

# <span id="page-60-0"></span>**13.3.3 The BINARY and VARBINARY Types**

The BINARY and VARBINARY types are similar to [CHAR](#page-59-0) and [VARCHAR](#page-59-0), except that they store binary strings rather than nonbinary strings. That is, they store byte strings rather than character strings. This means they have the binary character set and collation, and comparison and sorting are based on the numeric values of the bytes in the values.

The permissible maximum length is the same for BINARY and VARBINARY as it is for [CHAR](#page-59-0) and [VARCHAR](#page-59-0), except that the length for BINARY and VARBINARY is measured in bytes rather than characters.

The BINARY and VARBINARY data types are distinct from the CHAR BINARY and VARCHAR BINARY data types. For the latter types, the BINARY attribute does not cause the column to be treated as a binary string column. Instead, it causes the binary (\_bin) collation for the column character set (or the table default character set if no column character set is specified) to be used, and the column itself stores nonbinary character strings rather than binary byte strings. For example, if the default character set is utf8mb4, CHAR(5) BINARY is treated as CHAR(5) CHARACTER SET utf8mb4 COLLATE utf8mb4\_bin. This differs from BINARY(5), which stores 5-byte binary strings that have the binary character set and collation. For information about the differences between the binary collation of the binary character set and the \_bin collations of nonbinary character sets, see Section 12.8.5, "The binary Collation Compared to \_bin Collations".

If strict SQL mode is not enabled and you assign a value to a BINARY or VARBINARY column that exceeds the column's maximum length, the value is truncated to fit and a warning is generated. For cases of truncation, to cause an error to occur (rather than a warning) and suppress insertion of the value, use strict SQL mode. See Section 7.1.11, "Server SQL Modes".

When BINARY values are stored, they are right-padded with the pad value to the specified length. The pad value is 0x00 (the zero byte). Values are right-padded with 0x00 for inserts, and no trailing bytes are removed for retrievals. All bytes are significant in comparisons, including ORDER BY and DISTINCT operations. 0x00 and space differ in comparisons, with 0x00 sorting before space.

Example: For a BINARY(3) column, 'a ' becomes 'a \0' when inserted. 'a\0' becomes 'a \0\0' when inserted. Both inserted values remain unchanged for retrievals.

For VARBINARY, there is no padding for inserts and no bytes are stripped for retrievals. All bytes are significant in comparisons, including ORDER BY and DISTINCT operations. 0x00 and space differ in comparisons, with 0x00 sorting before space.

For those cases where trailing pad bytes are stripped or comparisons ignore them, if a column has an index that requires unique values, inserting values into the column that differ only in number of trailing pad bytes results in a duplicate-key error. For example, if a table contains 'a', an attempt to store 'a \0' causes a duplicate-key error.

You should consider the preceding padding and stripping characteristics carefully if you plan to use the BINARY data type for storing binary data and you require that the value retrieved be exactly the same as the value stored. The following example illustrates how 0x00-padding of BINARY values affects column value comparisons:

```
mysql> CREATE TABLE t (c BINARY(3));
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO t SET c = 'a';
Query OK, 1 row affected (0.01 sec)
mysql> SELECT HEX(c), c = 'a', c = 'a\0\0' from t;
+--------+---------+-------------+
| HEX(c) | c = 'a' | c = 'a\0\0' |
+--------+---------+-------------+
| 610000 | 0 | 1 |
+--------+---------+-------------+
1 row in set (0.09 sec)
```

If the value retrieved must be the same as the value specified for storage with no padding, it might be preferable to use VARBINARY or one of the [BLOB](#page-61-0) data types instead.

![](_page_61_Picture_10.jpeg)

#### **Note**

Within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

# <span id="page-61-0"></span>**13.3.4 The BLOB and TEXT Types**

A BLOB is a binary large object that can hold a variable amount of data. The four BLOB types are TINYBLOB, BLOB, MEDIUMBLOB, and LONGBLOB. These differ only in the maximum length of the values they can hold. The four TEXT types are TINYTEXT, TEXT, MEDIUMTEXT, and LONGTEXT. These correspond to the four BLOB types and have the same maximum lengths and storage requirements. See [Section 13.7, "Data Type Storage Requirements"](#page-104-0).

BLOB values are treated as binary strings (byte strings). They have the binary character set and collation, and comparison and sorting are based on the numeric values of the bytes in column values. TEXT values are treated as nonbinary strings (character strings). They have a character set other than binary, and values are sorted and compared based on the collation of the character set.

If strict SQL mode is not enabled and you assign a value to a BLOB or TEXT column that exceeds the column's maximum length, the value is truncated to fit and a warning is generated. For truncation of nonspace characters, you can cause an error to occur (rather than a warning) and suppress insertion of the value by using strict SQL mode. See Section 7.1.11, "Server SQL Modes".

Truncation of excess trailing spaces from values to be inserted into [TEXT](#page-61-0) columns always generates a warning, regardless of the SQL mode.

For TEXT and BLOB columns, there is no padding on insert and no bytes are stripped on select.

If a TEXT column is indexed, index entry comparisons are space-padded at the end. This means that, if the index requires unique values, duplicate-key errors occur for values that differ only in the number of trailing spaces. For example, if a table contains 'a', an attempt to store 'a ' causes a duplicate-key error. This is not true for BLOB columns.

In most respects, you can regard a BLOB column as a [VARBINARY](#page-60-0) column that can be as large as you like. Similarly, you can regard a TEXT column as a [VARCHAR](#page-59-0) column. BLOB and TEXT differ from [VARBINARY](#page-60-0) and [VARCHAR](#page-59-0) in the following ways:

- For indexes on BLOB and TEXT columns, you must specify an index prefix length. For [CHAR](#page-59-0) and [VARCHAR](#page-59-0), a prefix length is optional. See Section 10.3.5, "Column Indexes".
- BLOB and TEXT columns cannot have DEFAULT values.

If you use the BINARY attribute with a TEXT data type, the column is assigned the binary (\_bin) collation of the column character set.

LONG and LONG VARCHAR map to the MEDIUMTEXT data type. This is a compatibility feature.

MySQL Connector/ODBC defines BLOB values as LONGVARBINARY and TEXT values as LONGVARCHAR.

Because BLOB and TEXT values can be extremely long, you might encounter some constraints in using them:

• Only the first max\_sort\_length bytes of the column are used when sorting. The default value of max\_sort\_length is 1024. You can make more bytes significant in sorting or grouping by increasing the value of max\_sort\_length at server startup or runtime. Any client can change the value of its session max\_sort\_length variable:

```
mysql> SET max_sort_length = 2000;
mysql> SELECT id, comment FROM t
 -> ORDER BY comment;
```

- Instances of BLOB or TEXT columns in the result of a query that is processed using a temporary table causes the server to use a table on disk rather than in memory because the MEMORY storage engine does not support those data types (see Section 10.4.4, "Internal Temporary Table Use in MySQL"). Use of disk incurs a performance penalty, so include BLOB or TEXT columns in the query result only if they are really needed. For example, avoid using SELECT \*, which selects all columns.
- The maximum size of a BLOB or TEXT object is determined by its type, but the largest value you actually can transmit between the client and server is determined by the amount of available memory

and the size of the communications buffers. You can change the message buffer size by changing the value of the max\_allowed\_packet variable, but you must do so for both the server and your client program. For example, both mysql and mysqldump enable you to change the client-side max\_allowed\_packet value. See Section 7.1.1, "Configuring the Server", Section 6.5.1, "mysql — The MySQL Command-Line Client", and Section 6.5.4, "mysqldump — A Database Backup Program". You may also want to compare the packet sizes and the size of the data objects you are storing with the storage requirements, see [Section 13.7, "Data Type Storage Requirements"](#page-104-0)

Each BLOB or TEXT value is represented internally by a separately allocated object. This is in contrast to all other data types, for which storage is allocated once per column when the table is opened.

In some cases, it may be desirable to store binary data such as media files in BLOB or TEXT columns. You may find MySQL's string handling functions useful for working with such data. See [Section 14.8,](#page-186-0) ["String Functions and Operators".](#page-186-0) For security and other reasons, it is usually preferable to do so using application code rather than giving application users the FILE privilege. You can discuss specifics for various languages and platforms in the MySQL Forums ([http://forums.mysql.com/\)](http://forums.mysql.com/).

![](_page_63_Picture_4.jpeg)

#### **Note**

Within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

## <span id="page-63-0"></span>**13.3.5 The ENUM Type**

An ENUM is a string object with a value chosen from a list of permitted values that are enumerated explicitly in the column specification at table creation time.

See [Section 13.3.1, "String Data Type Syntax"](#page-55-2) for [ENUM](#page-63-0) type syntax and length limits.

The [ENUM](#page-63-0) type has these advantages:

- Compact data storage in situations where a column has a limited set of possible values. The strings you specify as input values are automatically encoded as numbers. See [Section 13.7, "Data Type](#page-104-0) [Storage Requirements"](#page-104-0) for storage requirements for the ENUM type.
- Readable queries and output. The numbers are translated back to the corresponding strings in query results.

and these potential issues to consider:

- If you make enumeration values that look like numbers, it is easy to mix up the literal values with their internal index numbers, as explained in [Enumeration Limitations.](#page-66-1)
- Using ENUM columns in ORDER BY clauses requires extra care, as explained in [Enumeration Sorting.](#page-65-0)
- [Creating and Using ENUM Columns](#page-63-1)
- [Index Values for Enumeration Literals](#page-64-0)
- [Handling of Enumeration Literals](#page-64-1)
- [Empty or NULL Enumeration Values](#page-65-1)
- [Enumeration Sorting](#page-65-0)
- [Enumeration Limitations](#page-66-1)

### <span id="page-63-1"></span>**Creating and Using ENUM Columns**

An enumeration value must be a quoted string literal. For example, you can create a table with an ENUM column like this:

```
CREATE TABLE shirts (
 name VARCHAR(40),
 size ENUM('x-small', 'small', 'medium', 'large', 'x-large')
);
INSERT INTO shirts (name, size) VALUES ('dress shirt','large'), ('t-shirt','medium'),
 ('polo shirt','small');
SELECT name, size FROM shirts WHERE size = 'medium';
+---------+--------+
| name | size |
+---------+--------+
| t-shirt | medium |
+---------+--------+
UPDATE shirts SET size = 'small' WHERE size = 'large';
COMMIT;
```

Inserting 1 million rows into this table with a value of 'medium' would require 1 million bytes of storage, as opposed to 6 million bytes if you stored the actual string 'medium' in a VARCHAR column.

### <span id="page-64-0"></span>**Index Values for Enumeration Literals**

Each enumeration value has an index:

- The elements listed in the column specification are assigned index numbers, beginning with 1.
- The index value of the empty string error value is 0. This means that you can use the following SELECT statement to find rows into which invalid ENUM values were assigned:

```
mysql> SELECT * FROM tbl_name WHERE enum_col=0;
```

- The index of the NULL value is NULL.
- The term "index" here refers to a position within the list of enumeration values. It has nothing to do with table indexes.

For example, a column specified as ENUM('Mercury', 'Venus', 'Earth') can have any of the values shown here. The index of each value is also shown.

| Value     | Index |
|-----------|-------|
| NULL      | NULL  |
| ''        | 0     |
| 'Mercury' | 1     |
| 'Venus'   | 2     |
| 'Earth'   | 3     |

An [ENUM](#page-63-0) column can have a maximum of 65,535 distinct elements.

If you retrieve an ENUM value in a numeric context, the column value's index is returned. For example, you can retrieve numeric values from an ENUM column like this:

```
mysql> SELECT enum_col+0 FROM tbl_name;
```

Functions such as SUM() or AVG() that expect a numeric argument cast the argument to a number if necessary. For ENUM values, the index number is used in the calculation.

### <span id="page-64-1"></span>**Handling of Enumeration Literals**

Trailing spaces are automatically deleted from ENUM member values in the table definition when a table is created.

When retrieved, values stored into an ENUM column are displayed using the lettercase that was used in the column definition. Note that ENUM columns can be assigned a character set and collation. For

binary or case-sensitive collations, lettercase is taken into account when assigning values to the column.

If you store a number into an ENUM column, the number is treated as the index into the possible values, and the value stored is the enumeration member with that index. (However, this does not work with LOAD DATA, which treats all input as strings.) If the numeric value is quoted, it is still interpreted as an index if there is no matching string in the list of enumeration values. For these reasons, it is not advisable to define an ENUM column with enumeration values that look like numbers, because this can easily become confusing. For example, the following column has enumeration members with string values of '0', '1', and '2', but numeric index values of 1, 2, and 3:

```
numbers ENUM('0','1','2')
```

If you store 2, it is interpreted as an index value, and becomes '1' (the value with index 2). If you store '2', it matches an enumeration value, so it is stored as '2'. If you store '3', it does not match any enumeration value, so it is treated as an index and becomes '2' (the value with index 3).

```
mysql> INSERT INTO t (numbers) VALUES(2),('2'),('3');
mysql> SELECT * FROM t;
+---------+
| numbers |
+---------+
| 1 |
| 2 |
| 2 |
+---------+
```

To determine all possible values for an ENUM column, use SHOW COLUMNS FROM tbl\_name LIKE 'enum\_col' and parse the ENUM definition in the Type column of the output.

In the C API, ENUM values are returned as strings. For information about using result set metadata to distinguish them from other strings, see [C API Basic Data Structures.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-data-structures.md)

## <span id="page-65-1"></span>**Empty or NULL Enumeration Values**

An enumeration value can also be the empty string ('') or NULL under certain circumstances:

• If you insert an invalid value into an ENUM (that is, a string not present in the list of permitted values), the empty string is inserted instead as a special error value. This string can be distinguished from a "normal" empty string by the fact that this string has the numeric value 0. See [Index Values for](#page-64-0) [Enumeration Literals](#page-64-0) for details about the numeric indexes for the enumeration values.

If strict SQL mode is enabled, attempts to insert invalid ENUM values result in an error.

• If an ENUM column is declared to permit NULL, the NULL value is a valid value for the column, and the default value is NULL. If an ENUM column is declared NOT NULL, its default value is the first element of the list of permitted values.

## <span id="page-65-0"></span>**Enumeration Sorting**

ENUM values are sorted based on their index numbers, which depend on the order in which the enumeration members were listed in the column specification. For example, 'b' sorts before 'a' for ENUM('b', 'a'). The empty string sorts before nonempty strings, and NULL values sort before all other enumeration values.

To prevent unexpected results when using the ORDER BY clause on an ENUM column, use one of these techniques:

- Specify the ENUM list in alphabetic order.
- Make sure that the column is sorted lexically rather than by index number by coding ORDER BY CAST(col AS CHAR) or ORDER BY CONCAT(col).

## <span id="page-66-1"></span>**Enumeration Limitations**

An enumeration value cannot be an expression, even one that evaluates to a string value.

For example, this CREATE TABLE statement does not work because the CONCAT function cannot be used to construct an enumeration value:

```
CREATE TABLE sizes (
 size ENUM('small', CONCAT('med','ium'), 'large')
);
```

You also cannot employ a user variable as an enumeration value. This pair of statements do not work:

```
SET @mysize = 'medium';
CREATE TABLE sizes (
 size ENUM('small', @mysize, 'large')
);
```

We strongly recommend that you do not use numbers as enumeration values, because it does not save on storage over the appropriate [TINYINT](#page-39-0) or [SMALLINT](#page-39-0) type, and it is easy to mix up the strings and the underlying number values (which might not be the same) if you quote the ENUM values incorrectly. If you do use a number as an enumeration value, always enclose it in quotation marks. If the quotation marks are omitted, the number is regarded as an index. See [Handling of Enumeration](#page-64-1) [Literals](#page-64-1) to see how even a quoted number could be mistakenly used as a numeric index value.

Duplicate values in the definition cause a warning, or an error if strict SQL mode is enabled.

## <span id="page-66-0"></span>**13.3.6 The SET Type**

A SET is a string object that can have zero or more values, each of which must be chosen from a list of permitted values specified when the table is created. SET column values that consist of multiple set members are specified with members separated by commas (,). A consequence of this is that SET member values should not themselves contain commas.

For example, a column specified as SET('one', 'two') NOT NULL can have any of these values:

```
'''one'
'two'
'one,two'
```

A [SET](#page-66-0) column can have a maximum of 64 distinct members.

Duplicate values in the definition cause a warning, or an error if strict SQL mode is enabled.

Trailing spaces are automatically deleted from SET member values in the table definition when a table is created.

See [String Type Storage Requirements](#page-106-0) for storage requirements for the [SET](#page-66-0) type.

See [Section 13.3.1, "String Data Type Syntax"](#page-55-2) for [SET](#page-66-0) type syntax and length limits.

When retrieved, values stored in a SET column are displayed using the lettercase that was used in the column definition. Note that SET columns can be assigned a character set and collation. For binary or case-sensitive collations, lettercase is taken into account when assigning values to the column.

MySQL stores SET values numerically, with the low-order bit of the stored value corresponding to the first set member. If you retrieve a SET value in a numeric context, the value retrieved has bits set corresponding to the set members that make up the column value. For example, you can retrieve numeric values from a SET column like this:

```
mysql> SELECT set_col+0 FROM tbl_name;
```

If a number is stored into a SET column, the bits that are set in the binary representation of the number determine the set members in the column value. For a column specified as SET('a','b','c','d'), the members have the following decimal and binary values.

| SET Member | Decimal Value | Binary Value |
|------------|---------------|--------------|
| 'a'        | 1             | 0001         |
| 'b'        | 2             | 0010         |
| 'c'        | 4             | 0100         |
| 'd'        | 8             | 1000         |

If you assign a value of 9 to this column, that is 1001 in binary, so the first and fourth SET value members 'a' and 'd' are selected and the resulting value is 'a,d'.

For a value containing more than one SET element, it does not matter what order the elements are listed in when you insert the value. It also does not matter how many times a given element is listed in the value. When the value is retrieved later, each element in the value appears once, with elements listed according to the order in which they were specified at table creation time. Suppose that a column is specified as SET('a','b','c','d'):

```
mysql> CREATE TABLE myset (col SET('a', 'b', 'c', 'd'));
```

If you insert the values 'a,d', 'd,a', 'a,d,d', 'a,d,a', and 'd,a,d':

```
mysql> INSERT INTO myset (col) VALUES 
-> ('a,d'), ('d,a'), ('a,d,a'), ('a,d,d'), ('d,a,d');
Query OK, 5 rows affected (0.01 sec)
Records: 5 Duplicates: 0 Warnings: 0
```

Then all these values appear as 'a,d' when retrieved:

```
mysql> SELECT col FROM myset;
+------+
| col |
+------+
| a,d |
| a,d |
| a,d |
| a,d |
| a,d |
+------+
5 rows in set (0.04 sec)
```

If you set a SET column to an unsupported value, the value is ignored and a warning is issued:

```
mysql> INSERT INTO myset (col) VALUES ('a,d,d,s');
Query OK, 1 row affected, 1 warning (0.03 sec)
mysql> SHOW WARNINGS;
+---------+------+------------------------------------------+
| Level | Code | Message |
+---------+------+------------------------------------------+
| Warning | 1265 | Data truncated for column 'col' at row 1 |
+---------+------+------------------------------------------+
1 row in set (0.04 sec)
mysql> SELECT col FROM myset;
+------+
| col |
+------+
| a,d |
| a,d |
| a,d |
| a,d |
| a,d |
| a,d |
```

```
+------+
6 rows in set (0.01 sec)
```

If strict SQL mode is enabled, attempts to insert invalid SET values result in an error.

SET values are sorted numerically. NULL values sort before non-NULL SET values.

Functions such as SUM() or AVG() that expect a numeric argument cast the argument to a number if necessary. For SET values, the cast operation causes the numeric value to be used.

Normally, you search for SET values using the [FIND\\_IN\\_SET\(\)](#page-191-1) function or the LIKE operator:

```
mysql> SELECT * FROM tbl_name WHERE FIND_IN_SET('value',set_col)>0;
mysql> SELECT * FROM tbl_name WHERE set_col LIKE '%value%';
```

The first statement finds rows where set\_col contains the value set member. The second is similar, but not the same: It finds rows where set\_col contains value anywhere, even as a substring of another set member.

The following statements also are permitted:

```
mysql> SELECT * FROM tbl_name WHERE set_col & 1;
mysql> SELECT * FROM tbl_name WHERE set_col = 'val1,val2';
```

The first of these statements looks for values containing the first set member. The second looks for an exact match. Be careful with comparisons of the second type. Comparing set values to 'val1,val2' returns different results than comparing values to 'val2,val1'. You should specify the values in the same order they are listed in the column definition.

To determine all possible values for a SET column, use SHOW COLUMNS FROM tbl\_name LIKE set\_col and parse the SET definition in the Type column of the output.

In the C API, SET values are returned as strings. For information about using result set metadata to distinguish them from other strings, see [C API Basic Data Structures.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-data-structures.md)

# <span id="page-68-0"></span>**13.4 Spatial Data Types**

The [Open Geospatial Consortium](http://www.opengeospatial.org) (OGC) is an international consortium of more than 250 companies, agencies, and universities participating in the development of publicly available conceptual solutions that can be useful with all kinds of applications that manage spatial data.

The Open Geospatial Consortium publishes the OpenGIS® Implementation Standard for Geographic information - Simple feature access - Part 2: SQL option, a document that proposes several conceptual ways for extending an SQL RDBMS to support spatial data. This specification is available from the OGC website at<http://www.opengeospatial.org/standards/sfs>.

Following the OGC specification, MySQL implements spatial extensions as a subset of the **SQL with Geometry Types** environment. This term refers to an SQL environment that has been extended with a set of geometry types. A geometry-valued SQL column is implemented as a column that has a geometry type. The specification describes a set of SQL geometry types, as well as functions on those types to create and analyze geometry values.

MySQL spatial extensions enable the generation, storage, and analysis of geographic features:

- Data types for representing spatial values
- Functions for manipulating spatial values
- Spatial indexing for improved access times to spatial columns

The spatial data types and functions are available for MyISAM, InnoDB, NDB, and ARCHIVE tables. For indexing spatial columns, MyISAM and InnoDB support both SPATIAL and non-SPATIAL indexes. The other storage engines support non-SPATIAL indexes, as described in Section 15.1.15, "CREATE INDEX Statement".

A **geographic feature** is anything in the world that has a location. A feature can be:

- An entity. For example, a mountain, a pond, a city.
- A space. For example, town district, the tropics.
- A definable location. For example, a crossroad, as a particular place where two streets intersect.

Some documents use the term **geospatial feature** to refer to geographic features.

**Geometry** is another word that denotes a geographic feature. Originally the word **geometry** meant measurement of the earth. Another meaning comes from cartography, referring to the geometric features that cartographers use to map the world.

The discussion here considers these terms synonymous: **geographic feature**, **geospatial feature**, **feature**, or **geometry**. The term most commonly used is **geometry**, defined as a point or an aggregate of points representing anything in the world that has a location.

The following material covers these topics:

- The spatial data types implemented in MySQL model
- The basis of the spatial extensions in the OpenGIS geometry model
- Data formats for representing spatial data
- How to use spatial data in MySQL
- Use of indexing for spatial data
- MySQL differences from the OpenGIS specification

For information about functions that operate on spatial data, see Section 14.16, "Spatial Analysis Functions".

## **Additional Resources**

These standards are important for the MySQL implementation of spatial operations:

- SQL/MM Part 3: Spatial.
- The [Open Geospatial Consortium](http://www.opengeospatial.org) publishes the OpenGIS® Implementation Standard for Geographic information, a document that proposes several conceptual ways for extending an SQL RDBMS to support spatial data. See in particular Simple Feature Access - Part 1: Common Architecture, and Simple Feature Access - Part 2: SQL Option. The Open Geospatial Consortium (OGC) maintains a website at <http://www.opengeospatial.org/>. The specification is available there at [http://](http://www.opengeospatial.org/standards/sfs) [www.opengeospatial.org/standards/sfs.](http://www.opengeospatial.org/standards/sfs) It contains additional information relevant to the material here.
- The grammar for [spatial reference system](#page-80-0) (SRS) definitions is based on the grammar defined in OpenGIS Implementation Specification: Coordinate Transformation Services, Revision 1.00, OGC 01-009, January 12, 2001, Section 7.2. This specification is available at [http://](http://www.opengeospatial.org/standards/ct) [www.opengeospatial.org/standards/ct.](http://www.opengeospatial.org/standards/ct) For differences from that specification in SRS definitions as implemented in MySQL, see Section 15.1.19, "CREATE SPATIAL REFERENCE SYSTEM Statement".

If you have questions or concerns about the use of the spatial extensions to MySQL, you can discuss them in the GIS forum: [https://forums.mysql.com/list.php?23.](https://forums.mysql.com/list.php?23)

## <span id="page-70-0"></span>**13.4.1 Spatial Data Types**

MySQL has spatial data types that correspond to OpenGIS classes. The basis for these types is described in [Section 13.4.2, "The OpenGIS Geometry Model"](#page-71-0).

Some spatial data types hold single geometry values:

- GEOMETRY
- POINT
- LINESTRING
- POLYGON

GEOMETRY can store geometry values of any type. The other single-value types (POINT, LINESTRING, and POLYGON) restrict their values to a particular geometry type.

The other spatial data types hold collections of values:

- MULTIPOINT
- MULTILINESTRING
- MULTIPOLYGON
- GEOMETRYCOLLECTION

GEOMETRYCOLLECTION can store a collection of objects of any type. The other collection types (MULTIPOINT, MULTILINESTRING, and MULTIPOLYGON) restrict collection members to those having a particular geometry type.

Example: To create a table named geom that has a column named g that can store values of any geometry type, use this statement:

```
CREATE TABLE geom (g GEOMETRY);
```

Columns with a spatial data type can have an SRID attribute, to explicitly indicate the spatial reference system (SRS) for values stored in the column. For example:

```
CREATE TABLE geom (
 p POINT SRID 0,
 g GEOMETRY NOT NULL SRID 4326
);
```

SPATIAL indexes can be created on spatial columns if they are NOT NULL and have a specific SRID, so if you plan to index the column, declare it with the NOT NULL and SRID attributes:

```
CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326);
```

InnoDB tables permit SRID values for Cartesian and geographic SRSs. MyISAM tables permit SRID values for Cartesian SRSs.

The SRID attribute makes a spatial column SRID-restricted, which has these implications:

- The column can contain only values with the given SRID. Attempts to insert values with a different SRID produce an error.
- The optimizer can use SPATIAL indexes on the column. See Section 10.3.3, "SPATIAL Index Optimization".

Spatial columns with no SRID attribute are not SRID-restricted and accept values with any SRID. However, the optimizer cannot use SPATIAL indexes on them until the column definition is modified to include an SRID attribute, which may require that the column contents first be modified so that all values have the same SRID.

For other examples showing how to use spatial data types in MySQL, see [Section 13.4.6, "Creating](#page-81-0) [Spatial Columns"](#page-81-0). For information about spatial reference systems, see [Section 13.4.5, "Spatial](#page-80-0) [Reference System Support"](#page-80-0).

## <span id="page-71-0"></span>**13.4.2 The OpenGIS Geometry Model**

The set of geometry types proposed by OGC's **SQL with Geometry Types** environment is based on the **OpenGIS Geometry Model**. In this model, each geometric object has the following general properties:

- It is associated with a spatial reference system, which describes the coordinate space in which the object is defined.
- It belongs to some geometry class.

### **13.4.2.1 The Geometry Class Hierarchy**

The geometry classes define a hierarchy as follows:

- Geometry (noninstantiable)
  - Point (instantiable)
  - Curve (noninstantiable)
    - LineString (instantiable)
      - Line
      - LinearRing
  - Surface (noninstantiable)
    - Polygon (instantiable)
  - GeometryCollection (instantiable)
    - MultiPoint (instantiable)
    - MultiCurve (noninstantiable)
      - MultiLineString (instantiable)
    - MultiSurface (noninstantiable)
      - MultiPolygon (instantiable)

It is not possible to create objects in noninstantiable classes. It is possible to create objects in instantiable classes. All classes have properties, and instantiable classes may also have assertions (rules that define valid class instances).

Geometry is the base class. It is an abstract class. The instantiable subclasses of Geometry are restricted to zero-, one-, and two-dimensional geometric objects that exist in two-dimensional coordinate space. All instantiable geometry classes are defined so that valid instances of a geometry class are topologically closed (that is, all defined geometries include their boundary).

The base Geometry class has subclasses for Point, Curve, Surface, and GeometryCollection:

• Point represents zero-dimensional objects.

- Curve represents one-dimensional objects, and has subclass LineString, with sub-subclasses Line and LinearRing.
- Surface is designed for two-dimensional objects and has subclass Polygon.
- GeometryCollection has specialized zero-, one-, and two-dimensional collection classes named MultiPoint, MultiLineString, and MultiPolygon for modeling geometries corresponding to collections of Points, LineStrings, and Polygons, respectively. MultiCurve and MultiSurface are introduced as abstract superclasses that generalize the collection interfaces to handle Curves and Surfaces.

Geometry, Curve, Surface, MultiCurve, and MultiSurface are defined as noninstantiable classes. They define a common set of methods for their subclasses and are included for extensibility.

Point, LineString, Polygon, GeometryCollection, MultiPoint, MultiLineString, and MultiPolygon are instantiable classes.