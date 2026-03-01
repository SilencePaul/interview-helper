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

margin 负值：
  margin-top/left 负值 → 元素向上/左移动
  margin-right 负值 → 右侧元素左移（自身不动）
  margin-bottom 负值 → 下方元素上移（自身不动）
```

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

**常见优先级计算：**
```css
p span .warning { }         /* 1 + 1 + 10 = 12 */
#footer .note p { }         /* 100 + 10 + 1 = 111 */
a:hover { }                 /* 1 + 10 = 11 */
```

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

```javascript
// ❌ 差 - 多次读写 DOM（每次读强制刷新渲染队列）
const h = element.offsetHeight;
element.style.height = h + 10 + 'px';
// 再次读取时浏览器必须重排...

// ✅ 好 - 批量修改
element.style.cssText = 'width:100px; height:100px; top:50px';
// 或用 DocumentFragment 批量修改 DOM
```

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

---

## Flex 布局

> **一句话理解：** Flex 是一维布局（主轴+交叉轴），通过 justify-content 控制主轴对齐，align-items 控制交叉轴对齐。

**核心结论（可背）：**
```css
/* 容器属性 */
display: flex;
flex-direction: row | column | row-reverse | column-reverse;  /* 主轴方向 */
justify-content: flex-start | flex-end | center | space-between | space-around;  /* 主轴对齐 */
align-items: flex-start | flex-end | center | stretch | baseline;  /* 交叉轴对齐 */
flex-wrap: nowrap | wrap;  /* 是否换行 */
gap: 10px;  /* 子项间距 */

/* 子项属性 */
flex: 1;        /* flex-grow:1 flex-shrink:1 flex-basis:0（最常用，等分空间） */
flex: auto;     /* flex-grow:1 flex-shrink:1 flex-basis:auto */
flex: none;     /* flex-grow:0 flex-shrink:0 flex-basis:auto（不伸缩） */
align-self: center;  /* 单个子项的交叉轴对齐 */
```

**居中方案（最常用）：**
```css
/* Flex 居中（推荐） */
.parent { display: flex; justify-content: center; align-items: center; }

/* transform 居中 */
.parent { position: relative; }
.child { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }

/* margin auto 水平居中 */
.block { margin: 0 auto; }
```

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

```css
/* rem 响应式：根据屏幕宽度动态调整 html 字体大小 */
html { font-size: calc(100vw / 375 * 16); }  /* 以 375px 设计稿为基准 */
```

---

## CSS 隐藏元素

> **一句话理解：** display:none 从渲染树消失（触发重排）；visibility:hidden 保留空间（触发重绘）；opacity:0 保留空间且可交互。

**核心结论（可背）：**
| 方式 | 占空间 | 响应事件 | 触发 | 子元素可显示 |
|---|---|---|---|---|
| `display: none` | ❌ | ❌ | 重排 | ❌（非继承，无法覆盖） |
| `visibility: hidden` | ✅ | ❌ | 重绘 | ✅（设 visible 可显示） |
| `opacity: 0` | ✅ | ✅ | 合成 | 不可单独设 |
| `position: absolute; out of screen` | ❌（脱流） | ❌ | 重排 | — |

---

## 圣杯布局 & 双飞翼布局

> **一句话理解：** 都实现"中间自适应，两侧固定"的三栏布局，中间列在 HTML 中最先渲染。

**核心结论（可背）：**
```
圣杯布局：三列都 float:left，中间 width:100%，利用 padding + relative + margin 负值定位两侧
双飞翼布局：中间列套一层 wrapper，width:100%，内层用 margin 留出两侧空间，margin 负值定位两侧

区别：
  圣杯：使用 relative 定位，HTML 结构：wrapper 包裹三列
  双飞翼：使用 margin 留位，HTML 结构：中间列单独 wrapper，两侧在外
  双飞翼更简单，不需要 relative 定位
```

---

## CSS 继承

> **一句话理解：** 字体/文本/颜色类属性默认继承，盒模型/定位/背景类属性默认不继承。

**核心结论（可背）：**
```
可继承属性（常用）：
  字体：font-family、font-size、font-weight、font-style
  文本：color、text-align、line-height、letter-spacing、text-indent
  可见性：visibility
  列表：list-style
  光标：cursor

不可继承属性（常用）：
  盒模型：width、height、margin、padding、border
  背景：background
  定位：position、top/left/right/bottom、z-index、float
  显示：display

line-height 继承特殊规则：
  父 line-height 写具体数值（30px）→ 子继承 30px
  父 line-height 写比例（1.5）→ 子继承比例（各自 fontSize × 1.5）
  父 line-height 写百分比（200%）→ 子继承父 fontSize×200% 的计算结果（不是比例）
```

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
| 如何实现垂直居中？ | ①flex + justify-content/align-items:center ②position:absolute + transform:translate(-50%,-50%) ③line-height=高度 |
