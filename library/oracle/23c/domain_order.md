# Oracle 23c - domain_order
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/domain_order.html

Examples

The following example creates the domain `DAY_OF_WEEK` and associates it with the column `CALENDAR_DATES.DAY_OF_WEEK_ABBR`. Passing this column to `DOMAIN_ORDER` returns the result of the `ORDER` expression (`MON = 0`, `TUE = 1`, etc.). Using this in the `ORDER BY` returns the rows sorted by their position in the week instead of alphabetically.

The query casts the string `"MON"` to `DAY_OF_WEEK` to get its sort value.

All other calls to `DOMAIN_ORDER` pass non-domain values, so return `NULL`.

```
CREATE DOMAIN day_of_week AS CHAR(3 CHAR)
  ORDER CASE UPPER(day_of_week)
     WHEN 'MON' THEN 0
     WHEN 'TUE' THEN 1
     WHEN 'WED' THEN 2
     WHEN 'THU' THEN 3
     WHEN 'FRI' THEN 4
     WHEN 'SAT' THEN 5
     WHEN 'SUN' THEN 6
     ELSE 7
  END;
```

```
CREATE TABLE calendar_dates (
  calendar_date    DATE,
  day_of_week_abbr day_of_week
);
```

```
INSERT INTO calendar_dates 
VALUES(DATE'2023-05-01', 'MON'), 
      (DATE'2023-05-02', 'TUE'), 
      (DATE'2023-05-05', 'FRI'), 
      (DATE'2023-05-08', 'mon');
```

```
SELECT day_of_week_abbr, 
       DOMAIN_ORDER(day_of_week_abbr) domain_column, 
       DOMAIN_ORDER(calendar_date) nondomain_column, 
       DOMAIN_ORDER(CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_ORDER('MON') nondomain_value
  FROM calendar_dates
  ORDER BY DOMAIN_ORDER(day_of_week_abbr);
  
DAY_OF_WEEK_ABBR DOMAIN_COLUMN NONDOMAIN_COLUMN DOMAIN_VALUE NONDOMAIN_VALUE    
---------------- ------------- ---------------- ------------ ---------------
MON                          0 <null>                      0 <null>             
mon                          0 <null>                      0 <null>             
TUE                          1 <null>                      0 <null>             
FRI                          4 <null>                      0 <null>
```

The following example creates the multicolumn domain `CURRENCY` with an order expression. This sorts the values by currency then value. The columns `AMOUNT` and `CURRENCY_CODE` in `ORDER_ITEMS` are associated with this domain.

In the query, only the domain\_cols expression formats the columns according to the order expression. All other calls to `DOMAIN_ORDER` have a mismatch between its arguments and the domain columns so return `NULL`:

```
CREATE DOMAIN currency AS (
  amount        AS NUMBER(10, 2)
  currency_code AS CHAR(3 CHAR)
)
ORDER currency_code || TO_CHAR(amount, '999999999.00');
```

```
CREATE TABLE order_items (
  order_id      INTEGER,
  product_id    INTEGER,
  amount        NUMBER(10, 2),
  currency_code CHAR(3 CHAR),
  DOMAIN currency(amount, currency_code)
);
```

```
INSERT INTO order_items
VALUES (1, 1,    9.99, 'USD'),
       (2, 2, 1234.56, 'USD'),
       (3, 3, 4321,    'EUR'),
       (4, 4, 3141592, 'JPY'),
       (5, 5, 2718281, 'JPY');
```

```
SELECT order_id,
       product_id,
       DOMAIN_ORDER(amount, currency_code) domain_cols,
       DOMAIN_ORDER(currency_code, amount) domain_cols_wrong_order,
       DOMAIN_ORDER(order_id, product_id) nondomain_cols,
       DOMAIN_ORDER(amount) domain_cols_subset
  FROM order_items
  ORDER BY domain_cols;
  
  ORDER_ID PRODUCT_ID DOMAIN_COLS      DOMAIN_COLS_WRONG_ORDER NONDOMAIN_COLS DOMAIN_COLS_SUBSET
---------- ---------- ---------------- ----------------------- -------------- ------------------
         3          3 EUR      4321.00 <null>                  <null>         <null>            
         5          5 JPY   2718281.00 <null>                  <null>         <null>            
         4          4 JPY   3141592.00 <null>                  <null>         <null>            
         1          1 USD         9.99 <null>                  <null>         <null>            
         2          2 USD      1234.56 <null>                  <null>         <null>
```