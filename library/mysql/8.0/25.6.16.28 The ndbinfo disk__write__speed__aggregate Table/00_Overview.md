---
source: MySQL 8.0 Reference
title: 00_Overview
---

The disk\_write\_speed\_aggregate table provides aggregated information about the speed of disk writes during LCP, backup, and restore operations.

The disk\_write\_speed\_aggregate table contains the following columns:

• node\_id

Node ID of this node

• thr\_no

Thread ID of this LDM thread

• backup\_lcp\_speed\_last\_sec

Number of bytes written to disk by backup and LCP processes in the last second

• redo\_speed\_last\_sec

Number of bytes written to REDO log in the last second

• backup\_lcp\_speed\_last\_10sec

Number of bytes written to disk by backup and LCP processes per second, averaged over the last 10 seconds

• redo\_speed\_last\_10sec

Number of bytes written to REDO log per second, averaged over the last 10 seconds

• std\_dev\_backup\_lcp\_speed\_last\_10sec

Standard deviation in number of bytes written to disk by backup and LCP processes per second, averaged over the last 10 seconds

• std\_dev\_redo\_speed\_last\_10sec

Standard deviation in number of bytes written to REDO log per second, averaged over the last 10 seconds

• backup\_lcp\_speed\_last\_60sec

Number of bytes written to disk by backup and LCP processes per second, averaged over the last 60 seconds

• redo\_speed\_last\_60sec

Number of bytes written to REDO log per second, averaged over the last 10 seconds

• std\_dev\_backup\_lcp\_speed\_last\_60sec

Standard deviation in number of bytes written to disk by backup and LCP processes per second, averaged over the last 60 seconds

• std\_dev\_redo\_speed\_last\_60sec

Standard deviation in number of bytes written to REDO log per second, averaged over the last 60 seconds

• slowdowns\_due\_to\_io\_lag

Number of seconds since last node start that disk writes were slowed due to REDO log I/O lag

• slowdowns\_due\_to\_high\_cpu

Number of seconds since last node start that disk writes were slowed due to high CPU usage

• disk\_write\_speed\_set\_to\_min

Number of seconds since last node start that disk write speed was set to minimum

• current\_target\_disk\_write\_speed

Actual speed of disk writes per LDM thread (aggregated)