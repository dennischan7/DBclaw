# Oracle 11g - statements_5002
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_5002.htm

Semantics

OR REPLACE

Specify `OR` `REPLACE` to redefine an existing context namespace using a different package.

namespace

Specify the name of the context namespace to create or modify. Context namespaces are always stored in the schema `SYS`.

schema

Specify the schema owning `package`. If you omit `schema`, then Oracle Database uses the current schema.

package

Specify the PL/SQL package that sets or resets the context attributes under the namespace for a user session.

To provide some design flexibility, Oracle Database does not verify the existence of the schema or the validity of the package at the time you create the context.

INITIALIZED Clause

The `INITIALIZED` clause lets you specify an entity other than Oracle Database that can initialize the context namespace.

EXTERNALLY `EXTERNALLY` indicates that the namespace can be initialized using an OCI interface when establishing a session.

GLOBALLY `GLOBALLY` indicates that the namespace can be initialized by the LDAP directory when a global user connects to the database.

After the session is established, only the designated PL/SQL package can issue commands to write to any attributes inside the namespace.

ACCESSED GLOBALLY

This clause indicates that any application context set in `namespace` is accessible throughout the entire instance. This setting lets multiple sessions share application attributes.

Examples

Creating an Application Context: Example This example uses a PL/SQL package `emp_mgmt`, which validates and secures a human resources application. See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/create_package.md#LNPLS01371) for the example that creates that package. The following statement creates the context namespace `hr_context` and associates it with the package `emp_mgmt`:

```
CREATE CONTEXT hr_context USING emp_mgmt;
```

You can control data access based on this context using the `SYS_CONTEXT` function. For example, the `emp_mgmt` package has defined an attribute `department_id` as a particular department identifier. You can secure the base table `employees` by creating a view that restricts access based on the value of `department_id`, as follows:

```
CREATE VIEW hr_org_secure_view AS
   SELECT * FROM employees
   WHERE department_id = SYS_CONTEXT('hr_context', 'department_id');
```