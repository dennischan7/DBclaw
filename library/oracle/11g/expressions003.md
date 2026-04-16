# Oracle 11g - expressions003
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/expressions003.htm

[Go to main content](#BEGIN)

300/522 

# Compound Expressions

A compound expression specifies a combination of other expressions.

compound\_expression::=

You can use any built-in function as an expression (["Function Expressions"](expressions008.md#i1033636)). However, in a compound expression, some combinations of functions are inappropriate and are rejected. For example, the `LENGTH` function is inappropriate within an aggregate function.

The `PRIOR` operator is used in `CONNECT` `BY` clauses of hierarchical queries.

Some valid compound expressions are:

```
('CLARK' || 'SMITH') 
LENGTH('MOOSE') * 57 
SQRT(144) + 72 
my_fun(TO_CHAR(sysdate,'DD-MMM-YY'))
```

Scripting on this page enhances content navigation, but does not change the content in any way.