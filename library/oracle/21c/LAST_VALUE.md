# Oracle 21c - LAST_VALUE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/LAST_VALUE.html

`LAST_VALUE` is an analytic function that is useful for data densification. It returns the last value in an ordered set of values.

Note:

The two forms of this syntax have the same behavior. The top branch is the ANSI format, which Oracle recommends for ANSI compatibility.

{`RESPECT` | `IGNORE`} `NULLS` determines whether null values of `expr` are included in or eliminated from the calculation. The default is `RESPECT` `NULLS`. If the last value in the set is null, then the function returns `NULL` unless you specify `IGNORE` `NULLS`. If you specify `IGNORE NULLS`, then `LAST_VALUE` returns the last non-null value in the set, or `NULL` if all values are null. Refer to "[Using Partitioned Outer Joins: Examples](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2177515)" for an example of data densification.

You cannot nest analytic functions by using `LAST_VALUE` or any other analytic function for `expr`. However, you can use other built-in function expressions for `expr`. Refer to "[About SQL Expressions](About-SQL-Expressions.md#GUID-68789A5C-B142-496F-ADEE-837F75F95B2B)" for information on valid forms of `expr`.

If you omit the `windowing_clause` of the `analytic_clause`, it defaults to `RANGE` `BETWEEN` `UNBOUNDED` `PRECEDING` `AND` `CURRENT` `ROW`. This default sometimes returns an unexpected value, because the last value in the window is at the bottom of the window, which is not fixed. It keeps changing as the current row changes. For expected results, specify the `windowing_clause` as `RANGE` `BETWEEN` `UNBOUNDED` `PRECEDING` `AND` `UNBOUNDED` `FOLLOWING`. Alternatively, you can specify the `windowing_clause` as `RANGE` `BETWEEN` `CURRENT` `ROW` `AND` `UNBOUNDED` `FOLLOWING`.

Examples

The following example returns, for each row, the hire date of the employee earning the lowest salary:

```
SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
               FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 13-JAN-01
        101 Kochhar                        17000 21-SEP-05 13-JAN-01
        102 De Haan                        17000 13-JAN-01 13-JAN-01
```

This example illustrates the nondeterministic nature of the `LAST_VALUE` function. Kochhar and De Haan have the same salary, so they are in adjacent rows. Kochhar appears first because the rows in the subquery are ordered by `hire_date`. However, if the rows are ordered by hire\_`date` in descending order, as in the next example, then the function returns a different value:

```
SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
               FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date DESC);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 21-SEP-05
        102 De Haan                        17000 13-JAN-01 21-SEP-05
        101 Kochhar                        17000 21-SEP-05 21-SEP-05
```

The following two examples show how to make the `LAST_VALUE` function deterministic by ordering on a unique key. By ordering within the function by both salary and the unique key `employee_id`, you can ensure the same result regardless of the ordering in the subquery.

```
SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC, employee_id ROWS BETWEEN UNBOUNDED PRECEDING
               AND UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 13-JAN-01
        101 Kochhar                        17000 21-SEP-05 13-JAN-01
        102 De Haan                        17000 13-JAN-01 13-JAN-01

SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC, employee_id ROWS BETWEEN UNBOUNDED PRECEDING
               AND UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date DESC);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 13-JAN-01
        101 Kochhar                        17000 21-SEP-05 13-JAN-01
        102 De Haan                        17000 13-JAN-01 13-JAN-01
```

The following two examples show that the `LAST_VALUE` function is deterministic when you use a logical offset (`RANGE` instead of `ROWS`). When duplicates are found for the `ORDER` `BY` expression, the `LAST_VALUE` is the highest value of `expr`:

```
SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC RANGE BETWEEN UNBOUNDED PRECEDING AND
               UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 21-SEP-05
        102 De Haan                        17000 13-JAN-01 21-SEP-05
        101 Kochhar                        17000 21-SEP-05 21-SEP-05

SELECT employee_id, last_name, salary, hire_date,
       LAST_VALUE(hire_date)
         OVER (ORDER BY salary DESC RANGE BETWEEN UNBOUNDED PRECEDING AND
               UNBOUNDED FOLLOWING) AS lv
  FROM (SELECT * FROM employees
          WHERE department_id = 90
          ORDER BY hire_date DESC);

EMPLOYEE_ID LAST_NAME                     SALARY HIRE_DATE LV
----------- ------------------------- ---------- --------- ---------
        100 King                           24000 17-JUN-03 21-SEP-05
        102 De Haan                        17000 13-JAN-01 21-SEP-05
        101 Kochhar                        17000 21-SEP-05 21-SEP-05
```