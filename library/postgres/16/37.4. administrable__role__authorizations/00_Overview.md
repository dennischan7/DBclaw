---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view administrable\_role\_authorizations identifies all roles that the current user has the admin option for.

#### **Table 37.2. administrable\_role\_authorizations Columns**

```
Column Type
       Description
grantee sql_identifier
       Name of the role to which this role membership was granted (can be the current user, or
       a different role in case of nested role memberships)
role_name sql_identifier
       Name of a role
is_grantable yes_or_no
       Always YES
```

# <span id="page-155-0"></span>**37.5. applicable\_roles**

The view applicable\_roles identifies all roles whose privileges the current user can use. This means there is some chain of role grants from the current user to the role in question. The current user itself is also an applicable role. The set of applicable roles is generally used for permission checking.

#### **Table 37.3. applicable\_roles Columns**

```
Column Type
      Description
grantee sql_identifier
```

Name of the role to which this role membership was granted (can be the current user, or a different role in case of nested role memberships)

role\_name sql\_identifier

Name of a role

is\_grantable yes\_or\_no

YES if the grantee has the admin option on the role, NO if not