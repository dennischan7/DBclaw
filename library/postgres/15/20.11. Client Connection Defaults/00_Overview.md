---
source: PostgreSQL 15 Reference
title: 00_Overview
---

## <span id="page-83-0"></span>**20.11.1. Statement Behavior**

```
client_min_messages (enum)
```

Controls which [message levels](#page-71-0) are sent to the client. Valid values are DEBUG5, DEBUG4, DE-BUG3, DEBUG2, DEBUG1, LOG, NOTICE, WARNING, and ERROR. Each level includes all the levels that follow it. The later the level, the fewer messages are sent. The default is NOTICE. Note that LOG has a different rank here than in [log\\_min\\_messages.](#page-69-1)

INFO level messages are always sent to the client.

```
search_path (string)
```

This variable specifies the order in which schemas are searched when an object (table, data type, function, etc.) is referenced by a simple name with no schema specified. When there are objects of identical names in different schemas, the one found first in the search path is used. An object that is not in any of the schemas in the search path can only be referenced by specifying its containing schema with a qualified (dotted) name.

The value for search\_path must be a comma-separated list of schema names. Any name that is not an existing schema, or is a schema for which the user does not have USAGE permission, is silently ignored.

If one of the list items is the special name \$user, then the schema having the name returned by CURRENT\_USER is substituted, if there is such a schema and the user has USAGE permission for it. (If not, \$user is ignored.)

The system catalog schema, pg\_catalog, is always searched, whether it is mentioned in the path or not. If it is mentioned in the path then it will be searched in the specified order. If pg\_catalog is not in the path then it will be searched *before* searching any of the path items.

Likewise, the current session's temporary-table schema, pg\_temp\_nnn, is always searched if it exists. It can be explicitly listed in the path by using the alias pg\_temp. If it is not listed in the path then it is searched first (even before pg\_catalog). However, the temporary schema is only searched for relation (table, view, sequence, etc.) and data type names. It is never searched for function or operator names.

When objects are created without specifying a particular target schema, they will be placed in the first valid schema named in search\_path. An error is reported if the search path is empty.

The default value for this parameter is "\$user", public. This setting supports shared use of a database (where no users have private schemas, and all share use of public), private per-user schemas, and combinations of these. Other effects can be obtained by altering the default search path setting, either globally or per-user.

For more information on schema handling, see Section 5.9. In particular, the default configuration is suitable only when the database has a single user or a few mutually-trusting users.

The current effective value of the search path can be examined via the SQL function current\_schemas (see Section 9.26). This is not quite the same as examining the value of search\_path, since current\_schemas shows how the items appearing in search\_path were resolved.

```
row_security (boolean)
```

This variable controls whether to raise an error in lieu of applying a row security policy. When set to on, policies apply normally. When set to off, queries fail which would otherwise apply at least one policy. The default is on. Change to off where limited row visibility could cause incorrect results; for example, pg\_dump makes that change by default. This variable has no effect on roles which bypass every row security policy, to wit, superusers and roles with the BY-PASSRLS attribute.

For more information on row security policies, see CREATE POLICY.

```
default_table_access_method (string)
```

This parameter specifies the default table access method to use when creating tables or materialized views if the CREATE command does not explicitly specify an access method, or when SELECT ... INTO is used, which does not allow specifying a table access method. The default is heap.

```
default_tablespace (string)
```

This variable specifies the default tablespace in which to create objects (tables and indexes) when a CREATE command does not explicitly specify a tablespace.

The value is either the name of a tablespace, or an empty string to specify using the default tablespace of the current database. If the value does not match the name of any existing tablespace, PostgreSQL will automatically use the default tablespace of the current database. If a nondefault tablespace is specified, the user must have CREATE privilege for it, or creation attempts will fail.

This variable is not used for temporary tables; for them, [temp\\_tablespaces](#page-85-0) is consulted instead.

This variable is also not used when creating databases. By default, a new database inherits its tablespace setting from the template database it is copied from.

If this parameter is set to a value other than the empty string when a partitioned table is created, the partitioned table's tablespace will be set to that value, which will be used as the default tablespace for partitions created in the future, even if default\_tablespace has changed since then.

For more information on tablespaces, see [Section 23.6](#page-137-0).

```
default_toast_compression (enum)
```

This variable sets the default TOAST compression method for values of compressible columns. (This can be overridden for individual columns by setting the COMPRESSION column option in CREATE TABLE or ALTER TABLE.) The supported compression methods are pglz and (if PostgreSQL was compiled with --with-lz4) lz4. The default is pglz.

```
temp_tablespaces (string)
```

This variable specifies tablespaces in which to create temporary objects (temp tables and indexes on temp tables) when a CREATE command does not explicitly specify a tablespace. Temporary files for purposes such as sorting large data sets are also created in these tablespaces.

The value is a list of names of tablespaces. When there is more than one name in the list, PostgreSQL chooses a random member of the list each time a temporary object is to be created; except that within a transaction, successively created temporary objects are placed in successive tablespaces from the list. If the selected element of the list is an empty string, PostgreSQL will automatically use the default tablespace of the current database instead.

When temp\_tablespaces is set interactively, specifying a nonexistent tablespace is an error, as is specifying a tablespace for which the user does not have CREATE privilege. However, when using a previously set value, nonexistent tablespaces are ignored, as are tablespaces for which the user lacks CREATE privilege. In particular, this rule applies when using a value set in postgresql.conf.

The default value is an empty string, which results in all temporary objects being created in the default tablespace of the current database.

See also [default\\_tablespace.](#page-84-0)

```
check_function_bodies (boolean)
```

This parameter is normally on. When set to off, it disables validation of the routine body string during CREATE FUNCTION and CREATE PROCEDURE. Disabling validation avoids side effects of the validation process, in particular preventing false positives due to problems such as forward references. Set this parameter to off before loading functions on behalf of other users; pg\_dump does so automatically.

```
default_transaction_isolation (enum)
```

Each SQL transaction has an isolation level, which can be either "read uncommitted", "read committed", "repeatable read", or "serializable". This parameter controls the default isolation level of each new transaction. The default is "read committed".

Consult Chapter 13 and SET TRANSACTION for more information.

```
default_transaction_read_only (boolean)
```

A read-only SQL transaction cannot alter non-temporary tables. This parameter controls the default read-only status of each new transaction. The default is off (read/write).

Consult SET TRANSACTION for more information.

```
default_transaction_deferrable (boolean)
```

When running at the serializable isolation level, a deferrable read-only SQL transaction may be delayed before it is allowed to proceed. However, once it begins executing it does not incur any of the overhead required to ensure serializability; so serialization code will have no reason to force it to abort because of concurrent updates, making this option suitable for longrunning read-only transactions.

This parameter controls the default deferrable status of each new transaction. It currently has no effect on read-write transactions or those operating at isolation levels lower than serializable. The default is off.

Consult SET TRANSACTION for more information.

```
transaction_isolation (enum)
```

This parameter reflects the current transaction's isolation level. At the beginning of each transaction, it is set to the current value of [default\\_transaction\\_isolation](#page-85-1). Any subsequent attempt to change it is equivalent to a SET TRANSACTION command.

```
transaction_read_only (boolean)
```

This parameter reflects the current transaction's read-only status. At the beginning of each transaction, it is set to the current value of [default\\_transaction\\_read\\_only](#page-85-2). Any subsequent attempt to change it is equivalent to a SET TRANSACTION command.

```
transaction_deferrable (boolean)
```

This parameter reflects the current transaction's deferrability status. At the beginning of each transaction, it is set to the current value of [default\\_transaction\\_deferrable.](#page-85-3) Any subsequent attempt to change it is equivalent to a SET TRANSACTION command.

```
session_replication_role (enum)
```

Controls firing of replication-related triggers and rules for the current session. Possible values are origin (the default), replica and local. Setting this parameter results in discarding any previously cached query plans. Only superusers and users with the appropriate SET privilege can change this setting.

The intended use of this setting is that logical replication systems set it to replica when they are applying replicated changes. The effect of that will be that triggers and rules (that have not been altered from their default configuration) will not fire on the replica. See the ALTER TABLE clauses ENABLE TRIGGER and ENABLE RULE for more information.

PostgreSQL treats the settings origin and local the same internally. Third-party replication systems may use these two values for their internal purposes, for example using local to designate a session whose changes should not be replicated.

Since foreign keys are implemented as triggers, setting this parameter to replica also disables all foreign key checks, which can leave data in an inconsistent state if improperly used.

```
statement_timeout (integer)
```

Abort any statement that takes more than the specified amount of time. If log\_min\_error\_statement is set to ERROR or lower, the statement that timed out will also be logged. If this value is specified without units, it is taken as milliseconds. A value of zero (the default) disables the timeout.

The timeout is measured from the time a command arrives at the server until it is completed by the server. If multiple SQL statements appear in a single simple-Query message, the timeout is applied to each statement separately. (PostgreSQL versions before 13 usually treated the timeout as applying to the whole query string.) In extended query protocol, the timeout starts running when any query-related message (Parse, Bind, Execute, Describe) arrives, and it is canceled by completion of an Execute or Sync message.

Setting statement\_timeout in postgresql.conf is not recommended because it would affect all sessions.

```
lock_timeout (integer)
```

Abort any statement that waits longer than the specified amount of time while attempting to acquire a lock on a table, index, row, or other database object. The time limit applies separately to each lock acquisition attempt. The limit applies both to explicit locking requests (such as LOCK TABLE, or SELECT FOR UPDATE without NOWAIT) and to implicitly-acquired locks. If this value is specified without units, it is taken as milliseconds. A value of zero (the default) disables the timeout.

Unlike statement\_timeout, this timeout can only occur while waiting for locks. Note that if statement\_timeout is nonzero, it is rather pointless to set lock\_timeout to the same or larger value, since the statement timeout would always trigger first. If log\_min\_error\_statement is set to ERROR or lower, the statement that timed out will be logged.

Setting lock\_timeout in postgresql.conf is not recommended because it would affect all sessions.

```
idle_in_transaction_session_timeout (integer)
```

Terminate any session that has been idle (that is, waiting for a client query) within an open transaction for longer than the specified amount of time. If this value is specified without units, it is taken as milliseconds. A value of zero (the default) disables the timeout.

This option can be used to ensure that idle sessions do not hold locks for an unreasonable amount of time. Even when no significant locks are held, an open transaction prevents vacuuming away recently-dead tuples that may be visible only to this transaction; so remaining idle for a long time can contribute to table bloat. See [Section 25.1](#page-159-0) for more details.

```
idle_session_timeout (integer)
```

Terminate any session that has been idle (that is, waiting for a client query), but not within an open transaction, for longer than the specified amount of time. If this value is specified without units, it is taken as milliseconds. A value of zero (the default) disables the timeout.

Unlike the case with an open transaction, an idle session without a transaction imposes no large costs on the server, so there is less need to enable this timeout than idle\_in\_transaction\_session\_timeout.

Be wary of enforcing this timeout on connections made through connection-pooling software or other middleware, as such a layer may not react well to unexpected connection closure. It may be helpful to enable this timeout only for interactive sessions, perhaps by applying it only to particular users.

```
vacuum_freeze_table_age (integer)
```

VACUUM performs an aggressive scan if the table's pg\_class.relfrozenxid field has reached the age specified by this setting. An aggressive scan differs from a regular VACUUM in that it visits every page that might contain unfrozen XIDs or MXIDs, not just those that might contain dead tuples. The default is 150 million transactions. Although users can set this value anywhere from zero to two billion, VACUUM will silently limit the effective value to 95% of [au](#page-82-0)[tovacuum\\_freeze\\_max\\_age,](#page-82-0) so that a periodic manual VACUUM has a chance to run before an anti-wraparound autovacuum is launched for the table. For more information see [Section 25.1.5.](#page-162-0)

```
vacuum_freeze_min_age (integer)
```

Specifies the cutoff age (in transactions) that VACUUM should use to decide whether to freeze row versions while scanning a table. The default is 50 million transactions. Although users can set this value anywhere from zero to one billion, VACUUM will silently limit the effective value to half the value of [autovacuum\\_freeze\\_max\\_age](#page-82-0), so that there is not an unreasonably short time between forced autovacuums. For more information see [Section 25.1.5.](#page-162-0)

```
vacuum_failsafe_age (integer)
```

Specifies the maximum age (in transactions) that a table's pg\_class.relfrozenxid field can attain before VACUUM takes extraordinary measures to avoid system-wide transaction ID wraparound failure. This is VACUUM's strategy of last resort. The failsafe typically triggers when an autovacuum to prevent transaction ID wraparound has already been running for some time, though it's possible for the failsafe to trigger during any VACUUM.

When the failsafe is triggered, any cost-based delay that is in effect will no longer be applied, and further non-essential maintenance tasks (such as index vacuuming) are bypassed.

The default is 1.6 billion transactions. Although users can set this value anywhere from zero to 2.1 billion, VACUUM will silently adjust the effective value to no less than 105% of [autovacu](#page-82-0)[um\\_freeze\\_max\\_age](#page-82-0).

```
vacuum_multixact_freeze_table_age (integer)
```

VACUUM performs an aggressive scan if the table's pg\_class.relminmxid field has reached the age specified by this setting. An aggressive scan differs from a regular VACUUM in that it visits every page that might contain unfrozen XIDs or MXIDs, not just those that might contain dead tuples. The default is 150 million multixacts. Although users can set this value anywhere from zero to two billion, VACUUM will silently limit the effective value to 95% of [autovacuum\\_multix](#page-83-1)[act\\_freeze\\_max\\_age](#page-83-1), so that a periodic manual VACUUM has a chance to run before an anti-wraparound is launched for the table. For more information see [Section 25.1.5.1.](#page-166-1)

```
vacuum_multixact_freeze_min_age (integer)
```

Specifies the cutoff age (in multixacts) that VACUUM should use to decide whether to replace multixact IDs with a newer transaction ID or multixact ID while scanning a table. The default is 5 million multixacts. Although users can set this value anywhere from zero to one billion, VACUUM will silently limit the effective value to half the value of [autovacuum\\_multixact\\_freeze\\_max\\_age,](#page-83-1) so that there is not an unreasonably short time between forced autovacuums. For more information see [Section 25.1.5.1](#page-166-1).

```
vacuum_multixact_failsafe_age (integer)
```

Specifies the maximum age (in multixacts) that a table's pg\_class.relminmxid field can attain before VACUUM takes extraordinary measures to avoid system-wide multixact ID wraparound failure. This is VACUUM's strategy of last resort. The failsafe typically triggers when an autovacuum to prevent transaction ID wraparound has already been running for some time, though it's possible for the failsafe to trigger during any VACUUM.

When the failsafe is triggered, any cost-based delay that is in effect will no longer be applied, and further non-essential maintenance tasks (such as index vacuuming) are bypassed.

The default is 1.6 billion multixacts. Although users can set this value anywhere from zero to 2.1 billion, VACUUM will silently adjust the effective value to no less than 105% of [autovacuum\\_mul](#page-83-1)[tixact\\_freeze\\_max\\_age.](#page-83-1)

```
bytea_output (enum)
```

Sets the output format for values of type bytea. Valid values are hex (the default) and escape (the traditional PostgreSQL format). See Section 8.4 for more information. The bytea type always accepts both formats on input, regardless of this setting.

```
xmlbinary (enum)
```

Sets how binary values are to be encoded in XML. This applies for example when bytea values are converted to XML by the functions xmlelement or xmlforest. Possible values are base64 and hex, which are both defined in the XML Schema standard. The default is base64. For further information about XML-related functions, see Section 9.15.

The actual choice here is mostly a matter of taste, constrained only by possible restrictions in client applications. Both methods support all possible values, although the hex encoding will be somewhat larger than the base64 encoding.

```
xmloption (enum)
```

Sets whether DOCUMENT or CONTENT is implicit when converting between XML and character string values. See Section 8.13 for a description of this. Valid values are DOCUMENT and CON-TENT. The default is CONTENT.

According to the SQL standard, the command to set this option is

```
SET XML OPTION { DOCUMENT | CONTENT };
```

This syntax is also available in PostgreSQL.

```
gin_pending_list_limit (integer)
```

Sets the maximum size of a GIN index's pending list, which is used when fastupdate is enabled. If the list grows larger than this maximum size, it is cleaned up by moving the entries in it to the index's main GIN data structure in bulk. If this value is specified without units, it is taken as kilobytes. The default is four megabytes (4MB). This setting can be overridden for individual GIN indexes by changing index storage parameters. See Section 70.4.1 and Section 70.5 for more information.

```
restrict_nonsystem_relation_kind (string)
```

Set relation kinds for which access to non-system relations is prohibited. The value takes the form of a comma-separated list of relation kinds. Currently, the supported relation kinds are view and foreign-table.

## <span id="page-89-1"></span><span id="page-89-0"></span>**20.11.2. Locale and Formatting**

```
DateStyle (string)
```

Sets the display format for date and time values, as well as the rules for interpreting ambiguous date input values. For historical reasons, this variable contains two independent components: the output format specification (ISO, Postgres, SQL, or German) and the input/output specification for year/month/day ordering (DMY, MDY, or YMD). These can be set separately or together. The keywords Euro and European are synonyms for DMY; the keywords US, NonEuro, and NonEuropean are synonyms for MDY. See Section 8.5 for more information. The built-in default is ISO, MDY, but initdb will initialize the configuration file with a setting that corresponds to the behavior of the chosen lc\_time locale.

```
IntervalStyle (enum)
```

Sets the display format for interval values. The value sql\_standard will produce output matching SQL standard interval literals. The value postgres (which is the default) will produce output matching PostgreSQL releases prior to 8.4 when the [DateStyle](#page-89-0) parameter was set to ISO. The value postgres\_verbose will produce output matching PostgreSQL releases prior to 8.4 when the DateStyle parameter was set to non-ISO output. The value iso\_8601 will produce output matching the time interval "format with designators" defined in section 4.4.3.2 of ISO 8601.

The IntervalStyle parameter also affects the interpretation of ambiguous interval input. See Section 8.5.4 for more information.

<span id="page-90-1"></span>TimeZone (string)

Sets the time zone for displaying and interpreting time stamps. The built-in default is GMT, but that is typically overridden in postgresql.conf; initdb will install a setting there corresponding to its system environment. See Section 8.5.3 for more information.

<span id="page-90-0"></span>timezone\_abbreviations (string)

Sets the collection of time zone abbreviations that will be accepted by the server for datetime input. The default is 'Default', which is a collection that works in most of the world; there are also 'Australia' and 'India', and other collections can be defined for a particular installation. See Section B.4 for more information.

```
extra_float_digits (integer)
```

This parameter adjusts the number of digits used for textual output of floating-point values, including float4, float8, and geometric data types.

If the value is 1 (the default) or above, float values are output in shortest-precise format; see Section 8.1.3. The actual number of digits generated depends only on the value being output, not on the value of this parameter. At most 17 digits are required for float8 values, and 9 for float4 values. This format is both fast and precise, preserving the original binary float value exactly when correctly read. For historical compatibility, values up to 3 are permitted.

If the value is zero or negative, then the output is rounded to a given decimal precision. The precision used is the standard number of digits for the type (FLT\_DIG or DBL\_DIG as appropriate) reduced according to the value of this parameter. (For example, specifying -1 will cause float4 values to be output rounded to 5 significant digits, and float8 values rounded to 14 digits.) This format is slower and does not preserve all the bits of the binary float value, but may be more human-readable.

### **Note**

The meaning of this parameter, and its default value, changed in PostgreSQL 12; see Section 8.1.3 for further discussion.

<span id="page-90-2"></span>client\_encoding (string)

Sets the client-side encoding (character set). The default is to use the database encoding. The character sets supported by the PostgreSQL server are described in [Section 24.3.1](#page-149-0).

lc\_messages (string)

Sets the language in which messages are displayed. Acceptable values are system-dependent; see [Section 24.1](#page-140-0) for more information. If this variable is set to the empty string (which is the default) then the value is inherited from the execution environment of the server in a system-dependent way.

On some systems, this locale category does not exist. Setting this variable will still work, but there will be no effect. Also, there is a chance that no translated messages for the desired language exist. In that case you will continue to see the English messages.

Only superusers and users with the appropriate SET privilege can change this setting.

lc\_monetary (string)

Sets the locale to use for formatting monetary amounts, for example with the to\_char family of functions. Acceptable values are system-dependent; see [Section 24.1](#page-140-0) for more information. If this variable is set to the empty string (which is the default) then the value is inherited from the execution environment of the server in a system-dependent way.

```
lc_numeric (string)
```

Sets the locale to use for formatting numbers, for example with the to\_char family of functions. Acceptable values are system-dependent; see [Section 24.1](#page-140-0) for more information. If this variable is set to the empty string (which is the default) then the value is inherited from the execution environment of the server in a system-dependent way.

```
lc_time (string)
```

Sets the locale to use for formatting dates and times, for example with the to\_char family of functions. Acceptable values are system-dependent; see [Section 24.1](#page-140-0) for more information. If this variable is set to the empty string (which is the default) then the value is inherited from the execution environment of the server in a system-dependent way.

```
default_text_search_config (string)
```

Selects the text search configuration that is used by those variants of the text search functions that do not have an explicit argument specifying the configuration. See Chapter 12 for further information. The built-in default is pg\_catalog.simple, but initdb will initialize the configuration file with a setting that corresponds to the chosen lc\_ctype locale, if a configuration matching that locale can be identified.