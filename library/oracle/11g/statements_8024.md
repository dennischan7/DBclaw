# Oracle 11g - statements_8024
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8024.htm

[Go to main content](#BEGIN)

452/522 

# DROP OUTLINE

Purpose

Note:

Oracle strongly recommends that you use SQL plan management for new applications. SQL plan management creates SQL plan baselines, which offer superior SQL performance stability compared with stored outlines.

You can migrate existing stored outlines to SQL plan baselines by using the `MIGRATE_STORED_OUTLINE` function of the `DBMS_SPM` package or Enterprise Manager DB Control. When the migration is complete, the stored outlines are marked as migrated and can be removed. You can drop all migrated stored outlines on your system by using the `DROP_MIGRATED_STORED_OUTLINE` function of the `DBMS_SPM` package.

See Also: [Oracle Database Performance Tuning Guide](../../server.112/e41573/optplanmgmt.md#PFGRF007) for more information about SQL plan management and [Oracle Database PL/SQL Packages and Types Reference](../../appdev.112/e40758/d_spm.md#ARPLS150) for information about the `DBMS_SPM` package

Use the `DROP` `OUTLINE` statement to drop a stored outline.

Prerequisites

To drop an outline, you must have the `DROP` `ANY` `OUTLINE` system privilege.

Semantics

outline

Specify the name of the outline to be dropped.

After the outline is dropped, if the SQL statement for which the stored outline was created is compiled, then the optimizer generates a new execution plan without the influence of the outline.

Examples

Dropping an Outline: Example The following statement drops the stored outline called `salaries`.

```
DROP OUTLINE salaries;
```

Scripting on this page enhances content navigation, but does not change the content in any way.