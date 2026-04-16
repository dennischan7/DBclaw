# Oracle 23c - value-expressions-graph_table
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/value-expressions-graph_table.html

Semantics

See [Aggregate Functions](Aggregate-Functions.md#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848) for the semantics of aggregate functions.

The arguments of the aggregate function together must reference exactly one group variable. In addition, they can reference any number of singleton variables. Note that an element variable is said to have group degree of reference when the variable is declared in a quantified path pattern while the reference occurs outside the quantified path pattern. On the other hand, if the reference does not cross a quantifier then the reference has singleton degree of reference. Singleton variables may be element pattern variables declared in the graph pattern or iterator variables declared in the Rows Clause. Also see Element Variable for more details on the contextual interpretation of graph element references.

The order in which values are aggregated in case of `LISTAGG`, `JSON_ARRAYAGG` and `XMLAGG` is non-deterministic unless an `ORDER BY` clause is specified. For example: `LISTAGG(edge1.property1 ORDER BY edge1.property1))`. There is currently no way to explicitly order by path order in such a way that elements are ordered in the same order as the vertices or edges in the path. However, when omitting the `ORDER BY` clause, the current implementation nevertheless implicitly orders by path order, but it should not be relied upon as this behavior may change over time.

Restrictions

* Only `WHERE` clauses that are not within a quantified pattern may contain aggregations. For example, the graph pattern `WHERE` clause as well as non-quantified element pattern `WHERE` clauses may contain aggregations, while parenthesized path pattern `WHERE` clauses may not contain aggregations since parenthesized path patterns currently have a restriction that they must always be quantified.
* The arguments of an aggregate function in `GRAPH_TABLE` together must reference exactly one group variable. In addition, they may reference any number of singleton variables. For example, `MATCH -[e1]-> WHERE SUM(e1.prop) > 10` is not allowed since variable `e1` has singleton degree of reference within the `SUM` aggregate, while `MATCH -[e2]->{1,10} WHERE SUM(e2.prop) > 10` and `MATCH -[e3]->{1,1} WHERE SUM(e3.prop) > 10` are allowed since variables `e2` and `e3` have group degree of reference within the `SUM` aggregates.
* Variable references must be inside property references, vertex or edge ID functions, or JSON dot-notation expressions. For example, `vertex_equal`, `edge_equal`, `IS SOURCE OF` and `IS DESTINATION OF` cannot be used in aggregate functions. For example, `COUNT(edge1)` is not allowed but `COUNT(edge_id(edge1))` and `COUNT(edge1.some_property))` are allowed.
* The arguments of an aggregate function in `GRAPH_TABLE` cannot reference anything other than a vertex or edge declared within the graph pattern of the `GRAPH_TABLE`. For example, it is not possible to reference a column that is passed from an outer query.
* In case of `LISTAGG`, `JSON_ARRAYAGG` and `XMLAGG` there is no way to specify that the order of elements in the result should be in the order of the vertices or edges in the path, although the current implement nevertheless implicitly orders by path order.

Examples

Example 1

The following query finds all paths that have a length between 2 and 5 edges (`{2,5}`), starting from a person named Alice and following both incoming and outgoing edges labeled friends. Edges along paths should not be traversed twice (`COUNT(edge_id(e) = COUNT(DISTINCT edge_id(e))`). The query returns all friendship IDs along paths as well as the length of each path.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (p IS person) -[e IS friends]-{2,5} (friend IS person)
       WHERE p.name = 'Alice' AND
             COUNT(edge_id(e)) = COUNT(DISTINCT edge_id(e))
       COLUMNS (LISTAGG(e.friendship_id, ', ') AS friendship_ids,
                COUNT(edge_id(e)) AS path_length))
ORDER BY path_length, friendship_ids;
```

Note that in the element pattern `WHERE` clause of the query above, p.name references a property of a single edge, while `edge_id(e)` within the `COUNT` aggregates accesses a list of element IDs since the edge variable e is enclosed by the quantifier `{2,5}`. Similarly, the two property references in the `COLUMNS` clause access a list of property values and edge ID values.

The result is:

```
FRIENDSHIP_IDS    PATH_LENGTH
----------------- -----------
2, 3              2
2, 4              2
2, 3, 1           3
2, 4, 1           3
2, 3, 1, 4        4
2, 4, 1, 3        4
```

Example 2

The following query finds all paths between university `ABC` and university `XYZ` such that paths have a length of up to 3 edges (`{,3}`). For each path, a JSON array is returned such that the array contains the `friendship_id` value for edges labeled friends, and the subject value for edges labeled `student_of`. Note that the `friendship_id` property is cast to `VARCHAR(100)` to make it type-compatible with the subject property.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (u1 IS university) -[e]-{,3} (u2 IS university)
       WHERE u1.name = 'ABC' AND u2.name = 'XYZ'
       COLUMNS (JSON_ARRAYAGG(CASE WHEN e.subject IS NOT NULL THEN e.subject
                              ELSE CAST(e.friendship_id AS VARCHAR(100)) END) AS path))
ORDER BY path;
The result is:
PATH
-----------------------
["Arts","3","Math"]
["Music","4","Math"]
```

Example 3

Example 3 The following query finds all paths that have a length between 2 and 3 edges (`{2,3}`), starting from a person named John and following only outgoing edges labeled friends and vertices labeled person. Vertices along paths should not have the same person\_id as John (`WHERE p.person_id <> friend.person_id`).

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (p IS person) ( -[e IS friends]-> (friend IS person)
                             WHERE p.person_id <> friend.person_id){2,3}
       WHERE p.name = 'John'
       COLUMNS (COUNT(edge_id(e)) AS path_length,
                LISTAGG(friend.name, ', ') AS names,
                LISTAGG(e.meeting_date, ', ') AS meeting_dates ))
ORDER BY path_length;
```

Above, the `COLUMNS` clause contains three aggregates, the first to compute the length of each path, the second to create a comma-separated list of person names along paths, and the third to create a comma-separate list of meeting dates along paths.

The result of the query is:

```
PATH_LENGTH NAMES               MEETING_DATES                                                      
----------- ------------------- -----------------------------------                                
          2 Bob, Mary           01-SEP-00, 10-JUL-01                                               
          3 Bob, Mary, Alice    01-SEP-00, 10-JUL-01, 19-SEP-00
```