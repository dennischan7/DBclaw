---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_transform stores information about transforms, which are a mechanism to adapt data types to procedural languages. See CREATE TRANSFORM for more information.

### **Table 52.55. pg\_transform Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

trftype oid (references [pg\\_type](#page-45-0).oid)

OID of the data type this transform is for

trflang oid (references [pg\\_language](#page-23-0).oid)

OID of the language this transform is for

trffromsql regproc (references [pg\\_proc](#page-29-0).oid)

The OID of the function to use when converting the data type for input to the procedural language (e.g., function parameters). Zero is stored if the default behavior should be used.

trftosql regproc (references [pg\\_proc](#page-29-0).oid)

#### **Description**

The OID of the function to use when converting output from the procedural language (e.g., return values) to the data type. Zero is stored if the default behavior should be used.

# <span id="page-42-0"></span>**52.56. pg\_trigger**

The catalog pg\_trigger stores triggers on tables and views. See CREATE TRIGGER for more information.

### **Table 52.56. pg\_trigger Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

tgrelid oid (references [pg\\_class](#page-8-0).oid)

The table this trigger is on

tgparentid oid (references [pg\\_trigger](#page-42-0).oid)

Parent trigger that this trigger is cloned from (this happens when partitions are created or attached to a partitioned table); zero if not a clone

tgname name

Trigger name (must be unique among triggers of same table)

tgfoid oid (references [pg\\_proc](#page-29-0).oid)

The function to be called

tgtype int2

Bit mask identifying trigger firing conditions

tgenabled char

Controls in which session\_replication\_role modes the trigger fires. O = trigger fires in "origin" and "local" modes, D = trigger is disabled, R = trigger fires in "replica" mode, A = trigger fires always.

tgisinternal bool

True if trigger is internally generated (usually, to enforce the constraint identified by tgconstraint)

tgconstrrelid oid (references [pg\\_class](#page-8-0).oid)

The table referenced by a referential integrity constraint (zero if trigger is not for a referential integrity constraint)

tgconstrindid oid (references [pg\\_class](#page-8-0).oid)

The index supporting a unique, primary key, referential integrity, or exclusion constraint (zero if trigger is not for one of these types of constraint)

tgconstraint oid (references [pg\\_constraint](#page-11-0).oid)

The [pg\\_constraint](#page-11-0) entry associated with the trigger (zero if trigger is not for a constraint)

tgdeferrable bool

True if constraint trigger is deferrable

tginitdeferred bool

True if constraint trigger is initially deferred

tgnargs int2

Number of argument strings passed to trigger function

tgattr int2vector (references [pg\\_attribute](#page-3-0).attnum)

Column numbers, if trigger is column-specific; otherwise an empty array

tgargs bytea

Argument strings to pass to trigger, each NULL-terminated

tgqual pg\_node\_tree

Expression tree (in nodeToString() representation) for the trigger's WHEN condition, or null if none

tgoldtable name

REFERENCING clause name for OLD TABLE, or null if none

tgnewtable name

REFERENCING clause name for NEW TABLE, or null if none

Currently, column-specific triggering is supported only for UPDATE events, and so tgattr is relevant only for that event type. tgtype might contain bits for other event types as well, but those are presumed to be table-wide regardless of what is in tgattr.

## **Note**

When tgconstraint is nonzero, tgconstrrelid, tgconstrindid, tgdeferrable, and tginitdeferred are largely redundant with the referenced [pg\\_con](#page-11-0)[straint](#page-11-0) entry. However, it is possible for a non-deferrable trigger to be associated with a deferrable constraint: foreign key constraints can have some deferrable and some non-deferrable triggers.

## **Note**

pg\_class.relhastriggers must be true if a relation has any triggers in this catalog.

# <span id="page-43-0"></span>**52.57. pg\_ts\_config**

The pg\_ts\_config catalog contains entries representing text search configurations. A configuration specifies a particular text search parser and a list of dictionaries to use for each of the parser's output token types. The parser is shown in the pg\_ts\_config entry, but the token-to-dictionary mapping is defined by subsidiary entries in [pg\\_ts\\_config\\_map](#page-44-0).

PostgreSQL's text search features are described at length in Chapter 12.

### **Table 52.57. pg\_ts\_config Columns**

### **Column Type Description** oid oid Row identifier cfgname name Text search configuration name cfgnamespace oid (references [pg\\_namespace](#page-25-0).oid) The OID of the namespace that contains this configuration cfgowner oid (references [pg\\_authid](#page-5-0).oid) Owner of the configuration cfgparser oid (references [pg\\_ts\\_parser](#page-44-1).oid) The OID of the text search parser for this configuration

# <span id="page-44-0"></span>**52.58. pg\_ts\_config\_map**

The pg\_ts\_config\_map catalog contains entries showing which text search dictionaries should be consulted, and in what order, for each output token type of each text search configuration's parser.

PostgreSQL's text search features are described at length in Chapter 12.

### **Table 52.58. pg\_ts\_config\_map Columns**

```
Column Type
       Description
mapcfg oid (references pg_ts_config.oid)
       The OID of the pg_ts_config entry owning this map entry
maptokentype int4
       A token type emitted by the configuration's parser
mapseqno int4
       Order in which to consult this entry (lower mapseqnos first)
mapdict oid (references pg_ts_dict.oid)
       The OID of the text search dictionary to consult
```

# <span id="page-44-2"></span>**52.59. pg\_ts\_dict**

The pg\_ts\_dict catalog contains entries defining text search dictionaries. A dictionary depends on a text search template, which specifies all the implementation functions needed; the dictionary itself provides values for the user-settable parameters supported by the template. This division of labor allows dictionaries to be created by unprivileged users. The parameters are specified by a text string dictinitoption, whose format and meaning vary depending on the template.

PostgreSQL's text search features are described at length in Chapter 12.

### **Table 52.59. pg\_ts\_dict Columns**

```
Column Type
       Description
oid oid
       Row identifier
dictname name
       Text search dictionary name
dictnamespace oid (references pg_namespace.oid)
       The OID of the namespace that contains this dictionary
dictowner oid (references pg_authid.oid)
       Owner of the dictionary
dicttemplate oid (references pg_ts_template.oid)
       The OID of the text search template for this dictionary
dictinitoption text
       Initialization option string for the template
```

# <span id="page-44-1"></span>**52.60. pg\_ts\_parser**

The pg\_ts\_parser catalog contains entries defining text search parsers. A parser is responsible for splitting input text into lexemes and assigning a token type to each lexeme. Since a parser must be implemented by C-language-level functions, creation of new parsers is restricted to database superusers. PostgreSQL's text search features are described at length in Chapter 12.

### **Table 52.60. pg\_ts\_parser Columns**

| Column Type<br>Description                                                                           |
|------------------------------------------------------------------------------------------------------|
| oid oid<br>Row identifier                                                                            |
| prsname name<br>Text search parser name                                                              |
| prsnamespace oid (references pg_namespace.oid)<br>The OID of the namespace that contains this parser |
| prsstart regproc (references pg_proc.oid)<br>OID of the parser's startup function                    |
| prstoken regproc (references pg_proc.oid)<br>OID of the parser's next-token function                 |
| prsend regproc (references pg_proc.oid)<br>OID of the parser's shutdown function                     |
| prsheadline regproc (references pg_proc.oid)<br>OID of the parser's headline function (zero if none) |
| prslextype regproc (references pg_proc.oid)<br>OID of the parser's lextype function                  |

# <span id="page-45-1"></span>**52.61. pg\_ts\_template**

The pg\_ts\_template catalog contains entries defining text search templates. A template is the implementation skeleton for a class of text search dictionaries. Since a template must be implemented by C-language-level functions, creation of new templates is restricted to database superusers.

PostgreSQL's text search features are described at length in Chapter 12.

### **Table 52.61. pg\_ts\_template Columns**

| Column Type<br>Description                                                                                |
|-----------------------------------------------------------------------------------------------------------|
| oid oid<br>Row identifier                                                                                 |
| tmplname name<br>Text search template name                                                                |
| tmplnamespace oid (references pg_namespace.oid)<br>The OID of the namespace that contains this template   |
| tmplinit regproc (references pg_proc.oid)<br>OID of the template's initialization function (zero if none) |
| tmpllexize regproc (references pg_proc.oid)<br>OID of the template's lexize function                      |

# <span id="page-45-0"></span>**52.62. pg\_type**

The catalog pg\_type stores information about data types. Base types and enum types (scalar types) are created with CREATE TYPE, and domains with CREATE DOMAIN. A composite type is automatically created for each table in the database, to represent the row structure of the table. It is also possible to create composite types with CREATE TYPE AS.

### **Table 52.62. pg\_type Columns**

### **Column Type Description**

oid oid

Row identifier

typname name

Data type name

typnamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this type

typowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the type

#### typlen int2

For a fixed-size type, typlen is the number of bytes in the internal representation of the type. But for a variable-length type, typlen is negative. -1 indicates a "varlena" type (one that has a length word), -2 indicates a null-terminated C string.

#### typbyval bool

typbyval determines whether internal routines pass a value of this type by value or by reference. typbyval had better be false if typlen is not 1, 2, or 4 (or 8 on machines where Datum is 8 bytes). Variable-length types are always passed by reference. Note that typbyval can be false even if the length would allow pass-by-value.

#### typtype char

typtype is b for a base type, c for a composite type (e.g., a table's row type), d for a domain, e for an enum type, p for a pseudo-type, r for a range type, or m for a multirange type. See also typrelid and typbasetype.

#### typcategory char

typcategory is an arbitrary classification of data types that is used by the parser to determine which implicit casts should be "preferred". See [Table 52.63.](#page-48-0)

#### typispreferred bool

True if the type is a preferred cast target within its typcategory

#### typisdefined bool

True if the type is defined, false if this is a placeholder entry for a not-yet-defined type. When typisdefined is false, nothing except the type name, namespace, and OID can be relied on.

#### typdelim char

Character that separates two values of this type when parsing array input. Note that the delimiter is associated with the array element data type, not the array data type.

### typrelid oid (references [pg\\_class](#page-8-0).oid)

If this is a composite type (see typtype), then this column points to the [pg\\_class](#page-8-0) entry that defines the corresponding table. (For a free-standing composite type, the [pg\\_class](#page-8-0) entry doesn't really represent a table, but it is needed anyway for the type's [pg\\_attribute](#page-3-0) entries to link to.) Zero for non-composite types.

#### typsubscript regproc (references [pg\\_proc](#page-29-0).oid)

Subscripting handler function's OID, or zero if this type doesn't support subscripting. Types that are "true" array types have typsubscript = array\_subscript\_handler, but other types may have other handler functions to implement specialized subscripting behavior.

#### typelem oid (references [pg\\_type](#page-45-0).oid)

If typelem is not zero then it identifies another row in pg\_type, defining the type yielded by subscripting. This should be zero if typsubscript is zero. However, it can be zero when typsubscript isn't zero, if the handler doesn't need typelem to determine the subscripting result type. Note that a typelem dependency is considered to

#### **Description**

imply physical containment of the element type in this type; so DDL changes on the element type might be restricted by the presence of this type.

typarray oid (references [pg\\_type](#page-45-0).oid)

If typarray is not zero then it identifies another row in pg\_type, which is the "true" array type having this type as element

typinput regproc (references [pg\\_proc](#page-29-0).oid)

Input conversion function (text format)

typoutput regproc (references [pg\\_proc](#page-29-0).oid)

Output conversion function (text format)

typreceive regproc (references [pg\\_proc](#page-29-0).oid)

Input conversion function (binary format), or zero if none

typsend regproc (references [pg\\_proc](#page-29-0).oid)

Output conversion function (binary format), or zero if none

typmodin regproc (references [pg\\_proc](#page-29-0).oid)

Type modifier input function, or zero if type does not support modifiers

typmodout regproc (references [pg\\_proc](#page-29-0).oid)

Type modifier output function, or zero to use the standard format

typanalyze regproc (references [pg\\_proc](#page-29-0).oid)

Custom ANALYZE function, or zero to use the standard function

#### typalign char

typalign is the alignment required when storing a value of this type. It applies to storage on disk as well as most representations of the value inside PostgreSQL. When multiple values are stored consecutively, such as in the representation of a complete row on disk, padding is inserted before a datum of this type so that it begins on the specified boundary. The alignment reference is the beginning of the first datum in the sequence. Possible values are:

- c = char alignment, i.e., no alignment needed.
- s = short alignment (2 bytes on most machines).
- i = int alignment (4 bytes on most machines).
- d = double alignment (8 bytes on many machines, but by no means all).

#### typstorage char

typstorage tells for varlena types (those with typlen = -1) if the type is prepared for toasting and what the default strategy for attributes of this type should be. Possible values are:

- p (plain): Values must always be stored plain (non-varlena types always use this value).
- e (external): Values can be stored in a secondary "TOAST" relation (if relation has one, see pg\_class.reltoastrelid).
- m (main): Values can be compressed and stored inline.
- x (extended): Values can be compressed and/or moved to a secondary relation.

x is the usual choice for toast-able types. Note that m values can also be moved out to secondary storage, but only as a last resort (e and x values are moved first).

typnotnull bool

typnotnull represents a not-null constraint on a type. Used for domains only.

#### typbasetype oid (references [pg\\_type](#page-45-0).oid)

If this is a domain (see typtype), then typbasetype identifies the type that this one is based on. Zero if this type is not a domain.

#### typtypmod int4

Domains use typtypmod to record the typmod to be applied to their base type (-1 if base type does not use a typmod). -1 if this type is not a domain.

#### typndims int4

typndims is the number of array dimensions for a domain over an array (that is, typbasetype is an array type). Zero for types other than domains over array types.

#### typcollation oid (references [pg\\_collation](#page-10-0).oid)

typcollation specifies the collation of the type. If the type does not support collations, this will be zero. A base type that supports collations will have a nonzero value here, typically DEFAULT\_COLLATION\_OID. A domain over a collatable type can have a collation OID different from its base type's, if one was specified for the domain.

#### typdefaultbin pg\_node\_tree

If typdefaultbin is not null, it is the nodeToString() representation of a default expression for the type. This is only used for domains.

#### typdefault text

typdefault is null if the type has no associated default value. If typdefaultbin is not null, typdefault must contain a human-readable version of the default expression represented by typdefaultbin. If typdefaultbin is null and typdefault is not, then typdefault is the external representation of the type's default value, which can be fed to the type's input converter to produce a constant.

#### typacl aclitem[]

Access privileges; see Section 5.7 for details

## **Note**

For fixed-width types used in system tables, it is critical that the size and alignment defined in pg\_type agree with the way that the compiler will lay out the column in a structure representing a table row.

[Table 52.63](#page-48-0) lists the system-defined values of typcategory. Any future additions to this list will also be upper-case ASCII letters. All other ASCII characters are reserved for user-defined categories.

<span id="page-48-0"></span>**Table 52.63. typcategory Codes**

| Code | Category              |
|------|-----------------------|
| A    | Array types           |
| B    | Boolean types         |
| C    | Composite types       |
| D    | Date/time types       |
| E    | Enum types            |
| G    | Geometric types       |
| I    | Network address types |
| N    | Numeric types         |
| P    | Pseudo-types          |

| Code | Category           |
|------|--------------------|
| R    | Range types        |
| S    | String types       |
| T    | Timespan types     |
| U    | User-defined types |
| V    | Bit-string types   |
| X    | unknown type       |

# <span id="page-49-1"></span>**52.63. pg\_user\_mapping**

The catalog pg\_user\_mapping stores the mappings from local user to remote. Access to this catalog is restricted from normal users, use the view [pg\\_user\\_mappings](#page-74-0) instead.

**Table 52.64. pg\_user\_mapping Columns**

| Column Type<br>Description                                                                                         |  |
|--------------------------------------------------------------------------------------------------------------------|--|
| oid oid<br>Row identifier                                                                                          |  |
| umuser oid (references pg_authid.oid)<br>OID of the local role being mapped, or zero if the user mapping is public |  |
| umserver oid (references pg_foreign_server.oid)<br>The OID of the foreign server that contains this mapping        |  |
| umoptions text[]<br>User mapping specific options, as "keyword=value" strings                                      |  |