---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL's full-text search capability has few user-tunable parameters. You can exert more control over full-text searching behavior if you have a MySQL source distribution because some changes require source code modifications. See Section 2.8, "Installing MySQL from Source".

Full-text search is carefully tuned for effectiveness. Modifying the default behavior in most cases can actually decrease effectiveness. Do not alter the MySQL sources unless you know what you are doing.

Most full-text variables described in this section must be set at server startup time. A server restart is required to change them; they cannot be modified while the server is running.

Some variable changes require that you rebuild the FULLTEXT indexes in your tables. Instructions for doing so are given later in this section.

- [Configuring Minimum and Maximum Word Length](#page-1-0)
- [Configuring the Natural Language Search Threshold](#page-1-1)
- [Modifying Boolean Full-Text Search Operators](#page-1-2)
- [Character Set Modifications](#page-1-3)
- [Rebuilding InnoDB Full-Text Indexes](#page-2-0)

- [Optimizing InnoDB Full-Text Indexes](#page-2-1)
- [Rebuilding MyISAM Full-Text Indexes](#page-2-2)

### <span id="page-1-0"></span>**Configuring Minimum and Maximum Word Length**

The minimum and maximum lengths of words to be indexed are defined by the innodb\_ft\_min\_token\_size and innodb\_ft\_max\_token\_size for InnoDB search indexes, and ft\_min\_word\_len and ft\_max\_word\_len for MyISAM ones.

![](_page_1_Picture_5.jpeg)

### **Note**

Minimum and maximum word length full-text parameters do not apply to FULLTEXT indexes created using the ngram parser. ngram token size is defined by the ngram\_token\_size option.

After changing any of these options, rebuild your FULLTEXT indexes for the change to take effect. For example, to make two-character words searchable, you could put the following lines in an option file:

```
[mysqld]
innodb_ft_min_token_size=2
ft_min_word_len=2
```

Then restart the server and rebuild your FULLTEXT indexes. For MyISAM tables, note the remarks regarding myisamchk in the instructions that follow for rebuilding MyISAM full-text indexes.

### <span id="page-1-1"></span>**Configuring the Natural Language Search Threshold**

For MyISAM search indexes, the 50% threshold for natural language searches is determined by the particular weighting scheme chosen. To disable it, look for the following line in storage/myisam/ ftdefs.h:

```
#define GWS_IN_USE GWS_PROB
```

Change that line to this:

```
#define GWS_IN_USE GWS_FREQ
```

Then recompile MySQL. There is no need to rebuild the indexes in this case.

![](_page_1_Picture_17.jpeg)

### **Note**

By making this change, you severely decrease MySQL's ability to provide adequate relevance values for the MATCH() function. If you really need to search for such common words, it would be better to search using IN BOOLEAN MODE instead, which does not observe the 50% threshold.

### <span id="page-1-2"></span>**Modifying Boolean Full-Text Search Operators**

To change the operators used for boolean full-text searches on MyISAM tables, set the ft\_boolean\_syntax system variable. (InnoDB does not have an equivalent setting.) This variable can be changed while the server is running, but you must have privileges sufficient to set global system variables (see Section 7.1.9.1, "System Variable Privileges"). No rebuilding of indexes is necessary in this case.

### <span id="page-1-3"></span>**Character Set Modifications**

For the built-in full-text parser, you can change the set of characters that are considered word characters in several ways, as described in the following list. After making the modification, rebuild the indexes for each table that contains any FULLTEXT indexes. Suppose that you want to treat the hyphen character ('-') as a word character. Use one of these methods:

- Modify the MySQL source: In storage/innobase/handler/ha\_innodb.cc (for InnoDB), or in storage/myisam/ftdefs.h (for MyISAM), see the true\_word\_char() and misc\_word\_char() macros. Add '-' to one of those macros and recompile MySQL.
- Modify a character set file: This requires no recompilation. The true\_word\_char() macro uses a "character type" table to distinguish letters and numbers from other characters. . You can edit the contents of the <ctype><map> array in one of the character set XML files to specify that '-' is a "letter." Then use the given character set for your FULLTEXT indexes. For information about the <ctype><map> array format, see Section 12.13.1, "Character Definition Arrays".
- Add a new collation for the character set used by the indexed columns, and alter the columns to use that collation. For general information about adding collations, see Section 12.14, "Adding a Collation to a Character Set". For an example specific to full-text indexing, see [Section 14.9.7, "Adding a User-](#page-3-0)[Defined Collation for Full-Text Indexing"](#page-3-0).

### <span id="page-2-0"></span>**Rebuilding InnoDB Full-Text Indexes**

For the changes to take effect, FULLTEXT indexes must be rebuilt after modifying any of the following full-text index variables: innodb\_ft\_min\_token\_size; innodb\_ft\_max\_token\_size; innodb\_ft\_server\_stopword\_table; innodb\_ft\_user\_stopword\_table; innodb\_ft\_enable\_stopword; ngram\_token\_size. Modifying innodb\_ft\_min\_token\_size, innodb\_ft\_max\_token\_size, or ngram\_token\_size requires restarting the server.

To rebuild FULLTEXT indexes for an InnoDB table, use ALTER TABLE with the DROP INDEX and ADD INDEX options to drop and re-create each index.

### <span id="page-2-1"></span>**Optimizing InnoDB Full-Text Indexes**

Running OPTIMIZE TABLE on a table with a full-text index rebuilds the full-text index, removing deleted Document IDs and consolidating multiple entries for the same word, where possible.

To optimize a full-text index, enable innodb\_optimize\_fulltext\_only and run OPTIMIZE TABLE.

```
mysql> set GLOBAL innodb_optimize_fulltext_only=ON;
Query OK, 0 rows affected (0.01 sec)
mysql> OPTIMIZE TABLE opening_lines;
+--------------------+----------+----------+----------+
| Table | Op | Msg_type | Msg_text |
+--------------------+----------+----------+----------+
| test.opening_lines | optimize | status | OK |
+--------------------+----------+----------+----------+
1 row in set (0.01 sec)
```

To avoid lengthy rebuild times for full-text indexes on large tables, you can use the innodb\_ft\_num\_word\_optimize option to perform the optimization in stages. The innodb\_ft\_num\_word\_optimize option defines the number of words that are optimized each time OPTIMIZE TABLE is run. The default setting is 2000, which means that 2000 words are optimized each time OPTIMIZE TABLE is run. Subsequent OPTIMIZE TABLE operations continue from where the preceding OPTIMIZE TABLE operation ended.

## <span id="page-2-2"></span>**Rebuilding MyISAM Full-Text Indexes**

If you modify full-text variables that affect indexing (ft\_min\_word\_len, ft\_max\_word\_len, or ft\_stopword\_file), or if you change the stopword file itself, you must rebuild your FULLTEXT indexes after making the changes and restarting the server.

To rebuild the FULLTEXT indexes for a MyISAM table, it is sufficient to do a QUICK repair operation:

```
mysql> REPAIR TABLE tbl_name QUICK;
```

Alternatively, use ALTER TABLE as just described. In some cases, this may be faster than a repair operation.

Each table that contains any FULLTEXT index must be repaired as just shown. Otherwise, queries for the table may yield incorrect results, and modifications to the table causes the server to see the table as corrupt and in need of repair.

If you use myisamchk to perform an operation that modifies MyISAM table indexes (such as repair or analyze), the FULLTEXT indexes are rebuilt using the default full-text parameter values for minimum word length, maximum word length, and stopword file unless you specify otherwise. This can result in queries failing.

The problem occurs because these parameters are known only by the server. They are not stored in MyISAM index files. To avoid the problem if you have modified the minimum or maximum word length or stopword file values used by the server, specify the same ft\_min\_word\_len, ft\_max\_word\_len, and ft\_stopword\_file values for myisamchk that you use for mysqld. For example, if you have set the minimum word length to 3, you can repair a table with myisamchk like this:

```
myisamchk --recover --ft_min_word_len=3 tbl_name.MYI
```

To ensure that myisamchk and the server use the same values for full-text parameters, place each one in both the [mysqld] and [myisamchk] sections of an option file:

```
[mysqld]
ft_min_word_len=3
[myisamchk]
ft_min_word_len=3
```

An alternative to using myisamchk for MyISAM table index modification is to use the REPAIR TABLE, ANALYZE TABLE, OPTIMIZE TABLE, or ALTER TABLE statements. These statements are performed by the server, which knows the proper full-text parameter values to use.

# <span id="page-3-0"></span>**14.9.7 Adding a User-Defined Collation for Full-Text Indexing**

![](_page_3_Picture_9.jpeg)

### **Warning**

User-defined collations are deprecated; you should expect support for them to be removed in a future version of MySQL. As of MySQL 8.0.33, the server issues a warning for any use of COLLATE user\_defined\_collation in an SQL statement; a warning is also issued when the server is started with - collation-server set equal to the name of a user-defined collation.

This section describes how to add a user-defined collation for full-text searches using the built-in fulltext parser. The sample collation is like latin1\_swedish\_ci but treats the '-' character as a letter rather than as a punctuation character so that it can be indexed as a word character. General information about adding collations is given in Section 12.14, "Adding a Collation to a Character Set"; it is assumed that you have read it and are familiar with the files involved.

To add a collation for full-text indexing, use the following procedure. The instructions here add a collation for a simple character set, which as discussed in Section 12.14, "Adding a Collation to a Character Set", can be created using a configuration file that describes the character set properties. For a complex character set such as Unicode, create collations using C source files that describe the character set properties.

1. Add a collation to the Index.xml file. The permitted range of IDs for user-defined collations is given in Section 12.14.2, "Choosing a Collation ID". The ID must be unused, so choose a value different from 1025 if that ID is already taken on your system.

```
<charset name="latin1">
...
<collation name="latin1_fulltext_ci" id="1025"/>
</charset>
```

2. Declare the sort order for the collation in the latin1.xml file. In this case, the order can be copied from latin1\_swedish\_ci:

```
<collation name="latin1_fulltext_ci">
<map>
00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
60 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
50 51 52 53 54 55 56 57 58 59 5A 7B 7C 7D 7E 7F
80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
41 41 41 41 5C 5B 5C 43 45 45 45 45 49 49 49 49
44 4E 4F 4F 4F 4F 5D D7 D8 55 55 55 59 59 DE DF
41 41 41 41 5C 5B 5C 43 45 45 45 45 49 49 49 49
44 4E 4F 4F 4F 4F 5D F7 D8 55 55 55 59 59 DE FF
</map>
</collation>
```

3. Modify the ctype array in latin1.xml. Change the value corresponding to 0x2D (which is the code for the '-' character) from 10 (punctuation) to 01 (uppercase letter). In the following array, this is the element in the fourth row down, third value from the end.

```
<ctype>
<map>
20 20 20 20 20 20 20 20 20 28 28 28 28 28 20 20
20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
48 10 10 10 10 10 10 10 10 10 10 10 10 01 10 10
84 84 84 84 84 84 84 84 84 84 10 10 10 10 10 10
10 81 81 81 81 81 81 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 01 01 01 01 10 10 10 10 10
10 82 82 82 82 82 82 02 02 02 02 02 02 02 02 02
02 02 02 02 02 02 02 02 02 02 02 10 10 10 10 20
10 00 10 02 10 10 10 10 10 10 01 10 01 00 01 00
00 10 10 10 10 10 10 10 10 10 02 10 02 00 02 01
48 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 10 01 01 01 01 01 01 01 02
02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02
02 02 02 02 02 02 02 10 02 02 02 02 02 02 02 02
</map>
</ctype>
```

- 4. Restart the server.
- 5. To employ the new collation, include it in the definition of columns that are to use it:

```
mysql> DROP TABLE IF EXISTS t1;
Query OK, 0 rows affected (0.13 sec)
mysql> CREATE TABLE t1 (
 a TEXT CHARACTER SET latin1 COLLATE latin1_fulltext_ci,
 FULLTEXT INDEX(a)
 ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.47 sec)
```

6. Test the collation to verify that hyphen is considered as a word character:

```
mysql> INSERT INTO t1 VALUEs ('----'),('....'),('abcd');
Query OK, 3 rows affected (0.22 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT * FROM t1 WHERE MATCH a AGAINST ('----' IN BOOLEAN MODE);
+------+
| a |
+------+
```

```
| ---- |
+------+
1 row in set (0.00 sec)
```

## <span id="page-5-0"></span>**14.9.8 ngram Full-Text Parser**

The built-in MySQL full-text parser uses the white space between words as a delimiter to determine where words begin and end, which is a limitation when working with ideographic languages that do not use word delimiters. To address this limitation, MySQL provides an ngram full-text parser that supports Chinese, Japanese, and Korean (CJK). The ngram full-text parser is supported for use with InnoDB and MyISAM.

![](_page_5_Picture_4.jpeg)

### **Note**

MySQL also provides a MeCab full-text parser plugin for Japanese, which tokenizes documents into meaningful words. For more information, see [Section 14.9.9, "MeCab Full-Text Parser Plugin"](#page-7-0).

An ngram is a contiguous sequence of n characters from a given sequence of text. The ngram parser tokenizes a sequence of text into a contiguous sequence of n characters. For example, you can tokenize "abcd" for different values of n using the ngram full-text parser.

```
n=1: 'a', 'b', 'c', 'd'
n=2: 'ab', 'bc', 'cd'
n=3: 'abc', 'bcd'
n=4: 'abcd'
```

The ngram full-text parser is a built-in server plugin. As with other built-in server plugins, it is automatically loaded when the server is started.

The full-text search syntax described in Section 14.9, "Full-Text Search Functions" applies to the ngram parser plugin. Differences in parsing behavior are described in this section. Fulltext-related configuration options, except for minimum and maximum word length options (innodb\_ft\_min\_token\_size, innodb\_ft\_max\_token\_size, ft\_min\_word\_len, ft\_max\_word\_len) are also applicable.

### **Configuring ngram Token Size**

The ngram parser has a default ngram token size of 2 (bigram). For example, with a token size of 2, the ngram parser parses the string "abc def" into four tokens: "ab", "bc", "de" and "ef".

ngram token size is configurable using the ngram\_token\_size configuration option, which has a minimum value of 1 and maximum value of 10.

Typically, ngram\_token\_size is set to the size of the largest token that you want to search for. If you only intend to search for single characters, set ngram\_token\_size to 1. A smaller token size produces a smaller full-text search index, and faster searches. If you need to search for words comprised of more than one character, set ngram\_token\_size accordingly. For example, "Happy Birthday" is "生日快乐" in simplified Chinese, where "生日" is "birthday", and "快乐" translates as "happy". To search on two-character words such as these, set ngram\_token\_size to a value of 2 or higher.

As a read-only variable, ngram\_token\_size may only be set as part of a startup string or in a configuration file:

• Startup string:

```
mysqld --ngram_token_size=2
```

• Configuration file:

```
[mysqld]
ngram_token_size=2
```

![](_page_6_Picture_1.jpeg)

### **Note**

The following minimum and maximum word length configuration options are ignored for FULLTEXT indexes that use the ngram parser: innodb\_ft\_min\_token\_size, innodb\_ft\_max\_token\_size, ft\_min\_word\_len, and ft\_max\_word\_len.

### **Creating a FULLTEXT Index that Uses the ngram Parser**

To create a FULLTEXT index that uses the ngram parser, specify WITH PARSER ngram with CREATE TABLE, ALTER TABLE, or CREATE INDEX.

The following example demonstrates creating a table with an ngram FULLTEXT index, inserting sample data (Simplified Chinese text), and viewing tokenized data in the Information Schema INNODB\_FT\_INDEX\_CACHE table.

```
mysql> USE test;
mysql> CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT,
 FULLTEXT (title,body) WITH PARSER ngram
 ) ENGINE=InnoDB CHARACTER SET utf8mb4;
mysql> SET NAMES utf8mb4;
INSERT INTO articles (title,body) VALUES
 ('数据库管理','在本教程中我将向你展示如何管理数据库'),
 ('数据库应用开发','学习开发数据库应用程序');
mysql> SET GLOBAL innodb_ft_aux_table="test/articles";
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_CACHE ORDER BY doc_id, position;
```

To add a FULLTEXT index to an existing table, you can use ALTER TABLE or CREATE INDEX. For example:

```
CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT
 ) ENGINE=InnoDB CHARACTER SET utf8mb4;
ALTER TABLE articles ADD FULLTEXT INDEX ft_index (title,body) WITH PARSER ngram;
# Or:
CREATE FULLTEXT INDEX ft_index ON articles (title,body) WITH PARSER ngram;
```

### **ngram Parser Space Handling**

The ngram parser eliminates spaces when parsing. For example:

- "ab cd" is parsed to "ab", "cd"
- "a bc" is parsed to "bc"

### **ngram Parser Stopword Handling**

The built-in MySQL full-text parser compares words to entries in the stopword list. If a word is equal to an entry in the stopword list, the word is excluded from the index. For the ngram parser, stopword handling is performed differently. Instead of excluding tokens that are equal to entries in the stopword list, the ngram parser excludes tokens that contain stopwords. For example, assuming ngram\_token\_size=2, a document that contains "a,b" is parsed to "a," and ",b". If a comma (",") is defined as a stopword, both "a," and ",b" are excluded from the index because they contain a comma. By default, the ngram parser uses the default stopword list, which contains a list of English stopwords. For a stopword list applicable to Chinese, Japanese, or Korean, you must create your own. For information about creating a stopword list, see Section 14.9.4, "Full-Text Stopwords".

Stopwords greater in length than ngram\_token\_size are ignored.

### **ngram Parser Term Search**

For natural language mode search, the search term is converted to a union of ngram terms. For example, the string "abc" (assuming ngram\_token\_size=2) is converted to "ab bc". Given two documents, one containing "ab" and the other containing "abc", the search term "ab bc" matches both documents.

For boolean mode search, the search term is converted to an ngram phrase search. For example, the string 'abc' (assuming ngram\_token\_size=2) is converted to '"ab bc"'. Given two documents, one containing 'ab' and the other containing 'abc', the search phrase '"ab bc"' only matches the document containing 'abc'.

### **ngram Parser Wildcard Search**

Because an ngram FULLTEXT index contains only ngrams, and does not contain information about the beginning of terms, wildcard searches may return unexpected results. The following behaviors apply to wildcard searches using ngram FULLTEXT search indexes:

- If the prefix term of a wildcard search is shorter than ngram token size, the query returns all indexed rows that contain ngram tokens starting with the prefix term. For example, assuming ngram\_token\_size=2, a search on "a\*" returns all rows starting with "a".
- If the prefix term of a wildcard search is longer than ngram token size, the prefix term is converted to an ngram phrase and the wildcard operator is ignored. For example, assuming ngram\_token\_size=2, an "abc\*" wildcard search is converted to "ab bc".

## **ngram Parser Phrase Search**

Phrase searches are converted to ngram phrase searches. For example, The search phrase "abc" is converted to "ab bc", which returns documents containing "abc" and "ab bc".

The search phrase "abc def" is converted to "ab bc de ef", which returns documents containing "abc def" and "ab bc de ef". A document that contains "abcdef" is not returned.

# <span id="page-7-0"></span>**14.9.9 MeCab Full-Text Parser Plugin**

The built-in MySQL full-text parser uses the white space between words as a delimiter to determine where words begin and end, which is a limitation when working with ideographic languages that do not use word delimiters. To address this limitation for Japanese, MySQL provides a MeCab full-text parser plugin. The MeCab full-text parser plugin is supported for use with InnoDB and MyISAM.

![](_page_7_Picture_15.jpeg)

### **Note**

MySQL also provides an ngram full-text parser plugin that supports Japanese. For more information, see [Section 14.9.8, "ngram Full-Text Parser".](#page-5-0)

The MeCab full-text parser plugin is a full-text parser plugin for Japanese that tokenizes a sequence of text into meaningful words. For example, MeCab tokenizes "データベース管理" ("Database Management") into "データベース" ("Database") and "管理" ("Management"). By comparison, the [ngram](#page-5-0) full-text parser tokenizes text into a contiguous sequence of n characters, where n represents a number between 1 and 10.

In addition to tokenizing text into meaningful words, MeCab indexes are typically smaller than ngram indexes, and MeCab full-text searches are generally faster. One drawback is that it may take longer for the MeCab full-text parser to tokenize documents, compared to the ngram full-text parser.

The full-text search syntax described in Section 14.9, "Full-Text Search Functions" applies to the MeCab parser plugin. Differences in parsing behavior are described in this section. Full-text related configuration options are also applicable.

For additional information about the MeCab parser, refer to the [MeCab: Yet Another Part-of-Speech](http://taku910.github.io/mecab/) [and Morphological Analyzer](http://taku910.github.io/mecab/) project on Github.

### **Installing the MeCab Parser Plugin**

The MeCab parser plugin requires mecab and mecab-ipadic.

On supported Fedora, Debian and Ubuntu platforms (except Ubuntu 12.04 where the system mecab version is too old), MySQL dynamically links to the system mecab installation if it is installed to the default location. On other supported Unix-like platforms, libmecab.so is statically linked in libpluginmecab.so, which is located in the MySQL plugin directory. mecab-ipadic is included in MySQL binaries and is located in MYSQL\_HOME\lib\mecab.

You can install mecab and mecab-ipadic using a native package management utility (on Fedora, Debian, and Ubuntu), or you can build mecab and mecab-ipadic from source. For information about installing mecab and mecab-ipadic using a native package management utility, see [Installing MeCab](#page-10-0) [From a Binary Distribution \(Optional\)](#page-10-0). If you want to build mecab and mecab-ipadic from source, see [Building MeCab From Source \(Optional\).](#page-11-0)

On Windows, libmecab.dll is found in the MySQL bin directory. mecab-ipadic is located in MYSQL\_HOME/lib/mecab.

To install and configure the MeCab parser plugin, perform the following steps:

1. In the MySQL configuration file, set the mecab\_rc\_file configuration option to the location of the mecabrc configuration file, which is the configuration file for MeCab. If you are using the MeCab package distributed with MySQL, the mecabrc file is located in MYSQL\_HOME/lib/mecab/etc/.

```
[mysqld]
loose-mecab-rc-file=MYSQL_HOME/lib/mecab/etc/mecabrc
```

The loose prefix is an option modifier. The mecab\_rc\_file option is not recognized by MySQL until the MeCaB parser plugin is installed but it must be set before attempting to install the MeCaB parser plugin. The loose prefix allows you restart MySQL without encountering an error due to an unrecognized variable.

If you use your own MeCab installation, or build MeCab from source, the location of the mecabrc configuration file may differ.

For information about the MySQL configuration file and its location, see Section 6.2.2.2, "Using Option Files".

2. Also in the MySQL configuration file, set the minimum token size to 1 or 2, which are the values recommended for use with the MeCab parser. For InnoDB tables, minimum token size is defined by the innodb\_ft\_min\_token\_size configuration option, which has a default value of 3. For MyISAM tables, minimum token size is defined by ft\_min\_word\_len, which has a default value of 4.

```
[mysqld]
innodb_ft_min_token_size=1
```

3. Modify the mecabrc configuration file to specify the dictionary you want to use. The mecabipadic package distributed with MySQL binaries includes three dictionaries (ipadic\_euc-jp, ipadic\_sjis, and ipadic\_utf-8). The mecabrc configuration file packaged with MySQL contains and entry similar to the following:

```
dicdir = /path/to/mysql/lib/mecab/lib/mecab/dic/ipadic_euc-jp
```

To use the ipadic\_utf-8 dictionary, for example, modify the entry as follows:

dicdir=MYSQL\_HOME/lib/mecab/dic/ipadic\_utf-8

If you are using your own MeCab installation or have built MeCab from source, the default dicdir entry in the mecabrc file is likely to differ, as are the dictionaries and their location.

![](_page_9_Picture_3.jpeg)

### **Note**

After the MeCab parser plugin is installed, you can use the mecab\_charset status variable to view the character set used with MeCab. The three MeCab dictionaries provided with the MySQL binary support the following character sets.

- The ipadic\_euc-jp dictionary supports the ujis and eucjpms character sets.
- The ipadic\_sjis dictionary supports the sjis and cp932 character sets.
- The ipadic\_utf-8 dictionary supports the utf8mb3 and utf8mb4 character sets.

mecab\_charset only reports the first supported character set. For example, the ipadic\_utf-8 dictionary supports both utf8mb3 and utf8mb4. mecab\_charset always reports utf8 when this dictionary is in use.

- 4. Restart MySQL.
- 5. Install the MeCab parser plugin:

The MeCab parser plugin is installed using INSTALL PLUGIN. The plugin name is mecab, and the shared library name is libpluginmecab.so. For additional information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

```
INSTALL PLUGIN mecab SONAME 'libpluginmecab.so';
```

Once installed, the MeCab parser plugin loads at every normal MySQL restart.

6. Verify that the MeCab parser plugin is loaded using the SHOW PLUGINS statement.

```
mysql> SHOW PLUGINS;
```

A mecab plugin should appear in the list of plugins.

### **Creating a FULLTEXT Index that uses the MeCab Parser**

To create a FULLTEXT index that uses the mecab parser, specify WITH PARSER ngram with CREATE TABLE, ALTER TABLE, or CREATE INDEX.

This example demonstrates creating a table with a mecab FULLTEXT index, inserting sample data, and viewing tokenized data in the Information Schema INNODB\_FT\_INDEX\_CACHE table:

```
mysql> USE test;
mysql> CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT,
 FULLTEXT (title,body) WITH PARSER mecab
 ) ENGINE=InnoDB CHARACTER SET utf8mb4;
mysql> SET NAMES utf8mb4;
mysql> INSERT INTO articles (title,body) VALUES
```

```
 ('データベース管理','このチュートリアルでは、私はどのようにデータベースを管理する方法を紹介します'),
 ('データベースアプリケーション開発','データベースアプリケーションを開発することを学ぶ');
mysql> SET GLOBAL innodb_ft_aux_table="test/articles";
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_CACHE ORDER BY doc_id, position;
```

To add a FULLTEXT index to an existing table, you can use ALTER TABLE or CREATE INDEX. For example:

```
CREATE TABLE articles (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
 title VARCHAR(200),
 body TEXT
 ) ENGINE=InnoDB CHARACTER SET utf8mb4;
ALTER TABLE articles ADD FULLTEXT INDEX ft_index (title,body) WITH PARSER mecab;
# Or:
CREATE FULLTEXT INDEX ft_index ON articles (title,body) WITH PARSER mecab;
```

### **MeCab Parser Space Handling**

The MeCab parser uses spaces as separators in query strings. For example, the MeCab parser tokenizes データベース管理 as データベース and 管理.

## **MeCab Parser Stopword Handling**

By default, the MeCab parser uses the default stopword list, which contains a short list of English stopwords. For a stopword list applicable to Japanese, you must create your own. For information about creating stopword lists, see Section 14.9.4, "Full-Text Stopwords".

### **MeCab Parser Term Search**

For natural language mode search, the search term is converted to a union of tokens. For example, データベース管理 is converted to データベース 管理.

```
SELECT COUNT(*) FROM articles 
 WHERE MATCH(title,body) AGAINST('データベース管理' IN NATURAL LANGUAGE MODE);
```

For boolean mode search, the search term is converted to a search phrase. For example, データベース管理 is converted to データベース 管理.

```
SELECT COUNT(*) FROM articles 
 WHERE MATCH(title,body) AGAINST('データベース管理' IN BOOLEAN MODE);
```

## **MeCab Parser Wildcard Search**

Wildcard search terms are not tokenized. A search on データベース管理\* is performed on the prefix, データベース管理.

```
SELECT COUNT(*) FROM articles 
 WHERE MATCH(title,body) AGAINST('データベース*' IN BOOLEAN MODE);
```

### **MeCab Parser Phrase Search**

Phrases are tokenized. For example, データベース管理 is tokenized as データベース 管理.

```
SELECT COUNT(*) FROM articles 
 WHERE MATCH(title,body) AGAINST('"データベース管理"' IN BOOLEAN MODE);
```

### <span id="page-10-0"></span>**Installing MeCab From a Binary Distribution (Optional)**

This section describes how to install mecab and mecab-ipadic from a binary distribution using a native package management utility. For example, on Fedora, you can use Yum to perform the installation:

```
$> yum mecab-devel
```

On Debian or Ubuntu, you can perform an APT installation:

```
$> apt-get install mecab
$> apt-get install mecab-ipadic
```

### <span id="page-11-0"></span>**Installing MeCab From Source (Optional)**

If you want to build mecab and mecab-ipadic from source, basic installation steps are provided below. For additional information, refer to the MeCab documentation.

- 1. Download the tar.gz packages for mecab and mecab-ipadic from [http://taku910.github.io/mecab/](http://taku910.github.io/mecab/#download) [#download](http://taku910.github.io/mecab/#download). As of February, 2016, the latest available packages are mecab-0.996.tar.gz and mecab-ipadic-2.7.0-20070801.tar.gz.
- 2. Install mecab:

```
$> tar zxfv mecab-0.996.tar
$> cd mecab-0.996
$> ./configure
$> make
$> make check
$> su
$> make install
```

3. Install mecab-ipadic:

```
$> tar zxfv mecab-ipadic-2.7.0-20070801.tar
$> cd mecab-ipadic-2.7.0-20070801
$> ./configure
$> make
$> su
$> make install
```

4. Compile MySQL using the WITH\_MECAB CMake option. Set the WITH\_MECAB option to system if you have installed mecab and mecab-ipadic to the default location.

```
-DWITH_MECAB=system
```

If you defined a custom installation directory, set WITH\_MECAB to the custom directory. For example:

```
-DWITH_MECAB=/path/to/mecab
```