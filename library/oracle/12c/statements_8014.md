# Oracle 12c - statements_8014
Source: https://docs.oracle.com/database/121/SQLRF/statements_8014.htm

Semantics

diskgroup\_name

Specify the name of the disk group you want to drop.

INCLUDING CONTENTS

Specify `INCLUDING` `CONTENTS` to confirm that Oracle ASM should drop all the files in the disk group. You must specify this clause if the disk group contains any files.

EXCLUDING CONTENTS

Specify `EXCLUDING` `CONTENTS` to ensure that Oracle ASM drops the disk group only when the disk group is empty. This is the default. If the disk group is not empty, then an error will be returned.

FORCE

This clause clears the headers on the disk belonging to a disk group that cannot be mounted by the Oracle ASM instance. The disk group cannot be mounted by any instance of the database.

The Oracle ASM instance first determines whether the disk group is being used by any other Oracle ASM instance using the same storage subsystem. If it is being used, and if the disk group is in the same cluster, or on the same node, then the statement fails. If the disk group is in a different cluster, then the system further checks to determine whether the disk group is mounted by any instance in the other cluster. If it is mounted elsewhere, then the statement fails. However, this latter check is not as definitive as the checks for disk groups in the same cluster. Therefore, use this clause with caution.

Examples

Dropping a Diskgroup: Example The following statement drops the Oracle ASM disk group `dgroup_01`, which was created in ["Creating a Diskgroup: Example"](statements_5009.md#CACIHAAD), and all of the files in the disk group:

```
DROP DISKGROUP dgroup_01 INCLUDING CONTENTS;
```