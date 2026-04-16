# Oracle 11g - functions108
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions108.htm

[Go to main content](#BEGIN)

148/522 

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