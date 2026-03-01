# LLM 评估

## 速览
- LLM-as-Judge 用强大模型（GPT-4o）自动评估 LLM 输出，替代昂贵的人工标注，是当前生产评估的主流方案。
- Pairwise（两两比较）比 Pointwise（单独打分）更可靠——模型更擅长"A 比 B 好"的相对判断。
- LLM-as-Judge 主要偏差：位置偏差（偏向第一个）、冗长偏差（偏向更长）、自我增强偏差（偏向自己风格）。
- 幻觉分两类：内在幻觉（与 context 矛盾）和外在幻觉（无法从 context 验证，即编造）。
- 检测幻觉的实用方法：原子声明分解 + NLI/LLM 逐一验证（FActScore 框架）。
- RAG 评估核心：Faithfulness（答案忠于检索内容，反幻觉）+ Answer Relevancy（答案回答了问题）。
- 对齐评估（RLHF/DPO）核心指标：人类偏好胜率（win rate vs baseline），而非传统 NLP 指标。
- 基准测试（MMLU/HumanEval）有饱和和过拟合风险，Chatbot Arena 的真实用户盲测更可信。

---

## LLM-as-Judge

> **一句话理解：** 用 GPT-4o 等强模型自动给其他 LLM 的输出打分或排名，取代昂贵的人工标注，是目前 LLM 评估的主流自动化方案。

**核心结论（可背）：**
| 评估范式 | 原理 | 优点 | 局限 |
|---|---|---|---|
| Pointwise（单独打分） | 对单个回答在 1~5 分量表打分 | 简单，可量化 | 分数绝对值不稳定，模型间分数不可比 |
| Pairwise（两两比较） | 给定两个回答，选出更好的那个 | 更符合人类判断方式，结果更可靠 | 组合爆炸（N个答案需N²次比较） |
| Reference-based | 与标准答案对比打分 | 有明确评分基准 | 需要人工标注 ground truth |
| Reference-free | 不需要标准答案，直接评估质量 | 无需 GT，可大规模运行 | 偏差风险更高 |

**机制解释：**
```
LLM-as-Judge prompt 设计要素：
  1. 明确评估标准（Criteria）：
     - 事实准确性（Factual Accuracy）
     - 相关性（Relevance）
     - 完整性（Completeness）
     - 语言质量（Fluency）
  2. 评分量表：5分制 或 A/B/tie 三选一
  3. Chain-of-Thought：要求先给出评分理由再打分（减少随意性）
  4. 输出格式：JSON（方便解析）

三大偏差及缓解：
  位置偏差（Position Bias）：
    表现：倾向于选 Pairwise 中的第一个选项
    缓解：交换 A/B 位置各跑一次，取一致结论
  冗长偏差（Verbosity Bias）：
    表现：倾向于更长的回答（即使内容不更好）
    缓解：在 prompt 中明确"长度不是质量标准"
  自我增强偏差（Self-Enhancement Bias）：
    表现：GPT-4 倾向于给 GPT-4 的输出更高分
    缓解：用多个不同评估模型，取共识

LMSYS Chatbot Arena：
  真实用户盲测 Pairwise 比较，ELO 积分排名
  最接近真实人类偏好的评估，但成本高、速度慢
```

**面试官常问：**
```
Q: LLM-as-Judge 和人类评估哪个更可信？
A: 人类评估更权威，但成本高、速度慢、一致性差（不同评估者标准不同）。
   LLM-as-Judge 在强模型（GPT-4o）上与专家人工评估的相关性达 80%+，
   速度快 100× 且成本低，适合大规模自动化评估和快速迭代。
   高风险决策仍需人工 review。

Q: 如何验证 LLM-as-Judge 本身是否可信？
A: ① 与人类标注者结论的一致性（Cohen's Kappa ≥ 0.6 为合格）
   ② 位置偏差测试（交换 A/B 位置，结论应一致）
   ③ 对已知好/坏答案的判断准确率
   ④ 定期用人工校准评估结果
```

**易错点：**
- ❌ LLM-as-Judge 完全客观 → ✅ 有位置偏差、冗长偏差、自我增强偏差，需要设计减偏措施
- ❌ Pointwise 分数在不同模型间可比 → ✅ 不同 LLM 对同一回答的评分量表理解不同，跨模型分数不可直接比较

**面试30秒回答：**
> LLM-as-Judge 用 GPT-4o 等强模型自动评估 LLM 输出，是生产评估的主流方案。Pairwise（A vs B 选更好的）比 Pointwise（单独打分）更可靠，因为相对判断更符合人类直觉。三大偏差要注意：位置偏差（交换 AB 顺序跑两次缓解）、冗长偏差（prompt 中明确"长度不是质量"）、自我增强偏差（用多个评估模型取共识）。与人类评估相关性 80%+，速度快 100 倍，适合大规模自动化评估。

🎯 **Interview Triggers:**
- 为什么 Pairwise 比 Pointwise 打分更可靠，背后的认知原理是什么？（WHY）
- LLM-as-Judge 和人类评估哪个更可信，什么场景必须用人工？（TRADEOFF）
- 如果评估模型和被评估模型是同一家公司的，结果可信吗？（FAILURE）

🧠 **Question Type:** principle explanation · comparison/tradeoff · debugging/failure analysis

🔥 **Follow-up Paths:**
- 三大偏差缓解 → 位置偏差交换顺序
- 评估结果校准 → 与人类标注的 Kappa 一致性
- 多模型共识 → 减少自我增强偏差

🛠 **Engineering Hooks:**
- Pairwise：每个样本交换 A/B 位置各评估一次，只取两次结论一致的样本
- 评估 prompt 末尾加 "请先给出理由，再给出评分"（CoT 减少随意打分）
- 用 GPT-4o 或 Claude Sonnet 作裁判（弱模型裁判不准）
- 与人工标注的 Cohen's Kappa ≥ 0.6 为合格
- 监控评估成本（Pairwise 样本数 = 原来的 2×）

---

## 幻觉检测与分类

> **一句话理解：** 幻觉是 LLM 生成听起来合理但实际错误或无法验证的信息，分为内在幻觉（与上下文矛盾）和外在幻觉（编造事实），检测靠原子声明分解 + 逐一验证。

**核心结论（可背）：**
```
幻觉分类：
  内在幻觉（Intrinsic Hallucination）：
    生成内容与提供的 context/source 直接矛盾
    例：文档说"公司成立于2010年"，LLM 说"成立于2015年"
    检测：NLI 模型或 LLM 判断声明是否与 context 一致

  外在幻觉（Extrinsic Hallucination）：
    生成内容无法从 context 中验证（超出范围的编造）
    例：文档未提及 CEO 姓名，LLM 编造了一个名字
    检测：更难，需要外部知识库或人工核查

  幻觉成因：
    训练数据噪声（错误信息混入训练集）
    过度自信（LLM 倾向于给出确定性答案而非"不知道"）
    知识截止（训练后的新事件）
    长 context 中的注意力分散
```

**机制解释：**
```
FActScore 框架（Min et al. 2023）：
  步骤：
  1. 将 LLM 输出拆分为原子事实声明（Atomic Facts）
     例："爱因斯坦生于1879年，在德国乌尔姆" → 两个原子声明
  2. 对每个原子声明，用检索+LLM 判断是否有来源支持
  3. FActScore = 有支持的声明数 / 总声明数

SelfCheckGPT（不需要外部知识库）：
  核心思路：对同一问题多次采样，不一致的声明更可能是幻觉
  ① 对同一问题生成 n 个独立回答
  ② 对每个声明，检查它在其他 n-1 个回答中是否一致
  ③ 一致性低 → 幻觉概率高

RAG 场景的幻觉检测：
  Faithfulness = 答案中有 context 支持的声明比例
  具体：原子声明 → LLM 判断 context 是否支持
  RAGAS 框架自动计算
```

**面试官常问：**
```
Q: 怎么减少 LLM 幻觉？
A: ① RAG：提供外部 context，约束 LLM "只基于以下文档回答"
   ② 温度降低：Temperature 接近 0，减少随机性
   ③ RLHF/Constitutional AI：训练阶段减少幻觉倾向
   ④ 让 LLM 表达不确定性："我不确定" / "根据我的知识..."
   ⑤ 输出后验证：FActScore / SelfCheckGPT 自动检测

Q: LLM 能自己检测自己的幻觉吗？
A: 有限度地可以。Self-consistency 检查（多次采样不一致 → 可能幻觉）有效果，
   但 LLM 经常对错误答案也表现出高置信度。
   SelfCheckGPT 利用的正是这种不一致性来检测，但需要多次推理（成本高）。
```

**易错点：**
- ❌ RAG 完全消除幻觉 → ✅ RAG 提供 context 约束，但 LLM 仍可能忽略 context 或对 context 外的问题幻觉
- ❌ 幻觉只有"说错事实"这一种 → ✅ 还包括：引用不存在的文献、编造引号中的人名、夸大数字等多种形式

**面试30秒回答：**
> 幻觉分两类：内在幻觉（与给定 context 矛盾）和外在幻觉（无法从 context 验证的编造）。最实用的检测框架是 FActScore：把 LLM 输出拆成原子声明逐一验证，准确率有来源支持的声明比例即为分数。SelfCheckGPT 不需要外部知识库：多次采样，不一致的声明更可能是幻觉。减少幻觉的优先手段：RAG 提供约束 context + 让 LLM 表达不确定性 + 降低 Temperature。

🎯 **Interview Triggers:**
- 内在幻觉和外在幻觉在检测难度上有什么本质差异？（WHY）
- SelfCheckGPT 和 FActScore 各自适合什么场景？（TRADEOFF）
- RAG 场景下 LLM 忽略 context 用自己的知识回答，算哪种幻觉？（FAILURE）

🧠 **Question Type:** principle explanation · comparison/tradeoff · debugging/failure analysis

🔥 **Follow-up Paths:**
- 内在幻觉检测 → NLI 模型（entailment/contradiction）分类
- 外在幻觉 → FActScore 原子声明 + 知识库验证
- 减少幻觉 → RAG 约束 + Temperature 降低

🛠 **Engineering Hooks:**
- FActScore：原子声明粒度建议句子级（不要段落级），召回用 Wikipedia 或内部知识库
- SelfCheckGPT 采样数：5 次足够，每次 `temperature=1.0` 最大多样性
- 幻觉监控指标：生产中每日抽样 50~100 条，Faithfulness < 0.8 时触发告警
- NLI 模型：`cross-encoder/nli-deberta-v3-base`（开源，快速）

---

## RAG 评估（RAGAS）

> **一句话理解：** RAGAS 用四个指标自动评估 RAG 系统——Faithfulness（答案忠于 context 防幻觉）和 Answer Relevancy（答案回答了问题）不需要 Ground Truth，是快速迭代的核心指标。

**核心结论（可背）：**
| 指标 | 评估的是 | 是否需要 GT | 低分说明 |
|---|---|---|---|
| Faithfulness | 答案声明全部来自 context（反幻觉） | 否 | LLM 在编造 context 外的信息 |
| Answer Relevancy | 答案确实回答了问题 | 否 | LLM 答非所问或偏题 |
| Context Recall | 检索找到了所有必要信息 | 是 | 检索漏掉关键信息 |
| Context Precision | 检索结果都是有用的 | 是 | 检索引入太多无关噪声 |
| Answer Correctness | 答案事实准确性（综合） | 是 | 答案有错误信息 |

**机制解释：**
```
Faithfulness 计算：
  1. LLM 将答案拆分为原子声明列表
  2. 对每个声明，LLM 判断是否有 context 支撑
  3. Faithfulness = 有支撑的声明数 / 总声明数
  Faithfulness = 1.0 → 所有声明都在 context 中找到依据（无幻觉）

Answer Relevancy 计算：
  1. LLM 根据答案反向生成若干可能问题
  2. 计算这些反向问题与原始问题的 Embedding 余弦相似度
  3. 相似度高 → 答案确实在回答这个问题

诊断逻辑：
  Faithfulness 低 + Answer Relevancy 高：
    → LLM 在答题，但引入了 context 外的信息（幻觉）
    → 优化：加强 prompt 约束，改善检索质量
  Faithfulness 高 + Context Recall 低：
    → LLM 忠于 context，但检索漏掉了关键信息
    → 优化：改进检索策略（混合检索、增大 Top-K）
```

**面试官常问：**
```
Q: 没有 Ground Truth 时如何评估 RAG？
A: 用 Faithfulness + Answer Relevancy 两个无需 GT 的指标。
   ① Faithfulness 检查幻觉（答案是否忠于检索内容）
   ② Answer Relevancy 检查相关性（答案是否回答了问题）
   两者结合可以覆盖最重要的失败模式，无需人工标注。

Q: RAGAS 自身可靠吗？RAGAS 评分高就代表 RAG 效果好吗？
A: RAGAS 本身用 LLM 作裁判，有 LLM-as-Judge 的偏差问题。
   建议：① 用强模型（GPT-4o）作裁判 ② 定期用人工校验 RAGAS 分数
   RAGAS 分数高是必要条件，不是充分条件——还需要端到端的用户满意度验证。
```

**易错点：**
- ❌ Faithfulness 高就代表 RAG 没问题 → ✅ 还要检查 Answer Relevancy（不答非所问）和 Context Recall（检索完整性）
- ❌ RAGAS 评估不需要强 LLM → ✅ RAGAS 用 LLM 作裁判，弱模型会给出不准确的评分，推荐 GPT-4o

**面试30秒回答：**
> RAGAS 的两个核心无需 GT 的指标：Faithfulness（把答案拆成原子声明，LLM 检查每条是否有 context 支撑，低分=幻觉）和 Answer Relevancy（根据答案反向生成问题，与原问题相似度高=没答非所问）。有 GT 时再加 Context Recall（检索是否完整）和 Context Precision（检索是否精准）。诊断逻辑：Faithfulness 低→幻觉问题改 prompt；Recall 低→检索质量改检索策略。

🎯 **Interview Triggers:**
- RAGAS 的 Faithfulness 指标低，应该优化检索还是生成，如何区分？（FAILURE）
- 没有 Ground Truth 能做完整的 RAG 评估吗？（TRADEOFF）
- RAGAS 本身用 LLM 作裁判，怎么保证 RAGAS 评估结果可信？（WHY）

🧠 **Question Type:** debugging/failure analysis · performance optimization · principle explanation

🔥 **Follow-up Paths:**
- Faithfulness 低 → 区分是检索噪声还是 Prompt 约束问题
- Context Recall 低 → 回到混合检索/Top-K 调整
- 评估结果可信度 → 人工校验 RAGAS 样本

🛠 **Engineering Hooks:**
- 评估触发：每次改动 Prompt/检索策略/Re-ranker 后自动跑 RAGAS
- 最小评估集：100 条（含长文档、多跳问题、无答案问题各占比 20%）
- 达标线参考：`Faithfulness > 0.8`，`Answer Relevancy > 0.8`
- 裁判模型：GPT-4o（最准，$0.005/次）vs Claude Haiku（省钱，但稍差）
- 每月人工抽 20~30 条对比 RAGAS 和人工结论，计算一致性

---

## 对齐评估（RLHF / DPO）

> **一句话理解：** 对齐评估衡量 LLM 是否符合人类价值观（有用、无害、诚实），核心指标是与基线的人类偏好胜率（win rate），传统 NLP 指标在这里无效。

**核心结论（可背）：**
```
对齐三目标（Anthropic 3H）：
  Helpful（有用）：回答用户问题，完成任务
  Harmless（无害）：不产生有害、歧视性、危险内容
  Honest（诚实）：不虚假，能表达不确定性，不欺骗

主要对齐方法：
  RLHF（Reinforcement Learning from Human Feedback）：
    ① 人类标注偏好对（A 比 B 好）
    ② 训练奖励模型（Reward Model）学习偏好
    ③ PPO 强化学习优化 LLM 最大化奖励
    代价：复杂、不稳定、需要大量人工标注

  DPO（Direct Preference Optimization，2023）：
    跳过奖励模型，直接在偏好对上优化 LLM
    更简单稳定，已成为 RLHF 的常用替代
    公式：最大化"好回答"与"差回答"的对数概率差

  Constitutional AI（Claude 的方法）：
    用一组原则（Constitution）让 LLM 自我批评和修改
    减少人工标注依赖

评估指标：
  Win Rate：与基线模型（如上一版本）的 Pairwise 比较胜率
  Human Preference Score：人工 Pairwise 比较结果
  Arena ELO：Chatbot Arena 的真实用户盲测 ELO 分数
  Safety Rate：有害输出比例（越低越好）
```

**面试官常问：**
```
Q: 为什么 BLEU/ROUGE 不适合评估对话 LLM？
A: BLEU/ROUGE 基于 n-gram 重叠，评估生成文本与参考答案的字符相似度。
   对话任务没有唯一正确答案，语义相同的回答可能字符完全不同。
   LLM 评估需要语义理解，用 LLM-as-Judge 或人类偏好评估更合适。

Q: DPO 比 RLHF 好在哪里？
A: DPO 优点：不需要单独训练奖励模型，训练更稳定，实现更简单。
   DPO 局限：对偏好数据质量要求更高，某些复杂对齐场景效果不如 RLHF。
   实际趋势：2023 年后 DPO 及其变体（KTO、IPO）成为主流。
```

**易错点：**
- ❌ 对齐评估用 BLEU 分数 → ✅ BLEU/ROUGE 衡量字符相似度，对开放生成任务无意义；用 Win Rate 或 LLM-as-Judge
- ❌ RLHF 训练后模型对齐一劳永逸 → ✅ 对齐是持续工程，用户行为和价值观在变化，需要持续收集偏好数据和迭代

**面试30秒回答：**
> 对齐评估衡量 LLM 的有用性、无害性和诚实性，核心指标是人类偏好胜率（Win Rate）——与基线模型 Pairwise 比较，人类选择哪个更好。技术上：RLHF 用人类偏好数据训练奖励模型再 PPO 强化学习，复杂但效果强；DPO 跳过奖励模型直接优化偏好对，更简单稳定，是 2023 年后的主流方案。BLEU/ROUGE 对这类任务无意义——同义不同词的答案 BLEU 分数为零但质量一样好。

🎯 **Interview Triggers:**
- 为什么对话 LLM 评估不用 BLEU/ROUGE？（WHY）
- RLHF 和 DPO 各自的核心局限是什么？（TRADEOFF）
- 奖励模型被 hack（reward hacking）是什么意思，怎么检测？（FAILURE）

🧠 **Question Type:** comparison/tradeoff · principle explanation · debugging/failure analysis

🔥 **Follow-up Paths:**
- 奖励模型 → RM 训练数据质量决定上限
- DPO 变体 → KTO/IPO 更稳定
- 对齐评估 → Win Rate vs base model

🛠 **Engineering Hooks:**
- 对齐评估核心指标：Win Rate（与上一版本 Pairwise 胜率，目标 >50%）
- DPO 数据格式：`{"prompt": ..., "chosen": ..., "rejected": ...}`，quality > quantity
- 偏好数据质量：标注者间一致性 Cohen's Kappa ≥ 0.7 才可用
- Reward Hacking 检测：奖励分数高但人类评分低（奖励和真实偏好脱钩），定期人工校验
- 监控 Safety Rate（有害输出比例）和 Refusal Rate（过度拒绝比例）

---

## 基准测试与评估体系

> **一句话理解：** MMLU/HumanEval 等基准测试提供可复现的量化对比，但存在饱和和数据污染风险；Chatbot Arena 的真实用户盲测偏好最接近实际效果。

**核心结论（可背）：**
| 基准 | 测试内容 | 优点 | 局限 |
|---|---|---|---|
| MMLU | 57 学科多选题（高中到专业） | 覆盖广，标准化 | 选项题，不测生成能力 |
| HumanEval | 164 道 Python 编程题（Pass@k） | 代码能力量化 | 题目已被大量学习，泄露严重 |
| HELM | 多任务 Holistic 评估（斯坦福） | 全面、标准化 | 复杂，更新慢 |
| BIG-Bench Hard | 200+ 困难推理任务 | 区分度高 | 部分任务争议 |
| Chatbot Arena | 真实用户盲测 Pairwise（ELO） | 最接近真实偏好 | 慢、成本高、领域不均 |
| MT-Bench | GPT-4 评分的多轮对话 | 快速、可自动化 | LLM-as-Judge 偏差 |

**机制解释：**
```
基准测试的主要问题：
  1. 数据污染（Data Contamination）：
     训练数据包含测试集 → 分数虚高（过拟合基准）
     已有研究发现多个模型可能有不同程度的污染

  2. 基准饱和（Benchmark Saturation）：
     顶级模型都在 MMLU 上 90%+ → 区分度不够
     → 需要更难的基准（GPQA Diamond，博士级问题）

  3. 泛化性问题：
     基准高分 ≠ 实际任务表现好
     需要在自己的业务任务上做 domain-specific eval

自建评估体系建议：
  ① 业务相关 test cases（最重要）
  ② RAGAS（RAG 场景）/ LLM-as-Judge（对话场景）
  ③ 少量参考公开基准作为横向对比
  ④ 人工抽样验证（定期校准自动评估准确性）
```

**面试官常问：**
```
Q: 选型时应该看哪个基准？
A: 没有万能基准，要看业务场景：
   通用推理/知识：MMLU + GPQA
   代码生成：HumanEval + LiveCodeBench（抗污染）
   对话质量：Chatbot Arena ELO（最可信）
   RAG/问答系统：自建 eval + RAGAS
   最重要的是：在自己的业务数据上测，不要只看公开基准。

Q: 如何判断一个模型是否在基准上有数据污染？
A: ① 用未公开的私有测试集测试
   ② 测试轻微改写的题目（如改数字、换人名），若分数大幅下降则可能过拟合
   ③ 对比模型发布时间和基准数据创建时间
   ④ 参考有污染分析的第三方评测报告
```

**易错点：**
- ❌ 基准分数高的模型一定适合我的业务 → ✅ 基准是通用参考，业务适配性必须在自己的数据上验证
- ❌ 公开基准能客观反映模型能力 → ✅ 数据污染、基准饱和、测试方式差异使公开基准可信度下降，Chatbot Arena 是目前最可靠的

**面试30秒回答：**
> 主要基准：MMLU 测多学科知识选择题，HumanEval 测 Python 代码生成，Chatbot Arena 是真实用户盲测 ELO 排名。注意两个主要问题：数据污染（训练数据包含测试集导致分数虚高）和基准饱和（顶级模型都 90%+，区分度差）。选型原则：Chatbot Arena 最接近真实偏好，但对业务适配性必须在自己的数据上测——公开基准只作横向参考。自建评估体系：业务 test cases + LLM-as-Judge + 人工抽样校验。

🎯 **Interview Triggers:**
- 为什么不能只看公开基准选模型，还要在自己数据上测？（WHY）
- Chatbot Arena 和 MMLU 分别适合用来判断什么？（TRADEOFF）
- 如何判断一个模型是否在某基准上有数据污染？（FAILURE）

🧠 **Question Type:** comparison/tradeoff · system design · debugging/failure analysis

🔥 **Follow-up Paths:**
- 自建 eval set → 业务场景覆盖
- 数据污染检测 → 私有测试集 + 改写题目测试
- 模型选型决策 → Chatbot Arena + 业务 eval 双重验证

🛠 **Engineering Hooks:**
- 自建 eval set 最低 200 条，覆盖：正常 case / 边缘 case / 对抗 case 各 1/3
- 污染测试：用改写版题目（换数字/人名）对比原题得分，分数大幅下降则可能污染
- 模型升级决策：新模型在 eval set 上显著优于当前模型（p-value < 0.05）才升级
- 监控基准分数趋势（每次迭代后跑 eval CI）
- 记录每个 eval 样本的逐条分数，失败案例归类分析

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| LLM-as-Judge 是什么？ | 用强模型（GPT-4o）自动评估 LLM 输出，替代人工标注，速度快 100× |
| Pairwise vs Pointwise？ | Pairwise（A vs B 更好）更可靠；Pointwise（单独打分）简单但分数绝对值不稳 |
| LLM-as-Judge 有哪些偏差？ | 位置偏差（交换顺序缓解）、冗长偏差（prompt 说明）、自我增强偏差（多模型共识）|
| 幻觉分哪两类？ | 内在幻觉（与 context 矛盾）、外在幻觉（编造 context 外信息）|
| FActScore 是什么？ | 原子声明分解 + 逐一验证有无来源支撑，分数 = 有支撑声明比例 |
| SelfCheckGPT 原理？ | 多次采样，不一致的声明更可能是幻觉，不需要外部知识库 |
| RAGAS 四大指标？ | Faithfulness + Answer Relevancy（无需GT）+ Context Recall + Context Precision（需GT）|
| RLHF vs DPO？ | RLHF：训练奖励模型+PPO，复杂；DPO：直接优化偏好对，简单稳定，2023后主流 |
| 为什么不用 BLEU 评估对话？ | BLEU 衡量字符 n-gram 重叠，开放生成无唯一答案，语义等价的回答 BLEU 为零 |
| 选型看哪个基准最可靠？ | Chatbot Arena（真实用户盲测 ELO）最可信；业务适配性必须在自己数据上测 |
