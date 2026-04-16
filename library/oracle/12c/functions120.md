# Oracle 12c - functions120
Source: https://docs.oracle.com/database/121/SQLRF/functions120.htm

[Go to main content](#BEGIN)

193/555 

# NLS\_CHARSET\_ID

Syntax

Purpose

`NLS_CHARSET_ID` returns the character set ID number corresponding to character set name `string`. The `string` argument is a run-time `VARCHAR2` value. The `string` value '`CHAR_CS`' returns the database character set ID number of the server. The `string` value '`NCHAR_CS`' returns the national character set ID number of the server.

Invalid character set names return null.

Examples

The following example returns the character set ID of a character set:

```
SELECT NLS_CHARSET_ID('ja16euc') 
  FROM DUAL; 

NLS_CHARSET_ID('JA16EUC')
------------------------- 
                      830
```

Scripting on this page enhances content navigation, but does not change the content in any way.