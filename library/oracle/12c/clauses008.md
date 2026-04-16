# Oracle 12c - clauses008
Source: https://docs.oracle.com/database/121/SQLRF/clauses008.htm

[Go to main content](#BEGIN)

354/555 

# size\_clause

Purpose

The `size_clause` lets you specify a number of bytes, kilobytes (K), megabytes (M), gigabytes (G), terabytes (T), petabytes (P), or exabytes (E) in any statement that lets you establish amounts of disk or memory space.

Semantics

Use the `size_clause` to specify a number or multiple of bytes. If you do not specify any of the multiple abbreviations, then the `integer` is interpreted as bytes.

Note:

Not all multiples of bytes are appropriate in all cases, and context-sensitive limitations may apply. In the latter case, Oracle issues an error message.

Scripting on this page enhances content navigation, but does not change the content in any way.