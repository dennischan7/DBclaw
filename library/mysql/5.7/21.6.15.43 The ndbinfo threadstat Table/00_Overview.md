---
source: MySQL 5.7 Reference
title: 00_Overview
---

The threadstat table provides a rough snapshot of statistics for threads running in the NDB kernel.

The threadstat table contains the following columns:

• node\_id

Node ID

• thr\_no

Thread ID

• thr\_nm

Thread name

• c\_loop

Number of loops in main loop

• c\_exec

Number of signals executed

• c\_wait

Number of times waiting for additional input

• c\_l\_sent\_prioa

Number of priority A signals sent to own node

• c\_l\_sent\_priob

Number of priority B signals sent to own node

• c\_r\_sent\_prioa

Number of priority A signals sent to remote node

• c\_r\_sent\_priob

Number of priority B signals sent to remote node

• os\_tid

OS thread ID

• os\_now

OS time (ms)

• os\_ru\_utime

OS user CPU time (µs)

• os\_ru\_stime

OS system CPU time (µs)

• os\_ru\_minflt

OS page reclaims (soft page faults)

• os\_ru\_majflt

OS page faults (hard page faults)

• os\_ru\_nvcsw

OS voluntary context switches

• os\_ru\_nivcsw

OS involuntary context switches

### **Notes**

os\_time uses the system gettimeofday() call.

The values of the os\_ru\_utime, os\_ru\_stime, os\_ru\_minflt, os\_ru\_majflt, os\_ru\_nvcsw, and os\_ru\_nivcsw columns are obtained using the system getrusage() call, or the equivalent.

Since this table contains counts taken at a given point in time, for best results it is necessary to query this table periodically and store the results in an intermediate table or tables. The MySQL Server's Event Scheduler can be employed to automate such monitoring. For more information, see Section 23.4, "Using the Event Scheduler".