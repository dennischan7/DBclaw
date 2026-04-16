---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view enabled\_roles identifies the currently "enabled roles". The enabled roles are recursively defined as the current user together with all roles that have been granted to the enabled roles with automatic inheritance. In other words, these are all roles that the current user has direct or indirect, automatically inheriting membership in.

For permission checking, the set of "applicable roles" is applied, which can be broader than the set of enabled roles. So generally, it is better to use the view applicable\_roles instead of this one; See [Section 37.5](#page-155-0) for details on applicable\_roles view.

#### **Table 37.23. enabled\_roles Columns**

```
Column Type
       Description
role_name sql_identifier
       Name of a role
```