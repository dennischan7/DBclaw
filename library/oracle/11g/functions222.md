# Oracle 11g - functions222
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions222.htm

[Go to main content](#BEGIN)

262/522 

# TZ\_OFFSET

Syntax

Purpose

`TZ_OFFSET` returns the time zone offset corresponding to the argument based on the date the statement is executed. You can enter a valid time zone region name, a time zone offset from UTC (which simply returns itself), or the keyword `SESSIONTIMEZONE` or `DBTIMEZONE`. For a listing of valid values for `time_zone_name`, query the `TZNAME` column of the `V$TIMEZONE_NAMES` dynamic performance view.

Note:

Time zone region names are needed by the daylight saving feature. These names are stored in two types of time zone files: one large and one small. One of these files is the default file, depending on your environment and the release of Oracle Database you are using. For more information regarding time zone files and names, see

[Oracle Database Globalization Support Guide](../../server.112/e10729/applocaledata.md#NLSPG014)

.

Examples

The following example returns the time zone offset of the US/Eastern time zone from UTC:

```
SELECT TZ_OFFSET('US/Eastern') FROM DUAL;

TZ_OFFS
-------
-04:00
```

Scripting on this page enhances content navigation, but does not change the content in any way.