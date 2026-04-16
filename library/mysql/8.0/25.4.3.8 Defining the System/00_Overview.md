---
source: MySQL 8.0 Reference
title: 00_Overview
---

The [system] section is used for parameters applying to the cluster as a whole. The [Name](#page-173-0) system parameter is used with MySQL Enterprise Monitor; [ConfigGenerationNumber](#page-173-1) and [PrimaryMGMNode](#page-174-2) are not used in production environments. Except when using NDB Cluster with MySQL Enterprise Monitor, is not necessary to have a [system] section in the config.ini file.

More information about these parameters can be found in the following list:

<span id="page-173-1"></span>• [ConfigGenerationNumber](#page-173-1)

| Version (or<br>later) | NDB 8.0.13                                                                        |
|-----------------------|-----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                          |
| Default               | 0                                                                                 |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                    |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.0.13) |

Configuration generation number. This parameter is currently unused.

<span id="page-173-0"></span>• [Name](#page-173-0)

| Version (or<br>later) | NDB 8.0.13                                                                        |
|-----------------------|-----------------------------------------------------------------------------------|
| Type or units         | string                                                                            |
| Default               | []                                                                                |
| Range                 |                                                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.0.13) |

Set a name for the cluster. This parameter is required for deployments with MySQL Enterprise Monitor; it is otherwise unused.

You can obtain the value of this parameter by checking the Ndb\_system\_name status variable. In NDB API applications, you can also retrieve it using [get\\_system\\_name\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-get-system-name).

# <span id="page-174-2"></span>• [PrimaryMGMNode](#page-174-2)

| Version (or<br>later) | NDB 8.0.13                                                                        |
|-----------------------|-----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                          |
| Default               | 0                                                                                 |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                    |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.0.13) |

Node ID of the primary management node. This parameter is currently unused.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 25.19 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 25.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |