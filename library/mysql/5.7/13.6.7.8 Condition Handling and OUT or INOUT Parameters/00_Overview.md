---
source: MySQL 5.7 Reference
title: 00_Overview
---

If a stored procedure exits with an unhandled exception, modified values of OUT and INOUT parameters are not propogated back to the caller.

If an exception is handled by a CONTINUE or EXIT handler that contains a [RESIGNAL](#page-72-0) statement, execution of [RESIGNAL](#page-72-0) pops the Diagnostics Area stack, thus signalling the exception (that is, the information that existed before entry into the handler). If the exception is an error, the values of OUT and INOUT parameters are not propogated back to the caller.