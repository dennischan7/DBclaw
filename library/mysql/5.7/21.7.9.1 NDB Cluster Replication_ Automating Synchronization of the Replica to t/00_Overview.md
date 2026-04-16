---
source: MySQL 5.7 Reference
title: 00_Overview
---

It is possible to automate much of the process described in the previous section (see [Section 21.7.9,](#page-128-0) ["NDB Cluster Backups With NDB Cluster Replication"\)](#page-128-0). The following Perl script reset-replica.pl serves as an example of how you can do this.

```
#!/user/bin/perl -w
# file: reset-replica.pl
# Copyright (c) 2005, 2020, Oracle and/or its affiliates. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to:
# Free Software Foundation, Inc.