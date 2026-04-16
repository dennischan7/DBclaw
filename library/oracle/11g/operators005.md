# Oracle 11g - operators005
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/operators005.htm

[Go to main content](#BEGIN)

37/522 

# Set Operators

Set operators combine the results of two component queries into a single result. Queries containing set operators are called compound queries. [Table 4-4](#CIHECBJH) lists SQL set operators. They are fully described, including examples and restrictions on these operators, in ["The UNION [ALL], INTERSECT, MINUS Operators"](queries004.md#i2054381).

Table 4-4 Set Operators

| Operator | Returns |
| --- | --- |
| `UNION` | All distinct rows selected by either query |
| `UNION ALL` | All rows selected by either query, including all duplicates |
| `INTERSECT` | All distinct rows selected by both queries |
| `MINUS` | All distinct rows selected by the first query but not the second |

Scripting on this page enhances content navigation, but does not change the content in any way.