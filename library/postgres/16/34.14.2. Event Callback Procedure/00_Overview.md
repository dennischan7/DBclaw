---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PGEventProc

PGEventProc is a typedef for a pointer to an event procedure, that is, the user callback function that receives events from libpq. The signature of an event procedure must be

```
int eventproc(PGEventId evtId, void *evtInfo, void *passThrough)
```

The evtId parameter indicates which PGEVT event occurred. The evtInfo pointer must be cast to the appropriate structure type to obtain further information about the event. The passThrough parameter is the pointer provided to [PQregisterEventProc](#page-9-4) when the event procedure was registered. The function should return a non-zero value if it succeeds and zero if it fails.

A particular event procedure can be registered only once in any PGconn. This is because the address of the procedure is used as a lookup key to identify the associated instance data.

### **Caution**

On Windows, functions can have two different addresses: one visible from outside a DLL and another visible from inside the DLL. One should be careful that only one of these addresses is used with libpq's event-procedure functions, else confusion will result. The simplest rule for writing code that will work is to ensure that event procedures are declared static. If the procedure's address must be available outside its own source file, expose a separate function to return the address.

## <span id="page-9-4"></span>**34.14.3. Event Support Functions**

PQregisterEventProc

Registers an event callback procedure with libpq.

```
int PQregisterEventProc(PGconn *conn, PGEventProc proc,
 const char *name, void *passThrough);
```

An event procedure must be registered once on each PGconn you want to receive events about. There is no limit, other than memory, on the number of event procedures that can be registered with a connection. The function returns a non-zero value if it succeeds and zero if it fails.

The proc argument will be called when a libpq event is fired. Its memory address is also used to lookup instanceData. The name argument is used to refer to the event procedure in error messages. This value cannot be NULL or a zero-length string. The name string is copied into the PGconn, so what is passed need not be long-lived. The passThrough pointer is passed to the proc whenever an event occurs. This argument can be NULL.

```
PQsetInstanceData
```

Sets the connection conn's instanceData for procedure proc to data. This returns nonzero for success and zero for failure. (Failure is only possible if proc has not been properly registered in conn.)

```
int PQsetInstanceData(PGconn *conn, PGEventProc proc, void
 *data);
```

<span id="page-9-0"></span>PQinstanceData

Returns the connection conn's instanceData associated with procedure proc, or NULL if there is none.

```
void *PQinstanceData(const PGconn *conn, PGEventProc proc);
```

<span id="page-9-3"></span>PQresultSetInstanceData

Sets the result's instanceData for proc to data. This returns non-zero for success and zero for failure. (Failure is only possible if proc has not been properly registered in the result.)

```
int PQresultSetInstanceData(PGresult *res, PGEventProc proc,
 void *data);
```

Beware that any storage represented by data will not be accounted for by [PQresultMemo](#page-4-1)[rySize](#page-4-1), unless it is allocated using [PQresultAlloc](#page-4-2). (Doing so is recommendable because it eliminates the need to free such storage explicitly when the result is destroyed.)

```
PQresultInstanceData
```

Returns the result's instanceData associated with proc, or NULL if there is none.

```
void *PQresultInstanceData(const PGresult *res, PGEventProc
 proc);
```