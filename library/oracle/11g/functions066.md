# Oracle 11g - functions066
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions066.htm

# FIRST\_VALUE

Syntax

See Also:

["Analytic Functions"](functions004.md#i81407)

for information on syntax, semantics, and restrictions, including valid forms of

`expr`

Purpose

`FIRST_VALUE` is an analytic function. It returns the first value in an ordered set of values. If the first value in the set is null, then the function returns `NULL` unless you specify `IGNORE NULLS`. This setting is useful for data densification.

Note:

The two forms of this syntax have the same behavior. The top branch is the ANSI format, which Oracle recommends. The bottom branch is deprecated but is supported for backward compatibility.

{`RESPECT` | `IGNORE`} `NULLS` determines whether null values of `expr` are included in or eliminated from the calculation. The default is `RESPECT` `NULLS`. If you specify `IGNORE NULLS`, then `FIRST_VALUE` returns the first non-null value in the set, or `NULL` if all values are null. Refer to ["Using Partitioned Outer Joins: Examples"](statements_10002.md#i2177515) for an example of data densification.

You cannot nest analytic functions by using `FIRST_VALUE` or any other analytic function for `expr`. However, you can use other built-in function expressions for `expr`. Refer to ["About SQL Expressions"](expressions001.md#i1002626) for information on valid forms of `expr`.

Examples

The following example selects, for each employee in Department 90, the name of the employee with the lowest salary.

```
SELECT department_id, last_name, salary,
       FIRST_VALUE(last_name)
         OVER (ORDER BY salary ASC ROWS UNBOUNDED PRECEDING) AS lowest_sal
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY employee_id)
  ORDER BY last_name;

DEPARTMENT_ID LAST_NAME                     SALARY LOWEST_SAL
------------- ------------------------- ---------- -------------------------
           90 De Haan                        17000 Kochhar
           90 King                           24000 Kochhar
           90 Kochhar                        17000 Kochhar
```

The example illustrates the nondeterministic nature of the `FIRST_VALUE` function. Kochhar and DeHaan have the same salary, so are in adjacent rows. Kochhar appears first because the rows returned by the subquery are ordered by `employee_id`. However, if the rows returned by the subquery are ordered by `employee_id` in descending order, as in the next example, then the function returns a different value:

```
SELECT department_id, last_name, salary,
       FIRST_VALUE(last_name)
         OVER (ORDER BY salary ASC ROWS UNBOUNDED PRECEDING) AS fv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER by employee_id DESC)
  ORDER BY last_name;

DEPARTMENT_ID LAST_NAME                     SALARY FV
------------- ------------------------- ---------- -------------------------
           90 De Haan                        17000 De Haan
           90 King                           24000 De Haan
           90 Kochhar                        17000 De Haan
```

The following example shows how to make the `FIRST_VALUE` function deterministic by ordering on a unique key.

```
SELECT department_id, last_name, salary, hire_date,
       FIRST_VALUE(last_name)
         OVER (ORDER BY salary ASC, hire_date ROWS UNBOUNDED PRECEDING) AS fv
  FROM (SELECT * FROM employees 
          WHERE department_id = 90
          ORDER BY employee_id DESC)
  ORDER BY last_name;

DEPARTMENT_ID LAST_NAME           SALARY HIRE_DATE FV
------------- --------------- ---------- --------- -------------------------
           90 De Haan              17000 13-JAN-01 De Haan
           90 King                 24000 17-JUN-03 De Haan
           90 Kochhar              17000 21-SEP-05 De Haan
```

When you use a logical offset (`RANGE` instead of `ROWS`), the function is deterministic. When duplicates are found for the `ORDER` `BY` expression, the `FIRST_VALUE` is the lowest value of `expr`:

```
SELECT department_id, last_name, salary,
       FIRST_VALUE(last_name)
         OVER (ORDER BY salary ASC RANGE UNBOUNDED PRECEDING) AS lowest_sal
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY employee_id);
 
DEPARTMENT_ID LAST_NAME                     SALARY LOWEST_SAL
------------- ------------------------- ---------- -------------------------
           90 De Haan                        17000 De Haan
           90 Kochhar                        17000 De Haan
           90 King                           24000 De Haan
```