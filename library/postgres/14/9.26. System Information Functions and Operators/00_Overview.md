---
source: PostgreSQL 14 Reference
title: 00_Overview
---

[Table 9.65](#page-1-0) shows several functions that extract session and system information.

In addition to the functions listed in this section, there are a number of functions related to the statistics system that also provide system information. See Section 28.2.22 for more information.

### <span id="page-1-0"></span>**Table 9.65. Session Information Functions**

### **Function Description** current\_catalog → name current\_database () → name Returns the name of the current database. (Databases are called "catalogs" in the SQL standard, so current\_catalog is the standard's spelling.) current\_query () → text Returns the text of the currently executing query, as submitted by the client (which might contain more than one statement). current\_role → name This is equivalent to current\_user. current\_schema → name current\_schema () → name Returns the name of the schema that is first in the search path (or a null value if the search path is empty). This is the schema that will be used for any tables or other named objects that are created without specifying a target schema. current\_schemas ( include\_implicit boolean ) → name[] Returns an array of the names of all schemas presently in the effective search path, in their priority order. (Items in the current search\_path setting that do not correspond to existing, searchable schemas are omitted.) If the Boolean argument is true, then implicitly-searched system schemas such as pg\_catalog are included in the result. current\_user → name Returns the user name of the current execution context. inet\_client\_addr () → inet Returns the IP address of the current client, or NULL if the current connection is via a Unix-domain socket. inet\_client\_port () → integer

#### **Description**

Returns the IP port number of the current client, or NULL if the current connection is via a Unix-domain socket.

inet\_server\_addr () → inet

Returns the IP address on which the server accepted the current connection, or NULL if the current connection is via a Unix-domain socket.

inet\_server\_port () → integer

Returns the IP port number on which the server accepted the current connection, or NULL if the current connection is via a Unix-domain socket.

pg\_backend\_pid () → integer

Returns the process ID of the server process attached to the current session.

pg\_blocking\_pids ( integer ) → integer[]

Returns an array of the process ID(s) of the sessions that are blocking the server process with the specified process ID from acquiring a lock, or an empty array if there is no such server process or it is not blocked.

One server process blocks another if it either holds a lock that conflicts with the blocked process's lock request (hard block), or is waiting for a lock that would conflict with the blocked process's lock request and is ahead of it in the wait queue (soft block). When using parallel queries the result always lists client-visible process IDs (that is, pg\_backend\_pid results) even if the actual lock is held or awaited by a child worker process. As a result of that, there may be duplicated PIDs in the result. Also note that when a prepared transaction holds a conflicting lock, it will be represented by a zero process ID. Frequent calls to this function could have some impact on database performance, because it needs exclusive access to the lock manager's shared state for a short time.

pg\_conf\_load\_time () → timestamp with time zone

Returns the time when the server configuration files were last loaded. If the current session was alive at the time, this will be the time when the session itself re-read the configuration files (so the reading will vary a little in different sessions). Otherwise it is the time when the postmaster process re-read the configuration files.

pg\_current\_logfile ( [ text ] ) → text

Returns the path name of the log file currently in use by the logging collector. The path includes the log\_directory directory and the individual log file name. The result is NULL if the logging collector is disabled. When multiple log files exist, each in a different format, pg\_current\_logfile without an argument returns the path of the file having the first format found in the ordered list: stderr, csvlog. NULL is returned if no log file has any of these formats. To request information about a specific log file format, supply either csvlog or stderr as the value of the optional parameter. The result is NULL if the log format requested is not configured in log\_destination. The result reflects the contents of the current\_logfiles file.

pg\_my\_temp\_schema () → oid

Returns the OID of the current session's temporary schema, or zero if it has none (because it has not created any temporary tables).

pg\_is\_other\_temp\_schema ( oid ) → boolean

Returns true if the given OID is the OID of another session's temporary schema. (This can be useful, for example, to exclude other sessions' temporary tables from a catalog display.)

pg\_jit\_available () → boolean

Returns true if a JIT compiler extension is available (see Chapter 32) and the jit configuration parameter is set to on.

#### **Description**

pg\_listening\_channels () → setof text

Returns the set of names of asynchronous notification channels that the current session is listening to.

pg\_notification\_queue\_usage () → double precision

Returns the fraction (0–1) of the asynchronous notification queue's maximum size that is currently occupied by notifications that are waiting to be processed. See LISTEN and NOTIFY for more information.

pg\_postmaster\_start\_time () → timestamp with time zone Returns the time when the server started.

pg\_safe\_snapshot\_blocking\_pids ( integer ) → integer[]

Returns an array of the process ID(s) of the sessions that are blocking the server process with the specified process ID from acquiring a safe snapshot, or an empty array if there is no such server process or it is not blocked.

A session running a SERIALIZABLE transaction blocks a SERIALIZABLE READ ONLY DEFERRABLE transaction from acquiring a snapshot until the latter determines that it is safe to avoid taking any predicate locks. See [Section 13.2.3](#page-115-0) for more information about serializable and deferrable transactions.

Frequent calls to this function could have some impact on database performance, because it needs access to the predicate lock manager's shared state for a short time.

pg\_trigger\_depth () → integer

Returns the current nesting level of PostgreSQL triggers (0 if not called, directly or indirectly, from inside a trigger).

session\_user → name

Returns the session user's name.

user → name

This is equivalent to current\_user.

version () → text

Returns a string describing the PostgreSQL server's version. You can also get this information from server\_version, or for a machine-readable version use server\_version\_num. Software developers should use server\_version\_num (available since 8.2) or PQserverVersion instead of parsing the text version.

### **Note**

current\_catalog, current\_role, current\_schema, current\_user, session\_user, and user have special syntactic status in SQL: they must be called without trailing parentheses. In PostgreSQL, parentheses can optionally be used with current\_schema, but not with the others.

The session\_user is normally the user who initiated the current database connection; but superusers can change this setting with SET SESSION AUTHORIZATION. The current\_user is the user identifier that is applicable for permission checking. Normally it is equal to the session user, but it can be changed with SET ROLE. It also changes during the execution of functions with the attribute SECURITY DEFINER. In Unix parlance, the session user is the "real user" and the current user is the "effective user". current\_role and user are synonyms for current\_user. (The SQL standard draws a distinction between current\_role and current\_user, but PostgreSQL does not, since it unifies users and roles into a single kind of entity.)

[Table 9.66](#page-4-0) lists functions that allow querying object access privileges programmatically. (See Section 5.7 for more information about privileges.) In these functions, the user whose privileges are being inquired about can be specified by name or by OID (pg\_authid.oid), or if the name is given as public then the privileges of the PUBLIC pseudo-role are checked. Also, the user argument can be omitted entirely, in which case the current\_user is assumed. The object that is being inquired about can be specified either by name or by OID, too. When specifying by name, a schema name can be included if relevant. The access privilege of interest is specified by a text string, which must evaluate to one of the appropriate privilege keywords for the object's type (e.g., SELECT). Optionally, WITH GRANT OPTION can be added to a privilege type to test whether the privilege is held with grant option. Also, multiple privilege types can be listed separated by commas, in which case the result will be true if any of the listed privileges is held. (Case of the privilege string is not significant, and extra whitespace is allowed between but not within privilege names.) Some examples:

```
SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH
 GRANT OPTION');
```

### <span id="page-4-0"></span>**Table 9.66. Access Privilege Inquiry Functions**

### **Function**

#### **Description**

has\_any\_column\_privilege ( [ user name or oid, ] table text or oid, privilege text ) → boolean

Does user have privilege for any column of table? This succeeds either if the privilege is held for the whole table, or if there is a column-level grant of the privilege for at least one column. Allowable privilege types are SELECT, INSERT, UPDATE, and REFER-ENCES.

has\_column\_privilege ( [ user name or oid, ] table text or oid, column text or smallint, privilege text ) → boolean

Does user have privilege for the specified table column? This succeeds either if the privilege is held for the whole table, or if there is a column-level grant of the privilege for the column. The column can be specified by name or by attribute number (pg\_attribute.attnum). Allowable privilege types are SELECT, INSERT, UPDATE, and REFER-ENCES.

has\_database\_privilege ( [ user name or oid, ] database text or oid, privilege text ) → boolean

Does user have privilege for database? Allowable privilege types are CREATE, CON-NECT, TEMPORARY, and TEMP (which is equivalent to TEMPORARY).

has\_foreign\_data\_wrapper\_privilege ( [ user name or oid, ] fdw text or oid, privilege text ) → boolean

Does user have privilege for foreign-data wrapper? The only allowable privilege type is USAGE.

has\_function\_privilege ( [ user name or oid, ] function text or oid, privilege text ) → boolean

Does user have privilege for function? The only allowable privilege type is EXECUTE. When specifying a function by name rather than by OID, the allowed input is the same as for the regprocedure data type (see Section 8.19). An example is:

```
SELECT has_function_privilege('joeuser', 'myfunc(int,
 text)', 'execute');
```

has\_language\_privilege ( [ user name or oid, ] language text or oid, privilege text ) → boolean

#### **Description**

Does user have privilege for language? The only allowable privilege type is USAGE.

has\_schema\_privilege ( [ user name or oid, ] schema text or oid, privilege text ) → boolean

Does user have privilege for schema? Allowable privilege types are CREATE and USAGE.

has\_sequence\_privilege ( [ user name or oid, ] sequence text or oid, privilege text ) → boolean

Does user have privilege for sequence? Allowable privilege types are USAGE, SELECT, and UPDATE.

has\_server\_privilege ( [ user name or oid, ] server text or oid, privilege text ) → boolean

Does user have privilege for foreign server? The only allowable privilege type is USAGE.

has\_table\_privilege ( [ user name or oid, ] table text or oid, privilege text ) → boolean

Does user have privilege for table? Allowable privilege types are SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, and TRIGGER.

has\_tablespace\_privilege ( [ user name or oid, ] tablespace text or oid, privilege text ) → boolean

Does user have privilege for tablespace? The only allowable privilege type is CREATE.

has\_type\_privilege ( [ user name or oid, ] type text or oid, privilege text ) → boolean

Does user have privilege for data type? The only allowable privilege type is USAGE. When specifying a type by name rather than by OID, the allowed input is the same as for the regtype data type (see Section 8.19).

pg\_has\_role ( [ user name or oid, ] role text or oid, privilege text ) → boolean

Does user have privilege for role? Allowable privilege types are MEMBER and USAGE. MEMBER denotes direct or indirect membership in the role (that is, the right to do SET ROLE), while USAGE denotes whether the privileges of the role are immediately available without doing SET ROLE. WITH ADMIN OPTION or WITH GRANT OPTION can be added to either of these privilege types to test whether the ADMIN privilege is held (all four spellings test the same thing). This function does not allow the special case of setting user to public, because the PUBLIC pseudo-role can never be a member of real roles.

row\_security\_active ( table text or oid ) → boolean

Is row-level security active for the specified table in the context of the current user and current environment?

[Table 9.67](#page-5-0) shows the operators available for the aclitem type, which is the catalog representation of access privileges. See Section 5.7 for information about how to read access privilege values.

### <span id="page-5-0"></span>**Table 9.67. aclitem Operators**

#### **Operator**

**Description Example(s)**

aclitem = aclitem → boolean

### **Operator**

### **Description Example(s)**

Are aclitems equal? (Notice that type aclitem lacks the usual set of comparison operators; it has only equality. In turn, aclitem arrays can only be compared for equality.)

```
'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::a-
clitem → f
```

```
aclitem[] @> aclitem → boolean
```

Does array contain the specified privileges? (This is true if there is an array entry that matches the aclitem's grantee and grantor, and has at least the specified set of privileges.)

```
'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @>
'calvin=r*/hobbes'::aclitem → t
```

```
aclitem[] ~ aclitem → boolean
```

This is a deprecated alias for @>.

```
'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] ~
```

<span id="page-6-0"></span>[Table 9.68](#page-6-0) shows some additional functions to manage the aclitem type.

### **Table 9.68. aclitem Functions**

#### **Function**

#### **Description**

```
acldefault ( type "char", ownerId oid ) → aclitem[]
```

Constructs an aclitem array holding the default access privileges for an object of type type belonging to the role with OID ownerId. This represents the access privileges that will be assumed when an object's ACL entry is null. (The default access privileges are described in Section 5.7.) The type parameter must be one of 'c' for COLUMN, 'r' for TABLE and table-like objects, 's' for SEQUENCE, 'd' for DATABASE, 'f' for FUNC-TION or PROCEDURE, 'l' for LANGUAGE, 'L' for LARGE OBJECT, 'n' for SCHEMA, 't' for TABLESPACE, 'F' for FOREIGN DATA WRAPPER, 'S' for FOREIGN SERVER, or 'T' for TYPE or DOMAIN.

```
aclexplode ( aclitem[] ) → setof record ( grantor oid, grantee oid, priv-
      ilege_type text, is_grantable boolean )
```

Returns the aclitem array as a set of rows. If the grantee is the pseudo-role PUBLIC, it is represented by zero in the grantee column. Each granted privilege is represented as SELECT, INSERT, etc. Note that each privilege is broken out as a separate row, so only one keyword appears in the privilege\_type column.

```
makeaclitem ( grantee oid, grantor oid, privileges text, is_grantable
      boolean ) → aclitem
      Constructs an aclitem with the given properties.
```

[Table 9.69](#page-7-0) shows functions that determine whether a certain object is *visible* in the current schema search path. For example, a table is said to be visible if its containing schema is in the search path and no table of the same name appears earlier in the search path. This is equivalent to the statement that the table can be referenced by name without explicit schema qualification. Thus, to list the names of all visible tables:

```
SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

<sup>&#</sup>x27;calvin=r\*/hobbes'::aclitem → t

For functions and operators, an object in the search path is said to be visible if there is no object of the same name *and argument data type(s)* earlier in the path. For operator classes and families, both the name and the associated index access method are considered.

### <span id="page-7-0"></span>**Table 9.69. Schema Visibility Inquiry Functions**

```
Function
       Description
pg_collation_is_visible ( collation oid ) → boolean
       Is collation visible in search path?
pg_conversion_is_visible ( conversion oid ) → boolean
       Is conversion visible in search path?
pg_function_is_visible ( function oid ) → boolean
       Is function visible in search path? (This also works for procedures and aggregates.)
pg_opclass_is_visible ( opclass oid ) → boolean
       Is operator class visible in search path?
pg_operator_is_visible ( operator oid ) → boolean
       Is operator visible in search path?
pg_opfamily_is_visible ( opclass oid ) → boolean
       Is operator family visible in search path?
pg_statistics_obj_is_visible ( stat oid ) → boolean
       Is statistics object visible in search path?
pg_table_is_visible ( table oid ) → boolean
       Is table visible in search path? (This works for all types of relations, including views, ma-
       terialized views, indexes, sequences and foreign tables.)
pg_ts_config_is_visible ( config oid ) → boolean
       Is text search configuration visible in search path?
pg_ts_dict_is_visible ( dict oid ) → boolean
       Is text search dictionary visible in search path?
pg_ts_parser_is_visible ( parser oid ) → boolean
       Is text search parser visible in search path?
pg_ts_template_is_visible ( template oid ) → boolean
       Is text search template visible in search path?
pg_type_is_visible ( type oid ) → boolean
       Is type (or domain) visible in search path?
```

All these functions require object OIDs to identify the object to be checked. If you want to test an object by name, it is convenient to use the OID alias types (regclass, regtype, regprocedure, regoperator, regconfig, or regdictionary), for example:

```
SELECT pg_type_is_visible('myschema.widget'::regtype);
```

Note that it would not make much sense to test a non-schema-qualified type name in this way — if the name can be recognized at all, it must be visible.

[Table 9.70](#page-8-0) lists functions that extract information from the system catalogs.

### <span id="page-8-0"></span>**Table 9.70. System Catalog Information Functions**

#### **Function**

#### **Description**

- format\_type ( type oid, typemod integer ) → text
  - Returns the SQL name for a data type that is identified by its type OID and possibly a type modifier. Pass NULL for the type modifier if no specific modifier is known.
- pg\_get\_catalog\_foreign\_keys () → setof record ( fktable regclass, fkcols text[], pktable regclass, pkcols text[], is\_array boolean, is\_opt boolean )

Returns a set of records describing the foreign key relationships that exist within the PostgreSQL system catalogs. The fktable column contains the name of the referencing catalog, and the fkcols column contains the name(s) of the referencing column(s). Similarly, the pktable column contains the name of the referenced catalog, and the pkcols column contains the name(s) of the referenced column(s). If is\_array is true, the last referencing column is an array, each of whose elements should match some entry in the referenced catalog. If is\_opt is true, the referencing column(s) are allowed to contain zeroes instead of a valid reference.

- pg\_get\_constraintdef ( constraint oid [, pretty boolean ] ) → text Reconstructs the creating command for a constraint. (This is a decompiled reconstruction, not the original text of the command.)
- pg\_get\_expr ( expr pg\_node\_tree, relation oid [, pretty boolean ] ) → text Decompiles the internal form of an expression stored in the system catalogs, such as the default value for a column. If the expression might contain Vars, specify the OID of the relation they refer to as the second parameter; if no Vars are expected, passing zero is sufficient.
- pg\_get\_functiondef ( func oid ) → text

Reconstructs the creating command for a function or procedure. (This is a decompiled reconstruction, not the original text of the command.) The result is a complete CREATE OR REPLACE FUNCTION or CREATE OR REPLACE PROCEDURE statement.

- pg\_get\_function\_arguments ( func oid ) → text
  - Reconstructs the argument list of a function or procedure, in the form it would need to appear in within CREATE FUNCTION (including default values).
- pg\_get\_function\_identity\_arguments ( func oid ) → text Reconstructs the argument list necessary to identify a function or procedure, in the form it would need to appear in within commands such as ALTER FUNCTION. This form omits default values.
- pg\_get\_function\_result ( func oid ) → text Reconstructs the RETURNS clause of a function, in the form it would need to appear in within CREATE FUNCTION. Returns NULL for a procedure.
- pg\_get\_indexdef ( index oid [, column integer, pretty boolean ] ) → text Reconstructs the creating command for an index. (This is a decompiled reconstruction, not the original text of the command.) If column is supplied and is not zero, only the definition of that column is reconstructed.
- pg\_get\_keywords () → setof record ( word text, catcode "char", barelabel boolean, catdesc text, baredesc text )

Returns a set of records describing the SQL keywords recognized by the server. The word column contains the keyword. The catcode column contains a category code: U for an unreserved keyword, C for a keyword that can be a column name, T for a keyword that can be a type or function name, or R for a fully reserved keyword. The barelabel column contains true if the keyword can be used as a "bare" column label in SELECT

#### **Description**

lists, or false if it can only be used after AS. The catdesc column contains a possibly-localized string describing the keyword's category. The baredesc column contains a possibly-localized string describing the keyword's column label status.

pg\_get\_partition\_constraintdef ( table oid ) → text

Reconstructs the definition of a partition constraint. (This is a decompiled reconstruction, not the original text of the command.)

pg\_get\_ruledef ( rule oid [, pretty boolean ] ) → text

Reconstructs the creating command for a rule. (This is a decompiled reconstruction, not the original text of the command.)

pg\_get\_serial\_sequence ( table text, column text ) → text

Returns the name of the sequence associated with a column, or NULL if no sequence is associated with the column. If the column is an identity column, the associated sequence is the sequence internally created for that column. For columns created using one of the serial types (serial, smallserial, bigserial), it is the sequence created for that serial column definition. In the latter case, the association can be modified or removed with ALTER SEQUENCE OWNED BY. (This function probably should have been called pg\_get\_owned\_sequence; its current name reflects the fact that it has historically been used with serial-type columns.) The first parameter is a table name with optional schema, and the second parameter is a column name. Because the first parameter potentially contains both schema and table names, it is parsed per usual SQL rules, meaning it is lower-cased by default. The second parameter, being just a column name, is treated literally and so has its case preserved. The result is suitably formatted for passing to the sequence functions (see Section 9.17).

A typical use is in reading the current value of the sequence for an identity or serial column, for example:

```
SELECT currval(pg_get_serial_sequence('sometable', 'id'));
```

pg\_get\_statisticsobjdef ( statobj oid ) → text

Reconstructs the creating command for an extended statistics object. (This is a decompiled reconstruction, not the original text of the command.)

pg\_get\_triggerdef ( trigger oid [, pretty boolean ] ) → text

Reconstructs the creating command for a trigger. (This is a decompiled reconstruction, not the original text of the command.)

pg\_get\_userbyid ( role oid ) → name

Returns a role's name given its OID.

pg\_get\_viewdef ( view oid [, pretty boolean ] ) → text

Reconstructs the underlying SELECT command for a view or materialized view. (This is a decompiled reconstruction, not the original text of the command.)

pg\_get\_viewdef ( view oid, wrap\_column integer ) → text

Reconstructs the underlying SELECT command for a view or materialized view. (This is a decompiled reconstruction, not the original text of the command.) In this form of the function, pretty-printing is always enabled, and long lines are wrapped to try to keep them shorter than the specified number of columns.

pg\_get\_viewdef ( view text [, pretty boolean ] ) → text

Reconstructs the underlying SELECT command for a view or materialized view, working from a textual name for the view rather than its OID. (This is deprecated; use the OID variant instead.)

#### **Description**

```
pg_index_column_has_property ( index regclass, column integer, proper-
      ty text ) → boolean
```

Tests whether an index column has the named property. Common index column properties are listed in [Table 9.71.](#page-12-0) (Note that extension access methods can define additional property names for their indexes.) NULL is returned if the property name is not known or does not apply to the particular object, or if the OID or column number does not identify a valid object.

pg\_index\_has\_property ( index regclass, property text ) → boolean Tests whether an index has the named property. Common index properties are listed in [Table 9.72](#page-12-1). (Note that extension access methods can define additional property names for their indexes.) NULL is returned if the property name is not known or does not apply to the particular object, or if the OID does not identify a valid object.

```
pg_indexam_has_property ( am oid, property text ) → boolean
```

Tests whether an index access method has the named property. Access method properties are listed in [Table 9.73](#page-13-0). NULL is returned if the property name is not known or does not apply to the particular object, or if the OID does not identify a valid object.

```
pg_options_to_table ( options_array text[] ) → setof record ( op-
      tion_name text, option_value text )
```

Returns the set of storage options represented by a value from pg\_class.reloptions or pg\_attribute.attoptions.

```
pg_tablespace_databases ( tablespace oid ) → setof oid
```

Returns the set of OIDs of databases that have objects stored in the specified tablespace. If this function returns any rows, the tablespace is not empty and cannot be dropped. To identify the specific objects populating the tablespace, you will need to connect to the database(s) identified by pg\_tablespace\_databases and query their pg\_class catalogs.

```
pg_tablespace_location ( tablespace oid ) → text
       Returns the file system path that this tablespace is located in.
```

```
pg_typeof ( "any" ) → regtype
```

Returns the OID of the data type of the value that is passed to it. This can be helpful for troubleshooting or dynamically constructing SQL queries. The function is declared as returning regtype, which is an OID alias type (see Section 8.19); this means that it is the same as an OID for comparison purposes but displays as a type name.

For example:

```
SELECT pg_typeof(33);
 pg_typeof
-----------
 integer
SELECT typlen FROM pg_type WHERE oid = pg_typeof(33);
 typlen
--------
 4
```

```
COLLATION FOR ( "any" ) → text
```

Returns the name of the collation of the value that is passed to it. The value is quoted and schema-qualified if necessary. If no collation was derived for the argument expression, then NULL is returned. If the argument is not of a collatable data type, then an error is raised.

#### **Description**

For example:

```
SELECT collation for (description) FROM pg_description
 LIMIT 1;
 pg_collation_for
------------------
 "default"
SELECT collation for ('foo' COLLATE "de_DE");
 pg_collation_for
------------------
 "de_DE"
```

### to\_regclass ( text ) → regclass

Translates a textual relation name to its OID. A similar result is obtained by casting the string to type regclass (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regcollation ( text ) → regcollation
```

Translates a textual collation name to its OID. A similar result is obtained by casting the string to type regcollation (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regnamespace ( text ) → regnamespace
```

Translates a textual schema name to its OID. A similar result is obtained by casting the string to type regnamespace (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regoper ( text ) → regoper
```

Translates a textual operator name to its OID. A similar result is obtained by casting the string to type regoper (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found or is ambiguous. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regoperator ( text ) → regoperator
```

Translates a textual operator name (with parameter types) to its OID. A similar result is obtained by casting the string to type regoperator (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regproc ( text ) → regproc
```

Translates a textual function or procedure name to its OID. A similar result is obtained by casting the string to type regproc (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found or is ambiguous. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regprocedure ( text ) → regprocedure
```

Translates a textual function or procedure name (with argument types) to its OID. A similar result is obtained by casting the string to type regprocedure (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

```
to_regrole ( text ) → regrole
```

#### **Description**

Translates a textual role name to its OID. A similar result is obtained by casting the string to type regrole (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

to\_regtype ( text ) → regtype

Translates a textual type name to its OID. A similar result is obtained by casting the string to type regtype (see Section 8.19); however, this function will return NULL rather than throwing an error if the name is not found. Also unlike the cast, this does not accept a numeric OID as input.

Most of the functions that reconstruct (decompile) database objects have an optional pretty flag, which if true causes the result to be "pretty-printed". Pretty-printing suppresses unnecessary parentheses and adds whitespace for legibility. The pretty-printed format is more readable, but the default format is more likely to be interpreted the same way by future versions of PostgreSQL; so avoid using pretty-printed output for dump purposes. Passing false for the pretty parameter yields the same result as omitting the parameter.

<span id="page-12-0"></span>**Table 9.71. Index Column Properties**

| Name               | Description                                                                                                 |  |
|--------------------|-------------------------------------------------------------------------------------------------------------|--|
| asc                | Does the column sort in ascending order on a<br>forward scan?                                               |  |
| desc               | Does the column sort in descending order on a<br>forward scan?                                              |  |
| nulls_first        | Does the column sort with nulls first on a for<br>ward scan?                                                |  |
| nulls_last         | Does the column sort with nulls last on a for<br>ward scan?                                                 |  |
| orderable          | Does the column possess any defined sort order<br>ing?                                                      |  |
| distance_orderable | Can the column be scanned in order by a "dis<br>tance" operator, for example ORDER BY col<br><-> constant ? |  |
| returnable         | Can the column value be returned by an in<br>dex-only scan?                                                 |  |
| search_array       | Does the column natively support col =<br>ANY(array) searches?                                              |  |
| search_nulls       | Does the column support IS NULL and IS<br>NOT NULL searches?                                                |  |

### <span id="page-12-1"></span>**Table 9.72. Index Properties**

| Name          | Description                                                                                                                  |
|---------------|------------------------------------------------------------------------------------------------------------------------------|
| clusterable   | Can the index be used in a CLUSTER command?                                                                                  |
| index_scan    | Does the index support plain (non-bitmap)<br>scans?                                                                          |
| bitmap_scan   | Does the index support bitmap scans?                                                                                         |
| backward_scan | Can the scan direction be changed in mid-scan<br>(to support FETCH BACKWARD on a cursor<br>without needing materialization)? |

**Table 9.73. Index Access Method Properties**

<span id="page-13-0"></span>

| Name          | Description                                                                       |  |
|---------------|-----------------------------------------------------------------------------------|--|
| can_order     | Does the access method support ASC, DESC and<br>related keywords in CREATE INDEX? |  |
| can_unique    | Does the access method support unique indexes?                                    |  |
| can_multi_col | Does the access method support indexes with<br>multiple columns?                  |  |
| can_exclude   | Does the access method support exclusion con<br>straints?                         |  |
| can_include   | Does the access method support the INCLUDE<br>clause of CREATE INDEX?             |  |

<span id="page-13-1"></span>[Table 9.74](#page-13-1) lists functions related to database object identification and addressing.

### **Table 9.74. Object Information and Addressing Functions**

**Function**

### **Description** pg\_describe\_object ( classid oid, objid oid, objsubid integer ) → text

Returns a textual description of a database object identified by catalog OID, object OID, and sub-object ID (such as a column number within a table; the sub-object ID is zero when referring to a whole object). This description is intended to be human-readable, and might be translated, depending on server configuration. This is especially useful to determine the identity of an object referenced in the pg\_depend catalog. This function returns NULL values for undefined objects.

pg\_identify\_object ( classid oid, objid oid, objsubid integer ) → record ( type text, schema text, name text, identity text )

Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. This information is intended to be machine-readable, and is never translated. type identifies the type of database object; schema is the schema name that the object belongs in, or NULL for object types that do not belong to schemas; name is the name of the object, quoted if necessary, if the name (along with schema name, if pertinent) is sufficient to uniquely identify the object, otherwise NULL; identity is the complete object identity, with the precise format depending on object type, and each name within the format being schema-qualified and quoted as necessary. Undefined objects are identified with NULL values.

pg\_identify\_object\_as\_address ( classid oid, objid oid, objsubid integer ) → record ( type text, object\_names text[], object\_args text[] )

Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. The returned information is independent of the current server, that is, it could be used to identify an identically named object in another server. type identifies the type of database object; object\_names and object\_args are text arrays that together form a reference to the object. These three values can be passed to pg\_get\_object\_address to obtain the internal address of the object.

pg\_get\_object\_address ( type text, object\_names text[], object\_args text[] ) → record ( classid oid, objid oid, objsubid integer ) Returns a row containing enough information to uniquely identify the database object specified by a type code and object name and argument arrays. The returned values are the ones that would be used in system catalogs such as pg\_depend; they can be passed to other system functions such as pg\_describe\_object or pg\_identify\_object. classid is the OID of the system catalog containing the object; objid is the

#### **Description**

OID of the object itself, and objsubid is the sub-object ID, or zero if none. This function is the inverse of pg\_identify\_object\_as\_address. Undefined objects are identified with NULL values.

The functions shown in [Table 9.75](#page-14-0) extract comments previously stored with the COMMENT command. A null value is returned if no comment could be found for the specified parameters.

### <span id="page-14-0"></span>**Table 9.75. Comment Information Functions**

#### **Function**

#### **Description**

col\_description ( table oid, column integer ) → text

Returns the comment for a table column, which is specified by the OID of its table and its column number. (obj\_description cannot be used for table columns, since columns do not have OIDs of their own.)

obj\_description ( object oid, catalog name ) → text

Returns the comment for a database object specified by its OID and the name of the containing system catalog. For example, obj\_description(123456, 'pg\_class') would retrieve the comment for the table with OID 123456.

obj\_description ( object oid ) → text

Returns the comment for a database object specified by its OID alone. This is *deprecated* since there is no guarantee that OIDs are unique across different system catalogs; therefore, the wrong comment might be returned.

shobj\_description ( object oid, catalog name ) → text

Returns the comment for a shared database object specified by its OID and the name of the containing system catalog. This is just like obj\_description except that it is used for retrieving comments on shared objects (that is, databases, roles, and tablespaces). Some system catalogs are global to all databases within each cluster, and the descriptions for objects in them are stored globally as well.

The functions shown in [Table 9.76](#page-14-1) provide server transaction information in an exportable form. The main use of these functions is to determine which transactions were committed between two snapshots.

### <span id="page-14-1"></span>**Table 9.76. Transaction ID and Snapshot Information Functions**

#### **Function**

### **Description**

age ( xid ) → integer

Returns the number of transactions between the supplied transaction id and the current transaction counter.

mxid\_age ( xid ) → integer

Returns the number of multixacts IDs between the supplied multixact ID and the current multixacts counter.

pg\_current\_xact\_id () → xid8

Returns the current transaction's ID. It will assign a new one if the current transaction does not have one already (because it has not performed any database updates).

pg\_current\_xact\_id\_if\_assigned () → xid8

Returns the current transaction's ID, or NULL if no ID is assigned yet. (It's best to use this variant if the transaction might otherwise be read-only, to avoid unnecessary consumption of an XID.)

#### **Description**

pg\_xact\_status ( xid8 ) → text

Reports the commit status of a recent transaction. The result is one of in progress, committed, or aborted, provided that the transaction is recent enough that the system retains the commit status of that transaction. If it is old enough that no references to the transaction survive in the system and the commit status information has been discarded, the result is NULL. Applications might use this function, for example, to determine whether their transaction committed or aborted after the application and database server become disconnected while a COMMIT is in progress. Note that prepared transactions are reported as in progress; applications must check pg\_prepared\_xacts if they need to determine whether a transaction ID belongs to a prepared transaction.

pg\_current\_snapshot () → pg\_snapshot

Returns a current *snapshot*, a data structure showing which transaction IDs are now inprogress.

pg\_snapshot\_xip ( pg\_snapshot ) → setof xid8

Returns the set of in-progress transaction IDs contained in a snapshot.

pg\_snapshot\_xmax ( pg\_snapshot ) → xid8

Returns the xmax of a snapshot.

pg\_snapshot\_xmin ( pg\_snapshot ) → xid8

Returns the xmin of a snapshot.

pg\_visible\_in\_snapshot ( xid8, pg\_snapshot ) → boolean

Is the given transaction ID *visible* according to this snapshot (that is, was it completed before the snapshot was taken)? Note that this function will not give the correct answer for a subtransaction ID.

pg\_get\_multixact\_members ( multixid xid ) → setof record ( xid xid, mode text )

Returns the transaction ID and lock mode for each member of the specified multixact ID. The lock modes forupd, fornokeyupd, sh, and keysh correspond to the row-level locks FOR UPDATE, FOR NO KEY UPDATE, FOR SHARE, and FOR KEY SHARE, respectively, as described in [Section 13.3.2](#page-119-0). Two additional modes are specific to multixacts: nokeyupd, used by updates that do not modify key columns, and upd, used by updates or deletes that modify key columns.

The internal transaction ID type xid is 32 bits wide and wraps around every 4 billion transactions. However, the functions shown in [Table 9.76](#page-14-1), except age, mxid\_age, and pg\_get\_multixact\_members, use a 64-bit type xid8 that does not wrap around during the life of an installation, and can be converted to xid by casting if required. The data type pg\_snapshot stores information about transaction ID visibility at a particular moment in time. Its components are described in [Table 9.77](#page-15-0). pg\_snapshot's textual representation is xmin:xmax:xip\_list. For example 10:20:10,14,15 means xmin=10, xmax=20, xip\_list=10, 14, 15.

<span id="page-15-0"></span>**Table 9.77. Snapshot Components**

| Name | Description                                                                                                                                                                             |  |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| xmin | Lowest transaction ID that was still active. All<br>transaction IDs less than xmin are either com<br>mitted and visible, or rolled back and dead.                                       |  |
| xmax | One past the highest completed transaction<br>ID. All transaction IDs greater than or equal to<br>xmax had not yet completed as of the time of<br>the snapshot, and thus are invisible. |  |

| Name     | Description                                                                                                                                                                                                                                                                                                                        |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| xip_list | Transactions in progress at the time of the snap<br>shot. A transaction ID that is xmin <= X <<br>xmax and not in this list was already completed<br>at the time of the snapshot, and thus is either vis<br>ible or dead according to its commit status. This<br>list does not include the transaction IDs of sub<br>transactions. |

In releases of PostgreSQL before 13 there was no xid8 type, so variants of these functions were provided that used bigint to represent a 64-bit XID, with a correspondingly distinct snapshot data type txid\_snapshot. These older functions have txid in their names. They are still supported for backward compatibility, but may be removed from a future release. See [Table 9.78](#page-16-0).

<span id="page-16-0"></span>**Table 9.78. Deprecated Transaction ID and Snapshot Information Functions**

| Function<br>Description                                                                       |
|-----------------------------------------------------------------------------------------------|
| txid_current () → bigint<br>See pg_current_xact_id().                                         |
| txid_current_if_assigned () → bigint<br>See pg_current_xact_id_if_assigned().                 |
| txid_current_snapshot () → txid_snapshot<br>See pg_current_snapshot().                        |
| txid_snapshot_xip ( txid_snapshot ) → setof bigint<br>See pg_snapshot_xip().                  |
| txid_snapshot_xmax ( txid_snapshot ) → bigint<br>See pg_snapshot_xmax().                      |
| txid_snapshot_xmin ( txid_snapshot ) → bigint<br>See pg_snapshot_xmin().                      |
| txid_visible_in_snapshot ( bigint, txid_snapshot ) → boolean<br>See pg_visible_in_snapshot(). |
| txid_status ( bigint ) → text<br>See pg_xact_status().                                        |

The functions shown in [Table 9.79](#page-16-1) provide information about when past transactions were committed. They only provide useful data when the track\_commit\_timestamp configuration option is enabled, and only for transactions that were committed after it was enabled.

<span id="page-16-1"></span>**Table 9.79. Committed Transaction Information Functions**

| Function<br>Description                                                                                                                                                         |  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| pg_xact_commit_timestamp ( xid ) → timestamp with time zone<br>Returns the commit timestamp of a transaction.                                                                   |  |
| pg_xact_commit_timestamp_origin ( xid ) → record ( timestamp timestamp<br>with time zone, roident oid)<br>Returns the commit timestamp and replication origin of a transaction. |  |
| pg_last_committed_xact () → record ( xid xid, timestamp timestamp with<br>time zone, roident oid )                                                                              |  |

#### **Description**

Returns the transaction ID, commit timestamp and replication origin of the latest committed transaction.

The functions shown in [Table 9.80](#page-17-0) print information initialized during initdb, such as the catalog version. They also show information about write-ahead logging and checkpoint processing. This information is cluster-wide, not specific to any one database. These functions provide most of the same information, from the same source, as the pg\_controldata application.

<span id="page-17-0"></span>**Table 9.80. Control Data Functions**

### **Function Description** pg\_control\_checkpoint () → record Returns information about current checkpoint state, as shown in [Table 9.81](#page-17-1). pg\_control\_system () → record Returns information about current control file state, as shown in [Table 9.82.](#page-18-0) pg\_control\_init () → record Returns information about cluster initialization state, as shown in [Table 9.83](#page-18-1). pg\_control\_recovery () → record Returns information about recovery state, as shown in [Table 9.84.](#page-18-2)

<span id="page-17-1"></span>**Table 9.81. pg\_control\_checkpoint Output Columns**

| Column Name          | Data Type                |
|----------------------|--------------------------|
| checkpoint_lsn       | pg_lsn                   |
| redo_lsn             | pg_lsn                   |
| redo_wal_file        | text                     |
| timeline_id          | integer                  |
| prev_timeline_id     | integer                  |
| full_page_writes     | boolean                  |
| next_xid             | text                     |
| next_oid             | oid                      |
| next_multixact_id    | xid                      |
| next_multi_offset    | xid                      |
| oldest_xid           | xid                      |
| oldest_xid_dbid      | oid                      |
| oldest_active_xid    | xid                      |
| oldest_multi_xid     | xid                      |
| oldest_multi_dbid    | oid                      |
| oldest_commit_ts_xid | xid                      |
| newest_commit_ts_xid | xid                      |
| checkpoint_time      | timestamp with time zone |

**Table 9.82. pg\_control\_system Output Columns**

<span id="page-18-0"></span>

| Column Name              | Data Type                |
|--------------------------|--------------------------|
| pg_control_version       | integer                  |
| catalog_version_no       | integer                  |
| system_identifier        | bigint                   |
| pg_control_last_modified | timestamp with time zone |

<span id="page-18-1"></span>**Table 9.83. pg\_control\_init Output Columns**

| Column Name                | Data Type |
|----------------------------|-----------|
| max_data_alignment         | integer   |
| database_block_size        | integer   |
| blocks_per_segment         | integer   |
| wal_block_size             | integer   |
| bytes_per_wal_segment      | integer   |
| max_identifier_length      | integer   |
| max_index_columns          | integer   |
| max_toast_chunk_size       | integer   |
| large_object_chunk_size    | integer   |
| float8_pass_by_value       | boolean   |
| data_page_checksum_version | integer   |

<span id="page-18-2"></span>**Table 9.84. pg\_control\_recovery Output Columns**

| Column Name                   | Data Type |
|-------------------------------|-----------|
| min_recovery_end_lsn          | pg_lsn    |
| min_recovery_end_timeline     | integer   |
| backup_start_lsn              | pg_lsn    |
| backup_end_lsn                | pg_lsn    |
| end_of_backup_record_required | boolean   |