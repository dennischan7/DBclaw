---
source: MySQL 8.4 Reference
title: 00_Overview
---

To perform optimizer tracing entails the following steps:

- 1. Enable tracing by executing SET optimizer\_trace="enabled=ON".
- 2. Execute the statement to be traced. See [Section 10.15.3, "Traceable Statements",](#page-73-0) for a listing of statements which can be traced.
- 3. Examine the contents of the INFORMATION\_SCHEMA.OPTIMIZER\_TRACE table.
- 4. To examine traces for multiple queries, repeat the previous two steps as needed.
- 5. To disable tracing after you have finished, execute SET optimizer\_trace="enabled=OFF".

You can trace only statements which are executed within the current session; you cannot see traces from other sessions.