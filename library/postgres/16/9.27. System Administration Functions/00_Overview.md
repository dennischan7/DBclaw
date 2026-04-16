---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The functions described in this section are used to control and monitor a PostgreSQL installation.

# <span id="page-30-2"></span>**9.27.1. Configuration Settings Functions**

[Table 9.89](#page-30-2) shows the functions available to query and alter run-time configuration parameters.

**Table 9.89. Configuration Settings Functions**

![](_page_30_Figure_11.jpeg)

### **Description Example(s)**

Sets the parameter setting\_name to new\_value, and returns that value. If is\_local is true, the new value will only apply during the current transaction. If you want the new value to apply for the rest of the current session, use false instead. This function corresponds to the SQL command SET.

set\_config('log\_statement\_stats', 'off', false) → off