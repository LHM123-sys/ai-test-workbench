# AI 测试工作台 · AI-Test-Workbench

AI 应用全生命周期测试体系：从离线评测到线上观测。

## 项目结构

| 目录 | 内容 |
|---|---|
| `ai_test_workbench.py` | AI 测试工作台（RAG 回归/注入攻防/检索质量/缺陷分类） |
| `api_auto_demo/` | pytest 接口自动化框架 + GitHub Actions CI |
| `test_platform/` | FastAPI 测试平台（用例管理/执行记录/登录/多环境） |
| `perf_test/` | Locust 性能压测脚本 |

## 技术栈
- 后端：Python + FastAPI + SQLite
- 测试：pytest + Locust
- CI：GitHub Actions
- 前端：HTML + JS（内嵌）
