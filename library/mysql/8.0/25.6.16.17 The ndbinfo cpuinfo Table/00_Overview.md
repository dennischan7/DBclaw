---
source: MySQL 8.0 Reference
title: 00_Overview
---

The cpuinfo table provides information about the CPU on which a given data node executes.

The cpuinfo table contains the following columns:

• node\_id

Node ID

• cpu\_no

CPU ID

• cpu\_online

1 if the CPU is online, otherwise 0

• core\_id

CPU core ID

• socket\_id

CPU socket ID

# **Notes**

The cpuinfo table is available on all operating systems supported by NDB, with the exception of MacOS and FreeBSD.

This table was added in NDB 8.0.23.

# <span id="page-147-0"></span>**25.6.16.18 The ndbinfo cpustat Table**

The cpustat table provides per-thread CPU statistics gathered each second, for each thread running in the NDB kernel.

The cpustat table contains the following columns:

• node\_id

ID of the node where the thread is running

• thr\_no

Thread ID (specific to this node)

• OS\_user

OS user time

• OS\_system

### OS system time

• OS\_idle

OS idle time

• thread\_exec

Thread execution time

• thread\_sleeping

Thread sleep time

• thread\_spinning

Thread spin time

• thread\_send

Thread send time

• thread\_buffer\_full

Thread buffer full time

• elapsed\_time

Elapsed time

# <span id="page-148-0"></span>**25.6.16.19 The ndbinfo cpustat\_50ms Table**

The cpustat\_50ms table provides raw, per-thread CPU data obtained each 50 milliseconds for each thread running in the NDB kernel.

Like [cpustat\\_1sec](#page-149-0) and [cpustat\\_20sec](#page-150-0), this table shows 20 measurement sets per thread, each referencing a period of the named duration. Thus, cpsustat\_50ms provides 1 second of history.

The cpustat\_50ms table contains the following columns:

• node\_id

ID of the node where the thread is running

• thr\_no

Thread ID (specific to this node)

• OS\_user\_time

OS user time

• OS\_system\_time

OS system time

• OS\_idle\_time

OS idle time

• exec\_time

Thread execution time

• sleep\_time

Thread sleep time

• spin\_time

Thread spin time

• send\_time

Thread send time

• buffer\_full\_time

Thread buffer full time

• elapsed\_time

Elapsed time

# <span id="page-149-0"></span>**25.6.16.20 The ndbinfo cpustat\_1sec Table**

The cpustat-1sec table provides raw, per-thread CPU data obtained each second for each thread running in the NDB kernel.

Like [cpustat\\_50ms](#page-148-0) and [cpustat\\_20sec](#page-150-0), this table shows 20 measurement sets per thread, each referencing a period of the named duration. Thus, cpsustat\_1sec provides 20 seconds of history.

The cpustat\_1sec table contains the following columns:

• node\_id

ID of the node where the thread is running

• thr\_no

Thread ID (specific to this node)

• OS\_user\_time

OS user time

• OS\_system\_time

OS system time

• OS\_idle\_time

OS idle time

• exec\_time

Thread execution time

• sleep\_time

Thread sleep time

• spin\_time

Thread spin time

• send\_time

### Thread send time

• buffer\_full\_time

Thread buffer full time

• elapsed\_time

Elapsed time

# <span id="page-150-0"></span>**25.6.16.21 The ndbinfo cpustat\_20sec Table**

The cpustat\_20sec table provides raw, per-thread CPU data obtained each 20 seconds, for each thread running in the NDB kernel.

Like [cpustat\\_50ms](#page-148-0) and [cpustat\\_1sec](#page-149-0), this table shows 20 measurement sets per thread, each referencing a period of the named duration. Thus, cpsustat\_20sec provides 400 seconds of history.

The cpustat\_20sec table contains the following columns:

• node\_id

ID of the node where the thread is running

• thr\_no

Thread ID (specific to this node)

• OS\_user\_time

OS user time

• OS\_system\_time

OS system time

• OS\_idle\_time

OS idle time

• exec\_time

Thread execution time

• sleep\_time

Thread sleep time

• spin\_time

Thread spin time

• send\_time

Thread send time

• buffer\_full\_time

Thread buffer full time

• elapsed\_time

Elapsed time