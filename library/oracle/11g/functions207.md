# Oracle 11g - functions207
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions207.htm

[Go to main content](#BEGIN)

247/522 

# TO\_NCHAR (character)

Syntax

to\_nchar\_char::=

Purpose

`TO_NCHAR` (character) converts a character string, `CHAR`, `VARCHAR2`, `CLOB`, or `NCLOB` value to the national character set. The value returned is always `NVARCHAR2`. This function is equivalent to the `TRANSLATE` ... `USING` function with a `USING` clause in the national character set.

Examples

The following example converts `VARCHAR2` data from the `oe.customers` table to the national character set:

```
SELECT TO_NCHAR(cust_last_name) FROM customers
   WHERE customer_id=103;

TO_NCHAR(CUST_LAST_NAME)
--------------------------------------------------
Taylor
```

Scripting on this page enhances content navigation, but does not change the content in any way.