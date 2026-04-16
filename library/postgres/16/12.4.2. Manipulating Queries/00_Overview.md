---
source: PostgreSQL 16 Reference
title: 00_Overview
---

[Section 12.3.2](#page-88-0) showed how raw textual queries can be converted into tsquery values. PostgreSQL also provides functions and operators that can be used to manipulate queries that are already in tsquery form.

```
tsquery && tsquery
```

Returns the AND-combination of the two given queries.

```
tsquery || tsquery
```

Returns the OR-combination of the two given queries.

```
!! tsquery
```

Returns the negation (NOT) of the given query.

```
tsquery <-> tsquery
```

Returns a query that searches for a match to the first given query immediately followed by a match to the second given query, using the <-> (FOLLOWED BY) tsquery operator. For example:

```
SELECT to_tsquery('fat') <-> to_tsquery('cat | rat');
   ?column?
  ----------------------------
   'fat' <-> ( 'cat' | 'rat' )
tsquery_phrase(query1 tsquery, query2 tsquery [, distance integer
]) returns tsquery
```

Returns a query that searches for a match to the first given query followed by a match to the second given query at a distance of exactly distance lexemes, using the <N> tsquery operator. For example:

```
SELECT tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10);
   tsquery_phrase
  ------------------
   'fat' <10> 'cat'
numnode(query tsquery) returns integer
```

Returns the number of nodes (lexemes plus operators) in a tsquery. This function is useful to determine if the query is meaningful (returns > 0), or contains only stop words (returns 0). Examples:

```
SELECT numnode(plainto_tsquery('the any'));
  NOTICE: query contains only stopword(s) or doesn't contain
   lexeme(s), ignored
   numnode
  ---------
   0
  SELECT numnode('foo & bar'::tsquery);
   numnode
  ---------
   3
querytree(query tsquery) returns text
```

Returns the portion of a tsquery that can be used for searching an index. This function is useful for detecting unindexable queries, for example those containing only stop words or only negated terms. For example:

```
SELECT querytree(to_tsquery('defined'));
 querytree
-----------
 'defin'
SELECT querytree(to_tsquery('!defined'));
 querytree
-----------
 T
```