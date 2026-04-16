---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_init\_privs records information about the initial privileges of objects in the system. There is one entry for each object in the database which has a non-default (non-NULL) initial set of privileges.

Objects can have initial privileges either by having those privileges set when the system is initialized (by initdb) or when the object is created during a CREATE EXTENSION and the extension script sets initial privileges using the GRANT system. Note that the system will automatically handle recording of the privileges during the extension script and that extension authors need only use the GRANT and REVOKE statements in their script to have the privileges recorded. The privtype column indicates if the initial privilege was set by initdb or during a CREATE EXTENSION command.

Objects which have initial privileges set by initdb will have entries where privtype is 'i', while objects which have initial privileges set by CREATE EXTENSION will have entries where privtype is 'e'.

### **Table 52.28. pg\_init\_privs Columns**

#### **Column Type**

#### **Description**

objoid oid (references any OID column)

The OID of the specific object

classoid oid (references [pg\\_class](#page-8-0).oid)

The OID of the system catalog the object is in

objsubid int4

For a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero.

privtype char

A code defining the type of initial privilege of this object; see text

initprivs aclitem[]

The initial access privileges; see Section 5.7 for details

# <span id="page-23-0"></span>**52.29. pg\_language**

The catalog pg\_language registers languages in which you can write functions or stored procedures. See CREATE LANGUAGE and Chapter 42 for more information about language handlers.

### **Table 52.29. pg\_language Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

lanname name

#### **Description**

Name of the language

lanowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the language

#### lanispl bool

This is false for internal languages (such as SQL) and true for user-defined languages. Currently, pg\_dump still uses this to determine which languages need to be dumped, but this might be replaced by a different mechanism in the future.

#### lanpltrusted bool

True if this is a trusted language, which means that it is believed not to grant access to anything outside the normal SQL execution environment. Only superusers can create functions in untrusted languages.

#### lanplcallfoid oid (references [pg\\_proc](#page-29-0).oid)

For noninternal languages this references the language handler, which is a special function that is responsible for executing all functions that are written in the particular language. Zero for internal languages.

#### laninline oid (references [pg\\_proc](#page-29-0).oid)

This references a function that is responsible for executing "inline" anonymous code blocks (DO blocks). Zero if inline blocks are not supported.

#### lanvalidator oid (references [pg\\_proc](#page-29-0).oid)

This references a language validator function that is responsible for checking the syntax and validity of new functions when they are created. Zero if no validator is provided.

lanacl aclitem[]

Access privileges; see Section 5.7 for details

# <span id="page-24-0"></span>**52.30. pg\_largeobject**

The catalog pg\_largeobject holds the data making up "large objects". A large object is identified by an OID assigned when it is created. Each large object is broken into segments or "pages" small enough to be conveniently stored as rows in pg\_largeobject. The amount of data per page is defined to be LOBLKSIZE (which is currently BLCKSZ/4, or typically 2 kB).

Prior to PostgreSQL 9.0, there was no permission structure associated with large objects. As a result, pg\_largeobject was publicly readable and could be used to obtain the OIDs (and contents) of all large objects in the system. This is no longer the case; use [pg\\_largeobject\\_metadata](#page-25-2) to obtain a list of large object OIDs.

### **Table 52.30. pg\_largeobject Columns**

#### **Column Type**

#### **Description**

loid oid (references [pg\\_largeobject\\_metadata](#page-25-2).oid)

Identifier of the large object that includes this page

pageno int4

Page number of this page within its large object (counting from zero)

data bytea

Actual data stored in the large object. This will never be more than LOBLKSIZE bytes and might be less.

Each row of pg\_largeobject holds data for one page of a large object, beginning at byte offset (pageno \* LOBLKSIZE) within the object. The implementation allows sparse storage: pages might be missing, and might be shorter than LOBLKSIZE bytes even if they are not the last page of the object. Missing regions within a large object read as zeroes.

# <span id="page-25-2"></span>**52.31. pg\_largeobject\_metadata**

The catalog pg\_largeobject\_metadata holds metadata associated with large objects. The actual large object data is stored in [pg\\_largeobject](#page-24-0).

**Table 52.31. pg\_largeobject\_metadata Columns**

## **Column Type Description** oid oid Row identifier lomowner oid (references [pg\\_authid](#page-5-0).oid) Owner of the large object lomacl aclitem[] Access privileges; see Section 5.7 for details

# <span id="page-25-0"></span>**52.32. pg\_namespace**

The catalog pg\_namespace stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.

**Table 52.32. pg\_namespace Columns**

| Column Type<br>Description                                         |
|--------------------------------------------------------------------|
| oid oid<br>Row identifier                                          |
| nspname name<br>Name of the namespace                              |
| nspowner oid (references pg_authid.oid)<br>Owner of the namespace  |
| nspacl aclitem[]<br>Access privileges; see Section 5.7 for details |

# <span id="page-25-1"></span>**52.33. pg\_opclass**

The catalog pg\_opclass defines index access method operator classes. Each operator class defines semantics for index columns of a particular data type and a particular index access method. An operator class essentially specifies that a particular operator family is applicable to a particular indexable column data type. The set of operators from the family that are actually usable with the indexed column are whichever ones accept the column's data type as their left-hand input.

Operator classes are described at length in Section 38.16.

**Table 52.33. pg\_opclass Columns**

| Column Type<br>Description                                                        |
|-----------------------------------------------------------------------------------|
| oid oid<br>Row identifier                                                         |
| opcmethod oid (references pg_am.oid)<br>Index access method operator class is for |

opcname name

Name of this operator class

opcnamespace oid (references [pg\\_namespace](#page-25-0).oid)

Namespace of this operator class

opcowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the operator class

opcfamily oid (references [pg\\_opfamily](#page-27-0).oid)

Operator family containing the operator class

opcintype oid (references [pg\\_type](#page-45-0).oid)

Data type that the operator class indexes

opcdefault bool

True if this operator class is the default for opcintype

opckeytype oid (references [pg\\_type](#page-45-0).oid)

Type of data stored in index, or zero if same as opcintype

An operator class's opcmethod must match the opfmethod of its containing operator family. Also, there must be no more than one pg\_opclass row having opcdefault true for any given combination of opcmethod and opcintype.

# <span id="page-26-0"></span>**52.34. pg\_operator**

The catalog pg\_operator stores information about operators. See CREATE OPERATOR and Section 38.14 for more information.

### **Table 52.34. pg\_operator Columns**

#### **Column Type Description**

oid oid

Row identifier

oprname name

Name of the operator

oprnamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this operator

oprowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the operator

oprkind char

b = infix operator ("both"), or l = prefix operator ("left")

oprcanmerge bool

This operator supports merge joins

oprcanhash bool

This operator supports hash joins

oprleft oid (references [pg\\_type](#page-45-0).oid)

Type of the left operand (zero for a prefix operator)

oprright oid (references [pg\\_type](#page-45-0).oid)

Type of the right operand

oprresult oid (references [pg\\_type](#page-45-0).oid)

Type of the result (zero for a not-yet-defined "shell" operator)

oprcom oid (references [pg\\_operator](#page-26-0).oid)

Commutator of this operator (zero if none)

oprnegate oid (references [pg\\_operator](#page-26-0).oid)

Negator of this operator (zero if none)

oprcode regproc (references [pg\\_proc](#page-29-0).oid)

Function that implements this operator (zero for a not-yet-defined "shell" operator)

oprrest regproc (references [pg\\_proc](#page-29-0).oid)

Restriction selectivity estimation function for this operator (zero if none)

oprjoin regproc (references [pg\\_proc](#page-29-0).oid)

Join selectivity estimation function for this operator (zero if none)

# <span id="page-27-0"></span>**52.35. pg\_opfamily**

The catalog pg\_opfamily defines operator families. Each operator family is a collection of operators and associated support routines that implement the semantics specified for a particular index access method. Furthermore, the operators in a family are all "compatible", in a way that is specified by the access method. The operator family concept allows cross-data-type operators to be used with indexes and to be reasoned about using knowledge of access method semantics.

Operator families are described at length in Section 38.16.

### **Table 52.35. pg\_opfamily Columns**

### **Column Type Description**

oid oid

Row identifier

opfmethod oid (references [pg\\_am](#page-1-0).oid)

Index access method operator family is for

opfname name

Name of this operator family

opfnamespace oid (references [pg\\_namespace](#page-25-0).oid)

Namespace of this operator family

opfowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the operator family

The majority of the information defining an operator family is not in its pg\_opfamily row, but in the associated rows in [pg\\_amop](#page-2-0), [pg\\_amproc](#page-3-2), and [pg\\_opclass](#page-25-1).