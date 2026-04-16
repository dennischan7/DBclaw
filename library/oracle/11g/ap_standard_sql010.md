# Oracle 11g - ap_standard_sql010
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/ap_standard_sql010.htm

|  |  |
| --- | --- |
| X010, XML type | Oracle fully supports this feature. |
| X011, Arrays of XML types | Oracle supports this feature using named array types (in the standard, array types are anonymous) |
| X012, Multisets of XML type | The Oracle equivalent of a multiset of XML type is a nested table with a single column of XML type. |
| X013, Distinct types of XML | A distinct type can be emulated using an object type with a single attribute. |
| X014, Attributes of XML type | In Oracle, attributes of object types may be of type `XMLType`, but the syntax for creating object types is nonstandard. |
| X016, Persistent XML values | Oracle fully supports this feature. |
| X020, XML Concatenation | Oracle fully supports this feature. |
| X025, `XMLCast` | Oracle provides equivalents for the following elements of this feature:   * To cast from XML to a scalar type, use `EXTRACTVALUE`. If the XML value is typed, then the result is in the nearest analog to the XML type, otherwise the result type is `VARCHAR`(4000). Use `CAST` to convert to any other scalar type. * To cast from a scalar type to XML, pass the scalar value in to `XMLQuery` and insert it in a document constructor.   Since Oracle has only one XML type, there is no need to cast from XML to XML. |
| X031, `XMLElement` | Oracle fully supports this feature. |
| X032, `XMLForest` | Oracle fully supports this feature. |
| X034, `XMLAgg` | Oracle fully supports this feature. |
| X035, `XMLAgg`: `ORDER` `BY` option | Oracle fully supports this feature. |
| X036, `XMLComment` | Oracle fully supports this feature. |
| X036, `XMLPi` | Oracle fully supports this feature. |
| X038, `XMLText` | The Oracle `XMLCData` function may be used to create a text node. |
| X040, Basic table mapping | Oracle table mappings are available through a Java interface and through a package. Oracle table mappings have been generalized to map queries and not just tables. To map only a table: `SELECT` `*` `FROM` `table_name`. This provides support for the following elements of this feature:   * X041, Basic table mapping: null absent * X042, Basic table mapping: null as nil * X043, Basic table mapping: table as forest * X044, Basic table mapping: table as element * X045, Basic table mapping: with target namespace * X046, Basic table mapping: data mapping * X047, Basic table mapping: metadata mapping * X049, Basic table mapping: hex encoding   Oracle does not support the following element of this feature: |
| X060, `XMLParse`: Character string input and `CONTENT` option | Oracle does not support the {`PRESERVE` | `STRIP`} `WHITESPACE` syntax. The behavior is always `STRIP` `WHITESPACE`. |
| X061, `XMLParse`: Character string input and `DOCUMENT` option | Oracle does not support the {`PRESERVE` | `STRIP`} `WHITESPACE` syntax. The behavior is always `STRIP` `WHITESPACE`. |
| X070, `XMLSerialize`: Character string serialization and `CONTENT` option | Oracle fully supports this feature. |
| X071, `XMLSerialize`: Character string serialization and `DOCUMENT` option | Oracle fully supports this feature. |
| X072, `XMLSerialize`: Character string serialization | Oracle fully supports this feature. |
| X076, `XMLSerialize`: `VERSION` option | Use `XMLRoot` to set the XML version prior to serialization. |
| X080, Namespaces in XML publishing | In the Oracle implementation of `XMLElement`, `XMLAttributes` are used to define namespaces (`XMLNamespaces` is not implemented). However, `XMLAttributes` is not supported for `XMLForest`. |
| X086, XML namespace declarations in `XMLTable` | Oracle fully supports this feature. |
| X090, XML document predicate | In Oracle, you can test whether an XML value is a document by using the `ISFRAGMENT` method. |
| X096, `XMLExists` | Use `EXISTSNODE` to evaluate an XPath, returning 1 if a node is found, 0 if not. XQuery expressions other than XPath expressions are not supported. Also, Oracle supports XPath 1.0 expressions (not XPath 2,0, which is a subset of XQuery). |
| X120, XML parameters in SQL routines | Oracle fully supports this feature. |
| X121, XML parameters in external routines | Oracle supports XML values passed to external routines using a non-standard interface. |
| X141, `IS` `VALID` predicate: data drive case | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and supports the data-driven case. |
| X142, `IS` `VALID` predicate: `ACCORDING` `TO` clause | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and includes the equivalent of the `ACCORDING` `TO` clause. |
| X143, `IS` `VALID` predicate: `ELEMENT` clause | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and includes the equivalent of the `ELEMENT` clause. |
| X144, `IS` `VALID` predicate: schema location | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and supports the specification of a schema location for a registered XML Schema. |
| X145, `IS` `VALID` predicate outside check constraints | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and may be used outside check constraints. |
| X151, `IS` `VALID` predicate with `DOCUMENT` option | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and performs validation equivalent to the `DOCUMENT` clause. (`XMLISVALID` does not support "content" validation.) |
| X156, `IS` `VALID` predicate: optional `NAMESPACE` with `ELEMENT` clause | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and may be used to validate against an element in any namespace. |
| X157, `IS` `VALID` predicate: `NO` `NAMESPACE` with `ELEMENT` clause | The `XMLISVALID` method is equivalent to the `IS` `VALID` predicate, and may be used to validate against an element in the "no name" namespace. |
| X160, Basic Information Schema for registered XML Schemas | The Oracle static data dictionary view `ALL_XML_SCHEMAS` provides a list of the registered XML schemas that are accessible to the current user. The `ALL_XML_SCHEMAS`.`SCHEMA_URL` column corresponds to the standard `XML_SCHEMAS`.`XML_SCHEMA_LOCATION` column. The target namespace of the registered XML Schemas can be learned by examining `ALL_XML_SCHEMAS`.`SCHEMA`. Oracle has no equivalents for the other columns of the standard's `XML_SCHEMAS`. |
| X161, Advanced Information Schema for registered XML Schemas | Oracle does not have static data dictionary views corresponding to `XML_SCHEMA_NAMESPACES` and `XML_SCHEMA_ELEMENTS` in the standard. However, all the information about registered XML Schemas may be learned by examining the actual XML Schema, which is found in the `ALL_XML_SCHEMAS`.`SCHEMA` column. This may also be examined to learn whether a registered XML Schema is nondeterministic, and which of its namespaces and elements are nondeterministic. |
| X191, `XML`(`DOCUMENT` (`XMLSCHEMA`)) type | Oracle does not support this syntax. However, a column of a table can be constrained by a registered XML Schema, in which case all values of the column will be of `XML`(`DOCUMENT`(`XMLSCHEMA`)) type. |
| X200, XMLQuery | Oracle fully supports the following elements of this feature:   * X201, XMLQuery: `RETURNING` `CONTENT` * X203, XMLQuery: passing a context item * X204, XMLQuery: initializing an XQuery variable   Oracle does not support the following elements of this feature:   * X202, XMLQuery: `RETURNING` `SEQUENCE` * { `NULL` | `EMPTY` } `ON` `EMPTY` syntax * Mandatory `BY` { `REF` | `VALUE` } in the `PASSING` clause (Oracle supports only value semantics) |
| X221, XML passing mechanism `BY` `VALUE` | Oracle supports only value semantics, but does not support the explicit `BY` `VALUE` clause. |
| X232, `XML`(`CONTENT`(`ANY`)) type | Oracle does not support this syntax as a type modifier, but the Oracle `XMLType` supports this data type for transient values. Persistent values are of type `XML`(`DOCUMENT`(`ANY`)), which is a subset of `XML`(`CONTENT`(`ANY`)). |
| X241, `RETURNING` `CONTENT` in XML publishing | Oracle does not support this syntax. In Oracle, the behavior of the publishing functions (`XMLAgg`, `XMLComment`, `XMLConcat`, `XMLElement`, `XMLForest`, and `XMLPi`) is always `RETURNING` `CONTENT`. |
| X251, Persistent XML values of `XML`(`DOCUMENT`(`UNTYPED`)) type | Oracle fully supports this feature. |
| X252, Persistent values of type `XML`(`DOCUMENT`(`ANY`)) | Oracle fully supports this feature. |
| X256, Persistent values of `XML`(`DOCUMENT`(`XMLSCHEMA`)) type | Oracle fully supports this feature. |
| X260, XML type, `ELEMENT` clause | Oracle does not support this syntax. However, a column of a table may be constrained by a top-level element in a registered XML Schema. |
| X262, XML type, optional `NAMESPACE` with `ELEMENT` clause | Oracle does not support this syntax. However, a column of a table may be constrained by a top-level element in a namespace other than the target namespace of a registered XML Schema. |
| X263, XML type: `NO` `NAMESPACE` with `ELEMENT` clause | Oracle does not support this syntax. However, a column of a table may be constrained by a top-level element in the "no name" namespace of a registered XML Schema. |
| X264, XML type: schema location | Oracle does not support this syntax. However, a column of a table may be constrained by a registered XML Schema that is identified by a schema location. |
| X271, XMLValidate: data driven case | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and supports the data-driven case. |
| X272, XMLValidate: `ACCORDING` `TO` clause | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and may be used to specify a particular registered XML Schema. |
| X273, XMLValidate: `ELEMENT` clause | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and may be used to specify a particular element of a particular registered XML Schema. |
| X274, XMLValidate: schema location | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and may be used to specify a particular registered XML Schema by its schema location URL. |
| X281, XMLValidate with `DOCUMENT` option | The `SCHEMAVALIDATE` method is equivalent to XMLValidate. `SCHEMAVALIDATE` performs validation only of XML documents (not content). |
| X285, XMLValidate: optional `NAMESPACE` with `ELEMENT` clause | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and may be used to specify a particular element in a namespace other than the target namespace of a particular registered XML Schema. |
| X286, XMLValidate: `NO` `NAMESPACE` with `ELEMENT` clause | The `SCHEMAVALIDATE` method is equivalent to XMLValidate, and may be used to specify a particular element in the "no name" namespace of a particular registered XML Schema. |
| X300, `XMLTable` | Oracle does not support reverse axes in the column path expressions. Aside from that restriction, Oracle fully supports the following elements of this feature:   * X086, XML namespace declarations in `XMLTable` * X302, `XMLTable` with ordinality column * X303, `XMLTable`: column default option * X304, `XMLTable`: passing a context item * X305, `XMLTable`: initializing an XQuery variable   Oracle does not support the following elements of this feature:   * X301, `XMLTable`: derived column list option * Mandatory `BY` {`REF` | `VALUE`} in the `PASSING` clause. Oracle supports only `BY` `VALUE` semantics currently. |