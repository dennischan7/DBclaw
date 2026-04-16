---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The following resources contain additional information about genetic algorithms:

- [The Hitch-Hiker's Guide to Evolutionary Computation](http://www.faqs.org/faqs/ai-faq/genetic/part1/)<sup>1</sup> , (FAQ for [news://comp.ai.genetic\)](news://comp.ai.genetic)
- [Evolutionary Computation and its application to art and design](https://www.red3d.com/cwr/evolve.md)<sup>2</sup> , by Craig Reynolds
- [elma04]
- [fong]

<sup>1</sup> <http://www.faqs.org/faqs/ai-faq/genetic/part1/>

<sup>2</sup> <https://www.red3d.com/cwr/evolve.html>

# <span id="page-81-0"></span>**Chapter 63. Table Access Method Interface Definition**

This chapter explains the interface between the core PostgreSQL system and *table access methods*, which manage the storage for tables. The core system knows little about these access methods beyond what is specified here, so it is possible to develop entirely new access method types by writing addon code.

Each table access method is described by a row in the pg\_am system catalog. The pg\_am entry specifies a name and a *handler function* for the table access method. These entries can be created and deleted using the CREATE ACCESS METHOD and DROP ACCESS METHOD SQL commands.

A table access method handler function must be declared to accept a single argument of type internal and to return the pseudo-type table\_am\_handler. The argument is a dummy value that simply serves to prevent handler functions from being called directly from SQL commands. The result of the function must be a pointer to a struct of type TableAmRoutine, which contains everything that the core code needs to know to make use of the table access method. The return value needs to be of server lifetime, which is typically achieved by defining it as a static const variable in global scope. The TableAmRoutine struct, also called the access method's *API struct*, defines the behavior of the access method using callbacks. These callbacks are pointers to plain C functions and are not visible or callable at the SQL level. All the callbacks and their behavior is defined in the TableAmRoutine structure (with comments inside the struct defining the requirements for callbacks). Most callbacks have wrapper functions, which are documented from the point of view of a user (rather than an implementor) of the table access method. For details, please refer to the [src/](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/access/tableam.h;hb=HEAD) [include/access/tableam.h](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/access/tableam.h;hb=HEAD)<sup>1</sup> file.

To implement an access method, an implementor will typically need to implement an AM-specific type of tuple table slot (see [src/include/executor/tuptable.h](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/executor/tuptable.h;hb=HEAD)<sup>2</sup> ), which allows code outside the access method to hold references to tuples of the AM, and to access the columns of the tuple.

Currently, the way an AM actually stores data is fairly unconstrained. For example, it's possible, but not required, to use postgres' shared buffer cache. In case it is used, it likely makes sense to use PostgreSQL's standard page layout as described in [Section 73.6](#page-167-0).

One fairly large constraint of the table access method API is that, currently, if the AM wants to support modifications and/or indexes, it is necessary for each tuple to have a tuple identifier (TID) consisting of a block number and an item number (see also [Section 73.6\)](#page-167-0). It is not strictly necessary that the subparts of TIDs have the same meaning they e.g., have for heap, but if bitmap scan support is desired (it is optional), the block number needs to provide locality.

For crash safety, an AM can use postgres' WAL, or a custom implementation. If WAL is chosen, either [Generic WAL Records](#page-98-0) can be used, or a [Custom WAL Resource Manager](#page-100-0) can be implemented.

To implement transactional support in a manner that allows different table access methods be accessed within a single transaction, it likely is necessary to closely integrate with the machinery in src/ backend/access/transam/xlog.c.

Any developer of a new table access method can refer to the existing heap implementation present in src/backend/access/heap/heapam\_handler.c for details of its implementation.

<sup>1</sup> <https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/access/tableam.h;hb=HEAD>

<sup>2</sup> <https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/executor/tuptable.h;hb=HEAD>

# <span id="page-82-0"></span>**Chapter 64. Index Access Method Interface Definition**

This chapter defines the interface between the core PostgreSQL system and *index access methods*, which manage individual index types. The core system knows nothing about indexes beyond what is specified here, so it is possible to develop entirely new index types by writing add-on code.

All indexes in PostgreSQL are what are known technically as *secondary indexes*; that is, the index is physically separate from the table file that it describes. Each index is stored as its own physical *relation* and so is described by an entry in the pg\_class catalog. The contents of an index are entirely under the control of its index access method. In practice, all index access methods divide indexes into standard-size pages so that they can use the regular storage manager and buffer manager to access the index contents. (All the existing index access methods furthermore use the standard page layout described in [Section 73.6,](#page-167-0) and most use the same format for index tuple headers; but these decisions are not forced on an access method.)

An index is effectively a mapping from some data key values to *tuple identifiers*, or TIDs, of row versions (tuples) in the index's parent table. A TID consists of a block number and an item number within that block (see [Section 73.6\)](#page-167-0). This is sufficient information to fetch a particular row version from the table. Indexes are not directly aware that under MVCC, there might be multiple extant versions of the same logical row; to an index, each tuple is an independent object that needs its own index entry. Thus, an update of a row always creates all-new index entries for the row, even if the key values did not change. [\(HOT tuples](#page-170-0) are an exception to this statement; but indexes do not deal with those, either.) Index entries for dead tuples are reclaimed (by vacuuming) when the dead tuples themselves are reclaimed.