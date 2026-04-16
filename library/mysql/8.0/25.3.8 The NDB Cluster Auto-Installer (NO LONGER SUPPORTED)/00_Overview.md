---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_22_Picture_7.jpeg)

## **Note**

This feature has been removed from NDB Cluster, and is no longer supported. See Section 25.2.4, "What is New in MySQL NDB Cluster 8.0", for more information.

The web-based graphical configuration installer (Auto-Installer) was removed in NDB 8.0.23, and is no longer included as part of the NDB Cluster distribution.

# <span id="page-22-0"></span>**25.4 Configuration of NDB Cluster**

A MySQL server that is part of an NDB Cluster differs in one chief respect from a normal (nonclustered) MySQL server, in that it employs the NDB storage engine. This engine is also referred to sometimes as NDBCLUSTER, although NDB is preferred.

To avoid unnecessary allocation of resources, the server is configured by default with the NDB storage engine disabled. To enable NDB, you must modify the server's my.cnf configuration file, or start the server with the [--ndbcluster](#page-174-0) option.

This MySQL server is a part of the cluster, so it also must know how to access a management node to obtain the cluster configuration data. The default behavior is to look for the management node on localhost. However, should you need to specify that its location is elsewhere, this can be done in my.cnf, or with the mysql client. Before the NDB storage engine can be used, at least one management node must be operational, as well as any desired data nodes.

For more information about [--ndbcluster](#page-174-0) and other mysqld options specific to NDB Cluster, see [MySQL Server Options for NDB Cluster.](#page-174-1)

For general information about installing NDB Cluster, see Section 25.3, "NDB Cluster Installation".

# <span id="page-22-1"></span>**25.4.1 Quick Test Setup of NDB Cluster**

To familiarize you with the basics, we describe the simplest possible configuration for a functional NDB Cluster. After this, you should be able to design your desired setup from the information provided in the other relevant sections of this chapter.

First, you need to create a configuration directory such as /var/lib/mysql-cluster, by executing the following command as the system root user:

```
$> mkdir /var/lib/mysql-cluster
```

In this directory, create a file named config.ini that contains the following information. Substitute appropriate values for HostName and DataDir as necessary for your system.

```
# file "config.ini" - showing minimal setup consisting of 1 data node,