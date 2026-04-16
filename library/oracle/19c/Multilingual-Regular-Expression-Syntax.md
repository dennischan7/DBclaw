# Oracle 19c - Multilingual-Regular-Expression-Syntax
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Multilingual-Regular-Expression-Syntax.html

|  |  |
| --- | --- |
| \ | The backslash character can have four different meanings depending on the context. It can:   * Stand for itself * Quote the next character * Introduce an operator * Do nothing |
| \* | Matches zero or more occurrences |
| + | Matches one or more occurrences |
| ? | Matches zero or one occurrence |
| | | Alternation operator for specifying alternative matches |
| ^ | Matches the beginning of a string by default. In multiline mode, it matches the beginning of any line anywhere within the source string. |
| $ | Matches the end of a string by default. In multiline mode, it matches the end of any line anywhere within the source string. |
| . | Matches any character in the supported character set except `NULL` |
| [ ] | Bracket expression for specifying a matching list that should match any one of the expressions represented in the list. A non-matching list expression begins with a circumflex (^) and specifies a list that matches any character except for the expressions represented in the list.  To specify a right bracket (]) in the bracket expression, place it first in the list (after the initial circumflex (^), if any).  To specify a hyphen in the bracket expression, place it first in the list (after the initial circumflex (^), if any), last in the list, or as an ending range point in a range expression. |
| ( ) | Grouping expression, treated as a single subexpression |
| {m} | Matches exactly m times |
| {m,} | Matches at least m times |
| {m,n} | Matches at least m times but no more than n times |
| \n | The backreference expression (n is a digit between 1 and 9) matches the nth subexpression enclosed between '(' and ')' preceding the \n |
| [..] | Specifies one collation element, and can be a multicharacter element (for example, [.ch.] in Spanish) |
| [: :] | Specifies character classes (for example, [:alpha:]). It matches any character within the character class. |
| [==] | Specifies equivalence classes. For example, [=a=] matches all characters having base letter 'a'. |