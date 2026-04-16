---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL Keyring originally implemented keystore capabilities using server plugins, but began transitioning to use the component infrastructure in MySQL 8.0. The transition includes revising the underlying implementation of keyring plugins to use the component infrastructure. This is facilitated using the plugin named daemon\_keyring\_proxy\_plugin that acts as a bridge between the plugin and component service APIs, and enables keyring plugins to continue to be used with no change to user-visible characteristics.

daemon\_keyring\_proxy\_plugin is built in and nothing need be done to install or enable it.

# <span id="page-122-1"></span>**7.6.9 MySQL Plugin Services**

MySQL server plugins have access to server "plugin services." The plugin services interface complements the plugin API by exposing server functionality that plugins can call. For developer information about writing plugin services, see [MySQL Services for Plugins.](https://dev.mysql.com/doc/extending-mysql/8.4/en/services-for-plugins.md) The following sections describe plugin services available at the SQL and C-language levels.

# <span id="page-122-0"></span>**7.6.9.1 The Locking Service**

MySQL distributions provide a locking interface that is accessible at two levels:

- At the SQL level, as a set of loadable functions that each map onto calls to the service routines.
- As a C language interface, callable as a plugin service from server plugins or loadable functions.

For general information about plugin services, see [Section 7.6.9, "MySQL Plugin Services"](#page-122-1). For general information about loadable functions, see [Adding a Loadable Function.](https://dev.mysql.com/doc/extending-mysql/8.4/en/adding-loadable-function.md)

The locking interface has these characteristics:

- Locks have three attributes: Lock namespace, lock name, and lock mode:
  - Locks are identified by the combination of namespace and lock name. The namespace enables different applications to use the same lock names without colliding by creating locks in separate namespaces. For example, if applications A and B use namespaces of ns1 and ns2, respectively, each application can use lock names lock1 and lock2 without interfering with the other application.
  - A lock mode is either read or write. Read locks are shared: If a session has a read lock on a given lock identifier, other sessions can acquire a read lock on the same identifier. Write locks are exclusive: If a session has a write lock on a given lock identifier, other sessions cannot acquire a read or write lock on the same identifier.
- Namespace and lock names must be non-NULL, nonempty, and have a maximum length of 64 characters. A namespace or lock name specified as NULL, the empty string, or a string longer than 64 characters results in an [ER\\_LOCKING\\_SERVICE\\_WRONG\\_NAME](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_locking_service_wrong_name) error.
- The locking interface treats namespace and lock names as binary strings, so comparisons are casesensitive.

- The locking interface provides functions to acquire locks and release locks. No special privilege is required to call these functions. Privilege checking is the responsibility of the calling application.
- Locks can be waited for if not immediately available. Lock acquisition calls take an integer timeout value that indicates how many seconds to wait to acquire locks before giving up. If the timeout is reached without successful lock acquisition, an [ER\\_LOCKING\\_SERVICE\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_locking_service_timeout) error occurs. If the timeout is 0, there is no waiting and the call produces an error if locks cannot be acquired immediately.
- The locking interface detects deadlock between lock-acquisition calls in different sessions. In this case, the locking service chooses a caller and terminates its lock-acquisition request with an [ER\\_LOCKING\\_SERVICE\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_locking_service_deadlock) error. This error does not cause transactions to roll back. To choose a session in case of deadlock, the locking service prefers sessions that hold read locks over sessions that hold write locks.
- A session can acquire multiple locks with a single lock-acquisition call. For a given call, lock acquisition is atomic: The call succeeds if all locks are acquired. If acquisition of any lock fails, the call acquires no locks and fails, typically with an [ER\\_LOCKING\\_SERVICE\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_locking_service_timeout) or [ER\\_LOCKING\\_SERVICE\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_locking_service_deadlock) error.
- A session can acquire multiple locks for the same lock identifier (namespace and lock name combination). These lock instances can be read locks, write locks, or a mix of both.
- Locks acquired within a session are released explicitly by calling a release-locks function, or implicitly when the session terminates (either normally or abnormally). Locks are not released when transactions commit or roll back.
- Within a session, all locks for a given namespace when released are released together.

The interface provided by the locking service is distinct from that provided by GET\_LOCK() and related SQL functions (see Section 14.14, "Locking Functions"). For example, GET\_LOCK() does not implement namespaces and provides only exclusive locks, not distinct read and write locks.

#### <span id="page-123-0"></span>**The Locking Service C Interface**

This section describes how to use the locking service C language interface. To use the function interface instead, see [The Locking Service Function Interface](#page-124-0) For general characteristics of the locking service interface, see [Section 7.6.9.1, "The Locking Service".](#page-122-0) For general information about plugin services, see [Section 7.6.9, "MySQL Plugin Services".](#page-122-1)

Source files that use the locking service should include this header file:

```
#include <mysql/service_locking.h>
```

To acquire one or more locks, call this function:

```
int mysql_acquire_locking_service_locks(MYSQL_THD opaque_thd,
 const char* lock_namespace,
 const char**lock_names,
 size_t lock_num,
 enum enum_locking_service_lock_type lock_type,
 unsigned long lock_timeout);
```

The arguments have these meanings:

- opaque\_thd: A thread handle. If specified as NULL, the handle for the current thread is used.
- lock\_namespace: A null-terminated string that indicates the lock namespace.
- lock\_names: An array of null-terminated strings that provides the names of the locks to acquire.
- lock\_num: The number of names in the lock\_names array.

- lock\_type: The lock mode, either LOCKING\_SERVICE\_READ or LOCKING\_SERVICE\_WRITE to acquire read locks or write locks, respectively.
- lock\_timeout: An integer number of seconds to wait to acquire the locks before giving up.

To release locks acquired for a given namespace, call this function:

```
int mysql_release_locking_service_locks(MYSQL_THD opaque_thd,
 const char* lock_namespace);
```

The arguments have these meanings:

- opaque\_thd: A thread handle. If specified as NULL, the handle for the current thread is used.
- lock\_namespace: A null-terminated string that indicates the lock namespace.

Locks acquired or waited for by the locking service can be monitored at the SQL level using the Performance Schema. For details, see [Locking Service Monitoring](#page-126-0).

## <span id="page-124-0"></span>**The Locking Service Function Interface**

This section describes how to use the locking service interface provided by its loadable functions. To use the C language interface instead, see [The Locking Service C Interface](#page-123-0) For general characteristics of the locking service interface, see [Section 7.6.9.1, "The Locking Service"](#page-122-0). For general information about loadable functions, see [Adding a Loadable Function](https://dev.mysql.com/doc/extending-mysql/8.4/en/adding-loadable-function.md).

- [Installing or Uninstalling the Locking Service Function Interface](#page-124-1)
- [Using the Locking Service Function Interface](#page-125-0)
- [Locking Service Monitoring](#page-126-0)
- [Locking Service Interface Function Reference](#page-127-0)

#### <span id="page-124-1"></span>**Installing or Uninstalling the Locking Service Function Interface**

The locking service routines described in [The Locking Service C Interface](#page-123-0) need not be installed because they are built into the server. The same is not true of the loadable functions that map onto calls to the service routines: The functions must be installed before use. This section describes how to do that. For general information about loadable function installation, see [Section 7.7.1, "Installing and](#page-130-0) [Uninstalling Loadable Functions"](#page-130-0).

The locking service functions are implemented in a plugin library file located in the directory named by the plugin\_dir system variable. The file base name is locking\_service. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To install the locking service functions, use the CREATE FUNCTION statement, adjusting the .so suffix for your platform as necessary:

```
CREATE FUNCTION service_get_read_locks RETURNS INT
 SONAME 'locking_service.so';
CREATE FUNCTION service_get_write_locks RETURNS INT
 SONAME 'locking_service.so';
CREATE FUNCTION service_release_locks RETURNS INT
 SONAME 'locking_service.so';
```

If the functions are used on a replication source server, install them on all replica servers as well to avoid replication problems.

Once installed, the functions remain installed until uninstalled. To remove them, use the DROP FUNCTION statement:

```
DROP FUNCTION service_get_read_locks;
```

```
DROP FUNCTION service_get_write_locks;
DROP FUNCTION service_release_locks;
```

#### <span id="page-125-0"></span>**Using the Locking Service Function Interface**

Before using the locking service functions, install them according to the instructions provided at [Installing or Uninstalling the Locking Service Function Interface](#page-124-1).

To acquire one or more read locks, call this function:

```
mysql> SELECT service_get_read_locks('mynamespace', 'rlock1', 'rlock2', 10);
+---------------------------------------------------------------+
| service_get_read_locks('mynamespace', 'rlock1', 'rlock2', 10) |
+---------------------------------------------------------------+
| 1 |
+---------------------------------------------------------------+
```

The first argument is the lock namespace. The final argument is an integer timeout indicating how many seconds to wait to acquire the locks before giving up. The arguments in between are the lock names.

For the example just shown, the function acquires locks with lock identifiers (mynamespace, rlock1) and (mynamespace, rlock2).

To acquire write locks rather than read locks, call this function:

```
mysql> SELECT service_get_write_locks('mynamespace', 'wlock1', 'wlock2', 10);
+----------------------------------------------------------------+
| service_get_write_locks('mynamespace', 'wlock1', 'wlock2', 10) |
+----------------------------------------------------------------+
| 1 |
+----------------------------------------------------------------+
```

In this case, the lock identifiers are (mynamespace, wlock1) and (mynamespace, wlock2).

To release all locks for a namespace, use this function:

```
mysql> SELECT service_release_locks('mynamespace');
+--------------------------------------+
| service_release_locks('mynamespace') |
+--------------------------------------+
| 1 |
+--------------------------------------+
```

Each locking function returns nonzero for success. If the function fails, an error occurs. For example, the following error occurs because lock names cannot be empty:

```
mysql> SELECT service_get_read_locks('mynamespace', '', 10);
ERROR 3131 (42000): Incorrect locking service lock name ''.
```

A session can acquire multiple locks for the same lock identifier. As long as a different session does not have a write lock for an identifier, the session can acquire any number of read or write locks. Each lock request for the identifier acquires a new lock. The following statements acquire three write locks with the same identifier, then three read locks for the same identifier:

```
SELECT service_get_write_locks('ns', 'lock1', 'lock1', 'lock1', 0);
SELECT service_get_read_locks('ns', 'lock1', 'lock1', 'lock1', 0);
```

If you examine the Performance Schema metadata\_locks table at this point, you should find that the session holds six distinct locks with the same (ns, lock1) identifier. (For details, see [Locking](#page-126-0) [Service Monitoring.](#page-126-0))

Because the session holds at least one write lock on (ns, lock1), no other session can acquire a lock for it, either read or write. If the session held only read locks for the identifier, other sessions could acquire read locks for it, but not write locks.

Locks for a single lock-acquisition call are acquired atomically, but atomicity does not hold across calls. Thus, for a statement such as the following, where [service\\_get\\_write\\_locks\(\)](#page-127-1) is called once per row of the result set, atomicity holds for each individual call, but not for the statement as a whole:

SELECT service\_get\_write\_locks('ns', 'lock1', 'lock2', 0) FROM t1 WHERE ... ;

![](_page_126_Picture_3.jpeg)

#### **Caution**

Because the locking service returns a separate lock for each successful request for a given lock identifier, it is possible for a single statement to acquire a large number of locks. For example:

```
INSERT INTO ... SELECT service_get_write_locks('ns', t1.col_name, 0) FROM t1;
```

These types of statements may have certain adverse effects. For example, if the statement fails part way through and rolls back, locks acquired up to the point of failure still exist. If the intent is for there to be a correspondence between rows inserted and locks acquired, that intent is not satisfied. Also, if it is important that locks are granted in a certain order, be aware that result set order may differ depending on which execution plan the optimizer chooses. For these reasons, it may be best to limit applications to a single lock-acquisition call per statement.

#### <span id="page-126-0"></span>**Locking Service Monitoring**

The locking service is implemented using the MySQL Server metadata locks framework, so you monitor locking service locks acquired or waited for by examining the Performance Schema metadata\_locks table.

First, enable the metadata lock instrument:

```
mysql> UPDATE performance_schema.setup_instruments SET ENABLED = 'YES'
 -> WHERE NAME = 'wait/lock/metadata/sql/mdl';
```

Then acquire some locks and check the contents of the metadata\_locks table:

```
mysql> SELECT service_get_write_locks('mynamespace', 'lock1', 0);
+----------------------------------------------------+
| service_get_write_locks('mynamespace', 'lock1', 0) |
+----------------------------------------------------+
| 1 |
+----------------------------------------------------+
mysql> SELECT service_get_read_locks('mynamespace', 'lock2', 0);
+---------------------------------------------------+
| service_get_read_locks('mynamespace', 'lock2', 0) |
+---------------------------------------------------+
| 1 |
+---------------------------------------------------+
mysql> SELECT OBJECT_TYPE, OBJECT_SCHEMA, OBJECT_NAME, LOCK_TYPE, LOCK_STATUS
 -> FROM performance_schema.metadata_locks
 -> WHERE OBJECT_TYPE = 'LOCKING SERVICE'\G
*************************** 1. row ***************************
 OBJECT_TYPE: LOCKING SERVICE
OBJECT_SCHEMA: mynamespace
 OBJECT_NAME: lock1
 LOCK_TYPE: EXCLUSIVE
 LOCK_STATUS: GRANTED
*************************** 2. row ***************************
 OBJECT_TYPE: LOCKING SERVICE
OBJECT_SCHEMA: mynamespace
 OBJECT_NAME: lock2
 LOCK_TYPE: SHARED
 LOCK_STATUS: GRANTED
```

Locking service locks have an OBJECT\_TYPE value of LOCKING SERVICE. This is distinct from, for example, locks acquired with the GET\_LOCK() function, which have an OBJECT\_TYPE of USER LEVEL LOCK.

The lock namespace, name, and mode appear in the OBJECT\_SCHEMA, OBJECT\_NAME, and LOCK\_TYPE columns. Read and write locks have LOCK\_TYPE values of SHARED and EXCLUSIVE, respectively.

The LOCK\_STATUS value is GRANTED for an acquired lock, PENDING for a lock that is being waited for. You can expect to see PENDING if one session holds a write lock and another session is attempting to acquire a lock having the same identifier.

#### <span id="page-127-0"></span>**Locking Service Interface Function Reference**

The SQL interface to the locking service implements the loadable functions described in this section. For usage examples, see [Using the Locking Service Function Interface](#page-125-0).

The functions share these characteristics:

- The return value is nonzero for success. Otherwise, an error occurs.
- Namespace and lock names must be non-NULL, nonempty, and have a maximum length of 64 characters.
- Timeout values must be integers indicating how many seconds to wait to acquire locks before giving up with an error. If the timeout is 0, there is no waiting and the function produces an error if locks cannot be acquired immediately.

These locking service functions are available:

```
• service_get_read_locks(namespace, lock_name[, lock_name] ..., timeout)
```

Acquires one or more read (shared) locks in the given namespace using the given lock names, timing out with an error if the locks are not acquired within the given timeout value.

```
• service_get_write_locks(namespace, lock_name[, lock_name] ..., timeout)
```

Acquires one or more write (exclusive) locks in the given namespace using the given lock names, timing out with an error if the locks are not acquired within the given timeout value.

<span id="page-127-3"></span>• [service\\_release\\_locks\(](#page-127-3)namespace)

For the given namespace, releases all locks that were acquired within the current session using [service\\_get\\_read\\_locks\(\)](#page-127-2) and [service\\_get\\_write\\_locks\(\)](#page-127-1).

It is not an error for there to be no locks in the namespace.