---
source: MySQL 8.4 Reference
title: 00_Overview
---

Tables in the performance\_schema database can be grouped as follows:

- Setup tables. These tables are used to configure and display monitoring characteristics.
- Current events tables. The [events\\_waits\\_current](#page-27-0) table contains the most recent event for each thread. Other similar tables contain current events at different levels of the event hierarchy: [events\\_stages\\_current](#page-34-0) for stage events, [events\\_statements\\_current](#page-39-0) for statement events, and [events\\_transactions\\_current](#page-50-0) for transaction events.
- History tables. These tables have the same structure as the current events tables, but contain more rows. For example, for wait events, [events\\_waits\\_history](#page-29-0) table contains the most recent 10 events per thread. [events\\_waits\\_history\\_long](#page-30-0) contains the most recent 10,000 events. Other similar tables exist for stage, statement, and transaction histories.

To change the sizes of the history tables, set the appropriate system variables at server startup. For example, to set the sizes of the wait event history tables, set [performance\\_schema\\_events\\_waits\\_history\\_size](#page-173-0) and [performance\\_schema\\_events\\_waits\\_history\\_long\\_size](#page-173-1).

- Summary tables. These tables contain information aggregated over groups of events, including those that have been discarded from the history tables.
- Instance tables. These tables document what types of objects are instrumented. An instrumented object, when used by the server, produces an event. These tables provide event names and explanatory notes or status information.
- Miscellaneous tables. These do not fall into any of the other table groups.