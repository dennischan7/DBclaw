# Oracle 23c - Aggregate-Functions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Aggregate-Functions.html

Aggregate functions return a single result row based on groups of rows, rather than on single rows. Aggregate functions can appear in select lists and in `ORDER` `BY` and `HAVING` clauses. They are commonly used with the `GROUP` `BY` clause in a `SELECT` statement, where the database divides the rows of a queried table or view into groups. In a query containing a `GROUP` `BY` clause, the elements of the select list can be aggregate functions, `GROUP` `BY` expressions, constants, or expressions involving one of these. Oracle applies the aggregate functions to each group of rows and returns a single result row for each group.

If you omit the `GROUP` `BY` clause, then Oracle applies aggregate functions in the select list to all the rows in the queried table or view. You use aggregate functions in the `HAVING` clause to eliminate groups from the output based on the results of the aggregate functions, rather than on the values of the individual rows of the queried table or view.

Many aggregate functions that take a single argument accept the following clauses:

* `DISTINCT` and `UNIQUE`, which are synonymous, cause an aggregate function to consider only distinct values of the argument expression. The syntax diagrams for aggregate functions in this chapter use the keyword `DISTINCT` for simplicity.
* `ALL` causes an aggregate function to consider all values, including all duplicates.

For example, the `DISTINCT` average of 1, 1, 1, and 3 is 2. The `ALL` average is 1.5. If you specify neither, then the default is `ALL`.

Some aggregate functions allow the `windowing_clause`, which is part of the syntax of analytic functions. Refer to [windowing\_clause](Analytic-Functions.md#GUID-527832F7-63C0-4445-8C16-307FA5084056__I97640) for information about this clause.

All aggregate functions except `COUNT`(\*), `GROUPING`, and `GROUPING_ID` ignore nulls. You can use the `NVL` function in the argument to an aggregate function to substitute a value for a null. `COUNT` and `REGR_COUNT` never return null, but return either a number or zero. For all the remaining aggregate functions, if the data set contains no rows, or contains only rows with nulls as arguments to the aggregate function, then the function returns null.

The aggregate functions `MIN`, `MAX`, `SUM`, `AVG`, `COUNT`, `VARIANCE`, and `STDDEV`, when followed by the `KEEP` keyword, can be used in conjunction with the `FIRST` or `LAST` function to operate on a set of values from a set of rows that rank as the `FIRST` or `LAST` with respect to a given sorting specification. Refer to [FIRST](FIRST.md#GUID-85AB9246-0E0A-44A1-A7E6-4E57502E9238) for more information.

You can nest aggregate functions. For example, the following example calculates the average of the maximum salaries of all the departments in the sample schema `hr`:

```
SELECT AVG(MAX(salary))
  FROM employees
  GROUP BY department_id;

AVG(MAX(SALARY))
----------------
      10926.3333
```

This calculation evaluates the inner aggregate (`MAX`(`salary`)) for each group defined by the `GROUP` `BY` clause (`department_id`), and aggregates the results again.

FILTER Clause Syntax

```
aggregate_function ( aggregate_function_arguments ) [ FILTER ( WHERE condition )]
```

FILTER Clause Semantics

Specify the `FILTER WHERE` `condition` clause optionally at the end of an aggregate function to filter the rows of data that are fed into the aggregate function. The `FILTER WHERE` clause works in the same way that a `WHERE` clause filters rows, but it is localized to the specific aggregate function.

Rules

You can use `FILTER WHERE` before the `OVER` clause when the aggregate function is used as a window function.

You cannot use `FILTER WHERE` after a non-aggregate function.

condition

`condition` can be any conditions that are currently supported in the `WHERE` clause, except for subqueries, window functions, and outer references. It can refer to any columns in the underlying tables that the aggregation function aggregates for. The condition is applied to the rows filtered by the `WHERE` clause, after which the specific aggregation is performed on the filtered rows by the `FILTER` clause.