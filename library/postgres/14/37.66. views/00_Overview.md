---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view views contains all views defined in the current database. Only those views are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.64. views Columns**

```
Column Type
       Description
table_catalog sql_identifier
       Name of the database that contains the view (always the current database)
table_schema sql_identifier
       Name of the schema that contains the view
table_name sql_identifier
       Name of the view
view_definition character_data
       Query expression defining the view (null if the view is not owned by a currently enabled
       role)
check_option character_data
       CASCADED or LOCAL if the view has a CHECK OPTION defined on it, NONE if not
is_updatable yes_or_no
       YES if the view is updatable (allows UPDATE and DELETE), NO if not
is_insertable_into yes_or_no
       YES if the view is insertable into (allows INSERT), NO if not
is_trigger_updatable yes_or_no
       YES if the view has an INSTEAD OF UPDATE trigger defined on it, NO if not
is_trigger_deletable yes_or_no
```

YES if the view has an INSTEAD OF DELETE trigger defined on it, NO if not

is\_trigger\_insertable\_into yes\_or\_no YES if the view has an INSTEAD OF INSERT trigger defined on it, NO if not

# **Part V. Server Programming**

This part is about extending the server functionality with user-defined functions, data types, triggers, etc. These are advanced topics which should probably be approached only after all the other user documentation about PostgreSQL has been understood. Later chapters in this part describe the server-side programming languages available in the PostgreSQL distribution as well as general issues concerning server-side programming languages. It is essential to read at least the earlier sections of [Chapter 38](#page-150-0) (covering functions) before diving into the material about server-side programming languages.

## **Table of Contents**

| 38. Extending SQL 1113                                           |      |
|------------------------------------------------------------------|------|
| 38.1. How Extensibility Works 1113                               |      |
| 38.2. The PostgreSQL Type System 1113                            |      |
| 38.2.1. Base Types 1113                                          |      |
| 38.2.2. Container Types 1113                                     |      |
| 38.2.3. Domains 1114                                             |      |
| 38.2.4. Pseudo-Types 1114                                        |      |
| 38.2.5. Polymorphic Types                                        | 1114 |
| 38.3. User-Defined Functions 1116                                |      |
| 38.4. User-Defined Procedures                                    | 1117 |
| 38.5. Query Language (SQL) Functions 1117                        |      |
| 38.5.1. Arguments for SQL Functions 1118                         |      |
| 38.5.2. SQL Functions on Base Types                              | 1119 |
| 38.5.3. SQL Functions on Composite Types 1121                    |      |
| 38.5.4. SQL Functions with Output Parameters 1124                |      |
| 38.5.5. SQL Procedures with Output Parameters 1125               |      |
| 38.5.6. SQL Functions with Variable Numbers of Arguments 1125    |      |
| 38.5.7. SQL Functions with Default Values for Arguments 1126     |      |
| 38.5.8. SQL Functions as Table Sources 1127                      |      |
| 38.5.9. SQL Functions Returning Sets 1128                        |      |
| 38.5.10. SQL Functions Returning TABLE 1131                      |      |
| 38.5.11. Polymorphic SQL Functions 1132                          |      |
| 38.5.12. SQL Functions with Collations 1134                      |      |
| 38.6. Function Overloading 1134                                  |      |
| 38.7. Function Volatility Categories                             | 1135 |
| 38.8. Procedural Language Functions 1137                         |      |
| 38.9. Internal Functions 1137                                    |      |
| 38.10. C-Language Functions 1137                                 |      |
| 38.10.1. Dynamic Loading 1137                                    |      |
| 38.10.2. Base Types in C-Language Functions 1139                 |      |
| 38.10.3. Version 1 Calling Conventions                           | 1141 |
| 38.10.4. Writing Code 1144                                       |      |
| 38.10.5. Compiling and Linking Dynamically-Loaded Functions 1145 |      |
| 38.10.6. Composite-Type Arguments 1147                           |      |
| 38.10.7. Returning Rows (Composite Types) 1148                   |      |
| 38.10.8. Returning Sets 1150                                     |      |
| 38.10.9. Polymorphic Arguments and Return Types                  | 1156 |
| 38.10.10. Shared Memory and LWLocks 1157                         |      |
| 38.10.11. Using C++ for Extensibility 1158                       |      |
| 38.11. Function Optimization Information                         | 1158 |
| 38.12. User-Defined Aggregates                                   | 1159 |
| 38.12.1. Moving-Aggregate Mode 1161                              |      |
| 38.12.2. Polymorphic and Variadic Aggregates 1162                |      |
| 38.12.3. Ordered-Set Aggregates 1164                             |      |
| 38.12.4. Partial Aggregation 1165                                |      |
| 38.12.5. Support Functions for Aggregates 1166                   |      |
| 38.13. User-Defined Types                                        | 1166 |
|                                                                  |      |
| 38.13.1. TOAST Considerations 1169                               |      |
| 38.14. User-Defined Operators                                    | 1171 |
| 38.15. Operator Optimization Information                         | 1171 |
| 38.15.1. COMMUTATOR 1172                                         |      |
| 38.15.2. NEGATOR 1172                                            |      |
| 38.15.3. RESTRICT 1173                                           |      |
| 38.15.4. JOIN 1173                                               |      |
| 38.15.5. HASHES 1174                                             |      |

| 38.15.6. MERGES 1175                                    |      |
|---------------------------------------------------------|------|
| 38.16. Interfacing Extensions to Indexes                | 1175 |
| 38.16.1. Index Methods and Operator Classes             | 1176 |
| 38.16.2. Index Method Strategies 1176                   |      |
| 38.16.3. Index Method Support Routines 1178             |      |
| 38.16.4. An Example 1181                                |      |
| 38.16.5. Operator Classes and Operator Families         | 1183 |
| 38.16.6. System Dependencies on Operator Classes 1186   |      |
| 38.16.7. Ordering Operators 1187                        |      |
| 38.16.8. Special Features of Operator Classes 1188      |      |
| 38.17. Packaging Related Objects into an Extension 1188 |      |
| 38.17.1. Extension Files                                | 1189 |
| 38.17.2. Extension Relocatability 1191                  |      |
| 38.17.3. Extension Configuration Tables                 | 1192 |
| 38.17.4. Extension Updates 1193                         |      |
|                                                         |      |
| 38.17.5. Installing Extensions Using Update Scripts     | 1194 |
| 38.17.6. Security Considerations for Extensions 1195    |      |
| 38.17.7. Extension Example 1196                         |      |
| 38.18. Extension Building Infrastructure 1197           |      |
| 39. Triggers 1201                                       |      |
| 39.1. Overview of Trigger Behavior 1201                 |      |
| 39.2. Visibility of Data Changes 1204                   |      |
| 39.3. Writing Trigger Functions in C 1204               |      |
| 39.4. A Complete Trigger Example 1207                   |      |
| 40. Event Triggers 1211                                 |      |
| 40.1. Overview of Event Trigger Behavior                | 1211 |
| 40.2. Event Trigger Firing Matrix 1212                  |      |
| 40.3. Writing Event Trigger Functions in C 1215         |      |
| 40.4. A Complete Event Trigger Example                  | 1216 |
| 40.5. A Table Rewrite Event Trigger Example 1218        |      |
| 41. The Rule System                                     | 1219 |
|                                                         |      |
| 41.1. The Query Tree 1219                               |      |
| 41.2. Views and the Rule System 1220                    |      |
| 41.2.1. How SELECT Rules Work 1221                      |      |
| 41.2.2. View Rules in Non-SELECT Statements 1225        |      |
| 41.2.3. The Power of Views in PostgreSQL 1226           |      |
| 41.2.4. Updating a View 1227                            |      |
| 41.3. Materialized Views 1227                           |      |
| 41.4. Rules on INSERT, UPDATE, and DELETE 1230          |      |
| 41.4.1. How Update Rules Work                           | 1231 |
| 41.4.2. Cooperation with Views 1235                     |      |
| 41.5. Rules and Privileges                              | 1241 |
| 41.6. Rules and Command Status 1243                     |      |
| 41.7. Rules Versus Triggers 1243                        |      |
| 42. Procedural Languages 1246                           |      |
| 42.1. Installing Procedural Languages 1246              |      |
| 43. PL/pgSQL — SQL Procedural Language 1249             |      |
| 43.1. Overview 1249                                     |      |
|                                                         |      |
| 43.1.1. Advantages of Using PL/pgSQL 1249               |      |
| 43.1.2. Supported Argument and Result Data Types 1249   |      |
| 43.2. Structure of PL/pgSQL 1250                        |      |
| 43.3. Declarations 1252                                 |      |
| 43.3.1. Declaring Function Parameters 1252              |      |
| 43.3.2. ALIAS 1256                                      |      |
| 43.3.3. Copying Types 1256                              |      |
| 43.3.4. Row Types                                       | 1256 |
| 43.3.5. Record Types 1257                               |      |
| 43.3.6. Collation of PL/pgSQL Variables 1257            |      |

|       | 43.4. | Expressions                                          | 1238 |
|-------|-------|------------------------------------------------------|------|
|       | 43.5. | Basic Statements                                     | 1259 |
|       |       | 43.5.1. Assignment                                   | 1259 |
|       |       | 43.5.2. Executing SQL Commands                       |      |
|       |       | 43.5.3. Executing a Command with a Single-Row Result |      |
|       |       | 43.5.4. Executing Dynamic Commands                   |      |
|       |       | 43.5.5. Obtaining the Result Status                  |      |
|       |       | 43.5.6. Doing Nothing At All                         |      |
|       | 12.6  |                                                      |      |
|       | 43.6. | Control Structures                                   |      |
|       |       | 43.6.1. Returning from a Function                    |      |
|       |       | 43.6.2. Returning from a Procedure                   |      |
|       |       | 43.6.3. Calling a Procedure                          |      |
|       |       | 43.6.4. Conditionals                                 | 1270 |
|       |       | 43.6.5. Simple Loops                                 | 1273 |
|       |       | 43.6.6. Looping through Query Results                | 1276 |
|       |       | 43.6.7. Looping through Arrays                       | 1277 |
|       |       | 43.6.8. Trapping Errors                              |      |
|       |       | 43.6.9. Obtaining Execution Location Information     |      |
|       | 43 7  | Cursors                                              |      |
|       | 13.7. | 43.7.1. Declaring Cursor Variables                   |      |
|       |       | 43.7.2. Opening Cursors                              |      |
|       |       | 43.7.3. Using Cursors                                |      |
|       |       |                                                      |      |
|       | 42.0  | 43.7.4. Looping through a Cursor's Result            |      |
|       |       | Transaction Management                               |      |
|       | 43.9. | Errors and Messages                                  |      |
|       |       | 43.9.1. Reporting Errors and Messages                |      |
|       |       | 43.9.2. Checking Assertions                          |      |
|       | 43.10 | ). Trigger Functions                                 | 1291 |
|       |       | 43.10.1. Triggers on Data Changes                    | 1291 |
|       |       | 43.10.2. Triggers on Events                          | 1299 |
|       | 43.11 | PL/pgSQL under the Hood                              |      |
|       |       | 43.11.1. Variable Substitution                       |      |
|       |       | 43.11.2. Plan Caching                                |      |
|       | 43 12 | 2. Tips for Developing in PL/pgSQL                   |      |
|       | 13.12 | 43.12.1. Handling of Quotation Marks                 |      |
|       |       | 43.12.2. Additional Compile-Time and Run-Time Checks |      |
|       | 42 13 | 3. Porting from Oracle PL/SQL                        |      |
|       | 45.13 | · · · · · · · · · · · · · · · · · · ·                |      |
|       |       | 43.13.1. Porting Examples                            |      |
|       |       | 43.13.2. Other Things to Watch For                   |      |
|       |       | 43.13.3. Appendix                                    |      |
| 14. P |       | — Tel Procedural Language                            |      |
|       |       | Overview                                             |      |
|       |       | PL/Tcl Functions and Arguments                       |      |
|       | 44.3. | Data Values in PL/Tcl                                | 1319 |
|       | 44.4. | Global Data in PL/Tcl                                | 1319 |
|       | 44.5. | Database Access from PL/Tcl                          | 1320 |
|       |       | Trigger Functions in PL/Tcl                          |      |
|       |       | Event Trigger Functions in PL/Tcl                    |      |
|       |       | Error Handling in PL/Tcl                             |      |
|       |       | Explicit Subtransactions in PL/Tcl                   |      |
|       |       | ). Transaction Management                            |      |
|       |       |                                                      |      |
|       |       | PL/Tcl Configuration                                 |      |
| 45 -  |       | 2. Tcl Procedure Names                               |      |
| 15. P |       | l — Perl Procedural Language                         |      |
|       |       | PL/Perl Functions and Arguments                      |      |
|       |       | Data Values in PL/Perl                               |      |
|       | 45.3. | Built-in Functions                                   |      |
|       |       | 45.3.1. Database Access from PL/Perl                 | 1333 |

| 45.4. Global Values in PL/Perl                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 1337                                                                                                                                         |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 1338                                                                                                                                         |
| 45.5. Trusted and Untrusted PL/Perl                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 1339                                                                                                                                         |
| 45.6. PL/Perl Triggers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 1340                                                                                                                                         |
| 45.7. PL/Perl Event Triggers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1342                                                                                                                                         |
| 45.8. PL/Perl Under the Hood                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1342                                                                                                                                         |
| 45.8.1. Configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 1342                                                                                                                                         |
| 45.8.2. Limitations and Missing Features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                              |
| 46. PL/Python — Python Procedural Language                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                              |
| 46.1. Python 2 vs. Python 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                              |
| 46.2. PL/Python Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                              |
| 46.3. Data Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                              |
| 46.3.1. Data Type Mapping                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                              |
| 46.3.2. Null, None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                              |
| 46.3.3. Arrays, Lists                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                              |
| 46.3.4. Composite Types                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                              |
| 46.3.5. Set-Returning Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                              |
| 46.4. Sharing Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                              |
| 46.5. Anonymous Code Blocks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                              |
| 46.6. Trigger Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                              |
| 46.7. Database Access                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                              |
| 46.7.1. Database Access Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                              |
| 46.7.2. Trapping Errors                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                              |
| 46.8. Explicit Subtransactions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 1357                                                                                                                                         |
| 46.8.1. Subtransaction Context Managers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 1357                                                                                                                                         |
| 46.8.2. Older Python Versions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 1358                                                                                                                                         |
| 46.9. Transaction Management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1358                                                                                                                                         |
| 46.10. Utility Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                              |
| 46.11. Environment Variables                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                              |
| 47. Server Programming Interface                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                              |
| 47.1. Interface Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                              |
| 47.2. Interface Support Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                              |
| 47.3. Memory Management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                              |
| 47.4. Transaction Management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                              |
| · · · · · · · · · · · · · · · · · · ·                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 1422                                                                                                                                         |
| 47.5. Visibility of Data Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 1422<br>1425                                                                                                                                 |
| 47.5. Visibility of Data Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 1422<br>1425<br>1425                                                                                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 1422<br>1425<br>1425<br>1429                                                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 1422<br>1425<br>1425<br>1429<br>1432                                                                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 1422<br>1425<br>1425<br>1429<br>1432<br>1432                                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 1422<br>1425<br>1425<br>1429<br>1432<br>1432                                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1435                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots                                                                                                                                                                                                                                                                                                                                                                                                                                             | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1435                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding  49.1. Logical Decoding Examples  49.2. Logical Decoding Concepts  49.2.1. Logical Decoding  49.2.2. Replication Slots  49.2.3. Output Plugins                                                                                                                                                                                                                                                                                                                                                                                                               | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436                                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding  49.1. Logical Decoding Examples  49.2. Logical Decoding Concepts  49.2.1. Logical Decoding  49.2.2. Replication Slots  49.2.3. Output Plugins  49.2.4. Exported Snapshots                                                                                                                                                                                                                                                                                                                                                                                   | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436                                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface                                                                                                                                                                                                                                                                                                                                           | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1436                                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface                                                                                                                                                                                                                                                                                                      | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436<br>1437<br>1437                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding                                                                                                                                                                                                                                                   | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1436<br>1436<br>1436<br>1437<br>1437                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6. Logical Decoding Output Plugins                                                                                                                                                                                                             | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436<br>1437<br>1437                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding                                                                                                                                                                                                                                                   | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436<br>1437<br>1437                                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6. Logical Decoding Output Plugins                                                                                                                                                                                                             | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437                                                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding  49.1. Logical Decoding Examples  49.2. Logical Decoding Concepts  49.2.1. Logical Decoding  49.2.2. Replication Slots  49.2.3. Output Plugins  49.2.4. Exported Snapshots  49.3. Streaming Replication Protocol Interface  49.4. Logical Decoding SQL Interface  49.5. System Catalogs Related to Logical Decoding  49.6. Logical Decoding Output Plugins  49.6.1. Initialization Function                                                                                                                                                                  | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437                                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding  49.1. Logical Decoding Examples  49.2. Logical Decoding Concepts  49.2.1. Logical Decoding  49.2.2. Replication Slots  49.2.3. Output Plugins  49.2.4. Exported Snapshots  49.3. Streaming Replication Protocol Interface  49.4. Logical Decoding SQL Interface  49.5. System Catalogs Related to Logical Decoding  49.6. Logical Decoding Output Plugins  49.6.1. Initialization Function  49.6.2. Capabilities  49.6.3. Output Modes                                                                                                                      | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1438<br>1439                         |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6.1. Initialization Function 49.6.2. Capabilities 49.6.3. Output Modes 49.6.4. Output Plugin Callbacks                                                                                                                                          | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1438<br>1439<br>1439                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6.1. Initialization Function 49.6.2. Capabilities 49.6.3. Output Modes 49.6.4. Output Plugin Callbacks 49.6.5. Functions for Producing Output                                                                                                  | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1437<br>1438<br>1439<br>1449         |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6.1. Initialization Function 49.6.2. Capabilities 49.6.3. Output Modes 49.6.4. Output Plugin Callbacks 49.6.5. Functions for Producing Output 49.7. Logical Decoding Output Writers                                                              | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1437<br>1439<br>1449                 |
| 47.5. Visibility of Data Changes 47.6. Examples  48. Background Worker Processes  49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6.1. Initialization Function 49.6.2. Capabilities 49.6.3. Output Modes 49.6.4. Output Plugin Callbacks 49.6.5. Functions for Producing Output 49.7. Logical Decoding Output Writers 49.8. Synchronous Replication Support for Logical Decoding | 1422<br>1425<br>1425<br>1429<br>1432<br>1432<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1438<br>1439<br>1449<br>1445         |
| 47.5. Visibility of Data Changes 47.6. Examples 48. Background Worker Processes 49. Logical Decoding 49.1. Logical Decoding Examples 49.2. Logical Decoding Concepts 49.2.1. Logical Decoding 49.2.2. Replication Slots 49.2.3. Output Plugins 49.2.4. Exported Snapshots 49.3. Streaming Replication Protocol Interface 49.4. Logical Decoding SQL Interface 49.5. System Catalogs Related to Logical Decoding 49.6.1. Initialization Function 49.6.2. Capabilities 49.6.3. Output Modes 49.6.4. Output Plugin Callbacks 49.6.5. Functions for Producing Output 49.7. Logical Decoding Output Writers                                                              | 1422<br>1425<br>1425<br>1429<br>1432<br>1435<br>1435<br>1436<br>1436<br>1437<br>1437<br>1437<br>1437<br>1438<br>1439<br>1445<br>1445<br>1445 |

#### Server Programming

| 49.10. Two-phase Commit Support for Logical Decoding 1447 |  |
|-----------------------------------------------------------|--|
| 50. Replication Progress Tracking 1449                    |  |
|                                                           |  |

# <span id="page-150-0"></span>**Chapter 38. Extending SQL**

In the sections that follow, we will discuss how you can extend the PostgreSQL SQL query language by adding:

- functions (starting in [Section 38.3\)](#page-153-0)
- aggregates (starting in [Section 38.12](#page-196-0))
- data types (starting in Section 38.13)
- operators (starting in Section 38.14)
- operator classes for indexes (starting in Section 38.16)
- packages of related objects (starting in Section 38.17)

# <span id="page-150-1"></span>**38.1. How Extensibility Works**

PostgreSQL is extensible because its operation is catalog-driven. If you are familiar with standard relational database systems, you know that they store information about databases, tables, columns, etc., in what are commonly known as system catalogs. (Some systems call this the data dictionary.) The catalogs appear to the user as tables like any other, but the DBMS stores its internal bookkeeping in them. One key difference between PostgreSQL and standard relational database systems is that PostgreSQL stores much more information in its catalogs: not only information about tables and columns, but also information about data types, functions, access methods, and so on. These tables can be modified by the user, and since PostgreSQL bases its operation on these tables, this means that PostgreSQL can be extended by users. By comparison, conventional database systems can only be extended by changing hardcoded procedures in the source code or by loading modules specially written by the DBMS vendor.

The PostgreSQL server can moreover incorporate user-written code into itself through dynamic loading. That is, the user can specify an object code file (e.g., a shared library) that implements a new type or function, and PostgreSQL will load it as required. Code written in SQL is even more trivial to add to the server. This ability to modify its operation "on the fly" makes PostgreSQL uniquely suited for rapid prototyping of new applications and storage structures.

# <span id="page-150-2"></span>**38.2. The PostgreSQL Type System**

PostgreSQL data types can be divided into base types, container types, domains, and pseudo-types.

## <span id="page-150-3"></span>**38.2.1. Base Types**

Base types are those, like integer, that are implemented below the level of the SQL language (typically in a low-level language such as C). They generally correspond to what are often known as abstract data types. PostgreSQL can only operate on such types through functions provided by the user and only understands the behavior of such types to the extent that the user describes them. The builtin base types are described in Chapter 8.

Enumerated (enum) types can be considered as a subcategory of base types. The main difference is that they can be created using just SQL commands, without any low-level programming. Refer to Section 8.7 for more information.

## <span id="page-150-4"></span>**38.2.2. Container Types**

PostgreSQL has three kinds of "container" types, which are types that contain multiple values of other types. These are arrays, composites, and ranges.

Arrays can hold multiple values that are all of the same type. An array type is automatically created for each base type, composite type, range type, and domain type. But there are no arrays of arrays. So far as the type system is concerned, multi-dimensional arrays are the same as one-dimensional arrays. Refer to Section 8.15 for more information.

Composite types, or row types, are created whenever the user creates a table. It is also possible to use CREATE TYPE to define a "stand-alone" composite type with no associated table. A composite type is simply a list of types with associated field names. A value of a composite type is a row or record of field values. Refer to Section 8.16 for more information.

A range type can hold two values of the same type, which are the lower and upper bounds of the range. Range types are user-created, although a few built-in ones exist. Refer to Section 8.17 for more information.

## <span id="page-151-0"></span>**38.2.3. Domains**

A domain is based on a particular underlying type and for many purposes is interchangeable with its underlying type. However, a domain can have constraints that restrict its valid values to a subset of what the underlying type would allow. Domains are created using the SQL command CREATE DOMAIN. Refer to Section 8.18 for more information.

## <span id="page-151-1"></span>**38.2.4. Pseudo-Types**

There are a few "pseudo-types" for special purposes. Pseudo-types cannot appear as columns of tables or components of container types, but they can be used to declare the argument and result types of functions. This provides a mechanism within the type system to identify special classes of functions. Table 8.27 lists the existing pseudo-types.

## <span id="page-151-2"></span>**38.2.5. Polymorphic Types**

Some pseudo-types of special interest are the *polymorphic types*, which are used to declare *polymorphic functions*. This powerful feature allows a single function definition to operate on many different data types, with the specific data type(s) being determined by the data types actually passed to it in a particular call. The polymorphic types are shown in [Table 38.1.](#page-151-3) Some examples of their use appear in [Section 38.5.11.](#page-169-0)

<span id="page-151-3"></span>**Table 38.1. Polymorphic Types**

| Name               | Family | Description                                                                                                                            |
|--------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------|
| anyelement         | Simple | Indicates that a function accepts any<br>data type                                                                                     |
| anyarray           | Simple | Indicates that a function accepts any<br>array data type                                                                               |
| anynonarray        | Simple | Indicates that a function accepts any<br>non-array data type                                                                           |
| anyenum            | Simple | Indicates that a function accepts any<br>enum data type (see Section 8.7)                                                              |
| anyrange           | Simple | Indicates that a function accepts any<br>range data type (see Section 8.17)                                                            |
| anymultirange      | Simple | Indicates that a function accepts any<br>multirange data type (see Section 8.17)                                                       |
| anycompatible      | Common | Indicates that a function accepts any<br>data type, with automatic promotion of<br>multiple arguments to a common data<br>type         |
| anycompatiblearray | Common | Indicates that a function accepts any<br>array data type, with automatic promo<br>tion of multiple arguments to a com<br>mon data type |

| Name                    | Family | Description                                                                                                                               |
|-------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------|
| anycompatiblenonarray   | Common | Indicates that a function accepts any<br>non-array data type, with automatic<br>promotion of multiple arguments to a<br>common data type  |
| anycompatiblerange      | Common | Indicates that a function accepts any<br>range data type, with automatic pro<br>motion of multiple arguments to a<br>common data type     |
| anycompatiblemultirange | Common | Indicates that a function accepts any<br>multirange data type, with automatic<br>promotion of multiple arguments to a<br>common data type |

Polymorphic arguments and results are tied to each other and are resolved to specific data types when a query calling a polymorphic function is parsed. When there is more than one polymorphic argument, the actual data types of the input values must match up as described below. If the function's result type is polymorphic, or it has output parameters of polymorphic types, the types of those results are deduced from the actual types of the polymorphic inputs as described below.

For the "simple" family of polymorphic types, the matching and deduction rules work like this:

Each position (either argument or return value) declared as anyelement is allowed to have any specific actual data type, but in any given call they must all be the *same* actual type. Each position declared as anyarray can have any array data type, but similarly they must all be the same type. And similarly, positions declared as anyrange must all be the same range type. Likewise for anymultirange.

Furthermore, if there are positions declared anyarray and others declared anyelement, the actual array type in the anyarray positions must be an array whose elements are the same type appearing in the anyelement positions. anynonarray is treated exactly the same as anyelement, but adds the additional constraint that the actual type must not be an array type. anyenum is treated exactly the same as anyelement, but adds the additional constraint that the actual type must be an enum type.

Similarly, if there are positions declared anyrange and others declared anyelement or anyarray, the actual range type in the anyrange positions must be a range whose subtype is the same type appearing in the anyelement positions and the same as the element type of the anyarray positions. If there are positions declared anymultirange, their actual multirange type must contain ranges matching parameters declared anyrange and base elements matching parameters declared anyelement and anyarray.

Thus, when more than one argument position is declared with a polymorphic type, the net effect is that only certain combinations of actual argument types are allowed. For example, a function declared as equal(anyelement, anyelement) will take any two input values, so long as they are of the same data type.

When the return value of a function is declared as a polymorphic type, there must be at least one argument position that is also polymorphic, and the actual data type(s) supplied for the polymorphic arguments determine the actual result type for that call. For example, if there were not already an array subscripting mechanism, one could define a function that implements subscripting as subscript(anyarray, integer) returns anyelement. This declaration constrains the actual first argument to be an array type, and allows the parser to infer the correct result type from the actual first argument's type. Another example is that a function declared as f(anyarray) returns anyenum will only accept arrays of enum types.

In most cases, the parser can infer the actual data type for a polymorphic result type from arguments that are of a different polymorphic type in the same family; for example anyarray can be deduced from anyelement or vice versa. An exception is that a polymorphic result of type anyrange requires an argument of type anyrange; it cannot be deduced from anyarray or anyelement arguments. This is because there could be multiple range types with the same subtype.

Note that anynonarray and anyenum do not represent separate type variables; they are the same type as anyelement, just with an additional constraint. For example, declaring a function as f(anyelement, anyenum) is equivalent to declaring it as f(anyenum, anyenum): both actual arguments have to be the same enum type.

For the "common" family of polymorphic types, the matching and deduction rules work approximately the same as for the "simple" family, with one major difference: the actual types of the arguments need not be identical, so long as they can be implicitly cast to a single common type. The common type is selected following the same rules as for UNION and related constructs (see Section 10.5). Selection of the common type considers the actual types of anycompatible and anycompatiblenonarray inputs, the array element types of anycompatiblearray inputs, the range subtypes of anycompatiblerange inputs, and the multirange subtypes of anycompatiblemultirange inputs. If anycompatiblenonarray is present then the common type is required to be a non-array type. Once a common type is identified, arguments in anycompatible and anycompatiblenonarray positions are automatically cast to that type, and arguments in anycompatiblearray positions are automatically cast to the array type for that type.

Since there is no way to select a range type knowing only its subtype, use of anycompatiblerange and/or anycompatiblemultirange requires that all arguments declared with that type have the same actual range and/or multirange type, and that that type's subtype agree with the selected common type, so that no casting of the range values is required. As with anyrange and anymultirange, use of anycompatiblerange and anymultirange as a function result type requires that there be an anycompatiblerange or anycompatiblemultirange argument.

Notice that there is no anycompatibleenum type. Such a type would not be very useful, since there normally are not any implicit casts to enum types, meaning that there would be no way to resolve a common type for dissimilar enum inputs.

The "simple" and "common" polymorphic families represent two independent sets of type variables. Consider for example

```
CREATE FUNCTION myfunc(a anyelement, b anyelement,
 c anycompatible, d anycompatible)
RETURNS anycompatible AS ...
```

In an actual call of this function, the first two inputs must have exactly the same type. The last two inputs must be promotable to a common type, but this type need not have anything to do with the type of the first two inputs. The result will have the common type of the last two inputs.

A variadic function (one taking a variable number of arguments, as in [Section 38.5.6](#page-162-1)) can be polymorphic: this is accomplished by declaring its last parameter as VARIADIC anyarray or VARIADIC anycompatiblearray. For purposes of argument matching and determining the actual result type, such a function behaves the same as if you had written the appropriate number of anynonarray or anycompatiblenonarray parameters.

# <span id="page-153-0"></span>**38.3. User-Defined Functions**

PostgreSQL provides four kinds of functions:

- query language functions (functions written in SQL) ([Section 38.5\)](#page-154-1)
- procedural language functions (functions written in, for example, PL/pgSQL or PL/Tcl) ([Sec](#page-174-0)[tion 38.8\)](#page-174-0)
- internal functions [\(Section 38.9](#page-174-1))

• C-language functions ([Section 38.10\)](#page-174-2)

Every kind of function can take base types, composite types, or combinations of these as arguments (parameters). In addition, every kind of function can return a base type or a composite type. Functions can also be defined to return sets of base or composite values.

Many kinds of functions can take or return certain pseudo-types (such as polymorphic types), but the available facilities vary. Consult the description of each kind of function for more details.

It's easiest to define SQL functions, so we'll start by discussing those. Most of the concepts presented for SQL functions will carry over to the other types of functions.

Throughout this chapter, it can be useful to look at the reference page of the CREATE FUNCTION command to understand the examples better. Some examples from this chapter can be found in funcs.sql and funcs.c in the src/tutorial directory in the PostgreSQL source distribution.

# <span id="page-154-0"></span>**38.4. User-Defined Procedures**

A procedure is a database object similar to a function. The key differences are:

- Procedures are defined with the CREATE PROCEDURE command, not CREATE FUNCTION.
- Procedures do not return a function value; hence CREATE PROCEDURE lacks a RETURNS clause. However, procedures can instead return data to their callers via output parameters.
- While a function is called as part of a query or DML command, a procedure is called in isolation using the CALL command.
- A procedure can commit or roll back transactions during its execution (then automatically beginning a new transaction), so long as the invoking CALL command is not part of an explicit transaction block. A function cannot do that.
- Certain function attributes, such as strictness, don't apply to procedures. Those attributes control how the function is used in a query, which isn't relevant to procedures.

The explanations in the following sections about how to define user-defined functions apply to procedures as well, except for the points made above.

Collectively, functions and procedures are also known as *routines*. There are commands such as AL-TER ROUTINE and DROP ROUTINE that can operate on functions and procedures without having to know which kind it is. Note, however, that there is no CREATE ROUTINE command.

# <span id="page-154-1"></span>**38.5. Query Language (SQL) Functions**

SQL functions execute an arbitrary list of SQL statements, returning the result of the last query in the list. In the simple (non-set) case, the first row of the last query's result will be returned. (Bear in mind that "the first row" of a multirow result is not well-defined unless you use ORDER BY.) If the last query happens to return no rows at all, the null value will be returned.

Alternatively, an SQL function can be declared to return a set (that is, multiple rows) by specifying the function's return type as SETOF sometype, or equivalently by declaring it as RETURNS TA-BLE(columns). In this case all rows of the last query's result are returned. Further details appear below.

The body of an SQL function must be a list of SQL statements separated by semicolons. A semicolon after the last statement is optional. Unless the function is declared to return void, the last statement must be a SELECT, or an INSERT, UPDATE, or DELETE that has a RETURNING clause.

Any collection of commands in the SQL language can be packaged together and defined as a function. Besides SELECT queries, the commands can include data modification queries (INSERT, UPDATE, and DELETE), as well as other SQL commands. (You cannot use transaction control commands, e.g., COMMIT, SAVEPOINT, and some utility commands, e.g., VACUUM, in SQL functions.) However, the final command must be a SELECT or have a RETURNING clause that returns whatever is specified as the function's return type. Alternatively, if you want to define an SQL function that performs actions but has no useful value to return, you can define it as returning void. For example, this function removes rows with negative salaries from the emp table:

```
CREATE FUNCTION clean_emp() RETURNS void AS '
 DELETE FROM emp
 WHERE salary < 0;
' LANGUAGE SQL;
SELECT clean_emp();
 clean_emp
-----------
(1 row)
```

You can also write this as a procedure, thus avoiding the issue of the return type. For example:

```
CREATE PROCEDURE clean_emp() AS '
 DELETE FROM emp
 WHERE salary < 0;
' LANGUAGE SQL;
CALL clean_emp();
```

In simple cases like this, the difference between a function returning void and a procedure is mostly stylistic. However, procedures offer additional functionality such as transaction control that is not available in functions. Also, procedures are SQL standard whereas returning void is a PostgreSQL extension.

### **Note**

The entire body of an SQL function is parsed before any of it is executed. While an SQL function can contain commands that alter the system catalogs (e.g., CREATE TABLE), the effects of such commands will not be visible during parse analysis of later commands in the function. Thus, for example, CREATE TABLE foo (...); INSERT INTO foo VALUES(...); will not work as desired if packaged up into a single SQL function, since foo won't exist yet when the INSERT command is parsed. It's recommended to use PL/pgSQL instead of an SQL function in this type of situation.

The syntax of the CREATE FUNCTION command requires the function body to be written as a string constant. It is usually most convenient to use dollar quoting (see Section 4.1.2.4) for the string constant. If you choose to use regular single-quoted string constant syntax, you must double single quote marks (') and backslashes (\) (assuming escape string syntax) in the body of the function (see Section 4.1.2.1).

## <span id="page-155-0"></span>**38.5.1. Arguments for SQL Functions**

Arguments of an SQL function can be referenced in the function body using either names or numbers. Examples of both methods appear below.

To use a name, declare the function argument as having a name, and then just write that name in the function body. If the argument name is the same as any column name in the current SQL command within the function, the column name will take precedence. To override this, qualify the argument name with the name of the function itself, that is function\_name.argument\_name. (If this would conflict with a qualified column name, again the column name wins. You can avoid the ambiguity by choosing a different alias for the table within the SQL command.)

In the older numeric approach, arguments are referenced using the syntax \$n: \$1 refers to the first input argument, \$2 to the second, and so on. This will work whether or not the particular argument was declared with a name.

If an argument is of a composite type, then the dot notation, e.g., argname.fieldname or \$1.fieldname, can be used to access attributes of the argument. Again, you might need to qualify the argument's name with the function name to make the form with an argument name unambiguous.

SQL function arguments can only be used as data values, not as identifiers. Thus for example this is reasonable:

```
INSERT INTO mytable VALUES ($1);
but this will not work:
INSERT INTO $1 VALUES (42);
```

### **Note**

The ability to use names to reference SQL function arguments was added in PostgreSQL 9.2. Functions to be used in older servers must use the \$n notation.

## <span id="page-156-0"></span>**38.5.2. SQL Functions on Base Types**

The simplest possible SQL function has no arguments and simply returns a base type, such as integer:

```
CREATE FUNCTION one() RETURNS integer AS $$
 SELECT 1 AS result;
$$ LANGUAGE SQL;
-- Alternative syntax for string literal:
CREATE FUNCTION one() RETURNS integer AS '
 SELECT 1 AS result;
' LANGUAGE SQL;
SELECT one();
 one
-----
 1
```

Notice that we defined a column alias within the function body for the result of the function (with the name result), but this column alias is not visible outside the function. Hence, the result is labeled one instead of result.

It is almost as easy to define SQL functions that take base types as arguments:

```
CREATE FUNCTION add_em(x integer, y integer) RETURNS integer AS $$
 SELECT x + y;
$$ LANGUAGE SQL;
SELECT add_em(1, 2) AS answer;
 answer
--------
 3
```

Alternatively, we could dispense with names for the arguments and use numbers:

```
CREATE FUNCTION add_em(integer, integer) RETURNS integer AS $$
 SELECT $1 + $2;
$$ LANGUAGE SQL;
SELECT add_em(1, 2) AS answer;
 answer
--------
 3
```

Here is a more useful function, which might be used to debit a bank account:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS
 numeric AS $$
 UPDATE bank
 SET balance = balance - debit
 WHERE accountno = tf1.accountno;
 SELECT 1;
$$ LANGUAGE SQL;
```

A user could execute this function to debit account 17 by \$100.00 as follows:

```
SELECT tf1(17, 100.0);
```

In this example, we chose the name accountno for the first argument, but this is the same as the name of a column in the bank table. Within the UPDATE command, accountno refers to the column bank.accountno, so tf1.accountno must be used to refer to the argument. We could of course avoid this by using a different name for the argument.

In practice one would probably like a more useful result from the function than a constant 1, so a more likely definition is:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS
 numeric AS $$
 UPDATE bank
 SET balance = balance - debit
 WHERE accountno = tf1.accountno;
 SELECT balance FROM bank WHERE accountno = tf1.accountno;
$$ LANGUAGE SQL;
```

which adjusts the balance and returns the new balance. The same thing could be done in one command using RETURNING:

```
CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS
 numeric AS $$
 UPDATE bank
 SET balance = balance - debit
 WHERE accountno = tf1.accountno
 RETURNING balance;
$$ LANGUAGE SQL;
```

If the final SELECT or RETURNING clause in a SQL function does not return exactly the function's declared result type, PostgreSQL will automatically cast the value to the required type, if that is possible with an implicit or assignment cast. Otherwise, you must write an explicit cast. For example, suppose we wanted the previous add\_em function to return type float8 instead. It's sufficient to write

```
CREATE FUNCTION add_em(integer, integer) RETURNS float8 AS $$
 SELECT $1 + $2;
$$ LANGUAGE SQL;
```

since the integer sum can be implicitly cast to float8. (See Chapter 10 or CREATE CAST for more about casts.)

## <span id="page-158-0"></span>**38.5.3. SQL Functions on Composite Types**

When writing functions with arguments of composite types, we must not only specify which argument we want but also the desired attribute (field) of that argument. For example, suppose that emp is a table containing employee data, and therefore also the name of the composite type of each row of the table. Here is a function double\_salary that computes what someone's salary would be if it were doubled:

```
CREATE TABLE emp (
 name text,
 salary numeric,
 age integer,
 cubicle point
);
INSERT INTO emp VALUES ('Bill', 4200, 45, '(2,1)');
CREATE FUNCTION double_salary(emp) RETURNS numeric AS $$
 SELECT $1.salary * 2 AS salary;
$$ LANGUAGE SQL;
SELECT name, double_salary(emp.*) AS dream
 FROM emp
 WHERE emp.cubicle ~= point '(2,1)';
 name | dream
------+-------
 Bill | 8400
```

Notice the use of the syntax \$1.salary to select one field of the argument row value. Also notice how the calling SELECT command uses table\_name.\* to select the entire current row of a table as a composite value. The table row can alternatively be referenced using just the table name, like this:

```
SELECT name, double_salary(emp) AS dream
 FROM emp
```

```
 WHERE emp.cubicle ~= point '(2,1)';
```

but this usage is deprecated since it's easy to get confused. (See Section 8.16.5 for details about these two notations for the composite value of a table row.)

Sometimes it is handy to construct a composite argument value on-the-fly. This can be done with the ROW construct. For example, we could adjust the data being passed to the function:

```
SELECT name, double_salary(ROW(name, salary*1.1, age, cubicle)) AS
 dream
 FROM emp;
```

It is also possible to build a function that returns a composite type. This is an example of a function that returns a single emp row:

```
CREATE FUNCTION new_emp() RETURNS emp AS $$
 SELECT text 'None' AS name,
 1000.0 AS salary,
 25 AS age,
 point '(2,2)' AS cubicle;
$$ LANGUAGE SQL;
```

In this example we have specified each of the attributes with a constant value, but any computation could have been substituted for these constants.

Note two important things about defining the function:

- The select list order in the query must be exactly the same as that in which the columns appear in the composite type. (Naming the columns, as we did above, is irrelevant to the system.)
- We must ensure each expression's type can be cast to that of the corresponding column of the composite type. Otherwise we'll get errors like this:

```
ERROR: return type mismatch in function declared to return emp
DETAIL: Final statement returns text instead of point at column
 4.
```

As with the base-type case, the system will not insert explicit casts automatically, only implicit or assignment casts.

A different way to define the same function is:

```
CREATE FUNCTION new_emp() RETURNS emp AS $$
 SELECT ROW('None', 1000.0, 25, '(2,2)')::emp;
$$ LANGUAGE SQL;
```

Here we wrote a SELECT that returns just a single column of the correct composite type. This isn't really better in this situation, but it is a handy alternative in some cases — for example, if we need to compute the result by calling another function that returns the desired composite value. Another example is that if we are trying to write a function that returns a domain over composite, rather than a plain composite type, it is always necessary to write it as returning a single column, since there is no way to cause a coercion of the whole row result.

We could call this function directly either by using it in a value expression:

```
SELECT new_emp();
 new_emp
--------------------------
 (None,1000.0,25,"(2,2)")
or by calling it as a table function:
SELECT * FROM new_emp();
 name | salary | age | cubicle
------+--------+-----+---------
 None | 1000.0 | 25 | (2,2)
```

The second way is described more fully in [Section 38.5.8.](#page-164-0)

When you use a function that returns a composite type, you might want only one field (attribute) from its result. You can do that with syntax like this:

```
SELECT (new_emp()).name;
 name
------
 None
```

The extra parentheses are needed to keep the parser from getting confused. If you try to do it without them, you get something like this:

```
SELECT new_emp().name;
ERROR: syntax error at or near "."
LINE 1: SELECT new_emp().name;
 ^
```

Another option is to use functional notation for extracting an attribute:

```
SELECT name(new_emp());
 name
------
 None
```

As explained in Section 8.16.5, the field notation and functional notation are equivalent.

Another way to use a function returning a composite type is to pass the result to another function that accepts the correct row type as input:

```
CREATE FUNCTION getname(emp) RETURNS text AS $$
 SELECT $1.name;
$$ LANGUAGE SQL;
SELECT getname(new_emp());
 getname
---------
```

```
 None
(1 row)
```

## <span id="page-161-0"></span>**38.5.4. SQL Functions with Output Parameters**

An alternative way of describing a function's results is to define it with *output parameters*, as in this example:

```
CREATE FUNCTION add_em (IN x int, IN y int, OUT sum int)
AS 'SELECT x + y'
LANGUAGE SQL;
SELECT add_em(3,7);
 add_em
--------
 10
(1 row)
```

This is not essentially different from the version of add\_em shown in [Section 38.5.2](#page-156-0). The real value of output parameters is that they provide a convenient way of defining functions that return several columns. For example,

```
CREATE FUNCTION sum_n_product (x int, y int, OUT sum int, OUT
 product int)
AS 'SELECT x + y, x * y'
LANGUAGE SQL;
 SELECT * FROM sum_n_product(11,42);
 sum | product
-----+---------
 53 | 462
(1 row)
```

What has essentially happened here is that we have created an anonymous composite type for the result of the function. The above example has the same end result as

```
CREATE TYPE sum_prod AS (sum int, product int);
CREATE FUNCTION sum_n_product (int, int) RETURNS sum_prod
AS 'SELECT $1 + $2, $1 * $2'
LANGUAGE SQL;
```

but not having to bother with the separate composite type definition is often handy. Notice that the names attached to the output parameters are not just decoration, but determine the column names of the anonymous composite type. (If you omit a name for an output parameter, the system will choose a name on its own.)

Notice that output parameters are not included in the calling argument list when invoking such a function from SQL. This is because PostgreSQL considers only the input parameters to define the function's calling signature. That means also that only the input parameters matter when referencing the function for purposes such as dropping it. We could drop the above function with either of

```
DROP FUNCTION sum_n_product (x int, y int, OUT sum int, OUT product
 int);
```

```
DROP FUNCTION sum_n_product (int, int);
```

Parameters can be marked as IN (the default), OUT, INOUT, or VARIADIC. An INOUT parameter serves as both an input parameter (part of the calling argument list) and an output parameter (part of the result record type). VARIADIC parameters are input parameters, but are treated specially as described below.

## <span id="page-162-0"></span>**38.5.5. SQL Procedures with Output Parameters**

Output parameters are also supported in procedures, but they work a bit differently from functions. In CALL commands, output parameters must be included in the argument list. For example, the bank account debiting routine from earlier could be written like this:

```
CREATE PROCEDURE tp1 (accountno integer, debit numeric, OUT
 new_balance numeric) AS $$
 UPDATE bank
 SET balance = balance - debit
 WHERE accountno = tp1.accountno
 RETURNING balance;
$$ LANGUAGE SQL;
```

To call this procedure, an argument matching the OUT parameter must be included. It's customary to write NULL:

```
CALL tp1(17, 100.0, NULL);
```

If you write something else, it must be an expression that is implicitly coercible to the declared type of the parameter, just as for input parameters. Note however that such an expression will not be evaluated.

When calling a procedure from PL/pgSQL, instead of writing NULL you must write a variable that will receive the procedure's output. See Section 43.6.3 for details.

## <span id="page-162-1"></span>**38.5.6. SQL Functions with Variable Numbers of Arguments**

SQL functions can be declared to accept variable numbers of arguments, so long as all the "optional" arguments are of the same data type. The optional arguments will be passed to the function as an array. The function is declared by marking the last parameter as VARIADIC; this parameter must be declared as being of an array type. For example:

```
CREATE FUNCTION mleast(VARIADIC arr numeric[]) RETURNS numeric AS $
$
 SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;
SELECT mleast(10, -1, 5, 4.4);
 mleast 
--------
 -1
(1 row)
```

Effectively, all the actual arguments at or beyond the VARIADIC position are gathered up into a onedimensional array, as if you had written

```
SELECT mleast(ARRAY[10, -1, 5, 4.4]); -- doesn't work
```

You can't actually write that, though — or at least, it will not match this function definition. A parameter marked VARIADIC matches one or more occurrences of its element type, not of its own type.

Sometimes it is useful to be able to pass an already-constructed array to a variadic function; this is particularly handy when one variadic function wants to pass on its array parameter to another one. Also, this is the only secure way to call a variadic function found in a schema that permits untrusted users to create objects; see Section 10.3. You can do this by specifying VARIADIC in the call:

```
SELECT mleast(VARIADIC ARRAY[10, -1, 5, 4.4]);
```

This prevents expansion of the function's variadic parameter into its element type, thereby allowing the array argument value to match normally. VARIADIC can only be attached to the last actual argument of a function call.

Specifying VARIADIC in the call is also the only way to pass an empty array to a variadic function, for example:

```
SELECT mleast(VARIADIC ARRAY[]::numeric[]);
```

Simply writing SELECT mleast() does not work because a variadic parameter must match at least one actual argument. (You could define a second function also named mleast, with no parameters, if you wanted to allow such calls.)

The array element parameters generated from a variadic parameter are treated as not having any names of their own. This means it is not possible to call a variadic function using named arguments (Section 4.3), except when you specify VARIADIC. For example, this will work:

```
SELECT mleast(VARIADIC arr => ARRAY[10, -1, 5, 4.4]);
but not these:
SELECT mleast(arr => 10);
SELECT mleast(arr => ARRAY[10, -1, 5, 4.4]);
```

## <span id="page-163-0"></span>**38.5.7. SQL Functions with Default Values for Arguments**

Functions can be declared with default values for some or all input arguments. The default values are inserted whenever the function is called with insufficiently many actual arguments. Since arguments can only be omitted from the end of the actual argument list, all parameters after a parameter with a default value have to have default values as well. (Although the use of named argument notation could allow this restriction to be relaxed, it's still enforced so that positional argument notation works sensibly.) Whether or not you use it, this capability creates a need for precautions when calling functions in databases where some users mistrust other users; see Section 10.3.

#### For example:

```
CREATE FUNCTION foo(a int, b int DEFAULT 2, c int DEFAULT 3)
RETURNS int
LANGUAGE SQL
AS $$
```

```
 SELECT $1 + $2 + $3;
$$;
SELECT foo(10, 20, 30);
 foo 
-----
 60
(1 row)
SELECT foo(10, 20);
 foo 
-----
 33
(1 row)
SELECT foo(10);
 foo 
-----
 15
(1 row)
SELECT foo(); -- fails since there is no default for the first
 argument
ERROR: function foo() does not exist
```

The = sign can also be used in place of the key word DEFAULT.

## <span id="page-164-0"></span>**38.5.8. SQL Functions as Table Sources**

All SQL functions can be used in the FROM clause of a query, but it is particularly useful for functions returning composite types. If the function is defined to return a base type, the table function produces a one-column table. If the function is defined to return a composite type, the table function produces a column for each attribute of the composite type.

Here is an example:

```
CREATE TABLE foo (fooid int, foosubid int, fooname text);
INSERT INTO foo VALUES (1, 1, 'Joe');
INSERT INTO foo VALUES (1, 2, 'Ed');
INSERT INTO foo VALUES (2, 1, 'Mary');
CREATE FUNCTION getfoo(int) RETURNS foo AS $$
 SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;
SELECT *, upper(fooname) FROM getfoo(1) AS t1;
 fooid | foosubid | fooname | upper
-------+----------+---------+-------
 1 | 1 | Joe | JOE
(1 row)
```

As the example shows, we can work with the columns of the function's result just the same as if they were columns of a regular table.

Note that we only got one row out of the function. This is because we did not use SETOF. That is described in the next section.

## <span id="page-165-0"></span>**38.5.9. SQL Functions Returning Sets**

When an SQL function is declared as returning SETOF sometype, the function's final query is executed to completion, and each row it outputs is returned as an element of the result set.

This feature is normally used when calling the function in the FROM clause. In this case each row returned by the function becomes a row of the table seen by the query. For example, assume that table foo has the same contents as above, and we say:

```
CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
 SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;
SELECT * FROM getfoo(1) AS t1;
Then we would get:
 fooid | foosubid | fooname
-------+----------+---------
 1 | 1 | Joe
 1 | 2 | Ed
(2 rows)
```

It is also possible to return multiple rows with the columns defined by output parameters, like this:

```
CREATE TABLE tab (y int, z int);
INSERT INTO tab VALUES (1, 2), (3, 4), (5, 6), (7, 8);
CREATE FUNCTION sum_n_product_with_tab (x int, OUT sum int, OUT
 product int)
RETURNS SETOF record
AS $$
 SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;
SELECT * FROM sum_n_product_with_tab(10);
 sum | product
-----+---------
 11 | 10
 13 | 30
 15 | 50
 17 | 70
(4 rows)
```

The key point here is that you must write RETURNS SETOF record to indicate that the function returns multiple rows instead of just one. If there is only one output parameter, write that parameter's type instead of record.

It is frequently useful to construct a query's result by invoking a set-returning function multiple times, with the parameters for each invocation coming from successive rows of a table or subquery. The preferred way to do this is to use the LATERAL key word, which is described in Section 7.2.1.5. Here is an example using a set-returning function to enumerate elements of a tree structure:

```
SELECT * FROM nodes;
 name | parent
```

```
-----------+--------
 Top |
 Child1 | Top
 Child2 | Top
 Child3 | Top
 SubChild1 | Child1
 SubChild2 | Child1
(6 rows)
CREATE FUNCTION listchildren(text) RETURNS SETOF text AS $$
 SELECT name FROM nodes WHERE parent = $1
$$ LANGUAGE SQL STABLE;
SELECT * FROM listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)
SELECT name, child FROM nodes, LATERAL listchildren(name) AS child;
 name | child
--------+-----------
 Top | Child1
 Top | Child2
 Top | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

This example does not do anything that we couldn't have done with a simple join, but in more complex calculations the option to put some of the work into a function can be quite convenient.

Functions returning sets can also be called in the select list of a query. For each row that the query generates by itself, the set-returning function is invoked, and an output row is generated for each element of the function's result set. The previous example could also be done with queries like these:

```
SELECT listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)
SELECT name, listchildren(name) FROM nodes;
 name | listchildren
--------+--------------
 Top | Child1
 Top | Child2
 Top | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

In the last SELECT, notice that no output row appears for Child2, Child3, etc. This happens because listchildren returns an empty set for those arguments, so no result rows are generated. This is the same behavior as we got from an inner join to the function result when using the LATERAL syntax.

PostgreSQL's behavior for a set-returning function in a query's select list is almost exactly the same as if the set-returning function had been written in a LATERAL FROM-clause item instead. For example,

```
SELECT x, generate_series(1,5) AS g FROM tab;
```

is almost equivalent to

```
SELECT x, g FROM tab, LATERAL generate_series(1,5) AS g;
```

It would be exactly the same, except that in this specific example, the planner could choose to put g on the outside of the nested-loop join, since g has no actual lateral dependency on tab. That would result in a different output row order. Set-returning functions in the select list are always evaluated as though they are on the inside of a nested-loop join with the rest of the FROM clause, so that the function(s) are run to completion before the next row from the FROM clause is considered.

If there is more than one set-returning function in the query's select list, the behavior is similar to what you get from putting the functions into a single LATERAL ROWS FROM( ... ) FROM-clause item. For each row from the underlying query, there is an output row using the first result from each function, then an output row using the second result, and so on. If some of the set-returning functions produce fewer outputs than others, null values are substituted for the missing data, so that the total number of rows emitted for one underlying row is the same as for the set-returning function that produced the most outputs. Thus the set-returning functions run "in lockstep" until they are all exhausted, and then execution continues with the next underlying row.

Set-returning functions can be nested in a select list, although that is not allowed in FROM-clause items. In such cases, each level of nesting is treated separately, as though it were a separate LATERAL ROWS FROM( ... ) item. For example, in

```
SELECT srf1(srf2(x), srf3(y)), srf4(srf5(z)) FROM tab;
```

the set-returning functions srf2, srf3, and srf5 would be run in lockstep for each row of tab, and then srf1 and srf4 would be applied in lockstep to each row produced by the lower functions.

Set-returning functions cannot be used within conditional-evaluation constructs, such as CASE or COALESCE. For example, consider

```
SELECT x, CASE WHEN x > 0 THEN generate_series(1, 5) ELSE 0 END
 FROM tab;
```

It might seem that this should produce five repetitions of input rows that have x > 0, and a single repetition of those that do not; but actually, because generate\_series(1, 5) would be run in an implicit LATERAL FROM item before the CASE expression is ever evaluated, it would produce five repetitions of every input row. To reduce confusion, such cases produce a parse-time error instead.

### **Note**

If a function's last command is INSERT, UPDATE, or DELETE with RETURNING, that command will always be executed to completion, even if the function is not declared with SETOF or the calling query does not fetch all the result rows. Any extra rows produced by the RE-TURNING clause are silently dropped, but the commanded table modifications still happen (and are all completed before returning from the function).

### **Note**

Before PostgreSQL 10, putting more than one set-returning function in the same select list did not behave very sensibly unless they always produced equal numbers of rows. Otherwise, what you got was a number of output rows equal to the least common multiple of the numbers of rows produced by the set-returning functions. Also, nested set-returning functions did not work as described above; instead, a set-returning function could have at most one set-returning argument, and each nest of set-returning functions was run independently. Also, conditional execution (set-returning functions inside CASE etc) was previously allowed, complicating things even more. Use of the LATERAL syntax is recommended when writing queries that need to work in older PostgreSQL versions, because that will give consistent results across different versions. If you have a query that is relying on conditional execution of a set-returning function, you may be able to fix it by moving the conditional test into a custom set-returning function. For example,

```
SELECT x, CASE WHEN y > 0 THEN generate_series(1, z) ELSE 5
 END FROM tab;
could become
CREATE FUNCTION case_generate_series(cond bool, start int, fin
 int, els int)
 RETURNS SETOF int AS $$
BEGIN
 IF cond THEN
 RETURN QUERY SELECT generate_series(start, fin);
 ELSE
 RETURN QUERY SELECT els;
 END IF;
END$$ LANGUAGE plpgsql;
SELECT x, case_generate_series(y > 0, 1, z, 5) FROM tab;
```

## <span id="page-168-0"></span>**38.5.10. SQL Functions Returning TABLE**

There is another way to declare a function as returning a set, which is to use the syntax RETURNS TABLE(columns). This is equivalent to using one or more OUT parameters plus marking the function as returning SETOF record (or SETOF a single output parameter's type, as appropriate). This notation is specified in recent versions of the SQL standard, and thus may be more portable than using SETOF.

For example, the preceding sum-and-product example could also be done this way:

This formulation will work the same in all versions of PostgreSQL.

```
CREATE FUNCTION sum_n_product_with_tab (x int)
RETURNS TABLE(sum int, product int) AS $$
 SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;
```

It is not allowed to use explicit OUT or INOUT parameters with the RETURNS TABLE notation you must put all the output columns in the TABLE list.

## <span id="page-169-0"></span>**38.5.11. Polymorphic SQL Functions**

SQL functions can be declared to accept and return the polymorphic types described in [Section 38.2.5.](#page-151-2) Here is a polymorphic function make\_array that builds up an array from two arbitrary data type elements:

```
CREATE FUNCTION make_array(anyelement, anyelement) RETURNS anyarray
 AS $$
 SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;
SELECT make_array(1, 2) AS intarray, make_array('a'::text, 'b') AS
 textarray;
 intarray | textarray
----------+-----------
 {1,2} | {a,b}
(1 row)
```

Notice the use of the typecast 'a'::text to specify that the argument is of type text. This is required if the argument is just a string literal, since otherwise it would be treated as type unknown, and array of unknown is not a valid type. Without the typecast, you will get errors like this:

```
ERROR: could not determine polymorphic type because input has type
 unknown
```

With make\_array declared as above, you must provide two arguments that are of exactly the same data type; the system will not attempt to resolve any type differences. Thus for example this does not work:

```
SELECT make_array(1, 2.5) AS numericarray;
ERROR: function make_array(integer, numeric) does not exist
```

An alternative approach is to use the "common" family of polymorphic types, which allows the system to try to identify a suitable common type:

```
CREATE FUNCTION make_array2(anycompatible, anycompatible)
RETURNS anycompatiblearray AS $$
 SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;
SELECT make_array2(1, 2.5) AS numericarray;
 numericarray
--------------
 {1,2.5}
(1 row)
```

Because the rules for common type resolution default to choosing type text when all inputs are of unknown types, this also works:

```
SELECT make_array2('a', 'b') AS textarray;
 textarray 
-----------
 {a,b}
(1 row)
```

It is permitted to have polymorphic arguments with a fixed return type, but the converse is not. For example:

```
CREATE FUNCTION is_greater(anyelement, anyelement) RETURNS boolean
 AS $$
 SELECT $1 > $2;
$$ LANGUAGE SQL;
SELECT is_greater(1, 2);
 is_greater
------------
 f
(1 row)
CREATE FUNCTION invalid_func() RETURNS anyelement AS $$
 SELECT 1;
$$ LANGUAGE SQL;
ERROR: cannot determine result data type
DETAIL: A result of type anyelement requires at least one input of
 type anyelement, anyarray, anynonarray, anyenum, or anyrange.
Polymorphism can be used with functions that have output arguments. For example:
```

```
CREATE FUNCTION dup (f1 anyelement, OUT f2 anyelement, OUT f3
 anyarray)
AS 'select $1, array[$1,$1]' LANGUAGE SQL;
SELECT * FROM dup(22);
 f2 | f3
----+---------
 22 | {22,22}
(1 row)
```

Polymorphism can also be used with variadic functions. For example:

```
CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS
 $$
 SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;
SELECT anyleast(10, -1, 5, 4);
 anyleast 
----------
 -1
(1 row)
SELECT anyleast('abc'::text, 'def');
 anyleast 
----------
 abc
(1 row)
CREATE FUNCTION concat_values(text, VARIADIC anyarray) RETURNS text
 AS $$
 SELECT array_to_string($2, $1);
$$ LANGUAGE SQL;
```

```
SELECT concat_values('|', 1, 4, 2);
 concat_values 
---------------
 1|4|2
(1 row)
```

## <span id="page-171-0"></span>**38.5.12. SQL Functions with Collations**

When an SQL function has one or more parameters of collatable data types, a collation is identified for each function call depending on the collations assigned to the actual arguments, as described in Section 24.2. If a collation is successfully identified (i.e., there are no conflicts of implicit collations among the arguments) then all the collatable parameters are treated as having that collation implicitly. This will affect the behavior of collation-sensitive operations within the function. For example, using the anyleast function described above, the result of

```
SELECT anyleast('abc'::text, 'ABC');
```

will depend on the database's default collation. In C locale the result will be ABC, but in many other locales it will be abc. The collation to use can be forced by adding a COLLATE clause to any of the arguments, for example

```
SELECT anyleast('abc'::text, 'ABC' COLLATE "C");
```

Alternatively, if you wish a function to operate with a particular collation regardless of what it is called with, insert COLLATE clauses as needed in the function definition. This version of anyleast would always use en\_US locale to compare strings:

```
CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS
 $$
 SELECT min($1[i] COLLATE "en_US") FROM generate_subscripts($1,
 1) g(i);
$$ LANGUAGE SQL;
```

But note that this will throw an error if applied to a non-collatable data type.

If no common collation can be identified among the actual arguments, then an SQL function treats its parameters as having their data types' default collation (which is usually the database's default collation, but could be different for parameters of domain types).

The behavior of collatable parameters can be thought of as a limited form of polymorphism, applicable only to textual data types.

# <span id="page-171-1"></span>**38.6. Function Overloading**

More than one function can be defined with the same SQL name, so long as the arguments they take are different. In other words, function names can be *overloaded*. Whether or not you use it, this capability entails security precautions when calling functions in databases where some users mistrust other users; see Section 10.3. When a query is executed, the server will determine which function to call from the data types and the number of the provided arguments. Overloading can also be used to simulate functions with a variable number of arguments, up to a finite maximum number.

When creating a family of overloaded functions, one should be careful not to create ambiguities. For instance, given the functions:

```
CREATE FUNCTION test(int, real) RETURNS ...
CREATE FUNCTION test(smallint, double precision) RETURNS ...
```

it is not immediately clear which function would be called with some trivial input like test(1, 1.5). The currently implemented resolution rules are described in Chapter 10, but it is unwise to design a system that subtly relies on this behavior.

A function that takes a single argument of a composite type should generally not have the same name as any attribute (field) of that type. Recall that attribute(table) is considered equivalent to table.attribute. In the case that there is an ambiguity between a function on a composite type and an attribute of the composite type, the attribute will always be used. It is possible to override that choice by schema-qualifying the function name (that is, schema.func(table) ) but it's better to avoid the problem by not choosing conflicting names.

Another possible conflict is between variadic and non-variadic functions. For instance, it is possible to create both foo(numeric) and foo(VARIADIC numeric[]). In this case it is unclear which one should be matched to a call providing a single numeric argument, such as foo(10.1). The rule is that the function appearing earlier in the search path is used, or if the two functions are in the same schema, the non-variadic one is preferred.

When overloading C-language functions, there is an additional constraint: The C name of each function in the family of overloaded functions must be different from the C names of all other functions, either internal or dynamically loaded. If this rule is violated, the behavior is not portable. You might get a run-time linker error, or one of the functions will get called (usually the internal one). The alternative form of the AS clause for the SQL CREATE FUNCTION command decouples the SQL function name from the function name in the C source code. For instance:

```
CREATE FUNCTION test(int) RETURNS int
 AS 'filename', 'test_1arg'
 LANGUAGE C;
CREATE FUNCTION test(int, int) RETURNS int
 AS 'filename', 'test_2arg'
 LANGUAGE C;
```

The names of the C functions here reflect one of many possible conventions.

# <span id="page-172-0"></span>**38.7. Function Volatility Categories**

Every function has a *volatility* classification, with the possibilities being VOLATILE, STABLE, or IMMUTABLE. VOLATILE is the default if the CREATE FUNCTION command does not specify a category. The volatility category is a promise to the optimizer about the behavior of the function:

- A VOLATILE function can do anything, including modifying the database. It can return different results on successive calls with the same arguments. The optimizer makes no assumptions about the behavior of such functions. A query using a volatile function will re-evaluate the function at every row where its value is needed.
- A STABLE function cannot modify the database and is guaranteed to return the same results given the same arguments for all rows within a single statement. This category allows the optimizer to optimize multiple calls of the function to a single call. In particular, it is safe to use an expression containing such a function in an index scan condition. (Since an index scan will evaluate the comparison value only once, not once at each row, it is not valid to use a VOLATILE function in an index scan condition.)
- An IMMUTABLE function cannot modify the database and is guaranteed to return the same results given the same arguments forever. This category allows the optimizer to pre-evaluate the function when a query calls it with constant arguments. For example, a query like SELECT ... WHERE

x = 2 + 2 can be simplified on sight to SELECT ... WHERE x = 4, because the function underlying the integer addition operator is marked IMMUTABLE.

For best optimization results, you should label your functions with the strictest volatility category that is valid for them.

Any function with side-effects *must* be labeled VOLATILE, so that calls to it cannot be optimized away. Even a function with no side-effects needs to be labeled VOLATILE if its value can change within a single query; some examples are random(), currval(), timeofday().

Another important example is that the current\_timestamp family of functions qualify as STABLE, since their values do not change within a transaction.

There is relatively little difference between STABLE and IMMUTABLE categories when considering simple interactive queries that are planned and immediately executed: it doesn't matter a lot whether a function is executed once during planning or once during query execution startup. But there is a big difference if the plan is saved and reused later. Labeling a function IMMUTABLE when it really isn't might allow it to be prematurely folded to a constant during planning, resulting in a stale value being re-used during subsequent uses of the plan. This is a hazard when using prepared statements or when using function languages that cache plans (such as PL/pgSQL).

For functions written in SQL or in any of the standard procedural languages, there is a second important property determined by the volatility category, namely the visibility of any data changes that have been made by the SQL command that is calling the function. A VOLATILE function will see such changes, a STABLE or IMMUTABLE function will not. This behavior is implemented using the snapshotting behavior of MVCC (see Chapter 13): STABLE and IMMUTABLE functions use a snapshot established as of the start of the calling query, whereas VOLATILE functions obtain a fresh snapshot at the start of each query they execute.

### **Note**

Functions written in C can manage snapshots however they want, but it's usually a good idea to make C functions work this way too.

Because of this snapshotting behavior, a function containing only SELECT commands can safely be marked STABLE, even if it selects from tables that might be undergoing modifications by concurrent queries. PostgreSQL will execute all commands of a STABLE function using the snapshot established for the calling query, and so it will see a fixed view of the database throughout that query.

The same snapshotting behavior is used for SELECT commands within IMMUTABLE functions. It is generally unwise to select from database tables within an IMMUTABLE function at all, since the immutability will be broken if the table contents ever change. However, PostgreSQL does not enforce that you do not do that.

A common error is to label a function IMMUTABLE when its results depend on a configuration parameter. For example, a function that manipulates timestamps might well have results that depend on the TimeZone setting. For safety, such functions should be labeled STABLE instead.

### **Note**

PostgreSQL requires that STABLE and IMMUTABLE functions contain no SQL commands other than SELECT to prevent data modification. (This is not a completely bulletproof test, since such functions could still call VOLATILE functions that modify the database. If you do that, you will find that the STABLE or IMMUTABLE function does not notice the database changes applied by the called function, since they are hidden from its snapshot.)

# <span id="page-174-0"></span>**38.8. Procedural Language Functions**

PostgreSQL allows user-defined functions to be written in other languages besides SQL and C. These other languages are generically called *procedural languages* (PLs). Procedural languages aren't built into the PostgreSQL server; they are offered by loadable modules. See Chapter 42 and following chapters for more information.

# <span id="page-174-1"></span>**38.9. Internal Functions**

Internal functions are functions written in C that have been statically linked into the PostgreSQL server. The "body" of the function definition specifies the C-language name of the function, which need not be the same as the name being declared for SQL use. (For reasons of backward compatibility, an empty body is accepted as meaning that the C-language function name is the same as the SQL name.)

Normally, all internal functions present in the server are declared during the initialization of the database cluster (see Section 19.2), but a user could use CREATE FUNCTION to create additional alias names for an internal function. Internal functions are declared in CREATE FUNCTION with language name internal. For instance, to create an alias for the sqrt function:

```
CREATE FUNCTION square_root(double precision) RETURNS double
 precision
 AS 'dsqrt'
 LANGUAGE internal
 STRICT;
```

(Most internal functions expect to be declared "strict".)

### **Note**

Not all "predefined" functions are "internal" in the above sense. Some predefined functions are written in SQL.

# <span id="page-174-2"></span>**38.10. C-Language Functions**

User-defined functions can be written in C (or a language that can be made compatible with C, such as C++). Such functions are compiled into dynamically loadable objects (also called shared libraries) and are loaded by the server on demand. The dynamic loading feature is what distinguishes "C language" functions from "internal" functions — the actual coding conventions are essentially the same for both. (Hence, the standard internal function library is a rich source of coding examples for user-defined C functions.)

Currently only one calling convention is used for C functions ("version 1"). Support for that calling convention is indicated by writing a PG\_FUNCTION\_INFO\_V1() macro call for the function, as illustrated below.

## <span id="page-174-3"></span>**38.10.1. Dynamic Loading**

The first time a user-defined function in a particular loadable object file is called in a session, the dynamic loader loads that object file into memory so that the function can be called. The CREATE FUNCTION for a user-defined C function must therefore specify two pieces of information for the function: the name of the loadable object file, and the C name (link symbol) of the specific function to call within that object file. If the C name is not explicitly specified then it is assumed to be the same as the SQL function name.

The following algorithm is used to locate the shared object file based on the name given in the CREATE FUNCTION command:

- 1. If the name is an absolute path, the given file is loaded.
- 2. If the name starts with the string \$libdir, that part is replaced by the PostgreSQL package library directory name, which is determined at build time.
- 3. If the name does not contain a directory part, the file is searched for in the path specified by the configuration variable dynamic\_library\_path.
- 4. Otherwise (the file was not found in the path, or it contains a non-absolute directory part), the dynamic loader will try to take the name as given, which will most likely fail. (It is unreliable to depend on the current working directory.)

If this sequence does not work, the platform-specific shared library file name extension (often .so) is appended to the given name and this sequence is tried again. If that fails as well, the load will fail.

It is recommended to locate shared libraries either relative to \$libdir or through the dynamic library path. This simplifies version upgrades if the new installation is at a different location. The actual directory that \$libdir stands for can be found out with the command pg\_config --pkglibdir.

The user ID the PostgreSQL server runs as must be able to traverse the path to the file you intend to load. Making the file or a higher-level directory not readable and/or not executable by the postgres user is a common mistake.

In any case, the file name that is given in the CREATE FUNCTION command is recorded literally in the system catalogs, so if the file needs to be loaded again the same procedure is applied.

### **Note**

PostgreSQL will not compile a C function automatically. The object file must be compiled before it is referenced in a CREATE FUNCTION command. See [Section 38.10.5](#page-182-0) for additional information.

To ensure that a dynamically loaded object file is not loaded into an incompatible server, PostgreSQL checks that the file contains a "magic block" with the appropriate contents. This allows the server to detect obvious incompatibilities, such as code compiled for a different major version of PostgreSQL. To include a magic block, write this in one (and only one) of the module source files, after having included the header fmgr.h:

PG\_MODULE\_MAGIC;

After it is used for the first time, a dynamically loaded object file is retained in memory. Future calls in the same session to the function(s) in that file will only incur the small overhead of a symbol table lookup. If you need to force a reload of an object file, for example after recompiling it, begin a fresh session.

Optionally, a dynamically loaded file can contain initialization and finalization functions. If the file includes a function named \_PG\_init, that function will be called immediately after loading the file. The function receives no parameters and should return void. If the file includes a function named \_PG\_fini, that function will be called immediately before unloading the file. Likewise, the function receives no parameters and should return void. Note that \_PG\_fini will only be called during an unload of the file, not during process termination. (Presently, unloads are disabled and will never occur, but this may change in the future.)

## <span id="page-176-0"></span>**38.10.2. Base Types in C-Language Functions**

To know how to write C-language functions, you need to know how PostgreSQL internally represents base data types and how they can be passed to and from functions. Internally, PostgreSQL regards a base type as a "blob of memory". The user-defined functions that you define over a type in turn define the way that PostgreSQL can operate on it. That is, PostgreSQL will only store and retrieve the data from disk and use your user-defined functions to input, process, and output the data.

Base types can have one of three internal formats:

- pass by value, fixed-length
- pass by reference, fixed-length
- pass by reference, variable-length

By-value types can only be 1, 2, or 4 bytes in length (also 8 bytes, if sizeof(Datum) is 8 on your machine). You should be careful to define your types such that they will be the same size (in bytes) on all architectures. For example, the long type is dangerous because it is 4 bytes on some machines and 8 bytes on others, whereas int type is 4 bytes on most Unix machines. A reasonable implementation of the int4 type on Unix machines might be:

```
/* 4-byte integer, passed by value */
typedef int int4;
```

(The actual PostgreSQL C code calls this type int32, because it is a convention in C that intXX means XX *bits*. Note therefore also that the C type int8 is 1 byte in size. The SQL type int8 is called int64 in C. See also [Table 38.2](#page-177-0).)

On the other hand, fixed-length types of any size can be passed by-reference. For example, here is a sample implementation of a PostgreSQL type:

```
/* 16-byte structure, passed by reference */
typedef struct
{
 double x, y;
} Point;
```

Only pointers to such types can be used when passing them in and out of PostgreSQL functions. To return a value of such a type, allocate the right amount of memory with palloc, fill in the allocated memory, and return a pointer to it. (Also, if you just want to return the same value as one of your input arguments that's of the same data type, you can skip the extra palloc and just return the pointer to the input value.)

Finally, all variable-length types must also be passed by reference. All variable-length types must begin with an opaque length field of exactly 4 bytes, which will be set by SET\_VARSIZE; never set this field directly! All data to be stored within that type must be located in the memory immediately following that length field. The length field contains the total length of the structure, that is, it includes the size of the length field itself.

Another important point is to avoid leaving any uninitialized bits within data type values; for example, take care to zero out any alignment padding bytes that might be present in structs. Without this, logically-equivalent constants of your data type might be seen as unequal by the planner, leading to inefficient (though not incorrect) plans.

### **Warning**

*Never* modify the contents of a pass-by-reference input value. If you do so you are likely to corrupt on-disk data, since the pointer you are given might point directly into a disk buffer. The sole exception to this rule is explained in [Section 38.12](#page-196-0).

As an example, we can define the type text as follows:

```
typedef struct {
 int32 length;
 char data[FLEXIBLE_ARRAY_MEMBER];
} text;
```

The [FLEXIBLE\_ARRAY\_MEMBER] notation means that the actual length of the data part is not specified by this declaration.

When manipulating variable-length types, we must be careful to allocate the correct amount of memory and set the length field correctly. For example, if we wanted to store 40 bytes in a text structure, we might use a code fragment like this:

```
#include "postgres.h"
...
char buffer[40]; /* our source data */
...
text *destination = (text *) palloc(VARHDRSZ + 40);
SET_VARSIZE(destination, VARHDRSZ + 40);
memcpy(destination->data, buffer, 40);
...
```

VARHDRSZ is the same as sizeof(int32), but it's considered good style to use the macro VARHDRSZ to refer to the size of the overhead for a variable-length type. Also, the length field *must* be set using the SET\_VARSIZE macro, not by simple assignment.

[Table 38.2](#page-177-0) shows the C types corresponding to many of the built-in SQL data types of PostgreSQL. The "Defined In" column gives the header file that needs to be included to get the type definition. (The actual definition might be in a different file that is included by the listed file. It is recommended that users stick to the defined interface.) Note that you should always include postgres.h first in any source file of server code, because it declares a number of things that you will need anyway, and because including other headers first can cause portability issues.

<span id="page-177-0"></span>**Table 38.2. Equivalent C Types for Built-in SQL Types**

| SQL Type      | C Type    | Defined In                           |
|---------------|-----------|--------------------------------------|
| boolean       | bool      | postgres.h (maybe compiler built-in) |
| box           | BOX*      | utils/geo_decls.h                    |
| bytea         | bytea*    | postgres.h                           |
| "char"        | char      | (compiler built-in)                  |
| character     | BpChar*   | postgres.h                           |
| cid           | CommandId | postgres.h                           |
| date          | DateADT   | utils/date.h                         |
| float4 (real) | float4    | postgres.h                           |

| SQL Type                     | C Type        | Defined In           |
|------------------------------|---------------|----------------------|
| float8 (double<br>precision) | float8        | postgres.h           |
| int2 (smallint)              | int16         | postgres.h           |
| int4 (integer)               | int32         | postgres.h           |
| int8 (bigint)                | int64         | postgres.h           |
| interval                     | Interval*     | datatype/timestamp.h |
| lseg                         | LSEG*         | utils/geo_decls.h    |
| name                         | Name          | postgres.h           |
| numeric                      | Numeric       | utils/numeric.h      |
| oid                          | Oid           | postgres.h           |
| oidvector                    | oidvector*    | postgres.h           |
| path                         | PATH*         | utils/geo_decls.h    |
| point                        | POINT*        | utils/geo_decls.h    |
| regproc                      | RegProcedure  | postgres.h           |
| text                         | text*         | postgres.h           |
| tid                          | ItemPointer   | storage/itemptr.h    |
| time                         | TimeADT       | utils/date.h         |
| time with time<br>zone       | TimeTzADT     | utils/date.h         |
| timestamp                    | Timestamp     | datatype/timestamp.h |
| timestamp with<br>time zone  | TimestampTz   | datatype/timestamp.h |
| varchar                      | VarChar*      | postgres.h           |
| xid                          | TransactionId | postgres.h           |

Now that we've gone over all of the possible structures for base types, we can show some examples of real functions.

## <span id="page-178-0"></span>**38.10.3. Version 1 Calling Conventions**

The version-1 calling convention relies on macros to suppress most of the complexity of passing arguments and results. The C declaration of a version-1 function is always:

Datum funcname(PG\_FUNCTION\_ARGS)

In addition, the macro call:

PG\_FUNCTION\_INFO\_V1(funcname);

must appear in the same source file. (Conventionally, it's written just before the function itself.) This macro call is not needed for internal-language functions, since PostgreSQL assumes that all internal functions use the version-1 convention. It is, however, required for dynamically-loaded functions.

In a version-1 function, each actual argument is fetched using a PG\_GETARG\_xxx() macro that corresponds to the argument's data type. (In non-strict functions there needs to be a previous check about argument null-ness using PG\_ARGISNULL(); see below.) The result is returned using a PG\_RE-TURN\_xxx() macro for the return type. PG\_GETARG\_xxx() takes as its argument the number of the function argument to fetch, where the count starts at 0. PG\_RETURN\_xxx() takes as its argument the actual value to return.

Here are some examples using the version-1 calling convention:

```
#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
PG_MODULE_MAGIC;
/* by value */
PG_FUNCTION_INFO_V1(add_one);
Datum
add_one(PG_FUNCTION_ARGS)
{
 int32 arg = PG_GETARG_INT32(0);
 PG_RETURN_INT32(arg + 1);
}
/* by reference, fixed length */
PG_FUNCTION_INFO_V1(add_one_float8);
Datum
add_one_float8(PG_FUNCTION_ARGS)
{
 /* The macros for FLOAT8 hide its pass-by-reference nature. */
 float8 arg = PG_GETARG_FLOAT8(0);
 PG_RETURN_FLOAT8(arg + 1.0);
}
PG_FUNCTION_INFO_V1(makepoint);
Datum
makepoint(PG_FUNCTION_ARGS)
{
 /* Here, the pass-by-reference nature of Point is not hidden.
 */
 Point *pointx = PG_GETARG_POINT_P(0);
 Point *pointy = PG_GETARG_POINT_P(1);
 Point *new_point = (Point *) palloc(sizeof(Point));
 new_point->x = pointx->x;
 new_point->y = pointy->y;
 PG_RETURN_POINT_P(new_point);
}
/* by reference, variable length */
PG_FUNCTION_INFO_V1(copytext);
```

```
Datum
copytext(PG_FUNCTION_ARGS)
{
 text *t = PG_GETARG_TEXT_PP(0);
 /*
 * VARSIZE_ANY_EXHDR is the size of the struct in bytes, minus
 the
 * VARHDRSZ or VARHDRSZ_SHORT of its header. Construct the
 copy with a
 * full-length header.
 */
 text *new_t = (text *) palloc(VARSIZE_ANY_EXHDR(t) +
 VARHDRSZ);
 SET_VARSIZE(new_t, VARSIZE_ANY_EXHDR(t) + VARHDRSZ);
 /*
 * VARDATA is a pointer to the data region of the new struct. 
 The source
 * could be a short datum, so retrieve its data through
 VARDATA_ANY.
 */
 memcpy((void *) VARDATA(new_t), /* destination */
 (void *) VARDATA_ANY(t), /* source */
 VARSIZE_ANY_EXHDR(t)); /* how many bytes */
 PG_RETURN_TEXT_P(new_t);
}
PG_FUNCTION_INFO_V1(concat_text);
Datum
concat_text(PG_FUNCTION_ARGS)
{
 text *arg1 = PG_GETARG_TEXT_PP(0);
 text *arg2 = PG_GETARG_TEXT_PP(1);
 int32 arg1_size = VARSIZE_ANY_EXHDR(arg1);
 int32 arg2_size = VARSIZE_ANY_EXHDR(arg2);
 int32 new_text_size = arg1_size + arg2_size + VARHDRSZ;
 text *new_text = (text *) palloc(new_text_size);
 SET_VARSIZE(new_text, new_text_size);
 memcpy(VARDATA(new_text), VARDATA_ANY(arg1), arg1_size);
 memcpy(VARDATA(new_text) + arg1_size, VARDATA_ANY(arg2),
 arg2_size);
 PG_RETURN_TEXT_P(new_text);
}
```

Supposing that the above code has been prepared in file funcs.c and compiled into a shared object, we could define the functions to PostgreSQL with commands like this:

```
CREATE FUNCTION add_one(integer) RETURNS integer
 AS 'DIRECTORY/funcs', 'add_one'
 LANGUAGE C STRICT;
-- note overloading of SQL function name "add_one"
```

```
CREATE FUNCTION add_one(double precision) RETURNS double precision
 AS 'DIRECTORY/funcs', 'add_one_float8'
 LANGUAGE C STRICT;
CREATE FUNCTION makepoint(point, point) RETURNS point
 AS 'DIRECTORY/funcs', 'makepoint'
 LANGUAGE C STRICT;
CREATE FUNCTION copytext(text) RETURNS text
 AS 'DIRECTORY/funcs', 'copytext'
 LANGUAGE C STRICT;
CREATE FUNCTION concat_text(text, text) RETURNS text
 AS 'DIRECTORY/funcs', 'concat_text'
 LANGUAGE C STRICT;
```

Here, DIRECTORY stands for the directory of the shared library file (for instance the PostgreSQL tutorial directory, which contains the code for the examples used in this section). (Better style would be to use just 'funcs' in the AS clause, after having added DIRECTORY to the search path. In any case, we can omit the system-specific extension for a shared library, commonly .so.)

Notice that we have specified the functions as "strict", meaning that the system should automatically assume a null result if any input value is null. By doing this, we avoid having to check for null inputs in the function code. Without this, we'd have to check for null values explicitly, using PG\_ARGISNUL-L().

The macro PG\_ARGISNULL(n) allows a function to test whether each input is null. (Of course, doing this is only necessary in functions not declared "strict".) As with the PG\_GETARG\_xxx() macros, the input arguments are counted beginning at zero. Note that one should refrain from executing PG\_GETARG\_xxx() until one has verified that the argument isn't null. To return a null result, execute PG\_RETURN\_NULL(); this works in both strict and nonstrict functions.

At first glance, the version-1 coding conventions might appear to be just pointless obscurantism, compared to using plain C calling conventions. They do however allow us to deal with NULLable arguments/return values, and "toasted" (compressed or out-of-line) values.

Other options provided by the version-1 interface are two variants of the PG\_GETARG\_xxx() macros. The first of these, PG\_GETARG\_xxx\_COPY(), guarantees to return a copy of the specified argument that is safe for writing into. (The normal macros will sometimes return a pointer to a value that is physically stored in a table, which must not be written to. Using the PG\_GETARG\_xxx\_COPY() macros guarantees a writable result.) The second variant consists of the PG\_GETARG\_xxx\_SLICE() macros which take three arguments. The first is the number of the function argument (as above). The second and third are the offset and length of the segment to be returned. Offsets are counted from zero, and a negative length requests that the remainder of the value be returned. These macros provide more efficient access to parts of large values in the case where they have storage type "external". (The storage type of a column can be specified using ALTER TABLE tablename ALTER COLUMN colname SET STORAGE storagetype. storagetype is one of plain, external, extended, or main.)

Finally, the version-1 function call conventions make it possible to return set results ([Section 38.10.8\)](#page-187-0) and implement trigger functions (Chapter 39) and procedural-language call handlers (Chapter 56). For more details see src/backend/utils/fmgr/README in the source distribution.

## <span id="page-181-0"></span>**38.10.4. Writing Code**

Before we turn to the more advanced topics, we should discuss some coding rules for PostgreSQL Clanguage functions. While it might be possible to load functions written in languages other than C into PostgreSQL, this is usually difficult (when it is possible at all) because other languages, such as C++, FORTRAN, or Pascal often do not follow the same calling convention as C. That is, other languages do not pass argument and return values between functions in the same way. For this reason, we will assume that your C-language functions are actually written in C.

The basic rules for writing and building C functions are as follows:

- Use pg\_config --includedir-server to find out where the PostgreSQL server header files are installed on your system (or the system that your users will be running on).
- Compiling and linking your code so that it can be dynamically loaded into PostgreSQL always requires special flags. See [Section 38.10.5](#page-182-0) for a detailed explanation of how to do it for your particular operating system.
- Remember to define a "magic block" for your shared library, as described in [Section 38.10.1](#page-174-3).
- When allocating memory, use the PostgreSQL functions palloc and pfree instead of the corresponding C library functions malloc and free. The memory allocated by palloc will be freed automatically at the end of each transaction, preventing memory leaks.
- Always zero the bytes of your structures using memset (or allocate them with palloc0 in the first place). Even if you assign to each field of your structure, there might be alignment padding (holes in the structure) that contain garbage values. Without this, it's difficult to support hash indexes or hash joins, as you must pick out only the significant bits of your data structure to compute a hash. The planner also sometimes relies on comparing constants via bitwise equality, so you can get undesirable planning results if logically-equivalent values aren't bitwise equal.
- Most of the internal PostgreSQL types are declared in postgres.h, while the function manager interfaces (PG\_FUNCTION\_ARGS, etc.) are in fmgr.h, so you will need to include at least these two files. For portability reasons it's best to include postgres.h *first*, before any other system or user header files. Including postgres.h will also include elog.h and palloc.h for you.
- Symbol names defined within object files must not conflict with each other or with symbols defined in the PostgreSQL server executable. You will have to rename your functions or variables if you get error messages to this effect.

## <span id="page-182-0"></span>**38.10.5. Compiling and Linking Dynamically-Loaded Functions**

Before you are able to use your PostgreSQL extension functions written in C, they must be compiled and linked in a special way to produce a file that can be dynamically loaded by the server. To be precise, a *shared library* needs to be created.

For information beyond what is contained in this section you should read the documentation of your operating system, in particular the manual pages for the C compiler, cc, and the link editor, ld. In addition, the PostgreSQL source code contains several working examples in the contrib directory. If you rely on these examples you will make your modules dependent on the availability of the PostgreSQL source code, however.

Creating shared libraries is generally analogous to linking executables: first the source files are compiled into object files, then the object files are linked together. The object files need to be created as *position-independent code* (PIC), which conceptually means that they can be placed at an arbitrary location in memory when they are loaded by the executable. (Object files intended for executables are usually not compiled that way.) The command to link a shared library contains special flags to distinguish it from linking an executable (at least in theory — on some systems the practice is much uglier).

In the following examples we assume that your source code is in a file foo.c and we will create a shared library foo.so. The intermediate object file will be called foo.o unless otherwise noted. A shared library can contain more than one object file, but we only use one here.

#### FreeBSD

The compiler flag to create PIC is -fPIC. To create shared libraries the compiler flag is shared.

```
gcc -fPIC -c foo.c
gcc -shared -o foo.so foo.o
```

This is applicable as of version 3.0 of FreeBSD.

#### HP-UX

The compiler flag of the system compiler to create PIC is +z. When using GCC it's -fPIC. The linker flag for shared libraries is -b. So:

```
cc +z -c foo.c
or:
gcc -fPIC -c foo.c
and then:
ld -b -o foo.sl foo.o
```

HP-UX uses the extension .sl for shared libraries, unlike most other systems.

#### Linux

The compiler flag to create PIC is -fPIC. The compiler flag to create a shared library is shared. A complete example looks like this:

```
cc -fPIC -c foo.c
cc -shared -o foo.so foo.o
```

#### macOS

Here is an example. It assumes the developer tools are installed.

```
cc -c foo.c
cc -bundle -flat_namespace -undefined suppress -o foo.so foo.o
```

#### NetBSD

The compiler flag to create PIC is -fPIC. For ELF systems, the compiler with the flag -shared is used to link shared libraries. On the older non-ELF systems, ld -Bshareable is used.

```
gcc -fPIC -c foo.c
gcc -shared -o foo.so foo.o
```

#### OpenBSD

The compiler flag to create PIC is -fPIC. ld -Bshareable is used to link shared libraries.

```
gcc -fPIC -c foo.c
ld -Bshareable -o foo.so foo.o
```

#### Solaris

The compiler flag to create PIC is -KPIC with the Sun compiler and -fPIC with GCC. To link shared libraries, the compiler option is -G with either compiler or alternatively -shared with GCC.

```
cc -KPIC -c foo.c
cc -G -o foo.so foo.o
or
gcc -fPIC -c foo.c
gcc -G -o foo.so foo.o
```

### **Tip**

If this is too complicated for you, you should consider using [GNU Libtool](https://www.gnu.org/software/libtool/)<sup>1</sup> , which hides the platform differences behind a uniform interface.

The resulting shared library file can then be loaded into PostgreSQL. When specifying the file name to the CREATE FUNCTION command, one must give it the name of the shared library file, not the intermediate object file. Note that the system's standard shared-library extension (usually .so or .sl) can be omitted from the CREATE FUNCTION command, and normally should be omitted for best portability.

Refer back to [Section 38.10.1](#page-174-3) about where the server expects to find the shared library files.

## <span id="page-184-0"></span>**38.10.6. Composite-Type Arguments**

Composite types do not have a fixed layout like C structures. Instances of a composite type can contain null fields. In addition, composite types that are part of an inheritance hierarchy can have different fields than other members of the same inheritance hierarchy. Therefore, PostgreSQL provides a function interface for accessing fields of composite types from C.

Suppose we want to write a function to answer the query:

```
SELECT name, c_overpaid(emp, 1500) AS overpaid
 FROM emp
 WHERE name = 'Bill' OR name = 'Sam';
```

Using the version-1 calling conventions, we can define c\_overpaid as:

```
#include "postgres.h"
#include "executor/executor.h" /* for GetAttributeByName() */
PG_MODULE_MAGIC;
```

<sup>1</sup> <https://www.gnu.org/software/libtool/>

```
PG_FUNCTION_INFO_V1(c_overpaid);
Datum
c_overpaid(PG_FUNCTION_ARGS)
{
 HeapTupleHeader t = PG_GETARG_HEAPTUPLEHEADER(0);
 int32 limit = PG_GETARG_INT32(1);
 bool isnull;
 Datum salary;
 salary = GetAttributeByName(t, "salary", &isnull);
 if (isnull)
 PG_RETURN_BOOL(false);
 /* Alternatively, we might prefer to do PG_RETURN_NULL() for
 null salary. */
 PG_RETURN_BOOL(DatumGetInt32(salary) > limit);
}
```

GetAttributeByName is the PostgreSQL system function that returns attributes out of the specified row. It has three arguments: the argument of type HeapTupleHeader passed into the function, the name of the desired attribute, and a return parameter that tells whether the attribute is null. GetAttributeByName returns a Datum value that you can convert to the proper data type by using the appropriate DatumGetXXX() macro. Note that the return value is meaningless if the null flag is set; always check the null flag before trying to do anything with the result.

There is also GetAttributeByNum, which selects the target attribute by column number instead of name.

The following command declares the function c\_overpaid in SQL:

```
CREATE FUNCTION c_overpaid(emp, integer) RETURNS boolean
 AS 'DIRECTORY/funcs', 'c_overpaid'
 LANGUAGE C STRICT;
```

Notice we have used STRICT so that we did not have to check whether the input arguments were NULL.

## <span id="page-185-0"></span>**38.10.7. Returning Rows (Composite Types)**

To return a row or composite-type value from a C-language function, you can use a special API that provides macros and functions to hide most of the complexity of building composite data types. To use this API, the source file must include:

```
#include "funcapi.h"
```

There are two ways you can build a composite data value (henceforth a "tuple"): you can build it from an array of Datum values, or from an array of C strings that can be passed to the input conversion functions of the tuple's column data types. In either case, you first need to obtain or construct a TupleDesc descriptor for the tuple structure. When working with Datums, you pass the TupleDesc to BlessTupleDesc, and then call heap\_form\_tuple for each row. When working with C strings, you pass the TupleDesc to TupleDescGetAttInMetadata, and then call BuildTupleFromCStrings for each row. In the case of a function returning a set of tuples, the setup steps can all be done once during the first call of the function.

Several helper functions are available for setting up the needed TupleDesc. The recommended way to do this in most functions returning composite values is to call:

```
TypeFuncClass get_call_result_type(FunctionCallInfo fcinfo,
 Oid *resultTypeId,
 TupleDesc *resultTupleDesc)
```

passing the same fcinfo struct passed to the calling function itself. (This of course requires that you use the version-1 calling conventions.) resultTypeId can be specified as NULL or as the address of a local variable to receive the function's result type OID. resultTupleDesc should be the address of a local TupleDesc variable. Check that the result is TYPEFUNC\_COMPOSITE; if so, resultTupleDesc has been filled with the needed TupleDesc. (If it is not, you can report an error along the lines of "function returning record called in context that cannot accept type record".)

### **Tip**

get\_call\_result\_type can resolve the actual type of a polymorphic function result; so it is useful in functions that return scalar polymorphic results, not only functions that return composites. The resultTypeId output is primarily useful for functions returning polymorphic scalars.

### **Note**

get\_call\_result\_type has a sibling get\_expr\_result\_type, which can be used to resolve the expected output type for a function call represented by an expression tree. This can be used when trying to determine the result type from outside the function itself. There is also get\_func\_result\_type, which can be used when only the function's OID is available. However these functions are not able to deal with functions declared to return record, and get\_func\_result\_type cannot resolve polymorphic types, so you should preferentially use get\_call\_result\_type.

Older, now-deprecated functions for obtaining TupleDescs are:

```
TupleDesc RelationNameGetTupleDesc(const char *relname)
```

to get a TupleDesc for the row type of a named relation, and:

```
TupleDesc TypeGetTupleDesc(Oid typeoid, List *colaliases)
```

to get a TupleDesc based on a type OID. This can be used to get a TupleDesc for a base or composite type. It will not work for a function that returns record, however, and it cannot resolve polymorphic types.

Once you have a TupleDesc, call:

```
TupleDesc BlessTupleDesc(TupleDesc tupdesc)
```

if you plan to work with Datums, or:

AttInMetadata \*TupleDescGetAttInMetadata(TupleDesc tupdesc)

if you plan to work with C strings. If you are writing a function returning set, you can save the results of these functions in the FuncCallContext structure — use the tuple\_desc or attinmeta field respectively.

When working with Datums, use:

```
HeapTuple heap_form_tuple(TupleDesc tupdesc, Datum *values, bool
 *isnull)
```

to build a HeapTuple given user data in Datum form.

When working with C strings, use:

```
HeapTuple BuildTupleFromCStrings(AttInMetadata *attinmeta, char
 **values)
```

to build a HeapTuple given user data in C string form. values is an array of C strings, one for each attribute of the return row. Each C string should be in the form expected by the input function of the attribute data type. In order to return a null value for one of the attributes, the corresponding pointer in the values array should be set to NULL. This function will need to be called again for each row you return.

Once you have built a tuple to return from your function, it must be converted into a Datum. Use:

```
HeapTupleGetDatum(HeapTuple tuple)
```

to convert a HeapTuple into a valid Datum. This Datum can be returned directly if you intend to return just a single row, or it can be used as the current return value in a set-returning function.

An example appears in the next section.

## <span id="page-187-0"></span>**38.10.8. Returning Sets**

C-language functions have two options for returning sets (multiple rows). In one method, called *ValuePerCall* mode, a set-returning function is called repeatedly (passing the same arguments each time) and it returns one new row on each call, until it has no more rows to return and signals that by returning NULL. The set-returning function (SRF) must therefore save enough state across calls to remember what it was doing and return the correct next item on each call. In the other method, called *Materialize* mode, an SRF fills and returns a tuplestore object containing its entire result; then only one call occurs for the whole result, and no inter-call state is needed.

When using ValuePerCall mode, it is important to remember that the query is not guaranteed to be run to completion; that is, due to options such as LIMIT, the executor might stop making calls to the set-returning function before all rows have been fetched. This means it is not safe to perform cleanup activities in the last call, because that might not ever happen. It's recommended to use Materialize mode for functions that need access to external resources, such as file descriptors.

The remainder of this section documents a set of helper macros that are commonly used (though not required to be used) for SRFs using ValuePerCall mode. Additional details about Materialize mode can be found in src/backend/utils/fmgr/README. Also, the contrib modules in the PostgreSQL source distribution contain many examples of SRFs using both ValuePerCall and Materialize mode.

To use the ValuePerCall support macros described here, include funcapi.h. These macros work with a structure FuncCallContext that contains the state that needs to be saved across calls. Within the calling SRF, fcinfo->flinfo->fn\_extra is used to hold a pointer to FuncCallContext across calls. The macros automatically fill that field on first use, and expect to find the same pointer there on subsequent uses.

```
typedef struct FuncCallContext
{
 /*
 * Number of times we've been called before
 *
 * call_cntr is initialized to 0 for you by
 SRF_FIRSTCALL_INIT(), and
 * incremented for you every time SRF_RETURN_NEXT() is called.
 */
 uint64 call_cntr;
 /*
 * OPTIONAL maximum number of calls
 *
 * max_calls is here for convenience only and setting it is
 optional.
 * If not set, you must provide alternative means to know when
 the
 * function is done.
 */
 uint64 max_calls;
 /*
 * OPTIONAL pointer to miscellaneous user-provided context
 information
 *
 * user_fctx is for use as a pointer to your own data to retain
 * arbitrary context information between calls of your
 function.
 */
 void *user_fctx;
 /*
 * OPTIONAL pointer to struct containing attribute type input
 metadata
 *
 * attinmeta is for use when returning tuples (i.e., composite
 data types)
 * and is not used when returning base data types. It is only
 needed
 * if you intend to use BuildTupleFromCStrings() to create the
 return
 * tuple.
 */
 AttInMetadata *attinmeta;
 /*
 * memory context used for structures that must live for
 multiple calls
 *
 * multi_call_memory_ctx is set by SRF_FIRSTCALL_INIT() for
 you, and used
 * by SRF_RETURN_DONE() for cleanup. It is the most appropriate
 memory
```

```
 * context for any memory that is to be reused across multiple
 calls
 * of the SRF.
 */
 MemoryContext multi_call_memory_ctx;
 /*
 * OPTIONAL pointer to struct containing tuple description
 *
 * tuple_desc is for use when returning tuples (i.e., composite
 data types)
 * and is only needed if you are going to build the tuples with
 * heap_form_tuple() rather than with BuildTupleFromCStrings().
 Note that
 * the TupleDesc pointer stored here should usually have been
 run through
 * BlessTupleDesc() first.
 */
 TupleDesc tuple_desc;
} FuncCallContext;
```

The macros to be used by an SRF using this infrastructure are:

```
SRF_IS_FIRSTCALL()
```

Use this to determine if your function is being called for the first or a subsequent time. On the first call (only), call:

```
SRF_FIRSTCALL_INIT()
```

to initialize the FuncCallContext. On every function call, including the first, call:

```
SRF_PERCALL_SETUP()
```

to set up for using the FuncCallContext.

If your function has data to return in the current call, use:

```
SRF_RETURN_NEXT(funcctx, result)
```

to return it to the caller. (result must be of type Datum, either a single value or a tuple prepared as described above.) Finally, when your function is finished returning data, use:

```
SRF_RETURN_DONE(funcctx)
```

to clean up and end the SRF.

The memory context that is current when the SRF is called is a transient context that will be cleared between calls. This means that you do not need to call pfree on everything you allocated using palloc; it will go away anyway. However, if you want to allocate any data structures to live across calls, you need to put them somewhere else. The memory context referenced by multi\_call\_memory\_ctx is a suitable location for any data that needs to survive until the SRF is finished running. In most cases, this means that you should switch into multi\_call\_memory\_ctx while doing the first-call setup. Use funcctx->user\_fctx to hold a pointer to any such cross-call data structures. (Data you allocate in multi\_call\_memory\_ctx will go away automatically when the query ends, so it is not necessary to free that data manually, either.)

### **Warning**

While the actual arguments to the function remain unchanged between calls, if you detoast the argument values (which is normally done transparently by the PG\_GETARG\_xxx macro) in the transient context then the detoasted copies will be freed on each cycle. Accordingly, if you keep references to such values in your user\_fctx, you must either copy them into the multi\_call\_memory\_ctx after detoasting, or ensure that you detoast the values only in that context.

A complete pseudo-code example looks like the following:

```
Datum
my_set_returning_function(PG_FUNCTION_ARGS)
{
 FuncCallContext *funcctx;
 Datum result;
 further declarations as needed
 if (SRF_IS_FIRSTCALL())
 {
 MemoryContext oldcontext;
 funcctx = SRF_FIRSTCALL_INIT();
 oldcontext = MemoryContextSwitchTo(funcctx-
>multi_call_memory_ctx);
 /* One-time setup code appears here: */
 user code
 if returning composite
 build TupleDesc, and perhaps AttInMetadata
 endif returning composite
 user code
 MemoryContextSwitchTo(oldcontext);
 }
 /* Each-time setup code appears here: */
 user code
 funcctx = SRF_PERCALL_SETUP();
 user code
 /* this is just one way we might test whether we are done: */
 if (funcctx->call_cntr < funcctx->max_calls)
 {
 /* Here we want to return another item: */
 user code
 obtain result Datum
 SRF_RETURN_NEXT(funcctx, result);
 }
 else
 {
 /* Here we are done returning items, so just report that
 fact. */
 /* (Resist the temptation to put cleanup code here.) */
 SRF_RETURN_DONE(funcctx);
 }
}
```

A complete example of a simple SRF returning a composite type looks like:

```
PG_FUNCTION_INFO_V1(retcomposite);
Datum
retcomposite(PG_FUNCTION_ARGS)
{
 FuncCallContext *funcctx;
 int call_cntr;
 int max_calls;
 TupleDesc tupdesc;
 AttInMetadata *attinmeta;
 /* stuff done only on the first call of the function */
 if (SRF_IS_FIRSTCALL())
 {
 MemoryContext oldcontext;
 /* create a function context for cross-call persistence */
 funcctx = SRF_FIRSTCALL_INIT();
 /* switch to memory context appropriate for multiple
 function calls */
 oldcontext = MemoryContextSwitchTo(funcctx-
>multi_call_memory_ctx);
 /* total number of tuples to be returned */
 funcctx->max_calls = PG_GETARG_UINT32(0);
 /* Build a tuple descriptor for our result type */
 if (get_call_result_type(fcinfo, NULL, &tupdesc) !=
 TYPEFUNC_COMPOSITE)
 ereport(ERROR,
 (errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
 errmsg("function returning record called in
 context "
 "that cannot accept type record")));
 /*
 * generate attribute metadata needed later to produce
 tuples from raw
 * C strings
 */
 attinmeta = TupleDescGetAttInMetadata(tupdesc);
 funcctx->attinmeta = attinmeta;
 MemoryContextSwitchTo(oldcontext);
 }
 /* stuff done on every call of the function */
 funcctx = SRF_PERCALL_SETUP();
 call_cntr = funcctx->call_cntr;
 max_calls = funcctx->max_calls;
 attinmeta = funcctx->attinmeta;
```

```
 if (call_cntr < max_calls) /* do when there is more left to
 send */
 {
 char **values;
 HeapTuple tuple;
 Datum result;
 /*
 * Prepare a values array for building the returned tuple.
 * This should be an array of C strings which will
 * be processed later by the type input functions.
 */
 values = (char **) palloc(3 * sizeof(char *));
 values[0] = (char *) palloc(16 * sizeof(char));
 values[1] = (char *) palloc(16 * sizeof(char));
 values[2] = (char *) palloc(16 * sizeof(char));
 snprintf(values[0], 16, "%d", 1 * PG_GETARG_INT32(1));
 snprintf(values[1], 16, "%d", 2 * PG_GETARG_INT32(1));
 snprintf(values[2], 16, "%d", 3 * PG_GETARG_INT32(1));
 /* build a tuple */
 tuple = BuildTupleFromCStrings(attinmeta, values);
 /* make the tuple into a datum */
 result = HeapTupleGetDatum(tuple);
 /* clean up (this is not really necessary) */
 pfree(values[0]);
 pfree(values[1]);
 pfree(values[2]);
 pfree(values);
 SRF_RETURN_NEXT(funcctx, result);
 }
 else /* do when there is no more left */
 {
 SRF_RETURN_DONE(funcctx);
 }
}
One way to declare this function in SQL is:
CREATE TYPE __retcomposite AS (f1 integer, f2 integer, f3 integer);
CREATE OR REPLACE FUNCTION retcomposite(integer, integer)
 RETURNS SETOF __retcomposite
 AS 'filename', 'retcomposite'
 LANGUAGE C IMMUTABLE STRICT;
A different way is to use OUT parameters:
CREATE OR REPLACE FUNCTION retcomposite(IN integer, IN integer,
 OUT f1 integer, OUT f2 integer, OUT f3 integer)
 RETURNS SETOF record
 AS 'filename', 'retcomposite'
```

```
 LANGUAGE C IMMUTABLE STRICT;
```

Notice that in this method the output type of the function is formally an anonymous record type.

## <span id="page-193-0"></span>**38.10.9. Polymorphic Arguments and Return Types**

C-language functions can be declared to accept and return the polymorphic types described in [Sec](#page-151-2)[tion 38.2.5](#page-151-2). When a function's arguments or return types are defined as polymorphic types, the function author cannot know in advance what data type it will be called with, or need to return. There are two routines provided in fmgr.h to allow a version-1 C function to discover the actual data types of its arguments and the type it is expected to return. The routines are called get\_fn\_expr\_rettype(FmgrInfo \*flinfo) and get\_fn\_expr\_argtype(FmgrInfo \*flinfo, int argnum). They return the result or argument type OID, or InvalidOid if the information is not available. The structure flinfo is normally accessed as fcinfo->flinfo. The parameter argnum is zero based. get\_call\_result\_type can also be used as an alternative to get\_fn\_expr\_rettype. There is also get\_fn\_expr\_variadic, which can be used to find out whether variadic arguments have been merged into an array. This is primarily useful for VARIADIC "any" functions, since such merging will always have occurred for variadic functions taking ordinary array types.

For example, suppose we want to write a function to accept a single element of any type, and return a one-dimensional array of that type:

```
PG_FUNCTION_INFO_V1(make_array);
Datum
make_array(PG_FUNCTION_ARGS)
{
 ArrayType *result;
 Oid element_type = get_fn_expr_argtype(fcinfo->flinfo,
 0);
 Datum element;
 bool isnull;
 int16 typlen;
 bool typbyval;
 char typalign;
 int ndims;
 int dims[MAXDIM];
 int lbs[MAXDIM];
 if (!OidIsValid(element_type))
 elog(ERROR, "could not determine data type of input");
 /* get the provided element, being careful in case it's NULL */
 isnull = PG_ARGISNULL(0);
 if (isnull)
 element = (Datum) 0;
 else
 element = PG_GETARG_DATUM(0);
 /* we have one dimension */
 ndims = 1;
 /* and one element */
 dims[0] = 1;
 /* and lower bound is 1 */
 lbs[0] = 1;
 /* get required info about the element type */
 get_typlenbyvalalign(element_type, &typlen, &typbyval,
 &typalign);
```

```
 /* now build the array */
 result = construct_md_array(&element, &isnull, ndims, dims,
 lbs,
 element_type, typlen, typbyval,
 typalign);
 PG_RETURN_ARRAYTYPE_P(result);
}
```

The following command declares the function make\_array in SQL:

```
CREATE FUNCTION make_array(anyelement) RETURNS anyarray
 AS 'DIRECTORY/funcs', 'make_array'
 LANGUAGE C IMMUTABLE;
```

There is a variant of polymorphism that is only available to C-language functions: they can be declared to take parameters of type "any". (Note that this type name must be double-quoted, since it's also an SQL reserved word.) This works like anyelement except that it does not constrain different "any" arguments to be the same type, nor do they help determine the function's result type. A C-language function can also declare its final parameter to be VARIADIC "any". This will match one or more actual arguments of any type (not necessarily the same type). These arguments will *not* be gathered into an array as happens with normal variadic functions; they will just be passed to the function separately. The PG\_NARGS() macro and the methods described above must be used to determine the number of actual arguments and their types when using this feature. Also, users of such a function might wish to use the VARIADIC keyword in their function call, with the expectation that the function would treat the array elements as separate arguments. The function itself must implement that behavior if wanted, after using get\_fn\_expr\_variadic to detect that the actual argument was marked with VARIADIC.

## <span id="page-194-0"></span>**38.10.10. Shared Memory and LWLocks**

Add-ins can reserve LWLocks and an allocation of shared memory on server startup. The add-in's shared library must be preloaded by specifying it in shared\_preload\_libraries. Shared memory is reserved by calling:

```
void RequestAddinShmemSpace(int size)
from your _PG_init function.
```

LWLocks are reserved by calling:

```
void RequestNamedLWLockTranche(const char *tranche_name, int
 num_lwlocks)
```

from \_PG\_init. This will ensure that an array of num\_lwlocks LWLocks is available under the name tranche\_name. Use GetNamedLWLockTranche to get a pointer to this array.

To avoid possible race-conditions, each backend should use the LWLock AddinShmemInitLock when connecting to and initializing its allocation of shared memory, as shown here:

```
static mystruct *ptr = NULL;
if (!ptr)
```

```
{
 bool found;
 LWLockAcquire(AddinShmemInitLock, LW_EXCLUSIVE);
 ptr = ShmemInitStruct("my struct name", size, &found);
 if (!found)
 {
 initialize contents of shmem area;
 acquire any requested LWLocks using:
 ptr->locks = GetNamedLWLockTranche("my tranche
 name");
 }
 LWLockRelease(AddinShmemInitLock);
}
```

## <span id="page-195-0"></span>**38.10.11. Using C++ for Extensibility**

Although the PostgreSQL backend is written in C, it is possible to write extensions in C++ if these guidelines are followed:

- All functions accessed by the backend must present a C interface to the backend; these C functions can then call C++ functions. For example, extern C linkage is required for backend-accessed functions. This is also necessary for any functions that are passed as pointers between the backend and C++ code.
- Free memory using the appropriate deallocation method. For example, most backend memory is allocated using palloc(), so use pfree() to free it. Using C++ delete in such cases will fail.
- Prevent exceptions from propagating into the C code (use a catch-all block at the top level of all extern C functions). This is necessary even if the C++ code does not explicitly throw any exceptions, because events like out-of-memory can still throw exceptions. Any exceptions must be caught and appropriate errors passed back to the C interface. If possible, compile C++ with -fnoexceptions to eliminate exceptions entirely; in such cases, you must check for failures in your C++ code, e.g., check for NULL returned by new().
- If calling backend functions from C++ code, be sure that the C++ call stack contains only plain old data structures (POD). This is necessary because backend errors generate a distant longjmp() that does not properly unroll a C++ call stack with non-POD objects.

In summary, it is best to place C++ code behind a wall of extern C functions that interface to the backend, and avoid exception, memory, and call stack leakage.

# <span id="page-195-1"></span>**38.11. Function Optimization Information**

By default, a function is just a "black box" that the database system knows very little about the behavior of. However, that means that queries using the function may be executed much less efficiently than they could be. It is possible to supply additional knowledge that helps the planner optimize function calls.

Some basic facts can be supplied by declarative annotations provided in the CREATE FUNCTION command. Most important of these is the function's [volatility category](#page-172-0) (IMMUTABLE, STABLE, or VOLATILE); one should always be careful to specify this correctly when defining a function. The parallel safety property (PARALLEL UNSAFE, PARALLEL RESTRICTED, or PARALLEL SAFE) must also be specified if you hope to use the function in parallelized queries. It can also be useful to specify the function's estimated execution cost, and/or the number of rows a set-returning function is estimated to return. However, the declarative way of specifying those two facts only allows specifying a constant value, which is often inadequate.

It is also possible to attach a *planner support function* to an SQL-callable function (called its *target function*), and thereby provide knowledge about the target function that is too complex to be represented declaratively. Planner support functions have to be written in C (although their target functions might not be), so this is an advanced feature that relatively few people will use.

A planner support function must have the SQL signature

```
supportfn(internal) returns internal
```

It is attached to its target function by specifying the SUPPORT clause when creating the target function.

The details of the API for planner support functions can be found in file src/include/nodes/ supportnodes.h in the PostgreSQL source code. Here we provide just an overview of what planner support functions can do. The set of possible requests to a support function is extensible, so more things might be possible in future versions.

Some function calls can be simplified during planning based on properties specific to the function. For example, int4mul(n, 1) could be simplified to just n. This type of transformation can be performed by a planner support function, by having it implement the SupportRequestSimplify request type. The support function will be called for each instance of its target function found in a query parse tree. If it finds that the particular call can be simplified into some other form, it can build and return a parse tree representing that expression. This will automatically work for operators based on the function, too — in the example just given, n \* 1 would also be simplified to n. (But note that this is just an example; this particular optimization is not actually performed by standard PostgreSQL.) We make no guarantee that PostgreSQL will never call the target function in cases that the support function could simplify. Ensure rigorous equivalence between the simplified expression and an actual execution of the target function.

For target functions that return boolean, it is often useful to estimate the fraction of rows that will be selected by a WHERE clause using that function. This can be done by a support function that implements the SupportRequestSelectivity request type.

If the target function's run time is highly dependent on its inputs, it may be useful to provide a nonconstant cost estimate for it. This can be done by a support function that implements the Support-RequestCost request type.

For target functions that return sets, it is often useful to provide a non-constant estimate for the number of rows that will be returned. This can be done by a support function that implements the Support-RequestRows request type.

For target functions that return boolean, it may be possible to convert a function call appearing in WHERE into an indexable operator clause or clauses. The converted clauses might be exactly equivalent to the function's condition, or they could be somewhat weaker (that is, they might accept some values that the function condition does not). In the latter case the index condition is said to be *lossy*; it can still be used to scan an index, but the function call will have to be executed for each row returned by the index to see if it really passes the WHERE condition or not. To create such conditions, the support function must implement the SupportRequestIndexCondition request type.

# <span id="page-196-0"></span>**38.12. User-Defined Aggregates**

Aggregate functions in PostgreSQL are defined in terms of *state values* and *state transition functions*. That is, an aggregate operates using a state value that is updated as each successive input row is processed. To define a new aggregate function, one selects a data type for the state value, an initial value for the state, and a state transition function. The state transition function takes the previous state value and the aggregate's input value(s) for the current row, and returns a new state value. A *final function* can also be specified, in case the desired result of the aggregate is different from the data that needs to be kept in the running state value. The final function takes the ending state value and returns whatever is wanted as the aggregate result. In principle, the transition and final functions are just ordinary functions that could also be used outside the context of the aggregate. (In practice, it's often helpful for performance reasons to create specialized transition functions that can only work when called as part of an aggregate.)

Thus, in addition to the argument and result data types seen by a user of the aggregate, there is an internal state-value data type that might be different from both the argument and result types.

If we define an aggregate that does not use a final function, we have an aggregate that computes a running function of the column values from each row. sum is an example of this kind of aggregate. sum starts at zero and always adds the current row's value to its running total. For example, if we want to make a sum aggregate to work on a data type for complex numbers, we only need the addition function for that data type. The aggregate definition would be:

```
CREATE AGGREGATE sum (complex)
(
 sfunc = complex_add,
 stype = complex,
 initcond = '(0,0)'
);
which we might use like this:
SELECT sum(a) FROM test_complex;
 sum
-----------
 (34,53.9)
```

(Notice that we are relying on function overloading: there is more than one aggregate named sum, but PostgreSQL can figure out which kind of sum applies to a column of type complex.)

The above definition of sum will return zero (the initial state value) if there are no nonnull input values. Perhaps we want to return null in that case instead — the SQL standard expects sum to behave that way. We can do this simply by omitting the initcond phrase, so that the initial state value is null. Ordinarily this would mean that the sfunc would need to check for a null state-value input. But for sum and some other simple aggregates like max and min, it is sufficient to insert the first nonnull input value into the state variable and then start applying the transition function at the second nonnull input value. PostgreSQL will do that automatically if the initial state value is null and the transition function is marked "strict" (i.e., not to be called for null inputs).

Another bit of default behavior for a "strict" transition function is that the previous state value is retained unchanged whenever a null input value is encountered. Thus, null values are ignored. If you need some other behavior for null inputs, do not declare your transition function as strict; instead code it to test for null inputs and do whatever is needed.

avg (average) is a more complex example of an aggregate. It requires two pieces of running state: the sum of the inputs and the count of the number of inputs. The final result is obtained by dividing these quantities. Average is typically implemented by using an array as the state value. For example, the built-in implementation of avg(float8) looks like:

```
CREATE AGGREGATE avg (float8)
(
 sfunc = float8_accum,
 stype = float8[],
 finalfunc = float8_avg,
```

```
 initcond = '{0,0,0}'
);
```

### **Note**

float8\_accum requires a three-element array, not just two elements, because it accumulates the sum of squares as well as the sum and count of the inputs. This is so that it can be used for some other aggregates as well as avg.

Aggregate function calls in SQL allow DISTINCT and ORDER BY options that control which rows are fed to the aggregate's transition function and in what order. These options are implemented behind the scenes and are not the concern of the aggregate's support functions.

For further details see the CREATE AGGREGATE command.

## <span id="page-198-0"></span>**38.12.1. Moving-Aggregate Mode**

Aggregate functions can optionally support *moving-aggregate mode*, which allows substantially faster execution of aggregate functions within windows with moving frame starting points. (See Section 3.5 and Section 4.2.8 for information about use of aggregate functions as window functions.) The basic idea is that in addition to a normal "forward" transition function, the aggregate provides an *inverse transition function*, which allows rows to be removed from the aggregate's running state value when they exit the window frame. For example a sum aggregate, which uses addition as the forward transition function, would use subtraction as the inverse transition function. Without an inverse transition function, the window function mechanism must recalculate the aggregate from scratch each time the frame starting point moves, resulting in run time proportional to the number of input rows times the average frame length. With an inverse transition function, the run time is only proportional to the number of input rows.

The inverse transition function is passed the current state value and the aggregate input value(s) for the earliest row included in the current state. It must reconstruct what the state value would have been if the given input row had never been aggregated, but only the rows following it. This sometimes requires that the forward transition function keep more state than is needed for plain aggregation mode. Therefore, the moving-aggregate mode uses a completely separate implementation from the plain mode: it has its own state data type, its own forward transition function, and its own final function if needed. These can be the same as the plain mode's data type and functions, if there is no need for extra state.

As an example, we could extend the sum aggregate given above to support moving-aggregate mode like this:

```
CREATE AGGREGATE sum (complex)
(
 sfunc = complex_add,
 stype = complex,
 initcond = '(0,0)',
 msfunc = complex_add,
 minvfunc = complex_sub,
 mstype = complex,
 minitcond = '(0,0)'
);
```

The parameters whose names begin with m define the moving-aggregate implementation. Except for the inverse transition function minvfunc, they correspond to the plain-aggregate parameters without m.

The forward transition function for moving-aggregate mode is not allowed to return null as the new state value. If the inverse transition function returns null, this is taken as an indication that the inverse function cannot reverse the state calculation for this particular input, and so the aggregate calculation will be redone from scratch for the current frame starting position. This convention allows moving-aggregate mode to be used in situations where there are some infrequent cases that are impractical to reverse out of the running state value. The inverse transition function can "punt" on these cases, and yet still come out ahead so long as it can work for most cases. As an example, an aggregate working with floating-point numbers might choose to punt when a NaN (not a number) input has to be removed from the running state value.

When writing moving-aggregate support functions, it is important to be sure that the inverse transition function can reconstruct the correct state value exactly. Otherwise there might be user-visible differences in results depending on whether the moving-aggregate mode is used. An example of an aggregate for which adding an inverse transition function seems easy at first, yet where this requirement cannot be met is sum over float4 or float8 inputs. A naive declaration of sum(float8) could be

```
CREATE AGGREGATE unsafe_sum (float8)
(
 stype = float8,
 sfunc = float8pl,
 mstype = float8,
 msfunc = float8pl,
 minvfunc = float8mi
);
```

This aggregate, however, can give wildly different results than it would have without the inverse transition function. For example, consider

```
SELECT
 unsafe_sum(x) OVER (ORDER BY n ROWS BETWEEN CURRENT ROW AND 1
 FOLLOWING)
FROM (VALUES (1, 1.0e20::float8),
 (2, 1.0::float8)) AS v (n,x);
```

This query returns 0 as its second result, rather than the expected answer of 1. The cause is the limited precision of floating-point values: adding 1 to 1e20 results in 1e20 again, and so subtracting 1e20 from that yields 0, not 1. Note that this is a limitation of floating-point arithmetic in general, not a limitation of PostgreSQL.

## <span id="page-199-0"></span>**38.12.2. Polymorphic and Variadic Aggregates**

Aggregate functions can use polymorphic state transition functions or final functions, so that the same functions can be used to implement multiple aggregates. See [Section 38.2.5](#page-151-2) for an explanation of polymorphic functions. Going a step further, the aggregate function itself can be specified with polymorphic input type(s) and state type, allowing a single aggregate definition to serve for multiple input data types. Here is an example of a polymorphic aggregate:

```
CREATE AGGREGATE array_accum (anycompatible)
(
 sfunc = array_append,
 stype = anycompatiblearray,
 initcond = '{}'
);
```

Here, the actual state type for any given aggregate call is the array type having the actual input type as elements. The behavior of the aggregate is to concatenate all the inputs into an array of that type. (Note:

the built-in aggregate array\_agg provides similar functionality, with better performance than this definition would have.)

Here's the output using two different actual data types as arguments:

```
SELECT attrelid::regclass, array_accum(attname)
 FROM pg_attribute
 WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
 GROUP BY attrelid;
 attrelid | array_accum 
---------------+---------------------------------------
 pg_tablespace | {spcname,spcowner,spcacl,spcoptions}
(1 row)
SELECT attrelid::regclass, array_accum(atttypid::regtype)
 FROM pg_attribute
 WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
 GROUP BY attrelid;
 attrelid | array_accum 
---------------+---------------------------
 pg_tablespace | {name,oid,aclitem[],text[]}
(1 row)
```

Ordinarily, an aggregate function with a polymorphic result type has a polymorphic state type, as in the above example. This is necessary because otherwise the final function cannot be declared sensibly: it would need to have a polymorphic result type but no polymorphic argument type, which CREATE FUNCTION will reject on the grounds that the result type cannot be deduced from a call. But sometimes it is inconvenient to use a polymorphic state type. The most common case is where the aggregate support functions are to be written in C and the state type should be declared as internal because there is no SQL-level equivalent for it. To address this case, it is possible to declare the final function as taking extra "dummy" arguments that match the input arguments of the aggregate. Such dummy arguments are always passed as null values since no specific value is available when the final function is called. Their only use is to allow a polymorphic final function's result type to be connected to the aggregate's input type(s). For example, the definition of the built-in aggregate array\_agg is equivalent to

```
CREATE FUNCTION array_agg_transfn(internal, anynonarray)
 RETURNS internal ...;
CREATE FUNCTION array_agg_finalfn(internal, anynonarray)
 RETURNS anyarray ...;
CREATE AGGREGATE array_agg (anynonarray)
(
 sfunc = array_agg_transfn,
 stype = internal,
 finalfunc = array_agg_finalfn,
 finalfunc_extra
);
```

Here, the finalfunc\_extra option specifies that the final function receives, in addition to the state value, extra dummy argument(s) corresponding to the aggregate's input argument(s). The extra anynonarray argument allows the declaration of array\_agg\_finalfn to be valid.

An aggregate function can be made to accept a varying number of arguments by declaring its last argument as a VARIADIC array, in much the same fashion as for regular functions; see Section 38.5.6. The aggregate's transition function(s) must have the same array type as their last argument. The transition function(s) typically would also be marked VARIADIC, but this is not strictly required.

#### **Note**

Variadic aggregates are easily misused in connection with the ORDER BY option (see Section 4.2.7), since the parser cannot tell whether the wrong number of actual arguments have been given in such a combination. Keep in mind that everything to the right of ORDER BY is a sort key, not an argument to the aggregate. For example, in

```
SELECT myaggregate(a ORDER BY a, b, c) FROM ...
```

the parser will see this as a single aggregate function argument and three sort keys. However, the user might have intended

```
SELECT myaggregate(a, b, c ORDER BY a) FROM ...
```

If myaggregate is variadic, both these calls could be perfectly valid.

For the same reason, it's wise to think twice before creating aggregate functions with the same names and different numbers of regular arguments.

### **38.12.3. Ordered-Set Aggregates**

The aggregates we have been describing so far are "normal" aggregates. PostgreSQL also supports *ordered-set aggregates*, which differ from normal aggregates in two key ways. First, in addition to ordinary aggregated arguments that are evaluated once per input row, an ordered-set aggregate can have "direct" arguments that are evaluated only once per aggregation operation. Second, the syntax for the ordinary aggregated arguments specifies a sort ordering for them explicitly. An ordered-set aggregate is usually used to implement a computation that depends on a specific row ordering, for instance rank or percentile, so that the sort ordering is a required aspect of any call. For example, the built-in definition of percentile\_disc is equivalent to:

```
CREATE FUNCTION ordered_set_transition(internal, anyelement)
 RETURNS internal ...;
CREATE FUNCTION percentile_disc_final(internal, float8, anyelement)
 RETURNS anyelement ...;
CREATE AGGREGATE percentile_disc (float8 ORDER BY anyelement)
(
 sfunc = ordered_set_transition,
 stype = internal,
 finalfunc = percentile_disc_final,
 finalfunc_extra
);
```

This aggregate takes a float8 direct argument (the percentile fraction) and an aggregated input that can be of any sortable data type. It could be used to obtain a median household income like this:

```
SELECT percentile_disc(0.5) WITHIN GROUP (ORDER BY income) FROM
 households;
 percentile_disc
```

----------------- 50489

Here, 0.5 is a direct argument; it would make no sense for the percentile fraction to be a value varying across rows.

Unlike the case for normal aggregates, the sorting of input rows for an ordered-set aggregate is *not* done behind the scenes, but is the responsibility of the aggregate's support functions. The typical implementation approach is to keep a reference to a "tuplesort" object in the aggregate's state value, feed the incoming rows into that object, and then complete the sorting and read out the data in the final function. This design allows the final function to perform special operations such as injecting additional "hypothetical" rows into the data to be sorted. While normal aggregates can often be implemented with support functions written in PL/pgSQL or another PL language, ordered-set aggregates generally have to be written in C, since their state values aren't definable as any SQL data type. (In the above example, notice that the state value is declared as type internal — this is typical.) Also, because the final function performs the sort, it is not possible to continue adding input rows by executing the transition function again later. This means the final function is not READ\_ONLY; it must be declared in CREATE AGGREGATE as READ\_WRITE, or as SHAREABLE if it's possible for additional final-function calls to make use of the already-sorted state.

The state transition function for an ordered-set aggregate receives the current state value plus the aggregated input values for each row, and returns the updated state value. This is the same definition as for normal aggregates, but note that the direct arguments (if any) are not provided. The final function receives the last state value, the values of the direct arguments if any, and (if finalfunc\_extra is specified) null values corresponding to the aggregated input(s). As with normal aggregates, finalfunc\_extra is only really useful if the aggregate is polymorphic; then the extra dummy argument(s) are needed to connect the final function's result type to the aggregate's input type(s).

Currently, ordered-set aggregates cannot be used as window functions, and therefore there is no need for them to support moving-aggregate mode.

### **38.12.4. Partial Aggregation**

Optionally, an aggregate function can support *partial aggregation*. The idea of partial aggregation is to run the aggregate's state transition function over different subsets of the input data independently, and then to combine the state values resulting from those subsets to produce the same state value that would have resulted from scanning all the input in a single operation. This mode can be used for parallel aggregation by having different worker processes scan different portions of a table. Each worker produces a partial state value, and at the end those state values are combined to produce a final state value. (In the future this mode might also be used for purposes such as combining aggregations over local and remote tables; but that is not implemented yet.)

To support partial aggregation, the aggregate definition must provide a *combine function*, which takes two values of the aggregate's state type (representing the results of aggregating over two subsets of the input rows) and produces a new value of the state type, representing what the state would have been after aggregating over the combination of those sets of rows. It is unspecified what the relative order of the input rows from the two sets would have been. This means that it's usually impossible to define a useful combine function for aggregates that are sensitive to input row order.

As simple examples, MAX and MIN aggregates can be made to support partial aggregation by specifying the combine function as the same greater-of-two or lesser-of-two comparison function that is used as their transition function. SUM aggregates just need an addition function as combine function. (Again, this is the same as their transition function, unless the state value is wider than the input data type.)

The combine function is treated much like a transition function that happens to take a value of the state type, not of the underlying input type, as its second argument. In particular, the rules for dealing with null values and strict functions are similar. Also, if the aggregate definition specifies a non-null initcond, keep in mind that that will be used not only as the initial state for each partial aggregation run, but also as the initial state for the combine function, which will be called to combine each partial result into that state.

If the aggregate's state type is declared as internal, it is the combine function's responsibility that its result is allocated in the correct memory context for aggregate state values. This means in particular that when the first input is NULL it's invalid to simply return the second input, as that value will be in the wrong context and will not have sufficient lifespan.

When the aggregate's state type is declared as internal, it is usually also appropriate for the aggregate definition to provide a *serialization function* and a *deserialization function*, which allow such a state value to be copied from one process to another. Without these functions, parallel aggregation cannot be performed, and future applications such as local/remote aggregation will probably not work either.

A serialization function must take a single argument of type internal and return a result of type bytea, which represents the state value packaged up into a flat blob of bytes. Conversely, a deserialization function reverses that conversion. It must take two arguments of types bytea and internal, and return a result of type internal. (The second argument is unused and is always zero, but it is required for type-safety reasons.) The result of the deserialization function should simply be allocated in the current memory context, as unlike the combine function's result, it is not long-lived.

Worth noting also is that for an aggregate to be executed in parallel, the aggregate itself must be marked PARALLEL SAFE. The parallel-safety markings on its support functions are not consulted.

### **38.12.5. Support Functions for Aggregates**

A function written in C can detect that it is being called as an aggregate support function by calling AggCheckCallContext, for example:

```
if (AggCheckCallContext(fcinfo, NULL))
```

One reason for checking this is that when it is true, the first input must be a temporary state value and can therefore safely be modified in-place rather than allocating a new copy. See int8inc() for an example. (While aggregate transition functions are always allowed to modify the transition value inplace, aggregate final functions are generally discouraged from doing so; if they do so, the behavior must be declared when creating the aggregate. See CREATE AGGREGATE for more detail.)

The second argument of AggCheckCallContext can be used to retrieve the memory context in which aggregate state values are being kept. This is useful for transition functions that wish to use "expanded" objects (see [Section 38.13.1\)](#page-6-0) as their state values. On first call, the transition function should return an expanded object whose memory context is a child of the aggregate state context, and then keep returning the same expanded object on subsequent calls. See array\_append() for an example. (array\_append() is not the transition function of any built-in aggregate, but it is written to behave efficiently when used as transition function of a custom aggregate.)

Another support routine available to aggregate functions written in C is AggGetAggref, which returns the Aggref parse node that defines the aggregate call. This is mainly useful for ordered-set aggregates, which can inspect the substructure of the Aggref node to find out what sort ordering they are supposed to implement. Examples can be found in orderedsetaggs.c in the PostgreSQL source code.

## <span id="page-3-0"></span>**38.13. User-Defined Types**

As described in Section 38.2, PostgreSQL can be extended to support new data types. This section describes how to define new base types, which are data types defined below the level of the SQL language. Creating a new base type requires implementing functions to operate on the type in a lowlevel language, usually C.

The examples in this section can be found in complex.sql and complex.c in the src/tutorial directory of the source distribution. See the README file in that directory for instructions about running the examples.

 A user-defined type must always have input and output functions. These functions determine how the type appears in strings (for input by the user and output to the user) and how the type is organized in memory. The input function takes a null-terminated character string as its argument and returns the internal (in memory) representation of the type. The output function takes the internal representation of the type as argument and returns a null-terminated character string. If we want to do anything more with the type than merely store it, we must provide additional functions to implement whatever operations we'd like to have for the type.

Suppose we want to define a type complex that represents complex numbers. A natural way to represent a complex number in memory would be the following C structure:

```
typedef struct Complex {
 double x;
 double y;
} Complex;
```

We will need to make this a pass-by-reference type, since it's too large to fit into a single Datum value.

As the external string representation of the type, we choose a string of the form (x,y).

The input and output functions are usually not hard to write, especially the output function. But when defining the external string representation of the type, remember that you must eventually write a complete and robust parser for that representation as your input function. For instance:

```
PG_FUNCTION_INFO_V1(complex_in);
Datum
complex_in(PG_FUNCTION_ARGS)
{
 char *str = PG_GETARG_CSTRING(0);
 double x,
 y;
 Complex *result;
 if (sscanf(str, " ( %lf , %lf )", &x, &y) != 2)
 ereport(ERROR,
 (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
 errmsg("invalid input syntax for type %s: \"%s\"",
 "complex", str)));
 result = (Complex *) palloc(sizeof(Complex));
 result->x = x;
 result->y = y;
 PG_RETURN_POINTER(result);
}
```

The output function can simply be:

```
PG_FUNCTION_INFO_V1(complex_out);
Datum
complex_out(PG_FUNCTION_ARGS)
```

```
{
 Complex *complex = (Complex *) PG_GETARG_POINTER(0);
 char *result;
 result = psprintf("(%g,%g)", complex->x, complex->y);
 PG_RETURN_CSTRING(result);
}
```

You should be careful to make the input and output functions inverses of each other. If you do not, you will have severe problems when you need to dump your data into a file and then read it back in. This is a particularly common problem when floating-point numbers are involved.

Optionally, a user-defined type can provide binary input and output routines. Binary I/O is normally faster but less portable than textual I/O. As with textual I/O, it is up to you to define exactly what the external binary representation is. Most of the built-in data types try to provide a machine-independent binary representation. For complex, we will piggy-back on the binary I/O converters for type float8:

```
PG_FUNCTION_INFO_V1(complex_recv);
Datum
complex_recv(PG_FUNCTION_ARGS)
{
 StringInfo buf = (StringInfo) PG_GETARG_POINTER(0);
 Complex *result;
 result = (Complex *) palloc(sizeof(Complex));
 result->x = pq_getmsgfloat8(buf);
 result->y = pq_getmsgfloat8(buf);
 PG_RETURN_POINTER(result);
}
PG_FUNCTION_INFO_V1(complex_send);
Datum
complex_send(PG_FUNCTION_ARGS)
{
 Complex *complex = (Complex *) PG_GETARG_POINTER(0);
 StringInfoData buf;
 pq_begintypsend(&buf);
 pq_sendfloat8(&buf, complex->x);
 pq_sendfloat8(&buf, complex->y);
 PG_RETURN_BYTEA_P(pq_endtypsend(&buf));
}
```

Once we have written the I/O functions and compiled them into a shared library, we can define the complex type in SQL. First we declare it as a shell type:

```
CREATE TYPE complex;
```

This serves as a placeholder that allows us to reference the type while defining its I/O functions. Now we can define the I/O functions:

```
CREATE FUNCTION complex_in(cstring)
 RETURNS complex
 AS 'filename'
 LANGUAGE C IMMUTABLE STRICT;
CREATE FUNCTION complex_out(complex)
 RETURNS cstring
 AS 'filename'
 LANGUAGE C IMMUTABLE STRICT;
CREATE FUNCTION complex_recv(internal)
 RETURNS complex
 AS 'filename'
 LANGUAGE C IMMUTABLE STRICT;
CREATE FUNCTION complex_send(complex)
 RETURNS bytea
 AS 'filename'
 LANGUAGE C IMMUTABLE STRICT;
```

Finally, we can provide the full definition of the data type:

```
CREATE TYPE complex (
 internallength = 16,
 input = complex_in,
 output = complex_out,
 receive = complex_recv,
 send = complex_send,
 alignment = double
);
```

 When you define a new base type, PostgreSQL automatically provides support for arrays of that type. The array type typically has the same name as the base type with the underscore character (\_) prepended.

Once the data type exists, we can declare additional functions to provide useful operations on the data type. Operators can then be defined atop the functions, and if needed, operator classes can be created to support indexing of the data type. These additional layers are discussed in following sections.

If the internal representation of the data type is variable-length, the internal representation must follow the standard layout for variable-length data: the first four bytes must be a char[4] field which is never accessed directly (customarily named vl\_len\_). You must use the SET\_VARSIZE() macro to store the total size of the datum (including the length field itself) in this field and VARSIZE() to retrieve it. (These macros exist because the length field may be encoded depending on platform.)

For further details see the description of the CREATE TYPE command.

### <span id="page-6-0"></span>**38.13.1. TOAST Considerations**

If the values of your data type vary in size (in internal form), it's usually desirable to make the data type TOAST-able (see Section 70.2). You should do this even if the values are always too small to be compressed or stored externally, because TOAST can save space on small data too, by reducing header overhead.

To support TOAST storage, the C functions operating on the data type must always be careful to unpack any toasted values they are handed by using PG\_DETOAST\_DATUM. (This detail is customarily hidden by defining type-specific GETARG\_DATATYPE\_P macros.) Then, when running the CREATE TYPE command, specify the internal length as variable and select some appropriate storage option other than plain.

If data alignment is unimportant (either just for a specific function or because the data type specifies byte alignment anyway) then it's possible to avoid some of the overhead of PG\_DETOAST\_DA-TUM. You can use PG\_DETOAST\_DATUM\_PACKED instead (customarily hidden by defining a GETARG\_DATATYPE\_PP macro) and using the macros VARSIZE\_ANY\_EXHDR and VARDA-TA\_ANY to access a potentially-packed datum. Again, the data returned by these macros is not aligned even if the data type definition specifies an alignment. If the alignment is important you must go through the regular PG\_DETOAST\_DATUM interface.

#### **Note**

Older code frequently declares vl\_len\_ as an int32 field instead of char[4]. This is OK as long as the struct definition has other fields that have at least int32 alignment. But it is dangerous to use such a struct definition when working with a potentially unaligned datum; the compiler may take it as license to assume the datum actually is aligned, leading to core dumps on architectures that are strict about alignment.

Another feature that's enabled by TOAST support is the possibility of having an *expanded* in-memory data representation that is more convenient to work with than the format that is stored on disk. The regular or "flat" varlena storage format is ultimately just a blob of bytes; it cannot for example contain pointers, since it may get copied to other locations in memory. For complex data types, the flat format may be quite expensive to work with, so PostgreSQL provides a way to "expand" the flat format into a representation that is more suited to computation, and then pass that format in-memory between functions of the data type.

To use expanded storage, a data type must define an expanded format that follows the rules given in src/include/utils/expandeddatum.h, and provide functions to "expand" a flat varlena value into expanded format and "flatten" the expanded format back to the regular varlena representation. Then ensure that all C functions for the data type can accept either representation, possibly by converting one into the other immediately upon receipt. This does not require fixing all existing functions for the data type at once, because the standard PG\_DETOAST\_DATUM macro is defined to convert expanded inputs into regular flat format. Therefore, existing functions that work with the flat varlena format will continue to work, though slightly inefficiently, with expanded inputs; they need not be converted until and unless better performance is important.

C functions that know how to work with an expanded representation typically fall into two categories: those that can only handle expanded format, and those that can handle either expanded or flat varlena inputs. The former are easier to write but may be less efficient overall, because converting a flat input to expanded form for use by a single function may cost more than is saved by operating on the expanded format. When only expanded format need be handled, conversion of flat inputs to expanded form can be hidden inside an argument-fetching macro, so that the function appears no more complex than one working with traditional varlena input. To handle both types of input, write an argument-fetching function that will detoast external, short-header, and compressed varlena inputs, but not expanded inputs. Such a function can be defined as returning a pointer to a union of the flat varlena format and the expanded format. Callers can use the VARATT\_IS\_EXPANDED\_HEADER() macro to determine which format they received.

The TOAST infrastructure not only allows regular varlena values to be distinguished from expanded values, but also distinguishes "read-write" and "read-only" pointers to expanded values. C functions that only need to examine an expanded value, or will only change it in safe and non-semantically-visible ways, need not care which type of pointer they receive. C functions that produce a modified version of an input value are allowed to modify an expanded input value in-place if they receive a read-write pointer, but must not modify the input if they receive a read-only pointer; in that case they have to copy the value first, producing a new value to modify. A C function that has constructed a new expanded value should always return a read-write pointer to it. Also, a C function that is modifying a read-write expanded value in-place should take care to leave the value in a sane state if it fails partway through.

For examples of working with expanded values, see the standard array infrastructure, particularly src/backend/utils/adt/array\_expanded.c.

## <span id="page-8-0"></span>**38.14. User-Defined Operators**

Every operator is "syntactic sugar" for a call to an underlying function that does the real work; so you must first create the underlying function before you can create the operator. However, an operator is *not merely* syntactic sugar, because it carries additional information that helps the query planner optimize queries that use the operator. The next section will be devoted to explaining that additional information.

PostgreSQL supports prefix and infix operators. Operators can be overloaded; that is, the same operator name can be used for different operators that have different numbers and types of operands. When a query is executed, the system determines the operator to call from the number and types of the provided operands.

Here is an example of creating an operator for adding two complex numbers. We assume we've already created the definition of type complex (see [Section 38.13\)](#page-3-0). First we need a function that does the work, then we can define the operator:

```
CREATE FUNCTION complex_add(complex, complex)
 RETURNS complex
 AS 'filename', 'complex_add'
 LANGUAGE C IMMUTABLE STRICT;
CREATE OPERATOR + (
 leftarg = complex,
 rightarg = complex,
 function = complex_add,
 commutator = +
);
Now we could execute a query like this:
SELECT (a + b) AS c FROM test_complex;
 c
-----------------
 (5.2,6.05)
```

(133.42,144.95)

We've shown how to create a binary operator here. To create a prefix operator, just omit the leftarg. The function clause and the argument clauses are the only required items in CREATE OPERATOR. The commutator clause shown in the example is an optional hint to the query optimizer. Further details about commutator and other optimizer hints appear in the next section.