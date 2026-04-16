---
source: MySQL 8.0 Reference
title: 00_Overview
---

### **Table 14.16 XML Functions**

| Name           | Description                                                |
|----------------|------------------------------------------------------------|
| ExtractValue() | Extract a value from an XML string using XPath<br>notation |
| UpdateXML()    | Return replaced XML fragment                               |

This section discusses XML and related functionality in MySQL.

![](_page_25_Picture_12.jpeg)

### **Note**

It is possible to obtain XML-formatted output from MySQL in the mysql and mysqldump clients by invoking them with the --xml option. See Section 6.5.1, "mysql — The MySQL Command-Line Client", and Section 6.5.4, "mysqldump — A Database Backup Program".

Two functions providing basic XPath 1.0 (XML Path Language, version 1.0) capabilities are available. Some basic information about XPath syntax and usage is provided later in this section; however, an in-depth discussion of these topics is beyond the scope of this manual, and you should refer to the [XML Path Language \(XPath\) 1.0 standard](http://www.w3.org/TR/xpath) for definitive information. A useful resource for those new to XPath or who desire a refresher in the basics is the [Zvon.org XPath Tutorial,](http://www.zvon.org/xxl/XPathTutorial/) which is available in several languages.

![](_page_25_Picture_16.jpeg)

### **Note**

These functions remain under development. We continue to improve these and other aspects of XML and XPath functionality in MySQL 8.0 and onwards. You may discuss these, ask questions about them, and obtain help from other users with them in the [MySQL XML User Forum](https://forums.mysql.com/list.php?44).

XPath expressions used with these functions support user variables and local stored program variables. User variables are weakly checked; variables local to stored programs are strongly checked (see also Bug #26518):

• **User variables (weak checking).** Variables using the syntax \$@variable\_name (that is, user variables) are not checked. No warnings or errors are issued by the server if a variable has the wrong type or has previously not been assigned a value. This also means the user is fully responsible for any typographical errors, since no warnings are given if (for example) \$@myvairable is used where \$@myvariable was intended.

### Example:

```
mysql> SET @xml = '<a><b>X</b><b>Y</b></a>';
Query OK, 0 rows affected (0.00 sec)
mysql> SET @i =1, @j = 2;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @i, ExtractValue(@xml, '//b[$@i]');
+------+--------------------------------+
| @i | ExtractValue(@xml, '//b[$@i]') |
+------+--------------------------------+
| 1 | X |
+------+--------------------------------+
1 row in set (0.00 sec)
mysql> SELECT @j, ExtractValue(@xml, '//b[$@j]');
+------+--------------------------------+
| @j | ExtractValue(@xml, '//b[$@j]') |
+------+--------------------------------+
| 2 | Y |
+------+--------------------------------+
1 row in set (0.00 sec)
mysql> SELECT @k, ExtractValue(@xml, '//b[$@k]');
+------+--------------------------------+
| @k | ExtractValue(@xml, '//b[$@k]') |
+------+--------------------------------+
| NULL | |
+------+--------------------------------+
1 row in set (0.00 sec)
```

• **Variables in stored programs (strong checking).** Variables using the syntax \$variable\_name can be declared and used with these functions when they are called inside stored programs. Such variables are local to the stored program in which they are defined, and are strongly checked for type and value.

### Example:

```
mysql> DELIMITER |
mysql> CREATE PROCEDURE myproc ()
 -> BEGIN
 -> DECLARE i INT DEFAULT 1;
 -> DECLARE xml VARCHAR(25) DEFAULT '<a>X</a><a>Y</a><a>Z</a>';
 ->
 -> WHILE i < 4 DO
 -> SELECT xml, i, ExtractValue(xml, '//a[$i]');
 -> SET i = i+1;
 -> END WHILE;
 -> END |
Query OK, 0 rows affected (0.01 sec)
mysql> DELIMITER ;
mysql> CALL myproc();
+--------------------------+---+------------------------------+
| xml | i | ExtractValue(xml, '//a[$i]') |
+--------------------------+---+------------------------------+
| <a>X</a><a>Y</a><a>Z</a> | 1 | X |
+--------------------------+---+------------------------------+
1 row in set (0.00 sec)
+--------------------------+---+------------------------------+
```

```
| xml | i | ExtractValue(xml, '//a[$i]') |
+--------------------------+---+------------------------------+
| <a>X</a><a>Y</a><a>Z</a> | 2 | Y |
+--------------------------+---+------------------------------+
1 row in set (0.01 sec)
+--------------------------+---+------------------------------+
| xml | i | ExtractValue(xml, '//a[$i]') |
+--------------------------+---+------------------------------+
| <a>X</a><a>Y</a><a>Z</a> | 3 | Z |
+--------------------------+---+------------------------------+
1 row in set (0.01 sec)
```

**Parameters.** Variables used in XPath expressions inside stored routines that are passed in as parameters are also subject to strong checking.

Expressions containing user variables or variables local to stored programs must otherwise (except for notation) conform to the rules for XPath expressions containing variables as given in the XPath 1.0 specification.

![](_page_27_Picture_4.jpeg)

### **Note**

A user variable used to store an XPath expression is treated as an empty string. Because of this, it is not possible to store an XPath expression as a user variable. (Bug #32911)

<span id="page-27-0"></span>• [ExtractValue\(](#page-27-0)xml\_frag, xpath\_expr)

[ExtractValue\(\)](#page-27-0) takes two string arguments, a fragment of XML markup xml\_frag and an XPath expression xpath\_expr (also known as a locator); it returns the text (CDATA) of the first text node which is a child of the element or elements matched by the XPath expression.

Using this function is the equivalent of performing a match using the xpath\_expr after appending /text(). In other words, [ExtractValue\('<a><b>Sakila</b></a>', '/a/b'\)](#page-27-0) and [ExtractValue\('<a><b>Sakila</b></a>', '/a/b/text\(\)'\)](#page-27-0) produce the same result. If xml\_frag or xpath\_expr is NULL, the function returns NULL.

If multiple matches are found, the content of the first child text node of each matching element is returned (in the order matched) as a single, space-delimited string.

If no matching text node is found for the expression (including the implicit /text())—for whatever reason, as long as xpath\_expr is valid, and xml\_frag consists of elements which are properly nested and closed—an empty string is returned. No distinction is made between a match on an empty element and no match at all. This is by design.

If you need to determine whether no matching element was found in xml\_frag or such an element was found but contained no child text nodes, you should test the result of an expression that uses the XPath count() function. For example, both of these statements return an empty string, as shown here:

```
mysql> SELECT ExtractValue('<a><b/></a>', '/a/b');
+-------------------------------------+
| ExtractValue('<a><b/></a>', '/a/b') |
+-------------------------------------+
| |
+-------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue('<a><c/></a>', '/a/b');
+-------------------------------------+
| ExtractValue('<a><c/></a>', '/a/b') |
+-------------------------------------+
| |
+-------------------------------------+
1 row in set (0.00 sec)
```

However, you can determine whether there was actually a matching element using the following:

```
mysql> SELECT ExtractValue('<a><b/></a>', 'count(/a/b)');
+-------------------------------------+
| ExtractValue('<a><b/></a>', 'count(/a/b)') |
+-------------------------------------+
| 1 |
+-------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue('<a><c/></a>', 'count(/a/b)');
+-------------------------------------+
| ExtractValue('<a><c/></a>', 'count(/a/b)') |
+-------------------------------------+
| 0 |
+-------------------------------------+
1 row in set (0.01 sec)
```

![](_page_28_Picture_3.jpeg)

### **Important**

[ExtractValue\(\)](#page-27-0) returns only CDATA, and does not return any tags that might be contained within a matching tag, nor any of their content (see the result returned as val1 in the following example).

```
mysql> SELECT
 -> ExtractValue('<a>ccc<b>ddd</b></a>', '/a') AS val1,
 -> ExtractValue('<a>ccc<b>ddd</b></a>', '/a/b') AS val2,
 -> ExtractValue('<a>ccc<b>ddd</b></a>', '//b') AS val3,
 -> ExtractValue('<a>ccc<b>ddd</b></a>', '/b') AS val4,
 -> ExtractValue('<a>ccc<b>ddd</b><b>eee</b></a>', '//b') AS val5;
+------+------+------+------+---------+
| val1 | val2 | val3 | val4 | val5 |
+------+------+------+------+---------+
| ccc | ddd | ddd | | ddd eee |
+------+------+------+------+---------+
```

This function uses the current SQL collation for making comparisons with contains(), performing the same collation aggregation as other string functions (such as CONCAT()), in taking into account the collation coercibility of their arguments; see Section 12.8.4, "Collation Coercibility in Expressions", for an explanation of the rules governing this behavior.

(Previously, binary—that is, case-sensitive—comparison was always used.)

NULL is returned if xml\_frag contains elements which are not properly nested or closed, and a warning is generated, as shown in this example:

```
mysql> SELECT ExtractValue('<a>c</a><b', '//a');
+-----------------------------------+
| ExtractValue('<a>c</a><b', '//a') |
+-----------------------------------+
| NULL |
+-----------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1525
Message: Incorrect XML value: 'parse error at line 1 pos 11:
 END-OF-INPUT unexpected ('>' wanted)'
1 row in set (0.00 sec)
mysql> SELECT ExtractValue('<a>c</a><b/>', '//a');
+-------------------------------------+
| ExtractValue('<a>c</a><b/>', '//a') |
+-------------------------------------+
| c |
```

```
+-------------------------------------+
1 row in set (0.00 sec)
```

<span id="page-29-0"></span>• [UpdateXML\(](#page-29-0)xml\_target, xpath\_expr, new\_xml)

This function replaces a single portion of a given fragment of XML markup xml\_target with a new XML fragment new\_xml, and then returns the changed XML. The portion of xml\_target that is replaced matches an XPath expression xpath\_expr supplied by the user.

If no expression matching xpath\_expr is found, or if multiple matches are found, the function returns the original xml\_target XML fragment. All three arguments should be strings. If any of the arguments to UpdateXML() are NULL, the function returns NULL.

```
mysql> SELECT
 -> UpdateXML('<a><b>ccc</b><d></d></a>', '/a', '<e>fff</e>') AS val1,
 -> UpdateXML('<a><b>ccc</b><d></d></a>', '/b', '<e>fff</e>') AS val2,
 -> UpdateXML('<a><b>ccc</b><d></d></a>', '//b', '<e>fff</e>') AS val3,
 -> UpdateXML('<a><b>ccc</b><d></d></a>', '/a/d', '<e>fff</e>') AS val4,
 -> UpdateXML('<a><d></d><b>ccc</b><d></d></a>', '/a/d', '<e>fff</e>') AS val5
 -> \G
*************************** 1. row ***************************
val1: <e>fff</e>
val2: <a><b>ccc</b><d></d></a>
val3: <a><e>fff</e><d></d></a>
val4: <a><b>ccc</b><e>fff</e></a>
val5: <a><d></d><b>ccc</b><d></d></a>
```

![](_page_29_Picture_6.jpeg)

### **Note**

A discussion in depth of XPath syntax and usage are beyond the scope of this manual. Please see the [XML Path Language \(XPath\) 1.0 specification](http://www.w3.org/TR/xpath) for definitive information. A useful resource for those new to XPath or who are wishing a refresher in the basics is the [Zvon.org XPath Tutorial](http://www.zvon.org/xxl/XPathTutorial/), which is available in several languages.

Descriptions and examples of some basic XPath expressions follow:

• /tag

Matches <tag/> if and only if <tag/> is the root element.

Example: /a has a match in <a><b/></a> because it matches the outermost (root) tag. It does not match the inner a element in <b><a/></b> because in this instance it is the child of another element.

• /tag1/tag2

Matches <tag2/> if and only if it is a child of <tag1/>, and <tag1/> is the root element.

Example: /a/b matches the b element in the XML fragment <a><b/></a> because it is a child of the root element a. It does not have a match in <b><a/></b> because in this case, b is the root element (and hence the child of no other element). Nor does the XPath expression have a match in <a><c><b/></c></a>; here, b is a descendant of a, but not actually a child of a.

This construct is extendable to three or more elements. For example, the XPath expression /a/b/c matches the c element in the fragment <a><b><c/></b></a>.

• //tag

Matches any instance of <tag>.

Example: //a matches the a element in any of the following: <a><b><c/></b></a>; <c><a><b/ ></a></b>; <c><b><a/></b></c>.

// can be combined with /. For example, //a/b matches the b element in either of the fragments <a><b/></a> or <c><a><b/></a></c>.

![](_page_30_Picture_2.jpeg)

### **Note**

//tag is the equivalent of /descendant-or-self::\*/tag. A common error is to confuse this with /descendant-or-self::tag, although the latter expression can actually lead to very different results, as can be seen here:

```
mysql> SET @xml = '<a><b><c>w</c><b>x</b><d>y</d>z</b></a>';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @xml;
+-----------------------------------------+
| @xml |
+-----------------------------------------+
| <a><b><c>w</c><b>x</b><d>y</d>z</b></a> |
+-----------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue(@xml, '//b[1]');
+------------------------------+
| ExtractValue(@xml, '//b[1]') |
+------------------------------+
| x z |
+------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue(@xml, '//b[2]');
+------------------------------+
| ExtractValue(@xml, '//b[2]') |
+------------------------------+
| |
+------------------------------+
1 row in set (0.01 sec)
mysql> SELECT ExtractValue(@xml, '/descendant-or-self::*/b[1]');
+---------------------------------------------------+
| ExtractValue(@xml, '/descendant-or-self::*/b[1]') |
+---------------------------------------------------+
| x z |
+---------------------------------------------------+
1 row in set (0.06 sec)
mysql> SELECT ExtractValue(@xml, '/descendant-or-self::*/b[2]');
+---------------------------------------------------+
| ExtractValue(@xml, '/descendant-or-self::*/b[2]') |
+---------------------------------------------------+
| |
+---------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue(@xml, '/descendant-or-self::b[1]');
+-------------------------------------------------+
| ExtractValue(@xml, '/descendant-or-self::b[1]') |
+-------------------------------------------------+
| z |
+-------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT ExtractValue(@xml, '/descendant-or-self::b[2]');
+-------------------------------------------------+
| ExtractValue(@xml, '/descendant-or-self::b[2]') |
+-------------------------------------------------+
| x |
+-------------------------------------------------+
1 row in set (0.00 sec)
```

- The \* operator acts as a "wildcard" that matches any element. For example, the expression /\*/b matches the b element in either of the XML fragments <a><b/></a> or <c><b/></c>. However, the expression does not produce a match in the fragment <b><a/></b> because b must be a child of some other element. The wildcard may be used in any position: The expression /\*/b/\* matches any child of a b element that is itself not the root element.
- You can match any of several locators using the | (UNION) operator. For example, the expression //b|//c matches all b and c elements in the XML target.
- It is also possible to match an element based on the value of one or more of its attributes. This done using the syntax tag[@attribute="value"]. For example, the expression //b[@id="idB"] matches the second b element in the fragment <a><b id="idA"/><c/><b id="idB"/></ a>. To match against any element having attribute="value", use the XPath expression // \*[attribute="value"].

To filter multiple attribute values, simply use multiple attribute-comparison clauses in succession. For example, the expression //b[@c="x"][@d="y"] matches the element <b c="x" d="y"/> occurring anywhere in a given XML fragment.

To find elements for which the same attribute matches any of several values, you can use multiple locators joined by the | operator. For example, to match all b elements whose c attributes have either of the values 23 or 17, use the expression //b[@c="23"]|//b[@c="17"]. You can also use the logical or operator for this purpose: //b[@c="23" or @c="17"].

![](_page_31_Picture_6.jpeg)

### **Note**

The difference between or and | is that or joins conditions, while | joins result sets.

**XPath Limitations.** The XPath syntax supported by these functions is currently subject to the following limitations:

- Nodeset-to-nodeset comparison (such as '/a/b[@c=@d]') is not supported.
- All of the standard XPath comparison operators are supported. (Bug #22823)
- Relative locator expressions are resolved in the context of the root node. For example, consider the following query and result:

```
mysql> SELECT ExtractValue(
 -> '<a><b c="1">X</b><b c="2">Y</b></a>',
 -> 'a/b'
 -> ) AS result;
+--------+
| result |
+--------+
| X Y |
+--------+
1 row in set (0.03 sec)
```

In this case, the locator a/b resolves to /a/b.

Relative locators are also supported within predicates. In the following example, d[../@c="1"] is resolved as /a/b[@c="1"]/d:

```
mysql> SELECT ExtractValue(
 -> '<a>
 -> <b c="1"><d>X</d></b>
 -> <b c="2"><d>X</d></b>
 -> </a>',
 -> 'a/b/d[../@c="1"]')
 -> AS result;
+--------+
| result |
+--------+
```

```
| X |
+--------+
1 row in set (0.00 sec)
```

- Locators prefixed with expressions that evaluate as scalar values—including variable references, literals, numbers, and scalar function calls—are not permitted, and their use results in an error.
- The :: operator is not supported in combination with node types such as the following:

```
• axis::comment()
• axis::text()
• axis::processing-instructions()
```

• axis::node()

However, name tests (such as axis::name and axis::\*) are supported, as shown in these examples:

```
mysql> SELECT ExtractValue('<a><b>x</b><c>y</c></a>','/a/child::b');
+-------------------------------------------------------+
| ExtractValue('<a><b>x</b><c>y</c></a>','/a/child::b') |
+-------------------------------------------------------+
| x |
+-------------------------------------------------------+
1 row in set (0.02 sec)
mysql> SELECT ExtractValue('<a><b>x</b><c>y</c></a>','/a/child::*');
+-------------------------------------------------------+
| ExtractValue('<a><b>x</b><c>y</c></a>','/a/child::*') |
+-------------------------------------------------------+
| x y |
+-------------------------------------------------------+
1 row in set (0.01 sec)
```

- "Up-and-down" navigation is not supported in cases where the path would lead "above" the root element. That is, you cannot use expressions which match on descendants of ancestors of a given element, where one or more of the ancestors of the current element is also an ancestor of the root element (see Bug #16321).
- The following XPath functions are not supported, or have known issues as indicated:

```
• id()
```

- lang()
- local-name()
- name()
- namespace-uri()
- normalize-space()
- starts-with()
- string()
- substring-after()
- substring-before()
- translate()
- The following axes are not supported:

- following-sibling
- following
- preceding-sibling
- preceding

XPath expressions passed as arguments to [ExtractValue\(\)](#page-27-0) and [UpdateXML\(\)](#page-29-0) may contain the colon character (:) in element selectors, which enables their use with markup employing XML namespaces notation. For example:

```
mysql> SET @xml = '<a>111<b:c>222<d>333</d><e:f>444</e:f></b:c></a>';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT ExtractValue(@xml, '//e:f');
+-----------------------------+
| ExtractValue(@xml, '//e:f') |
+-----------------------------+
| 444 |
+-----------------------------+
1 row in set (0.00 sec)
mysql> SELECT UpdateXML(@xml, '//b:c', '<g:h>555</g:h>');
+--------------------------------------------+
| UpdateXML(@xml, '//b:c', '<g:h>555</g:h>') |
+--------------------------------------------+
| <a>111<g:h>555</g:h></a> |
+--------------------------------------------+
1 row in set (0.00 sec)
```

This is similar in some respects to what is permitted by [Apache Xalan](http://xalan.apache.org/) and some other parsers, and is much simpler than requiring namespace declarations or the use of the namespace-uri() and local-name() functions.

**Error handling.** For both [ExtractValue\(\)](#page-27-0) and [UpdateXML\(\)](#page-29-0), the XPath locator used must be valid and the XML to be searched must consist of elements which are properly nested and closed. If the locator is invalid, an error is generated:

```
mysql> SELECT ExtractValue('<a>c</a><b/>', '/&a');
ERROR 1105 (HY000): XPATH syntax error: '&a'
```

If xml\_frag does not consist of elements which are properly nested and closed, NULL is returned and a warning is generated, as shown in this example:

```
mysql> SELECT ExtractValue('<a>c</a><b', '//a');
+-----------------------------------+
| ExtractValue('<a>c</a><b', '//a') |
+-----------------------------------+
| NULL |
+-----------------------------------+
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1525
Message: Incorrect XML value: 'parse error at line 1 pos 11:
 END-OF-INPUT unexpected ('>' wanted)'
1 row in set (0.00 sec)
mysql> SELECT ExtractValue('<a>c</a><b/>', '//a');
+-------------------------------------+
| ExtractValue('<a>c</a><b/>', '//a') |
+-------------------------------------+
| c |
+-------------------------------------+
1 row in set (0.00 sec)
```

![](_page_34_Picture_1.jpeg)

### **Important**

The replacement XML used as the third argument to [UpdateXML\(\)](#page-29-0) is not checked to determine whether it consists solely of elements which are properly nested and closed.

**XPath Injection.** code injection occurs when malicious code is introduced into the system to gain unauthorized access to privileges and data. It is based on exploiting assumptions made by developers about the type and content of data input from users. XPath is no exception in this regard.

A common scenario in which this can happen is the case of application which handles authorization by matching the combination of a login name and password with those found in an XML file, using an XPath expression like this one:

```
//user[login/text()='neapolitan' and password/text()='1c3cr34m']/attribute::id
```

This is the XPath equivalent of an SQL statement like this one:

```
SELECT id FROM users WHERE login='neapolitan' AND password='1c3cr34m';
```

A PHP application employing XPath might handle the login process like this:

```
<?php
 $file = "users.xml";
 $login = $POST["login"];
 $password = $POST["password"];
 $xpath = "//user[login/text()=$login and password/text()=$password]/attribute::id";
 if( file_exists($file) )
 {
 $xml = simplexml_load_file($file);
 if($result = $xml->xpath($xpath))
 echo "You are now logged in as user $result[0].";
 else
 echo "Invalid login name or password.";
 }
 else
 exit("Failed to open $file.");
?>
```

No checks are performed on the input. This means that a malevolent user can "short-circuit" the test by entering ' or 1=1 for both the login name and password, resulting in \$xpath being evaluated as shown here:

```
//user[login/text()='' or 1=1 and password/text()='' or 1=1]/attribute::id
```

Since the expression inside the square brackets always evaluates as true, it is effectively the same as this one, which matches the id attribute of every user element in the XML document:

```
//user/attribute::id
```

One way in which this particular attack can be circumvented is simply by quoting the variable names to be interpolated in the definition of \$xpath, forcing the values passed from a Web form to be converted to strings:

```
$xpath = "//user[login/text()='$login' and password/text()='$password']/attribute::id";
```

This is the same strategy that is often recommended for preventing SQL injection attacks. In general, the practices you should follow for preventing XPath injection attacks are the same as for preventing SQL injection:

• Never accepted untested data from users in your application.

- Check all user-submitted data for type; reject or convert data that is of the wrong type
- Test numeric data for out of range values; truncate, round, or reject values that are out of range. Test strings for illegal characters and either strip them out or reject input containing them.
- Do not output explicit error messages that might provide an unauthorized user with clues that could be used to compromise the system; log these to a file or database table instead.

Just as SQL injection attacks can be used to obtain information about database schemas, so can XPath injection be used to traverse XML files to uncover their structure, as discussed in Amit Klein's paper [Blind XPath Injection](http://www.packetstormsecurity.org/papers/bypass/Blind_XPath_Injection_20040518.pdf) (PDF file, 46KB).

It is also important to check the output being sent back to the client. Consider what can happen when we use the MySQL [ExtractValue\(\)](#page-27-0) function:

```
mysql> SELECT ExtractValue(
 -> LOAD_FILE('users.xml'),
 -> '//user[login/text()="" or 1=1 and password/text()="" or 1=1]/attribute::id'
 -> ) AS id;
+-------------------------------+
| id |
+-------------------------------+
| 00327 13579 02403 42354 28570 |
+-------------------------------+
1 row in set (0.01 sec)
```

Because [ExtractValue\(\)](#page-27-0) returns multiple matches as a single space-delimited string, this injection attack provides every valid ID contained within users.xml to the user as a single row of output. As an extra safeguard, you should also test output before returning it to the user. Here is a simple example:

```
mysql> SELECT @id = ExtractValue(
 -> LOAD_FILE('users.xml'),
 -> '//user[login/text()="" or 1=1 and password/text()="" or 1=1]/attribute::id'
 -> );
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT IF(
 -> INSTR(@id, ' ') = 0,
 -> @id,
 -> 'Unable to retrieve user ID')
 -> AS singleID;
+----------------------------+
| singleID |
+----------------------------+
| Unable to retrieve user ID |
+----------------------------+
1 row in set (0.00 sec)
```

In general, the guidelines for returning data to users securely are the same as for accepting user input. These can be summed up as:

- Always test outgoing data for type and permissible values.
- Never permit unauthorized users to view error messages that might provide information about the application that could be used to exploit it.

# <span id="page-35-0"></span>**14.12 Bit Functions and Operators**

**Table 14.17 Bit Functions and Operators**

| Name | Description |
|------|-------------|
| &    | Bitwise AND |
| >>   | Right shift |
| <<   | Left shift  |
| ^    | Bitwise XOR |

| Name        | Description                            |
|-------------|----------------------------------------|
| BIT_COUNT() | Return the number of bits that are set |
|             | Bitwise OR                             |
| ~           | Bitwise inversion                      |

The following list describes available bit functions and operators:

<span id="page-36-2"></span>• [|](#page-36-2)

### Bitwise OR.

The result type depends on whether the arguments are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the arguments have a binary string type, and at least one of them is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the arguments. If the arguments have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 29 | 15;
 -> 31
mysql> SELECT _binary X'40404040' | X'01020304';
 -> 'ABCD'
```

If bitwise OR is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-36-0"></span>• [&](#page-36-0)

### Bitwise AND.

The result type depends on whether the arguments are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the arguments have a binary string type, and at least one of them is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the arguments. If the arguments have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 29 & 15;
 -> 13
mysql> SELECT HEX(_binary X'FF' & b'11110000');
 -> 'F0'
```

If bitwise AND is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-36-1"></span>• [^](#page-36-1)

### Bitwise XOR.

The result type depends on whether the arguments are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the arguments have a binary string type, and at least one of them is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the arguments. If the arguments have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 1 ^ 1;
 -> 0
mysql> SELECT 1 ^ 0;
 -> 1
mysql> SELECT 11 ^ 3;
 -> 8
mysql> SELECT HEX(_binary X'FEDC' ^ X'1111');
 -> 'EFCD'
```

If bitwise XOR is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-37-1"></span>• [<<](#page-37-1)

Shifts a longlong (BIGINT) number or binary string to the left.

The result type depends on whether the bit argument is evaluated as a binary string or number:

- Binary-string evaluation occurs when the bit argument has a binary string type, and is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to an unsigned 64-bit integer as necessary.
- Binary-string evaluation produces a binary string of the same length as the bit argument. Numeric evaluation produces an unsigned 64-bit integer.

Bits shifted off the end of the value are lost without warning, regardless of the argument type. In particular, if the shift count is greater or equal to the number of bits in the bit argument, all bits in the result are 0.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 1 << 2;
 -> 4
mysql> SELECT HEX(_binary X'00FF00FF00FF' << 8);
 -> 'FF00FF00FF00'
```

If a bit shift is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-37-0"></span>• [>>](#page-37-0)

Shifts a longlong (BIGINT) number or binary string to the right.

The result type depends on whether the bit argument is evaluated as a binary string or number:

- Binary-string evaluation occurs when the bit argument has a binary string type, and is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to an unsigned 64-bit integer as necessary.
- Binary-string evaluation produces a binary string of the same length as the bit argument. Numeric evaluation produces an unsigned 64-bit integer.

Bits shifted off the end of the value are lost without warning, regardless of the argument type. In particular, if the shift count is greater or equal to the number of bits in the bit argument, all bits in the result are 0.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 4 >> 2;
 -> 1
mysql> SELECT HEX(_binary X'00FF00FF00FF' >> 8);
 -> '0000FF00FF00'
```

If a bit shift is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-38-1"></span>• [~](#page-38-1)

Invert all bits.

The result type depends on whether the bit argument is evaluated as a binary string or number:

- Binary-string evaluation occurs when the bit argument has a binary string type, and is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to an unsigned 64-bit integer as necessary.
- Binary-string evaluation produces a binary string of the same length as the bit argument. Numeric evaluation produces an unsigned 64-bit integer.

For more information, see the introductory discussion in this section.

```
mysql> SELECT 5 & ~1;
 -> 4
mysql> SELECT HEX(~X'0000FFFF1111EEEE');
 -> 'FFFF0000EEEE1111'
```

If bitwise inversion is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-38-0"></span>• [BIT\\_COUNT\(](#page-38-0)N)

Returns the number of bits that are set in the argument N as an unsigned 64-bit integer, or NULL if the argument is NULL.

```
mysql> SELECT BIT_COUNT(64), BIT_COUNT(BINARY 64);
 -> 1, 7
mysql> SELECT BIT_COUNT('64'), BIT_COUNT(_binary '64');
 -> 1, 7
mysql> SELECT BIT_COUNT(X'40'), BIT_COUNT(_binary X'40');
 -> 1, 1
```

Bit functions and operators comprise [BIT\\_COUNT\(\)](#page-38-0), [BIT\\_AND\(\)](#page-182-0), [BIT\\_OR\(\)](#page-183-0), [BIT\\_XOR\(\)](#page-184-0), [&](#page-36-0), [|](#page-36-2), [^](#page-36-1), [~](#page-38-1), [<<](#page-37-1), and [>>](#page-37-0). (The [BIT\\_AND\(\)](#page-182-0), [BIT\\_OR\(\)](#page-183-0), and [BIT\\_XOR\(\)](#page-184-0) aggregate functions are described in [Section 14.19.1, "Aggregate Function Descriptions".](#page-181-0)) Prior to MySQL 8.0, bit functions and operators required BIGINT (64-bit integer) arguments and returned BIGINT values, so they had a maximum range of 64 bits. Non-BIGINT arguments were converted to BIGINT prior to performing the operation and truncation could occur.

In MySQL 8.0, bit functions and operators permit binary string type arguments (BINARY, VARBINARY, and the BLOB types) and return a value of like type, which enables them to take arguments and produce return values larger than 64 bits. Nonbinary string arguments are converted to BIGINT and processed as such, as before.

An implication of this change in behavior is that bit operations on binary string arguments might produce a different result in MySQL 8.0 than in 5.7. For information about how to prepare in MySQL 5.7 for potential incompatibilities between MySQL 5.7 and 8.0, see [Bit Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.md), in [MySQL](https://dev.mysql.com/doc/refman/5.7/en/) [5.7 Reference Manual](https://dev.mysql.com/doc/refman/5.7/en/).

- [Bit Operations Prior to MySQL 8.0](#page-39-0)
- [Bit Operations in MySQL 8.0](#page-40-0)
- [Binary String Bit-Operation Examples](#page-42-0)
- [Bitwise AND, OR, and XOR Operations](#page-44-0)
- [Bitwise Complement and Shift Operations](#page-44-1)
- [BIT\\_COUNT\(\) Operations](#page-45-0)
- [BIT\\_AND\(\), BIT\\_OR\(\), and BIT\\_XOR\(\) Operations](#page-45-1)
- [Special Handling of Hexadecimal Literals, Bit Literals, and NULL Literals](#page-46-0)
- [Bit-Operation Incompatibilities with MySQL 5.7](#page-46-1)

# <span id="page-39-0"></span>**Bit Operations Prior to MySQL 8.0**

Bit operations prior to MySQL 8.0 handle only unsigned 64-bit integer argument and result values (that is, unsigned BIGINT values). Conversion of arguments of other types to BIGINT occurs as necessary. Examples:

• This statement operates on numeric literals, treated as unsigned 64-bit integers:

```
mysql> SELECT 127 | 128, 128 << 2, BIT_COUNT(15);
+-----------+----------+---------------+
| 127 | 128 | 128 << 2 | BIT_COUNT(15) |
+-----------+----------+---------------+
| 255 | 512 | 4 |
+-----------+----------+---------------+
```

• This statement performs to-number conversions on the string arguments ('127' to 127, and so forth) before performing the same operations as the first statement and producing the same results:

```
mysql> SELECT '127' | '128', '128' << 2, BIT_COUNT('15');
+---------------+------------+-----------------+
| '127' | '128' | '128' << 2 | BIT_COUNT('15') |
+---------------+------------+-----------------+
| 255 | 512 | 4 |
+---------------+------------+-----------------+
```

• This statement uses hexadecimal literals for the bit-operation arguments. MySQL by default treats hexadecimal literals as binary strings, but in numeric context evaluates them as numbers (see Section 11.1.4, "Hexadecimal Literals"). Prior to MySQL 8.0, numeric context includes bit operations. Examples:

```
mysql> SELECT X'7F' | X'80', X'80' << 2, BIT_COUNT(X'0F');
+---------------+------------+------------------+
| X'7F' | X'80' | X'80' << 2 | BIT_COUNT(X'0F') |
+---------------+------------+------------------+
| 255 | 512 | 4 |
+---------------+------------+------------------+
```

Handling of bit-value literals in bit operations is similar to hexadecimal literals (that is, as numbers).

# <span id="page-40-0"></span>**Bit Operations in MySQL 8.0**

MySQL 8.0 extends bit operations to handle binary string arguments directly (without conversion) and produce binary string results. (Arguments that are not integers or binary strings are still converted to integers, as before.) This extension enhances bit operations in the following ways:

- Bit operations become possible on values longer than 64 bits.
- It is easier to perform bit operations on values that are more naturally represented as binary strings than as integers.

For example, consider UUID values and IPv6 addresses, which have human-readable text formats like this:

```
UUID: 6ccd780c-baba-1026-9564-5b8c656024db
IPv6: fe80::219:d1ff:fe91:1a72
```

It is cumbersome to operate on text strings in those formats. An alternative is convert them to fixedlength binary strings without delimiters. UUID\_TO\_BIN() and INET6\_ATON() each produce a value of data type BINARY(16), a binary string 16 bytes (128 bits) long. The following statements illustrate this (HEX() is used to produce displayable values):

```
mysql> SELECT HEX(UUID_TO_BIN('6ccd780c-baba-1026-9564-5b8c656024db'));
+----------------------------------------------------------+
| HEX(UUID_TO_BIN('6ccd780c-baba-1026-9564-5b8c656024db')) |
+----------------------------------------------------------+
| 6CCD780CBABA102695645B8C656024DB |
+----------------------------------------------------------+
mysql> SELECT HEX(INET6_ATON('fe80::219:d1ff:fe91:1a72'));
+---------------------------------------------+
| HEX(INET6_ATON('fe80::219:d1ff:fe91:1a72')) |
+---------------------------------------------+
| FE800000000000000219D1FFFE911A72 |
+---------------------------------------------+
```

Those binary values are easily manipulable with bit operations to perform actions such as extracting the timestamp from UUID values, or extracting the network and host parts of IPv6 addresses. (For examples, see later in this discussion.)

Arguments that count as binary strings include column values, routine parameters, local variables, and user-defined variables that have a binary string type: BINARY, VARBINARY, or one of the BLOB types.

What about hexadecimal literals and bit literals? Recall that those are binary strings by default in MySQL, but numbers in numeric context. How are they handled for bit operations in MySQL 8.0? Does MySQL continue to evaluate them in numeric context, as is done prior to MySQL 8.0? Or do bit operations evaluate them as binary strings, now that binary strings can be handled "natively" without conversion?

Answer: It has been common to specify arguments to bit operations using hexadecimal literals or bit literals with the intent that they represent numbers, so MySQL continues to evaluate bit operations in numeric context when all bit arguments are hexadecimal or bit literals, for backward compatbility. If you require evaluation as binary strings instead, that is easily accomplished: Use the \_binary introducer for at least one literal.

• These bit operations evaluate the hexadecimal literals and bit literals as integers:

```
mysql> SELECT X'40' | X'01', b'11110001' & b'01001111';
+---------------+---------------------------+
| X'40' | X'01' | b'11110001' & b'01001111' |
+---------------+---------------------------+
| 65 | 65 |
+---------------+---------------------------+
```

• These bit operations evaluate the hexadecimal literals and bit literals as binary strings, due to the \_binary introducer:

```
mysql> SELECT _binary X'40' | X'01', b'11110001' & _binary b'01001111';
+-----------------------+-----------------------------------+
| _binary X'40' | X'01' | b'11110001' & _binary b'01001111' |
+-----------------------+-----------------------------------+
| A | A |
+-----------------------+-----------------------------------+
```

Although the bit operations in both statements produce a result with a numeric value of 65, the second statement operates in binary-string context, for which 65 is ASCII A.

In numeric evaluation context, permitted values of hexadecimal literal and bit literal arguments have a maximum of 64 bits, as do results. By contrast, in binary-string evaluation context, permitted arguments (and results) can exceed 64 bits:

```
mysql> SELECT _binary X'4040404040404040' | X'0102030405060708';
+---------------------------------------------------+
| _binary X'4040404040404040' | X'0102030405060708' |
+---------------------------------------------------+
| ABCDEFGH |
+---------------------------------------------------+
```

There are several ways to refer to a hexadecimal literal or bit literal in a bit operation to cause binarystring evaluation:

```
_binary literal
BINARY literal
CAST(literal AS BINARY)
```

Another way to produce binary-string evaluation of hexadecimal literals or bit literals is to assign them to user-defined variables, which results in variables that have a binary string type:

```
mysql> SET @v1 = X'40', @v2 = X'01', @v3 = b'11110001', @v4 = b'01001111';
mysql> SELECT @v1 | @v2, @v3 & @v4;
+-----------+-----------+
| @v1 | @v2 | @v3 & @v4 |
+-----------+-----------+
| A | A |
+-----------+-----------+
```

In binary-string context, bitwise operation arguments must have the same length or an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs:

```
mysql> SELECT _binary X'40' | X'0001';
ERROR 3513 (HY000): Binary operands of bitwise
operators must be of equal length
```

To satisfy the equal-length requirement, pad the shorter value with leading zero digits or, if the longer value begins with leading zero digits and a shorter result value is acceptable, strip them:

```
mysql> SELECT _binary X'0040' | X'0001';
+---------------------------+
| _binary X'0040' | X'0001' |
+---------------------------+
| A |
+---------------------------+
mysql> SELECT _binary X'40' | X'01';
+-----------------------+
| _binary X'40' | X'01' |
+-----------------------+
| A |
+-----------------------+
```

Padding or stripping can also be accomplished using functions such as LPAD(), RPAD(), SUBSTR(), or [CAST\(\)](#page-13-0). In such cases, the expression arguments are no longer all literals and \_binary becomes unnecessary. Examples:

```
mysql> SELECT LPAD(X'40', 2, X'00') | X'0001';
```

```
+---------------------------------+
| LPAD(X'40', 2, X'00') | X'0001' |
+---------------------------------+
| A |
+---------------------------------+
mysql> SELECT X'40' | SUBSTR(X'0001', 2, 1);
+-------------------------------+
| X'40' | SUBSTR(X'0001', 2, 1) |
+-------------------------------+
| A |
+-------------------------------+
```

# <span id="page-42-0"></span>**Binary String Bit-Operation Examples**

The following example illustrates use of bit operations to extract parts of a UUID value, in this case, the timestamp and IEEE 802 node number. This technique requires bitmasks for each extracted part.

Convert the text UUID to the corresponding 16-byte binary value so that it can be manipulated using bit operations in binary-string context:

```
mysql> SET @uuid = UUID_TO_BIN('6ccd780c-baba-1026-9564-5b8c656024db');
mysql> SELECT HEX(@uuid);
+----------------------------------+
| HEX(@uuid) |
+----------------------------------+
| 6CCD780CBABA102695645B8C656024DB |
+----------------------------------+
```

Construct bitmasks for the timestamp and node number parts of the value. The timestamp comprises the first three parts (64 bits, bits 0 to 63) and the node number is the last part (48 bits, bits 80 to 127):

```
mysql> SET @ts_mask = CAST(X'FFFFFFFFFFFFFFFF' AS BINARY(16));
mysql> SET @node_mask = CAST(X'FFFFFFFFFFFF' AS BINARY(16)) >> 80;
mysql> SELECT HEX(@ts_mask);
+----------------------------------+
| HEX(@ts_mask) |
+----------------------------------+
| FFFFFFFFFFFFFFFF0000000000000000 |
+----------------------------------+
mysql> SELECT HEX(@node_mask);
+----------------------------------+
| HEX(@node_mask) |
+----------------------------------+
| 00000000000000000000FFFFFFFFFFFF |
+----------------------------------+
```

The CAST(... AS BINARY(16)) function is used here because the masks must be the same length as the UUID value against which they are applied. The same result can be produced using other functions to pad the masks to the required length:

```
SET @ts_mask= RPAD(X'FFFFFFFFFFFFFFFF' , 16, X'00');
SET @node_mask = LPAD(X'FFFFFFFFFFFF', 16, X'00') ;
```

Use the masks to extract the timestamp and node number parts:

```
mysql> SELECT HEX(@uuid & @ts_mask) AS 'timestamp part';
+----------------------------------+
| timestamp part |
+----------------------------------+
| 6CCD780CBABA10260000000000000000 |
+----------------------------------+
mysql> SELECT HEX(@uuid & @node_mask) AS 'node part';
+----------------------------------+
| node part |
+----------------------------------+
| 000000000000000000005B8C656024DB |
+----------------------------------+
```

The preceding example uses these bit operations: right shift ([>>](#page-37-0)) and bitwise AND ([&](#page-36-0)).

![](_page_43_Picture_1.jpeg)

### **Note**

UUID\_TO\_BIN() takes a flag that causes some bit rearrangement in the resulting binary UUID value. If you use that flag, modify the extraction masks accordingly.

The next example uses bit operations to extract the network and host parts of an IPv6 address. Suppose that the network part has a length of 80 bits. Then the host part has a length of 128 − 80 = 48 bits. To extract the network and host parts of the address, convert it to a binary string, then use bit operations in binary-string context.

Convert the text IPv6 address to the corresponding binary string:

```
mysql> SET @ip = INET6_ATON('fe80::219:d1ff:fe91:1a72');
```

Define the network length in bits:

```
mysql> SET @net_len = 80;
```

Construct network and host masks by shifting the all-ones address left or right. To do this, begin with the address ::, which is shorthand for all zeros, as you can see by converting it to a binary string like this:

```
mysql> SELECT HEX(INET6_ATON('::')) AS 'all zeros';
+----------------------------------+
| all zeros |
+----------------------------------+
| 00000000000000000000000000000000 |
+----------------------------------+
```

To produce the complementary value (all ones), use the [~](#page-38-1) operator to invert the bits:

```
mysql> SELECT HEX(~INET6_ATON('::')) AS 'all ones';
+----------------------------------+
| all ones |
+----------------------------------+
| FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF |
+----------------------------------+
```

Shift the all-ones value left or right to produce the network and host masks:

```
mysql> SET @net_mask = ~INET6_ATON('::') << (128 - @net_len);
mysql> SET @host_mask = ~INET6_ATON('::') >> @net_len;
```

Display the masks to verify that they cover the correct parts of the address:

```
mysql> SELECT INET6_NTOA(@net_mask) AS 'network mask';
+----------------------------+
| network mask |
+----------------------------+
| ffff:ffff:ffff:ffff:ffff:: |
+----------------------------+
mysql> SELECT INET6_NTOA(@host_mask) AS 'host mask';
+------------------------+
| host mask |
+------------------------+
| ::ffff:255.255.255.255 |
+------------------------+
```

Extract and display the network and host parts of the address:

```
mysql> SET @net_part = @ip & @net_mask;
mysql> SET @host_part = @ip & @host_mask;
mysql> SELECT INET6_NTOA(@net_part) AS 'network part';
+-----------------+
| network part |
+-----------------+
| fe80::219:0:0:0 |
+-----------------+
```

```
mysql> SELECT INET6_NTOA(@host_part) AS 'host part';
+------------------+
| host part |
+------------------+
| ::d1ff:fe91:1a72 |
+------------------+
```

The preceding example uses these bit operations: Complement ([~](#page-38-1)), left shift ([<<](#page-37-1)), and bitwise AND ([&](#page-36-0)).

The remaining discussion provides details on argument handling for each group of bit operations, more information about literal-value handling in bit operations, and potential incompatibilities between MySQL 8.0 and older MySQL versions.

# <span id="page-44-0"></span>**Bitwise AND, OR, and XOR Operations**

For [&](#page-36-0), [|](#page-36-2), and [^](#page-36-1) bit operations, the result type depends on whether the arguments are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the arguments have a binary string type, and at least one of them is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the arguments. If the arguments have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

Examples of numeric evaluation:

```
mysql> SELECT 64 | 1, X'40' | X'01';
+--------+---------------+
| 64 | 1 | X'40' | X'01' |
+--------+---------------+
| 65 | 65 |
+--------+---------------+
```

Examples of binary-string evaluation:

```
mysql> SELECT _binary X'40' | X'01';
+-----------------------+
| _binary X'40' | X'01' |
+-----------------------+
| A |
+-----------------------+
mysql> SET @var1 = X'40', @var2 = X'01';
mysql> SELECT @var1 | @var2;
+---------------+
| @var1 | @var2 |
+---------------+
| A |
+---------------+
```

# <span id="page-44-1"></span>**Bitwise Complement and Shift Operations**

For [~](#page-38-1), [<<](#page-37-1), and [>>](#page-37-0) bit operations, the result type depends on whether the bit argument is evaluated as a binary string or number:

- Binary-string evaluation occurs when the bit argument has a binary string type, and is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument conversion to an unsigned 64-bit integer as necessary.
- Binary-string evaluation produces a binary string of the same length as the bit argument. Numeric evaluation produces an unsigned 64-bit integer.

For shift operations, bits shifted off the end of the value are lost without warning, regardless of the argument type. In particular, if the shift count is greater or equal to the number of bits in the bit argument, all bits in the result are 0.

### Examples of numeric evaluation:

```
mysql> SELECT ~0, 64 << 2, X'40' << 2;
+----------------------+---------+------------+
| ~0 | 64 << 2 | X'40' << 2 |
+----------------------+---------+------------+
| 18446744073709551615 | 256 | 256 |
+----------------------+---------+------------+
```

### Examples of binary-string evaluation:

```
mysql> SELECT HEX(_binary X'1111000022220000' >> 16);
+----------------------------------------+
| HEX(_binary X'1111000022220000' >> 16) |
+----------------------------------------+
| 0000111100002222 |
+----------------------------------------+
mysql> SELECT HEX(_binary X'1111000022220000' << 16);
+----------------------------------------+
| HEX(_binary X'1111000022220000' << 16) |
+----------------------------------------+
| 0000222200000000 |
+----------------------------------------+
mysql> SET @var1 = X'F0F0F0F0';
mysql> SELECT HEX(~@var1);
+-------------+
| HEX(~@var1) |
+-------------+
| 0F0F0F0F |
+-------------+
```

# <span id="page-45-0"></span>**BIT\_COUNT() Operations**

The [BIT\\_COUNT\(\)](#page-38-0) function always returns an unsigned 64-bit integer, or NULL if the argument is NULL.

```
mysql> SELECT BIT_COUNT(127);
+----------------+
| BIT_COUNT(127) |
+----------------+
| 7 |
+----------------+
mysql> SELECT BIT_COUNT(b'010101'), BIT_COUNT(_binary b'010101');
+----------------------+------------------------------+
| BIT_COUNT(b'010101') | BIT_COUNT(_binary b'010101') |
+----------------------+------------------------------+
| 3 | 3 |
+----------------------+------------------------------+
```

# <span id="page-45-1"></span>**BIT\_AND(), BIT\_OR(), and BIT\_XOR() Operations**

For the [BIT\\_AND\(\)](#page-182-0), [BIT\\_OR\(\)](#page-183-0), and [BIT\\_XOR\(\)](#page-184-0) bit functions, the result type depends on whether the function argument values are evaluated as binary strings or numbers:

- Binary-string evaluation occurs when the argument values have a binary string type, and the argument is not a hexadecimal literal, bit literal, or NULL literal. Numeric evaluation occurs otherwise, with argument value conversion to unsigned 64-bit integers as necessary.
- Binary-string evaluation produces a binary string of the same length as the argument values. If argument values have unequal lengths, an [ER\\_INVALID\\_BITWISE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_operands_size) error occurs. If the argument size exceeds 511 bytes, an [ER\\_INVALID\\_BITWISE\\_AGGREGATE\\_OPERANDS\\_SIZE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_bitwise_aggregate_operands_size) error occurs. Numeric evaluation produces an unsigned 64-bit integer.

NULL values do not affect the result unless all values are NULL. In that case, the result is a neutral value having the same length as the length of the argument values (all bits 1 for [BIT\\_AND\(\)](#page-182-0), all bits 0 for [BIT\\_OR\(\)](#page-183-0), and [BIT\\_XOR\(\)](#page-184-0)).

Example:

```
mysql> CREATE TABLE t (group_id INT, a VARBINARY(6));
mysql> INSERT INTO t VALUES (1, NULL);
mysql> INSERT INTO t VALUES (1, NULL);
mysql> INSERT INTO t VALUES (2, NULL);
mysql> INSERT INTO t VALUES (2, X'1234');
mysql> INSERT INTO t VALUES (2, X'FF34');
mysql> SELECT HEX(BIT_AND(a)), HEX(BIT_OR(a)), HEX(BIT_XOR(a))
 FROM t GROUP BY group_id;
+-----------------+----------------+-----------------+
| HEX(BIT_AND(a)) | HEX(BIT_OR(a)) | HEX(BIT_XOR(a)) |
+-----------------+----------------+-----------------+
| FFFFFFFFFFFF | 000000000000 | 000000000000 |
| 1234 | FF34 | ED00 |
+-----------------+----------------+-----------------+
```

# <span id="page-46-0"></span>**Special Handling of Hexadecimal Literals, Bit Literals, and NULL Literals**

For backward compatibility, MySQL 8.0 evaluates bit operations in numeric context when all bit arguments are hexadecimal literals, bit literals, or NULL literals. That is, bit operations on binary-string bit arguments do not use binary-string evaluation if all bit arguments are unadorned hexadecimal literals, bit literals, or NULL literals. (This does not apply to such literals if they are written with a \_binary introducer, [BINARY](#page-12-0) operator, or other way of specifying them explicitly as binary strings.)

The literal handling just described is the same as prior to MySQL 8.0. Examples:

• These bit operations evaluate the literals in numeric context and produce a BIGINT result:

```
b'0001' | b'0010'
X'0008' << 8
```

• These bit operations evaluate NULL in numeric context and produce a BIGINT result that has a NULL value:

```
NULL & NULL
NULL >> 4
```

In MySQL 8.0, you can cause those operations to evaluate the arguments in binary-string context by indicating explicitly that at least one argument is a binary string:

```
_binary b'0001' | b'0010'
_binary X'0008' << 8
BINARY NULL & NULL
BINARY NULL >> 4
```

The result of the last two expressions is NULL, just as without the BINARY operator, but the data type of the result is a binary string type rather than an integer type.

# <span id="page-46-1"></span>**Bit-Operation Incompatibilities with MySQL 5.7**

Because bit operations can handle binary string arguments natively in MySQL 8.0, some expressions produce a different result in MySQL 8.0 than in 5.7. The five problematic expression types to watch out for are:

```
nonliteral_binary { & | ^ } binary
binary { & | ^ } nonliteral_binary
nonliteral_binary { << >> } anything
~ nonliteral_binary
AGGR_BIT_FUNC(nonliteral_binary)
```

Those expressions return BIGINT in MySQL 5.7, binary string in 8.0.

Explanation of notation:

- { op1 op2 ... }: List of operators that apply to the given expression type.
- binary: Any kind of binary string argument, including a hexadecimal literal, bit literal, or NULL literal.

- nonliteral\_binary: An argument that is a binary string value other than a hexadecimal literal, bit literal, or NULL literal.
- AGGR\_BIT\_FUNC: An aggregate function that takes bit-value arguments: [BIT\\_AND\(\)](#page-182-0), [BIT\\_OR\(\)](#page-183-0), [BIT\\_XOR\(\)](#page-184-0).

For information about how to prepare in MySQL 5.7 for potential incompatibilities between MySQL 5.7 and 8.0, see [Bit Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.md), in [MySQL 5.7 Reference Manual.](https://dev.mysql.com/doc/refman/5.7/en/)