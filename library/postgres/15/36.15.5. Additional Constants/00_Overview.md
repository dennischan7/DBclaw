---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Note that all constants here describe errors and all of them are defined to represent negative values. In the descriptions of the different constants you can also find the value that the constants represent in the current implementation. However you should not rely on this number. You can however rely on the fact all of them are defined to represent negative values.

```
ECPG_INFORMIX_NUM_OVERFLOW
```

Functions return this value if an overflow occurred in a calculation. Internally it is defined as -1200 (the Informix definition).

```
ECPG_INFORMIX_NUM_UNDERFLOW
```

Functions return this value if an underflow occurred in a calculation. Internally it is defined as -1201 (the Informix definition).

```
ECPG_INFORMIX_DIVIDE_ZERO
```

Functions return this value if an attempt to divide by zero is observed. Internally it is defined as -1202 (the Informix definition).

```
ECPG_INFORMIX_BAD_YEAR
```

Functions return this value if a bad value for a year was found while parsing a date. Internally it is defined as -1204 (the Informix definition).

```
ECPG_INFORMIX_BAD_MONTH
```

Functions return this value if a bad value for a month was found while parsing a date. Internally it is defined as -1205 (the Informix definition).

```
ECPG_INFORMIX_BAD_DAY
```

Functions return this value if a bad value for a day was found while parsing a date. Internally it is defined as -1206 (the Informix definition).

```
ECPG_INFORMIX_ENOSHORTDATE
```

Functions return this value if a parsing routine needs a short date representation but did not get the date string in the right length. Internally it is defined as -1209 (the Informix definition).

```
ECPG_INFORMIX_DATE_CONVERT
```

Functions return this value if an error occurred during date formatting. Internally it is defined as -1210 (the Informix definition).

```
ECPG_INFORMIX_OUT_OF_MEMORY
```

Functions return this value if memory was exhausted during their operation. Internally it is defined as -1211 (the Informix definition).

```
ECPG_INFORMIX_ENOTDMY
```

Functions return this value if a parsing routine was supposed to get a format mask (like mmddyy) but not all fields were listed correctly. Internally it is defined as -1212 (the Informix definition).

```
ECPG_INFORMIX_BAD_NUMERIC
```

Functions return this value either if a parsing routine cannot parse the textual representation for a numeric value because it contains errors or if a routine cannot complete a calculation involving numeric variables because at least one of the numeric variables is invalid. Internally it is defined as -1213 (the Informix definition).

```
ECPG_INFORMIX_BAD_EXPONENT
```

Functions return this value if a parsing routine cannot parse an exponent. Internally it is defined as -1216 (the Informix definition).

```
ECPG_INFORMIX_BAD_DATE
```

Functions return this value if a parsing routine cannot parse a date. Internally it is defined as -1218 (the Informix definition).

```
ECPG_INFORMIX_EXTRA_CHARS
```

Functions return this value if a parsing routine is passed extra characters it cannot parse. Internally it is defined as -1264 (the Informix definition).

# <span id="page-115-0"></span>**36.16. Oracle Compatibility Mode**

ecpg can be run in a so-called *Oracle compatibility mode*. If this mode is active, it tries to behave as if it were Oracle Pro\*C.

Specifically, this mode changes ecpg in three ways:

- Pad character arrays receiving character string types with trailing spaces to the specified length
- Zero byte terminate these character arrays, and set the indicator variable if truncation occurs
- Set the null indicator to -1 when character arrays receive empty character string types