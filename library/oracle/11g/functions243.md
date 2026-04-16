# Oracle 11g - functions243
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions243.htm

[Go to main content](#BEGIN)

283/522 

# XMLEXISTS

Syntax

XML\_passing\_clause::=

Purpose

`XMLExists` checks whether a given XQuery expression returns a nonempty XQuery sequence. If so, the function returns `TRUE`; otherwise, it returns `FALSE`. The argument `XQuery_string` is a literal string, but it can contain XQuery variables that you bind using the `XML_passing_clause`.

The `expr` in the `XML_passing_clause` is an expression returning an `XMLType` or an instance of a SQL scalar data type that is used as the context for evaluating the XQuery expression. You can specify only one `expr` in the `PASSING` clause without an identifier. The result of evaluating each `expr` is bound to the corresponding identifier in the `XQuery_string`. If any `expr` that is not followed by an `AS` clause, then the result of evaluating that expression is used as the context item for evaluating the `XQuery_string`.

Scripting on this page enhances content navigation, but does not change the content in any way.