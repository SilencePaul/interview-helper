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

---

## state vs props

> **一句话理解：** props 是父传的只读数据，state 是组件自己管理的可变数据；两者变化都触发重新渲染。

**核心结论（可背）：**
| 维度 | `props` | `state` |
|---|---|---|
| 来源 | 父组件传入 | 组件内部初始化 |
| 可变性 | 只读（子不能直接修改） | 可变（通过 setState 修改） |
| 触发渲染 | ✅ props 改变触发重渲染 | ✅ setState 触发重渲染 |
| 适用场景 | 父子数据传递、配置组件 | 组件自身交互状态（展开/折叠、表单值） |

---

## 合成事件

> **一句话理解：** React 的合成事件是跨浏览器的事件包装层，统一事件 API，并通过事件委托（根节点）提升性能。

**核心结论（可背）：**
```
原生事件：各浏览器实现不同
合成事件（SyntheticEvent）：
  - React 在根节点统一监听所有事件（事件委托）
  - 对原生事件做跨浏览器封装，API 统一
  - 支持事件池（旧版 React，事件处理后对象被回收）
  - React17 起将事件绑定到 root 节点（而非 document），更利于微前端

阻止默认行为：e.preventDefault()  （不能用 return false）
阻止冒泡：e.stopPropagation()
```

---

## setState 同步 vs 异步

> **一句话理解：** setState 默认是异步批处理（积攒多次更新一次 render），React18 之前可通过 setTimeout/原生事件让其同步执行。

**核心结论（可背）：**
```
React18 以前：
  合成事件/生命周期中 → 异步（批处理，多次 setState 合并为一次 render）
  setTimeout/原生事件中 → 同步（每次 setState 都触发一次 render）

React18：
  全面自动批处理（包括 setTimeout/Promise），所有 setState 都批处理
  需要同步时：用 flushSync(() => setState(...))

为什么要批处理？
  避免每次 setState 都触发 render，多次状态变化合并成一次 DOM 更新，性能更好
```

```jsx
// React18：flushSync 强制同步
import { flushSync } from 'react-dom';

flushSync(() => {
  setState({ count: count + 1 });
});
// 此处 state 已更新
console.log(this.state.count); // 同步读到最新值
```

---

## 生命周期

> **一句话理解：** 挂载（constructor→render→componentDidMount）、更新（getDerivedStateFromProps→render→componentDidUpdate）、卸载（componentWillUnmount）三个阶段。

**核心结论（可背）：**
```
挂载阶段：
  constructor()                   → 初始化 state，绑定方法
  static getDerivedStateFromProps → props → state 的静态映射（纯函数）
  render()                        → 生成虚拟 DOM
  componentDidMount()             → DOM 已挂载，发请求/初始化第三方库

更新阶段：
  static getDerivedStateFromProps → 每次 render 前调用
  shouldComponentUpdate()         → 返回 false 跳过渲染（性能优化）
  render()
  getSnapshotBeforeUpdate()       → DOM 更新前获取快照（如滚动位置）
  componentDidUpdate()            → DOM 已更新

卸载阶段：
  componentWillUnmount()          → 清理定时器、取消请求、解绑事件
```

**React16 废弃的生命周期：**
```
❌ componentWillMount
❌ componentWillReceiveProps
❌ componentWillUpdate

废弃原因：Fiber 架构中 render 阶段可被中断并重启，这些方法可能被多次执行，
在其中做 setState/fetch/操作 DOM 等操作会导致问题。
替代：getDerivedStateFromProps / getSnapshotBeforeUpdate
```

---

## 函数组件 vs 类组件

> **一句话理解：** 函数组件 + Hooks 是现代 React 主流，类组件有 this 和生命周期，函数组件通过 Hooks 替代。

**核心结论（可背）：**
| 维度 | 函数组件 | 类组件 |
|---|---|---|
| 语法 | 函数，简洁 | ES6 class，复杂 |
| 状态 | `useState` Hook | `this.state` |
| 生命周期 | `useEffect` 模拟 | 完整生命周期方法 |
| this | 无 this | 有 this（需 bind） |
| 复用逻辑 | 自定义 Hook | HOC / renderProps |

---

## 受控组件 vs 非受控组件

> **一句话理解：** 受控组件的表单值由 React state 控制（通过 onChange 同步），非受控组件的值存在 DOM 中（通过 ref 读取）。

**核心结论（可背）：**
```jsx
// 受控组件：state 控制输入值
const [value, setValue] = useState('');
<input value={value} onChange={(e) => setValue(e.target.value)} />

// 非受控组件：通过 ref 读取 DOM 值
const inputRef = useRef();
<input ref={inputRef} />
// 读取时：inputRef.current.value
```

| 维度 | 受控组件 | 非受控组件 |
|---|---|---|
| 数据来源 | React state | DOM 节点 |
| 优点 | 验证/格式化方便，完全可控 | 代码简洁，适合简单场景 |
| 缺点 | 每个输入都要 onChange | 无法实时验证输入 |

---

## 组件通信

> **一句话理解：** 父子用 props/回调，跨层用 Context，全局状态用 Redux。

**核心结论（可背）：**
| 场景 | 方式 |
|---|---|
| 父 → 子 | props 传值 |
| 子 → 父 | props 传回调函数，子调用 `props.callback(data)` |
| 兄弟组件 | 提升状态到共同父组件 |
| 跨层级 | `React.createContext` + `Provider/Consumer` 或 `useContext` |
| 全局状态 | Redux / Redux Toolkit / Zustand |

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
| `useLayoutEffect` | 同步副作用（在 DOM 变更后、浏览器绘制前执行） |

```jsx
// useEffect 依赖数组控制执行时机
useEffect(() => { /* 每次渲染后都执行 */ });
useEffect(() => { /* 只在挂载时执行（类似 componentDidMount） */ }, []);
useEffect(() => { /* dep 变化时执行 */ }, [dep]);
useEffect(() => {
  return () => { /* 清理函数（类似 componentWillUnmount） */ };
}, []);
```

**useEffect vs useLayoutEffect：**
```
useEffect：异步执行，在浏览器绘制之后 → 不阻塞渲染，推荐首选
useLayoutEffect：同步执行，在 DOM 更新后、浏览器绘制前 → 避免闪烁，但可能延迟渲染
```

**Hooks 使用规则：**
```
① 只在函数组件或自定义 Hook 中调用
② 不在循环/条件/嵌套函数中调用（必须保证调用顺序稳定）
  原因：Hooks 用链表按顺序存储，顺序改变会导致取值错位
```

---

## Redux

> **一句话理解：** Redux = 单一状态树 + 不可变更新 + 纯函数 Reducer，解决多组件复杂状态共享问题。

**核心结论（可背）：**
```
数据流：View → dispatch(action) → reducer(state, action) → 新 state → View 更新

三大原则：
  ① 单一数据源：整个应用只有一个 store
  ② state 只读：只能 dispatch action 来修改
  ③ 纯函数更新：reducer 必须是纯函数（相同输入输出相同，无副作用）
```

```javascript
// Redux Toolkit（官方推荐写法）
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { count: 0 },
  reducers: {
    increment(state) { state.count++; },  // Immer 让你写"可变"代码
    decrement(state) { state.count--; }
  }
});

const store = configureStore({ reducer: { counter: counterSlice.reducer } });
store.dispatch(counterSlice.actions.increment());
```

**Redux vs Vuex：**
```
Redux：dispatch(action) → reducer → 新 state（不可变更新）
Vuex：commit(mutation) → 直接修改 state（可变更新）
共同点：单向数据流、单一数据源、可预测变化
```

---

## React Router

> **一句话理解：** React Router 在 URL 变化时渲染匹配的组件，支持 hash 和 history 两种路由模式。

**核心结论（可背）：**
```
路由实现原理：
  hash 模式：监听 hashchange 事件，匹配 # 后的路径
  history 模式：使用 pushState/replaceState，监听 popstate 事件

常用组件/API：
  <BrowserRouter>  → history 模式路由容器
  <HashRouter>     → hash 模式路由容器
  <Route path="/" component={Home} />  → 路径匹配组件
  <Switch>         → 只渲染第一个匹配的 Route
  <Link to="/about">  → 路由链接（不刷新页面）
  <Redirect to="/" /> → 重定向
  useHistory()     → 编程式导航
  useParams()      → 获取动态路由参数
```

---

## 虚拟 DOM & Diff 算法

> **一句话理解：** 虚拟 DOM 是 JS 对象描述的 DOM 树，Diff 算法同层比较找差异，批量最小化更新真实 DOM。

**核心结论（可背）：**
```
虚拟 DOM 工作流程：
  ① JSX 编译为 React.createElement() 调用
  ② 生成 Virtual DOM 树（JS 对象）
  ③ 状态/props 变化 → 生成新的 VDOM 树
  ④ Diff 算法对比两棵树 → 生成 patch（变化集合）
  ⑤ 将 patch 应用到真实 DOM

Diff 三层优化：
  树层：只比同层，跨层的节点直接删除重建
  组件层：同类型组件继续 diff，不同类型直接替换
  元素层：同层用 key 标识，key 相同则复用节点（只移动），key 不同则重建
```

**虚拟 DOM 不一定更快：**
```
✅ 优势：大量 DOM 操作时合并批量更新，保证性能下限，跨平台能力
❌ 劣势：初次渲染多一层 JS 对象计算；少量 DOM 操作时直接操作更快
```

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
| 列表优化 | 稳定 `key` | 帮助 Diff 算法复用节点 |

```jsx
// React.memo：props 不变时跳过子组件渲染
const Child = React.memo(function Child({ value }) {
  return <div>{value}</div>;
});

// useMemo：依赖不变时跳过昂贵计算
const result = useMemo(() => expensiveCalculation(a, b), [a, b]);

// useCallback：依赖不变时返回同一函数引用（配合 memo 使用）
const handleClick = useCallback(() => doSomething(id), [id]);
```

**避免的反模式：**
```
❌ 内联对象/函数作为 props → 每次渲染都是新引用，memo 失效
  <Child style={{ margin: 0 }} />   // 坏的
  const styles = { margin: 0 };
  <Child style={styles} />          // 好的

❌ 频繁挂载/卸载大组件 → 用 CSS visibility/display 代替
```

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
  利用 requestIdleCallback（时间切片）在浏览器空闲时执行渲染
  高优先级任务（用户交互）可打断低优先级渲染任务

两个阶段：
  Render 阶段（可中断）：Diff 计算，构建新 Fiber 树，生成 effects 列表
  Commit 阶段（不可中断）：将 effects 应用到真实 DOM
```

---

## React18 新特性

> **一句话理解：** React18 引入 Concurrent 并发渲染，setState 全面自动批处理，Suspense 支持数据获取，Transition 区分紧急/非紧急更新。

**核心结论（可背）：**
| 特性 | 说明 |
|---|---|
| Concurrent 并发模式 | 渲染可中断，高优先级任务（用户交互）可打断低优先级渲染 |
| 自动批处理 | setTimeout/Promise 中的多次 setState 也自动批处理（旧版不行） |
| `startTransition` | 标记非紧急更新，让用户交互响应更流畅 |
| `Suspense` | 支持数据获取场景，`fallback` 在异步内容加载完成前显示 |
| `useId` | 服务端/客户端稳定唯一 ID（SSR 场景） |
| `createRoot` | 替代 `ReactDOM.render`，开启 Concurrent 特性的入口 |

```jsx
// React18 入口
const root = createRoot(document.getElementById('root'));
root.render(<App />);

// startTransition：标记非紧急更新
import { startTransition } from 'react';
startTransition(() => {
  setSearchResults(computeResults(query));  // 可被中断的低优先级更新
});

// Suspense 数据加载
<Suspense fallback={<Spinner />}>
  <AsyncComponent />
</Suspense>
```

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| React 和 Vue 的区别？ | React：函数式，单向数据流，JS-first（JSX），状态管理需自选；Vue：双向绑定，MVVM，模板语法，内置状态管理 |
| setState 同步还是异步？ | React18：全部批处理（异步）；旧版：合成事件/生命周期中异步，setTimeout/原生事件中同步 |
| 函数组件 vs 类组件？ | 函数组件用 Hooks 替代 state 和生命周期，更简洁，是现代 React 主流；类组件有 this 和完整生命周期 |
| useEffect 和 useLayoutEffect 区别？ | useEffect：异步，浏览器绘制后执行；useLayoutEffect：同步，DOM 变更后绘制前执行，避免闪烁 |
| useMemo 和 useCallback 区别？ | useMemo 缓存计算结果（值），useCallback 缓存函数引用（函数本身） |
| React.memo 和 PureComponent？ | memo 用于函数组件，PureComponent 用于类组件，都做浅比较避免不必要重渲染 |
| Fiber 是什么？ | 可中断的渲染架构，把同步递归拆成异步可打断的任务，高优先级任务可抢占低优先级 |
| 虚拟 DOM 一定更快吗？ | 不一定。少量 DOM 操作时直接操作更快；虚拟 DOM 优势在于批量更新和跨平台能力 |
| Redux 三大原则？ | 单一数据源、state 只读（只能 dispatch action）、纯函数 reducer |
| key 的作用？ | 帮助 Diff 算法识别列表元素，复用已有节点（只移动而非重建），不要用 index 作 key |
