---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The information schema consists of a set of views that contain information about the objects defined in the current database. The information schema is defined in the SQL standard and can therefore be expected to be portable and remain stable — unlike the system catalogs, which are specific to PostgreSQL and are modeled after implementation concerns. The information schema views do not, however, contain information about PostgreSQL-specific features; to inquire about those you need to query the system catalogs or other PostgreSQL-specific views.

### **Note**

When querying the database for constraint information, it is possible for a standard-compliant query that expects to return one row to return several. This is because the SQL standard requires constraint names to be unique within a schema, but PostgreSQL does not enforce this restriction. PostgreSQL automatically-generated constraint names avoid duplicates in the same schema, but users can specify such duplicate names.

This problem can appear when querying information schema views such as check\_constraint\_routine\_usage, check\_constraints, domain\_constraints, and referential\_constraints. Some other views have similar issues but contain the table name to help distinguish duplicate rows, e.g., constraint\_column\_usage, constraint\_table\_usage, table\_constraints.