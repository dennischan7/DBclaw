# Oracle 12c - statements_6005
Source: https://docs.oracle.com/database/121/SQLRF/statements_6005.htm

Semantics

OR REPLACE

Specify `OR` `REPLACE` to replace the definition of the operator schema object.

Restriction on Replacing an Operator You can replace the definition only if the operator has no dependent objects, such as indextypes supporting the operator.

schema

Specify the schema containing the operator. If you omit `schema`, then the database creates the operator in your own schema.

operator

Specify the name of the operator to be created. The name must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570).

binding\_clause

Use the `binding_clause` to specify one or more parameter data types (`parameter_type`) for binding the operator to a function. The signature of each binding—the sequence of the data types of the arguments to the corresponding function—must be unique according to the rules of overloading.

The `parameter_type` can itself be an object type. If it is, then you can optionally qualify it with its schema.

Restriction on Binding Operators You cannot specify a `parameter_type` of `REF`, `LONG`, or `LONG` `RAW`.

RETURN Clause

Specify the return data type for the binding.

The `return_type` can itself be an object type. If so, then you can optionally qualify it with its schema.

Restriction on Binding Return Data Type You cannot specify a `return_type` of `REF`, `LONG`, or `LONG` `RAW`.

implementation\_clause

Use this clause to describe the implementation of the binding.

ANCILLARY TO Clause

Use the `ANCILLARY` `TO` clause to indicate that the operator binding is ancillary to the specified primary operator binding (`primary_operator`). If you specify this clause, then do not specify a previous binding with just one number parameter.

context\_clause

Use the `context_clause` to describe the functional implementation of a binding that is not ancillary to a primary operator binding.

WITH INDEX CONTEXT, SCAN CONTEXT Use this clause to indicate that the functional evaluation of the operator uses the index and a scan context that is specified by the implementation type.

COMPUTE ANCILLARY DATA Specify `COMPUTE` `ANCILLARY` `DATA` to indicate that the operator binding computes ancillary data.

WITH COLUMN CONTEXT Specify `WITH` `COLUMN` `CONTEXT` to indicate that Oracle Database should pass the column information to the functional implementation for the operator.

If you specify this clause, then the signature of the function implemented must include one extra `ODCIFuncCallInfo` structure.

using\_function\_clause

The `using_function_clause` lets you specify the function that provides the implementation for the binding. The `function_name` can be a standalone function, packaged function, type method, or a synonym for any of these.

If the function is subsequently dropped, then the database marks all dependent objects `INVALID`, including the operator. However, if you then subsequently issue an `ALTER` `OPERATOR` ... `DROP` `BINDING` statement to drop the binding, then subsequent queries and DML will revalidate the dependent objects.