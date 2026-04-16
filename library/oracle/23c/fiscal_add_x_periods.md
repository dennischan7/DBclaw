# Oracle 23c - fiscal_add_x_periods
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/fiscal_add_x_periods.html

Purpose

The fiscal variants of this class of functions is equivalent to the definitions above for calendar. The difference has to do with what constitutes a month. If the fiscal year start is on the 1st of a month, these functions will return exactly the same value as their calendar counterparts. If the fiscal year start is not on the 1st, however, then they will diverge.

`FISCAL_ADD_YEARS` adds or subtracts the given number of years, where a year is always defined as a period of 12 months. See below for how months are handled.

`FISCAL_ADD_QUARTERS` adds or subtracts the given number of quarters, where a quarter is always defined as a period of 3 months. See below for how months are handled.

`FISCAL_ADD_MONTHS` This is handled the same as `CALENDAR_ADD_MONTHS`. When the fiscal year start is not on the first of the month, the positional day within the given month is mapped to the corresponding positional day within the target month. The same rules apply when the starting positional day is the last day of the starting fiscal month, or when the starting positional day is greater than the number of days in the target fiscal month.

`FISCAL_ADD_WEEKS` adds or subtracts the given number of weeks, where a week is always defined as a period of 7 days.

`FISCAL_ADD_DAYS` simply adds or subtracts the given number of days.