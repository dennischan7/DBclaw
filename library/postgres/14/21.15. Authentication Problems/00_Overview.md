---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Authentication failures and related problems generally manifest themselves through error messages like the following:

```
FATAL: no pg_hba.conf entry for host "123.123.123.123", user
 "andym", database "testdb"
```

This is what you are most likely to get if you succeed in contacting the server, but it does not want to talk to you. As the message suggests, the server refused the connection request because it found no matching entry in its pg\_hba.conf configuration file.

```
FATAL: password authentication failed for user "andym"
```

Messages like this indicate that you contacted the server, and it is willing to talk to you, but not until you pass the authorization method specified in the pg\_hba.conf file. Check the password you are providing, or check your Kerberos or ident software if the complaint mentions one of those authentication types.

FATAL: user "andym" does not exist

The indicated database user name was not found.

FATAL: database "testdb" does not exist

The database you are trying to connect to does not exist. Note that if you do not specify a database name, it defaults to the database user name, which might or might not be the right thing.

### **Tip**

The server log might contain more information about an authentication failure than is reported to the client. If you are confused about the reason for a failure, check the server log.

# <span id="page-119-0"></span>**Chapter 22. Database Roles**

PostgreSQL manages database access permissions using the concept of *roles*. A role can be thought of as either a database user, or a group of database users, depending on how the role is set up. Roles can own database objects (for example, tables and functions) and can assign privileges on those objects to other roles to control who has access to which objects. Furthermore, it is possible to grant *membership* in a role to another role, thus allowing the member role to use privileges assigned to another role.

The concept of roles subsumes the concepts of "users" and "groups". In PostgreSQL versions before 8.1, users and groups were distinct kinds of entities, but now there are only roles. Any role can act as a user, a group, or both.

This chapter describes how to create and manage roles. More information about the effects of role privileges on various database objects can be found in Section 5.7.