# Oracle 11g - statements_5008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_5008.htm

Prerequisites

You must have the `SYSASM` system privilege to issue this statement.

Before issuing this statement, you must format the disks using an operating system format utility. Also ensure that the Oracle Database user has read/write permission and the disks can be discovered using the `ASM_DISKSTRING`.

When you store your database files in Oracle ASM disk groups, rather than in a file system or on raw devices, before the database instance can access your files in the disk groups, you must configure and start up an Oracle ASM instance to manage the disk groups.

Each database instance communicates with a single Oracle ASM instance on the same node as the database. Multiple database instances on the same node can communicate with a single Oracle ASM instance.

Semantics

diskgroup\_name

Specify the name of the disk group. Disk groups are subject to the same naming conventions and restrictions as database schema objects. Refer to ["Database Object Naming Rules"](sql_elements008.md#i27570) for information on database object names. However, disk groups are not schema objects. Disk group names are not case sensitive, even if you specify them with quotation marks. They are always stored internally as uppercase.

Note:

Oracle does not recommend using quoted identifiers for disk group names. These quoted identifiers are accepted when issuing the

`CREATE` `DISKGROUP`

statement in SQL\*Plus, but they may not be valid when using other tools that manage disk groups.

REDUNDANCY Clause

The `REDUNDANCY` clause lets you specify the redundancy level of the disk group.

* `NORMAL` `REDUNDANCY` requires the existence of at least two failure groups (see the `FAILGROUP` clause that follows). Oracle ASM provides redundancy for all files in the disk group according to the attributes specified in the disk group templates. `NORMAL` `REDUNDANCY` disk groups can tolerate the loss of one group. Refer to `ALTER` `DISKGROUP` ... [diskgroup\_template\_clauses](statements_1007.md#i2168808) for more information on disk group templates.

  `NORMAL` `REDUNDANCY` is the default if you omit the `REDUNDANCY` clause. Therefore, if you omit this clause, you must create at least two failure groups, or the create operation will fail.
* `HIGH` `REDUNDANCY` requires the existence of at least three failure groups. Oracle ASM fixes mirroring at 3-way mirroring, with each extent getting two mirrored copies. `HIGH` `REDUNDANCY` disk groups can tolerate the loss of two failure groups.
* `EXTERNAL` `REDUNDANCY` indicates that Oracle ASM does not provide any redundancy for the disk group. The disks within the disk group must provide redundancy (for example, using a storage array), or you must be willing to tolerate loss of the disk group if a disk fails (for example, in a test environment). You cannot specify the `FAILGROUP` clause if you specify `EXTERNAL` `REDUNDANCY`.

You cannot change the redundancy level after the disk group has been created.

QUORUM | REGULAR

Use these keywords to qualify either failure group or disk specifications.

* `REGULAR` disks, or disks in non-quorum failure groups, can contain any files.
* `QUORUM` disks, or disks in quorum failure groups, cannot contain any database files, the Oracle Cluster Registry (OCR), or dynamic volumes. However, `QUORUM` disks can contain the voting file for Cluster Synchronization Services (CSS). Oracle ASM uses quorum disks or disks in quorum failure groups for voting files whenever possible.

  Disks in quorum failure groups are not considered when determining redundancy requirements.

If you specify neither keyword, then `REGULAR` is the default.

Specify either `QUORUM` or `REGULAR` before the keyword `FAILGROUP` if you are explicitly specifying the failure group. If you are creating a disk group with implicitly created failure groups, then specify these keywords before the keyword `DISK`.

FAILGROUP Clause

Use this clause to specify a name for one or more failure groups. If you omit this clause, and you have specified `NORMAL` or `HIGH` `REDUNDANCY`, then Oracle Database automatically adds each disk in the disk group to its own failure group. The implicit name of the failure group is the same as the operating system independent disk name (see ["NAME Clause"](#i2177129)).

You cannot specify this clause if you are creating an `EXTERNAL` `REDUNDANCY` disk group.

qualified\_disk\_clause

Specify `DISK` `qualified_disk_clause` to add a disk to a disk group.

search\_string  For each disk you are adding to the disk group, specify the operating system dependent search string that Oracle ASM will use to find the disk. The `search_string` must point to a subset of the disks returned by discovery using the strings in the `ASM_DISKSTRING` initialization parameter. If `search_string` does not point to any disks the Oracle Database user has read/write access to, then Oracle ASM returns an error. If it points to one or more disks that have already been assigned to a different disk group, then Oracle Database returns an error unless you also specify `FORCE`.

For each valid candidate disk, Oracle ASM formats the disk header to indicate that it is a member of the new disk group.

See Also:

The

[`ASM_DISKSTRING`](../../server.112/e40402/initparams011.md#REFRN10248)

initialization parameter for more information on specifying the search string

NAME Clause The `NAME` clause is valid only if the `search_string` points to a single disk. This clause lets you specify an operating system independent name for the disk. The name can be up to 30 alphanumeric characters. The first character must be alphabetic. If you omit this clause and you assigned a label to a disk through ASMLIB, then that label is used as the disk name. If you omit this clause and you did not assign a label through ASMLIB, then Oracle ASM creates a default name of the form `diskgroup_name`\_####, where #### is the disk number. You use this name to refer to the disk in subsequent Oracle ASM operations.

SIZE Clause Use this clause to specify in bytes the size of the disk. If you specify a size greater than the capacity of the disk, then Oracle ASM returns an error. If you specify a size less than the capacity of the disk, then you limit the disk space Oracle ASM will use. If you omit this clause, then Oracle ASM attempts programmatically to determine the size of the disk.

FORCE Specify `FORCE` if you want Oracle ASM to add the disk to the disk group even if the disk is already a member of a different disk group.

Caution:

Using

`FORCE`

in this way may destroy existing disk groups.

For this clause to be valid, the disk must already be a member of a disk group and the disk cannot be part of a mounted disk group.

NOFORCE Specify `NOFORCE` if you want Oracle ASM to return an error if the disk is already a member of a different disk group. `NOFORCE` is the default.

ATTRIBUTE Clause

Use this clause to set attribute values for the disk group. You can view the current attribute values by querying the `V$ASM_ATTRIBUTE` view. [Table 14-1](#BGEDFCIB) lists the attributes you can set with this clause. All attribute values are strings.

Table 14-1 Disk Group Attributes

| Attribute | Valid Values | Description |
| --- | --- | --- |
| `ACCESS_CONTROL.ENABLED` | `true` or `false` | Specifies whether Oracle ASM File Access Control is enabled for a disk group. If set to `true`, accessing Oracle ASM files is subject to access control. If `false`, any user can access every file in the disk group. All other operations behave independently of this attribute. The default value is `false`.  If both the `compatible.rdbms` and `compatible.asm` attributes are set to at least 11.2, you can set this attribute in an `ALTER` `DISKGROUP` ... `SET` `ATTRIBUTE` statement. You cannot set this attribute when creating a disk group.  When you set up file access control on an existing disk group, the files previously created remain accessible by everyone, unless you run the `ALTER` `DISKGROUP` `SET` `PERMISSION` statement to restrict the permissions.  Note: This attribute is used in conjunction with `ACCESS_CONTROL`.`UMASK` to manage Oracle ASM File Access Control. After setting the `ACCESS_CONTROL`.`ENABLED` disk attribute, you must set permissions with the `ACCESS_CONTROL`.`UMASK` attribute. |
| `ACCESS_CONTROL.UMASK` | A three-digit number where each digit is 0, 2, or 6. | Determines which permissions are masked out on the creation of an Oracle ASM file for the user that owns the file (first digit), users in the same user group (second digit), and others not in the user group (third digit). This attribute applies to all files on a disk group. Setting to 0 masks out nothing. Setting to 2 masks out write permission. Setting to 6 masks out both read and write permissions. The default value is `066`.  If both the `compatible.rdbms` and `compatible.asm` attributes are set to at least 11.2, you can set this attribute in an `ALTER` `DISKGROUP` ... `SET` `ATTRIBUTE` statement. You cannot set this attribute when creating a disk group.  When you set up file access control on an existing disk group, the files previously created remain accessible by everyone, unless you run the `ALTER` `DISKGROUP` `SET` `PERMISSION` statement to restrict the permissions.  Note: This attribute is used in conjunction with `ACCESS_CONTROL`.`ENABLED` to manage Oracle ASM File Access Control. Before setting `ACCESS_CONTROL`.`UMASK`, you must set `ACCESS_CONTROL`.`ENABLED` to `true`. |
| `AU_SIZE` | Size in bytes. Valid values are powers of 2 from 1M to 64M. Examples '4M', '4194304'. | Specifies the allocation unit size. This attribute can be set only during disk group creation; it cannot be modified with an `ALTER` `DISKGROUP` statement. |
| `COMPATIBLE.ADVM` | Valid Oracle Database version number | Determines whether the disk group can contain Oracle ADVM volumes. The value must be set to `11`.`2` or higher. Before setting this attribute, the `COMPATIBLE`.`ASM` value must be `11`.`2` or higher. Also, the Oracle ADVM volume drivers must be loaded.  By default, the value of the `COMPATIBLE`.`ADVM` attribute is empty until set. |
| `COMPATIBLE.ASM` | Valid Oracle Database version number | Determines the minimum software version for an Oracle ASM instance that can use the disk group. This setting also affects the format of the data structures for the Oracle ASM metadata on the disk.  For Oracle ASM in Oracle Database 11g, `10`.`1` is the default setting for the `COMPATIBLE`.`ASM` attribute when using the SQL `CREATE` `DISKGROUP` statement, the ASMCMD mkdg command, and Oracle Enterprise Manager Create Disk Group page. When creating a disk group with ASMCA, the default setting is `11`.`2`. |
| `COMPATIBLE.RDBMS` | Valid Oracle Database version number | Determines the minimum `COMPATIBLE` database initialization parameter setting for any database instance that is allowed to use the disk group.  Before advancing the `COMPATIBLE`.`RDBMS` attribute, ensure that the values for the `COMPATIBLE` initialization parameter for all of the databases that access the disk group are set to at least the value of the new setting for `COMPATIBLE`.`RDBMS`. For example, if the `COMPATIBLE` initialization parameters of the databases are set to either `11`.`1` or `11`.`2`, then `COMPATIBLE`.`RDBMS` can be set to any value between `10`.`1` and `11`.`1` inclusively.  For Oracle ASM in Oracle Database 11g, `10`.`1` is the default setting for the `COMPATIBLE`.`RDBMS` attribute when using the SQL `CREATE` `DISKGROUP` statement, the ASMCMD mkdg command, ASMCA Create Disk Group page, and Oracle Enterprise Manager Create Disk Group page. |
| `DISK_REPAIR_TIME` | 0 to 136 years | When disks are taken offline, Oracle ASM drops them after a default period of time. If both the `compatible.rdbms` and `compatible.asm` attributes are set to at least 11.1, you can set the `disk_repair_time` attribute in an `ALTER` `DISKGROUP` ... `SET` `ATTRIBUTE` statement to change that default period of time so that the disk can be repaired and brought back online. You cannot set this attribute when creating a disk group.  The time can be specified in units of minute (M) or hour (H). The specified time elapses only when the disk group is mounted. If you omit the unit, then the default is H. If you omit this attribute, and both `compatible.rdbms` and `compatible.asm` are set to at least 11.1, then the default is 3.6 H. Otherwise the disk is dropped immediately. You can override this attribute with an `ALTER` `DISKGROUP` ... `OFFLINE` `DISK` statement and the `DROP` `AFTER` clause.  Note: If a disk is taken offline using the current value of `disk_repair_time`, and the value of this attribute is subsequently changed, then the changed value is used by Oracle ASM in the disk offline logic.  See Also: The `ALTER` `DISKGROUP` ... [disk\_offline\_clause](statements_1007.md#BABFJHFG) and [Oracle Automatic Storage Management Administrator's Guide](../../server.112/e18951/asmdiskgrps.md#OSTMG10044) for more information |
| `SECTOR_SIZE` | Sector size of the disks in the disk group. Valid values are '512' '4096', and '4K'. | All disks in the disk group must have a sector size equal to the attribute value specified. When processing the `CREATE` `DISKGROUP` statement, Oracle ASM queries the operating system for the sector size of every disk specified in this statement before it is added to the disk group, ensuring that a disk group is made up of disks with identical sector size. If a disk is found to have a different sector size than is specified for this attribute, then the statement fails. Similar checks are performed when mounting the disk group. If you omit this attribute in the `CREATE` `DISKGROUP` statement, then Oracle ASM proceeds with the create operation as long as all specified disks are found to have identical sector size, and that value is assumed as the disk group sector size.  When new disks are added to an existing disk group, using the `ALTER` `DISKGROUP` ... `ADD` `DISK` statement, the new disks must also have sector size value identical to the disk group attribute. Oracle ASM verifies this and the `ALTER` `DISKGROUP` statement fails if any of the disks to be added are found to be of a different sector size.  By setting a value for this attribute, you can establish the sector size you intend for the disk group, rather than letting Oracle ASM assume a value for all the disks in the disk group. As a result, users can query the `SECTOR_SIZE` column of the `V$ASM_ATTRIBUTE` view to determine the intended sector size before attempting to add a new disk to the disk group. |