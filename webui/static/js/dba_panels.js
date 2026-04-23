/**
 * DBA SafeGuard WebUI — Panel Management, Sidebar, Theme Toggle, Tabs
 *
 * Manages:
 *   - Sidebar navigation → tab switching
 *   - Theme toggle (dark/light)
 *   - Context panel toggle
 *   - Pipeline bar expand/collapse
 *   - Toast notifications
 *   - Approval badge counter
 *   - Mode badge updates
 *   - Chat auto-resize
 */

import { store, subscribe, on, loadPersistedTheme } from './dba_store.js';
import { sseClient } from './dba_sse.js';

// ---------------------------------------------------------------------------
// Panel Titles Map
// ---------------------------------------------------------------------------

const PANEL_TITLES = {
    chat: 'SQL 对话',
    dashboard: '仪表盘',
    approvals: '审批队列',
    audit: '审计日志',
    admin: '管理',
};

// Mode display names
const MODE_NAMES = ['READONLY', 'CONSERVATIVE', 'MODERATE', 'AGGRESSIVE', 'MADMAN'];
const MODE_LABELS = ['只读审计', '极度保守', '适度', '激进', '疯子'];

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------

export function initPanels() {
    loadPersistedTheme();
    _applyTheme(store.theme);
    _initSidebarNav();
    _initThemeToggle();
    _initContextPanel();
    _initPipelineBar();
    _initChatInput();
    _bindStoreSubscriptions();

    // SSE connect is now deferred — called from index.html after session init
}


// ---------------------------------------------------------------------------
// Sidebar Navigation
// ---------------------------------------------------------------------------

function _initSidebarNav() {
    const navItems = document.querySelectorAll('.sidebar-nav-item[data-panel]');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const panel = item.dataset.panel;
            store.activePanel = panel;
        });
    });

    // React to store changes
    subscribe('activePanel', (newPanel) => {
        // Update nav items
        navItems.forEach(item => {
            item.classList.toggle('active', item.dataset.panel === newPanel);
        });

        // Update tab panels
        document.querySelectorAll('.tab-panel').forEach(p => {
            p.classList.toggle('active', p.id === `panel-${newPanel}`);
        });

        // Update main title
        const titleEl = document.getElementById('mainTitle');
        if (titleEl) titleEl.textContent = PANEL_TITLES[newPanel] || newPanel;
    });
}


// ---------------------------------------------------------------------------
// Theme Toggle
// ---------------------------------------------------------------------------

function _initThemeToggle() {
    const btn = document.getElementById('btnThemeToggle');
    if (!btn) return;

    btn.addEventListener('click', () => {
        store.theme = store.theme === 'dark' ? 'light' : 'dark';
    });

    subscribe('theme', (newTheme) => {
        _applyTheme(newTheme);
        btn.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    });

    // Set initial icon
    btn.textContent = store.theme === 'dark' ? '🌙' : '☀️';
}

function _applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
}


// ---------------------------------------------------------------------------
// Context Panel
// ---------------------------------------------------------------------------

function _initContextPanel() {
    const panel = document.getElementById('contextPanel');
    const btnToggle = document.getElementById('btnToggleContext');
    const btnClose = document.getElementById('btnCloseContext');

    if (!panel) return;

    const toggleCtx = () => {
        panel.classList.toggle('collapsed');
    };

    if (btnToggle) btnToggle.addEventListener('click', toggleCtx);
    if (btnClose) btnClose.addEventListener('click', () => panel.classList.add('collapsed'));
}


// ---------------------------------------------------------------------------
// Pipeline Bar
// ---------------------------------------------------------------------------

function _initPipelineBar() {
    const bar = document.getElementById('ctxPipelineBar');
    const summary = document.getElementById('ctxPipelineSummary');
    if (!bar || !summary) return;

    summary.addEventListener('click', () => {
        bar.classList.toggle('expanded');
    });
}


// ---------------------------------------------------------------------------
// Chat Input Auto-Resize
// ---------------------------------------------------------------------------

function _initChatInput() {
    const textarea = document.getElementById('chatInput');
    if (!textarea) return;

    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    });

    // Enter to send, Shift+Enter for newline
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.getElementById('btnSendChat')?.click();
        }
    });
}


// ---------------------------------------------------------------------------
// Store Subscriptions (reactive UI updates)
// ---------------------------------------------------------------------------

function _bindStoreSubscriptions() {

    // --- Approval badge ---
    subscribe('pendingCount', (count) => {
        const badge = document.getElementById('approvalBadge');
        if (!badge) return;
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : String(count);
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    });

    // --- Safety mode badge ---
    subscribe('safetyMode', (mode) => {
        _updateModeBadge('modeBadge', mode);
        _updateModeBadge('adminModeBadge', mode);
        _updateModeSwitcher(mode);
        _updateModeDescription(mode);
    });

    // --- Pipeline stages ---
    subscribe('pipelineStages', (stages) => {
        _renderPipelineStages(stages);
    });

    // --- Current task ---
    subscribe('currentTask', (task) => {
        _updateContextTask(task);
    });
}


// ---------------------------------------------------------------------------
// Mode Badge Update
// ---------------------------------------------------------------------------

function _updateModeBadge(elementId, mode) {
    const el = document.getElementById(elementId);
    if (!el) return;
    // Remove old mode classes
    for (let i = 0; i <= 4; i++) el.classList.remove(`mode-${i}`);
    el.classList.add(`mode-${mode}`);
    el.textContent = MODE_NAMES[mode] || `MODE_${mode}`;
}

function _updateModeSwitcher(mode) {
    const switcher = document.getElementById('safetySwitcher');
    if (!switcher) return;
    switcher.querySelectorAll('.safety-switcher-option').forEach(opt => {
        opt.classList.toggle('active', opt.dataset.mode === String(mode));
    });
}

function _updateModeDescription(mode) {
    const el = document.getElementById('modeDescription');
    if (!el) return;
    const descriptions = [
        '强制锁定只读连接，纯诊断无写入权限',
        '仅自动放行L0，任何写操作强制人工审批',
        '放行L0/L1，L2及以上强制人工确认并审核回滚脚本',
        '放行L0/L1/L2，仅拦截L3/L4破坏性操作',
        '全量放行L0-L4，无阻断自动执行（需管理员密码）',
    ];
    el.textContent = descriptions[mode] || '';
}


// ---------------------------------------------------------------------------
// Pipeline Stages Render
// ---------------------------------------------------------------------------

const STAGE_ICONS = {
    pending: '○',
    running: '◉',
    passed: '✓',
    failed: '✗',
    skipped: '−',
    blocked: '⏸',
};

function _renderPipelineStages(stages) {
    const container = document.getElementById('ctxPipelineStages');
    const statusEl = document.getElementById('ctxPipelineStatus');
    if (!container) return;

    if (!stages || stages.length === 0) {
        container.innerHTML = '';
        if (statusEl) statusEl.textContent = '等待任务';
        return;
    }

    // Summary text
    const running = stages.find(s => s.status === 'running');
    const failed = stages.find(s => s.status === 'failed');
    const allPassed = stages.every(s => s.status === 'passed' || s.status === 'skipped');

    if (statusEl) {
        if (failed) statusEl.textContent = `❌ ${failed.stage} 失败`;
        else if (running) statusEl.textContent = `⏳ ${running.stage}`;
        else if (allPassed) statusEl.textContent = '✅ 全部通过';
        else statusEl.textContent = '等待中';
    }

    // Render individual stages
    container.innerHTML = stages.map(s => `
        <div class="pipeline-stage ${s.status}">
            <span class="pipeline-stage-icon">${STAGE_ICONS[s.status] || '○'}</span>
            <span class="pipeline-stage-name">${_escapeHtml(s.stage)}</span>
            <span class="pipeline-stage-time">${s.duration_ms != null ? s.duration_ms + 'ms' : ''}</span>
        </div>
    `).join('');
}


// ---------------------------------------------------------------------------
// Context Panel Task Update
// ---------------------------------------------------------------------------

function _updateContextTask(task) {
    const setTextContent = (id, text) => {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    };

    if (!task) {
        setTextContent('ctxTaskId', '-');
        setTextContent('ctxIntent', '-');
        setTextContent('ctxInstance', '-');
        setTextContent('ctxSourceMessage', '-');
        setTextContent('ctxValidationContent', '-');
        const riskEl = document.getElementById('ctxRiskLevel');
        if (riskEl) riskEl.textContent = '-';
        const generatedBlock = document.getElementById('ctxGeneratedSqlBlock');
        const generatedEmpty = document.getElementById('ctxGeneratedSqlEmpty');
        if (generatedBlock) generatedBlock.style.display = 'none';
        if (generatedEmpty) generatedEmpty.style.display = 'block';
        const rollbackBlock = document.getElementById('ctxRollbackBlock');
        const rollbackEmpty = document.getElementById('ctxRollbackEmpty');
        if (rollbackBlock) rollbackBlock.style.display = 'none';
        if (rollbackEmpty) rollbackEmpty.style.display = 'block';
        return;
    }

    const intentText = typeof task.intent === 'object'
        ? (task.intent?.label || task.intent?.intent || '-')
        : (task.intent || '-');
    const generated = task.generated_sql_meta || task.generated_sql || null;

    setTextContent('ctxTaskId', task.task_id || '-');
    setTextContent('ctxIntent', intentText);
    setTextContent('ctxInstance', task.instance_name || '-');
    setTextContent('ctxSourceMessage', task.source_message || '-');

    // Risk level badge
    const riskEl = document.getElementById('ctxRiskLevel');
    if (riskEl && task.risk_level != null) {
        riskEl.innerHTML = `<span class="risk-badge risk-L${task.risk_level}">L${task.risk_level}</span>`;
    } else if (riskEl) {
        riskEl.textContent = '-';
    }

    // Generated SQL
    const generatedBlock = document.getElementById('ctxGeneratedSqlBlock');
    const generatedEmpty = document.getElementById('ctxGeneratedSqlEmpty');
    const generatedSql = document.getElementById('ctxGeneratedSql');
    if (generated && generated.sql) {
        if (generatedBlock) generatedBlock.style.display = 'block';
        if (generatedEmpty) generatedEmpty.style.display = 'none';
        if (generatedSql) generatedSql.textContent = generated.sql;
    } else {
        if (generatedBlock) generatedBlock.style.display = 'none';
        if (generatedEmpty) generatedEmpty.style.display = 'block';
    }

    // Validation
    const validEl = document.getElementById('ctxValidationContent');
    if (validEl) {
        validEl.textContent = task.validation || '-';
    }

    // Rollback SQL
    const rollbackBlock = document.getElementById('ctxRollbackBlock');
    const rollbackEmpty = document.getElementById('ctxRollbackEmpty');
    const rollbackSql = document.getElementById('ctxRollbackSql');
    if (task.rollback_sql) {
        if (rollbackBlock) rollbackBlock.style.display = 'block';
        if (rollbackEmpty) rollbackEmpty.style.display = 'none';
        if (rollbackSql) rollbackSql.textContent = task.rollback_sql;
    } else {
        if (rollbackBlock) rollbackBlock.style.display = 'none';
        if (rollbackEmpty) rollbackEmpty.style.display = 'block';
    }
}


// ---------------------------------------------------------------------------
// Toast System
// ---------------------------------------------------------------------------

let _toastId = 0;

/**
 * Show a toast notification.
 * @param {string} message
 * @param {'success'|'error'|'warning'|'info'} type
 * @param {number} duration  Auto-dismiss in ms (0 = sticky)
 */
export function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const id = ++_toastId;
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.id = `toast-${id}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || ''}</span>
        <span class="toast-message">${_escapeHtml(message)}</span>
        <span class="toast-close" onclick="this.parentElement.remove()">×</span>
    `;

    container.appendChild(toast);

    if (duration > 0) {
        setTimeout(() => toast.remove(), duration);
    }
}


// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

function _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

export {
    PANEL_TITLES,
    MODE_NAMES,
    MODE_LABELS,
};
