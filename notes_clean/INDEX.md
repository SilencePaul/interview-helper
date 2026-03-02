# 面试八股文索引

> 共 41 篇，按专题分类，每篇均含 速览 / 核心结论（可背）/ 面试高频考点汇总。

---

## 前端（6篇）

| 笔记 | 核心主题 |
|---|---|
| [HTML](./前端/HTML.md) | DOCTYPE、语义化、HTML5新特性、src vs href、defer vs async、link vs @import |
| [CSS](./前端/CSS.md) | 盒模型、BFC、选择器优先级、重排/重绘/合成、Flex布局、定位、CSS单位、清除浮动 |
| [Javascript](./前端/Javascript.md) | 数据类型、原型链、继承、闭包、this、Promise、async/await、ES6特性、事件委托、GC |
| [VUE](./前端/VUE.md) | MVVM、响应式(defineProperty/Proxy)、生命周期、组件通信、Vue Router、Vuex、Vue3 |
| [React](./前端/React.md) | JSX、state/props、Hooks、生命周期、Redux、React Router、Fiber、React18 |
| [浏览器与网络](./前端/浏览器与网络.md) | 多进程架构、事件循环、跨域、输入URL全流程、HTTP缓存、HTTP/2、浏览器存储 |

---

## 数据库（7篇）

| 笔记 | 核心主题 |
|---|---|
| [数据库基础](./数据库/数据库基础.md) | 三大范式、ER图、关系型vs非关系型、SQL分类(DDL/DML/DCL) |
| [索引](./数据库/索引.md) | B+树原理、聚簇/非聚簇、覆盖索引、最左前缀、索引失效、EXPLAIN |
| [事务](./数据库/事务.md) | ACID、隔离级别、脏读/不可重复读/幻读、MVCC、undo log |
| [锁](./数据库/锁.md) | 行锁/表锁、共享锁/排他锁、意向锁、间隙锁、死锁检测 |
| [引擎](./数据库/引擎.md) | InnoDB vs MyISAM、InnoDB特性（事务/行锁/外键/MVCC） |
| [日志](./数据库/日志.md) | redo log（崩溃恢复）、undo log（回滚/MVCC）、binlog（主从复制）、两阶段提交 |
| [mySQL语句](./数据库/mySQL语句.md) | SELECT/JOIN/GROUP BY/HAVING、子查询、窗口函数、常用函数 |
| [Redis](./数据库/Redis.md) | 数据结构、持久化(RDB/AOF)、淘汰策略、缓存穿透/击穿/雪崩、主从/哨兵/集群 |

---

## 计算机网络（6篇）

| 笔记 | 核心主题 |
|---|---|
| [网络基础](./计算机网络/网络基础.md) | OSI七层、TCP/IP四层、IP地址、子网划分、路由、ARP/DNS |
| [传输协议](./计算机网络/传输协议.md) | TCP三次握手/四次挥手、可靠传输、流量控制、拥塞控制、TCP vs UDP |
| [应用层协议](./计算机网络/应用层协议.md) | HTTP方法/状态码、HTTPS(TLS握手)、HTTP/1.1/2/3、WebSocket |
| [浏览器](./计算机网络/浏览器.md) | 输入URL全流程、渲染管线、重排/重绘、JS阻塞、资源加载优化 |
| [网络安全](./计算机网络/网络安全.md) | XSS、CSRF、SQL注入、HTTPS、CSP、SameSite Cookie |
| [计算机系统](./计算机网络/计算机系统.md) | 冯诺依曼体系、CPU、内存、缓存(局部性原理)、I/O |

---

## 操作系统（7篇）

| 笔记 | 核心主题 |
|---|---|
| [操作系统基础](./操作系统/操作系统基础.md) | OS职责、系统调用、用户态/内核态切换、中断机制 |
| [线程与进程](./操作系统/线程与进程.md) | 进程vs线程、PCB、进程状态、调度算法、上下文切换、协程 |
| [互斥与同步](./操作系统/互斥与同步.md) | 临界区、互斥锁、信号量、条件变量、死锁(4条件/银行家算法) |
| [存储系统](./操作系统/存储系统.md) | 虚拟内存、分页/分段、页表、TLB、缺页中断、页面置换算法 |
| [文件系统](./操作系统/文件系统.md) | 文件组织、inode、目录、链接(硬链接/软链接)、文件描述符 |
| [磁盘系统](./操作系统/磁盘系统.md) | 磁盘结构、寻道/旋转/传输时间、磁盘调度算法(SSTF/SCAN) |
| [Linux](./操作系统/Linux.md) | 常用命令、文件权限、进程管理、网络工具、Shell脚本基础 |

---

## 设计模式（7篇）

| 笔记 | 核心主题 |
|---|---|
| [单例模式](./设计模式/单例模式.md) | 保证全局唯一实例、懒汉式/饿汉式、线程安全实现 |
| [工厂模式](./设计模式/工厂模式.md) | 简单工厂/工厂方法/抽象工厂，解耦对象创建与使用 |
| [建造者模式](./设计模式/建造者模式.md) | 分步构建复杂对象，链式调用，分离构建过程和表示 |
| [代理模式](./设计模式/代理模式.md) | 静态代理/动态代理，访问控制、懒加载、日志、缓存 |
| [观察者模式](./设计模式/观察者模式.md) | 发布-订阅，Subject/Observer，事件驱动架构基础 |
| [策略模式](./设计模式/策略模式.md) | 算法族封装，运行时切换策略，消除 if-else |
| [装饰器模式](./设计模式/装饰器模式.md) | 动态扩展对象功能，不修改原类，组合优于继承 |

---

## LLM 大模型（7篇）

| 笔记 | 核心主题 |
|---|---|
| [LLM基础](./llm/LLM基础.md) | Transformer架构、Self-Attention(O(n²))、Tokenization(BPE/WordPiece)、预训练/SFT/RLHF |
| [提示词工程](./llm/提示词工程.md) | Zero-shot/Few-shot/Role Prompting、CoT、Self-Consistency、ReAct、System Prompt设计 |
| [RAG检索增强](./llm/RAG检索增强.md) | RAG三代演进(Naive→Advanced→Modular)、向量检索、查询改写、重排序、RAGAS评估 |
| [智能体](./llm/智能体.md) | Agent架构(LLM+工具+记忆+规划)、ReAct框架、Function Calling、多Agent协作 |
| [推理系统](./llm/推理系统.md) | 量化(GPTQ/AWQ INT4/INT8)、Continuous Batching、PagedAttention、KV Cache、vLLM |
| [LLM工程实践](./llm/LLM工程实践.md) | Token成本控制、前缀缓存、Batch API、流式输出(SSE)、TTFT/TPOT延迟指标 |
| [评估](./llm/评估.md) | LLM-as-Judge、Pairwise vs Pointwise、位置/冗长/自我增强偏差、自动化评估流程 |

---

## 快速复习路线

**一轮（掌握核心）：** HTML → CSS → Javascript → 计算机网络/传输协议 → 数据库/索引 → 数据库/事务 → 操作系统/线程与进程

**二轮（深入扩展）：** VUE → React → 浏览器与网络 → 数据库/锁 → 数据库/Redis → 操作系统/存储系统 → 设计模式全部

**三轮（查漏补缺）：** 根据面试反馈，重点复习高频考点汇总表中的薄弱项

**LLM 专题：** LLM基础 → 提示词工程 → RAG检索增强 → 智能体 → 推理系统 → LLM工程实践 → 评估
