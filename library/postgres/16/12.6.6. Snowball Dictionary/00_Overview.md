---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The Snowball dictionary template is based on a project by Martin Porter, inventor of the popular Porter's stemming algorithm for the English language. Snowball now provides stemming algorithms for many languages (see the [Snowball site](https://snowballstem.org/)<sup>7</sup> for more information). Each algorithm understands how to reduce common variant forms of words to a base, or stem, spelling within its language. A Snowball dictionary requires a language parameter to identify which stemmer to use, and optionally can specify a stopword file name that gives a list of words to eliminate. (PostgreSQL's standard stopword lists are also provided by the Snowball project.) For example, there is a built-in definition equivalent to

```
CREATE TEXT SEARCH DICTIONARY english_stem (
 TEMPLATE = snowball,
 Language = english,
 StopWords = english
);
```

The stopword file format is the same as already explained.

A Snowball dictionary recognizes everything, whether or not it is able to simplify the word, so it should be placed at the end of the dictionary list. It is useless to have it before any other dictionary because a token will never pass through it to the next dictionary.

# <span id="page-111-0"></span>**12.7. Configuration Example**

A text search configuration specifies all options necessary to transform a document into a tsvector: the parser to use to break text into tokens, and the dictionaries to use to transform each token into a lexeme. Every call of to\_tsvector or to\_tsquery needs a text search configuration to perform its processing. The configuration parameter default\_text\_search\_config specifies the name of the default configuration, which is the one used by text search functions if an explicit configuration parameter is omitted. It can be set in postgresql.conf, or set for an individual session using the SET command.

Several predefined text search configurations are available, and you can create custom configurations easily. To facilitate management of text search objects, a set of SQL commands is available, and there are several psql commands that display information about text search objects ([Section 12.10\)](#page-118-0).

As an example we will create a configuration pg, starting by duplicating the built-in english configuration:

```
CREATE TEXT SEARCH CONFIGURATION public.pg ( COPY =
 pg_catalog.english );
```

We will use a PostgreSQL-specific synonym list and store it in \$SHAREDIR/tsearch\_data/pg\_dict.syn. The file contents look like:

```
postgres pg
```

<sup>7</sup> <https://snowballstem.org/>

```
pgsql pg
postgresql pg
We define the synonym dictionary like this:
CREATE TEXT SEARCH DICTIONARY pg_dict (
 TEMPLATE = synonym,
 SYNONYMS = pg_dict
);
Next we register the Ispell dictionary english_ispell, which has its own configuration files:
CREATE TEXT SEARCH DICTIONARY english_ispell (
 TEMPLATE = ispell,
 DictFile = english,
 AffFile = english,
 StopWords = english
);
Now we can set up the mappings for words in configuration pg:
ALTER TEXT SEARCH CONFIGURATION pg
 ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
 word, hword, hword_part
 WITH pg_dict, english_ispell, english_stem;
We choose not to index or search some token types that the built-in configuration does handle:
ALTER TEXT SEARCH CONFIGURATION pg
 DROP MAPPING FOR email, url, url_path, sfloat, float;
Now we can test our configuration:
SELECT * FROM ts_debug('public.pg', '
PostgreSQL, the highly scalable, SQL compliant, open source object-
relational
database management system, is now undergoing beta testing of the
 next
version of our software.
');
The next step is to set the session to use the new configuration, which was created in the public
schema:
=> \dF
 List of text search configurations
 Schema | Name | Description
---------+------+-------------
 public | pg |
SET default_text_search_config = 'public.pg';
SET
SHOW default_text_search_config;
 default_text_search_config
```

--------------------------- public.pg