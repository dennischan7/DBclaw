# Oracle 11g - functions104
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions104.htm

[Go to main content](#BEGIN)

144/522 

# NCHR

Syntax

Purpose

`NCHR` returns the character having the binary equivalent to `number` in the national character set. The value returned is always `NVARCHAR2`. This function is equivalent to using the `CHR` function with the `USING` `NCHAR_CS` clause.

This function takes as an argument a `NUMBER` value, or any value that can be implicitly converted to `NUMBER`, and returns a character.

Examples

The following examples return the nchar character 187:

```
SELECT NCHR(187)
  FROM DUAL;

N
-
> 

SELECT CHR(187 USING NCHAR_CS)
  FROM DUAL;

C
-
>
```

Scripting on this page enhances content navigation, but does not change the content in any way.