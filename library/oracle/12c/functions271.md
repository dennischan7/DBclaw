# Oracle 12c - functions271
Source: https://docs.oracle.com/database/121/SQLRF/functions271.htm

[Go to main content](#BEGIN)

344/555 

# ROUND and TRUNC Date Functions

[Table 7-13](#CJAEFAIA) lists the format models you can use with the `ROUND` and `TRUNC` date functions and the units to which they round and truncate dates. The default model, 'DD', returns the date rounded or truncated to the day with a time of midnight.

Table 7-13 Date Format Models for the ROUND and TRUNC Date Functions

| Format Model | Rounding or Truncating Unit |
| --- | --- |
| ``` CC SCC ``` | One greater than the first two digits of a four-digit year |
| ``` SYYYY YYYY YEAR SYEAR YYY YY Y ``` | Year (rounds up on July 1) |
| ``` IYYY IYY IY I ``` | Year containing the calendar week, as defined by the ISO 8601 standard |
| ``` Q ``` | Quarter (rounds up on the sixteenth day of the second month of the quarter) |
| ``` MONTH MON MM RM ``` | Month (rounds up on the sixteenth day) |
| ``` WW ``` | Same day of the week as the first day of the year |
| ``` IW ``` | Same day of the week as the first day of the calendar week as defined by the ISO 8601 standard, which is Monday |
| ``` W ``` | Same day of the week as the first day of the month |
| ``` DDD DD J ``` | Day |
| ``` DAY DY D ``` | Starting day of the week |
| ``` HH HH12 HH24 ``` | Hour |
| ``` MI ``` | Minute |

The starting day of the week used by the format models DAY, DY, and D is specified implicitly by the initialization parameter `NLS_TERRITORY`.

Scripting on this page enhances content navigation, but does not change the content in any way.