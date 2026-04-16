---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL provides infrastructure to create custom modules for continuous archiving (see Section 26.3). While archiving via a shell command (i.e., archive\_command) is much simpler, a custom archive module will often be considerably more robust and performant.

When a custom archive\_library is configured, PostgreSQL will submit completed WAL files to the module, and the server will avoid recycling or removing these WAL files until the module indicates that the files were successfully archived. It is ultimately up to the module to decide what to do with each WAL file, but many recommendations are listed at Section 26.3.1.

Archiving modules must at least consist of an initialization function (see [Section 51.1](#page-147-0)) and the required callbacks (see [Section 51.2\)](#page-147-1). However, archive modules are also permitted to do much more (e.g., declare GUCs and register background workers).

The contrib/basic\_archive module contains a working example, which demonstrates some useful techniques.

## <span id="page-147-0"></span>**51.1. Initialization Functions**

An archive library is loaded by dynamically loading a shared library with the archive\_library's name as the library base name. The normal library search path is used to locate the library. To provide the required archive module callbacks and to indicate that the library is actually an archive module, it needs to provide a function named \_PG\_archive\_module\_init. The result of the function must be a pointer to a struct of type ArchiveModuleCallbacks, which contains everything that the core code needs to know to make use of the archive module. The return value needs to be of server lifetime, which is typically achieved by defining it as a static const variable in global scope.

```
typedef struct ArchiveModuleCallbacks
{
 ArchiveStartupCB startup_cb;
 ArchiveCheckConfiguredCB check_configured_cb;
 ArchiveFileCB archive_file_cb;
 ArchiveShutdownCB shutdown_cb;
} ArchiveModuleCallbacks;
typedef const ArchiveModuleCallbacks *(*ArchiveModuleInit) (void);
```

Only the archive\_file\_cb callback is required. The others are optional.

## <span id="page-147-1"></span>**51.2. Archive Module Callbacks**

The archive callbacks define the actual archiving behavior of the module. The server will call them as required to process each individual WAL file.