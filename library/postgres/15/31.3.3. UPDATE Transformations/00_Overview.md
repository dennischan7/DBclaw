---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Whenever an UPDATE is processed, the row filter expression is evaluated for both the old and new row (i.e. using the data before and after the update). If both evaluations are true, it replicates the UPDATE change. If both evaluations are false, it doesn't replicate the change. If only one of the old/new rows matches the row filter expression, the UPDATE is transformed to INSERT or DELETE, to avoid any data inconsistency. The row on the subscriber should reflect what is defined by the row filter expression on the publisher.

If the old row satisfies the row filter expression (it was sent to the subscriber) but the new row doesn't, then, from a data consistency perspective the old row should be removed from the subscriber. So the UPDATE is transformed into a DELETE.

If the old row doesn't satisfy the row filter expression (it wasn't sent to the subscriber) but the new row does, then, from a data consistency perspective the new row should be added to the subscriber. So the UPDATE is transformed into an INSERT.

<span id="page-78-0"></span>[Table 31.1](#page-78-0) summarizes the applied transformations.

**Table 31.1. UPDATE Transformation Summary**

| Old row  | New row  | Transformation  |
|----------|----------|-----------------|
| no match | no match | don't replicate |
| no match | match    | INSERT          |
| match    | no match | DELETE          |
| match    | match    | UPDATE          |