---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_conversion describes encoding conversion functions. See CREATE CON-VERSION for more information.

### **Table 52.14. pg\_conversion Columns**

## **Column Type Description** oid oid Row identifier conname name Conversion name (unique within a namespace) connamespace oid (references [pg\\_namespace](#page-25-0).oid) The OID of the namespace that contains this conversion conowner oid (references [pg\\_authid](#page-5-0).oid) Owner of the conversion conforencoding int4 Source encoding ID contoencoding int4 Destination encoding ID conproc regproc (references [pg\\_proc](#page-29-0).oid) Conversion function condefault bool True if this is the default conversion

# <span id="page-13-0"></span>**52.15. pg\_database**

The catalog pg\_database stores information about the available databases. Databases are created with the CREATE DATABASE command. Consult Chapter 23 for details about the meaning of some of the parameters.

Unlike most system catalogs, pg\_database is shared across all databases of a cluster: there is only one copy of pg\_database per cluster, not one per database.

### **Table 52.15. pg\_database Columns**

#### **Column Type**

#### **Description**

oid oid

Row identifier

datname name

Database name

datdba oid (references [pg\\_authid](#page-5-0).oid)

Owner of the database, usually the user who created it

encoding int4

Character encoding for this database (pg\_encoding\_to\_char() can translate this number to the encoding name)

datcollate name

LC\_COLLATE for this database

datctype name

LC\_CTYPE for this database

datistemplate bool

If true, then this database can be cloned by any user with CREATEDB privileges; if false, then only superusers or the owner of the database can clone it.

datallowconn bool

If false then no one can connect to this database. This is used to protect the template0 database from being altered.

datconnlimit int4

Sets maximum number of concurrent connections that can be made to this database. -1 means no limit, -2 indicates the database is invalid.

datlastsysoid oid

Last system OID in the database; useful particularly to pg\_dump

datfrozenxid xid

All transaction IDs before this one have been replaced with a permanent ("frozen") transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent transaction ID wraparound or to allow pg\_xact to be shrunk. It is the minimum of the per-table [pg\\_class](#page-8-0).relfrozenxid values.

datminmxid xid

All multixact IDs before this one have been replaced with a transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent multixact ID wraparound or to allow pg\_multixact to be shrunk. It is the minimum of the per-table [pg\\_class](#page-8-0).relminmxid values.

dattablespace oid (references [pg\\_tablespace](#page-41-0).oid)

The default tablespace for the database. Within this database, all tables for which [pg\\_class](#page-8-0).reltablespace is zero will be stored in this tablespace; in particular, all the non-shared system catalogs will be there.

datacl aclitem[]

Access privileges; see Section 5.7 for details