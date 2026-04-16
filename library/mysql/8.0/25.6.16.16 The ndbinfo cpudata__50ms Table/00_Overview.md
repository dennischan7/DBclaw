---
source: MySQL 8.0 Reference
title: 00_Overview
---

The cpudata\_50ms table provides data about CPU usage per 50-millisecond interval over the last second.

The cpustat table contains the following columns:

• node\_id

Node ID

• measurement\_id

Measurement sequence ID; later measurements have lower IDs

• cpu\_no

CPU ID

• cpu\_online

1 if the CPU is currently online, otherwise 0

• cpu\_userspace\_time

CPU time spent in userspace

• cpu\_idle\_time

CPU time spent idle

• cpu\_system\_time

CPU time spent in system time

• cpu\_interrupt\_time

CPU time spent handling interrupts (hardware and software)

• cpu\_exec\_vm\_time

CPU time spent in virtual machine execution

• elapsed\_time

Time in microseconds used for this measurement

### **Notes**

The cpudata\_50ms table is available only on Linux and Solaris operating systems.

This table was added in NDB 8.0.23.