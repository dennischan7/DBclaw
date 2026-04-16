# Oracle 12c - statements_8020
Source: https://docs.oracle.com/database/121/SQLRF/statements_8020.htm

[Go to main content](#BEGIN)

475/555 

# DROP JAVA

Purpose

Use the `DROP` `JAVA` statement to drop a Java source, class, or resource schema object.

Prerequisites

The Java source, class, or resource must be in your own schema or you must have the `DROP` `ANY` `PROCEDURE` system privilege. You also must have the `EXECUTE` object privilege on Java classes to use this command.

Semantics

JAVA SOURCE

Specify `SOURCE` to drop a Java source schema object and all Java class schema objects derived from it.

JAVA CLASS

Specify `CLASS` to drop a Java class schema object.

JAVA RESOURCE

Specify `RESOURCE` to drop a Java resource schema object.

object\_name

Specify the name of an existing Java class, source, or resource schema object. Enclose the `object_name` in double quotation marks to preserve lower- or mixed-case names.

Scripting on this page enhances content navigation, but does not change the content in any way.