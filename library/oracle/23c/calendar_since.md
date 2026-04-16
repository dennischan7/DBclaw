# Oracle 23c - calendar_since
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/calendar_since.html

Purpose

The `CALENDAR_SINCE` function determines the relative interval between the `dtexpr` and `SYSDATE`. It reports the interval in human-readable text using an interval of the appropriate scope using the following rules:

If < 2 minutes, then seconds.

If < 120 minutes, then minutes.

If < 2 days, then hours.

If < 14 days, then days.

If < 60 days, then weeks.

If < 365 days, then months.

Else years.

If the `dtexpr` < `SYSDATE` then the text is reported as `"X periods ago"` (e.g. 2 days ago, 4 months ago, etc.).

If the `dtexpr` > `SYSDATE` then the text is reported as `"In X periods"` (i.e. 3 days from now, 5 months from now, etc.)

If the `dtexpr` = `SYSDATE` then the returned text is `"Now"`. The text will be properly translated based on the `NLS_LANGUAGE`.

For all periods except for year, the reported intervals will be truncated to an integer (i.e. 2.8 weeks would be reported as 2 weeks). For years, it is truncated at the tenths place (i.e. 1.89 years would be reported as 1.8 years, with 1.0 years omitting the decimal).

The `fmt` parameter is a text value that must be either `LONG` or `SHORT` (case-insensitive) and represents the format of the output text. The format shown above is the `LONG` format and is the default. When `fmt` is `SHORT`, however, the short format is used. For example, "2 days ago" becomes "2d" and "3 days from now" becomes "in 3d". The following are the shorted period names in English.

Table 7-3 Shorted Period Names in English

| LONG | SHORT |
| --- | --- |
| `Now` | `Now` |
| `seconds` | `s` |
| `minutes` | `m` |
| `hours` | `h` |
| `days` | `d` |
| `weeks` | `w` |
| `months` | `mo` |
| `years` | `y` |