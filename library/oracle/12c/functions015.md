# Oracle 12c - functions015
Source: https://docs.oracle.com/database/121/SQLRF/functions015.htm

[Go to main content](#BEGIN)

88/555 

# ASCIISTR

Syntax

Purpose

`ASCIISTR` takes as its argument a string, or an expression that resolves to a string, in any character set and returns an ASCII version of the string in the database character set. Non-ASCII characters are converted to the form `\xxxx`, where `xxxx` represents a UTF-16 code unit.

Examples

The following example returns the ASCII string equivalent of the text string "`ABÄCDE`":

```
SELECT ASCIISTR('ABÄCDE')
  FROM DUAL;

ASCIISTR('
----------
AB\00C4CDE
```

Scripting on this page enhances content navigation, but does not change the content in any way.