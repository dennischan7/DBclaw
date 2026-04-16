# Oracle 23c - domain_check
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/domain_check.html

* `domain_name` must be an identifier and can be specified using `domain_owner.domain_name`. If you specify it without `domain_owner`, it resolves first to the current user then as a public synonym. If the name cannot be resolved, an error is raised.
* If `domain_name` refers to a non-existent domain or one that you do not have `EXECUTE` privileges on, then `DOMAIN_CHECK` will raise an error.
* If the domain column data type is `STRICT`, then the value is converted to the domain column's data type. For example, if the domain column data type is `VARCHAR2(100) STRICT`, then the value is converted to `VARCHAR2(100)`. Note that the conversion will not automatically trim the input to the maximum length. If the value evaluates to 'abc' for some row and the domain data type is `CHAR(2 CHAR)`, the conversion will fail instead of returning 'ab'.

  If the domain column data type is not `STRICT`, then the value is converted to the most permissive variant of the domain column's data type in terms of length, scale, and precision. For example, if the input value is a `VARCHAR2(30)`, it is converted to a `VARCHAR2(100)` because it is shorter than the domain length. If the input value is a `VARCHAR2(200)`, it remains a `VARCHAR2(200)` because this is larger than the domain length.
* If the data type conversion fails, the error is masked and `DOMAIN_CHECK` returns `FALSE`. You can use `DOMAIN_CHECK` to filter out values that cannot be inserted into a column of the given domain.

  If the data type conversion succeeds and `domain_name` does not have any enabled constraint associated with it, `DOMAIN_CHECK` returns `TRUE`.
* If the data type conversion succeeds and `domain_name` has enabled constraints that are all satisfied for a given converted value, `DOMAIN_CHECK` returns `TRUE`. If any of the domain constraints are not satisfied, it returns `FALSE` .

MULTI-COLUMN Domains

When calling `DOMAIN_CHECK` for multicolumn domains, the number if arguments for `expr` must match the number of columns in the domain. If there is a mismatch, `DOMAIN_CHECK` raises an error.

If domain `D` has `n` columns, then you should call `DOMAIN_CHECK` should be called with D+1 arguments, like `DOMAIN_CHECK(D, arg1, ..., argn)`.

If `D` does not exist or you have no privilege to access `D`, then an error is raised. If all the checks return true, `TRUE` is returned. This means that:

* `arg1` is successfully converted to the data type of column 1 in `D`, `arg2` is successfully converted to the data type of column 2 in `D`and so on to `argn` is successfully converted to the data type of column `n` in `D` .
* All of `D`'s enabled constraints are all satisfied with column 1 substituted by `arg1` converted to `D`'s column 1 data type, column 2 substituted by `arg2` converted to `D`'s column 2 data type, and so on to column `n` substituted by `argn` converted to `D`'s column `n` data type .

Example

The following example creates a domain `dgreater` with two columns `c1` and `c2` of type `NUMBER` and a check constraint that `c1` be greater than `c2`:

```
CREATE DOMAIN dgreater AS (c1 AS NUMBER, c2 AS NUMBER ) CHECK (c1 > c2);
```

Then `DOMAIN_CHECK (dgreater, 1, 2)` returns `FALSE` because `c1` is less than `c2` (the check condition fails). `DOMAIN_CHECK (dgreater, 2, 1)` returns `TRUE` because because `c1` is greater than `c2` (the check condition passes).

Flexible Domains

When calling `DOMAIN_CHECK` for flexible domains, the number of arguments for `expr` must match the number of domain columns plus discriminant columns. If there is a mismatch `DOMAIN_CHECK` raises an error.

Checking flexible domain constraints is equivalent to checking constraints of the corresponding subdomain.

You must have the `EXECUTE` privilege on the flexible domain in order to use `DOMAIN_CHECK`.

Operations that require `EXECUTE` privilege on a flexible domain (such as when associating columns with the flexible domain, or during `DOMAIN_CHECK` with the first argument the flexible domain name) require `EXECUTE` privilege on the sub-domains. This is because a flexible domain is translated during its creation to a multi-column domain. Therefore the following rules apply:

* Associating columns to a flex domain is equivalent to associating them to the corresponding multi-column domain.
* Checking flexible domain constraints is equivalent to checking constraints of the corresponding multi-column domain.
* Evaluating flexible domain display and order properties is equivalent to evaluating properties on the corresponding multi-column domain.

Examples

Example 1

The following example creates a strict domain of data type `CHAR(3 CHAR)`:

```
CREATE DOMAIN three_chars AS CHAR(3 CHAR) STRICT;
```

Calling `DOMAIN_CHECK` returns true for strings three characters or shorter. For strings four characters or more long it returns false:

```
SELECT DOMAIN_CHECK (three_chars, 'ab') two_chars,
       DOMAIN_CHECK (three_chars, 'abc') three_chars,
       DOMAIN_CHECK (three_chars, 'abcd') four_chars;
       
TWO_CHARS   THREE_CHARS FOUR_CHARS
----------- ----------- -----------
TRUE        TRUE        FALSE
```

Example 2

The following example creates a domain dgreater with two columns `c1` and `c2` of type `NUMBER` and a check constraint that `c1` be greater than `c2`:

```
CREATE DOMAIN dgreater AS (
  c1 AS NUMBER, c2 AS NUMBER 
) 
  CHECK (c1 > c2);
```

The first query passes one expression value. This raises an error because there are two columns in the domain:

```
SELECT DOMAIN_CHECK (dgreater, 1) one_expr;

ORA-11515: incorrect number of columns in domain association list
```

In the second query:

* `first_lower` is `FALSE` because this fails the domain constraint
* `first_higher` is `TRUE` because it passes the domain constraint
* `letters` is `FALSE` because the values cannot be converted to numbers

```
SELECT DOMAIN_CHECK (dgreater, 1, 2) first_lower, 
       DOMAIN_CHECK (dgreater, 2, 1) first_higher,
       DOMAIN_CHECK (dgreater, 'b', 'a') letters;

FIRST_LOWER FIRST_HIGHER LETTERS
----------- -----------  -----------
FALSE       TRUE         FALSE
```

Example 3

The following example creates the domain `DAY_OF_WEEK` with no domain constraints. All calls to `DOMAIN_CHECK` return true because all the input values can be converted to `CHAR`. It is a non-strict domain, so there is no length check.

```
CREATE DOMAIN day_of_week AS CHAR(3 CHAR);

CREATE TABLE calendar_dates (
  calendar_date    DATE,
  day_of_week_abbr day_of_week
);

INSERT INTO calendar_dates 
VALUES(DATE'2023-05-01', 'MON'), 
      (DATE'2023-05-02', 'tue'), 
      (DATE'2023-05-05', 'fRI');
      
SELECT day_of_week_abbr, 
       DOMAIN_CHECK(day_of_week, day_of_week_abbr) domain_column, 
       DOMAIN_CHECK(day_of_week, calendar_date) nondomain_column, 
       DOMAIN_CHECK(day_of_week, CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_CHECK(day_of_week, 'mon') nondomain_value
  FROM calendar_dates;
  
DAY DOMAIN_COLUMN   NONDOMAIN_COLUMN   DOMAIN_VALUE   NONDOMAIN_VALUE
--- --------------- ------------------ -------------- -----------------
FRI TRUE            TRUE               TRUE           TRUE
mon TRUE            TRUE               TRUE           TRUE
MON TRUE            TRUE               TRUE           TRUE
```

Example 4

The following example creates the domain `DAY_OF_WEEK` with a constraint to ensure the values are the uppercase day name abbreviations (`MON`, `TUE`, etc.). Validating this constraint is deferred until commit, so you can insert invalid values.

Using `DOMAIN_CHECK` to test the values for the domain column `DAY_OF_WEEK_ABBR` returns `TRUE` for the value that conforms to the constraint (`MON`) and `FALSE` for those that do not (`tue`, `fRI`):

```
CREATE DOMAIN day_of_week AS CHAR(3 CHAR)
  CONSTRAINT CHECK(day_of_week IN ('MON','TUE','WED','THU','FRI','SAT','SUN'))
  INITIALLY DEFERRED;

CREATE TABLE calendar_dates (
  calendar_date    DATE,
  day_of_week_abbr day_of_week
);

INSERT INTO calendar_dates 
VALUES(DATE'2023-05-01', 'MON'), 
      (DATE'2023-05-02', 'tue'), 
      (DATE'2023-05-05', 'fRI');

SELECT day_of_week_abbr, 
       DOMAIN_CHECK(day_of_week, day_of_week_abbr) domain_column, 
       DOMAIN_CHECK(day_of_week, calendar_date) nondomain_column, 
       DOMAIN_CHECK(day_of_week, CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_CHECK(day_of_week, 'mon') nondomain_value
  FROM calendar_dates;

DAY DOMAIN_COLUMN NONDOMAIN_COLUMN DOMAIN_VALUE NONDOMAIN_VALUE
--- ------------- ---------------- ------------ -----------
MON TRUE          FALSE            TRUE         FALSE
tue FALSE         FALSE            TRUE         FALSE
fRI FALSE         FALSE            TRUE         FALSE
```

Example 5

The following example creates the multicolumn domain currency with two deferred constraints:

```
CREATE DOMAIN currency AS (
  amount        AS NUMBER(10, 2)
  currency_code AS CHAR(3 CHAR)
)
CONSTRAINT supported_currencies_c 
  CHECK ( currency_code IN ( 'USD', 'GBP', 'EUR', 'JPY' ) )
  DEFERRABLE INITIALLY DEFERRED
CONSTRAINT non_negative_amounts_c 
  CHECK ( amount >= 0 )
  DEFERRABLE INITIALLY DEFERRED;
```

The columns `AMOUNT` and `CURRENCY_CODE` in the table `ORDER_ITEMS` are associated with domain `currency`:

```
CREATE TABLE order_items (
  order_id      INTEGER,
  product_id    INTEGER,
  amount        NUMBER(10, 2),
  currency_code CHAR(3 CHAR),
  DOMAIN currency(amount, currency_code)
);
INSERT INTO order_items
VALUES (1, 1,    9.99, 'USD'),
       (2, 2, 1234.56, 'GBP'),
       (3, 3, -999999, 'JPY'),
       (4, 4, 3141592, 'XXX') ,
       (5, 5, 2718281, '123');
```

The query makes four calls to `DOMAIN_CHECK`:

```
SELECT order_id,
       product_id,
       amount,
       currency_code,
       DOMAIN_CHECK(currency, order_id, product_id) order_product,
       DOMAIN_CHECK(currency, amount, currency_code) amount_currency,
       DOMAIN_CHECK(currency, currency_code, amount) currency_amount,
       DOMAIN_CHECK(currency, order_id, currency_code) order_currency
  FROM order_items;
   
  ORDER_ID PRODUCT_ID     AMOUNT CUR ORDER_PRODUCT AMOUNT_CURRENCY CURRENCY_AMOUNT ORDER_CURRENCY
---------- ---------- ---------- --- ------------- --------------- --------------- -----------
         1          1       9.99 USD FALSE         TRUE            FALSE           TRUE
         2          2    1234.56 GBP FALSE         TRUE            FALSE           TRUE
         3          3    -999999 JPY FALSE         FALSE           FALSE           TRUE
         4          4    3141592 XXX FALSE         FALSE           FALSE           FALSE
         5          5    2718281 123 FALSE         FALSE           FALSE           FALSE
```

In the example above:

* `ORDER_PRODUCT` is `FALSE` for all rows because the values for `PRODUCT_ID` do not conform to the `supported_currencies_c` constraint.
* `AMOUNT_CURRENCY` is `FALSE` for the rows with values that violate the constraints (`AMOUNT = -999999`, and `CURRENCY_CODE = "XXX"` and `"123"`). It is `TRUE` for the valid values.
* `CURRENCY_AMOUNT` is `FALSE` for all rows. For the first four rows this is because the values for the first argument, `CURRENCY_CODE` are all letters. These cannot be converted to the type of the first column in the domain (`NUMBER`), leading to a type error. For the fifth row, the amount (`2718281`) does not conform to the `supported_currencies_c` constraint.
* `ORDER_CURRENCY` is `FALSE` for the row with values that violate the constraints (`CURRENCY_CODE = "XXX"` and `"123"`). It is `TRUE` for the valid values.

Example 6

The following statement tries to validate the string "raises an error" against the non-existent domain `NOT_A_DOMAIN`. This raises an exception:

```
SELECT DOMAIN_CHECK(not_a_domain, 'raises an error');
ORA-11504: The domain specified does not exist or the user does not have privileges on the domain for the operation.
```