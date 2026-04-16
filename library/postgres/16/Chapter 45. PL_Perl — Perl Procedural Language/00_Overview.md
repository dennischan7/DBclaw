---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PL/Perl is a loadable procedural language that enables you to write PostgreSQL functions and procedures in the [Perl programming language](https://www.perl.org)<sup>1</sup> .

The main advantage to using PL/Perl is that this allows use, within stored functions and procedures, of the manyfold "string munging" operators and functions available for Perl. Parsing complex strings might be easier using Perl than it is with the string functions and control structures provided in PL/ pgSQL.

To install PL/Perl in a particular database, use CREATE EXTENSION plperl.

#### **Tip**

If a language is installed into template1, all subsequently created databases will have the language installed automatically.

#### **Note**

Users of source packages must specially enable the build of PL/Perl during the installation process. (Refer to Chapter 17 for more information.) Users of binary packages might find PL/ Perl in a separate subpackage.