# Oracle 23c - graph-pattern
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/graph-pattern.html

Semantics

Syntactically, an `element_variable_declaration` is an identifier and can thus be either double quoted or unquoted. Declaring an element variable is optional and if no element variable is declared then the element pattern has an implicit variable with an (implicit) unique name. Implicit variables cannot be referenced elsewhere in the query.

Multiple vertex patterns may declare the same element variable and multiple edge patterns may also declare the same element variable. In such cases, there are not multiple variables but there is a single variable that is shared by the different vertex or edge patterns.

Declared variables are visible within the `GRAPH_TABLE` in which they are declared. They may be referenced in `WHERE` and `COLUMNS` clauses defined in the same `GRAPH_TABLE`.

If an element variable is declared in a quantified path pattern, then it may bind to more than one vertex or edge within a single solution to the pattern. References are interpreted contextually: if the reference occurs outside the quantified path pattern, then the reference is to the complete list of graph elements that are bound to the element variable. In this circumstance, the element variable is said to have group degree of reference. However, if the reference does not cross a quantifier, then the reference has singleton degree of reference.

For example, in `(X) -[E WHERE E.P > 1]->{1,10} (Y) WHERE SUM(E.P) < 100` the edge variable `E` is referenced twice: once in the edge pattern and once outside the edge pattern. Within the edge pattern, `E` has singleton degree of reference and the property reference `E`.`P` references a property of a single edge. On the other hand, the reference within the `SUM` aggregate has group degree of reference (because of the quantifier `{1,10}`) and references the list of edges that are bound to `E`.

Examples

Example 1

The following query finds friends of friends of John following incoming or outgoing edges that have a property `meeting_date` with a value greater than `DATE '2000-09-015'`:

```
SELECT DISTINCT name
FROM GRAPH_TABLE ( students_graph
  MATCH (a IS person) -[e IS friends WHERE e.meeting_date > DATE '2000-09-15']-{2} ("b" IS person)
  WHERE a.name = 'John' AND a.name <> "b".name
  COLUMNS ("b".name)
);
```

In the query above, `a` and `"b"` are vertex variables, `e` is an edge variable and `e.meeting_date`, `a.name` and `"b".name` are property references that access a property value of the referenced vertex or edge.

The result shows that John has two such friends of friends:

```
NAME
----------
Bob
Alice
```

Example 2

The following query finds friends of Mary and the universities that Mary and her friends went to:

```
SELECT *
FROM GRAPH_TABLE ( students_graph
  MATCH (p1 IS person) -[e1 IS friends]- (p2 IS person)
      , (p1) -[IS student_of]-> (u1 IS university)
      , (p2) -[IS student_of]-> (u2 IS university)
  WHERE p1.name = 'Mary'
  COLUMNS (p1.name, p2.name AS friend, e1.meeting_date, u1.name AS univ_1, u2.name AS univ_2)
);
```

In the query above, `p1`, `p2`, `u1` and `u2` are vertex variables, while `e1` is an edge variable. The pattern `-[IS student_of]->` appears twice and implicitly declares two unique variables that cannot be referenced. Furthermore, there are two vertex patterns that share variable `p1` and there are two vertex patterns that share variable `p2`. Vertices will only bind to such variable if both vertex patterns match.

The result shows that Mary has three friends, one of which goes to the same university `XYZ`, while two other friends go to a different university `ABC`:

```
NAME       FRIEND     MEETING_D UNIV_1     UNIV_2
---------- ---------- --------- ---------- ----------
Mary       John       19-SEP-00 XYZ        ABC
Mary       Bob        10-JUL-01 XYZ        ABC
Mary       Alice      19-SEP-00 XYZ        XYZ
```

Example 3

The following query finds all paths that have a length between 2 and 5 edges (`{2,5}`), starting from a person named Alice and following both incoming and outgoing edges labeled `friends`. Edges along paths should not be traversed twice (`COUNT(e.friendship_id`) = `COUNT(DISTINCT e.friendship_id`)). The query returns all friendship IDs along paths as well as the length of each path.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (p IS person) -[e IS friends]-{2,5} (friend IS person)
       WHERE p.name = 'Alice' AND
             COUNT(e.friendship_id) = COUNT(DISTINCT e.friendship_id)
       COLUMNS (LISTAGG(e.friendship_id, ', ') AS friendship_ids,
                COUNT(e.friendship_id) AS path_length));
```

Note that in the element pattern `WHERE` clause of the query above, `p.name` references a property of a single edge, while `e.friendship_id` within the `COUNT` aggregate accesses a list of property values since the edge variable `e` is enclosed by the quantifier `{2,5}`. Similarly, the two property references in the `COLUMNS` clause both access a list of property values.

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