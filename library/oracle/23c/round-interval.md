# Oracle 23c - round-interval
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/round-interval.html

Purpose

`ROUND(interval)` returns the interval rounded up to the unit specified by the second argument `fmt`, the format model .

For `INTERVAL YEAR TO MONTH`, `fmt` can only be year. The default `fmt` is year.

For  `INTERVAL DAY TO SECOND`, `fmt` can be day, hour and minute. The default `fmt` is day. Note that `fmt` does not support second.

`ROUND(interval)` rounds up on the mid value of next part of `fmt` as follows:

* If `fmt` is year, `ROUND(interval)` rounds up on the mid value of month which is 6.
* If `fmt` is day, `ROUND(interval)` rounds up on the mid value of hour which is 12.
* If `fmt` is hour, `ROUND(interval)` rounds up on the mid value of minute which is 30.
* If `fmt` is minute, `ROUND(interval)` rounds up on the mid value of second which is 30.

The result precision for year and day is the input precision for year plus one and day plus one respectively, since `ROUND(interval)` can have overflow. If an interval already has the maximum precision for year and day, the statement compiles but errors at runtime.

Examples

```
SELECT ROUND(INTERVAL '+123-06' YEAR(3) TO MONTH) AS year_round;

YEAR_ROUND
----------
+124-00
```

```
SELECT ROUND(INTERVAL '+99-11' YEAR(2) TO MONTH, 'YEAR') AS year_round;

YEAR_ROUND
----------
+100-00
```

```
SELECT ROUND(INTERVAL '-999999999-11' YEAR(9) TO MONTH, 'YEAR')AS year_round;

ORA-01873: the leading precision of the interval is too small
```

```
SELECT ROUND(INTERVAL '+4 12:42:10.222' DAY(2) TO SECOND(3), 'DD') AS day_round;

DAY_ROUND
-------------------
+05 00:00:00.000000
```