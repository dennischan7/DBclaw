# Oracle 11g - statements_1007
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_1007.htm

Semantics

diskgroup\_name

Specify the name of the disk group you want to modify. To determine the names of existing disk groups, query the [`V$ASM_DISKGROUP`](../../server.112/e40402/dynviews_1027.md#REFRN30171) dynamic performance view.

add\_disk\_clause

Use this clause to add one or more disks to the disk group and specify attributes for the newly added disk. Oracle ASM automatically rebalances the disk group as part of this operation.

You cannot use this clause to change the failure group of a disk. Instead you must drop the disk from the disk group and then add the disk back into the disk group as part of the new failure group.

To determine the names of the disks already in this disk group, query the [`V$ASM_DISK`](../../server.112/e40402/dynviews_1024.md#REFRN30170) dynamic performance view.

QUORUM | REGULAR 

The semantics of these keyword are the same as the semantics in a `CREATE` `DISKGROUP` statement. See [QUORUM | REGULAR](statements_5008.md#CACJHFHD) for more information on these keywords.

You cannot change this qualifier for an existing disk or disk group. Therefore, you cannot specify in this clause a keyword different from the keyword that was specified when the disk group was created.

FAILGROUP Clause Use this clause to assign the newly added disk to a failure group. If you omit this clause and you are adding the disk to a normal or high redundancy disk group, then Oracle Database automatically adds the newly added disk to its own failure group. The implicit name of the failure group is the same as the operating system independent disk name (see ["NAME Clause"](statements_5008.md#i2177129)).

You cannot specify this clause if you are creating an external redundancy disk group.

qualified\_disk\_clause

This clause has the same semantics in `CREATE` `DISKGROUP` and `ALTER` `DISKGROUP` statements. For complete information on this clause, refer to [qualified\_disk\_clause](statements_5008.md#i2177293) in the documentation on `CREATE` `DISKGROUP`.

drop\_disk\_clause

Use this clause to drop one or more disks from the disk group.

DROP DISK 

The `DROP` `DISK` clause lets you drop one or more disks from the disk group and automatically rebalance the disk group. When you drop a disk, Oracle ASM relocates all the data from the disk and clears the disk header so that it no longer is part of the disk group. The disk header is not cleared if you specify the `FORCE` keyword.

Specify `disk_name` as shown in the `NAME` column of the `V$ASM_DISK` dynamic performance view.

If a disk to be dropped is a quorum disk or belongs to a quorum failure group, then you must specify `QUORUM` in order to drop the disk. See [QUORUM | REGULAR](#BGBEHDFI).

DROP DISKS IN FAILGROUP 

The `DROP` `DISKS` `IN` `FAILGROUP` clause lets you drop all the disks in the specified failure group. The behavior is otherwise the same as that for the `DROP` `DISK` clause.

If the specified failure group is a quorum failure group, then you must specify the `QUORUM` keyword in order to drop the disks. See [QUORUM | REGULAR](#BGBEHDFI).

FORCE | NOFORCE These keywords let you specify when the disk is considered to be no longer part of the disk group. The default and recommended setting is `NOFORCE`.

* When you specify `NOFORCE`, Oracle ASM reallocates all of the extents of the disk to other disks and then expels the disk from the disk group and rebalances the disk group.

  Caution:

  `DROP` `DISK`

  ...

  `NOFORCE`

  returns control to the user before the disk can be safely reused or removed from the system. To ensure that the drop disk operation has completed, query the

  `V$ASM_DISK`

  view to verify that

  `HEADER_STATUS`

  has the value

  `FORMER`

  . Do not attempt to remove or reuse a disk if

  `STATE`

  has the value

  `DROPPING`

  . Query the

  `V$ASM_OPERATION`

  view for approximate information on how long it will take to complete the rebalance resulting from dropping the disk.If you also specify

  `REBALANCE`

  ...

  `WAIT`

  (see

  [rebalance\_diskgroup\_clause](#i2168800)

  ), then the statement will not return until the rebalance operation is complete and the disk has been cleared. However, you should always verify that the

  `HEADER_STATUS`

  column of

  `V$ASM_DISK`

  is

  `FORMER`

  , because of the unlikely event the rebalance operations fails.
* When you specify `FORCE`, Oracle Database expels the disk from the disk group immediately. It then reconstructs the data from the redundant copies on other disks, reallocates the data to other disks, and rebalances the disk group.

  The `FORCE` clause can be useful, for example, if Oracle ASM can no longer read the disk to be dropped. However, it is more time consuming than a `NOFORCE` drop, and it can leave portions of a file with reduced protection. You cannot specify `FORCE` for an external redundancy disk group at all, because in the absence of redundant data on the disk, Oracle ASM must read the data from the disk before it can be dropped.

The rebalance operation invoked when a disk is dropped is time consuming, whether or not you specify `FORCE` or `NOFORCE`. You can monitor the progress by querying the [`V$ASM_OPERATION`](../../server.112/e40402/dynviews_1031.md#REFRN30173) dynamic performance view. Refer to [rebalance\_diskgroup\_clause](#i2168800) for more information on rebalance operations.

resize\_disk\_clause

Use this clause to specify a new size for one or more disks in the disk group. This clause lets you override the size being returned by the operating system or the size you specified previously for the disks. The `QUORUM` and `REGULAR` keywords have the same semantics here as they have when adding a disk to a disk group. See [QUORUM | REGULAR](#BGBEHDFI).

RESIZE ALL Specify this clause to perform a resize operation on every disk in the disk group.

RESIZE DISK Specify this clause to resize only the specified disk.

Specify `disk_name` as shown in the `NAME` column of the `V$ASM_DISK` dynamic performance view.

If a disk to be resized is a quorum group, then you must specify `QUORUM` in order to drop the disk group. See [QUORUM | REGULAR](#BGBEHDFI).

RESIZE DISKS IN FAILGROUP Specify this clause to resize every disk in the specified failure group. If you omit both of the optional keywords `REGULAR` and `QUORUM`, then `REGULAR` is the default. If the failure group you are resizing is a `QUORUM` failure group, then you must specify the `QUORUM` keyword.

SIZE Specify the size of the disk in kilobytes, megabytes, gigabytes, or terabytes. You cannot specify a size greater than the capacity of the disk. If you specify a size smaller than the disk capacity, then you limit the amount of disk space Oracle ASM will use. If you omit this clause, then Oracle ASM uses the size being returned by the operating system.

disk\_offline\_clause

Use the `disk_offline_clause` to take one or more disks offline. This clause fails if the redundancy level of the disk group would be violated by taking the specified disks offline.

Specify `disk_name` as shown in the `NAME` column of the `V$ASM_DISK` dynamic performance view.

The `QUORUM` and `REGULAR` keywords have the same semantics here as they have when adding a disk to a disk group. See [QUORUM | REGULAR](#BGBEHDFI).

By default, Oracle ASM drops a disk shortly after it is taken offline. You can delay this operation by specifying the `timeout_clause`, which gives you the opportunity to repair the disk and bring it back online. You can specify the timeout value in units of minute or hour. If you omit the unit, then the default is hour.

You can change the timeout period by specifying this clause multiple times. Each time you specify it, Oracle ASM measures the time from the most recent previous `disk_offline_clause` while the disk group is mounted. To learn how much time remains before Oracle ASM will drop an offline disk, query the `repair_timer` column of `V$ASM_DISK`.

This clause overrides any previous setting of the `disk_repair_time` attribute. Refer to [Table 14-1, "Disk Group Attributes"](statements_5008.md#BGEDFCIB) for more information about disk group attributes.

disk\_online\_clause

Use the `disk_online_clause` to bring one or more disks online and rebalance the disk group. Specify `disk_name` as shown in the `NAME` column of the `V$ASM_DISK` dynamic performance view. The `QUORUM` and `REGULAR` keywords have the same semantics here as they have when adding a disk to a disk group. See [QUORUM | REGULAR](#BGBEHDFI). The `WAIT` and `NOWAIT` keywords have the same semantics here as they have for a manual rebalancing of a disk group. See [WAIT | NOWAIT](#BABHEIIB) for more information.

rebalance\_diskgroup\_clause

Use this clause to manually rebalance the disk group. Oracle ASM redistributes data files evenly across all drives. This clause is rarely necessary, because Oracle ASM allocates files evenly and automatically rebalances disk groups when the storage configuration changes. However, it is useful if you want to use the `POWER` clause to control the speed of what would otherwise be an automatic rebalance operation.

POWER In the `POWER` clause, specify a value from 0 to 11, where 0 stops the rebalance operation and 11 permits Oracle ASM to execute the rebalance as fast as possible. The value you specify in the `POWER` clause defaults to the value of the `ASM_POWER_LIMIT` initialization parameter.

If you omit the `POWER` clause, then Oracle ASM executes both automatic and specified rebalance operations at the power determined by the value of the `ASM_POWER_LIMIT` initialization parameter.

Note:

Beginning with Oracle Database 11

g

Release 2 (11.2.0.2), if the

`COMPATIBLE`

.

`ASM`

disk group attribute is set to 11.2.0.2 or higher, then you can specify a value from 0 to 1024 in the

`POWER`

clause.

WAIT | NOWAIT Use this clause to specify when in the course of the rebalance operation control should be returned to the user.

* Specify `WAIT` to allow a script that adds or removes disks to wait for the disk group to be rebalanced before returning control to the user. You can explicitly terminate a rebalance operation running in `WAIT` mode, although doing so does not undo any completed disk add or drop operation in the same statement.
* Specify `NOWAIT` if you want control returned to the user immediately after the statement is issued. This is the default.

You can monitor the progress of the rebalance operation by querying the [`V$ASM_OPERATION`](../../server.112/e40402/dynviews_1031.md#REFRN30173) dynamic performance view.

check\_diskgroup\_clause

The `check_diskgroup_clause` lets you verify the internal consistency of Oracle ASM disk group metadata. The disk group must be mounted. Oracle ASM displays summary errors and writes the details of the detected errors in the alert log.

The `CHECK` keyword performs the following operations:

* Checks the consistency of the disk.
* Cross checks all the file extent maps and allocation tables for consistently.
* Checks that the alias metadata directory and file directory are linked correctly.
* Checks that the alias directory tree is linked correctly.
* Checks that Oracle ASM metadata directories do not have unreachable allocated blocks.

REPAIR | NOREPAIR This clause lets you instruct Oracle ASM whether or not to attempt to repair any errors found during the consistency check. The default is `NOREPAIR`. The `NOREPAIR` setting is useful if you want to be alerted to any inconsistencies but do not want Oracle ASM to take any automatic action to resolve them.

Deprecated Clauses In earlier releases, you could specify `CHECK` for `ALL`, `DISK`, `DISKS` `IN` `FAILGROUP`, or `FILE`. Those clauses have been deprecated as they are no longer needed. If you specify them, then their behavior is the same as in earlier releases and a message is added to the alert log. However, Oracle recommends that you do not introduce these clauses into your new code, as they are scheduled for desupport. The deprecated clauses are these:

* `ALL` checks all disks and files in the disk group.
* `DISK` checks one or more specified disks in the disk group.
* `DISKS` `IN` `FAILGROUP` checks all disks in a specified failure group.
* `FILE` checks one or more specified files in the disk group. You must use one of the reference forms of the filename. Refer to [ASM\_filename](clauses004.md#i1026664) for information on the reference forms of Oracle ASM filenames.

diskgroup\_template\_clauses

A template is a named collection of attributes. When you create a disk group, Oracle ASM associates a set of initial system default templates with that disk group. The attributes defined by the template are applied to all files in the disk group. [Table 10-2](#BGBCHIIF) lists the system default templates and the attributes they apply to the various file types. The `diskgroup_template_clauses` described following the table let you change the template attributes and create new templates.

You cannot use this clause to change the attributes of a disk group file after it has been created. Instead, you must use Recovery Manager (RMAN) to copy the file into a new file with the new attributes.

Table 10-2 Oracle Automatic Storage Management System Default File Group Templates

| Template Name | File Type | Mirroring Level in External Redundancy Disk Groups | Mirroring Level in Normal Redundancy Disk Groups | Mirroring Level in High Redundancy Disk Groups | Striped | Region |
| --- | --- | --- | --- | --- | --- | --- |
| `CONTROLFILE` | Control files | Unprotected | 3-way mirror | 3-way mirror | `FINE` | `COLD` |
| `DATAFILE` | Data Files and copies | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `ONLINELOG` | Online logs | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `ARCHIVELOG` | Archive logs | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `TEMPFILE` | Temp files | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `BACKUPSET` | Data File backup pieces, data file incremental backup pieces, and archive log backup pieces | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `PARAMETERFILE` | SPFILE | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `DATAGUARDCONFIG` | Disaster recovery configurations (used in standby databases) | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `FLASHBACK` | Flashback logs | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `CHANGETRACKING` | Block change tracking data (used during incremental backups) | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `DUMPSET` | Data Pump dumpset | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `XTRANSPORT` | Cross-platform converted data file | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `AUTOBACKUP` | Automatic backup files | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `ASMPARAMETERFILE` | SPFILE | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |
| `OCRFILE` | Oracle Cluster Registry file | Unprotected | 2-way mirror | 3-way mirror | `COARSE` | `COLD` |

ADD TEMPLATE Use this clause to add one or more named templates to a disk group. To determine the names of existing templates, query the [`V$ASM_TEMPLATE`](../../server.112/e40402/dynviews_1032.md#REFRN30174) dynamic performance view.

MODIFY TEMPLATE Use this clause to modify the attributes of a system default or user-defined disk group template. Only the specified attributes are altered. Unspecified properties retain their current values.

Note:

In earlier releases, the keywords

`ALTER` `TEMPLATE`

were used instead of

`MODIFY` `TEMPLATE`

. The

`ALTER`

keyword is still supported for backward compatibility, but it replaced with

`MODIFY`

for consistency with other Oracle SQL.

template\_name Specify the name of the template to be added or modified. Template names are subject to the same naming conventions and restrictions as database schema objects. Refer to ["Database Object Naming Rules"](sql_elements008.md#i27570) for information on database object names.

redundancy\_clause  Specify the redundancy level of the newly added or modified template:

* `MIRROR`: Files to which this template are applied are protected by mirroring their data blocks. In normal redundancy disk groups, each primary extent has one mirror extent (2-way mirroring). For high redundancy disk groups, each primary extent has two mirror extents (3-way mirroring). You cannot specify `MIRROR` for templates in external redundancy disk groups.
* `HIGH`: Files to which this template are applied are protected by mirroring their data blocks. Each primary extent has two mirror extents (3-way mirroring) for both normal redundancy and high redundancy disk groups. You cannot specify `HIGH` for templates in external redundancy disk groups.
* `UNPROTECTED`: Files to which this template are applied are not protected by Automated Storage Management from media failures. Disks taken offline, either through system action or by user command, can cause loss of unprotected files. `UNPROTECTED` is the only valid setting for external redundancy disk groups. `UNPROTECTED` may not be specified for templates in high redundancy disk groups. Oracle discourages the use of unprotected files in high and normal redundancy disk groups.

If you omit this clause, then the value defaults to `MIRROR` for a normal redundancy disk group, `HIGH` for a high redundancy disk group, and `UNPROTECTED` for an external redundancy disk group.

striping\_clause  Specify how the files to which this template are applied will be striped:

* `FINE`: Files to which this template are applied are striped every 128KB. This striping mode is not valid for an Oracle ASM spfile.
* `COARSE`: Files to which this template are applied are striped every 1MB. This is the default value.

disk\_region\_clause  

This clause lets you determine the Intelligent Data Placement attribute of the disk group file. Specify the region of the disk in which you want Oracle ASM to allocate extents for the file:

* `HOT`: Extents are allocated in the region of the disk furthest away from the spindle. These outer tracks on the disk are longer than inner tracks, and so have more sectors and increased throughput.
* `COLD`: Extents are allocated in the region of the disk closest to the spindle.
* `MIRRORHOT` and `MIRRORCOLD`: Specify the region desired for the mirrored datablocks of the file.

If no space is available in the desired disk region, then Oracle ASM allocates extents in the other region but initiates a rebalance to adjust the size of the region.

DROP TEMPLATE Use this clause to drop one or more templates from the disk group. You can use this clause to drop only user-defined templates, not system default templates.

diskgroup\_directory\_clauses

Before you can create alias names for Oracle ASM filenames (see [diskgroup\_alias\_clauses](#i2168812)), you must specify the full directory structure in which the alias name will reside. The `diskgroup_directory_clauses` let you create and manipulate such a directory structure.

ADD DIRECTORY Use this clause to create a new directory path for hierarchically named aliases. Use a slash (/) to separate components of the directory. Each directory component can be up to 48 bytes in length and must not contain the slash character. You cannot use a space for the first or last character of any component. The total length of the directory path cannot exceed 256 bytes minus the length of any alias name you intend to create in this directory (see [diskgroup\_alias\_clauses](#i2168812)).

DROP DIRECTORY Use this clause to drop a directory for hierarchically named aliases. Oracle ASM will not drop the directory if it contains any alias definitions unless you also specify `FORCE`. This clause is not valid for dropping directories created as part of a system alias. Such directories are labeled with the value `Y` in the `SYSTEM_CREATED` column of the [`V$ASM_ALIAS`](../../server.112/e40402/dynviews_1021.md#REFRN30168) dynamic performance view.

RENAME DIRECTORY Use this clause to change the name of a directory for hierarchically named aliases. This clause is not valid for renaming directories created as part of a system alias. Such directories are labeled with the value `Y` in the `SYSTEM_CREATED` column of the [`V$ASM_ALIAS`](../../server.112/e40402/dynviews_1021.md#REFRN30168) dynamic performance view.

diskgroup\_alias\_clauses

When an Oracle ASM file is created, either implicitly or by user specification, Oracle ASM assigns to the file a fully qualified name ending in a dotted pair of numbers (see [file\_specification](clauses004.md#g1057086)). The `diskgroup_alias_clauses` let you create more user-friendly alias names for the Oracle ASM filenames. You cannot specify an alias name that ends in a dotted pair of numbers, as this format is indistinguishable from an Oracle ASM filename.

Before specifying this clause, you must first create the directory structure appropriate for your naming conventions (see [diskgroup\_directory\_clauses](#i2175401)). The total length of the alias name, including the directory prefix, is limited to 256 bytes. Alias names are case insensitive but case retentive.

ADD ALIAS Use this clause to create an alias name for an Oracle ASM filename. The `alias_name` consists of the full directory path and the alias itself. To determine the names of existing Oracle ASM aliases, query the [`V$ASM_ALIAS`](../../server.112/e40402/dynviews_1021.md#REFRN30168) dynamic performance view. Refer to [ASM\_filename](clauses004.md#i1026664) for information on Oracle ASM filenames.

DROP ALIAS Use this clause to remove an alias name from the disk group directory. Each alias name consists of the full directory path and the alias itself. The underlying file to which the alias refers remains unchanged.

RENAME ALIAS Use this clause to change the name of an existing alias. The `alias_name` consists of the full directory path and the alias itself.

Restriction on Dropping and Renaming Aliases You cannot drop or rename a system-generated alias. To determine whether an alias was system generated, query the `SYSTEM_CREATED` column of the [`V$ASM_ALIAS`](../../server.112/e40402/dynviews_1021.md#REFRN30168) dynamic performance view.

diskgroup\_volume\_clauses

Use these clauses to manipulate logical Oracle ASM Dynamic Volume Manager (Oracle ADVM) volumes corresponding to physical volume devices. To use these clauses, Oracle ASM must be started and the disk group being modified must be mounted.

add\_volume\_clause  Use this clause to add a volume to the disk group.

For `asm_volume`, specify the name of the volume. The name can contain only alphanumeric characters and the first character must be alphabetic. The maximum length of the name is platform dependant. Refer to [Oracle Automatic Storage Management Administrator's Guide](../../server.112/e18951/asm_util007.md#OSTMG94739) for more information.

For `size_clause`, specify the size of the Oracle ADVM volume. The Oracle ASM instance determines whether sufficient space exists to create the volume. If sufficient space does not exist, then the Oracle ASM instance returns an error. If sufficient space does exist, then all nodes in the cluster with an Oracle ASM instance running and the disk group mounted are notified of the addition. Oracle ASM creates and enables on those nodes a volume device that can be used to create and mount file systems.

The following optional settings are also available:

* In the `redundancy_clause`, specify the redundancy level of the Oracle ADVM volume. You can specify this clause only when creating a volume in a normal redundancy disk group. You can specify the following volume redundancy levels:

  + `MIRROR`: 2-way mirroring of the volume. This is the default.
  + `HIGH`: 3-way mirroring of the volume.
  + `UNPROTECTED`: No mirroring of the volume.

  You cannot specify the `redundancy_clause` when creating a volume in a high redundancy disk group or an external redundancy disk group. If you do so, then an error will result. In high redundancy disk groups, Oracle Database automatically sets the volume redundancy to `HIGH` (3-way mirroring). In external redundancy disk groups, Oracle Database automatically sets the volume redundancy to `UNPROTECTED` (no mirroring).
* In the `STRIPE_WIDTH` clause, specify a stripe width for the Oracle ADVM Volume. The valid range is from 4KB to 1MB, at intervals of the power of 2. The default value is 128K.
* In the `STRIPE_COLUMNS` clause, specify the number of stripes in a stripe set of the Oracle ADVM volume. The valid range is 1 to 8. The default is 4. If `STRIPE_COLUMNS` is set to 1, then striping becomes disabled. In this case, the stripe width is the extent size of the volume. This volume extent size is 64 times the allocation unit (AU) size of the disk group
* In the `disk_region_clause` clause, specify the Intelligent Data Placement attribute of both the primary and nonprimary mirror of the disk group volume. The default for both is `COLD`. See [disk\_region\_clause](#BGBJECEI) for details on this clause.

modify\_volume\_clause  Use this clause to modify the characteristics of an existing Oracle ADVM volume. You must specify at least one of the following clauses:

* In the `disk_region_clause` clause, specify the Intelligent Data Placement attribute of both the primary and nonprimary mirror of the disk group volume. The default for the primary mirror is `COLD`. The default for mirror and high redundancy is `HOT`. See [disk\_region\_clause](#BGBJECEI) for details on this clause.
* In the `MOUNTPATH` clause, specify the mountpath name associated with the volume. The `mountpath_name` can be up to 1024 characters.
* In the `USAGE` clause, specify the usage name associated with the volume. The `usage_name` can be up to 30 characters.

RESIZE VOLUME Clause  

Use this clause to change the size of an existing Oracle ADVM volume. In an Oracle ASM cluster, the new size is propagated to all nodes. If an Oracle Automatic Storage Management File System (ACFS) exists on the volume, then you must use the `acfsutil` `size` command instead of the `ALTER` `DISKGROUP` statement.

DROP VOLUME Clause  Use this clause to remove the Oracle ASM file that is the storage container for an existing Oracle ADVM volume. In an Oracle ASM cluster, all nodes with an Oracle ASM instance running and with this disk group open are notified of the drop operation, which results in removal of the volume device. If the volume file is open, then this clause returns an error.

diskgroup\_attributes

Use this clause to specify attributes for the disk group. [Table 14-1, "Disk Group Attributes"](statements_5008.md#BGEDFCIB) lists the attributes you can set with this clause. Refer to the `CREATE` `DISKGROUP` ["ATTRIBUTE Clause"](statements_5008.md#BABECECH) for information on the behavior of this clause.

modify\_diskgroup\_file

Use this clause to modify the Intelligent Data Placement attributes of an existing disk group file. When you modify the Intelligent Data Placement for a file, this action will apply to new extensions of the file, but existing file contents are not affected until a rebalance operation. To apply the new Intelligent Data Placement policy for existing file contents, you can manually initiate a rebalance. A rebalance operation uses the last specified policy for the file extents.

drop\_diskgroup\_file\_clause

Use this clause to drop a file from the disk group. Oracle ASM also drops all aliases associated with the file being dropped. You must use one of the reference forms of the filename. Most Oracle ASM files do not need to be manually deleted because, as Oracle Managed Files, they are removed automatically when they are no longer needed. Refer to [ASM\_filename](clauses004.md#i1026664) for information on the reference forms of Oracle ASM filenames.

You cannot drop a disk group file it if is the spfile that was used to start up the current instance or any instance in the Oracle ASM cluster.

usergroup\_clauses

Use these clauses to add a user group to the disk group, remove a user group from the disk group, or to add a member to or drop a member from an existing user group.

ADD USERGROUP  Use this clause to add a user group to the disk group. You must have `SYSASM` or `SYSDBA` privilege to create a user group. The user group name can be up to 30 characters long. If you specify the user name, then it must be in the OS password file.

MODIFY USERGROUP  Use these clauses to add a member to or drop a member from an existing user group. You must be an Oracle ASM administrator (with SYSASM privilege) or the creator (with SYSDBA privilege) of the user group to use these clauses. The user name must be an existing user in the OS password file.

DROP USERGROUP  Use this clause to drop an existing user group from the disk group. You must be an Oracle ASM administrator (with SYSASM privilege) or the creator (with SYSDBA privilege) of the user group to use this clause. Dropping a user group may leave a disk group file without a valid user group. In this case, you can update the disk group file manually to add a new, valid group using the [file\_permissions\_clause](#BGBJGAFA).

user\_clauses

Use these clauses to add a user to or drop a user from a disk group.

ADD USER  Use this clause to add one or more operating system (OS) users to an Oracle ASM disk group and give those users access privileges on the disk group. The `user` names must be existing OS users, and their user names must have a corresponding OS user ID or system ID. If a specified user already exists in the disk group, as shown by `V$ASM_USER`, then the command records an error and continues to add other users, if any have been specified. This command is seldom needed, because the OS user running the database instance is added to a disk group automatically when the instance accesses the disk group. However, this clause is useful when adding users that are not associated with a particular database instance.

DROP USER  Use this clause to drop one or more users from the disk group. If a specified user is not in the disk group, then this clause records an error and continues to drop other users, if any are specified. If the user owns any files, then you must specify the `CASCADE` keyword, which drops the user and all the user's files. If any files owned by the user are open, then `DROP` `USER` `CASCADE` fails with an error.

To delete a user without deleting the files owned by that user, change the owner of each of these files to another user and then issue an `ALTER` `DISKGROUP` ... `DROP` `USER` statement on the user.

file\_permissions\_clause

Use this clause to change the permission settings of a disk group file. The three classes of permissions are owner, user group, and other. You must be the file owner or the Oracle ASM administrator to use this clause. You cannot use this clause on an open file.

file\_owner\_clause

Use this clause to set the owner or user group for a specified file. You must be the Oracle ASM administrator to change the owner of the file. You must be the owner of the file or the Oracle ASM administrator to change the user group of a file. In addition, to change the associated user group of a file, the specified user group must already exist in the disk group, and the owner of the file must be a member of that user group. You cannot use this clause on an open file.

undrop\_disk\_clause

Use this clause to cancel the drop of disks from the disk group. You can cancel the pending drop of all the disks in one or more disk groups (by specifying `diskgroup_name`) or of all the disks in all disk groups (by specifying `ALL`).

This clause is not relevant for disks that have already been completely dropped from the disk group or for disk groups that have been completely dropped. This clause results in a long-running operation. You can see the status of the operation by querying the `V$ASM_OPERATION` dynamic performance view.

See Also:

[`V$ASM_OPERATION`](../../server.112/e40402/dynviews_1031.md#REFRN30173)

for more information on the details of long-running Oracle ASM operations

diskgroup\_availability

Use this clause to make one or more disk groups available or unavailable to the database instances running on the same node as the Oracle ASM instance. This clause does not affect the status of the disk group on other nodes in a cluster.

MOUNT 

Specify `MOUNT` to mount the disk groups in the local Oracle ASM instance. Specify `ALL` `MOUNT` to mount all disk groups specified in the `ASM_DISKGROUPS` initialization parameter. File operations can only be performed when a disk group is mounted. If Oracle ASM is running in a cluster or a standalone server managed by Oracle Restart, then the `MOUNT` clause automatically brings the corresponding resource online.

RESTRICTED | NORMAL Use these clauses to determine the manner in which the disk groups are mounted.

* In the `RESTRICTED` mode, the disk group is mounted in single-instance exclusive mode. No other Oracle ASM instance in the same cluster can mount that disk group. In this mode the disk group is not usable by any Oracle ASM client.
* In the `NORMAL` mode, the disk group is mounted in shared mode, so that other Oracle ASM instances and clients can access the disk group. This is the default.

FORCE | NOFORCE Use these clauses to determine the circumstances under which the disk groups are mounted.

* In the `FORCE` mode, Oracle ASM attempts to mount the disk group even if it cannot discover all of the devices that belong to the disk group. This setting is useful if some of the disks in a normal or high redundancy disk group became unavailable while the disk group was dismounted. When `MOUNT` `FORCE` succeeds, Oracle ASM takes the missing disks offline.

  If Oracle ASM discovers all of the disks in the disk group, then `MOUNT` `FORCE` fails. Therefore, use the `MOUNT` `FORCE` setting only if some disks are unavailable. Otherwise, use `NOFORCE`.

  In normal- and high-redundancy disk groups, disks from one failure group can be unavailable and `MOUNT` `FORCE` will succeed. Also in high-redundancy disk groups, two disks in two different failure groups can be unavailable and `MOUNT` `FORCE` will succeed. Any other combination of unavailable disks causes the operation to fail, because Oracle ASM cannot guarantee that a valid copy of all user data or metadata exists on the available disks.
* In the `NOFORCE` mode, Oracle ASM does not attempt to mount the disk group unless it can discover all the member disks. This is the default.

See Also:

ASM\_DISKGROUPS for more information about adding disk group names to the initialization parameter file

DISMOUNT 

Specify `DISMOUNT` to dismount the specified disk groups. Oracle ASM returns an error if any file in the disk group is open unless you also specify `FORCE`. Specify `ALL` `DISMOUNT` to dismount all currently mounted disk groups. File operations can only be performed when a disk group is mounted. If Oracle ASM is running in a cluster or a standalone server managed by Oracle Restart, then the `DISMOUNT` clause automatically takes the corresponding resource offline.

FORCE Specify `FORCE` if you want Oracle ASM to dismount the disk groups even if some files in the disk group are open.

enable\_disable\_volume

Use this clause to enable or disable one or more volumes in the disk group.

* For each volume you enable, Oracle ASM creates a volume device file on the local node that can be used to create or mount the file system.
* For each volume you disable, Oracle ASM deletes the device file on the local node. If the volume file is open on the local node, then the `DISABLE` clause returns an error.

Use the `ALL` keyword to enable or disable all volumes in the disk group. If you specify `ALTER` `DISKGROUP` `ALL` `...`, then you must use the `ALL` keyword in this clause as well.

Examples

The following examples require a disk group called `dgroup_01`. They assume that `ASM_DISKSTRING` is set to `/devices/disks/*`. In addition, they assume the Oracle user has read/write permission to `/devices/disks/d100`. Refer to ["Creating a Diskgroup: Example"](statements_5008.md#CACIHAAD) to create `dgroup_01`.

Adding a Disk to a Disk Group: Example To add a disk, `d100`, to a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  ADD DISK '/devices/disks/d100';
```

Dropping a Disk from a Disk Group: Example To drop a disk, `dgroup_01_0000`, from a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  DROP DISK dgroup_01_0000;
```

Undropping a Disk from a Disk Group: Example To cancel the drop of disks from a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  UNDROP DISKS;
```

Resizing a Disk Group: Example To resize every disk in a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  RESIZE ALL
  SIZE 36G;
```

Rebalancing a Disk Group: Example To manually rebalance a disk group, `dgroup_01`, and permit Oracle ASM to execute the rebalance as fast as possible, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  REBALANCE POWER 11 WAIT;
```

The `WAIT` keyword causes the database to wait for the disk group to be rebalanced before returning control to the user.

Verifying the Internal Consistency of Disk Group Metadata: Example To verify the internal consistency of Oracle ASM disk group metadata and instruct Oracle ASM to repair any errors found, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  CHECK ALL
  REPAIR;
```

Adding a Named Template to a Disk Group: Example To add a named template, `template_01` to a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  ADD TEMPLATE template_01
    ATTRIBUTES (UNPROTECTED COARSE);
```

Changing the Attributes of a Disk Group Template: Example To modify the attributes of a system default or user-defined disk group template, `template_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  MODIFY TEMPLATE template_01
    ATTRIBUTES (FINE);
```

Dropping a User-Defined Template from a Disk Group: Example To drop a user-defined template, `template_01`, from a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  DROP TEMPLATE template_01;
```

Creating a Directory Path for Hierarchically Named Aliases: Example To specify the directory structure in which alias names will reside, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  ADD DIRECTORY '+dgroup_01/alias_dir';
```

Creating an Alias Name for an Oracle ASM Filename: Example To create a user alias by specifying the numeric Oracle ASM filename, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  ADD ALIAS '+dgroup_01/alias_dir/datafile.dbf'
    FOR '+dgroup_01.261.1';
```

Dismounting a Disk Group: Example To dismount a disk group, `dgroup_01`, issue the following statement. This statement dismounts the disk group even if one or more files are active:

```
ALTER DISKGROUP dgroup_01
  DISMOUNT FORCE;
```

Mounting a Disk Group: Example To mount a disk group, `dgroup_01`, issue the following statement:

```
ALTER DISKGROUP dgroup_01
  MOUNT;
```