---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Custom server settings to use when running a regression test suite can be set in the PGOPTIONS environment variable (for settings that allow this):

```
make check PGOPTIONS="-c force_parallel_mode=regress -c
 work_mem=50MB"
```

When running against a temporary installation, custom settings can also be set by supplying a prewritten postgresql.conf:

```
echo 'log_checkpoints = on' > test_postgresql.conf
echo 'work_mem = 50MB' >> test_postgresql.conf
make check EXTRA_REGRESS_OPTS="--temp-config=test_postgresql.conf"
```

This can be useful to enable additional logging, adjust resource limits, or enable extra run-time checks such as debug\_discard\_caches.