# GitHub 首版发布前检查清单

## 版本与仓库信息

- [ ] 确认首版 Tag 使用 `v0.1.0`
- [ ] 确认 GitHub 仓库名、描述、Topics、Social Preview 已设置
- [ ] 把仓库链接补回 `package.json`、Issue 模板和后续发布材料
- [ ] 确认 README 首页标题、项目简介、版本线说明均使用 DBclaw

## 发布内容

- [ ] GitHub Release 页面使用 `docs/releases/github-release-v0.1.0.md` 作为首版说明基础
- [ ] 核对 [CHANGELOG.md](CHANGELOG.md) 中 `v0.1.0` 条目
- [ ] 检查旧版 `RELEASE_v0.2.0` 到 `RELEASE_v0.9.0` 已归档为上游说明，不再充当 DBclaw 自身发布历史
- [ ] 在 Release 说明中写清楚“基于 Hermes 演化而来，但 DBclaw 自有版本线从 `v0.1.0` 开始”

## 安装与启动链路

- [ ] 全新环境执行一次虚拟环境创建
- [ ] 执行 `pip install -r requirements.txt`
- [ ] 如需校验元信息，执行 `pip install -e .`
- [ ] 配置数据库实例环境变量
- [ ] 配置 LLM 所需环境变量
- [ ] 成功启动 `python -B webui/server.py`
- [ ] 成功访问 `http://127.0.0.1:8787`
- [ ] 完成一条只读查询并确认结果表格、审计日志正常

## 界面与演示材料

- [ ] 检查 `picture/` 下 5 张截图都可正常展示
- [ ] 在 GitHub Release 页面至少放 3 到 5 张关键截图
- [ ] 截图不包含真实实例名、真实账号名、真实 SQL 凭据、API Key 或内部地址

## 安全与合规

- [ ] 确认配置文件中不再提交明文数据库密码或 API Key
- [ ] 确认 `.env.example` 中只保留占位值
- [ ] 确认示例文档中的凭据是安全占位，不是线上真实值
- [ ] 再跑一次敏感词扫描：`password`、`secret`、`token`、`sk-`、`BEGIN PRIVATE KEY`
- [ ] 检查是否有测试数据库、聊天历史或缓存文件包含敏感生产数据

## GitHub 协作面

- [ ] Bug Report 模板已改成 DBclaw 语义
- [ ] Feature Request 模板已改成 DBclaw 语义
- [ ] Issue 模板中不再保留上游 Hermes 仓库链接
- [ ] 如准备接收外部贡献，再检查 PR 模板和 CONTRIBUTING 文案