---
source: MySQL 8.4 Reference
title: 00_Overview
---

To measure the speed of a specific MySQL expression or function, invoke the BENCHMARK() function using the mysql client program. Its syntax is BENCHMARK(loop\_count,expr). The return value is always zero, but mysql prints a line displaying approximately how long the statement took to execute. For example:

```
mysql> SELECT BENCHMARK(1000000,1+1);
+------------------------+
| BENCHMARK(1000000,1+1) |
+------------------------+
| 0 |
+------------------------+
1 row in set (0.32 sec)
```

This result was obtained on a Pentium II 400MHz system. It shows that MySQL can execute 1,000,000 simple addition expressions in 0.32 seconds on that system.

The built-in MySQL functions are typically highly optimized, but there may be some exceptions. BENCHMARK() is an excellent tool for finding out if some function is a problem for your queries.

# <span id="page-56-0"></span>**10.13.2 Using Your Own Benchmarks**

Benchmark your application and database to find out where the bottlenecks are. After fixing one bottleneck (or by replacing it with a "dummy" module), you can proceed to identify the next bottleneck. Even if the overall performance for your application currently is acceptable, you should at least make a plan for each bottleneck and decide how to solve it if someday you really need the extra performance.

A free benchmark suite is the Open Source Database Benchmark, available at [http://](http://osdb.sourceforge.net/) [osdb.sourceforge.net/.](http://osdb.sourceforge.net/)

It is very common for a problem to occur only when the system is very heavily loaded. We have had many customers who contact us when they have a (tested) system in production and have encountered load problems. In most cases, performance problems turn out to be due to issues of basic database design (for example, table scans are not good under high load) or problems with the operating system or libraries. Most of the time, these problems would be much easier to fix if the systems were not already in production.

To avoid problems like this, benchmark your whole application under the worst possible load:

- The mysqlslap program can be helpful for simulating a high load produced by multiple clients issuing queries simultaneously. See Section 6.5.7, "mysqlslap — A Load Emulation Client".
- You can also try benchmarking packages such as SysBench and DBT2, available at [https://](https://launchpad.net/sysbench) [launchpad.net/sysbench,](https://launchpad.net/sysbench) and <http://osdldbt.sourceforge.net/#dbt2>.

These programs or packages can bring a system to its knees, so be sure to use them only on your development systems.