---
source: MySQL 8.4 Reference
title: 00_Overview
---

Anything written to the trace is automatically written to the debug file.

# <span id="page-75-0"></span>**10.15.8 The optimizer\_trace System Variable**

The optimizer\_trace system variable has these on/off switches:

- enabled: Enables (ON) or disables (OFF) tracing
- one\_line: If set to ON, the trace contains no whitespace, thus conserving space. This renders the trace difficult to read for humans, still usable by JSON parsers, since they ignore whitespace.

# <span id="page-75-2"></span>**10.15.9 The end\_markers\_in\_json System Variable**

When reading a very large JSON document, it can be difficult to pair its closing bracket and opening brackets; setting end\_markers\_in\_json=ON repeats the structure's key, if it has one, near the closing bracket. This variable affects both optimizer traces and the output of EXPLAIN FORMAT=JSON.

![](_page_75_Picture_14.jpeg)

#### **Note**

If end\_markers\_in\_json is enabled, the repetition of the key means the result is not a valid JSON document, and causes JSON parsers to throw an error.

# <span id="page-75-1"></span>**10.15.10 Selecting Optimizer Features to Trace**

Some features in the optimizer can be invoked many times during statement optimization and execution, and thus can make the trace grow beyond reason. They are:

- Greedy search: With an N-table join, this could explore factorial(N) plans.
- Range optimizer
- Dynamic range optimization: Shown as range checked for each record in EXPLAIN output; each outer row causes a re-run of the range optimizer.
- Subqueries: A subquery in which the WHERE clause may be executed once per row.

Those features can be excluded from tracing by setting one or more switches of the optimizer\_trace\_features system variable to OFF. These switches are listed here:

• greedy\_search: Greedy search is not traced.

- range\_optimizer: The range optimizer is not traced.
- dynamic\_range: Only the first call to the range optimizer on this JOIN\_TAB::SQL\_SELECT is traced.
- repeated\_subselect: Only the first execution of this Item\_subselect is traced.

### **10.15.11 Trace General Structure**

A trace follows the actual execution path very closely; for each join, there is a join preparation object, a join optimization object, and a join execution object. Query transformations (IN to EXISTS, outer join to inner join, and so on), simplifications (elimination of clauses), and equality propagation are shown in subobjects. Calls to the range optimizer, cost evaluations, reasons why an access path is chosen over another one, or why a sorting method is chosen over another one, are shown as well.