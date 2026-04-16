---
source: PostgreSQL 14 Reference
title: 00_Overview
---

## <span id="page-60-2"></span><span id="page-60-0"></span>**20.8.1. Where to Log**

log\_destination (string)

PostgreSQL supports several methods for logging server messages, including stderr, csvlog and syslog. On Windows, eventlog is also supported. Set this parameter to a list of desired log destinations separated by commas. The default is to log to stderr only. This parameter can only be set in the postgresql.conf file or on the server command line.

If csvlog is included in log\_destination, log entries are output in "comma separated value" (CSV) format, which is convenient for loading logs into programs. See [Section 20.8.4](#page-70-0) for details. [logging\\_collector](#page-60-1) must be enabled to generate CSV-format log output.

When either stderr or csvlog are included, the file current\_logfiles is created to record the location of the log file(s) currently in use by the logging collector and the associated logging destination. This provides a convenient way to find the logs currently in use by the instance. Here is an example of this file's content:

```
stderr log/postgresql.log
csvlog log/postgresql.csv
```

current\_logfiles is recreated when a new log file is created as an effect of rotation, and when log\_destination is reloaded. It is removed when neither stderr nor csvlog are included in log\_destination, and when the logging collector is disabled.

### **Note**

On most Unix systems, you will need to alter the configuration of your system's syslog daemon in order to make use of the syslog option for log\_destination. PostgreSQL can log to syslog facilities LOCAL0 through LOCAL7 (see [syslog\\_facility\)](#page-62-0), but the default syslog configuration on most platforms will discard all such messages. You will need to add something like:

```
local0.* /var/log/postgresql
```

to the syslog daemon's configuration file to make it work.

On Windows, when you use the eventlog option for log\_destination, you should register an event source and its library with the operating system so that the Windows Event Viewer can display event log messages cleanly. See [Section 19.12](#page-15-0) for details.

```
logging_collector (boolean)
```

This parameter enables the *logging collector*, which is a background process that captures log messages sent to stderr and redirects them into log files. This approach is often more useful than logging to syslog, since some types of messages might not appear in syslog output. (One common example is dynamic-linker failure messages; another is error messages produced by scripts such as archive\_command.) This parameter can only be set at server start.

### **Note**

It is possible to log to stderr without using the logging collector; the log messages will just go to wherever the server's stderr is directed. However, that method is only suitable for low log volumes, since it provides no convenient way to rotate log files. Also, on some platforms not using the logging collector can result in lost or garbled log output, because multiple processes writing concurrently to the same log file can overwrite each other's output.

### **Note**

The logging collector is designed to never lose messages. This means that in case of extremely high load, server processes could be blocked while trying to send additional log messages when the collector has fallen behind. In contrast, syslog prefers to drop messages if it cannot write them, which means it may fail to log some messages in such cases but it will not block the rest of the system.

#### <span id="page-61-0"></span>log\_directory (string)

When logging\_collector is enabled, this parameter determines the directory in which log files will be created. It can be specified as an absolute path, or relative to the cluster data directory. This parameter can only be set in the postgresql.conf file or on the server command line. The default is log.

#### log\_filename (string)

When logging\_collector is enabled, this parameter sets the file names of the created log files. The value is treated as a strftime pattern, so %-escapes can be used to specify timevarying file names. (Note that if there are any time-zone-dependent %-escapes, the computation is done in the zone specified by [log\\_timezone.](#page-70-1)) The supported %-escapes are similar to those listed in the Open Group's [strftime](https://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.md) <sup>1</sup> specification. Note that the system's strftime is not used directly, so platform-specific (nonstandard) extensions do not work. The default is postgresql-%Y- %m-%d\_%H%M%S.log.

If you specify a file name without escapes, you should plan to use a log rotation utility to avoid eventually filling the entire disk. In releases prior to 8.4, if no % escapes were present, PostgreSQL would append the epoch of the new log file's creation time, but this is no longer the case.

If CSV-format output is enabled in log\_destination, .csv will be appended to the timestamped log file name to create the file name for CSV-format output. (If log\_filename ends in .log, the suffix is replaced instead.)

This parameter can only be set in the postgresql.conf file or on the server command line.

```
log_file_mode (integer)
```

On Unix systems this parameter sets the permissions for log files when logging\_collector is enabled. (On Microsoft Windows this parameter is ignored.) The parameter value is expected to be a numeric mode specified in the format accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).)

The default permissions are 0600, meaning only the server owner can read or write the log files. The other commonly useful setting is 0640, allowing members of the owner's group to read the files. Note however that to make use of such a setting, you'll need to alter [log\\_directory](#page-61-0) to store the files somewhere outside the cluster data directory. In any case, it's unwise to make the log files world-readable, since they might contain sensitive data.

This parameter can only be set in the postgresql.conf file or on the server command line.

<sup>1</sup> <https://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html>

```
log_rotation_age (integer)
```

When logging\_collector is enabled, this parameter determines the maximum amount of time to use an individual log file, after which a new log file will be created. If this value is specified without units, it is taken as minutes. The default is 24 hours. Set to zero to disable time-based creation of new log files. This parameter can only be set in the postgresql.conf file or on the server command line.

```
log_rotation_size (integer)
```

When logging\_collector is enabled, this parameter determines the maximum size of an individual log file. After this amount of data has been emitted into a log file, a new log file will be created. If this value is specified without units, it is taken as kilobytes. The default is 10 megabytes. Set to zero to disable size-based creation of new log files. This parameter can only be set in the postgresql.conf file or on the server command line.

```
log_truncate_on_rotation (boolean)
```

When logging\_collector is enabled, this parameter will cause PostgreSQL to truncate (overwrite), rather than append to, any existing log file of the same name. However, truncation will occur only when a new file is being opened due to time-based rotation, not during server startup or size-based rotation. When off, pre-existing files will be appended to in all cases. For example, using this setting in combination with a log\_filename like postgresql-%H.log would result in generating twenty-four hourly log files and then cyclically overwriting them. This parameter can only be set in the postgresql.conf file or on the server command line.

Example: To keep 7 days of logs, one log file per day named server\_log.Mon, server\_log.Tue, etc, and automatically overwrite last week's log with this week's log, set log\_filename to server\_log.%a, log\_truncate\_on\_rotation to on, and log\_rotation\_age to 1440.

Example: To keep 24 hours of logs, one log file per hour, but also rotate sooner if the log file size exceeds 1GB, set log\_filename to server\_log.%H%M, log\_truncate\_on\_rotation to on, log\_rotation\_age to 60, and log\_rotation\_size to 1000000. Including %M in log\_filename allows any size-driven rotations that might occur to select a file name different from the hour's initial file name.

```
syslog_facility (enum)
```

When logging to syslog is enabled, this parameter determines the syslog "facility" to be used. You can choose from LOCAL0, LOCAL1, LOCAL2, LOCAL3, LOCAL4, LOCAL5, LOCAL6, LOCAL7; the default is LOCAL0. See also the documentation of your system's syslog daemon. This parameter can only be set in the postgresql.conf file or on the server command line.

```
syslog_ident (string)
```

When logging to syslog is enabled, this parameter determines the program name used to identify PostgreSQL messages in syslog logs. The default is postgres. This parameter can only be set in the postgresql.conf file or on the server command line.

```
syslog_sequence_numbers (boolean)
```

When logging to syslog and this is on (the default), then each message will be prefixed by an increasing sequence number (such as [2]). This circumvents the "--- last message repeated N times ---" suppression that many syslog implementations perform by default. In more modern syslog implementations, repeated message suppression can be configured (for example, \$RepeatedMsgReduction in rsyslog), so this might not be necessary. Also, you could turn this off if you actually want to suppress repeated messages.

This parameter can only be set in the postgresql.conf file or on the server command line.

```
syslog_split_messages (boolean)
```

When logging to syslog is enabled, this parameter determines how messages are delivered to syslog. When on (the default), messages are split by lines, and long lines are split so that they will fit into 1024 bytes, which is a typical size limit for traditional syslog implementations. When off, PostgreSQL server log messages are delivered to the syslog service as is, and it is up to the syslog service to cope with the potentially bulky messages.

If syslog is ultimately logging to a text file, then the effect will be the same either way, and it is best to leave the setting on, since most syslog implementations either cannot handle large messages or would need to be specially configured to handle them. But if syslog is ultimately writing into some other medium, it might be necessary or more useful to keep messages logically together.

This parameter can only be set in the postgresql.conf file or on the server command line.

```
event_source (string)
```

When logging to event log is enabled, this parameter determines the program name used to identify PostgreSQL messages in the log. The default is PostgreSQL. This parameter can only be set at server start.

## <span id="page-63-2"></span>**20.8.2. When to Log**

```
log_min_messages (enum)
```

Controls which [message levels](#page-64-0) are written to the server log. Valid values are DEBUG5, DEBUG4, DEBUG3, DEBUG2, DEBUG1, INFO, NOTICE, WARNING, ERROR, LOG, FATAL, and PANIC. Each level includes all the levels that follow it. The later the level, the fewer messages are sent to the log. The default is WARNING. Note that LOG has a different rank here than in [client\\_min\\_mes](#page-75-0)[sages.](#page-75-0) Only superusers can change this setting.

```
log_min_error_statement (enum)
```

Controls which SQL statements that cause an error condition are recorded in the server log. The current SQL statement is included in the log entry for any message of the specified [severity](#page-64-0) or higher. Valid values are DEBUG5, DEBUG4, DEBUG3, DEBUG2, DEBUG1, INFO, NOTICE, WARNING, ERROR, LOG, FATAL, and PANIC. The default is ERROR, which means statements causing errors, log messages, fatal errors, or panics will be logged. To effectively turn off logging of failing statements, set this parameter to PANIC. Only superusers can change this setting.

```
log_min_duration_statement (integer)
```

Causes the duration of each completed statement to be logged if the statement ran for at least the specified amount of time. For example, if you set it to 250ms then all SQL statements that run 250ms or longer will be logged. Enabling this parameter can be helpful in tracking down unoptimized queries in your applications. If this value is specified without units, it is taken as milliseconds. Setting this to zero prints all statement durations. -1 (the default) disables logging statement durations. Only superusers can change this setting.

This overrides [log\\_min\\_duration\\_sample,](#page-64-1) meaning that queries with duration exceeding this setting are not subject to sampling and are always logged.

For clients using extended query protocol, durations of the Parse, Bind, and Execute steps are logged independently.

### **Note**

When using this option together with [log\\_statement,](#page-69-0) the text of statements that are logged because of log\_statement will not be repeated in the duration log message. If you are not using syslog, it is recommended that you log the PID or session ID using [log\\_line\\_pre-](#page-67-0) [fix](#page-67-0) so that you can link the statement message to the later duration message using the process ID or session ID.

<span id="page-64-1"></span>log\_min\_duration\_sample (integer)

Allows sampling the duration of completed statements that ran for at least the specified amount of time. This produces the same kind of log entries as [log\\_min\\_duration\\_statement,](#page-63-1) but only for a subset of the executed statements, with sample rate controlled by [log\\_statement\\_sample\\_rate.](#page-64-2) For example, if you set it to 100ms then all SQL statements that run 100ms or longer will be considered for sampling. Enabling this parameter can be helpful when the traffic is too high to log all queries. If this value is specified without units, it is taken as milliseconds. Setting this to zero samples all statement durations. -1 (the default) disables sampling statement durations. Only superusers can change this setting.

This setting has lower priority than log\_min\_duration\_statement, meaning that statements with durations exceeding log\_min\_duration\_statement are not subject to sampling and are always logged.

Other notes for log\_min\_duration\_statement apply also to this setting.

<span id="page-64-2"></span>log\_statement\_sample\_rate (floating point)

Determines the fraction of statements with duration exceeding [log\\_min\\_duration\\_sample](#page-64-1) that will be logged. Sampling is stochastic, for example 0.5 means there is statistically one chance in two that any given statement will be logged. The default is 1.0, meaning to log all sampled statements. Setting this to zero disables sampled statement-duration logging, the same as setting log\_min\_duration\_sample to -1. Only superusers can change this setting.

log\_transaction\_sample\_rate (floating point)

Sets the fraction of transactions whose statements are all logged, in addition to statements logged for other reasons. It applies to each new transaction regardless of its statements' durations. Sampling is stochastic, for example 0.1 means there is statistically one chance in ten that any given transaction will be logged. log\_transaction\_sample\_rate can be helpful to construct a sample of transactions. The default is 0, meaning not to log statements from any additional transactions. Setting this to 1 logs all statements of all transactions. Only superusers can change this setting.

### **Note**

Like all statement-logging options, this option can add significant overhead.

[Table 20.2](#page-64-0) explains the message severity levels used by PostgreSQL. If logging output is sent to syslog or Windows' eventlog, the severity levels are translated as shown in the table.

<span id="page-64-0"></span>**Table 20.2. Message Severity Levels**

| Severity         | Usage                                                                                                       | syslog | eventlog    |
|------------------|-------------------------------------------------------------------------------------------------------------|--------|-------------|
| DEBUG1<br>DEBUG5 | Provides successively-more-detailed<br>information for use by developers.                                   | DEBUG  | INFORMATION |
| INFO             | Provides information implicitly re<br>quested by the user, e.g., output from<br>VACUUM VERBOSE.             | INFO   | INFORMATION |
| NOTICE           | Provides information that might be<br>helpful to users, e.g., notice of trunca<br>tion of long identifiers. | NOTICE | INFORMATION |

| Severity | Usage                                                                                 | syslog  | eventlog    |
|----------|---------------------------------------------------------------------------------------|---------|-------------|
| WARNING  | Provides warnings of likely problems,<br>e.g., COMMIT outside a transaction<br>block. | NOTICE  | WARNING     |
| ERROR    | Reports an error that caused the cur<br>rent command to abort.                        | WARNING | ERROR       |
| LOG      | Reports information of interest to ad<br>ministrators, e.g., checkpoint activity.     | INFO    | INFORMATION |
| FATAL    | Reports an error that caused the cur<br>rent session to abort.                        | ERR     | ERROR       |
| PANIC    | Reports an error that caused all data<br>base sessions to abort.                      | CRIT    | ERROR       |