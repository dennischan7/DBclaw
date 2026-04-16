# Oracle 23c - JSON_TRANSFORM
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/JSON_TRANSFORM.html

* Use `ADD_SET` to add missing value to an array, as if adding an element to a set.
* Use `APPEND` to append the values that are specified by the RHS to the array that is targeted by the LHS path expression.

  `APPEND` has the effect of `INSERT` for an array position of last+1.

  An error is raised if the LHS path expression targets an existing field whose value is not an array.

  If the RHS targets an array then the LHS array is updated by appending the elements of the RHS array to it, in order.
* Use `CASE` to set conditions to perform a sequence of `JSON_TRANSFORM` operations.

  This is a control operation that conditionally applies other operations, which in turn can modify data.

  The syntax is keyword `CASE` followed by one or more `WHEN` clauses, followed optionally by an `ELSE` clause, followed by `END`.

  A `WHEN` clause is keyword `WHEN` followed by a path expression, followed by a `THEN` clause.

  The path expression contains a filter condition, which checks for the existence of some data.

  A `THEN` or an `ELSE` clause is keyword `THEN` or `ELSE`, respectively, followed by parentheses (()) containing zero or more `JSON_TRANSFORM` operations.

  The operations of a `THEN` clause are performed if the condition of its `WHEN` clause is satisfied. The operations of the optional `ELSE` clause are performed if the condition of no `WHEN` clause is satisfied.

  The syntax of the `JSON_TRANSFORM` `CASE` operation is thus essentially the same as an Oracle SQL searched `CASE` expression, except that it is the predicate that is tested and the resulting effect of each `THEN`/`ELSE` branch.

  For SQL, the predicate tested is a SQL comparison. For `JSON_TRANSFORM`, the predicate is a path expression that checks for the existence of some data. (The check is essentially done using `JSON_EXISTS`.)

  For SQL, each `THEN`/`ELSE` branch holds a SQL expression to evaluate, and its value is returned as the result of the `CASE` expression. For json\_transform, each `THEN`/`ELSE` branch holds a (parenthesized) sequence of `JSON_TRANSFORM` operations, which are performed in order.

  The conditional path expressions of the `WHEN` clauses are tested in order, until one succeeds (those that follow are not tested). The `THEN` operations for the successful `WHEN` test are then performed, in order.
* Use `COPY` to replace the elements of the array that is targeted by the LHS path expression with the values that are specified by the RHS. An error is raised if the LHS path expression does not target an array. The operation can accept a sequence of multiple values matched by the RHS path expression.
* `INSERT` Insert the value of the specified SQL expression at the location that's targeted by the specified path expression that follows the equal sign (=), which must be either the field of an object or an array position (otherwise, an error is raised). By default, an error is raised if a targeted object field already exists.

  `INSERT` for an object field has the effect of `SET` with clause `CREATE ON MISSING` (default for `SET`), except that the default behavior for `ON EXISTING` is `ERROR`, not `REPLACE`.)

  You can specify an array position past the current end of an array. In that case, the array is lengthened to accommodate insertion of the value at the indicated position, and the intervening positions are filled with JSON null values.

  For example, if the input JSON data is `{"a":["b"]}` then `INSERT '$.a[3]'=42` returns `{"a":["b", null, null 42]}` as the modified data. The elements at array positions 1 and 2 are null.
* Use `INTERSECT` to remove all elements of the array that is targeted by the LHS path expression that are not equal to any value specified by the RHS. Remove any duplicate elements. Note that this is a set operation. The order of all array elements is undefined after the operation.
* Use `MERGE` to add specified fields (name and value) matched by the RHS path expression to the object that is targeted by the LHS path expression. Ignore any fields specified by the RHS that are already in the targeted LHS object. If the same field is specified more than once by the RHS then use only the last one in the sequence of matches.
* Use `MINUS` to remove all elements of the array that is targeted by the LHS path expression that are equal to a value specified by the RHS. Remove any duplicate elements. Note that this is a set operation. The order of all array elements is undefined after the operation.
* `KEEP` removes all parts of the input data that are not targeted by at least one of the specified path expressions. A topmost object or array is not removed, it is emptied and becomes an empty object ({}) or array ([]).
* Use `NESTED PATH` to define a scope (a particular part of your data) in which to apply a sequence of operations.
* Use `PREPEND` to prepend the values that are specified by the RHS to the array that is targeted by the LHS path expression. The operation can accept a sequence of multiple values matched by the RHS path expression.

  An error is raised if the LHS path expression targets an existing field whose value is not an array.

  When prepending a single value, `PREPEND` has the effect of `INSERT` for an array position of 0.

  If the RHS targets an array then the LHS array is updated by prepending the elements of the RHS array to it, in order.
* `REMOVE` Remove the input data that's targeted by the specified path expression. An error is raised if you try to remove all of the data, for example you cannot use `REMOVE '$'`. By default, no error is raised if the targeted data does not exist (`IGNORE ON MISSING`).
* Use `REMOVE_SET` to remove all occurrences of a value from an array, as if removing an element from a set.
* `RENAME` renames the field that is targeted by the specified path expression to the value of the SQL expression that follows the equal sign (=). By default, no error is raised if the targeted field does not exist (`IGNORE ON MISSING`).
* `REPLACE` replaces the data that's targeted by the specified path expression with the value of the specified SQL expression that follows the equal sign (=). By default, no error is raised if the targeted data does not exist (`IGNORE ON MISSING`).

  `REPLACE` has the effect of `SET` with clause `IGNORE ON MISSING`.
* `SET` Set what the LHS specifies to the value specified by what follows the equal sign (=). The LHS can be either a SQL/JSON variable or a path expression that targets data. If the RHS is a SQL expression then its value is assigned to the LHS variable. When the LHS specifies a path expression, the default behavior is to replace existing targeted data with the new value, or insert the new value at the targeted location if the path expression matches nothing. (See operator `INSERT` about inserting an array element past the end of the array.)
* When the LHS specifies a SQL/JSON variable, the variable is dynamically assigned to whatever is specified by the RHS. (The variable is created if it does not yet exist.) The variable continues to have that value until it is set to a different value by a subsequent `SET` operation (in the same `JSON_TRANSFORM` invocation).

  If the RHS is a path expression then its targeted data is assigned to the variable.

  Setting a variable is a control operation; it can affect how subsequent operations modify data, but it does not, itself, directly modify data.

  When the LHS specifies a path expression, the default behavior is like that of SQL `UPSERT`: replace existing targeted data with the new value, or insert the new value at the targeted location if the path expression matches nothing. (See operator `INSERT` about inserting an array element past the end of the array.)
* `SORT` sorts the elements of the array targeted by the specified path. The result includes all elements of the array (none are dropped); the only possible change is that they are reordered.
* Use `UNION` to add the values specified by the RHS to the array that is targeted by the LHS path expression. Remove any duplicate elements. The operation can accept a sequence of multiple values matched by the RHS path expression. Note that this is a set operation. The order of all array elements is undefined after the operation.