---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view collation\_character\_set\_applicability identifies which character set the available collations are applicable to. In PostgreSQL, there is only one character set per database (see explanation in [Section 37.7](#page-122-0)), so this view does not provide much useful information.

**Table 37.9. collation\_character\_set\_applicability Columns**

```
Column Type
       Description
collation_catalog sql_identifier
       Name of the database containing the collation (always the current database)
collation_schema sql_identifier
       Name of the schema containing the collation
collation_name sql_identifier
       Name of the default collation
character_set_catalog sql_identifier
       Character sets are currently not implemented as schema objects, so this column is null
character_set_schema sql_identifier
       Character sets are currently not implemented as schema objects, so this column is null
character_set_name sql_identifier
       Name of the character set
```