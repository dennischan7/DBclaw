# Oracle 19c - Single-Row-Functions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Single-Row-Functions.html

Datetime functions operate on date (`DATE`), timestamp (`TIMESTAMP`, `TIMESTAMP` `WITH` `TIME` `ZONE`, and `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`), and interval (`INTERVAL` `DAY` `TO` `SECOND`, `INTERVAL` `YEAR` `TO` `MONTH`) values.

Some of the datetime functions were designed for the Oracle `DATE` data type (`ADD_MONTHS`, `CURRENT_DATE`, `LAST_DAY`, `NEW_TIME`, and `NEXT_DAY`). If you provide a timestamp value as their argument, then Oracle Database internally converts the input type to a `DATE` value and returns a `DATE` value. The exceptions are the `MONTHS_BETWEEN` function, which returns a number, and the `ROUND` and `TRUNC` functions, which do not accept timestamp or interval values at all.

The remaining datetime functions were designed to accept any of the three types of data (date, timestamp, and interval) and to return a value of one of these types.

All of the datetime functions that return current system datetime information, such as `SYSDATE`, `SYSTIMESTAMP`, `CURRENT_TIMESTAMP`, and so forth, are evaluated once for each SQL statement, regardless how many times they are referenced in that statement.

The datetime functions are: