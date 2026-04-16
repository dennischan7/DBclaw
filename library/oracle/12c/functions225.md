# Oracle 12c - functions225
Source: https://docs.oracle.com/database/121/SQLRF/functions225.htm

[Go to main content](#BEGIN)

298/555 

# TO\_NCHAR (number)

Syntax

to\_nchar\_number::=

Purpose

`TO_NCHAR` (number) converts `n` to a string in the national character set. The value `n` can be of type `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE`. The function returns a value of the same type as the argument. The optional `fmt` and `'nlsparam'` corresponding to `n` can be of `DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `TIME` `ZONE`, `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`, `INTERVAL` `MONTH` `TO` `YEAR`, or `INTERVAL` `DAY` `TO` `SECOND` data type.

Examples

The following example converts the `customer_id` values from the sample table `oe.orders` to the national character set:

```
SELECT TO_NCHAR(customer_id) "NCHAR_Customer_ID"  FROM orders 
   WHERE order_status > 9
   ORDER BY "NCHAR_Customer_ID";

NCHAR_Customer_ID
----------------------------------------
102
103
148
148
149
```

Scripting on this page enhances content navigation, but does not change the content in any way.