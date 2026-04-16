---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_cast stores data type conversion paths, both built-in and user-defined.

It should be noted that pg\_cast does not represent every type conversion that the system knows how to perform; only those that cannot be deduced from some generic rule. For example, casting between a domain and its base type is not explicitly represented in pg\_cast. Another important exception is that "automatic I/O conversion casts", those performed using a data type's own I/O functions to convert to or from text or other string types, are not explicitly represented in pg\_cast.

### **Table 52.10. pg\_cast Columns**

### **Column Type Description** oid oid Row identifier castsource oid (references [pg\\_type](#page-45-0).oid) OID of the source data type casttarget oid (references [pg\\_type](#page-45-0).oid) OID of the target data type castfunc oid (references [pg\\_proc](#page-29-0).oid) The OID of the function to use to perform this cast. Zero is stored if the cast method doesn't require a function. castcontext char Indicates what contexts the cast can be invoked in. e means only as an explicit cast (us-

castmethod char

Indicates how the cast is performed. f means that the function specified in the castfunc field is used. i means that the input/output functions are used. b means that the types are binary-coercible, thus no conversion is required.

ing CAST or :: syntax). a means implicitly in assignment to a target column, as well as

explicitly. i means implicitly in expressions, as well as the other cases.

The cast functions listed in pg\_cast must always take the cast source type as their first argument type, and return the cast destination type as their result type. A cast function can have up to three arguments. The second argument, if present, must be type integer; it receives the type modifier associated with the destination type, or -1 if there is none. The third argument, if present, must be type boolean; it receives true if the cast is an explicit cast, false otherwise.

It is legitimate to create a pg\_cast entry in which the source and target types are the same, if the associated function takes more than one argument. Such entries represent "length coercion functions" that coerce values of the type to be legal for a particular type modifier value.

When a pg\_cast entry has different source and target types and a function that takes more than one argument, it represents converting from one type to another and applying a length coercion in a single step. When no such entry is available, coercion to a type that uses a type modifier involves two steps, one to convert between data types and a second to apply the modifier.

# <span id="page-8-0"></span>**52.11. pg\_class**

The catalog pg\_class describes tables and other objects that have columns or are otherwise similar to a table. This includes indexes (but see also [pg\\_index](#page-21-0)), sequences (but see also [pg\\_sequence](#page-34-0)), views, materialized views, composite types, and TOAST tables; see relkind. Below, when we mean all of these kinds of objects we speak of "relations". Not all of pg\_class's columns are meaningful for all relation kinds.

### **Table 52.11. pg\_class Columns**

#### **Column Type Description**

oid oid

Row identifier

relname name

Name of the table, index, view, etc.

relnamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this relation

reltype oid (references [pg\\_type](#page-45-0).oid)

The OID of the data type that corresponds to this table's row type, if any; zero for indexes, sequences, and toast tables, which have no pg\_type entry

reloftype oid (references [pg\\_type](#page-45-0).oid)

For typed tables, the OID of the underlying composite type; zero for all other relations

relowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the relation

relam oid (references [pg\\_am](#page-1-0).oid)

If this is a table or an index, the access method used (heap, B-tree, hash, etc.); otherwise zero (zero occurs for sequences, as well as relations without storage, such as views)

relfilenode oid

Name of the on-disk file of this relation; zero means this is a "mapped" relation whose disk file name is determined by low-level state

reltablespace oid (references [pg\\_tablespace](#page-41-0).oid)

The tablespace in which this relation is stored. If zero, the database's default tablespace is implied. Not meaningful if the relation has no on-disk file, except for partitioned tables, where this is the tablespace in which partitions will be created when one is not specified in the creation command.

relpages int4

#### **Description**

Size of the on-disk representation of this table in pages (of size BLCKSZ). This is only an estimate used by the planner. It is updated by VACUUM, ANALYZE, and a few DDL commands such as CREATE INDEX.

#### reltuples float4

Number of live rows in the table. This is only an estimate used by the planner. It is updated by VACUUM, ANALYZE, and a few DDL commands such as CREATE INDEX. If the table has never yet been vacuumed or analyzed, reltuples contains -1 indicating that the row count is unknown.

#### relallvisible int4

Number of pages that are marked all-visible in the table's visibility map. This is only an estimate used by the planner. It is updated by VACUUM, ANALYZE, and a few DDL commands such as CREATE INDEX.

#### reltoastrelid oid (references [pg\\_class](#page-8-0).oid)

OID of the TOAST table associated with this table, zero if none. The TOAST table stores large attributes "out of line" in a secondary table.

#### relhasindex bool

True if this is a table and it has (or recently had) any indexes

#### relisshared bool

True if this table is shared across all databases in the cluster. Only certain system catalogs (such as [pg\\_database](#page-13-0)) are shared.

#### relpersistence char

p = permanent table, u = unlogged table, t = temporary table

#### relkind char

r = ordinary table, i = index, S = sequence, t = TOAST table, v = view, m = materialized view, c = composite type, f = foreign table, p = partitioned table, I = partitioned index

#### relnatts int2

Number of user columns in the relation (system columns not counted). There must be this many corresponding entries in [pg\\_attribute](#page-3-0). See also pg\_attribute.attnum.

#### relchecks int2

Number of CHECK constraints on the table; see [pg\\_constraint](#page-11-0) catalog

#### relhasrules bool

True if table has (or once had) rules; see [pg\\_rewrite](#page-33-0) catalog

#### relhastriggers bool

True if table has (or once had) triggers; see [pg\\_trigger](#page-42-0) catalog

#### relhassubclass bool

True if table or index has (or once had) any inheritance children

#### relrowsecurity bool

True if table has row-level security enabled; see [pg\\_policy](#page-28-0) catalog

#### relforcerowsecurity bool

True if row-level security (when enabled) will also apply to table owner; see [pg\\_poli](#page-28-0)[cy](#page-28-0) catalog

#### relispopulated bool

True if relation is populated (this is true for all relations other than some materialized views)

#### relreplident char

#### **Description**

Columns used to form "replica identity" for rows: d = default (primary key, if any), n = nothing, f = all columns, i = index with indisreplident set (same as nothing if the index used has been dropped)

relispartition bool

True if table or index is a partition

relrewrite oid (references [pg\\_class](#page-8-0).oid)

For new relations being written during a DDL operation that requires a table rewrite, this contains the OID of the original relation; otherwise zero. That state is only visible internally; this field should never contain anything other than zero for a user-visible relation.

relfrozenxid xid

All transaction IDs before this one have been replaced with a permanent ("frozen") transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent transaction ID wraparound or to allow pg\_xact to be shrunk. Zero (InvalidTransactionId) if the relation is not a table.

relminmxid xid

All multixact IDs before this one have been replaced by a transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent multixact ID wraparound or to allow pg\_multixact to be shrunk. Zero (InvalidMulti-XactId) if the relation is not a table.

relacl aclitem[]

Access privileges; see Section 5.7 for details

reloptions text[]

Access-method-specific options, as "keyword=value" strings

relpartbound pg\_node\_tree

If table is a partition (see relispartition), internal representation of the partition bound

Several of the Boolean flags in pg\_class are maintained lazily: they are guaranteed to be true if that's the correct state, but may not be reset to false immediately when the condition is no longer true. For example, relhasindex is set by CREATE INDEX, but it is never cleared by DROP INDEX. Instead, VACUUM clears relhasindex if it finds the table has no indexes. This arrangement avoids race conditions and improves concurrency.

# <span id="page-10-0"></span>**52.12. pg\_collation**

The catalog pg\_collation describes the available collations, which are essentially mappings from an SQL name to operating system locale categories. See Section 24.2 for more information.

### **Table 52.12. pg\_collation Columns**

### **Column Type Description**

oid oid

Row identifier

collname name

Collation name (unique per namespace and encoding)

collnamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this collation

collowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the collation

collprovider char

#### **Description**

Provider of the collation: d = database default, c = libc, i = icu

collisdeterministic bool

Is the collation deterministic?

collencoding int4

Encoding in which the collation is applicable, or -1 if it works for any encoding

collcollate name

LC\_COLLATE for this collation object

collctype name

LC\_CTYPE for this collation object

collversion text

Provider-specific version of the collation. This is recorded when the collation is created and then checked when it is used, to detect changes in the collation definition that could lead to data corruption.

Note that the unique key on this catalog is (collname, collencoding, collnamespace) not just (collname, collnamespace). PostgreSQL generally ignores all collations that do not have collencoding equal to either the current database's encoding or -1, and creation of new entries with the same name as an entry with collencoding = -1 is forbidden. Therefore it is sufficient to use a qualified SQL name (schema.name) to identify a collation, even though this is not unique according to the catalog definition. The reason for defining the catalog this way is that initdb fills it in at cluster initialization time with entries for all locales available on the system, so it must be able to hold entries for all encodings that might ever be used in the cluster.

In the template0 database, it could be useful to create collations whose encoding does not match the database encoding, since they could match the encodings of databases later cloned from template0. This would currently have to be done manually.

# <span id="page-11-0"></span>**52.13. pg\_constraint**

The catalog pg\_constraint stores check, primary key, unique, foreign key, and exclusion constraints on tables. (Column constraints are not treated specially. Every column constraint is equivalent to some table constraint.) Not-null constraints are represented in the [pg\\_attribute](#page-3-0) catalog, not here.

User-defined constraint triggers (created with CREATE CONSTRAINT TRIGGER) also give rise to an entry in this table.

Check constraints on domains are stored here, too.

### **Table 52.13. pg\_constraint Columns**

## **Column Type**

#### **Description**

oid oid

Row identifier

conname name

Constraint name (not necessarily unique!)

connamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this constraint

contype char

c = check constraint, f = foreign key constraint, p = primary key constraint, u = unique constraint, t = constraint trigger, x = exclusion constraint

condeferrable bool

#### **Description**

Is the constraint deferrable?

condeferred bool

Is the constraint deferred by default?

convalidated bool

Has the constraint been validated? Currently, can be false only for foreign keys and CHECK constraints

conrelid oid (references [pg\\_class](#page-8-0).oid)

The table this constraint is on; zero if not a table constraint

contypid oid (references [pg\\_type](#page-45-0).oid)

The domain this constraint is on; zero if not a domain constraint

conindid oid (references [pg\\_class](#page-8-0).oid)

The index supporting this constraint, if it's a unique, primary key, foreign key, or exclusion constraint; else zero

conparentid oid (references [pg\\_constraint](#page-11-0).oid)

The corresponding constraint of the parent partitioned table, if this is a constraint on a partition; else zero

confrelid oid (references [pg\\_class](#page-8-0).oid)

If a foreign key, the referenced table; else zero

confupdtype char

Foreign key update action code: a = no action, r = restrict, c = cascade, n = set null, d = set default

confdeltype char

Foreign key deletion action code: a = no action, r = restrict, c = cascade, n = set null, d = set default

confmatchtype char

Foreign key match type: f = full, p = partial, s = simple

conislocal bool

This constraint is defined locally for the relation. Note that a constraint can be locally defined and inherited simultaneously.

coninhcount int4

The number of direct inheritance ancestors this constraint has. A constraint with a nonzero number of ancestors cannot be dropped nor renamed.

connoinherit bool

This constraint is defined locally for the relation. It is a non-inheritable constraint.

conkey int2[] (references [pg\\_attribute](#page-3-0).attnum)

If a table constraint (including foreign keys, but not constraint triggers), list of the constrained columns

confkey int2[] (references [pg\\_attribute](#page-3-0).attnum)

If a foreign key, list of the referenced columns

conpfeqop oid[] (references [pg\\_operator](#page-26-0).oid)

If a foreign key, list of the equality operators for PK = FK comparisons

conppeqop oid[] (references [pg\\_operator](#page-26-0).oid)

If a foreign key, list of the equality operators for PK = PK comparisons

conffeqop oid[] (references [pg\\_operator](#page-26-0).oid)

If a foreign key, list of the equality operators for FK = FK comparisons

conexclop oid[] (references [pg\\_operator](#page-26-0).oid)

If an exclusion constraint, list of the per-column exclusion operators

conbin pg\_node\_tree

If a check constraint, an internal representation of the expression. (It's recommended to use pg\_get\_constraintdef() to extract the definition of a check constraint.)

In the case of an exclusion constraint, conkey is only useful for constraint elements that are simple column references. For other cases, a zero appears in conkey and the associated index must be consulted to discover the expression that is constrained. (conkey thus has the same contents as [pg\\_in](#page-21-0)[dex](#page-21-0).indkey for the index.)

## **Note**

pg\_class.relchecks needs to agree with the number of check-constraint entries found in this table for each relation.