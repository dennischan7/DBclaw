---
source: PostgreSQL 14 Reference
title: 00_Overview
---

This section describes the message flow and the semantics of each message type. (Details of the exact representation of each message appear in [Section 53.7.](#page-102-0)) There are several different sub-protocols depending on the state of the connection: start-up, query, function call, COPY, and termination. There are also special provisions for asynchronous operations (including notification responses and command cancellation), which can occur at any time after the start-up phase.