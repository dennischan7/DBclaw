---
source: MySQL 5.7 Reference
title: 00_Overview
---

[SIGNAL](#page-76-0), [RESIGNAL](#page-72-0), and [GET DIAGNOSTICS](#page-66-0) are not permissible as prepared statements. For example, this statement is invalid:

```
PREPARE stmt1 FROM 'SIGNAL SQLSTATE "02000"';
```

SQLSTATE values in class '04' are not treated specially. They are handled the same as other exceptions.

In standard SQL, the first condition relates to the SQLSTATE value returned for the previous SQL statement. In MySQL, this is not guaranteed, so to get the main error, you cannot do this:

```
GET DIAGNOSTICS CONDITION 1 @errno = MYSQL_ERRNO;
```

Instead, do this:

```
GET DIAGNOSTICS @cno = NUMBER;
GET DIAGNOSTICS CONDITION @cno @errno = MYSQL_ERRNO;
```