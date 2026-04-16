# Oracle 11g - functions125
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions125.htm

[Go to main content](#BEGIN)

165/522 

# PATH

Syntax

Purpose

`PATH` is an ancillary function used only with the `UNDER_PATH` and `EQUALS_PATH` conditions. It returns the relative path that leads to the resource specified in the parent condition.

The `correlation_integer` can be any `NUMBER` integer and is used to correlate this ancillary function with its primary condition. Values less than 1 are treated as 1.

Examples

Refer to the related function [DEPTH](functions053.md#i1150333) for an example using both of these ancillary functions of the `EQUALS_PATH` and `UNDER_PATH` conditions.

Scripting on this page enhances content navigation, but does not change the content in any way.