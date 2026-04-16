---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL Group Replication builds on an implementation of the Paxos distributed algorithm to provide distributed coordination between servers. As such, it requires a majority of servers to be active to reach quorum and thus make a decision. This has direct impact on the number of failures the system can tolerate without compromising itself and its overall functionality. The number of servers (n) needed to tolerate f failures is then n = 2 x f + 1.

In practice this means that to tolerate one failure the group must have three servers in it. As such if one server fails, there are still two servers to form a majority (two out of three) and allow the system to continue to make decisions automatically and progress. However, if a second server fails involuntarily, then the group (with one server left) blocks, because there is no majority to reach a decision.

The following is a small table illustrating the formula above.

| Group Size | Majority | Instant Failures Tolerated |
|------------|----------|----------------------------|
| 1          | 1        | 0                          |
| 2          | 2        | 0                          |
| 3          | 2        | 1                          |
| 4          | 3        | 1                          |
| 5          | 3        | 2                          |
| 6          | 4        | 2                          |
| 7          | 4        | 3                          |