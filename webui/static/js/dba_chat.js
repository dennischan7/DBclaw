/**
 * DBA SafeGuard WebUI — Chat Module
 *
 * Handles:
 *   - Send button / Enter key → POST /api/dba/chat
 *   - Render user & assistant messages
 *   - Pipeline progress bar inline in chat
 *   - Approval card inline rendering
 *   - Rollback display
 */

import { store, subscribe, dispatch, on } from './dba_store.js';

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

let _csrfToken = '';
let _chatContainer = null;
let _chatInput = null;
let _sendBtn = null;
let _queryResultId = 0;

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------

export function initChat() {
    _chatContainer = document.getElementById('chatMessages');
    _chatInput = document.getElementById('chatInput');
    _sendBtn = document.getElementById('btnSendChat');

    if (!_chatContainer || !_chatInput || !_sendBtn) return;

    // Send button click
    _sendBtn.addEventListener('click', _handleSend);

    // Listen for approval SSE events to render inline
    on('approval:event', (detail) => {
        if (detail.type === 'approval_requested') {
            _appendApprovalCard(detail.data);
        }
    });

    // Listen for task pipeline events
    on('task:event', (detail) => {
        if (detail.type === 'task_stage') {
            _updateInlinePipeline(detail.data);
        }
    });
}


// ---------------------------------------------------------------------------
// Session & CSRF
// ---------------------------------------------------------------------------

export async function ensureSession() {
    if (_csrfToken) return _csrfToken;
    return _initSession();
}

async function _initSession() {
    try {
        const resp = await fetch('/api/dba/session');
        const data = await resp.json();
        _csrfToken = data.csrf_token || resp.headers.get('X-CSRF-Token') || '';
        // Expose CSRF token for inline scripts
        if (window.__dba) window.__dba._csrfToken = _csrfToken;
        if (data.user_id) store.userId = data.user_id;
        if (data.role != null) store.userRole = data.role;
    } catch (e) {
        console.error('[Chat] Session init failed:', e);
    }
}


// ---------------------------------------------------------------------------
// Send Message
// ---------------------------------------------------------------------------

async function _handleSend() {
    const text = _chatInput.value.trim();
    if (!text || store.chatLoading) return;

    // Add user message to UI
    _appendUserMessage(text);
    _chatInput.value = '';
    _chatInput.style.height = 'auto';

    // Set loading state
    store.chatLoading = true;
    _sendBtn.classList.add('loading');
    _sendBtn.disabled = true;

    // Show thinking indicator
    const thinkingId = _appendThinking();

    try {
        const data = await _postChat({ message: text });
        _removeThinking(thinkingId);

        // Track conversation_id returned by server
        if (data.conversation_id) {
            store.currentConversationId = data.conversation_id;
        }

        if (data.error && !data.generated_sql) {
            _appendErrorMessage(data.error);
        } else {
            _appendAssistantResponse(data);
        }

        // Notify sidebar to refresh conversation list
        dispatch('conversations:changed');
    } catch (e) {
        _removeThinking(thinkingId);
        _appendErrorMessage(`请求失败: ${e.message}`);
    } finally {
        store.chatLoading = false;
        _sendBtn.classList.remove('loading');
        _sendBtn.disabled = false;
        _chatInput.focus();
    }
}

async function _postChat(payload) {
    const resp = await fetch('/api/dba/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': _csrfToken,
        },
        body: JSON.stringify({
            instance_name: store.currentInstance,
            dialect: store.instanceDialect || 'postgresql',
            safety_mode: store.safetyMode,
            conversation_id: store.currentConversationId || '',
            ...payload,
        }),
    });
    return resp.json();
}


// ---------------------------------------------------------------------------
// Message Rendering
// ---------------------------------------------------------------------------

let _msgId = 0;

function _appendUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'chat-msg user';
    div.innerHTML = `<div class="chat-msg-content">${_escapeHtml(text)}</div>`;
    _chatContainer.appendChild(div);
    _scrollToBottom();
}

function _appendThinking() {
    const id = `thinking-${++_msgId}`;
    const div = document.createElement('div');
    div.className = 'chat-msg assistant';
    div.id = id;
    div.innerHTML = `
        <div class="chat-msg-content text-muted">
            <span class="thinking-dots">⏳ 正在分析</span>
        </div>`;
    _chatContainer.appendChild(div);
    _scrollToBottom();
    return id;
}

function _removeThinking(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function _appendErrorMessage(text) {
    const div = document.createElement('div');
    div.className = 'chat-msg error';
    div.innerHTML = `<div class="chat-msg-content">❌ ${_escapeHtml(text)}</div>`;
    _chatContainer.appendChild(div);
    _scrollToBottom();
}

function _appendAssistantResponse(data, options = {}) {
    const div = document.createElement('div');
    div.className = 'chat-msg assistant';
    const updateContext = options.updateContext !== false;

    let html = '';

    if (data.generated_sql) {
        html += _renderGeneratedSqlCard(data.generated_sql, data.source_message || '', !data.task);
    }

    // Pipeline summary
    if (data.task && data.task.stage_results && data.task.stage_results.length > 0) {
        html += _renderPipelineSummary(data.task);
    }

    // Risk badge
    if (data.task && data.task.risk_level != null) {
        html += `<span class="risk-badge risk-L${data.task.risk_level}">L${data.task.risk_level}</span> `;
    }

    // Main response text
    if (data.response) {
        html += `<div class="chat-msg-content">${_formatResponse(data.response)}</div>`;
    }

    // SQL block (if present)
    if (data.task && data.task.sql) {
        const riskClass = data.task.risk_level != null ? `risk-L${data.task.risk_level}` : '';
        html += `
            <div class="sql-block">
                <div class="sql-block-risk-bar ${riskClass}"></div>
                <pre>${_highlightSQL(_escapeHtml(data.task.sql))}</pre>
            </div>`;
    }

    // Execution result
    if (data.task && data.task.execution_result) {
        const execResult = data.task.execution_result;
        if (typeof execResult === 'object') {
            html += _renderExecutionResult(execResult);
        }
    }

    // Rollback SQL (if present)
    if (data.task && data.task.rollback_sql) {
        html += `
            <details class="rollback-details mt-2">
                <summary class="text-sm text-muted" style="cursor:pointer">
                    🔄 查看回滚脚本
                </summary>
                <div class="sql-block" style="margin-top:4px">
                    <pre>${_highlightSQL(_escapeHtml(data.task.rollback_sql))}</pre>
                </div>
                <button class="btn btn-danger btn-sm mt-2 rollback-exec-btn"
                        data-sql="${_escapeAttr(data.task.rollback_sql)}"
                        data-task-id="${_escapeAttr(data.task.task_id || '')}">
                    ⚠️ 执行回滚
                </button>
            </details>`;
    }

    // Approval pending notice
    if (data.needs_approval) {
        html += `
            <div class="approval-notice text-warning text-sm mt-2">
                ⏳ 此操作需要审批，已提交审批队列。
                <a href="#" class="go-to-approvals">前往审批 →</a>
            </div>`;
    }

    div.innerHTML = html;

    // Wire rollback execute button
    const rollbackBtn = div.querySelector('.rollback-exec-btn');
    if (rollbackBtn) {
        rollbackBtn.addEventListener('click', () => _executeRollback(rollbackBtn));
    }

    const confirmBtn = div.querySelector('.generated-sql-confirm');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => _confirmGeneratedSql(confirmBtn));
    }

    // Wire go-to-approvals link
    const approvalLink = div.querySelector('.go-to-approvals');
    if (approvalLink) {
        approvalLink.addEventListener('click', (e) => {
            e.preventDefault();
            store.activePanel = 'approvals';
        });
    }

    div.querySelectorAll('.query-result-card[data-result-set-id]').forEach((card) => {
        _bindQueryResultCard(card);
    });

    _chatContainer.appendChild(div);

    // Update context panel with task info
    if (updateContext && data.task) {
        store.currentTask = data.task;
        store.currentTaskId = data.task.task_id;
        if (data.task.stage_results) {
            store.pipelineStages = data.task.stage_results;
        }
    } else if (updateContext && data.generated_sql) {
        store.currentTaskId = null;
        store.pipelineStages = [];
        store.currentTask = {
            task_id: '-',
            intent: data.intent || null,
            instance_name: store.currentInstance,
            source_message: data.source_message || '',
            generated_sql: data.generated_sql,
        };
    }

    _scrollToBottom();
}

function _renderExecutionResult(execResult) {
    if (!execResult) return '';

    let html = `<div class="execution-result text-sm mt-2">`;
    if (execResult.success) {
        html += `<span class="text-success">✅ 执行成功</span>`;
        const resultData = execResult.data;
        if (resultData && Array.isArray(resultData.columns)) {
            const totalRows = resultData.total_rows;
            const loadedCount = resultData.loaded_count ?? (Array.isArray(resultData.rows) ? resultData.rows.length : 0);
            if (totalRows != null) {
                html += ` — 返回 ${totalRows} 行`;
            } else if (loadedCount != null) {
                html += ` — 已加载 ${loadedCount} 行`;
                if (resultData.has_more) {
                    html += `，继续下滑可加载更多`;
                }
            }
            if (execResult.execution_time_ms != null) {
                html += ` (${execResult.execution_time_ms}ms)`;
            }
            html += `</div>`;
            html += _renderQueryResultTable(resultData);
            return html;
        }

        if (execResult.rows_affected != null) {
            html += ` — 影响 ${execResult.rows_affected} 行`;
        }
        if (execResult.execution_time_ms != null) {
            html += ` (${execResult.execution_time_ms}ms)`;
        }
    } else {
        html += `<span class="text-error">❌ 执行失败: ${_escapeHtml(execResult.error || '')}</span>`;
    }
    html += `</div>`;
    return html;
}

function _renderQueryResultTable(resultData) {
    const columns = Array.isArray(resultData.columns) ? resultData.columns : [];
    const rows = Array.isArray(resultData.rows) ? resultData.rows : [];
    const resultSetId = resultData.result_set_id || '';
    const loadedCount = resultData.loaded_count ?? rows.length;
    const totalRows = resultData.total_rows;
    const hasMore = Boolean(resultData.has_more && resultSetId);
    const tableId = `query-result-${++_queryResultId}`;
    const title = totalRows != null
        ? `查询结果 · ${totalRows} 行`
        : `查询结果 · 已加载 ${loadedCount} 行`;
    const subtitle = hasMore
        ? `首批 ${loadedCount} 行已加载，滚动到底部自动继续读取。`
        : `当前结果已完整加载。`;

    const headerCells = columns
        .map((column) => `<th>${_escapeHtml(String(column))}</th>`)
        .join('');
    const bodyRows = _renderQueryResultRows(rows, columns.length);

    return `
        <section class="query-result-card"
                 data-result-set-id="${_escapeAttr(resultSetId)}"
                 data-conversation-id="${_escapeAttr(store.currentConversationId || '')}"
                 data-offset="${loadedCount}"
                 data-has-more="${hasMore ? 'true' : 'false'}"
                 data-loading="false"
                 id="${tableId}">
            <div class="query-result-header">
                <div>
                    <div class="query-result-title">${_escapeHtml(title)}</div>
                    <div class="query-result-subtitle">${_escapeHtml(subtitle)}</div>
                </div>
                <div class="query-result-meta">
                    <span class="query-result-pill">批次 ${_escapeHtml(String(resultData.page_size || rows.length || 0))}</span>
                    <span class="query-result-pill ${hasMore ? 'is-live' : ''}">${hasMore ? 'Live' : 'Preview'}</span>
                </div>
            </div>
            <div class="query-result-table-wrapper">
                <table class="data-table query-result-table">
                    <thead>
                        <tr>
                            <th class="query-result-rownum">#</th>
                            ${headerCells}
                        </tr>
                    </thead>
                    <tbody>${bodyRows}</tbody>
                </table>
            </div>
            <div class="query-result-footer">
                <span class="query-result-status">${hasMore ? '向下滚动加载更多结果' : '全部结果已展示'}</span>
            </div>
        </section>`;
}

function _renderQueryResultRows(rows, columnCount, startIndex = 0) {
    return rows.map((row, rowIndex) => {
        const cells = Array.isArray(row) ? row : [];
        const paddedCells = [];
        for (let index = 0; index < columnCount; index++) {
            paddedCells.push(_renderQueryResultCell(cells[index]));
        }
        return `<tr>
            <td class="query-result-rownum">${startIndex + rowIndex + 1}</td>
            ${paddedCells.join('')}
        </tr>`;
    }).join('');
}

function _renderQueryResultCell(value) {
    let display = '';
    let cellClass = 'query-result-cell';

    if (value == null) {
        display = '<span class="query-result-null">NULL</span>';
    } else if (typeof value === 'number') {
        cellClass += ' is-number';
        display = _escapeHtml(String(value));
    } else if (typeof value === 'boolean') {
        display = _escapeHtml(value ? 'true' : 'false');
    } else if (typeof value === 'object') {
        display = _escapeHtml(JSON.stringify(value));
    } else {
        display = _escapeHtml(String(value));
    }

    return `<td class="${cellClass}" title="${_escapeAttr(typeof value === 'object' && value != null ? JSON.stringify(value) : String(value ?? ''))}">${display}</td>`;
}

function _bindQueryResultCard(card) {
    if (!card || card.dataset.bound === 'true') return;
    const wrapper = card.querySelector('.query-result-table-wrapper');
    if (!wrapper) return;

    wrapper.addEventListener('scroll', () => {
        const maxScroll = wrapper.scrollHeight - wrapper.clientHeight;
        if (maxScroll <= 0) return;
        const ratio = wrapper.scrollTop / maxScroll;
        if (ratio >= 0.85) {
            _loadMoreQueryResult(card);
        }
    });
    card.dataset.bound = 'true';
}

async function _loadMoreQueryResult(card) {
    if (!card) return;
    if (card.dataset.loading === 'true') return;
    if (card.dataset.hasMore !== 'true') return;

    const resultSetId = card.dataset.resultSetId;
    const conversationId = card.dataset.conversationId;
    const offset = Number(card.dataset.offset || '0');
    if (!resultSetId || !conversationId) return;

    card.dataset.loading = 'true';
    _setQueryResultStatus(card, '正在加载下一批 100 行…');

    try {
        const resp = await fetch(
            `/api/dba/chat/results/${encodeURIComponent(resultSetId)}?conversation_id=${encodeURIComponent(conversationId)}&offset=${offset}&limit=100`
        );
        const data = await resp.json();
        if (!resp.ok || data.error) {
            throw new Error(data.error || '结果加载失败');
        }

        const rows = Array.isArray(data.rows) ? data.rows : [];
        const tbody = card.querySelector('tbody');
        const columnCount = Array.isArray(data.columns) ? data.columns.length : 0;
        if (tbody && rows.length > 0) {
            tbody.insertAdjacentHTML('beforeend', _renderQueryResultRows(rows, columnCount, offset));
        }

        card.dataset.offset = String(data.loaded_count ?? (offset + rows.length));
        card.dataset.hasMore = data.has_more ? 'true' : 'false';

        const titleEl = card.querySelector('.query-result-title');
        if (titleEl) {
            titleEl.textContent = data.total_rows != null
                ? `查询结果 · ${data.total_rows} 行`
                : `查询结果 · 已加载 ${data.loaded_count ?? (offset + rows.length)} 行`;
        }
        const subtitleEl = card.querySelector('.query-result-subtitle');
        if (subtitleEl) {
            subtitleEl.textContent = data.has_more
                ? `已连续加载 ${data.loaded_count ?? (offset + rows.length)} 行，继续下滑可追加更多结果。`
                : '结果流已结束，当前表格即完整结果。';
        }

        _setQueryResultStatus(
            card,
            data.has_more ? '继续下滑加载更多结果' : '全部结果已展示'
        );
    } catch (error) {
        _setQueryResultStatus(card, `加载失败：${error.message}`);
    } finally {
        card.dataset.loading = 'false';
    }
}

function _setQueryResultStatus(card, text) {
    const status = card.querySelector('.query-result-status');
    if (status) {
        status.textContent = text;
    }
}


// ---------------------------------------------------------------------------
// Pipeline Summary (inline in chat)
// ---------------------------------------------------------------------------

const STAGE_ICONS = {
    pending: '○', running: '◉', passed: '✓', failed: '✗', skipped: '−', blocked: '⏸',
};

function _renderPipelineSummary(task) {
    const stages = task.stage_results || [];
    if (stages.length === 0) return '';

    const passed = stages.filter(s => s.status === 'passed').length;
    const failed = stages.filter(s => s.status === 'failed').length;
    const total = stages.length;

    let statusText = `${passed}/${total} 阶段通过`;
    let statusClass = 'text-success';
    if (failed > 0) {
        statusText = `${failed} 阶段失败`;
        statusClass = 'text-error';
    }

    const stageHtml = stages.map(s => {
        const icon = STAGE_ICONS[s.status] || '○';
        const timeStr = s.duration_ms != null ? `${s.duration_ms}ms` : '';
        return `<div class="pipeline-stage ${s.status}">
            <span class="pipeline-stage-icon">${icon}</span>
            <span class="pipeline-stage-name">${_escapeHtml(s.stage)}</span>
            <span class="pipeline-stage-time">${timeStr}</span>
        </div>`;
    }).join('');

    return `
        <div class="pipeline-bar" data-task-id="${_escapeAttr(task.task_id || '')}" style="margin-bottom:8px">
            <div class="pipeline-summary" onclick="this.parentElement.classList.toggle('expanded')">
                <span class="${statusClass}">${statusText}</span>
                <span class="expand-icon">▶</span>
            </div>
            <div class="pipeline-stages">${stageHtml}</div>
        </div>`;
}

function _renderGeneratedSqlCard(generatedSql, sourceMessage, canExecute) {
    const assumptions = Array.isArray(generatedSql.assumptions) ? generatedSql.assumptions : [];
    const summary = generatedSql.summary ? `<div class="text-sm mt-1">${_escapeHtml(generatedSql.summary)}</div>` : '';
    const assumptionHtml = assumptions.length > 0
        ? `<div class="text-xs text-muted mt-1">假设: ${_escapeHtml(assumptions.join('；'))}</div>`
        : '';
    const confidence = generatedSql.confidence != null
        ? `<div class="text-xs text-muted mt-1">置信度: ${_escapeHtml(String(generatedSql.confidence))}</div>`
        : '';
    const docHint = generatedSql.library_context_used
        ? '<div class="text-xs text-muted mt-1">已参考当前数据库官方文档切片</div>'
        : '';
    const actionHtml = canExecute && generatedSql.sql && generatedSql.requires_confirmation
        ? `<button class="btn btn-primary btn-sm mt-2 generated-sql-confirm"
                data-sql="${_escapeAttr(generatedSql.sql)}"
                data-source-message="${_escapeAttr(sourceMessage)}">
                ▶ 确认执行该 SQL
           </button>`
        : '';

    return `
        <div class="sql-generation-card" style="margin-bottom:8px;padding:10px;border:1px solid var(--border-primary);border-radius:10px;background:var(--bg-secondary)">
            <div class="text-sm text-muted">候选 SQL</div>
            ${summary}
            ${generatedSql.sql ? `
                <div class="sql-block" style="margin-top:8px">
                    <div class="sql-block-risk-bar risk-L1"></div>
                    <pre>${_highlightSQL(_escapeHtml(generatedSql.sql))}</pre>
                </div>` : `<div class="text-error text-sm mt-2">${_escapeHtml(generatedSql.error || '未能生成 SQL')}</div>`}
            ${assumptionHtml}
            ${confidence}
            ${docHint}
            ${actionHtml}
        </div>`;
}


// ---------------------------------------------------------------------------
// Approval Card (inline from SSE)
// ---------------------------------------------------------------------------

function _appendApprovalCard(data) {
    const div = document.createElement('div');
    div.className = 'chat-msg assistant';
    div.innerHTML = `
        <div class="approval-card risk-L${data.risk_level || 0}" id="approval-${_escapeAttr(data.request_id)}">
            <div class="approval-header">
                <span class="risk-badge risk-L${data.risk_level || 0}">L${data.risk_level || 0}</span>
                <span class="approval-title">审批请求</span>
                <span class="text-xs text-dimmed">${data.request_id || ''}</span>
            </div>
            <div class="approval-sql">${_escapeHtml(data.sql || '')}</div>
            <div class="approval-meta">
                <span>实例: ${_escapeHtml(data.instance_name || '-')}</span>
                <span>操作: ${_escapeHtml(data.operation_type || '-')}</span>
                <span>影响表: ${_escapeHtml((data.tables_affected || []).join(', ') || '-')}</span>
            </div>
            <div class="approval-actions">
                <button class="btn btn-primary btn-sm approve-btn" data-id="${_escapeAttr(data.request_id)}">
                    ✅ 通过
                </button>
                <button class="btn btn-danger btn-sm reject-btn" data-id="${_escapeAttr(data.request_id)}">
                    ❌ 驳回
                </button>
            </div>
        </div>`;

    // Wire approval buttons
    const approveBtn = div.querySelector('.approve-btn');
    const rejectBtn = div.querySelector('.reject-btn');

    if (approveBtn) {
        approveBtn.addEventListener('click', () => _quickApprove(data.request_id, div));
    }
    if (rejectBtn) {
        rejectBtn.addEventListener('click', () => _quickReject(data.request_id, div));
    }

    _chatContainer.appendChild(div);
    _scrollToBottom();
}


// ---------------------------------------------------------------------------
// Quick Approve/Reject from Chat
// ---------------------------------------------------------------------------

async function _quickApprove(requestId, cardDiv) {
    try {
        const resp = await fetch('/api/dba/approvals/approve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': _csrfToken,
            },
            body: JSON.stringify({ request_id: requestId }),
        });
        const data = await resp.json();
        if (data.success) {
            const card = cardDiv.querySelector('.approval-card');
            if (card) {
                card.classList.add('approval-resolved');
                const actions = card.querySelector('.approval-actions');
                if (actions) actions.innerHTML = '<span class="approval-resolved-label">✅ 已通过</span>';
            }
        } else {
            _appendErrorMessage(data.error || '审批失败');
        }
    } catch (e) {
        _appendErrorMessage(`审批请求失败: ${e.message}`);
    }
}

async function _quickReject(requestId, cardDiv) {
    const comment = prompt('请输入驳回原因:');
    if (!comment || !comment.trim()) return;

    try {
        const resp = await fetch('/api/dba/approvals/reject', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': _csrfToken,
            },
            body: JSON.stringify({ request_id: requestId, comment }),
        });
        const data = await resp.json();
        if (data.success) {
            const card = cardDiv.querySelector('.approval-card');
            if (card) {
                card.classList.add('approval-resolved');
                const actions = card.querySelector('.approval-actions');
                if (actions) actions.innerHTML = '<span class="approval-resolved-label">❌ 已驳回</span>';
            }
        } else {
            _appendErrorMessage(data.error || '驳回失败');
        }
    } catch (e) {
        _appendErrorMessage(`驳回请求失败: ${e.message}`);
    }
}


// ---------------------------------------------------------------------------
// Execute Rollback
// ---------------------------------------------------------------------------

async function _executeRollback(btn) {
    if (!confirm('⚠️ 确定要执行回滚脚本吗？此操作将修改数据库。')) return;

    const sql = btn.dataset.sql;
    if (!sql) return;

    btn.disabled = true;
    btn.textContent = '⏳ 执行中…';

    try {
        const resp = await fetch('/api/dba/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': _csrfToken,
            },
            body: JSON.stringify({
                message: sql,
                instance_name: store.currentInstance,
                dialect: store.instanceDialect,
                is_rollback: true,
            }),
        });
        const data = await resp.json();
        if (data.error) {
            _appendErrorMessage(`回滚失败: ${data.error}`);
        } else {
            _appendAssistantResponse(data);
        }
    } catch (e) {
        _appendErrorMessage(`回滚执行失败: ${e.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = '⚠️ 执行回滚';
    }
}


// ---------------------------------------------------------------------------
// Inline pipeline update (from SSE)
// ---------------------------------------------------------------------------

function _updateInlinePipeline(data) {
    if (!data || !data.stages || !data.task_id) return;
    if (store.currentTaskId && data.task_id !== store.currentTaskId) return;

    const bar = _chatContainer.querySelector(`.pipeline-bar[data-task-id="${CSS.escape(data.task_id)}"]`);
    if (!bar) return;

    const stagesDiv = bar.querySelector('.pipeline-stages');
    if (stagesDiv) {
        stagesDiv.innerHTML = data.stages.map(s => {
            const icon = STAGE_ICONS[s.status] || '○';
            const timeStr = s.duration_ms != null ? `${s.duration_ms}ms` : '';
            return `<div class="pipeline-stage ${s.status}">
                <span class="pipeline-stage-icon">${icon}</span>
                <span class="pipeline-stage-name">${_escapeHtml(s.stage)}</span>
                <span class="pipeline-stage-time">${timeStr}</span>
            </div>`;
        }).join('');
    }
}

async function _confirmGeneratedSql(btn) {
    const sql = btn.dataset.sql || '';
    const sourceMessage = btn.dataset.sourceMessage || '';
    if (!sql || store.chatLoading) return;

    btn.disabled = true;
    _appendUserMessage('确认执行生成的 SQL');
    const thinkingId = _appendThinking();
    store.chatLoading = true;
    _sendBtn.classList.add('loading');
    _sendBtn.disabled = true;

    try {
        const data = await _postChat({
            message: '确认执行生成的 SQL',
            execute_sql: sql,
            source_message: sourceMessage,
        });
        _removeThinking(thinkingId);
        if (data.conversation_id) {
            store.currentConversationId = data.conversation_id;
        }
        if (data.error && !data.generated_sql) {
            _appendErrorMessage(data.error);
        } else {
            _appendAssistantResponse(data);
        }
        dispatch('conversations:changed');
    } catch (e) {
        _removeThinking(thinkingId);
        _appendErrorMessage(`确认执行失败: ${e.message}`);
    } finally {
        store.chatLoading = false;
        _sendBtn.classList.remove('loading');
        _sendBtn.disabled = false;
    }
}


// ---------------------------------------------------------------------------
// SQL Syntax Highlight (simple keyword-based)
// ---------------------------------------------------------------------------

const SQL_KEYWORDS = new Set([
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET',
    'DELETE', 'CREATE', 'ALTER', 'DROP', 'TABLE', 'INDEX', 'VIEW', 'DATABASE',
    'GRANT', 'REVOKE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON',
    'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL',
    'AS', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'UNION',
    'ALL', 'DISTINCT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'IF',
    'BEGIN', 'COMMIT', 'ROLLBACK', 'TRUNCATE', 'CASCADE', 'CONSTRAINT',
    'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'DEFAULT', 'CHECK', 'UNIQUE',
    'ADD', 'COLUMN', 'RENAME', 'TO', 'WITH', 'RECURSIVE', 'EXPLAIN', 'ANALYZE',
]);

function _highlightSQL(escaped) {
    return escaped.replace(/\b(\w+)\b/g, (match) => {
        if (SQL_KEYWORDS.has(match.toUpperCase())) {
            return `<span class="sql-keyword">${match}</span>`;
        }
        return match;
    }).replace(/('(?:[^'\\]|\\.)*')/g, '<span class="sql-string">$1</span>')
      .replace(/(\b\d+(?:\.\d+)?\b)/g, '<span class="sql-number">$1</span>')
      .replace(/(--[^\n]*)/g, '<span class="sql-comment">$1</span>');
}


// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

function _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

function _escapeAttr(text) {
    return (text || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
}

function _formatResponse(text) {
    // Convert newlines to <br> and preserve code blocks
    return _escapeHtml(text).replace(/\n/g, '<br>');
}

function _scrollToBottom() {
    if (_chatContainer) {
        requestAnimationFrame(() => {
            _chatContainer.scrollTop = _chatContainer.scrollHeight;
        });
    }
}


// ---------------------------------------------------------------------------
// Conversation Management
// ---------------------------------------------------------------------------

/**
 * Load an existing conversation — fetch messages from server and render.
 */
export async function loadConversation(convId) {
    if (!_chatContainer) return;
    try {
        const resp = await fetch(`/api/dba/conversations/${convId}/messages`);
        const data = await resp.json();
        if (data.error) {
            console.error('Load conversation failed:', data.error);
            return;
        }
        // Clear chat area
        _chatContainer.innerHTML = '';
        store.currentConversationId = convId;
        store.currentTask = null;
        store.currentTaskId = null;
        store.pipelineStages = [];
        let lastTask = null;

        // Render messages
        const messages = data.messages || [];
        for (const msg of messages) {
            if (msg.role === 'user') {
                _appendUserMessage(msg.content);
            } else if (msg.role === 'assistant') {
                // Reconstruct response object for _appendAssistantResponse
                const respObj = { response: msg.content };
                if (msg.task_snapshot) {
                    if (msg.task_snapshot.generated_sql) {
                        respObj.generated_sql = msg.task_snapshot.generated_sql;
                        respObj.response_type = msg.task_snapshot.response_type || 'generation';
                        respObj.source_message = msg.task_snapshot.source_message || '';
                    } else {
                        respObj.task = msg.task_snapshot;
                        lastTask = msg.task_snapshot;
                    }
                }
                if (msg.intent) {
                    respObj.intent = { label: msg.intent };
                }
                _appendAssistantResponse(respObj, { updateContext: false });
            }
        }
        if (lastTask) {
            store.currentTask = lastTask;
            store.currentTaskId = lastTask.task_id || null;
            store.pipelineStages = lastTask.stage_results || [];
        }
    } catch (e) {
        console.error('Load conversation error:', e);
    }
}

/**
 * Start a new (empty) conversation — clear chat and reset ID.
 */
export function startNewConversation() {
    if (_chatContainer) {
        _chatContainer.innerHTML = '';
    }
    store.currentConversationId = null;
    store.currentTask = null;
    store.currentTaskId = null;
    store.pipelineStages = [];
    if (_chatInput) _chatInput.focus();
}
