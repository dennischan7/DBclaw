# Oracle 11g - functions150
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions150.htm

# REGEXP\_SUBSTR

Syntax

Purpose

`REGEXP_SUBSTR` extends the functionality of the `SUBSTR` function by letting you search a string for a regular expression pattern. It is also similar to `REGEXP_INSTR`, but instead of returning the position of the substring, it returns the substring itself. This function is useful if you need the contents of a match string but not its position in the source string. The function returns the string as `VARCHAR2` or `CLOB` data in the same character set as `source_char`.

This function complies with the POSIX regular expression standard and the Unicode Regular Expression Guidelines. For more information, refer to [Appendix D, "Oracle Regular Expression Support"](ap_posix.md#g693775).

* `source_char` is a character expression that serves as the search value. It is commonly a character column and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`.
* `pattern` is the regular expression. It is usually a text literal and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. It can contain up to 512 bytes. If the data type of `pattern` is different from the data type of `source_char`, then Oracle Database converts `pattern` to the data type of `source_char`. For a listing of the operators you can specify in `pattern`, refer to [Appendix D, "Oracle Regular Expression Support"](ap_posix.md#g693775).
* `position` is a positive integer indicating the character of `source_char` where Oracle should begin the search. The default is 1, meaning that Oracle begins the search at the first character of `source_char`.
* `occurrence` is a positive integer indicating which occurrence of `pattern` in `source_char` Oracle should search for. The default is 1, meaning that Oracle searches for the first occurrence of `pattern`.

  If `occurrence` is greater than 1, then the database searches for the second occurrence beginning with the first character following the first occurrence of `pattern`, and so forth. This behavior is different from the `SUBSTR` function, which begins its search for the second occurrence at the second character of the first occurrence.
* `match_parameter` is a text literal that lets you change the default matching behavior of the function. The behavior of this parameter is the same for this function as for `REGEXP_COUNT`. Refer to [REGEXP\_COUNT](functions147.md#CIHDAIHJ) for detailed information.
* For a `pattern` with subexpressions, `subexpr` is a nonnegative integer from 0 to 9 indicating which subexpression in `pattern` is to be returned by the function. This parameter has the same semantics that it has for the `REGEXP_INSTR` function. Refer to [REGEXP\_INSTR](functions148.md#i1239887) for more information.

Examples

The following example examines the string, looking for the first substring bounded by commas. Oracle Database searches for a comma followed by one or more occurrences of non-comma characters followed by a comma. Oracle returns the substring, including the leading and trailing commas.

```
SELECT
  REGEXP_SUBSTR('500 Oracle Parkway, Redwood Shores, CA',
                ',[^,]+,') "REGEXPR_SUBSTR"
  FROM DUAL;

REGEXPR_SUBSTR
-----------------
, Redwood Shores,
```

The following example examines the string, looking for `http://` followed by a substring of one or more alphanumeric characters and optionally, a period (`.`). Oracle searches for a minimum of three and a maximum of four occurrences of this substring between `http://` and either a slash (`/`) or the end of the string.

```
SELECT
  REGEXP_SUBSTR('http://www.example.com/products',
                'http://([[:alnum:]]+\.?){3,4}/?') "REGEXP_SUBSTR"
  FROM DUAL;

REGEXP_SUBSTR
----------------------
http://www.example.com/
```

The next two examples use the `subexpr` argument to return a specific subexpression of `pattern`. The first statement returns the first subexpression in `pattern`:

```
SELECT REGEXP_SUBSTR('1234567890', '(123)(4(56)(78))', 1, 1, 'i', 1) 
"REGEXP_SUBSTR" FROM DUAL;

REGEXP_SUBSTR
-------------------
123
```

The next statement returns the fourth subexpression in `pattern`:

```
SELECT REGEXP_SUBSTR('1234567890', '(123)(4(56)(78))', 1, 1, 'i', 4) 
"REGEXP_SUBSTR" FROM DUAL;

REGEXP_SUBSTR
-------------------
78
```