---
source: PostgreSQL 16 Reference
title: 00_Overview
---

[Table 9.68](#page-14-0) lists functions that allow querying object access privileges programmatically. (See Section 5.7 for more information about privileges.) In these functions, the user whose privileges are being inquired about can be specified by name or by OID (pg\_authid.oid), or if the name is given as public then the privileges of the PUBLIC pseudo-role are checked. Also, the user argument can be omitted entirely, in which case the current\_user is assumed. The object that is being inquired about can be specified either by name or by OID, too. When specifying by name, a schema name can be included if relevant. The access privilege of interest is specified by a text string, which must evaluate to one of the appropriate privilege keywords for the object's type (e.g., SELECT). Optionally, WITH GRANT OPTION can be added to a privilege type to test whether the privilege is held with grant option. Also, multiple privilege types can be listed separated by commas, in which case the result will be true if any of the listed privileges is held. (Case of the privilege string is not significant, and extra whitespace is allowed between but not within privilege names.) Some examples:

```
SELECT has_table_privilege('myschema.mytable', 'select');
```

SELECT has\_table\_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');

### <span id="page-14-0"></span>**Table 9.68. Access Privilege Inquiry Functions**

#### **Function**

### **Description**

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

Does user have privilege for language? The only allowable privilege type is USAGE.

has\_parameter\_privilege ( [ user name or oid, ] parameter text, privilege text ) → boolean

Does user have privilege for configuration parameter? The parameter name is case-insensitive. Allowable privilege types are SET and ALTER SYSTEM.

has\_schema\_privilege ( [ user name or oid, ] schema text or oid, privilege text ) → boolean

Does user have privilege for schema? Allowable privilege types are CREATE and USAGE.

has\_sequence\_privilege ( [ user name or oid, ] sequence text or oid, privilege text ) → boolean

Does user have privilege for sequence? Allowable privilege types are USAGE, SELECT, and UPDATE.

#### **Description**

has\_server\_privilege ( [ user name or oid, ] server text or oid, privilege text ) → boolean

Does user have privilege for foreign server? The only allowable privilege type is USAGE.

has\_table\_privilege ( [ user name or oid, ] table text or oid, privilege text ) → boolean

Does user have privilege for table? Allowable privilege types are SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, and TRIGGER.

has\_tablespace\_privilege ( [ user name or oid, ] tablespace text or oid, privilege text ) → boolean

Does user have privilege for tablespace? The only allowable privilege type is CREATE.

has\_type\_privilege ( [ user name or oid, ] type text or oid, privilege text ) → boolean

Does user have privilege for data type? The only allowable privilege type is USAGE. When specifying a type by name rather than by OID, the allowed input is the same as for the regtype data type (see Section 8.19).

pg\_has\_role ( [ user name or oid, ] role text or oid, privilege text ) → boolean

Does user have privilege for role? Allowable privilege types are MEMBER, USAGE, and SET. MEMBER denotes direct or indirect membership in the role without regard to what specific privileges may be conferred. USAGE denotes whether the privileges of the role are immediately available without doing SET ROLE, while SET denotes whether it is possible to change to the role using the SET ROLE command. WITH ADMIN OPTION or WITH GRANT OPTION can be added to any of these privilege types to test whether the ADMIN privilege is held (all six spellings test the same thing). This function does not allow the special case of setting user to public, because the PUBLIC pseudo-role can never be a member of real roles.

row\_security\_active ( table text or oid ) → boolean

Is row-level security active for the specified table in the context of the current user and current environment?

[Table 9.69](#page-15-0) shows the operators available for the aclitem type, which is the catalog representation of access privileges. See Section 5.7 for information about how to read access privilege values.

## <span id="page-15-0"></span>**Table 9.69. aclitem Operators**

#### **Operator**

### **Description Example(s)**

```
aclitem = aclitem → boolean
```

Are aclitems equal? (Notice that type aclitem lacks the usual set of comparison operators; it has only equality. In turn, aclitem arrays can only be compared for equality.)

'calvin=r\*w/hobbes'::aclitem = 'calvin=r\*w\*/hobbes'::aclitem → f

```
aclitem[] @> aclitem → boolean
```

Does array contain the specified privileges? (This is true if there is an array entry that matches the aclitem's grantee and grantor, and has at least the specified set of privileges.)

```
Operator
      Description
      Example(s)
       '{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @>
       'calvin=r*/hobbes'::aclitem → t
aclitem[] ~ aclitem → boolean
      This is a deprecated alias for @>.
       '{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] ~
       'calvin=r*/hobbes'::aclitem → t
```

<span id="page-16-0"></span>[Table 9.70](#page-16-0) shows some additional functions to manage the aclitem type.

## **Table 9.70. aclitem Functions**

# **Function**

### **Description**

```
acldefault ( type "char", ownerId oid ) → aclitem[]
```

Constructs an aclitem array holding the default access privileges for an object of type type belonging to the role with OID ownerId. This represents the access privileges that will be assumed when an object's ACL entry is null. (The default access privileges are described in Section 5.7.) The type parameter must be one of 'c' for COLUMN, 'r' for TABLE and table-like objects, 's' for SEQUENCE, 'd' for DATABASE, 'f' for FUNCTION or PROCEDURE, 'l' for LANGUAGE, 'L' for LARGE OBJECT, 'n' for SCHEMA, 'p' for PA-RAMETER, 't' for TABLESPACE, 'F' for FOREIGN DATA WRAPPER, 'S' for FOREIGN SERVER, or 'T' for TYPE or DOMAIN.

```
aclexplode ( aclitem[] ) → setof record ( grantor oid, grantee oid, priv-
      ilege_type text, is_grantable boolean )
```

Returns the aclitem array as a set of rows. If the grantee is the pseudo-role PUBLIC, it is represented by zero in the grantee column. Each granted privilege is represented as SELECT, INSERT, etc (see Table 5.1 for a full list). Note that each privilege is broken out as a separate row, so only one keyword appears in the privilege\_type column.

```
makeaclitem ( grantee oid, grantor oid, privileges text, is_grantable
      boolean ) → aclitem
```

Constructs an aclitem with the given properties. privileges is a comma-separated list of privilege names such as SELECT, INSERT, etc, all of which are set in the result. (Case of the privilege string is not significant, and extra whitespace is allowed between but not within privilege names.)