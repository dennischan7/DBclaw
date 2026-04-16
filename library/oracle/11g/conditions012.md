# Oracle 11g - conditions012
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/conditions012.htm

[Go to main content](#BEGIN)

325/522 

# EXISTS Condition

An `EXISTS` condition tests for existence of rows in a subquery.

[Table 7-11](#CJADBJFF) shows the `EXISTS` condition.

Table 7-11 EXISTS Condition

| Type of Condition | Operation | Example |
| --- | --- | --- |
| ``` EXISTS ``` | `TRUE` if a subquery returns at least one row. | ``` SELECT department_id   FROM departments d   WHERE EXISTS   (SELECT * FROM employees e     WHERE d.department_id      = e.department_id)    ORDER BY department_id; ``` |

Scripting on this page enhances content navigation, but does not change the content in any way.