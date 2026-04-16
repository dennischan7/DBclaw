---
source: PostgreSQL 14 Reference
title: 00_Overview
---

ECPG has some limited support for C++ applications. This section describes some caveats.

The ecpg preprocessor takes an input file written in C (or something like C) and embedded SQL commands, converts the embedded SQL commands into C language chunks, and finally generates a .c file. The header file declarations of the library functions used by the C language chunks that ecpg generates are wrapped in extern "C" { ... } blocks when used under C++, so they should work seamlessly in C++.

In general, however, the ecpg preprocessor only understands C; it does not handle the special syntax and reserved words of the C++ language. So, some embedded SQL code written in C++ application code that uses complicated features specific to C++ might fail to be preprocessed correctly or might not work as expected.

A safe way to use the embedded SQL code in a C++ application is hiding the ECPG calls in a C module, which the C++ application code calls into to access the database, and linking that together with the rest of the C++ code. See [Section 36.13.2](#page-50-0) about that.