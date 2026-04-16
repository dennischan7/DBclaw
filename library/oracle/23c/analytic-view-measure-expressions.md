# Oracle 23c - analytic-view-measure-expressions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/analytic-view-measure-expressions.html

You can use analytic view expressions to create calculated measures within the definition of an analytic view or in a query that selects from an analytic view.

Analytic view expressions differ from other types of expressions in that they reference elements of hierarchies and analytic views rather than tables and columns.

An analytic view expression is one of the following:

* An `av_meas_expression`, which is based on a measure in an analytic view
* An `av_hier_expression`, which returns an attribute value of the related member

You use an analytic view expression as the `calc_meas_expression` parameter in a `calc_measure_clause` in a `CREATE` `ANALYTIC` `VIEW` statement and in the `WITH` or `FROM` clauses of a `SELECT` statement.

In defining a calculated measure, you may also use the following types of expression:

* Simple
* Case
* Compound
* Datetime
* Interval

lead\_lag\_function\_name::=

calc\_meas\_order\_by\_clause::=

hier\_navigation\_expression::=

hier\_ancestor\_expression::=

hier\_parent\_expression::=

hier\_lead\_lag\_expression::=

hier\_member\_at\_expression::=

av\_meas\_expression

An expression that performs hierarchical navigation to locate related measure values.

lead\_lag\_expression

An expression that specifies a lead or lag operation that locates a related measure value by navigating forward or backward by some number of members within a hierarchy.

The `calc_meas_expression` parameter is evaluated in the new context created by the `lead_lag_expression`. This context has the same members as the outer context, except that the member of the specified hierarchy is changed to the related member specified by the lead or lag operation. The lead or lag function is run over the hierarchy members specified by the `lead_lag_clause` parameter.

lead\_lag\_function\_name

The lead or lag function may be one of the following:

* `LAG` returns the measure value of an earlier member.
* `LAG_DIFF` returns the difference between the measure value of the current member and the measure value of an earlier member.
* `LAG_DIFF_PERCENT` returns the percent difference between the measure value of the current member and the measure value of an earlier member.
* `LEAD` returns the measure value of a later member.
* `LEAD_DIFF` returns the difference between the measure value of the current member and the measure value of a later member.
* `LEAD_DIFF_PERCENT` returns the percent difference between the measure value of the current member and the measure value of a later member.

lead\_lag\_clause

Specifies the hierarchy to evaluate and an offset value. The parameters of the `lead_lag_clause` are the following:

* `HIERARCHY` `hierarchy_ref` specifies the alias of a hierarchy as defined in the analytic view.
* `OFFSET` `offset_expr` specifies a `calc_meas_expression` that resolves to a number. The number specifies how many members to move either forward or backward from the current member. The ordering of members within a level is determined by the definition of the attribute dimension used by the hierarchy.
* `WITHIN` `LEVEL` specifies locating the related member by moving forward or backward by the offset number of members within the members that have the same level depth as the current member. The ordering of members within the level is determined by the definition of the attribute dimension used by the hierarchy.

  The `WITHIN` `LEVEL` operation is the default if neither the `WITHIN` `LEVEL` nor the `ACROSS` `ANCESTOR` `AT` `LEVEL` keywords are specified.
* `WITHIN` `PARENT` specifies locating the related member by moving forward or backward by the offset number of members within the members that have the same parent as the current member.
* `ACROSS` `ANCESTOR` `AT` `LEVEL` `level_ref` specifies locating the related member by navigating up to the ancestor (or to the member itself if no ancestor exists) of the current member at the level specified by `level_ref`, and noting the position of each ancestor member (including the member itself) within its parent. The `level_ref` parameter is the name of a level in the specified hierarchy.

  Once the ancestor member is found, navigation moves either forward or backward the offset number of members within the members that have the same depth as the ancestor member. After locating the related ancestor, navigation proceeds back down the hierarchy from this member, matching the position within the parent as recorded on the way up (in reverse order). The position within the parent is either an offset from the first child or the last child depending on whether `POSITION` `FROM` `BEGINNING` or `POSITION` `FROM` `END` is specified. The default value is `POSITION` `FROM` `BEGINNING`. The ordering of members within the level is determined by the definition of the attribute dimension used by the hierarchy.

av\_window\_expression

An `av_window_expression` selects the set of members that are in the specified range starting from the current member and that are at the same depth as the current member. You can further restrict the selection of members by specifying a hierarchical relationship using a WITHIN phrase. Aggregation is then performed over the selected measure values to produce a single result for the expression.

The parameters for an `av_window_expression` are the following:

* `aggregate_function` is any existing SQL aggregate function except `COLLECT`, `GROUP_ID`, `GROUPING`, `GROUPING_ID`, `SYS_XMLAGG`, `XMLAGG`, and any multi-argument function. A user defined aggregate function is also allowed. The arguments to the aggregate function are `calc_meas_expression` expressions. These expressions are evaluated using the outer context, with the member of the specified hierarchy changed to each member in the related range. Therefore, each expression argument is evaluated once per related member. The results are then aggregated using the `aggregate_function`.
* `OVER` `(``av_window_clause``)` specifies the hierarchy to use and the boundaries of the window to consider.

av\_window\_clause

The `av_window_clause` parameter selects a range of members related to the current member. The range is between the members specified by the `preceding_boundary` or `following_boundary` parameters. The range is always computed over members at the same level as the current member.

Use `IN member_set` to specify an arbitrary member set to be used as the window for the window expression.

The parameters for a `av_window_clause` are the following:

* `HIERARCHY` `hierarchy_ref` specifies the alias of the hierarchy as defined in the analytic view.
* `BETWEEN` `preceding_boundary` or `following_boundary` defines the set of members to relate to the current member.
* `WITHIN` `LEVEL` selects the related members by applying the boundary clause to all members of the current level. This is the default when the `WITHIN` keyword is not specified.
* `WITHIN` `PARENT` selects the related members by applying the boundary clause to all members that share a parent with the current member.
* `WITHIN` `ANCESTOR` `AT` `LEVEL` selects the related members by applying the boundary clause to all members at the current depth that share an ancestor (or is the member itself) at the specified level with the current member. The value of the window expression is `NULL` if the current member is above the specified level. If the level is not in the specified hierarchy, then an error occurs.

preceding\_boundary

The `preceding_boundary` parameter defines a range of members from the specified number of members backward in the level from the current member and forward to the specified end of the boundary. The following parameters specify the range:

* `UNBOUNDED` `PRECEDING` begins the range at the first member in the level.
* `offset_expr` `PRECEDING` begins the range at the `offset_expr` number of members backward from the current member. The `offset_expr` expression is a `calc_meas_expression` that resolves to a number. If the offset number is greater than the number of members from the current member to the first member in the level, than the first member is used as the start of the range.
* `CURRENT` `MEMBER` ends the range at the current member.
* `offset_expr` `PRECEDING` ends the range at the member that is `offset_expr` backward from the current member.
* `offset_expr` `FOLLOWING` ends the range at the member that is `offset_expr` forward from the current member.
* `UNBOUNDED` `FOLLOWING` ends the range at the last member in the level.

following\_boundary

The `following_boundary` parameter defines a range of members from the specified number of members from the current member forward to the specified end of the range. The following parameters specify the range:

* `CURRENT` `MEMBER` begins the range at the current member.
* `offset_expr` `FOLLOWING` begins the range at the member that is `offset_expr` forward from the current member.
* `offset_expr` `FOLLOWING` ends the range at the member that is `offset_expr` forward from the current member.
* `UNBOUNDED` `FOLLOWING` ends the range at the last member in the level.

hierarchy\_ref

A reference to a hierarchy of an analytic view. The `hier_alias` parameter specifies the alias of a hierarchy in the definition of the analytic view. You may use double quotes to escape special characters or preserve case, or both.

The optional `attr_dim_alias` parameter specifies the alias of an attribute dimension in the definition of the analytic view. You may use the `attr_dim_alias` parameter to resolve the ambiguity if the specified hierarchy alias conflicts with another hierarchy alias in the analytic view or if an attribute dimension is used more than once in the analytic view definition. You may use the `attr_dim_alias` parameter even when a name conflict does not exist.

rank\_expression

Hierarchical rank calculations rank the related members of the specified hierarchy based on the order of the specified measure values and return the rank of the current member within those results.

Hierarchical rank calculations locate a set of related members in the specified hierarchy, rank all the related members based on the order of the specified measure values, and then return the rank of the current member within those results. The related members are a set of members at the same level as the current member. You may optionally restrict the set by some hierarchical relationship, but the set always includes the current member. The ordering of the measure values is determined by the `calc_meas_order_by_clause` of the `rank_clause`.

rank\_function\_name

Each hierarchical ranking function assigns an order number to each related member based on the `calc_meas_order_by_clause`, starting at 1. The functions differ in the way they treat measure values that are the same.

The functions and the differences between them are the following:

* `RANK`, which assigns the same rank to identical measure values. The rank after a set of tied values is the number of tied values plus the tied order value; therefore, the ordering may not be consecutive numbers.
* `DENSE_RANK`, which assigns the same minimum rank to identical measure values. The rank after a set of tied values is always one more than the tied value; therefore, the ordering always has consecutive numbers.
* `AVERAGE_RANK`, assigns the same average rank to identical values. The next value after the average rank value is the number of identical values plus 1, that sum divided by 2, plus the average rank value. For example, for the series of five values 4, 5, 10, 5, 7, `AVERAGE_RANK` returns 1, 1.5, 1.5, 3, 4. For the series 2, 12, 10, 12, 17, 12, the returned ranks are 1, 2, 3, 3, 3, 5.
* `ROW_NUMBER`, which assigns values that are unique and consecutive across the hierarchy members. If the `calc_meas_order_by_clause` results in equal values then the results are non-deterministic.

rank\_clause

The `rank_clause` locates a range of hierarchy members related to the current member. The range is some subset of the members in the same level as the current member. The subset is determined from the `WITHIN` clause.

Valid values for the `WITHIN` clause are:

* `WITHIN LEVEL`, which specifies that the related members are all the members of the current level. This is the default subset if the `WITHIN` keyword is not specified.
* `WITHIN PARENT`, which specifies that the related members all share a parent with the current member
* `WITHIN ANCESTOR AT LEVEL`, which specifies that the related members are all of the members of the current level that share an ancestor (or self) at the specified level with the current member.

share\_of\_expression

A `share_of_expression` expression calculates the ratio of an expression's value for the current context over the expression's value at a related context. The expression is a `calc_meas_expression` that is evaluated at the current context and the related context. The `share_clause` specification determines the related context to use.

share\_clause

A `share_clause` modifies the outer context by setting the member for the specified hierarchy to a related member.

The parameters of the share clause are the following:

* `HIERARCHY` `hierarchy_ref` specifies the name of the hierarchy that is the outer context for the `share_of_expression` calculations.
* `PARENT` specifies that the related member is the parent of the current member.
* `LEVEL` `level_ref` specifies that the related member is the ancestor (or is the member itself) of the current member at the specified level in the hierarchy. If the current member is above the specified level, then `NULL` is returned for the share expression. If the level is not in the hierarchy, then an error occurs.
* `MEMBER` `member_expression` specifies that the related member is the member returned after evaluating the `member_expression` in the current context. If the value of the specified member is `NULL`, then `NULL` is returned for the share expression.

member\_expression

A `member_expression` a member expression is an expression that returns a single member in a hierarchy. A member set contains multiple members (possibly including duplicates), and may be empty. A multiple member expression is an expression that returns a member set.

The hierarchy can be determined from the outer expression (enforced by the syntax).

A `member_expression` can be one of the following:

* `level_member_literal` expression specifies a particular member contained within a particular level. The member is identified by specifying a key value.
* `hier_navigation_expr` is an expression that relates one member of the hierarchy to another member.
* `CURRENT` `MEMBER` indicates that the function should operate on the current member of the hierarchy, typically the starting point of a function, used in the innermost function when nesting. For example, `HIER_PARENT(HIER_PARENT(CURRENT MEMBER))` returns the grandparent of the current member.

  When used within a hierarchical window expression, for example, the current member is the one in which the window is currently operating. The current member can also be provided by some member set functions as well as in `QUALIFY`.
* The `NULL` keyword is simply a placeholder for a member that is not in the hierarchy, called an empty member. This can be specified explicitly, but can also be the result of a function. For example, `HIER_PARENT` on the `ALL` member of a hierarchy will result in the empty member. The empty member should not be confused with `NULL` members that are true hierarchy members of `SKIP WHEN NULL` levels.
* The `ALL` keyword specifies the `ALL` member, the ultimate ancestor of every other member in the hierarchy. Every hierarchy has an implicit `ALL` member contained within an implicit `ALL` level.

level\_member\_literal

A level member expression specifies a particular member contained within a particular level. The member is identified by specifying a key value. If the attribute name is not specified, it is assumed to be the primary key attribute. Typically, just a single attribute needs qualification.

In the case of a level with either a multi-column key or a `SKIP WHEN NULL` level, multiple attributes need to be qualified in order to uniquely identify a member. If the key attribute is specified, ordering is not important. If not specified, the ordering is assumed to be the ordering as defined in the `xxx_HIER_LEVEL_ID_ATTRS` data dictionary view.

pos\_member\_keys

The `member_key_expr` expression resolves to the key value for the member. When specified by position, all components of the key must be given in the order found in the `ALL_HIER_LEVEL_ID_ATTRS` dictionary view. For a hierarchy in which the specified level is not determined by the child level, then all member key values of all such child levels must be provided preceding the current level's member key or keys. Duplicate key components are only specified the first time they appear.

The primary key is used when `level_member_literal` is specified using the `pos_member_keys` phrase. You can reference an alternate key by using the `named_member_keys` phrase.

named\_member\_keys

The `member_key_expr` expression resolves to the key value for the member. The `attr_name` parameter is an identifier for the name of the attribute. If all of the attribute names do not make up a key or alternate key of the specified level, then an error occurs.

When specified by name, all components of the key must be given and all must use the attribute name = value form, in any order. For a hierarchy in which the specified level is not determined by the child level, then all member key values of all such child levels must be provided, also using the named form. Duplicate key components are only specified once.

hier\_navigation\_expression

A `hier_navigation_expression` expression navigates from the specified member to a different member in the hierarchy.

hier\_ancestor\_expression

Returns the ancestor of the specified member at the given level. The level can either be specified by name or depth. If the member has no ancestor at the specified level, the empty member is returned.

The depth is specified as an expression that must resolve to a number. If the member is at a level or depth above the specified member, or the member is `NULL`, then `NULL` is returned for the expression value. If the specified level is not in the context hierarchy, then an error occurs.

hier\_parent\_expression

Returns the parent of the specified member, or the empty member if it has no parent (i.e. is the `ALL` member).

hier\_first\_expression

Returns the first element in the specified member set. If the member set is empty, the empty member is returned.

hier\_last\_expression

Returns the last element in the specified member set. If the member set is empty, the empty member is returned.

hier\_member\_at\_expression

Returns the member in the specified member set at the position identified by the given expression representing the position, where positions are 1-based. If the specified position is greater than the number of elements in the member set, the empty member is returned. The expression must be coercible to a numeric type, and will be rounded to the nearest integer. If the expression resolves to an integer less than 1, the empty member is returned.

hier\_lead\_lag\_expression

Navigates from the specified member to a related member by moving forward or backward some number of members within the context hierarchy. The `HIER_LEAD` keyword returns a later member. The `HIER_LAG` keyword returns an earlier member.

hier\_lead\_lag\_clause

Navigates the `offset_expr` number of members forward or backward from the specified member. The ordering of members within a level is specified in the definition of the attribute dimension.

The optional parameters of `hier_lead_lag_clause` are the following:

* `WITHIN` `LEVEL` locates the related member by moving forward or backward `offset_expr` members within the members that have the same depth as the current member. The ordering of members within the level is determined by the definition of the attribute dimension. The `WITHIN` `LEVEL` operation is the default if neither the `WITHIN` nor the `ACROSS` keywords are used.
* `WITHIN` `PARENT` locates the related member by moving forward or backward `offset_expr` members within the members that have the same depth as the current member, but only considers members that share a parent with the current member. The ordering of members within the level is determined by the definition of the attribute dimension.
* `WITHIN` `ACROSS` `ANCESTOR` `AT` `LEVEL` locates the related member by navigating up to the ancestor of the current member (or to the member itself) at the specified level, noting the position of each ancestor member (including the member itself) within its parent. Once the ancestor member is found, navigation moves forward or backward `offset_expr` members within the members that have the same depth as the ancestor member.

  After locating the related ancestor, navigation moves back down the hierarchy from that member, matching the position within the parent as recorded on the way up (in reverse order). The position within the parent is either an offset from the first child or the last child depending on whether `POSITION` `FROM` `BEGINNING` or `POSITION` `FROM` `END` is specified, defaulting to `POSITION` `FROM` `BEGINNING`. The ordering of members within the level is determined by the definition of the attribute dimension.

qdr\_expression

A `qdr_expression` is a qualified data reference that evaluates the specified `calc_meas_expression` in a new context and sets the hierarchy member to the new value.

qualifier

A qualifier modifies the outer context by setting the member for the specified hierarchy to the member resulting from evaluating `member_expression`. If `member_expression` is `NULL`, then the result of the `qdr_expression` selection is `NULL`.

av\_hier\_expression

An `av_hier_expression` performs hierarchy navigation to locate an attribute value of the related member. An `av_hier_expression` may be a top-level expression, whereas a `hier_navigation_expression` may only be used as a `member_expression` argument.

For example, in the following query `HIER_MEMBER__NAME` is an `av_hier_expression` and `HIER_PARENT` is a `hier_navigation_expression`.

```
HIER_MEMBER_NAME(HIER_PARENT(CURRENT MEMBER) WITHIN HIERARCHY product_hier))
```

hier\_function\_name

The `hier_function_name` values are the following:

* `HIER_CAPTION`, which returns the caption of the related member in the hierarchy.
* `HIER_DEPTH`, which returns one less than the number of ancestors between the related member and the ALL member in the hierarchy. The depth of the ALL member is 0.
* `HIER_DESCRIPTION`, which returns the description of the related member in the hierarchy.
* `HIER_LEVEL`, which returns as a string value the name of the level to which the related member belongs in the hierarchy.
* `HIER_MEMBER_NAME`, which returns the member name of the related member in the hierarchy.
* `HIER_MEMBER_UNIQUE_NAME`, which returns the member unique name of the related member in the hierarchy.

member\_set

The primary purpose of member sets is to allow them to be used within hierarchical functions. A member set is the result of either a member to set function or a set to set function.

member\_to\_set\_func

All member to set functions take a member expression as input and produce a member set in hierarchy order. The variants that have a self\_clause can specify whether or not the member specified in the given member expression itself should be included in the resulting member set, with the default being that it is excluded. If the given member is the empty member, all functions return an empty set even when `INCLUDE SELF` is specified.

hier\_ancestors

Returns a member set consisting of all ancestors of the specified member, optionally including the member itself. If the member has no ancestors (i.e. is the `ALL` member) and self is excluded, an empty set is returned.

hier\_descendants

Returns a member set consisting of all descendants of the specified member, optionally including the member itself. If the `AT` clause is specified, the set of descendants are filtered to only include members at the specified level or depth. If the member has no descendants (i.e. is a leaf) optionally filtered to the given level and self is excluded, an empty set is returned.

hier\_siblings

Returns a member set consisting of all siblings of the specified member, optionally including the member itself. A sibling is defined as any member whose parent is equal to the parent of the given member. If the member has no siblings and self is excluded, an empty set is returned.

hier\_children

Returns a member set consisting of all children of the specified member. If the member has no children, an empty set is returned.

hier\_level\_members

Returns a member set consisting of members at the same level as the given member that have a common ancestor as defined by the `WITHIN` clause. This function always includes self. `WITHIN PARENT` returns all members that are children of the given memberâs parent. `WITHIN ANCESTOR AT` returns all members at the same level as the given member that have the same ancestor at the specified level. `WITHIN LEVEL` returns all members at the same level as the given member. If the `WITHIN` clause is omitted, the default is `WITHIN LEVEL`.

hier\_member\_set

Returns a member set consisting of explicitly specified members, in the order specified. This function is in its own category as it is not really performing a navigation, but simply building a set from some number of given members. Duplicate members are allowed. Any empty members in the given set are ignored, as a member set will never include the empty member.

set\_to\_set\_func

The functions in this section all operate on a member set. They perform standard set operations and further hierarchical navigation.

hier\_union

Returns the distinct union of members among the two given sets by taking all distinct members of the first set followed by all members in the second set that are not in the first set.

hier\_union\_all

Returns all members in the first set followed by all members in the second set, retaining duplicates.

hier\_intersect

Returns all distinct members in order from the first set that also appear in the second set.

hier\_minus

Returns all distinct members in order from the first set that do not appear in the second set.

hier\_distinct

Returns the distinct members in order from the given set.

hier\_range

Returns members in order from the set that fall within the specified range. In all cases, `number` is an expression that is coercible to a number. When `PERCENT` is not specified, the expression must evaluate to a positive integer. `FIRST` will return the first `N`members in the set. If `N` is greater than the number of elements in the set, all elements are returned. `LAST` will return the last `N` members in the set. If `N` is greater than the number of elements in the set, all elements are returned. `BETWEEN` will return all elements whose position in the set is >= the start position and <= the given end position, with positions being 1-based. If the `PERCENT` keyword is specified, the `number` arguments all represent percentages and must evaluate to a number between 0 and 100.

hier\_window

Returns all members in order from the given set which fall within the specified boundary relative to the given member. If the given member is not in the given set, an empty set is returned.

hier\_expand

For each member in the given set, applies the specified member to set function. References to `CURRENT MEMBER` in the member to set function refer to the current member in the set to which it is being applied. The member sets produced for the members are combined using the semantics of `HIER_UNION_ALL` (i.e. retaining duplicates).

hier\_cond

Use `IN` `member_set` to specify an arbitrary member set to use for the comparison.

hier\_position

Returns the numeric 1-based position of the first occurrence of the member identified by mbr\_expr in the specified member set, with references to `CURRENT MEMBER` referring to the current member in the set to which it is being applied. If the member does not appear in the set, `NULL` is returned. This could be useful if a user wanted to order the output of a query based on the set order.

hier\_count

Returns the number of members in the member set. If the `DISTINCT` keyword is included, returns the number of distinct members in the member set.