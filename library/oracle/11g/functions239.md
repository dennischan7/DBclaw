# Oracle 11g - functions239
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions239.htm

[Go to main content](#BEGIN)

279/522 

# XMLCOMMENT

Syntax

Purpose

`XMLComment` generates an XML comment using an evaluated result of `value_expr`. The `value_expr` must resolve to a string. It cannot contain two consecutive dashes (hyphens). The value returned by the function takes the following form:

```
<!--string-->
```

If `value_expr` resolves to null, then the function returns null.

Examples

The following example uses the `DUAL` table to illustrate the `XMLComment` syntax:

```
SELECT XMLCOMMENT('OrderAnalysisComp imported, reconfigured, disassembled')
   AS "XMLCOMMENT" FROM DUAL;
 
XMLCOMMENT
--------------------------------------------------------------------------------
<!--OrderAnalysisComp imported, reconfigured, disassembled-->
```

Scripting on this page enhances content navigation, but does not change the content in any way.