---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The interval type in C enables your programs to deal with data of the SQL type interval. See Section 8.5 for the equivalent type in the PostgreSQL server.

The following functions can be used to work with the interval type:

```
PGTYPESinterval_new
```

Return a pointer to a newly allocated interval variable.

```
interval *PGTYPESinterval_new(void);
PGTYPESinterval_free
```

Release the memory of a previously allocated interval variable.

```
void PGTYPESinterval_free(interval *intvl);
PGTYPESinterval_from_asc
```

Parse an interval from its textual representation.

```
interval *PGTYPESinterval_from_asc(char *str, char **endptr);
```

The function parses the input string str and returns a pointer to an allocated interval variable. At the moment ECPG always parses the complete string and so it currently does not support to store the address of the first invalid character in \*endptr. You can safely set endptr to NULL.

```
PGTYPESinterval_to_asc
```

Convert a variable of type interval to its textual representation.

```
char *PGTYPESinterval_to_asc(interval *span);
```

The function converts the interval variable that span points to into a C char\*. The output looks like this example: @ 1 day 12 hours 59 mins 10 secs. The result must be freed with PGTYPESchar\_free().

```
PGTYPESinterval_copy
```

Copy a variable of type interval.

```
int PGTYPESinterval_copy(interval *intvlsrc, interval
 *intvldest);
```

The function copies the interval variable that intvlsrc points to into the variable that intvldest points to. Note that you need to allocate the memory for the destination variable before.