---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_default\_acl stores initial privileges to be assigned to newly created objects.

### **Table 52.17. pg\_default\_acl Columns**

| Column Type<br>Description                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------------------------|
| oid oid<br>Row identifier                                                                                                               |
| defaclrole oid (references pg_authid.oid)<br>The OID of the role associated with this entry                                             |
| defaclnamespace oid (references pg_namespace.oid)<br>The OID of the namespace associated with this entry, or zero if none               |
| defaclobjtype char<br>Type of object this entry is for: r = relation (table, view), S = sequence, f = function, T<br>= type, n = schema |
| defaclacl aclitem[]<br>Access privileges that this type of object should have on creation                                               |

A pg\_default\_acl entry shows the initial privileges to be assigned to an object belonging to the indicated user. There are currently two types of entry: "global" entries with defaclnamespace = zero, and "per-schema" entries that reference a particular schema. If a global entry is present then it *overrides* the normal hard-wired default privileges for the object type. A per-schema entry, if present, represents privileges to be *added to* the global or hard-wired default privileges.

Note that when an ACL entry in another catalog is null, it is taken to represent the hard-wired default privileges for its object, *not* whatever might be in pg\_default\_acl at the moment. pg\_default\_acl is only consulted during object creation.

# <span id="page-15-0"></span>**52.18. pg\_depend**

The catalog pg\_depend records the dependency relationships between database objects. This information allows DROP commands to find which other objects must be dropped by DROP CASCADE or prevent dropping in the DROP RESTRICT case.

See also [pg\\_shdepend](#page-35-0), which performs a similar function for dependencies involving objects that are shared across a database cluster.

### **Table 52.18. pg\_depend Columns**

```
Column Type
       Description
classid oid (references pg_class.oid)
```

#### **Description**

The OID of the system catalog the dependent object is in, or zero for a DEPENDEN-CY\_PIN entry

objid oid (references any OID column)

The OID of the specific dependent object, or zero for a DEPENDENCY\_PIN entry

objsubid int4

For a table column, this is the column number (the objid and classid refer to the table itself). For all other object types, this column is zero.

refclassid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog the referenced object is in

refobjid oid (references any OID column)

The OID of the specific referenced object

refobjsubid int4

For a table column, this is the column number (the refobjid and refclassid refer to the table itself). For all other object types, this column is zero.

deptype char

A code defining the specific semantics of this dependency relationship; see text

In all cases, a pg\_depend entry indicates that the referenced object cannot be dropped without also dropping the dependent object. However, there are several subflavors identified by deptype:

```
DEPENDENCY_NORMAL (n)
```

A normal relationship between separately-created objects. The dependent object can be dropped without affecting the referenced object. The referenced object can only be dropped by specifying CASCADE, in which case the dependent object is dropped, too. Example: a table column has a normal dependency on its data type.

```
DEPENDENCY_AUTO (a)
```

The dependent object can be dropped separately from the referenced object, and should be automatically dropped (regardless of RESTRICT or CASCADE mode) if the referenced object is dropped. Example: a named constraint on a table is made auto-dependent on the table, so that it will go away if the table is dropped.

```
DEPENDENCY_INTERNAL (i)
```

The dependent object was created as part of creation of the referenced object, and is really just a part of its internal implementation. A direct DROP of the dependent object will be disallowed outright (we'll tell the user to issue a DROP against the referenced object, instead). A DROP of the referenced object will result in automatically dropping the dependent object whether CASCADE is specified or not. If the dependent object has to be dropped due to a dependency on some other object being removed, its drop is converted to a drop of the referenced object, so that NORMAL and AUTO dependencies of the dependent object behave much like they were dependencies of the referenced object. Example: a view's ON SELECT rule is made internally dependent on the view, preventing it from being dropped while the view remains. Dependencies of the rule (such as tables it refers to) act as if they were dependencies of the view.

```
DEPENDENCY_PARTITION_PRI (P)
DEPENDENCY_PARTITION_SEC (S)
```

The dependent object was created as part of creation of the referenced object, and is really just a part of its internal implementation; however, unlike INTERNAL, there is more than one such referenced object. The dependent object must not be dropped unless at least one of these referenced objects is dropped; if any one is, the dependent object should be dropped whether or not CASCADE is specified. Also unlike INTERNAL, a drop of some other object that the dependent object depends on does not result in automatic deletion of any partition-referenced object. Hence, if the drop does not cascade to at least one of these objects via some other path, it will be refused. (In most cases, the dependent object shares all its non-partition dependencies with at least one partition-referenced object, so that this restriction does not result in blocking any cascaded delete.) Primary and secondary partition dependencies behave identically except that the primary dependency is preferred for use in error messages; hence, a partition-dependent object should have one primary partition dependency and one or more secondary partition dependencies. Note that partition dependencies are made in addition to, not instead of, any dependencies the object would normally have. This simplifies ATTACH/DETACH PARTITION operations: the partition dependencies need only be added or removed. Example: a child partitioned index is made partition-dependent on both the partition table it is on and the parent partitioned index, so that it goes away if either of those is dropped, but not otherwise. The dependency on the parent index is primary, so that if the user tries to drop the child partitioned index, the error message will suggest dropping the parent index instead (not the table).

#### DEPENDENCY\_EXTENSION (e)

The dependent object is a member of the *extension* that is the referenced object (see [pg\\_exten](#page-19-0)[sion](#page-19-0)). The dependent object can be dropped only via DROP EXTENSION on the referenced object. Functionally this dependency type acts the same as an INTERNAL dependency, but it's kept separate for clarity and to simplify pg\_dump.

```
DEPENDENCY_AUTO_EXTENSION (x)
```

The dependent object is not a member of the extension that is the referenced object (and so it should not be ignored by pg\_dump), but it cannot function without the extension and should be auto-dropped if the extension is. The dependent object may be dropped on its own as well. Functionally this dependency type acts the same as an AUTO dependency, but it's kept separate for clarity and to simplify pg\_dump.

```
DEPENDENCY_PIN (p)
```

There is no dependent object; this type of entry is a signal that the system itself depends on the referenced object, and so that object must never be deleted. Entries of this type are created only by initdb. The columns for the dependent object contain zeroes.

Other dependency flavors might be needed in future.

Note that it's quite possible for two objects to be linked by more than one pg\_depend entry. For example, a child partitioned index would have both a partition-type dependency on its associated partition table, and an auto dependency on each column of that table that it indexes. This sort of situation expresses the union of multiple dependency semantics. A dependent object can be dropped without CASCADE if any of its dependencies satisfies its condition for automatic dropping. Conversely, all the dependencies' restrictions about which objects must be dropped together must be satisfied.

# <span id="page-17-0"></span>**52.19. pg\_description**

The catalog pg\_description stores optional descriptions (comments) for each database object. Descriptions can be manipulated with the COMMENT command and viewed with psql's \d commands. Descriptions of many built-in system objects are provided in the initial contents of pg\_description.

See also [pg\\_shdescription](#page-36-0), which performs a similar function for descriptions involving objects that are shared across a database cluster.

### **Table 52.19. pg\_description Columns**

### **Column Type Description**

objoid oid (references any OID column)

#### **Description**

The OID of the object this description pertains to

classoid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog this object appears in

objsubid int4

For a comment on a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero.

description text

Arbitrary text that serves as the description of this object