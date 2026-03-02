# Vue

---

## 速览

- Vue = MVVM 框架，Model 驱动 View，View 操作通过 ViewModel 双向同步。
- v-show vs v-if：show 切换 CSS display（保留 DOM），if 真正销毁/重建 DOM。
- 双向绑定：Vue2 用 Object.defineProperty（无法监听新增属性/数组索引），Vue3 改用 Proxy（全量拦截）。
- computed（有缓存，依赖不变不重算）vs watch（无缓存，监听变化执行副作用）。
- 生命周期 10 阶段：beforeCreate → created → beforeMount → mounted → beforeUpdate → updated → beforeDestroy → destroyed（+ activated/deactivated）。
- 组件通信 5 方式：props/emit、provide/inject、EventBus、$attrs/$listeners、Vuex。
- Vue Router：hash 模式（#，兼容性好）vs history 模式（pushState，需服务端配合）。
- Vuex = state + getters + mutations（同步）+ actions（异步）+ modules。
- Vue3 vs Vue2：Proxy 响应式、Composition API、树摇、多根节点、setup 代替 beforeCreate/created。

---

## MVVM 架构

> **一句话理解：** Model 是数据，View 是界面，ViewModel 是中间桥梁——数据变化自动更新视图，视图操作自动同步数据。

**核心结论（可背）：**
```
Model（数据层）
    ↕  双向绑定
ViewModel（Vue 实例）
  - 数据观测（Observer）
  - 模板编译（Compiler）
  - 虚拟 DOM Diff
    ↕  DOM 操作
View（视图层）
```

| 架构 | 特点 | 问题 |
|---|---|---|
| MVC | Controller 手动更新 View | Controller 臃肿，View/Model 耦合 |
| MVVM | ViewModel 自动双向绑定 | 引入框架开销，调试困难 |

🎯 **Interview Triggers:**
- MVVM 和 MVC 的区别是什么？（COMPARISON）
- Vue 的双向绑定是怎么实现的？（MECHANISM）
- 为什么说 Vue 是 MVVM 框架？（CLASSIFICATION）

🧠 **Question Type:** comparison · mechanism · classification

🔥 **Follow-up Paths:**
- MVC → Controller 手动更新 View → 代码量大且耦合
- MVVM → ViewModel 观测数据 → 自动触发 View 更新
- Vue 的 MVVM → Observer（数据）+ Compiler（模板）+ Watcher（连接）

🛠 **Engineering Hooks:**
- MVVM 降低了 DOM 操作复杂度，但深度嵌套的响应式数据有性能开销
- Vue DevTools 利用 ViewModel 层可以实现状态时间旅行调试
- 大型项目中 Pinia/Vuex 是 Model 层的延伸，将数据管理与视图进一步解耦

---

## v-show vs v-if

> **一句话理解：** v-if 是真正的条件渲染（DOM 增删），v-show 只切换 CSS（保留 DOM）。

**核心结论（可背）：**
| 维度 | `v-if` | `v-show` |
|---|---|---|
| 实现方式 | DOM 节点真实创建/销毁 | 切换 `display: none` |
| 初始开销 | 低（false 时不渲染） | 高（无论条件都先渲染） |
| 切换开销 | 高（每次都销毁/重建） | 低（只改 CSS 属性） |
| 适用场景 | 条件很少改变 | 频繁切换显示/隐藏 |

**v-if + v-for 不建议同用（Vue2）：**
```
v-for 优先级高于 v-if（Vue2）
→ 每个循环项都需要执行 v-if 判断，性能浪费
→ 正确做法：先用 computed 过滤数组，再用 v-for 渲染
```

🎯 **Interview Triggers:**
- v-if 和 v-show 的区别，各自适合什么场景？（COMPARISON）
- v-if 和 v-for 为什么不建议同时使用？（PRINCIPLE）
- v-show 能用于组件吗？和元素有区别吗？（DETAIL）

🧠 **Question Type:** comparison · design principle · detail

🔥 **Follow-up Paths:**
- v-if → DOM 销毁/重建 → 组件生命周期重置 → 适合一次性条件
- v-for + v-if → 每项都判断 → 先 computed 过滤 → 再 v-for 渲染
- v-show 对组件 → 组件保持活跃（生命周期不重置）→ keep-alive 效果

🛠 **Engineering Hooks:**
- 权限控制（鉴权后才显示的菜单）用 v-if，避免无权限用户通过 CSS 看到 DOM
- 频繁切换的 Tab 面板用 v-show（或 keep-alive），避免每次重建子组件
- Vue3 中 v-if 优先级高于 v-for（与 Vue2 相反），同用时行为不同，需注意

---

## 双向数据绑定

> **一句话理解：** Vue2 通过 Object.defineProperty 劫持属性的 getter/setter；Vue3 用 Proxy 代理整个对象，能监听新增/删除/数组索引变化。

**核心结论（可背）：**
```javascript
// Vue2：Object.defineProperty（逐属性劫持）
Object.defineProperty(obj, 'name', {
  get() { /* 依赖收集（dep.depend()） */ return val; },
  set(newVal) { val = newVal; /* 通知更新（dep.notify()） */ }
})
// 缺点：无法检测属性新增/删除；无法监听数组索引变化

// Vue3：Proxy（代理整个对象）
const proxy = new Proxy(obj, {
  get(target, key) { track(target, key); return target[key]; },
  set(target, key, val) { target[key] = val; trigger(target, key); return true; },
  deleteProperty(target, key) { delete target[key]; trigger(target, key); return true; }
})
// 优点：自动深度响应，监听新增/删除属性，监听数组所有操作
```

**Vue2 局限性：**
```
❌ this.obj.newProp = 'x'    // 不响应，需用 Vue.set(obj, 'newProp', 'x')
❌ this.arr[0] = 'x'        // 不响应，需用 Vue.set(arr, 0, 'x') 或 splice
❌ delete this.obj.prop     // 不响应，需用 Vue.delete(obj, 'prop')
```

🎯 **Interview Triggers:**
- Vue2 的响应式原理是什么，有什么局限？（MECHANISM + LIMITATION）
- Vue3 为什么用 Proxy 替代 defineProperty？（EVOLUTION）
- 数组变化在 Vue2 中为什么无法被监测到？（FAILURE）

🧠 **Question Type:** mechanism · evolution · failure analysis

🔥 **Follow-up Paths:**
- defineProperty → 逐属性劫持 → 初始化时遍历递归 → 新增属性无法监测
- Proxy → 代理整个对象 → 拦截所有操作（包括增删）→ 懒代理（访问时才代理）
- 数组监测 → Vue2 重写 7 个方法（push/pop/shift/unshift/splice/sort/reverse）

🛠 **Engineering Hooks:**
- Vue2 中修改数组用 `this.$set` 或数组变异方法（splice），不用下标直接赋值
- Vue3 中可以直接 `arr[0] = 'x'` 触发响应（Proxy 能监听到）
- 避免在 Vue3 中解构响应式对象（解构后失去响应性），用 `toRefs()` 代替

---

## computed vs watch

> **一句话理解：** computed 是有缓存的派生数据（依赖不变就不重算），watch 是监听变化执行副作用（无缓存，每次变化都执行）。

**核心结论（可背）：**
| 维度 | `computed` | `watch` |
|---|---|---|
| 缓存 | ✅ 有缓存，依赖不变不重新计算 | ❌ 无缓存，每次变化都执行 |
| 返回值 | 有返回值（用于模板渲染） | 无返回值（执行副作用） |
| 适用场景 | 从已有数据派生新数据 | 数据变化时请求接口、触发动画 |
| 异步支持 | ❌ 不支持异步 | ✅ 支持异步 |

```javascript
// computed：计算全名（有缓存）
computed: {
  fullName() { return this.first + ' ' + this.last; }
}

// watch：监听 userId 变化后请求数据
watch: {
  userId: {
    handler(newVal) { this.fetchUser(newVal); },
    immediate: true  // 立即执行一次
  }
}
```

🎯 **Interview Triggers:**
- computed 的缓存机制是如何实现的？（MECHANISM）
- 什么时候用 computed，什么时候用 watch？（SCENARIO）
- watch 的 deep 和 immediate 选项的作用？（DETAIL）

🧠 **Question Type:** mechanism · scenario selection · detail

🔥 **Follow-up Paths:**
- computed 缓存 → 依赖的响应式数据不变 → 不重算 → 基于 Watcher 脏值标记
- computed vs watch → 有返回值用 computed；需副作用/异步用 watch
- deep:true → 深度监听对象内部变化；immediate:true → 初始化时立即执行一次

🛠 **Engineering Hooks:**
- 模板中复杂计算必须用 computed（缓存），不要在模板中写方法调用（每次渲染都执行）
- watch 用于跨组件响应（如路由参数变化触发数据刷新）
- Vue3 中 `watchEffect` = 自动收集依赖的 watch（不需要显式指定监听属性）

---

## 生命周期

> **一句话理解：** Vue 组件从创建到销毁经历 10 个钩子，核心是 created（数据就绪）和 mounted（DOM 就绪）。

**核心结论（可背）：**
| 钩子 | 适合做的事 |
|---|---|
| `created` | 发起数据请求（data 已可用，DOM 未挂载） |
| `mounted` | 操作 DOM、初始化第三方库（DOM 已挂载） |
| `beforeDestroy` | 清除定时器、取消订阅、解绑事件 |

**keep-alive 独有钩子：**
```
activated   → 组件被激活时（从缓存中恢复）
deactivated → 组件被停用时（隐藏到缓存）
```

🎯 **Interview Triggers:**
- created 和 mounted 的区别，数据请求放在哪个里？（SCENARIO）
- 父子组件的生命周期执行顺序？（ORDER）
- keep-alive 的 activated 和 mounted 的区别？（DETAIL）

🧠 **Question Type:** scenario · execution order · detail

🔥 **Follow-up Paths:**
- created → data 初始化完，DOM 未挂载 → 可发请求（SSR 也能用）
- 父子生命周期 → 父 beforeMount → 子 mounted → 父 mounted（子先完成挂载）
- activated → keep-alive 缓存组件重新显示 → 不触发 mounted → 适合刷新数据

🛠 **Engineering Hooks:**
- SSR（服务端渲染）中数据请求必须放 created（mounted 在服务端不执行）
- 第三方图表库（ECharts/D3）初始化放 mounted，确保 DOM 已存在
- 组件销毁必须在 beforeDestroy 清除：定时器（clearInterval）、WebSocket 连接、事件监听

---

## 组件通信

> **一句话理解：** 父子用 props/emit，跨层级用 provide/inject，兄弟用 EventBus，全局状态用 Vuex。

**核心结论（可背）：**
| 场景 | 方式 | 说明 |
|---|---|---|
| 父 → 子 | `props` | 父传值，子只读 |
| 子 → 父 | `$emit` | 子触发事件，父监听 |
| 跨层级 | `provide / inject` | 祖先提供，后代注入（非响应式） |
| 兄弟组件 | `EventBus` | 全局事件总线（小型项目） |
| 全局状态 | `Vuex / Pinia` | 统一状态管理（中大型项目） |

🎯 **Interview Triggers:**
- Vue 组件通信有哪些方式？（OVERVIEW）
- provide/inject 为什么说是非响应式的，如何让它响应式？（DETAIL）
- EventBus 有什么缺点，大型项目为什么不推荐？（TRADEOFF）

🧠 **Question Type:** overview · detail · tradeoff

🔥 **Follow-up Paths:**
- provide/inject 非响应式 → 传入 ref 或 reactive 对象则有响应性
- EventBus 缺点 → 事件满天飞 → 难以追踪来源 → 内存泄漏（未取消监听）
- Vuex/Pinia → 集中管理 → 可追溯 → devtools 支持时间旅行

🛠 **Engineering Hooks:**
- Vue3 推荐用 Pinia 替代 Vuex（更简洁，TS 友好，无 mutations）
- `v-model` 是 `:value + @input` 的语法糖，本质是 props + emit 的封装
- 大型应用组件通信设计原则：尽量向上提升状态（状态提升），减少兄弟直接通信

---

## Vue Router

> **一句话理解：** hash 模式用 `#` 分割路由（兼容性好，不需要服务端），history 模式用 pushState（URL 干净，需服务端配合处理 404）。

**核心结论（可背）：**
| 维度 | Hash 模式（`#`） | History 模式 |
|---|---|---|
| URL 样式 | `example.com/#/user/1` | `example.com/user/1` |
| 原理 | `window.location.hash` + `hashchange` 事件 | `history.pushState/replaceState` + `popstate` 事件 |
| 服务端配合 | ❌ 不需要（`#` 后不发送到服务器） | ✅ 需要（刷新时服务器需返回 index.html） |
| SEO | 差（`#` 后内容搜索引擎不识别） | 好（标准 URL） |

🎯 **Interview Triggers:**
- history 模式刷新后 404 如何解决？（FAILURE）
- hash 模式的 # 为什么不会发送到服务器？（MECHANISM）
- Vue Router 的导航守卫有哪些，执行顺序？（DETAIL）

🧠 **Question Type:** failure · mechanism · guard execution order

🔥 **Follow-up Paths:**
- history 刷新 404 → 服务端 nginx `try_files $uri /index.html` → 前端路由接管
- hash → # 后的内容是 fragment identifier → HTTP 请求不包含 fragment
- 导航守卫顺序 → beforeEach → 组件 beforeRouteLeave → beforeEach → beforeRouteEnter → afterEach

🛠 **Engineering Hooks:**
- Nginx 配置 `try_files $uri $uri/ /index.html` 解决 history 模式刷新 404
- 路由懒加载：`component: () => import('./views/Home.vue')` 减少首屏 bundle 大小
- `beforeEach` 守卫用于全局权限鉴定（检查 token/登录状态），未登录跳转 login 页

---

## Vue3 vs Vue2

> **一句话理解：** Vue3 用 Proxy 替代 defineProperty，用 Composition API 替代 Options API，更好支持 TypeScript 和树摇。

**核心结论（可背）：**
| 特性 | Vue2 | Vue3 |
|---|---|---|
| 响应式原理 | `Object.defineProperty`（无法监听新增属性/数组） | `Proxy`（全量拦截，监听新增/删除/数组） |
| 组件 API | Options API（data/methods/computed 分组） | Composition API（按功能逻辑组织） |
| TypeScript | 支持有限 | 原生 TS 重写，完全支持 |
| 模板根节点 | 只能有一个根节点 | 支持多根节点（Fragment） |
| 生命周期 | `beforeCreate / created` | 被 `setup()` 替代 |
| 打包体积 | 全量引入 | 支持 Tree-Shaking |

**Composition API vs Options API：**
```javascript
// Composition API（Vue3 风格）
import { ref, computed } from 'vue';
export default {
  setup() {
    const count = ref(0);
    const double = computed(() => count.value * 2);
    const increment = () => count.value++;
    return { count, double, increment };
  }
}
```

🎯 **Interview Triggers:**
- Composition API 相比 Options API 的优势是什么？（COMPARISON）
- Vue3 为什么性能优于 Vue2？（PERFORMANCE）
- ref 和 reactive 的区别？（DETAIL）

🧠 **Question Type:** comparison · performance · detail

🔥 **Follow-up Paths:**
- Composition API → 按逻辑聚合 → 复用通过自定义 Composable（vs Mixin 的命名冲突）
- 性能优化 → Proxy 懒代理 + 静态节点提升 + Patch Flag + Tree-Shaking
- ref → 包装原始值（.value 访问）；reactive → 代理对象（直接访问）

🛠 **Engineering Hooks:**
- Vue3 组合式函数（Composable）是 Mixin 的替代品（无命名冲突，来源明确）
- `<script setup>` 语法糖让 Composition API 更简洁（无需 return 导出）
- Vue3 + TS 项目中用 `defineProps<{ title: string }>()` 实现 props 类型检查

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| MVVM 和 MVC 的区别？ | MVC 需手动更新 View；MVVM 通过 ViewModel 双向自动绑定，消除了 Controller 臃肿 |
| v-show vs v-if？ | v-if 销毁/重建 DOM（切换成本高）；v-show 切换 CSS（初始成本高），频繁切换用 v-show |
| Vue2 为什么监听不到数组索引？ | defineProperty 只能劫持已有属性，无法监听赋值给新索引的操作；Vue 重写了 push/pop 等 7 个方法 |
| computed 和 watch 的区别？ | computed 有缓存，用于派生数据；watch 无缓存，用于副作用（如请求、动画） |
| 父子组件通信方式？ | 父→子：props；子→父：$emit；跨层：provide/inject；全局：Vuex |
| hash 模式 vs history 模式？ | hash 不需服务端配合但 SEO 差；history URL 干净需服务端配合（刷新需 nginx 配置） |
| Vue3 为什么用 Proxy？ | defineProperty 无法监听属性新增/删除/数组索引，Proxy 全量拦截且支持懒代理 |
| Composition API 的优势？ | 按逻辑功能聚合代码（而不是 data/methods 分散），便于复用和 TS 类型推断 |
| Diff 算法优化？ | 只比同层（O(n)）、标签不同直接删、同层用 key 标识复用 |
| Vuex mutation 为什么必须同步？ | 便于 devtools 追踪每次状态快照，异步操作需放在 action 中 |
