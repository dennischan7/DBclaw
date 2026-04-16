---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Informix-compatible mode supports a different structure than the one described in [Section 36.7.2](#page-85-0). See below:

```
struct sqlvar_compat
{
 short sqltype;
 int sqllen;
 char *sqldata;
 short *sqlind;
 char *sqlname;
 char *sqlformat;
 short sqlitype;
 short sqlilen;
 char *sqlidata;
 int sqlxid;
 char *sqltypename;
 short sqltypelen;
 short sqlownerlen;
 short sqlsourcetype;
 char *sqlownername;
 int sqlsourceid;
 char *sqlilongdata;
```

```
 int sqlflags;
 void *sqlreserved;
};
struct sqlda_compat
{
 short sqld;
 struct sqlvar_compat *sqlvar;
 char desc_name[19];
 short desc_occ;
 struct sqlda_compat *desc_next;
 void *reserved;
};
typedef struct sqlvar_compat sqlvar_t;
typedef struct sqlda_compat sqlda_t;
The global properties are:
sqld
   The number of fields in the SQLDA descriptor.
sqlvar
   Pointer to the per-field properties.
desc_name
   Unused, filled with zero-bytes.
desc_occ
   Size of the allocated structure.
desc_next
   Pointer to the next SQLDA structure if the result set contains more than one record.
reserved
   Unused pointer, contains NULL. Kept for Informix-compatibility.
The per-field properties are below, they are stored in the sqlvar array:
sqltype
   Type of the field. Constants are in sqltypes.h
sqllen
   Length of the field data.
sqldata
   Pointer to the field data. The pointer is of char * type, the data pointed by it is in a binary
   format. Example:
   int intval;
   switch (sqldata->sqlvar[i].sqltype)
```

```
{
    case SQLINTEGER:
    intval = *(int *)sqldata->sqlvar[i].sqldata;
    break;
    ...
   }
sqlind
   Pointer to the NULL indicator. If returned by DESCRIBE or FETCH then it's always a valid
   pointer. If used as input for EXECUTE ... USING sqlda; then NULL-pointer value means
   that the value for this field is non-NULL. Otherwise a valid pointer and sqlitype has to be
   properly set. Example:
   if (*(int2 *)sqldata->sqlvar[i].sqlind != 0)
    printf("value is NULL\n");
sqlname
   Name of the field. 0-terminated string.
sqlformat
   Reserved in Informix, value of PQfformat for the field.
sqlitype
   Type of the NULL indicator data. It's always SQLSMINT when returning data from the server.
   When the SQLDA is used for a parameterized query, the data is treated according to the set type.
sqlilen
   Length of the NULL indicator data.
sqlxid
   Extended type of the field, result of PQftype.
sqltypename
sqltypelen
sqlownerlen
sqlsourcetype
sqlownername
sqlsourceid
sqlflags
sqlreserved
   Unused.
sqlilongdata
   It equals to sqldata if sqllen is larger than 32kB.
Example:
EXEC SQL INCLUDE sqlda.h;
 sqlda_t *sqlda; /* This doesn't need to be under
 embedded DECLARE SECTION */
```

```
 EXEC SQL BEGIN DECLARE SECTION;
 char *prep_stmt = "select * from table1";
 int i;
 EXEC SQL END DECLARE SECTION;
 ...
 EXEC SQL PREPARE mystmt FROM :prep_stmt;
 EXEC SQL DESCRIBE mystmt INTO sqlda;
 printf("# of fields: %d\n", sqlda->sqld);
 for (i = 0; i < sqlda->sqld; i++)
 printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);
 EXEC SQL DECLARE mycursor CURSOR FOR mystmt;
 EXEC SQL OPEN mycursor;
 EXEC SQL WHENEVER NOT FOUND GOTO out;
 while (1)
 {
 EXEC SQL FETCH mycursor USING sqlda;
 }
 EXEC SQL CLOSE mycursor;
 free(sqlda); /* The main structure is all to be free(),
 * sqlda and sqlda->sqlvar is in one allocated
 area */
```

For more information, see the sqlda.h header and the src/interfaces/ecpg/test/compat\_informix/sqlda.pgc regression test.