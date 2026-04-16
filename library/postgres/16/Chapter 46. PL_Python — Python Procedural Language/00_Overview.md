---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The PL/Python procedural language allows PostgreSQL functions and procedures to be written in the [Python language](https://www.python.org)<sup>1</sup> .

To install PL/Python in a particular database, use CREATE EXTENSION plpython3u.

#### **Tip**

If a language is installed into template1, all subsequently created databases will have the language installed automatically.

PL/Python is only available as an "untrusted" language, meaning it does not offer any way of restricting what users can do in it and is therefore named plpython3u. A trusted variant plpython might become available in the future if a secure execution mechanism is developed in Python. The writer of a function in untrusted PL/Python must take care that the function cannot be used to do anything unwanted, since it will be able to do anything that could be done by a user logged in as the database administrator. Only superusers can create functions in untrusted languages such as plpython3u.

#### **Note**

Users of source packages must specially enable the build of PL/Python during the installation process. (Refer to the installation instructions for more information.) Users of binary packages might find PL/Python in a separate subpackage.

## <span id="page-41-0"></span>**46.1. PL/Python Functions**

Functions in PL/Python are declared via the standard CREATE FUNCTION syntax:

```
CREATE FUNCTION funcname (argument-list)
 RETURNS return-type
AS $$
 # PL/Python function body
$$ LANGUAGE plpython3u;
```

The body of a function is simply a Python script. When the function is called, its arguments are passed as elements of the list args; named arguments are also passed as ordinary variables to the Python script. Use of named arguments is usually more readable. The result is returned from the Python code in the usual way, with return or yield (in case of a result-set statement). If you do not provide a return value, Python returns the default None. PL/Python translates Python's None into the SQL null value. In a procedure, the result from the Python code must be None (typically achieved by ending the procedure without a return statement or by using a return statement without argument); otherwise, an error will be raised.

For example, a function to return the greater of two integers can be defined as:

```
CREATE FUNCTION pymax (a integer, b integer)
```

<sup>1</sup> <https://www.python.org>

```
 RETURNS integer
AS $$
 if a > b:
 return a
 return b
$$ LANGUAGE plpython3u;
```

The Python code that is given as the body of the function definition is transformed into a Python function. For example, the above results in:

```
def __plpython_procedure_pymax_23456():
 if a > b:
 return a
 return b
```

assuming that 23456 is the OID assigned to the function by PostgreSQL.

The arguments are set as global variables. Because of the scoping rules of Python, this has the subtle consequence that an argument variable cannot be reassigned inside the function to the value of an expression that involves the variable name itself, unless the variable is redeclared as global in the block. For example, the following won't work:

```
CREATE FUNCTION pystrip(x text)
 RETURNS text
AS $$
 x = x.strip() # error
 return x
$$ LANGUAGE plpython3u;
```

because assigning to x makes x a local variable for the entire block, and so the x on the right-hand side of the assignment refers to a not-yet-assigned local variable x, not the PL/Python function parameter. Using the global statement, this can be made to work:

```
CREATE FUNCTION pystrip(x text)
 RETURNS text
AS $$
 global x
 x = x.strip() # ok now
 return x
$$ LANGUAGE plpython3u;
```

But it is advisable not to rely on this implementation detail of PL/Python. It is better to treat the function parameters as read-only.

## <span id="page-42-0"></span>**46.2. Data Values**

Generally speaking, the aim of PL/Python is to provide a "natural" mapping between the PostgreSQL and the Python worlds. This informs the data mapping rules described below.