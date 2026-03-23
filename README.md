# Interviewer Agent v2

一个基于中文八股知识库的命令行面试练习工具。

它会从知识库中抽取概念，生成面试题，评估你的回答，并在回答不够完整时继续追问一轮。

## 功能概览

- 从本地知识库抽题
- 支持按模块 / 文件范围训练
- 支持 dev 模式（离线 mock）和 prod 模式（真实 LLM）
- 支持多种 provider：Anthropic / OpenAI / Ollama / SiliconFlow
- 提供 `doctor` 配置检查
- 提供 `smoke` 非交互链路验证
- 自动保存每轮练习记录到 `data/history/`
- 追问会根据低分维度做定向深挖（概念 / 完整性 / 场景 / 表达）

## 项目结构

```text
app/                    CLI 入口（python -m app ...）
interviewer/            面试主流程
knowledge/              知识块解析、索引构建与加载
llm/                    LLM 抽象与 provider 实现
notes_clean_v2/         中文八股知识库
data/                   生成的索引数据
tests/                  pytest 测试
.env                    本地运行配置（不提交）
.env.example            配置模板
```

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置

复制模板：

```bash
cp .env.example .env
```

推荐默认配置（SiliconFlow）：

```env
LLM_PROVIDER=siliconflow
MODEL_INTERVIEWER=Qwen/Qwen2.5-7B-Instruct
SILICONFLOW_API_KEY=你的密钥
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

支持的 provider：

| Provider | `LLM_PROVIDER` | 必填项 | 示例模型 |
|---|---|---|---|
| SiliconFlow | `siliconflow` | `SILICONFLOW_API_KEY` | `Qwen/Qwen2.5-7B-Instruct` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4o` |
| Ollama | `ollama` | 无 | `llama3` |

## 常用命令

### 1. 构建索引

```bash
python -m app build-index
```

### 2. 检查配置

```bash
python -m app doctor
```

会检查：
- `.env` 是否存在
- provider / model 是否有效
- 对应 API key 是否已设置
- notes 目录是否存在
- index 文件是否存在

### 3. 做一次 smoke test

dev 模式（不走真实 API）：

```bash
python -m app smoke
```

prod 模式（走真实 provider）：

```bash
python -m app smoke --prod
```

### 4. 训练统计

查看最近训练统计：

```bash
python -m app stats
python -m app stats --limit 30
python -m app stats --module 数据库
python -m app stats --json
```

会输出：
- 最近 N 次平均分
- 低分率
- 四个维度的平均分
- 当前最弱维度
- 各分类平均分
- 最常见 missing points

### 5. 浏览训练历史

查看最近历史：

```bash
python -m app history
python -m app history --limit 20
python -m app history --module 数据库
python -m app history --latest --json
```

只看最新一条：

```bash
python -m app history --latest
```

完整展开最新一条：

```bash
python -m app history --latest --full
```

只看低分记录：

```bash
python -m app history --low-score
```

### 6. 正式练习

每次练习结束后，系统会自动把本轮结果保存到：

```bash
data/history/
```

记录内容包括：
- 训练时间
- mode / scope
- 概念标题与分类
- 每一轮题目
- 你的回答
- 总分
- 维度分（准确性 / 完整性 / 场景意识 / 表达清晰度）
- strengths / missing points / ideal answer


随机抽题：

```bash
python -m app interview --prod
```

连续练多题：

```bash
python -m app interview --count 3
python -m app interview --prod --count 5
```

快速刷题（跳过追问）：

```bash
python -m app interview --count 10 --no-followup
python -m app interview --prod --count 20 --no-followup
```

多题训练结束后，会自动输出一段 session summary，包括：
- 本轮完成题数
- 平均分
- 低分轮次
- 当前最弱维度
- 最佳 topic / 最低分 topic
- 本轮最常见 missing point
- 下一步训练建议
- 涉及的 topic 列表

并自动保存一份 JSON 到：

```bash
data/summaries/
```

查看 summary：

```bash
python -m app summary
python -m app summary --latest
python -m app summary --latest --json
```

优先复习历史低分题：

```bash
python -m app interview --review-wrong
python -m app interview --prod --review-wrong
```

按模块训练：

```bash
python -m app interview --prod --module 数据库
```

按文件训练：

```bash
python -m app interview --prod --file 索引.md
```

## 运行模式

### dev

- 使用 `MockLLM`
- 不需要 API key
- 适合本地开发和流程验证

### prod

- 使用真实 LLM provider
- 需要正确配置 `.env`
- 适合真实练习

## 常见报错

### 1. `Configuration error: ... API_KEY is required`
说明 `.env` 里缺少对应 provider 的 key。

### 2. `Configuration error: Index not found ...`
先执行：

```bash
python -m app build-index
```

### 3. `Could not connect to ...`
通常是：
- 网络不通
- `BASE_URL` 配错
- 本地 Ollama 没启动

### 4. `Model not found or unavailable`
通常是：
- `MODEL_INTERVIEWER` 写错了
- 当前账号没有该模型权限
- provider 不支持该模型名

### 5. `Authentication failed`
通常是 API key 错误、过期，或账号权限不足。

## Web UI（轻量版）

启动一个零额外依赖的本地 Web UI：

```bash
python -m app.web
```

默认地址：

```bash
http://127.0.0.1:8008
```

当前 UI 提供：
- stats 面板
- 最近 history 列表
- 最近 summary 列表
- JSON 预览

## 测试

```bash
pytest -q
```

## 当前推荐用法

如果你想最快跑起来，建议直接用：

```env
LLM_PROVIDER=siliconflow
MODEL_INTERVIEWER=Qwen/Qwen2.5-7B-Instruct
SILICONFLOW_API_KEY=...
```

然后执行：

```bash
python -m app doctor
python -m app smoke --prod
python -m app interview --prod
```
