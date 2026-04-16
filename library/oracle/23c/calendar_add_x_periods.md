# Oracle 23c - calendar_add_x_periods
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/calendar_add_x_periods.html

* `dtexpr` is a datetime expression with one of the following types (or any value that can be implicitly converted to `DATE`): `DATE`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP WITH LOCAL TIME ZONE` .
* The `num_periods` parameter is an integer that when positive will add periods and when negative will subtract periods.
* `nlsparam` is a text expression representing an NLS parameter setting. The only currently supported parameter is `NLS_DATE_LANGUAGE`, and is specified in the same manner as for `TO_CHAR` and `TO_DATE`.

The `CALENDAR_ADD_X_PERIODS`, `FISCAL_ADD_X_PERIODS`, and `RETAIL_ADD_X_PERIODS` functions take a `num_periods` parameter indicating how many periods (years, quarters, months, weeks, days) to add to the given `dtexpr`. The functions will return a `DATE` (with hour/minute/second components retained from the given `DATE`).

`CALENDAR_ADD_YEARS` adds or subtracts the given number of years, where a year is always defined as a period of 12 months.

`CALENDAR_ADD_QUARTERS` adds or subtracts the given number of quarters, where a quarter is always defined as a period of 3 months.

`CALENDAR_ADD_MONTHS` is identical to the existing `ADD_MONTHS` function. This will add or subtract to get a target month. If the given date is the last day of its month or if the resulting month has fewer days than the day component of the given date, the last day of the resulting month is used. Otherwise, the result has the same day component as the given date.

`CALENDAR_ADD_WEEKS` adds or subtracts the given number of weeks, where a week is always defined as a period of 7 days.

`CALENDAR_ADD_DAYS` simply adds or subtracts the given number of days.