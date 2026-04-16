# Oracle 23c - graph-table-shape
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/graph-table-shape.html

Examples

Example 1

The following query finds all friends path with length between 0 and 3 starting from a person named John. It outputs one row per vertex.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (n IS person) -[e1 IS friends]->{0,3} (IS person)
       WHERE n.name = 'John'
       ONE ROW PER VERTEX (v)
       COLUMNS (
        LISTAGG(e1.friendship_id, ', ') AS friendship_ids,
        v.name)
     );
```

The results are:

```
FRIENDSHIP_IDS       NAME
-------------------- ---------------
                     John
1                    John
1                    Bob
1, 4                 John
1, 4                 Bob
1, 4                 Mary
1, 4, 3              John
1, 4, 3              Bob
1, 4, 3              Mary
1, 4, 3              John
1, 4, 2              John
1, 4, 2              Bob
1, 4, 2              Mary
1, 4, 2              Alice
```

The results above show data from five paths that were matched:

* The empty path (zero `friendship_ids`) contains a single person named John.
* The path with `friendship_ids` 1 contains two persons named John and Bob.
* The path with `friendship_ids` 1, 4 contains three persons named John, Bob and Mary.
* The path with `friendship_ids` 1, 4, 3 contains four persons named John, Bob, Mary and John (this is a cycle).
* The path with `friendship_ids` 1, 4, 2 contains four persons named John, Bob, Mary and Alice.

Example 2

The following query again finds all friends path with length between 0 and 3 starting from a person named John. This time it outputs one row per step.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (n IS person) -[e1 IS friends]->{0,3} (IS person)
       WHERE n.name = 'John'
       ONE ROW PER STEP (src, e2, dst)
       COLUMNS (
         LISTAGG(e1.friendship_id, ', ') AS friendship_ids,
         src.name AS src_name,
         e2.friendship_id,
         dst.name AS dst_name)
     );
```

The results are:

```
FRIENDSHIP_IDS       SRC_NAME   FRIENDSHIP_ID DST_NAME
-------------------- ---------- ------------- ----------
                     John
1                    John       1             Bob
1, 4                 John       1             Bob
1, 4                 Bob        4             Mary
1, 4, 3              John       1             Bob
1, 4, 3              Bob        4             Mary
1, 4, 3              Mary       3             John
1, 4, 2              John       1             Bob
1, 4, 2              Bob        4             Mary
1, 4, 2              Mary       2             Alice
```

The results above show data from five paths that were matched:

* The empty path (no `friendship_ids`) has a single step in which iterator vertex variable `src` is bound to the vertex corresponding to the person named John, while iterator edge variable `e2` and iterator vertex variable dst are not bound, resulting in NULL values for `FRIENDSHIP_ID` and `DST_NAME`.
* The path with `friendship_ids` 1 has a single step since it has a single edge. In this step, iterator vertex variable `src` is bound to the vertex corresponding to John, iterator edge variable `e2` is bound to the edge with `friendship_ids` 1, and iterator vertex variable `dst` is bound to the vertex corresponding to Bob.
* The path with `friendship_ids` 1, 4 has two steps since it has two edges.
* The path with `friendship_ids` 1, 4, 3 has three steps since it has three edges.
* The path with `friendship_ids` 1, 4, 2 again has three steps since it has three edges.

Example 3

The following query matches paths between universities ABC and XYZ such that paths consist of an incoming student\_of edge, followed by one or two friends edges, followed by an outgoing student\_of edge. The query returns one row per vertex and for each row it returns the match number, the element number, the type of the vertex (either person or university), as well as the name of the university or the person.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH (u1 IS university)
               <-[IS student_of]- (p1 IS person)
               -[IS friends]-{1,2} (p2 IS person)
               -[IS student_of]-> (u2 IS university)
       WHERE u1.name = 'ABC' AND u2.name = 'XYZ'
       ONE ROW PER VERTEX (v)
       COLUMNS (MATCHNUM() AS matchnum,
                ELEMENT_NUMBER(v) AS element_number,
                CASE WHEN v.person_id IS NOT NULL
                  THEN 'person'
                  ELSE 'university'
                  END AS label,
                v.name))
ORDER BY matchnum, element_number;
```

The results are:

```
MATCHNUM ELEMENT_NUMBER        LABEL       NAME
---------- -------------- ---------- ----------
         1              1 university         ABC
         1              3 person             John
         1              5 person             Mary
         1              7 university         XYZ
         2              1 university         ABC
         2              3 person             Bob
         2              5 person             John
         2              7 person             Mary
         2              9 university         XYZ
         3              1 university         ABC
         3              3 person             Bob
         3              5 person             Mary
         3              7 university         XYZ
         4              1 university         ABC
         4              3 person             John
         4              5 person             Mary
         4              7 person             Alice
         4              9 university         XYZ
         6              1 university         ABC
         6              3 person             John
         6              5 person             Bob
         6              7 person             Mary
         6              9 university         XYZ
         8              1 university         ABC
         8              3 person             Bob
         8              5 person             Mary
         8              7 person             Alice
         8              9 university         XYZ
```

Note that a total of 6 paths were matched with match numbers `1`, `2`, `3`, `4`, `6` and `8`. Each path has university `ABC` as the first vertex and university `XYZ` as the last vertex. Furthermore, paths with match numbers `1` and `3` contain two person vertices while the other paths (match numbers `2`, `4`, `6` and `8`) contain three person vertices.

Example 4

Like in Example 3, the following query matches paths between universities `ABC` and `XYZ`. In Example 4, the graph pattern is split into three path patterns. The first path pattern matches an incoming `student_of edge`, the second path pattern matches one or two friends' edges, and the third path pattern matches again a `student_of edge`. The query returns one row per vertex in the second path. This path contains only person vertices. For each vertex, the query returns the match number, the path name, the element number, and all the vertex properties.

```
SELECT *
FROM GRAPH_TABLE ( students_graph
       MATCH path1 = (u1 IS university) <-[IS student_of]- (p1 IS person),
             path2 = (p1) -[IS friends]-{1,2} (p2 IS person),
             path3 = (p2) -[IS student_of]-> (u2 IS university)
       WHERE u1.name = 'ABC' AND u2.name = 'XYZ'
       ONE ROW PER VERTEX (v) IN (path2)
       COLUMNS (MATCHNUM() AS matchnum,
                PATH_NAME() AS path_name,
                ELEMENT_NUMBER(v) AS element_number,
                v.*))
ORDER BY matchnum, element_number;
The results are:
MATCHNUM PATH_NAME ELEMENT_NUMBER PERSON_ID NAME  DOB       HEIGHT    ID
-------- --------- -------------- --------- ----- --------- --------- --
       1 PATH2                  1         1 John  13-JUN-63       1.8
       1 PATH2                  3         2 Mary  25-SEP-82      1.65
       2 PATH2                  1         3 Bob   11-MAR-66      1.75
       2 PATH2                  3         1 John  13-JUN-63       1.8
       2 PATH2                  5         2 Mary  25-SEP-82      1.65
       3 PATH2                  1         3 Bob   11-MAR-66      1.75
       3 PATH2                  3         2 Mary  25-SEP-82      1.65
       4 PATH2                  1         1 John  13-JUN-63       1.8
       4 PATH2                  3         2 Mary  25-SEP-82      1.65
       4 PATH2                  5         4 Alice 01-FEB-87       1.7
       6 PATH2                  1         1 John  13-JUN-63       1.8
       6 PATH2                  3         3 Bob   11-MAR-66      1.75
       6 PATH2                  5         2 Mary  25-SEP-82      1.65
       8 PATH2                  1         3 Bob   11-MAR-66      1.75
       8 PATH2                  3         2 Mary  25-SEP-82      1.65
       8 PATH2                  5         4 Alice 01-FEB-87       1.7
```

Like in Example 3, a total of 6 paths were matched with match numbers `1`, `2`, `3`, `4`, `6` and `8`. Paths with match numbers `1` and `3` contain two person vertices while the other paths (match numbers `2`, `4`, `6` and `8`) contain three person vertices. The all properties reference `v.*` expands to properties `PERSON_ID`, `NAME`, `DOB`, `HEIGHT` and `ID`. Thus, even though person vertices do not have property ID (only university vertices do), the expansion still includes property ID because an all properties reference with an iterator variable always expands to either all vertex properties or all edge properties in the graph based on the iterator variable type.