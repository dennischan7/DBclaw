---
source: PostgreSQL 14 Reference
title: 00_Overview
---

WAL is automatically enabled; no action is required from the administrator except ensuring that the disk-space requirements for the WAL logs are met, and that any necessary tuning is done (see [Sec](#page-58-0)[tion 30.5\)](#page-58-0).

WAL records are appended to the WAL logs as each new record is written. The insert position is described by a Log Sequence Number (LSN) that is a byte offset into the logs, increasing monotonically with each new record. LSN values are returned as the datatype pg\_lsn. Values can be compared to calculate the volume of WAL data that separates them, so they are used to measure the progress of replication and recovery.

WAL logs are stored in the directory pg\_wal under the data directory, as a set of segment files, normally each 16 MB in size (but the size can be changed by altering the --wal-segsize initdb option). Each segment is divided into pages, normally 8 kB each (this size can be changed via the - with-wal-blocksize configure option). The log record headers are described in access/xlogrecord.h; the record content is dependent on the type of event that is being logged. Segment files are given ever-increasing numbers as names, starting at 000000010000000000000001. The numbers do not wrap, but it will take a very, very long time to exhaust the available stock of numbers.

It is advantageous if the log is located on a different disk from the main database files. This can be achieved by moving the pg\_wal directory to another location (while the server is shut down, of course) and creating a symbolic link from the original location in the main data directory to the new location.

The aim of WAL is to ensure that the log is written before database records are altered, but this can be subverted by disk drives that falsely report a successful write to the kernel, when in fact they have only cached the data and not yet stored it on the disk. A power failure in such a situation might lead to irrecoverable data corruption. Administrators should try to ensure that disks holding PostgreSQL's WAL log files do not make such false reports. (See [Section 30.1](#page-54-0).)

After a checkpoint has been made and the log flushed, the checkpoint's position is saved in the file pg\_control. Therefore, at the start of recovery, the server first reads pg\_control and then the checkpoint record; then it performs the REDO operation by scanning forward from the log location indicated in the checkpoint record. Because the entire content of data pages is saved in the log on the first page modification after a checkpoint (assuming full\_page\_writes is not disabled), all pages changed since the checkpoint will be restored to a consistent state.

To deal with the case where pg\_control is corrupt, we should support the possibility of scanning existing log segments in reverse order — newest to oldest — in order to find the latest checkpoint. This has not been implemented yet. pg\_control is small enough (less than one disk page) that it is not subject to partial-write problems, and as of this writing there have been no reports of database failures due solely to the inability to read pg\_control itself. So while it is theoretically a weak spot, pg\_control does not seem to be a problem in practice.