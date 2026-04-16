# Oracle 11g - statements_9016
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_9016.htm

Purpose

Use the `MERGE` statement to select rows from one or more sources for update or insertion into a table or view. You can specify conditions to determine whether to update or insert into the target table or view.

This statement is a convenient way to combine multiple operations. It lets you avoid multiple `INSERT`, `UPDATE`, and `DELETE` DML statements.

`MERGE` is a deterministic statement. You cannot update the same row of the target table multiple times in the same `MERGE` statement.

Note:

In previous releases of Oracle Database, when you created an Oracle Virtual Private Database policy on an application that included the

`MERGE` `INTO`

statement, the

`MERGE` `INTO`

statement would be prevented with an

`ORA-28132: Merge into syntax does not support security policies`

error, due to the presence of the Virtual Private Database policy. Beginning with Oracle Database 11

g

Release 2 (11.2.0.2), you can create policies on applications that include

`MERGE` `INTO`

operations. To do so, in the

`DBMS_RLS`

.

`ADD_POLICY` `statement_types`

parameter, include the

`INSERT`

,

`UPDATE`

, and

`DELETE`

statements, or just omit the

`statement_types`

parameter altogether. Refer to

[Oracle Database Security Guide](../../network.112/e36292/vpd.md#DBSEG249)

for more information on enforcing policies on specific SQL statement types.

Semantics

INTO Clause

Use the `INTO` clause to specify the target table or view you are updating or inserting into. In order to merge data into a view, the view must be updatable. Refer to ["Notes on Updatable Views"](statements_8004.md#CEGCADFA) for more information.

Restriction on Target Views You cannot specify a target view on which an `INSTEAD` `OF` trigger has been defined.

USING Clause

Use the `USING` clause to specify the source of the data to be updated or inserted. The source can be a table, view, or the result of a subquery.

ON Clause

Use the `ON` clause to specify the condition upon which the `MERGE` operation either updates or inserts. For each row in the target table for which the search condition is true, Oracle Database updates the row with corresponding data from the source table. If the condition is not true for any rows, then the database inserts into the target table based on the corresponding source table row.

Restrictions on the ON Clause 

In previous releases of Oracle Database, when you created an Oracle Virtual Private Database policy on an application that included the `MERGE` `INTO` statement, the `MERGE` `INTO` statement would be prevented with an `ORA-28132: Merge into syntax does not support security policies` error, due to the presence of the Virtual Private Database policy. Beginning with Oracle Database 11g Release 2 (11.2.0.2), you can create policies on applications that include `MERGE` `INTO` operations. To do so, in the `DBMS_RLS`.`ADD_POLICY` `statement_types` parameter, include the `INSERT`, `UPDATE`, and `DELETE` statements, or just omit the `statement_types` parameter altogether. Refer to [Oracle Database Security Guide](../../network.112/e36292/vpd.md#DBSEG249) for more information on enforcing policies on specific SQL statement types.

merge\_update\_clause

The `merge_update_clause` specifies the new column values of the target table. Oracle performs this update if the condition of the `ON` clause is true. If the update clause is executed, then all update triggers defined on the target table are activated.

Specify the `where_clause` if you want the database to execute the update operation only if the specified condition is true. The condition can refer to either the data source or the target table. If the condition is not true, then the database skips the update operation when merging the row into the table.

Specify the `DELETE` `where_clause` to clean up data in a table while populating or updating it. The only rows affected by this clause are those rows in the destination table that are updated by the merge operation. The `DELETE` `WHERE` condition evaluates the updated value, not the original value that was evaluated by the `UPDATE` `SET` ... `WHERE` condition. If a row of the destination table meets the `DELETE` condition but is not included in the join defined by the `ON` clause, then it is not deleted. Any delete triggers defined on the target table will be activated for each row deletion.

You can specify this clause by itself or with the `merge_insert_clause`. If you specify both, then they can be in either order.

Restrictions on the merge\_update\_clause This clause is subject to the following restrictions:

merge\_insert\_clause

The `merge_insert_clause` specifies values to insert into the column of the target table if the condition of the `ON` clause is false. If the insert clause is executed, then all insert triggers defined on the target table are activated. If you omit the column list after the `INSERT` keyword, then the number of columns in the target table must match the number of values in the `VALUES` clause.

To insert all of the source rows into the table, you can use a constant filter predicate in the `ON` clause condition. An example of a constant filter predicate is `ON` (`0=1`). Oracle Database recognizes such a predicate and makes an unconditional insert of all source rows into the table. This approach is different from omitting the `merge_update_clause`. In that case, the database still must perform a join. With constant filter predicate, no join is performed.

Specify the `where_clause` if you want Oracle Database to execute the insert operation only if the specified condition is true. The condition can refer only to the data source table. Oracle Database skips the insert operation for all rows for which the condition is not true.

You can specify this clause by itself or with the `merge_update_clause`. If you specify both, then they can be in either order.

Restriction on the merge\_insert\_clause You cannot specify `DEFAULT` when inserting into a view.

error\_logging\_clause

The error\_logging\_clause has the same behavior in a `MERGE` statement as in an `INSERT` statement. Refer to the `INSERT` statement [error\_logging\_clause](statements_9014.md#BGBEIACB) for more information.

Examples

Merging into a Table: Example The following example uses the `bonuses` table in the sample schema `oe` with a default bonus of 100. It then inserts into the `bonuses` table all employees who made sales, based on the `sales_rep_id` column of the `oe.orders` table. Finally, the human resources manager decides that employees with a salary of $8000 or less should receive a bonus. Those who have not made sales get a bonus of 1% of their salary. Those who already made sales get an increase in their bonus equal to 1% of their salary. The `MERGE` statement implements these changes in one step:

```
CREATE TABLE bonuses (employee_id NUMBER, bonus NUMBER DEFAULT 100);

INSERT INTO bonuses(employee_id)
   (SELECT e.employee_id FROM employees e, orders o
   WHERE e.employee_id = o.sales_rep_id
   GROUP BY e.employee_id); 

SELECT * FROM bonuses ORDER BY employee_id;

EMPLOYEE_ID      BONUS
----------- ----------
        153        100
        154        100
        155        100
        156        100
        158        100
        159        100
        160        100
        161        100
        163        100

MERGE INTO bonuses D
   USING (SELECT employee_id, salary, department_id FROM employees
   WHERE department_id = 80) S
   ON (D.employee_id = S.employee_id)
   WHEN MATCHED THEN UPDATE SET D.bonus = D.bonus + S.salary*.01
     DELETE WHERE (S.salary > 8000)
   WHEN NOT MATCHED THEN INSERT (D.employee_id, D.bonus)
     VALUES (S.employee_id, S.salary*.01)
     WHERE (S.salary <= 8000);

SELECT * FROM bonuses ORDER BY employee_id;

EMPLOYEE_ID      BONUS
----------- ----------
        153        180
        154        175
        155        170
        159        180
        160        175
        161        170
        164         72
        165         68
        166         64
        167         62
        171         74
        172         73
        173         61
        179         62
```