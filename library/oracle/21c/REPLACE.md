# Oracle 21c - REPLACE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/REPLACE.html

`REPLACE` returns `char` with every occurrence of `search_string` replaced with `replacement_string`. If `replacement_string` is omitted or null, then all occurrences of `search_string` are removed. If `search_string` is null, then `char` is returned.

Both `search_string` and `replacement_string`, as well as `char`, can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. The string returned is in the same character set as `char`. The function returns `VARCHAR2` if the first argument is not a LOB and returns `CLOB` if the first argument is a LOB.

`REPLACE` provides functionality related to that provided by the `TRANSLATE` function. `TRANSLATE` provides single-character, one-to-one substitution. `REPLACE` lets you substitute one string for another as well as to remove character strings.

See Also:

* [TRANSLATE](TRANSLATE.md#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690)
* Appendix C in [Oracle Database Globalization Support Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/21/sqlrf&id=NLSPG-GUID-AFCE41ED-775B-4A00-AF38-C436776AE0C5) for the collation determination rules, which define the collation `REPLACE` uses to compare characters from `char` with characters from `search_string`, and for the collation derivation rules, which define the collation assigned to the character return value of this function

The following example replaces occurrences of `J` with `BL`:

```
SELECT REPLACE('JACK and JUE','J','BL') "Changes"
     FROM DUAL;

Changes
--------------
BLACK and BLUE
```