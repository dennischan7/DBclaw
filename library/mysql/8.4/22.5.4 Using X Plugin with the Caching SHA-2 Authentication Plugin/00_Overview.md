---
source: MySQL 8.4 Reference
title: 00_Overview
---

X Plugin supports MySQL user accounts created with the caching\_sha2\_password authentication plugin. For more information on this plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication". You can use X Plugin to authenticate against such accounts using non-SSL connections with SHA256\_MEMORY authentication and SSL connections with PLAIN authentication.

Although the caching\_sha2\_password authentication plugin holds an authentication cache, this cache is not shared with X Plugin, so X Plugin uses its own authentication cache for SHA256\_MEMORY authentication. The X Plugin authentication cache stores hashes of user account passwords, and cannot be accessed using SQL. If a user account is modified or removed, the relevant entries are removed from the cache. The X Plugin authentication cache is maintained by the mysqlx\_cache\_cleaner plugin, which is enabled by default, and has no related system variables or status variables.

Before you can use non-SSL X Protocol connections to authenticate an account that uses the caching\_sha2\_password authentication plugin, the account must have authenticated at least once over an X Protocol connection with SSL, to supply the password to the X Plugin authentication cache. Once this initial authentication over SSL has succeeded, non-SSL X Protocol connections can be used.

It is possible to disable the mysqlx\_cache\_cleaner plugin by starting the MySQL server with the option --mysqlx\_cache\_cleaner=0. If you do this, the X Plugin authentication cache is disabled, and therefore SSL must always be used for X Protocol connections when authenticating with SHA256\_MEMORY authentication.

# <span id="page-20-2"></span>**22.5.5 Connection Compression with X Plugin**

X Plugin supports compression of messages sent over X Protocol connections. Connections can be compressed if the server and the client agree on a mutually supported compression algorithm. Enabling compression reduces the number of bytes sent over the network, but adds to the server and client an additional CPU cost for compression and decompression operations. The benefits of compression therefore occur primarily when there is low network bandwidth, network transfer time dominates the cost of compression and decompression operations, and result sets are large.

![](_page_20_Picture_5.jpeg)

#### **Note**

Different MySQL clients implement support for connection compression differently; consult your client documentation for details. For example, for classic MySQL protocol connections, see Section 6.2.8, "Connection Compression Control".

- [Configuring Connection Compression for X Plugin](#page-20-0)
- [Compressed Connection Characteristics for X Plugin](#page-22-0)
- [Monitoring Connection Compression for X Plugin](#page-23-0)

# <span id="page-20-0"></span>**Configuring Connection Compression for X Plugin**

By default, X Plugin supports the zstd, LZ4, and Deflate compression algorithms. Compression with the Deflate algorithm is carried out using the zlib software library, so the deflate\_stream compression algorithm setting for X Protocol connections is equivalent to the zlib setting for classic MySQL protocol connections.

On the server side, you can disallow any of the compression algorithms by setting the [mysqlx\\_compression\\_algorithms](#page-28-0) system variable to include only those permitted. The algorithm names zstd\_stream, lz4\_message, and deflate\_stream can be specified in any combination, and the order and lettercase are not important. If the system variable value is the empty string, no compression algorithms are permitted and connections are uncompressed.

The following table compares the characteristics of the different compression algorithms and shows their assigned priorities. By default, the server chooses the highest-priority algorithm permitted in common by the server and the client; clients may change the priorities as described later. The short form alias for the algorithms can be used by clients when specifying them.

**Table 22.1 X Protocol Compression Algorithm Characteristics**

<span id="page-20-1"></span>

| Algorithm             | Alias | Compression<br>Ratio | Throughput | CPU Cost | Default Priority |
|-----------------------|-------|----------------------|------------|----------|------------------|
| zsth_stream           | zstd  | High                 | High       | Medium   | First            |
| lz4_message           | lz4   | Low                  | High       | Lowest   | Second           |
| deflate_streamdeflate |       | High                 | Low        | Highest  | Third            |

The X Protocol set of permitted compression algorithms (whether user-specified or default) is independent of the set of compression algorithms permitted by MySQL Server for classic MySQL protocol connections, which is specified by the protocol\_compression\_algorithms server system variable. If you do not specify the [mysqlx\\_compression\\_algorithms](#page-28-0) system variable, X Plugin does not fall back to using compression settings for classic MySQL protocol connections. Instead, its default is to permit all algorithms shown in [Table 22.1, "X Protocol Compression](#page-20-1) [Algorithm Characteristics"](#page-20-1). This is unlike the situation for the TLS context, where MySQL Server settings are used if the X Plugin system variables are not set, as described in [Section 22.5.3, "Using](#page-18-0) [Encrypted Connections with X Plugin"](#page-18-0). For information about compression for classic MySQL protocol connections, see Section 6.2.8, "Connection Compression Control".

On the client side, an X Protocol connection request can specify several parameters for compression control:

- The compression mode.
- The compression level.
- The list of permitted compression algorithms in priority order.

![](_page_21_Picture_6.jpeg)

#### **Note**

Some clients or Connectors might not support a given compression-control feature. For example, specifying compression level for X Protocol connections is supported only by MySQL Shell, not by other MySQL clients or Connectors. See the documentation for specific products for details about supported features and how to use them.

The connection mode has these permitted values:

- disabled: The connection is uncompressed.
- preferred: The server and client negotiate to find a compression algorithm they both permit. If no common algorithm is available, the connection is uncompressed. This is the default mode if not specified explicitly.
- required: Compression algorithm negotiation occurs as for preferred mode, but if no common algorithm is available, the connection request terminates with an error.

In addition to agreeing on a compression algorithm for each connection, the server and client can agree on a compression level from the numeric range that applies to the agreed algorithm. As the compression level for an algorithm increases, the data compression ratio increases, which reduces the network bandwidth and transfer time needed to send the message to the client. However, the effort required for data compression also increases, taking up time and CPU and memory resources on the server. Increases in the compression effort do not have a linear relationship to increases in the compression ratio.

The client can request a specific compression level during capability negotiations with the server for an X Protocol connection.

The default compression levels used by X Plugin in MySQL 8.4 have been selected through performance testing as being a good trade-off between compression time and network transit time. These defaults are not necessarily the same as the library default for each algorithm. They apply if the client does not request a compression level for the algorithm. The default compression levels are initially set to 3 for zstd, 2 for LZ4, and 3 for Deflate. You can adjust these settings using the [mysqlx\\_zstd\\_default\\_compression\\_level](#page-37-0), [mysqlx\\_lz4\\_default\\_compression\\_level](#page-31-0), and [mysqlx\\_deflate\\_default\\_compression\\_level](#page-29-0) system variables.

To prevent excessive resource consumption on the server, X Plugin sets a maximum compression level that the server permits for each algorithm. If a client requests a compression level that exceeds this setting, the server uses its maximum permitted compression level (compression level requests by a client are supported only by MySQL Shell). The maximum compression levels are initially set to 11 for zstd, 8 for LZ4, and 5 for Deflate. You can

```
adjust these settings using the mysqlx_zstd_max_client_compression_level,
mysqlx_lz4_max_client_compression_level, and
mysqlx_deflate_max_client_compression_level system variables.
```

If the server and client permit more than one algorithm in common, the default priority order for choosing an algorithm during negotiation is shown in [Table 22.1, "X Protocol Compression Algorithm](#page-20-1) [Characteristics"](#page-20-1). For clients that support specifying compression algorithms, the connection request can include a list of algorithms permitted by the client, specified using the algorithm name or its alias. The order of these algorithms in the list is taken as a priority order by the server. The algorithm used in this case is the first of those in the client list that is also permitted on the server side. However, the option for compression algorithms is subject to the compression mode:

- If the compression mode is disabled, the compression algorithms option is ignored.
- If the compression mode is preferred but no algorithm permitted on the client side is permitted on the server side, the connection is uncompressed.
- If the compression mode is required but no algorithm permitted on the client side is permitted on the server side, an error occurs.

To monitor the effects of message compression, use the X Plugin status variables described in [Monitoring Connection Compression for X Plugin](#page-23-0). You can use these status variables to calculate the benefit of message compression with your current settings, and use that information to tune your settings.

# <span id="page-22-0"></span>**Compressed Connection Characteristics for X Plugin**

X Protocol connection compression operates with the following behaviors and boundaries:

- The \_stream and \_message suffixes in algorithm names refer to two different operational modes: In stream mode, all X Protocol messages in a single connection are compressed into a continuous stream and must be decompressed in the same manner—following the order they were compressed and without skipping any messages. In message mode, each message is compressed individually and independently, and need not be decompressed in the order in which they were compressed. Also, message mode does not require all compressed messages to be decompressed.
- Compression is not applied to any messages that are sent before authentication succeeds.
- Compression is not applied to control flow messages such as Mysqlx.Ok, Mysqlx.Error, and Mysqlx.Sql.StmtExecuteOk messages.
- All other X Protocol messages can be compressed if the server and client agree on a mutually permitted compression algorithm during capability negotiation. If the client does not request compression at that stage, neither the client nor the server applies compression to messages.
- When messages sent over X Protocol connections are compressed, the limit specified by the [mysqlx\\_max\\_allowed\\_packet](#page-32-0) system variable still applies. The network packet must be smaller than this limit after the message payload has been decompressed. If the limit is exceeded, X Plugin returns a decompression error and closes the connection.
- The following points pertain to compression level requests by clients, which is supported only by MySQL Shell:
  - Compression levels must be specified by the client as an integer. If any other type of value is supplied, the connection closes with an error.
  - If a client specifies an algorithm but not a compression level, the server uses its default compression level for the algorithm.
  - If a client requests an algorithm compression level that exceeds the server maximum permitted level, the server uses the maximum permitted level.

• If a client requests an algorithm compression level that is less than the server minimum permitted level, the server uses the minimum permitted level.

# <span id="page-23-0"></span>**Monitoring Connection Compression for X Plugin**

You can monitor the effects of message compression using the X Plugin status variables. When message compression is in use, the session [Mysqlx\\_compression\\_algorithm](#page-38-1) status variable shows which compression algorithm is in use for the current X Protocol connection, and [Mysqlx\\_compression\\_level](#page-39-0) shows the compression level that was selected.

X Plugin status variables can be used to calculate the efficiency of the compression algorithms that are selected (the data compression ratio), and the overall effect of using message compression. Use the session value of the status variables in the following calculations to see what the benefit of message compression was for a specific session with a known compression algorithm. Or use the global value of the status variables to check the overall benefit of message compression for your server across all sessions using X Protocol connections, including all the compression algorithms that have been used for those sessions, and all sessions that did not use message compression. You can then tune message compression by adjusting the permitted compression algorithms, maximum compression level, and default compression level, as described in [Configuring Connection Compression for X](#page-20-0) [Plugin.](#page-20-0)

When message compression is in use, the [Mysqlx\\_bytes\\_sent](#page-38-2) status variable shows the total number of bytes sent out from the server, including compressed message payloads measured after compression, any items in compressed messages that were not compressed such as X Protocol headers, and any uncompressed messages. The [Mysqlx\\_bytes\\_sent\\_compressed\\_payload](#page-38-3) status variable shows the total number of bytes sent as compressed message payloads, measured after compression, and the [Mysqlx\\_bytes\\_sent\\_uncompressed\\_frame](#page-38-4) status variable shows the total number of bytes for those same message payloads but measured before compression. The compression ratio, which shows the efficiency of the compression algorithm, can therefore be calculated using the following expression:

```
mysqlx_bytes_sent_uncompressed_frame / mysqlx_bytes_sent_compressed_payload
```

The effectiveness of compression for X Protocol messages sent by the server can be calculated using the following expression:

```
(mysqlx_bytes_sent - mysqlx_bytes_sent_compressed_payload + mysqlx_bytes_sent_uncompressed_frame) / mysqlx_bytes_sent
```

### For messages received by the server from clients, the

[Mysqlx\\_bytes\\_received\\_compressed\\_payload](#page-38-5) status variable shows the total number of bytes received as compressed message payloads, measured before decompression, and the [Mysqlx\\_bytes\\_received\\_uncompressed\\_frame](#page-38-6) status variable shows the total number of bytes for those same message payloads but measured after decompression. The [Mysqlx\\_bytes\\_received](#page-38-7) status variable includes compressed message payloads measured before decompression, any uncompressed items in compressed messages, and any uncompressed messages.