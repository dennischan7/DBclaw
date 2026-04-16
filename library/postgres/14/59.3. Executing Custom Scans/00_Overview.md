---
source: PostgreSQL 14 Reference
title: 00_Overview
---

When a CustomScan is executed, its execution state is represented by a CustomScanState, which is declared as follows:

```
typedef struct CustomScanState
{
 ScanState ss;
 uint32 flags;
 const CustomExecMethods *methods;
} CustomScanState;
```

ss is initialized as for any other scan state, except that if the scan is for a join rather than a base relation, ss.ss\_currentRelation is left NULL. flags is a bit mask with the same meaning as in CustomPath and CustomScan. methods must point to a (usually statically allocated) object implementing the required custom scan state methods, which are further detailed below. Typically, a CustomScanState, which need not support copyObject, will actually be a larger structure embedding the above as its first member.