# Oracle 12c - conditions005
Source: https://docs.oracle.com/database/121/SQLRF/conditions005.htm

## IS ANY Condition

The `IS` `ANY` condition can be used only in the `model_clause` of a `SELECT` statement. Use this condition to qualify all values of a dimension column, including `NULL`.

is\_any\_condition::=

The condition always returns a Boolean value of `TRUE` in order to qualify all values of the column.

Example

The following example sets sales for each product for year 2000 to 0:

```
SELECT country, prod, year, s
  FROM sales_view_ref
  MODEL
    PARTITION BY (country)
    DIMENSION BY (prod, year)
    MEASURES (sale s)
    IGNORE NAV
    UNIQUE DIMENSION
    RULES UPSERT SEQUENTIAL ORDER
    (
      s[ANY, 2000] = 0
    )
  ORDER BY country, prod, year;

COUNTRY       PROD                                         YEAR           S
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000           0
France        Mouse Pad                                    2001     3269.09
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000           0
France        Standard Mouse                               2001     2164.54
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000           0
Germany       Mouse Pad                                    2001     9535.08
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000           0
Germany       Standard Mouse                               2001     6456.13
 
16 rows selected.
```

The preceding example requires the view `sales_view_ref`. Refer to ["The MODEL clause: Examples"](statements_10002.md#i2171160) to create this view.

## IS PRESENT Condition

is\_present\_condition::=

The `IS` `PRESENT` condition can be used only in the `model_clause` of a `SELECT` statement. Use this condition to test whether the cell referenced is present prior to the execution of the `model_clause`.

The condition returns `TRUE` if the cell exists prior to the execution of the `model_clause` and `FALSE` if it does not.

Example

In the following example, if sales of the Mouse Pad for year 1999 exist, then sales of the Mouse Pad for year 2000 is set to sales of the Mouse Pad for year 1999. Otherwise, sales of the Mouse Pad for year 2000 is set to 0.

```
SELECT country, prod, year, s
  FROM sales_view_ref
  MODEL
    PARTITION BY (country)
    DIMENSION BY (prod, year)
    MEASURES (sale s)
    IGNORE NAV
    UNIQUE DIMENSION
    RULES UPSERT SEQUENTIAL ORDER
    (
      s['Mouse Pad', 2000] =
        CASE WHEN s['Mouse Pad', 1999] IS PRESENT
             THEN s['Mouse Pad', 1999]
             ELSE 0
        END
    )
  ORDER BY country, prod, year;

COUNTRY       PROD                                         YEAR           S
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000     3678.69
France        Mouse Pad                                    2001     3269.09
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000     1274.31
France        Standard Mouse                               2001     2164.54
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000     8346.44
Germany       Mouse Pad                                    2001     9535.08
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000     2637.31
Germany       Standard Mouse                               2001     6456.13
16 rows selected.
```

The preceding example requires the view `sales_view_ref`. Refer to ["The MODEL clause: Examples"](statements_10002.md#i2171160) to create this view.