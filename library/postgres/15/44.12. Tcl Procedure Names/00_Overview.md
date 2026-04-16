---
source: PostgreSQL 15 Reference
title: 00_Overview
---

In PostgreSQL, the same function name can be used for different function definitions as long as the number of arguments or their types differ. Tcl, however, requires all procedure names to be distinct. PL/Tcl deals with this by making the internal Tcl procedure names contain the object ID of the function from the system table pg\_proc as part of their name. Thus, PostgreSQL functions with the same name and different argument types will be different Tcl procedures, too. This is not normally a concern for a PL/Tcl programmer, but it might be visible when debugging.

# <span id="page-189-0"></span>**Chapter 45. PL/Perl — Perl Procedural Language**

PL/Perl is a loadable procedural language that enables you to write PostgreSQL functions and procedures in the [Perl programming language](https://www.perl.org)<sup>1</sup> .

The main advantage to using PL/Perl is that this allows use, within stored functions and procedures, of the manyfold "string munging" operators and functions available for Perl. Parsing complex strings might be easier using Perl than it is with the string functions and control structures provided in PL/ pgSQL.

To install PL/Perl in a particular database, use CREATE EXTENSION plperl.

#### **Tip**

If a language is installed into template1, all subsequently created databases will have the language installed automatically.

#### **Note**

Users of source packages must specially enable the build of PL/Perl during the installation process. (Refer to Chapter 17 for more information.) Users of binary packages might find PL/ Perl in a separate subpackage.