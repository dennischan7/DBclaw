---
source: MySQL 8.0 Reference
title: 00_Overview
---

The [mysql](#page-77-0) client typically is used interactively, like this:

```
mysql db_name
```

However, it is also possible to put your SQL statements in a file and then tell [mysql](#page-77-0) to read its input from that file. To do so, create a text file text\_file that contains the statements you wish to execute. Then invoke [mysql](#page-77-0) as shown here:

```
mysql db_name < text_file
```

If you place a USE db\_name statement as the first statement in the file, it is unnecessary to specify the database name on the command line:

```
mysql < text_file
```

If you are already running [mysql](#page-77-0), you can execute an SQL script file using the source command or \. command:

```
mysql> source file_name
mysql> \. file_name
```

Sometimes you may want your script to display progress information to the user. For this you can insert statements like this:

```
SELECT '<info_to_display>' AS ' ';
```

The statement shown outputs <info\_to\_display>.

You can also invoke [mysql](#page-77-0) with the [--verbose](#page-105-3) option, which causes each statement to be displayed before the result that it produces.

[mysql](#page-77-0) ignores Unicode byte order mark (BOM) characters at the beginning of input files. Previously, it read them and sent them to the server, resulting in a syntax error. Presence of a BOM does not cause [mysql](#page-77-0) to change its default character set. To do that, invoke [mysql](#page-77-0) with an option such as [-](#page-89-0) [default-character-set=utf8mb4](#page-89-0).

For more information about batch mode, see Section 5.5, "Using mysql in Batch Mode".