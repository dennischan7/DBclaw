# Oracle 12c - functions013
Source: https://docs.oracle.com/database/121/SQLRF/functions013.htm

# APPROX\_COUNT\_DISTINCT

Note:

The

`APPROX_COUNT_DISTINCT`

function is available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

Syntax

Purpose

`APPROX_COUNT_DISTINCT` returns the approximate number of rows that contain distinct values of `expr`.

This function provides an alternative to the `COUNT` `(DISTINCT` `expr``)` function, which returns the exact number of rows that contain distinct values of `expr`. `APPROX_COUNT_DISTINCT` processes large amounts of data significantly faster than `COUNT`, with negligible deviation from the exact result.

For `expr`, you can specify a column of any scalar data type other than `BFILE`, `BLOB`, `CLOB`, `LONG`, `LONG` `RAW`, or `NCLOB`.

`APPROX_COUNT_DISTINCT` ignores rows that contain a null value for `expr`. This function returns a `NUMBER`.

Examples

The following statement returns the approximate number of rows with distinct values for `manager_id`:

```
SELECT APPROX_COUNT_DISTINCT(manager_id) AS "Active Managers"
  FROM employees;

Active Managers
---------------
             18
```

The following statement returns the approximate number of distinct customers for each product:

```
SELECT prod_id, APPROX_COUNT_DISTINCT(cust_id) AS "Number of Customers"
  FROM sales
  GROUP BY prod_id
  ORDER BY prod_id;

   PROD_ID Number of Customers
---------- -------------------
        13                2516
        14                2030
        15                2105
        16                2367
        17                2093
        18                2975
        19                2630
        20                3791
. . .
```