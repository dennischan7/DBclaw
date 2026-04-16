---
source: MySQL 8.4 Reference
title: 00_Overview
---

The audit\_api\_message\_emit component enables applications to add their own message events to the audit log, using the [audit\\_api\\_message\\_emit\\_udf\(\)](#page-147-0) function.

The audit\_api\_message\_emit component cooperates with all plugins of audit type. For concreteness, examples use the audit\_log plugin described in [Section 8.4.5, "MySQL Enterprise](#page-63-1) [Audit"](#page-63-1).

- [Installing or Uninstalling the Audit Message Component](#page-147-1)
- [Audit Message Function](#page-147-2)

## <span id="page-147-1"></span>**Installing or Uninstalling the Audit Message Component**

To be usable by the server, the component library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To install the audit\_api\_message\_emit component, use this statement:

```
INSTALL COMPONENT "file://component_audit_api_message_emit";
```

Component installation is a one-time operation that need not be done per server startup. INSTALL COMPONENT loads the component, and also registers it in the mysql.component system table to cause it to be loaded during subsequent server startups.

To uninstall the audit\_api\_message\_emit component, use this statement:

```
UNINSTALL COMPONENT "file://component_audit_api_message_emit";
```

UNINSTALL COMPONENT unloads the component, and unregisters it from the mysql.component system table to cause it not to be loaded during subsequent server startups.

Because installing and uninstalling the audit\_api\_message\_emit component installs and uninstalls the [audit\\_api\\_message\\_emit\\_udf\(\)](#page-147-0) function that the component implements, it is not necessary to use CREATE FUNCTION or DROP FUNCTION to do so.

## <span id="page-147-2"></span>**Audit Message Function**

This section describes the [audit\\_api\\_message\\_emit\\_udf\(\)](#page-147-0) function implemented by the audit\_api\_message\_emit component.

Before using the audit message function, install the audit message component according to the instructions provided at [Installing or Uninstalling the Audit Message Component](#page-147-1).

<span id="page-147-0"></span>• [audit\\_api\\_message\\_emit\\_udf\(](#page-147-0)component, producer, message[, key, value] ...)

Adds a message event to the audit log. Message events include component, producer, and message strings of the caller's choosing, and optionally a set of key-value pairs.

An event posted by this function is sent to all enabled plugins of audit type, each of which handles the event according to its own rules. If no plugin of audit type is enabled, posting the event has no effect.

## Arguments:

- component: A string that specifies a component name.
- producer: A string that specifies a producer name.
- message: A string that specifies the event message.
- key, value: Events may include 0 or more key-value pairs that specify an arbitrary applicationprovided data map. Each key argument is a string that specifies a name for its immediately following value argument. Each value argument specifies a value for its immediately following key argument. Each value can be a string or numeric value, or NULL.

## Return value:

The string OK to indicate success. An error occurs if the function fails.

```
mysql> SELECT audit_api_message_emit_udf('component_text',
 'producer_text',
                                   'message_text',
                                   'key1', 'value1',
                                   'key2', 123,
                                   'key3', NULL) AS 'Message';
+---------+
| Message |
+---------+
| OK |
+---------+
```

#### Additional information:

Each audit plugin that receives an event posted by [audit\\_api\\_message\\_emit\\_udf\(\)](#page-147-0) logs the event in plugin-specific format. For example, the audit\_log plugin (see [Section 8.4.5, "MySQL](#page-63-1) [Enterprise Audit"](#page-63-1)) logs message values as follows, depending on the log format configured by the [audit\\_log\\_format](#page-138-0) system variable:

• JSON format ([audit\\_log\\_format=JSON](#page-138-0)):

```
{
 ...
 "class": "message",
 "event": "user",
 ...
 "message_data": {
 "component": "component_text",
 "producer": "producer_text",
 "message": "message_text",
 "map": {
 "key1": "value1",
 "key2": 123,
 "key3": null
 }
 }
}
```

• New-style XML format ([audit\\_log\\_format=NEW](#page-138-0)):

```
<AUDIT_RECORD>
 ...
 <NAME>Message</NAME>
 ...
 <COMMAND_CLASS>user</COMMAND_CLASS>
 <COMPONENT>component_text</COMPONENT>
 <PRODUCER>producer_text</PRODUCER>
 <MESSAGE>message_text</MESSAGE>
 <MAP>
 <ELEMENT>
 <KEY>key1</KEY>
 <VALUE>value1</VALUE>
 </ELEMENT>
 <ELEMENT>
 <KEY>key2</KEY>
 <VALUE>123</VALUE>
 </ELEMENT>
 <ELEMENT>
 <KEY>key3</KEY>
 <VALUE/>
 </ELEMENT>
 </MAP>
</AUDIT_RECORD>
```

• Old-style XML format ([audit\\_log\\_format=OLD](#page-138-0)):

```
<AUDIT_RECORD
 ...
 NAME="Message"
```

```
 ...
 COMMAND_CLASS="user"
 COMPONENT="component_text"
 PRODUCER="producer_text"
 MESSAGE="message_text"/>
```

![](_page_149_Picture_2.jpeg)

#### **Note**

Message events logged in old-style XML format do not include the keyvalue map due to representational constraints imposed by this format.

Messages posted by [audit\\_api\\_message\\_emit\\_udf\(\)](#page-147-0) have an event class of MYSQL\_AUDIT\_MESSAGE\_CLASS and a subclass of MYSQL\_AUDIT\_MESSAGE\_USER. (Internally generated audit messages have the same class and a subclass of MYSQL\_AUDIT\_MESSAGE\_INTERNAL; this subclass currently is unused.) To refer to such events in audit\_log filtering rules, use a class element with a name value of message. For example:

```
{
 "filter": {
 "class": {
 "name": "message"
 }
 }
}
```

Should it be necessary to distinguish user-generated and internally generated message events, test the subclass value against user or internal.

Filtering based on the contents of the key-value map is not supported.

For information about writing filtering rules, see [Section 8.4.5.7, "Audit Log Filtering"](#page-100-0).