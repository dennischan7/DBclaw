---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes functions used to manipulate user-level locks.

**Table 14.19 Locking Functions**

| Name                | Description                                                               |
|---------------------|---------------------------------------------------------------------------|
| GET_LOCK()          | Get a named lock                                                          |
| IS_FREE_LOCK()      | Whether the named lock is free                                            |
| IS_USED_LOCK()      | Whether the named lock is in use; return<br>connection identifier if true |
| RELEASE_ALL_LOCKS() | Release all current named locks                                           |
| RELEASE_LOCK()      | Release the named lock                                                    |

<span id="page-82-1"></span>• [GET\\_LOCK\(](#page-82-1)str,timeout)

Tries to obtain a lock with a name given by the string str, using a timeout of timeout seconds. A negative timeout value means infinite timeout. The lock is exclusive. While held by one session, other sessions cannot obtain a lock of the same name.

Returns 1 if the lock was obtained successfully, 0 if the attempt timed out (for example, because another client has previously locked the name), or NULL if an error occurred (such as running out of memory or the thread was killed with mysqladmin kill).

A lock obtained with [GET\\_LOCK\(\)](#page-82-1) is released explicitly by executing [RELEASE\\_LOCK\(\)](#page-84-3) or implicitly when your session terminates (either normally or abnormally). Locks obtained with [GET\\_LOCK\(\)](#page-82-1) are not released when transactions commit or roll back.

[GET\\_LOCK\(\)](#page-82-1) is implemented using the metadata locking (MDL) subsystem. Multiple simultaneous locks can be acquired and [GET\\_LOCK\(\)](#page-82-1) does not release any existing locks. For example, suppose that you execute these statements:

```
SELECT GET_LOCK('lock1',10);
SELECT GET_LOCK('lock2',10);
SELECT RELEASE_LOCK('lock2');
SELECT RELEASE_LOCK('lock1');
```

The second [GET\\_LOCK\(\)](#page-82-1) acquires a second lock and both [RELEASE\\_LOCK\(\)](#page-84-3) calls return 1 (success).

It is even possible for a given session to acquire multiple locks for the same name. Other sessions cannot acquire a lock with that name until the acquiring session releases all its locks for the name.

Uniquely named locks acquired with [GET\\_LOCK\(\)](#page-82-1) appear in the Performance Schema metadata\_locks table. The OBJECT\_TYPE column says USER LEVEL LOCK and the OBJECT\_NAME column indicates the lock name. In the case that multiple locks are acquired for the same name, only the first lock for the name registers a row in the metadata\_locks table. Subsequent locks for the name increment a counter in the lock but do not acquire additional metadata locks. The metadata\_locks row for the lock is deleted when the last lock instance on the name is released.

The capability of acquiring multiple locks means there is the possibility of deadlock among clients. When this happens, the server chooses a caller and terminates its lock-acquisition request with an [ER\\_USER\\_LOCK\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_user_lock_deadlock) error. This error does not cause transactions to roll back.

MySQL enforces a maximum length on lock names of 64 characters.

[GET\\_LOCK\(\)](#page-82-1) can be used to implement application locks or to simulate record locks. Names are locked on a server-wide basis. If a name has been locked within one session, [GET\\_LOCK\(\)](#page-82-1) blocks any request by another session for a lock with the same name. This enables clients that agree on a given lock name to use the name to perform cooperative advisory locking. But be aware that it also enables a client that is not among the set of cooperating clients to lock a name, either inadvertently or deliberately, and thus prevent any of the cooperating clients from locking that name. One way to reduce the likelihood of this is to use lock names that are database-specific or application-specific. For example, use lock names of the form db\_name.str or app\_name.str.

If multiple clients are waiting for a lock, the order in which they acquire it is undefined. Applications should not assume that clients acquire the lock in the same order that they issued the lock requests.

[GET\\_LOCK\(\)](#page-82-1) is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

Since GET\_LOCK() establishes a lock only on a single mysqld, it is not suitable for use with NDB Cluster, which has no way of enforcing an SQL lock across multiple MySQL servers. See Section 25.2.7.10, "Limitations Relating to Multiple NDB Cluster Nodes", for more information.

![](_page_83_Picture_12.jpeg)

### **Caution**

With the capability of acquiring multiple named locks, it is possible for a single statement to acquire a large number of locks. For example:

```
INSERT INTO ... SELECT GET_LOCK(t1.col_name) FROM t1;
```

These types of statements may have certain adverse effects. For example, if the statement fails part way through and rolls back, locks acquired up to the point of failure still exist. If the intent is for there to be a correspondence between rows inserted and locks acquired, that intent is not satisfied. Also, if it is important that locks are granted in a certain order, be aware that

result set order may differ depending on which execution plan the optimizer chooses. For these reasons, it may be best to limit applications to a single lock-acquisition call per statement.

A different locking interface is available as either a plugin service or a set of loadable functions. This interface provides lock namespaces and distinct read and write locks, unlike the interface provided by [GET\\_LOCK\(\)](#page-82-1) and related functions. For details, see Section 7.6.9.1, "The Locking Service".

<span id="page-84-0"></span>• [IS\\_FREE\\_LOCK\(](#page-84-0)str)

Checks whether the lock named str is free to use (that is, not locked). Returns 1 if the lock is free (no one is using the lock), 0 if the lock is in use, and NULL if an error occurs (such as an incorrect argument).

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-84-1"></span>• [IS\\_USED\\_LOCK\(](#page-84-1)str)

Checks whether the lock named str is in use (that is, locked). If so, it returns the connection identifier of the client session that holds the lock. Otherwise, it returns NULL.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-84-2"></span>• [RELEASE\\_ALL\\_LOCKS\(\)](#page-84-2)

Releases all named locks held by the current session and returns the number of locks released (0 if there were none)

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.

<span id="page-84-3"></span>• [RELEASE\\_LOCK\(](#page-84-3)str)

Releases the lock named by the string str that was obtained with [GET\\_LOCK\(\)](#page-82-1). Returns 1 if the lock was released, 0 if the lock was not established by this thread (in which case the lock is not released), and NULL if the named lock did not exist. The lock does not exist if it was never obtained by a call to [GET\\_LOCK\(\)](#page-82-1) or if it has previously been released.

The DO statement is convenient to use with [RELEASE\\_LOCK\(\)](#page-84-3). See Section 15.2.3, "DO Statement".

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.