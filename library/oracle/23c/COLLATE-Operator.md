# Oracle 23c - COLLATE-Operator
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/COLLATE-Operator.html

The `COLLATE` operator determines the collation for an expression. This operator enables you to override the collation that the database would have derived for the expression using standard collation derivation rules.

`COLLATE` is a postfix unary operator. It has the same precedence as other unary operators, but it is evaluated after all prefix unary operators have been evaluated.

You can apply this operator to expressions of type `VARCHAR2`, `CHAR`, `LONG`, `NVARCHAR`, or `NCHAR`.

The `COLLATE` operator takes one argument, `collation_name`, for which you can specify a named collation or pseudo-collation. If the collation name contains a space, then you must enclose the name in double quotation marks.

[Table 4-3](COLLATE-Operator.md#GUID-1B8CE3B0-77FC-455C-8400-6F81CF188D7B__CIHDBHCB "The first column lists the single COLLATE operator, the second column describes it, and the third column provides an example.") describes the `COLLATE` operator.