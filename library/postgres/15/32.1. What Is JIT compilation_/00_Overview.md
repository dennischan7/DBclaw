---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Just-in-Time (JIT) compilation is the process of turning some form of interpreted program evaluation into a native program, and doing so at run time. For example, instead of using general-purpose code that can evaluate arbitrary SQL expressions to evaluate a particular SQL predicate like WHERE a.col = 3, it is possible to generate a function that is specific to that expression and can be natively executed by the CPU, yielding a speedup.

PostgreSQL has builtin support to perform JIT compilation using [LLVM](https://llvm.org/)<sup>1</sup> when PostgreSQL is built with --with-llvm.

See src/backend/jit/README for further details.