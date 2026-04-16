# Oracle 11g - functions149
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions149.htm

# REGEXP\_REPLACE

Syntax

Purpose

`REGEXP_REPLACE` extends the functionality of the `REPLACE` function by letting you search a string for a regular expression pattern. By default, the function returns `source_char` with every occurrence of the regular expression pattern replaced with `replace_string`. The string returned is in the same character set as `source_char`. The function returns `VARCHAR2` if the first argument is not a LOB and returns `CLOB` if the first argument is a LOB.

This function complies with the POSIX regular expression standard and the Unicode Regular Expression Guidelines. For more information, refer to [Appendix D, "Oracle Regular Expression Support"](ap_posix.md#g693775).

* `source_char` is a character expression that serves as the search value. It is commonly a character column and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB` or `NCLOB`.
* `pattern` is the regular expression. It is usually a text literal and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. It can contain up to 512 bytes. If the data type of `pattern` is different from the data type of `source_char`, then Oracle Database converts `pattern` to the data type of `source_char`. For a listing of the operators you can specify in `pattern`, refer to [Appendix D, "Oracle Regular Expression Support"](ap_posix.md#g693775).
* `replace_string` can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. If `replace_string` is a `CLOB` or `NCLOB`, then Oracle truncates `replace_string` to 32K. The `replace_string` can contain up to 500 backreferences to subexpressions in the form `\n`, where `n` is a number from 1 to 9. If you want to include a backslash (`\`) in `replace_string`, then you must precede it with the escape character, which is also a backslash. For example, to replace `\2` you would enter `\\2`. For more information on backreference expressions, refer to the notes to ["Oracle Regular Expression Support"](ap_posix.md#g693775), [Table D-1](ap_posix001.md#BABJDBHB).
* `position` is a positive integer indicating the character of `source_char` where Oracle should begin the search. The default is 1, meaning that Oracle begins the search at the first character of `source_char`.
* `occurrence` is a nonnegative integer indicating the occurrence of the replace operation:

  + If you specify 0, then Oracle replaces all occurrences of the match.
  + If you specify a positive integer `n`, then Oracle replaces the `n`th occurrence.

  If `occurrence` is greater than 1, then the database searches for the second occurrence beginning with the first character following the first occurrence of `pattern`, and so forth. This behavior is different from the `INSTR` function, which begins its search for the second occurrence at the second character of the first occurrence.
* `match_parameter` is a text literal that lets you change the default matching behavior of the function. The behavior of this parameter is the same for this function as for `REGEXP_COUNT`. Refer to [REGEXP\_COUNT](functions147.md#CIHDAIHJ) for detailed information.

Examples

The following example examines `phone_number`, looking for the pattern `xxx`.`xxx`.`xxxx`. Oracle reformats this pattern with (`xxx`) `xxx`-`xxxx`.

```
SELECT
  REGEXP_REPLACE(phone_number,
                 '([[:digit:]]{3})\.([[:digit:]]{3})\.([[:digit:]]{4})',
                 '(\1) \2-\3') "REGEXP_REPLACE"
  FROM employees
  ORDER BY "REGEXP_REPLACE";

REGEXP_REPLACE
--------------------------------------------------------------------------------
(515) 123-4444
(515) 123-4567
(515) 123-4568
(515) 123-4569
(515) 123-5555
. . .
```

The following example examines `country_name`. Oracle puts a space after each non-null character in the string.

```
SELECT
  REGEXP_REPLACE(country_name, '(.)', '\1 ') "REGEXP_REPLACE"
  FROM countries;

REGEXP_REPLACE
--------------------------------------------------------------------------------
A r g e n t i n a
A u s t r a l i a
B e l g i u m
B r a z i l
C a n a d a
. . .
```

The following example examines the string, looking for two or more spaces. Oracle replaces each occurrence of two or more spaces with a single space.

```
SELECT
  REGEXP_REPLACE('500   Oracle     Parkway,    Redwood  Shores, CA',
                 '( ){2,}', ' ') "REGEXP_REPLACE"
  FROM DUAL;

REGEXP_REPLACE
--------------------------------------
500 Oracle Parkway, Redwood Shores, CA
```