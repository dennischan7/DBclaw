# Oracle 23c - graph-reference
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/graph-reference.html

Prerequisites

To query a property graph, you must have `READ` or `SELECT` object privilege on the graph. Note that you do not require `READ` or `SELECT` object privilege on the tables or materialized views that underlie the graph.

To issue an Oracle Flashback Query using the `graph_ref_as_of_clause` in `GRAPH_TABLE`, you must additionally have `FLASHBACK` object privilege on the tables and materialized views that underlie the graph. This is needed only for those tables and views that are accessed by the query, based on the specified graph pattern and label expressions used therein. Alternatively, you must have `FLASHBACK ANY TABLE` system privilege.

Semantics

A graph name may be qualified with a schema name to allow for querying graphs created by other users. Furthermore, you can specify the `graph_ref_as_of_clause` clause to retrieve the result of the graph query at a particular change number (`SCN`) or timestamp. If you specify `SCN`, then `expr` must evaluate to a number. If you specify `TIMESTAMP`, then `expr` must evaluate to a timestamp value. In either case, `expr` cannot evaluate to NULL.

Example 1

The following query counts the number of persons in the students\_graph owned by user scott:

```
SELECT COUNT(*)
FROM GRAPH_TABLE ( scott.students_graph
  MATCH (a IS person)
  COLUMNS (a.name)
);
```

The output is:

```
  COUNT(*)
----------
      4
```

Example 2

The following example queries a graph at two different timestamps. It first inserts a new row into the university table that underlies the `students_graph`. It then queries versions of the graph before and after the insertion.

```
INSERT INTO university (name) VALUES ('u3');
```

```
SELECT COUNT(*)
FROM GRAPH_TABLE (
  students_graph
  MATCH (u IS university)
  COLUMNS (u.*)
);
```

```
SELECT COUNT(*)
FROM GRAPH_TABLE (
  students_graph AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' MINUTE)
  MATCH (u IS university)
  COLUMNS (u.*)
);
```

```
DELETE FROM university WHERE name = 'u3';
```

The output of the first query is:

```
  COUNT(*)
----------
         3
```

The output of the second query is:

```
   COUNT(*)
----------
         2
```

Note: this example assumes that the second `SELECT` query is run at least two minutes after the graph was created and within two minutes after running the `INSERT` statement, otherwise the output is different.