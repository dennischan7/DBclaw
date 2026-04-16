---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The timestamp type in C enables your programs to deal with data of the SQL type timestamp. See Section 8.5 for the equivalent type in the PostgreSQL server.

The following functions can be used to work with the timestamp type:

```
PGTYPEStimestamp_from_asc
```

Parse a timestamp from its textual representation into a timestamp variable.

```
timestamp PGTYPEStimestamp_from_asc(char *str, char **endptr);
```

The function receives the string to parse (str) and a pointer to a C char\* (endptr). At the moment ECPG always parses the complete string and so it currently does not support to store the address of the first invalid character in \*endptr. You can safely set endptr to NULL.

The function returns the parsed timestamp on success. On error, PGTYPESInvalidTimestamp is returned and errno is set to PGTYPES\_TS\_BAD\_TIMESTAMP. See [PGTYPESIn](#page-47-1)[validTimestamp](#page-47-1) for important notes on this value.

In general, the input string can contain any combination of an allowed date specification, a whitespace character and an allowed time specification. Note that time zones are not supported by ECPG. It can parse them but does not apply any calculation as the PostgreSQL server does for example. Timezone specifiers are silently discarded.

<span id="page-41-0"></span>[Table 36.5](#page-41-0) contains a few examples for input strings.

**Table 36.5. Valid Input Formats for PGTYPEStimestamp\_from\_asc**

| Input                       | Result                                                   |
|-----------------------------|----------------------------------------------------------|
| 1999-01-08 04:05:06         | 1999-01-08 04:05:06                                      |
| January 8 04:05:06 1999 PST | 1999-01-08 04:05:06                                      |
| 1999-Jan-08 04:05:06.789-8  | 1999-01-08 04:05:06.789 (time<br>zone specifier ignored) |
| J2451187 04:05-08:00        | 1999-01-08 04:05:00 (time zone<br>specifier ignored)     |

PGTYPEStimestamp\_to\_asc

Converts a date to a C char\* string.

```
char *PGTYPEStimestamp_to_asc(timestamp tstamp);
```

The function receives the timestamp tstamp as its only argument and returns an allocated string that contains the textual representation of the timestamp. The result must be freed with PGTYPE-Schar\_free().

PGTYPEStimestamp\_current

Retrieve the current timestamp.

```
void PGTYPEStimestamp_current(timestamp *ts);
```

The function retrieves the current timestamp and saves it into the timestamp variable that ts points to.

```
PGTYPEStimestamp_fmt_asc
```

Convert a timestamp variable to a C char\* using a format mask.

```
int PGTYPEStimestamp_fmt_asc(timestamp *ts, char *output, int
 str_len, char *fmtstr);
```

The function receives a pointer to the timestamp to convert as its first argument (ts), a pointer to the output buffer (output), the maximal length that has been allocated for the output buffer (str\_len) and the format mask to use for the conversion (fmtstr).

Upon success, the function returns 0 and a negative value if an error occurred.

You can use the following format specifiers for the format mask. The format specifiers are the same ones that are used in the strftime function in libc. Any non-format specifier will be copied into the output buffer.

- %A is replaced by national representation of the full weekday name.
- %a is replaced by national representation of the abbreviated weekday name.
- %B is replaced by national representation of the full month name.
- %b is replaced by national representation of the abbreviated month name.
- %C is replaced by (year / 100) as decimal number; single digits are preceded by a zero.
- %c is replaced by national representation of time and date.
- %D is equivalent to %m/%d/%y.
- %d is replaced by the day of the month as a decimal number (01–31).
- %E\* %O\* POSIX locale extensions. The sequences %Ec %EC %Ex %EX %Ey %EY %Od %Oe %OH %OI %Om %OM %OS %Ou %OU %OV %Ow %OW %Oy are supposed to provide alternative representations.

Additionally %OB implemented to represent alternative months names (used standalone, without day mentioned).

- %e is replaced by the day of month as a decimal number (1–31); single digits are preceded by a blank.
- %F is equivalent to %Y-%m-%d.
- %G is replaced by a year as a decimal number with century. This year is the one that contains the greater part of the week (Monday as the first day of the week).
- %g is replaced by the same year as in %G, but as a decimal number without century (00–99).
- %H is replaced by the hour (24-hour clock) as a decimal number (00–23).
- %h the same as %b.
- %I is replaced by the hour (12-hour clock) as a decimal number (01–12).
- %j is replaced by the day of the year as a decimal number (001–366).
- %k is replaced by the hour (24-hour clock) as a decimal number (0–23); single digits are preceded by a blank.
- %l is replaced by the hour (12-hour clock) as a decimal number (1–12); single digits are preceded by a blank.
- %M is replaced by the minute as a decimal number (00–59).
- %m is replaced by the month as a decimal number (01–12).
- %n is replaced by a newline.
- %O\* the same as %E\*.

- %p is replaced by national representation of either "ante meridiem" or "post meridiem" as appropriate.
- %R is equivalent to %H:%M.
- %r is equivalent to %I:%M:%S %p.
- %S is replaced by the second as a decimal number (00–60).
- %s is replaced by the number of seconds since the Epoch, UTC.
- %T is equivalent to %H:%M:%S
- %t is replaced by a tab.
- %U is replaced by the week number of the year (Sunday as the first day of the week) as a decimal number (00–53).
- %u is replaced by the weekday (Monday as the first day of the week) as a decimal number (1–7).
- %V is replaced by the week number of the year (Monday as the first day of the week) as a decimal number (01–53). If the week containing January 1 has four or more days in the new year, then it is week 1; otherwise it is the last week of the previous year, and the next week is week 1.
- %v is equivalent to %e-%b-%Y.
- %W is replaced by the week number of the year (Monday as the first day of the week) as a decimal number (00–53).
- %w is replaced by the weekday (Sunday as the first day of the week) as a decimal number (0–6).
- %X is replaced by national representation of the time.
- %x is replaced by national representation of the date.
- %Y is replaced by the year with century as a decimal number.
- %y is replaced by the year without century as a decimal number (00–99).
- %Z is replaced by the time zone name.
- %z is replaced by the time zone offset from UTC; a leading plus sign stands for east of UTC, a minus sign for west of UTC, hours and minutes follow with two digits each and no delimiter between them (common form for [RFC 822](https://datatracker.ietf.org/doc/html/rfc822)<sup>1</sup> date headers).
- %+ is replaced by national representation of the date and time.
- %-\* GNU libc extension. Do not do any padding when performing numerical outputs.
- \$\_\* GNU libc extension. Explicitly specify space for padding.
- %0\* GNU libc extension. Explicitly specify zero for padding.
- %% is replaced by %.

PGTYPEStimestamp\_sub

Subtract one timestamp from another one and save the result in a variable of type interval.

<sup>1</sup> <https://datatracker.ietf.org/doc/html/rfc822>

```
int PGTYPEStimestamp_sub(timestamp *ts1, timestamp *ts2,
 interval *iv);
```

The function will subtract the timestamp variable that ts2 points to from the timestamp variable that ts1 points to and will store the result in the interval variable that iv points to.

Upon success, the function returns 0 and a negative value if an error occurred.

```
PGTYPEStimestamp_defmt_asc
```

Parse a timestamp value from its textual representation using a formatting mask.

```
int PGTYPEStimestamp_defmt_asc(char *str, char *fmt, timestamp
 *d);
```

The function receives the textual representation of a timestamp in the variable str as well as the formatting mask to use in the variable fmt. The result will be stored in the variable that d points to.

If the formatting mask fmt is NULL, the function will fall back to the default formatting mask which is %Y-%m-%d %H:%M:%S.

This is the reverse function to [PGTYPEStimestamp\\_fmt\\_asc](#page-41-1). See the documentation there in order to find out about the possible formatting mask entries.

```
PGTYPEStimestamp_add_interval
```

Add an interval variable to a timestamp variable.

```
int PGTYPEStimestamp_add_interval(timestamp *tin, interval
 *span, timestamp *tout);
```

The function receives a pointer to a timestamp variable tin and a pointer to an interval variable span. It adds the interval to the timestamp and saves the resulting timestamp in the variable that tout points to.

Upon success, the function returns 0 and a negative value if an error occurred.

```
PGTYPEStimestamp_sub_interval
```

Subtract an interval variable from a timestamp variable.

```
int PGTYPEStimestamp_sub_interval(timestamp *tin, interval
 *span, timestamp *tout);
```

The function subtracts the interval variable that span points to from the timestamp variable that tin points to and saves the result into the variable that tout points to.

Upon success, the function returns 0 and a negative value if an error occurred.