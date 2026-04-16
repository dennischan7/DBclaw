# Oracle 23c - ceil-interval
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ceil-interval.html

Purpose

`CEIL(interval)` returns the interval rounded up to the unit specified by the second argument `fmt`, the format model. If the first argument is truncated to the units of `fmt`, the output equals the input. For example, `CEIL(INTERVAL '+123-0' YEAR(3) TO MONTH)` returns 123 years and no months (+123-00).

The result of `CEIL(interval)` is never smaller than `interval`. The result precision for year and day is the input precision for year plus one and day plus one, since `CEIL(interval)` can have overflow. If an interval already has the maximum precision for year and day, the statement compiles but errors at runtime.

For `INTERVAL YEAR TO MONTH`, `fmt` can only be year. The default `fmt` is year.

For `INTERVAL DAY TO SECOND`, `fmt` can be day, hour, and minute. The default `fmt` is day. Note that `fmt` does not support second.

`CEIL(interval)` supports the format models of `ROUND` and `TRUNC`.

Examples

```
SELECT CEIL(INTERVAL '+123-5' YEAR(3) TO MONTH) AS year_ceil;

YEAR_CEIL
---------
+124-00
```

```
SELECT CEIL(INTERVAL '+99-11' YEAR(2) TO MONTH, 'YEAR');

YEAR_CEIL
---------
+100-00
```

```
SELECT CEIL(INTERVAL '+999999999-11' YEAR(9) TO MONTH, 'YEAR') AS year_ceil;

ORA-01873: the leading precision of the interval is too small
```

```
SELECT CEIL(INTERVAL '+4 12:42:10.222' DAY(2) TO SECOND(3), 'DD') AS day_ceil;

DAY_CEIL
-------------------
+05 00:00:00.000000
```