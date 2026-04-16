---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Some functions such as PGTYPESnumeric\_to\_asc return a pointer to a freshly allocated character string. These results should be freed with PGTYPESchar\_free instead of free. (This is important only on Windows, where memory allocation and release sometimes need to be done by the same library.)