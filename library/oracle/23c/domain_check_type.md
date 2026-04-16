# Oracle 23c - domain_check_type
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/domain_check_type.html

Examples

Example 1

The following example creates a strict domain of data type `CHAR(3 CHAR)`:

```
CREATE DOMAIN three_chars AS CHAR(3 CHAR) STRICT;
```

Calling `DOMAIN_CHECK_TYPE` returns true for strings three characters or shorter. For strings four characters or more long it returns false:

```
SELECT DOMAIN_CHECK_TYPE (three_chars, 'ab') two_chars,
       DOMAIN_CHECK_TYPE (three_chars, 'abc') three_chars,
       DOMAIN_CHECK_TYPE (three_chars, 'abcd') four_chars;
       
TWO_CHARS   THREE_CHARS FOUR_CHARS
----------- ----------- -----------
TRUE        TRUE        FALSE
```

Example 2

The following example creates a domain `dgreater` with two columns `c1` and `c2` of type `NUMBER` and a check constraint that `c1` be greater than `c2`:

```
CREATE DOMAIN dgreater AS (
  c1 AS NUMBER, c2 AS NUMBER 
) 
  CHECK (c1 > c2);
```

The first query passes one expression value. This raises an error because there are two columns in the domain.

```
SELECT DOMAIN_CHECK_TYPE (dgreater, 1) one_expr;

ORA-11515: incorrect number of columns in domain association list
```

```
SELECT DOMAIN_CHECK_TYPE (dgreater, 1, 2) first_lower, 
       DOMAIN_CHECK_TYPE (dgreater, 2, 1) first_higher,
       DOMAIN_CHECK_TYPE (dgreater, 'b', 'a') letters;

FIRST_LOWER FIRST_HIGHER LETTERS
----------- -----------  -----------
TRUE        TRUE         FALSE
```

Example 3

The following example creates the domain `DAY_OF_WEEK` with no domain constraints. All calls to `DOMAIN_CHECK_TYPE` return true because all the input values can be converted to `CHAR`. It's a non-strict domain, so there is no length check.

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
       DOMAIN_CHECK_TYPE(day_of_week, day_of_week_abbr) domain_column, 
       DOMAIN_CHECK_TYPE(day_of_week, calendar_date) nondomain_column, 
       DOMAIN_CHECK_TYPE(day_of_week, CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_CHECK_TYPE(day_of_week, 'mon') nondomain_value
  FROM calendar_dates;
  
DAY DOMAIN_COLUMN   NONDOMAIN_COLUMN   DOMAIN_VALUE   NONDOMAIN_VALUE
--- --------------- ------------------ -------------- -----------------
MON TRUE            TRUE               TRUE           TRUE
TUE TRUE            TRUE               TRUE           TRUE
FRI TRUE            TRUE               TRUE           TRUE
mon TRUE            TRUE               TRUE           TRUE
MON TRUE            TRUE               TRUE           TRUE
```

Example 4

The following example creates the domain DAY\_OF\_WEEK with a constraint to ensure the values are the uppercase day name abbreviations (MON, TUE, etc.).

Validating this constraint is deferred until commit, so you can insert invalid values.

Using `DOMAIN_CHECK_TYPE` returns `TRUE` for all values because they all pass the type check:

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
       DOMAIN_CHECK_TYPE(day_of_week, day_of_week_abbr) domain_column, 
       DOMAIN_CHECK_TYPE(day_of_week, calendar_date) nondomain_column, 
       DOMAIN_CHECK_TYPE(day_of_week, CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_CHECK_TYPE(day_of_week, 'mon') nondomain_value
  FROM calendar_dates;

DAY DOMAIN_COLUMN NONDOMAIN_COLUMN DOMAIN_VALUE NONDOMAIN_VALUE
--- ------------- ---------------- ------------ -----------
MON TRUE          TRUE             TRUE         TRUE
tue FALSE         TRUE             TRUE         TRUE
fRI FALSE         TRUE             TRUE         TRUE
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

The query makes four calls to `DOMAIN_CHECK_TYPE`:

```
SELECT order_id,
       product_id,
       amount,
       currency_code,
       DOMAIN_CHECK_TYPE(currency, order_id, product_id) order_product,
       DOMAIN_CHECK_TYPE(currency, amount, currency_code) amount_currency,
       DOMAIN_CHECK_TYPE(currency, currency_code, amount) currency_amount,
       DOMAIN_CHECK_TYPE(currency, order_id, currency_code) order_currency
  FROM order_items;
   
  ORDER_ID PRODUCT_ID     AMOUNT CUR ORDER_PRODUCT AMOUNT_CURRENCY CURRENCY_AMOUNT ORDER_CURRENCY
---------- ---------- ---------- --- ------------- --------------- --------------- -----------
         1          1       9.99 USD TRUE          TRUE            FALSE           TRUE
         2          2    1234.56 GBP TRUE          TRUE            FALSE           TRUE
         3          3    -999999 JPY TRUE          TRUE            FALSE           TRUE
         4          4    3141592 XXX TRUE          TRUE            FALSE           TRUE
         5          5    2718281 123 TRUE          TRUE            TRUE            TRUE
```

In the example above:

* `ORDER_PRODUCT` is `TRUE` for all rows because the values for `ORDER_ID` and `PRODUCT_ID` can be converted to the corresponding column types in the domain (`NUMBER` and `CHAR`).
* `AMOUNT_CURRENCY` is `TRUE` for all rows because the table columns match the domain columns.
* `CURRENCY_AMOUNT` is `FALSE` for the first four rows because the values for the first argument, `CURRENCY_CODE` are all letters. These cannot be converted to the type of the first column in the domain (`NUMBER`), leading to a type error. The fifth row is `TRUE` because the amount (`2718281`) can be converted to `CHAR`.
* `ORDER_CURRENCY` is `TRUE` for all rows because the types for `ORDER_ID` and `CURRENCY_CODE` match the corresponding domain column types (`NUMBER` and `CHAR`).

Example 6

The following statement tries to validate the string `"raises an error"` against the non-existent domain `NOT_A_DOMAIN`. This raises an exception:

```
SELECT DOMAIN_CHECK_TYPE(not_a_domain, 'raises an error');
ORA-11504: The domain specified does not exist or the user does not have privileges on the domain for the operation.
```