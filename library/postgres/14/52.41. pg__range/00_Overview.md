---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_range stores information about range types. This is in addition to the types' entries in [pg\\_type](#page-45-0).

### **Table 52.41. pg\_range Columns**

#### **Column Type**

#### **Description**

rngtypid oid (references [pg\\_type](#page-45-0).oid)

OID of the range type

rngsubtype oid (references [pg\\_type](#page-45-0).oid)

OID of the element type (subtype) of this range type

rngmultitypid oid (references [pg\\_type](#page-45-0).oid)

OID of the multirange type for this range type

rngcollation oid (references [pg\\_collation](#page-10-0).oid)

OID of the collation used for range comparisons, or zero if none

rngsubopc oid (references [pg\\_opclass](#page-25-1).oid)

OID of the subtype's operator class used for range comparisons

rngcanonical regproc (references [pg\\_proc](#page-29-0).oid)

OID of the function to convert a range value into canonical form, or zero if none

rngsubdiff regproc (references [pg\\_proc](#page-29-0).oid)

OID of the function to return the difference between two element values as double precision, or zero if none

rngsubopc (plus rngcollation, if the element type is collatable) determines the sort ordering used by the range type. rngcanonical is used when the element type is discrete. rngsubdiff is optional but should be supplied to improve performance of GiST indexes on the range type.

# <span id="page-33-1"></span>**52.42. pg\_replication\_origin**

The pg\_replication\_origin catalog contains all replication origins created. For more on replication origins see Chapter 50.

Unlike most system catalogs, pg\_replication\_origin is shared across all databases of a cluster: there is only one copy of pg\_replication\_origin per cluster, not one per database.

### **Table 52.42. pg\_replication\_origin Columns**

#### **Column Type**

**Description**

roident oid

A unique, cluster-wide identifier for the replication origin. Should never leave the system.

roname text

The external, user defined, name of a replication origin.

# <span id="page-33-0"></span>**52.43. pg\_rewrite**

The catalog pg\_rewrite stores rewrite rules for tables and views.

### **Table 52.43. pg\_rewrite Columns**

## **Column Type**

**Description**

oid oid

Row identifier

rulename name

Rule name

ev\_class oid (references [pg\\_class](#page-8-0).oid)

The table this rule is for

ev\_type char

Event type that the rule is for: 1 = SELECT, 2 = UPDATE, 3 = INSERT, 4 = DELETE

ev\_enabled char

Controls in which session\_replication\_role modes the rule fires. O = rule fires in "origin" and "local" modes, D = rule is disabled, R = rule fires in "replica" mode, A = rule fires always.

is\_instead bool

True if the rule is an INSTEAD rule

ev\_qual pg\_node\_tree

Expression tree (in the form of a nodeToString() representation) for the rule's qualifying condition

ev\_action pg\_node\_tree

Query tree (in the form of a nodeToString() representation) for the rule's action

## **Note**

pg\_class.relhasrules must be true if a table has any rules in this catalog.

# <span id="page-34-1"></span>**52.44. pg\_seclabel**

The catalog pg\_seclabel stores security labels on database objects. Security labels can be manipulated with the SECURITY LABEL command. For an easier way to view security labels, see [Sec](#page-63-0)[tion 52.84.](#page-63-0)

See also [pg\\_shseclabel](#page-36-1), which performs a similar function for security labels of database objects that are shared across a database cluster.

### **Table 52.44. pg\_seclabel Columns**

## **Column Type Description** objoid oid (references any OID column) The OID of the object this security label pertains to classoid oid (references [pg\\_class](#page-8-0).oid) The OID of the system catalog this object appears in objsubid int4 For a security label on a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero. provider text The label provider associated with this label. label text

# <span id="page-34-0"></span>**52.45. pg\_sequence**

The catalog pg\_sequence contains information about sequences. Some of the information about sequences, such as the name and the schema, is in [pg\\_class](#page-8-0)

### **Table 52.45. pg\_sequence Columns**

The security label applied to this object.

## **Column Type Description** seqrelid oid (references [pg\\_class](#page-8-0).oid) The OID of the [pg\\_class](#page-8-0) entry for this sequence seqtypid oid (references [pg\\_type](#page-45-0).oid) Data type of the sequence seqstart int8 Start value of the sequence seqincrement int8 Increment value of the sequence seqmax int8 Maximum value of the sequence seqmin int8

Minimum value of the sequence

seqcache int8

Cache size of the sequence

seqcycle bool

Whether the sequence cycles

# <span id="page-35-0"></span>**52.46. pg\_shdepend**

The catalog pg\_shdepend records the dependency relationships between database objects and shared objects, such as roles. This information allows PostgreSQL to ensure that those objects are unreferenced before attempting to delete them.

See also [pg\\_depend](#page-15-0), which performs a similar function for dependencies involving objects within a single database.

Unlike most system catalogs, pg\_shdepend is shared across all databases of a cluster: there is only one copy of pg\_shdepend per cluster, not one per database.

### **Table 52.46. pg\_shdepend Columns**

### **Column Type Description**

dbid oid (references [pg\\_database](#page-13-0).oid)

The OID of the database the dependent object is in, or zero for a shared object or a SHARED\_DEPENDENCY\_PIN entry

classid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog the dependent object is in, or zero for a SHARED\_DE-PENDENCY\_PIN entry

objid oid (references any OID column)

The OID of the specific dependent object, or zero for a SHARED\_DEPENDENCY\_PIN entry

objsubid int4

For a table column, this is the column number (the objid and classid refer to the table itself). For all other object types, this column is zero.

refclassid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog the referenced object is in (must be a shared catalog)

refobjid oid (references any OID column)

The OID of the specific referenced object

deptype char

A code defining the specific semantics of this dependency relationship; see text

In all cases, a pg\_shdepend entry indicates that the referenced object cannot be dropped without also dropping the dependent object. However, there are several subflavors identified by deptype:

```
SHARED_DEPENDENCY_OWNER (o)
```

The referenced object (which must be a role) is the owner of the dependent object.

```
SHARED_DEPENDENCY_ACL (a)
```

The referenced object (which must be a role) is mentioned in the ACL (access control list, i.e., privileges list) of the dependent object. (A SHARED\_DEPENDENCY\_ACL entry is not made for the owner of the object, since the owner will have a SHARED\_DEPENDENCY\_OWNER entry anyway.)

```
SHARED_DEPENDENCY_POLICY (r)
```

The referenced object (which must be a role) is mentioned as the target of a dependent policy object.

```
SHARED_DEPENDENCY_PIN (p)
```

There is no dependent object; this type of entry is a signal that the system itself depends on the referenced object, and so that object must never be deleted. Entries of this type are created only by initdb. The columns for the dependent object contain zeroes.

```
SHARED_DEPENDENCY_TABLESPACE (t)
```

The referenced object (which must be a tablespace) is mentioned as the tablespace for a relation that doesn't have storage.

Other dependency flavors might be needed in future. Note in particular that the current definition only supports roles and tablespaces as referenced objects.

# <span id="page-36-0"></span>**52.47. pg\_shdescription**

The catalog pg\_shdescription stores optional descriptions (comments) for shared database objects. Descriptions can be manipulated with the COMMENT command and viewed with psql's \d commands.

See also [pg\\_description](#page-17-0), which performs a similar function for descriptions involving objects within a single database.

Unlike most system catalogs, pg\_shdescription is shared across all databases of a cluster: there is only one copy of pg\_shdescription per cluster, not one per database.

### **Table 52.47. pg\_shdescription Columns**

### **Column Type Description**

objoid oid (references any OID column)

The OID of the object this description pertains to

classoid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog this object appears in

description text

Arbitrary text that serves as the description of this object

# <span id="page-36-1"></span>**52.48. pg\_shseclabel**

The catalog pg\_shseclabel stores security labels on shared database objects. Security labels can be manipulated with the SECURITY LABEL command. For an easier way to view security labels, see [Section 52.84](#page-63-0).

See also [pg\\_seclabel](#page-34-1), which performs a similar function for security labels involving objects within a single database.

Unlike most system catalogs, pg\_shseclabel is shared across all databases of a cluster: there is only one copy of pg\_shseclabel per cluster, not one per database.

## **Table 52.48. pg\_shseclabel Columns**

#### **Column Type Description**

objoid oid (references any OID column)

The OID of the object this security label pertains to

classoid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog this object appears in

provider text

The label provider associated with this label.

label text

The security label applied to this object.

# <span id="page-37-0"></span>**52.49. pg\_statistic**

The catalog pg\_statistic stores statistical data about the contents of the database. Entries are created by ANALYZE and subsequently used by the query planner. Note that all the statistical data is inherently approximate, even assuming that it is up-to-date.

Normally there is one entry, with stainherit = false, for each table column that has been analyzed. If the table has inheritance children, a second entry with stainherit = true is also created. This row represents the column's statistics over the inheritance tree, i.e., statistics for the data you'd see with SELECT column FROM table\*, whereas the stainherit = false row represents the results of SELECT column FROM ONLY table.

pg\_statistic also stores statistical data about the values of index expressions. These are described as if they were actual data columns; in particular, starelid references the index. No entry is made for an ordinary non-expression index column, however, since it would be redundant with the entry for the underlying table column. Currently, entries for index expressions always have stainherit = false.

Since different kinds of statistics might be appropriate for different kinds of data, pg\_statistic is designed not to assume very much about what sort of statistics it stores. Only extremely general statistics (such as nullness) are given dedicated columns in pg\_statistic. Everything else is stored in "slots", which are groups of associated columns whose content is identified by a code number in one of the slot's columns. For more information see src/include/catalog/pg\_statistic.h.

pg\_statistic should not be readable by the public, since even statistical information about a table's contents might be considered sensitive. (Example: minimum and maximum values of a salary column might be quite interesting.) [pg\\_stats](#page-68-0) is a publicly readable view on pg\_statistic that only exposes information about those tables that are readable by the current user.

### **Table 52.49. pg\_statistic Columns**

#### **Column Type Description**

starelid oid (references [pg\\_class](#page-8-0).oid)

The table or index that the described column belongs to

staattnum int2 (references [pg\\_attribute](#page-3-0).attnum)

The number of the described column

stainherit bool

If true, the stats include inheritance child columns, not just the values in the specified relation

stanullfrac float4

The fraction of the column's entries that are null

stawidth int4

#### **Description**

The average stored width, in bytes, of nonnull entries

#### stadistinct float4

The number of distinct nonnull data values in the column. A value greater than zero is the actual number of distinct values. A value less than zero is the negative of a multiplier for the number of rows in the table; for example, a column in which about 80% of the values are nonnull and each nonnull value appears about twice on average could be represented by stadistinct = -0.4. A zero value means the number of distinct values is unknown.

#### stakindN int2

A code number indicating the kind of statistics stored in the Nth "slot" of the pg\_statistic row.

#### staopN oid (references [pg\\_operator](#page-26-0).oid)

An operator used to derive the statistics stored in the Nth "slot". For example, a histogram slot would show the < operator that defines the sort order of the data. Zero if the statistics kind does not require an operator.

#### stacollN oid (references [pg\\_collation](#page-10-0).oid)

The collation used to derive the statistics stored in the Nth "slot". For example, a histogram slot for a collatable column would show the collation that defines the sort order of the data. Zero for noncollatable data.

#### stanumbersN float4[]

Numerical statistics of the appropriate kind for the Nth "slot", or null if the slot kind does not involve numerical values

#### stavaluesN anyarray

Column data values of the appropriate kind for the Nth "slot", or null if the slot kind does not store any data values. Each array's element values are actually of the specific column's data type, or a related type such as an array's element type, so there is no way to define these columns' type more specifically than anyarray.

# <span id="page-38-0"></span>**52.50. pg\_statistic\_ext**

The catalog pg\_statistic\_ext holds definitions of extended planner statistics. Each row in this catalog corresponds to a *statistics object* created with CREATE STATISTICS.

### **Table 52.50. pg\_statistic\_ext Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

stxrelid oid (references [pg\\_class](#page-8-0).oid)

Table containing the columns described by this object

stxname name

Name of the statistics object

stxnamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this statistics object

stxowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the statistics object

#### stxstattarget int4

stxstattarget controls the level of detail of statistics accumulated for this statistics object by ANALYZE. A zero value indicates that no statistics should be collected. A neg-

ative value says to use the maximum of the statistics targets of the referenced columns, if set, or the system default statistics target. Positive values of stxstattarget determine the target number of "most common values" to collect.

stxkeys int2vector (references [pg\\_attribute](#page-3-0).attnum)

An array of attribute numbers, indicating which table columns are covered by this statistics object; for example a value of 1 3 would mean that the first and the third table columns are covered

stxkind char[]

An array containing codes for the enabled statistics kinds; valid values are: d for n-distinct statistics, f for functional dependency statistics, m for most common values (MCV) list statistics, and e for expression statistics

stxexprs pg\_node\_tree

Expression trees (in nodeToString() representation) for statistics object attributes that are not simple column references. This is a list with one element per expression. Null if all statistics object attributes are simple references.

The pg\_statistic\_ext entry is filled in completely during CREATE STATISTICS, but the actual statistical values are not computed then. Subsequent ANALYZE commands compute the desired values and populate an entry in the [pg\\_statistic\\_ext\\_data](#page-39-0) catalog.

# <span id="page-39-0"></span>**52.51. pg\_statistic\_ext\_data**

The catalog pg\_statistic\_ext\_data holds data for extended planner statistics defined in [pg\\_statistic\\_ext](#page-38-0). Each row in this catalog corresponds to a *statistics object* created with CRE-ATE STATISTICS.

Like [pg\\_statistic](#page-37-0), pg\_statistic\_ext\_data should not be readable by the public, since the contents might be considered sensitive. (Example: most common combinations of values in columns might be quite interesting.) [pg\\_stats\\_ext](#page-69-0) is a publicly readable view on pg\_statistic\_ext\_data (after joining with [pg\\_statistic\\_ext](#page-38-0)) that only exposes information about tables the current user owns.

### **Table 52.51. pg\_statistic\_ext\_data Columns**

### **Column Type Description**

stxoid oid (references [pg\\_statistic\\_ext](#page-38-0).oid)

Extended statistics object containing the definition for this data

stxdndistinct pg\_ndistinct

N-distinct counts, serialized as pg\_ndistinct type

stxddependencies pg\_dependencies

Functional dependency statistics, serialized as pg\_dependencies type

stxdmcv pg\_mcv\_list

MCV (most-common values) list statistics, serialized as pg\_mcv\_list type

stxdexpr pg\_statistic[]

Per-expression statistics, serialized as an array of pg\_statistic type

# <span id="page-39-1"></span>**52.52. pg\_subscription**

The catalog pg\_subscription contains all existing logical replication subscriptions. For more information about logical replication see Chapter 31.

Unlike most system catalogs, pg\_subscription is shared across all databases of a cluster: there is only one copy of pg\_subscription per cluster, not one per database.

Access to the column subconninfo is revoked from normal users, because it could contain plaintext passwords.

### **Table 52.52. pg\_subscription Columns**

#### **Column Type**

**Description**

oid oid

Row identifier

subdbid oid (references [pg\\_database](#page-13-0).oid)

OID of the database that the subscription resides in

subname name

Name of the subscription

subowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the subscription

subenabled bool

If true, the subscription is enabled and should be replicating

subbinary bool

If true, the subscription will request that the publisher send data in binary format

substream bool

If true, the subscription will allow streaming of in-progress transactions

subconninfo text

Connection string to the upstream database

subslotname name

Name of the replication slot in the upstream database (also used for the local replication origin name); null represents NONE

subsynccommit text

The synchronous\_commit setting for the subscription's workers to use

subpublications text[]

Array of subscribed publication names. These reference publications defined in the upstream database. For more on publications see Section 31.1.