---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The pg\_upgrade module allows an installation to be migrated in-place from one major PostgreSQL version to another. Upgrades can be performed in minutes, particularly with --link mode. It requires steps similar to pg\_dumpall above, e.g., starting/stopping the server, running initdb. The pg\_upgrade documentation outlines the necessary steps.