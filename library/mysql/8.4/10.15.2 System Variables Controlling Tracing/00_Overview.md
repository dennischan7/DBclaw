---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following system variables affect optimizer tracing:

- optimizer\_trace: Enables or disables optimizer tracing. See [Section 10.15.8, "The](#page-75-0) [optimizer\\_trace System Variable"](#page-75-0).
- optimizer\_trace\_features: Enables or disables selected features of the MySQL Optimizer, using the syntax shown here:

```
SET optimizer_trace_features=option=value[,option=value][,...]
option: 
 {greedy_search | range_optimizer | dynamic_range | repeated_subselect}
value:
 {on | off | default}
```

See [Section 10.15.10, "Selecting Optimizer Features to Trace"](#page-75-1), for more information on the effects of these.

- optimizer\_trace\_max\_mem\_size: Maximum amount of memory that can be used for storing all traces.
- optimizer\_trace\_limit: The maximum number of optimizer traces to be shown. See [Section 10.15.4, "Tuning Trace Purging",](#page-74-0) for more information.
- optimizer\_trace\_offset: Offset of the first trace shown. See [Section 10.15.4, "Tuning Trace](#page-74-0) [Purging".](#page-74-0)
- end\_markers\_in\_json: If set to 1, causes the trace to repeat the key (if present) near the closing bracket. This also affects the output of EXPLAIN FORMAT=JSON in those versions of MySQL which support this statement. See [Section 10.15.9, "The end\\_markers\\_in\\_json System Variable"](#page-75-2).

### <span id="page-73-0"></span>**10.15.3 Traceable Statements**

Statements which are traceable are listed here:

- SELECT
- INSERT
- REPLACE
- UPDATE
- DELETE
- EXPLAIN with any of the preceding statements
- SET
- DO
- DECLARE, CASE, IF, and RETURN as used in stored routines
- CALL

Tracing is supported for both INSERT and REPLACE statements using VALUES, VALUES ROW, or SELECT.

Traces of multi-table UPDATE and DELETE statements are supported.

Tracing of SET optimizer\_trace is not supported.

For statements which are prepared and executed in separate steps, preparation and execution are traced separately.

# <span id="page-74-0"></span>**10.15.4 Tuning Trace Purging**

By default, each new trace overwrites the previous trace. Thus, if a statement contains substatements (such as invoking stored procedures, stored functions, or triggers), the topmost statement and substatements each generate one trace, but at the end of execution, the trace for only the last substatement is visible.

A user who wants to see the trace of a different substatement can enable or disable tracing for the desired substatement, but this requires editing the routine code, which may not always be possible. Another solution is to tune trace purging. This is done by setting the optimizer\_trace\_offset and optimizer\_trace\_limit system variables, like this:

```
SET optimizer_trace_offset=offset, optimizer_trace_limit=limit;
```

offset is a signed integer (default -1); limit is a positive integer (default 1). Such a SET statement has the following effects:

- All traces previously stored are cleared from memory.
- A subsequent SELECT from the OPTIMIZER\_TRACE table returns the first limit traces of the offset oldest stored traces (if offset >= 0), or the first limit traces of the -offset newest stored traces (if offset < 0).

#### Examples:

- SET optimizer\_trace\_offset=-1, optimizer\_trace\_limit=1: The most recent trace is shown (the default).
- SET optimizer\_trace\_offset=-2, optimizer\_trace\_limit=1: The next-to-last trace is shown.
- SET optimizer\_trace\_offset=-5, optimizer\_trace\_limit=5: The last five traces are shown.

Negative values for offset can thus prove useful when the substatements of interest are the last few in a stored routine. For example:

```
SET optimizer_trace_offset=-5, optimizer_trace_limit=5;
CALL stored_routine(); # more than 5 substatements in this routine
SELECT * FROM information_schema.OPTIMIZER_TRACE; # see only the last 5 traces
```

A positive offset can be useful when one knows that the interesting substatements are the first few in a stored routine.

The more accurately these two variables are set, the less memory is used. For example, SET optimizer\_trace\_offset=0, optimizer\_trace\_limit=5 requires sufficient memory to store five traces, so if only the three first are needed, is is better to use SET optimizer\_trace\_offset=0, optimizer\_trace\_limit=3, since tracing stops after limit traces. A stored routine may have a loop which executes many substatements and thus generates many traces, which can use a lot of memory; in such cases, choosing appropriate values for offset and limit can restrict tracing to, for example, a single iteration of the loop. This also decreases the impact of tracing on execution speed.

If offset is greater than or equal to 0, only limit traces are kept in memory. If offset is less than 0, that is not true: instead, -offset traces are kept in memory. Even if limit is smaller than offset, excluding the last statement, the last statement must still be traced because it will be within the limit after executing one more statement. Since an offset less than 0 is counted from the end, the "window" moves as more statements execute.

Using optimizer\_trace\_offset and optimizer\_trace\_limit, which are restrictions at the trace producer level, provide better (greater) speed and (less) memory usage than setting offsets or limits at the trace consumer (SQL) level with SELECT \* FROM OPTIMIZER\_TRACE LIMIT limit OFFSET offset, which saves almost nothing.