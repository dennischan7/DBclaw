# Oracle 19c - Format-Models
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Format-Models.html

|  |  |  |
| --- | --- | --- |
| ``` - / , . ; : "text" ``` | Yes | Punctuation and quoted text is reproduced in the result. |
| ``` AD A.D. ``` | Yes | AD indicator with or without periods. |
| ``` AM A.M. ``` | Yes | Meridian indicator with or without periods. |
| ``` BC B.C. ``` | Yes | BC indicator with or without periods. |
| ``` CC SCC ``` |  | Century.   * If the last 2 digits of a 4-digit year are between 01 and 99 (inclusive), then the century is one greater than the first 2 digits of that year. * If the last 2 digits of a 4-digit year are 00, then the century is the same as the first 2 digits of that year.   For example, 2002 returns 21; 2000 returns 20. |
| ``` D ``` | Yes | Day of week (1-7). This element depends on the NLS territory of the session. |
| `DAY` | Yes | Name of day. |
| ``` DD ``` | Yes | Day of month (1-31). |
| ``` DDD ``` | Yes | Day of year (1-366). |
| ``` DL ``` | Yes | Returns a value in the long date format, which is an extension of the Oracle Database `DATE` format, determined by the current value of the `NLS_DATE_FORMAT` parameter. Makes the appearance of the date components (day name, month number, and so forth) depend on the `NLS_TERRITORY` and `NLS_LANGUAGE` parameters. For example, in the `AMERICAN_AMERICA` locale, this is equivalent to specifying the format `'fmDay,` `Month` `dd,` `yyyy'`. In the `GERMAN_GERMANY` locale, it is equivalent to specifying the format '`fmDay, dd.` `Month yyyy`'.  Restriction: You can specify this format only with the `TS` element, separated by white space. |
| ``` DS ``` | Yes | Returns a value in the short date format. Makes the appearance of the date components (day name, month number, and so forth) depend on the `NLS_TERRITORY` and `NLS_LANGUAGE` parameters. For example, in the `AMERICAN_AMERICA` locale, this is equivalent to specifying the format '`MM/DD/RRRR`'. In the `ENGLISH_UNITED_KINGDOM` locale, it is equivalent to specifying the format '`DD/MM/RRRR`'.  Restriction: You can specify this format only with the `TS` element, separated by white space. |
| ``` DY ``` | Yes | Abbreviated name of day. |
| ``` E ``` | Yes | Abbreviated era name (Japanese Imperial, ROC Official, and Thai Buddha calendars). |
| ``` EE ``` | Yes | Full era name (Japanese Imperial, ROC Official, and Thai Buddha calendars). |
| ``` FF [1..9] ``` | Yes | Fractional seconds; no radix character is printed. Use the X format element to add the radix character. Use the numbers 1 to 9 after FF to specify the number of digits in the fractional second portion of the datetime value returned. If you do not specify a digit, then Oracle Database uses the precision specified for the datetime data type or the data type's default precision. Valid in timestamp and interval formats, but not in `DATE` formats.  Examples: `'HH:MI:SS.FF'`  `SELECT TO_CHAR(SYSTIMESTAMP, 'SS.FF3') from DUAL;` |
| ``` FM ``` | Yes | Returns a value with no leading or trailing blanks.  See Also: [FM](Format-Models.md#GUID-7FF68D9E-C7E2-4CA1-9DDB-5CC7169EEEEA__BABDAEDF) |
| ``` FX ``` | Yes | Requires exact matching between the character data and the format model.  See Also: [FX](Format-Models.md#GUID-7FF68D9E-C7E2-4CA1-9DDB-5CC7169EEEEA__CHDHIHEH) |
| ``` HH HH12 ``` | Yes | Hour of day (1-12). |
| ``` HH24 ``` | Yes | Hour of day (0-23). |
| ``` IW ``` |  | Calendar week of year (1-52 or 1-53), as defined by the ISO 8601 standard.   * A calendar week starts on Monday. * The first calendar week of the year includes January 4. * The first calendar week of the year may include December 29, 30 and 31. * The last calendar week of the year may include January 1, 2, and 3. |
| ``` IYYY ``` |  | 4-digit year of the year containing the calendar week, as defined by the ISO 8601 standard. |
| ``` IYY IY I ``` |  | Last 3, 2, or 1 digit(s) of the year containing the calendar week, as defined by the ISO 8601 standard. |
| ``` J ``` | Yes | Julian day; the number of days since January 1, 4712 BC. Number specified with J must be integers. |
| ``` MI ``` | Yes | Minute (0-59). |
| ``` MM ``` | Yes | Month (01-12; January = 01). |
| ``` MON ``` | Yes | Abbreviated name of month. |
| ``` MONTH ``` | Yes | Name of month. |
| ``` PM P.M. ``` | Yes | Meridian indicator with or without periods. |
| ``` Q ``` |  | Quarter of year (1, 2, 3, 4; January - March = 1). |
| ``` RM ``` | Yes | Roman numeral month (I-XII; January = I). |
| ``` RR ``` | Yes | Lets you store 20th century dates in the 21st century using only two digits.  See Also: [The RR Datetime Format Element](Format-Models.md#GUID-6C75461E-2E18-4C35-9EB4-038A7E1C9C1F) |
| ``` RRRR ``` | Yes | Round year. Accepts either 4-digit or 2-digit input. If 2-digit, provides the same return as RR. If you do not want this functionality, then enter the 4-digit year. |
| ``` SS ``` | Yes | Second (0-59). |
| ``` SSSSS ``` | Yes | Seconds past midnight (0-86399). |
| ``` TS ``` | Yes | Returns a value in the short time format. Makes the appearance of the time components (hour, minutes, and so forth) depend on the `NLS_TERRITORY` and `NLS_LANGUAGE` initialization parameters.  Restriction: You can specify this format only with the `DL` or `DS` element, separated by white space. |
| ``` TZD ``` | Yes | Daylight saving information. The TZD value is an abbreviated time zone string with daylight saving information. It must correspond with the region specified in TZR. Valid in timestamp and interval formats, but not in `DATE` formats.  Example: `PST` (for US/Pacific standard time); `PDT` (for US/Pacific daylight time). |
| ``` TZH ``` | Yes | Time zone hour. (See `TZM` format element.) Valid in timestamp and interval formats, but not in `DATE` formats.  Example: `'HH:MI:SS.FFTZH:TZM'`. |
| ``` TZM ``` | Yes | Time zone minute. (See `TZH` format element.) Valid in timestamp and interval formats, but not in `DATE` formats.  Example: `'HH:MI:SS.FFTZH:TZM'`. |
| ``` TZR ``` | Yes | Time zone region information. The value must be one of the time zone region names supported in the database. Valid in timestamp and interval formats, but not in `DATE` formats.  Example: US/Pacific |
| ``` WW ``` |  | Week of year (1-53) where week 1 starts on the first day of the year and continues to the seventh day of the year. |
| ``` W ``` |  | Week of month (1-5) where week 1 starts on the first day of the month and ends on the seventh. |
| ``` X ``` | Yes | Local radix character.  Example: `'HH:MI:SSXFF'`. |
| ``` Y,YYY ``` | Yes | Year with comma in this position. |
| ``` YEAR SYEAR ``` |  | Year, spelled out; `S` prefixes BC dates with a minus sign (-). |
| ``` YYYY SYYYY ``` | Yes | 4-digit year; `S` prefixes BC dates with a minus sign. |
| ``` YYY YY Y ``` | Yes | Last 3, 2, or 1 digit(s) of year. |