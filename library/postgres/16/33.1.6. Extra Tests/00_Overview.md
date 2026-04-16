---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The core regression test suite contains a few test files that are not run by default, because they might be platform-dependent or take a very long time to run. You can run these or other extra test files by setting the variable EXTRA\_TESTS. For example, to run the numeric\_big test:

make check EXTRA\_TESTS=numeric\_big

# <span id="page-132-0"></span>**33.2. Test Evaluation**

Some properly installed and fully functional PostgreSQL installations can "fail" some of these regression tests due to platform-specific artifacts such as varying floating-point representation and message wording. The tests are currently evaluated using a simple diff comparison against the outputs generated on a reference system, so the results are sensitive to small system differences. When a test is reported as "failed", always examine the differences between expected and actual results; you might find that the differences are not significant. Nonetheless, we still strive to maintain accurate reference files across all supported platforms, so it can be expected that all tests pass.

The actual outputs of the regression tests are in files in the src/test/regress/results directory. The test script uses diff to compare each output file against the reference outputs stored in the src/test/regress/expected directory. Any differences are saved for your inspection in src/test/regress/regression.diffs. (When running a test suite other than the core tests, these files of course appear in the relevant subdirectory, not src/test/regress.)

If you don't like the diff options that are used by default, set the environment variable PG\_RE-GRESS\_DIFF\_OPTS, for instance PG\_REGRESS\_DIFF\_OPTS='-c'. (Or you can run diff yourself, if you prefer.)

If for some reason a particular platform generates a "failure" for a given test, but inspection of the output convinces you that the result is valid, you can add a new comparison file to silence the failure report in future test runs. See [Section 33.3](#page-134-0) for details.