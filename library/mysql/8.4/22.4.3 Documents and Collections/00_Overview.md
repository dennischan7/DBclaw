---
source: MySQL 8.4 Reference
title: 00_Overview
---

When you are using MySQL as a Document Store, collections are containers within a schema that you can create, list, and drop. Collections contain JSON documents that you can add, find, update, and remove.

The examples in this section use the countryinfo collection in the world\_x schema. For instructions on setting up the world\_x schema, see [Section 22.4.2, "Download and Import world\\_x](#page-0-0) [Database"](#page-0-0).

# **Documents**

In MySQL, documents are represented as JSON objects. Internally, they are stored in an efficient binary format that enables fast lookups and updates.

• Simple document format for Python:

```
{"field1": "value", "field2" : 10, "field 3": null}
```

An array of documents consists of a set of documents separated by commas and enclosed within [ and ] characters.

• Simple array of documents for Python:

```
[{"Name": "Aruba", "Code:": "ABW"}, {"Name": "Angola", "Code:": "AGO"}]
```

MySQL supports the following Python value types in JSON documents:

- numbers (integer and floating point)
- strings
- boolean (False and True)
- None
- arrays of more JSON values
- nested (or embedded) objects of more JSON values

# **Collections**

Collections are containers for documents that share a purpose and possibly share one or more indexes. Each collection has a unique name and exists within a single schema.

The term schema is equivalent to a database, which means a group of database objects as opposed to a relational schema, used to enforce structure and constraints over data. A schema does not enforce conformity on the documents in a collection.

In this quick-start guide:

• Basic objects include:

| Object form          | Description                                                                                                                                                                                                         |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| db                   | db is a global variable assigned to the current<br>active schema. When you want to run operations<br>against the schema, for example to retrieve a<br>collection, you use methods available for the db<br>variable. |
| db.get_collections() | db.get_collections() returns a list of collections<br>in the schema. Use the list to get references to<br>collection objects, iterate over them, and so on.                                                         |

• Basic operations scoped by collections include:

| Operation form   | Description                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| db.name.add()    | The add() method inserts one document or a list<br>of documents into the named collection.    |
| db.name.find()   | The find() method returns some or all documents<br>in the named collection.                   |
| db.name.modify() | The modify() method updates documents in the<br>named collection.                             |
| db.name.remove() | The remove() method deletes one document or a<br>list of documents from the named collection. |

# **Related Information**

- See [Working with Collections](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-collections.md) for a general overview.
- [CRUD EBNF Definitions](https://dev.mysql.com/doc/x-devapi-userguide/en/mysql-x-crud-ebnf-definitions.md) provides a complete list of operations.