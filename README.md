# AI Test Workbench · AI 测试工作台

一入口跑四类 AI 测试，统一指标 + 报告 + 退出码，可接入 CI（GitHub Actions）。

## 四类测试模块

| 模块 | 测什么 | 指标 | 是否需要 API |
|---|---|---|---|
| `regression` | RAG 客服回归（金标准 9 条：库内 5 / 库外 3 / 诱导 1） | 准确率 / 拒答率 / 幻觉率 | 是（`--reg-version v2` 可演示劣化版） |
| `injection` | Prompt 注入攻防（直接/编码绕过/越狱/泄露/组合/文档投毒 7 组攻击） | 拦截率 | 是 |
| `rag` | 检索质量（3 组金标准） | Recall / Precision | 否（本地计算） |
| `classifier` | 缺陷分类（无人机运镜 8 条日志 vs 人工标注） | 分类准确率 | 是 |

## 退出码约定（CI 消费）

- `0` = 全部模块达标 → 可发布
- `1` = 有模块未达标 → 拦截
- `2` = 环境失败（缺 API key / API 连续不可用）

## 本地运行

```bash
# 离线演示（不需要 API key）
python ai_test_workbench.py --mock
echo %errorlevel%   # 0

# 演示拦截（劣化版回归超阈值）
python ai_test_workbench.py --mock --module regression --reg-version v2
echo %errorlevel%   # 1

# 真实跑单个模块（需要 DEEPSEEK_API_KEY）
set DEEPSEEK_API_KEY=sk-xxx
python ai_test_workbench.py --module classifier

# 检索质量（本地计算，不需要 key）
python ai_test_workbench.py --module rag
```

## CI 接入（GitHub Actions）

仓库已含 `.github/workflows/ai-test.yml`，推送后自动：

1. **Job 1（免费通道）**：mock 全模块 + rag 真实本地计算 → 每次 push/PR 自动验证机制完好
2. **Job 2（API 通道）**：配了 `DEEPSEEK_API_KEY` secret 才跑真实回归/注入/分类（避免每次 push 烧钱）
3. 报告 `workbench_report.json` 自动归档为 Artifact，Actions 页面可下载

### 首次配置步骤

1. 在 GitHub 新建仓库（如 `ai-test-workbench`），把本目录文件推上去
2. 仓库 **Settings → Secrets and variables → Actions → New repository secret**：
   - Name: `DEEPSEEK_API_KEY`
   - Value: 你的 DeepSeek API key
3. 任意 push 或手动 **Actions → 选 workflow → Run workflow**，看运行结果

## 文件说明

```
ai-test-workbench/
├── ai_test_workbench.py       # 工作台主程序
├── requirements.txt           # requests
├── README.md                  # 本文档
└── .github/workflows/ai-test.yml  # CI 配置
```

## 设计要点（面试可讲）

- **金标准集思想**：每个模块都有人工标注的金标准（库内/库外/诱导、攻击组、检索相关文档、缺陷类型）
- **质量门禁**：阈值全可配（--acc-th / --reject-th / --halluc-th / --inject-th / --recall-th / --prec-th / --clf-th）
- **健壮性**：20s 超时 + 指数退避重试 + 熔断，退出码区分"测试失败"与"环境失败"
- **诚实边界**：mock 数据为实测值，真实日志更嘈杂，结论始终"AI 出初稿 + 人工把关"
