# Oracle 11g - functions034
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions034.htm

# CONVERT

Syntax

Purpose

`CONVERT` converts a character string from one character set to another.

* The `char` argument is the value to be converted. It can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`.
* The `dest_char_set` argument is the name of the character set to which `char` is converted.
* The `source_char_set` argument is the name of the character set in which `char` is stored in the database. The default value is the database character set.

The return value for `CHAR` and `VARCHAR2` is `VARCHAR2`. For `NCHAR` and `NVARCHAR2`, it is `NVARCHAR2`. For `CLOB`, it is `CLOB`, and for `NCLOB`, it is `NCLOB`.

Both the destination and source character set arguments can be either literals or columns containing the name of the character set.

For complete correspondence in character conversion, it is essential that the destination character set contains a representation of all the characters defined in the source character set. Where a character does not exist in the destination character set, a replacement character appears. Replacement characters can be defined as part of a character set definition.

Note:

Oracle discourages the use of the

`CONVERT`

function in the current Oracle Database release. The return value of

`CONVERT`

has a character data type, so it should be either in the database character set or in the national character set, depending on the data type. Any

`dest_char_set`

that is not one of these two character sets is unsupported. The

`char`

argument and the

`source_char_set`

have the same requirements. Therefore, the only practical use of the function is to correct data that has been stored in a wrong character set.

Values that are in neither the database nor the national character set should be processed and stored as `RAW` or `BLOB`. Procedures in the PL/SQL packages `UTL_RAW` and `UTL_I18N`—for example, `UTL_RAW.CONVERT`—allow limited processing of such values. Procedures accepting a `RAW` argument in the packages `UTL_FILE`, `UTL_TCP`, `UTL_HTTP`, and `UTL_SMTP` can be used to output the processed data.

Examples

The following example illustrates character set conversion by converting a Latin-1 string to ASCII. The result is the same as importing the same string from a WE8ISO8859P1 database to a US7ASCII database.

```
SELECT CONVERT('Ä Ê Í Õ Ø A B C D E ', 'US7ASCII', 'WE8ISO8859P1') 
   FROM DUAL; 

CONVERT('ÄÊÍÕØABCDE' 
--------------------- 
A E I ? ? A B C D E ?
```

Common character sets include:

* US7ASCII: US 7-bit ASCII character set
* WE8ISO8859P1: ISO 8859-1 West European 8-bit character set
* EE8MSWIN1250: Microsoft Windows East European Code Page 1250
* WE8MSWIN1252: Microsoft Windows West European Code Page 1252
* WE8EBCDIC1047: IBM West European EBCDIC Code Page 1047
* JA16SJISTILDE: Japanese Shift-JIS Character Set, compatible with MS Code Page 932
* ZHT16MSWIN950: Microsoft Windows Traditional Chinese Code Page 950
* UTF8: Unicode 3.0 Universal character set CESU-8 encoding form
* AL32UTF8: Unicode 5.0 Universal character set UTF-8 encoding form

You can query the `V$NLS_VALID_VALUES` view to get a listing of valid character sets, as follows:

```
SELECT * FROM V$NLS_VALID_VALUES WHERE parameter = 'CHARACTERSET';
```