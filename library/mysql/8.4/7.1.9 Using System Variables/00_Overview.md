---
source: MySQL 8.4 Reference
title: 00_Overview
---

The MySQL server maintains many system variables that configure its operation. Section 7.1.8, "Server System Variables", describes the meaning of these variables. Each system variable has a default value. System variables can be set at server startup using options on the command line or in an option file. Most of them can be changed dynamically while the server is running by means of the SET statement, which enables you to modify operation of the server without having to stop and restart it. You can also use system variable values in expressions.

Many system variables are built in. System variables may also be installed by server plugins or components:

- System variables implemented by a server plugin are exposed when the plugin is installed and have names that begin with the plugin name. For example, the audit\_log plugin implements a system variable named audit\_log\_policy.
- System variables implemented by a component are exposed when the component is installed and have names that begin with a component-specific prefix. For example, the log\_filter\_dragnet error log filter component implements a system variable named log\_error\_filter\_rules, the full name of which is dragnet.log\_error\_filter\_rules. To refer to this variable, use the full name.

There are two scopes in which system variables exist. Global variables affect the overall operation of the server. Session variables affect its operation for individual client connections. A given system variable can have both a global and a session value. Global and session system variables are related as follows:

• When the server starts, it initializes each global variable to its default value. These defaults can be changed by options specified on the command line or in an option file. (See Section 6.2.2, "Specifying Program Options".)

• The server also maintains a set of session variables for each client that connects. The client's session variables are initialized at connect time using the current values of the corresponding global variables. For example, a client's SQL mode is controlled by the session sql\_mode value, which is initialized when the client connects to the value of the global sql mode value.

For some system variables, the session value is not initialized from the corresponding global value; if so, that is indicated in the variable description.

System variable values can be set globally at server startup by using options on the command line or in an option file. At startup, the syntax for system variables is the same as for command options, so within variable names, dashes and underscores may be used interchangeably. For example, -- general log=ON and --general-log=ON are equivalent.

When you use a startup option to set a variable that takes a numeric value, the value can be given with a suffix of K, M, G, T, P, or E (either uppercase or lowercase) to indicate a multiplier of 1024, 1024 $^2$ , 1024 $^3$ , 1024 $^4$ , 1024 $^5$ , or 1024 $^6$ ; that is, units of kilobytes, megabytes, gigabytes, terabytes, petabytes, or ettabytes, respectively. Thus, the following command starts the server with a sort buffer size of 256 kilobytes and a maximum packet size of one gigabyte:

```
mysqld --sort-buffer-size=256K --max-allowed-packet=1G
```

Within an option file, those variables are set like this:

```
[mysqld]
sort_buffer_size=256K
max_allowed_packet=1G
```

The lettercase of suffix letters does not matter; 256k and 256k are equivalent, as are 1g and 1g.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement, specify this maximum by using an option of the form  $--maximum-var\_name=value$  at server startup. For example, to prevent the value of  $sort\_buffer\_size$  from being increased to more than 32MB at runtime, use the option --maximum-sort-buffer-size=32M.

Many system variables are dynamic and can be changed at runtime by using the SET statement. For a list, see Section 7.1.9.2, "Dynamic System Variables". To change a system variable with SET, refer to it by name, optionally preceded by a modifier. At runtime, system variable names must be written using underscores, not dashes. The following examples briefly illustrate this syntax:

· Set a global system variable:

```
SET GLOBAL max_connections = 1000;
SET @@GLOBAL.max_connections = 1000;
```

Persist a global system variable to the mysqld-auto.cnf file (and set the runtime value):

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
```

• Persist a global system variable to the mysqld-auto.cnf file (without setting the runtime value):

```
SET PERSIST_ONLY back_log = 1000;
SET @@PERSIST_ONLY.back_log = 1000;
```

Set a session system variable:

```
SET SESSION sql_mode = 'TRADITIONAL';
SET @@SESSION.sql_mode = 'TRADITIONAL';
SET @@sql_mode = 'TRADITIONAL';
```

For complete details about SET syntax, see Section 15.7.6.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting and persisting system variables, see Section 7.1.9.1, "System Variable Privileges"

Suffixes for specifying a value multiplier can be used when setting a variable at server startup, but not to set the value with SET at runtime. On the other hand, with SET you can assign a variable's value using an expression, which is not true when you set a variable at server startup. For example, the first of the following lines is legal at server startup, but the second is not:

```
$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024
```

Conversely, the second of the following lines is legal at runtime, but the first is not:

```
mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;
```

To display system variable names and values, use the SHOW VARIABLES statement:

```
mysql> SHOW VARIABLES;
+-------------------------------------------------------+----------------------+
| Variable_name | Value |
+-------------------------------------------------------+----------------------+
| activate_all_roles_on_login | OFF |
| admin_address | |
| admin_port | 33062 |
| admin_ssl_ca | |
| admin_ssl_capath | |
| admin_ssl_cert | |
| admin_ssl_cipher | |
| admin_ssl_crl | |
| admin_ssl_crlpath | |
| admin_ssl_key | |
| admin_tls_ciphersuites | |
| admin_tls_version | TLSv1.2,TLSv1.3 |
| authentication_policy | *,, |
| auto_generate_certs | ON |
| auto_increment_increment | 1 |
| auto_increment_offset | 1 |
| autocommit | ON |
| automatic_sp_privileges | ON |
...
| version | 8.4.0 |
| version_comment | Source distribution |
| version_compile_machine | x86_64 |
| version_compile_os | Linux |
| version_compile_zlib | 1.2.13 |
| wait_timeout | 28800 |
| warning_count | 0 |
| windowing_use_high_precision | ON |
| xa_detach_on_prepare | ON |
+-------------------------------------------------------+----------------------+
```

With a LIKE clause, the statement displays only those variables that match the pattern. To obtain a specific variable name, use a LIKE clause as shown:

```
SHOW VARIABLES LIKE 'max_join_size';
SHOW SESSION VARIABLES LIKE 'max_join_size';
```

To get a list of variables whose name match a pattern, use the % wildcard character in a LIKE clause:

```
SHOW VARIABLES LIKE '%size%';
SHOW GLOBAL VARIABLES LIKE '%size%';
```

Wildcard characters can be used in any position within the pattern to be matched. Strictly speaking, because \_ is a wildcard that matches any single character, you should escape it as \\_ to match it literally. In practice, this is rarely necessary.

For SHOW VARIABLES, if you specify neither GLOBAL nor SESSION, MySQL returns SESSION values.

The reason for requiring the GLOBAL keyword when setting GLOBAL-only variables but not when retrieving them is to prevent problems in the future:

- Were a SESSION variable to be removed that has the same name as a GLOBAL variable, a client with privileges sufficient to modify global variables might accidentally change the GLOBAL variable rather than just the SESSION variable for its own session.
- Were a SESSION variable to be added with the same name as a GLOBAL variable, a client that intends to change the GLOBAL variable might find only its own SESSION variable changed.

# <span id="page-110-0"></span>**7.1.9.1 System Variable Privileges**

A system variable can have a global value that affects server operation as a whole, a session value that affects only the current session, or both:

- For dynamic system variables, the SET statement can be used to change their global or session runtime value (or both), to affect operation of the current server instance. (For information about dynamic variables, see [Section 7.1.9.2, "Dynamic System Variables".](#page-111-0))
- For certain global system variables, SET can be used to persist their value to the mysqldauto.cnf file in the data directory, to affect server operation for subsequent startups. (For information about persisting system variables and the mysqld-auto.cnf file, see [Section 7.1.9.3,](#page-129-0) ["Persisted System Variables".](#page-129-0))
- For persisted global system variables, RESET PERSIST can be used to remove their value from mysqld-auto.cnf, to affect server operation for subsequent startups.

This section describes the privileges required for operations that assign values to system variables at runtime. This includes operations that affect runtime values, and operations that persist values.

To set a global system variable, use a SET statement with the appropriate keyword. These privileges apply:

- To set a global system variable runtime value, use the SET GLOBAL statement, which requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege).
- To persist a global system variable to the mysqld-auto.cnf file (and set the runtime value), use the SET PERSIST statement, which requires the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege.
- To persist a global system variable to the mysqld-auto.cnf file (without setting the runtime value), use the SET PERSIST\_ONLY statement, which requires the SYSTEM\_VARIABLES\_ADMIN and PERSIST\_RO\_VARIABLES\_ADMIN privileges. SET PERSIST\_ONLY can be used for both dynamic and read-only system variables, but is particularly useful for persisting read-only variables, for which SET PERSIST cannot be used.
- Some global system variables are persist-restricted (see [Section 7.1.9.4, "Nonpersistible and Persist-](#page-133-0)[Restricted System Variables"\)](#page-133-0). To persist these variables, use the SET PERSIST\_ONLY statement, which requires the privileges described previously. In addition, you must connect to the server using an encrypted connection and supply an SSL certificate with the Subject value specified by the [persist\\_only\\_admin\\_x509\\_subject](#page-44-1) system variable.

To remove a persisted global system variable from the mysqld-auto.cnf file, use the RESET PERSIST statement. These privileges apply:

- For dynamic system variables, RESET PERSIST requires the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege.
- For read-only system variables, RESET PERSIST requires the SYSTEM\_VARIABLES\_ADMIN and PERSIST\_RO\_VARIABLES\_ADMIN privileges.
- For persist-restricted variables, RESET PERSIST does not require an encrypted connection to the server made using a particular SSL certificate.

If a global system variable has any exceptions to the preceding privilege requirements, the variable description indicates those exceptions. Examples include default\_table\_encryption and

[mandatory\\_roles](#page-19-0), which require additional privileges. These additional privileges apply to operations that set the global runtime value, but not operations that persist the value.

To set a session system variable runtime value, use the SET SESSION statement. In contrast to setting global runtime values, setting session runtime values normally requires no special privileges and can be done by any user to affect the current session. For some system variables, setting the session value may have effects outside the current session and thus is a restricted operation that can be done only by users who have a special privilege:

• The privilege required is SESSION\_VARIABLES\_ADMIN.

![](_page_111_Picture_4.jpeg)

#### **Note**

Any user who has SYSTEM\_VARIABLES\_ADMIN or SUPER effectively has SESSION\_VARIABLES\_ADMIN by implication and need not be granted SESSION\_VARIABLES\_ADMIN explicitly.

If a session system variable is restricted, the variable description indicates that restriction. Examples include binlog\_format and sql\_log\_bin. Setting the session value of these variables affects binary logging for the current session, but may also have wider implications for the integrity of server replication and backups.

SESSION\_VARIABLES\_ADMIN enables administrators to minimize the privilege footprint of users who may previously have been granted SYSTEM\_VARIABLES\_ADMIN or SUPER for the purpose of enabling them to modify restricted session system variables. Suppose that an administrator has created the following role to confer the ability to set restricted session system variables:

```
CREATE ROLE set_session_sysvars;
GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO set_session_sysvars;
```

Any user granted the set\_session\_sysvars role (and who has that role active) is able to set restricted session system variables. However, that user is also able to set global system variables, which may be undesirable.

By modifying the role to have SESSION\_VARIABLES\_ADMIN instead of SYSTEM\_VARIABLES\_ADMIN, the role privileges can be reduced to the ability to set restricted session system variables and nothing else. To modify the role, use these statements:

```
GRANT SESSION_VARIABLES_ADMIN ON *.* TO set_session_sysvars;
REVOKE SYSTEM_VARIABLES_ADMIN ON *.* FROM set_session_sysvars;
```

Modifying the role has an immediate effect: Any account granted the set\_session\_sysvars role no longer has SYSTEM\_VARIABLES\_ADMIN and is not able to set global system variables without being granted that ability explicitly. A similar GRANT/REVOKE sequence can be applied to any account that was granted SYSTEM\_VARIABLES\_ADMIN directly rather than by means of a role.

# <span id="page-111-0"></span>**7.1.9.2 Dynamic System Variables**

Many server system variables are dynamic and can be set at runtime. See Section 15.7.6.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting system variables, see [Section 7.1.9.1, "System Variable Privileges"](#page-110-0)

The following table lists all dynamic system variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

Variables that have a type of "string" take a string value. Variables that have a type of "numeric" take a numeric value. Variables that have a type of "boolean" can be set to 0, 1, ON or OFF. Variables that are marked as "enumeration" normally should be set to one of the available values for the variable, but can also be set to the number that corresponds to the desired enumeration value. For enumerated system

variables, the first enumeration value corresponds to 0. This differs from the ENUM data type used for table columns, for which the first enumeration value corresponds to 1.

**Table 7.5 Dynamic System Variable Summary**

| Variable Name                                    | Variable Type  | Variable Scope |
|--------------------------------------------------|----------------|----------------|
| activate_all_roles_on_login                      | Boolean        | Global         |
| admin_ssl_ca                                     | File name      | Global         |
| admin_ssl_capath                                 | Directory name | Global         |
| admin_ssl_cert                                   | File name      | Global         |
| admin_ssl_cipher                                 | String         | Global         |
| admin_ssl_crl                                    | File name      | Global         |
| admin_ssl_crlpath                                | Directory name | Global         |
| admin_ssl_key                                    | File name      | Global         |
| admin_tls_ciphersuites                           | String         | Global         |
| admin_tls_version                                | String         | Global         |
| audit_log_connection_policy                      | Enumeration    | Global         |
| audit_log_disable                                | Boolean        | Global         |
| audit_log_exclude_accounts                       | String         | Global         |
| audit_log_flush                                  | Boolean        | Global         |
| audit_log_format_unix_timestamp Boolean          |                | Global         |
| audit_log_include_accounts                       | String         | Global         |
| audit_log_password_history_keep_days Integer     |                | Global         |
| audit_log_prune_seconds                          | Integer        | Global         |
| audit_log_read_buffer_size                       | Integer        | Both           |
| audit_log_rotate_on_size                         | Integer        | Global         |
| audit_log_statement_policy                       | Enumeration    | Global         |
| authentication_kerberos_service_principal String |                | Global         |
| authentication_ldap_sasl_auth_method_name        | String         | Global         |
| authentication_ldap_sasl_bind_base_dn String     |                | Global         |
| authentication_ldap_sasl_bind_root_dn String     |                | Global         |
| authentication_ldap_sasl_bind_root_pwd String    |                | Global         |
| authentication_ldap_sasl_ca_pathString           |                | Global         |
| authentication_ldap_sasl_connect_timeout Integer |                | Global         |
| authentication_ldap_sasl_group_search_attr       | String         | Global         |
| authentication_ldap_sasl_group_search_filter     | String         | Global         |
| authentication_ldap_sasl_init_pool_size Integer  |                | Global         |
| authentication_ldap_sasl_log_statusInteger       |                | Global         |
| authentication_ldap_sasl_max_pool_size Integer   |                | Global         |
| authentication_ldap_sasl_referral Boolean        |                | Global         |
| authentication_ldap_sasl_response_timeout        | Integer        | Global         |
| authentication_ldap_sasl_server_host String      |                | Global         |
| authentication_ldap_sasl_server_port Integer     |                | Global         |
| authentication_ldap_sasl_tls                     | Boolean        | Global         |

| Variable Name                                     | Variable Type | Variable Scope |
|---------------------------------------------------|---------------|----------------|
| authentication_ldap_sasl_user_search_attr String  |               | Global         |
| authentication_ldap_simple_auth_method_name       | String        | Global         |
| authentication_ldap_simple_bind_base_dn String    |               | Global         |
| authentication_ldap_simple_bind_root_dn String    |               | Global         |
| authentication_ldap_simple_bind_root_pwd String   |               | Global         |
| authentication_ldap_simple_ca_pathString          |               | Global         |
| authentication_ldap_simple_connect_timeout        | Integer       | Global         |
| authentication_ldap_simple_group_search_attr      | String        | Global         |
| authentication_ldap_simple_group_search_filter    | String        | Global         |
| authentication_ldap_simple_init_pool_size Integer |               | Global         |
| authentication_ldap_simple_log_status Integer     |               | Global         |
| authentication_ldap_simple_max_pool_size Integer  |               | Global         |
| authentication_ldap_simple_referralBoolean        |               | Global         |
| authentication_ldap_simple_response_timeout       | Integer       | Global         |
| authentication_ldap_simple_server_host String     |               | Global         |
| authentication_ldap_simple_server_port Integer    |               | Global         |
| authentication_ldap_simple_tls                    | Boolean       | Global         |
| authentication_ldap_simple_user_search_attr       | String        | Global         |
| authentication_policy                             | String        | Global         |
| authentication_webauthn_rp_id                     | String        | Global         |
| auto_increment_increment                          | Integer       | Both           |
| auto_increment_offset                             | Integer       | Both           |
| autocommit                                        | Boolean       | Both           |
| automatic_sp_privileges                           | Boolean       | Global         |
| big_tables                                        | Boolean       | Both           |
| binlog_cache_size                                 | Integer       | Global         |
| binlog_checksum                                   | String        | Global         |
| binlog_direct_non_transactional_updates Boolan    |               | Both           |
| binlog_encryption                                 | Boolean       | Global         |
| binlog_error_action                               | Enumeration   | Global         |
| binlog_expire_logs_auto_purge                     | Boolean       | Global         |
| binlog_expire_logs_seconds                        | Integer       | Global         |
| binlog_format                                     | Enumeration   | Both           |
| binlog_group_commit_sync_delay Integer            |               | Global         |
| binlog_group_commit_sync_no_delay_count           | Integer       | Global         |
| binlog_max_flush_queue_time                       | Integer       | Global         |
| binlog_order_commits                              | Boolean       | Global         |
| binlog_row_image                                  | Enumeration   | Both           |
| binlog_row_metadata                               | Enumeration   | Global         |
| binlog_row_value_options                          | Set           | Both           |
| binlog_rows_query_log_events                      | Boolean       | Both           |

| Variable Name                                     | Variable Type | Variable Scope |
|---------------------------------------------------|---------------|----------------|
| binlog_stmt_cache_size                            | Integer       | Global         |
| binlog_transaction_compression                    | Boolean       | Both           |
| binlog_transaction_compression_level_zstd Integer |               | Both           |
| binlog_transaction_dependency_history_size        | Integer       | Global         |
| block_encryption_mode                             | String        | Both           |
| bulk_insert_buffer_size                           | Integer       | Both           |
| caching_sha2_password_digest_rounds Integer       |               | Global         |
| character_set_client                              | String        | Both           |
| character_set_connection                          | String        | Both           |
| character_set_database                            | String        | Both           |
| character_set_filesystem                          | String        | Both           |
| character_set_results                             | String        | Both           |
| character_set_server                              | String        | Both           |
| check_proxy_users                                 | Boolean       | Global         |
| clone_autotune_concurrency                        | Boolean       | Global         |
| clone_block_ddl                                   | Boolean       | Global         |
| clone_buffer_size                                 | Integer       | Global         |
| clone_ddl_timeout                                 | Integer       | Global         |
| clone_delay_after_data_drop                       | Integer       | Global         |
| clone_donor_timeout_after_network_failure Integer |               | Global         |
| clone_enable_compression                          | Boolean       | Global         |
| clone_max_concurrency                             | Integer       | Global         |
| clone_max_data_bandwidth                          | Integer       | Global         |
| clone_max_network_bandwidth                       | Integer       | Global         |
| clone_ssl_ca                                      | File name     | Global         |
| clone_ssl_cert                                    | File name     | Global         |
| clone_ssl_key                                     | File name     | Global         |
| clone_valid_donor_list                            | String        | Global         |
| collation_connection                              | String        | Both           |
| collation_database                                | String        | Both           |
| collation_server                                  | String        | Both           |
| completion_type                                   | Enumeration   | Both           |
| component_scheduler.enabled                       | Boolean       | Global         |
| concurrent_insert                                 | Enumeration   | Global         |
| connect_timeout                                   | Integer       | Global         |
| connection_control_failed_connections_threshold   | Integer       | Global         |
| connection_control_max_connection_delay Integer   |               | Global         |
| connection_control_min_connection_delay Integer   |               | Global         |
| connection_memory_chunk_size                      | Integer       | Both           |
| connection_memory_limit                           | Integer       | Both           |
| cte_max_recursion_depth                           | Integer       | Both           |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| debug                                            | String        | Both           |
| debug_sync                                       | String        | Session        |
| default_collation_for_utf8mb4                    | Enumeration   | Both           |
| default_password_lifetime                        | Integer       | Global         |
| default_storage_engine                           | Enumeration   | Both           |
| default_table_encryption                         | Boolean       | Both           |
| default_tmp_storage_engine                       | Enumeration   | Both           |
| default_week_format                              | Integer       | Both           |
| delay_key_write                                  | Enumeration   | Global         |
| delayed_insert_limit                             | Integer       | Global         |
| delayed_insert_timeout                           | Integer       | Global         |
| delayed_queue_size                               | Integer       | Global         |
| div_precision_increment                          | Integer       | Both           |
| dragnet.log_error_filter_rules                   | String        | Global         |
| end_markers_in_json                              | Boolean       | Both           |
| enforce_gtid_consistency                         | Enumeration   | Global         |
| enterprise_encryption.maximum_rsa_key_size       | Integer       | Global         |
| enterprise_encryption.rsa_support_legacy_padding | Boolean       | Global         |
| eq_range_index_dive_limit                        | Integer       | Both           |
| event_scheduler                                  | Enumeration   | Global         |
| explain_format                                   | Enumeration   | Both           |
| explain_json_format_version                      | Integer       | Both           |
| explicit_defaults_for_timestamp                  | Boolean       | Both           |
| flush                                            | Boolean       | Global         |
| flush_time                                       | Integer       | Global         |
| foreign_key_checks                               | Boolean       | Both           |
| ft_boolean_syntax                                | String        | Global         |
| general_log                                      | Boolean       | Global         |
| general_log_file                                 | File name     | Global         |
| generated_random_password_length Integer         |               | Both           |
| global_connection_memory_limit                   | Integer       | Global         |
| global_connection_memory_trackingBoolean         |               | Both           |
| group_concat_max_len                             | Integer       | Both           |
| group_replication_advertise_recovery_endpoints   | String        | Global         |
| group_replication_allow_local_lower_version_join | Boolean       | Global         |
| group_replication_auto_increment_increment       | Integer       | Global         |
| group_replication_autorejoin_tries Integer       |               | Global         |
| group_replication_bootstrap_groupBoolean         |               | Global         |
| group_replication_clone_thresholdInteger         |               | Global         |
| group_replication_communication_debug_options    | String        | Global         |
| group_replication_communication_max_message_size | Integer       | Global         |

| Variable Name                                                  | Variable Type | Variable Scope |
|----------------------------------------------------------------|---------------|----------------|
| group_replication_communication_stack String                   |               | Global         |
| group_replication_components_stop_timeout                      | Integer       | Global         |
| group_replication_compression_threshold Integer                |               | Global         |
| group_replication_consistency                                  | Enumeration   | Both           |
| group_replication_enforce_update_everywhere_checks             | Boolean       | Global         |
| group_replication_exit_state_actionEnumeration                 |               | Global         |
| group_replication_flow_control_applier_threshold               | Integer       | Global         |
| group_replication_flow_control_certifier_threshold             | Integer       | Global         |
| group_replication_flow_control_hold_percent                    | Integer       | Global         |
| group_replication_flow_control_max_quota Integer               |               | Global         |
| group_replication_flow_control_member_quota_percent            | Integer       | Global         |
| group_replication_flow_control_min_quota Integer               |               | Global         |
| group_replication_flow_control_min_recovery_quota              | Integer       | Global         |
| group_replication_flow_control_mode Enumeration                |               | Global         |
| group_replication_flow_control_period Integer                  |               | Global         |
| group_replication_flow_control_release_percent                 | Integer       | Global         |
| group_replication_force_membersString                          |               | Global         |
| group_replication_group_name                                   | String        | Global         |
| group_replication_group_seeds                                  | String        | Global         |
| group_replication_gtid_assignment_block_size                   | Integer       | Global         |
| group_replication_ip_allowlist                                 | String        | Global         |
| group_replication_local_address                                | String        | Global         |
| group_replication_member_expel_timeout Integer                 |               | Global         |
| group_replication_member_weightInteger                         |               | Global         |
| group_replication_message_cache_size Integer                   |               | Global         |
| group_replication_paxos_single_leader Boolean                  |               | Global         |
| group_replication_poll_spin_loopsInteger                       |               | Global         |
| group_replication_preemptive_garbage_collection                | Boolean       | Global         |
| group_replication_preemptive_garbage_collection_rows_threshold | Integer       | Global         |
| group_replication_recovery_compression_algorithms              | Set           | Global         |
| group_replication_recovery_get_public_key Boolean              |               | Global         |
| group_replication_recovery_public_key_path                     | File name     | Global         |
| group_replication_recovery_reconnect_interval                  | Integer       | Global         |
| group_replication_recovery_retry_count Integer                 |               | Global         |
| group_replication_recovery_ssl_caString                        |               | Global         |
| group_replication_recovery_ssl_capath String                   |               | Global         |
| group_replication_recovery_ssl_cert String                     |               | Global         |
| group_replication_recovery_ssl_cipher String                   |               | Global         |
| group_replication_recovery_ssl_crlFile name                    |               | Global         |
| group_replication_recovery_ssl_crlpath Directory name          |               | Global         |
| group_replication_recovery_ssl_keyString                       |               | Global         |

| Variable Name                                     | Variable Type | Variable Scope |
|---------------------------------------------------|---------------|----------------|
| group_replication_recovery_ssl_verify_server_cert | Boolean       | Global         |
| group_replication_recovery_tls_ciphersuites       | String        | Global         |
| group_replication_recovery_tls_version String     |               | Global         |
| group_replication_recovery_use_ssl Boolean        |               | Global         |
| group_replication_recovery_zstd_compression_level | Integer       | Global         |
| group_replication_single_primary_mode Boolan      |               | Global         |
| group_replication_ssl_mode                        | Enumeration   | Global         |
| group_replication_start_on_boot                   | Boolean       | Global         |
| group_replication_tls_source                      | Enumeration   | Global         |
| group_replication_transaction_size_limit Integer  |               | Global         |
| group_replication_unreachable_majority_timeout    | Integer       | Global         |
| group_replication_view_change_uuidString          |               | Global         |
| gtid_executed_compression_periodInteger           |               | Global         |
| gtid_mode                                         | Enumeration   | Global         |
| gtid_next                                         | Enumeration   | Session        |
| gtid_purged                                       | String        | Global         |
| histogram_generation_max_mem_size Integer         |               | Both           |
| host_cache_size                                   | Integer       | Global         |
| identity                                          | Integer       | Session        |
| immediate_server_version                          | Integer       | Session        |
| information_schema_stats_expiry Integer           |               | Both           |
| init_connect                                      | String        | Global         |
| init_replica                                      | String        | Global         |
| init_slave                                        | String        | Global         |
| innodb_adaptive_flushing                          | Boolean       | Global         |
| innodb_adaptive_flushing_lwm                      | Integer       | Global         |
| innodb_adaptive_hash_index                        | Boolean       | Global         |
| innodb_adaptive_max_sleep_delayInteger            |               | Global         |
| innodb_autoextend_increment                       | Integer       | Global         |
| innodb_background_drop_list_emptyBoolean          |               | Global         |
| innodb_buffer_pool_dump_at_shutdown Boolean       |               | Global         |
| innodb_buffer_pool_dump_now                       | Boolean       | Global         |
| innodb_buffer_pool_dump_pct                       | Integer       | Global         |
| innodb_buffer_pool_filename                       | File name     | Global         |
| innodb_buffer_pool_in_core_file                   | Boolean       | Global         |
| innodb_buffer_pool_load_abort                     | Boolean       | Global         |
| innodb_buffer_pool_load_now                       | Boolean       | Global         |
| innodb_buffer_pool_size                           | Integer       | Global         |
| innodb_change_buffer_max_size Integer             |               | Global         |
| innodb_change_buffering                           | Enumeration   | Global         |
| innodb_change_buffering_debug                     | Integer       | Global         |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| innodb_checkpoint_disabled                       | Boolean       | Global         |
| innodb_checksum_algorithm                        | Enumeration   | Global         |
| innodb_cmp_per_index_enabled                     | Boolean       | Global         |
| innodb_commit_concurrency                        | Integer       | Global         |
| innodb_compress_debug                            | Enumeration   | Global         |
| innodb_compression_failure_threshold_pct Integer |               | Global         |
| innodb_compression_level                         | Integer       | Global         |
| innodb_compression_pad_pct_maxInteger            |               | Global         |
| innodb_concurrency_tickets                       | Integer       | Global         |
| innodb_ddl_buffer_size                           | Integer       | Session        |
| innodb_ddl_log_crash_reset_debugBoolean          |               | Global         |
| innodb_ddl_threads                               | Integer       | Session        |
| innodb_deadlock_detect                           | Boolean       | Global         |
| innodb_default_row_format                        | Enumeration   | Global         |
| innodb_disable_sort_file_cache                   | Boolean       | Global         |
| innodb_doublewrite                               | Enumeration   | Global         |
| innodb_extend_and_initialize                     | Boolean       | Global         |
| innodb_fast_shutdown                             | Integer       | Global         |
| innodb_fil_make_page_dirty_debugInteger          |               | Global         |
| innodb_file_per_table                            | Boolean       | Global         |
| innodb_fill_factor                               | Integer       | Global         |
| innodb_flush_log_at_timeout                      | Integer       | Global         |
| innodb_flush_log_at_trx_commit                   | Enumeration   | Global         |
| innodb_flush_neighbors                           | Enumeration   | Global         |
| innodb_flush_sync                                | Boolean       | Global         |
| innodb_flushing_avg_loops                        | Integer       | Global         |
| innodb_fsync_threshold                           | Integer       | Global         |
| innodb_ft_aux_table                              | String        | Global         |
| innodb_ft_enable_diag_print                      | Boolean       | Global         |
| innodb_ft_enable_stopword                        | Boolean       | Both           |
| innodb_ft_num_word_optimize                      | Integer       | Global         |
| innodb_ft_result_cache_limit                     | Integer       | Global         |
| innodb_ft_server_stopword_table String           |               | Global         |
| innodb_ft_user_stopword_table                    | String        | Both           |
| innodb_idle_flush_pct                            | Integer       | Global         |
| innodb_io_capacity                               | Integer       | Global         |
| innodb_io_capacity_max                           | Integer       | Global         |
| innodb_limit_optimistic_insert_debugInteger      |               | Global         |
| innodb_lock_wait_timeout                         | Integer       | Both           |
| innodb_log_buffer_size                           | Integer       | Global         |
| innodb_log_checkpoint_fuzzy_nowBoolean           |               | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| innodb_log_checkpoint_now                    | Boolean       | Global         |
| innodb_log_checksums                         | Boolean       | Global         |
| innodb_log_compressed_pages                  | Boolean       | Global         |
| innodb_log_spin_cpu_abs_lwm                  | Integer       | Global         |
| innodb_log_spin_cpu_pct_hwm                  | Integer       | Global         |
| innodb_log_wait_for_flush_spin_hwmInteger    |               | Global         |
| innodb_log_write_ahead_size                  | Integer       | Global         |
| innodb_log_writer_threads                    | Boolean       | Global         |
| innodb_lru_scan_depth                        | Integer       | Global         |
| innodb_max_dirty_pages_pct                   | Numeric       | Global         |
| innodb_max_dirty_pages_pct_lwmNumeric        |               | Global         |
| innodb_max_purge_lag                         | Integer       | Global         |
| innodb_max_purge_lag_delay                   | Integer       | Global         |
| innodb_max_undo_log_size                     | Integer       | Global         |
| innodb_merge_threshold_set_all_debug Integer |               | Global         |
| innodb_monitor_disable                       | String        | Global         |
| innodb_monitor_enable                        | String        | Global         |
| innodb_monitor_reset                         | Enumeration   | Global         |
| innodb_monitor_reset_all                     | Enumeration   | Global         |
| innodb_old_blocks_pct                        | Integer       | Global         |
| innodb_old_blocks_time                       | Integer       | Global         |
| innodb_online_alter_log_max_sizeInteger      |               | Global         |
| innodb_open_files                            | Integer       | Global         |
| innodb_optimize_fulltext_only                | Boolean       | Global         |
| innodb_parallel_read_threads                 | Integer       | Session        |
| innodb_print_all_deadlocks                   | Boolean       | Global         |
| innodb_print_ddl_logs                        | Boolean       | Global         |
| innodb_purge_batch_size                      | Integer       | Global         |
| innodb_purge_rseg_truncate_frequency Integer |               | Global         |
| innodb_random_read_ahead                     | Boolean       | Global         |
| innodb_read_ahead_threshold                  | Integer       | Global         |
| innodb_redo_log_archive_dirs                 | String        | Global         |
| innodb_redo_log_capacity                     | Integer       | Global         |
| innodb_redo_log_encrypt                      | Boolean       | Global         |
| innodb_replication_delay                     | Integer       | Global         |
| innodb_rollback_segments                     | Integer       | Global         |
| innodb_saved_page_number_debugInteger        |               | Global         |
| innodb_segment_reserve_factor                | Numeric       | Global         |
| innodb_spin_wait_delay                       | Integer       | Global         |
| innodb_spin_wait_pause_multiplierInteger     |               | Global         |
| innodb_stats_auto_recalc                     | Boolean       | Global         |

| Variable Name                                | Variable Type  | Variable Scope |
|----------------------------------------------|----------------|----------------|
| innodb_stats_include_delete_marked Boolean   |                | Global         |
| innodb_stats_method                          | Enumeration    | Global         |
| innodb_stats_on_metadata                     | Boolean        | Global         |
| innodb_stats_persistent                      | Boolean        | Global         |
| innodb_stats_persistent_sample_pages Integer |                | Global         |
| innodb_stats_transient_sample_pages Integer  |                | Global         |
| innodb_status_output                         | Boolean        | Global         |
| innodb_status_output_locks                   | Boolean        | Global         |
| innodb_strict_mode                           | Boolean        | Both           |
| innodb_sync_spin_loops                       | Integer        | Global         |
| innodb_table_locks                           | Boolean        | Both           |
| innodb_thread_concurrency                    | Integer        | Global         |
| innodb_thread_sleep_delay                    | Integer        | Global         |
| innodb_tmpdir                                | Directory name | Both           |
| innodb_trx_purge_view_update_only_debug      | Boolean        | Global         |
| innodb_trx_rseg_n_slots_debug                | Integer        | Global         |
| innodb_undo_log_encrypt                      | Boolean        | Global         |
| innodb_undo_log_truncate                     | Boolean        | Global         |
| innodb_undo_tablespaces                      | Integer        | Global         |
| innodb_use_fdatasync                         | Boolean        | Global         |
| insert_id                                    | Integer        | Session        |
| interactive_timeout                          | Integer        | Both           |
| internal_tmp_mem_storage_engineEnumeration   |                | Both           |
| join_buffer_size                             | Integer        | Both           |
| keep_files_on_create                         | Boolean        | Both           |
| key_buffer_size                              | Integer        | Global         |
| key_cache_age_threshold                      | Integer        | Global         |
| key_cache_block_size                         | Integer        | Global         |
| key_cache_division_limit                     | Integer        | Global         |
| keyring_aws_cmk_id                           | String         | Global         |
| keyring_aws_region                           | Enumeration    | Global         |
| keyring_hashicorp_auth_path                  | String         | Global         |
| keyring_hashicorp_ca_path                    | File name      | Global         |
| keyring_hashicorp_caching                    | Boolean        | Global         |
| keyring_hashicorp_role_id                    | String         | Global         |
| keyring_hashicorp_secret_id                  | String         | Global         |
| keyring_hashicorp_server_url                 | String         | Global         |
| keyring_hashicorp_store_path                 | String         | Global         |
| keyring_okv_conf_dir                         | Directory name | Global         |
| keyring_operations                           | Boolean        | Global         |
| last_insert_id                               | Integer        | Session        |

| Variable Name                                  | Variable Type | Variable Scope |
|------------------------------------------------|---------------|----------------|
| lc_messages                                    | String        | Both           |
| lc_time_names                                  | String        | Both           |
| local_infile                                   | Boolean       | Global         |
| lock_wait_timeout                              | Integer       | Both           |
| log_bin_trust_function_creators                | Boolean       | Global         |
| log_error_services                             | String        | Global         |
| log_error_suppression_list                     | String        | Global         |
| log_error_verbosity                            | Integer       | Global         |
| log_output                                     | Set           | Global         |
| log_queries_not_using_indexes                  | Boolean       | Global         |
| log_raw                                        | Boolean       | Global         |
| log_slow_admin_statements                      | Boolean       | Global         |
| log_slow_extra                                 | Boolean       | Global         |
| log_slow_replica_statements                    | Boolean       | Global         |
| log_slow_slave_statements                      | Boolean       | Global         |
| log_statements_unsafe_for_binlogBoolean        |               | Global         |
| log_throttle_queries_not_using_indexes Integer |               | Global         |
| log_timestamps                                 | Enumeration   | Global         |
| long_query_time                                | Numeric       | Both           |
| low_priority_updates                           | Boolean       | Both           |
| mandatory_roles                                | String        | Global         |
| master_verify_checksum                         | Boolean       | Global         |
| max_allowed_packet                             | Integer       | Both           |
| max_binlog_cache_size                          | Integer       | Global         |
| max_binlog_size                                | Integer       | Global         |
| max_binlog_stmt_cache_size                     | Integer       | Global         |
| max_connect_errors                             | Integer       | Global         |
| max_connections                                | Integer       | Global         |
| max_delayed_threads                            | Integer       | Both           |
| max_error_count                                | Integer       | Both           |
| max_execution_time                             | Integer       | Both           |
| max_heap_table_size                            | Integer       | Both           |
| max_insert_delayed_threads                     | Integer       | Both           |
| max_join_size                                  | Integer       | Both           |
| max_length_for_sort_data                       | Integer       | Both           |
| max_points_in_geometry                         | Integer       | Both           |
| max_prepared_stmt_count                        | Integer       | Global         |
| max_relay_log_size                             | Integer       | Global         |
| max_seeks_for_key                              | Integer       | Both           |
| max_sort_length                                | Integer       | Both           |
| max_sp_recursion_depth                         | Integer       | Both           |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| max_user_connections                             | Integer       | Both           |
| max_write_lock_count                             | Integer       | Global         |
| min_examined_row_limit                           | Integer       | Both           |
| myisam_data_pointer_size                         | Integer       | Global         |
| myisam_max_sort_file_size                        | Integer       | Global         |
| myisam_sort_buffer_size                          | Integer       | Both           |
| myisam_stats_method                              | Enumeration   | Both           |
| myisam_use_mmap                                  | Boolean       | Global         |
| mysql_firewall_mode                              | Boolean       | Global         |
| mysql_firewall_trace                             | Boolean       | Global         |
| mysql_native_password_proxy_users Boolean        |               | Global         |
| mysqlx_compression_algorithms                    | Set           | Global         |
| mysqlx_connect_timeout                           | Integer       | Global         |
| mysqlx_deflate_default_compression_level Integer |               | Global         |
| mysqlx_deflate_max_client_compression_level      | Integer       | Global         |
| mysqlx_document_id_unique_prefixInteger          |               | Global         |
| mysqlx_enable_hello_notice                       | Boolean       | Global         |
| mysqlx_idle_worker_thread_timeoutInteger         |               | Global         |
| mysqlx_interactive_timeout                       | Integer       | Global         |
| mysqlx_lz4_default_compression_level Integer     |               | Global         |
| mysqlx_lz4_max_client_compression_level Integer  |               | Global         |
| mysqlx_max_allowed_packet                        | Integer       | Global         |
| mysqlx_max_connections                           | Integer       | Global         |
| mysqlx_min_worker_threads                        | Integer       | Global         |
| mysqlx_read_timeout                              | Integer       | Session        |
| mysqlx_wait_timeout                              | Integer       | Session        |
| mysqlx_write_timeout                             | Integer       | Session        |
| mysqlx_zstd_default_compression_level Integer    |               | Global         |
| mysqlx_zstd_max_client_compression_level         | Integer       | Global         |
| ndb_allow_copying_alter_table                    | Boolean       | Both           |
| ndb_autoincrement_prefetch_sz                    | Integer       | Both           |
| ndb_batch_size                                   | Integer       | Both           |
| ndb_blob_read_batch_bytes                        | Integer       | Both           |
| ndb_blob_write_batch_bytes                       | Integer       | Both           |
| ndb_clear_apply_status                           | Boolean       | Global         |
| ndb_conflict_role                                | Enumeration   | Global         |
| ndb_data_node_neighbour                          | Integer       | Global         |
| ndb_dbg_check_shares                             | Integer       | Both           |
| ndb_default_column_format                        | Enumeration   | Global         |
| ndb_default_column_format                        | Enumeration   | Global         |
| ndb_deferred_constraints                         | Integer       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| ndb_deferred_constraints                     | Integer       | Both           |
| ndb_distribution                             | Enumeration   | Global         |
| ndb_distribution                             | Enumeration   | Global         |
| ndb_eventbuffer_free_percent                 | Integer       | Global         |
| ndb_eventbuffer_max_alloc                    | Integer       | Global         |
| ndb_extra_logging                            | Integer       | Global         |
| ndb_force_send                               | Boolean       | Both           |
| ndb_fully_replicated                         | Boolean       | Both           |
| ndb_index_stat_enable                        | Boolean       | Both           |
| ndb_index_stat_option                        | String        | Both           |
| ndb_join_pushdown                            | Boolean       | Both           |
| ndb_log_binlog_index                         | Boolean       | Global         |
| ndb_log_cache_size                           | Integer       | Global         |
| ndb_log_empty_epochs                         | Boolean       | Global         |
| ndb_log_empty_epochs                         | Boolean       | Global         |
| ndb_log_empty_update                         | Boolean       | Global         |
| ndb_log_empty_update                         | Boolean       | Global         |
| ndb_log_exclusive_reads                      | Boolean       | Both           |
| ndb_log_exclusive_reads                      | Boolean       | Both           |
| ndb_log_transaction_compressionBoolean       |               | Global         |
| ndb_log_transaction_compression_level_zstd   | Integer       | Global         |
| ndb_log_update_as_write                      | Boolean       | Global         |
| ndb_log_update_minimal                       | Boolean       | Global         |
| ndb_log_updated_only                         | Boolean       | Global         |
| ndb_metadata_check                           | Boolean       | Global         |
| ndb_metadata_check_interval                  | Integer       | Global         |
| ndb_metadata_sync                            | Boolean       | Global         |
| ndb_optimization_delay                       | Integer       | Global         |
| ndb_optimized_node_selection                 | Integer       | Global         |
| ndb_read_backup                              | Boolean       | Global         |
| ndb_recv_thread_activation_threshold Integer |               | Global         |
| ndb_recv_thread_cpu_mask                     | Bitmap        | Global         |
| ndb_replica_batch_size                       | Integer       | Global         |
| ndb_replica_blob_write_batch_bytesInteger    |               | Global         |
| ndb_report_thresh_binlog_epoch_slip Integer  |               | Global         |
| ndb_report_thresh_binlog_mem_usage Integer   |               | Global         |
| ndb_row_checksum                             | Integer       | Both           |
| ndb_schema_dist_lock_wait_timeout Ineger     |               | Global         |
| ndb_show_foreign_key_mock_tables Boolean     |               | Global         |
| ndb_slave_conflict_role                      | Enumeration   | Global         |
| ndb_table_no_logging                         | Boolean       | Session        |

| Variable Name                               | Variable Type | Variable Scope |
|---------------------------------------------|---------------|----------------|
| ndb_table_temporary                         | Boolean       | Session        |
| ndb_use_exact_count                         | Boolean       | Both           |
| ndb_use_transactions                        | Boolean       | Both           |
| ndbinfo_max_bytes                           | Integer       | Both           |
| ndbinfo_max_rows                            | Integer       | Both           |
| ndbinfo_offline                             | Boolean       | Global         |
| ndbinfo_show_hidden                         | Boolean       | Both           |
| net_buffer_length                           | Integer       | Both           |
| net_read_timeout                            | Integer       | Both           |
| net_retry_count                             | Integer       | Both           |
| net_write_timeout                           | Integer       | Both           |
| offline_mode                                | Boolean       | Global         |
| old_alter_table                             | Boolean       | Both           |
| optimizer_prune_level                       | Integer       | Both           |
| optimizer_search_depth                      | Integer       | Both           |
| optimizer_switch                            | Set           | Both           |
| optimizer_trace                             | String        | Both           |
| optimizer_trace_features                    | String        | Both           |
| optimizer_trace_limit                       | Integer       | Both           |
| optimizer_trace_max_mem_size                | Integer       | Both           |
| optimizer_trace_offset                      | Integer       | Both           |
| original_commit_timestamp                   | Numeric       | Session        |
| original_server_version                     | Integer       | Session        |
| parser_max_mem_size                         | Integer       | Both           |
| partial_revokes                             | Boolean       | Global         |
| password_history                            | Integer       | Global         |
| password_require_current                    | Boolean       | Global         |
| password_reuse_interval                     | Integer       | Global         |
| performance_schema_max_digest_sample_age    | Integer       | Global         |
| performance_schema_show_processlist Boolean |               | Global         |
| preload_buffer_size                         | Integer       | Both           |
| print_identified_with_as_hex                | Boolean       | Both           |
| profiling                                   | Boolean       | Both           |
| profiling_history_size                      | Integer       | Both           |
| protocol_compression_algorithms Set         |               | Global         |
| pseudo_replica_mode                         | Boolean       | Session        |
| pseudo_slave_mode                           | Boolean       | Session        |
| pseudo_thread_id                            | Integer       | Session        |
| query_alloc_block_size                      | Integer       | Both           |
| query_prealloc_size                         | Integer       | Both           |
| rand_seed1                                  | Integer       | Session        |

| Variable Name                                         | Variable Type | Variable Scope |
|-------------------------------------------------------|---------------|----------------|
| rand_seed2                                            | Integer       | Session        |
| range_alloc_block_size                                | Integer       | Both           |
| range_optimizer_max_mem_size Integer                  |               | Both           |
| rbr_exec_mode                                         | Enumeration   | Session        |
| read_buffer_size                                      | Integer       | Both           |
| read_only                                             | Boolean       | Global         |
| read_rnd_buffer_size                                  | Integer       | Both           |
| regexp_stack_limit                                    | Integer       | Global         |
| regexp_time_limit                                     | Integer       | Global         |
| relay_log_purge                                       | Boolean       | Global         |
| replica_allow_batching                                | Boolean       | Global         |
| replica_checkpoint_group                              | Integer       | Global         |
| replica_checkpoint_period                             | Integer       | Global         |
| replica_compressed_protocol                           | Boolean       | Global         |
| replica_exec_mode                                     | Enumeration   | Global         |
| replica_max_allowed_packet                            | Integer       | Global         |
| replica_net_timeout                                   | Integer       | Global         |
| replica_parallel_type                                 | Enumeration   | Global         |
| replica_parallel_workers                              | Integer       | Global         |
| replica_pending_jobs_size_max                         | Integer       | Global         |
| replica_preserve_commit_order                         | Boolean       | Global         |
| replica_sql_verify_checksum                           | Boolean       | Global         |
| replica_transaction_retries                           | Integer       | Global         |
| replica_type_conversions                              | Set           | Global         |
| replication_optimize_for_static_plugin_config         | Boolean       | Global         |
| replication_sender_observe_commit_only Boolean        |               | Global         |
| require_row_format                                    | Boolean       | Session        |
| require_secure_transport                              | Boolean       | Global         |
| restrict_fk_on_non_standard_key Boolean               |               | Both           |
| resultset_metadata                                    | Enumeration   | Session        |
| rewriter_enabled                                      | Boolean       | Global         |
| rewriter_enabled_for_threads_without_privilege_checks | Boolean       | Global         |
| rewriter_verbose                                      | Integer       | Global         |
| rpl_read_size                                         | Integer       | Global         |
| rpl_semi_sync_master_enabled                          | Boolean       | Global         |
| rpl_semi_sync_master_timeout                          | Integer       | Global         |
| rpl_semi_sync_master_trace_levelInteger               |               | Global         |
| rpl_semi_sync_master_wait_for_slave_count             | Integer       | Global         |
| rpl_semi_sync_master_wait_no_slave Boolean            |               | Global         |
| rpl_semi_sync_master_wait_point Enumeration           |               | Global         |
| rpl_semi_sync_replica_enabled                         | Boolean       | Global         |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| rpl_semi_sync_replica_trace_levelInteger         |               | Global         |
| rpl_semi_sync_slave_enabled                      | Boolean       | Global         |
| rpl_semi_sync_slave_trace_level Integer          |               | Global         |
| rpl_semi_sync_source_enabled                     | Boolean       | Global         |
| rpl_semi_sync_source_timeout                     | Integer       | Global         |
| rpl_semi_sync_source_trace_levelInteger          |               | Global         |
| rpl_semi_sync_source_wait_for_replica_count      | Integer       | Global         |
| rpl_semi_sync_source_wait_no_replica Boolean     |               | Global         |
| rpl_semi_sync_source_wait_point Enumeration      |               | Global         |
| rpl_stop_replica_timeout                         | Integer       | Global         |
| rpl_stop_slave_timeout                           | Integer       | Global         |
| schema_definition_cache                          | Integer       | Global         |
| secondary_engine_cost_thresholdNumeric           |               | Session        |
| select_into_buffer_size                          | Integer       | Both           |
| select_into_disk_sync                            | Boolean       | Both           |
| select_into_disk_sync_delay                      | Integer       | Both           |
| server_id                                        | Integer       | Global         |
| session_track_gtids                              | Enumeration   | Both           |
| session_track_schema                             | Boolean       | Both           |
| session_track_state_change                       | Boolean       | Both           |
| session_track_system_variables                   | String        | Both           |
| session_track_transaction_info                   | Enumeration   | Both           |
| set_operations_buffer_size                       | Integer       | Both           |
| sha256_password_proxy_users                      | Boolean       | Global         |
| show_create_table_skip_secondary_engine Boolean  |               | Session        |
| show_create_table_verbosity                      | Boolean       | Both           |
| show_gipk_in_create_table_and_information_schema | Boolean       | Both           |
| slave_allow_batching                             | Boolean       | Global         |
| slave_checkpoint_group                           | Integer       | Global         |
| slave_checkpoint_period                          | Integer       | Global         |
| slave_compressed_protocol                        | Boolean       | Global         |
| slave_exec_mode                                  | Enumeration   | Global         |
| slave_max_allowed_packet                         | Integer       | Global         |
| slave_net_timeout                                | Integer       | Global         |
| slave_parallel_type                              | Enumeration   | Global         |
| slave_parallel_workers                           | Integer       | Global         |
| slave_pending_jobs_size_max                      | Integer       | Global         |
| slave_preserve_commit_order                      | Boolean       | Global         |
| slave_sql_verify_checksum                        | Boolean       | Global         |
| slave_transaction_retries                        | Integer       | Global         |
| slave_type_conversions                           | Set           | Global         |

| Variable Name                             | Variable Type  | Variable Scope |
|-------------------------------------------|----------------|----------------|
| slow_launch_time                          | Integer        | Global         |
| slow_query_log                            | Boolean        | Global         |
| slow_query_log_file                       | File name      | Global         |
| sort_buffer_size                          | Integer        | Both           |
| source_verify_checksum                    | Boolean        | Global         |
| sql_auto_is_null                          | Boolean        | Both           |
| sql_big_selects                           | Boolean        | Both           |
| sql_buffer_result                         | Boolean        | Both           |
| sql_generate_invisible_primary_keyBoolean |                | Both           |
| sql_log_bin                               | Boolean        | Session        |
| sql_log_off                               | Boolean        | Both           |
| sql_mode                                  | Set            | Both           |
| sql_notes                                 | Boolean        | Both           |
| sql_quote_show_create                     | Boolean        | Both           |
| sql_replica_skip_counter                  | Integer        | Global         |
| sql_require_primary_key                   | Boolean        | Both           |
| sql_safe_updates                          | Boolean        | Both           |
| sql_select_limit                          | Integer        | Both           |
| sql_slave_skip_counter                    | Integer        | Global         |
| sql_warnings                              | Boolean        | Both           |
| ssl_ca                                    | File name      | Global         |
| ssl_capath                                | Directory name | Global         |
| ssl_cert                                  | File name      | Global         |
| ssl_cipher                                | String         | Global         |
| ssl_crl                                   | File name      | Global         |
| ssl_crlpath                               | Directory name | Global         |
| ssl_key                                   | File name      | Global         |
| ssl_session_cache_mode                    | Boolean        | Global         |
| ssl_session_cache_timeout                 | Integer        | Global         |
| stored_program_cache                      | Integer        | Global         |
| stored_program_definition_cache Integer   |                | Global         |
| super_read_only                           | Boolean        | Global         |
| sync_binlog                               | Integer        | Global         |
| sync_master_info                          | Integer        | Global         |
| sync_relay_log                            | Integer        | Global         |
| sync_relay_log_info                       | Integer        | Global         |
| sync_source_info                          | Integer        | Global         |
| syseventlog.facility                      | String         | Global         |
| syseventlog.include_pid                   | Boolean        | Global         |
| syseventlog.tag                           | String         | Global         |
| table_definition_cache                    | Integer        | Global         |

| Variable Name                                   | Variable Type | Variable Scope |
|-------------------------------------------------|---------------|----------------|
| table_encryption_privilege_check Boolean        |               | Global         |
| table_open_cache                                | Integer       | Global         |
| tablespace_definition_cache                     | Integer       | Global         |
| telemetry.otel_log_level                        | Enumeration   | Global         |
| telemetry.query_text_enabled                    | Boolean       | Global         |
| telemetry.trace_enabled                         | Boolean       | Global         |
| temptable_max_mmap                              | Integer       | Global         |
| temptable_max_ram                               | Integer       | Global         |
| temptable_use_mmap                              | Boolean       | Global         |
| terminology_use_previous                        | Enumeration   | Both           |
| thread_cache_size                               | Integer       | Global         |
| thread_pool_high_priority_connection Integer    |               | Both           |
| thread_pool_longrun_trx_limit                   | Integer       | Global         |
| thread_pool_max_active_query_threads Integer    |               | Global         |
| thread_pool_max_transactions_limitInteger       |               | Global         |
| thread_pool_max_unused_threadsInteger           |               | Global         |
| thread_pool_prio_kickup_timer                   | Integer       | Global         |
| thread_pool_query_threads_per_group Integer     |               | Global         |
| thread_pool_stall_limit                         | Integer       | Global         |
| thread_pool_transaction_delay                   | Integer       | Global         |
| time_zone                                       | String        | Both           |
| timestamp                                       | Numeric       | Session        |
| tls_ciphersuites                                | String        | Global         |
| tls_version                                     | String        | Global         |
| tmp_table_size                                  | Integer       | Both           |
| transaction_alloc_block_size                    | Integer       | Both           |
| transaction_allow_batching                      | Boolean       | Session        |
| transaction_isolation                           | Enumeration   | Both           |
| transaction_prealloc_size                       | Integer       | Both           |
| transaction_read_only                           | Boolean       | Both           |
| unique_checks                                   | Boolean       | Both           |
| updatable_views_with_limit                      | Boolean       | Both           |
| use_secondary_engine                            | Enumeration   | Session        |
| validate_password_check_user_name Boolean       |               | Global         |
| validate_password_dictionary_file File name     |               | Global         |
| validate_password_length                        | Integer       | Global         |
| validate_password_mixed_case_count Integer      |               | Global         |
| validate_password_number_countInteger           |               | Global         |
| validate_password_policy                        | Enumeration   | Global         |
| validate_password_special_char_count Integer    |               | Global         |
| validate_password.changed_characters_percentage | Integer       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| validate_password.check_user_name Boolean    |               | Global         |
| validate_password.dictionary_file File name  |               | Global         |
| validate_password.length                     | Integer       | Global         |
| validate_password.mixed_case_count Integer   |               | Global         |
| validate_password.number_count Integer       |               | Global         |
| validate_password.policy                     | Enumeration   | Global         |
| validate_password.special_char_count Integer |               | Global         |
| version_tokens_session                       | String        | Both           |
| wait_timeout                                 | Integer       | Both           |
| windowing_use_high_precision                 | Boolean       | Both           |
| xa_detach_on_prepare                         | Boolean       | Both           |

# <span id="page-129-0"></span>**7.1.9.3 Persisted System Variables**

The MySQL server maintains system variables that configure its operation. A system variable can have a global value that affects server operation as a whole, a session value that affects the current session, or both. Many system variables are dynamic and can be changed at runtime using the SET statement to affect operation of the current server instance. SET can also be used to persist certain global system variables to the mysqld-auto.cnf file in the data directory, to affect server operation for subsequent startups. RESET PERSIST removes persisted settings from mysqld-auto.cnf.

The following discussion describes aspects of persisting system variables:

- [Overview of Persisted System Variables](#page-129-1)
- [Syntax for Persisting System Variables](#page-130-0)
- [Obtaining Information About Persisted System Variables](#page-131-0)
- [Format and Server Handling of the mysqld-auto.cnf File](#page-131-1)
- [Persisting Sensitive System Variables](#page-132-0)

### <span id="page-129-1"></span>**Overview of Persisted System Variables**

The capability of persisting global system variables at runtime enables server configuration that persists across server startups. Although many system variables can be set at startup from a my.cnf option file, or at runtime using the SET statement, those methods of configuring the server either require login access to the server host, or do not provide the capability of persistently configuring the server at runtime or remotely:

- Modifying an option file requires direct access to that file, which requires login access to the MySQL server host. This is not always convenient.
- Modifying system variables with SET GLOBAL is a runtime capability that can be done from clients run locally or from remote hosts, but the changes affect only the currently running server instance. The settings are not persistent and do not carry over to subsequent server startups.

To augment administrative capabilities for server configuration beyond what is achievable by editing option files or using SET GLOBAL, MySQL provides variants of SET syntax that persist system variable settings to a file named mysqld-auto.cnf file in the data directory. Examples:

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
SET PERSIST_ONLY back_log = 100;
SET @@PERSIST_ONLY.back_log = 100;
```

MySQL also provides a RESET PERSIST statement for removing persisted system variables from mysqld-auto.cnf.

Server configuration performed by persisting system variables has these characteristics:

- Persisted settings are made at runtime.
- Persisted settings are permanent. They apply across server restarts.
- Persisted settings can be made from local clients or clients who connect from a remote host. This provides the convenience of remotely configuring multiple MySQL servers from a central client host.
- To persist system variables, you need not have login access to the MySQL server host or file system access to option files. Ability to persist settings is controlled using the MySQL privilege system. See [Section 7.1.9.1, "System Variable Privileges".](#page-110-0)
- An administrator with sufficient privileges can reconfigure a server by persisting system variables, then cause the server to use the changed settings immediately by executing a RESTART statement.
- Persisted settings provide immediate feedback about errors. An error in a manually entered setting might not be discovered until much later. SET statements that persist system variables avoid the possibility of malformed settings because settings with syntax errors do not succeed and do not change server configuration.

### <span id="page-130-0"></span>**Syntax for Persisting System Variables**

These SET syntax options are available for persisting system variables:

• To persist a global system variable to the mysqld-auto.cnf option file in the data directory, precede the variable name by the PERSIST keyword or the @@PERSIST. qualifier:

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
```

Like SET GLOBAL, SET PERSIST sets the global variable runtime value, but also writes the variable setting to the mysqld-auto.cnf file (replacing any existing variable setting if there is one).

• To persist a global system variable to the mysqld-auto.cnf file without setting the global variable runtime value, precede the variable name by the PERSIST\_ONLY keyword or the @@PERSIST\_ONLY. qualifier:

```
SET PERSIST_ONLY back_log = 1000;
SET @@PERSIST_ONLY.back_log = 1000;
```

Like PERSIST, PERSIST\_ONLY writes the variable setting to mysqld-auto.cnf. However, unlike PERSIST, PERSIST\_ONLY does not modify the global variable runtime value. This makes PERSIST\_ONLY suitable for configuring read-only system variables that can be set only at server startup.

For more information about SET, see Section 15.7.6.1, "SET Syntax for Variable Assignment".

These RESET PERSIST syntax options are available for removing persisted system variables:

• To remove all persisted variables from mysqld-auto.cnf, use RESET PERSIST without naming any system variable:

```
RESET PERSIST;
```

• To remove a specific persisted variable from mysqld-auto.cnf, name it in the statement:

```
RESET PERSIST system_var_name;
```

This includes plugin system variables, even if the plugin is not currently installed. If the variable is not present in the file, an error occurs.

• To remove a specific persisted variable from mysqld-auto.cnf, but produce a warning rather than an error if the variable is not present in the file, add an IF EXISTS clause to the previous syntax:

```
RESET PERSIST IF EXISTS system_var_name;
```

For more information about RESET PERSIST, see Section 15.7.8.7, "RESET PERSIST Statement".

Using SET to persist a global system variable to a value of DEFAULT or to its literal default value assigns the variable its default value and adds a setting for the variable to mysqld-auto.cnf. To remove the variable from the file, use RESET PERSIST.

Some system variables cannot be persisted. See [Section 7.1.9.4, "Nonpersistible and Persist-](#page-133-0)[Restricted System Variables".](#page-133-0)

A system variable implemented by a plugin can be persisted if the plugin is installed when the SET statement is executed. Assignment of the persisted plugin variable takes effect for subsequent server restarts if the plugin is still installed. If the plugin is no longer installed, the plugin variable does not exist when the server reads the mysqld-auto.cnf file. In this case, the server writes a warning to the error log and continues:

```
currently unknown variable 'var_name'
was read from the persisted config file
```

### <span id="page-131-0"></span>**Obtaining Information About Persisted System Variables**

The Performance Schema persisted\_variables table provides an SQL interface to the mysqldauto.cnf file, enabling its contents to be inspected at runtime using SELECT statements. See Section 29.12.14.1, "Performance Schema persisted\_variables Table".

The Performance Schema variables\_info table contains information showing when and by which user each system variable was most recently set. See Section 29.12.14.2, "Performance Schema variables\_info Table".

RESET PERSIST affects the contents of the persisted\_variables table because the table contents correspond to the contents of the mysqld-auto.cnf file. On the other hand, because RESET PERSIST does not change variable values, it has no effect on the contents of the variables\_info table until the server is restarted.

### <span id="page-131-1"></span>**Format and Server Handling of the mysqld-auto.cnf File**

The mysqld-auto.cnf file uses a JSON format like this (reformatted slightly for readability):

```
{
 "Version": 1,
 "mysql_server": {
 "max_connections": {
 "Value": "152",
 "Metadata": {
 "Timestamp": 1519921341372531,
 "User": "root",
 "Host": "localhost"
 }
 },
 "transaction_isolation": {
 "Value": "READ-COMMITTED",
 "Metadata": {
 "Timestamp": 1519921553880520,
 "User": "root",
 "Host": "localhost"
 }
 },
 "mysql_server_static_options": {
 "innodb_api_enable_mdl": {
 "Value": "0",
 "Metadata": {
 "Timestamp": 1519922873467872,
 "User": "root",
```

```
 "Host": "localhost"
 }
 },
 "log_replica_updates": {
 "Value": "1",
 "Metadata": {
 "Timestamp": 1519925628441588,
 "User": "root",
 "Host": "localhost"
 }
 }
 }
 }
}
```

At startup, the server processes the mysqld-auto.cnf file after all other option files (see Section 6.2.2.2, "Using Option Files"). The server handles the file contents as follows:

- If the [persisted\\_globals\\_load](#page-44-0) system variable is disabled, the server ignores the mysqldauto.cnf file.
- The "mysql\_server\_static\_options" section contains read-only variables persisted using SET PERSIST\_ONLY. The section may also (despite its name) contain certain dynamic variables that are not read only. All variables present inside this section are appended to the command line and processed with other command-line options.
- All remaining persisted variables are set by executing the equivalent of a SET GLOBAL statement later, just before the server starts listening for client connections. These settings therefore do not take effect until late in the startup process, which might be unsuitable for certain system variables. It may be preferable to set such variables in my.cnf rather than in mysqld-auto.cnf.

Management of the mysqld-auto.cnf file should be left to the server. Manipulation of the file should be performed only using SET and RESET PERSIST statements, not manually:

• Removal of the file results in a loss of all persisted settings at the next server startup. (This is permissible if your intent is to reconfigure the server without these settings.) To remove all settings in the file without removing the file itself, use this statement:

RESET PERSIST;

• Manual changes to the file may result in a parse error at server startup. In this case, the server reports an error and exits. If this issue occurs, start the server with the [persisted\\_globals\\_load](#page-44-0) system variable disabled or with the --no-defaults option. Alternatively, remove the mysqldauto.cnf file. However, as noted previously, removing this file results in a loss of all persisted settings.

### <span id="page-132-0"></span>**Persisting Sensitive System Variables**

MySQL 8.4 has the capability to store persisted system variable values containing sensitive data such as private keys or passwords securely, and to restrict viewing of the values. No MySQL Server system variables are currently marked as sensitive, but this capability allows system variables containing sensitive data to be persisted securely in the future. A mysqld-auto.cnf option file created by MySQL 8.4 cannot be read by older releases of MySQL Server.

![](_page_132_Picture_12.jpeg)

### **Note**

A keyring component must be enabled on the MySQL Server instance to support secure storage for persisted system variable values, rather than a keyring plugin, which do not support the function. See Section 8.4.4, "The MySQL Keyring".

In the mysqld-auto.cnf option file, the names and values of sensitive system variables are stored in an encrypted format, along with a generated file key to decrypt them. The generated file key is in turn encrypted using a master key (persisted\_variables\_key) that is stored in a keyring. When

the server starts up, the persisted sensitive system variables are decrypted and used. By default, if encrypted values are present in the option file but cannot be successfully decrypted at startup, their default settings are used. The optional most secure setting makes the server halt startup if the encrypted values cannot be decrypted.

The system variable [persist\\_sensitive\\_variables\\_in\\_plaintext](#page-45-0) controls whether the server is permitted to store the values of sensitive system variables in an unencrypted format, if keyring component support is not available at the time when SET PERSIST is used to set the value. It also controls whether or not the server can start if the encrypted values cannot be decrypted.

- The default setting, ON, encrypts the values if keyring component support is available, and persists them unencrypted (with a warning) if it is not. The next time any persisted system variable is set, if keyring support is available at that time, the server encrypts the values of any unencrypted sensitive system variables. The ON setting also allows the server to start if encrypted system variable values cannot be decrypted, in which case a warning is issued and the default values for the system variables are used. In that situation, their values cannot be changed until they can be decrypted.
- The most secure setting, OFF, means sensitive system variable values cannot be persisted if keyring component support is unavailable. The OFF setting also means the server does not start if encrypted system variable values cannot be decrypted.

The privilege SENSITIVE\_VARIABLES\_OBSERVER allows a holder to view the values of sensitive system variables in the Performance Schema tables global\_variables, session\_variables, variables\_by\_thread, and persisted\_variables, to issue SELECT statements to return their values, and to track changes to them in session trackers for connections. Users without this privilege cannot view or track those system variable values.

If a SET statement is issued for a sensitive system variable, the query is rewritten to replace the value with "<redacted>" before it is logged to the general log and audit log. This takes place even if secure storage through a keyring component is not available on the server instance.

## <span id="page-133-0"></span>**7.1.9.4 Nonpersistible and Persist-Restricted System Variables**

SET PERSIST and SET PERSIST\_ONLY enable global system variables to be persisted to the mysqld-auto.cnf option file in the data directory (see Section 15.7.6.1, "SET Syntax for Variable Assignment"). However, not all system variables can be persisted, or can be persisted only under certain restrictive conditions. Here are some reasons why a system variable might be nonpersistible or persist-restricted:

- Session system variables cannot be persisted. Session variables cannot be set at server startup, so there is no reason to persist them.
- A global system variable might involve sensitive data such that it should be settable only by a user with direct access to the server host.
- A global system variable might be read only (that is, set only by the server). In this case, it cannot be set by users at all, whether at server startup or at runtime.
- A global system variable might be intended only for internal use.

Nonpersistible system variables cannot be persisted under any circumstances. Persist-restricted system variables can be persisted with SET PERSIST\_ONLY, but only by users for which the following conditions are satisfied:

- The [persist\\_only\\_admin\\_x509\\_subject](#page-44-1) system variable is set to an SSL certificate X.509 Subject value.
- The user connects to the server using an encrypted connection and supplies an SSL certificate with the designated Subject value.
- The user has sufficient privileges to use SET PERSIST\_ONLY (see [Section 7.1.9.1, "System](#page-110-0) [Variable Privileges"](#page-110-0)).

For example, [protocol\\_version](#page-48-0) is read only and set only by the server, so it cannot be persisted under any circumstances. On the other hand, bind\_address is persist-restricted, so it can be set by users who satisfy the preceding conditions.

The following system variables are nonpersistible. This list may change with ongoing development.

```
audit_log_current_session
audit_log_filter_id
caching_sha2_password_digest_rounds
character_set_system
core_file
have_statement_timeout
have_symlink
hostname
innodb_version
keyring_hashicorp_auth_path
keyring_hashicorp_ca_path
keyring_hashicorp_caching
keyring_hashicorp_commit_auth_path
keyring_hashicorp_commit_ca_path
keyring_hashicorp_commit_caching
keyring_hashicorp_commit_role_id
keyring_hashicorp_commit_server_url
keyring_hashicorp_commit_store_path
keyring_hashicorp_role_id
keyring_hashicorp_secret_id
keyring_hashicorp_server_url
keyring_hashicorp_store_path
large_files_support
large_page_size
license
locked_in_memory
log_bin
log_bin_basename
log_bin_index
lower_case_file_system
ndb_version
ndb_version_string
persist_only_admin_x509_subject
persisted_globals_load
protocol_version
relay_log_basename
relay_log_index
server_uuid
skip_external_locking
system_time_zone
version_comment
version_compile_machine
version_compile_os
version_compile_zlib
```

Persist-restricted system variables are those that are read only and can be set on the command line or in an option file, other than [persist\\_only\\_admin\\_x509\\_subject](#page-44-1) and [persisted\\_globals\\_load](#page-44-0). This list may change with ongoing development.

```
audit_log_file
audit_log_format
auto_generate_certs
basedir
bind_address
caching_sha2_password_auto_generate_rsa_keys
caching_sha2_password_private_key_path
caching_sha2_password_public_key_path
character_sets_dir
datadir
ft_stopword_file
init_file
innodb_buffer_pool_load_at_startup
innodb_data_file_path
innodb_data_home_dir
innodb_dedicated_server
```

```
innodb_directories
innodb_force_load_corrupted
innodb_log_group_home_dir
innodb_page_size
innodb_read_only
innodb_temp_data_file_path
innodb_temp_tablespaces_dir
innodb_undo_directory
innodb_undo_tablespaces
lc_messages_dir
log_error
mecab_rc_file
named_pipe
pid_file
plugin_dir
port
relay_log
replica_load_tmpdir
secure_file_priv
sha256_password_auto_generate_rsa_keys
sha256_password_private_key_path
sha256_password_public_key_path
shared_memory
shared_memory_base_name
skip_networking
slave_load_tmpdir
socket
ssl_ca
ssl_capath
ssl_cert
ssl_crl
ssl_crlpath
ssl_key
tmpdir
version_tokens_session_number
```

To configure the server to enable persisting persist-restricted system variables, use this procedure:

- 1. Ensure that MySQL is configured to support encrypted connections. See Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".
- 2. Designate an SSL certificate X.509 Subject value that signifies the ability to persist persistrestricted system variables, and generate a certificate that has that Subject. See Section 8.3.3, "Creating SSL and RSA Certificates and Keys".
- 3. Start the server with [persist\\_only\\_admin\\_x509\\_subject](#page-44-1) set to the designated Subject value. For example, put these lines in your server my.cnf file:

```
[mysqld]
persist_only_admin_x509_subject="subject-value"
```

The format of the Subject value is the same as used for CREATE USER ... REQUIRE SUBJECT. See Section 15.7.1.3, "CREATE USER Statement".

You must perform this step directly on the MySQL server host because [persist\\_only\\_admin\\_x509\\_subject](#page-44-1) itself cannot be persisted at runtime.

- 4. Restart the server.
- 5. Distribute the SSL certificate that has the designated Subject value to users who are to be permitted to persist persist-restricted system variables.

Suppose that myclient-cert.pem is the SSL certificate to be used by clients who can persist persist-restricted system variables. Display the certificate contents using the openssl command:

```
$> openssl x509 -text -in myclient-cert.pem
Certificate:
 Data:
```

```
 Version: 3 (0x2)
 Serial Number: 2 (0x2)
 Signature Algorithm: md5WithRSAEncryption
 Issuer: C=US, ST=IL, L=Chicago, O=MyOrg, OU=CA, CN=MyCN
 Validity
 Not Before: Oct 18 17:03:03 2018 GMT
 Not After : Oct 15 17:03:03 2028 GMT
 Subject: C=US, ST=IL, L=Chicago, O=MyOrg, OU=client, CN=MyCN
...
```

The openssl output shows that the certificate Subject value is:

```
C=US, ST=IL, L=Chicago, O=MyOrg, OU=client, CN=MyCN
```

To specify the Subject for MySQL, use this format:

```
/C=US/ST=IL/L=Chicago/O=MyOrg/OU=client/CN=MyCN
```

Configure the server my.cnf file with the Subject value:

```
[mysqld]
persist_only_admin_x509_subject="/C=US/ST=IL/L=Chicago/O=MyOrg/OU=client/CN=MyCN"
```

Restart the server so that the new configuration takes effect.

Distribute the SSL certificate (and any other associated SSL files) to the appropriate users. Such a user then connects to the server with the certificate and any other SSL options required to establish an encrypted connection.

To use X.509, clients must specify the --ssl-key and --ssl-cert options to connect. It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified. For example:

```
$> mysql --ssl-key=myclient-key.pem --ssl-cert=myclient-cert.pem --ssl-ca=mycacert.pem
```

Assuming that the user has sufficient privileges to use SET PERSIST\_ONLY, persist-restricted system variables can be persisted like this:

```
mysql> SET PERSIST_ONLY socket = '/tmp/mysql.sock';
Query OK, 0 rows affected (0.00 sec)
```

If the server is not configured to enable persisting persist-restricted system variables, or the user does not satisfy the required conditions for that capability, an error occurs:

```
mysql> SET PERSIST_ONLY socket = '/tmp/mysql.sock';
ERROR 1238 (HY000): Variable 'socket' is a non persistent read only variable
```