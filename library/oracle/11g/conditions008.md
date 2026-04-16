# Oracle 11g - conditions008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/conditions008.htm

[Go to main content](#BEGIN)

321/522 

# Null Conditions

A `NULL` condition tests for nulls. This is the only condition that you should use to test for nulls.

null\_condition::=

[Table 7-9](#CJAFCIGE) lists the null conditions.

Table 7-9 Null Condition

| Type of Condition | Operation | Example |
| --- | --- | --- |
| ``` IS [NOT] NULL ``` | Tests for nulls.  See Also: ["Nulls"](sql_elements005.md#i59110) | ``` SELECT last_name   FROM employees   WHERE commission_pct   IS NULL   ORDER BY last_name; ``` |

Scripting on this page enhances content navigation, but does not change the content in any way.