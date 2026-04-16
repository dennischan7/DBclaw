# Oracle 23c - floor-interval
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/floor-interval.html

Purpose

`FLOOR(interval)` returns the interval rounded down to the unit specified by the second argument `fmt`, the format model .

The result of `FLOOR(interval)` is never larger than `interval` . The result precision for year and day is the input precision for year plus one and day plus one, since `FLOOR(interval)` can have overflow . If an interval already has the maximum precision for year and day, the statement compiles but errors at runtime.

For `INTERVAL YEAR TO MONTH`, `fmt` can only be year. The default `fmt` is year.

For `INTERVAL DAY TO SECOND`, `fmt` can be day, hour and minute. The default `fmt` is day. Note that `fmt` does not support second.

`FLOOR(interval)` supports the format models of `ROUND` and `TRUNC`.

Examples

```
SELECT FLOOR(INTERVAL '+123-5' YEAR(3) TO MONTH) as year_floor;

YEAR_FLOOR
---------------------------------------------------------------------------
+000000123-00
```

```
SELECT FLOOR(INTERVAL '+99-11' YEAR(2) TO MONTH, 'YEAR') as year_floor;

YEAR_FLOOR
---------------------------------------------------------------------------
+000000099-00
```

```
SELECT FLOOR(INTERVAL '+4 12:42:10.222' DAY(2) TO SECOND(3), 'DD') as year_floor;

YEAR_FLOOR
---------------------------------------------------------------------------
+000000004 00:00:00.000000000
```