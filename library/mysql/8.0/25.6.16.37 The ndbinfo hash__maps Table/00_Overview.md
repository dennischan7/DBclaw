---
source: MySQL 8.0 Reference
title: 00_Overview
---

• id

The hash map's unique ID

• version

Hash map version (integer)

• state

Hash map state; see [Object::State](https://dev.mysql.com/doc/ndbapi/en/ndb-object.md#ndb-object-state) for values and descriptions.

• fq\_name

The hash map's fully qualified name

The hash\_maps table is actually a view consisting of the four columns having the same names of the [dict\\_obj\\_info](#page-154-0) table, as shown here:

```
CREATE VIEW hash_maps AS
 SELECT id, version, state, fq_name
 FROM dict_obj_info
 WHERE type=24; # Hash map; defined in dict_obj_types
```

See the description of [dict\\_obj\\_info](#page-154-0) for more information.

The hash\_maps table was added in NDB 8.0.29.