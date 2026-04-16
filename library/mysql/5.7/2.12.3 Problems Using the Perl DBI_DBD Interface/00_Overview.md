---
source: MySQL 5.7 Reference
title: 00_Overview
---

If Perl reports that it cannot find the ../mysql/mysql.so module, the problem is probably that Perl cannot locate the libmysqlclient.so shared library. You should be able to fix this problem by one of the following methods:

- Copy libmysqlclient.so to the directory where your other shared libraries are located (probably /usr/lib or /lib).
- Modify the -L options used to compile DBD::mysql to reflect the actual location of libmysqlclient.so.
- On Linux, you can add the path name of the directory where libmysqlclient.so is located to the /etc/ld.so.conf file.
- Add the path name of the directory where libmysqlclient.so is located to the LD\_RUN\_PATH environment variable. Some systems use LD\_LIBRARY\_PATH instead.

Note that you may also need to modify the -L options if there are other libraries that the linker fails to find. For example, if the linker cannot find libc because it is in /lib and the link command specifies - L/usr/lib, change the -L option to -L/lib or add -L/lib to the existing link command.

If you get the following errors from DBD::mysql, you are probably using gcc (or using an old binary compiled with gcc):

```
/usr/bin/perl: can't resolve symbol '__moddi3'
/usr/bin/perl: can't resolve symbol '__divdi3'
```

Add -L/usr/lib/gcc-lib/... -lgcc to the link command when the mysql.so library gets built (check the output from make for mysql.so when you compile the Perl client). The -L option should specify the path name of the directory where libgcc.a is located on your system.

Another cause of this problem may be that Perl and MySQL are not both compiled with gcc. In this case, you can solve the mismatch by compiling both with gcc.

# Chapter 3 Tutorial

# **Table of Contents**

| 3.1 Connecting to and Disconnecting from the Server 249               |     |
|-----------------------------------------------------------------------|-----|
| 3.2 Entering Queries 250                                              |     |
| 3.3 Creating and Using a Database 253                                 |     |
| 3.3.1 Creating and Selecting a Database 254                           |     |
| 3.3.2 Creating a Table 255                                            |     |
| 3.3.3 Loading Data into a Table 256                                   |     |
| 3.3.4 Retrieving Information from a Table 257                         |     |
| 3.4 Getting Information About Databases and Tables 270                |     |
| 3.5 Using mysql in Batch Mode 271                                     |     |
| 3.6 Examples of Common Queries 272                                    |     |
| 3.6.1 The Maximum Value for a Column 273                              |     |
| 3.6.2 The Row Holding the Maximum of a Certain Column                 | 273 |
| 3.6.3 Maximum of Column per Group 273                                 |     |
| 3.6.4 The Rows Holding the Group-wise Maximum of a Certain Column 274 |     |
| 3.6.5 Using User-Defined Variables 274                                |     |
| 3.6.6 Using Foreign Keys 275                                          |     |
| 3.6.7 Searching on Two Keys 277                                       |     |
| 3.6.8 Calculating Visits Per Day                                      | 277 |
| 3.6.9 Using AUTO_INCREMENT 278                                        |     |
| 3.7 Using MySQL with Apache 280                                       |     |
|                                                                       |     |

This chapter provides a tutorial introduction to MySQL by showing how to use the [mysql](#page-191-0) client program to create and use a simple database. [mysql](#page-191-0) (sometimes referred to as the "terminal monitor" or just "monitor") is an interactive program that enables you to connect to a MySQL server, run queries, and view the results. [mysql](#page-191-0) may also be used in batch mode: you place your queries in a file beforehand, then tell [mysql](#page-191-0) to execute the contents of the file. Both ways of using [mysql](#page-191-0) are covered here.

To see a list of options provided by [mysql](#page-191-0), invoke it with the [--help](#page-197-0) option:

```
$> mysql --help
```

This chapter assumes that [mysql](#page-191-0) is installed on your machine and that a MySQL server is available to which you can connect. If this is not true, contact your MySQL administrator. (If you are the administrator, you need to consult the relevant portions of this manual, such as Chapter 5, MySQL Server Administration.)

This chapter describes the entire process of setting up and using a database. If you are interested only in accessing an existing database, you may want to skip the sections that describe how to create the database and the tables it contains.

Because this chapter is tutorial in nature, many details are necessarily omitted. Consult the relevant sections of the manual for more information on the topics covered here.

# <span id="page-76-0"></span>**3.1 Connecting to and Disconnecting from the Server**

To connect to the server, you usually need to provide a MySQL user name when you invoke [mysql](#page-191-0) and, most likely, a password. If the server runs on a machine other than the one where you log in, you also need to specify a host name. Contact your administrator to find out what connection parameters you should use to connect (that is, what host, user name, and password to use). Once you know the proper parameters, you should be able to connect like this:

```
$> mysql -h host -u user -p
Enter password: ********
```

host and user represent the host name where your MySQL server is running and the user name of your MySQL account. Substitute appropriate values for your setup. The \*\*\*\*\*\*\*\* represents your password; enter it when [mysql](#page-191-0) displays the Enter password: prompt.

If that works, you should see some introductory information followed by a mysql> prompt:

```
$> mysql -h host -u user -p
Enter password: ********
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 25338 to server version: 5.7.44-standard
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql>
```

The mysql> prompt tells you that [mysql](#page-191-0) is ready for you to enter SQL statements.

If you are logging in on the same machine that MySQL is running on, you can omit the host, and simply use the following:

```
$> mysql -u user -p
```

If, when you attempt to log in, you get an error message such as ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2), it means that the MySQL server daemon (Unix) or service (Windows) is not running. Consult the administrator or see the section of Chapter 2, Installing and Upgrading MySQL that is appropriate to your operating system.

For help with other problems often encountered when trying to log in, see Section B.3.2, "Common Errors When Using MySQL Programs".

Some MySQL installations permit users to connect as the anonymous (unnamed) user to the server running on the local host. If this is the case on your machine, you should be able to connect to that server by invoking [mysql](#page-191-0) without any options:

```
$> mysql
```

After you have connected successfully, you can disconnect any time by typing QUIT (or \q) at the mysql> prompt:

```
mysql> QUIT
Bye
```

On Unix, you can also disconnect by pressing Control+D.

Most examples in the following sections assume that you are connected to the server. They indicate this by the mysql> prompt.

# <span id="page-77-0"></span>**3.2 Entering Queries**

Make sure that you are connected to the server, as discussed in the previous section. Doing so does not in itself select any database to work with, but that is okay. At this point, it is more important to find out a little about how to issue queries than to jump right in creating tables, loading data into them, and retrieving data from them. This section describes the basic principles of entering queries, using several queries you can try out to familiarize yourself with how [mysql](#page-191-0) works.

Here is a simple query that asks the server to tell you its version number and the current date. Type it in as shown here following the mysql> prompt and press Enter:

```
mysql> SELECT VERSION(), CURRENT_DATE;
```

```
+--------------+--------------+
| VERSION() | CURRENT_DATE |
+--------------+--------------+
| 5.7.1-m4-log | 2012-12-25 |
+--------------+--------------+
1 row in set (0.01 sec)
mysql>
```

This query illustrates several things about [mysql](#page-191-0):

- A query normally consists of an SQL statement followed by a semicolon. (There are some exceptions where a semicolon may be omitted. QUIT, mentioned earlier, is one of them. We'll get to others later.)
- When you issue a query, [mysql](#page-191-0) sends it to the server for execution and displays the results, then prints another mysql> prompt to indicate that it is ready for another query.
- [mysql](#page-191-0) displays query output in tabular form (rows and columns). The first row contains labels for the columns. The rows following are the query results. Normally, column labels are the names of the columns you fetch from database tables. If you're retrieving the value of an expression rather than a table column (as in the example just shown), [mysql](#page-191-0) labels the column using the expression itself.
- [mysql](#page-191-0) shows how many rows were returned and how long the query took to execute, which gives you a rough idea of server performance. These values are imprecise because they represent wall clock time (not CPU or machine time), and because they are affected by factors such as server load and network latency. (For brevity, the "rows in set" line is sometimes not shown in the remaining examples in this chapter.)

Keywords may be entered in any lettercase. The following queries are equivalent:

```
mysql> SELECT VERSION(), CURRENT_DATE;
mysql> select version(), current_date;
mysql> SeLeCt vErSiOn(), current_DATE;
```

Here is another query. It demonstrates that you can use [mysql](#page-191-0) as a simple calculator:

```
mysql> SELECT SIN(PI()/4), (4+1)*5;
+------------------+---------+
| SIN(PI()/4) | (4+1)*5 |
+------------------+---------+
| 0.70710678118655 | 25 |
+------------------+---------+
1 row in set (0.02 sec)
```

The queries shown thus far have been relatively short, single-line statements. You can even enter multiple statements on a single line. Just end each one with a semicolon:

```
mysql> SELECT VERSION(); SELECT NOW();
+------------------+
| VERSION() |
+------------------+
| 5.7.10-ndb-7.5.1 |
+------------------+
1 row in set (0.00 sec)
+---------------------+
| NOW() |
+---------------------+
| 2016-01-29 18:02:55 |
+---------------------+
1 row in set (0.00 sec)
```

A query need not be given all on a single line, so lengthy queries that require several lines are not a problem. [mysql](#page-191-0) determines where your statement ends by looking for the terminating semicolon, not by looking for the end of the input line. (In other words, [mysql](#page-191-0) accepts free-format input: it collects input lines but does not execute them until it sees the semicolon.)

Here is a simple multiple-line statement:

```
mysql> SELECT
 -> USER()
 -> ,
 -> CURRENT_DATE;
+---------------+--------------+
| USER() | CURRENT_DATE |
+---------------+--------------+
| jon@localhost | 2010-08-06 |
+---------------+--------------+
```

In this example, notice how the prompt changes from mysql> to -> after you enter the first line of a multiple-line query. This is how [mysql](#page-191-0) indicates that it has not yet seen a complete statement and is waiting for the rest. The prompt is your friend, because it provides valuable feedback. If you use that feedback, you can always be aware of what [mysql](#page-191-0) is waiting for.

If you decide you do not want to execute a query that you are in the process of entering, cancel it by typing \c:

```
mysql> SELECT
 -> USER()
 -> \c
mysql>
```

Here, too, notice the prompt. It switches back to mysql> after you type \c, providing feedback to indicate that [mysql](#page-191-0) is ready for a new query.

The following table shows each of the prompts you may see and summarizes what they mean about the state that [mysql](#page-191-0) is in.

| Prompt | Meaning                                                                                          |
|--------|--------------------------------------------------------------------------------------------------|
| mysql> | Ready for new query                                                                              |
| ->     | Waiting for next line of multiple-line query                                                     |
| '>     | Waiting for next line, waiting for completion of a<br>string that began with a single quote (')  |
| ">     | Waiting for next line, waiting for completion of a<br>string that began with a double quote (")  |
| `>     | Waiting for next line, waiting for completion of an<br>identifier that began with a backtick (`) |
| /*>    | Waiting for next line, waiting for completion of a<br>comment that began with /*                 |

Multiple-line statements commonly occur by accident when you intend to issue a query on a single line, but forget the terminating semicolon. In this case, [mysql](#page-191-0) waits for more input:

```
mysql> SELECT USER()
 ->
```

If this happens to you (you think you've entered a statement but the only response is a -> prompt), most likely [mysql](#page-191-0) is waiting for the semicolon. If you don't notice what the prompt is telling you, you might sit there for a while before realizing what you need to do. Enter a semicolon to complete the statement, and [mysql](#page-191-0) executes it:

```
mysql> SELECT USER()
 -> ;
+---------------+
| USER() |
+---------------+
| jon@localhost |
+---------------+
```

The '> and "> prompts occur during string collection (another way of saying that MySQL is waiting for completion of a string). In MySQL, you can write strings surrounded by either ' or " characters (for example, 'hello' or "goodbye"), and [mysql](#page-191-0) lets you enter strings that span multiple lines. When you see a '> or "> prompt, it means that you have entered a line containing a string that begins with a ' or " quote character, but have not yet entered the matching quote that terminates the string. This often indicates that you have inadvertently left out a quote character. For example:

```
mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
 '>
```

If you enter this SELECT statement, then press **Enter** and wait for the result, nothing happens. Instead of wondering why this query takes so long, notice the clue provided by the '> prompt. It tells you that [mysql](#page-191-0) expects to see the rest of an unterminated string. (Do you see the error in the statement? The string 'Smith is missing the second single quotation mark.)

At this point, what do you do? The simplest thing is to cancel the query. However, you cannot just type \c in this case, because [mysql](#page-191-0) interprets it as part of the string that it is collecting. Instead, enter the closing quote character (so [mysql](#page-191-0) knows you've finished the string), then type \c:

```
mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
 '> '\c
mysql>
```

The prompt changes back to mysql>, indicating that [mysql](#page-191-0) is ready for a new query.

The `> prompt is similar to the '> and "> prompts, but indicates that you have begun but not completed a backtick-quoted identifier.

It is important to know what the '>, ">, and `> prompts signify, because if you mistakenly enter an unterminated string, any further lines you type appear to be ignored by [mysql](#page-191-0)—including a line containing QUIT. This can be quite confusing, especially if you do not know that you need to supply the terminating quote before you can cancel the current query.

![](_page_80_Picture_9.jpeg)

#### **Note**

Multiline statements from this point on are written without the secondary (-> or other) prompts, to make it easier to copy and paste the statements to try for yourself.

# <span id="page-80-0"></span>**3.3 Creating and Using a Database**

Once you know how to enter SQL statements, you are ready to access a database.

Suppose that you have several pets in your home (your menagerie) and you would like to keep track of various types of information about them. You can do so by creating tables to hold your data and loading them with the desired information. Then you can answer different sorts of questions about your animals by retrieving data from the tables. This section shows you how to perform the following operations:

- Create a database
- Create a table
- Load data into the table
- Retrieve data from the table in various ways
- Use multiple tables

The menagerie database is simple (deliberately), but it is not difficult to think of real-world situations in which a similar type of database might be used. For example, a database like this could be used by a farmer to keep track of livestock, or by a veterinarian to keep track of patient records. A menagerie distribution containing some of the queries and sample data used in the following sections can be obtained from the MySQL website. It is available in both compressed tar file and Zip formats at [https://](https://dev.mysql.com/doc/) [dev.mysql.com/doc/](https://dev.mysql.com/doc/).

Use the SHOW statement to find out what databases currently exist on the server:

```
mysql> SHOW DATABASES;
+----------+
| Database |
+----------+
| mysql |
| test |
| tmp |
+----------+
```

The mysql database describes user access privileges. The test database often is available as a workspace for users to try things out.

The list of databases displayed by the statement may be different on your machine; SHOW DATABASES does not show databases that you have no privileges for if you do not have the SHOW DATABASES privilege. See Section 13.7.5.14, "SHOW DATABASES Statement".

If the test database exists, try to access it:

```
mysql> USE test
Database changed
```

USE, like QUIT, does not require a semicolon. (You can terminate such statements with a semicolon if you like; it does no harm.) The USE statement is special in another way, too: it must be given on a single line.

You can use the test database (if you have access to it) for the examples that follow, but anything you create in that database can be removed by anyone else with access to it. For this reason, you should probably ask your MySQL administrator for permission to use a database of your own. Suppose that you want to call yours menagerie. The administrator needs to execute a statement like this:

```
mysql> GRANT ALL ON menagerie.* TO 'your_mysql_name'@'your_client_host';
```

where your\_mysql\_name is the MySQL user name assigned to you and your\_client\_host is the host from which you connect to the server.

## <span id="page-81-0"></span>**3.3.1 Creating and Selecting a Database**

If the administrator creates your database for you when setting up your permissions, you can begin using it. Otherwise, you need to create it yourself:

```
mysql> CREATE DATABASE menagerie;
```

Under Unix, database names are case-sensitive (unlike SQL keywords), so you must always refer to your database as menagerie, not as Menagerie, MENAGERIE, or some other variant. This is also true for table names. (Under Windows, this restriction does not apply, although you must refer to databases and tables using the same lettercase throughout a given query. However, for a variety of reasons, the recommended best practice is always to use the same lettercase that was used when the database was created.)

![](_page_81_Picture_16.jpeg)

## **Note**

If you get an error such as ERROR 1044 (42000): Access denied for user 'micah'@'localhost' to database 'menagerie' when attempting to create a database, this means that your user account does not have the necessary privileges to do so. Discuss this with the administrator or see Section 6.2, "Access Control and Account Management".

Creating a database does not select it for use; you must do that explicitly. To make menagerie the current database, use this statement:

```
mysql> USE menagerie
Database changed
```

Your database needs to be created only once, but you must select it for use each time you begin a [mysql](#page-191-0) session. You can do this by issuing a USE statement as shown in the example. Alternatively, you can select the database on the command line when you invoke [mysql](#page-191-0). Just specify its name after any connection parameters that you might need to provide. For example:

```
$> mysql -h host -u user -p menagerie
Enter password: ********
```

![](_page_82_Picture_5.jpeg)

#### **Important**

menagerie in the command just shown is **not** your password. If you want to supply your password on the command line after the -p option, you must do so with no intervening space (for example, as -ppassword, not as -p password). However, putting your password on the command line is not recommended, because doing so exposes it to snooping by other users logged in on your machine.

![](_page_82_Picture_8.jpeg)

#### **Note**

You can see at any time which database is currently selected using SELECT DATABASE().

## <span id="page-82-0"></span>**3.3.2 Creating a Table**

Creating the database is the easy part, but at this point it is empty, as SHOW TABLES tells you:

```
mysql> SHOW TABLES;
Empty set (0.00 sec)
```

The harder part is deciding what the structure of your database should be: what tables you need and what columns should be in each of them.

You want a table that contains a record for each of your pets. This can be called the pet table, and it should contain, as a bare minimum, each animal's name. Because the name by itself is not very interesting, the table should contain other information. For example, if more than one person in your family keeps pets, you might want to list each animal's owner. You might also want to record some basic descriptive information such as species and sex.

How about age? That might be of interest, but it is not a good thing to store in a database. Age changes as time passes, which means you'd have to update your records often. Instead, it is better to store a fixed value such as date of birth. Then, whenever you need age, you can calculate it as the difference between the current date and the birth date. MySQL provides functions for doing date arithmetic, so this is not difficult. Storing birth date rather than age has other advantages, too:

- You can use the database for tasks such as generating reminders for upcoming pet birthdays. (If you think this type of query is somewhat silly, note that it is the same question you might ask in the context of a business database to identify clients to whom you need to send out birthday greetings in the current week or month, for that computer-assisted personal touch.)
- You can calculate age in relation to dates other than the current date. For example, if you store death date in the database, you can easily calculate how old a pet was when it died.

You can probably think of other types of information that would be useful in the pet table, but the ones identified so far are sufficient: name, owner, species, sex, birth, and death.

Use a CREATE TABLE statement to specify the layout of your table:

```
mysql> CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
 species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
```

VARCHAR is a good choice for the name, owner, and species columns because the column values vary in length. The lengths in those column definitions need not all be the same, and need not be 20. You can normally pick any length from 1 to 65535, whatever seems most reasonable to you. If you make a poor choice and it turns out later that you need a longer field, MySQL provides an ALTER TABLE statement.

Several types of values can be chosen to represent sex in animal records, such as 'm' and 'f', or perhaps 'male' and 'female'. It is simplest to use the single characters 'm' and 'f'.

The use of the DATE data type for the birth and death columns is a fairly obvious choice.

Once you have created a table, SHOW TABLES should produce some output:

```
mysql> SHOW TABLES;
+---------------------+
| Tables in menagerie |
+---------------------+
| pet |
+---------------------+
```

To verify that your table was created the way you expected, use a DESCRIBE statement:

```
mysql> DESCRIBE pet;
+---------+-------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| name | varchar(20) | YES | | NULL | |
| owner | varchar(20) | YES | | NULL | |
| species | varchar(20) | YES | | NULL | |
| sex | char(1) | YES | | NULL | |
| birth | date | YES | | NULL | |
| death | date | YES | | NULL | |
+---------+-------------+------+-----+---------+-------+
```

You can use DESCRIBE any time, for example, if you forget the names of the columns in your table or what types they have.

For more information about MySQL data types, see Chapter 11, Data Types.

# <span id="page-83-0"></span>**3.3.3 Loading Data into a Table**

After creating your table, you need to populate it. The LOAD DATA and INSERT statements are useful for this.

Suppose that your pet records can be described as shown here. (Observe that MySQL expects dates in 'YYYY-MM-DD' format; this may differ from what you are used to.)

| name     | owner  | species | sex | birth      | death      |
|----------|--------|---------|-----|------------|------------|
| Fluffy   | Harold | cat     | f   | 1993-02-04 |            |
| Claws    | Gwen   | cat     | m   | 1994-03-17 |            |
| Buffy    | Harold | dog     | f   | 1989-05-13 |            |
| Fang     | Benny  | dog     | m   | 1990-08-27 |            |
| Bowser   | Diane  | dog     | m   | 1979-08-31 | 1995-07-29 |
| Chirpy   | Gwen   | bird    | f   | 1998-09-11 |            |
| Whistler | Gwen   | bird    |     | 1997-12-09 |            |
| Slim     | Benny  | snake   | m   | 1996-04-29 |            |

Because you are beginning with an empty table, an easy way to populate it is to create a text file containing a row for each of your animals, then load the contents of the file into the table with a single statement.

You could create a text file pet.txt containing one record per line, with values separated by tabs, and given in the order in which the columns were listed in the CREATE TABLE statement. For missing values (such as unknown sexes or death dates for animals that are still living), you can use NULL values. To represent these in your text file, use \N (backslash, capital-N). For example, the record for Whistler the bird would look like this (where the whitespace between values is a single tab character):

```
Whistler Gwen bird \N 1997-12-09 \N
```

To load the text file pet.txt into the pet table, use this statement:

```
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```

If you created the file on Windows with an editor that uses \r\n as a line terminator, you should use this statement instead:

```
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet
 LINES TERMINATED BY '\r\n';
```

(On an Apple machine running macOS, you would likely want to use LINES TERMINATED BY '\r'.)

You can specify the column value separator and end of line marker explicitly in the LOAD DATA statement if you wish, but the defaults are tab and linefeed. These are sufficient for the statement to read the file pet.txt properly.

If the statement fails, it is likely that your MySQL installation does not have local file capability enabled by default. See Section 6.1.6, "Security Considerations for LOAD DATA LOCAL", for information on how to change this.

When you want to add new records one at a time, the INSERT statement is useful. In its simplest form, you supply values for each column, in the order in which the columns were listed in the CREATE TABLE statement. Suppose that Diane gets a new hamster named "Puffball." You could add a new record using an INSERT statement like this:

```
mysql> INSERT INTO pet
 VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);
```

String and date values are specified as quoted strings here. Also, with INSERT, you can insert NULL directly to represent a missing value. You do not use \N like you do with LOAD DATA.

From this example, you should be able to see that there would be a lot more typing involved to load your records initially using several INSERT statements rather than a single LOAD DATA statement.

# <span id="page-84-0"></span>**3.3.4 Retrieving Information from a Table**

The SELECT statement is used to pull information from a table. The general form of the statement is:

```
SELECT what_to_select
FROM which_table
WHERE conditions_to_satisfy;
```

what\_to\_select indicates what you want to see. This can be a list of columns, or \* to indicate "all columns." which\_table indicates the table from which you want to retrieve data. The WHERE clause is optional. If it is present, conditions\_to\_satisfy specifies one or more conditions that rows must satisfy to qualify for retrieval.

### **3.3.4.1 Selecting All Data**

The simplest form of SELECT retrieves everything from a table:

```
mysql> SELECT * FROM pet;
+----------+--------+---------+------+------------+------------+
| name | owner | species | sex | birth | death |
+----------+--------+---------+------+------------+------------+
| Fluffy | Harold | cat | f | 1993-02-04 | NULL |
| Claws | Gwen | cat | m | 1994-03-17 | NULL |
| Buffy | Harold | dog | f | 1989-05-13 | NULL |
| Fang | Benny | dog | m | 1990-08-27 | NULL |
| Bowser | Diane | dog | m | 1979-08-31 | 1995-07-29 |
| Chirpy | Gwen | bird | f | 1998-09-11 | NULL |
| Whistler | Gwen | bird | NULL | 1997-12-09 | NULL |
| Slim | Benny | snake | m | 1996-04-29 | NULL |
| Puffball | Diane | hamster | f | 1999-03-30 | NULL |
+----------+--------+---------+------+------------+------------+
```

This form of SELECT uses \*, which is shorthand for "select all columns." This is useful if you want to review your entire table, for example, after you've just loaded it with your initial data set. For example, you may happen to think that the birth date for Bowser does not seem quite right. Consulting your original pedigree papers, you find that the correct birth year should be 1989, not 1979.

There are at least two ways to fix this:

• Edit the file pet.txt to correct the error, then empty the table and reload it using DELETE and LOAD DATA:

```
mysql> DELETE FROM pet;
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```

However, if you do this, you must also re-enter the record for Puffball.

• Fix only the erroneous record with an UPDATE statement:

```
mysql> UPDATE pet SET birth = '1989-08-31' WHERE name = 'Bowser';
```

The UPDATE changes only the record in question and does not require you to reload the table.

### **3.3.4.2 Selecting Particular Rows**

As shown in the preceding section, it is easy to retrieve an entire table. Just omit the WHERE clause from the SELECT statement. But typically you don't want to see the entire table, particularly when it becomes large. Instead, you're usually more interested in answering a particular question, in which case you specify some constraints on the information you want. Let's look at some selection queries in terms of questions about your pets that they answer.

You can select only particular rows from your table. For example, if you want to verify the change that you made to Bowser's birth date, select Bowser's record like this:

```
mysql> SELECT * FROM pet WHERE name = 'Bowser';
+--------+-------+---------+------+------------+------------+
| name | owner | species | sex | birth | death |
+--------+-------+---------+------+------------+------------+
| Bowser | Diane | dog | m | 1989-08-31 | 1995-07-29 |
+--------+-------+---------+------+------------+------------+
```

The output confirms that the year is correctly recorded as 1989, not 1979.

String comparisons normally are case-insensitive, so you can specify the name as 'bowser', 'BOWSER', and so forth. The query result is the same.

You can specify conditions on any column, not just name. For example, if you want to know which animals were born during or after 1998, test the birth column:

```
mysql> SELECT * FROM pet WHERE birth >= '1998-1-1';
+----------+-------+---------+------+------------+-------+
| name | owner | species | sex | birth | death |
+----------+-------+---------+------+------------+-------+
```

```
| Chirpy | Gwen | bird | f | 1998-09-11 | NULL |
| Puffball | Diane | hamster | f | 1999-03-30 | NULL |
+----------+-------+---------+------+------------+-------+
```

You can combine conditions, for example, to locate female dogs:

```
mysql> SELECT * FROM pet WHERE species = 'dog' AND sex = 'f';
+-------+--------+---------+------+------------+-------+
| name | owner | species | sex | birth | death |
+-------+--------+---------+------+------------+-------+
| Buffy | Harold | dog | f | 1989-05-13 | NULL |
+-------+--------+---------+------+------------+-------+
```

The preceding query uses the AND logical operator. There is also an OR operator:

```
mysql> SELECT * FROM pet WHERE species = 'snake' OR species = 'bird';
+----------+-------+---------+------+------------+-------+
| name | owner | species | sex | birth | death |
+----------+-------+---------+------+------------+-------+
| Chirpy | Gwen | bird | f | 1998-09-11 | NULL |
| Whistler | Gwen | bird | NULL | 1997-12-09 | NULL |
| Slim | Benny | snake | m | 1996-04-29 | NULL |
+----------+-------+---------+------+------------+-------+
```

AND and OR may be intermixed, although AND has higher precedence than OR. If you use both operators, it is a good idea to use parentheses to indicate explicitly how conditions should be grouped:

```
mysql> SELECT * FROM pet WHERE (species = 'cat' AND sex = 'm')
 OR (species = 'dog' AND sex = 'f');
+-------+--------+---------+------+------------+-------+
| name | owner | species | sex | birth | death |
+-------+--------+---------+------+------------+-------+
| Claws | Gwen | cat | m | 1994-03-17 | NULL |
| Buffy | Harold | dog | f | 1989-05-13 | NULL |
+-------+--------+---------+------+------------+-------+
```