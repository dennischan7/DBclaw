# Oracle 11g - pseudocolumns
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/pseudocolumns.htm

[Go to main content](#BEGIN)

11/522

# 2 Pseudocolumns

A pseudocolumn behaves like a table column, but is not actually stored in the table. You can select from pseudocolumns, but you cannot insert, update, or delete their values. A pseudocolumn is also similar to a function without arguments (refer to [Chapter 5, "Functions"](functions.md#g1593736)). However, functions without arguments typically return the same value for every row in the result set, whereas pseudocolumns typically return a different value for each row.

This chapter contains the following sections:

Scripting on this page enhances content navigation, but does not change the content in any way.