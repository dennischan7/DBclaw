---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The FDW author needs to implement a handler function, and optionally a validator function. Both functions must be written in a compiled language such as C, using the version-1 interface. For details on C language calling conventions and dynamic loading, see Section 38.10.

The handler function simply returns a struct of function pointers to callback functions that will be called by the planner, executor, and various maintenance commands. Most of the effort in writing an FDW is in implementing these callback functions. The handler function must be registered with PostgreSQL as taking no arguments and returning the special pseudo-type fdw\_handler. The callback functions are plain C functions and are not visible or callable at the SQL level. The callback functions are described in [Section 57.2.](#page-147-0)

The validator function is responsible for validating options given in CREATE and ALTER commands for its foreign data wrapper, as well as foreign servers, user mappings, and foreign tables using the wrapper. The validator function must be registered as taking two arguments, a text array containing the options to be validated, and an OID representing the type of object the options are associated with. The latter corresponds to the OID of the system catalog the object would be stored in, one of:

- AttributeRelationId
- ForeignDataWrapperRelationId
- ForeignServerRelationId
- ForeignTableRelationId
- UserMappingRelationId

If no validator function is supplied, options are not checked at object creation time or object alteration time.

# <span id="page-147-0"></span>**57.2. Foreign Data Wrapper Callback Routines**

The FDW handler function returns a palloc'd FdwRoutine struct containing pointers to the callback functions described below. The scan-related functions are required, the rest are optional.

The FdwRoutine struct type is declared in src/include/foreign/fdwapi.h, which see for additional details.