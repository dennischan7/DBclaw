# Oracle 11g - expressions012
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/expressions012.htm

[Go to main content](#BEGIN)

309/522 

# Placeholder Expressions

A placeholder expression provides a location in a SQL statement for which a third-generation language bind variable will provide a value. You can specify the placeholder expression with an optional indicator variable. This form of expression can appear only in embedded SQL statements or SQL statements processed in an Oracle Call Interface (OCI) program.

placeholder\_expression::=

Some valid placeholder expressions are:

```
:employee_name INDICATOR :employee_name_indicator_var
:department_location
```

Scripting on this page enhances content navigation, but does not change the content in any way.