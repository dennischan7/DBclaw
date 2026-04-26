# DBclaw Database Support

本文档说明 DBclaw 在 fresh clone / 新服务器部署时的数据库依赖策略。

## 默认支持

基础安装已经内置以下数据库连接能力：

- PostgreSQL
- MySQL
- WebUI 配置管理页面的数据库实例测试连接

推荐安装命令：

```bash
pip install -e .
```

如果你使用 `requirements.txt`，同样会安装 PostgreSQL / MySQL 所需的核心驱动：

```bash
pip install -r requirements.txt
```

## 可选扩展数据库

以下数据库由于依赖额外系统客户端或驱动，不纳入默认安装。

### Oracle

Python 安装命令：

```bash
pip install -e ".[dba-oracle]"
```

额外要求：

- 需要 Oracle Instant Client
- Linux / macOS 需要正确配置动态库路径
- Windows 需要把 Instant Client 目录加入 PATH

常见报错：

- `DPI-1047`：通常表示 Oracle Instant Client 未安装或未被找到

### SQL Server

Python 安装命令：

```bash
pip install -e ".[dba-sqlserver]"
```

额外要求：

- 需要系统安装 ODBC Driver for SQL Server
- Linux 通常还需要 `unixodbc` / `unixodbc-dev`
- Windows 需要安装 Microsoft ODBC Driver

常见报错：

- 找不到 `pyodbc`
- 找不到 ODBC Driver 17 / 18
- ODBC 共享库缺失

### Hive

Python 安装命令：

```bash
pip install -e ".[dba-hive]"
```

额外要求：

- 需要 Hadoop / Thrift 相关运行环境
- 具体认证方式取决于 HiveServer2 配置

## 部署建议

### 面向大多数开发者

如果你的团队主要使用 PostgreSQL 和 MySQL，只需要基础安装：

```bash
pip install -e .
```

### 面向多数据库团队

建议把数据库支持拆成两层：

- 基础镜像 / 基础虚拟环境：只包含默认依赖
- 数据库专项环境：按实际需要额外安装 Oracle、SQL Server、Hive 驱动

这样可以避免某个系统驱动安装失败，阻断整个 DBclaw 部署流程。

## WebUI 缺驱动行为

从当前版本开始，WebUI 管理页在测试连接时会返回面向用户的安装提示，而不是直接暴露底层 `No module named ...` 异常。

提示分三类：

- 缺少核心依赖，例如 `sqlalchemy`
- 缺少数据库方言驱动，例如 `pyodbc`
- 缺少系统客户端，例如 Oracle Instant Client / ODBC Driver