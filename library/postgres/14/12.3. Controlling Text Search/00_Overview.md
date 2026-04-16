---
source: PostgreSQL 14 Reference
title: 00_Overview
---

To implement full text searching there must be a function to create a tsvector from a document and a tsquery from a user query. Also, we need to return results in a useful order, so we need a function that compares documents with respect to their relevance to the query. It's also important to be able to display the results nicely. PostgreSQL provides support for all of these functions.

## <span id="page-75-0"></span>**12.3.1. Parsing Documents**

PostgreSQL provides the function to\_tsvector for converting a document to the tsvector data type.

```
to_tsvector([ config regconfig, ] document text) returns tsvector
```

to\_tsvector parses a textual document into tokens, reduces the tokens to lexemes, and returns a tsvector which lists the lexemes together with their positions in the document. The document is processed according to the specified or default text search configuration. Here is a simple example:

```
SELECT to_tsvector('english', 'a fat cat sat on a mat - it ate a
 fat rats');
 to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```

In the example above we see that the resulting tsvector does not contain the words a, on, or it, the word rats became rat, and the punctuation sign - was ignored.

The to\_tsvector function internally calls a parser which breaks the document text into tokens and assigns a type to each token. For each token, a list of dictionaries ([Section 12.6](#page-90-0)) is consulted, where the list can vary depending on the token type. The first dictionary that *recognizes* the token emits one or more normalized *lexemes* to represent the token. For example, rats became rat because one of the dictionaries recognized that the word rats is a plural form of rat. Some words are recognized as *stop words* [\(Section 12.6.1\)](#page-91-0), which causes them to be ignored since they occur too frequently to be useful in searching. In our example these are a, on, and it. If no dictionary in the list recognizes the token then it is also ignored. In this example that happened to the punctuation sign - because there are in fact no dictionaries assigned for its token type (Space symbols), meaning space tokens will never be indexed. The choices of parser, dictionaries and which types of tokens to index are determined by the selected text search configuration [\(Section 12.7\)](#page-99-0). It is possible to have many different configurations in the same database, and predefined configurations are available for various languages. In our example we used the default configuration english for the English language.

The function setweight can be used to label the entries of a tsvector with a given *weight*, where a weight is one of the letters A, B, C, or D. This is typically used to mark entries coming from different parts of a document, such as title versus body. Later, this information can be used for ranking of search results.

Because to\_tsvector(NULL) will return NULL, it is recommended to use coalesce whenever a field might be null. Here is the recommended method for creating a tsvector from a structured document:

```
UPDATE tt SET ti =
 setweight(to_tsvector(coalesce(title,'')), 'A') ||
 setweight(to_tsvector(coalesce(keyword,'')), 'B') ||
 setweight(to_tsvector(coalesce(abstract,'')), 'C') ||
 setweight(to_tsvector(coalesce(body,'')), 'D');
```

Here we have used setweight to label the source of each lexeme in the finished tsvector, and then merged the labeled tsvector values using the tsvector concatenation operator ||. ([Sec](#page-82-0)[tion 12.4.1](#page-82-0) gives details about these operations.)

### <span id="page-76-0"></span>**12.3.2. Parsing Queries**

PostgreSQL provides the functions to\_tsquery, plainto\_tsquery, phraseto\_tsquery and websearch\_to\_tsquery for converting a query to the tsquery data type. to\_tsquery offers access to more features than either plainto\_tsquery or phraseto\_tsquery, but it is less forgiving about its input. websearch\_to\_tsquery is a simplified version of to\_tsquery with an alternative syntax, similar to the one used by web search engines.

```
to_tsquery([ config regconfig, ] querytext text) returns tsquery
```

to\_tsquery creates a tsquery value from querytext, which must consist of single tokens separated by the tsquery operators & (AND), | (OR), ! (NOT), and <-> (FOLLOWED BY), possibly grouped using parentheses. In other words, the input to to\_tsquery must already follow the general rules for tsquery input, as described in Section 8.11.2. The difference is that while basic tsquery input takes the tokens at face value, to\_tsquery normalizes each token into a lexeme using the specified or default configuration, and discards any tokens that are stop words according to the configuration. For example:

```
SELECT to_tsquery('english', 'The & Fat & Rats');
 to_tsquery 
---------------
 'fat' & 'rat'
```

As in basic tsquery input, weight(s) can be attached to each lexeme to restrict it to match only tsvector lexemes of those weight(s). For example:

```
SELECT to_tsquery('english', 'Fat | Rats:AB');
 to_tsquery
```

```
------------------
 'fat' | 'rat':AB
```

Also, \* can be attached to a lexeme to specify prefix matching:

```
SELECT to_tsquery('supern:*A & star:A*B');
 to_tsquery 
--------------------------
 'supern':*A & 'star':*AB
```

Such a lexeme will match any word in a tsvector that begins with the given string.

to\_tsquery can also accept single-quoted phrases. This is primarily useful when the configuration includes a thesaurus dictionary that may trigger on such phrases. In the example below, a thesaurus contains the rule supernovae stars : sn:

```
SELECT to_tsquery('''supernovae stars'' & !crab');
 to_tsquery
---------------
 'sn' & !'crab'
```

Without quotes, to\_tsquery will generate a syntax error for tokens that are not separated by an AND, OR, or FOLLOWED BY operator.

```
plainto_tsquery([ config regconfig, ] querytext text)
 returns tsquery
```

plainto\_tsquery transforms the unformatted text querytext to a tsquery value. The text is parsed and normalized much as for to\_tsvector, then the & (AND) tsquery operator is inserted between surviving words.

#### Example:

```
SELECT plainto_tsquery('english', 'The Fat Rats');
 plainto_tsquery 
-----------------
 'fat' & 'rat'
```

Note that plainto\_tsquery will not recognize tsquery operators, weight labels, or prefix-match labels in its input:

```
SELECT plainto_tsquery('english', 'The Fat & Rats:C');
 plainto_tsquery 
---------------------
 'fat' & 'rat' & 'c'
```

Here, all the input punctuation was discarded.

```
phraseto_tsquery([ config regconfig, ] querytext text)
 returns tsquery
```

phraseto\_tsquery behaves much like plainto\_tsquery, except that it inserts the <-> (FOLLOWED BY) operator between surviving words instead of the & (AND) operator. Also, stop words are not simply discarded, but are accounted for by inserting <N> operators rather than <-> operators. This function is useful when searching for exact lexeme sequences, since the FOLLOWED BY operators check lexeme order not just the presence of all the lexemes.

#### Example:

```
SELECT phraseto_tsquery('english', 'The Fat Rats');
 phraseto_tsquery
------------------
 'fat' <-> 'rat'
```

Like plainto\_tsquery, the phraseto\_tsquery function will not recognize tsquery operators, weight labels, or prefix-match labels in its input:

```
SELECT phraseto_tsquery('english', 'The Fat & Rats:C');
 phraseto_tsquery
-----------------------------
 'fat' <-> 'rat' <-> 'c'
websearch_to_tsquery([ config regconfig, ] querytext text)
 returns tsquery
```

websearch\_to\_tsquery creates a tsquery value from querytext using an alternative syntax in which simple unformatted text is a valid query. Unlike plainto\_tsquery and phraseto\_tsquery, it also recognizes certain operators. Moreover, this function will never raise syntax errors, which makes it possible to use raw user-supplied input for search. The following syntax is supported:

- unquoted text: text not inside quote marks will be converted to terms separated by & operators, as if processed by plainto\_tsquery.
- "quoted text": text inside quote marks will be converted to terms separated by <-> operators, as if processed by phraseto\_tsquery.
- OR: the word "or" will be converted to the | operator.
- -: a dash will be converted to the ! operator.

Other punctuation is ignored. So like plainto\_tsquery and phraseto\_tsquery, the websearch\_to\_tsquery function will not recognize tsquery operators, weight labels, or prefix-match labels in its input.

### Examples:

```
SELECT websearch_to_tsquery('english', 'The fat rats');
 websearch_to_tsquery
----------------------
 'fat' & 'rat'
(1 row)
SELECT websearch_to_tsquery('english', '"supernovae stars" -crab');
 websearch_to_tsquery
----------------------------------
 'supernova' <-> 'star' & !'crab'
(1 row)
SELECT websearch_to_tsquery('english', '"sad cat" or "fat rat"');
 websearch_to_tsquery
-----------------------------------
```

```
 'sad' <-> 'cat' | 'fat' <-> 'rat'
(1 row)
SELECT websearch_to_tsquery('english', 'signal -"segmentation
 fault"');
 websearch_to_tsquery
---------------------------------------
 'signal' & !( 'segment' <-> 'fault' )
(1 row)
SELECT websearch_to_tsquery('english', '""" )( dummy \\ query <-
>');
 websearch_to_tsquery
----------------------
 'dummi' & 'queri'
(1 row)
```