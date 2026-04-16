---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PL/pgSQL can be used to define trigger functions on data changes or database events. A trigger function is created with the CREATE FUNCTION command, declaring it as a function with no arguments and a return type of trigger (for data change triggers) or event\_trigger (for database event triggers). Special local variables named TG\_something are automatically defined to describe the condition that triggered the call.