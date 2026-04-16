# Oracle 12c - conditions013
Source: https://docs.oracle.com/database/121/SQLRF/conditions013.htm

[Go to main content](#BEGIN)

70/555 

# EXISTS Condition

An `EXISTS` condition tests for existence of rows in a subquery.

[Table 6-11](#CJADBJFF) shows the `EXISTS` condition.

Table 6-11 EXISTS Condition

| Type of Condition | Operation | Example |
| --- | --- | --- |
| ``` EXISTS ``` | `TRUE` if a subquery returns at least one row. | ``` SELECT department_id   FROM departments d   WHERE EXISTS   (SELECT * FROM employees e     WHERE d.department_id      = e.department_id)    ORDER BY department_id; ``` |

Scripting on this page enhances content navigation, but does not change the content in any way.