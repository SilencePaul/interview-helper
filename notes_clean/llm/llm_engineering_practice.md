# LLM 工程实践

---

## 速览

- Token 成本控制三板斧：Prompt 压缩（LLMLingua）、前缀缓存（Anthropic/OpenAI，90% 折扣）、批量请求（Batch API，50% 折扣）。
- 流式输出（SSE）让用户感知到"实时响应"，核心指标 TTFT（首 Token 时延）比 TPOT（逐 Token 时延）更影响用户体验。
- 限流重试：指数退避 + 随机 Jitter，只重试 429/5xx，绝不重试 400/401。
- LLM 可观测性三支柱：Trace（完整请求/响应链路）+ Metrics（延迟/成本/错误率）+ Logs；LangSmith/LangFuse 是主流工具。
- PII 处理流程：检测 → 替换占位符 → 调用 LLM → 反向映射还原，绝不将原始 PII 写入 Trace。
- Prompt 版本管理：每条 Prompt 存 hash + 版本号，生产切换用 Feature Flag，A/B 测试需统计显著性（≥1000 样本）。
- 生产三件套：超时（hard timeout）+ 熔断器（N 次失败后 open circuit）+ 降级（主模型失败 → 备用模型 → 静态兜底）。
- Model Routing：简单任务走 Haiku/GPT-4o-mini（节省 10-50×），复杂任务走 Opus/o1；RouteLLM 训练路由模型可降本 2-4×。

---

## Token 成本控制

> **一句话理解：** LLM 成本 = Token 用量 × 单价，压缩 Prompt、缓存前缀、批量请求是三种正交的降本手段，叠加可降低 70%+ 成本。

**核心结论（可背）：**
| 手段 | 原理 | 降本幅度 | 代价 |
|---|---|---|---|
| Prompt 压缩（LLMLingua） | 删除冗余 Token，保留关键信息 | 30~50% | 轻微信息损失 |
| 前缀缓存（Prefix Caching） | 相同 Prompt 前缀只计算一次，后续读缓存 | 输入 Token 最高 90% 折扣 | 前缀需 >1024 Token 才生效 |
| 批量请求（Batch API） | 异步离线处理，非实时返回 | 约 50% 折扣 | 延迟高（分钟到小时级） |
| 模型路由 | 简单任务用便宜模型 | 10~50× | 需路由逻辑额外复杂度 |

**机制解释：**
```
成本公式：
  total_cost = (input_tokens × input_price + output_tokens × output_price) / 1_000_000

Anthropic Prompt Caching 规则：
  - 系统 Prompt 前缀 ≥ 1024 Token → 自动缓存，缓存命中价格为原价 10%
  - 缓存生命周期：5 分钟（ephemeral）
  - 最适合：长系统 Prompt + 短用户输入的场景（如 RAG 的固定 system prompt）

OpenAI Context Caching：
  - ≥ 1024 Token，自动缓存，命中价格为原价 50%

LLMLingua Prompt 压缩：
  - 用小模型（GPT2）计算每个 Token 的困惑度（perplexity）
  - 低困惑度 Token（容易预测）→ 可压缩删除
  - 压缩率可达 4x，QA 任务效果损失 <5%

实践建议：
  ① 系统 Prompt 固定部分放最前面，变量部分放后面（利用 Prefix Cache）
  ② RAG 检索结果在注入前先做摘要/压缩（减少 context token）
  ③ 批量评估任务用 Batch API，交互式场景用实时 API
  ④ 记录每次请求的 token 用量，按用户/功能拆分成本
```

**面试官常问：**
- Q：如何把 LLM API 成本降低 70%？
  A：三步走：① 模型路由（简单任务用 Haiku/GPT-4o-mini，10× 节省）② 开启前缀缓存（固定长系统 Prompt 场景节省 80-90%）③ 批量任务走 Batch API（50% 折扣）。三者叠加可轻松 70%+。

**易错点：**
- ❌ Prompt 越短越好 → ✅ 过度压缩会损失必要上下文，关键约束和示例不能删
- ❌ 前缀缓存对所有请求都有效 → ✅ 需要前缀 ≥1024 Token 且每次请求前缀完全一致，任何改动都会使缓存失效

> **面试30秒回答：**
> LLM 成本 = 输入 Token × 价格 + 输出 Token × 价格，降本三板斧：一是 Prompt 压缩，LLMLingua 删冗余 Token，降 30-50%；二是前缀缓存，固定系统 Prompt 前缀命中缓存后只收 10% 费用；三是简单任务路由到便宜模型（Haiku/GPT-4o-mini），比 Opus/GPT-4o 便宜 10-50 倍。三者叠加可降本 70%+。

---

## 流式输出（Streaming）

> **一句话理解：** 流式输出用 SSE 协议边生成边推送，让用户看到"实时打字"效果，TTFT（首 Token 延迟）是决定用户感知速度的核心指标。

**核心结论（可背）：**
```
SSE（Server-Sent Events）格式：
  Content-Type: text/event-stream
  每条事件：data: {"content": "hello"}\n\n
  结束标记：data: [DONE]\n\n

关键指标：
  TTFT（Time to First Token）：用户等待第一个字出现的时间 → 影响感知速度
  TPOT（Time Per Output Token）：每个 Token 的生成时间 → 影响阅读流畅度
  通常 TTFT 对用户体验影响更大（等待焦虑）
```

**机制解释：**
```python
# Python 后端：OpenAI SDK 流式调用
from openai import OpenAI
client = OpenAI()

def stream_response(user_message: str):
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta  # SSE: yield 给前端

# 前端：EventSource 接收
# const source = new EventSource('/api/stream');
# source.onmessage = (e) => appendText(e.data);

Nginx 注意事项：
  Nginx 默认会缓冲代理响应 → SSE 无法实时到达客户端
  必须设置：proxy_buffering off; 或 X-Accel-Buffering: no
```

**面试官常问：**
- Q：流式输出遇到 Nginx 缓冲问题怎么解决？
  A：在响应 header 中设置 `X-Accel-Buffering: no`，同时在 Nginx 配置中 `proxy_buffering off`。这告诉 Nginx 不要缓冲上游的 SSE 响应，直接转发给客户端。

**易错点：**
- ❌ 流式输出可以直接输出 JSON → ✅ 流式 JSON 需要特殊处理（分块组装），或用专门的 streaming structured output 库
- ❌ Nginx/proxy 透明转发 SSE → ✅ 默认缓冲会破坏 SSE，必须显式关闭 buffering

> **面试30秒回答：**
> 流式输出用 SSE 协议实现：后端设置 `Content-Type: text/event-stream`，每生成一个 Token 就 `data: {...}\n\n` 推送给前端，前端用 EventSource 接收。关键指标是 TTFT（首 Token 时延），影响用户等待感知。最常见坑是 Nginx 缓冲：默认会缓存代理响应导致 SSE 无法实时到达，必须设置 `proxy_buffering off` 或响应头 `X-Accel-Buffering: no`。

---

## 限流与重试（Rate Limiting & Retry）

> **一句话理解：** 指数退避 + 随机 Jitter 是 LLM API 限流重试的标准方案，只重试 429/5xx，绝不重试 400，用 tenacity 库三行代码搞定。

**核心结论（可背）：**
```
重试规则：
  ✅ 可重试：429（Rate Limit）、529、502/503/504（服务暂时不可用）
  ❌ 不可重试：400（请求格式错误）、401（认证失败）、404（资源不存在）
  → 4xx（除429）是客户端错误，重试不会修复

指数退避公式（带 Jitter）：
  wait = min(cap, base × 2^attempt) + random(0, 1)
  例：cap=60s, base=1s → 第1次等1~2s，第2次等2~3s，第4次等8~9s...

最大并发控制（防止自己打爆 Rate Limit）：
  asyncio.Semaphore(10)  # 最多10个并发请求
```

**机制解释：**
```python
from tenacity import (
    retry, wait_exponential, stop_after_attempt,
    retry_if_exception_type, wait_random
)
from openai import RateLimitError, APIStatusError

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=60) + wait_random(0, 1),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RateLimitError),
)
async def call_llm(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 并发控制
semaphore = asyncio.Semaphore(10)
async def rate_limited_call(prompt):
    async with semaphore:
        return await call_llm(prompt)
```

**面试官常问：**
- Q：为什么指数退避要加 Jitter？
  A：没有 Jitter 时，多个客户端同时被 429 → 同时等待相同时间 → 同时重试 → 再次 429（Thundering Herd 惊群效应）。加随机 Jitter 打散重试时间，避免雪崩式重试风暴。

**易错点：**
- ❌ 对所有错误都重试 → ✅ 400/401 重试毫无意义，会白白消耗重试次数和时间
- ❌ 不加并发限制 → ✅ 高并发场景应用 Semaphore 控制同时飞行的请求数，防止自己触发 Rate Limit

> **面试30秒回答：**
> 限流重试标准方案：指数退避 + 随机 Jitter，公式 `min(cap, base×2^n) + random(0,1)`。只重试 429（Rate Limit）和 5xx（服务器错误），400/401 是客户端错误，重试不会修复。加 Jitter 是为了防止惊群效应——多个客户端同时被限流后同时重试会导致更大的冲击。用 tenacity 库加一个 `@retry` 装饰器就能实现，再用 `asyncio.Semaphore` 控制最大并发数，防止自己打爆 Rate Limit。

---

## LLM 可观测性（Observability）

> **一句话理解：** 三支柱：Trace（完整调用链路）+ Metrics（延迟/成本/错误率）+ Logs（结构化日志），LangSmith 或 LangFuse 是主流工具，核心目的是让 LLM 应用问题可调试、可归因。

**核心结论（可背）：**
| 支柱 | 内容 | 关键指标 |
|---|---|---|
| Trace | 完整请求/响应链路，含子调用（检索/工具） | span 耗时、token 用量、cost_usd |
| Metrics | 聚合统计，监控系统健康 | TTFT p50/p95、error_rate、cost/session |
| Logs | 结构化事件日志 | 含 trace_id 便于关联 |

**机制解释：**
```python
# LangSmith 结构化日志模式
import json, time, uuid

def llm_call_with_logging(prompt: str, model: str) -> dict:
    trace_id = str(uuid.uuid4())
    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    latency_ms = (time.time() - start) * 1000
    usage = response.usage

    # 结构化日志，便于 Datadog/Grafana 聚合
    log_entry = {
        "trace_id": trace_id,
        "model": model,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "latency_ms": latency_ms,
        "cost_usd": compute_cost(model, usage),
    }
    print(json.dumps(log_entry))  # 输出到日志系统

    return {"content": response.choices[0].message.content, "trace_id": trace_id}

LangSmith 使用：
  - @traceable 装饰器自动追踪函数调用
  - 自动捕获 LangChain 所有节点
  - 支持 dataset eval：批量跑 eval set，比较不同版本 prompt

LangFuse：
  - 开源替代，可自部署
  - generations.create() API 手动上报
  - 支持 prompt 版本管理
```

**面试官常问：**
- Q：生产环境 LLM 应用出了问题怎么排查？
  A：① 用 trace_id 找到出问题的完整调用链 ② 检查每个 span 的输入/输出和 token 数 ③ 对比正常/异常请求的 prompt 差异 ④ 看 LangSmith 中的评估分数趋势 ⑤ 检查检索步骤（RAG场景）是否拿到了正确文档。关键是所有调用必须有 trace_id 串联。

**易错点：**
- ❌ 把用户原始输入（含 PII）全部写入 Trace → ✅ 先匿名化再上报，或只记录 hash
- ❌ 只监控总延迟 → ✅ 要细化到 TTFT（首 Token）和各子步骤（检索/重排/生成）分别计时

> **面试30秒回答：**
> LLM 可观测性三支柱：Trace 记完整调用链路（每个步骤的输入/输出/Token/耗时），Metrics 聚合监控健康（TTFT p95、成本/会话、错误率），Logs 结构化事件日志带 trace_id 串联。工具上 LangSmith 最成熟（@traceable 装饰器自动追踪），LangFuse 是开源自部署替代。生产排查流程：trace_id → 找调用链 → 定位异常 span → 对比输入差异。

---

## 内容安全与 PII 处理

> **一句话理解：** 内容安全 = 拦截有害输入/输出；PII 处理 = 匿名化后调用 LLM 再还原，绝不让原始 PII 进入第三方 API 或日志。

**核心结论（可背）：**
```
内容安全层次：
  输入过滤：
    ① OpenAI Moderation API（免费）：检测 hate/violence/sexual/self-harm
    ② Llama Guard（开源）：可私有化部署，延迟低
    ③ 关键词/正则黑名单：快速，但覆盖不全

  输出过滤：
    ④ 相同工具检测 LLM 输出
    ⑤ 结构化输出验证（Pydantic）：格式约束防注入

PII 处理管道：
  检测 → 替换 → 调用 → 还原

  工具：
    Microsoft Presidio：支持 50+ 实体类型，可自定义规则
    正则：email/电话/身份证/银行卡等
```

**机制解释：**
```python
# PII 匿名化管道（伪代码）
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def anonymize_and_call(user_input: str) -> str:
    # 1. 检测 PII
    results = analyzer.analyze(text=user_input, language="en")

    # 2. 替换为占位符（保存映射表）
    anonymized = anonymizer.anonymize(text=user_input, analyzer_results=results)
    # 例："张三的手机是13800138000" → "<PERSON>的手机是<PHONE_NUMBER>"

    # 3. 调用 LLM（PII 不出境）
    response = call_llm(anonymized.text)

    # 4. 反向还原（如有必要）
    return restore_pii(response, anonymized.items)

Prompt Injection 防御：
  ① 指令层级：System Prompt 指令优先级高于 User 输入
  ② 输入验证：检测 "ignore previous instructions" 等注入模式
  ③ 输出验证：结构化输出 + Pydantic schema 约束
```

**面试官常问：**
- Q：用户输入包含 PII，如何安全地调用第三方 LLM？
  A：三步走：① 用 Presidio 或正则检测 PII 实体 ② 替换为占位符（`<PERSON>/<PHONE_NUMBER>`）并本地保存映射表 ③ 用匿名化后的文本调用 LLM，如需在响应中还原再做反向映射。整个流程 PII 不离开自己的系统。

**易错点：**
- ❌ PII 检测 100% 准确 → ✅ 规则和模型都有漏检，高风险场景需人工复核，并在合规层面有明确告知
- ❌ 原始 PII 可以写入 Trace/日志 → ✅ 日志中只记录匿名化后的版本或 hash，禁止明文 PII 进入任何外部系统

> **面试30秒回答：**
> PII 处理管道四步：检测（Presidio/正则识别姓名/手机/身份证等）→ 替换为占位符（保留本地映射表）→ 调用第三方 LLM（PII 不出境）→ 还原（如有必要反向映射）。内容安全双向拦截：输入用 OpenAI Moderation API 或 Llama Guard 过滤有害内容，输出同样过滤。关键原则：原始 PII 绝不写入日志或 Trace，只记录匿名化版本。

---

## Prompt 版本管理与 A/B 测试

> **一句话理解：** Prompt 是软件，要像代码一样版本化管理；A/B 测试靠流量分割 + 固定 eval set + 统计显著性验证，不靠直觉。

**核心结论（可背）：**
```
Prompt 版本化要素：
  - 每条 Prompt 存储：内容 + hash + 版本号 + 描述 + 创建时间
  - 生产/测试环境用 Feature Flag 切换（环境变量 PROMPT_VERSION=v2）
  - 工具：LangSmith Hub、PromptLayer、Git 文件追踪

A/B 测试流程：
  1. 控制组（v1 Prompt）vs 实验组（v2 Prompt）
  2. 流量分割：5~10% 金丝雀 → 确认无问题 → 50/50 → 全量
  3. 固定 eval set（≥500 条，覆盖边缘案例）
  4. 指标：任务完成率、用户评分、幻觉率、成本
  5. 统计显著性：p-value < 0.05 才算 v2 显著更好
  6. 若 v2 更差：Feature Flag 秒级回滚
```

**机制解释：**
```
关键配置示例（Feature Flag）：
  # settings.py
  PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1")
  PROMPTS = {
      "v1": "你是一个客服助手，请简洁地回答用户问题。",
      "v2": "你是一个专业客服助手。请用友善的语气回答，答案控制在3句话内。",
  }
  current_prompt = PROMPTS[PROMPT_VERSION]

A/B 测试指标选择：
  首选：与业务直接相关的指标
    - 用户满意度评分（1-5星）
    - 任务完成率（用户是否追问）
    - 会话轮数（轮数少 = 一次解决问题）
  辅助：自动化指标（LLM-as-Judge）
    - 相关性、完整性、有害性评分
  不推荐：BLEU/ROUGE（开放生成无意义）
```

**面试官常问：**
- Q：如何安全地在生产环境测试新 Prompt？
  A：金丝雀发布（5% 流量先试水）+ Feature Flag（秒级回滚）+ 固定 eval set 自动评估（不依赖生产流量的主观感受）。先跑 eval set 确认无退步，再逐步放量到 50/50，统计显著后全量。

**易错点：**
- ❌ 主观感觉 v2 更好就上线 → ✅ 需要 ≥500 样本 + p-value < 0.05 统计显著性验证
- ❌ Prompt 直接硬编码在业务代码里 → ✅ Prompt 应存储在配置/数据库中，支持热更新，不需要发版

> **面试30秒回答：**
> Prompt 版本管理：每条 Prompt 存 hash + 版本号，通过 Feature Flag（环境变量）切换，支持秒级回滚。A/B 测试流程：固定 eval set（≥500 条）分别跑 v1/v2，收集任务完成率/用户评分/幻觉率等业务指标，p-value < 0.05 才算显著。生产部署走金丝雀（5% → 50% → 100%），发现问题立刻回滚。核心原则：不靠直觉，靠数据和统计显著性。

---

## 生产部署最佳实践

> **一句话理解：** 生产三件套：超时（防止永久阻塞）+ 熔断器（防止故障扩散）+ 降级（保证用户始终有响应），LLM 外部依赖必须视为不可靠。

**核心结论（可背）：**
```
三件套：
  ① 超时（Timeout）：
     硬超时（hard timeout）= 网络超时 + 模型生成超时
     流式：设置首 Token 超时（TTFT SLA），如 5s 内必须开始流
     非流式：总时间上限，如 30s
     超时后：返回降级响应，不等待

  ② 熔断器（Circuit Breaker）：
     Closed（正常）→ 连续 N 次失败 → Open（熔断，直接返回降级）
     → 冷却期后 Half-Open（允许少量请求试探）
     → 成功则回 Closed，否则重新 Open

  ③ 降级策略（Fallback）：
     Level 1：主模型（GPT-4o）→ Level 2：备用模型（GPT-4o-mini）
     Level 3：本地小模型 / 规则模板 → Level 4：静态兜底响应
     原则：降级要对用户透明（不能沉默失败）
```

**机制解释：**
```python
# 超时 + 降级示例
import asyncio

async def call_with_fallback(prompt: str) -> str:
    # 主模型：30s 超时
    try:
        return await asyncio.wait_for(
            call_llm(prompt, model="gpt-4o"),
            timeout=30.0
        )
    except (asyncio.TimeoutError, Exception) as e:
        log_error("primary_model_failed", error=str(e))
        # 降级到备用模型
        try:
            return await asyncio.wait_for(
                call_llm(prompt, model="gpt-4o-mini"),
                timeout=10.0
            )
        except Exception:
            # 最终兜底
            return "抱歉，服务暂时不可用，请稍后重试。"

健康检查：
  GET /health → 检查 LLM API 连通性 + 延迟
  超过阈值（如 p95 > 5s）→ 告警
  用于负载均衡器判断是否路由请求到该实例
```

**面试官常问：**
- Q：LLM API 突然不可用，用户侧怎么保证不中断？
  A：熔断器 + 多级降级：主模型故障 → 熔断器触发 → 直接走备用模型（不等待主模型超时）→ 备用也不可用 → 本地规则/静态响应。关键是熔断器要配置合理的失败阈值和冷却时间，避免频繁切换。

**易错点：**
- ❌ 没有设置超时，请求无限等待 → ✅ 必须设置 hard timeout，LLM 响应时间不可预测
- ❌ 降级时沉默失败（用户看到空白） → ✅ 降级必须对用户有响应，告知服务降级原因

> **面试30秒回答：**
> 生产部署三件套：超时（30s 硬上限，超时立即降级不等待）、熔断器（连续 N 次失败 → 断路 → 冷却 → 半开试探，防止故障扩散）、降级（主模型 → 备用模型 → 本地规则 → 静态兜底，层层保底）。关键原则：LLM API 是外部依赖，必须视为不可靠，任何调用路径都要有 Plan B。降级一定要对用户有明确响应，禁止沉默失败。

---

## Model Selection & Routing Strategy

> **一句话理解：** 不同复杂度的任务用不同价位的模型，通过路由器（规则/分类器/RouteLLM）自动分配，在质量不降的前提下降低 2-10× 成本。

**核心结论（可背）：**
| 任务复杂度 | 推荐模型 | 约参考价格（输入/1M Token） | 适用场景 |
|---|---|---|---|
| 简单（分类/提取/关键词） | Haiku / GPT-4o-mini | ~$0.15 | 意图识别、实体抽取、格式转换 |
| 中等（摘要/QA/翻译） | Sonnet / GPT-4o | ~$3 | 客服问答、文档摘要、代码补全 |
| 复杂（推理/分析/规划） | Opus / o1 / GPT-4 | ~$15-75 | 复杂推理、代码 Debug、多步规划 |

**机制解释：**
```
四种路由策略：

① 规则路由（最简单）：
   - 按 Prompt 长度、关键词、任务类型硬编码规则
   - 例：包含"分析""设计""规划" → 高级模型；否则 → 低级模型
   - 优点：零延迟，无额外成本；缺点：覆盖不全，需维护

② 分类器路由：
   - 小模型（BERT/FastText）预测查询复杂度
   - 输出：simple/medium/complex → 映射到模型
   - 延迟：<10ms，成本几乎可忽略
   - 缺点：分类器本身需要训练数据

③ RouteLLM（开源，LMSYSLab）：
   - 训练专门的路由模型，学习"哪类问题需要强模型"
   - 输入：query → 输出：路由概率（是否需要强模型）
   - 效果：GPT-4 调用比例从 100% 降至 20-30%，质量几乎不降
   - 原理：利用 Chatbot Arena 的偏好数据作训练信号

④ Cascade（级联）路由：
   - 先用弱模型生成，同时评估置信度/质量
   - 置信度低 → 升级到强模型重新生成
   - 优点：自适应；缺点：增加延迟（需要两次调用）

LiteLLM（统一代理层）：
   - 统一 API 调用 100+ 模型提供商
   - 支持 fallback 路由：主模型 → 备用模型
   - 支持负载均衡（多个 API Key 轮转）
   - 格式：与 OpenAI SDK 兼容，改一行代码切换模型
```

**面试官常问：**
- Q：如何设计一个 LLM 路由系统？
  A：三层架构：① 规则层（关键词/长度快速粗分）→ ② 分类器层（BERT 预测复杂度细分）→ ③ 执行层（LiteLLM 统一调用 + fallback）。生产上先 100% 跑规则路由，收集数据，再训练分类器，最后考虑 RouteLLM。评估指标：成本降幅 + 质量保持率（LLM-as-Judge 对比全走高级模型的基线）。

- Q：RouteLLM 是什么原理？
  A：RouteLLM 是 LMSYS Lab 开源的路由模型。用 Chatbot Arena 的人类偏好对（哪个回答更好）作训练数据，学习"哪类 query 在弱模型和强模型之间有明显质量差距"。推理时只需将 query 输入路由模型，输出一个概率值，决定走强模型还是弱模型。实测 GPT-4 调用比例可从 100% 降到 20%，总体质量几乎不变。

**易错点：**
- ❌ 所有任务都用最强模型，安全保险 → ✅ 成本线性增长，简单任务用高级模型是资源浪费，GPT-4o-mini 在分类/提取任务上准确率接近 GPT-4o
- ❌ 路由系统增加复杂度不值得 → ✅ 规则路由 10 行代码即可实现，在流量大时降本效果显著；复杂应用才考虑分类器和 RouteLLM

> **面试30秒回答：**
> Model Routing 核心思路：按任务复杂度分层，简单任务（分类/提取）走 Haiku/GPT-4o-mini（$0.15/1M），中等任务走 Sonnet/GPT-4o（$3/1M），复杂推理才用 Opus/o1（$15-75/1M）。四种路由策略：规则路由（最简单，关键词分流）、分类器路由（BERT 预测复杂度）、RouteLLM（LMSYS 开源，训练路由模型，GPT-4 调用降至 20% 质量几乎不变）、Cascade（先弱后强，自适应升级）。统一调用层用 LiteLLM，兼容 OpenAI SDK，一行切换模型。

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| LLM 成本怎么降 70%？ | 模型路由（简单任务 Haiku/mini）+ 前缀缓存（固定 system prompt 命中 90% 折扣）+ Batch API（50% 折扣）|
| 前缀缓存什么时候生效？ | 前缀 Token 数 ≥ 1024 且完全一致，任何改动使缓存失效；适合长系统 Prompt 场景 |
| SSE 流式输出 Nginx 踩坑？ | Nginx 默认缓冲代理响应，需设置 proxy_buffering off 或 X-Accel-Buffering: no |
| 重试哪些错误码？ | ✅ 429/5xx；❌ 400/401/404（客户端错误，重试无效）|
| 为什么要加 Jitter？ | 防止惊群效应——无 Jitter 时所有客户端同时重试，再次触发限流 |
| LLM 可观测性怎么做？ | Trace（调用链路） + Metrics（TTFT/成本/错误率）+ Logs（含 trace_id）；LangSmith/LangFuse |
| PII 怎么安全调用第三方 LLM？ | 检测（Presidio）→ 占位符替换（保存映射）→ 调用 LLM → 还原，PII 不出境 |
| Prompt A/B 测试方法？ | 固定 eval set ≥500 条，5% 金丝雀 → 50/50，p-value < 0.05 显著才全量上线 |
| 生产 LLM 应用必备三件套？ | 超时（hard timeout）+ 熔断器（N 次失败断路）+ 降级（多级 fallback 保底）|
| RouteLLM 是什么？效果如何？ | LMSYS 开源路由模型，用 Arena 偏好数据训练，GPT-4 调用比例降至 20%，质量几乎不变 |
