# Oracle 12c - functions217
Source: https://docs.oracle.com/database/121/SQLRF/functions217.htm

# TO\_CHAR (number)

Syntax

to\_char\_number::=

Purpose

`TO_CHAR` (number) converts `n` to a value of `VARCHAR2` data type, using the optional number format `fmt`. The value `n` can be of type `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE`. If you omit `fmt`, then `n` is converted to a `VARCHAR2` value exactly long enough to hold its significant digits.

If `n` is negative, then the sign is applied after the format is applied. Thus `TO_CHAR(-1, '$9')` returns -$1, rather than $-1.

Refer to ["Format Models"](sql_elements004.md#i34510) for information on number formats.

The `'nlsparam'` argument specifies these characters that are returned by number format elements:

This argument can have this form:

```
'NLS_NUMERIC_CHARACTERS = ''dg''
   NLS_CURRENCY = ''text''
   NLS_ISO_CURRENCY = territory '
```

The characters `d` and `g` represent the decimal character and group separator, respectively. They must be different single-byte characters. Within the quoted string, you must use two single quotation marks around the parameter values. Ten characters are available for the currency symbol.

If you omit `'nlsparam'` or any one of the parameters, then this function uses the default parameter values for your session.

Examples

The following statement uses implicit conversion to combine a string and a number into a number:

```
SELECT TO_CHAR('01110' + 1) FROM DUAL;

TO_C
----
1111
```

Compare this example with the first example for [TO\_CHAR (character)](functions215.md#i1006717).

In the next example, the output is blank padded to the left of the currency symbol. In the optional number format `fmt`, `L` designates local currency symbol and `MI` designates a trailing minus sign. See [Table 2-13, "Number Format Elements"](sql_elements004.md#BABIGFBA) for a complete listing of number format elements. The example shows the output in a session in which the session parameter `NLS_TERRITORY` is set to `AMERICA`.

```
SELECT TO_CHAR(-10000,'L99G999D99MI') "Amount"
     FROM DUAL;

Amount
--------------
  $10,000.00-
```

In the next example, `NLS_CURRENCY` specifies the string to use as the local currency symbol for the `L` number format element. `NLS_NUMERIC_CHARACTERS` specifies comma as the character to use as the decimal separator for the `D` number format element and period as the character to use as the group separator for the `G` number format element. These characters are expected in many countries, for example in Germany.

```
SELECT TO_CHAR(-10000,'L99G999D99MI',
   'NLS_NUMERIC_CHARACTERS = '',.''
   NLS_CURRENCY = ''AusDollars'' ') "Amount"
     FROM DUAL;

Amount
-------------------
AusDollars10.000,00-
```

In the next example, `NLS_ISO_CURRENCY` instructs the database to use the international currency symbol for the territory of `POLAND` for the `C` number format element:

```
SELECT TO_CHAR(-10000,'99G999D99C',
   'NLS_NUMERIC_CHARACTERS = '',.''
   NLS_ISO_CURRENCY=POLAND') "Amount"
     FROM DUAL;

Amount
-----------------
    -10.000,00PLN
```