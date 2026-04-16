---
source: MySQL 8.0 Reference
title: 00_Overview
---

The arbitrator\_validity\_detail table shows the view that each data node in the cluster has of the arbitrator. It is a subset of the [membership](#page-172-0) table.

The arbitrator\_validity\_detail table contains the following columns:

• node\_id

This node's node ID

• arbitrator

Node ID of arbitrator

• arb\_ticket

Internal identifier used to track arbitration

• arb\_connected

Whether this node is connected to the arbitrator; either of Yes or No

• arb\_state

Arbitration state

### **Notes**

The node ID is the same as that reported by ndb\_mgm -e "SHOW".

All nodes should show the same arbitrator and arb\_ticket values as well as the same arb\_state value. Possible arb\_state values are ARBIT\_NULL, ARBIT\_INIT, ARBIT\_FIND, ARBIT\_PREP1, ARBIT\_PREP2, ARBIT\_START, ARBIT\_RUN, ARBIT\_CHOOSE, ARBIT\_CRASH, and UNKNOWN.

arb\_connected shows whether the current node is connected to the arbitrator.