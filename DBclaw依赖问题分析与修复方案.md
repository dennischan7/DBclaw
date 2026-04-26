# DBclaw 数据库依赖问题分析与修复方案（第二版）

> 更新时间：2026-04-26

## 第二版结论

第一版方案把重点放在拆分 `dba` extra，本身方向是对的，但还不足以解决 fresh clone 后 WebUI 配置管理页直接报 `no module named 'sqlalchemy'` 的问题。

第二版已经明确采用以下实施策略：

- WebUI 数据库实例配置视为核心功能
- 基础安装默认支持 PostgreSQL + MySQL
- `sqlalchemy`、`sqlglot`、`pymysql`、`psycopg2-binary` 纳入默认依赖
- Oracle、SQL Server、Hive 保留为按需安装的独立 extra
- WebUI 测试连接缺驱动时返回明确安装提示，而不是原始 ImportError

## 问题现象

用户 clone 项目后在新服务器部署，启动 WebUI 配置数据库实例时报错：
```
no module named 'sqlalchemy'
```

## 问题分析

### 1. 第一版问题定位

`pyproject.toml` 中定义了 `[dba]` extra：

```toml
dba = [
  "sqlglot>=25.0.0,<26",
  "sqlalchemy>=2.0.0,<3",
  "pymysql>=1.1.0,<2",
  "psycopg2-binary>=2.9.0,<3",
  "cx_Oracle>=8.3.0,<9",
  "pyodbc>=5.0.0,<6",
  "pyhive[hive_pure_sasl]>=0.7.0,<1",
]
```

### 2. 存在的问题

| 问题 | 说明 |
|------|------|
| **用户不知道要安装 `[dba]` extra** | `requirements.txt` 没包含这些依赖，README 也没说明安装方法 |
| **部分包需要系统级依赖** | `cx_Oracle` 需要 Oracle Instant Client，`pyodbc` 需要 ODBC 驱动，`pyhive` 需要 Hadoop 库 |
| **安装失败阻断流程** | `pip install ".[dba]"` 会因 Oracle/SqlServer 包编译失败而整体失败 |
| **`requirements.txt` 与 `pyproject.toml` 不一致** | 文档说 requirements.txt 仅供参考，实际依赖在 pyproject.toml，但用户习惯看 requirements.txt |

### 3. 各数据库驱动依赖情况

| 数据库 | Python 包 | 系统依赖 | 安装难度 |
|--------|-----------|----------|----------|
| PostgreSQL | `psycopg2-binary` | 无 | ✅ 简单 |
| MySQL | `pymysql` | 无 | ✅ 简单 |
| Oracle | `cx_Oracle` | Oracle Instant Client | ❌ 复杂 |
| SqlServer | `pyodbc` | ODBC Driver for SQL Server | ❌ 复杂 |
| Hive | `pyhive` | Hadoop/Thrift 库 | ❌ 复杂 |

## 第二版实施设计

### 方案总览

第二版不再把目标定义为“让用户自己决定是否安装 `dba` extra”，而是改为：

1. 基础安装即满足 WebUI 核心数据库配置能力。
2. PostgreSQL / MySQL 作为默认支持数据库，开箱可用。
3. Oracle / SQL Server / Hive 因为依赖系统驱动，明确定位为扩展能力。
4. README、requirements、运行时报错三处口径统一。

### 已落地改造

| 模块 | 第二版改造 |
|------|------|
| `pyproject.toml` | 将 SQLAlchemy、sqlglot、PyMySQL、psycopg2-binary 移入基础依赖；新增 `dba-oracle`、`dba-sqlserver`、`dba-hive` |
| `requirements.txt` | 同步基础数据库依赖，并标记重型数据库按需安装 |
| `webui/dba_bridge.py` | 测试连接时对缺少核心依赖、缺少数据库驱动、缺少系统客户端分别给出友好提示 |
| `README.md` | 安装说明改为优先 `pip install -e .`，并说明默认支持与扩展驱动安装方式 |
| `docs/database-support.md` | 新增跨数据库部署说明 |
| `tests/test_webui_db_connection.py` | 新增针对性自动化测试 |

## 修复方案

### 方案一：拆分 extras（推荐）

将 `dba` 拆分为多个子 extra，让用户按需安装：

```toml
# 数据库驱动 - 按数据库类型拆分
dba-postgres = ["sqlalchemy>=2.0.0,<3", "psycopg2-binary>=2.9.0,<3", "sqlglot>=25.0.0,<26"]
dba-mysql = ["sqlalchemy>=2.0.0,<3", "pymysql>=1.1.0,<2", "sqlglot>=25.0.0,<26"]
dba-oracle = ["sqlalchemy>=2.0.0,<3", "cx-oracle>=8.3.0,<9", "sqlglot>=25.0.0,<26"]
dba-sqlserver = ["sqlalchemy>=2.0.0,<3", "pyodbc>=5.0.0,<6", "sqlglot>=25.0.0,<26"]
dba-hive = ["sqlalchemy>=2.0.0,<3", "pyhive[hive_pure_sasl]>=0.7.0,<1", "sqlglot>=25.0.0,<26"]

# 默认 dba 只包含无需系统依赖的数据库
dba = ["dbclaw[dba-postgres]", "dbclaw[dba-mysql]"]
```

**优点**：
- 用户可以 `pip install ".[dba]"` 安装常用数据库支持（PostgreSQL + MySQL）
- Oracle/SqlServer 用户明确知道需要额外安装
- 避免 `cx_Oracle` 编译失败阻断其他依赖安装

### 方案二：更新 README 文档

在 README.md 中添加清晰的安装说明：

```markdown
## 安装

### 基础安装

```bash
pip install -e "."
```

### 数据库支持（按需选择）

```bash
# PostgreSQL（推荐，无需额外依赖）
pip install -e ".[dba-postgres]"

# MySQL（推荐，无需额外依赖）
pip install -e ".[dba-mysql]"

# 同时支持 PostgreSQL + MySQL
pip install -e ".[dba]"

# Oracle（需要先安装 Oracle Instant Client）
pip install -e ".[dba-oracle]"

# SQL Server（需要先安装 ODBC Driver）
pip install -e ".[dba-sqlserver]"
```

### Oracle / SQL Server 额外依赖

Oracle 和 SQL Server 的 Python 驱动需要系统级客户端库：

**Oracle:**
1. 下载 [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html)
2. 解压到 `/usr/local/lib/oracle`
3. 设置环境变量：
   ```bash
   export LD_LIBRARY_PATH=/usr/local/lib/oracle:$LD_LIBRARY_PATH
   ```
4. 再安装：`pip install -e ".[dba-oracle]"

**SQL Server:**
1. 安装 ODBC Driver：
   ```bash
   # Ubuntu/Debian
   apt-get install -y unixodbc-dev
   curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
   curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
   apt-get update
   ACCEPT_EULA=Y apt-get install -y msodbcsql17
   ```
2. 再安装：`pip install -e ".[dba-sqlserver]"
```

### 方案三：创建数据库驱动安装指南文档

创建 `docs/db-drivers.md`，详细说明各数据库驱动的安装方法、常见问题和解决方案。

### 方案四：更新 requirements.txt（可选）

将数据库依赖写入 `requirements.txt`，并标注哪些需要系统依赖：

```txt
# 数据库支持 - SQLAlchemy + 驱动
sqlalchemy>=2.0.0
sqlglot>=25.0.0

# PostgreSQL（无系统依赖）
psycopg2-binary>=2.9.0

# MySQL（无系统依赖）
pymysql>=1.1.0

# Oracle（需要 Oracle Instant Client）
# cx-Oracle>=8.3.0

# SQL Server（需要 ODBC Driver）
# pyodbc>=5.0.0

# Hive（需要 Hadoop 库）
# pyhive>=0.7.0
```

## 实施步骤

### 步骤 1：修改 pyproject.toml

编辑 `pyproject.toml`，替换 `[project.optional-dependencies]` 中的 `dba` 定义：

```toml
# 在 [project.optional-dependencies] 部分添加：
dba-postgres = ["sqlalchemy>=2.0.0,<3", "psycopg2-binary>=2.9.0,<3", "sqlglot>=25.0.0,<26"]
dba-mysql = ["sqlalchemy>=2.0.0,<3", "pymysql>=1.1.0,<2", "sqlglot>=25.0.0,<26"]
dba-oracle = ["sqlalchemy>=2.0.0,<3", "cx-oracle>=8.3.0,<9", "sqlglot>=25.0.0,<26"]
dba-sqlserver = ["sqlalchemy>=2.0.0,<3", "pyodbc>=5.0.0,<6", "sqlglot>=25.0.0,<26"]
dba-hive = ["sqlalchemy>=2.0.0,<3", "pyhive[hive_pure_sasl]>=0.7.0,<1", "sqlglot>=25.0.0,<26"]
dba = ["dbclaw[dba-postgres]", "dbclaw[dba-mysql]"]
```

删除原来的 `dba = [...]` 行。

### 步骤 2：更新 README.md

在安装章节添加数据库支持说明（见上方内容）。

### 步骤 3：创建 docs/db-drivers.md

编写数据库驱动安装指南，包含：
- 各数据库驱动的系统依赖说明
- Linux/macOS/Windows 安装步骤
- 常见问题和解决方案
- Docker 部署时的注意事项

### 步骤 4：更新 requirements.txt（可选）

将数据库依赖写入 requirements.txt，方便用户快速查看。

### 步骤 5：提交并推送

```bash
git add pyproject.toml README.md docs/db-drivers.md requirements.txt
git commit -m "feat: split dba extras by database type, add driver installation docs"
git push
```

## 验证方法

在新环境 clone 后测试：

```bash
# 应该成功安装
pip install -e ".[dba]"

# 应该能导入
python -c "from sqlalchemy import create_engine; print('OK')"

# PostgreSQL 连接测试
python -c "from sqlalchemy import create_engine; e = create_engine('postgresql://user:pass@localhost/test'); print('PostgreSQL OK')"
```

## 总结

| 项目 | 改动 |
|------|------|
| `pyproject.toml` | 拆分 `dba` 为 `dba-postgres`, `dba-mysql`, `dba-oracle`, `dba-sqlserver`, `dba-hive` |
| `README.md` | 添加数据库支持安装说明 |
| `docs/db-drivers.md` | 新建文档，说明系统级依赖安装 |
| `requirements.txt` | 可选更新，标注哪些需要系统依赖 |

核心思路：**让无系统依赖的数据库（PostgreSQL、MySQL）默认可用，有系统依赖的数据库明确标注并单独安装**。