---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_foreign\_table contains auxiliary information about foreign tables. A foreign table is primarily represented by a [pg\\_class](#page-8-0) entry, just like a regular table. Its pg\_foreign\_table entry contains the information that is pertinent only to foreign tables and not any other kind of relation.

### **Table 52.25. pg\_foreign\_table Columns**

### **Column Type**

#### **Description**

ftrelid oid (references [pg\\_class](#page-8-0).oid)

The OID of the [pg\\_class](#page-8-0) entry for this foreign table

ftserver oid (references [pg\\_foreign\\_server](#page-20-0).oid)

OID of the foreign server for this foreign table

ftoptions text[]

Foreign table options, as "keyword=value" strings

# <span id="page-21-0"></span>**52.26. pg\_index**

The catalog pg\_index contains part of the information about indexes. The rest is mostly in [pg\\_class](#page-8-0).

### **Table 52.26. pg\_index Columns**

#### **Column Type**

#### **Description**

indexrelid oid (references [pg\\_class](#page-8-0).oid)

The OID of the [pg\\_class](#page-8-0) entry for this index

indrelid oid (references [pg\\_class](#page-8-0).oid)

The OID of the [pg\\_class](#page-8-0) entry for the table this index is for

indnatts int2

The total number of columns in the index (duplicates pg\_class.relnatts); this number includes both key and included attributes

indnkeyatts int2

The number of *key columns* in the index, not counting any *included columns*, which are merely stored and do not participate in the index semantics

indisunique bool

If true, this is a unique index

indisprimary bool

If true, this index represents the primary key of the table (indisunique should always be true when this is true)

indisexclusion bool

If true, this index supports an exclusion constraint

indimmediate bool

If true, the uniqueness check is enforced immediately on insertion (irrelevant if indisunique is not true)

indisclustered bool

If true, the table was last clustered on this index

indisvalid bool

If true, the index is currently valid for queries. False means the index is possibly incomplete: it must still be modified by INSERT/UPDATE operations, but it cannot safely be used for queries. If it is unique, the uniqueness property is not guaranteed true either.

indcheckxmin bool

#### **Description**

If true, queries must not use the index until the xmin of this pg\_index row is below their TransactionXmin event horizon, because the table may contain broken HOT chains with incompatible rows that they can see

#### indisready bool

If true, the index is currently ready for inserts. False means the index must be ignored by INSERT/UPDATE operations.

#### indislive bool

If false, the index is in process of being dropped, and should be ignored for all purposes (including HOT-safety decisions)

#### indisreplident bool

If true this index has been chosen as "replica identity" using ALTER TABLE ... RE-PLICA IDENTITY USING INDEX ...

#### indkey int2vector (references [pg\\_attribute](#page-3-0).attnum)

This is an array of indnatts values that indicate which table columns this index indexes. For example a value of 1 3 would mean that the first and the third table columns make up the index entries. Key columns come before non-key (included) columns. A zero in this array indicates that the corresponding index attribute is an expression over the table columns, rather than a simple column reference.

#### indcollation oidvector (references [pg\\_collation](#page-10-0).oid)

For each column in the index key (indnkeyatts values), this contains the OID of the collation to use for the index, or zero if the column is not of a collatable data type.

#### indclass oidvector (references [pg\\_opclass](#page-25-1).oid)

For each column in the index key (indnkeyatts values), this contains the OID of the operator class to use. See [pg\\_opclass](#page-25-1) for details.

#### indoption int2vector

This is an array of indnkeyatts values that store per-column flag bits. The meaning of the bits is defined by the index's access method.

#### indexprs pg\_node\_tree

Expression trees (in nodeToString() representation) for index attributes that are not simple column references. This is a list with one element for each zero entry in indkey. Null if all index attributes are simple references.

#### indpred pg\_node\_tree

Expression tree (in nodeToString() representation) for partial index predicate. Null if not a partial index.