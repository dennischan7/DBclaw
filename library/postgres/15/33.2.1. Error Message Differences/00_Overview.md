---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Some of the regression tests involve intentional invalid input values. Error messages can come from either the PostgreSQL code or from the host platform system routines. In the latter case, the messages can vary between platforms, but should reflect similar information. These differences in messages will result in a "failed" regression test that can be validated by inspection.