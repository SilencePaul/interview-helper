# HTML

---

## 速览

- DOCTYPE 声明告诉浏览器使用标准模式（W3C）还是怪异模式（Quirks），必须写在第一行。
- HTML 语义化 = 用正确的标签表达内容结构，利于 SEO、可访问性、可维护性。
- HTML5 新增：语义化标签、Canvas/SVG、LocalStorage/SessionStorage、WebSocket、WebWorker、视频/音频标签。
- src vs href：src 嵌入资源（阻塞解析），href 建立链接（不阻塞）。
- defer vs async：都异步下载 JS；defer 等 DOM 解析完再执行（有顺序），async 下载完立即执行（无顺序）。
- link vs @import：link 与 HTML 同步加载，@import 页面加载完才加载，推荐用 link。

---

## DOCTYPE 与渲染模式

> **一句话理解：** `<!DOCTYPE html>` 告诉浏览器用标准模式渲染，否则可能触发怪异模式（各浏览器行为不一致）。

**核心结论（可背）：**
| 模式 | 触发条件 | 行为 |
|---|---|---|
| 标准模式（Strict mode） | 有正确的 DOCTYPE 声明 | 按 W3C 标准解析 CSS 和 JS |
| 怪异模式（Quirks mode） | DOCTYPE 缺失或错误 | 各浏览器用自己的方式兼容旧页面 |

```html
<!-- HTML5 标准写法（推荐） -->
<!DOCTYPE html>
```

🎯 **Interview Triggers:**
- DOCTYPE 缺失会有什么影响？（FAILURE）
- 怪异模式和标准模式的具体差异有哪些？（COMPARISON）
- HTML5 的 DOCTYPE 为什么比以前简单？（EVOLUTION）

🧠 **Question Type:** failure analysis · comparison · historical context

🔥 **Follow-up Paths:**
- DOCTYPE 缺失 → 怪异模式 → 盒模型计算方式不同 → 布局混乱
- 怪异模式差异 → IE 盒模型（border-box 默认） vs W3C 盒模型（content-box）
- HTML5 DOCTYPE → 不再基于 SGML DTD → 只需 `<!DOCTYPE html>` 即可

🛠 **Engineering Hooks:**
- 所有 HTML 文件首行必须 `<!DOCTYPE html>`，缺失会导致跨浏览器样式差异
- 用 W3C 验证器检测页面是否在标准模式下渲染
- 旧项目迁移：DOCTYPE 修复 + `box-sizing: border-box` 全局设置通常是必须的第一步

---

## HTML 语义化

> **一句话理解：** 语义化 = 用 `<nav>` 代替 `<div class="nav">`，让标签自带含义，机器和人都能理解页面结构。

**核心结论（可背）：**
| 标签 | 语义含义 |
|---|---|
| `<header>` | 页眉，含 logo、导航、搜索框 |
| `<nav>` | 导航链接区域 |
| `<main>` | 页面主要内容区域 |
| `<section>` | 文档中的一个章节/区段 |
| `<article>` | 独立的内容块（如一篇文章） |
| `<aside>` | 侧边栏、补充内容 |
| `<footer>` | 页脚 |

**语义化的好处：**
```
① 可读性：代码结构清晰，便于开发和维护
② SEO：搜索引擎更好地理解页面内容，提升排名
③ 可访问性：盲人阅读器等辅助设备能正确解析
④ 无 CSS 时：页面也能呈现合理的内容结构
```

🎯 **Interview Triggers:**
- HTML 语义化的好处有哪些？（BENEFIT）
- `<article>` 和 `<section>` 有什么区别？（DETAIL）
- 什么情况下用 `<div>` 比语义化标签更合适？（TRADEOFF）

🧠 **Question Type:** benefit enumeration · distinction · pragmatic tradeoff

🔥 **Follow-up Paths:**
- SEO → 搜索引擎爬虫优先识别语义标签 → 提升页面权重
- 可访问性 → 屏幕阅读器 ARIA → WCAG 标准
- article vs section → article 独立可复用，section 章节划分

🛠 **Engineering Hooks:**
- `<main>` 每页只用一个（屏幕阅读器跳转主内容的锚点）
- 列表数据用 `<ul>/<ol>/<li>` 而非 `<div>`，利于 SEO 和可访问性
- `<button>` 代替 `<div onclick>` —— 语义正确且自带键盘支持（Enter/Space 触发）

---

## defer vs async

> **一句话理解：** 都是异步加载 JS；defer 等 DOM 解析完顺序执行，async 下载完立即执行（不保证顺序）。

**核心结论（可背）：**
```
普通 <script>：阻塞 DOM 解析，下载+执行完才继续
  ─── DOM 解析 ──┤ 等待 JS ├── DOM 解析 ───>

<script async>：并行下载，下载完立即执行（可能打断 DOM 解析）
  ─── DOM 解析 ──────────────────────>
  ───── JS 下载 ──┤ 立即执行 ├

<script defer>：并行下载，DOM 解析完后按序执行
  ─── DOM 解析 ──────────────────────>
  ───── JS 下载 ──────────────────────┤ 顺序执行
```

| 属性 | 执行时机 | 执行顺序 | 适用场景 |
|---|---|---|---|
| `async` | 下载完立即执行 | 不保证顺序 | 独立脚本（如统计、广告） |
| `defer` | DOM 解析完后按序执行 | 保证文档顺序 | 有依赖关系的脚本 |

🎯 **Interview Triggers:**
- defer 和 async 的区别，各自适用什么场景？（COMPARISON）
- 为什么推荐把 script 放在 body 底部？defer 能替代这个做法吗？（EVOLUTION）
- 多个 async 脚本的执行顺序是什么？（DETAIL）

🧠 **Question Type:** comparison · evolution · execution detail

🔥 **Follow-up Paths:**
- script 底部 → 等 DOM 构建完 → defer 解决同样问题且不影响 HTML 位置
- async 无序 → 多个 async 谁先下完谁先执行 → 不适合有依赖的脚本
- DOMContentLoaded 事件 → defer 脚本执行完后才触发

🛠 **Engineering Hooks:**
- 现代项目统一用 `<script defer src="...">` 放在 `<head>` 中（兼顾性能和顺序）
- 第三方无依赖统计脚本（Google Analytics）用 `async`，不阻塞也不依赖其他脚本
- `type="module"` 的 script 默认等同 defer 行为

---

## src vs href

> **一句话理解：** src 把资源嵌入页面（阻塞解析），href 只是建立引用链接（不阻塞）。

**核心结论（可背）：**
| 属性 | 含义 | 行为 | 典型标签 |
|---|---|---|---|
| `src` | source，资源嵌入到文档中 | 浏览器遇到 src 会暂停页面解析，下载并执行 | `<script>/<img>/<iframe>` |
| `href` | hypertext reference，建立文档与资源的链接 | 浏览器并行下载，不暂停页面解析 | `<a>/<link>` |

🎯 **Interview Triggers:**
- src 为什么会阻塞 DOM 解析？（MECHANISM）
- `<img src>` 和 `<link href>` 都是加载外部资源，为什么行为不同？（COMPARISON）
- 如何优化 src 资源加载性能？（OPTIMIZATION）

🧠 **Question Type:** mechanism · comparison · optimization

🔥 **Follow-up Paths:**
- src 阻塞 → JS 需立即执行（可能操作 DOM） → 必须等待下载完
- img src → 不阻塞 HTML 解析，但阻塞页面完全加载（onload 事件）
- 优化 → defer/async/懒加载/预加载（preload/prefetch）

🛠 **Engineering Hooks:**
- 图片用 `loading="lazy"` 实现原生懒加载（屏幕外不加载）
- 关键 CSS 用 `<link rel="preload" as="style">` 预加载，减少渲染阻塞
- CDN 资源的 `<script src>` 可加 `crossorigin="anonymous"` + SRI（子资源完整性校验）

---

## link vs @import

> **一句话理解：** link 并行加载 CSS，@import 串行（页面加载完才加载），始终推荐用 link。

**核心结论（可背）：**
| 维度 | `<link>` | `@import` |
|---|---|---|
| 语言属性 | HTML 标签 | CSS 语法 |
| 加载时机 | 与 HTML 同时加载 | 页面加载完毕后加载（可能白屏） |
| JS 可控 | 可通过 DOM 动态添加 | 不能动态添加 |
| 兼容性 | 无问题 | IE5+ 才支持 |
| 权重 | 高于 @import | — |

🎯 **Interview Triggers:**
- 为什么不推荐在生产环境用 @import？（FAILURE）
- link 和 @import 的加载时机为什么不同？（MECHANISM）
- 什么场景下 @import 是合理的用法？（SCENARIO）

🧠 **Question Type:** failure analysis · mechanism · valid use case

🔥 **Follow-up Paths:**
- @import 延迟加载 → CSSOM 构建延迟 → 渲染阻塞延长 → 白屏时间增加
- 动态加载 CSS → JS 操作 link DOM → @import 无法动态控制
- @import 合理场景 → CSS 预处理器（Sass/Less）中组织文件结构（编译后消除）

🛠 **Engineering Hooks:**
- 生产环境永远用 `<link rel="stylesheet">` 加载 CSS，禁止 @import
- Sass/Less 中 @import 由构建工具合并，最终只输出一个 link 标签
- 多主题切换用 JS 动态添加/替换 link 标签实现，@import 无法做到

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| DOCTYPE 的作用？ | 告诉浏览器用标准模式，避免怪异模式各浏览器行为不一致 |
| 语义化 HTML 的好处？ | 可读性、SEO 友好、可访问性（屏幕阅读器），无 CSS 时结构依然清晰 |
| src vs href？ | src 嵌入资源（阻塞解析）；href 建立链接（不阻塞） |
| defer vs async？ | async 下载完立即执行（无序）；defer DOM 解析后按序执行 |
| link vs @import？ | link 同步加载，@import 延迟加载；link 可被 JS 控制，@import 不能 |
| HTML5 最重要的新特性？ | 语义化标签、WebSocket、WebWorker、LocalStorage、Canvas、Video/Audio |
