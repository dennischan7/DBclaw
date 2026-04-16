---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following table lists the most common NDB cluster log messages. For information about the cluster log, log events, and event types, see [Section 25.6.3, "Event Reports Generated in NDB Cluster".](#page-66-0) These log messages also correspond to log event types in the MGM API; see [The Ndb\\_logevent\\_type Type,](https://dev.mysql.com/doc/ndbapi/en/mgm-types.md#mgm-ndb-logevent-type) for related information of interest to Cluster API developers.

**Table 25.53 Common NDB cluster log messages**

| Log Message                                                                | Description                                                                                                                                                                                                 | Event Name                     | Event Type | Priority | Severity |
|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|------------|----------|----------|
| Node<br>mgm_node_id:<br>Node<br>data_node_id<br>Connected                  | The data node<br>having node<br>ID node_id<br>has connected<br>to the<br>management<br>server (node<br>mgm_node_id).                                                                                        | Connected                      | Connection | 8        | INFO     |
| Node<br>mgm_node_id:<br>Node<br>data_node_id<br>Disconnected               | The data node<br>having node ID<br>data_node_id<br>has<br>disconnected<br>from the<br>management<br>server (node<br>mgm_node_id).                                                                           | Disconnected Connection        |            | 8        | ALERT    |
| Node<br>data_node_id:<br>Communication<br>to Node<br>api_node_id<br>closed | The API node<br>or SQL node<br>having node ID<br>api_node_id<br>is no longer<br>communicating<br>with data node<br>data_node_id.                                                                            | CommunicationClosed Connection |            | 8        | INFO     |
| Node<br>data_node_id:<br>Communication<br>to Node<br>api_node_id<br>opened | The API node<br>or SQL node<br>having node ID<br>api_node_id<br>is now<br>communicating<br>with data node<br>data_node_id.                                                                                  | CommunicationOpened Connection |            | 8        | INFO     |
| Node<br>mgm_node_id:<br>Node<br>api_node_id:<br>API version                | The API node<br>having node ID<br>api_node_id<br>has connected<br>to management<br>node<br>mgm_node_id<br>using NDB<br>API version<br>version<br>(generally the<br>same as the<br>MySQL version<br>number). | ConnectedApiVersion Connection |            | 8        | INFO     |
| Node<br>node_id:<br>Global<br>checkpoint<br>gci started                    | A global<br>checkpoint with<br>the ID gci has<br>been started;<br>node node_id<br>is the master                                                                                                             | GlobalCheckpointStarted        | Checkpoint | 9        | INFO     |

| Log Message                                                                                                                         | Description                                                                                                                                                                                                                                                                       | Event Name               | Event Type                              | Priority | Severity |
|-------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|-----------------------------------------|----------|----------|
|                                                                                                                                     | responsible<br>for this global<br>checkpoint.                                                                                                                                                                                                                                     |                          |                                         |          |          |
| Node<br>node_id:<br>Global<br>checkpoint<br>gci<br>completed                                                                        | The global<br>checkpoint<br>having the ID<br>gci has been<br>completed;<br>node node_id<br>was the master<br>responsible<br>for this global<br>checkpoint.                                                                                                                        |                          | GlobalCheckpointCompleted<br>Checkpoint | 10       | INFO     |
| Node<br>node_id:<br>Local<br>checkpoint<br>lcp<br>started.<br>Keep GCI =<br>current_gci<br>oldest<br>restorable<br>GCI =<br>old_gci | The local<br>checkpoint<br>having<br>sequence ID<br>lcp has been<br>started on node<br>node_id. The<br>most recent<br>GCI that can<br>be used has<br>the index<br>current_gci,<br>and the oldest<br>GCI from which<br>the cluster can<br>be restored<br>has the index<br>old_gci. | LocalCheckpointStarted   | Checkpoint                              | 7        | INFO     |
| Node<br>node_id:<br>Local<br>checkpoint<br>lcp<br>completed                                                                         | The local<br>checkpoint<br>having<br>sequence ID<br>lcp on node<br>node_id<br>has been<br>completed.                                                                                                                                                                              | LocalCheckpointCompleted | Checkpoint                              | 8        | INFO     |
| Node<br>node_id:<br>Local<br>Checkpoint<br>stopped in<br>CALCULATED_KEEP_GCI                                                        | The node<br>was unable to<br>determine the<br>most recent<br>usable GCI.                                                                                                                                                                                                          | LCPStoppedInCalcKeepGci  | Checkpoint                              | 0        | ALERT    |
| Node<br>node_id:<br>Table ID =<br>table_id,<br>fragment<br>ID =<br>fragment_id<br>has<br>completed                                  | A table<br>fragment<br>has been<br>checkpointed<br>to disk on node<br>node_id. The<br>GCI in progress<br>has the index<br>started_gci,                                                                                                                                            | LCPFragmentCompleted     | Checkpoint                              | 11       | INFO     |

| Log Message                                                                                  | Description                                                                                                                                                                                                                                                                       | Event Name                  | Event Type | Priority | Severity |
|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|------------|----------|----------|
| LCP on Node<br>node_id<br>maxGciStarted:<br>started_gci<br>maxGciCompleted:<br>completed_gci | and the most<br>recent GCI<br>to have been<br>completed<br>has the index<br>completed_gci.                                                                                                                                                                                        |                             |            |          |          |
| Node<br>node_id:<br>ACC Blocked<br>num_1 and<br>TUP Blocked<br>num_2 times<br>last second    | Undo logging<br>is blocked<br>because the log<br>buffer is close<br>to overflowing.                                                                                                                                                                                               | UndoLogBlockedCheckpoint    |            | 7        | INFO     |
| Node<br>node_id:<br>Start<br>initiated<br>version                                            | Data node<br>node_id,<br>running<br>NDB version<br>version, is<br>beginning its<br>startup process.                                                                                                                                                                               | NDBStartStarted StartUp     |            | 1        | INFO     |
| Node<br>node_id:<br>Started<br>version                                                       | Data node<br>node_id,<br>running<br>NDB version<br>version,<br>has started<br>successfully.                                                                                                                                                                                       | NDBStartCompleted StartUp   |            | 1        | INFO     |
| Node<br>node_id:<br>STTORRY<br>received<br>after<br>restart<br>finished                      | The node has<br>received a<br>signal indicating<br>that a cluster<br>restart has<br>completed.                                                                                                                                                                                    | STTORRYRecieved StartUp     |            | 15       | INFO     |
| Node<br>node_id:<br>Start<br>phase phase<br>completed<br>(type)                              | The node has<br>completed<br>start phase<br>phase of a<br>type start. For<br>a listing of start<br>phases, see<br>Section 25.6.4,<br>"Summary of<br>NDB Cluster<br>Start Phases".<br>(type is one<br>of initial,<br>system, node,<br>initial<br>node, or<br><unknown>.)</unknown> | StartPhaseCompleted StartUp |            | 4        | INFO     |
| Node<br>node_id:<br>CM_REGCONF                                                               | Node<br>president_id<br>has been                                                                                                                                                                                                                                                  | CM_REGCONF                  | StartUp    | 3        | INFO     |

| Log Message                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                  | Event Name              | Event Type | Priority | Severity |
|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|------------|----------|----------|
| president =<br>president_id,<br>own Node<br>= own_id,<br>our dynamic<br>id =<br>dynamic_id                                                           | selected as<br>"president".<br>own_id and<br>dynamic_id<br>should always<br>be the same<br>as the ID<br>(node_id) of<br>the reporting<br>node.                                                                                                                                                               |                         |            |          |          |
| Node<br>node_id:<br>CM_REGREF<br>from Node<br>president_id<br>to our Node<br>node_id.<br>Cause =<br>cause                                            | The reporting<br>node (ID<br>node_id)<br>was unable to<br>accept node<br>president_id<br>as president.<br>The cause of<br>the problem<br>is given as<br>one of Busy,<br>Election<br>with wait<br>= false, Not<br>president,<br>Election<br>without<br>selecting<br>new<br>candidate,<br>or No such<br>cause. | CM_REGREF               | StartUp    | 8        | INFO     |
| Node<br>node_id:<br>We are Node<br>own_id with<br>dynamic ID<br>dynamic_id,<br>our left<br>neighbor is<br>Node id_1,<br>our right<br>is Node<br>id_2 | The node has<br>discovered its<br>neighboring<br>nodes in the<br>cluster (node<br>id_1 and<br>node id_2).<br>node_id,<br>own_id, and<br>dynamic_id<br>should always<br>be the same;<br>if they are not,<br>this indicates<br>a serious<br>misconfiguration<br>of the cluster<br>nodes.                       | FIND_NEIGHBOURS StartUp |            | 8        | INFO     |
| Node<br>node_id:<br>type<br>shutdown<br>initiated                                                                                                    | The node<br>has received<br>a shutdown<br>signal. The<br>type of                                                                                                                                                                                                                                             | NDBStopStartedStartUp   |            | 1        | INFO     |

| Log Message                    | Description                                                         | Event Name               | Event Type | Priority | Severity |
|--------------------------------|---------------------------------------------------------------------|--------------------------|------------|----------|----------|
|                                | shutdown is                                                         |                          |            |          |          |
|                                | either Cluster                                                      |                          |            |          |          |
|                                | or Node.                                                            |                          |            |          |          |
| Node                           | The node                                                            | NDBStopCompleted StartUp |            | 1        | INFO     |
| node_id:<br>Node               | has been<br>shut down.                                              |                          |            |          |          |
| shutdown                       | This report                                                         |                          |            |          |          |
| completed                      | may include                                                         |                          |            |          |          |
| [, action]                     | an action,                                                          |                          |            |          |          |
| [Initiated                     | which if present                                                    |                          |            |          |          |
| by signal                      | is one of                                                           |                          |            |          |          |
| signal.]                       | restarting,                                                         |                          |            |          |          |
|                                | no start,                                                           |                          |            |          |          |
|                                | or initial.<br>The report may                                       |                          |            |          |          |
|                                | also include a                                                      |                          |            |          |          |
|                                | reference to an                                                     |                          |            |          |          |
|                                | NDB Protocol                                                        |                          |            |          |          |
|                                | signal;                                                             |                          |            |          |          |
|                                | for possible                                                        |                          |            |          |          |
|                                | signals, refer to                                                   |                          |            |          |          |
|                                | Operations and                                                      |                          |            |          |          |
|                                | Signals.                                                            |                          |            |          |          |
| Node<br>node_id:               | The node has<br>been forcibly                                       | NDBStopForcedStartUp     |            | 1        | ALERT    |
| Forced node                    | shut down. The                                                      |                          |            |          |          |
| shutdown                       | action (one of                                                      |                          |            |          |          |
| completed                      | restarting,                                                         |                          |            |          |          |
| [, action].                    | no start,                                                           |                          |            |          |          |
| [Occurred                      | or initial)                                                         |                          |            |          |          |
| during                         | subsequently                                                        |                          |            |          |          |
| startphase<br>start_phase.]    | being taken,<br>if any, is also                                     |                          |            |          |          |
| [ Initiated                    | reported. If                                                        |                          |            |          |          |
| by signal.]                    | the shutdown                                                        |                          |            |          |          |
| [Caused                        | occurred while                                                      |                          |            |          |          |
| by error                       | the node                                                            |                          |            |          |          |
| error_code:                    | was starting,                                                       |                          |            |          |          |
|                                | the report<br>'error_message(error_classification).<br>includes the |                          |            |          |          |
| error_status'.<br>[(extra info | start_phase                                                         |                          |            |          |          |
| extra_code)]]                  | during which                                                        |                          |            |          |          |
|                                | the node failed.                                                    |                          |            |          |          |
|                                | If this was                                                         |                          |            |          |          |
|                                | a result of a                                                       |                          |            |          |          |
|                                | signal sent to                                                      |                          |            |          |          |
|                                | the node, this<br>information is                                    |                          |            |          |          |
|                                | also provided                                                       |                          |            |          |          |
|                                | (see Operations                                                     |                          |            |          |          |
|                                | and Signals,                                                        |                          |            |          |          |
|                                | for more                                                            |                          |            |          |          |
|                                | information).                                                       |                          |            |          |          |
|                                | If the error                                                        |                          |            |          |          |
|                                | causing the                                                         |                          |            |          |          |
|                                | failure is known,                                                   |                          |            |          |          |

| Log Message                                                                                                                | Description                                                                                                                                                                                                                                                                                                                                  | Event Name            | Event Type  | Priority | Severity |
|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|-------------|----------|----------|
|                                                                                                                            | this is also<br>included;<br>for more<br>information<br>about NDB error<br>messages and<br>classifications,<br>see NDB<br>Cluster API<br>Errors.                                                                                                                                                                                             |                       |             |          |          |
| Node<br>node_id:<br>Node<br>shutdown<br>aborted                                                                            | The node<br>shutdown<br>process was<br>aborted by the<br>user.                                                                                                                                                                                                                                                                               | NDBStopAbortedStartUp |             | 1        | INFO     |
| Node<br>node_id:<br>StartLog:<br>[GCI Keep:<br>keep_pos<br>LastCompleted:<br>last_pos<br>NewestRestorable:<br>restore_pos] | This reports<br>global<br>checkpoints<br>referenced<br>during a node<br>start. The redo<br>log prior to<br>keep_pos<br>is dropped.<br>last_pos is<br>the last global<br>checkpoint<br>in which data<br>node the<br>participated;<br>restore_pos<br>is the global<br>checkpoint<br>which is<br>actually used to<br>restore all data<br>nodes. | StartREDOLog StartUp  |             | 4        | INFO     |
| startup_message<br>[Listed<br>separately; see<br>below.]                                                                   | There are a<br>number of<br>possible startup<br>messages that<br>can be logged<br>under different<br>circumstances.<br>These are listed<br>separately; see<br>Section 25.6.2.2,<br>"NDB Cluster<br>Log Startup<br>Messages".                                                                                                                 | StartReport           | StartUp     | 4        | INFO     |
| Node<br>node_id:<br>Node<br>restart<br>completed                                                                           | Copying of<br>data dictionary<br>information to<br>the restarted                                                                                                                                                                                                                                                                             | NR_CopyDict           | NodeRestart | 8        | INFO     |

| Log Message                                                                                                                 | Description                                                                                       | Event Name                      | Event Type  | Priority | Severity |
|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------|-------------|----------|----------|
| copy of<br>dictionary<br>information                                                                                        | node has been<br>completed.                                                                       |                                 |             |          |          |
| Node<br>node_id:<br>Node<br>restart<br>completed<br>copy of<br>distribution<br>information                                  | Copying of data<br>distribution<br>information to<br>the restarted<br>node has been<br>completed. | NR_CopyDistr NodeRestart        |             | 8        | INFO     |
| Node<br>node_id:<br>Node<br>restart<br>starting<br>to copy the<br>fragments<br>to Node<br>node_id                           | Copy of<br>fragments to<br>starting data<br>node node_id<br>has begun                             | NR_CopyFragsStarted NodeRestart |             | 8        | INFO     |
| Node<br>node_id:<br>Table ID =<br>table_id,<br>fragment<br>ID =<br>fragment_id<br>have been<br>copied<br>to Node<br>node_id | Fragment<br>fragment_id<br>from table<br>table_id has<br>been copied<br>to data node<br>node_id   | NR_CopyFragDone NodeRestart     |             | 10       | INFO     |
| Node<br>node_id:<br>Node<br>restart<br>completed<br>copying the<br>fragments<br>to Node<br>node_id                          | Copying of all<br>table fragments<br>to restarting<br>data node<br>node_id has<br>been completed  | NR_CopyFragsCompleted           | NodeRestart | 8        | INFO     |
| Node<br>node_id:<br>Node<br>node1_id<br>completed<br>failure<br>of Node<br>node2_id                                         | Data node<br>node1_id<br>has detected<br>the failure of<br>data node<br>node2_id                  | NodeFailCompleted NodeRestart   |             | 8        | ALERT    |
| All nodes<br>completed<br>failure<br>of Node<br>node_id                                                                     | All (remaining)<br>data nodes<br>have detected<br>the failure of<br>data node<br>node_id          | NodeFailCompleted NodeRestart   |             | 8        | ALERT    |

| Log Message                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                        | Event Name                    | Event Type  | Priority | Severity |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|-------------|----------|----------|
| Node<br>failure of<br>node_idblock<br>completed                                                                                                                                                                                                                                                                      | The failure<br>of data node<br>node_id<br>has been<br>detected in<br>the blockNDB<br>kernel block,<br>where block<br>is 1 of DBTC,<br>DBDICT,<br>DBDIH,<br>or DBLQH;<br>for more<br>information, see<br>NDB Kernel<br>Blocks                                                                                                                                       | NodeFailCompleted NodeRestart |             | 8        | ALERT    |
| Node<br>mgm_node_id:<br>Node<br>data_node_id<br>has failed.<br>The Node<br>state at<br>failure was<br>state_code                                                                                                                                                                                                     | A data node<br>has failed. Its<br>state at the<br>time of failure<br>is described by<br>an arbitration<br>state code<br>state_code:<br>possible state<br>code values<br>can be found<br>in the file<br>include/<br>kernel/<br>signaldata/<br>ArbitSignalData.hpp.                                                                                                  | NODE_FAILREP NodeRestart      |             | 8        | ALERT    |
| President<br>restarts<br>arbitration<br>thread<br>[state=state_code]<br>or Prepare<br>arbitrator<br>node<br>node_id<br>[ticket=ticket_id]<br>or Receive<br>arbitrator<br>node<br>node_id<br>[ticket=ticket_id]<br>or Started<br>arbitrator<br>node<br>node_id<br>[ticket=ticket_id]<br>or Lost<br>arbitrator<br>node | This is a report<br>on the current<br>state and<br>progress of<br>arbitration in<br>the cluster.<br>node_id is the<br>node ID of the<br>management<br>node or<br>SQL node<br>selected as<br>the arbitrator.<br>state_code<br>is an arbitration<br>state code,<br>as found in<br>include/<br>kernel/<br>signaldata/<br>ArbitSignalData.hpp.<br>When an<br>error has | ArbitState                    | NodeRestart | 6        | INFO     |

| Log Message              | Description                  | Event Name  | Event Type  | Priority | Severity |
|--------------------------|------------------------------|-------------|-------------|----------|----------|
| node_id                  | occurred, an                 |             |             |          |          |
| - process                | error_message,               |             |             |          |          |
| failure                  | also defined in              |             |             |          |          |
| [state=state_code]       | ArbitSignalData.hpp,         |             |             |          |          |
| or Lost                  | is provided.                 |             |             |          |          |
| arbitrator               | ticket_id                    |             |             |          |          |
| node                     | is a unique                  |             |             |          |          |
| node_id                  | identifier                   |             |             |          |          |
| - process                | handed out by                |             |             |          |          |
| exit                     | the arbitrator               |             |             |          |          |
| [state=state_code]       | when it is                   |             |             |          |          |
| or Lost                  | selected to all              |             |             |          |          |
| arbitrator               | the nodes that               |             |             |          |          |
| node                     | participated in              |             |             |          |          |
| node_id -                | its selection;               |             |             |          |          |
| error_message            | this is used to              |             |             |          |          |
| [state=state_code]       | ensure that                  |             |             |          |          |
|                          | each node                    |             |             |          |          |
|                          | requesting                   |             |             |          |          |
|                          | arbitration<br>was one of    |             |             |          |          |
|                          | the nodes that               |             |             |          |          |
|                          | took part in                 |             |             |          |          |
|                          | the selection                |             |             |          |          |
|                          | process.                     |             |             |          |          |
|                          |                              |             |             |          |          |
| Arbitration              | This message                 | ArbitResult | NodeRestart | 2        | ALERT    |
| check lost               | reports on                   |             |             |          |          |
| - less than              | the result of                |             |             |          |          |
| 1/2 nodes                | arbitration.<br>In the event |             |             |          |          |
| left or                  | of arbitration               |             |             |          |          |
| Arbitration<br>check won | failure, an                  |             |             |          |          |
| - all node               | error_message                |             |             |          |          |
| groups and               | and an                       |             |             |          |          |
| more than                | arbitration                  |             |             |          |          |
| 1/2 nodes                | state_code                   |             |             |          |          |
| left or                  | are provided;                |             |             |          |          |
| Arbitration              | definitions for              |             |             |          |          |
| check won -              | both of these                |             |             |          |          |
| node group               | are found in                 |             |             |          |          |
| majority or              | include/                     |             |             |          |          |
| Arbitration              | kernel/                      |             |             |          |          |
| check lost               | signaldata/                  |             |             |          |          |
| - missing                | ArbitSignalData.hpp.         |             |             |          |          |
| node group               |                              |             |             |          |          |
| or Network               |                              |             |             |          |          |
| partitioning             |                              |             |             |          |          |
| -                        |                              |             |             |          |          |
| arbitration              |                              |             |             |          |          |
| required or              |                              |             |             |          |          |
| Arbitration              |                              |             |             |          |          |
| won -                    |                              |             |             |          |          |
| positive                 |                              |             |             |          |          |
| reply                    |                              |             |             |          |          |
| from node                |                              |             |             |          |          |
| node_id or               |                              |             |             |          |          |

| Log Message        | Description                  | Event Name                      | Event Type  | Priority | Severity |
|--------------------|------------------------------|---------------------------------|-------------|----------|----------|
| Arbitration        |                              |                                 |             |          |          |
| lost -             |                              |                                 |             |          |          |
| negative           |                              |                                 |             |          |          |
| reply              |                              |                                 |             |          |          |
| from node          |                              |                                 |             |          |          |
| node_id            |                              |                                 |             |          |          |
| or Network         |                              |                                 |             |          |          |
| partitioning       |                              |                                 |             |          |          |
| - no               |                              |                                 |             |          |          |
| arbitrator         |                              |                                 |             |          |          |
| available          |                              |                                 |             |          |          |
| or Network         |                              |                                 |             |          |          |
| partitioning       |                              |                                 |             |          |          |
| - no               |                              |                                 |             |          |          |
| arbitrator         |                              |                                 |             |          |          |
| configured or      |                              |                                 |             |          |          |
| Arbitration        |                              |                                 |             |          |          |
| failure -          |                              |                                 |             |          |          |
| error_message      |                              |                                 |             |          |          |
| [state=state_code] |                              |                                 |             |          |          |
| Node               | This node is                 | GCP_TakeoverStarted NodeRestart |             | 7        | INFO     |
| node_id:           | attempting                   |                                 |             |          |          |
| GCP Take           | to assume                    |                                 |             |          |          |
| over               | responsibility               |                                 |             |          |          |
| started            | for the                      |                                 |             |          |          |
|                    | next global                  |                                 |             |          |          |
|                    | checkpoint                   |                                 |             |          |          |
|                    | (that is, it is              |                                 |             |          |          |
|                    | becoming the                 |                                 |             |          |          |
|                    | master node)                 |                                 |             |          |          |
| Node               | This node has                | GCP_TakeoverCompleted           | NodeRestart | 7        | INFO     |
| node_id:           | become the                   |                                 |             |          |          |
|                    | master, and                  |                                 |             |          |          |
| GCP Take           | has assumed                  |                                 |             |          |          |
| over               | responsibility               |                                 |             |          |          |
| completed          | for the                      |                                 |             |          |          |
|                    | next global                  |                                 |             |          |          |
|                    | checkpoint                   |                                 |             |          |          |
|                    |                              |                                 |             |          |          |
| Node               | This node is                 | LCP_TakeoverStarted NodeRestart |             | 7        | INFO     |
| node_id:           | attempting                   |                                 |             |          |          |
| LCP Take           | to assume                    |                                 |             |          |          |
| over               | responsibility               |                                 |             |          |          |
| started            | for the next                 |                                 |             |          |          |
|                    | set of local                 |                                 |             |          |          |
|                    | checkpoints                  |                                 |             |          |          |
|                    | (that is, it is              |                                 |             |          |          |
|                    | becoming the<br>master node) |                                 |             |          |          |
|                    |                              |                                 |             |          |          |
| Node               | This node has                | LCP_TakeoverCompleted           | NodeRestart | 7        | INFO     |
| node_id:           | become the                   |                                 |             |          |          |
| LCP Take           | master, and                  |                                 |             |          |          |
| over               | has assumed                  |                                 |             |          |          |
| completed          | responsibility               |                                 |             |          |          |
|                    | for the next                 |                                 |             |          |          |

| Log Message                                                                                                                                                                                                                                                                                                                                                          | Description                                                                                                    | Event Name                    | Event Type | Priority | Severity |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|-------------------------------|------------|----------|----------|
|                                                                                                                                                                                                                                                                                                                                                                      | set of local<br>checkpoints                                                                                    |                               |            |          |          |
| Node<br>node_id:<br>Trans.<br>Count =<br>transactions,<br>Commit<br>Count =<br>commits,<br>Read Count<br>= reads,<br>Simple Read<br>Count =<br>simple_reads,<br>Write Count<br>= writes,<br>AttrInfo<br>Count =<br>AttrInfo_objects,<br>Concurrent<br>Operations<br>=<br>concurrent_operations,<br>Abort Count<br>= aborts,<br>Scans =<br>scans,<br>Range<br>scans = | This report of<br>transaction<br>activity is given<br>approximately<br>once every 10<br>seconds                | TransReportCounters Statistic |            | 8        | INFO     |
| range_scans<br>Node<br>node_id:<br>Operations=operations                                                                                                                                                                                                                                                                                                             | Number of<br>operations<br>performed<br>by this node,<br>provided<br>approximately<br>once every 10<br>seconds | OperationReportCounters       | Statistic  | 8        | INFO     |
| Node<br>node_id:<br>Table<br>with ID =<br>table_id<br>created                                                                                                                                                                                                                                                                                                        | A table having<br>the table ID<br>shown has<br>been created                                                    | TableCreated Statistic        |            | 7        | INFO     |
| Node<br>node_id:<br>Mean loop<br>Counter in<br>doJob last<br>8192 times<br>= count                                                                                                                                                                                                                                                                                   |                                                                                                                | JobStatistic Statistic        |            | 9        | INFO     |
| Mean send<br>size to                                                                                                                                                                                                                                                                                                                                                 | This node is<br>sending an                                                                                     | SendBytesStatistic Statistic  |            | 9        | INFO     |

| Log Message                                                                                                                                                                                                                                     | Description                                                                                                                                                                                                                                   | Event Name               | Event Type | Priority | Severity |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|------------|----------|----------|
| Node =<br>node_id<br>last 4096<br>sends =<br>bytes bytes                                                                                                                                                                                        | average of<br>bytes bytes<br>per send to<br>node node_id                                                                                                                                                                                      |                          |            |          |          |
| Mean<br>receive<br>size to<br>Node =<br>node_id<br>last 4096<br>sends =<br>bytes bytes                                                                                                                                                          | This node is<br>receiving an<br>average of<br>bytes of data<br>each time it<br>receives data<br>from node<br>node_id                                                                                                                          | ReceiveBytesStatistic    | Statistic  | 9        | INFO     |
| Node<br>node_id:<br>Data<br>usage is<br>data_memory_percentage%<br>(data_pages_used<br>32K pages<br>of total<br>data_pages_total)<br>/ Node<br>node_id:<br>Index<br>usage is<br>(index_pages_used<br>8K pages<br>of total<br>index_pages_total) | This report<br>is generated<br>when a DUMP<br>1000 command<br>is issued in<br>the cluster<br>management<br>client<br>index_memory_percentage%                                                                                                 | MemoryUsage              | Statistic  | 5        | INFO     |
| Node<br>node1_id:<br>Transporter<br>to node<br>node2_id<br>reported<br>error<br>error_code:<br>error_message                                                                                                                                    | A transporter<br>error occurred<br>while<br>communicating<br>with node<br>node2_id;<br>for a listing<br>of transporter<br>error codes<br>and messages,<br>see NDB<br>Transporter<br>Errors, in<br>MySQL<br>NDB Cluster<br>Internals<br>Manual | TransporterError Error   |            | 2        | ERROR    |
| Node<br>node1_id:<br>Transporter<br>to node<br>node2_id<br>reported<br>error                                                                                                                                                                    | A warning of<br>a potential<br>transporter<br>problem while<br>communicating<br>with node<br>node2_id;                                                                                                                                        | TransporterWarning Error |            | 8        | WARNING  |

| Log Message            | Description                                                                   | Event Name               | Event Type | Priority | Severity |
|------------------------|-------------------------------------------------------------------------------|--------------------------|------------|----------|----------|
| error_code:            | for a listing                                                                 |                          |            |          |          |
| error_message          | of transporter                                                                |                          |            |          |          |
|                        | error codes                                                                   |                          |            |          |          |
|                        | and messages,                                                                 |                          |            |          |          |
|                        | see NDB                                                                       |                          |            |          |          |
|                        | Transporter                                                                   |                          |            |          |          |
|                        | Errors, for more                                                              |                          |            |          |          |
|                        | information                                                                   |                          |            |          |          |
| Node                   | This node                                                                     | MissedHeartbeat Error    |            | 8        | WARNING  |
| node1_id:              | missed a                                                                      |                          |            |          |          |
| Node                   | heartbeat                                                                     |                          |            |          |          |
| node2_id               | from node                                                                     |                          |            |          |          |
| missed                 | node2_id                                                                      |                          |            |          |          |
| heartbeat              |                                                                               |                          |            |          |          |
| heartbeat_id           |                                                                               |                          |            |          |          |
| Node                   | This node has                                                                 | DeadDueToHeartbeat Error |            | 8        | ALERT    |
| node1_id:              | missed at least                                                               |                          |            |          |          |
| Node                   | 3 heartbeats                                                                  |                          |            |          |          |
| node2_id               | from node                                                                     |                          |            |          |          |
| declared               | node2_id,                                                                     |                          |            |          |          |
| dead due               | and so has<br>declared that                                                   |                          |            |          |          |
| to missed<br>heartbeat | node "dead"                                                                   |                          |            |          |          |
|                        |                                                                               |                          |            |          |          |
| Node                   | This node                                                                     | SentHeartbeatInfo        |            | 12       | INFO     |
| node1_id:              | has sent a                                                                    |                          |            |          |          |
| Node Sent              | heartbeat<br>to node                                                          |                          |            |          |          |
| Heartbeat<br>to node = | node2_id                                                                      |                          |            |          |          |
| node2_id               |                                                                               |                          |            |          |          |
|                        | This report is                                                                |                          |            | 7        |          |
| Node<br>node_id:       | seen during                                                                   | EventBufferStatus2 Info  |            |          | INFO     |
| Event                  | heavy event                                                                   |                          |            |          |          |
| buffer                 | buffer usage,                                                                 |                          |            |          |          |
| status                 | for example,                                                                  |                          |            |          |          |
| (object_id):           | when many                                                                     |                          |            |          |          |
| used=bytes_used        | updates are                                                                   |                          |            |          |          |
| (percent_used%         | being applied                                                                 |                          |            |          |          |
| of alloc)              | in a relatively                                                               |                          |            |          |          |
| alloc=bytes_allocated  | short period                                                                  |                          |            |          |          |
| max=bytes_available    | of time; the                                                                  |                          |            |          |          |
|                        | report shows<br>latest_consumed_epoch=latest_consumed_epoch                   |                          |            |          |          |
|                        | the number of<br>latest_buffered_epoch=latest_buffered_epoch<br>bytes and the |                          |            |          |          |
|                        | report_reason=report_reason<br>percentage of                                  |                          |            |          |          |
|                        | event buffer                                                                  |                          |            |          |          |
|                        | memory used,                                                                  |                          |            |          |          |
|                        | the bytes                                                                     |                          |            |          |          |
|                        | allocated and                                                                 |                          |            |          |          |
|                        | percentage                                                                    |                          |            |          |          |
|                        | still available,                                                              |                          |            |          |          |
|                        | and the latest                                                                |                          |            |          |          |
|                        | buffered and                                                                  |                          |            |          |          |
|                        | consumed                                                                      |                          |            |          |          |
|                        | epochs;                                                                       |                          |            |          |          |
|                        | for more                                                                      |                          |            |          |          |

| Log Message                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Event Name          | Event Type | Priority | Severity |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|------------|----------|----------|
|                                                                                                                                                                                                                | information, see<br>Section 25.6.2.3,<br>"Event Buffer<br>Reporting in the<br>Cluster Log"                                                                                                                                                                                                                                                                                                                                                                                            |                     |            |          |          |
| Node<br>node_id:<br>Entering<br>single user<br>mode, Node<br>node_id:<br>Entered<br>single user<br>mode Node<br>API_node_id<br>has<br>exclusive<br>access, Node<br>node_id:<br>Entering<br>single user<br>mode | These reports<br>are written<br>to the cluster<br>log when<br>entering and<br>exiting single<br>user mode;<br>API_node_id<br>is the node ID<br>of the API or<br>SQL having<br>exclusive<br>access to<br>the cluster<br>(for more<br>information, see<br>Section 25.6.6,<br>"NDB Cluster<br>Single User<br>Mode"); the<br>message<br>Unknown<br>single<br>user report<br>API_node_id<br>indicates an<br>error has taken<br>place and<br>should never be<br>seen in normal<br>operation | SingleUser          | Info       | 7        | INFO     |
| Node<br>node_id:<br>Backup<br>backup_id<br>started<br>from node<br>mgm_node_id                                                                                                                                 | A backup has<br>been started<br>using the<br>management<br>node having<br>mgm_node_id;<br>this message is<br>also displayed<br>in the cluster<br>management<br>client when<br>the START<br>BACKUP<br>command is<br>issued; for more<br>information, see<br>Section 25.6.8.2,<br>"Using The<br>NDB Cluster<br>Management                                                                                                                                                               | BackupStartedBackup |            | 7        | INFO     |

| Log Message                                                                                                                                                                                                                                                      | Description                                                                                                                                                                                         | Event Name                 | Event Type | Priority | Severity |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|------------|----------|----------|
|                                                                                                                                                                                                                                                                  | Client to Create<br>a Backup"                                                                                                                                                                       |                            |            |          |          |
| Node<br>node_id:<br>Backup<br>backup_id<br>started<br>from node<br>mgm_node_id<br>completed.<br>StartGCP:<br>start_gcp<br>StopGCP:<br>stop_gcp<br>#Records:<br>records<br>#LogRecords:<br>log_records<br>Data:<br>data_bytes<br>bytes Log:<br>log_bytes<br>bytes | The backup<br>having the ID<br>backup_id<br>has been<br>completed;<br>for more<br>information, see<br>Section 25.6.8.2,<br>"Using The<br>NDB Cluster<br>Management<br>Client to Create<br>a Backup" | BackupCompleted Backup     |            | 7        | INFO     |
| Node<br>node_id:<br>Backup<br>request<br>from<br>mgm_node_id<br>failed to<br>start.<br>Error:<br>error_code                                                                                                                                                      | The backup<br>failed to start;<br>for error codes,<br>see MGM API<br>Errors                                                                                                                         | BackupFailedToStart Backup |            | 7        | ALERT    |
| Node<br>node_id:<br>Backup<br>backup_id<br>started<br>from<br>mgm_node_id<br>has been<br>aborted.<br>Error:<br>error_code                                                                                                                                        | The backup<br>was terminated<br>after starting,<br>possibly<br>due to user<br>intervention                                                                                                          | BackupAbortedBackup        |            | 7        | ALERT    |

# <span id="page-62-0"></span>**25.6.2.2 NDB Cluster Log Startup Messages**

Possible startup messages with descriptions are provided in the following list:

```
• Initial start, waiting for %s to connect, nodes [ all: %s connected: %s
 no-wait: %s ]
```

```
• Waiting until nodes: %s connects, nodes [ all: %s connected: %s no-wait:
 %s ]
```

```
• Waiting %u sec for nodes %s to connect, nodes [ all: %s connected: %s no-
 wait: %s ]
• Waiting for non partitioned start, nodes [ all: %s connected: %s missing:
 %s no-wait: %s ]
• Waiting %u sec for non partitioned start, nodes [ all: %s connected: %s
 missing: %s no-wait: %s ]
• Initial start with nodes %s [ missing: %s no-wait: %s ]
• Start with all nodes %s
• Start with nodes %s [ missing: %s no-wait: %s ]
```

• Start potentially partitioned with nodes %s [ missing: %s no-wait: %s ]

# <span id="page-63-0"></span>**25.6.2.3 Event Buffer Reporting in the Cluster Log**

• Unknown startreport: 0x%x [ %s %s %s %s ]

NDB uses one or more memory buffers for events received from the data nodes. There is one such buffer for each [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object subscribing to table events, which means that there are usually two buffers for each mysqld performing binary logging (one buffer for schema events, and one for data events). Each buffer contains epochs made up of events. These events consist of operation types (insert, update, delete) and row data (before and after images plus metadata).

NDB generates messages in the cluster log to describe the state of these buffers. Although these reports appear in the cluster log, they refer to buffers on API nodes (unlike most other cluster log messages, which are generated by data nodes).

Event buffer logging reports in the cluster log use the format shown here:

```
Node node_id: Event buffer status (object_id):
used=bytes_used (percent_used% of alloc)
alloc=bytes_allocated (percent_alloc% of max) max=bytes_available
latest_consumed_epoch=latest_consumed_epoch
latest_buffered_epoch=latest_buffered_epoch
report_reason=report_reason
```

The fields making up this report are listed here, with descriptions:

- node\_id: ID of the node where the report originated.
- object\_id: ID of the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object where the report originated.
- bytes\_used: Number of bytes used by the buffer.
- percent\_used: Percentage of allocated bytes used.
- bytes\_allocated: Number of bytes allocated to this buffer.
- percent\_alloc: Percentage of available bytes used; not printed if ndb\_eventbuffer\_max\_alloc is equal to 0 (unlimited).
- bytes\_available: Number of bytes available; this is 0 if ndb\_eventbuffer\_max\_alloc is 0 (unlimited).
- latest\_consumed\_epoch: The epoch most recently consumed to completion. (In NDB API applications, this is done by calling [nextEvent\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md#ndb-ndb-nextevent).)
- latest\_buffered\_epoch: The epoch most recently buffered (completely) in the event buffer.
- report\_reason: The reason for making the report. Possible reasons are shown later in this section.

Possible reasons for reporting are described in the following list:

• ENOUGH\_FREE\_EVENTBUFFER: The event buffer has sufficient space.

LOW\_FREE\_EVENTBUFFER: The event buffer is running low on free space.

The threshold free percentage level triggering these reports can be adjusted by setting the ndb\_report\_thresh\_binlog\_mem\_usage server variable.

- BUFFERED\_EPOCHS\_OVER\_THRESHOLD: Whether the number of buffered epochs has exceeded the configured threshold. This number is the difference between the latest epoch that has been received in its entirety and the epoch that has most recently been consumed (in NDB API applications, this is done by calling [nextEvent\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md#ndb-ndb-nextevent) or [nextEvent2\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md#ndb-ndb-nextevent2)). The report is generated every second until the number of buffered epochs goes below the threshold, which can be adjusted by setting the ndb\_report\_thresh\_binlog\_epoch\_slip server variable. You can also adjust the threshold in NDB API applications by calling [setEventBufferQueueEmptyEpoch\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md#ndb-ndb-seteventbufferqueueemptyepoch).
- PARTIALLY\_DISCARDING: Event buffer memory is exhausted—that is, 100% of ndb\_eventbuffer\_max\_alloc has been used. Any partially buffered epoch is buffered to completion even is usage exceeds 100%, but any new epochs received are discarded. This means that a gap has occurred in the event stream.
- COMPLETELY\_DISCARDING: No epochs are buffered.
- PARTIALLY\_BUFFERING: The buffer free percentage following the gap has risen to the threshold, which can be set in the mysql client using the ndb\_eventbuffer\_free\_percent server system variable or in NDB API applications by calling [set\\_eventbuffer\\_free\\_percent\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md#ndb-ndb-set-eventbuffer-free-percent). New epochs are buffered. Epochs that could not be completed due to the gap are discarded.
- COMPLETELY\_BUFFERING: All epochs received are being buffered, which means that there is sufficient event buffer memory. The gap in the event stream has been closed.