---
source: MySQL 5.7 Reference
title: 00_Overview
---

The [computer] section has no real significance other than serving as a way to avoid the need of defining host names for each node in the system. All parameters mentioned here are required.

• Id

| Version (or<br>later) | NDB 7.5.0                                                               |
|-----------------------|-------------------------------------------------------------------------|
| Type or units         | string                                                                  |
| Default               | []                                                                      |
| Range                 |                                                                         |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the |

cluster, wiping and restoring the cluster file system from a backup, and then restarting the cluster. (NDB 7.5.0)

This is a unique identifier, used to refer to the host computer elsewhere in the configuration file.

![](_page_1_Picture_3.jpeg)

### **Important**

The computer ID is not the same as the node ID used for a management, API, or data node. Unlike the case with node IDs, you cannot use NodeId in place of Id in the [computer] section of the config.ini file.

### • HostName

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

This is the computer's hostname or IP address.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 21.7 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 21.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |