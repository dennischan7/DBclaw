# Oracle 23c - time_bucket-datetime
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/time_bucket-datetime.html

Examples

The following examples use the `NLS_DATE_FORMAT` `YYYY-MM-DD`. Set the date format with `ALTER SESSION`:

```
ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD';
```

Example 1

```
SELECT TIME_BUCKET (DATE â2022-06-29â, INTERVAL â5â YEAR, DATE â2000-01-01â, START);
```

The result is:

```
2020-01-01
```

The 5-year time bucket that contains `2022-06-29` is from `2020-01-01`(start) to `2025- 01-01`(end). The fourth argument `START` is used, so the start of the time bucket `2020-01-01` is returned.

Example 2

The following two queries are equivalent:

```
SELECT TIME_BUCKET ( DATE â-2022-06-29â, âP5Mâ, DATE â-2022-01-01â, END );
```

Or:

```
SELECT TIME_BUCKET ( DATE â-2022-06-29â, INTERVAL â5â MONTH, DATE â-2022-01-01â, END);
```

The result is:

```
-2022-11-01
```

The 5-month time bucket that contains `-2022-06-29` is from `2022-06-01`(start) to `-2022- 11-01`(end). The fourth argument `END` is used, so the end of the time bucket `2022-11-01` is returned.

Example 3

```
SELECT TIME_BUCKET ( DATE â2005-03-10â, 'P1Y', DATE â2004-02-29â ON OVERFLOW ERROR );
```

The result is:

```
 ORA-01839: date not valid for month specified
```

The one-year time bucket that contains `â2005-03-10â` is from error (or `â2005-02-29â`) (start) to error (or `â2006-02-29â`) (end). Default fourth argument `START` is used, so the start of the time bucket should be returned which is an error.

Example 4

```
SELECT TIME_BUCKET ( DATE â2005-03-10â, 'P1Y', DATE â2004-02-29â ON OVERFLOW ROUND );
```

The result is:

```
2005-02-28
```

The one-year time bucket that contains `â2005-03-10â` is from `â2005-02-28â`(start) to `â2006- 02-28â`(end) since February 29 is rounded to February 28. Default fourth argument `START` is used, so the start of the time bucket is returned: `â2005-02-28â`.

Example 5

```
SELECT TIME_BUCKET ( DATE â2004-04-02â, âP1Yâ, DATE â2003-02-28â LAST DAY OF MONTH );
```

The result is:

```
2004-02-29
```

The one-year time bucket that contains `â2003-02-28â` is from `â2004-02-29â`(start) to `â2005- 02-28â`(end) since `â2004-02-28â` is rounded to the last day of that month which is `â2004-02-29â`. Default fourth argument `START` is used, so the start of the time bucket is returned: `â2004-02- 29â`.