# Oracle 11g - functions085
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions085.htm

# LAST\_VALUE

Syntax

See Also:

["Analytic Functions"](functions004.md#i81407)

for information on syntax, semantics, and restrictions, including valid forms of

`expr`

Purpose

`LAST_VALUE` is an analytic function that is useful for data densification. It returns the last value in an ordered set of values.

Note:

The two forms of this syntax have the same behavior. The top branch is the ANSI format, which Oracle recommends. The bottom branch is deprecated but is supported for backward compatibility.

{`RESPECT` | `IGNORE`} `NULLS` determines whether null values of `expr` are included in or eliminated from the calculation. The default is `RESPECT` `NULLS`. If the last value in the set is null, then the function returns `NULL` unless you specify `IGNORE` `NULLS`. If you specify `IGNORE NULLS`, then `LAST_VALUE` returns the last non-null value in the set, or `NULL` if all values are null. Refer to ["Using Partitioned Outer Joins: Examples"](statements_10002.md#i2177515) for an example of data densification.

You cannot nest analytic functions by using `LAST_VALUE` or any other analytic function for `expr`. However, you can use other built-in function expressions for `expr`. Refer to ["About SQL Expressions"](expressions001.md#i1002626) for information on valid forms of `expr`.

If you omit the `windowing_clause` of the `analytic_clause`, it defaults to `RANGE` `BETWEEN` `UNBOUNDED` `PRECEDING` `AND` `CURRENT` `ROW`. This default sometimes returns an unexpected value, because the last value in the window is at the bottom of the window, which is not fixed. It keeps changing as the current row changes. For expected results, specify the `windowing_clause` as `RANGE` `BETWEEN` `UNBOUNDED` `PRECEDING` `AND` `UNBOUNDED` `FOLLOWING`. Alternatively, you can specify the `windowing_clause` as `RANGE` `BETWEEN` `CURRENT` `ROW` `AND` `UNBOUNDED` `FOLLOWING`.

Examples

The following example returns, for each row, the hire date of the employee earning the highest salary:

```
SELECT last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
               FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date);

LAST_NAME           SALARY HIRE_DATE LV
--------------- ---------- --------- ---------
De Haan              17000 13-JAN-01 17-JUN-03
Kochhar              17000 21-SEP-05 17-JUN-03
King                 24000 17-JUN-03 17-JUN-03
```

This example illustrates the nondeterministic nature of the `LAST_VALUE` function. Kochhar and De Haan have the same salary, so they are in adjacent rows. Kochhar appears first because the rows in the subquery are ordered by `hire_date`. However, if the rows are ordered by `hire_date` in descending order, as in the next example, then the function returns a different value:

```
SELECT last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
               FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90 
          ORDER BY hire_date DESC);

LAST_NAME           SALARY HIRE_DATE LV
--------------- ---------- --------- ---------
Kochhar              17000 21-SEP-05 17-JUN-03
De Haan              17000 13-JAN-01 17-JUN-03
King                 24000 17-JUN-03 17-JUN-03
```

The following two examples show how to make the `LAST_VALUE` function deterministic by ordering on a unique key. By ordering within the function by both `salary` and `hire_date`, you can ensure the same result regardless of the ordering in the subquery.

```
SELECT last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary, hire_date ROWS BETWEEN UNBOUNDED PRECEDING AND
               UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90 
          ORDER BY hire_date)
  ORDER BY last_name, salary, hire_date;

LAST_NAME           SALARY HIRE_DATE LV
--------------- ---------- --------- ---------
De Haan              17000 13-JAN-01 17-JUN-03
King                 24000 17-JUN-03 17-JUN-03
Kochhar              17000 21-SEP-05 17-JUN-03

SELECT last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary, hire_date ROWS BETWEEN UNBOUNDED PRECEDING AND
               UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90 
          ORDER BY hire_date DESC)
  ORDER BY last_name, salary, hire_date;

LAST_NAME           SALARY HIRE_DATE LV
--------------- ---------- --------- ---------
De Haan              17000 13-JAN-01 17-JUN-03
King                 24000 17-JUN-03 17-JUN-03
Kochhar              17000 21-SEP-05 17-JUN-03
```

When you use a logical offset (`RANGE` instead of `ROWS`), the function is deterministic. When duplicates are found for the `ORDER` `BY` expression, the `LAST_VALUE` is the highest value of `expr`:

```
SELECT last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
               FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date DESC);
 
LAST_NAME                     SALARY HIRE_DATE LV
------------------------- ---------- --------- ---------
De Haan                        17000 13-JAN-01 17-JUN-03
Kochhar                        17000 21-SEP-05 17-JUN-03
King                           24000 17-JUN-03 17-JUN-03
```