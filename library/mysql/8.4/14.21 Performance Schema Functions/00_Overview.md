---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL includes built-in SQL functions that format or retrieve Performance Schema data, and that may be used as equivalents for the corresponding sys schema stored functions. The built-in functions can be invoked in any schema and require no qualifier, unlike the sys functions, which require either a sys. schema qualifier or that sys be the current schema.

**Table 14.31 Performance Schema Functions**

| Name                   | Description                                     |
|------------------------|-------------------------------------------------|
| FORMAT_BYTES()         | Convert byte count to value with units          |
| FORMAT_PICO_TIME()     | Convert time in picoseconds to value with units |
| PS_CURRENT_THREAD_ID() | Performance Schema thread ID for current thread |
| PS_THREAD_ID()         | Performance Schema thread ID for given thread   |

The built-in functions supersede the corresponding sys functions, which are deprecated; expect them to be removed in a future version of MySQL. Applications that use the sys functions should be adjusted to use the built-in functions instead, keeping in mind some minor differences between the sys functions and the built-in functions. For details about these differences, see the function descriptions in this section.

<span id="page-45-0"></span>• [FORMAT\\_BYTES\(](#page-45-0)count)

Given a numeric byte count, converts it to human-readable format and returns a string consisting of a value and a units indicator. The string contains the number of bytes rounded to 2 decimal places and a minimum of 3 significant digits. Numbers less than 1024 bytes are represented as whole numbers and are not rounded. Returns NULL if count is NULL.

The units indicator depends on the size of the byte-count argument as shown in the following table.

| Argument Value     | Result Units | Result Units Indicator |
|--------------------|--------------|------------------------|
| Up to 1023         | bytes        | bytes                  |
| Up to 10242<br>− 1 | kibibytes    | KiB                    |
| Up to 10243<br>− 1 | mebibytes    | MiB                    |
| Up to 10244<br>− 1 | gibibytes    | GiB                    |
| Up to 10245<br>− 1 | tebibytes    | TiB                    |
| Up to 10246<br>− 1 | pebibytes    | PiB                    |
| 10246<br>and up    | exbibytes    | EiB                    |

```
mysql> SELECT FORMAT_BYTES(512), FORMAT_BYTES(18446644073709551615);
+-------------------+------------------------------------+
| FORMAT_BYTES(512) | FORMAT_BYTES(18446644073709551615) |
+-------------------+------------------------------------+
| 512 bytes | 16.00 EiB |
+-------------------+------------------------------------+
```

[FORMAT\\_BYTES\(\)](#page-45-0) may be used instead of the sys schema format\_bytes() function, keeping in mind this difference:

- [FORMAT\\_BYTES\(\)](#page-45-0) uses the EiB units indicator. sys.format\_bytes() does not.
- <span id="page-46-0"></span>• [FORMAT\\_PICO\\_TIME\(](#page-46-0)time\_val)

Given a numeric Performance Schema latency or wait time in picoseconds, converts it to humanreadable format and returns a string consisting of a value and a units indicator. The string contains the decimal time rounded to 2 decimal places and a minimum of 3 significant digits. Times under 1 nanosecond are represented as whole numbers and are not rounded.

If time\_val is NULL, this function returns NULL.

The units indicator depends on the size of the time-value argument as shown in the following table.

| Argument Value         | Result Units | Result Units Indicator |
|------------------------|--------------|------------------------|
| Up to 103<br>− 1       | picoseconds  | ps                     |
| Up to 106<br>− 1       | nanoseconds  | ns                     |
| Up to 109<br>− 1       | microseconds | us                     |
| Up to 1012<br>− 1      | milliseconds | ms                     |
| Up to 60×1012<br>− 1   | seconds      | s                      |
| Up to 3.6×1015<br>− 1  | minutes      | min                    |
| Up to 8.64×1016<br>− 1 | hours        | h                      |
| 8.64×1016 and up       | days         | d                      |

```
mysql> SELECT FORMAT_PICO_TIME(3501), FORMAT_PICO_TIME(188732396662000);
+------------------------+-----------------------------------+
| FORMAT_PICO_TIME(3501) | FORMAT_PICO_TIME(188732396662000) |
+------------------------+-----------------------------------+
| 3.50 ns | 3.15 min |
+------------------------+-----------------------------------+
```

[FORMAT\\_PICO\\_TIME\(\)](#page-46-0) may be used instead of the sys schema format\_time() function, keeping in mind these differences:

- To indicate minutes, sys.format\_time() uses the m units indicator, whereas [FORMAT\\_PICO\\_TIME\(\)](#page-46-0) uses min.
- sys.format\_time() uses the w (weeks) units indicator. [FORMAT\\_PICO\\_TIME\(\)](#page-46-0) does not.

<span id="page-47-0"></span>• [PS\\_CURRENT\\_THREAD\\_ID\(\)](#page-47-0)

Returns a BIGINT UNSIGNED value representing the Performance Schema thread ID assigned to the current connection.

The thread ID return value is a value of the type given in the THREAD\_ID column of Performance Schema tables.

Performance Schema configuration affects [PS\\_CURRENT\\_THREAD\\_ID\(\)](#page-47-0) the same way as for [PS\\_THREAD\\_ID\(\)](#page-47-1). For details, see the description of that function.

```
mysql> SELECT PS_CURRENT_THREAD_ID();
+------------------------+
| PS_CURRENT_THREAD_ID() |
+------------------------+
| 52 |
+------------------------+
mysql> SELECT PS_THREAD_ID(CONNECTION_ID());
+-------------------------------+
| PS_THREAD_ID(CONNECTION_ID()) |
+-------------------------------+
| 52 |
+-------------------------------+
```

[PS\\_CURRENT\\_THREAD\\_ID\(\)](#page-47-0) may be used as a shortcut for invoking the sys schema ps\_thread\_id() function with an argument of NULL or CONNECTION\_ID().

<span id="page-47-1"></span>• [PS\\_THREAD\\_ID\(](#page-47-1)connection\_id)

Given a connection ID, returns a BIGINT UNSIGNED value representing the Performance Schema thread ID assigned to the connection ID, or NULL if no thread ID exists for the connection ID. The latter can occur for threads that are not instrumented, or if connection\_id is NULL.

The connection ID argument is a value of the type given in the PROCESSLIST\_ID column of the Performance Schema threads table or the Id column of SHOW PROCESSLIST output.

The thread ID return value is a value of the type given in the THREAD\_ID column of Performance Schema tables.

Performance Schema configuration affects [PS\\_THREAD\\_ID\(\)](#page-47-1) operation as follows. (These remarks also apply to [PS\\_CURRENT\\_THREAD\\_ID\(\)](#page-47-0).)

- Disabling the thread\_instrumentation consumer disables statistics from being collected and aggregated at the thread level, but has no effect on [PS\\_THREAD\\_ID\(\)](#page-47-1).
- If performance\_schema\_max\_thread\_instances is not 0, the Performance Schema allocates memory for thread statistics and assigns an internal ID to each thread for which instance memory is available. If there are threads for which instance memory is not available, [PS\\_THREAD\\_ID\(\)](#page-47-1) returns NULL; in this case, Performance\_schema\_thread\_instances\_lost is nonzero.
- If performance\_schema\_max\_thread\_instances is 0, the Performance Schema allocates no thread memory and [PS\\_THREAD\\_ID\(\)](#page-47-1) returns NULL.
- If the Performance Schema itself is disabled, [PS\\_THREAD\\_ID\(\)](#page-47-1) produces an error.

```
mysql> SELECT PS_THREAD_ID(6);
+-----------------+
| PS_THREAD_ID(6) |
+-----------------+
| 45 |
```

+-----------------+

[PS\\_THREAD\\_ID\(\)](#page-47-1) may be used instead of the sys schema ps\_thread\_id() function, keeping in mind this difference:

• With an argument of NULL, sys.ps\_thread\_id() returns the thread ID for the current connection, whereas [PS\\_THREAD\\_ID\(\)](#page-47-1) returns NULL. To obtain the current connection thread ID, use [PS\\_CURRENT\\_THREAD\\_ID\(\)](#page-47-0) instead.