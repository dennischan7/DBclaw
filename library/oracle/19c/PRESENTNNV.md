# Oracle 19c - PRESENTNNV
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/PRESENTNNV.html

In the following example, if a row containing sales for the Mouse Pad for the year 2002 exists, and the sales value is not null, then the sales value remains unchanged. If the row exists and the sales value is null, then the sales value is set to 10. If the row does not exist, then the row is created with the sales value set to 10.

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
    ( s['Mouse Pad', 2002] = 
        PRESENTNNV(s['Mouse Pad', 2002], s['Mouse Pad', 2002], 10)
    )
  ORDER BY country, prod, year;

COUNTRY       PROD                                         YEAR           S
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000     3000.72
France        Mouse Pad                                    2001     3269.09
France        Mouse Pad                                    2002          10
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000     1274.31
France        Standard Mouse                               2001     2164.54
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000     7375.46
Germany       Mouse Pad                                    2001     9535.08
Germany       Mouse Pad                                    2002          10
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000     2637.31
Germany       Standard Mouse                               2001     6456.13

18 rows selected.
```

The preceding example requires the view `sales_view_ref`. Refer to "[Examples](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2066378)" to create this view.