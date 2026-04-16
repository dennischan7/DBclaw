---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The functions shown in [Table 9.101](#page-44-0) provide native access to files on the machine hosting the server. Only files within the database cluster directory and the log\_directory can be accessed, unless the user is a superuser or is granted the role pg\_read\_server\_files. Use a relative path for files in the cluster directory, and a path matching the log\_directory configuration setting for log files.

Note that granting users the EXECUTE privilege on pg\_read\_file(), or related functions, allows them the ability to read any file on the server that the database server process can read; these functions bypass all in-database privilege checks. This means that, for example, a user with such access is able to read the contents of the pg\_authid table where authentication information is stored, as well as read any table data in the database. Therefore, granting access to these functions should be carefully considered.

When granting privilege on these functions, note that the table entries showing optional parameters are mostly implemented as several physical functions with different parameter lists. Privilege must be granted separately on each such function, if it is to be used. psql's \df command can be useful to check what the actual function signatures are.

Some of these functions take an optional missing\_ok parameter, which specifies the behavior when the file or directory does not exist. If true, the function returns NULL or an empty result set, as appropriate. If false, an error is raised. (Failure conditions other than "file not found" are reported as errors in any case.) The default is false.

### <span id="page-44-0"></span>**Table 9.101. Generic File Access Functions**

#### **Function**

#### **Description**

pg\_ls\_dir ( dirname text [, missing\_ok boolean, include\_dot\_dirs boolean ] ) → setof text

Returns the names of all files (and directories and other special files) in the specified directory. The include\_dot\_dirs parameter indicates whether "." and ".." are to be included in the result set; the default is to exclude them. Including them can be useful when missing\_ok is true, to distinguish an empty directory from a non-existent directory.

This function is restricted to superusers by default, but other users can be granted EXE-CUTE to run the function.

pg\_ls\_logdir () → setof record ( name text, size bigint, modification timestamp with time zone )

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's log directory. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and roles with privileges of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

pg\_ls\_waldir () → setof record ( name text, size bigint, modification timestamp with time zone )

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's write-ahead log (WAL) directory. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and roles with privileges of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

pg\_ls\_logicalmapdir () → setof record ( name text, size bigint, modification timestamp with time zone )

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's pg\_logical/mappings directory. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and members of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

pg\_ls\_logicalsnapdir () → setof record ( name text, size bigint, modification timestamp with time zone )

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's pg\_logical/snapshots directory. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and members of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

pg\_ls\_replslotdir ( slot\_name text ) → setof record ( name text, size bigint, modification timestamp with time zone )

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's pg\_replslot/slot\_name directory, where slot\_name is the name of the replication slot provided as input of the function. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and members of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

pg\_ls\_archive\_statusdir () → setof record ( name text, size bigint, modification timestamp with time zone )

#### **Description**

Returns the name, size, and last modification time (mtime) of each ordinary file in the server's WAL archive status directory (pg\_wal/archive\_status). Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and members of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

```
pg_ls_tmpdir ( [ tablespace oid ] ) → setof record ( name text, size big-
      int, modification timestamp with time zone )
```

Returns the name, size, and last modification time (mtime) of each ordinary file in the temporary file directory for the specified tablespace. If tablespace is not provided, the pg\_default tablespace is examined. Filenames beginning with a dot, directories, and other special files are excluded.

This function is restricted to superusers and members of the pg\_monitor role by default, but other users can be granted EXECUTE to run the function.

```
pg_read_file ( filename text [, offset bigint, length bigint ] [, miss-
      ing_ok boolean ] ) → text
```

Returns all or part of a text file, starting at the given byte offset, returning at most length bytes (less if the end of file is reached first). If offset is negative, it is relative to the end of the file. If offset and length are omitted, the entire file is returned. The bytes read from the file are interpreted as a string in the database's encoding; an error is thrown if they are not valid in that encoding.

This function is restricted to superusers by default, but other users can be granted EXE-CUTE to run the function.

```
pg_read_binary_file ( filename text [, offset bigint, length bigint ] [,
      missing_ok boolean ] ) → bytea
```

Returns all or part of a file. This function is identical to pg\_read\_file except that it can read arbitrary binary data, returning the result as bytea not text; accordingly, no encoding checks are performed.

This function is restricted to superusers by default, but other users can be granted EXE-CUTE to run the function.

In combination with the convert\_from function, this function can be used to read a text file in a specified encoding and convert to the database's encoding:

```
SELECT
 convert_from(pg_read_binary_file('file_in_utf8.txt'),
 'UTF8');
```

pg\_stat\_file ( filename text [, missing\_ok boolean ] ) → record ( size bigint, access timestamp with time zone, modification timestamp with time zone, change timestamp with time zone, creation timestamp with time zone, isdir boolean )

Returns a record containing the file's size, last access time stamp, last modification time stamp, last file status change time stamp (Unix platforms only), file creation time stamp (Windows only), and a flag indicating if it is a directory.

This function is restricted to superusers by default, but other users can be granted EXE-CUTE to run the function.

## <span id="page-45-0"></span>**9.27.10. Advisory Lock Functions**

The functions shown in [Table 9.102](#page-46-0) manage advisory locks. For details about proper use of these functions, see [Section 13.3.5.](#page-134-0)

All these functions are intended to be used to lock application-defined resources, which can be identified either by a single 64-bit key value or two 32-bit key values (note that these two key spaces do not overlap). If another session already holds a conflicting lock on the same resource identifier, the functions will either wait until the resource becomes available, or return a false result, as appropriate for the function. Locks can be either shared or exclusive: a shared lock does not conflict with other shared locks on the same resource, only with exclusive locks. Locks can be taken at session level (so that they are held until released or the session ends) or at transaction level (so that they are held until the current transaction ends; there is no provision for manual release). Multiple session-level lock requests stack, so that if the same resource identifier is locked three times there must then be three unlock requests to release the resource in advance of session end.

## <span id="page-46-0"></span>**Table 9.102. Advisory Lock Functions**

```
Function
       Description
pg_advisory_lock ( key bigint ) → void
pg_advisory_lock ( key1 integer, key2 integer ) → void
       Obtains an exclusive session-level advisory lock, waiting if necessary.
pg_advisory_lock_shared ( key bigint ) → void
pg_advisory_lock_shared ( key1 integer, key2 integer ) → void
       Obtains a shared session-level advisory lock, waiting if necessary.
pg_advisory_unlock ( key bigint ) → boolean
pg_advisory_unlock ( key1 integer, key2 integer ) → boolean
       Releases a previously-acquired exclusive session-level advisory lock. Returns true if
       the lock is successfully released. If the lock was not held, false is returned, and in ad-
       dition, an SQL warning will be reported by the server.
pg_advisory_unlock_all () → void
       Releases all session-level advisory locks held by the current session. (This function is
       implicitly invoked at session end, even if the client disconnects ungracefully.)
pg_advisory_unlock_shared ( key bigint ) → boolean
pg_advisory_unlock_shared ( key1 integer, key2 integer ) → boolean
       Releases a previously-acquired shared session-level advisory lock. Returns true if the
       lock is successfully released. If the lock was not held, false is returned, and in addi-
       tion, an SQL warning will be reported by the server.
pg_advisory_xact_lock ( key bigint ) → void
pg_advisory_xact_lock ( key1 integer, key2 integer ) → void
       Obtains an exclusive transaction-level advisory lock, waiting if necessary.
pg_advisory_xact_lock_shared ( key bigint ) → void
pg_advisory_xact_lock_shared ( key1 integer, key2 integer ) → void
       Obtains a shared transaction-level advisory lock, waiting if necessary.
pg_try_advisory_lock ( key bigint ) → boolean
pg_try_advisory_lock ( key1 integer, key2 integer ) → boolean
       Obtains an exclusive session-level advisory lock if available. This will either obtain the
       lock immediately and return true, or return false without waiting if the lock cannot
       be acquired immediately.
pg_try_advisory_lock_shared ( key bigint ) → boolean
pg_try_advisory_lock_shared ( key1 integer, key2 integer ) → boolean
       Obtains a shared session-level advisory lock if available. This will either obtain the lock
       immediately and return true, or return false without waiting if the lock cannot be ac-
```

quired immediately.

#### **Description**

```
pg_try_advisory_xact_lock ( key bigint ) → boolean
pg_try_advisory_xact_lock ( key1 integer, key2 integer ) → boolean
       Obtains an exclusive transaction-level advisory lock if available. This will either obtain
       the lock immediately and return true, or return false without waiting if the lock can-
       not be acquired immediately.
```

```
pg_try_advisory_xact_lock_shared ( key bigint ) → boolean
pg_try_advisory_xact_lock_shared ( key1 integer, key2 integer ) →
      boolean
```

Obtains a shared transaction-level advisory lock if available. This will either obtain the lock immediately and return true, or return false without waiting if the lock cannot be acquired immediately.