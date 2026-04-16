# Oracle 23c - alter-pmem-filestore
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/alter-pmem-filestore.html

MOUNT

Use this command to mount a PMEM file store. If you have already specified the mount point and backing file paths in the `init.ora` file you can issue the command like this:

```
ALTER PMEM FILESTORE 'filestore_name' MOUNT
```

You can also specify the mount point and backing file paths in the command line. In this case, you must ensure that there is no mismatch between the values in the `init.ora` file and the values you specify in the command line. The command fails when a mismatch occurs, unless you specify `FORCE` to override the values in the `init.ora` file. The paths on the command line become the new paths for the PMEM file store.

If you use a `spfile`, then the parameters are automatically updated with the new paths specified on the command line.

Use the mount PMEM file store command in cases when the PMEM file store was not already automatically mounted during database startup.

Specify the mount point path or the backing file path on the command line when:

Before you can change the mount point and the backing file, you must first dismount the file store.

Examples

Example 1: Resize File Store Named cloud\_db\_1

```
ALTER PMEM FILESTORE cloud_db_1 RESIZE 5T
```

Example 2: Mount File Store Named cloud\_db\_1

```
ALTER  PMEM FILESTORE cloud_db_1 MOUNT  MOUNTPOINT â/corp/db/cloud_db_1â
    BACKINGFILE â/var/pmem/foo_1â
```

Example 3: Dismount File Store Named cloud\_db\_1

```
ALTER PMEM FILESTORE cloud_db_1 DISMOUNT
```