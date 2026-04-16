---
source: MySQL 5.7 Reference
title: 00_Overview
---

**Table 12.16 XML Functions**

| Name           | Description                                                |
|----------------|------------------------------------------------------------|
| ExtractValue() | Extract a value from an XML string using XPath<br>notation |
| UpdateXML()    | Return replaced XML fragment                               |

This section discusses XML and related functionality in MySQL.

![](_page_95_Picture_1.jpeg)

#### **Note**

It is possible to obtain XML-formatted output from MySQL in the mysql and mysqldump clients by invoking them with the --xml option. See Section 4.5.1, "mysql — The MySQL Command-Line Client", and Section 4.5.4, "mysqldump — A Database Backup Program".

Two functions providing basic XPath 1.0 (XML Path Language, version 1.0) capabilities are available. Some basic information about XPath syntax and usage is provided later in this section; however, an in-depth discussion of these topics is beyond the scope of this manual, and you should refer to the [XML Path Language \(XPath\) 1.0 standard](http://www.w3.org/TR/xpath) for definitive information. A useful resource for those new to XPath or who desire a refresher in the basics is the [Zvon.org XPath Tutorial,](http://www.zvon.org/xxl/XPathTutorial/) which is available in several languages.

![](_page_95_Picture_5.jpeg)

#### **Note**

These functions remain under development. We continue to improve these and other aspects of XML and XPath functionality in MySQL 5.7 and onwards. You may discuss these, ask questions about them, and obtain help from other users with them in the [MySQL XML User Forum](https://forums.mysql.com/list.php?44).

XPath expressions used with these functions support user variables and local stored program variables. User variables are weakly checked; variables local to stored programs are strongly checked (see also Bug #26518):

• **User variables (weak checking).** Variables using the syntax \$@variable\_name (that is, user variables) are not checked. No warnings or errors are issued by the server if a variable has the wrong type or has previously not been assigned a value. This also means the user is fully responsible for any typographical errors, since no warnings are given if (for example) \$@myvairable is used where \$@myvariable was intended.

#### Example:

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

• **Variables in stored programs (strong checking).** Variables using the syntax \$variable\_name can be declared and used with these functions when they are called inside stored programs. Such

variables are local to the stored program in which they are defined, and are strongly checked for type and value.

#### Example:

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

![](_page_96_Picture_6.jpeg)

#### **Note**

A user variable used to store an XPath expression is treated as an empty string. Because of this, it is not possible to store an XPath expression as a user variable. (Bug #32911)

<span id="page-96-0"></span>• [ExtractValue\(](#page-96-0)xml\_frag, xpath\_expr)

[ExtractValue\(\)](#page-96-0) takes two string arguments, a fragment of XML markup xml\_frag and an XPath expression xpath\_expr (also known as a locator); it returns the text (CDATA) of the first text node which is a child of the element or elements matched by the XPath expression.

Using this function is the equivalent of performing a match using the xpath\_expr after appending /text(). In other words, [ExtractValue\('<a><b>Sakila</b></a>', '/a/b'\)](#page-96-0) and [ExtractValue\('<a><b>Sakila</b></a>', '/a/b/text\(\)'\)](#page-96-0) produce the same result.

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

![](_page_97_Picture_7.jpeg)

#### **Important**

[ExtractValue\(\)](#page-96-0) returns only CDATA, and does not return any tags that might be contained within a matching tag, nor any of their content (see the result returned as val1 in the following example).

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
```

+------+------+------+------+---------+

This function uses the current SQL collation for making comparisons with contains(), performing the same collation aggregation as other string functions (such as [CONCAT\(\)](#page-39-0)), in taking into account the collation coercibility of their arguments; see Section 10.8.4, "Collation Coercibility in Expressions", for an explanation of the rules governing this behavior.

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
+-------------------------------------+
1 row in set (0.00 sec)
```

<span id="page-98-0"></span>• [UpdateXML\(](#page-98-0)xml\_target, xpath\_expr, new\_xml)

This function replaces a single portion of a given fragment of XML markup xml\_target with a new XML fragment new\_xml, and then returns the changed XML. The portion of xml\_target that is replaced matches an XPath expression xpath\_expr supplied by the user.

If no expression matching xpath\_expr is found, or if multiple matches are found, the function returns the original xml\_target XML fragment. All three arguments should be strings.

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

![](_page_98_Picture_10.jpeg)

#### **Note**

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

![](_page_99_Picture_13.jpeg)

## **Note**

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
```

```
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

![](_page_100_Picture_7.jpeg)

#### **Note**

The difference between or and | is that or joins conditions, while | joins result sets.

**XPath Limitations.** The XPath syntax supported by these functions is currently subject to the following limitations:

• Nodeset-to-nodeset comparison (such as '/a/b[@c=@d]') is not supported.

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
• axis::node()
```

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
  - id()
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

XPath expressions passed as arguments to [ExtractValue\(\)](#page-96-0) and [UpdateXML\(\)](#page-98-0) may contain the colon character (:) in element selectors, which enables their use with markup employing XML namespaces notation. For example:

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

**Error handling.** For both [ExtractValue\(\)](#page-96-0) and [UpdateXML\(\)](#page-98-0), the XPath locator used must be valid and the XML to be searched must consist of elements which are properly nested and closed. If the locator is invalid, an error is generated:

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

![](_page_103_Picture_5.jpeg)

### **Important**

The replacement XML used as the third argument to [UpdateXML\(\)](#page-98-0) is not checked to determine whether it consists solely of elements which are properly nested and closed.

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
```

```
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

- Never accepted untested data from users in your application.
- Check all user-submitted data for type; reject or convert data that is of the wrong type
- Test numeric data for out of range values; truncate, round, or reject values that are out of range. Test strings for illegal characters and either strip them out or reject input containing them.
- Do not output explicit error messages that might provide an unauthorized user with clues that could be used to compromise the system; log these to a file or database table instead.

Just as SQL injection attacks can be used to obtain information about database schemas, so can XPath injection be used to traverse XML files to uncover their structure, as discussed in Amit Klein's paper [Blind XPath Injection](http://www.packetstormsecurity.org/papers/bypass/Blind_XPath_Injection_20040518.pdf) (PDF file, 46KB).

It is also important to check the output being sent back to the client. Consider what can happen when we use the MySQL [ExtractValue\(\)](#page-96-0) function:

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

Because [ExtractValue\(\)](#page-96-0) returns multiple matches as a single space-delimited string, this injection attack provides every valid ID contained within users.xml to the user as a single row of output. As an extra safeguard, you should also test output before returning it to the user. Here is a simple example:

```
mysql> SELECT @id = ExtractValue(
 -> LOAD_FILE('users.xml'),
 -> '//user[login/text()="" or 1=1 and password/text()="" or 1=1]/attribute::id'
 -> );
Query OK, 0 rows affected (0.00 sec)
```

```
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

# <span id="page-105-3"></span>**12.12 Bit Functions and Operators**

**Table 12.17 Bit Functions and Operators**

| Name        | Description                            |
|-------------|----------------------------------------|
| &           | Bitwise AND                            |
| >>          | Right shift                            |
| <<          | Left shift                             |
| ^           | Bitwise XOR                            |
| BIT_COUNT() | Return the number of bits that are set |
|             | Bitwise OR                             |
| ~           | Bitwise inversion                      |

The following list describes available bit functions and operators:

<span id="page-105-2"></span>• [|](#page-105-2)

Bitwise OR.

The result is an unsigned 64-bit integer.

```
mysql> SELECT 29 | 15;
 -> 31
```

<span id="page-105-0"></span>• [&](#page-105-0)

Bitwise AND.

The result is an unsigned 64-bit integer.

```
mysql> SELECT 29 & 15;
 -> 13
```

<span id="page-105-1"></span>• [^](#page-105-1)

Bitwise XOR.

The result is an unsigned 64-bit integer.

```
mysql> SELECT 1 ^ 1;
 -> 0
mysql> SELECT 1 ^ 0;
 -> 1
```

```
mysql> SELECT 11 ^ 3;
 -> 8
```

<span id="page-106-1"></span>• [<<](#page-106-1)

Shifts a longlong (BIGINT) number to the left.

The result is an unsigned 64-bit integer. The value is truncated to 64 bits. In particular, if the shift count is greater or equal to the width of an unsigned 64-bit number, the result is zero.

```
mysql> SELECT 1 << 2;
 -> 4
```

<span id="page-106-0"></span>• [>>](#page-106-0)

Shifts a longlong (BIGINT) number to the right.

The result is an unsigned 64-bit integer. The value is truncated to 64 bits. In particular, if the shift count is greater or equal to the width of an unsigned 64-bit number, the result is zero.

```
mysql> SELECT 4 >> 2;
 -> 1
```

<span id="page-106-3"></span>• [~](#page-106-3)

Invert all bits.

The result is an unsigned 64-bit integer.

```
mysql> SELECT 5 & ~1;
 -> 4
```

<span id="page-106-2"></span>• [BIT\\_COUNT\(](#page-106-2)N)

Returns the number of bits that are set in the argument N as an unsigned 64-bit integer, or NULL if the argument is NULL.

```
mysql> SELECT BIT_COUNT(29), BIT_COUNT(b'101010');
 -> 4, 3
```

Bit functions and operators comprise [BIT\\_COUNT\(\)](#page-106-2), [BIT\\_AND\(\)](#page-197-0), [BIT\\_OR\(\)](#page-197-1), [BIT\\_XOR\(\)](#page-197-2), [&](#page-105-0), [|](#page-105-2), [^](#page-105-1), [~](#page-106-3), [<<](#page-106-1), and [>>](#page-106-0). (The [BIT\\_AND\(\)](#page-197-0), [BIT\\_OR\(\)](#page-197-1), and [BIT\\_XOR\(\)](#page-197-2) functions are aggregate functions described at [Section 12.19.1, "Aggregate Function Descriptions"](#page-196-0).) Currently, bit functions and operators require BIGINT (64-bit integer) arguments and return BIGINT values, so they have a maximum range of 64 bits. Arguments of other types are converted to BIGINT and truncation might occur.

An extension for MySQL 8.0 changes this cast-to-BIGINT behavior: Bit functions and operators permit binary string type arguments (BINARY, VARBINARY, and the BLOB types), enabling them to take arguments and produce return values larger than 64 bits. Consequently, bit operations on binary arguments in MySQL 5.7 might produce different results in MySQL 8.0. To provide advance notice about this potential change in behavior, the server produces warnings as of MySQL 5.7.11 for bit operations for which binary arguments are not converted to integer in MySQL 8.0. These warnings afford an opportunity to rewrite affected statements. To produce MySQL 5.7 behavior explicitly in a way that does not change after an upgrade to 8.0, cast bit-operation binary arguments to convert them to integer.

The five problematic expression types to watch out for are:

```
nonliteral_binary { & | ^ } binary
binary { & | ^ } nonliteral_binary
nonliteral_binary { << >> } anything
~ nonliteral_binary
AGGR_BIT_FUNC(nonliteral_binary)
```

Those expressions return BIGINT in MySQL 5.7, binary string in 8.0.

#### Explanation of notation:

- { op1 op2 ... }: List of operators that apply to the given expression type.
- binary: Any kind of binary string argument, including a hexadecimal literal, bit literal, or NULL literal.
- nonliteral\_binary: An argument that is a binary string value other than a hexadecimal literal, bit literal, or NULL literal.
- AGGR\_BIT\_FUNC: An aggregate function that takes bit-value arguments: [BIT\\_AND\(\)](#page-197-0), [BIT\\_OR\(\)](#page-197-1), [BIT\\_XOR\(\)](#page-197-2).

The server produces a single warning for each problematic expression in a statement, not a warning for each row processed. Suppose that a statement containing two problematic expressions selects three rows from a table. The number of warnings per statement execution is two, not six. The following example illustrates this.

```
mysql> CREATE TABLE t(vbin1 VARBINARY(32), vbin2 VARBINARY(32));
Query OK, 0 rows affected (0.03 sec)
mysql> INSERT INTO t VALUES (3,1), (3,2), (3,3);
Query OK, 3 rows affected (0.01 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT HEX(vbin1 & vbin2) AS op1,
 -> HEX(vbin1 | vbin2) AS op2
 -> FROM t;
+------+------+
| op1 | op2 |
+------+------+
| 1 | 3 |
| 2 | 3 |
| 3 | 3 |
+------+------+
3 rows in set, 2 warnings (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1287
Message: Bitwise operations on BINARY will change behavior in a future
 version, check the 'Bit functions' section in the manual.
*************************** 2. row ***************************
 Level: Warning
 Code: 1287
Message: Bitwise operations on BINARY will change behavior in a future
 version, check the 'Bit functions' section in the manual.
2 rows in set (0.00 sec)
```

To avoid having an affected statement produce a different result after an upgrade to MySQL 8.0, rewrite it so that it generates no bit-operation warnings. To do this, cast at least one binary argument to BIGINT with [CAST\(... AS UNSIGNED\)](#page-89-0). This makes the MySQL 5.7 implicit binary-to-integer cast explicit:

```
mysql> SELECT HEX(CAST(vbin1 AS UNSIGNED) & CAST(vbin2 AS UNSIGNED)) AS op1,
 -> HEX(CAST(vbin1 AS UNSIGNED) | CAST(vbin2 AS UNSIGNED)) AS op2
 -> FROM t;
+------+------+
| op1 | op2 |
+------+------+
| 1 | 3 |
| 2 | 3 |
| 3 | 3 |
+------+------+
3 rows in set (0.01 sec)
mysql> SHOW WARNINGS\G
Empty set (0.00 sec)
```

With the statement rewritten as shown, MySQL 8.0 respects the intention to treat the binary arguments as integers and produces the same result as in 5.7. Also, replicating the statement from MySQL 5.7 to 8.0 does not produce different results on different servers.

An affected statement that cannot be rewritten is subject to these potential problems with respect to upgrades and replication:

- The statement might return a different result after an upgrade to MySQL 8.0.
- Replication to MySQL 8.0 from older versions might fail for statement-based and mixed-format binary logging. This is also true for replaying older binary logs on an 8.0 server (for example, using mysqlbinlog). To avoid this, switch to row-based binary logging on the older source server.