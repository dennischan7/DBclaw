---
source: PostgreSQL 15 Reference
title: 00_Overview
---

New probes can be defined within the code wherever the developer desires, though this will require a recompilation. Below are the steps for inserting new probes:

- 1. Decide on probe names and data to be made available through the probes
- 2. Add the probe definitions to src/backend/utils/probes.d
- 3. Include pg\_trace.h if it is not already present in the module(s) containing the probe points, and insert TRACE\_POSTGRESQL probe macros at the desired locations in the source code
- 4. Recompile and verify that the new probes are available

**Example:** Here is an example of how you would add a probe to trace all new transactions by transaction ID.

- 1. Decide that the probe will be named transaction-start and requires a parameter of type LocalTransactionId
- 2. Add the probe definition to src/backend/utils/probes.d:

```
probe transaction__start(LocalTransactionId);
```

Note the use of the double underline in the probe name. In a DTrace script using the probe, the double underline needs to be replaced with a hyphen, so transaction-start is the name to document for users.

3. At compile time, transaction\_\_start is converted to a macro called TRACE\_POST-GRESQL\_TRANSACTION\_START (notice the underscores are single here), which is available by including pg\_trace.h. Add the macro call to the appropriate location in the source code. In this case, it looks like the following:

```
TRACE_POSTGRESQL_TRANSACTION_START(vxid.localTransactionId);
```

4. After recompiling and running the new binary, check that your newly added probe is available by executing the following DTrace command. You should see similar output:

| # dtrace -ln transaction-start |          |                         |
|--------------------------------|----------|-------------------------|
| ID<br>PROVIDER                 | MODULE   | FUNCTION NAME           |
| 18705 postgresql49878          | postgres | StartTransactionCommand |
| transaction-start              |          |                         |
| 18755 postgresql49877          | postgres | StartTransactionCommand |
| transaction-start              |          |                         |
| 18805 postgresql49876          | postgres | StartTransactionCommand |
| transaction-start              |          |                         |
| 18855 postgresql49875          | postgres | StartTransactionCommand |
| transaction-start              |          |                         |
| 18986 postgresql49873          | postgres | StartTransactionCommand |
| transaction-start              |          |                         |

There are a few things to be careful about when adding trace macros to the C code:

- You should take care that the data types specified for a probe's parameters match the data types of the variables used in the macro. Otherwise, you will get compilation errors.
- On most platforms, if PostgreSQL is built with --enable-dtrace, the arguments to a trace macro will be evaluated whenever control passes through the macro, *even if no tracing is being done*. This is usually not worth worrying about if you are just reporting the values of a few local variables. But beware of putting expensive function calls into the arguments. If you need to do that, consider protecting the macro with a check to see if the trace is actually enabled:

```
if (TRACE_POSTGRESQL_TRANSACTION_START_ENABLED())
 TRACE_POSTGRESQL_TRANSACTION_START(some_function(...));
```

Each trace macro has a corresponding ENABLED macro.