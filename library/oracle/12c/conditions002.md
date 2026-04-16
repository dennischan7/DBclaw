# Oracle 12c - conditions002
Source: https://docs.oracle.com/database/121/SQLRF/conditions002.htm

# Comparison Conditions

Comparison conditions compare one expression with another. The result of such a comparison can be `TRUE`, `FALSE`, or `UNKNOWN`.

Large objects (LOBs) are not supported in comparison conditions. However, you can use PL/SQL programs for comparisons on `CLOB` data.

When comparing numeric expressions, Oracle uses numeric precedence to determine whether the condition compares `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE` values. Refer to ["Numeric Precedence"](sql_elements001.md#i156865) for information on numeric precedence.

When comparing character expressions, Oracle uses the rules described in ["Data Type Comparison Rules"](sql_elements002.md#i55214). The rules define how the character sets of the expressions are aligned before the comparison, the use of binary or linguistic comparison (collation), and the use of blank-padded comparison semantics.

When character values are compared linguistically using the comparison conditions, they are first transformed to collation keys and then compared like `RAW` values. The collation keys are the same values that are returned by the function `NLSSORT` and are subject to the same restrictions that are described in ["NLSSORT"](functions125.md#i78399). As a result of these restrictions, two expressions may compare as linguistically equal if they do not differ in the prefix that was used to produce the collation key, even if they differ in the rest of the value.

Two objects of nonscalar type are comparable if they are of the same named type and there is a one-to-one correspondence between their elements. In addition, nested tables of user-defined object types, even if their elements are comparable, must have `MAP` methods defined on them to be used in equality or `IN` conditions.

[Table 6-2](#CJAGAABC) lists comparison conditions.

Table 6-2 Comparison Conditions

| Type of Condition | Purpose | Example |
| --- | --- | --- |
| `=` | Equality test. | ``` SELECT *   FROM employees   WHERE salary = 2500   ORDER BY employee_id; ``` |
| `!=`  `^=`  `<>`  `logical_negation_symbol``=` (Note 1) | Inequality test. Some forms of the inequality condition may be unavailable on some platforms. | ``` SELECT *   FROM employees   WHERE salary != 2500   ORDER BY employee_id; ``` |
| `>`  `<` | Greater-than and less-than tests. | ``` SELECT * FROM employees   WHERE salary > 2500   ORDER BY employee_id; SELECT * FROM employees   WHERE salary < 2500   ORDER BY employee_id; ``` |
| `>=`  `<=` | Greater-than-or-equal-to and less-than-or-equal-to tests. | ``` SELECT * FROM employees   WHERE salary >= 2500   ORDER BY employee_id; SELECT * FROM employees   WHERE salary <= 2500   ORDER BY employee_id; ``` |
| `ANY`  `SOME` | Compares a value to each value in a list or returned by a query. Must be preceded by =, !=, >, <, <=, >=. Can be followed by any expression or subquery that returns one or more values.  Evaluates to `FALSE` if the query returns no rows. | ``` SELECT * FROM employees   WHERE salary = ANY   (SELECT salary     FROM employees   WHERE department_id = 30)   ORDER BY employee_id; ``` |
| `ALL` | Compares a value to every value in a list or returned by a query. Must be preceded by =, !=, >, <, <=, >=. Can be followed by any expression or subquery that returns one or more values.  Evaluates to `TRUE` if the query returns no rows. | ``` SELECT * FROM employees   WHERE salary >=   ALL (1400, 3000)   ORDER BY employee_id; ``` |

Note 1: `logical_negation_symbol` is the ASCII character with decimal value 170.

## Simple Comparison Conditions

A simple comparison condition specifies a comparison with expressions or subquery results.

simple\_comparison\_condition::=

expression\_list::=

If you use the lower form of this condition with a single expression to the left of the operator, then you can use the upper or lower form of `expression_list`. If you use the lower form of this condition with multiple expressions to the left of the operator, then you must use the lower form of `expression_list`. In either case, the expressions in `expression_list` must match in number and data type the expressions to the left of the operator. If you specify `subquery`, then the values returned by the subquery must match in number and data type the expressions to the left of the operator.

See Also:

["Expression Lists"](expressions016.md#i1033664)

for more information about combining expressions and

[SELECT](statements_10002.md#i2065646)

for information about subqueries

## Group Comparison Conditions

A group comparison condition specifies a comparison with any or all members in a list or subquery.

group\_comparison\_condition::=

expression\_list::=

If you use the upper form of this condition (with a single expression to the left of the operator), then you must use the upper form of `expression_list`. If you use the lower form of this condition (with multiple expressions to the left of the operator), then you must use the lower form of `expression_list`, and the expressions in each `expression_list` must match in number and data type the expressions to the left of the operator. If you specify `subquery`, then the values returned by the subquery must match in number and data type the expressions to the left of the operator.