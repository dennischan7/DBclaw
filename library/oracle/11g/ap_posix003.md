# Oracle 11g - ap_posix003
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/ap_posix003.htm

[Go to main content](#BEGIN)

515/522 

# Perl-influenced Extensions in Oracle Regular Expressions

Oracle Database regular expression functions and conditions accept a number of Perl-influenced operators that are in common use, although not part of the POSIX standard. [Table D-3](#CEGCDCCF) lists those operators. For more complete descriptions with examples, refer to [Oracle Database Advanced Application Developer's Guide](../../appdev.112/e41502/adfns_regexp.md#ADFNS1012).

Table D-3 Perl-influenced Operators in Oracle Regular Expressions

| Operator | Description |
| --- | --- |
| \d | A digit character. |
| \D | A nondigit character. |
| \w | A word character. |
| \W | A nonword character. |
| \s | A whitespace character. |
| \S | A non-whitespace character. |
| \A | Matches only at the beginning of a string, or before a newline character at the end of a string. |
| \Z | Matches only at the end of a string. |
| \*? | Matches the preceding pattern element 0 or more times (nongreedy). |
| +? | Matches the preceding pattern element 1 or more times (nongreedy). |
| ?? | Matches the preceding pattern element 0 or 1 time (nongreedy). |
| {n}? | Matches the preceding pattern element exactly `n` times (nongreedy). |
| {n,}? | Matches the preceding pattern element at least `n` times (nongreedy). |
| {n,m}? | Matches the preceding pattern element at least `n` but not more than `m` times (nongreedy). |

Scripting on this page enhances content navigation, but does not change the content in any way.