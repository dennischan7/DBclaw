---
source: MySQL 8.4 Reference
title: 00_Overview
---

This table provides an overview of the command options, system variables, and status variables provided by X Plugin.

**Table 22.2 X Plugin Option and Variable Reference**

| Name                     | Cmd-Line                                           | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------|----------------------------------------------------|-------------|------------|------------|-----------|---------|
| mysqlx                   | Yes                                                | Yes         |            |            |           |         |
| Mysqlx_aborted_clients   |                                                    |             |            | Yes        | Global    | No      |
| Mysqlx_address           |                                                    |             |            | Yes        | Global    | No      |
| mysqlx_bind_address Yes  |                                                    | Yes         | Yes        |            | Global    | No      |
| Mysqlx_bytes_received    |                                                    |             |            | Yes        | Both      | No      |
|                          | Mysqlx_bytes_received_compressed_payload           |             |            | Yes        | Both      | No      |
|                          | Mysqlx_bytes_received_uncompressed_frame           |             |            | Yes        | Both      | No      |
| Mysqlx_bytes_sent        |                                                    |             |            | Yes        | Both      | No      |
|                          | Mysqlx_bytes_sent_compressed_payload               |             |            | Yes        | Both      | No      |
|                          | Mysqlx_bytes_sent_uncompressed_frame               |             |            | Yes        | Both      | No      |
|                          | Mysqlx_compression_algorithm                       |             |            | Yes        | Session   | No      |
|                          | mysqlx_compression_algorithms<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_compression_level |                                                    |             |            | Yes        | Session   | No      |
| mysqlx_connect_timeout   | Yes                                                | Yes         | Yes        |            | Global    | Yes     |
|                          | Mysqlx_connection_accept_errors                    |             |            | Yes        | Both      | No      |
| Mysqlx_connection_errors |                                                    |             |            | Yes        | Both      | No      |
|                          | Mysqlx_connections_accepted                        |             |            | Yes        | Global    | No      |
|                          | Mysqlx_connections_closed                          |             |            | Yes        | Global    | No      |
|                          | Mysqlx_connections_rejected                        |             |            | Yes        | Global    | No      |
| Mysqlx_crud_create_view  |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_delete       |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_drop_view    |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_find         |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_insert       |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_modify_view  |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_crud_update       |                                                    |             |            | Yes        | Both      | No      |
|                          | mysqlx_deflate_default_compression_level<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_deflate_max_client_compression_level<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_document_id_unique_prefix<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_enable_hello_notice<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_errors_sent       |                                                    |             |            | Yes        | Both      | No      |
|                          | Mysqlx_errors_unknown_message_type                 |             |            | Yes        | Both      | No      |
| Mysqlx_expect_close      |                                                    |             |            | Yes        | Both      | No      |
| Mysqlx_expect_open       |                                                    |             |            | Yes        | Both      | No      |
|                          | mysqlx_idle_worker_thread_timeout<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_init_error        |                                                    |             |            | Yes        | Both      | No      |
|                          | mysqlx_interactive_timeout<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_lz4_default_compression_level<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_lz4_max_client_compression_level<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_max_allowed_packet<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |

| Name                        | Cmd-Line                             | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|--------------------------------------|-------------|------------|------------|-----------|---------|
| mysqlx_max_connections      | Yes                                  | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_messages_sent        |                                      |             |            | Yes        | Both      | No      |
|                             | mysqlx_min_worker_threads<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_notice_global_sent   |                                      |             |            | Yes        | Both      | No      |
| Mysqlx_notice_other_sent    |                                      |             |            | Yes        | Both      | No      |
|                             | Mysqlx_notice_warning_sent           |             |            | Yes        | Both      | No      |
|                             | Mysqlx_notified_by_group_replication |             |            | Yes        | Both      | No      |
| Mysqlx_port                 |                                      |             |            | Yes        | Global    | No      |
| mysqlx_port                 | Yes                                  | Yes         | Yes        |            | Global    | No      |
| mysqlx_port_open_timeout    | Yes                                  | Yes         | Yes        |            | Global    | No      |
| mysqlx_read_timeout Yes     |                                      | Yes         | Yes        |            | Session   | Yes     |
| Mysqlx_rows_sent            |                                      |             |            | Yes        | Both      | No      |
| Mysqlx_sessions             |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_accepted    |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_closed      |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_fatal_error |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_killed      |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_rejected    |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_socket               |                                      |             |            | Yes        | Global    | No      |
| mysqlx_socketYes            |                                      | Yes         | Yes        |            | Global    | No      |
|                             | Mysqlx_ssl_accept_renegotiates       |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_accepts          |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_active           |                                      |             |            | Yes        | Both      | No      |
| mysqlx_ssl_caYes            |                                      | Yes         | Yes        |            | Global    | No      |
| mysqlx_ssl_capath Yes       |                                      | Yes         | Yes        |            | Global    | No      |
| mysqlx_ssl_certYes          |                                      | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_cipher           |                                      |             |            | Yes        | Both      | No      |
| mysqlx_ssl_cipher Yes       |                                      | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_cipher_list      |                                      |             |            | Yes        | Both      | No      |
| mysqlx_ssl_crlYes           |                                      | Yes         | Yes        |            | Global    | No      |
| mysqlx_ssl_crlpath Yes      |                                      | Yes         | Yes        |            | Global    | No      |
|                             | Mysqlx_ssl_ctx_verify_depth          |             |            | Yes        | Both      | No      |
|                             | Mysqlx_ssl_ctx_verify_mode           |             |            | Yes        | Both      | No      |
|                             | Mysqlx_ssl_finished_accepts          |             |            | Yes        | Global    | No      |
| mysqlx_ssl_keyYes           |                                      | Yes         | Yes        |            | Global    | No      |
|                             | Mysqlx_ssl_server_not_after          |             |            | Yes        | Global    | No      |
|                             | Mysqlx_ssl_server_not_before         |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_verify_depth     |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_verify_mode      |                                      |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_version          |                                      |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_create_collection        |             |            | Yes        | Both      | No      |

| Name                     | Cmd-Line                                        | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------|-------------------------------------------------|-------------|------------|------------|-----------|---------|
|                          | Mysqlx_stmt_create_collection_index             |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_disable_notices                     |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_drop_collection                     |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_drop_collection_index               |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_enable_notices                      |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_ensure_collection                   |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_execute_mysqlx                      |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_execute_sql  |                                                 |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_execute_xplugin                     |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_get_collection_options              |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_kill_client  |                                                 |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_clients |                                                 |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_notices |                                                 |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_objects |                                                 |             |            | Yes        | Both      | No      |
|                          | Mysqlx_stmt_modify_collection_options           |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_ping         |                                                 |             |            | Yes        | Both      | No      |
| mysqlx_wait_timeout Yes  |                                                 | Yes         | Yes        |            | Session   | Yes     |
| Mysqlx_worker_threads    |                                                 |             |            | Yes        | Global    | No      |
|                          | Mysqlx_worker_threads_active                    |             |            | Yes        | Global    | No      |
| mysqlx_write_timeout Yes |                                                 | Yes         | Yes        |            | Session   | Yes     |
|                          | mysqlx_zstd_default_compression_level<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_zstd_max_client_compression_level<br>Yes | Yes         | Yes        |            | Global    | Yes     |

# <span id="page-26-1"></span><span id="page-26-0"></span>**22.5.6.2 X Plugin Options and System Variables**

To control activation of X Plugin, use this option:

• [--mysqlx\[=value\]](#page-26-0)

| Command-Line Format | mysqlx[=value]       |
|---------------------|----------------------|
| Type                | Enumeration          |
| Default Value       | ON                   |
| Valid Values        | ON                   |
|                     | OFF                  |
|                     | FORCE                |
|                     | FORCE_PLUS_PERMANENT |

This option controls how the server loads X Plugin at startup. In MySQL 8.4, X Plugin is enabled by default, but this option may be used to control its activation state.

The option value should be one of those available for plugin-loading options, as described in Section 7.6.1, "Installing and Uninstalling Plugins".

If X Plugin is enabled, it exposes several system variables that permit control over its operation:

<span id="page-26-2"></span>• [mysqlx\\_bind\\_address](#page-26-2)

| Command-Line Format  | mysqlx-bind-address=addr |
|----------------------|--------------------------|
| System Variable      | mysqlx_bind_address      |
| Scope                | Global                   |
| Dynamic              | No                       |
| SET_VAR Hint Applies | No                       |
| Type                 | String                   |
| Default Value        | *                        |

The network address on which X Plugin listens for TCP/IP connections. This variable is not dynamic and can be configured only at startup. This is the X Plugin equivalent of the bind\_address system variable; see that variable description for more information.

By default, X Plugin accepts TCP/IP connections on all server host IPv4 interfaces, and, if the server host supports IPv6, on all IPv6 interfaces. If [mysqlx\\_bind\\_address](#page-26-2) is specified, its value must satisfy these requirements:

- A single address value, which may specify a single non-wildcard IP address (either IPv4 or IPv6), or a host name, or one of the wildcard address formats that permit listening on multiple network interfaces (\*, 0.0.0.0, or ::).
- A list of comma-separated values. When the variable names a list of multiple values, each value must specify a single non-wildcard IP address (either IPv4 or IPv6) or a host name. Wildcard address formats (\*, 0.0.0.0, or ::) are not allowed in a list of values.
- The value may also include a network namespace specifier.

IP addresses can be specified as IPv4 or IPv6 addresses. For any value that is a host name, X Plugin resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP addresses, X Plugin uses the first IPv4 address if there are any, or the first IPv6 address otherwise.

X Plugin treats different types of addresses as follows:

- If the address is \*, X Plugin accepts TCP/IP connections on all server host IPv4 interfaces, and, if the server host supports IPv6, on all IPv6 interfaces. Use this address to permit both IPv4 and IPv6 connections for X Plugin. This value is the default. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is 0.0.0.0, X Plugin accepts TCP/IP connections on all server host IPv4 interfaces. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is ::, X Plugin accepts TCP/IP connections on all server host IPv4 and IPv6 interfaces. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is an IPv4-mapped address, X Plugin accepts TCP/IP connections for that address, in either IPv4 or IPv6 format. For example, if X Plugin is bound to ::ffff:127.0.0.1, a client such as MySQL Shell can connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.
- If the address is a "regular" IPv4 or IPv6 address (such as 127.0.0.1 or ::1), X Plugin accepts TCP/IP connections only for that IPv4 or IPv6 address.

These rules apply to specifying a network namespace for an address:

- A network namespace can be specified for an IP address or a host name.
- A network namespace cannot be specified for a wildcard IP address.

- For a given address, the network namespace is optional. If given, it must be specified as a /ns suffix immediately following the address.
- An address with no /ns suffix uses the host system global namespace. The global namespace is therefore the default.
- An address with a /ns suffix uses the namespace named ns.
- The host system must support network namespaces and each named namespace must previously have been set up. Naming a nonexistent namespace produces an error.
- If the variable value specifies multiple addresses, it can include addresses in the global namespace, in named namespaces, or a mix.

For additional information about network namespaces, see Section 7.1.14, "Network Namespace Support".

![](_page_28_Picture_7.jpeg)

#### **Important**

Because X Plugin is not a mandatory plugin, it does not prevent server startup if there is an error in the specified address or list of addresses (as MySQL Server does for bind\_address errors). With X Plugin, if one of the listed addresses cannot be parsed or if X Plugin cannot bind to it, the address is skipped, an error message is logged, and X Plugin attempts to bind to each of the remaining addresses. X Plugin's [Mysqlx\\_address](#page-38-9) status variable displays only those addresses from the list for which the bind succeeded. If none of the listed addresses results in a successful bind, or if a single specified address fails, X Plugin logs the error message [ER\\_XPLUGIN\\_FAILED\\_TO\\_PREPARE\\_IO\\_INTERFACES](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_xplugin_failed_to_prepare_io_interfaces) stating that X Protocol cannot be used. [mysqlx\\_bind\\_address](#page-26-2) is not dynamic, so to fix any issues you must stop the server, correct the system variable value, and restart the server.

<span id="page-28-0"></span>• [mysqlx\\_compression\\_algorithms](#page-28-0)

| Command-Line Format  | mysqlx-compression                     |
|----------------------|----------------------------------------|
|                      | algorithms=value                       |
| System Variable      | mysqlx_compression_algorithms          |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Set                                    |
| Default Value        | deflate_stream,lz4_message,zstd_stream |
| Valid Values         | deflate_stream                         |
|                      | lz4_message                            |
|                      | zstd_stream                            |

The compression algorithms that are permitted for use on X Protocol connections. By default, the Deflate, LZ4, and zstd algorithms are all permitted. To disallow any of the algorithms, set [mysqlx\\_compression\\_algorithms](#page-28-0) to include only the ones you permit. The algorithm names deflate\_stream, lz4\_message, and zstd\_stream can be specified in any combination, and the order and case are not important. If you set the system variable to the empty string, no compression algorithms are permitted and only uncompressed connections are used. Use the algorithm-specific system variables to adjust the default and maximum compression level for each permitted algorithm.

For more details, and information on how connection compression for X Protocol relates to the equivalent settings for MySQL Server, see [Section 22.5.5, "Connection Compression with X Plugin"](#page-20-2).

<span id="page-29-2"></span>• [mysqlx\\_connect\\_timeout](#page-29-2)

| Command-Line Format  | mysqlx-connect-timeout=# |
|----------------------|--------------------------|
| System Variable      | mysqlx_connect_timeout   |
| Scope                | Global                   |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Type                 | Integer                  |
| Default Value        | 30                       |
| Minimum Value        | 1                        |
| Maximum Value        | 1000000000               |
| Unit                 | seconds                  |

The number of seconds X Plugin waits for the first packet to be received from newly connected clients. This is the X Plugin equivalent of connect\_timeout; see that variable description for more information.

<span id="page-29-0"></span>• [mysqlx\\_deflate\\_default\\_compression\\_level](#page-29-0)

| Command-Line Format  |                                            |
|----------------------|--------------------------------------------|
|                      | mysqlx_deflate_default_compression_level=# |
| System Variable      | mysqlx_deflate_default_compression_level   |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 3                                          |
| Minimum Value        | 1                                          |
| Maximum Value        | 9                                          |

The default compression level that the server uses for the Deflate algorithm on X Protocol connections. Specify the level as an integer from 1 (the lowest compression effort) to 9 (the highest effort). This level is used if the client does not request a compression level during capability negotiation. If you do not specify this system variable, the server uses level 3 as the default. For more information, see [Section 22.5.5, "Connection Compression with X Plugin"](#page-20-2).

<span id="page-29-1"></span>• [mysqlx\\_deflate\\_max\\_client\\_compression\\_level](#page-29-1)

| Command-Line Format  |                                               |  |
|----------------------|-----------------------------------------------|--|
|                      | mysqlx_deflate_max_client_compression_level=# |  |
| System Variable      | mysqlx_deflate_max_client_compression_level   |  |
| Scope                | Global                                        |  |
| Dynamic              | Yes                                           |  |
| SET_VAR Hint Applies | No                                            |  |
| Type                 | Integer                                       |  |
| Default Value        | 5                                             |  |

| Minimum Value | 1 |
|---------------|---|
| Maximum Value | 9 |

The maximum compression level that the server permits for the Deflate algorithm on X Protocol connections. The range is the same as for the default compression level for this algorithm. If the client requests a higher compression level than this, the server uses the level you set here. If you do not specify this system variable, the server sets a maximum compression level of 5.

#### <span id="page-30-0"></span>• [mysqlx\\_document\\_id\\_unique\\_prefix](#page-30-0)

| Command-Line Format  | mysqlx-document-id-unique-prefix=# |
|----------------------|------------------------------------|
| System Variable      | mysqlx_document_id_unique_prefix   |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Integer                            |
| Default Value        | 0                                  |
| Minimum Value        | 0                                  |
| Maximum Value        | 65535                              |

Sets the first 4 bytes of document IDs generated by the server when documents are added to a collection. By setting this variable to a unique value per instance, you can ensure document IDs are unique across instances. See [Understanding Document IDs.](https://dev.mysql.com/doc/x-devapi-userguide/en/understanding-automatic-document-ids.md)

#### <span id="page-30-1"></span>• [mysqlx\\_enable\\_hello\\_notice](#page-30-1)

| Command-Line Format  | mysqlx-enable-hello-notice[={OFF <br>ON}] |
|----------------------|-------------------------------------------|
| System Variable      | mysqlx_enable_hello_notice                |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Boolean                                   |
| Default Value        | ON                                        |

Controls messages sent to classic MySQL protocol clients that try to connect over X Protocol. When enabled, clients which do not support X Protocol that attempt to connect to the server X Protocol port receive an error explaining they are using the wrong protocol.

# <span id="page-30-2"></span>• [mysqlx\\_idle\\_worker\\_thread\\_timeout](#page-30-2)

| Command-Line Format  | mysqlx-idle-worker-thread<br>timeout=# |
|----------------------|----------------------------------------|
| System Variable      | mysqlx_idle_worker_thread_timeout      |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Integer                                |
| Default Value        | 60                                     |
| Minimum Value        | 0                                      |

| Maximum Value | 3600    |
|---------------|---------|
| Unit          | seconds |

The number of seconds after which idle worker threads are terminated.

<span id="page-31-2"></span>• [mysqlx\\_interactive\\_timeout](#page-31-2)

| Command-Line Format  | mysqlx-interactive-timeout=# |
|----------------------|------------------------------|
| System Variable      | mysqlx_interactive_timeout   |
| Scope                | Global                       |
| Dynamic              | Yes                          |
| SET_VAR Hint Applies | No                           |
| Type                 | Integer                      |
| Default Value        | 28800                        |
| Minimum Value        | 1                            |
| Maximum Value        | 2147483                      |
| Unit                 | seconds                      |

The default value of the [mysqlx\\_wait\\_timeout](#page-36-2) session variable for interactive clients. (The number of seconds to wait for interactive clients to timeout.)

<span id="page-31-0"></span>• [mysqlx\\_lz4\\_default\\_compression\\_level](#page-31-0)

| Command-Line Format  |                                        |
|----------------------|----------------------------------------|
|                      | mysqlx_lz4_default_compression_level=# |
| System Variable      | mysqlx_lz4_default_compression_level   |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Integer                                |
| Default Value        | 2                                      |
| Minimum Value        | 0                                      |
| Maximum Value        | 16                                     |

The default compression level that the server uses for the LZ4 algorithm on X Protocol connections. Specify the level as an integer from 0 (the lowest compression effort) to 16 (the highest effort). This level is used if the client does not request a compression level during capability negotiation. If you do not specify this system variable, the server uses level 2 as the default. For more information, see [Section 22.5.5, "Connection Compression with X Plugin".](#page-20-2)

<span id="page-31-1"></span>• [mysqlx\\_lz4\\_max\\_client\\_compression\\_level](#page-31-1)

| Command-Line Format  |                                           |
|----------------------|-------------------------------------------|
|                      | mysqlx_lz4_max_client_compression_level=# |
| System Variable      | mysqlx_lz4_max_client_compression_level   |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |

| Default Value | 8  |
|---------------|----|
| Minimum Value | 0  |
| Maximum Value | 16 |

The maximum compression level that the server permits for the LZ4 algorithm on X Protocol connections. The range is the same as for the default compression level for this algorithm. If the client requests a higher compression level than this, the server uses the level you set here. If you do not specify this system variable, the server sets a maximum compression level of 8.

<span id="page-32-0"></span>• [mysqlx\\_max\\_allowed\\_packet](#page-32-0)

| Command-Line Format  | mysqlx-max-allowed-packet=# |
|----------------------|-----------------------------|
| System Variable      | mysqlx_max_allowed_packet   |
| Scope                | Global                      |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | No                          |
| Type                 | Integer                     |
| Default Value        | 67108864                    |
| Minimum Value        | 512                         |
| Maximum Value        | 1073741824                  |
| Unit                 | bytes                       |

The maximum size of network packets that can be received by X Plugin. This limit also applies when compression is used for the connection, so the network packet must be smaller than this size after the message has been decompressed. This is the X Plugin equivalent of max\_allowed\_packet; see that variable description for more information.

<span id="page-32-1"></span>• [mysqlx\\_max\\_connections](#page-32-1)

| Command-Line Format  | mysqlx-max-connections=# |
|----------------------|--------------------------|
| System Variable      | mysqlx_max_connections   |
| Scope                | Global                   |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Type                 | Integer                  |
| Default Value        | 100                      |
| Minimum Value        | 1                        |
| Maximum Value        | 65535                    |

The maximum number of concurrent client connections X Plugin can accept. This is the X Plugin equivalent of max\_connections; see that variable description for more information.

For modifications to this variable, if the new value is smaller than the current number of connections, the new limit is taken into account only for new connections.

<span id="page-32-2"></span>• [mysqlx\\_min\\_worker\\_threads](#page-32-2)

| Command-Line Format | mysqlx-min-worker-threads=# |
|---------------------|-----------------------------|
| System Variable     | mysqlx_min_worker_threads   |
| Scope               | Global<br>3803              |

| Dynamic              | Yes     |
|----------------------|---------|
| SET_VAR Hint Applies | No      |
| Type                 | Integer |
| Default Value        | 2       |
| Minimum Value        | 1       |
| Maximum Value        | 100     |

The minimum number of worker threads used by X Plugin for handling client requests.

#### <span id="page-33-0"></span>• [mysqlx\\_port](#page-33-0)

| Command-Line Format  | mysqlx-port=port_num |
|----------------------|----------------------|
| System Variable      | mysqlx_port          |
| Scope                | Global               |
| Dynamic              | No                   |
| SET_VAR Hint Applies | No                   |
| Type                 | Integer              |
| Default Value        | 33060                |
| Minimum Value        | 1                    |
| Maximum Value        | 65535                |

The network port on which X Plugin listens for TCP/IP connections. This is the X Plugin equivalent of port; see that variable description for more information.

#### <span id="page-33-1"></span>• [mysqlx\\_port\\_open\\_timeout](#page-33-1)

| Command-Line Format  | mysqlx-port-open-timeout=# |
|----------------------|----------------------------|
| System Variable      | mysqlx_port_open_timeout   |
| Scope                | Global                     |
| Dynamic              | No                         |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 0                          |
| Minimum Value        | 0                          |
| Maximum Value        | 120                        |
| Unit                 | seconds                    |

The number of seconds X Plugin waits for a TCP/IP port to become free.

### <span id="page-33-2"></span>• [mysqlx\\_read\\_timeout](#page-33-2)

| Command-Line Format  | mysqlx-read-timeout=# |
|----------------------|-----------------------|
| System Variable      | mysqlx_read_timeout   |
| Scope                | Session               |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 30                    |

| Maximum Value | 2147483 |
|---------------|---------|
| Unit          | seconds |
| Minimum Value | 1       |

The number of seconds that X Plugin waits for blocking read operations to complete. After this time, if the read operation is not successful, X Plugin closes the connection and returns a warning notice with the error code ER\_IO\_READ\_ERROR to the client application.

<span id="page-34-0"></span>• [mysqlx\\_socket](#page-34-0)

| Command-Line Format  | mysqlx-socket=file_name |
|----------------------|-------------------------|
| System Variable      | mysqlx_socket           |
| Scope                | Global                  |
| Dynamic              | No                      |
| SET_VAR Hint Applies | No                      |
| Type                 | String                  |
| Default Value        | /tmp/mysqlx.sock        |

The path to a Unix socket file which X Plugin uses for connections. This setting is only used by MySQL Server when running on Unix operating systems. Clients can use this socket to connect to MySQL Server using X Plugin.

The default [mysqlx\\_socket](#page-34-0) path and file name is based on the default path and file name for the main socket file for MySQL Server, with the addition of an x appended to the file name. The default path and file name for the main socket file is /tmp/mysql.sock, therefore the default path and file name for the X Plugin socket file is /tmp/mysqlx.sock.

If you specify an alternative path and file name for the main socket file at server startup using the socket system variable, this does not affect the default for the X Plugin socket file. In this situation, if you want to store both sockets at a single path, you must set the [mysqlx\\_socket](#page-34-0) system variable as well. For example in a configuration file:

```
socket=/home/sockets/mysqld/mysql.sock
mysqlx_socket=/home/sockets/xplugin/xplugin.sock
```

If you change the default path and file name for the main socket file at compile time using the MYSQL\_UNIX\_ADDR compile option, this does affect the default for the X Plugin socket file, which is formed by appending an x to the MYSQL\_UNIX\_ADDR file name. If you want to set a different default for the X Plugin socket file at compile time, use the MYSQLX\_UNIX\_ADDR compile option.

The MYSQLX\_UNIX\_PORT environment variable can also be used to set a default for the X Plugin socket file at server startup (see Section 6.9, "Environment Variables"). If you set this environment variable, it overrides the compiled MYSQLX\_UNIX\_ADDR value, but is overridden by the [mysqlx\\_socket](#page-34-0) value.

<span id="page-34-1"></span>• [mysqlx\\_ssl\\_ca](#page-34-1)

| Command-Line Format  | mysqlx-ssl-ca=file_name |
|----------------------|-------------------------|
| System Variable      | mysqlx_ssl_ca           |
| Scope                | Global                  |
| Dynamic              | No                      |
| SET_VAR Hint Applies | No                      |
| Type                 | File name               |

| Default Value | NULL |
|---------------|------|
|---------------|------|

The [mysqlx\\_ssl\\_ca](#page-34-1) system variable is like ssl\_ca, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-35-0"></span>• [mysqlx\\_ssl\\_capath](#page-35-0)

| Command-Line Format  | mysqlx-ssl-capath=dir_name |
|----------------------|----------------------------|
| System Variable      | mysqlx_ssl_capath          |
| Scope                | Global                     |
| Dynamic              | No                         |
| SET_VAR Hint Applies | No                         |
| Type                 | Directory name             |
| Default Value        | NULL                       |

The [mysqlx\\_ssl\\_capath](#page-35-0) system variable is like ssl\_capath, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-35-1"></span>• [mysqlx\\_ssl\\_cert](#page-35-1)

| Command-Line Format  | mysqlx-ssl-cert=file_name |
|----------------------|---------------------------|
| System Variable      | mysqlx_ssl_cert           |
| Scope                | Global                    |
| Dynamic              | No                        |
| SET_VAR Hint Applies | No                        |
| Type                 | File name                 |
| Default Value        | NULL                      |

The [mysqlx\\_ssl\\_cert](#page-35-1) system variable is like ssl\_cert, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-35-2"></span>• [mysqlx\\_ssl\\_cipher](#page-35-2)

| Command-Line Format  | mysqlx-ssl-cipher=name |
|----------------------|------------------------|
| System Variable      | mysqlx_ssl_cipher      |
| Scope                | Global                 |
| Dynamic              | No                     |
| SET_VAR Hint Applies | No                     |
| Type                 | String                 |
| Default Value        | NULL                   |

The [mysqlx\\_ssl\\_cipher](#page-35-2) system variable is like ssl\_cipher, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-35-3"></span>• [mysqlx\\_ssl\\_crl](#page-35-3)

| System Variable      | mysqlx_ssl_crl |
|----------------------|----------------|
| Scope                | Global         |
| Dynamic              | No             |
| SET_VAR Hint Applies | No             |
| Type                 | File name      |
| Default Value        | NULL           |

The [mysqlx\\_ssl\\_crl](#page-35-3) system variable is like ssl\_crl, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-36-0"></span>• [mysqlx\\_ssl\\_crlpath](#page-36-0)

| Command-Line Format  | mysqlx-ssl-crlpath=dir_name |
|----------------------|-----------------------------|
| System Variable      | mysqlx_ssl_crlpath          |
| Scope                | Global                      |
| Dynamic              | No                          |
| SET_VAR Hint Applies | No                          |
| Type                 | Directory name              |
| Default Value        | NULL                        |

The [mysqlx\\_ssl\\_crlpath](#page-36-0) system variable is like ssl\_crlpath, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-36-1"></span>• [mysqlx\\_ssl\\_key](#page-36-1)

| Command-Line Format  | mysqlx-ssl-key=file_name |
|----------------------|--------------------------|
| System Variable      | mysqlx_ssl_key           |
| Scope                | Global                   |
| Dynamic              | No                       |
| SET_VAR Hint Applies | No                       |
| Type                 | File name                |
| Default Value        | NULL                     |

The [mysqlx\\_ssl\\_key](#page-36-1) system variable is like ssl\_key, except that it applies to X Plugin rather than the MySQL Server main connection interface. For information about configuring encryption support for X Plugin, see [Section 22.5.3, "Using Encrypted Connections with X Plugin".](#page-18-0)

<span id="page-36-2"></span>• [mysqlx\\_wait\\_timeout](#page-36-2)

| Command-Line Format  | mysqlx-wait-timeout=# |
|----------------------|-----------------------|
| System Variable      | mysqlx_wait_timeout   |
| Scope                | Session               |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 28800                 |
| Minimum Value        | 1<br>3807             |

| Maximum Value | 2147483 |
|---------------|---------|
| Unit          | seconds |

The number of seconds that X Plugin waits for activity on a connection. After this time, if the read operation is not successful, X Plugin closes the connection. If the client is noninteractive, the initial value of the session variable is copied from the global [mysqlx\\_wait\\_timeout](#page-36-2) variable. For interactive clients, the initial value is copied from the session [mysqlx\\_interactive\\_timeout](#page-31-2).

#### <span id="page-37-2"></span>• [mysqlx\\_write\\_timeout](#page-37-2)

| Command-Line Format  | mysqlx-write-timeout=# |
|----------------------|------------------------|
| System Variable      | mysqlx_write_timeout   |
| Scope                | Session                |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Integer                |
| Default Value        | 60                     |
| Minimum Value        | 1                      |
| Maximum Value        | 2147483                |
| Unit                 | seconds                |

The number of seconds that X Plugin waits for blocking write operations to complete. After this time, if the write operation is not successful, X Plugin closes the connection.

# <span id="page-37-0"></span>• [mysqlx\\_zstd\\_default\\_compression\\_level](#page-37-0)

| Command-Line Format  |                                         |
|----------------------|-----------------------------------------|
|                      | mysqlx_zstd_default_compression_level=# |
| System Variable      | mysqlx_zstd_default_compression_level   |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Integer                                 |
| Default Value        | 3                                       |
| Minimum Value        | -131072                                 |
| Maximum Value        | 22                                      |
|                      |                                         |

The default compression level that the server uses for the zstd algorithm on X Protocol connections. For versions of the zstd library from 1.4.0, you can set positive values from 1 to 22 (the highest compression effort), or negative values which represent progressively lower effort. A value of 0 is converted to a value of 1. For earlier versions of the zstd library, you can only specify the value 3. This level is used if the client does not request a compression level during capability negotiation. If you do not specify this system variable, the server uses level 3 as the default. For more information, see [Section 22.5.5, "Connection Compression with X Plugin".](#page-20-2)

#### <span id="page-37-1"></span>• [mysqlx\\_zstd\\_max\\_client\\_compression\\_level](#page-37-1)

| Command-Line Format |                                            |
|---------------------|--------------------------------------------|
|                     | mysqlx_zstd_max_client_compression_level=# |
| System Variable     | mysqlx_zstd_max_client_compression_level   |
| Scope               | Global                                     |

| Dynamic              | Yes     |
|----------------------|---------|
| SET_VAR Hint Applies | No      |
| Type                 | Integer |
| Default Value        | 11      |
| Minimum Value        | -131072 |
| Maximum Value        | 22      |

The maximum compression level that the server permits for the zstd algorithm on X Protocol connections. The range is the same as for the default compression level for this algorithm. If the client requests a higher compression level than this, the server uses the level you set here. If you do not specify this system variable, the server sets a maximum compression level of 11.

# <span id="page-38-8"></span><span id="page-38-0"></span>**22.5.6.3 X Plugin Status Variables**

The X Plugin status variables have the following meanings.

• [Mysqlx\\_aborted\\_clients](#page-38-8)

The number of clients that were disconnected because of an input or output error.

<span id="page-38-9"></span>• [Mysqlx\\_address](#page-38-9)

The network address or addresses for which X Plugin accepts TCP/IP connections. If multiple addresses were specified using the [mysqlx\\_bind\\_address](#page-26-2) system variable, [Mysqlx\\_address](#page-38-9) displays only those addresses for which the bind succeeded. If the bind has failed for every network address specified by [mysqlx\\_bind\\_address](#page-26-2), or if the skip\_networking option has been used, the value of [Mysqlx\\_address](#page-38-9) is UNDEFINED. If X Plugin startup is not yet complete, the value of [Mysqlx\\_address](#page-38-9) is empty.

<span id="page-38-7"></span>• [Mysqlx\\_bytes\\_received](#page-38-7)

The total number of bytes received through the network. If compression is used for the connection, this figure comprises compressed message payloads measured before decompression ([Mysqlx\\_bytes\\_received\\_compressed\\_payload](#page-38-5)), any items in compressed messages that were not compressed such as X Protocol headers, and any uncompressed messages.

<span id="page-38-5"></span>• [Mysqlx\\_bytes\\_received\\_compressed\\_payload](#page-38-5)

The number of bytes received as compressed message payloads, measured before decompression.

<span id="page-38-6"></span>• [Mysqlx\\_bytes\\_received\\_uncompressed\\_frame](#page-38-6)

The number of bytes received as compressed message payloads, measured after decompression.

<span id="page-38-2"></span>• [Mysqlx\\_bytes\\_sent](#page-38-2)

The total number of bytes sent through the network. If compression is used for the connection, this figure comprises compressed message payloads measured after compression ([Mysqlx\\_bytes\\_sent\\_compressed\\_payload](#page-38-3)), any items in compressed messages that were not compressed such as X Protocol headers, and any uncompressed messages.

<span id="page-38-3"></span>• [Mysqlx\\_bytes\\_sent\\_compressed\\_payload](#page-38-3)

The number of bytes sent as compressed message payloads, measured after compression.

<span id="page-38-4"></span>• [Mysqlx\\_bytes\\_sent\\_uncompressed\\_frame](#page-38-4)

The number of bytes sent as compressed message payloads, measured before compression.

<span id="page-38-1"></span>• [Mysqlx\\_compression\\_algorithm](#page-38-1)

(Session scope) The compression algorithm in use for the X Protocol connection for this session. The permitted compression algorithms are listed by the [mysqlx\\_compression\\_algorithms](#page-28-0) system variable.

<span id="page-39-0"></span>• [Mysqlx\\_compression\\_level](#page-39-0)

(Session scope) The compression level in use for the X Protocol connection for this session.

<span id="page-39-1"></span>• [Mysqlx\\_connection\\_accept\\_errors](#page-39-1)

The number of connections which have caused accept errors.

<span id="page-39-2"></span>• [Mysqlx\\_connection\\_errors](#page-39-2)

The number of connections which have caused errors.

<span id="page-39-3"></span>• [Mysqlx\\_connections\\_accepted](#page-39-3)

The number of connections which have been accepted.

<span id="page-39-4"></span>• [Mysqlx\\_connections\\_closed](#page-39-4)

The number of connections which have been closed.

<span id="page-39-5"></span>• [Mysqlx\\_connections\\_rejected](#page-39-5)

The number of connections which have been rejected.

<span id="page-39-6"></span>• [Mysqlx\\_crud\\_create\\_view](#page-39-6)

The number of create view requests received.

<span id="page-39-7"></span>• [Mysqlx\\_crud\\_delete](#page-39-7)

The number of delete requests received.

<span id="page-39-8"></span>• [Mysqlx\\_crud\\_drop\\_view](#page-39-8)

The number of drop view requests received.

<span id="page-39-9"></span>• [Mysqlx\\_crud\\_find](#page-39-9)

The number of find requests received.

<span id="page-39-10"></span>• [Mysqlx\\_crud\\_insert](#page-39-10)

The number of insert requests received.

<span id="page-39-11"></span>• [Mysqlx\\_crud\\_modify\\_view](#page-39-11)

The number of modify view requests received.

<span id="page-39-12"></span>• [Mysqlx\\_crud\\_update](#page-39-12)

The number of update requests received.

<span id="page-39-13"></span>• [Mysqlx\\_cursor\\_close](#page-39-13)

The number of cursor-close messages received

<span id="page-39-14"></span>• [Mysqlx\\_cursor\\_fetch](#page-39-14)

The number of cursor-fetch messages received

<span id="page-40-12"></span>• [Mysqlx\\_cursor\\_open](#page-40-12)

The number of cursor-open messages received

<span id="page-40-0"></span>• [Mysqlx\\_errors\\_sent](#page-40-0)

The number of errors sent to clients.

<span id="page-40-1"></span>• [Mysqlx\\_errors\\_unknown\\_message\\_type](#page-40-1)

The number of unknown message types that have been received.

<span id="page-40-2"></span>• [Mysqlx\\_expect\\_close](#page-40-2)

The number of expectation blocks closed.

<span id="page-40-3"></span>• [Mysqlx\\_expect\\_open](#page-40-3)

The number of expectation blocks opened.

<span id="page-40-4"></span>• [Mysqlx\\_init\\_error](#page-40-4)

The number of errors during initialisation.

<span id="page-40-5"></span>• [Mysqlx\\_messages\\_sent](#page-40-5)

The total number of messages of all types sent to clients.

<span id="page-40-6"></span>• [Mysqlx\\_notice\\_global\\_sent](#page-40-6)

The number of global notifications sent to clients.

<span id="page-40-7"></span>• [Mysqlx\\_notice\\_other\\_sent](#page-40-7)

The number of other types of notices sent back to clients.

<span id="page-40-8"></span>• [Mysqlx\\_notice\\_warning\\_sent](#page-40-8)

The number of warning notices sent back to clients.

<span id="page-40-9"></span>• [Mysqlx\\_notified\\_by\\_group\\_replication](#page-40-9)

Number of Group Replication notifications sent to clients.

<span id="page-40-10"></span>• [Mysqlx\\_port](#page-40-10)

The TCP port which X Plugin is listening to. If a network bind has failed, or if the skip\_networking system variable is enabled, the value shows UNDEFINED.

<span id="page-40-13"></span>• [Mysqlx\\_prep\\_deallocate](#page-40-13)

The number of prepared-statement-deallocate messages received

<span id="page-40-14"></span>• [Mysqlx\\_prep\\_execute](#page-40-14)

The number of prepared-statement-execute messages received

<span id="page-40-15"></span>• [Mysqlx\\_prep\\_prepare](#page-40-15)

The number of prepared-statement messages received

<span id="page-40-11"></span>• [Mysqlx\\_rows\\_sent](#page-40-11)

The number of rows sent back to clients.

<span id="page-41-0"></span>• [Mysqlx\\_sessions](#page-41-0)

The number of sessions that have been opened.

<span id="page-41-1"></span>• [Mysqlx\\_sessions\\_accepted](#page-41-1)

The number of session attempts which have been accepted.

<span id="page-41-2"></span>• [Mysqlx\\_sessions\\_closed](#page-41-2)

The number of sessions that have been closed.

<span id="page-41-3"></span>• [Mysqlx\\_sessions\\_fatal\\_error](#page-41-3)

The number of sessions that have closed with a fatal error.

<span id="page-41-4"></span>• [Mysqlx\\_sessions\\_killed](#page-41-4)

The number of sessions which have been killed.

<span id="page-41-5"></span>• [Mysqlx\\_sessions\\_rejected](#page-41-5)

The number of session attempts which have been rejected.

<span id="page-41-6"></span>• [Mysqlx\\_socket](#page-41-6)

The Unix socket which X Plugin is listening to.

<span id="page-41-7"></span>• [Mysqlx\\_ssl\\_accept\\_renegotiates](#page-41-7)

The number of negotiations needed to establish the connection.

<span id="page-41-8"></span>• [Mysqlx\\_ssl\\_accepts](#page-41-8)

The number of accepted SSL connections.

<span id="page-41-9"></span>• [Mysqlx\\_ssl\\_active](#page-41-9)

If SSL is active.

<span id="page-41-10"></span>• [Mysqlx\\_ssl\\_cipher](#page-41-10)

The current SSL cipher (empty for non-SSL connections).

<span id="page-41-11"></span>• [Mysqlx\\_ssl\\_cipher\\_list](#page-41-11)

A list of possible SSL ciphers (empty for non-SSL connections).

<span id="page-41-12"></span>• [Mysqlx\\_ssl\\_ctx\\_verify\\_depth](#page-41-12)

The certificate verification depth limit currently set in ctx.

<span id="page-41-13"></span>• [Mysqlx\\_ssl\\_ctx\\_verify\\_mode](#page-41-13)

The certificate verification mode currently set in ctx.

<span id="page-41-14"></span>• [Mysqlx\\_ssl\\_finished\\_accepts](#page-41-14)

The number of successful SSL connections to the server.

<span id="page-41-15"></span>• [Mysqlx\\_ssl\\_server\\_not\\_after](#page-41-15)

The last date for which the SSL certificate is valid.

<span id="page-41-16"></span>• [Mysqlx\\_ssl\\_server\\_not\\_before](#page-41-16)

The first date for which the SSL certificate is valid.

<span id="page-42-0"></span>• [Mysqlx\\_ssl\\_verify\\_depth](#page-42-0)

The certificate verification depth for SSL connections.

<span id="page-42-1"></span>• [Mysqlx\\_ssl\\_verify\\_mode](#page-42-1)

The certificate verification mode for SSL connections.

<span id="page-42-2"></span>• [Mysqlx\\_ssl\\_version](#page-42-2)

The name of the protocol used for SSL connections.

<span id="page-42-3"></span>• [Mysqlx\\_stmt\\_create\\_collection](#page-42-3)

The number of create collection statements received.

<span id="page-42-4"></span>• [Mysqlx\\_stmt\\_create\\_collection\\_index](#page-42-4)

The number of create collection index statements received.

<span id="page-42-5"></span>• [Mysqlx\\_stmt\\_disable\\_notices](#page-42-5)

The number of disable notice statements received.

<span id="page-42-6"></span>• [Mysqlx\\_stmt\\_drop\\_collection](#page-42-6)

The number of drop collection statements received.

<span id="page-42-7"></span>• [Mysqlx\\_stmt\\_drop\\_collection\\_index](#page-42-7)

The number of drop collection index statements received.

<span id="page-42-8"></span>• [Mysqlx\\_stmt\\_enable\\_notices](#page-42-8)

The number of enable notice statements received.

<span id="page-42-9"></span>• [Mysqlx\\_stmt\\_ensure\\_collection](#page-42-9)

The number of ensure collection statements received.

<span id="page-42-10"></span>• [Mysqlx\\_stmt\\_execute\\_mysqlx](#page-42-10)

The number of StmtExecute messages received with namespace set to mysqlx.

<span id="page-42-11"></span>• [Mysqlx\\_stmt\\_execute\\_sql](#page-42-11)

The number of StmtExecute requests received for the SQL namespace.

<span id="page-42-12"></span>• [Mysqlx\\_stmt\\_execute\\_xplugin](#page-42-12)

This status variable is no longer used.

<span id="page-42-13"></span>• [Mysqlx\\_stmt\\_get\\_collection\\_options](#page-42-13)

The number of get collection object statements received.

<span id="page-42-14"></span>• [Mysqlx\\_stmt\\_kill\\_client](#page-42-14)

The number of kill client statements received.

<span id="page-42-15"></span>• [Mysqlx\\_stmt\\_list\\_clients](#page-42-15)

The number of list client statements received.

<span id="page-43-0"></span>• [Mysqlx\\_stmt\\_list\\_notices](#page-43-0)

The number of list notice statements received.

<span id="page-43-1"></span>• [Mysqlx\\_stmt\\_list\\_objects](#page-43-1)

The number of list object statements received.

<span id="page-43-2"></span>• [Mysqlx\\_stmt\\_modify\\_collection\\_options](#page-43-2)

The number of modify collection options statements received.

<span id="page-43-3"></span>• [Mysqlx\\_stmt\\_ping](#page-43-3)

The number of ping statements received.

<span id="page-43-4"></span>• [Mysqlx\\_worker\\_threads](#page-43-4)

The number of worker threads available.

• [Mysqlx\\_worker\\_threads\\_active](#page-43-5)

The number of worker threads currently used.

# <span id="page-43-5"></span>**22.5.7 Monitoring X Plugin**

For general X Plugin monitoring, use the status variables that it exposes. See [Section 22.5.6.3,](#page-38-0) ["X Plugin Status Variables"](#page-38-0). For information specifically about monitoring the effects of message compression, see [Monitoring Connection Compression for X Plugin](#page-23-0).

# **Monitoring SQL Generated by X Plugin**

This section describes how to monitor the SQL statements which X Plugin generates when you run X DevAPI operations. When you execute a CRUD statement, it is translated into SQL and executed against the server. To be able to monitor the generated SQL, the Performance Schema tables must be enabled. The SQL is registered under the performance\_schema.events\_statements\_current, performance\_schema.events\_statements\_history, and performance\_schema.events\_statements\_history\_long tables. The following example uses the world\_x schema, imported as part of the quickstart tutorials in this section. We use MySQL Shell in Python mode, and the \sql command which enables you to issue SQL statements without changing to SQL mode. This is important, because if you instead try to switch to SQL mode, the procedure shows the result of this operation rather than the X DevAPI operation. The \sql command is used in the same way if you are using MySQL Shell in JavaScript mode.

1. Check if the events\_statements\_history consumer is enabled. Issue:

```
mysql-py> \sql SELECT enabled FROM performance_schema.setup_consumers WHERE NAME = 'events_statements_history'
+---------+
| enabled |
+---------+
| YES |
+---------+
```

2. Check if all instruments report data to the consumer. Issue:

```
mysql-py> \sql SELECT NAME, ENABLED, TIMED FROM performance_schema.setup_instruments WHERE NAME LIKE 'statement/%' AND NOT (ENABLED and TIMED)
```

If this statement reports at least one row, you need to enable the instruments. See Section 29.4, "Performance Schema Runtime Configuration".

3. Get the thread ID of the current connection. Issue:

mysql-py> **\sql SELECT thread\_id INTO @id FROM performance\_schema.threads WHERE processlist\_id=connection\_id()**

4. Execute the X DevAPI CRUD operation for which you want to see the generated SQL. For example, issue:

```
mysql-py> db.CountryInfo.find("Name = :country").bind("country", "Italy")
```

You must not issue any further operations for the next step to show the correct result.

5. Show the last SQL query made by this thread ID. Issue:

```
mysql-py> \sql SELECT THREAD_ID, MYSQL_ERRNO,SQL_TEXT FROM performance_schema.events_statements_history WHERE THREAD_ID=@id ORDER BY TIMER_START DESC LIMIT 1;
+-----------+-------------+--------------------------------------------------------------------------------------+
| THREAD_ID | MYSQL_ERRNO | SQL_TEXT |
+-----------+-------------+--------------------------------------------------------------------------------------+
| 29 | 0 | SELECT doc FROM `world_x`.`CountryInfo` WHERE (JSON_EXTRACT(doc,'$.Name') = 'Italy') |
+-----------+-------------+--------------------------------------------------------------------------------------+
```

The result shows the SQL generated by X Plugin based on the most recent statement, in this case the X DevAPI CRUD operation from the previous step.

# Chapter 23 InnoDB Cluster

This chapter introduces MySQL InnoDB Cluster, which combines MySQL technologies to enable you to deploy and administer a complete integrated high availability solution for MySQL. This content is a high-level overview of InnoDB Cluster, for full documentation, see [MySQL InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster.md).

![](_page_46_Picture_2.jpeg)

### **Important**

InnoDB Cluster does not provide support for MySQL NDB Cluster. For more information about MySQL NDB Cluster, see Chapter 25, [MySQL NDB Cluster](#page-50-0) [8.4](#page-50-0) and [Section 25.2.6, "MySQL Server Using InnoDB Compared with NDB](#page-67-0) [Cluster"](#page-67-0).

An InnoDB Cluster consists of at least three MySQL Server instances, and it provides high-availability and scaling features. InnoDB Cluster uses the following MySQL technologies:

- [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/), which is an advanced client and code editor for MySQL.
- MySQL Server, and Group Replication, which enables a set of MySQL instances to provide highavailability. InnoDB Cluster provides an alternative, easy to use programmatic way to work with Group Replication.
- [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.4/en/), a lightweight middleware that provides transparent routing between your application and InnoDB Cluster.

The following diagram shows an overview of how these technologies work together:

![](_page_46_Figure_10.jpeg)

**Figure 23.1 InnoDB Cluster overview**

Being built on MySQL Group Replication, provides features such as automatic membership management, fault tolerance, automatic failover, and so on. An InnoDB Cluster usually runs in a singleprimary mode, with one primary instance (read-write) and multiple secondary instances (read-only). Advanced users can also take advantage of a multi-primary mode, where all instances are primaries. You can even change the topology of the cluster while InnoDB Cluster is online, to ensure the highest possible availability.

You work with InnoDB Cluster using the [AdminAPI](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-overview.md), provided as part of MySQL Shell. AdminAPI is available in JavaScript and Python, and is well suited to scripting and automation of deployments of MySQL to achieve high-availability and scalability. By using MySQL Shell's AdminAPI, you can avoid the need to configure many instances manually. Instead, AdminAPI provides an effective modern interface to sets of MySQL instances and enables you to provision, administer, and monitor your deployment from one central tool.

To get started with InnoDB Cluster you need to [download](https://dev.mysql.com/downloads/shell/) and [install](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md) MySQL Shell. You need some hosts with MySQL Server instances installed, and you can also [install](https://dev.mysql.com/doc/mysql-router/8.4/en/mysql-router-installation.md) MySQL Router.

InnoDB Cluster supports MySQL Clone, which enables you to provision instances simply. In the past, to provision a new instance before it joins a set of MySQL instances you would need to somehow manually transfer the transactions to the joining instance. This could involve making file copies, manually copying them, and so on. Using InnoDB Cluster, you can simply [add an instance](https://dev.mysql.com/doc/mysql-shell/8.4/en/add-instances-cluster.md) to the cluster and it is automatically provisioned.

Similarly, InnoDB Cluster is tightly integrated with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.4/en/) and you can use AdminAPI to [work](https://dev.mysql.com/doc/mysql-shell/8.4/en/registered-routers.md) [with](https://dev.mysql.com/doc/mysql-shell/8.4/en/registered-routers.md) them together. MySQL Router can automatically configure itself based on an InnoDB Cluster, in a process called [bootstrapping](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-bootstrapping-router.md), which removes the need for you to configure routing manually. MySQL Router then transparently connects client applications to the InnoDB Cluster, providing routing and load-balancing for client connections. This integration also enables you to administer some aspects of a MySQL Router bootstrapped against an InnoDB Cluster using AdminAPI. InnoDB Cluster status information includes details about MySQL Routers bootstrapped against the cluster. Operations enable you to [create MySQL Router users](https://dev.mysql.com/doc/mysql-shell/8.4/en/configuring-router-user.md) at the cluster level, to work with the MySQL Routers bootstrapped against the cluster, and so on.

For more information on these technologies, see the user documentation linked in the descriptions. In addition to this user documentation, there is developer documentation for all AdminAPI methods in the MySQL Shell JavaScript API Reference or MySQL Shell Python API Reference, available from [Connectors and APIs](https://dev.mysql.com/doc/index-connectors.md).

# Chapter 24 InnoDB ReplicaSet

This chapter introduces MySQL InnoDB ReplicaSet, which combines MySQL technologies to enable you to deploy and administer Chapter 19, Replication. This content is a high-level overview of InnoDB ReplicaSet, for full documentation, see [MySQL InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-replicaset.md)

An InnoDB ReplicaSet consists of at least two MySQL Server instances, and it provides all of the MySQL Replication features you are familiar with, such as read scale-out and data security. InnoDB ReplicaSet uses the following MySQL technologies:

- [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/), which is an advanced client and code editor for MySQL.
- MySQL Server, and Chapter 19, Replication, which enables a set of MySQL instances to provide availability and asynchronous read scale-out. InnoDB ReplicaSet provides an alternative, easy to use programmatic way to work with Replication.
- [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.4/en/), a lightweight middleware that provides transparent routing between your application and InnoDB ReplicaSet.

The interface to an InnoDB ReplicaSet is similar to [MySQL InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster.md), you use MySQL Shell to work with MySQL Server instances as a ReplicaSet, and MySQL Router is also tightly integrated in the same way as InnoDB Cluster.

Being based on MySQL Replication, an InnoDB ReplicaSet has a single primary, which replicates to one or more secondary instances. An InnoDB ReplicaSet does not provide all of the features which InnoDB Cluster provides, such as automatic failover, or multi-primary mode. But, it does support features such as configuring, adding, and removing instances in a similar way. You can manually switch over or fail over to a secondary instance, for example in the event of a failure. You can even adopt an existing Replication deployment and then administer it as an InnoDB ReplicaSet.

You work with InnoDB ReplicaSet using the [AdminAPI](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-overview.md), provided as part of MySQL Shell. AdminAPI is available in JavaScript and Python, and is well suited to scripting and automation of deployments of MySQL to achieve high-availability and scalability. By using MySQL Shell's AdminAPI, you can avoid the need to configure many instances manually. Instead, AdminAPI provides an effective modern interface to sets of MySQL instances and enables you to provision, administer, and monitor your deployment from one central tool.

To get started with InnoDB ReplicaSet you need to [download](https://dev.mysql.com/downloads/shell/) and [install](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md) MySQL Shell. You need some hosts with MySQL Server instances installed, and you can also [install](https://dev.mysql.com/doc/mysql-router/8.4/en/mysql-router-installation.md) MySQL Router.

InnoDB ReplicaSet supports MySQL Clone, which enables you to provision instances simply. In the past, to provision a new instance before it joined a MySQL Replication deployment, you would need to somehow manually transfer the transactions to the joining instance. This could involve making file copies, manually copying them, and so on. You can simply [add an instance](https://dev.mysql.com/doc/mysql-shell/8.4/en/add-instance-replicaset.md) to the replica set and it is automatically provisioned.

Similarly, InnoDB ReplicaSet is tightly integrated with [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.4/en/), and you can use AdminAPI to [work with](https://dev.mysql.com/doc/mysql-shell/8.4/en/registered-routers.md) them together. MySQL Router can automatically configure itself based on an InnoDB ReplicaSet, in a process called [bootstrapping](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-bootstrapping-router.md), which removes the need for you to configure routing manually. MySQL Router then transparently connects client applications to the InnoDB ReplicaSet, providing routing and load-balancing for client connections. This integration also enables you to administer some aspects of a MySQL Router bootstrapped against an InnoDB ReplicaSet using AdminAPI. InnoDB ReplicaSet status information includes details about MySQL Routers bootstrapped against the ReplicaSet. Operations enable you to [create MySQL Router users](https://dev.mysql.com/doc/mysql-shell/8.4/en/configuring-router-user.md) at the ReplicaSet level, to work with the MySQL Routers bootstrapped against the ReplicaSet, and so on.

For more information on these technologies, see the user documentation linked in the descriptions. In addition to this user documentation, there is developer documentation for all AdminAPI methods in the MySQL Shell JavaScript API Reference or MySQL Shell Python API Reference, available from [Connectors and APIs](https://dev.mysql.com/doc/index-connectors.md).

# <span id="page-50-0"></span>Chapter 25 MySQL NDB Cluster 8.4

# **Table of Contents**

| 25.1 General Information 3822                                                                |      |
|----------------------------------------------------------------------------------------------|------|
| 25.2 NDB Cluster Overview 3824                                                               |      |
| 25.2.1 NDB Cluster Core Concepts 3826                                                        |      |
| 25.2.2 NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions 3829                |      |
| 25.2.3 NDB Cluster Hardware, Software, and Networking Requirements 3832                      |      |
| 25.2.4 What is New in MySQL NDB Cluster 8.4 3833                                             |      |
| 25.2.5 Options, Variables, and Parameters Added, Deprecated or Removed in NDB 8.4 3837       |      |
| 25.2.6 MySQL Server Using InnoDB Compared with NDB Cluster 3838                              |      |
| 25.2.7 Known Limitations of NDB Cluster 3840                                                 |      |
| 25.3 NDB Cluster Installation 3852                                                           |      |
| 25.3.1 Installation of NDB Cluster on Linux 3854                                             |      |
| 25.3.2 Installing NDB Cluster on Windows                                                     | 3862 |
| 25.3.3 Initial Configuration of NDB Cluster 3871                                             |      |
| 25.3.4 Initial Startup of NDB Cluster 3872                                                   |      |
| 25.3.5 NDB Cluster Example with Tables and Data 3873                                         |      |
| 25.3.6 Safe Shutdown and Restart of NDB Cluster 3876                                         |      |
| 25.3.7 Upgrading and Downgrading NDB Cluster 3877                                            |      |
| 25.4 Configuration of NDB Cluster 3878                                                       |      |
| 25.4.1 Quick Test Setup of NDB Cluster 3878                                                  |      |
| 25.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables              | 3880 |
| 25.4.3 NDB Cluster Configuration Files 3902                                                  |      |
| 25.4.4 Using High-Speed Interconnects with NDB Cluster 4104                                  |      |
| 25.5 NDB Cluster Programs 4105                                                               |      |
| 25.5.1 ndbd — The NDB Cluster Data Node Daemon 4105                                          |      |
| 25.5.2 ndbinfo_select_all — Select From ndbinfo Tables 4114                                  |      |
| 25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded) 4119                       |      |
| 25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon 4120                              |      |
| 25.5.5 ndb_mgm — The NDB Cluster Management Client 4130                                      |      |
| 25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster                 |      |
| Tables 4135                                                                                  |      |
| 25.5.7 ndb_config — Extract NDB Cluster Configuration Information 4140                       |      |
| 25.5.8 ndb_delete_all — Delete All Rows from an NDB Table 4151                               |      |
| 25.5.9 ndb_desc — Describe NDB Tables 4154                                                   |      |
| 25.5.10 ndb_drop_index — Drop Index from an NDB Table 4163                                   |      |
| 25.5.11 ndb_drop_table — Drop an NDB Table 4167                                              |      |
| 25.5.12 ndb_error_reporter — NDB Error-Reporting Utility                                     | 4171 |
| 25.5.13 ndb_import — Import CSV Data Into NDB 4172                                           |      |
| 25.5.14 ndb_index_stat — NDB Index Statistics Utility 4185                                   |      |
| 25.5.15 ndb_move_data — NDB Data Copy Utility 4191                                           |      |
| 25.5.16 ndb_perror — Obtain NDB Error Message Information 4196                               |      |
| 25.5.17 ndb_print_backup_file — Print NDB Backup File Contents 4198                          |      |
| 25.5.18 ndb_print_file — Print NDB Disk Data File Contents 4202                              |      |
| 25.5.19 ndb_print_frag_file — Print NDB Fragment List File Contents 4203                     |      |
| 25.5.20 ndb_print_schema_file — Print NDB Schema File Contents 4204                          |      |
| 25.5.21 ndb_print_sys_file — Print NDB System File Contents 4204                             |      |
| 25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log 4204               |      |
| 25.5.23 ndb_restore — Restore an NDB Cluster Backup                                          | 4206 |
| 25.5.24 ndb_secretsfile_reader — Obtain Key Information from an Encrypted NDB Data File 4228 |      |
| 25.5.25 ndb_select_all — Print Rows from an NDB Table 4230                                   |      |
| 25.5.26 ndb_select_count — Print Row Counts for NDB Tables                                   | 4236 |
| 25.5.27 ndb_show_tables — Display List of NDB Tables                                         | 4239 |

| 25.5.28 ndb_sign_keys — Create, Sign, and Manage TLS Keys and Certificates for NDB |      |
|------------------------------------------------------------------------------------|------|
| Cluster 4243                                                                       |      |
| 25.5.29 ndb_size.pl — NDBCLUSTER Size Requirement Estimator 4251                   |      |
| 25.5.30 ndb_top — View CPU usage information for NDB threads 4253                  |      |
| 25.5.31 ndb_waiter — Wait for NDB Cluster to Reach a Given Status 4258             |      |
| 25.5.32 ndbxfrm — Compress, Decompress, Encrypt, and Decrypt Files Created by NDB  |      |
| Cluster 4264                                                                       |      |
| 25.6 Management of NDB Cluster 4269                                                |      |
| 25.6.1 Commands in the NDB Cluster Management Client 4270                          |      |
| 25.6.2 NDB Cluster Log Messages 4276                                               |      |
| 25.6.3 Event Reports Generated in NDB Cluster 4294                                 |      |
| 25.6.4 Summary of NDB Cluster Start Phases 4306                                    |      |
| 25.6.5 Performing a Rolling Restart of an NDB Cluster 4308                         |      |
| 25.6.6 NDB Cluster Single User Mode 4310                                           |      |
| 25.6.7 Adding NDB Cluster Data Nodes Online 4311                                   |      |
| 25.6.8 Online Backup of NDB Cluster 4321                                           |      |
| 25.6.9 Importing Data Into MySQL Cluster 4327                                      |      |
| 25.6.10 MySQL Server Usage for NDB Cluster                                         | 4328 |
| 25.6.11 NDB Cluster Disk Data Tables 4330                                          |      |
| 25.6.12 Online Operations with ALTER TABLE in NDB Cluster 4336                     |      |
| 25.6.13 Privilege Synchronization and NDB_STORED_USER 4339                         |      |
| 25.6.14 NDB API Statistics Counters and Variables 4340                             |      |
| 25.6.15 ndbinfo: The NDB Cluster Information Database 4352                         |      |
| 25.6.16 INFORMATION_SCHEMA Tables for NDB Cluster 4440                             |      |
| 25.6.17 NDB Cluster and the Performance Schema 4441                                |      |
| 25.6.18 Quick Reference: NDB Cluster SQL Statements 4442                           |      |
| 25.6.19 NDB Cluster Security 4449                                                  |      |
| 25.7 NDB Cluster Replication 4462                                                  |      |
| 25.7.1 NDB Cluster Replication: Abbreviations and Symbols 4464                     |      |
| 25.7.2 General Requirements for NDB Cluster Replication 4464                       |      |
| 25.7.3 Known Issues in NDB Cluster Replication 4465                                |      |
| 25.7.4 NDB Cluster Replication Schema and Tables 4471                              |      |
| 25.7.5 Preparing the NDB Cluster for Replication 4478                              |      |
| 25.7.6 Starting NDB Cluster Replication (Single Replication Channel) 4480          |      |
| 25.7.7 Using Two Replication Channels for NDB Cluster Replication 4482             |      |
| 25.7.8 Implementing Failover with NDB Cluster Replication 4483                     |      |
| 25.7.9 NDB Cluster Backups With NDB Cluster Replication 4484                       |      |
| 25.7.10 NDB Cluster Replication: Bidirectional and Circular Replication 4490       |      |
| 25.7.11 NDB Cluster Replication Using the Multithreaded Applier 4494               |      |
| 25.7.12 NDB Cluster Replication Conflict Resolution 4497                           |      |
| 25.8 NDB Cluster Release Notes 4514                                                |      |

This chapter provides information about MySQL NDB Cluster, a high-availability, high-redundancy version of MySQL adapted for the distributed computing environment, as well as information specific to NDB Cluster 8.4 (NDB 8.4.7), based on version 8.4 of the NDB storage engine. See [Section 25.2.4,](#page-62-0) ["What is New in MySQL NDB Cluster 8.4"](#page-62-0), for information about differences in NDB 8.4 as compared to earlier releases. See [MySQL NDB Cluster 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-cluster.md) for information about NDB Cluster 8.0. Both NDB 8.0 and NDB 8.4 are intended for use in production environments. NDB Cluster 7.6 and 7.5 are previous GA releases still supported in production, although new deployments can and should use either of MySQL NDB Cluster 8.0 or 8.4.

NDB Cluster 7.4 and older release series are no longer supported or maintained.

# <span id="page-51-0"></span>**25.1 General Information**

MySQL NDB Cluster uses the MySQL server with the NDB storage engine. Support for the [NDB](#page-50-0) storage engine is not included in standard MySQL Server 8.4 binaries built by Oracle. Instead, users of NDB

Cluster binaries from Oracle should upgrade to the most recent binary release of NDB Cluster for supported platforms—these include RPMs that should work with most Linux distributions. NDB Cluster 8.4 users who build from source should use the sources provided for MySQL 8.4 and build with the options required to provide NDB support. (Locations where the sources can be obtained are listed later in this section.)

![](_page_52_Picture_2.jpeg)

#### **Important**

MySQL NDB Cluster does not support InnoDB Cluster, which must be deployed using MySQL Server InnoDB storage engine as well as additional applications that are not included in the NDB Cluster distribution. MySQL Server 8.4 binaries cannot be used with MySQL NDB Cluster. For more information about deploying and using InnoDB Cluster, see [MySQL AdminAPI.](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-userguide.md) [Section 25.2.6,](#page-67-0) ["MySQL Server Using InnoDB Compared with NDB Cluster"](#page-67-0), discusses differences between the NDB and InnoDB storage engines.

**Supported Platforms.** NDB Cluster is currently available and supported on a number of platforms. For exact levels of support available for on specific combinations of operating system versions, operating system distributions, and hardware platforms, please refer to [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/cluster.md) [supportedplatforms/cluster.html](https://www.mysql.com/support/supportedplatforms/cluster.md).

**Availability.** NDB Cluster binary and source packages are available for supported platforms from <https://dev.mysql.com/downloads/cluster/>.

**Version strings used in NDB Cluster software.** The version string displayed by the mysql client supplied with the MySQL NDB Cluster distribution uses this format:

```
mysql-mysql_server_version-cluster
```

mysql\_server\_version represents the version of the MySQL Server on which the NDB Cluster release is based. Building from source using -DWITH\_NDB or the equivalent adds the -cluster suffix to the version string. (See [Section 25.3.1.4, "Building NDB Cluster from Source on Linux"](#page-90-0), and [Section 25.3.2.2, "Compiling and Installing NDB Cluster from Source on Windows"](#page-95-0).) You can see this format used in the mysql client, as shown here:

```
$> mysql
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 8.4.7-cluster Source distribution
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> SELECT VERSION()\G
*************************** 1. row ***************************
VERSION(): 8.4.7-cluster
1 row in set (0.00 sec)
```

The version string displayed by other NDB Cluster programs not normally included with the MySQL 8.4 distribution uses this format:

```
mysql-mysql_server_version ndb-ndb_engine_version
```

mysql\_server\_version represents the version of the MySQL Server on which the NDB Cluster release is based. For NDB Cluster 8.4, this is 8.4.n, where n is the release number. ndb\_engine\_version is the version of the [NDB](#page-50-0) storage engine used by this release of the NDB Cluster software. For NDB 8.4, this number is the same as the MySQL Server version. You can see this format used in the output of the SHOW command in the ndb\_mgm client, like this:

```
ndb_mgm> SHOW
Connected to Management Server at: localhost:1186 (using cleartext)
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
```

```
id=1 @10.0.10.6 (mysql-8.4.7 ndb-8.4.7, Nodegroup: 0, *)
id=2 @10.0.10.8 (mysql-8.4.7 ndb-8.4.7, Nodegroup: 0)
[ndb_mgmd(MGM)] 1 node(s)
id=3 @10.0.10.2 (mysql-8.4.7 ndb-8.4.7)
[mysqld(API)] 2 node(s)
id=4 @10.0.10.10 (mysql-8.4.7 ndb-8.4.7)
id=5 (not connected, accepting connect from any host)
```

**Compatibility with standard MySQL 8.4 releases.** While many standard MySQL schemas and applications can work using NDB Cluster, it is also true that unmodified applications and database schemas may be slightly incompatible or have suboptimal performance when run using NDB Cluster (see [Section 25.2.7, "Known Limitations of NDB Cluster"\)](#page-69-0). Most of these issues can be overcome, but this also means that you are very unlikely to be able to switch an existing application datastore that currently uses, for example, MyISAM or InnoDB—to use the [NDB](#page-50-0) storage engine without allowing for the possibility of changes in schemas, queries, and applications. A mysqld compiled without NDB support (that is, built without -DWITH\_NDB or -DWITH\_NDBCLUSTER\_STORAGE\_ENGINE) cannot function as a drop-in replacement for a mysqld that is built with it.

**NDB Cluster development source trees.** NDB Cluster development trees can also be accessed from [https://github.com/mysql/mysql-server.](https://github.com/mysql/mysql-server)

The NDB Cluster development sources maintained at <https://github.com/mysql/mysql-server>are licensed under the GPL. For information about obtaining MySQL sources using Git and building them yourself, see Section 2.8.5, "Installing MySQL Using a Development Source Tree".

![](_page_53_Picture_5.jpeg)

#### **Note**

As with MySQL Server 8.4, NDB Cluster 8.4 releases are built using CMake.

NDB Cluster 8.4 is available as an LTS release, and is recommended for new deployments. NDB Cluster 8.0 is the previous GA release series (see [MySQL NDB Cluster 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-cluster.md)), still supported in production. NDB Cluster 7.6 and 7.5 are earlier GA releases still supported in production, although we recommend NDB Cluster 8.4 for new deployments intended for use in production.

NDB Cluster 7.4 and 7.3 were previous GA releases which have been discontinued; they are no longer maintained or supported.

Additional information regarding NDB Cluster can be found on the MySQL website at [https://](https://www.mysql.com/products/cluster/) [www.mysql.com/products/cluster/](https://www.mysql.com/products/cluster/).

**Additional Resources.** More information about NDB Cluster can be found in the following places:

- For answers to some commonly asked questions about NDB Cluster, see Section A.10, "MySQL 8.4 FAQ: NDB Cluster".
- The NDB Cluster Forum: <https://forums.mysql.com/list.php?25>.
- Many NDB Cluster users and developers blog about their experiences with NDB Cluster, and make feeds of these available through [PlanetMySQL](http://www.planetmysql.org/).

# <span id="page-53-0"></span>**25.2 NDB Cluster Overview**

NDB Cluster is a technology that enables clustering of in-memory databases in a shared-nothing system. The shared-nothing architecture enables the system to work with very inexpensive hardware, and with a minimum of specific requirements for hardware or software.

NDB Cluster is designed not to have any single point of failure. In a shared-nothing system, each component is expected to have its own memory and disk, and the use of shared storage mechanisms such as network shares, network file systems, and SANs is not recommended or supported.

NDB Cluster integrates the standard MySQL server with an in-memory clustered storage engine called [NDB](#page-50-0) (which stands for "Network DataBase"). In our documentation, the term [NDB](#page-50-0) refers to the part of the setup that is specific to the storage engine, whereas "MySQL NDB Cluster" refers to the combination of one or more MySQL servers with the [NDB](#page-50-0) storage engine.

An NDB Cluster consists of a set of computers, known as hosts, each running one or more processes. These processes, known as nodes, may include MySQL servers (for access to NDB data), data nodes (for storage of the data), one or more management servers, and possibly other specialized data access programs. The relationship of these components in an NDB Cluster is shown here:

**Figure 25.1 NDB Cluster Components**

All these programs work together to form an NDB Cluster (see Section 25.5, "NDB Cluster Programs". When data is stored by the [NDB](#page-50-0) storage engine, the tables (and table data) are stored in the data nodes. Such tables are directly accessible from all other MySQL servers (SQL nodes) in the cluster. Thus, in a payroll application storing data in a cluster, if one application updates the salary of an employee, all other MySQL servers that query this data can see this change immediately.

An NDB Cluster 8.4 SQL node uses the mysqld server daemon, which is the same as the mysqld supplied with MySQL Server 8.4 distributions. You should keep in mind that an instance of mysqld, regardless of version, that is not connected to an NDB Cluster cannot use the [NDB](#page-50-0) storage engine and cannot access any NDB Cluster data.

The data stored in the data nodes for NDB Cluster can be mirrored; the cluster can handle failures of individual data nodes with no other impact than that a small number of transactions are aborted due to losing the transaction state. Because transactional applications are expected to handle transaction failure, this should not be a source of problems.

Individual nodes can be stopped and restarted, and can then rejoin the system (cluster). Rolling restarts (in which all nodes are restarted in turn) are used in making configuration changes and

software upgrades (see Section 25.6.5, "Performing a Rolling Restart of an NDB Cluster"). Rolling restarts are also used as part of the process of adding new data nodes online (see Section 25.6.7, "Adding NDB Cluster Data Nodes Online"). For more information about data nodes, how they are organized in an NDB Cluster, and how they handle and store NDB Cluster data, see [Section 25.2.2,](#page-58-0) ["NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions"](#page-58-0).

Backing up and restoring NDB Cluster databases can be done using the NDB-native functionality found in the NDB Cluster management client and the ndb\_restore program included in the NDB Cluster distribution. For more information, see Section 25.6.8, "Online Backup of NDB Cluster", and Section 25.5.23, "ndb\_restore — Restore an NDB Cluster Backup". You can also use the standard MySQL functionality provided for this purpose in mysqldump and the MySQL server. See Section 6.5.4, "mysqldump — A Database Backup Program", for more information.

NDB Cluster nodes can employ different transport mechanisms for inter-node communications; TCP/IP over standard 100 Mbps or faster Ethernet hardware is used in most real-world deployments.

# <span id="page-55-0"></span>**25.2.1 NDB Cluster Core Concepts**

[NDBCLUSTER](#page-50-0) (also known as [NDB](#page-50-0)) is an in-memory storage engine offering high-availability and datapersistence features.

The [NDBCLUSTER](#page-50-0) storage engine can be configured with a range of failover and load-balancing options, but it is easiest to start with the storage engine at the cluster level. NDB Cluster's [NDB](#page-50-0) storage engine contains a complete set of data, dependent only on other data within the cluster itself.

The "Cluster" portion of NDB Cluster is configured independently of the MySQL servers. In an NDB Cluster, each part of the cluster is considered to be a node.

![](_page_55_Picture_8.jpeg)

#### **Note**

In many contexts, the term "node" is used to indicate a computer, but when discussing NDB Cluster it means a process. It is possible to run multiple nodes on a single computer; for a computer on which one or more cluster nodes are being run we use the term cluster host.

There are three types of cluster nodes, and in a minimal NDB Cluster configuration, there are at least three nodes, one of each of these types:

- Management node: The role of this type of node is to manage the other nodes within the NDB Cluster, performing such functions as providing configuration data, starting and stopping nodes, and running backups. Because this node type manages the configuration of the other nodes, a node of this type should be started first, before any other node. A management node is started with the command ndb\_mgmd.
- Data node: This type of node stores cluster data. There are as many data nodes as there are fragment replicas, times the number of fragments (see [Section 25.2.2, "NDB Cluster Nodes, Node](#page-58-0) [Groups, Fragment Replicas, and Partitions"](#page-58-0)). For example, with two fragment replicas, each having two fragments, you need four data nodes. One fragment replica is sufficient for data storage, but provides no redundancy; therefore, it is recommended to have two (or more) fragment replicas to provide redundancy, and thus high availability. A data node is started with the command ndbd (see Section 25.5.1, "ndbd — The NDB Cluster Data Node Daemon") or ndbmtd (see Section 25.5.3, "ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)").

NDB Cluster tables are normally stored completely in memory rather than on disk (this is why we refer to NDB Cluster as an in-memory database). However, some NDB Cluster data can be stored on disk; see Section 25.6.11, "NDB Cluster Disk Data Tables", for more information.

• SQL node: This is a node that accesses the cluster data. In the case of NDB Cluster, an SQL node is a traditional MySQL server that uses the [NDBCLUSTER](#page-50-0) storage engine. An SQL node is a mysqld process started with the --ndbcluster and --ndb-connectstring options, which are explained elsewhere in this chapter, possibly with additional MySQL server options as well.

An SQL node is actually just a specialized type of API node, which designates any application which accesses NDB Cluster data. Another example of an API node is the ndb\_restore utility that is used to restore a cluster backup. It is possible to write such applications using the NDB API. For basic information about the NDB API, see [Getting Started with the NDB API.](https://dev.mysql.com/doc/ndbapi/en/ndb-getting-started.md)

![](_page_56_Picture_3.jpeg)

#### **Important**

It is not realistic to expect to employ a three-node setup in a production environment. Such a configuration provides no redundancy; to benefit from NDB Cluster's high-availability features, you must use multiple data and SQL nodes. The use of multiple management nodes is also highly recommended.

For a brief introduction to the relationships between nodes, node groups, fragment replicas, and partitions in NDB Cluster, see [Section 25.2.2, "NDB Cluster Nodes, Node Groups, Fragment Replicas,](#page-58-0) [and Partitions"](#page-58-0).

Configuration of a cluster involves configuring each individual node in the cluster and setting up individual communication links between nodes. NDB Cluster is currently designed with the intention that data nodes are homogeneous in terms of processor power, memory space, and bandwidth. In addition, to provide a single point of configuration, all configuration data for the cluster as a whole is located in one configuration file.

The management server manages the cluster configuration file and the cluster log. Each node in the cluster retrieves the configuration data from the management server, and so requires a way to determine where the management server resides. When interesting events occur in the data nodes, the nodes transfer information about these events to the management server, which then writes the information to the cluster log.

In addition, there can be any number of cluster client processes or applications. These include standard MySQL clients, NDB-specific API programs, and management clients. These are described in the next few paragraphs.

**Standard MySQL clients.** NDB Cluster can be used with existing MySQL applications written in PHP, Perl, C, C++, Java, Python, and so on. Such client applications send SQL statements to and receive responses from MySQL servers acting as NDB Cluster SQL nodes in much the same way that they interact with standalone MySQL servers.

MySQL clients using an NDB Cluster as a data source can be modified to take advantage of the ability to connect with multiple MySQL servers to achieve load balancing and failover. For example, Java clients using Connector/J 5.0.6 and later can use jdbc:mysql:loadbalance:// URLs (improved in Connector/J 5.1.7) to achieve load balancing transparently; for more information about using Connector/J with NDB Cluster, see [Using Connector/J with NDB Cluster](https://dev.mysql.com/doc/ndbapi/en/mccj-using-connectorj.md).

**NDB client programs.** Client programs can be written that access NDB Cluster data directly from the NDBCLUSTER storage engine, bypassing any MySQL Servers that may be connected to the cluster, using the NDB API, a high-level C++ API. Such applications may be useful for specialized purposes where an SQL interface to the data is not needed. For more information, see [The NDB API.](https://dev.mysql.com/doc/ndbapi/en/ndbapi.md)

NDB-specific Java applications can also be written for NDB Cluster using the NDB Cluster Connector for Java. This NDB Cluster Connector includes ClusterJ, a high-level database API similar to objectrelational mapping persistence frameworks such as Hibernate and JPA that connect directly to NDBCLUSTER, and so does not require access to a MySQL Server. See [Java and NDB Cluster](https://dev.mysql.com/doc/ndbapi/en/mccj-overview-java.md), and [The ClusterJ API and Data Object Model,](https://dev.mysql.com/doc/ndbapi/en/mccj-overview-clusterj-object-models.md) for more information.

NDB Cluster also supports applications written in JavaScript using Node.js. The MySQL Connector for JavaScript includes adapters for direct access to the NDB storage engine and as well as for the MySQL Server. Applications using this Connector are typically event-driven and use a domain object model similar in many ways to that employed by ClusterJ. For more information, see [MySQL NoSQL](https://dev.mysql.com/doc/ndbapi/en/ndb-nodejs.md) [Connector for JavaScript](https://dev.mysql.com/doc/ndbapi/en/ndb-nodejs.md).

**Management clients.** These clients connect to the management server and provide commands for starting and stopping nodes gracefully, starting and stopping message tracing (debug versions only), showing node versions and status, starting and stopping backups, and so on. An example of this type of program is the ndb\_mgm management client supplied with NDB Cluster (see Section 25.5.5, "ndb\_mgm — The NDB Cluster Management Client"). Such applications can be written using the MGM API, a C-language API that communicates directly with one or more NDB Cluster management servers. For more information, see [The MGM API.](https://dev.mysql.com/doc/ndbapi/en/mgm-api.md)

Oracle also makes available MySQL Cluster Manager, which provides an advanced command-line interface simplifying many complex NDB Cluster management tasks, such restarting an NDB Cluster with a large number of nodes. The MySQL Cluster Manager client also supports commands for getting and setting the values of most node configuration parameters as well as mysqld server options and variables relating to NDB Cluster. See [MySQL Cluster Manager 8.4.8 User Manual](https://dev.mysql.com/doc/mysql-cluster-manager/8.4/en/), for more information.

**Event logs.** NDB Cluster logs events by category (startup, shutdown, errors, checkpoints, and so on), priority, and severity. A complete listing of all reportable events may be found in Section 25.6.3, "Event Reports Generated in NDB Cluster". Event logs are of the two types listed here:

- Cluster log: Keeps a record of all desired reportable events for the cluster as a whole.
- Node log: A separate log which is also kept for each individual node.

![](_page_57_Picture_7.jpeg)

#### **Note**

Under normal circumstances, it is necessary and sufficient to keep and examine only the cluster log. The node logs need be consulted only for application development and debugging purposes.

**Checkpoint.** Generally speaking, when data is saved to disk, it is said that a checkpoint has been reached. More specific to NDB Cluster, a checkpoint is a point in time where all committed transactions are stored on disk. With regard to the [NDB](#page-50-0) storage engine, there are two types of checkpoints which work together to ensure that a consistent view of the cluster's data is maintained. These are shown in the following list:

• Local Checkpoint (LCP): This is a checkpoint that is specific to a single node; however, LCPs take place for all nodes in the cluster more or less concurrently. An LCP usually occurs every few minutes; the precise interval varies, and depends upon the amount of data stored by the node, the level of cluster activity, and other factors.

NDB 8.4 supports partial LCPs, which can significantly improve performance under some conditions. See the descriptions of the [EnablePartialLcp](#page-174-0) and [RecoveryWork](#page-177-0) configuration parameters which enable partial LCPs and control the amount of storage they use.

• Global Checkpoint (GCP): A GCP occurs every few seconds, when transactions for all nodes are synchronized and the redo-log is flushed to disk.

For more information about the files and directories created by local checkpoints and global checkpoints, see [NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md).

**Transporter.** We use the term transporter for the data transport mechanism employed between data nodes. MySQL NDB Cluster 8.4 supports three of these, which are listed here:

- TCP/IP over Ethernet. See Section 25.4.3.10, "NDB Cluster TCP/IP Connections".
- Direct TCP/IP. Uses machine-to-machine connections. See Section 25.4.3.11, "NDB Cluster TCP/IP Connections Using Direct Connections".

Although this transporter uses the same TCP/IP protocol as mentioned in the previous item, it requires setting up the hardware differently and is configured differently as well. For this reason, it is considered a separate transport mechanism for NDB Cluster.

• Shared memory (SHM). See Section 25.4.3.12, "NDB Cluster Shared-Memory Connections".

Because it is ubiquitous, most users employ TCP/IP over Ethernet for NDB Cluster.

Regardless of the transporter used, NDB attempts to make sure that communication between data node processes is performed using chunks that are as large as possible since this benefits all types of data transmission.

# <span id="page-58-0"></span>**25.2.2 NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions**

This section discusses the manner in which NDB Cluster divides and duplicates data for storage.

A number of concepts central to an understanding of this topic are discussed in the next few paragraphs.

**Data node.** An ndbd or ndbmtd process, which stores one or more fragment replicas—that is, copies of the partitions (discussed later in this section) assigned to the node group of which the node is a member.

Each data node should be located on a separate computer. While it is also possible to host multiple data node processes on a single computer, such a configuration is not usually recommended.

It is common for the terms "node" and "data node" to be used interchangeably when referring to an ndbd or ndbmtd process; where mentioned, management nodes (ndb\_mgmd processes) and SQL nodes (mysqld processes) are specified as such in this discussion.

**Node group.** A node group consists of one or more nodes, and stores partitions, or sets of fragment replicas (see next item).

The number of node groups in an NDB Cluster is not directly configurable; it is a function of the number of data nodes and of the number of fragment replicas ([NoOfReplicas](#page-153-0) configuration parameter), as shown here:

```
[# of node groups] = [# of data nodes] / NoOfReplicas
```

Thus, an NDB Cluster with 4 data nodes has 4 node groups if [NoOfReplicas](#page-153-0) is set to 1 in the config.ini file, 2 node groups if [NoOfReplicas](#page-153-0) is set to 2, and 1 node group if [NoOfReplicas](#page-153-0) is set to 4. Fragment replicas are discussed later in this section; for more information about [NoOfReplicas](#page-153-0), see [Section 25.4.3.6, "Defining NDB Cluster Data Nodes".](#page-149-0)

![](_page_58_Picture_15.jpeg)

#### **Note**

All node groups in an NDB Cluster must have the same number of data nodes.

You can add new node groups (and thus new data nodes) online, to a running NDB Cluster; see Section 25.6.7, "Adding NDB Cluster Data Nodes Online", for more information.

**Partition.** This is a portion of the data stored by the cluster. Each node is responsible for keeping at least one copy of any partitions assigned to it (that is, at least one fragment replica) available to the cluster.

The number of partitions used by default by NDB Cluster depends on the number of data nodes and the number of LDM threads in use by the data nodes, as shown here:

```
[# of partitions] = [# of data nodes] * [# of LDM threads]
```

When using data nodes running ndbmtd, the number of LDM threads is controlled by the setting for MaxNoOfExecutionThreads. When using ndbd there is a single LDM thread, which means that there are as many cluster partitions as nodes participating in the cluster. This is also the case when using ndbmtd with MaxNoOfExecutionThreads set to 3 or less. (You should be aware that the number of LDM threads increases with the value of this parameter, but not in a strictly linear fashion, and that there are additional constraints on setting it; see the description of MaxNoOfExecutionThreads for more information.)

**NDB and user-defined partitioning.** NDB Cluster normally partitions [NDBCLUSTER](#page-50-0) tables automatically. However, it is also possible to employ user-defined partitioning with [NDBCLUSTER](#page-50-0) tables. This is subject to the following limitations:

- 1. Only the KEY and LINEAR KEY partitioning schemes are supported in production with [NDB](#page-50-0) tables.
- 2. The maximum number of partitions that may be defined explicitly for any [NDB](#page-50-0) table is 8 \* [number of LDM threads] \* [number of node groups], the number of node groups in an NDB Cluster being determined as discussed previously in this section. When running ndbd for data node processes, setting the number of LDM threads has no effect (since ThreadConfig applies only to ndbmtd); in such cases, this value can be treated as though it were equal to 1 for purposes of performing this calculation.

See Section 25.5.3, "ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)", for more information.

For more information relating to NDB Cluster and user-defined partitioning, see [Section 25.2.7, "Known](#page-69-0) [Limitations of NDB Cluster",](#page-69-0) and Section 26.6.2, "Partitioning Limitations Relating to Storage Engines".

**Fragment replica.** This is a copy of a cluster partition. Each node in a node group stores a fragment replica. Also sometimes known as a partition replica. The number of fragment replicas is equal to the number of nodes per node group.

A fragment replica belongs entirely to a single node; a node can (and usually does) store several fragment replicas.

The following diagram illustrates an NDB Cluster with four data nodes running ndbd, arranged in two node groups of two nodes each; nodes 1 and 2 belong to node group 0, and nodes 3 and 4 belong to node group 1.

![](_page_59_Picture_11.jpeg)

#### **Note**

Only data nodes are shown here; although a working NDB Cluster requires an ndb\_mgmd process for cluster management and at least one SQL node to access the data stored by the cluster, these have been omitted from the figure for clarity.

**Figure 25.2 NDB Cluster with Two Node Groups**

![](_page_60_Figure_2.jpeg)

The data stored by the cluster is divided into four partitions, numbered 0, 1, 2, and 3. Each partition is stored—in multiple copies—on the same node group. Partitions are stored on alternate node groups as follows:

- Partition 0 is stored on node group 0; a primary fragment replica (primary copy) is stored on node 1, and a backup fragment replica (backup copy of the partition) is stored on node 2.
- Partition 1 is stored on the other node group (node group 1); this partition's primary fragment replica is on node 3, and its backup fragment replica is on node 4.
- Partition 2 is stored on node group 0. However, the placing of its two fragment replicas is reversed from that of Partition 0; for Partition 2, the primary fragment replica is stored on node 2, and the backup on node 1.
- Partition 3 is stored on node group 1, and the placement of its two fragment replicas are reversed from those of partition 1. That is, its primary fragment replica is located on node 4, with the backup on node 3.

What this means regarding the continued operation of an NDB Cluster is this: so long as each node group participating in the cluster has at least one node operating, the cluster has a complete copy of all data and remains viable. This is illustrated in the next diagram.

**Figure 25.3 Nodes Required for a 2x2 NDB Cluster**

In this example, the cluster consists of two node groups each consisting of two data nodes. Each data node is running an instance of ndbd. Any combination of at least one node from node group 0 and at least one node from node group 1 is sufficient to keep the cluster "alive". However, if both nodes from a single node group fail, the combination consisting of the remaining two nodes in the other node group is not sufficient. In this situation, the cluster has lost an entire partition and so can no longer provide access to a complete set of all NDB Cluster data.

The maximum number of node groups supported for a single NDB Cluster instance is 48.

# <span id="page-61-0"></span>**25.2.3 NDB Cluster Hardware, Software, and Networking Requirements**

One of the strengths of NDB Cluster is that it can be run on commodity hardware and has no unusual requirements in this regard, other than for large amounts of RAM, due to the fact that all live data storage is done in memory. (It is possible to reduce this requirement using Disk Data tables—see Section 25.6.11, "NDB Cluster Disk Data Tables", for more information about these.) You can obtain information about memory usage by data nodes by viewing the ndbinfo.memoryusage table, or the output of the REPORT MemoryUsage command in the ndb\_mgm client. For information about memory used by NDB tables, you can query the ndbinfo.memory\_per\_fragment table.

Increasing the number of CPUs, using faster CPUs, or both, on the computers hosting data nodes can generally be expected to enhance the performance of NDB Cluster. Memory requirements for cluster processes other than the data nodes are relatively small.

The software requirements for NDB Cluster are also modest. Host operating systems do not require any unusual modules, services, applications, or configuration to support NDB Cluster. For supported operating systems, a standard installation should be sufficient. The MySQL software requirements are simple: all that is needed is a production release of NDB Cluster. It is not strictly necessary to compile MySQL yourself merely to be able to use NDB Cluster. We assume that you are using the binaries appropriate to your platform, available from the NDB Cluster software downloads page at [https://](https://dev.mysql.com/downloads/cluster/) [dev.mysql.com/downloads/cluster/](https://dev.mysql.com/downloads/cluster/).

For communication between nodes, NDB Cluster supports TCP/IP networking in any standard topology, and the minimum expected for each host is a standard 100 Mbps Ethernet card, plus a switch, hub, or router to provide network connectivity for the cluster as a whole.

We strongly recommend that an NDB Cluster be run on its own subnet which is not shared with machines not forming part of the cluster; using a private or protected network allows the cluster to make exclusive use of bandwidth between cluster hosts. Using a separate switch for your NDB Cluster installation not only helps protect against unauthorized access to data stored in the cluster, but also ensures that cluster nodes are shielded from interference caused by transmissions between other computers on the network. For enhanced reliability, you can use dual switches and dual cards to remove the network as a single point of failure; many device drivers support failover for such communication links.

NDB supports encrypted live and backup files and file systems, as discussed in Section 25.6.19.4, "File System Encryption for NDB Cluster". Section 25.6.19.5, "TLS Link Encryption for NDB Cluster", provides information about enabling support for encrypted connections between nodes. Encrypted backups can be read by many NDB command-line programs including ndb\_restore, ndbxfrm, ndb\_print\_backup\_file, and ndb\_mgm. See Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup", for more information about creating encypted backups.

NDB Cluster also supports encrypted network connections between nodes; see Section 25.6.19.4, "File System Encryption for NDB Cluster", for details.

<span id="page-62-1"></span>**Network communication and latency.** NDB Cluster requires communication between data nodes and API nodes (including SQL nodes), as well as between data nodes and other data nodes, to execute queries and updates. Communication latency between these processes can directly affect the observed performance and latency of user queries. In addition, to maintain consistency and service despite the silent failure of nodes, NDB Cluster uses heartbeating and timeout mechanisms which treat an extended loss of communication from a node as node failure. This can lead to reduced redundancy. Recall that, to maintain data consistency, an NDB Cluster shuts down when the last node in a node group fails. Thus, to avoid increasing the risk of a forced shutdown, breaks in communication between nodes should be avoided wherever possible.

The failure of a data or API node results in the abort of all uncommitted transactions involving the failed node. Data node recovery requires synchronization of the failed node's data from a surviving data node, and re-establishment of disk-based redo and checkpoint logs, before the data node returns to service. This recovery can take some time, during which the Cluster operates with reduced redundancy.

Heartbeating relies on timely generation of heartbeat signals by all nodes. This may not be possible if the node is overloaded, has insufficient machine CPU due to sharing with other programs, or is experiencing delays due to swapping. If heartbeat generation is sufficiently delayed, other nodes treat the node that is slow to respond as failed.

This treatment of a slow node as a failed one may or may not be desirable in some circumstances, depending on the impact of the node's slowed operation on the rest of the cluster. When setting timeout values such as [HeartbeatIntervalDbDb](#page-192-0) and [HeartbeatIntervalDbApi](#page-193-0) for NDB Cluster, care must be taken care to achieve quick detection, failover, and return to service, while avoiding potentially expensive false positives.

Where communication latencies between data nodes are expected to be higher than would be expected in a LAN environment (on the order of 100 µs), timeout parameters must be increased to ensure that any allowed periods of latency periods are well within configured timeouts. Increasing timeouts in this way has a corresponding effect on the worst-case time to detect failure and therefore time to service recovery.

LAN environments can typically be configured with stable low latency, and such that they can provide redundancy with fast failover. Individual link failures can be recovered from with minimal and controlled latency visible at the TCP level (where NDB Cluster normally operates). WAN environments may offer a range of latencies, as well as redundancy with slower failover times. Individual link failures may require route changes to propagate before end-to-end connectivity is restored. At the TCP level this can appear as large latencies on individual channels. The worst-case observed TCP latency in these scenarios is related to the worst-case time for the IP layer to reroute around the failures.

# <span id="page-62-0"></span>**25.2.4 What is New in MySQL NDB Cluster 8.4**

- [What is New in NDB Cluster 8.4](#page-63-0)
- [Changes in NDB 8.x Innovation Releases](#page-64-0)

The following sections describe changes in the implementation of MySQL NDB Cluster in NDB Cluster 8.0 through 8.0.44, as compared to earlier release series.

NDB Cluster 8.4 is also available for production; while NDB 8.0 is still supported, we suggest that you use NDB 8.4 for new deployments; for more information, see Chapter 25, [MySQL NDB Cluster 8.4](#page-50-0). NDB Cluster 9.4 is available as an Innovation release for new features currently under development; see [What is New in NDB Cluster 9.4.](https://dev.mysql.com/doc/refman/9.4/en/mysql-cluster-what-is-new.md#mysql-cluster-what-is-new-9-4)

NDB Cluster 7.6 (see [What is New in NDB Cluster 7.6\)](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-what-is-new-7-6.md) is a previous GA release which is still supported in production, although we recommend that new deployments for production use MySQL NDB Cluster 8.4. NDB Cluster 7.5, 7.4, and 7.3 were previous GA releases which have reached their end of life, and are no longer supported or maintained. We recommend that new deployments for production use MySQL NDB Cluster 8.4.

# <span id="page-63-0"></span>**What is New in NDB Cluster 8.4**

Major changes and new features in NDB Cluster 8.4 which are likely to be of interest are listed here:

• **ndbinfo transporter\_details table.** The transporter\_details table provides information about individual transporters used in an NDB cluster. It is otherwise similar to the ndbinfo transporters table, which provides such information in aggregate form.

NDB 8.4.0 provides additional columns as compared to the version introduced in NDB 8.0. These new columns, along with brief dscriptions of each, are listed here:

- sendbuffer\_used\_bytes: Number of bytes of signal data currently stored pending send using this transporter.
- sendbuffer\_max\_used\_bytes: Historical maximum number of bytes of signal data stored pending send using this transporter. Reset when the transporter connects.
- sendbuffer\_alloc\_bytes: Number of bytes of send buffer currently allocated to store pending send bytes for this transporter. Send buffer memory is allocated in large blocks which may be sparsely used.
- sendbuffer\_max\_alloc\_bytes: Historical maximum number of bytes of send buffer allocated to store pending send bytes for this transporter.

NDB 8.4.1 adds a type column, which displays the transport's connection type (TCP or SHM).

See Section 25.6.15.65, "The ndbinfo transporter\_details Table", for more information.

• **NDB Replication: Filtering of unused updates.** Previously, when SQL nodes performing binary logging used log\_replica\_updates=OFF, any replicated updates which were applied on a replica NDB cluster were sent on to the SQL nodes performing binary logging. These updates were not actually applied or used for any other purpose; this entailed unnecessary network traffic and consumption of resources.

In NDB 8.4.0 and later, updates applied on the replica SQL node are filtered out on this node, and are no longer sent onward to any other SQL nodes. Updates that do not trigger any logging are also no longer sent by the replica.

- **Per-session binary log transaction cache sizing.** NDB 8.4.3 adds the ndb\_log\_cache\_size server system variable, which makes it possible to set the size of the transaction cache used for writing the binary log. This enables use of a large cache for logging NDB transactions, and (using binlog\_cache\_size) a smaller cache for logging other transactions, thus making more efficient use of resources.
- **Ndb.cfg file deprecation.** Use of an Ndb.cfg file for setting the connection string for an NDB process was not well documented or supported. As of NDB 8.4.3, use of this file is now formally deprecated; you should expect support for it to be removed in a future release of MySQL Cluster.

• **Microsecond node log timestamps.** Node log timestamps in [NDB](#page-50-0) 8.4.6 and later can be printed with microsecond resolution. Data nodes can enable this feature using the data node --ndb-logtimestamps=UTC option; management nodes can do this using the ndb\_mgmd option --ndblog-timestamps=UTC. For backwards compatible behavior, the default is LEGACY, which uses the system time zone and resolution in seconds, as in previous releases.

SQL nodes can use the roughly equivalent option --log-timestamps; you should be aware that this mysqld option does not accept LEGACY as a value.

For more information about NDB Cluster node logs, see Section 25.6.2, "NDB Cluster Log Messages".

MySQL Cluster Manager has an advanced command-line interface that can simplify many complex NDB Cluster management tasks. See [MySQL Cluster Manager 8.4.8 User Manual](https://dev.mysql.com/doc/mysql-cluster-manager/8.4/en/), for more information.

# <span id="page-64-0"></span>**Changes in NDB 8.x Innovation Releases**

New features and major changes in NDB Cluster Innovation releases (8.1, 8.2, 8.3) compared with NDB 8.0 which are likely to be of interest are listed here:

• **TLS for cluster node communications.** NDB Cluster 8.3 and later provides support for network communications secured by Transport Layer Security (TLS) and Internet Public Key Infrastructure (PKI) to authenticate and encrypt connections between NDB nodes, and between the NDB management server and its clients; TLS is applied to the NDB Transporter Protocol, and to the NDB Management Protocol.

This feature uses TLS mutual authentication, in which a node's own certificate file contains the chain of trust which the node uses to validate the certificates of its peers. When TLS is enabled on the cluster, data and management nodes use TLS to perform the following tasks:

- Mutually authenticate NDB clients and servers at the network level, preventing unprivileged access as a client or server
- Encrypt data transfer, avoiding data eavesdropping, modification, and man-in-the-middle attacks

Connections that use the MySQL client protocol employ MySQL user authentication, and may use TLS (including optional mutual TLS) as described elsewhere in this Manual; see Section 8.3, "Using Encrypted Connections", for more information.

NDB implements a new tool ndb\_sign\_keys which can be used to create and manage CA, certificate files, and keys. You can generate a set of keys and certificates for all nodes in a cluster with a given configuration file using ndb\_sign\_keys --create-key.

Using ndb\_sign\_keys, a node certificate can be bound to a particular hostname, made to expire on a given date, and be associated with a given node type, so that clients are distinct from servers, and management servers from data nodes. (Every NDB TLS certificate can be used for MGM client connections.) Private keys are created in place, so that copying of files containing private keys is minimized. Both private keys and certificates are labeled as either active or pending; ndb\_sign\_keys also provides help with rotating keys to allow for pending keys to replace active keys before the active keys expire.

Testing of node TLS connections can be done from the system shell using ndb\_mgm client with - test-tls, or within the ndb\_mgm client using the TLS INFO command. You can obtain information about certificates used by cluster nodes by checking the ndbinfo certificates table.

To enforce a requirement for TLS, set the client option ndb-mgm-tls=strict in my.cnf on each cluster host, then set [RequireTls=true](#page-148-0) in the [mgm default] section of the cluster config.ini file, and set [RequireTls=true](#page-188-0) in the [ndbd default] section of the configuration file as well. Then perform a rolling restart of the cluster, restarting the management server with - reload --config-file.

Use of TLS connections is also supported in NDB Cluster API applications in NDB 8.3 and later. For information about MGM API support, see [TLS Functions.](https://dev.mysql.com/doc/ndbapi/en/mgm-functions-tls.md) The NDB API [Ndb\\_cluster\\_connection](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md) class adds [configure\\_tls\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-configure-tls) [get\\_tls\\_certificate\\_path\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-get-tls-certificate-path) methods for setting up TLS connections by clients.

For more information, see Section 25.6.19.5, "TLS Link Encryption for NDB Cluster", as well as Section 25.5.28, "ndb\_sign\_keys — Create, Sign, and Manage TLS Keys and Certificates for NDB Cluster".

- **Binary log injector memory allocation.** In previous versions of NDB Cluster, when the NDB binary log injector was engaged in handling schema changes and tracking the state of the binary log, the choice of arena for allocation of memory for these purposes was forced by changing thread local pointers, thus attempting to try and catch all allocations performed during epoch processing. At the end of the epoch, those pointers were reset, arena memory was released, and the arena structures discarded; this released the memory, but also required setting it up again for the next epoch. The thread local pointer changes also introduced the risk of memory being allocated wrongly when activating functionality in different subsystems. MySQL NDB Cluster 8.3 makes the following improvements to this functionality:
  - Changes to thread local pointers are removed, and replaced by explicit arguments to provide the arena used for allocation during the epoch.
  - Re-use of the arena for next epoch, thus avoiding the need to set it up repeatedly.

These changes are internal only but should provide a noticeable improvememnt by saving on memory release and re-allocation over successive epochs.

• **NDB API primary key updates.** Previously, when using any other mechanism than [NdbRecord](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbrecord.md) in an attempt to update a primary key value, the NDB API returned error 4202 Set value on tuple key attribute is not allowed, even setting a value identical to the existing one. In NDB 8.1 and later, checking when performing updates by other means is handed off to the data nodes, as it was already when using NdbRecord to perform the update.

This means that you can now perform primary key updates using [NdbOperation::setValue\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndboperation.md#ndb-ndboperation-setvalue), [NdbInterpretedCode::write\\_attr\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbinterpretedcode.md#ndb-ndbinterpretedcode-write-attr), and other methods of [NdbOperation](https://dev.mysql.com/doc/ndbapi/en/ndb-ndboperation.md) and [NdbInterpretedCode](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbinterpretedcode.md) which set column values (including the NdbOperation methods [incValue\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndboperation.md#ndb-ndboperation-incvalue), [subValue\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndboperation.md#ndb-ndboperation-subvalue), the NdbInterpretedCode methods [add\\_val\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbinterpretedcode.md#ndb-ndbinterpretedcode-add-val), [sub\\_val\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbinterpretedcode.md#ndb-ndbinterpretedcode-sub-val), and so on). This also applies to the [NdbOperation](https://dev.mysql.com/doc/ndbapi/en/ndb-ndboperation.md) interface's OperationOptions::OO\_SETVALUE extension.

- **Improved warnings.** Made the following improvements in warning output:
  - The maximum time allowed without any progress is now also printed in addition to local checkpoint (LCP) elapsed time.
  - When an LCP reaches WAIT\_END\_LCP state, table IDs and fragment IDs are undefined and so no longer relevant; for this reason, we no longer attempt to print them at that point.
  - Removed duplicated information printed when the maximum limit was reached (the same information was shown as both warning and crash information).

In addition, we no longer print the message Validating excluded objects to the SQL node's error log every ndb\_metadata\_check\_interval (default 60) seconds when log\_error\_verbosity is greater than or equal to 3 (INFO level), due ot the fact that such messages tended to flood the error log, making it difficult to examine, and using excess disk space, while not providing any additional benefit to the user.

- Pushdown joins between queries featuring very large and possibly overlapping IN() and NOT IN() lists are now handled in a correct and safe manner.
- ndbcluster plugin log messages now use SYSTEM as the log level and NDB as the subsystem for logging. This means that informational messages from the ndbcluster plugin are always printed; their verbosity can be controlled by using --ndb\_extra\_logging.

# <span id="page-66-0"></span>**25.2.5 Options, Variables, and Parameters Added, Deprecated or Removed in NDB 8.4**

- [Parameters Introduced in NDB 8.4](#page-66-1)
- [Parameters Deprecated in NDB 8.4](#page-66-2)
- [Parameters Removed in NDB 8.4](#page-66-3)
- [Options and Variables Introduced in NDB 8.4](#page-66-4)
- [Options and Variables Deprecated in NDB 8.4](#page-67-1)
- [Options and Variables Removed in NDB 8.4](#page-67-2)

The next few sections contain information about NDB node configuration parameters and NDB-specific mysqld options and variables that have been added to, deprecated in, or removed from NDB 8.4 since NDB 8.0.

# <span id="page-66-1"></span>**Parameters Introduced in NDB 8.4**

The following node configuration parameters have been added in NDB 8.4.

- ApiFailureHandlingTimeout: Maximum time for API node failure handling before escalating. 0 means no time limit; minimum usable value is 10. Added in NDB 8.4.5.
- [RequireCertificate](#page-188-1): Node is required to find key and certificate in TLS search path. Added in NDB 8.3.0.
- RequireLinkTls: Read-only; is set to true if either endpoint of this connection requires TLS. Added in NDB 8.3.0.
- [RequireTls](#page-148-0): Client connection must authenticate with TLS before being used otherwise. Added in NDB 8.3.0.
- [RequireTls](#page-188-0): Require TLS-authenticated secure connections. Added in NDB 8.3.0.

# <span id="page-66-2"></span>**Parameters Deprecated in NDB 8.4**

No node configuration parameters have been deprecated in NDB 8.4.

# <span id="page-66-3"></span>**Parameters Removed in NDB 8.4**

No node configuration parameters have been removed in NDB 8.4.

# <span id="page-66-4"></span>**Options and Variables Introduced in NDB 8.4**

The following system variables, status variables, and server options have been added in NDB 8.4.

- Ndb\_schema\_participant\_count: Number of MySQL servers participating in NDB schema change distribution. Added in NDB 8.4.5.
- ndb-mgm-tls: Whether TLS connection requirements are strict or relaxed. Added in NDB 8.3.0 ndb-8.3.0.
- ndb-tls-search-path: Directories to search for NDB TLS CAs and private keys. Added in NDB 8.3.0-ndb-8.3.0.

• ndb\_log\_cache\_size: Set size of transaction cache used for recording NDB binary log. Added in NDB 8.4.3-ndb-8.4.3.

# <span id="page-67-1"></span>**Options and Variables Deprecated in NDB 8.4**

No system variables, status variables, or server options have been deprecated in NDB 8.4.

# <span id="page-67-2"></span>**Options and Variables Removed in NDB 8.4**

No system variables, status variables, or options have been removed in NDB 8.4.

# <span id="page-67-0"></span>**25.2.6 MySQL Server Using InnoDB Compared with NDB Cluster**

MySQL Server offers a number of choices in storage engines. Since both [NDB](#page-50-0) and InnoDB can serve as transactional MySQL storage engines, users of MySQL Server sometimes become interested in NDB Cluster. They see [NDB](#page-50-0) as a possible alternative or upgrade to the default InnoDB storage engine in MySQL. While [NDB](#page-50-0) and InnoDB share common characteristics, there are differences in architecture and implementation, so that some existing MySQL Server applications and usage scenarios can be a good fit for NDB Cluster, but not all of them.

In this section, we discuss and compare some characteristics of the [NDB](#page-50-0) storage engine used by NDB 8.4 with InnoDB used in MySQL 8.4. The next few sections provide a technical comparison. In many instances, decisions about when and where to use NDB Cluster must be made on a case-by-case basis, taking all factors into consideration. While it is beyond the scope of this documentation to provide specifics for every conceivable usage scenario, we also attempt to offer some very general guidance on the relative suitability of some common types of applications for [NDB](#page-50-0) as opposed to InnoDB back ends.

NDB Cluster 8.4 uses a mysqld based on MySQL 8.4, including support for InnoDB 1.1. While it is possible to use InnoDB tables with NDB Cluster, such tables are not clustered. It is also not possible to use programs or libraries from an NDB Cluster 8.4 distribution with MySQL Server 8.4, or the reverse.

While it is also true that some types of common business applications can be run either on NDB Cluster or on MySQL Server (most likely using the InnoDB storage engine), there are some important architectural and implementation differences. [Section 25.2.6.1, "Differences Between the NDB and](#page-67-3) [InnoDB Storage Engines"](#page-67-3), provides a summary of the these differences. Due to the differences, some usage scenarios are clearly more suitable for one engine or the other; see [Section 25.2.6.2, "NDB](#page-68-0) [and InnoDB Workloads"](#page-68-0). This in turn has an impact on the types of applications that better suited for use with [NDB](#page-50-0) or InnoDB. See [Section 25.2.6.3, "NDB and InnoDB Feature Usage Summary",](#page-69-1) for a comparison of the relative suitability of each for use in common types of database applications.

For information about the relative characteristics of the [NDB](#page-50-0) and MEMORY storage engines, see When to Use MEMORY or NDB Cluster.

See Chapter 18, Alternative Storage Engines, for additional information about MySQL storage engines.

# <span id="page-67-3"></span>**25.2.6.1 Differences Between the NDB and InnoDB Storage Engines**

The [NDB](#page-50-0) storage engine is implemented using a distributed, shared-nothing architecture, which causes it to behave differently from InnoDB in a number of ways. For those unaccustomed to working with [NDB](#page-50-0), unexpected behaviors can arise due to its distributed nature with regard to transactions, foreign keys, table limits, and other characteristics. These are shown in the following table:

**Table 25.1 Differences between InnoDB and NDB storage engines**

| Feature              | InnoDB (MySQL 8.4) | NDB 8.4         |
|----------------------|--------------------|-----------------|
| MySQL Server Version | 8.4                | 8.4             |
| InnoDB Version       | InnoDB 8.4.8       | InnoDB 8.4.8    |
| NDB Cluster Version  | N/A                | NDB 8.4.7/8.4.7 |

| Feature                                                 | InnoDB (MySQL 8.4)                                                                                     | NDB 8.4                                                                                                                                                                                          |
|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Storage Limits                                          | 64TB                                                                                                   | 128TB                                                                                                                                                                                            |
| Foreign Keys                                            | Yes                                                                                                    | Yes                                                                                                                                                                                              |
| Transactions                                            | All standard types                                                                                     | READ COMMITTED                                                                                                                                                                                   |
| MVCC                                                    | Yes                                                                                                    | No                                                                                                                                                                                               |
| Data Compression                                        | Yes                                                                                                    | No (NDB checkpoint and backup<br>files can be compressed)                                                                                                                                        |
| Large Row Support (> 14K)                               | Supported for VARBINARY,<br>VARCHAR, BLOB, and TEXT<br>columns                                         | Supported for BLOB and<br>TEXT columns only (Using<br>these types to store very large<br>amounts of data can lower NDB<br>performance)                                                           |
| Replication Support                                     | Asynchronous and<br>semisynchronous replication<br>using MySQL Replication;<br>MySQL Group Replication | Automatic synchronous<br>replication within an NDB<br>Cluster; asynchronous replication<br>between NDB Clusters,<br>using MySQL Replication<br>(Semisynchronous replication is<br>not supported) |
| Scaleout for Read Operations                            | Yes (MySQL Replication)                                                                                | Yes (Automatic partitioning<br>in NDB Cluster; NDB Cluster<br>Replication)                                                                                                                       |
| Scaleout for Write Operations                           | Requires application-level<br>partitioning (sharding)                                                  | Yes (Automatic partitioning in<br>NDB Cluster is transparent to<br>applications)                                                                                                                 |
| High Availability (HA)                                  | Built-in, from InnoDB cluster                                                                          | Yes (Designed for 99.999%<br>uptime)                                                                                                                                                             |
| Node Failure Recovery and<br>Failover                   | From MySQL Group Replication                                                                           | Automatic (Key element in NDB<br>architecture)                                                                                                                                                   |
| Time for Node Failure Recovery                          | 30 seconds or longer                                                                                   | Typically < 1 second                                                                                                                                                                             |
| Real-Time Performance                                   | No                                                                                                     | Yes                                                                                                                                                                                              |
| In-Memory Tables                                        | No                                                                                                     | Yes (Some data can optionally<br>be stored on disk; both in<br>memory and disk data storage<br>are durable)                                                                                      |
| NoSQL Access to Storage<br>Engine                       | Yes                                                                                                    | Yes (Multiple APIs, including<br>Memcached, Node.js/JavaScript,<br>Java, JPA, C++, and HTTP/<br>REST)                                                                                            |
| Concurrent and Parallel Writes                          | Yes                                                                                                    | Up to 48 writers, optimized for<br>concurrent writes                                                                                                                                             |
| Conflict Detection and Resolution<br>(Multiple Sources) | Yes (MySQL Group Replication)                                                                          | Yes                                                                                                                                                                                              |
| Hash Indexes                                            | No                                                                                                     | Yes                                                                                                                                                                                              |
| Online Addition of Nodes                                | Read/write replicas using MySQL<br>Group Replication                                                   | Yes (all node types)                                                                                                                                                                             |
| Online Upgrades                                         | Yes (using replication)                                                                                | Yes                                                                                                                                                                                              |
| Online Schema Modifications                             | Yes, as part of MySQL 8.4                                                                              | Yes                                                                                                                                                                                              |

# <span id="page-68-0"></span>**25.2.6.2 NDB and InnoDB Workloads**

NDB Cluster has a range of unique attributes that make it ideal to serve applications requiring high availability, fast failover, high throughput, and low latency. Due to its distributed architecture and multinode implementation, NDB Cluster also has specific constraints that may keep some workloads from performing well. A number of major differences in behavior between the [NDB](#page-50-0) and InnoDB storage engines with regard to some common types of database-driven application workloads are shown in the following table::

**Table 25.2 Differences between InnoDB and NDB storage engines, common types of data-driven application workloads.**

| Workload                                            | InnoDB | NDB Cluster (NDB)                                                                          |
|-----------------------------------------------------|--------|--------------------------------------------------------------------------------------------|
| High-Volume OLTP Applications                       | Yes    | Yes                                                                                        |
| DSS Applications (data marts,<br>analytics)         | Yes    | Limited (Join operations across<br>OLTP datasets not exceeding<br>3TB in size)             |
| Custom Applications                                 | Yes    | Yes                                                                                        |
| Packaged Applications                               | Yes    | Limited (should be mostly<br>primary key access); NDB<br>Cluster 8.4 supports foreign keys |
| In-Network Telecoms<br>Applications (HLR, HSS, SDP) | No     | Yes                                                                                        |
| Session Management and<br>Caching                   | Yes    | Yes                                                                                        |
| E-Commerce Applications                             | Yes    | Yes                                                                                        |
| User Profile Management, AAA<br>Protocol            | Yes    | Yes                                                                                        |

# <span id="page-69-1"></span>**25.2.6.3 NDB and InnoDB Feature Usage Summary**

When comparing application feature requirements to the capabilities of InnoDB with [NDB](#page-50-0), some are clearly more compatible with one storage engine than the other.

The following table lists supported application features according to the storage engine to which each feature is typically better suited.

**Table 25.3 Supported application features according to the storage engine to which each feature is typically better suited**

|                       | Preferred application requirements for InnoDB | Preferred application requirements for NDB                                                                     |
|-----------------------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| •<br>Foreign keys     |                                               | •<br>Write scaling                                                                                             |
|                       | Note                                          | •<br>99.999% uptime                                                                                            |
|                       | NDB Cluster 8.4<br>supports foreign keys      | •<br>Online addition of nodes and online schema<br>operations                                                  |
| •<br>Full table scans |                                               | •<br>Multiple SQL and NoSQL APIs (see NDB<br>Cluster APIs: Overview and Concepts)                              |
| •                     | Very large databases, rows, or transactions   | •<br>Real-time performance                                                                                     |
| •                     | Transactions other than READ COMMITTED        | •<br>Limited use of BLOB columns                                                                               |
|                       |                                               | •<br>Foreign keys are supported, although their use<br>may have an impact on performance at high<br>throughput |

# <span id="page-69-0"></span>**25.2.7 Known Limitations of NDB Cluster**

In the sections that follow, we discuss known limitations in current releases of NDB Cluster as compared with the features available when using the MyISAM and InnoDB storage engines. If you check the "Cluster" category in the MySQL bugs database at [http://bugs.mysql.com,](http://bugs.mysql.com) you can find known bugs in the following categories under "MySQL Server:" in the MySQL bugs database at [http://](http://bugs.mysql.com) [bugs.mysql.com](http://bugs.mysql.com), which we intend to correct in upcoming releases of NDB Cluster:

- NDB Cluster
- Cluster Direct API (NDBAPI)
- Cluster Disk Data
- Cluster Replication
- ClusterJ

This information is intended to be complete with respect to the conditions just set forth. You can report any discrepancies that you encounter to the MySQL bugs database using the instructions given in Section 1.6, "How to Report Bugs or Problems". Any problem which we do not plan to fix in NDB Cluster 8.4, is added to the list.

![](_page_70_Picture_8.jpeg)

#### **Note**

Limitations and other issues specific to NDB Cluster Replication are described in Section 25.7.3, "Known Issues in NDB Cluster Replication".