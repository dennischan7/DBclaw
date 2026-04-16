---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following table summarizes INFORMATION\_SCHEMA thread pool tables. For greater detail, see the individual table descriptions.

**Table 28.7 INFORMATION\_SCHEMA Thread Pool Tables**

| Table Name            | Description                         |
|-----------------------|-------------------------------------|
| TP_THREAD_GROUP_STATE | Thread pool thread group states     |
| TP_THREAD_GROUP_STATS | Thread pool thread group statistics |
| TP_THREAD_STATE       | Thread pool thread information      |

## <span id="page-102-2"></span>**28.5.2 The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATE Table**

![](_page_102_Picture_2.jpeg)

#### **Note**

As of MySQL 8.0.14, the thread pool INFORMATION\_SCHEMA tables are also available as Performance Schema tables. (See Section 29.12.16, "Performance Schema Thread Pool Tables".) The INFORMATION\_SCHEMA tables are deprecated; expect them to be removed in a future version of MySQL. Applications should transition away from the old tables to the new tables. For example, if an application uses this query:

SELECT \* FROM INFORMATION\_SCHEMA.TP\_THREAD\_GROUP\_STATE;

The application should use this query instead:

SELECT \* FROM performance\_schema.tp\_thread\_group\_state;

The TP\_THREAD\_GROUP\_STATE table has one row per thread group in the thread pool. Each row provides information about the current state of a group.

For descriptions of the columns in the INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATE table, see Section 29.12.16.1, "The tp\_thread\_group\_state Table". The Performance Schema tp\_thread\_group\_state table has equivalent columns.

## <span id="page-102-0"></span>**28.5.3 The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATS Table**

![](_page_102_Picture_11.jpeg)

#### **Note**

As of MySQL 8.0.14, the thread pool INFORMATION\_SCHEMA tables are also available as Performance Schema tables. (See Section 29.12.16, "Performance Schema Thread Pool Tables".) The INFORMATION\_SCHEMA tables are deprecated; expect them to be removed in a future version of MySQL. Applications should transition away from the old tables to the new tables. For example, if an application uses this query:

SELECT \* FROM INFORMATION\_SCHEMA.TP\_THREAD\_GROUP\_STATS;

The application should use this query instead:

SELECT \* FROM performance\_schema.tp\_thread\_group\_stats;

The TP\_THREAD\_GROUP\_STATS table reports statistics per thread group. There is one row per group.

For descriptions of the columns in the INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATS table, see Section 29.12.16.2, "The tp\_thread\_group\_stats Table". The Performance Schema tp\_thread\_group\_stats table has equivalent columns.

# <span id="page-102-1"></span>**28.5.4 The INFORMATION\_SCHEMA TP\_THREAD\_STATE Table**

![](_page_102_Picture_20.jpeg)

### **Note**

As of MySQL 8.0.14, the thread pool INFORMATION\_SCHEMA tables are also available as Performance Schema tables. (See Section 29.12.16, "Performance Schema Thread Pool Tables".) The INFORMATION\_SCHEMA tables are deprecated; expect them to be removed in a future version of MySQL. Applications should transition away from the old tables to the new tables. For example, if an application uses this query:

SELECT \* FROM INFORMATION\_SCHEMA.TP\_THREAD\_STATE;

The application should use this query instead:

SELECT \* FROM performance\_schema.tp\_thread\_state;

The TP\_THREAD\_STATE table has one row per thread created by the thread pool to handle connections.

For descriptions of the columns in the INFORMATION\_SCHEMA TP\_THREAD\_STATE table, see Section 29.12.16.3, "The tp\_thread\_state Table". The Performance Schema tp\_thread\_state table has equivalent columns.