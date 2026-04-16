---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Text search parsers are responsible for splitting raw document text into *tokens* and identifying each token's type, where the set of possible types is defined by the parser itself. Note that a parser does not modify the text at all — it simply identifies plausible word boundaries. Because of this limited scope, there is less need for application-specific custom parsers than there is for custom dictionaries. At present PostgreSQL provides just one built-in parser, which has been found to be useful for a wide range of applications.

The built-in parser is named pg\_catalog.default. It recognizes 23 token types, shown in [Ta](#page-100-0)[ble 12.1](#page-100-0).

<span id="page-100-0"></span>**Table 12.1. Default Parser's Token Types**

| Alias           | Description                                  | Example                                                  |
|-----------------|----------------------------------------------|----------------------------------------------------------|
| asciiword       | Word, all ASCII letters                      | elephant                                                 |
| word            | Word, all letters                            | mañana                                                   |
| numword         | Word, letters and digits                     | beta1                                                    |
| asciihword      | Hyphenated word, all<br>ASCII                | up-to-date                                               |
| hword           | Hyphenated word, all let<br>ters             | lógico-matemática                                        |
| numhword        | Hyphenated word, letters<br>and digits       | postgresql-beta1                                         |
| hword_asciipart | Hyphenated word part, all<br>ASCII           | postgresql in the context post<br>gresql-beta1           |
| hword_part      | Hyphenated word part, all<br>letters         | lógico or matemática in the context<br>lógico-matemática |
| hword_numpart   | Hyphenated word part, let<br>ters and digits | beta1 in the context post<br>gresql-beta1                |
| email           | Email address                                | foo@example.com                                          |
| protocol        | Protocol head                                | http://                                                  |
| url             | URL                                          | example.com/stuff/index.html                             |
| host            | Host                                         | example.com                                              |
| url_path        | URL path                                     | /stuff/index.html, in the context<br>of a URL            |

| Alias   | Description         | Example                                                      |
|---------|---------------------|--------------------------------------------------------------|
| file    | File or path name   | /usr/local/foo.txt, if not within<br>a URL                   |
| sfloat  | Scientific notation | -1.234e56                                                    |
| float   | Decimal notation    | -1.234                                                       |
| int     | Signed integer      | -1234                                                        |
| uint    | Unsigned integer    | 1234                                                         |
| version | Version number      | 8.3.0                                                        |
| tag     | XML tag             | <a href="dictionaries.html"></a>                             |
| entity  | XML entity          | &                                                            |
| blank   | Space symbols       | (any whitespace or punctuation not other<br>wise recognized) |

## **Note**

The parser's notion of a "letter" is determined by the database's locale setting, specifically lc\_ctype. Words containing only the basic ASCII letters are reported as a separate token type, since it is sometimes useful to distinguish them. In most European languages, token types word and asciiword should be treated alike.

email does not support all valid email characters as defined by [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322)<sup>1</sup> . Specifically, the only non-alphanumeric characters supported for email user names are period, dash, and underscore.

tag does not support all valid tag names as defined by [W3C Recommendation, XML](https://www.w3.org/TR/xml/)<sup>2</sup> . Specifically, the only tag names supported are those starting with an ASCII letter, underscore, or colon, and containing only letters, digits, hyphens, underscores, periods, and colons. tag also includes XML comments starting with <!-- and ending with -->, and XML declarations (but note that this includes anything starting with <?x and ending with >).

It is possible for the parser to produce overlapping tokens from the same piece of text. As an example, a hyphenated word will be reported both as the entire word and as each component:

```
SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
 alias | description | 
 token
-----------------+------------------------------------------
+---------------
 numhword | Hyphenated word, letters and digits | foo-
bar-beta1
 hword_asciipart | Hyphenated word part, all ASCII | foo
 blank | Space symbols | -
 hword_asciipart | Hyphenated word part, all ASCII | bar
 blank | Space symbols | -
 hword_numpart | Hyphenated word part, letters and digits | beta1
```

This behavior is desirable since it allows searches to work for both the whole compound word and for components. Here is another instructive example:

<sup>1</sup> <https://datatracker.ietf.org/doc/html/rfc5322>

<sup>2</sup> <https://www.w3.org/TR/xml/>

```
SELECT alias, description, token FROM ts_debug('http://example.com/
stuff/index.html');
 alias | description | token
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url | URL | example.com/stuff/index.html
 host | Host | example.com
 url_path | URL path | /stuff/index.html
```

# <span id="page-102-0"></span>**12.6. Dictionaries**

Dictionaries are used to eliminate words that should not be considered in a search (*stop words*), and to *normalize* words so that different derived forms of the same word will match. A successfully normalized word is called a *lexeme*. Aside from improving search quality, normalization and removal of stop words reduce the size of the tsvector representation of a document, thereby improving performance. Normalization does not always have linguistic meaning and usually depends on application semantics.

Some examples of normalization:

- Linguistic Ispell dictionaries try to reduce input words to a normalized form; stemmer dictionaries remove word endings
- URL locations can be canonicalized to make equivalent URLs match:
  - http://www.pgsql.ru/db/mw/index.html
  - http://www.pgsql.ru/db/mw/
  - http://www.pgsql.ru/db/../db/mw/index.html
- Color names can be replaced by their hexadecimal values, e.g., red, green, blue, magenta -> FF0000, 00FF00, 0000FF, FF00FF
- If indexing numbers, we can remove some fractional digits to reduce the range of possible numbers, so for example *3.14*159265359, *3.14*15926, *3.14* will be the same after normalization if only two digits are kept after the decimal point.

A dictionary is a program that accepts a token as input and returns:

- an array of lexemes if the input token is known to the dictionary (notice that one token can produce more than one lexeme)
- a single lexeme with the TSL\_FILTER flag set, to replace the original token with a new token to be passed to subsequent dictionaries (a dictionary that does this is called a *filtering dictionary*)
- an empty array if the dictionary knows the token, but it is a stop word
- NULL if the dictionary does not recognize the input token

PostgreSQL provides predefined dictionaries for many languages. There are also several predefined templates that can be used to create new dictionaries with custom parameters. Each predefined dictionary template is described below. If no existing template is suitable, it is possible to create new ones; see the contrib/ area of the PostgreSQL distribution for examples.

A text search configuration binds a parser together with a set of dictionaries to process the parser's output tokens. For each token type that the parser can return, a separate list of dictionaries is specified by the configuration. When a token of that type is found by the parser, each dictionary in the list is consulted in turn, until some dictionary recognizes it as a known word. If it is identified as a stop word, or if no dictionary recognizes the token, it will be discarded and not indexed or searched for. Normally, the first dictionary that returns a non-NULL output determines the result, and any remaining dictionaries are not consulted; but a filtering dictionary can replace the given word with a modified word, which is then passed to subsequent dictionaries.

The general rule for configuring a list of dictionaries is to place first the most narrow, most specific dictionary, then the more general dictionaries, finishing with a very general dictionary, like a Snowball stemmer or simple, which recognizes everything. For example, for an astronomy-specific search (astro\_en configuration) one could bind token type asciiword (ASCII word) to a synonym dictionary of astronomical terms, a general English dictionary and a Snowball English stemmer:

```
ALTER TEXT SEARCH CONFIGURATION astro_en
 ADD MAPPING FOR asciiword WITH astrosyn, english_ispell,
 english_stem;
```

A filtering dictionary can be placed anywhere in the list, except at the end where it'd be useless. Filtering dictionaries are useful to partially normalize words to simplify the task of later dictionaries. For example, a filtering dictionary could be used to remove accents from accented letters, as is done by the unaccent module.

## <span id="page-103-0"></span>**12.6.1. Stop Words**

Stop words are words that are very common, appear in almost every document, and have no discrimination value. Therefore, they can be ignored in the context of full text searching. For example, every English text contains words like a and the, so it is useless to store them in an index. However, stop words do affect the positions in tsvector, which in turn affect ranking:

```
SELECT to_tsvector('english', 'in the list of stop words');
 to_tsvector
----------------------------
 'list':3 'stop':5 'word':6
```

The missing positions 1,2,4 are because of stop words. Ranks calculated for documents with and without stop words are quite different:

```
SELECT ts_rank_cd (to_tsvector('english', 'in the list of stop
 words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
 0.05
SELECT ts_rank_cd (to_tsvector('english', 'list stop words'),
 to_tsquery('list & stop'));
 ts_rank_cd
------------
 0.1
```

It is up to the specific dictionary how it treats stop words. For example, ispell dictionaries first normalize words and then look at the list of stop words, while Snowball stemmers first check the list of stop words. The reason for the different behavior is an attempt to decrease noise.