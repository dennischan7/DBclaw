# Oracle 23c - fiscal
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/fiscal.html

|  |  |
| --- | --- |
| `YYYY` | 4-digit calendar year of the last day in the fiscal year (only positive years supported). For example, if the fiscal year starts on June 1, then June 1, 2024 would be in year 2025. |
| `SYYYY` | 4-digit calendar year of the last day in the fiscal year, with BC years as negative. |
| `Q` | Quarter of fiscal year (1-4), with quarter 1 representing the start of the fiscal year. For example, if the fiscal year starts on June 1, then June 1 would be in quarter 1. |
| `MM` | Month of year (1-12), 2-digit, representing the associated calendar month of the last day in the fiscal month. For example, if the fiscal year starts on June 15, then June 20 would be in month 07. |
| `MON` | Abbreviated name of month, where the month name is determined by the calendar month of the last day in the fiscal month. For example, if the fiscal year starts on June 15, then June 20 would be in month `JUL`. |
| `MONTH` | Name of month, where the month name is determined by the calendar month of the last day in the fiscal month. For example, if the fiscal year starts on June 15, then June 20 would be in month `JULY`. |
| `WW` | Week number (1-53), 2-digits with week 1 representing the start of the fiscal year. For example, if the fiscal year starts on June 1, then June 1 would be in week 1. |
| `DY` | Abbreviated name of day |
| `DAY` | Name of day |
| `D` | Day of week (1-7). Depends on the `NLS_TERRITORY` |
| `DD` | Day of month (1-31), 2-digits, with day 1 representing the first day of the fiscal month. For example, if the fiscal year starts on June 15, then June 20 would be day 6 (in the month of July). |
| `DDD` | Day of year (1-366), 3-digits, with day 1 representing the first day in the fiscal year. |