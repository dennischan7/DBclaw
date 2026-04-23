# Phase 8 — DBA SafeGuard Web UI 详细开发计划

> **项目**: DBA SafeGuard Web UI (hermes-webui 扩展)
> **分支**: `dev` → `feature/webui`
> **设计系统**: 参见 [`DESIGN.md`](DESIGN.md)（遵循 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 标准格式）
> **预估工期**: 3 周（Phase A-G）
> **版本**: v2 — 含架构健壮性补丁（状态管理 / SSE 竞态修复 / 安全左移 / 性能护栏）

---

## 目录

1. [架构概览](#1-架构概览)
2. [技术选型](#2-技术选型)
3. [文件清单](#3-文件清单)
4. [Phase A — 基础框架搭建 (Day 1-3)](#phase-a--基础框架搭建-day-1-3)
5. [Phase B — 后端 API 桥接层 + 安全中间件 (Day 4-6)](#phase-b--后端-api-桥接层--安全中间件-day-4-6)
6. [Phase C — 对话页面 (Day 7-10)](#phase-c--对话页面-day-7-10)
7. [Phase D — 观测大盘 (Day 11-13)](#phase-d--观测大盘-day-11-13)
8. [Phase E — 审计日志 (Day 14-15)](#phase-e--审计日志-day-14-15)
9. [Phase F — 管理配置 (Day 16-18)](#phase-f--管理配置-day-16-18)
10. [Phase G — 集成测试与打磨 (Day 19-21)](#phase-g--集成测试与打磨-day-19-21)
11. [设计规范速查](#11-设计规范速查)
12. [约束与边界](#12-约束与边界)

---

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Browser (ES6 Modules, Vanilla JS)                │
│                                                                     │
│  dba_store.js ←──── Proxy 响应式状态中心 (Pub-Sub)                  │
│       ↓ subscribe                                                   │
│  ┌──────────┬───────────────────────┬──────────────┐                │
│  │ Sidebar  │ Main Panel            │ Context Panel│   dba_panels.js│
│  │ 240px    │ (Chat/Dashboard/      │ 280px        │   dba_chat.js  │
│  │          │  Audit/Admin)         │ (collapsible)│   dba_charts.js│
│  └──────────┴───────────────────────┴──────────────┘                │
│       ↓ fetch() + SSE                                               │
│  dba_sse.js ←──── 健壮 SSE 客户端 (断线重连 + 状态恢复)             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                      hermes-webui (Python)                          │
│  routes.py ──→ dba_routes.py ──→ dba_bridge.py                     │
│  (10 lines)   (REST endpoints)   (import plugin modules directly)  │
│                    ↑                                                │
│           auth_middleware.py ← 统一鉴权 + @admin_required           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│              .hermes/plugins/dba-safeguard/ (existing)              │
│  engine/dba_loop.py    security/approval_manager.py                 │
│  security/risk_rules.py  security/safety_mode.py                    │
│  tools/audit_logger.py   tools/db_connector.py                      │
│  skill_engine/skill_manager.py  memory/dba_memory_provider.py       │
└─────────────────────────────────────────────────────────────────────┘
```

**关键设计决策：**
- hermes-webui 的 Python 后端**直接 import** DBA 插件模块，无需另建 HTTP 微服务
- 前端使用 **`<script type="module">`** 进行 ES6 模块化，避免全局变量污染
- **dba_store.js** 提供 Proxy 响应式全局状态，数据驱动视图更新（Pub-Sub 模式）
- **dba_sse.js** 封装健壮的 SSE 客户端，含断线重连、状态恢复、UI 反馈
- **安全中间件左移至 Phase B**，API 鉴权在设计路由时同步实现，而非最后打磨
- 图表库用 Chart.js（CDN 引入），无构建步骤
- SSE（Server-Sent Events）用于实时 Pipeline 进度和审批事件推送

---

## 2. 技术选型

| 层 | 技术 | 理由 |
|---|------|------|
| 前端框架 | Vanilla JS + ES6 Modules | 与 hermes-webui 保持一致，零构建步骤，`<script type="module">` 避免全局污染 |
| 状态管理 | Proxy + EventTarget (dba_store.js) | 极简响应式 Pub-Sub，替代跨文件 DOM 面条代码 |
| CSS | 原生 CSS Variables | DESIGN.md 定义的 token 直接映射 CSS Variables |
| 图表 | Chart.js 4.x (CDN) | 轻量、暗色主题支持好 |
| 实时通信 | SSE (封装 EventSource) | Pipeline 进度 + 审批事件推送，带状态恢复 |
| 后端路由 | Python http.server 扩展 | hermes-webui 模式 if/elif 路由 |
| 安全中间件 | auth_middleware.py | 统一鉴权装饰器，Phase B 同步实现 |
| 数据导出 | CSV (后端生成) | 审计日志批量导出，无 Excel 依赖 |
| 主题切换 | CSS Variables + `data-theme` 属性 | 暗色/亮色一键切换 |

---

## 3. 文件清单

### 新增文件 (9)

| 文件 | 行数估算 | 用途 |
|------|---------|------|
| `dba_bridge.py` | ~400 | 后端桥接层 — import 插件模块，提供统一 Python API |
| `dba_routes.py` | ~350 | HTTP 路由 — REST endpoints + SSE streams |
| `auth_middleware.py` | ~80 | **[v2 新增]** 鉴权中间件 — session 校验 + `@admin_required` 装饰器 + CSRF |
| `static/js/dba_store.js` | ~120 | **[v2 新增]** 全局状态管理 — Proxy 响应式 + EventTarget Pub-Sub |
| `static/js/dba_sse.js` | ~150 | **[v2 新增]** 健壮 SSE 客户端 — 断线重连 + 状态恢复 + UI 反馈 |
| `static/js/dba_panels.js` | ~500 | 前端面板管理 — 三栏布局、Tab 切换、面板渲染 |
| `static/js/dba_chat.js` | ~600 | 对话面板 — 消息渲染、SQL 高亮、审批卡片、Pipeline |
| `static/js/dba_charts.js` | ~300 | 图表组件 — Chart.js 封装、大盘统计渲染 |
| `tests/test_dba_api.py` | ~250 | API 测试 — dba_bridge + dba_routes + auth 单元测试 |

### 修改文件 (5)

| 文件 | 改动量 | 改动内容 |
|------|-------|---------|
| `routes.py` | +10 行 | 添加 `/api/dba/*` 路由分发到 dba_routes |
| `streaming.py` | +30 行 | 添加 DBA Pipeline SSE 流支持 |
| `templates/index.html` | +25 行 | 添加 DBA 面板 DOM 骨架 + `<script type="module">` JS 引入 |
| `static/js/panels.js` | +5 行 | switchPanel() 添加 DBA 面板 case |
| `static/css/style.css` | +200 行 | DBA 组件样式（遵循 DESIGN.md） |

---

## Phase A — 基础框架搭建 (Day 1-3)

### A1. Fork & 配置 hermes-webui

**目标**: 将 hermes-webui 克隆到本地并验证可运行

```bash
# 克隆到 .hermes 下
cd ~/.hermes
git clone https://github.com/nesquena/hermes-webui.git webui
cd webui
pip install -r requirements.txt
python server.py  # 验证 http://localhost:8787 可访问
```

**验收标准**: 浏览器打开 `http://localhost:8787`，原版 hermes-webui 正常工作

### A2. 注入 DESIGN.md CSS Variables

**文件**: `static/css/style.css`

将 DESIGN.md 中的 Color Palette 和 Typography 转化为 CSS Variables：

```css
/* ===== DBA SafeGuard Design Tokens ===== */
:root[data-theme="dark"], :root {
    /* Brand */
    --brand-primary: #5B6FE6;
    --brand-primary-hover: #6E80F0;
    --brand-primary-muted: rgba(91, 111, 230, 0.15);

    /* Risk Levels */
    --risk-L0: #27AE60;
    --risk-L1: #5B6FE6;
    --risk-L2: #E6A817;
    --risk-L3: #E67E22;
    --risk-L4: #E74C3C;

    /* Surfaces */
    --bg-page: #0D1117;
    --bg-surface: #161B22;
    --bg-surface-elevated: #1C2128;
    --bg-surface-hover: #21262D;
    --bg-input: #0D1117;

    /* Borders */
    --border-primary: #30363D;
    --border-secondary: #21262D;
    --border-focus: #5B6FE6;

    /* Text */
    --text-primary: #E6EDF3;
    --text-secondary: #8B949E;
    --text-tertiary: #6E7681;

    /* Typography */
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

    /* Spacing */
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 20px;
    --space-6: 24px;
    --space-8: 32px;
}

:root[data-theme="light"] {
    --bg-page: #FFFFFF;
    --bg-surface: #F6F8FA;
    --bg-surface-elevated: #FFFFFF;
    --bg-surface-hover: #F3F4F6;
    --bg-input: #FFFFFF;
    --border-primary: #D0D7DE;
    --text-primary: #1F2328;
    --text-secondary: #656D76;
    --text-tertiary: #8C959F;
}
```

**验收标准**: 暗色/亮色两套变量定义完成，`data-theme` 切换生效

### A3. 三栏布局骨架

**文件**: `templates/index.html` + `static/css/style.css`

在 index.html 中添加 DBA 面板 DOM（注意使用 ES6 Module 引入）：

```html
<div id="dba-panel" class="panel-view" style="display:none">
  <div class="dba-connection-bar" id="dba-connection-bar" style="display:none">
    <!-- SSE 断线重连提示条 -->
    <span>⚠ 连接断开，重连中...</span>
  </div>
  <div class="dba-layout">
    <aside class="dba-sidebar"><!-- A5 填充 --></aside>
    <main class="dba-main"><!-- Phase C-F 填充 --></main>
    <aside class="dba-context"><!-- Phase C 填充 --></aside>
  </div>
</div>

<!-- ES6 Module 引入 — 避免全局变量污染 -->
<script type="module" src="/static/js/dba_store.js"></script>
<script type="module" src="/static/js/dba_sse.js"></script>
<script type="module" src="/static/js/dba_panels.js"></script>
<script type="module" src="/static/js/dba_chat.js"></script>
<script type="module" src="/static/js/dba_charts.js"></script>
```

CSS 三栏布局：

```css
.dba-layout {
    display: flex;
    height: 100vh;
    background: var(--bg-page);
    color: var(--text-primary);
    font-family: var(--font-sans);
}
.dba-sidebar { width: 240px; border-right: 1px solid var(--border-primary); }
.dba-main { flex: 1; min-width: 480px; overflow-y: auto; }
.dba-context { width: 280px; border-left: 1px solid var(--border-primary); }
.dba-context.collapsed { display: none; }

/* SSE 断线提示条 */
.dba-connection-bar {
    background: var(--risk-L3);
    color: #fff;
    text-align: center;
    padding: 4px 0;
    font-size: 12px;
    font-weight: 500;
}
```

**验收标准**: 三栏布局正确渲染，左右栏固定宽度，中栏自适应

### A4. 主题切换功能

```javascript
// dba_panels.js
function toggleTheme() {
    const theme = document.documentElement.getAttribute('data-theme');
    const newTheme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('dba-theme', newTheme);
}
// 初始化时读取 localStorage
document.documentElement.setAttribute('data-theme',
    localStorage.getItem('dba-theme') || 'dark');
```

**验收标准**: 点击切换按钮，暗色/亮色主题即时切换，刷新后保持

### A5. 左侧导航栏

实现 Sidebar 内容（参见 DESIGN.md Layout Principles — Sidebar）：
- 品牌标识 + 折叠按钮
- 4 个导航 Tab（Chat / Dashboard / Audit / Admin）
- 会话列表（搜索框 + 时间分组）
- 底部：实例选择器 + 安全模式显示 + 版本号

**验收标准**: 导航 Tab 点击切换中栏内容，会话列表可搜索

### A6. 全局状态管理模块 (dba_store.js) ⚡ v2 新增

**动机**: 没有 React/Vue 框架时，多个 JS 文件（dba_chat.js、dba_charts.js、dba_panels.js）之间同步共享状态（当前实例、安全模式、未读审批数、Pipeline 进度）极易演变成 `document.getElementById` 面条代码。用 Proxy + EventTarget 实现极简响应式 Pub-Sub，让**数据驱动视图**。

**文件**: `static/js/dba_store.js` (~120 行)

```javascript
// dba_store.js — 极简 Proxy 响应式全局状态
const _emitter = new EventTarget();

const _state = {
    // === 连接 ===
    currentInstance: null,         // 当前选中的数据库实例名
    instances: [],                 // 可用实例列表

    // === 安全 ===
    safetyMode: { mode: 2, name: '适度', locked: false },
    userRole: 'developer',         // 'readonly' | 'developer' | 'admin'

    // === 对话 ===
    activeTaskId: null,            // 当前活跃任务 ID
    pipelineStages: {},            // { taskId: { stages: [...], summary: '...' } }

    // === 审批 ===
    pendingApprovals: [],          // 未处理审批列表
    unreadApprovalCount: 0,        // 侧栏 badge 数字

    // === 连接状态 ===
    sseConnected: true,            // SSE 连接状态
};

// Proxy 拦截 set，自动触发事件
const store = new Proxy(_state, {
    set(target, key, value) {
        const old = target[key];
        target[key] = value;
        if (old !== value) {
            _emitter.dispatchEvent(new CustomEvent('change', {
                detail: { key, value, old }
            }));
            _emitter.dispatchEvent(new CustomEvent(`change:${key}`, {
                detail: { value, old }
            }));
        }
        return true;
    }
});

// 订阅 API
export function subscribe(key, callback) {
    const handler = (e) => callback(e.detail.value, e.detail.old);
    _emitter.addEventListener(`change:${key}`, handler);
    return () => _emitter.removeEventListener(`change:${key}`, handler);  // 返回 unsubscribe
}

export function subscribeAny(callback) {
    const handler = (e) => callback(e.detail.key, e.detail.value, e.detail.old);
    _emitter.addEventListener('change', handler);
    return () => _emitter.removeEventListener('change', handler);
}

export default store;
```

**使用方式**（其他模块 import）：

```javascript
// dba_panels.js
import store, { subscribe } from './dba_store.js';

// 侧栏审批 badge — 订阅 unreadApprovalCount 变更，自动更新 DOM
subscribe('unreadApprovalCount', (count) => {
    document.getElementById('approval-badge').textContent = count || '';
    document.getElementById('approval-badge').style.display = count > 0 ? 'inline' : 'none';
});

// 安全模式变更 — sidebar 自动同步
subscribe('safetyMode', (mode) => {
    document.getElementById('sidebar-mode').textContent = mode.name;
    document.getElementById('sidebar-mode').className = `mode-badge mode-${mode.mode}`;
});

// 任何模块修改 store 即可触发所有订阅者更新
store.unreadApprovalCount = 3;  // → sidebar badge 自动显示 "3"
store.safetyMode = { mode: 1, name: '保守', locked: false };  // → sidebar 自动更新
```

**核心原则**：
- **单一数据源**: 所有跨模块共享状态集中在 store 中
- **只写 store，不直接操纵 DOM**: 各模块通过 `subscribe()` 注册视图更新回调
- **无框架依赖**: 纯 Proxy + EventTarget，零依赖，< 120 行

**验收标准**:
- 在 dba_chat.js 中修改 `store.currentInstance`，dba_panels.js 的侧栏实例名自动更新
- 在 dba_sse.js 中修改 `store.pendingApprovals`，侧栏 badge 和大盘卡片同步更新

### A7. ES6 Module 化 ⚡ v2 新增

**动机**: 使用 `<script type="module">` 代替传统 `<script src>`，每个 JS 文件都是独立模块作用域，通过 `import/export` 共享，避免全局变量污染。

**规范**:
- 所有新增 JS 文件使用 `export` / `import` 语法
- HTML 中用 `<script type="module">` 引入
- 模块间依赖关系:

```
dba_store.js  ← 无依赖 (纯状态)
     ↑
dba_sse.js    ← import store (更新连接状态、审批列表)
     ↑
dba_panels.js ← import store, subscribe (侧栏、Tab 切换)
dba_chat.js   ← import store, subscribe, SSEClient (对话、Pipeline)
dba_charts.js ← import store, subscribe (大盘图表)
```

- 不破坏 hermes-webui 原有的非 Module 脚本（`panels.js` 等保持不变）

**验收标准**: 浏览器 DevTools Console 无 `Uncaught ReferenceError` 全局变量错误

---

## Phase B — 后端 API 桥接层 + 安全中间件 (Day 4-6)

### B1. auth_middleware.py — 鉴权中间件 ⚡ 安全左移

**动机**: 安全不应在最后打磨阶段（Phase G）才加入。将 CSRF 校验、Admin 权限检查在 API 路由设计时同步实现，作为 Phase B 的第一步。

**文件**: `auth_middleware.py` (~80 行)

```python
import hashlib, hmac, secrets, time, functools
from http.cookies import SimpleCookie

# --- Session 管理 ---
_sessions = {}  # {session_token: {"user_id": str, "role": str, "created": float}}
_csrf_tokens = {}  # {session_token: csrf_token}

def create_session(user_id: str, role: str = "developer") -> str:
    """创建会话，返回 session token"""
    token = secrets.token_urlsafe(32)
    _sessions[token] = {"user_id": user_id, "role": role, "created": time.time()}
    _csrf_tokens[token] = secrets.token_urlsafe(32)
    return token

def get_session(handler) -> dict | None:
    """从请求 Cookie 中提取会话信息"""
    cookie = SimpleCookie(handler.headers.get("Cookie", ""))
    token = cookie.get("dba_session")
    if not token:
        return None
    session = _sessions.get(token.value)
    if session and time.time() - session["created"] < 86400:  # 24h TTL
        return session
    return None

def verify_csrf(handler, body: dict) -> bool:
    """校验 POST 请求中的 CSRF token"""
    cookie = SimpleCookie(handler.headers.get("Cookie", ""))
    token = cookie.get("dba_session")
    if not token:
        return False
    expected = _csrf_tokens.get(token.value)
    return body.get("_csrf") == expected

# --- 装饰器 ---
def require_auth(handler_func):
    """要求已登录会话"""
    @functools.wraps(handler_func)
    def wrapper(handler, *args, **kwargs):
        session = get_session(handler)
        if not session:
            return handler.send_error(401, "未登录")
        kwargs["session"] = session
        return handler_func(handler, *args, **kwargs)
    return wrapper

def admin_required(handler_func):
    """要求 Admin 角色 — 用于安全模式切换、风险规则管理、技能管理等"""
    @functools.wraps(handler_func)
    def wrapper(handler, *args, **kwargs):
        session = get_session(handler)
        if not session:
            return handler.send_error(401, "未登录")
        if session["role"] != "admin":
            return handler.send_error(403, "需要管理员权限")
        kwargs["session"] = session
        return handler_func(handler, *args, **kwargs)
    return wrapper
```

**装饰器应用对照表**:

| 接口类别 | 装饰器 | 示例端点 |
|---------|--------|---------|
| 只读查询 | `@require_auth` | `GET /api/dba/audit`, `GET /api/dba/dashboard/*` |
| 审批操作 | `@require_auth` | `POST /api/dba/approvals/{id}/approve` |
| 任务提交 | `@require_auth` | `POST /api/dba/task` |
| 安全模式 | `@admin_required` | `POST /api/dba/safety-mode` |
| 风险规则 | `@admin_required` | `POST/DELETE /api/dba/risk-rules` |
| 技能管理 | `@admin_required` | `POST /api/dba/skills/{name}/toggle` |
| 实例管理 | `@admin_required` | `POST /api/dba/instances` (添加/删除) |
| SSE 流 | `@require_auth` | `GET /api/dba/stream/*` |

**POST 请求 CSRF 保护**: 所有 POST/DELETE 请求在路由层统一校验 `_csrf` 字段。

**验收标准**: 未登录直接访问 `/api/dba/*` 返回 401；developer 角色访问 admin 接口返回 403

### B2. dba_bridge.py — 插件模块桥接

**核心 API 函数**（每个函数封装一个插件模块调用，返回 dict）：

```python
# === 审批管理 ===
def get_pending_approvals(limit=50) -> list[dict]
def get_approval_stats() -> dict          # {total, pending, approved, rejected, ...}
def approve_request(request_id, reviewer) -> dict
def reject_request(request_id, reviewer, reason) -> dict
def modify_and_approve(request_id, reviewer, modified_sql) -> dict

# === 审计日志 ===
def query_audit_logs(start_time, end_time, user_id, instance, risk_level, op_type, limit, offset) -> dict
    # 返回 {"items": [...], "total": int, "page": int, "per_page": int}
def export_audit_csv(filters) -> str      # 返回 CSV 字符串

# === Pipeline & Task ===
def submit_task(user_message, instance_name, user_id, session_id) -> str  # 返回 task_id
def get_task_status(task_id) -> dict      # DBATask → dict (含全部 stage 状态快照)
def list_tasks(status, session_id, limit) -> list[dict]

# === 安全模式 ===
def get_safety_mode() -> dict             # {mode, mode_name, locked, ...}
def switch_safety_mode(target_mode, admin_password=None) -> dict

# === 风险规则 ===
def list_risk_rules() -> list[dict]       # 硬编码 + 自定义规则
def add_custom_rule(rule) -> dict
def delete_custom_rule(rule_id) -> dict

# === 连接管理 ===
def list_instances() -> list[dict]
def get_instance_status(name) -> dict     # 连通性检测

# === 技能管理 ===
def list_skills() -> list[dict]
def toggle_skill(skill_name, enabled) -> dict

# === 大盘统计 ===
def get_dashboard_stats() -> dict         # 聚合统计数据
def get_execution_trend(days=7) -> list   # 按天聚合的执行趋势
def get_risk_distribution() -> dict       # L0-L4 分布
```

**实现要点**：
- 每个函数用 `try/except` 包裹，失败返回 `{"error": str(e)}`
- `submit_task()` 启动后台线程运行 `DBAPipeline.run()`，通过 callback 推送 SSE 事件
- `get_task_status()` 返回**全量阶段快照**（用于 SSE 状态恢复）
- 所有函数幂等，无副作用（除了 approve/reject/submit）
- `query_audit_logs()` 返回分页格式 `{items, total, page, per_page}`，不返回全量

### B3. dba_routes.py — HTTP 路由

| Method | Endpoint | 装饰器 | Handler | 说明 |
|--------|----------|--------|---------|------|
| POST | `/api/dba/auth/login` | 无 | `login()` | 登录（admin_password 校验） |
| GET | `/api/dba/auth/me` | `@require_auth` | `get_me()` | 当前用户信息 + CSRF token |
| GET | `/api/dba/approvals/pending` | `@require_auth` | `get_pending_approvals()` | 待审批列表 |
| GET | `/api/dba/approvals/stats` | `@require_auth` | `get_approval_stats()` | 审批统计 |
| POST | `/api/dba/approvals/{id}/approve` | `@require_auth` | `approve_request()` | 通过审批 |
| POST | `/api/dba/approvals/{id}/reject` | `@require_auth` | `reject_request()` | 驳回审批 (body: reason) |
| POST | `/api/dba/approvals/{id}/modify` | `@require_auth` | `modify_and_approve()` | 修改后执行 (body: sql) |
| GET | `/api/dba/audit` | `@require_auth` | `query_audit_logs()` | 审计日志 (query: filters + page) |
| GET | `/api/dba/audit/export` | `@require_auth` | `export_audit_csv()` | 导出 CSV |
| POST | `/api/dba/task` | `@require_auth` | `submit_task()` | 提交任务 |
| GET | `/api/dba/task/{id}` | `@require_auth` | `get_task_status()` | 查询任务状态 |
| GET | `/api/dba/tasks` | `@require_auth` | `list_tasks()` | 任务列表 |
| GET | `/api/dba/safety-mode` | `@require_auth` | `get_safety_mode()` | 当前安全模式 |
| POST | `/api/dba/safety-mode` | `@admin_required` | `switch_safety_mode()` | 切换安全模式 |
| GET | `/api/dba/risk-rules` | `@require_auth` | `list_risk_rules()` | 风险规则列表 |
| POST | `/api/dba/risk-rules` | `@admin_required` | `add_custom_rule()` | 添加自定义规则 |
| DELETE | `/api/dba/risk-rules/{id}` | `@admin_required` | `delete_custom_rule()` | 删除规则 |
| GET | `/api/dba/instances` | `@require_auth` | `list_instances()` | 数据库实例列表 |
| GET | `/api/dba/instances/{name}/status` | `@require_auth` | `get_instance_status()` | 实例连通性 |
| GET | `/api/dba/skills` | `@require_auth` | `list_skills()` | 技能列表 |
| POST | `/api/dba/skills/{name}/toggle` | `@admin_required` | `toggle_skill()` | 启用/禁用技能 |
| GET | `/api/dba/dashboard/stats` | `@require_auth` | `get_dashboard_stats()` | 大盘统计 |
| GET | `/api/dba/dashboard/trend` | `@require_auth` | `get_execution_trend()` | 执行趋势 |
| GET | `/api/dba/dashboard/risk` | `@require_auth` | `get_risk_distribution()` | 风险分布 |
| GET | `/api/dba/stream/pipeline/{task_id}` | `@require_auth` | SSE stream | Pipeline 进度推送 |
| GET | `/api/dba/stream/approvals` | `@require_auth` | SSE stream | 审批事件推送 |

**路由分发**: 在 `routes.py` 中添加：

```python
# routes.py (existing file, add ~10 lines)
if path.startswith("/api/dba/"):
    from dba_routes import handle_dba_request
    return handle_dba_request(self, method, path, body)
```

**CSRF 保护**: 在 `handle_dba_request()` 入口统一拦截：

```python
def handle_dba_request(handler, method, path, body):
    # POST/DELETE 请求统一校验 CSRF
    if method in ("POST", "DELETE") and not path.endswith("/login"):
        if not verify_csrf(handler, body):
            return handler.send_error(403, "CSRF token invalid")
    # ... 路由分发
```

### B4. SSE 实时流（含状态恢复机制）⚡ v2 竞态修复

**问题**: 前端发送 `POST /api/dba/task` → 拿到 `task_id` → 建立 SSE 连接。如果后端 Pipeline 执行极快，在 SSE 连接建立前 Stage 1-2 就已完成，前端会永远丢失这些早期事件。

**解决方案**: SSE 连接建立后，后端**立即下发全量状态恢复事件**（State Recovery Event）。

**Pipeline 进度流**: `/api/dba/stream/pipeline/{task_id}`

```
-- SSE 连接建立后立即下发 --
event: state_recovery
data: {
    "task_id": "xxx",
    "stages": [
        {"stage": "INTENT_CLASSIFY", "status": "PASSED", "elapsed_ms": 12},
        {"stage": "PREFLIGHT", "status": "PASSED", "elapsed_ms": 45},
        {"stage": "SQL_VALIDATE", "status": "RUNNING", "elapsed_ms": 0},
        {"stage": "DUAL_VALIDATE", "status": "PENDING"},
        ...
    ],
    "current_stage": "SQL_VALIDATE"
}

-- 后续增量事件 --
event: stage_update
data: {"stage": "SQL_VALIDATE", "status": "PASSED", "elapsed_ms": 120, "detail": "语法正确"}

event: stage_update
data: {"stage": "DUAL_VALIDATE", "status": "RUNNING", "elapsed_ms": 0}

event: approval_needed
data: {"request_id": "xxx", "risk_level": "L2", "sql": "ALTER TABLE...", "created_at": "..."}

event: task_complete
data: {"task_id": "xxx", "success": true, "final_result": "..."}
```

**实现**: 后端 SSE handler 在发送增量事件前，先调用 `get_task_status(task_id)` 获取当前全量快照，封装为 `state_recovery` 事件下发。

**审批事件流**: `/api/dba/stream/approvals`

```
-- SSE 连接建立后立即下发 --
event: state_recovery
data: {"pending": [{"request_id": "xxx", "risk_level": "L2", ...}, ...]}

-- 后续增量事件 --
event: new_approval
data: {"request_id": "xxx", "risk_level": "L2", "sql": "...", "timestamp": "..."}

event: approval_resolved
data: {"request_id": "xxx", "status": "approved", "reviewer": "admin"}
```

### B5. 健壮 SSE 客户端 (dba_sse.js) ⚡ v2 新增

**动机**: 原生 `EventSource` 断线重连不够智能（无指数退避、无 UI 反馈、重连后丢失中间状态）。封装健壮的 SSE 客户端类。

**文件**: `static/js/dba_sse.js` (~150 行)

```javascript
// dba_sse.js — 健壮 SSE 客户端
import store from './dba_store.js';

export class SSEClient {
    constructor(url, { onStateRecovery, onEvent, maxRetries = 10 } = {}) {
        this.url = url;
        this.onStateRecovery = onStateRecovery;
        this.onEvent = onEvent;
        this.maxRetries = maxRetries;
        this._retryCount = 0;
        this._retryDelay = 1000;  // 初始 1s，指数退避
        this._es = null;
        this._closed = false;
    }

    connect() {
        if (this._closed) return;
        this._es = new EventSource(this.url);

        this._es.addEventListener('state_recovery', (e) => {
            // 全量状态恢复 — 修复竞态条件
            this._retryCount = 0;
            this._retryDelay = 1000;
            store.sseConnected = true;
            this._hideConnectionBar();
            if (this.onStateRecovery) {
                this.onStateRecovery(JSON.parse(e.data));
            }
        });

        this._es.addEventListener('stage_update', (e) => {
            if (this.onEvent) this.onEvent('stage_update', JSON.parse(e.data));
        });

        this._es.addEventListener('approval_needed', (e) => {
            if (this.onEvent) this.onEvent('approval_needed', JSON.parse(e.data));
        });

        this._es.addEventListener('approval_resolved', (e) => {
            if (this.onEvent) this.onEvent('approval_resolved', JSON.parse(e.data));
        });

        this._es.addEventListener('new_approval', (e) => {
            if (this.onEvent) this.onEvent('new_approval', JSON.parse(e.data));
        });

        this._es.addEventListener('task_complete', (e) => {
            if (this.onEvent) this.onEvent('task_complete', JSON.parse(e.data));
            this.close();  // 任务结束，关闭 SSE
        });

        this._es.onerror = () => {
            this._es.close();
            store.sseConnected = false;
            this._showConnectionBar();
            this._scheduleReconnect();
        };
    }

    close() {
        this._closed = true;
        if (this._es) {
            this._es.close();
            this._es = null;
        }
        this._hideConnectionBar();
    }

    _scheduleReconnect() {
        if (this._closed || this._retryCount >= this.maxRetries) return;
        this._retryCount++;
        const delay = Math.min(this._retryDelay * Math.pow(2, this._retryCount - 1), 30000);
        setTimeout(() => this.connect(), delay);
    }

    _showConnectionBar() {
        const bar = document.getElementById('dba-connection-bar');
        if (bar) bar.style.display = 'block';
    }

    _hideConnectionBar() {
        const bar = document.getElementById('dba-connection-bar');
        if (bar) bar.style.display = 'none';
    }
}
```

**关键特性**:
1. **状态恢复**: 连接建立后通过 `state_recovery` 事件对齐最新状态（修复竞态条件）
2. **指数退避重连**: 1s → 2s → 4s → 8s → ... → 30s（上限），最多 10 次
3. **UI 反馈**: 断线时顶部显示橙色"连接断开，重连中…"提示条
4. **清理残留动画**: 断线后 `store.sseConnected = false`，各模块 subscribe 该状态清理 RUNNING 动画
5. **优雅关闭**: `task_complete` 事件后自动关闭，不触发重连

**验收标准**:
- 手动断网 → 提示条出现 → 恢复网络 → 自动重连 → 提示条消失 → 状态恢复正确
- Pipeline 执行极快（< 100ms 完成前 3 阶段），前端连上 SSE 后通过 `state_recovery` 正确显示已完成阶段

### B6. API 测试

**文件**: `tests/test_dba_api.py`

覆盖内容：
- 所有 `dba_bridge.py` 函数（Mock 插件模块，不依赖真实数据库）
- `auth_middleware.py`: 登录/登出、session TTL、CSRF 校验、角色权限
- `dba_routes.py`: 未登录 → 401、developer 访问 admin 接口 → 403、正常调用
- SSE `state_recovery` 事件格式校验

**验收标准**: `pytest tests/test_dba_api.py -q` 全部通过

---

## Phase C — 对话页面 (Day 7-10)

### C1. 对话消息列表

**文件**: `dba_chat.js`

消息类型及渲染：

| 消息类型 | 渲染方式 |
|---------|---------|
| 用户消息 | 右对齐气泡，`--bg-surface` 背景 |
| AI 文本回复 | 左对齐，Markdown 渲染 |
| SQL 代码块 | 左侧风险色标条 + 行号 + 语法高亮（参见 DESIGN.md SQL Code Block） |
| Pipeline 摘要 | 折叠的 Pipeline Stage Bar（参见 DESIGN.md Pipeline Stage Bar） |
| 审批卡片 | Approval Card 组件（参见 DESIGN.md Approval Card） |
| 执行结果 | 结果表格 + 耗时标签 |
| 错误消息 | 红色左边框 + 错误详情 |

### C2. 消息输入区（含防重复提交）⚡ v2 增强

```
┌────────────────────────────────────────────┐
│ 💬 输入消息或 SQL...                        │
│                                            │
│                              [发送] [清空]  │
└────────────────────────────────────────────┘
```

- 多行输入 (`<textarea>`)，`Ctrl+Enter` 发送
- 输入框高度自适应（min 40px, max 200px）
- 发送后调用 `POST /api/dba/task`，启动 SSE 监听

**防重复提交机制**: ⚡

```javascript
let _submitting = false;
let _lastSubmitTime = 0;
const SUBMIT_COOLDOWN = 2000;  // 2 秒冷却

async function handleSubmit() {
    if (_submitting) return;  // 请求进行中，忽略
    if (Date.now() - _lastSubmitTime < SUBMIT_COOLDOWN) return;  // 冷却中

    const input = document.getElementById('chat-input').value.trim();
    if (!input) return;

    _submitting = true;
    _lastSubmitTime = Date.now();
    setSubmitButtonState(true);  // 按钮变灰 + 显示 spinner

    try {
        const res = await fetch('/api/dba/task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input, instance: store.currentInstance, _csrf: csrfToken })
        });
        const { task_id } = await res.json();
        store.activeTaskId = task_id;

        // 清空输入框
        document.getElementById('chat-input').value = '';

        // 启动 Pipeline SSE 监听
        startPipelineSSE(task_id);
    } finally {
        _submitting = false;
        setSubmitButtonState(false);
    }
}
```

**规则**:
- 提交进行中 → 按钮灰色 + spinner，无法重复点击
- 提交后 2 秒冷却期 → 防止快速连击
- 上一个任务 Pipeline 仍在执行时 → 允许新提交（前一个 SSE 继续监听）

### C3. Pipeline Stage Bar 组件（支持 State Recovery）⚡ v2 增强

**折叠态**: `校验中 3/9... ▶` （一行摘要）

**展开态**: 9 阶段垂直列表（参见 DESIGN.md Pipeline Stage Bar），每阶段：
- 状态图标 + 阶段名 + 耗时 + 详情折叠按钮
- RUNNING 状态带 pulse 呼吸动画
- 通过 SSE 事件实时更新

```javascript
import { SSEClient } from './dba_sse.js';
import store from './dba_store.js';

function startPipelineSSE(taskId) {
    const client = new SSEClient(`/api/dba/stream/pipeline/${taskId}`, {
        // 连接建立后 — 全量状态恢复（修复竞态条件）
        onStateRecovery: (snapshot) => {
            snapshot.stages.forEach(s => {
                updatePipelineStage(s.stage, s.status, s.elapsed_ms);
            });
        },
        // 后续增量事件
        onEvent: (type, data) => {
            switch (type) {
                case 'stage_update':
                    updatePipelineStage(data.stage, data.status, data.elapsed_ms);
                    break;
                case 'approval_needed':
                    renderApprovalCard(data);
                    break;
                case 'task_complete':
                    renderFinalResult(data);
                    break;
            }
        }
    });
    client.connect();
}
```

**SSE 断线时的行为**:
- Pipeline 中处于 RUNNING 状态的阶段 → 清除 pulse 动画，显示 `⏸ 连接中断` 状态
- 重连后 `state_recovery` 自动恢复正确状态（可能已跳过多个阶段）

### C4. Approval Card 组件（含过期机制 + 实时同步）⚡ v2 增强

参见 DESIGN.md Approval Card 完整规范。

交互流程：
1. Pipeline 到达 APPROVAL 阶段 → SSE 推送 `approval_needed` 事件
2. 前端渲染 Approval Card 嵌入对话流
3. 用户点击:
   - **通过** → `POST /api/dba/approvals/{id}/approve`
   - **驳回** → 弹出原因输入弹窗 → `POST /api/dba/approvals/{id}/reject`
   - **修改后执行** → 弹出 SQL 编辑器弹窗 → `POST /api/dba/approvals/{id}/modify`
4. 审批后 Pipeline 继续 → SSE 推送后续阶段

**审批卡片过期与实时同步机制**: ⚡

```javascript
// === 审批卡片实时同步 ===

// 1. 监听审批事件流 — 其他管理员审批后自动更新当前页卡片
const approvalSSE = new SSEClient('/api/dba/stream/approvals', {
    onStateRecovery: (snapshot) => {
        // 全量刷新待审批列表
        store.pendingApprovals = snapshot.pending;
    },
    onEvent: (type, data) => {
        if (type === 'approval_resolved') {
            // 其他管理员已审批 → 当前页面卡片变灰
            disableApprovalCard(data.request_id, data.status, data.reviewer);
        }
        if (type === 'new_approval') {
            store.unreadApprovalCount++;
        }
    }
});

// 2. 卡片变灰逻辑
function disableApprovalCard(requestId, status, reviewer) {
    const card = document.querySelector(`[data-approval-id="${requestId}"]`);
    if (!card) return;
    card.classList.add('approval-resolved');
    const label = status === 'approved' ? '✅ 已通过' : '❌ 已驳回';
    card.querySelector('.approval-actions').innerHTML =
        `<span class="approval-resolved-label">${label} (by ${reviewer})</span>`;
    card.querySelectorAll('button').forEach(btn => btn.disabled = true);
}

// 3. 创建时间显示 — 让用户感知卡片是否过时
function renderApprovalCard(data) {
    // ... 渲染卡片 ...
    // 底部显示创建时间: "创建于 14:23:05 (2分钟前)"
    const timeEl = card.querySelector('.approval-time');
    // 定时器每 30s 更新 "X分钟前"
    setInterval(() => {
        timeEl.textContent = formatRelativeTime(data.created_at);
    }, 30000);
}
```

**CSS 样式**:

```css
.approval-resolved {
    opacity: 0.5;
    pointer-events: none;
    border-color: var(--border-secondary) !important;
}
.approval-resolved-label {
    color: var(--text-secondary);
    font-size: 12px;
    font-style: italic;
}
```

**验收标准**:
- 管理员 A 在页面 1 通过审批 → 管理员 B 在页面 2 看到该卡片自动变灰并显示"已由 A 通过"
- 卡片底部显示"创建于 14:23:05 (5分钟前)"持续更新

### C5. 右侧上下文面板

参见 DESIGN.md Layout Principles — 右栏上下文面板。

内容区块（上到下）：
1. **任务上下文**: 实例名、方言、风险等级、安全模式（subscribe store 自动同步）
2. **Pipeline 进度**: 实时阶段条（与对话中的同步，共享同一 store 数据）
3. **目标表结构**: SQL 涉及的表的 schema（由后端返回）
4. **审批状态**: 当前待审批/已通过/已驳回

折叠按钮 `«` 可收起右栏（参见 DESIGN.md Responsive Behavior）。

### C6. SQL 语法高亮（含性能护栏）⚡ v2 增强

使用轻量级前端高亮（无需 Prism.js，自写 ~100 行正则）：
- 关键字: `SELECT|FROM|WHERE|JOIN|INSERT|UPDATE|DELETE|ALTER|DROP|CREATE` → `--brand-primary`
- 字符串: `'...'` → `--risk-L0` (绿色)
- 数字: → `--risk-L2` (琥珀)
- 注释: `--...` / `/* */` → `--text-tertiary`
- 表名/列名: 默认 `--text-primary`

**性能护栏**: ⚡

```javascript
const SQL_HIGHLIGHT_MAX_LENGTH = 5000;  // 超过 5000 字符不做语法高亮

function highlightSQL(sql) {
    if (sql.length > SQL_HIGHLIGHT_MAX_LENGTH) {
        const head = sql.substring(0, SQL_HIGHLIGHT_MAX_LENGTH);
        const tail = sql.substring(SQL_HIGHLIGHT_MAX_LENGTH);
        return doHighlight(head) +
            `<span class="sql-truncated">${escapeHtml(tail)}</span>` +
            `<span class="sql-truncated-label">[高亮已截断，完整 SQL 共 ${sql.length} 字符]</span>`;
    }
    return doHighlight(sql);
}

function doHighlight(sql) {
    // 极简正则 — 避免灾难性回溯 (Catastrophic Backtracking)
    // 规则: 只用线性时间正则，不用嵌套量词 (如 (a+)+)
    // 字符串匹配: /'[^']*'/ (非贪婪，无嵌套)
    // 注释匹配: /--[^\n]*/ 和 /\/\*[\s\S]*?\*\// (惰性量词)
    return sql
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')  // 先转义 HTML
        .replace(/'[^']*'/g, '<span class="sql-string">$&</span>')
        .replace(/--[^\n]*/g, '<span class="sql-comment">$&</span>')
        .replace(/\b(\d+(?:\.\d+)?)\b/g, '<span class="sql-number">$1</span>')
        .replace(/\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|ON|INSERT|INTO|VALUES|UPDATE|SET|DELETE|ALTER|TABLE|ADD|DROP|CREATE|INDEX|COLUMN|AND|OR|NOT|IN|IS|NULL|AS|ORDER|BY|GROUP|HAVING|LIMIT|OFFSET|UNION|ALL|DISTINCT|EXISTS|BETWEEN|LIKE|CASE|WHEN|THEN|ELSE|END|GRANT|REVOKE|TRUNCATE|CASCADE)\b/gi,
            '<span class="sql-keyword">$&</span>');
}
```

**正则安全原则**:
1. **不使用嵌套量词**: 如 `(a+)+`、`(a*)*` 会导致指数级回溯
2. **字符串匹配用 `[^']*`**: 匹配非引号字符，线性时间
3. **注释匹配用惰性量词 `*?`**: 确保最短匹配
4. **超长 SQL 截断高亮**: 5000 字符以上不做正则替换，防止主线程卡死

**验收标准**:
- 正常 SQL (< 500 字符) 高亮在 < 5ms 内完成
- 畸形 SQL (> 5000 字符, 嵌套复杂) 不会导致浏览器卡顿
- 用户输入"给 users 表加 phone 字段" → Pipeline 实时推进 → 审批卡片出现 → 点击通过 → 执行完成
- 全链路 SSE 实时更新无卡顿

---

## Phase D — 观测大盘 (Day 11-13)

### D1. 大盘布局

参见 DESIGN.md Layout Principles — 大盘布局。

### D2. 统计卡片 (Stat Card × 4)

| 卡片 | 数据来源 | 趋势对比 |
|------|---------|---------|
| 总执行次数 | `dashboard_stats.total_executions` | vs 上周同期 |
| 成功率 | `dashboard_stats.success_rate` | vs 上周同期 |
| 待审批数 | `store.unreadApprovalCount` (实时 subscribe) | 无趋势 |
| 活跃会话数 | `dashboard_stats.active_sessions` | 无趋势 |

使用 DESIGN.md Stat Card 组件规范。数字用 `Display 36px tabular-nums`。

**待审批数通过 store 订阅实时更新**（审批 SSE 流更新 store → 大盘卡片自动刷新）。

### D3. 执行趋势图 (Chart.js Line)

```javascript
// dba_charts.js
import store, { subscribe } from './dba_store.js';

function renderTrendChart(canvas, data) {
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [
                { label: '成功', data: data.map(d => d.success), borderColor: '#27AE60' },
                { label: '失败', data: data.map(d => d.failed), borderColor: '#E74C3C' },
                { label: '拦截', data: data.map(d => d.blocked), borderColor: '#E6A817' },
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#8B949E' } } },
            scales: {
                x: { ticks: { color: '#8B949E' }, grid: { color: '#21262D' } },
                y: { ticks: { color: '#8B949E' }, grid: { color: '#21262D' } }
            }
        }
    });
}
```

- 时间范围切换: 7天 / 30天（Tab 按钮）
- 数据来源: `GET /api/dba/dashboard/trend?days=7`

### D4. 风险分布图 (Chart.js Doughnut)

```javascript
function renderRiskChart(canvas, data) {
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['L0 安全', 'L1 低危', 'L2 中危', 'L3 高危', 'L4 灾难'],
            datasets: [{
                data: [data.L0, data.L1, data.L2, data.L3, data.L4],
                backgroundColor: ['#27AE60', '#5B6FE6', '#E6A817', '#E67E22', '#E74C3C']
            }]
        }
    });
}
```

### D5. 高危操作预警列表

- 显示最近 10 条 L3/L4 操作
- 每条：时间 + 用户 + SQL 摘要 + 风险 Badge + 状态
- 点击展开详情

### D6. 系统状态面板

- 当前安全模式（Safety Mode Switcher 组件只读显示，subscribe `store.safetyMode`）
- 各数据库实例连通性（绿色/红色圆点）
- 最近 5 条审计事件摘要

**验收标准**:
- 大盘页面加载 < 1s
- 图表正确渲染暗色主题
- 统计数据与审计日志数据一致
- 审批 SSE 推送新审批 → 待审批数 Stat Card 实时 +1

---

## Phase E — 审计日志 (Day 14-15)

### E1. 筛选栏

参见 DESIGN.md Layout Principles — 审计日志布局。

筛选项:
| 字段 | 控件 | 数据来源 |
|------|------|---------|
| 时间范围 | 日期选择器 (原生 `<input type="date">`) | - |
| 用户 | 下拉框 | 从审计日志中聚合 distinct user_id |
| 实例 | 下拉框 | `list_instances()` |
| 风险等级 | 多选 Badge（L0-L4） | 枚举 |
| 操作类型 | 下拉框 | SELECT/INSERT/UPDATE/DELETE/ALTER/DROP/... |
| 关键字搜索 | 文本输入框 | 全文搜索 SQL 内容 |

**筛选逻辑**: 所有条件 AND 组合，变更时自动查询（500ms debounce）

### E2. 数据表格（严格分页，不做虚拟滚动）⚡ v2 性能决策

参见 DESIGN.md Data Table 组件规范。

**性能决策**: ⚡

> 在 Vanilla JS 中，一次性往 DOM 中插入 1000 行复杂表格记录（带高亮、Badge、隐藏详情），极易导致浏览器渲染卡顿甚至假死。考虑到无构建工具，**严格采用传统底部页码分页**，是性能最好的解法。每页最多渲染 50-100 行 DOM 节点。

列定义:
| 列 | 宽度 | 内容 |
|---|------|------|
| 时间 | 90px | HH:mm:ss 格式 |
| 用户 | 80px | user_id |
| 实例 | 100px | instance_name |
| 类型 | 80px | operation_type |
| 风险 | 70px | Risk Level Badge |
| SQL | flex | 截断显示（max 80 字符），悬停 title 显示完整 |
| 状态 | 60px | ✅/❌ 图标 |
| 耗时 | 60px | Xms |

**行交互**:
- 悬停: 行背景 `--bg-surface-hover`
- 点击: 展开行详情（完整 SQL、校验详情、回滚脚本、错误信息）
- 键盘: `↑↓` 选行, `Enter` 展开/折叠

**不实现**:
- ❌ 无限滚动加载 — DOM 膨胀无上限
- ❌ 前端虚拟滚动 — 无构建工具手写过于复杂
- ✅ 传统分页 — 每次请求固定条数，DOM 节点固定上限

### E3. CSV 导出

- 点击「导出 CSV」按钮 → `GET /api/dba/audit/export?{当前筛选条件}`
- 后端生成 CSV → 响应 `Content-Type: text/csv; Content-Disposition: attachment`
- 文件名: `dba_audit_{YYYYMMDD_HHmmss}.csv`
- **导出全量**（不受分页限制）：后端流式生成 CSV，前端 `<a download>` 下载

### E4. 分页

- 每页 50 条（可选 20/50/100）
- 底部分页条: `共 X 条  ◀ 1 2 3 ... N ▶  每页 Y 条`
- URL query param: `?page=1&per_page=50`
- 后端 `query_audit_logs()` 返回 `{items, total, page, per_page}`，前端据此渲染分页条

**验收标准**:
- 每页 50 条 DOM 渲染 < 50ms
- 筛选组合正确过滤，切换筛选后自动回到第 1 页
- CSV 导出内容为全量数据（不受分页限制），与筛选条件一致
- 键盘 `↑↓` 导航当前页内行

---

## Phase F — 管理配置 (Day 16-18)

### 权限控制

- 管理配置 Tab **仅 Admin 角色可见**
- 前端: 根据 `store.userRole` 隐藏 Tab（subscribe 自动响应角色变化）
- 后端: 管理类接口统一使用 `@admin_required` 装饰器（Phase B1 已实现）

```javascript
// dba_panels.js
import store, { subscribe } from './dba_store.js';

subscribe('userRole', (role) => {
    document.getElementById('admin-tab').style.display = role === 'admin' ? '' : 'none';
});
```

### F1. 数据库连接管理

```
┌──────────────────────────────────────────┐
│ 数据库实例                [+ 添加实例]    │
│──────────────────────────────────────────│
│ ┌ pg_test ──────────────────── 🟢 在线 ┐│
│ │ PostgreSQL 15 @ localhost:5437        ││
│ │ DB: health_db_kimi / User: dbclaw_demo_user ││
│ │            [测试连接] [编辑] [删除]    ││
│ └──────────────────────────────────────┘│
│ ┌ mysql_prod ──────────────── 🔴 离线 ┐│
│ │ MySQL 8.0 @ prod-db:3306             ││
│ │ DB: app_db / User: admin              ││
│ │            [测试连接] [编辑] [删除]    ││
│ └──────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

- 添加/编辑: 弹窗表单（host, port, db, user, password, dialect）
- 密码字段: `type="password"`, 显示 `●●●●●●`
- 测试连接: 调用 `GET /api/dba/instances/{name}/status`

### F2. 安全模式管理

- Safety Mode Switcher 组件（可交互版本）
- 切换时调用 `POST /api/dba/safety-mode`（已有 `@admin_required` 保护）
- 疯子模式(MADMAN) → 弹出密码确认弹窗
- 锁定/解锁按钮
- 模式切换历史记录列表

### F3. 风险规则管理

```
┌──────────────────────────────────────────────────┐
│ 硬编码规则 (不可编辑)                              │
│──────────────────────────────────────────────────│
│ HC-001 | DELETE 无 WHERE → L4 灾难               │
│ HC-002 | UPDATE 无 WHERE → L4 灾难               │
│ HC-003 | DROP DATABASE    → L4 灾难               │
│ HC-004 | DROP TABLE       → L4 灾难               │
│ HC-005 | TRUNCATE TABLE   → L3 高危               │
│──────────────────────────────────────────────────│
│ 自定义规则                      [+ 添加规则]       │
│──────────────────────────────────────────────────│
│ CR-001 | ALTER TABLE > 100万行 → L3 高危  [删除]  │
│ CR-002 | 跨表 JOIN > 5 表     → L2 中危  [删除]  │
└──────────────────────────────────────────────────┘
```

### F4. 技能管理

- 技能列表: 名称 + 描述 + 启用/禁用 Toggle Switch
- 技能执行统计: 总次数、成功率、平均耗时

### F5. 知识库管理 (L4 Business Graph)

- 业务字典浏览 + 搜索
- 表关系图（文本列表展示，不做可视化图）
- 业务规则列表

### F6. 系统配置

- 当前 config.yaml 内容展示（只读 + 编辑按钮）
- 管理员密码修改
- 日志级别切换
- 内存清理按钮

**验收标准**:
- 非 Admin 用户看不到管理 Tab（subscribe `store.userRole` 自动控制）
- 安全模式切换生效且记录历史
- 数据库连接测试返回实际状态

---

## Phase G — 集成测试与打磨 (Day 19-21)

### G1. 端到端流程测试

| 场景 | 步骤 | 预期 |
|------|------|------|
| L0 查询 | 输入"查询users表前10条" → 自动执行 | Pipeline 全绿 ✓，结果表格展示 |
| L2 修改 | 输入"给users表加phone字段" → 审批卡片 → 通过 | 审批卡片出现，通过后执行完成 |
| L4 拦截 | 输入"删除users表" → 拦截 | Pipeline 风险评估阶段 FAILED 红色 |
| 驳回 | 审批卡片 → 驳回(填理由) | 任务终止，驳回原因显示 |
| 修改执行 | 审批卡片 → 修改SQL → 执行 | 修改后SQL执行成功 |
| CSV导出 | 审计日志 → 筛选 → 导出 | CSV 文件下载正确（全量不受分页限制） |
| 主题切换 | 点击主题按钮 | 全部组件暗/亮切换 |
| 安全模式 | Admin 切换到保守模式 | 后续操作审批阈值降低 |
| **SSE 竞态** ⚡ | Pipeline 极快完成 → 前端延迟连 SSE | `state_recovery` 事件正确恢复已完成阶段 |
| **SSE 断线** ⚡ | 手动断网 → 恢复 | 提示条出现 → 自动重连 → 状态恢复 |
| **防重复提交** ⚡ | 快速连击发送按钮 3 次 | 只提交 1 次，按钮显示 spinner |
| **审批并发** ⚡ | 管理员 A 通过审批 | 管理员 B 的页面卡片自动变灰 |
| **超长 SQL** ⚡ | 粘贴 10000 字符 SQL | 高亮截断正常，页面不卡顿 |
| **权限隔离** ⚡ | developer 角色访问 Admin Tab | Tab 隐藏，API 返回 403 |

### G2. 样式打磨

- 对照 DESIGN.md 逐项检查所有组件
- 检查暗色/亮色两套主题下所有组件一致性
- 确保 `tabular-nums` 数字对齐
- 检查所有 Risk Level Badge 颜色正确
- Pipeline 呼吸动画流畅
- Toast 通知位置和动画
- SSE 断线提示条样式和动画

### G3. 性能检查

- 大盘页面首次加载 < 1s
- 审计日志分页切换 < 100ms DOM 渲染
- SSE 连接断线自动重连 (指数退避 1s-30s)
- Chart.js 图表暗色主题正确
- SQL 高亮 5000 字符以内 < 10ms

### G4. 安全检查（已在 Phase B 左移实现，此处验证）

> ⚠️ 核心安全机制已在 Phase B1 实现（`@admin_required` 装饰器、CSRF token）。此处为最终审计验证，而非首次实现。

- [x] 鉴权中间件: `@require_auth` / `@admin_required`（Phase B1 ✅）
- [x] CSRF token: POST/DELETE 请求统一校验（Phase B3 ✅）
- [x] SSE endpoint 鉴权: `@require_auth`（Phase B3 ✅）
- [ ] 所有 API 参数经过校验（防 SQL 注入） — 验证 dba_bridge.py 的参数清洗
- [ ] 密码字段不在前端明文显示 — 检查 F1 数据库连接管理
- [ ] CSV 导出内容无 XSS 向量 — 后端 CSV 生成时转义特殊字符
- [ ] 前端 `innerHTML` 使用安全 — 检查所有 DOM 插入是否做了 HTML 转义

---

## 11. 设计规范速查

> 开发时打开 [DESIGN.md](DESIGN.md) 对照使用

### 最常用色值

```
品牌主色:     #5B6FE6
L0 安全:     #27AE60
L2 中危:     #E6A817
L4 灾难:     #E74C3C
页面背景:     #0D1117
卡片背景:     #161B22
主边框:       #30363D
主文本:       #E6EDF3
次级文本:     #8B949E
```

### 核心组件

1. **Risk Level Badge** — 见 DESIGN.md §04
2. **Pipeline Stage Bar** — 见 DESIGN.md §04，默认折叠，支持 SSE state_recovery
3. **Approval Card** — 见 DESIGN.md §04，含三个操作按钮 + 过期/并发同步机制
4. **Stat Card** — 见 DESIGN.md §04，Display 36px 数字，待审批数实时订阅
5. **SQL Code Block** — 见 DESIGN.md §04，左侧风险色标条，5000 字符性能护栏
6. **Data Table** — 见 DESIGN.md §04，40px 行高，严格分页
7. **Safety Mode Switcher** — 见 DESIGN.md §04，分段控件

### 架构组件

8. **dba_store.js** — Proxy 响应式全局状态，subscribe() Pub-Sub
9. **dba_sse.js** — SSEClient 类，断线重连 + state_recovery + UI 反馈
10. **auth_middleware.py** — @require_auth / @admin_required / CSRF 校验

---

## 12. 约束与边界

| 约束 | 说明 |
|------|------|
| PC 端优先 | 不做移动端适配，< 768px 显示提示 |
| 不自定义大盘 | 大盘布局固定，不支持拖拽/自定义面板 |
| Pipeline 默认折叠 | 思考流/校验过程不默认展开，可手动展开 |
| 仅 Admin 访问管理 | 管理配置页面需要 Admin 权限（@admin_required 装饰器） |
| CSV 不 Excel | 审计日志导出仅 CSV，不做 Excel |
| 无构建步骤 | Vanilla JS ES6 Modules + CDN，无 npm/webpack |
| 暗色默认 | 暗色主题为默认，亮色为可选 |
| 严格分页 | 审计日志不做虚拟滚动/无限滚动，每页最多 100 行 DOM |
| SQL 高亮上限 | 超过 5000 字符截断高亮，防止正则灾难性回溯 |
| 安全左移 | Auth/CSRF/RBAC 在 Phase B 路由层实现，不推迟到 Phase G |

---

## 附录: v2 改动摘要

| # | 问题 | 原方案 | 改进 | 落地阶段 |
|---|------|--------|------|---------|
| 1 | Vanilla JS 跨文件状态同步面条代码 | 各 JS 文件 getElementById 互操作 | **dba_store.js** — Proxy Pub-Sub 响应式状态中心 | Phase A6 |
| 2 | 全局变量污染 | `<script src>` 传统引入 | **`<script type="module">`** ES6 模块化 | Phase A7 |
| 3 | SSE 竞态：Pipeline 快于 SSE 连接 | 仅监听增量事件 | SSE 连接后下发 **state_recovery** 全量快照 | Phase B4 |
| 4 | EventSource 断线重连不智能 | 原生 EventSource 默认行为 | **dba_sse.js** — 指数退避 + UI 提示条 + 状态清理 | Phase B5 |
| 5 | 安全检查在 Phase G 才实现 | 最后打磨时加 CSRF/Auth | **auth_middleware.py** — Phase B 同步实现 | Phase B1 |
| 6 | 用户连击发送重复任务 | 无防护 | **防重复提交** — 锁 + 2s 冷却 + 按钮 spinner | Phase C2 |
| 7 | 审批卡片不知道已被他人处理 | 无实时同步 | **审批并发同步** — SSE 推送 + 卡片变灰 + 时间显示 | Phase C4 |
| 8 | 超长 SQL 正则灾难性回溯 | 全量正则高亮 | **5000 字符截断** + 极简线性正则 | Phase C6 |
| 9 | 1000+ 行 DOM 渲染卡顿 | "流畅滚动" 期望 | **严格分页** — 每页最多 100 行 DOM | Phase E2 |
