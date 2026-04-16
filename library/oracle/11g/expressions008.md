# Oracle 11g - expressions008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/expressions008.htm

# Function Expressions

You can use any built-in SQL function or user-defined function as an expression. Some valid built-in function expressions are:

```
LENGTH('BLAKE') 
ROUND(1234.567*43) 
SYSDATE
```

A user-defined function expression specifies a call to:

Some valid user-defined function expressions are:

```
circle_area(radius)
payroll.tax_rate(empno)
hr.employees.comm_pct@remote(dependents, empno)
DBMS_LOB.getlength(column_name)
my_function(a_column)
```

In a user-defined function being used as an expression, positional, named, and mixed notation are supported. For example, all of the following notations are correct:

```
CALL my_function(arg1 => 3, arg2 => 4) ...
```

```
CALL my_function(3, 4) ...

CALL my_function(3, arg2 => 4) ...
```

Restriction on User-Defined Function Expressions You cannot pass arguments of object type or `XMLType` to remote functions and procedures.