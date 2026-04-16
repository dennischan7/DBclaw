---
source: PostgreSQL 15 Reference
title: 00_Overview
---

its synonym

substitution

check for stopword

The current limitations of PostgreSQL's text search features are:

pg\_catalog | ispell | ispell dictionary

pg\_catalog | snowball | snowball stemmer

pg\_catalog | simple | simple dictionary: just lower case and

pg\_catalog | thesaurus | thesaurus dictionary: phrase by phrase

pg\_catalog | synonym | synonym dictionary: replace word by

- The length of each lexeme must be less than 2 kilobytes
- The length of a tsvector (lexemes + positions) must be less than 1 megabyte
- The number of lexemes must be less than 2<sup>64</sup>
- Position values in tsvector must be greater than 0 and no more than 16,383
- The match distance in a <N> (FOLLOWED BY) tsquery operator cannot be more than 16,384
- No more than 256 positions per lexeme
- The number of nodes (lexemes + operators) in a tsquery must be less than 32,768

For comparison, the PostgreSQL 8.1 documentation contained 10,441 unique words, a total of 335,420 words, and the most frequent word "postgresql" was mentioned 6,127 times in 655 documents.

Another example — the PostgreSQL mailing list archives contained 910,989 unique words with 57,491,343 lexemes in 461,020 messages.

# <span id="page-116-0"></span>**Chapter 13. Concurrency Control**

This chapter describes the behavior of the PostgreSQL database system when two or more sessions try to access the same data at the same time. The goals in that situation are to allow efficient access for all sessions while maintaining strict data integrity. Every developer of database applications should be familiar with the topics covered in this chapter.