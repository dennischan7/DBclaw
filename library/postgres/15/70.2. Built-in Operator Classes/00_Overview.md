---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The core PostgreSQL distribution includes the GIN operator classes shown in [Table 70.1.](#page-88-0) (Some of the optional modules described in Appendix F provide additional GIN operator classes.)

<span id="page-88-0"></span>**Table 70.1. Built-in GIN Operator Classes**

| Name           | Indexable Operators    |
|----------------|------------------------|
|                | && (anyarray,anyarray) |
|                | @> (anyarray,anyarray) |
| array_ops      | <@ (anyarray,anyarray) |
|                | = (anyarray,anyarray)  |
|                | @> (jsonb,jsonb)       |
|                | @? (jsonb,jsonpath)    |
| jsonb_ops      | @@ (jsonb,jsonpath)    |
|                | ? (jsonb,text)         |
|                | ?  (jsonb,text[])      |
|                | ?& (jsonb,text[])      |
|                | @> (jsonb,jsonb)       |
| jsonb_path_ops | @? (jsonb,jsonpath)    |
|                | @@ (jsonb,jsonpath)    |

<sup>1</sup> <http://www.sai.msu.su/~megera/wiki/Gin>

| Name         | Indexable Operators    |
|--------------|------------------------|
|              | @@ (tsvector,tsquery)  |
| tsvector_ops | @@@ (tsvector,tsquery) |

Of the two operator classes for type jsonb, jsonb\_ops is the default. jsonb\_path\_ops supports fewer operators but offers better performance for those operators. See Section 8.14.4 for details.