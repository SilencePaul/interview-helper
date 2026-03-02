# CSS

---

## 速览

- 盒模型：标准盒（content-box，width 不含 padding/border）vs 怪异盒（border-box，width 含 padding/border）。
- BFC = 独立渲染区域，用于：清除浮动、防止 margin 重叠、两栏布局。
- 选择器优先级：!important > 内联(1000) > ID(100) > class/属性/伪类(10) > 标签/伪元素(1)。
- 重排 > 重绘 > 合成（代价从高到低），transform/opacity 只触发合成（GPU 加速）。
- Flex：一维布局（主轴+交叉轴）；Grid：二维布局（行+列）。
- CSS 单位：px（固定）、em（相对父/自身字体）、rem（相对根字体）、vw/vh（相对视口）。
- 清除浮动三种方式：clear 属性、BFC（overflow: hidden）、::after 伪元素（推荐）。

---

## 盒模型

> **一句话理解：** 标准盒模型 width 只算 content，怪异盒模型 width 包含 padding 和 border，`box-sizing: border-box` 让布局更直观。

**核心结论（可背）：**
| 模型 | 属性 | width 包含 | 实际占用宽度 |
|---|---|---|---|
| 标准盒（W3C） | `content-box`（默认） | 只有 content | width + padding + border |
| 怪异盒（IE） | `border-box` | content + padding + border | width（padding/border 挤压内容） |

```css
/* 推荐全局设置 border-box，更直观 */
*, *::before, *::after { box-sizing: border-box; }
```

**margin 相关：**
```
margin 纵向重叠（折叠）：
  相邻兄弟元素、父子元素（无边框/内边距分隔）的 margin 取最大值，而非相加
  解决：触发 BFC（父元素 overflow:hidden 或 display:flex）
```

🎯 **Interview Triggers:**
- 标准盒模型和 IE 盒模型有什么区别？（COMPARISON）
- margin 塌陷是什么，如何解决？（PROBLEM）
- 为什么推荐全局设置 border-box？（RECOMMENDATION）

🧠 **Question Type:** comparison · problem-solution · best practice

🔥 **Follow-up Paths:**
- border-box vs content-box → 设计稿到代码转换时哪个更直观
- margin 塌陷 → 触发 BFC 解决 → display:flex 也能防止
- 全局 border-box → 避免手动计算 padding → 框架（Bootstrap/Tailwind）默认开启

🛠 **Engineering Hooks:**
- 现代项目第一行全局 CSS 通常是 `*, *::before, *::after { box-sizing: border-box; }`
- margin 塌陷的坑：父子元素 margin-top 重叠，给父元素加 `overflow: hidden` 快速修复
- 负 margin 技巧：`margin-left: -20px` 实现多列卡片右边距消除（等价于 gap）

---

## BFC（块格式化上下文）

> **一句话理解：** BFC 是页面上的独立容器，内部元素不影响外部，可用于清除浮动、解决 margin 重叠、实现两栏布局。

**核心结论（可背）：**

**触发 BFC 的条件：**
```
① float 不为 none
② position 为 absolute 或 fixed
③ overflow 不为 visible（auto/scroll/hidden）
④ display 为 inline-block、flex、grid、table-cell
⑤ 根元素（html）
```

**BFC 的应用：**
| 场景 | 方案 |
|---|---|
| 清除浮动（防止父元素高度塌陷） | 父元素触发 BFC（`overflow: hidden`） |
| 防止 margin 重叠 | 将一个元素包裹在新 BFC 容器中 |
| 两栏布局（左浮动 + 右自适应） | 右侧 `overflow: hidden` 触发 BFC |

**清除浮动三种方式：**
```css
/* 方式1：clear 属性（空标签，不推荐） */
.clearfix-div { clear: both; }

/* 方式2：触发 BFC */
.parent { overflow: hidden; }

/* 方式3：::after 伪元素（推荐）*/
.clearfix::after {
  content: '';
  display: table;
  clear: both;
}
.clearfix { *zoom: 1; } /* 兼容 IE */
```

🎯 **Interview Triggers:**
- BFC 是什么，如何触发？（CONCEPT）
- 为什么 BFC 能解决高度塌陷问题？（MECHANISM）
- overflow:hidden 触发 BFC，但其本身的 overflow 语义和 BFC 有什么关系？（DEPTH）

🧠 **Question Type:** concept · mechanism · depth question

🔥 **Follow-up Paths:**
- BFC 独立容器 → 内部浮动元素被包含 → 父元素高度可包裹浮动子元素
- margin 重叠 → 同一 BFC 内的相邻元素发生 → 不同 BFC 内则不会
- overflow:hidden 的 BFC 副作用 → 内容超出被裁剪 → 现代项目用 `display:flow-root` 代替

🛠 **Engineering Hooks:**
- `display: flow-root` 是专门用于触发 BFC 的属性，无副作用（优于 overflow:hidden）
- Flex/Grid 容器自动是 BFC，所以 flex 布局内不会有 margin 塌陷问题
- 两栏布局（左固定+右自适应）：左 float + 右 overflow:hidden，替代 calc() 计算

---

## 选择器优先级

> **一句话理解：** 优先级由 4 位数字决定：`!important` > 内联 > ID > class/属性/伪类 > 标签/伪元素，权重从左比到右。

**核心结论（可背）：**
```
优先级（权重）：
  !important：最高优先级（破坏层叠，慎用）
  内联样式（style=""）：1000
  ID 选择器（#id）：100
  类选择器（.class）/ 属性选择器（[attr]）/ 伪类（:hover）：10
  标签选择器（div）/ 伪元素（::before）：1
  通配符(*)、关系选择符(+ > ~ ||)：0

比较规则：从左到右依次比较，大的胜出，相等则看下一位；全相等则后声明的生效
```

🎯 **Interview Triggers:**
- CSS 选择器的优先级如何计算？（CALCULATION）
- `!important` 能被覆盖吗？（EDGE-CASE）
- 为什么不建议在生产中大量使用 !important？（PRACTICE）

🧠 **Question Type:** calculation · edge case · best practice

🔥 **Follow-up Paths:**
- 权重计算 → 四位数字对比 → `#id .class tag` = 111
- !important 覆盖 → 另一个 !important + 更高权重 → 或用 JS 内联样式
- 滥用 !important → 维护困难 → 优先通过提升选择器权重解决

🛠 **Engineering Hooks:**
- CSS Modules / CSS-in-JS 通过哈希类名解决权重冲突（无需 !important）
- 动态主题切换通过内联 CSS 变量（`--color-primary`）覆盖，优先级高
- 第三方组件样式覆盖困难时，用同级 + 更具体的选择器，尽量避免 !important

---

## 重排、重绘与合成

> **一句话理解：** 重排（修改布局）最昂贵，重绘（修改外观）次之，合成（GPU 直接处理 transform/opacity）最便宜。

**核心结论（可背）：**
```
重排（Reflow/Layout）：
  触发：改变尺寸/位置/DOM 结构、resize 窗口、读取 offsetWidth 等几何属性
  代价：重新计算布局，影响整个渲染树

重绘（Repaint）：
  触发：改变颜色/背景/visibility（不影响布局）
  代价：跳过布局，直接进入绘制

合成（Composite）：
  触发：transform、opacity、filter（GPU 独立图层处理）
  代价：最低，不占主线程
```

**优化手段：**
```css
/* ❌ 差 - 触发重排 */
element.left = '100px';

/* ✅ 好 - 只触发合成 */
element.transform = 'translateX(100px)';
```

🎯 **Interview Triggers:**
- 重排和重绘的区别，哪个代价更大？（COMPARISON）
- transform 为什么比修改 left/top 性能更好？（MECHANISM）
- 频繁读写 DOM 几何属性会发生什么，如何优化？（OPTIMIZATION）

🧠 **Question Type:** comparison · mechanism · optimization

🔥 **Follow-up Paths:**
- 重排 → 重新计算布局 → 影响所有子孙节点 → 代价 O(n)
- transform → GPU 合成层 → 不影响主线程 → 60fps 流畅动画
- 批量读写 → 强制同步布局 → FastDOM / requestAnimationFrame 批处理

🛠 **Engineering Hooks:**
- 动画必用 `transform + opacity`，触发 GPU 合成层，避免重排
- `will-change: transform` 提前提升到合成层（谨慎使用，占显存）
- 读取 `offsetWidth` 等几何属性前批量完成所有 DOM 写操作（避免布局抖动）

---

## 定位（Position）

> **一句话理解：** relative 相对自身原位偏移（占位），absolute 相对最近定位祖先（脱流），fixed 相对视口（脱流），sticky 相对视口+滚动。

**核心结论（可背）：**
| 值 | 定位基准 | 是否脱离文档流 | 原位是否保留 |
|---|---|---|---|
| `static`（默认） | 正常文档流 | 否 | ✅ |
| `relative` | 自身原始位置 | 否（占位） | ✅ |
| `absolute` | 最近有 position 的祖先（非 static） | ✅ | ❌ |
| `fixed` | 视口 | ✅ | ❌ |
| `sticky` | 相对定位 + 滚过阈值变 fixed | 否 | ✅ |

```
子绝父相：父元素 position: relative，子元素 position: absolute
z-index 只对定位元素生效（position 非 static）
```

🎯 **Interview Triggers:**
- absolute 定位的基准是什么？（MECHANISM）
- sticky 定位的原理和使用条件？（MECHANISM）
- 什么情况下 fixed 元素会失效？（EDGE-CASE）

🧠 **Question Type:** mechanism · edge case · positioning rules

🔥 **Follow-up Paths:**
- absolute → 向上查找第一个非 static 祖先 → 没有则相对 viewport（初始包含块）
- sticky → 正常流中 relative，滚动到阈值后 fixed → 需父容器有固定高度
- fixed 失效 → 祖先有 transform/filter/will-change → 改变了包含块为该祖先

🛠 **Engineering Hooks:**
- 模态框遮罩用 `position:fixed; inset:0`（简写 top/right/bottom/left 全 0）覆盖全屏
- 吸顶导航用 `position:sticky; top:0`，比 JS 监听 scroll 性能好
- `z-index` 失效常因元素非定位元素，加 `position:relative` 即可生效

---

## Flex 布局

> **一句话理解：** Flex 是一维布局（主轴+交叉轴），通过 justify-content 控制主轴对齐，align-items 控制交叉轴对齐。

**核心结论（可背）：**
```css
/* 容器属性 */
display: flex;
flex-direction: row | column | row-reverse | column-reverse;
justify-content: flex-start | flex-end | center | space-between | space-around;
align-items: flex-start | flex-end | center | stretch | baseline;
flex-wrap: nowrap | wrap;
gap: 10px;

/* 子项属性 */
flex: 1;        /* flex-grow:1 flex-shrink:1 flex-basis:0（等分空间） */
flex: auto;     /* flex-grow:1 flex-shrink:1 flex-basis:auto */
flex: none;     /* flex-grow:0 flex-shrink:0 flex-basis:auto（不伸缩） */
align-self: center;
```

**居中方案（最常用）：**
```css
/* Flex 居中（推荐） */
.parent { display: flex; justify-content: center; align-items: center; }

/* transform 居中 */
.parent { position: relative; }
.child { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
```

🎯 **Interview Triggers:**
- flex: 1 代表什么，展开写是什么？（SHORTHAND）
- justify-content 和 align-items 有什么区别？（CONCEPT）
- 如何用 Flex 实现垂直居中？（IMPLEMENTATION）

🧠 **Question Type:** shorthand expansion · concept · implementation

🔥 **Follow-up Paths:**
- flex:1 展开 → flex-grow:1 flex-shrink:1 flex-basis:0 → 子项等分剩余空间
- justify vs align → 主轴（flex-direction 方向）vs 交叉轴（垂直于主轴）
- 垂直居中 → flex + align-items:center → 或 margin:auto（flex 子项）

🛠 **Engineering Hooks:**
- 等宽多列：`display:flex` + 子项 `flex:1`，无需计算百分比宽度
- 最后一行左对齐：Flex + `justify-content:space-between` 时最后行变形，用幽灵元素/Grid 解决
- `gap` 属性（现代浏览器全支持）代替 margin 实现子项间距，避免首尾多余间距

---

## CSS 单位

> **一句话理解：** px 固定像素，em 相对父元素/自身字体，rem 相对根元素字体（推荐响应式），vw/vh 相对视口。

**核心结论（可背）：**
| 单位 | 参照 | 适用场景 |
|---|---|---|
| `px` | 绝对像素 | 固定尺寸、边框 |
| `em` | 父元素字体（font-size 时）/ 自身字体（其他属性时） | 组件内相对大小 |
| `rem` | 根元素（html）字体，默认 16px | 响应式布局（改根字体就全局缩放） |
| `vw/vh` | 视口宽度/高度的 1% | 全屏布局、响应式 |
| `%` | 父元素对应属性（width 参照父 width，padding 也参照父 width） | 流式布局 |

🎯 **Interview Triggers:**
- em 和 rem 的区别是什么？（COMPARISON）
- 为什么移动端响应式推荐用 rem？（SCENARIO）
- 1vw 等于多少像素？（CALCULATION）

🧠 **Question Type:** comparison · scenario · calculation

🔥 **Follow-up Paths:**
- em → 相对父元素字体 → 嵌套时累乘导致难以预测
- rem → 只相对根元素 → 统一缩放，JS 动态设置根字体实现响应式
- 1vw = 视口宽度的 1% → 375px 宽度设备上 1vw = 3.75px

🛠 **Engineering Hooks:**
- 移动端适配：Tailwind CSS 用 rem 单位，配合根字体动态调整实现全局缩放
- `clamp(min, val, max)` 流体排版：`font-size: clamp(16px, 4vw, 24px)` 无需媒体查询
- 容器查询（@container，现代浏览器）是比 vw/vh 更好的组件级响应式方案

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| 标准盒模型 vs IE 盒模型？ | 标准：width 只含 content；IE（border-box）：width 含 content+padding+border |
| BFC 是什么，怎么触发？ | 独立渲染容器，触发：overflow 非 visible、float、absolute/fixed、flex/grid/inline-block |
| 清除浮动有哪些方法？ | ①clear:both 空标签 ②父元素 overflow:hidden ③::after 伪元素（推荐） |
| 选择器优先级？ | !important > 内联(1000) > ID(100) > class/属性/伪类(10) > 标签/伪元素(1) |
| 重排和重绘的区别？ | 重排：影响布局（重新计算位置/尺寸），代价高；重绘：只影响外观，跳过布局；transform 直接合成 |
| Flex justify-content 和 align-items 区别？ | justify 控制主轴对齐；align 控制交叉轴对齐 |
| em 和 rem 的区别？ | em 相对父元素字体大小；rem 相对根元素（html），更适合响应式 |
| display:none vs visibility:hidden？ | none 从渲染树消失占位消失触发重排；hidden 保留空间只触发重绘；hidden 的子元素可设 visible 显示 |
| position absolute 的定位基准？ | 最近的 position 非 static 的祖先元素，没有则是 body |
| 如何实现垂直居中？ | ①flex + justify-content/align-items:center ②position:absolute + transform:translate(-50%,-50%) |
