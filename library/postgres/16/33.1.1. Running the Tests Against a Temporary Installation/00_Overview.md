---
source: PostgreSQL 16 Reference
title: 00_Overview
---

To run the parallel regression tests after building but before installation, type:

```
make check
```

in the top-level directory. (Or you can change to src/test/regress and run the command there.) Tests which are run in parallel are prefixed with "+", and tests which run sequentially are prefixed with "-". At the end you should see something like:

```
# All 213 tests passed.
```

or otherwise a note about which tests failed. See [Section 33.2](#page-132-0) below before assuming that a "failure" represents a serious problem.

Because this test method runs a temporary server, it will not work if you did the build as the root user, since the server will not start as root. Recommended procedure is not to do the build as root, or else to perform testing after completing the installation.

If you have configured PostgreSQL to install into a location where an older PostgreSQL installation already exists, and you perform make check before installing the new version, you might find that the tests fail because the new programs try to use the already-installed shared libraries. (Typical symptoms are complaints about undefined symbols.) If you wish to run the tests before overwriting the old installation, you'll need to build with configure --disable-rpath. It is not recommended that you use this option for the final installation, however.

The parallel regression test starts quite a few processes under your user ID. Presently, the maximum concurrency is twenty parallel test scripts, which means forty processes: there's a server process and a psql process for each test script. So if your system enforces a per-user limit on the number of processes, make sure this limit is at least fifty or so, else you might get random-seeming failures in the parallel test. If you are not in a position to raise the limit, you can cut down the degree of parallelism by setting the MAX\_CONNECTIONS parameter. For example:

```
make MAX_CONNECTIONS=10 check
```

runs no more than ten tests concurrently.