# Oracle 19c - Oracle-Compliance-with-FIPS-127-2
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Oracle-Compliance-with-FIPS-127-2.html

Oracle complied fully with last Federal Information Processing Standard (FIPS), which was FIPS PUB 127-2. That standard is no longer published. However, for users whose applications depend on information about the sizes of some database constructs that were defined in FIPS 127-2, the details of our compliance are listed in [Table C-4](Oracle-Compliance-with-FIPS-127-2.md#GUID-17C40E8F-D8E4-42BE-B552-9B6AB8A98CCB__CHDDDDEB "Column 1 contains database constructs, column 2 contains the FIPS standard size of each construct, and column 3 contains the Oracle Database size of each construct.").

Note 1: The number of `SET` clauses in an `UPDATE` statement refers to the number items separated by commas following the `SET` keyword.

Note 2: The FIPS PUB defines the length of a collection of columns to be the sum of: twice the number of columns, the length of each character column in bytes, decimal precision plus 1 of each exact numeric column, binary precision divided by 4 plus 1 of each approximate numeric column.

Note 3: The Oracle limit for the maximum row length is based on the maximum length of a row containing a `LONG` value of length 2 gigabytes and 999 `VARCHAR2` values, each of length 4000 bytes: 2(254) + 231 + (999(4000)).

Note 4: The Oracle limit for a `UNIQUE` key is half the size of an Oracle data block (specified by the initialization parameter `DB_BLOCK_SIZE`) minus some overhead.

Note 5: Oracle places no limit on the number of columns in a `GROUP` `BY` clause or the number of sort specifications in an `ORDER` `BY` clause. However, the sum of the sizes of all the expressions in either a `GROUP` `BY` clause or an `ORDER` `BY` clause is limited to the size of an Oracle data block (specified by the initialization parameter `DB_BLOCK_SIZE`) minus some overhead.

Note 6: The Oracle limit for the number of cursors simultaneously opened is specified by the initialization parameter `OPEN_CURSORS`. The maximum value of this parameter depends on the memory available on your operating system and exceeds 100 in all cases.