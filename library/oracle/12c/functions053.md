# Oracle 12c - functions053
Source: https://docs.oracle.com/database/121/SQLRF/functions053.htm

# CV

Syntax

Purpose

The `CV` function can be used only in the `model_clause` of a `SELECT` statement and then only on the right-hand side of a model rule. It returns the current value of a dimension column or a partitioning column carried from the left-hand side to the right-hand side of a rule. This function is used in the `model_clause` to provide relative indexing with respect to the dimension column. The return type is that of the data type of the dimension column. If you omit the argument, then it defaults to the dimension column associated with the relative position of the function within the cell reference.

The `CV` function can be used outside a cell reference. In this case, `dimension_column` is required.

Examples

The following example assigns the sum of the sales of the product represented by the current value of the dimension column (Mouse Pad or Standard Mouse) for years 1999 and 2000 to the sales of that product for year 2001:

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
      s[FOR prod IN ('Mouse Pad', 'Standard Mouse'), 2001] =
        s[CV( ), 1999] + s[CV( ), 2000]
    )
  ORDER BY country, prod, year;

COUNTRY       PROD                                         YEAR           S
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000     3000.72
France        Mouse Pad                                    2001     6679.41
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000     1274.31
France        Standard Mouse                               2001     3554.76
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000     7375.46
Germany       Mouse Pad                                    2001     15721.9
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000     2637.31
Germany       Standard Mouse                               2001     8900.45
 
16 rows selected.
```

The preceding example requires the view `sales_view_ref`. Refer to ["The MODEL clause: Examples"](statements_10002.md#i2171160) to create this view.