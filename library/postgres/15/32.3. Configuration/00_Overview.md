---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The configuration variable jit determines whether JIT compilation is enabled or disabled. If it is enabled, the configuration variables jit\_above\_cost, jit\_inline\_above\_cost, and jit\_optimize\_above\_cost determine whether JIT compilation is performed for a query, and how much effort is spent doing so.

jit\_provider determines which JIT implementation is used. It is rarely required to be changed. See [Section 32.4.2.](#page-94-0)

For development and debugging purposes a few additional configuration parameters exist, as described in Section 20.17.