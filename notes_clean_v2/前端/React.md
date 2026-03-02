# React

---

## 速览

- React = 声明式 UI 库（不是框架），单向数据流，组件化。
- JSX = JS 中写 HTML 语法糖，最终编译为 `React.createElement()` 调用。
- state vs props：state 是组件内部状态，props 是父组件传入的只读数据。
- setState 默认异步批量处理（React18 全面自动批处理），flushSync 可强制同步。
- 生命周期三阶段：挂载 → 更新 → 卸载；React16 新增 getDerivedStateFromProps / getSnapshotBeforeUpdate。
- 函数组件 + Hooks 是现代 React 主流（useState/useEffect/useMemo/useCallback/useRef）。
- 性能优化：React.memo（组件缓存）、useMemo（值缓存）、useCallback（函数缓存）、React.lazy（懒加载）。
- Fiber 架构：可中断的异步渲染，解决大型树更新时主线程被阻塞的问题。
- React18：自动批处理 setState、Concurrent 并发渲染、Suspense、Transition。

---

## JSX

> **一句话理解：** JSX 是 JavaScript 的语法扩展，让你可以在 JS 中写类 HTML 结构，Babel 会把它编译成 `React.createElement()` 调用。

**核心结论（可背）：**
```jsx
// JSX 语法
const element = <h1 className="title">Hello {name}</h1>;

// 编译结果
const element = React.createElement(
  'h1',
  { className: 'title' },
  'Hello ', name
);
```

**JSX 注意事项：**
```
① 根元素只能有一个（或用 <React.Fragment> / <> 包裹）
② 类名用 className（class 是 JS 保留字）
③ 事件名驼峰：onClick/onChange/onSubmit
④ 表达式用 {}，不能写语句（if/for），用三元表达式和 map
⑤ 列表渲染需要 key 属性（不要用 index 作 key）
```

🎯 **Interview Triggers:**
- JSX 的本质是什么，最终会变成什么？（MECHANISM）
- 为什么 JSX 用 className 而不是 class？（DETAIL）
- React17 之前为什么必须 `import React from 'react'`？（HISTORY）

🧠 **Question Type:** mechanism · detail · historical context

🔥 **Follow-up Paths:**
- JSX → Babel 编译 → React.createElement → Virtual DOM 节点
- className → class 是 JS 保留字 → JSX 是 JS 的超集，不能用保留字
- React17 → 新的 JSX 转换 → 无需显式 import React → 自动引入

🛠 **Engineering Hooks:**
- JSX 的条件渲染陷阱：`{count && <Comp />}` 当 count=0 时渲染 "0"，用三元或 `!!count` 避免
- React.Fragment (`<>`) 不生成额外 DOM 节点，用于返回多根元素
- JSX 注释需写成 `{/* 注释 */}` 而非 `<!-- -->`

---

## state vs props & setState

> **一句话理解：** props 是父传的只读数据，state 是组件自己管理的可变数据；setState 默认批处理（异步），React18 全面自动批处理。

**核心结论（可背）：**
| 维度 | `props` | `state` |
|---|---|---|
| 来源 | 父组件传入 | 组件内部初始化 |
| 可变性 | 只读（子不能直接修改） | 可变（通过 setState 修改） |
| 触发渲染 | ✅ props 改变触发重渲染 | ✅ setState 触发重渲染 |

**setState 批处理：**
```
React18 以前：
  合成事件/生命周期中 → 异步（批处理）
  setTimeout/原生事件中 → 同步（每次 setState 都触发 render）

React18：
  全面自动批处理（包括 setTimeout/Promise）
  需要同步：用 flushSync(() => setState(...))
```

🎯 **Interview Triggers:**
- setState 是同步还是异步，React18 前后的区别？（MECHANISM）
- 为什么 setState 要做批处理？（REASON）
- 如何在 setState 之后立即读到最新状态？（IMPLEMENTATION）

🧠 **Question Type:** mechanism · reason · implementation

🔥 **Follow-up Paths:**
- 批处理 → 合并多次更新为一次 render → 性能优化
- React18 前 setTimeout 中同步 → React18 全面批处理 → 用 flushSync 强制同步
- 立即读最新值 → `setState(prev => newVal)` 函数式更新，不依赖批处理结果

🛠 **Engineering Hooks:**
- 连续多次 setState 时，用函数式更新：`setState(prev => prev + 1)`（避免批处理导致读到旧值）
- React DevTools Profiler 可以看到每次 render 的触发原因（props/state 变化）
- 避免在 render 中直接修改 state（`this.state.x = 1`），必须用 setState

---

## React Hooks

> **一句话理解：** Hooks 让函数组件拥有状态和副作用能力，彻底替代了大多数类组件使用场景。

**核心结论（可背）：**
| Hook | 用途 |
|---|---|
| `useState` | 组件内部状态 |
| `useEffect` | 副作用（请求数据、订阅、操作 DOM） |
| `useContext` | 读取 Context 值 |
| `useRef` | 获取 DOM 引用 / 跨渲染保存值（不触发重渲染） |
| `useMemo` | 缓存计算结果（依赖不变不重算） |
| `useCallback` | 缓存函数引用（依赖不变不重建） |
| `useReducer` | 复杂状态逻辑（类似 Redux reducer） |

```jsx
// useEffect 依赖数组控制执行时机
useEffect(() => { /* 每次渲染后都执行 */ });
useEffect(() => { /* 只在挂载时执行 */ }, []);
useEffect(() => { /* dep 变化时执行 */ }, [dep]);
useEffect(() => {
  return () => { /* 清理函数 */ };
}, []);
```

**Hooks 使用规则：**
```
① 只在函数组件或自定义 Hook 中调用
② 不在循环/条件/嵌套函数中调用（必须保证调用顺序稳定）
  原因：Hooks 用链表按顺序存储，顺序改变会导致取值错位
```

🎯 **Interview Triggers:**
- Hooks 的两个使用规则是什么，为什么有这些限制？（RULE + REASON）
- useEffect 和 useLayoutEffect 的区别？（COMPARISON）
- useMemo 和 useCallback 的区别？（DISTINCTION）

🧠 **Question Type:** rule + reason · comparison · distinction

🔥 **Follow-up Paths:**
- Hooks 顺序 → 链表存储 → 条件/循环中调用 → 顺序变化 → 状态错位
- useEffect → 异步，浏览器绘制后执行；useLayoutEffect → 同步，绘制前执行（防闪烁）
- useMemo → 缓存值（计算结果）；useCallback → 缓存函数（函数引用不变）

🛠 **Engineering Hooks:**
- `useRef` 不仅用于 DOM，也用于跨渲染保存可变值（不触发重渲染）
- 自定义 Hook（`useXxx`）是封装复用逻辑的最佳方式（替代 Mixin 和 HOC）
- React Strict Mode 在开发环境故意执行两次 effect（验证清理函数正确性）

---

## React 性能优化

> **一句话理解：** 通过减少不必要的 render 次数（memo/shouldComponentUpdate）和减少渲染计算（useMemo/useCallback）来优化性能。

**核心结论（可背）：**
| 手段 | API | 说明 |
|---|---|---|
| 组件缓存 | `React.memo` | 浅比较 props，props 未变则跳过渲染 |
| 值缓存 | `useMemo` | 缓存计算结果，依赖不变不重算 |
| 函数缓存 | `useCallback` | 缓存函数引用，避免子组件不必要重渲染 |
| 懒加载 | `React.lazy + Suspense` | 按需加载组件，减小首屏 bundle |
| 类组件优化 | `PureComponent` | 自动实现浅比较 shouldComponentUpdate |

```jsx
// React.memo：props 不变时跳过子组件渲染
const Child = React.memo(function Child({ value }) {
  return <div>{value}</div>;
});

// useMemo + useCallback 组合使用
const result = useMemo(() => expensiveCalculation(a, b), [a, b]);
const handleClick = useCallback(() => doSomething(id), [id]);
```

**避免的反模式：**
```
❌ 内联对象/函数作为 props → 每次渲染都是新引用，memo 失效
  <Child style={{ margin: 0 }} />   // 坏的
  const styles = useMemo(() => ({ margin: 0 }), []);
  <Child style={styles} />          // 好的
```

🎯 **Interview Triggers:**
- React.memo 和 PureComponent 的区别？（COMPARISON）
- useMemo 和 useCallback 的使用场景和区别？（DISTINCTION）
- 内联函数/对象传给子组件会有什么问题？（FAILURE）

🧠 **Question Type:** comparison · distinction · failure case

🔥 **Follow-up Paths:**
- memo → 函数组件的 PureComponent → 浅比较 props → 未变则跳过
- useMemo → 缓存值；useCallback → 缓存函数 → 都是为了让引用稳定
- 内联 props → 每次 render 新引用 → memo 浅比较失效 → 必须用 useMemo/useCallback

🛠 **Engineering Hooks:**
- 不要过度优化：先 profiler 发现性能问题，再用 memo/useMemo（过度使用反而有开销）
- 列表组件必须给 key（不用 index），React DevTools 可高亮不必要的重渲染
- 大列表用虚拟滚动（react-virtual / react-window）而非 memo 优化

---

## Fiber 架构

> **一句话理解：** Fiber 把渲染工作拆分成小任务，让浏览器在空闲时执行，避免长时间阻塞主线程导致页面卡顿。

**核心结论（可背）：**
```
React15 问题：
  递归遍历整个 VDOM 树 → 同步不可中断
  大型组件树更新时占用主线程 → 用户交互无响应 → 掉帧卡顿

Fiber 解决方案（React16+）：
  将渲染工作切分为一个个 Fiber 节点（每个节点是一个小任务）
  利用时间切片在浏览器空闲时执行渲染
  高优先级任务（用户交互）可打断低优先级渲染任务

两个阶段：
  Render 阶段（可中断）：Diff 计算，构建新 Fiber 树，生成 effects 列表
  Commit 阶段（不可中断）：将 effects 应用到真实 DOM
```

🎯 **Interview Triggers:**
- Fiber 架构解决了什么问题？（PROBLEM）
- Fiber 的 Render 和 Commit 两个阶段有什么区别？（MECHANISM）
- 为什么 React16 废弃了 componentWillMount 等生命周期？（CONNECTION）

🧠 **Question Type:** problem-solution · mechanism · connection

🔥 **Follow-up Paths:**
- React15 同步递归 → 不可中断 → 长时间卡顿 → Fiber 可中断
- Render 可中断 → 废弃的生命周期可能被多次执行 → 产生副作用 bug
- Commit 不可中断 → 保证 DOM 更新的原子性

🛠 **Engineering Hooks:**
- Fiber 是 React18 并发特性（startTransition、Suspense）的基础
- 因 Render 阶段可重复执行，Strict Mode 下 React 故意执行两次渲染验证纯净性
- 避免在 render 函数中产生副作用（网络请求、全局状态修改），确保幂等性

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| React 和 Vue 的区别？ | React：函数式，单向数据流，JS-first（JSX），状态管理需自选；Vue：双向绑定，MVVM，模板语法 |
| setState 同步还是异步？ | React18：全部批处理（异步）；旧版：合成事件/生命周期中异步，setTimeout/原生事件中同步 |
| useEffect 和 useLayoutEffect 区别？ | useEffect：异步，浏览器绘制后执行；useLayoutEffect：同步，DOM 变更后绘制前执行 |
| useMemo 和 useCallback 区别？ | useMemo 缓存计算结果（值），useCallback 缓存函数引用（函数本身） |
| React.memo 和 PureComponent？ | memo 用于函数组件，PureComponent 用于类组件，都做浅比较避免不必要重渲染 |
| Fiber 是什么？ | 可中断的渲染架构，把同步递归拆成异步可打断的任务，高优先级任务可抢占低优先级 |
| 虚拟 DOM 一定更快吗？ | 不一定。少量 DOM 操作时直接操作更快；虚拟 DOM 优势在于批量更新和跨平台能力 |
| Redux 三大原则？ | 单一数据源、state 只读（只能 dispatch action）、纯函数 reducer |
| key 的作用？ | 帮助 Diff 算法识别列表元素，复用已有节点（只移动而非重建），不要用 index 作 key |
| Hooks 为什么不能在条件中调用？ | Hooks 按顺序存在链表中，条件调用导致顺序不稳定，会取错状态 |
