---
source: PostgreSQL 14 Reference
title: 00_Overview
---

There are three separate approaches to pattern matching provided by PostgreSQL: the traditional SQL LIKE operator, the more recent SIMILAR TO operator (added in SQL:1999), and POSIX-style regular expressions. Aside from the basic "does this string match this pattern?" operators, functions are available to extract or replace matching substrings and to split a string at matching locations.

## **Tip**

If you have pattern matching needs that go beyond this, consider writing a user-defined function in Perl or Tcl.

### **Caution**

While most regular-expression searches can be executed very quickly, regular expressions can be contrived that take arbitrary amounts of time and memory to process. Be wary of accepting regular-expression search patterns from hostile sources. If you must do so, it is advisable to impose a statement timeout.

Searches using SIMILAR TO patterns have the same security hazards, since SIMILAR TO provides many of the same capabilities as POSIX-style regular expressions.

LIKE searches, being much simpler than the other two options, are safer to use with possibly-hostile pattern sources.

The pattern matching operators of all three kinds do not support nondeterministic collations. If required, apply a different collation to the expression to work around this limitation.