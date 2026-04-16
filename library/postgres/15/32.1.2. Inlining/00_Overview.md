---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PostgreSQL is very extensible and allows new data types, functions, operators and other database objects to be defined; see Chapter 38. In fact the built-in objects are implemented using nearly the same mechanisms. This extensibility implies some overhead, for example due to function calls (see Section 38.3). To reduce that overhead, JIT compilation can inline the bodies of small functions into the expressions using them. That allows a significant percentage of the overhead to be optimized away.