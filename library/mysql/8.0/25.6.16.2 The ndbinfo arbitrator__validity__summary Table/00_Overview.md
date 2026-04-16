---
source: MySQL 8.0 Reference
title: 00_Overview
---

The arbitrator\_validity\_summary table provides a composite view of the arbitrator with regard to the cluster's data nodes.

The arbitrator\_validity\_summary table contains the following columns:

• arbitrator

### Node ID of arbitrator

• arb\_ticket

Internal identifier used to track arbitration

• arb\_connected

Whether this arbitrator is connected to the cluster

• consensus\_count

Number of data nodes that see this node as arbitrator; either of Yes or No

### **Notes**

In normal operations, this table should have only 1 row for any appreciable length of time. If it has more than 1 row for longer than a few moments, then either not all nodes are connected to the arbitrator, or all nodes are connected, but do not agree on the same arbitrator.

The arbitrator column shows the arbitrator's node ID.

arb\_ticket is the internal identifier used by this arbitrator.

arb\_connected shows whether this node is connected to the cluster as an arbitrator.