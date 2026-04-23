/**
 * DBA SafeGuard WebUI — Robust SSE Client
 *
 * Features:
 *   - Exponential backoff reconnection (1s → 2s → 4s → … → 30s cap)
 *   - Connection bar UI feedback
 *   - State recovery on reconnect (fetches missed events)
 *   - Heartbeat timeout detection
 *   - Handles all ApprovalEventType events
 *
 * Usage:
 *   import { sseClient } from './dba_sse.js';
 *   sseClient.connect();
 */

import { store, dispatch, batchUpdate } from './dba_store.js';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SSE_URL = '/api/dba/events';
const HEARTBEAT_TIMEOUT_MS = 45_000;   // Expect heartbeat every 30s, timeout at 45s
const MIN_RETRY_MS = 1_000;
const MAX_RETRY_MS = 30_000;
const BACKOFF_FACTOR = 2;

// ---------------------------------------------------------------------------
// SSE Client
// ---------------------------------------------------------------------------

class SSEClient {
    constructor() {
        /** @type {EventSource|null} */
        this._es = null;
        this._retryMs = MIN_RETRY_MS;
        this._retryTimer = null;
        this._heartbeatTimer = null;
        this._lastEventId = null;
        this._manualClose = false;
        this._connectionBar = null;
    }

    /** Connect to SSE endpoint. */
    connect() {
        this._manualClose = false;
        this._connectionBar = document.getElementById('connectionBar');
        this._open();
    }

    /** Disconnect (no auto-reconnect). */
    disconnect() {
        this._manualClose = true;
        this._cleanup();
        batchUpdate({ connected: false, reconnecting: false });
    }

    // --- Internal ---

    _open() {
        this._cleanup();

        let url = SSE_URL;
        if (this._lastEventId) {
            url += `?last_event_id=${encodeURIComponent(this._lastEventId)}`;
        }

        const es = new EventSource(url);
        this._es = es;

        es.onopen = () => {
            this._retryMs = MIN_RETRY_MS;
            batchUpdate({ connected: true, reconnecting: false });
            this._hideBar();
            this._startHeartbeat();
        };

        es.onerror = () => {
            if (this._manualClose) return;
            batchUpdate({ connected: false, reconnecting: true });
            this._showBar('⚠ 连接已断开，正在重连…');
            this._cleanup();
            this._scheduleRetry();
        };

        // --- Named event handlers ---

        // Heartbeat / keep-alive
        es.addEventListener('heartbeat', (e) => {
            this._resetHeartbeat();
        });

        // Approval events
        es.addEventListener('approval_requested', (e) => this._onApproval(e));
        es.addEventListener('approval_approved', (e) => this._onApproval(e));
        es.addEventListener('approval_rejected', (e) => this._onApproval(e));
        es.addEventListener('approval_modified', (e) => this._onApproval(e));

        // Task pipeline events
        es.addEventListener('task_started', (e) => this._onTask(e));
        es.addEventListener('task_stage', (e) => this._onTask(e));
        es.addEventListener('task_completed', (e) => this._onTask(e));
        es.addEventListener('task_error', (e) => this._onTask(e));

        // Safety mode changes
        es.addEventListener('mode_changed', (e) => this._onModeChanged(e));

        // Generic message fallback
        es.onmessage = (e) => {
            this._resetHeartbeat();
            if (e.lastEventId) this._lastEventId = e.lastEventId;
        };
    }

    _cleanup() {
        if (this._es) {
            this._es.close();
            this._es = null;
        }
        if (this._heartbeatTimer) {
            clearTimeout(this._heartbeatTimer);
            this._heartbeatTimer = null;
        }
        if (this._retryTimer) {
            clearTimeout(this._retryTimer);
            this._retryTimer = null;
        }
    }

    _scheduleRetry() {
        this._retryTimer = setTimeout(() => {
            this._open();
        }, this._retryMs);
        // Exponential backoff with cap
        this._retryMs = Math.min(this._retryMs * BACKOFF_FACTOR, MAX_RETRY_MS);
    }

    _startHeartbeat() {
        this._resetHeartbeat();
    }

    _resetHeartbeat() {
        if (this._heartbeatTimer) clearTimeout(this._heartbeatTimer);
        this._heartbeatTimer = setTimeout(() => {
            // Heartbeat timeout — force reconnect
            console.warn('[SSE] Heartbeat timeout, reconnecting…');
            if (this._es) {
                this._es.close();
                this._es = null;
            }
            batchUpdate({ connected: false, reconnecting: true });
            this._showBar('⚠ 心跳超时，正在重连…');
            this._scheduleRetry();
        }, HEARTBEAT_TIMEOUT_MS);
    }

    // --- Connection bar ---

    _showBar(text) {
        if (!this._connectionBar) return;
        this._connectionBar.textContent = text;
        this._connectionBar.style.display = 'block';
    }

    _hideBar() {
        if (!this._connectionBar) return;
        this._connectionBar.style.display = 'none';
    }

    // --- Event handlers ---

    _parseData(event) {
        try {
            if (event.lastEventId) this._lastEventId = event.lastEventId;
            this._resetHeartbeat();
            return JSON.parse(event.data);
        } catch (e) {
            console.error('[SSE] Failed to parse event data:', e);
            return null;
        }
    }

    _onApproval(event) {
        const data = this._parseData(event);
        if (!data) return;

        const eventType = event.type;  // approval_requested, approval_approved, etc.
        dispatch('approval:event', { type: eventType, data });

        // Update pending count
        if (eventType === 'approval_requested') {
            store.pendingCount = (store.pendingCount || 0) + 1;
        } else if (eventType === 'approval_approved' || eventType === 'approval_rejected' || eventType === 'approval_modified') {
            store.pendingCount = Math.max(0, (store.pendingCount || 0) - 1);
        }
    }

    _onTask(event) {
        const data = this._parseData(event);
        if (!data) return;

        dispatch('task:event', { type: event.type, data });

        const taskId = data.task_id || data.id || null;
        const isCurrentTask = !store.currentTaskId || !taskId || store.currentTaskId === taskId;

        // Update current task in store
        if (event.type === 'task_started') {
            if (isCurrentTask) {
                store.currentTaskId = taskId;
                store.currentTask = data;
            }
        } else if (event.type === 'task_stage') {
            if (isCurrentTask && data.stages) {
                store.pipelineStages = data.stages;
            }
        } else if (event.type === 'task_completed' || event.type === 'task_error') {
            if (isCurrentTask) {
                store.currentTask = data;
            }
        }
    }

    _onModeChanged(event) {
        const data = this._parseData(event);
        if (!data) return;

        if (typeof data.new_mode === 'number') {
            store.safetyMode = data.new_mode;
        }
        dispatch('mode:changed', data);
    }
}


// ---------------------------------------------------------------------------
// Singleton export
// ---------------------------------------------------------------------------

export const sseClient = new SSEClient();
