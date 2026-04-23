# DESIGN.md — DBA SafeGuard Web UI

> 设计系统规范文件，供 AI 编码代理阅读以生成一致的 UI。
> 灵感来源：Sentry（数据密集型暗色监控大盘）+ Linear（极简精准紫色调）+ Supabase（数据库工具暗翡翠主题）
> 参考框架：[awesome-design-md](https://github.com/VoltAgent/awesome-design-md) DESIGN.md 标准格式

---

## 01 / VISUAL THEME & ATMOSPHERE

### Design Philosophy

DBA SafeGuard 是一个**企业级数据库运维专家系统**的 Web UI。设计哲学：

- **白盒可观测**：全链路可视化 AI 思考与执行过程，让用户能看到每一步的状态
- **数据密集但不杂乱**：参考 Sentry 的 data-dense dashboard 美学，信息丰富但层次分明
- **安全感知**：风险等级通过颜色系统直觉传达，L0-L4 有明确的视觉语义
- **专业克制**：参考 Linear 的极简精准，避免花哨装饰，每个像素都有功能目的
- **暗色优先**：DBA 长时间工作环境，暗色减轻视觉疲劳，同时提供亮色模式切换

### Mood Keywords

`professional` · `data-dense` · `dark-first` · `security-aware` · `observable` · `precision`

### Visual Density

高密度数据展示（审计日志、大盘统计），但通过留白和分组保持可读性。参考 Sentry 的仪表盘密度而非 Linear 的极简。

---

## 02 / COLOR PALETTE & ROLES

### Brand Colors

| Token | Hex | Role |
|-------|-----|------|
| `--brand-primary` | `#5B6FE6` | 主品牌色 — 按钮、链接、活跃状态，沉稳的靛蓝 |
| `--brand-primary-hover` | `#6E80F0` | 主色悬停态 |
| `--brand-primary-muted` | `rgba(91, 111, 230, 0.15)` | 主色低饱和背景 |

### Risk Level Colors（最重要的语义色系）

| Token | Hex | Role |
|-------|-----|------|
| `--risk-L0` | `#27AE60` | L0 无损只读 — 安全绿 |
| `--risk-L1` | `#5B6FE6` | L1 低危 — 靛蓝 |
| `--risk-L2` | `#E6A817` | L2 中危 — 琥珀黄 |
| `--risk-L3` | `#E67E22` | L3 高危 — 警告橙 |
| `--risk-L4` | `#E74C3C` | L4 灾难 — 危险红 |

### Safety Mode Colors

| Token | Hex | Role |
|-------|-----|------|
| `--mode-readonly` | `#8E9AAF` | 只读审计模式 — 中性灰蓝 |
| `--mode-conservative` | `#27AE60` | 极度保守 — 安全绿 |
| `--mode-moderate` | `#5B6FE6` | 适度模式 — 品牌蓝（默认） |
| `--mode-aggressive` | `#E6A817` | 激进模式 — 琥珀黄 |
| `--mode-madman` | `#E74C3C` | 疯子模式 — 危险红 |

### Status Colors

| Token | Hex | Role |
|-------|-----|------|
| `--status-success` | `#27AE60` | 成功、通过、在线 |
| `--status-error` | `#E74C3C` | 错误、失败、离线 |
| `--status-warning` | `#E6A817` | 警告、待处理 |
| `--status-info` | `#5B6FE6` | 信息提示 |
| `--status-pending` | `#8E9AAF` | 等待中 |
| `--status-running` | `#3498DB` | 运行中（动画） |

### Surface Colors（暗色模式 — 默认）

| Token | Hex | Role |
|-------|-----|------|
| `--bg-page` | `#0D1117` | 页面底层背景 — 近黑（GitHub Dark 风格） |
| `--bg-surface` | `#161B22` | 卡片、面板背景 |
| `--bg-surface-elevated` | `#1C2128` | 悬浮面板、弹窗 |
| `--bg-surface-hover` | `#21262D` | 行悬停、按钮悬停 |
| `--bg-surface-active` | `#262C36` | 按下态、选中态 |
| `--bg-input` | `#0D1117` | 输入框背景 |

### Border Colors

| Token | Hex | Role |
|-------|-----|------|
| `--border-primary` | `#30363D` | 卡片边框、分割线 |
| `--border-secondary` | `#21262D` | 次级边框 |
| `--border-focus` | `#5B6FE6` | 焦点环 |
| `--border-risk` | 继承 `--risk-L*` | SQL 代码块左侧风险色标边框 |

### Text Colors

| Token | Hex | Role |
|-------|-----|------|
| `--text-primary` | `#E6EDF3` | 主文本 — 标题、正文 |
| `--text-secondary` | `#8B949E` | 次级文本 — 描述、时间戳 |
| `--text-tertiary` | `#6E7681` | 三级文本 — 占位符、禁用 |
| `--text-link` | `#5B6FE6` | 链接色 |
| `--text-inverse` | `#0D1117` | 反色文本（亮色按钮上） |

### Surface Colors（亮色模式）

| Token | Hex | Role |
|-------|-----|------|
| `--bg-page-light` | `#FFFFFF` | 页面背景 |
| `--bg-surface-light` | `#F6F8FA` | 卡片背景 |
| `--bg-surface-elevated-light` | `#FFFFFF` | 悬浮面板 |
| `--border-primary-light` | `#D0D7DE` | 边框 |
| `--text-primary-light` | `#1F2328` | 主文本 |
| `--text-secondary-light` | `#656D76` | 次级文本 |

---

## 03 / TYPOGRAPHY RULES

### Font Stack

| 用途 | 字体 | 备注 |
|------|------|------|
| 正文/UI | `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif` | 与 Linear 相同的技术精准感 |
| 代码/SQL | `"JetBrains Mono", "Fira Code", "Cascadia Code", "SF Mono", monospace` | SQL 代码高亮专用 |
| 数据/数字 | `"Tabular Nums" OpenType feature on Inter` | 大盘统计数字等宽对齐 |

### Type Scale

| 层级 | 大小 | 行高 | 字重 | 字间距 | 用途 |
|------|------|------|------|--------|------|
| Display | 36px | 1.10 | 600 | -0.5px | 大盘主统计数字 |
| H1 | 24px | 1.25 | 600 | -0.3px | 页面标题 |
| H2 | 20px | 1.30 | 600 | -0.2px | 面板标题、卡片标题 |
| H3 | 16px | 1.40 | 600 | 0 | 分组标题 |
| Body | 14px | 1.50 | 400 | 0 | 正文、表格内容 |
| Caption | 12px | 1.40 | 500 | 0 | 标签、时间戳、元数据 |
| Small | 11px | 1.30 | 400 | 0.2px | 极小文本、徽章内文字 |
| Code | 13px | 1.50 | 400 | 0 | SQL 代码、技术标识 |

### Typography Rules

- **不使用 16px 以上作为正文** — 数据密集型 UI 用 14px 正文保证信息密度
- **数字一律等宽** — `font-variant-numeric: tabular-nums;` 避免数据跳动
- **SQL 代码块** — JetBrains Mono，带行号，左侧风险色标边框
- **中文** — 使用 `"PingFang SC", "Microsoft YaHei"` fallback，因为用户交互以中文为主

---

## 04 / COMPONENT STYLINGS

### Buttons

| 变体 | 背景 | 文字 | 边框 | 圆角 | 用途 |
|------|------|------|------|------|------|
| Primary | `--brand-primary` | `--text-inverse` | none | 6px | 主操作（发送、确认） |
| Secondary | `transparent` | `--text-primary` | `--border-primary` | 6px | 次级操作（取消、查看） |
| Ghost | `transparent` | `--text-secondary` | none | 6px | 弱操作（关闭、折叠） |
| Danger | `--risk-L4` | `#FFFFFF` | none | 6px | 危险操作（删除、重置） |
| Approve | `--risk-L0` | `#FFFFFF` | none | 6px | 审批通过 |
| Reject | `--risk-L4` | `#FFFFFF` | none | 6px | 审批驳回 |

**States:**
- Default → Hover (亮度+8%) → Active (亮度-4%) → Disabled (opacity 0.4)
- 高度: Small 28px, Medium 32px, Large 36px
- 最小宽度: 64px; 内边距: 8px 12px

### Risk Level Badge（核心组件）

```
┌─────────┐
│ L0 安全  │  → bg: rgba(39,174,96,0.15), text: #27AE60, border: rgba(39,174,96,0.3)
└─────────┘
┌─────────┐
│ L1 低危  │  → bg: rgba(91,111,230,0.15), text: #5B6FE6, border: rgba(91,111,230,0.3)
└─────────┘
┌─────────┐
│ L2 中危  │  → bg: rgba(230,168,23,0.15), text: #E6A817, border: rgba(230,168,23,0.3)
└─────────┘
┌─────────┐
│ L3 高危  │  → bg: rgba(230,126,34,0.15), text: #E67E22, border: rgba(230,126,34,0.3)
└─────────┘
┌─────────┐
│ L4 灾难  │  → bg: rgba(231,76,60,0.15), text: #E74C3C, border: rgba(231,76,60,0.3)
└─────────┘
```

- 圆角: 4px; 内边距: 2px 8px; 字号: 12px / 500
- 边框: 1px solid 对应色 30% 透明度

### Safety Mode Switcher（安全模式切换器）

```
┌──────┬──────┬──────┬──────┬──────┐
│ 只读  │ 保守  │ 适度  │ 激进  │ 疯子  │
└──────┴──────┴──────┴──────┴──────┘
  灰蓝    绿     蓝     琥珀    红
```

- 分段控件样式（Segmented Control），当前模式高亮填充
- 疯子模式点击时弹出密码确认弹窗
- 锁定状态: 叠加🔒图标，不可点击

### Pipeline Stage Bar（管线阶段条 — 核心组件）

```
意图分类 → 预检 → 语法校验 → 双重校验 → 风险评估 → 回滚生成 → 审批 → 执行 → 审计
  ✅       ✅      🔄        ⏳        ⏳        ⏳       ⏳     ⏳     ⏳
```

| 状态 | 图标 | 颜色 | 动画 |
|------|------|------|------|
| PENDING | `○` 空心圆 | `--text-tertiary` | 无 |
| RUNNING | `◉` 实心圆 | `--status-running` | pulse 呼吸动画 |
| PASSED | `✓` 勾号 | `--status-success` | 无 |
| FAILED | `✕` 叉号 | `--status-error` | 无 |
| SKIPPED | `–` 横线 | `--text-tertiary` | 虚线连接 |
| BLOCKED | `⏸` 暂停 | `--status-warning` | 无 |

- 步骤间用线连接：已完成=实线绿色，进行中=蓝色动画，待处理=虚线灰色
- 不默认展开，折叠状态显示摘要：「校验中 3/9...」或「全部通过 ✓」
- 点击展开后每步显示: 阶段名 + 耗时 + 状态 + 详情折叠

### Approval Card（审批卡片 — 核心组件）

```
┌─────────────────────────────────────────────────┐
│ 🔒 人工审批请求                    L2 中危 ⚠️    │
│─────────────────────────────────────────────────│
│ SQL:                                             │
│ ┌─ amber left-border ──────────────────────────┐│
│ │ ALTER TABLE users ADD COLUMN phone VARCHAR(20)││
│ └──────────────────────────────────────────────┘│
│                                                  │
│ 影响表: users                                    │
│ 校验摘要: 语法正确，无性能风险                    │
│                                                  │
│ ▶ 查看回滚脚本                                   │
│                                                  │
│ ┌──────┐ ┌──────┐ ┌────────────┐               │
│ │ ✅ 通过│ │ ❌ 驳回│ │ ✏️ 修改后执行│               │
│ └──────┘ └──────┘ └────────────┘               │
└─────────────────────────────────────────────────┘
```

- 外边框: 1px solid `--risk-L*`（跟随风险等级）
- SQL 代码块左侧: 4px 宽色标条（风险等级色）
- 驳回按钮点击 → 弹出原因输入弹窗（必填）
- 修改后执行 → 弹出 SQL 编辑器弹窗

### Stat Card（统计卡片 — 大盘组件）

```
┌──────────────────┐
│ 总执行次数         │
│                    │
│    1,247           │  ← Display 36px, tabular-nums
│                    │
│ ↑ 12% vs 上周      │  ← Caption 12px, 绿色上升/红色下降
└──────────────────┘
```

- 背景: `--bg-surface`; 边框: `--border-primary`; 圆角: 8px
- 内边距: 20px; 标题: Caption 12px 500 `--text-secondary`
- 数字: Display 36px 600 `--text-primary`, `tabular-nums`
- 趋势: Caption 12px, 上升=绿+`↑`, 下降=红+`↓`

### Data Table（数据表格 — 审计日志核心组件）

| 属性 | 值 |
|------|-----|
| 表头背景 | `--bg-surface` |
| 表头字体 | Caption 12px / 600 / uppercase / `--text-secondary` |
| 行高 | 40px |
| 行背景（偶数） | `--bg-page` |
| 行背景（奇数） | `--bg-surface` 50% opacity |
| 行悬停 | `--bg-surface-hover` |
| 行点击展开 | `--bg-surface-active` |
| 单元格内边距 | 8px 12px |
| 边框 | 仅水平分割线 `--border-secondary` |

### SQL Code Block（SQL 代码块）

```
┌ 4px risk-color bar ┬──────────────────────────────┐
│                     │  1  SELECT u.name, o.total    │
│     L2 中危         │  2  FROM users u               │
│                     │  3  JOIN orders o ON u.id=o.uid│
│                     │  4  WHERE u.status = 'active'  │
│                     ├──────────────────────────────│
│                     │        [复制] [格式化]          │
└─────────────────────┴──────────────────────────────┘
```

- 背景: `#0D1117`; 边框: `--border-primary`; 圆角: 6px
- 左侧 4px 色标条: 颜色跟随风险等级
- 行号: `--text-tertiary`; 代码: JetBrains Mono 13px
- 右上角工具按钮: 复制 + 格式化, Ghost 按钮风格

### Form Elements

| 属性 | 值 |
|------|-----|
| 输入框高度 | 32px |
| 背景 | `--bg-input` |
| 边框 | 1px solid `--border-primary` |
| 圆角 | 6px |
| 文字 | Body 14px `--text-primary` |
| 占位符 | `--text-tertiary` |
| 焦点 | border-color `--border-focus`, box-shadow `0 0 0 2px rgba(91,111,230,0.2)` |
| 错误 | border-color `--risk-L4`, 下方错误提示 Caption 12px |
| 下拉框 | 同输入框样式, 右侧 chevron 图标 |
| 日期选择器 | 弹出式日历, 暗色主题匹配 |

### Navigation Tab

| 属性 | 值 |
|------|-----|
| 高度 | 36px |
| 字体 | Caption 12px / 600 |
| 默认色 | `--text-secondary` |
| 活跃色 | `--text-primary` |
| 活跃指示 | 底部 2px `--brand-primary` 横线 |
| 悬停 | `--bg-surface-hover` 背景 |
| 图标 | 16px, 文字左侧, 间距 6px |

### Toast Notification

| 类型 | 左侧色标 | 图标 |
|------|----------|------|
| Success | `--status-success` | ✓ |
| Error | `--status-error` | ✕ |
| Warning | `--status-warning` | ⚠ |
| Info | `--status-info` | ℹ |

- 位置: 右上角; 宽度: 360px; 圆角: 8px
- 背景: `--bg-surface-elevated`; 边框: `--border-primary`
- 左侧 4px 色标条; 自动消失: 5s; 可手动关闭

### Modal / Dialog

| 属性 | 值 |
|------|-----|
| 背景遮罩 | `rgba(0, 0, 0, 0.6)` + `backdrop-filter: blur(4px)` |
| 弹窗背景 | `--bg-surface-elevated` |
| 圆角 | 12px |
| 最大宽度 | 480px（小弹窗）/ 640px（中弹窗）/ 80vw（大弹窗） |
| 内边距 | 24px |
| 标题 | H2 20px / 600 |
| 关闭按钮 | 右上角 Ghost ✕ |
| 操作按钮 | 底部右对齐, Primary + Secondary |

---

## 05 / LAYOUT PRINCIPLES

### 三栏布局（主对话页）

```
┌──────────┬──────────────────────────┬──────────────┐
│          │                          │              │
│  Left    │      Center              │   Right      │
│  Sidebar │      Chat                │   Context    │
│          │                          │              │
│  240px   │      flex: 1             │   280px      │
│  fixed   │      min: 480px          │   collapsible│
│          │                          │              │
└──────────┴──────────────────────────┴──────────────┘
```

| 区域 | 宽度 | 内容 |
|------|------|------|
| 左栏 | 240px 固定 | 会话列表 + 导航 Tab（Chat/Dashboard/Audit/Admin） |
| 中栏 | flex: 1 (min 480px) | 对话区 / 大盘 / 审计 / 管理（按 Tab 切换） |
| 右栏 | 280px 可折叠 | 上下文面板（表结构、风险、Pipeline） |

### Sidebar（左栏）

```
┌──────────────────────┐
│ DBA SafeGuard   [≡]  │  ← 品牌标识 + 折叠按钮
│──────────────────────│
│ 💬 Chat              │  ← Nav Tab (活跃态)
│ 📊 Dashboard         │
│ 📋 Audit             │
│ ⚙️ Admin             │  ← 仅 Admin 可见
│──────────────────────│
│ 🔍 搜索会话...        │  ← 搜索框
│──────────────────────│
│ 📌 Pinned            │
│  ├ Session 1         │
│  └ Session 2         │
│──────────────────────│
│ 今天                  │
│  ├ 给users表加phone字段│
│  └ 查询订单数据       │
│ 昨天                  │
│  └ 索引优化建议       │
│──────────────────────│
│                      │
│ 实例: pg_test ▾      │  ← 数据库实例切换
│ 模式: 适度 ▾         │  ← 安全模式切换
│ v0.9.0               │  ← 版本号
└──────────────────────┘
```

### 右栏上下文面板

```
┌──────────────────────┐
│ 📋 任务上下文         │
│──────────────────────│
│ 实例: pg_test        │
│ 方言: PostgreSQL 15  │
│ 风险等级: L2 中危 ⚠️  │
│ 安全模式: 适度       │
│──────────────────────│
│ 📊 Pipeline          │
│ ✅ 意图分类  12ms    │
│ ✅ 预检      45ms    │
│ 🔄 语法校验  ...     │
│ ⏳ 双重校验          │
│ ⏳ ...               │
│──────────────────────│
│ 📄 目标表: users     │
│ ┌──────────────────┐ │
│ │ id    int PK     │ │
│ │ name  varchar    │ │
│ │ email varchar    │ │
│ │ ...              │ │
│ └──────────────────┘ │
│──────────────────────│
│ 🔒 审批状态: 待审批   │
└──────────────────────┘
```

### 大盘布局

```
┌──────────────────────────────────────────────────┐
│  [总执行次数] [成功率]  [待审批数] [活跃会话数]     │  ← 4 Stat Cards, 等宽 grid
│──────────────────────────────────────────────────│
│ ┌─────────────────────┐ ┌──────────────────────┐ │
│ │                     │ │                      │ │
│ │  执行趋势 (折线图)   │ │  风险分布 (饼图)      │ │  ← 2 列图表区
│ │  7天 | 30天          │ │  L0-L4              │ │
│ │                     │ │                      │ │
│ └─────────────────────┘ └──────────────────────┘ │
│──────────────────────────────────────────────────│
│ ┌─────────────────────┐ ┌──────────────────────┐ │
│ │ ⚠️ 高危操作预警      │ │ 📊 系统状态          │ │  ← 2 列列表区
│ │  待审批列表          │ │  安全模式 / 实例状态  │ │
│ │  最近拦截事件        │ │  最近审计事件        │ │
│ └─────────────────────┘ └──────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### 审计日志布局

```
┌──────────────────────────────────────────────────┐
│ 筛选栏:                                          │
│ [时间范围 ▾] [用户 ▾] [实例 ▾] [风险 ▾] [搜索🔍] [导出CSV] │
│──────────────────────────────────────────────────│
│ 时间       | 用户  | 实例    | 类型    | 风险 | SQL...      | 状态 | 耗时 │
│────────────┼───────┼────────┼────────┼──────┼────────────┼──────┼──── │
│ 14:23:05   | admin | pg_test| ALTER  | L2 ⚠ | ALTER TAB..| ✅    | 45ms│
│ 14:20:12   | dev   | pg_test| SELECT | L0 ✓ | SELECT u..| ✅    | 12ms│
│ 14:15:30   | admin | mysql_1| DROP   | L4 🔴| DROP TAB..| ❌    | -   │
│ ...        | ...   | ...    | ...    | ...  | ...        | ...  | ... │
│──────────────────────────────────────────────────│
│ 共 1,247 条  ◀ 1  2  3  4  5 ... 25 ▶  每页 50 条│  ← 分页
└──────────────────────────────────────────────────┘
```

### 管理配置布局

```
┌──────────────────────────────────────────────────┐
│ [数据库连接] [安全模式] [风险规则] [技能] [知识库] [系统]│  ← 内部 Tab
│──────────────────────────────────────────────────│
│                                                  │
│           (当前 Tab 对应的子页面内容)               │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Spacing Scale

| Token | 值 | 用途 |
|-------|-----|------|
| `--space-1` | 4px | 图标与文字间距、紧凑元素 |
| `--space-2` | 8px | 相关项间距、按钮内边距 |
| `--space-3` | 12px | 卡片内元素间距 |
| `--space-4` | 16px | 卡片内边距、标准间距 |
| `--space-5` | 20px | Stat Card 内边距 |
| `--space-6` | 24px | 区域间距、弹窗内边距 |
| `--space-8` | 32px | 大区域间距 |

### Grid System

- 大盘 Stat Cards: `grid-template-columns: repeat(4, 1fr); gap: 16px;`
- 大盘图表区: `grid-template-columns: 1fr 1fr; gap: 16px;`
- 管理页面表单: 单列, `max-width: 640px;`

---

## 06 / DEPTH & ELEVATION

| 层级 | 阴影 | 用途 |
|------|------|------|
| Level 0 | 无阴影，border `--border-primary` | 默认表面 — 卡片、表格 |
| Level 1 | `0 1px 3px rgba(0,0,0,0.12)` | 悬浮元素 — 下拉菜单 |
| Level 2 | `0 4px 12px rgba(0,0,0,0.15)` | 弹窗、Toast |
| Level 3 | `0 8px 24px rgba(0,0,0,0.2)` | Modal 遮罩内弹窗 |
| Focus Ring | `0 0 0 2px rgba(91,111,230,0.3)` | 焦点环（叠加在边框上） |

**原则**: 暗色模式下少用阴影（暗底不明显），主要通过 **边框层次** 传达深度（参考 Supabase 方式）。

---

## 07 / DO'S AND DON'TS

### DO ✅

- **DO** 用风险等级色标让用户一眼看出操作危险程度
- **DO** 所有 SQL 代码块左侧显示风险色标条
- **DO** Pipeline 阶段条默认折叠，避免信息过载
- **DO** 高危操作审批卡片必须显示回滚脚本（可折叠）
- **DO** 大盘统计数字使用 `tabular-nums` 等宽数字
- **DO** 表格行支持悬停高亮和点击展开
- **DO** 暗色模式用边框层次（border hierarchy）传达深度
- **DO** 审计日志表格支持键盘导航（↑↓翻行，Enter 展开）
- **DO** 加载状态使用骨架屏（skeleton），不用全屏 spinner

### DON'T ❌

- **DON'T** 隐藏风险信息 — 任何涉及数据修改的操作必须展示风险等级
- **DON'T** 允许 L2+ 操作一键执行 — 必须有审批确认弹窗
- **DON'T** 在前端明文显示数据库密码 — 密码字段用 `●●●●●●`
- **DON'T** 使用纯黑 `#000000` — 用 `#0D1117` 近黑色（减轻视觉疲劳）
- **DON'T** 在暗色模式使用重阴影 — 用 border 替代
- **DON'T** 使用 > 14px 正文字号 — 数据密集型 UI 保持紧凑
- **DON'T** 使用动画吸引注意力（除了 Pipeline RUNNING 状态的 pulse 呼吸动画）
- **DON'T** 让非 Admin 看到管理配置 Tab

---

## 08 / RESPONSIVE BEHAVIOR

| 断点 | 宽度 | 行为 |
|------|------|------|
| Desktop | ≥ 1280px | 三栏完整布局 |
| Narrow Desktop | 1024-1279px | 右栏默认折叠，点击展开 |
| Tablet | 768-1023px | 左栏折叠为图标栏，右栏隐藏 |
| 不支持 | < 768px | 显示"请使用桌面浏览器"提示 |

**注意**: 本项目为 PC 端优先，不做移动端适配（按开发计划要求）。Tablet 仅做基本可用。

---

## 09 / AGENT PROMPT GUIDE

### Quick Color Reference

```
Brand:     #5B6FE6 (indigo blue)
L0 Safe:   #27AE60 (green)
L1 Low:    #5B6FE6 (indigo)
L2 Medium: #E6A817 (amber)
L3 High:   #E67E22 (orange)
L4 Critical:#E74C3C (red)
BG Page:   #0D1117 (near-black)
BG Card:   #161B22 (dark surface)
Border:    #30363D (primary)
Text:      #E6EDF3 (primary)
Text Muted:#8B949E (secondary)
```

### Ready-to-use Prompts

**对话页面:**
> Build a three-panel chat interface: 240px left sidebar (session list + nav tabs), flex center (chat messages with SQL syntax highlighting and risk-level left-border), 280px right panel (task context with pipeline stages). Dark theme using the DESIGN.md color tokens. Pipeline stage bar collapsed by default, expandable on click.

**大盘页面:**
> Build a monitoring dashboard with 4 stat cards in a grid row (total executions, success rate, pending approvals, active sessions), below that a 2-column grid: left is a line chart (7/30 day execution trend with success/failure/blocked lines), right is a doughnut chart (L0-L4 risk distribution using risk-level colors). Below that, 2-column: left is a risk alert list, right is system status panel. All cards use --bg-surface background, --border-primary borders, 8px radius.

**审批卡片:**
> Build an approval card component with risk-level-colored border (L0=green, L2=amber, L4=red), containing: SQL code block with left color bar, risk badge, affected tables list, validation summary, collapsible rollback script section, and three action buttons: Approve (green), Reject (red, requires reason modal), Modify & Execute (secondary, opens SQL editor modal).
