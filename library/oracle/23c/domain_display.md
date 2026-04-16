# Oracle 23c - domain_display
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/domain_display.html

Examples

The following example creates the domain `DAY_OF_WEEK` and associates it with the column `CALENDAR_DATES.DAY_OF_WEEK_ABBR`. Passing this column to `DOMAIN_DISPLAY` returns it with the first letter of each word capitalized and all other letters in lowercase. `DOMAIN_DISPLAY` also returns this format when casting a string to the domain.

All other calls to `DOMAIN_DISPLAY` pass non-domain values, so return `NULL`.

```
CREATE DOMAIN day_of_week AS CHAR(3 CHAR)
  DISPLAY INITCAP(day_of_week);
```

```
CREATE TABLE calendar_dates (
  calendar_date DATE,
  day_of_week_abbr day_of_week
);
```

```
INSERT INTO calendar_dates 
VALUES(DATE'2023-05-01', 'MON'), 
      (DATE'2023-05-02', 'tue'), 
      (DATE'2023-05-05', 'fRI');
```

```
SELECT day_of_week_abbr, 
       DOMAIN_DISPLAY(day_of_week_abbr) domain_column, 
       DOMAIN_DISPLAY(calendar_date) nondomain_column,
       DOMAIN_DISPLAY(CAST('MON' AS day_of_week)) domain_value, 
       DOMAIN_DISPLAY('MON') nondomain_value
  FROM calendar_dates;

DAY_OF_WEEK_ABBR DOMAIN_COLUMN NONDOMAIN_COLUMN DOMAIN_VALUE NONDOMAIN_VALUE
---------------- ------------- ---------------- ------------ ---------------
MON              Mon           <null>           Mon          <null>         
tue              Tue           <null>           Mon          <null>             
fRI              Fri           <null>           Mon          <null>
```

The following example creates the multicolumn domain `CURRENCY` with a display expression. The columns `AMOUNT` and `CURRENCY_CODE` in `ORDER_ITEMS` are associated with this domain.

In the query, only the domain\_cols expression formats the columns according to the domain expression. All other calls to `DOMAIN_DISPLAY` have a mismatch between its arguments and the domain columns so return `NULL`:

```
CREATE DOMAIN currency AS (
  amount        AS NUMBER(10, 2)
  currency_code AS CHAR(3 CHAR)
)
DISPLAY CASE currency_code
  WHEN 'USD' THEN '$'
  WHEN 'GBP' THEN 'Â£'
  WHEN 'EUR' THEN 'â¬'
  WHEN 'JPY' THEN 'Â¥'
END || TO_CHAR(amount, '999,999,999.00');
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
       (2, 2, 1234.56, 'GBP'),
       (3, 3, 4321,    'EUR'),
       (4, 4, 3141592, 'JPY');
```

```
SELECT order_id,
       product_id,
       DOMAIN_DISPLAY(amount, currency_code) domain_cols,
       DOMAIN_DISPLAY(currency_code, amount) domain_cols_wrong_order,
       DOMAIN_DISPLAY(order_id, product_id) nondomain_cols,
       DOMAIN_DISPLAY(amount) domain_cols_subset
  FROM order_items;
  
  ORDER_ID PRODUCT_ID DOMAIN_COLS      DOMAIN_COLS_WRONG_ORDER NONDOMAIN_COLS DOMAIN_COLS_SUBSET
---------- ---------- ---------------- ----------------------- -------------- ------------------
         1          1 $           9.99 <null>                  <null>         <null>            
         2          2 Â£       1,234.56 <null>                  <null>         <null>            
         3          3 â¬       4,321.00 <null>                  <null>         <null>            
         4          4 Â¥   3,141,592.00 <null>                  <null>         <null>
```