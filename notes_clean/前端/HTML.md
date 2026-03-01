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

---

## HTML5 新特性

> **一句话理解：** HTML5 把浏览器变成了一个完整的应用平台，不再依赖 Flash/插件。

**核心结论（可背）：**
| 特性 | 说明 |
|---|---|
| 语义化标签 | `<header>/<nav>/<footer>/<article>/<section>` |
| 媒体标签 | `<video>/<audio>` 取代 Flash |
| 本地存储 | `localStorage`（持久）、`sessionStorage`（会话） |
| Canvas / SVG | 2D 绘图 API |
| WebSocket | 全双工实时通信协议 |
| WebWorker | 后台多线程 JS，不阻塞 UI |
| Geolocation | 地理位置 API（需用户授权） |
| 拖拽 API | 原生拖放事件 |
| 新表单控件 | `url/date/time/email/search` |
| PostMessage | 跨窗口/跨域通信 |

**移除的元素：**
```
纯表现性元素（用 CSS 替代）：basefont、big、center、font、s、strike、tt、u
负面可用性元素：frame、frameset、noframes
```

---

## src vs href

> **一句话理解：** src 把资源嵌入页面（阻塞解析），href 只是建立引用链接（不阻塞）。

**核心结论（可背）：**
| 属性 | 含义 | 行为 | 典型标签 |
|---|---|---|---|
| `src` | source，资源嵌入到文档中 | 浏览器遇到 src 会暂停页面解析，下载并执行 | `<script>/<img>/<iframe>` |
| `href` | hypertext reference，建立文档与资源的链接 | 浏览器并行下载，不暂停页面解析 | `<a>/<link>` |

```
JS 脚本放在 <body> 底部的原因：
  <script src="app.js"> 会阻塞 DOM 解析
  → 放底部确保 DOM 构建完后再执行 JS
  → 现代做法：用 defer 属性替代
```

---

## 行内元素 vs 块级元素

> **一句话理解：** 块级元素独占一行，可设宽高；行内元素在行内排列，宽高由内容决定。

**核心结论（可背）：**
| 维度 | 块级元素（Block） | 行内元素（Inline） |
|---|---|---|
| 排列方式 | 独占一行 | 同行显示（排满换行） |
| 宽高设置 | 可以 | 不可以（宽高由内容决定） |
| 内边距/外边距 | 四个方向都生效 | 上下方向 margin 不生效 |
| 能包含内容 | 块级 + 行内 | 只能包含文本和其他行内元素 |
| 典型标签 | `<div>/<p>/<h1~h6>/<ul>/<ol>/<li>` | `<span>/<a>/<strong>/<em>/<img>/<input>` |

```css
/* 相互转换 */
display: block;        /* 变成块级 */
display: inline;       /* 变成行内 */
display: inline-block; /* 行内但可设宽高 */
```

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

---

## iframe

> **一句话理解：** iframe 在页面中嵌套另一个网页，功能强但性能差、SEO 差，现代项目慎用。

**安全限制：**
```
X-Frame-Options 响应头：
  DENY          → 完全禁止嵌套
  SAMEORIGIN    → 只允许同源嵌套
  ALLOW-FROM URL → 允许指定域名嵌套

Content-Security-Policy: frame-ancestors 'self'
```

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
