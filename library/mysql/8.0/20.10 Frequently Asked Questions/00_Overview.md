---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section provides answers to frequently asked questions.

## **What is the maximum number of MySQL servers in a group?**

A group can consist of maximum 9 servers. Attempting to add another server to a group with 9 members causes the request to join to be refused. This limit has been identified from testing and benchmarking as a safe boundary where the group performs reliably on a stable local area network.

## **How are servers in a group connected?**

Servers in a group connect to the other servers in the group by opening a peer-topeer TCP connection. These connections are only used for internal communication and message passing between servers in the group. This address is configured by the [group\\_replication\\_local\\_address](#page-28-0) variable.

# **What is the group\_replication\_bootstrap\_group option used for?**

The bootstrap flag instructs a member to create a group and act as the initial seed server. The second member joining the group needs to ask the member that bootstrapped the group to dynamically change the configuration in order for it to be added to the group.

A member needs to bootstrap the group in two scenarios. When the group is originally created, or when shutting down and restarting the entire group.

# **How do I set credentials for the distributed recovery process?**

You can set the user credentials permanently as the credentials for the group\_replication\_recovery channel, using a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23). Alternatively, from MySQL 8.0.21, you can specify them on the START GROUP\_REPLICATION statement each time Group Replication is started.

User credentials set using CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO are stored in plain text in the replication metadata repositories on the server, but user credentials specified on START GROUP\_REPLICATION are saved in memory only, and are removed by a STOP GROUP\_REPLICATION statement or server shutdown. Using START GROUP\_REPLICATION to specify the user credentials therefore helps to secure the Group Replication servers against unauthorized access. However, this method is not compatible with starting Group Replication automatically, as specified by the [group\\_replication\\_start\\_on\\_boot](#page-43-0) system variable. For more information, see Section 20.6.3.1, "Secure User Credentials for Distributed Recovery".

## **Can I scale-out my write-load using Group Replication?**

Not directly, but MySQL Group replication is a shared nothing full replication solution, where all servers in the group replicate the same amount of data. Therefore if one member in the group writes N bytes to storage as the result of a transaction commit operation, then roughly N bytes are written to storage on other members as well, because the transaction is replicated everywhere.

However, given that other members do not have to do the same amount of processing that the original member had to do when it originally executed the transaction, they apply the changes faster. Transactions are replicated in a format that is used to apply row transformations only, without having to re-execute transactions again (row-based format).

Furthermore, given that changes are propagated and applied in row-based format, this means that they are received in an optimized and compact format, and likely reducing the number of IO operations required when compared to the originating member.

To summarize, you can scale-out processing, by spreading conflict free transactions throughout different members in the group. And you can likely scale-out a small fraction of your IO operations, since remote servers receive only the necessary changes to read-modify-write changes to stable storage.

# **Does Group Replication require more network bandwidth and CPU, when compared to simple replication and under the same workload?**

Some additional load is expected because servers need to be constantly interacting with each other for synchronization purposes. It is difficult to quantify how much more data. It also depends on the size of the group (three servers puts less stress on the bandwidth requirements than nine servers in the group).

Also the memory and CPU footprint are larger, because more complex work is done for the server synchronization part and for the group messaging.

# **Can I deploy Group Replication across wide-area networks?**

Yes, but the network connection between each member must be reliable and have suitable performance. Low latency, high bandwidth network connections are a requirement for optimal performance.

If network bandwidth alone is an issue, then Section 20.7.4, "Message Compression" can be used to lower the bandwidth required. However, if the network drops packets, leading to re-transmissions and higher end-to-end latency, throughput and latency are both negatively affected.

![](_page_48_Picture_12.jpeg)

### **Warning**

When the network round-trip time (RTT) between any group members is 5 seconds or more you could encounter problems as the built-in failure detection mechanism could be incorrectly triggered.

# **Do members automatically rejoin a group in case of temporary connectivity problems?**

This depends on the reason for the connectivity problem. If the connectivity problem is transient and the reconnection is quick enough that the failure detector is not aware of it, then the server may not be removed from the group. If it is a "long" connectivity problem, then the failure detector eventually suspects a problem and the server is removed from the group.

From MySQL 8.0, two settings are available to increase the chances of a member remaining in or rejoining a group:

- [group\\_replication\\_member\\_expel\\_timeout](#page-29-0) increases the time between the creation of a suspicion (which happens after an initial 5-second detection period) and the expulsion of the member. You can set a waiting period of up to 1 hour. From MySQL 8.0.21, a waiting period of 5 seconds is set by default.
- [group\\_replication\\_autorejoin\\_tries](#page-9-0) makes a member try to rejoin the group after an expulsion or unreachable majority timeout. The member makes the specified number of auto-rejoin attempts five minutes apart. From MySQL 8.0.21, this feature is activated by default and the member makes three auto-rejoin attempts.

If a server is expelled from the group and any auto-rejoin attempts do not succeed, you need to join it back again. In other words, after a server is removed explicitly from the group you need to rejoin it manually (or have a script doing it automatically).

## **When is a member excluded from a group?**

If the member becomes silent, the other members remove it from the group configuration. In practice this may happen when the member has crashed or there is a network disconnection.

The failure is detected after a given timeout elapses for a given member and a new configuration without the silent member in it is created.

## **What happens when one node is significantly lagging behind?**

There is no method for defining policies for when to expel members automatically from the group. You need to find out why a member is lagging behind and fix that or remove the member from the group. Otherwise, if the server is so slow that it triggers the flow control, then the entire group slows down as well. The flow control can be configured according to the your needs.

# **Upon suspicion of a problem in the group, is there a special member responsible for triggering a reconfiguration?**

No, there is no special member in the group in charge of triggering a reconfiguration.

Any member can suspect that there is a problem. All members need to (automatically) agree that a given member has failed. One member is in charge of expelling it from the group, by triggering a reconfiguration. Which member is responsible for expelling the member is not something you can control or set.

# **Can I use Group Replication for sharding?**

Group Replication is designed to provide highly available replica sets; data and writes are duplicated on each member in the group. For scaling beyond what a single system can provide, you need an orchestration and sharding framework built around a number of Group Replication sets, where each replica set maintains and manages a given shard or partition of your total dataset. This type of setup, often called a "sharded cluster", allows you to scale reads and writes linearly and without limit.

# **How do I use Group Replication with SELinux?**

If SELinux is enabled, which you can verify using sestatus -v, then you need to enable the use of the Group Replication communication port. See Setting the TCP Port Context for Group Replication.

# **How do I use Group Replication with iptables?**

If iptables is enabled, then you need to open up the Group Replication port for communication between the machines. To see the current rules in place on each machine, issue iptables -L. Assuming the port configured is 33061, enable communication over the necessary port by issuing iptables -A INPUT -p tcp --dport 33061 -j ACCEPT.

# **How do I recover the relay log for a replication channel used by a group member?**

The replication channels used by Group Replication behave in the same way as replication channels used in asynchronous source to replica replication, and as such rely on the relay log. In the event of a change of the relay\_log variable, or when the option is not set and the host name changes, there is a chance of errors. See Section 19.2.4.1, "The Relay Log" for a recovery procedure in this situation. Alternatively, another way of fixing the issue specifically in Group Replication is to issue a STOP GROUP\_REPLICATION statement and then a START GROUP\_REPLICATION statement to restart the instance. The Group Replication plugin creates the group\_replication\_applier channel again.

## **Why does Group Replication use two bind addresses?**

Group Replication uses two bind addresses in order to split network traffic between the SQL address, used by clients to communicate with the member, and the [group\\_replication\\_local\\_address](#page-28-0), used internally by the group members to communicate. For example, assume a server with two network interfaces assigned to the network addresses 203.0.113.1 and 198.51.100.179. In such a situation you could use 203.0.113.1:33061 for the internal group network address by setting [group\\_replication\\_local\\_address=203.0.113.1:33061](#page-28-0). Then you could use 198.51.100.179 for hostname and 3306 for the port. Client SQL applications would then connect to the member at 198.51.100.179:3306. This enables you to configure different rules on the different networks. Similarly, the internal group communication can be separated from the network connection used for client applications, for increased security.

## **How does Group Replication use network addresses and hostnames?**

Group Replication uses network connections between members and therefore its functionality is directly impacted by how you configure hostnames and ports. For example, Group Replication's distributed recovery process creates a connection to an existing group member using the server's hostname and port. When a member joins a group it receives the group membership information, using the network address information that is listed at performance\_schema.replication\_group\_members. One of the members listed in that table is selected as the donor of the missing data from the group to the joining member.

This means that any value you configure using a hostname, such as the SQL network address or the group seeds address, must be a fully qualified name and resolvable by each member of the group. You can ensure this for example through DNS, or correctly configured /etc/hosts files, or other local processes. If a you want to configure the MEMBER\_HOST value on a server, specify it using the - report-host option on the server before joining it to the group.

![](_page_50_Picture_8.jpeg)

#### **Important**

The assigned value is used directly and is not affected by the skip\_name\_resolve system variable.

To configure MEMBER\_PORT on a server, specify it using the report\_port system variable.

# **Why did the auto increment setting on the server change?**

When Group Replication is started on a server, the value of auto\_increment\_increment is changed to the value of [group\\_replication\\_auto\\_increment\\_increment](#page-8-0), which defaults to 7, and the value of auto\_increment\_offset is changed to the server ID. The changes are reverted when Group Replication is stopped. These settings avoid the selection of duplicate auto-increment values for writes on group members, which causes rollback of transactions. The default auto increment value of 7 for Group Replication represents a balance between the number of usable values and the permitted maximum size of a replication group (9 members).

The changes are only made and reverted if auto\_increment\_increment and auto\_increment\_offset each have their default value of 1. If their values have already been modified from the default, Group Replication does not alter them. From MySQL 8.0, the system variables are also not modified when Group Replication is in single-primary mode, where only one server writes.

## **How do I find the primary?**

If the group is operating in single-primary mode, it can be useful to find out which member is the primary. See Finding the Primary

# Chapter 21 MySQL Shell

MySQL Shell is an advanced client and code editor for MySQL Server. In addition to the provided SQL functionality, similar to mysql, MySQL Shell provides scripting capabilities for JavaScript and Python and includes APIs for working with MySQL. MySQL Shell is a component that you can install separately.

The following discussion briefly describes MySQL Shell's capabilities. For more information, see the MySQL Shell manual, available at [https://dev.mysql.com/doc/mysql-shell/en/.](https://dev.mysql.com/doc/mysql-shell/en/)

MySQL Shell includes the following APIs implemented in JavaScript and Python which you can use to develop code that interacts with MySQL.

- The X DevAPI enables developers to work with both relational and document data when MySQL Shell is connected to a MySQL server using the X Protocol. This enables you to use MySQL as a Document Store, sometimes referred to as "using NoSQL". For more information, see [Chapter 22,](#page-54-0) [Using MySQL as a Document Store](#page-54-0). For documentation on the concepts and usage of X DevAPI, which is implemented in MySQL Shell, see [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/).
- The AdminAPI enables database administrators to work with InnoDB Cluster, which provides an integrated solution for high availability and scalability using InnoDB based MySQL databases, without requiring advanced MySQL expertise. The AdminAPI also includes support for InnoDB ReplicaSet, which enables you to administer a set of MySQL instances running asynchronous GTID-based replication in a similar way to InnoDB Cluster. Additionally, the AdminAPI makes administration of MySQL Router easier, including integration with both InnoDB Cluster and InnoDB ReplicaSet. See [MySQL AdminAPI](https://dev.mysql.com/doc/mysql-shell/8.0/en/admin-api-userguide.md).

MySQL Shell is available in two editions, the Community Edition and the Commercial Edition. The Community Edition is available free of charge. The Commercial Edition provides additional Enterprise features at low cost.

# <span id="page-54-0"></span>Chapter 22 Using MySQL as a Document Store

# **Table of Contents**

| 22.1 Interfaces to a MySQL Document Store                               | 4026 |
|-------------------------------------------------------------------------|------|
| 22.2 Document Store Concepts 4026                                       |      |
| 22.3 JavaScript Quick-Start Guide: MySQL Shell for Document Store 4027  |      |
| 22.3.1 MySQL Shell 4028                                                 |      |
| 22.3.2 Download and Import world_x Database 4029                        |      |
| 22.3.3 Documents and Collections 4030                                   |      |
| 22.3.4 Relational Tables 4040                                           |      |
| 22.3.5 Documents in Tables 4046                                         |      |
| 22.4 Python Quick-Start Guide: MySQL Shell for Document Store 4047      |      |
| 22.4.1 MySQL Shell 4047                                                 |      |
| 22.4.2 Download and Import world_x Database 4049                        |      |
| 22.4.3 Documents and Collections 4049                                   |      |
| 22.4.4 Relational Tables 4060                                           |      |
| 22.4.5 Documents in Tables 4066                                         |      |
| 22.5 X Plugin 4067                                                      |      |
| 22.5.1 Checking X Plugin Installation 4067                              |      |
| 22.5.2 Disabling X Plugin 4067                                          |      |
| 22.5.3 Using Encrypted Connections with X Plugin 4067                   |      |
| 22.5.4 Using X Plugin with the Caching SHA-2 Authentication Plugin 4068 |      |
| 22.5.5 Connection Compression with X Plugin 4069                        |      |
| 22.5.6 X Plugin Options and Variables 4072                              |      |
| 22.5.7 Monitoring X Plugin                                              | 4092 |

This chapter introduces an alternative way of working with MySQL as a document store, sometimes referred to as "using NoSQL". If your intention is to use MySQL in a traditional (SQL) way, this chapter is probably not relevant to you.

Traditionally, relational databases such as MySQL have usually required a schema to be defined before documents can be stored. The features described in this section enable you to use MySQL as a document store, which is a schema-less, and therefore schema-flexible, storage system for documents. For example, when you create documents describing products, you do not need to know and define all possible attributes of any products before storing and operating with the documents. This differs from working with a relational database and storing products in a table, when all columns of the table must be known and defined before adding any products to the database. The features described in this chapter enable you to choose how you configure MySQL, using only the document store model, or combining the flexibility of the document store model with the power of the relational model.

To use MySQL as a document store, you use the following server features:

- X Plugin enables MySQL Server to communicate with clients using X Protocol, which is a prerequisite for using MySQL as a document store. X Plugin is enabled by default in MySQL Server as of MySQL 8.0. For instructions to verify X Plugin installation and to configure and monitor X Plugin, see [Section 22.5, "X Plugin"](#page-96-0).
- X Protocol supports both CRUD and SQL operations, authentication via SASL, allows streaming (pipelining) of commands and is extensible on the protocol and the message layer. Clients compatible with X Protocol include MySQL Shell and MySQL 8.0 Connectors.
- Clients that communicate with a MySQL Server using X Protocol can use X DevAPI to develop applications. X DevAPI offers a modern programming interface with a simple yet powerful design which provides support for established industry standard concepts. This chapter explains how to get started using either the JavaScript or Python implementation of X DevAPI in MySQL Shell as a client. See [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/) for in-depth tutorials on using X DevAPI.

# <span id="page-55-0"></span>**22.1 Interfaces to a MySQL Document Store**

To work with MySQL as a document store, you use dedicated components and a choice of clients that support communicating with the MySQL server to develop document based applications.

- The following MySQL products support X Protocol and enable you to use X DevAPI in your chosen language to develop applications that communicate with a MySQL Server functioning as a document store:
  - MySQL Shell (which provides implementations of X DevAPI in JavaScript and Python)
  - Connector/C++
  - Connector/J
  - Connector/Node.js
  - Connector/NET
  - Connector/Python
- MySQL Shell is an interactive interface to MySQL supporting JavaScript, Python, or SQL modes. You can use MySQL Shell to prototype applications, execute queries and update data. [Installing](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md) [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md) has instructions to download and install MySQL Shell.
- The quick-start guides (tutorials) in this chapter help you to get started using MySQL Shell with MySQL as a document store.

The quick-start guide for JavaScript is here: [Section 22.3, "JavaScript Quick-Start Guide: MySQL](#page-56-0) [Shell for Document Store"](#page-56-0).

The quick-start guide for Python is here: [Section 22.4, "Python Quick-Start Guide: MySQL Shell for](#page-76-0) [Document Store".](#page-76-0)

• The MySQL Shell User Guide at [MySQL Shell 8.0](https://dev.mysql.com/doc/mysql-shell/8.0/en/) provides detailed information about configuring and using MySQL Shell.

# <span id="page-55-1"></span>**22.2 Document Store Concepts**

This section explains the concepts introduced as part of using MySQL as a document store.

- [JSON Document](#page-55-2)
- [Collection](#page-56-1)
- [CRUD Operations](#page-56-2)

## <span id="page-55-2"></span>**JSON Document**

A JSON document is a data structure composed of key-value pairs and is the fundamental structure for using MySQL as document store. For example, the world\_x schema (installed later in this chapter) contains this document:

```
{
 "GNP": 4834,
 "_id": "00005de917d80000000000000023",
 "Code": "BWA",
 "Name": "Botswana",
 "IndepYear": 1966,
 "geography": {
 "Region": "Southern Africa",
 "Continent": "Africa",
```

```
 "SurfaceArea": 581730
 },
 "government": {
 "HeadOfState": "Festus G. Mogae",
 "GovernmentForm": "Republic"
 },
 "demographics": {
 "Population": 1622000,
 "LifeExpectancy": 39.29999923706055
 }
}
```

This document shows that the values of keys can be simple data types, such as integers or strings, but can also contain other documents, arrays, and lists of documents. For example, the geography key's value consists of multiple key-value pairs. A JSON document is represented internally using the MySQL binary JSON object, through the JSON MySQL datatype.

The most important differences between a document and the tables known from traditional relational databases are that the structure of a document does not have to be defined in advance, and a collection can contain multiple documents with different structures. Relational tables on the other hand require that their structure be defined, and all rows in the table must contain the same columns.

## <span id="page-56-1"></span>**Collection**

A collection is a container that is used to store JSON documents in a MySQL database. Applications usually run operations against a collection of documents, for example to find a specific document.

## <span id="page-56-2"></span>**CRUD Operations**

The four basic operations that can be issued against a collection are Create, Read, Update and Delete (CRUD). In terms of MySQL this means:

- Create a new document (insertion or addition)
- Read one or more documents (queries)
- Update one or more documents
- Delete one or more documents

# <span id="page-56-0"></span>**22.3 JavaScript Quick-Start Guide: MySQL Shell for Document Store**

This quick-start guide provides instructions to begin prototyping document store applications interactively with MySQL Shell. The guide includes the following topics:

- Introduction to MySQL functionality, MySQL Shell, and the world\_x example schema.
- Operations to manage collections and documents.
- Operations to manage relational tables.
- Operations that apply to documents within tables.

To follow this quick-start guide you need a MySQL server with X Plugin installed, the default in 8.0, and MySQL Shell to use as the client. [MySQL Shell 8.0](https://dev.mysql.com/doc/mysql-shell/8.0/en/) provides more in-depth information about MySQL Shell. The Document Store is accessed using X DevAPI, and MySQL Shell provides this API in both JavaScript and Python.

## **Related Information**

• [MySQL Shell 8.0](https://dev.mysql.com/doc/mysql-shell/8.0/en/) provides more in-depth information about MySQL Shell.

- See [Installing MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md) and [Section 22.5, "X Plugin"](#page-96-0) for more information about the tools used in this quick-start guide.
- [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/) provides more examples of using X DevAPI to develop applications which use Document Store.
- A [Python](#page-76-0) quick-start guide is also available.

## <span id="page-57-0"></span>**22.3.1 MySQL Shell**

This quick-start guide assumes a certain level of familiarity with MySQL Shell. The following section is a high level overview, see the MySQL Shell documentation for more information. MySQL Shell is a unified scripting interface to MySQL Server. It supports scripting in JavaScript and Python. JavaScript is the default processing mode.

## **Start MySQL Shell**

After you have installed and started MySQL server, connect MySQL Shell to the server instance. You need to know the address of the MySQL server instance you plan to connect to. To be able to use the instance as a Document Store, the server instance must have X Plugin installed and you should connect to the server using X Protocol. For example to connect to the instance ds1.example.com on the default X Protocol port of 33060 use the network string user@ds1.example.com:33060.

![](_page_57_Picture_8.jpeg)

#### **Tip**

If you connect to the instance using classic MySQL protocol, for example by using the default port of 3306 instead of the [mysqlx\\_port](#page-111-0), you cannot use the Document Store functionality shown in this tutorial. For example the db global object is not populated. To use the Document Store, always connect using X Protocol.

If MySQL Shell is not already running, open a terminal window and issue:

**mysqlsh user@ds1.example.com:33060/world\_x**

Alternatively, if MySQL Shell is already running use the \connect command by issuing:

**\connect user@ds1.example.com:33060/world\_x**

You need to specify the address of the MySQL server instance which you want to connect MySQL Shell to. For example in the previous example:

- user represents the user name of your MySQL account.
- ds1.example.com is the hostname of the server instance running MySQL. Replace this with the hostname of the MySQL server instance you are using as a Document Store.
- The default schema for this session is world\_x. For instructions on setting up the world\_x schema, see [Section 22.3.2, "Download and Import world\\_x Database"](#page-58-0).

For more information, see Section 6.2.5, "Connecting to the Server Using URI-Like Strings or Key-Value Pairs".

Once MySQL Shell opens, the mysql-js> prompt indicates that the active language for this session is JavaScript.

mysql-js>

MySQL Shell supports input-line editing as follows:

- **left-arrow** and **right-arrow** keys move horizontally within the current input line.
- **up-arrow** and **down-arrow** keys move up and down through the set of previously entered lines.

- **Backspace** deletes the character before the cursor and typing new characters enters them at the cursor position.
- **Enter** sends the current input line to the server.

## **Get Help for MySQL Shell**

Type mysqlsh --help at the prompt of your command interpreter for a list of command-line options.

```
mysqlsh --help
```

Type \help at the MySQL Shell prompt for a list of available commands and their descriptions.

```
mysql-js> \help
```

Type \help followed by a command name for detailed help about an individual MySQL Shell command. For example, to view help on the \connect command, issue:

```
mysql-js> \help \connect
```

## **Quit MySQL Shell**

To quit MySQL Shell, issue the following command:

```
mysql-js> \quit
```

## **Related Information**

- See [Interactive Code Execution](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-interactive-code-execution.md) for an explanation of how interactive code execution works in MySQL Shell.
- See [Getting Started with MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-getting-started.md) to learn about session and connection alternatives.

# <span id="page-58-0"></span>**22.3.2 Download and Import world\_x Database**

As part of this quick-start guide, an example schema is provided which is referred to as the world\_x schema. Many of the examples demonstrate Document Store functionality using this schema. Start your MySQL server so that you can load the world\_x schema, then follow these steps:

- 1. Download [world\\_x-db.zip.](http://downloads.mysql.com/docs/world_x-db.zip)
- 2. Extract the installation archive to a temporary location such as /tmp/. Unpacking the archive results in a single file named world\_x.sql.
- 3. Import the world\_x.sql file to your server. You can either:
  - Start MySQL Shell in SQL mode and import the file by issuing:

```
mysqlsh -u root --sql --file /tmp/world_x-db/world_x.sql
Enter password: ****
```

• Set MySQL Shell to SQL mode while it is running and source the schema file by issuing:

```
\sql
Switching to SQL mode... Commands end with ;
\source /tmp/world_x-db/world_x.sql
```

Replace /tmp/ with the path to the world\_x.sql file on your system. Enter your password if prompted. A non-root account can be used as long as the account has privileges to create new schemas.

## **The world\_x Schema**

The world\_x example schema contains the following JSON collection and relational tables:

- Collection
  - countryinfo: Information about countries in the world.
- Tables
  - country: Minimal information about countries of the world.
  - city: Information about some of the cities in those countries.
  - countrylanguage: Languages spoken in each country.

## **Related Information**

• [MySQL Shell Sessions](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-sessions.md) explains session types.

## <span id="page-59-0"></span>**22.3.3 Documents and Collections**

When you are using MySQL as a Document Store, collections are containers within a schema that you can create, list, and drop. Collections contain JSON documents that you can add, find, update, and remove.

The examples in this section use the countryinfo collection in the world\_x schema. For instructions on setting up the world\_x schema, see [Section 22.3.2, "Download and Import world\\_x](#page-58-0) [Database"](#page-58-0).

## **Documents**

In MySQL, documents are represented as JSON objects. Internally, they are stored in an efficient binary format that enables fast lookups and updates.

• Simple document format for JavaScript:

```
{field1: "value", field2 : 10, "field 3": null}
```

An array of documents consists of a set of documents separated by commas and enclosed within [ and ] characters.

• Simple array of documents for JavaScript:

```
[{"Name": "Aruba", "Code:": "ABW"}, {"Name": "Angola", "Code:": "AGO"}]
```

MySQL supports the following JavaScript value types in JSON documents:

- numbers (integer and floating point)
- strings
- boolean (False and True)
- null
- arrays of more JSON values
- nested (or embedded) objects of more JSON values

## **Collections**

Collections are containers for documents that share a purpose and possibly share one or more indexes. Each collection has a unique name and exists within a single schema.

The term schema is equivalent to a database, which means a group of database objects as opposed to a relational schema, used to enforce structure and constraints over data. A schema does not enforce conformity on the documents in a collection.

In this quick-start guide:

• Basic objects include:

| Object form         | Description                                                                                                                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| db                  | db is a global variable assigned to the current<br>active schema. When you want to run operations<br>against the schema, for example to retrieve a<br>collection, you use methods available for the db<br>variable. |
| db.getCollections() | db.getCollections() returns a list of collections<br>in the schema. Use the list to get references to<br>collection objects, iterate over them, and so on.                                                          |

• Basic operations scoped by collections include:

| Operation form   | Description                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| db.name.add()    | The add() method inserts one document or a list<br>of documents into the named collection.    |
| db.name.find()   | The find() method returns some or all documents<br>in the named collection.                   |
| db.name.modify() | The modify() method updates documents in the<br>named collection.                             |
| db.name.remove() | The remove() method deletes one document or a<br>list of documents from the named collection. |

## **Related Information**

- See [Working with Collections](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-collections.md) for a general overview.
- [CRUD EBNF Definitions](https://dev.mysql.com/doc/x-devapi-userguide/en/mysql-x-crud-ebnf-definitions.md) provides a complete list of operations.