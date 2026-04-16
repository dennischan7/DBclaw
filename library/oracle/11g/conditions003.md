# Oracle 11g - conditions003
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/conditions003.htm

[Go to main content](#BEGIN)

316/522 

# Floating-Point Conditions

The floating-point conditions let you determine whether an expression is infinite or is the undefined result of an operation (is not a number or `NaN`).

floating\_point\_condition::=

In both forms of floating-point condition, `expr` must resolve to a numeric data type or to any data type that can be implicitly converted to a numeric data type. [Table 7-3](#CJAFFCAE) describes the floating-point conditions.

Table 7-3 Floating-Point Conditions

| Type of Condition | Operation | Example |
| --- | --- | --- |
| ``` IS [NOT] NAN ``` | Returns `TRUE` if `expr` is the special value `NaN` when `NOT` is not specified. Returns `TRUE` if `expr` is not the special value `NaN` when `NOT` is specified. | ``` SELECT COUNT(*) FROM employees   WHERE commission_pct IS NOT NAN; ``` |
| ``` IS [NOT] INFINITE ``` | Returns `TRUE` if `expr` is the special value +`INF` or -`INF` when `NOT` is not specified. Returns `TRUE` if `expr` is neither +`INF` nor -`INF` when `NOT` is specified. | ``` SELECT last_name FROM employees   WHERE salary IS NOT INFINITE; ``` |

Scripting on this page enhances content navigation, but does not change the content in any way.