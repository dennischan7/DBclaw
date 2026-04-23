/**
 * DBA SafeGuard WebUI — Reactive State Store (Proxy + EventTarget Pub-Sub)
 *
 * Usage:
 *   import { store, subscribe, subscribeAny, dispatch } from './dba_store.js';
 *
 *   subscribe('safetyMode', (newVal, oldVal) => { ... });
 *   subscribeAny((key, newVal, oldVal) => { ... });
 *
 *   store.safetyMode = 2;          // triggers subscribed callbacks
 *   dispatch('task:updated', data); // custom event
 */

// ---------------------------------------------------------------------------
// Default State
// ---------------------------------------------------------------------------

const DEFAULT_STATE = {
    // SSE connection
    connected: false,
    reconnecting: false,

    // Auth
    userId: 'webui_user',
    userRole: 2,  // 0=READONLY, 1=DEVELOPER, 2=ADMIN

    // Active panel
    activePanel: 'chat',

    // Safety mode (0-4)
    safetyMode: 2,
    modeLocked: false,

    // Current instance
    currentInstance: 'pg_test',
    instanceDialect: 'postgresql',
    instanceOnline: true,

    // Current task
    currentTaskId: null,
    currentTask: null,
    pipelineStages: [],

    // Approval queue
    pendingApprovals: [],
    pendingCount: 0,

    // Theme
    theme: 'dark',

    // Chat
    chatMessages: [],
    chatLoading: false,
    currentConversationId: null,
    conversations: [],

    // Dashboard stats (cached)
    dashboardStats: null,

    // Audit
    auditLogs: [],
    auditPage: 1,
    auditPageSize: 50,
    auditTotal: 0,
};


// ---------------------------------------------------------------------------
// Key-specific listeners
// ---------------------------------------------------------------------------

/** @type {Map<string, Set<Function>>} */
const _keyListeners = new Map();

/** @type {Set<Function>} */
const _anyListeners = new Set();


/**
 * Subscribe to changes on a specific store key.
 * @param {string} key
 * @param {(newVal: any, oldVal: any) => void} cb
 * @returns {() => void} Unsubscribe function
 */
export function subscribe(key, cb) {
    if (!_keyListeners.has(key)) {
        _keyListeners.set(key, new Set());
    }
    _keyListeners.get(key).add(cb);
    return () => _keyListeners.get(key)?.delete(cb);
}


/**
 * Subscribe to any key change.
 * @param {(key: string, newVal: any, oldVal: any) => void} cb
 * @returns {() => void} Unsubscribe function
 */
export function subscribeAny(cb) {
    _anyListeners.add(cb);
    return () => _anyListeners.delete(cb);
}


// ---------------------------------------------------------------------------
// Custom Event Bus (for non-state events like 'task:updated')
// ---------------------------------------------------------------------------

const _eventTarget = new EventTarget();

/**
 * Dispatch a custom event.
 * @param {string} eventName
 * @param {any} data
 */
export function dispatch(eventName, data) {
    _eventTarget.dispatchEvent(new CustomEvent(eventName, { detail: data }));
}

/**
 * Listen for a custom event.
 * @param {string} eventName
 * @param {(data: any) => void} cb
 * @returns {() => void} Unsubscribe function
 */
export function on(eventName, cb) {
    const handler = (e) => cb(e.detail);
    _eventTarget.addEventListener(eventName, handler);
    return () => _eventTarget.removeEventListener(eventName, handler);
}


// ---------------------------------------------------------------------------
// Proxy Store
// ---------------------------------------------------------------------------

function _notify(key, newVal, oldVal) {
    // Key-specific listeners
    const listeners = _keyListeners.get(key);
    if (listeners) {
        for (const cb of listeners) {
            try { cb(newVal, oldVal); }
            catch (e) { console.error(`[Store] Listener error on '${key}':`, e); }
        }
    }
    // Any-key listeners
    for (const cb of _anyListeners) {
        try { cb(key, newVal, oldVal); }
        catch (e) { console.error('[Store] Any-listener error:', e); }
    }
}

const _raw = { ...DEFAULT_STATE };

export const store = new Proxy(_raw, {
    set(target, key, value) {
        const oldVal = target[key];
        if (oldVal === value) return true;  // No-op if same value
        target[key] = value;
        _notify(key, value, oldVal);
        return true;
    },
    get(target, key) {
        return target[key];
    },
});


// ---------------------------------------------------------------------------
// Batch update helper
// ---------------------------------------------------------------------------

/**
 * Update multiple store keys at once (notifications still fire per key).
 * @param {Record<string, any>} updates
 */
export function batchUpdate(updates) {
    for (const [key, value] of Object.entries(updates)) {
        store[key] = value;
    }
}


// ---------------------------------------------------------------------------
// Persistence (theme only, via localStorage)
// ---------------------------------------------------------------------------

const THEME_KEY = 'dba-safeguard-theme';

export function loadPersistedTheme() {
    try {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved === 'light' || saved === 'dark') {
            store.theme = saved;
        }
    } catch { /* localStorage unavailable */ }
}

subscribe('theme', (newTheme) => {
    try { localStorage.setItem(THEME_KEY, newTheme); }
    catch { /* ignore */ }
});


export default store;
