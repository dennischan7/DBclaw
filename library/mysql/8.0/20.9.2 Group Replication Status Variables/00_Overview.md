---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL 8.0 supports one status variable providing information about Group Replication. This variable is described here:

<span id="page-47-0"></span>• [group\\_replication\\_primary\\_member](#page-47-0)

Shows the primary member's UUID when the group is operating in single-primary mode. If the group is operating in multi-primary mode, this is an empty string.

![](_page_47_Picture_4.jpeg)

#### **Warning**

The group\_replication\_primary\_member status variable has been deprecated and is scheduled to be removed in a future version.

See Finding the Primary.