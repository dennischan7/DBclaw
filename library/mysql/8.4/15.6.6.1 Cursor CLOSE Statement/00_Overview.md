---
source: MySQL 8.4 Reference
title: 00_Overview
---

```
CLOSE cursor_name
```

This statement closes a previously opened cursor. For an example, see [Section 15.6.6, "Cursors"](#page-184-0).

An error occurs if the cursor is not open.

If not closed explicitly, a cursor is closed at the end of the [BEGIN ... END](#page-177-0) block in which it was declared.