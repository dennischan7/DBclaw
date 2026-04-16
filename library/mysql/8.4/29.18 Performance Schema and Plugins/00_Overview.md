---
source: MySQL 8.4 Reference
title: 00_Overview
---

Removing a plugin with UNINSTALL PLUGIN does not affect information already collected for code in that plugin. Time spent executing the code while the plugin was loaded was still spent even if the plugin is unloaded later. The associated event information, including aggregate information, remains readable in performance\_schema database tables. For additional information about the effect of plugin installation and removal, see Section 29.7, "Performance Schema Status Monitoring".

A plugin implementor who instruments plugin code should document its instrumentation characteristics to enable those who load the plugin to account for its requirements. For example, a third-party storage engine should include in its documentation how much memory the engine needs for mutex and other instruments.

# <span id="page-192-0"></span>**29.19 Using the Performance Schema to Diagnose Problems**

The Performance Schema is a tool to help a DBA do performance tuning by taking real measurements instead of "wild guesses." This section demonstrates some ways to use the Performance Schema for this purpose. The discussion here relies on the use of event filtering, which is described in Section 29.4.2, "Performance Schema Event Filtering".

The following example provides one methodology that you can use to analyze a repeatable problem, such as investigating a performance bottleneck. To begin, you should have a repeatable use case where performance is deemed "too slow" and needs optimization, and you should enable all instrumentation (no pre-filtering at all).

- 1. Run the use case.
- 2. Using the Performance Schema tables, analyze the root cause of the performance problem. This analysis relies heavily on post-filtering.
- 3. For problem areas that are ruled out, disable the corresponding instruments. For example, if analysis shows that the issue is not related to file I/O in a particular storage engine, disable the file I/O instruments for that engine. Then truncate the history and summary tables to remove previously collected events.

4. Repeat the process at step 1.

With each iteration, the Performance Schema output, particularly the [events\\_waits\\_history\\_long](#page-30-0) table, contains less and less "noise" caused by nonsignificant instruments, and given that this table has a fixed size, contains more and more data relevant to the analysis of the problem at hand.

With each iteration, investigation should lead closer and closer to the root cause of the problem, as the "signal/noise" ratio improves, making analysis easier.

- 5. Once a root cause of performance bottleneck is identified, take the appropriate corrective action, such as:
  - Tune the server parameters (cache sizes, memory, and so forth).
  - Tune a query by writing it differently,
  - Tune the database schema (tables, indexes, and so forth).
  - Tune the code (this applies to storage engine or server developers only).
- 6. Start again at step 1, to see the effects of the changes on performance.

The mutex\_instances.LOCKED\_BY\_THREAD\_ID and rwlock\_instances.WRITE\_LOCKED\_BY\_THREAD\_ID columns are extremely important for investigating performance bottlenecks or deadlocks. This is made possible by Performance Schema instrumentation as follows:

- 1. Suppose that thread 1 is stuck waiting for a mutex.
- 2. You can determine what the thread is waiting for:

```
SELECT * FROM performance_schema.events_waits_current
WHERE THREAD_ID = thread_1;
```

Say the query result identifies that the thread is waiting for mutex A, found in events\_waits\_current.OBJECT\_INSTANCE\_BEGIN.

3. You can determine which thread is holding mutex A:

```
SELECT * FROM performance_schema.mutex_instances
WHERE OBJECT_INSTANCE_BEGIN = mutex_A;
```

Say the query result identifies that it is thread 2 holding mutex A, as found in mutex\_instances.LOCKED\_BY\_THREAD\_ID.

4. You can see what thread 2 is doing:

```
SELECT * FROM performance_schema.events_waits_current
WHERE THREAD_ID = thread_2;
```