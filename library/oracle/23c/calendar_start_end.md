# Oracle 23c - calendar_start_end
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/calendar_start_end.html

* `dtexpr` is a datetime expression with one of the following types (or any value that can be implicitly converted to `DATE`): `DATE`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP WITH LOCAL TIME ZONE` .
* `nlsparam` is a text expression representing an NLS parameter setting. The only currently supported parameter is `NLS_DATE_LANGUAGE`, and is specified in the same manner as for `TO_CHAR` and `TO_DATE`.

`CALENDAR_START_END`, `FISCAL_START_END`, `CALENDAR_X_OF_Y`, `FISCAL_X_OF_Y`, `CALENDAR_ADD_X_PERIODS`, and `FISCAL_ADD_PERIODS` functions accept a `nlsparam`.

All functions that take an `nlsparam` allow the specification of `NLS_CALENDAR`, with the exception of the retail functions.

The `NLS_CALENDAR`, either inherited from the session or explicitly specified in the `nlsparam`, indicates which calendar is used for navigation and output. Only the `GREGORIAN` calendar is supported.

The `CALENDAR_START_END`, `FISCAL_START_END`, and `RETAIL_START_END` functions return a `DATE` (with hour/minute/second components set to midnight) representing the Gregorian date of the start or end of the associated period (year, quarter, month, week) in the associated calendar (calendar, fiscal, retail). Note that there are no functions for `DAY` because they would all just return the given date for both start and end.