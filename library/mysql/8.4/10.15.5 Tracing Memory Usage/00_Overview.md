---
source: MySQL 8.4 Reference
title: 00_Overview
---

Each stored trace is a string, which is extended (using realloc()) as optimization progresses by appending more data to it. The optimizer\_trace\_max\_mem\_size server system variable sets a limit on the total amount of memory used by all traces currently being stored. If this limit is reached, the current trace is not extended, which means the trace is incomplete; in this case the MISSING\_BYTES\_BEYOND\_MAX\_MEM\_SIZE column shows the number of bytes missing from the trace.