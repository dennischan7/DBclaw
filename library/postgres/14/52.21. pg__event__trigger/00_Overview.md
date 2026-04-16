---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_event\_trigger stores event triggers. See Chapter 40 for more information.

### **Table 52.21. pg\_event\_trigger Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

evtname name

Trigger name (must be unique)

evtevent name

#### **Description**

Identifies the event for which this trigger fires

evtowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the event trigger

evtfoid oid (references [pg\\_proc](#page-29-0).oid)

The function to be called

evtenabled char

Controls in which session\_replication\_role modes the event trigger fires. O = trigger fires in "origin" and "local" modes, D = trigger is disabled, R = trigger fires in "replica" mode, A = trigger fires always.

evttags text[]

Command tags for which this trigger will fire. If NULL, the firing of this trigger is not restricted on the basis of the command tag.

# <span id="page-19-0"></span>**52.22. pg\_extension**

The catalog pg\_extension stores information about the installed extensions. See Section 38.17 for details about extensions.

### **Table 52.22. pg\_extension Columns**

#### **Column Type Description**

oid oid

Row identifier

extname name

Name of the extension

extowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the extension

extnamespace oid (references [pg\\_namespace](#page-25-0).oid)

Schema containing the extension's exported objects

extrelocatable bool

True if extension can be relocated to another schema

extversion text

Version name for the extension

extconfig oid[] (references [pg\\_class](#page-8-0).oid)

Array of regclass OIDs for the extension's configuration table(s), or NULL if none

extcondition text[]

Array of WHERE-clause filter conditions for the extension's configuration table(s), or NULL if none

Note that unlike most catalogs with a "namespace" column, extnamespace is not meant to imply that the extension belongs to that schema. Extension names are never schema-qualified. Rather, extnamespace indicates the schema that contains most or all of the extension's objects. If extrelocatable is true, then this schema must in fact contain all schema-qualifiable objects belonging to the extension.

# <span id="page-19-1"></span>**52.23. pg\_foreign\_data\_wrapper**

The catalog pg\_foreign\_data\_wrapper stores foreign-data wrapper definitions. A foreign-data wrapper is the mechanism by which external data, residing on foreign servers, is accessed.

### **Table 52.23. pg\_foreign\_data\_wrapper Columns**

#### **Column Type Description**

oid oid

Row identifier

fdwname name

Name of the foreign-data wrapper

fdwowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the foreign-data wrapper

fdwhandler oid (references [pg\\_proc](#page-29-0).oid)

References a handler function that is responsible for supplying execution routines for the foreign-data wrapper. Zero if no handler is provided

fdwvalidator oid (references [pg\\_proc](#page-29-0).oid)

References a validator function that is responsible for checking the validity of the options given to the foreign-data wrapper, as well as options for foreign servers and user mappings using the foreign-data wrapper. Zero if no validator is provided

fdwacl aclitem[]

Access privileges; see Section 5.7 for details

fdwoptions text[]

Foreign-data wrapper specific options, as "keyword=value" strings

# <span id="page-20-0"></span>**52.24. pg\_foreign\_server**

The catalog pg\_foreign\_server stores foreign server definitions. A foreign server describes a source of external data, such as a remote server. Foreign servers are accessed via foreign-data wrappers.

### **Table 52.24. pg\_foreign\_server Columns**

### **Column Type Description**

oid oid

Row identifier

srvname name

Name of the foreign server

srvowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the foreign server

srvfdw oid (references [pg\\_foreign\\_data\\_wrapper](#page-19-1).oid)

OID of the foreign-data wrapper of this foreign server

srvtype text

Type of the server (optional)

srvversion text

Version of the server (optional)

srvacl aclitem[]

Access privileges; see Section 5.7 for details

srvoptions text[]

Foreign server specific options, as "keyword=value" strings