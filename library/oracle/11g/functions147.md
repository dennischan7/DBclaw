# Oracle 11g - functions147
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions147.htm

# REGEXP\_COUNT

Syntax

Purpose

`REGEXP_COUNT` complements the functionality of the `REGEXP_INSTR` function by returning the number of times a pattern occurs in a source string. The function evaluates strings using characters as defined by the input character set. It returns an integer indicating the number of occurrences of `pattern`. If no match is found, then the function returns 0.

* `source_char` is a character expression that serves as the search value. It is commonly a character column and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`.
* `pattern` is the regular expression. It is usually a text literal and can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. It can contain up to 512 bytes. If the data type of `pattern` is different from the data type of `source_char`, then Oracle Database converts `pattern` to the data type of `source_char`.

  `REGEXP_COUNT` ignores subexpression parentheses in `pattern`. For example, the pattern `'(123(45))'` is equivalent to `'12345'`. For a listing of the operators you can specify in `pattern`, refer to [Appendix D, "Oracle Regular Expression Support"](ap_posix.md#g693775).
* `position` is a positive integer indicating the character of `source_char` where Oracle should begin the search. The default is 1, meaning that Oracle begins the search at the first character of `source_char`. After finding the first occurrence of `pattern`, the database searches for a second occurrence beginning with the first character following the first occurrence.
* `match_param` is a text literal that lets you change the default matching behavior of the function. You can specify one or more of the following values for `match_param`:

  + `'i'` specifies case-insensitive matching.
  + `'c'` specifies case-sensitive matching.
  + `'n'` allows the period (.), which is the match-any-character character, to match the newline character. If you omit this parameter, then the period does not match the newline character.
  + `'m'` treats the source string as multiple lines. Oracle interprets the caret (`^`) and dollar sign (`$`) as the start and end, respectively, of any line anywhere in the source string, rather than only at the start or end of the entire source string. If you omit this parameter, then Oracle treats the source string as a single line.
  + `'x'` ignores whitespace characters. By default, whitespace characters match themselves.

  If you specify multiple contradictory values, then Oracle uses the last value. For example, if you specify `'ic'`, then Oracle uses case-sensitive matching. If you specify a character other than those shown above, then Oracle returns an error.

  If you omit `match_param`, then:

  + The default case sensitivity is determined by the value of the `NLS_SORT` parameter.
  + A period (.) does not match the newline character.
  + The source string is treated as a single line.

Examples

The following example shows that subexpressions parentheses in pattern are ignored:

```
SELECT REGEXP_COUNT('123123123123123', '(12)3', 1, 'i') REGEXP_COUNT
   FROM DUAL;
 
REGEXP_COUNT
------------
           5
```

In the following example, the function begins to evaluate the source string at the third character, so skips over the first occurrence of pattern:

```
SELECT REGEXP_COUNT('123123123123', '123', 3, 'i') COUNT FROM DUAL; 

     COUNT
----------
         3
```