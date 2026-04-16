---
source: MySQL 8.0 Reference
title: 00_Overview
---

If an error code is returned when issuing a backup request, the most likely cause is insufficient memory or disk space. You should check that there is enough memory allocated for the backup.

![](_page_98_Picture_3.jpeg)

### **Important**

If you have set BackupDataBufferSize and BackupLogBufferSize and their sum is greater than 4MB, then you must also set BackupMemory as well.

You should also make sure that there is sufficient space on the hard drive partition of the backup target.

NDB does not support repeatable reads, which can cause problems with the restoration process. Although the backup process is "hot", restoring an NDB Cluster from backup is not a 100% "hot" process. This is due to the fact that, for the duration of the restore process, running transactions get nonrepeatable reads from the restored data. This means that the state of the data is inconsistent while the restore is in progress.

# <span id="page-98-0"></span>**25.6.8.5 Taking an NDB Backup with Parallel Data Nodes**

It is possible in NDB 8.0 to take a backup with multiple local data managers (LDMs) acting in parallel on the data nodes. For this to work, all data nodes in the cluster must use multiple LDMs, and each data node must use the same number of LDMs. This means that all data nodes must run ndbmtd (ndbd is single-threaded and thus always has only one LDM) and they must be configured to use multiple LDMs before taking the backup; ndbmtd by default runs in single-threaded mode. You can cause them to use multiple LDMs by choosing an appropriate setting for one of the multi-threaded data node configuration parameters MaxNoOfExecutionThreads or ThreadConfig. Keep in mind that changing these parameters requires a restart of the cluster; this can be a rolling restart. In addition, the EnableMultithreadedBackup parameter must be set to 1 for each data node (this is the default).

Depending on the number of LDMs and other factors, you may also need to increase NoOfFragmentLogParts. If you are using large Disk Data tables, you may also need to increase DiskPageBufferMemory. As with single-threaded backups, you may also want or need to make adjustments to settings for BackupDataBufferSize, BackupMemory, and other configuration parameters relating to backups (see Backup parameters).

Once all data nodes are using multiple LDMs, you can take the parallel backup using the [START](#page-93-0) [BACKUP](#page-93-0) command in the NDB management client just as you would if the data nodes were running ndbd (or ndbmtd in single-threaded mode); no additional or special syntax is required, and you can specify a backup ID, wait option, or snapshot option in any combination as needed or desired.

Backups using multiple LDMs create subdirectories, one per LDM, under the directory BACKUP/ BACKUP-backup\_id/ (which in turn resides under the BackupDataDir) on each data node; these subdirectories are named BACKUP-backup\_id-PART-1-OF-N/, BACKUP-backup\_id-PART-2-OF-N/, and so on, up to BACKUP-backup\_id-PART-N-OF-N/, where backup\_id is the backup ID used for this backup and N is the number of LDMs per data node. Each of these subdirectories contains the usual backup files BACKUP-backup\_id-0.node\_id.Data, BACKUP-backup\_id.node\_id.ctl, and BACKUP-backup\_id.node\_id.log, where node\_id is the node ID of this data node.

ndb\_restore automatically checks for the presence of the subdirectories just described; if it finds them, it attempts to restore the backup in parallel. For information about restoring backups taken with multiple LDMs, see [Section 25.5.23.3, "Restoring from a backup taken in parallel".](#page-1-0)

To force creation of a single-threaded backup that can easily be imported by ndb\_restore from an NDB release prior to 8.0, you can set EnableMultithreadedBackup = 0 for all data nodes (you can do this by setting the parameter in the [ndbd default] section of the config.ini global configuration file). It is also possible to restore a parallel backup to a cluster running an older version of NDB. See Restoring an NDB backup to a previous version of NDB Cluster, for more information.