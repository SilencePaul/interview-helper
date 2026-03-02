# JavaScript

---

## 速览

- JS 有 8 种数据类型：7 种原始类型（Number/String/Boolean/Null/Undefined/Symbol/BigInt）+ Object（引用类型）。
- 判断类型：typeof（原始类型）、instanceof（原型链）、Object.prototype.toString（最准确）、constructor。
- 原型链：每个对象有 `__proto__` 指向构造函数的 `prototype`，`prototype.constructor` 指回构造函数，链尾为 `null`。
- 继承最优解：寄生组合继承（ES5）/ class extends（ES6）。
- 闭包：函数 + 函数创建时所在词法环境，可访问外部函数变量，常用于数据私有化，注意内存泄漏。
- this 四种绑定规则：new > 显式(call/apply/bind) > 隐式(对象方法) > 默认(全局)；箭头函数无自己的 this。
- Promise 三种状态：pending → fulfilled / rejected（不可逆）。async/await 是 Promise + Generator 语法糖。
- 事件流三阶段：捕获（顶→目标）→ 目标 → 冒泡（目标→顶）；事件委托利用冒泡减少事件绑定。
- 垃圾回收：标记-清除（现代主流）；常见内存泄漏：全局变量、定时器未清除、闭包引用。
- ES6 核心：let/const、解构、箭头函数、Class、Promise、async/await、Map/Set、Proxy、模块化(import/export)。

---

## 数据类型与判断

> **一句话理解：** JS 有 8 种类型，原始类型存栈，引用类型存堆（栈存指针），typeof 能判断基础类型，Object.prototype.toString 最精确。

**核心结论（可背）：**
```
原始类型（7种，按值传递）：
  Number、String、Boolean、Null、Undefined、Symbol（ES6）、BigInt（ES10）

引用类型（按引用传递）：
  Object（含 Array、Function、Date、RegExp、Map、Set...）
```

**四种类型检测方式：**
| 方式 | 原理 | 局限 |
|---|---|---|
| `typeof` | 返回字符串，检测原始类型 | `null` 返回 `"object"`（历史 bug）；无法区分 Array/Object |
| `instanceof` | 检查原型链上是否存在构造函数的 `prototype` | 不能判断原始类型；跨 iframe 失效 |
| `constructor` | 对象的 `constructor` 属性指向构造函数 | null/undefined 无 constructor |
| `Object.prototype.toString.call(x)` | 返回 `[object Type]`，最准确 | 写法稍麻烦 |

```javascript
typeof null           // "object"（bug，null 是原始类型）
typeof undefined      // "undefined"
typeof function(){}   // "function"
typeof []             // "object"

Object.prototype.toString.call([])        // "[object Array]"
Object.prototype.toString.call(null)      // "[object Null]"
```

**null vs undefined：**
```
null：明确表示"空值/无对象"，是主动赋的值，typeof → "object"（历史 bug）
undefined：变量声明未赋值、函数无返回值、对象属性不存在，typeof → "undefined"
NaN：Not a Number，typeof → "number"；NaN !== NaN，用 Number.isNaN() 判断
```

🎯 **Interview Triggers:**
- typeof null 为什么返回 "object"？（HISTORY）
- 如何精确判断一个变量是 Array 类型？（IMPLEMENTATION）
- null 和 undefined 的区别是什么？（DISTINCTION）

🧠 **Question Type:** historical context · implementation · distinction

🔥 **Follow-up Paths:**
- typeof null → JS 早期 bug → 二进制 000 前缀被误判为对象
- 判断 Array → `Array.isArray()` / `instanceof` / `Object.prototype.toString`
- null vs undefined → 主动置空 vs 未赋值；`null == undefined` 为 true

🛠 **Engineering Hooks:**
- API 返回值用 `null` 表示"没有数据"，用 `undefined` 表示"未传参"（语义区分）
- `Array.isArray()` 优于 `instanceof`（跨 iframe 环境下 instanceof 失效）
- 类型守卫（TypeScript）在编译时消除运行时类型判断的性能开销

---

## 原型与原型链

> **一句话理解：** 每个对象有 `__proto__` 链接到父对象，构造函数有 `prototype` 对象，原型链就是 `__proto__` 一级级向上查找属性，直到 null。

**核心结论（可背）：**
```
三个核心概念：
  prototype：函数对象特有，是该构造函数创建的实例的原型
  __proto__：每个对象都有，指向自己的原型（即构造函数的 prototype）
  constructor：原型对象上的属性，指回构造函数自身

关系公式：
  实例.__proto__ === 构造函数.prototype
  构造函数.prototype.constructor === 构造函数
  Object.prototype.__proto__ === null（链尾）
```

```
原型链查找过程：
  obj.prop
    → obj 自身有？返回
    → obj.__proto__ 有？返回
    → obj.__proto__.__proto__ 有？返回
    → ... 直到 null → 返回 undefined
```

**instanceof 原理：**
```javascript
// instanceof 沿 __proto__ 链找 构造函数.prototype
function myInstanceof(obj, Constructor) {
  let proto = Object.getPrototypeOf(obj);
  while (proto) {
    if (proto === Constructor.prototype) return true;
    proto = Object.getPrototypeOf(proto);
  }
  return false;
}
```

🎯 **Interview Triggers:**
- 原型链是什么，属性查找如何沿链进行？（MECHANISM）
- prototype 和 __proto__ 的区别？（DISTINCTION）
- instanceof 的原理是什么，手写实现？（IMPLEMENTATION）

🧠 **Question Type:** mechanism · distinction · implementation

🔥 **Follow-up Paths:**
- 属性查找 → 自身 → __proto__ → ... → null → undefined
- prototype（函数有）vs __proto__（所有对象有）→ 前者是后者的来源
- instanceof → 沿 __proto__ 链寻找 Constructor.prototype → 找到返回 true

🛠 **Engineering Hooks:**
- 不直接修改 `__proto__`（性能差），用 `Object.create(proto)` 创建指定原型的对象
- `Object.getPrototypeOf(obj)` 是 `obj.__proto__` 的标准 API 写法
- 继承链过深（>5层）影响属性查找性能，保持继承层级扁平

---

## 继承（寄生组合继承）

> **一句话理解：** 最优解是寄生组合继承（ES5）或 class extends（ES6），前者通过 Object.create 继承原型而不调用父构造函数，完美解决两次调用问题。

**核心结论（可背）：**
```javascript
// ✅ 寄生组合继承（面试最重要）
function Parent(name) {
  this.name = name;
}
Parent.prototype.sayName = function() { console.log(this.name); };

function Child(name, age) {
  Parent.call(this, name);  // 继承属性
  this.age = age;
}
// 继承原型（不调用 Parent 构造函数）
Child.prototype = Object.create(Parent.prototype);
Child.prototype.constructor = Child;

// ES6 等价写法
class Child extends Parent {
  constructor(name, age) {
    super(name);
    this.age = age;
  }
}
```

🎯 **Interview Triggers:**
- 为什么寄生组合继承比组合继承更优？（COMPARISON）
- ES6 class extends 和 ES5 寄生组合继承的区别？（EVOLUTION）
- 原型链继承有什么问题？（FAILURE）

🧠 **Question Type:** comparison · evolution · failure analysis

🔥 **Follow-up Paths:**
- 组合继承 → 父构造函数调用两次（new + call）→ 寄生组合只 call 一次
- class extends → 语法糖 → 底层仍是原型链，但支持 static 继承
- 原型链继承 → 引用类型属性共享 → 一个实例修改影响所有实例

🛠 **Engineering Hooks:**
- 现代项目统一用 ES6 class 语法（可读性强，TS 完全支持）
- 组合继承踩坑：父类构造函数有副作用（如请求）时调用两次会造成问题
- Mixin 模式：`Object.assign(Target.prototype, Mixin)` 组合多个来源的方法

---

## 深拷贝与浅拷贝

> **一句话理解：** 浅拷贝只复制第一层（引用类型仍共享），深拷贝递归复制所有层（完全独立）。

**核心结论（可背）：**
| 方式 | 深/浅 | 局限 |
|---|---|---|
| `Object.assign({}, obj)` | 浅拷贝 | 只复制第一层 |
| `{...obj}` 展开运算符 | 浅拷贝 | 只复制第一层 |
| `JSON.parse(JSON.stringify(obj))` | 深拷贝 | 不支持：函数/Symbol/undefined/循环引用/Date变字符串 |
| 递归手写深拷贝 | 深拷贝 | 需处理循环引用（WeakMap 记录已拷贝对象） |
| `structuredClone(obj)` | 深拷贝 | 现代浏览器原生 API，不支持函数 |

```javascript
// 手写深拷贝（处理循环引用）
function deepClone(obj, map = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (map.has(obj)) return map.get(obj);  // 处理循环引用
  const clone = Array.isArray(obj) ? [] : {};
  map.set(obj, clone);
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key], map);
    }
  }
  return clone;
}
```

🎯 **Interview Triggers:**
- 深拷贝和浅拷贝的区别？（CONCEPT）
- JSON.stringify 深拷贝的局限性有哪些？（LIMITATION）
- 如何处理深拷贝中的循环引用？（IMPLEMENTATION）

🧠 **Question Type:** concept · limitation · implementation

🔥 **Follow-up Paths:**
- 浅拷贝 → 引用类型只复制指针 → 修改嵌套对象影响原始对象
- JSON 序列化 → 丢失 undefined/Symbol/函数 → Date 变字符串
- 循环引用 → WeakMap 记录已处理对象 → 遇到已处理的直接返回

🛠 **Engineering Hooks:**
- 现代项目优先用 `structuredClone()`（原生，支持大多数内置类型）
- Lodash `_.cloneDeep()` 是生产环境最常用的深拷贝方案（处理边界情况全面）
- Redux 中 state 必须是不可变的，用展开运算符浅拷贝（只修改必要层级）

---

## 闭包

> **一句话理解：** 闭包 = 函数 + 其创建时的词法环境，让内层函数可以访问并"记住"外层函数的变量，常用于数据私有化和函数工厂。

**核心结论（可背）：**
```
闭包产生条件：
  1. 函数嵌套
  2. 内层函数引用了外层函数的变量
  3. 内层函数在外层函数作用域之外被调用

闭包的应用：
  ① 数据私有化（模拟私有变量）
  ② 函数工厂（柯里化）
  ③ 防抖/节流
  ④ 模块化（IIFE 模式）

闭包的问题：
  外层函数执行完后，内层函数仍引用其变量 → 变量不被 GC 回收 → 内存泄漏
  解决：使用完后将闭包引用置为 null
```

```javascript
// 经典闭包：计数器（数据私有化）
function makeCounter() {
  let count = 0;  // 私有变量
  return {
    increment() { count++; },
    getCount()  { return count; }
  };
}

// 经典面试题：for 循环 + 闭包
for (var i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 0);  // 输出 3 3 3
}
// 修复：let 替换 var（块级作用域，每次循环独立 i）
for (let i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 0);  // 输出 0 1 2
}
```

🎯 **Interview Triggers:**
- 什么是闭包，闭包的应用场景有哪些？（CONCEPT）
- 闭包会导致内存泄漏吗，如何解决？（FAILURE）
- for 循环 + setTimeout 经典题的输出和原因？（CLASSIC）

🧠 **Question Type:** concept · failure analysis · classic interview question

🔥 **Follow-up Paths:**
- 闭包 → 词法环境保留 → 外层作用域变量不被 GC 回收
- 内存泄漏 → 闭包持有 DOM 引用 → 置 null 或用 WeakRef
- for+setTimeout → var 只有函数作用域 → 循环结束 i 为 3 → let 修复

🛠 **Engineering Hooks:**
- 防抖/节流实现依赖闭包保存 timer 变量（无副作用的最小状态封装）
- React useState 内部也是闭包（Hook 的状态在 Fiber 节点上，闭包捕获）
- 避免在循环中创建大量闭包（每次迭代都创建新的函数对象，内存开销大）

---

## this 指向

> **一句话理解：** this 不是定义时确定，而是调用时确定，四种绑定优先级：new > 显式(call/apply/bind) > 隐式(对象方法) > 默认(全局/undefined)。

**核心结论（可背）：**
| 绑定方式 | 规则 | this 指向 |
|---|---|---|
| **new 绑定** | `new Foo()` | 新创建的对象 |
| **显式绑定** | `call/apply/bind` | 第一个参数指定的对象 |
| **隐式绑定** | `obj.fn()` | 调用对象 obj |
| **默认绑定** | 普通函数调用 `fn()` | 全局对象（严格模式为 undefined） |
| **箭头函数** | 无自己的 this | 继承外层词法作用域的 this（定义时确定） |

```javascript
// 隐式丢失（面试常考）
const obj = { name: 'obj', fn: function() { console.log(this.name); } };
const fn = obj.fn;
fn();  // undefined（this 变成全局，丢失 obj）

// 箭头函数 this（继承定义时的外层 this）
const obj2 = {
  name: 'obj2',
  fn: function() {
    const arrow = () => console.log(this.name);  // this 继承 fn 的 this
    arrow();
  }
};
obj2.fn();  // "obj2"
```

🎯 **Interview Triggers:**
- 隐式丢失是什么情况，举例说明？（FAILURE）
- 箭头函数的 this 和普通函数有什么区别？（COMPARISON）
- call/apply/bind 能改变箭头函数的 this 吗？（EDGE-CASE）

🧠 **Question Type:** failure case · comparison · edge case

🔥 **Follow-up Paths:**
- 隐式丢失 → `const fn = obj.fn; fn()` → this 变为全局
- 箭头函数 → 无自己 this → 继承外层函数的 this → 定义时确定
- 箭头函数 + bind → this 不变 → call/apply/bind 对箭头函数无效

🛠 **Engineering Hooks:**
- React 类组件中事件处理函数需在构造器中 `.bind(this)` 或用箭头函数避免 this 丢失
- Vue options API 的 methods 中避免箭头函数（会导致 this 不指向 Vue 实例）
- 定时器回调中的 this 问题：用箭头函数或 `.bind(this)` 保持外层上下文

---

## Promise & async/await

> **一句话理解：** Promise 解决回调地狱，有 pending/fulfilled/rejected 三种不可逆状态；async/await 是 Promise + Generator 的语法糖，让异步代码看起来像同步。

**核心结论（可背）：**
```
Promise 状态机：
  pending → fulfilled（resolve 触发）
  pending → rejected（reject 触发 / 抛出异常）
  状态一旦改变不可逆

Promise 静态方法：
  Promise.all([p1, p2])      → 全部成功才成功，一个失败即失败
  Promise.allSettled([p1,p2]) → 全部结束（无论成败），返回每个结果状态
  Promise.race([p1, p2])     → 第一个状态改变的 Promise 的结果
  Promise.any([p1, p2])      → 第一个 fulfilled（全部 rejected 才 rejected）
```

```javascript
// async/await 基本用法
async function fetchData() {
  try {
    const res = await fetch('/api/data');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);
  }
}
```

🎯 **Interview Triggers:**
- Promise.all 和 Promise.allSettled 的区别？（COMPARISON）
- async/await 的原理是什么？（MECHANISM）
- await 后面接一个非 Promise 值会怎样？（EDGE-CASE）

🧠 **Question Type:** comparison · mechanism · edge case

🔥 **Follow-up Paths:**
- all vs allSettled → 一个失败 all 立即 reject；allSettled 等全部完成
- async/await → Generator + 自动执行器 → await 挂起函数，放入微任务
- await 非 Promise → 包装为 `Promise.resolve(value)` → 正常工作

🛠 **Engineering Hooks:**
- 并行请求用 `Promise.all([fetch1(), fetch2()])`，不要用多个 await 串行
- `Promise.allSettled` 适合"全部执行，各自处理结果"（如批量上传文件）
- async 函数返回的一定是 Promise，调用者需用 `.then()` 或 `await` 接收

---

## 事件流与事件委托

> **一句话理解：** 事件流三阶段：捕获（从顶到目标）→ 目标 → 冒泡（从目标到顶）；事件委托将子元素事件委托给父元素，利用冒泡减少监听器数量。

**核心结论（可背）：**
```
事件流三阶段：
  1. 捕获阶段：window → document → html → ... → 目标的父元素
  2. 目标阶段：事件在目标元素处理
  3. 冒泡阶段：目标父元素 → ... → document → window

阻止：
  event.stopPropagation()  → 阻止冒泡
  event.preventDefault()   → 阻止默认行为

e.target vs e.currentTarget：
  e.target：真正触发事件的元素（点击的元素）
  e.currentTarget：绑定事件处理程序的元素

不支持冒泡的事件：blur、focus、mouseenter、mouseleave、load
```

```javascript
// ✅ 事件委托（推荐）
document.querySelector('ul').addEventListener('click', function(e) {
  if (e.target.tagName === 'LI') {
    console.log(e.target.textContent);
  }
});
// 优点：减少事件监听器数量，动态添加的子元素自动继承事件
```

🎯 **Interview Triggers:**
- 事件委托的原理是什么，有什么优缺点？（MECHANISM）
- e.target 和 e.currentTarget 的区别？（DISTINCTION）
- 哪些事件不冒泡，如何解决？（EDGE-CASE）

🧠 **Question Type:** mechanism · distinction · edge case

🔥 **Follow-up Paths:**
- 事件委托 → 冒泡 → 父元素监听 → 通过 e.target 判断来源
- e.target（触发元素）vs e.currentTarget（绑定元素）→ 委托场景两者不同
- 不冒泡事件 → 用捕获阶段监听 → `addEventListener(type, fn, true)`

🛠 **Engineering Hooks:**
- 长列表（>100 项）必须用事件委托代替逐项绑定，性能差异显著
- Vue 的 `v-on` 和 React 的合成事件底层都用了事件委托机制
- 动态渲染列表（如虚拟滚动）天然适合事件委托（元素动态创建/销毁）

---

## 防抖与节流

> **一句话理解：** 防抖 = 操作停止后才执行（搜索联想）；节流 = 固定频率执行（滚动/resize）。

**核心结论（可背）：**
```
防抖（Debounce）：
  事件触发后等待 n 毫秒，如果期间再次触发则重新计时
  适用：搜索框输入、窗口 resize、表单提交防重复

节流（Throttle）：
  单位时间内只执行一次
  适用：scroll 事件、mousemove、游戏帧更新
```

```javascript
// 防抖
function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// 节流（时间戳版）
function throttle(fn, interval) {
  let last = 0;
  return function(...args) {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn.apply(this, args);
    }
  };
}
```

🎯 **Interview Triggers:**
- 防抖和节流的区别，各自适用什么场景？（COMPARISON）
- 手写防抖函数（要求支持立即执行参数）？（IMPLEMENTATION）
- React 中如何在函数组件里正确使用防抖？（FRAMEWORK）

🧠 **Question Type:** comparison · implementation · framework integration

🔥 **Follow-up Paths:**
- 防抖 → 最后一次触发后执行 → 搜索框不频繁请求
- 节流 → 固定频率执行 → 滚动事件每 100ms 最多一次
- React 防抖 → useCallback + useRef 保存 timer → 避免组件重渲染重置

🛠 **Engineering Hooks:**
- Lodash `_.debounce()` / `_.throttle()` 生产环境直接用（处理 leading/trailing 边界）
- 搜索框防抖时间 300-500ms 为用户体验甜点（响应快且不频繁请求）
- 防抖的"立即执行"变体：第一次触发立即执行，之后等停止再执行

---

## 垃圾回收（GC）

> **一句话理解：** JS 引擎自动管理内存，现代 V8 使用标记-清除（老生代）+ Scavenge 复制算法（新生代）+ 分代回收策略。

**核心结论（可背）：**
```
标记-清除（Mark-Sweep）——现代主流算法：
  1. 从根（root）出发，标记所有可达对象
  2. 清除未被标记的对象
  缺点：产生内存碎片

V8 分代回收：
  新生代（小/短生命，1~8M）：Scavenge 复制算法
  老生代（大/长生命）：标记-清除 + 标记-整理

常见内存泄漏场景：
  ① 意外的全局变量（忘写 var/let）
  ② 闭包持有大对象引用
  ③ 定时器（setInterval）未清除
  ④ 事件监听器未移除
  ⑤ 已移除的 DOM 节点被 JS 变量引用
```

🎯 **Interview Triggers:**
- JS 的垃圾回收机制是什么？（MECHANISM）
- 常见的内存泄漏场景有哪些，如何排查？（FAILURE）
- WeakMap/WeakRef 为什么能避免内存泄漏？（MECHANISM）

🧠 **Question Type:** mechanism · failure analysis · weak reference

🔥 **Follow-up Paths:**
- 标记清除 → 从 root 出发可达 → 不可达即垃圾 → 分代优化频率
- 内存泄漏排查 → Chrome DevTools Memory → Heap Snapshot 对比
- WeakMap/WeakRef → 弱引用不阻止 GC → DOM 被移除后可被回收

🛠 **Engineering Hooks:**
- SPA 中组件销毁时必须清除：定时器（`clearInterval`）、事件监听（`removeEventListener`）
- React useEffect 返回清理函数防内存泄漏（组件卸载时自动执行）
- Chrome Performance Monitor 实时监控内存增长趋势，定位泄漏位置

---

## ES6 核心特性

> **一句话理解：** ES6 是 JS 最重要的版本更新，let/const 解决变量作用域，Promise 解决回调地狱，class 提供更清晰的面向对象写法。

**核心结论（可背）：**

**let / const vs var：**
```
var：函数作用域，变量提升，可重复声明，可重新赋值
let：块级作用域，暂时性死区，不可重复声明，可重新赋值
const：块级作用域，暂时性死区，不可重复声明，不可重新赋值（引用类型属性可改）
```

**Map vs Object / Set vs Array：**
```
Map：键可以是任何类型；记忆插入顺序；直接有 .size 属性
Set：存储唯一值（无重复）；常用于数组去重：[...new Set([1,1,2,3])]
WeakMap / WeakSet：键只能是对象，弱引用（不阻止 GC），不可遍历
```

**Proxy：**
```javascript
// 拦截对象的读写操作
const proxy = new Proxy(target, {
  get(target, prop) { return Reflect.get(target, prop); },
  set(target, prop, value) { return Reflect.set(target, prop, value); }
});
// Vue3 用 Proxy 替代 Object.defineProperty 实现响应式
```

🎯 **Interview Triggers:**
- var/let/const 的区别，暂时性死区是什么？（COMPARISON）
- Map 和 Object 的区别，什么时候用 Map？（COMPARISON）
- Proxy 相比 Object.defineProperty 有什么优势？（COMPARISON）

🧠 **Question Type:** comparison · use case · comparative advantage

🔥 **Follow-up Paths:**
- TDZ → let/const 声明前访问 → ReferenceError → 和 var 提升不同
- Map → 键可为任意类型 → 频繁增删 → Object 键只能是 string/Symbol
- Proxy → 代理整个对象 → 监听新增/删除 → Vue3 响应式基础

🛠 **Engineering Hooks:**
- 用 Set 去重：`[...new Set(arr)]`（替代 filter + indexOf，更简洁）
- 用 Map 存 DOM → key 的 metadata（比 WeakMap 多了 .size 属性）
- `Object.freeze()` 配合 const 创建真正不可变对象（浅冻结）

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| JS 数据类型有哪些？ | 7 种原始类型（Number/String/Boolean/Null/Undefined/Symbol/BigInt）+ Object 引用类型 |
| typeof null 为什么是 "object"？ | JS 早期 bug，null 二进制以 000 开头被误判为对象，已沿用至今 |
| 原型链是什么？ | 对象通过 `__proto__` 链接到原型，查找属性时逐级向上，直到 null |
| 深拷贝和浅拷贝的区别？ | 浅拷贝只复制第一层，引用类型仍共享；深拷贝递归复制所有层 |
| 闭包是什么，有什么问题？ | 函数+词法环境，可记住外层变量；问题：持有引用可能导致内存泄漏 |
| this 指向如何确定？ | new > call/apply/bind > obj.fn() > 全局；箭头函数继承外层词法 this |
| Promise 状态有哪些？ | pending/fulfilled/rejected，状态不可逆；all/allSettled/race/any |
| async/await 原理？ | 基于 Promise + Generator；await 将后续放入微任务队列 |
| 事件委托是什么？ | 将子元素事件监听委托给父元素，利用事件冒泡，减少监听器，支持动态元素 |
| 防抖和节流的区别？ | 防抖：停止触发后 n 毫秒执行（搜索）；节流：单位时间只执行一次（滚动）|
| var/let/const 区别？ | var：函数作用域+变量提升；let：块级作用域+TDZ；const：同 let 但不可重赋值 |
| 垃圾回收机制？ | 标记-清除为主（V8 分代：新生代 Scavenge，老生代标记整理），避免内存泄漏 |
