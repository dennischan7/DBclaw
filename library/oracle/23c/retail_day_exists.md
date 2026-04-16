# Oracle 23c - retail_day_exists
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/retail_day_exists.html

Purpose

The `RETAIL_DAY_EXISTS` function determines whether the `dtexpr` exists in the retail calendar, returning a boolean `TRUE` if it does exist and `FALSE` if it does not. When `is_restated` (which is mandatory for this function) is `RESTATED`, the function will return `FALSE` for any days that fall in the week removed from a restated retail year and `TRUE` for other days. When is\_restated is `NOT RESTATED`, the function will always return TRUE. This function is because all of the other functions will raise an error when `is_restated` is `RESTATED` and the input is one of the days not in the calendar. The `RETAIL_DAY_EXISTS` function allows a user to either filter out such rows in a `WHERE` clause, or to protect calls to the other functions with a `CASE` expression.

Example 1: Filter Invalid Rows Using WHERE Clause

In the following example, `RETAIL_DAY_EXISTS` allows the user to filter out invalid rows using the `WHERE` clause :

```
SELECT
RETAIL_MONTH(order_date, âDEFAULTâ, âRESTATEDâ) month,
SUM(sales) sales
FROM fact
WHERE RETAIL_DAY_EXISTS(order_date, âRESTATEDâ) = TRUE
GROUP BY ALL
ORDER BY 1;

MONTH SALES
---------- -----
FEB-RY2023 123
```

Example 2: Protect Calls Using CASE Expression

```
SELECT
CASE
WHEN RETAIL_DAY_EXISTS(order_date, âRESTATEDâ) = TRUE
THEN RETAIL_MONTH(order_date, âDEFAULTâ, âRESTATEDâ)
ELSE â#INVALID_DAY#â
END month,
SUM(sales) sales
FROM fact
GROUP BY ALL
ORDER BY 1;

MONTH SALES
------------- -----
FEB-RY2023 123
#INVALID_DAY# 456
```